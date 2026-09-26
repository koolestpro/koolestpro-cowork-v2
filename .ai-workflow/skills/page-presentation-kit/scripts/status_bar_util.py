"""
status_bar_util.py — shared helper for compositing the reusable mobile
status bar onto phone mockups. Used by BOTH frame_video.py (video framing)
and build_device_still.py (still framing) so the placement math and variant-
picking logic live in one place.

DESIGN HISTORY:

v1 (2026-07-29 AM) — painted the status bar directly on top of whatever
screen content already filled the whole screen rect. Collided with a page's
own header text (confirmed live: "9KURA41").

v2 (2026-07-29 AM, same day) — fixed the collision by reserving a strip
below the notch and pushing content down to make room. Ridwan's follow-up:
that's not where a real phone's status bar sits — on a real phone the time
and icons are AT THE SAME HEIGHT AS THE NOTCH/CAMERA, flanking it left and
right, not in a separate row underneath it.

v3 (this version) — the status bar now renders IN the actual notch-flanking
area: the two narrow transparent slivers in assets/frames/iphone-frame.png
immediately beside the notch (calibrated below via a live alpha-channel
scan, not guessed). This is a genuinely better fix than v2, not just a
repositioning — because that flanking area sits ABOVE where the screen
content rectangle starts (y=59 in the 450x974 native frame), there is zero
overlap with page content by construction. No reserved strip, no pushed-
down content, no possible collision — content fills the full screen rect
exactly like before any of this started.

The flanking slivers are filled with a color sampled from the content's own
top edge (so it reads as a seamless "wraparound" of the page's own header
color, not a visible seam or a mismatched patch — this is the "colour that
will match or complement whatever image we are doing" Ridwan asked for),
and the dark/light icon variant is auto-picked from that same sampled color.
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

FRAMES_DIR = Path(__file__).resolve().parents[4] / "assets" / "frames"
# .ai-workflow/skills/page-presentation-kit/scripts -> up 4 -> project root

# Calibrated 2026-07-29 by scanning assets/frames/iphone-frame.png's alpha
# channel row-by-row (450x974 native canvas). The notch's transparent cutout
# widens from top (~y20) to where it merges into the full screen rect
# (y=59). Two constants describe it:
#   NOTCH_FILL_Y_RANGE — rows to scan/fill when building the flank-fill mask
#   NOTCH_ICON_SAFE_L / _R — a conservative fixed rectangle, valid at every
#     row in that range, safe to place icon chips in without ever touching
#     the notch or the opaque bezel (found by intersecting the transparent
#     run at every row in the range — the tightest row wins).
NOTCH_FILL_Y_RANGE = (20, 59)
NOTCH_ICON_SAFE_L = (41, 35, 108, 57)   # x0,y0,x1,y1 — left flank
NOTCH_ICON_SAFE_R = (342, 35, 409, 57)  # x0,y0,x1,y1 — right flank


def compute_flank_mask(bezel_img):
    """Scan the bezel's alpha channel over NOTCH_FILL_Y_RANGE and return a
    single-channel 'L' mask (255 = fill this pixel) covering ONLY the two
    transparent slivers immediately beside the notch — explicitly excluding
    the outer rounded-corner cutouts (which touch the image's left/right
    edges and must stay see-through to the canvas background behind the
    phone, not be filled in)."""
    arr = np.asarray(bezel_img.convert("RGBA"))
    h, w = arr.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    y0, y1 = NOTCH_FILL_Y_RANGE
    for y in range(y0, min(y1, h)):
        row = arr[y, :, 3] < 10
        xs = np.where(row)[0]
        if len(xs) == 0:
            continue
        runs = []
        start = xs[0]
        prev = xs[0]
        for x in xs[1:]:
            if x - prev > 1:
                runs.append((start, prev))
                start = x
            prev = x
        runs.append((start, prev))
        # keep only runs that DON'T touch the outer edges (those are the
        # rounded-corner cutouts, not the notch flanks)
        inner = [r for r in runs if r[0] > 15 and r[1] < w - 15]
        for s, e in inner:
            mask[y, s:e + 1] = 255
    return Image.fromarray(mask, mode="L")


def sample_top_edge_color(img, strip_frac=0.02):
    """Median RGB of a thin strip at the very top of `img`.

    FIXED 2026-09-12: this used to return the MEAN of the strip, which
    included any thin white text sitting in the page's own top bar (e.g.
    "Free Shipping on Orders $90+ | ..."). That dragged the fill colour
    lighter than the bar itself, so the notch-flanking status bar painted a
    visibly brighter band above the header. Median is robust to that sparse
    text and returns the bar's true background colour."""
    img = img.convert("RGB")
    w, h = img.size
    strip_h = max(1, int(h * strip_frac))
    region = np.asarray(img.crop((0, 0, w, strip_h))).reshape(-1, 3)
    r, g, b = np.median(region, axis=0)
    return int(round(r)), int(round(g)), int(round(b))


def variant_from_color(rgb):
    r, g, b = rgb
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return "dark" if brightness > 128 else "light"


def _fit_into(chip, box_w, box_h):
    """Scale `chip` (RGBA) to fit inside box_w x box_h preserving aspect,
    centered — returns (resized_chip, offset_x, offset_y) relative to the
    box's own top-left."""
    scale = min(box_w / chip.width, box_h / chip.height)
    new_w, new_h = max(1, round(chip.width * scale)), max(1, round(chip.height * scale))
    resized = chip.resize((new_w, new_h), Image.LANCZOS)
    return resized, (box_w - new_w) / 2, (box_h - new_h) / 2


def build_notch_status_layer(bezel_img, fill_color, variant="auto"):
    """Returns (layer, variant_used) — an RGBA image the same size as
    `bezel_img`, transparent everywhere except the notch-flanking slivers,
    which are filled with `fill_color` and carry the time (left) / icons
    (right) chips. Composite this UNDER the bezel image (so the bezel's
    opaque notch/corners still mask correctly) and OVER the actual screen
    content (which occupies y>=59 and never overlaps this layer)."""
    if variant == "auto":
        variant = variant_from_color(fill_color)

    w, h = bezel_img.size
    mask = compute_flank_mask(bezel_img)

    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fill = Image.new("RGBA", (w, h), fill_color + (255,))
    layer.paste(fill, (0, 0), mask)

    time_chip = Image.open(FRAMES_DIR / f"status-bar-time-{variant}.png").convert("RGBA")
    icons_chip = Image.open(FRAMES_DIR / f"status-bar-icons-{variant}.png").convert("RGBA")

    lx0, ly0, lx1, ly1 = NOTCH_ICON_SAFE_L
    rx0, ry0, rx1, ry1 = NOTCH_ICON_SAFE_R

    resized, ox, oy = _fit_into(time_chip, lx1 - lx0, ly1 - ly0)
    layer.alpha_composite(resized, (round(lx0 + ox), round(ly0 + oy)))

    resized, ox, oy = _fit_into(icons_chip, rx1 - rx0, ry1 - ry0)
    layer.alpha_composite(resized, (round(rx0 + ox), round(ry0 + oy)))

    return layer, variant


def sample_variant_and_color_from_file(image_path):
    img = Image.open(image_path).convert("RGB")
    color = sample_top_edge_color(img)
    return variant_from_color(color), color

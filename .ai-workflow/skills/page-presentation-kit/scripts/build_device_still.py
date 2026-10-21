"""
build_device_still.py — canonical script for the still-image device mockups
(cover.png, {slug}-preview.png) that this project's SKILL.md previously
described as "Playwright/PIL compositing at the calibrated screen-region
coordinates... not via frame_video.py (that's video-only)" without actually
naming a reusable script for it — every run redid this ad hoc. This is that
script, going forward.

Reuses frame_video.py's calibrated placement math (compute_placement,
MACBOOK_NATIVE/SCREEN, IPHONE_NATIVE/SCREEN, make_background) so stills and
video stay visually consistent, and status_bar_util.py for the mobile status
bar overlay (added 2026-07-29 — see that module's docstring for why).

STYLE PRESETS (added 2026-07-29 PM, Ridwan's 3rd follow-up same day). Ridwan
shared two reference sprite sheets ("Double Screen Template.png" / "Triple
Screen Template.png", 8 arrangement styles each, saved at the project root)
showing the phone-mockup arrangement GEOMETRIES he wants this skill to keep
reusing — not the reference images themselves (they carry unrelated brand
content), just their positional/rotation/scale patterns. His instruction:
always build multi-phone previews using one of those 16 styles, freely using
either 2 or 3 phones, on either the koolestpro brand gradient or a plain
color — but ALWAYS keep the notch-flanking status bar design. STYLE_PRESETS
below distills the 16 reference tiles down to 8 reusable geometric
archetypes (some tiles are minor variations of the same underlying pattern):

  flat_even_2      <- reference "double" tile 1          (equal-size flat pair)
  flat_stagger_2   <- reference "double" tiles 2,5,6,8    (scale/height staggered flat pair)
  crossed_2        <- reference "double" tile 3           (angled pair, crossing, moderate scale)
  crossed_2_large  <- reference "double" tiles 4,7        (angled pair, crossing, large/tighter scale)
  flat_even_3      <- reference "triple" tile 1           (equal-size flat row of 3)
  flat_arc_3       <- reference "triple" tiles 2,3,5,6    (arc/stagger of 3, center prominent)
  fanned_stack_3   <- reference "triple" tiles 7,8        (overlapping card-fan stack of 3)
  angled_trio      <- this skill's original hardcoded 3-phone layout, kept as
                       its own selectable preset (also a valid reference-
                       matching arrangement) rather than discarded
  flat_packed_2    <- added 2026-07-31 PM, a 3rd reference image (flat, even,
                       big, tightly packed, "taking almost all the image
                       space") — flat_even_2's scale/spacing read too small
                       and too spread out against this new bar. Prefer this
                       over flat_even_2 whenever a big fill-the-frame look is
                       wanted; pass a narrower --width for a true packed look
                       since 2 phones can't fill a wide canvas's width alone.
  flat_packed_3    <- same fix, 3-phone case. Prefer over flat_even_3 by
                       default now — scale ~1.0 (92% of canvas height) with
                       tight cx spacing (~7-8% gap vs flat_even_3's ~13-14%).
  flat_packed_4    <- the 9th style, added 2026-09-12 for the Monthly Template
                       Showcase. 4 phones in a packed row (home hero / mid
                       section / range / product). scale 0.88 on the 2880x1800
                       canvas so 4 phones fit without clipping.

Three build modes:
  single   — one device (laptop or mobile), screenshot inside, on the brand
             gradient (or plain-color) background.
  cover    — laptop + phone together (the "{slug} cover.png" deliverable).
  preview  — 2 to 4 phone frames per a chosen STYLE_PRESET, each usually at a
             different scroll depth (the "{slug}-preview.png" deliverable).

Usage:
  python3 build_device_still.py single --device mobile --screenshot shot.png --output out.png --width 1440 --height 1080
  python3 build_device_still.py cover --screenshot-laptop desktop.png --screenshot-mobile mobile.png --output cover.png --width 1440 --height 1080
  python3 build_device_still.py preview --style flat_stagger_2 --screenshot shot1.png --screenshot shot2.png --output preview.png --width 2880 --height 1800
  python3 build_device_still.py preview --style fanned_stack_3 --screenshot shot1.png --screenshot shot2.png --screenshot shot3.png --output preview.png
  python3 build_device_still.py preview --style flat_packed_4 --screenshot shot1.png --screenshot shot2.png --screenshot shot3.png --screenshot shot4.png --output preview4.png
  python3 build_device_still.py preview --list-styles
"""

import argparse
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

import status_bar_util as sbu
from frame_video import (
    FRAMES_DIR, MACBOOK_NATIVE, MACBOOK_SCREEN, IPHONE_NATIVE, IPHONE_SCREEN,
    make_background, compute_placement, overlap_cover_geometry,
)

# ---------------------------------------------------------------------------
# STYLE_PRESETS — see module docstring for the reference-tile mapping.
# Each phone entry: cx/cy = center position as a fraction of canvas size,
# scale = fraction of the max phone height the canvas allows, rotate = degrees
# (matches _paste_scaled's rotate_deg), z = paint order (lower first).
# ---------------------------------------------------------------------------
# FIXED 2026-07-31 (Ridwan reviewed the first halos_pdp-01 run against his own
# reference tiles and flagged this directly): every preset below used to vary
# `scale` per phone (e.g. a bigger "hero" phone in the center of an arc, or a
# bigger front phone in a fan stack). Cropping the actual reference sprite
# sheets ("Double Screen Template.png" / "Triple Screen Template.png") into
# their 16 individual tiles and inspecting them directly shows every single
# tile uses IDENTICAL phone size within that arrangement — only position
# (cx/cy offset, overlap) and rotation vary, never scale. Every preset here now
# uses one shared `scale` per preset, not a per-phone value.
STYLE_PRESETS = {
    "flat_even_2": {
        "count": 2,
        "scale": 0.86,
        "phones": [
            {"cx": 0.30, "cy": 0.50, "rotate": 0, "z": 0},
            {"cx": 0.70, "cy": 0.50, "rotate": 0, "z": 1},
        ],
    },
    "flat_stagger_2": {
        "count": 2,
        "scale": 0.86,
        "phones": [
            {"cx": 0.33, "cy": 0.60, "rotate": 0, "z": 1},
            {"cx": 0.70, "cy": 0.40, "rotate": 0, "z": 0},
        ],
    },
    "crossed_2": {
        "count": 2,
        "scale": 0.86,
        "phones": [
            {"cx": 0.40, "cy": 0.48, "rotate": -9, "z": 0},
            {"cx": 0.60, "cy": 0.52, "rotate": 9, "z": 1},
        ],
    },
    "crossed_2_large": {
        "count": 2,
        "scale": 1.05,
        "phones": [
            {"cx": 0.37, "cy": 0.50, "rotate": -8, "z": 0},
            {"cx": 0.63, "cy": 0.50, "rotate": 8, "z": 1},
        ],
    },
    "flat_even_3": {
        "count": 3,
        "scale": 0.62,
        "phones": [
            {"cx": 0.20, "cy": 0.50, "rotate": 0, "z": 0},
            {"cx": 0.50, "cy": 0.50, "rotate": 0, "z": 1},
            {"cx": 0.80, "cy": 0.50, "rotate": 0, "z": 0},
        ],
    },
    "flat_arc_3": {
        "count": 3,
        "scale": 0.62,
        "phones": [
            {"cx": 0.22, "cy": 0.44, "rotate": 0, "z": 0},
            {"cx": 0.50, "cy": 0.56, "rotate": 0, "z": 2},
            {"cx": 0.78, "cy": 0.44, "rotate": 0, "z": 1},
        ],
    },
    "fanned_stack_3": {
        "count": 3,
        "scale": 0.62,
        "phones": [
            {"cx": 0.41, "cy": 0.52, "rotate": -7, "z": 0},
            {"cx": 0.50, "cy": 0.50, "rotate": 0, "z": 2},
            {"cx": 0.59, "cy": 0.52, "rotate": 7, "z": 1},
        ],
    },
    "angled_trio": {
        "count": 3,
        "scale": 0.66,
        "phones": [
            {"cx": 0.24, "cy": 0.52, "rotate": -10, "z": 0},
            {"cx": 0.50, "cy": 0.54, "rotate": 0, "z": 2},
            {"cx": 0.77, "cy": 0.50, "rotate": 10, "z": 1},
        ],
    },
    # FIXED 2026-07-31 PM: Ridwan shared a THIRD reference image (3 flat, even
    # phones, no rotation) and flagged that the existing presets read too
    # small and too spread out — "bigger and closely packed... taking almost
    # all the image space." Measured against the 2880x1800 canvas this
    # project's CLAUDE.md documents as the correct `{slug}-preview.png`
    # dimension: flat_even_3's scale=0.62 only fills ~57% of canvas height
    # and leaves a ~13.5%-of-width gap between adjacent phones — nowhere
    # near "almost all the image space." These two new presets keep the same
    # 2880x1800 canvas (that dimension was already correct, the phones
    # inside it were just too small/spread out) but push scale to ~1.0 (92%
    # of canvas height, the same ceiling every other preset's base_scale
    # already uses) and tighten cx spacing so the gap between phones drops
    # to ~7-8% of canvas width instead of ~13-14%. Prefer these over
    # flat_even_2/flat_even_3 whenever "big, fills the frame" is the goal —
    # flat_even_2/3 are kept only for a deliberately smaller/airier look.
    # FIXED 2026-07-31 PM (2nd follow-up same day): the first flat_packed_2/3
    # cut had the spacing backwards — thin outer margins (~2.5%) and WIDE
    # gaps between adjacent phones (~7.6%). Ridwan's exact correction: "space
    # around, or narrow gap between the devices, and then some space at the
    # right and left" — i.e. the reverse. Outer margins are now the bigger
    # number, inter-phone gaps are the thin one (roughly margin ~7-7.5% vs
    # gap ~2.5-3% for the 3-phone case). Phone scale itself is unchanged
    # (still maxed at ~92% of canvas height) — only how the leftover width is
    # distributed changed.
    #
    # Note on flat_packed_2's numbers: build_preview's scale is height-driven
    # (base_scale = canvas_h*0.92 / 974) regardless of phone count, so on a
    # wide 2880-width canvas 2 phones alone can't consume as much width as 3
    # can without exceeding the height ceiling and clipping top/bottom. For a
    # genuinely "packed" 2-phone look, pass a narrower --width at call time
    # (CLAUDE.md's own preview.png spec already says "or narrower for a
    # 2-phone style") rather than expecting this preset alone to fill a full
    # 2880-wide canvas — the cx spacing below is tuned to look packed at
    # whatever width is passed in, not tied to one fixed canvas size.
    "flat_packed_2": {
        "count": 2,
        "scale": 0.95,
        "phones": [
            {"cx": 0.326, "cy": 0.50, "rotate": 0, "z": 0},
            {"cx": 0.674, "cy": 0.50, "rotate": 0, "z": 1},
        ],
    },
    "flat_packed_3": {
        "count": 3,
        "scale": 1.0,
        "phones": [
            {"cx": 0.208, "cy": 0.50, "rotate": 0, "z": 0},
            {"cx": 0.500, "cy": 0.50, "rotate": 0, "z": 1},
            {"cx": 0.792, "cy": 0.50, "rotate": 0, "z": 0},
        ],
    },
    # flat_packed_4 <- the 9th style, added 2026-09-12 for the Monthly Template
    # Showcase (a 4-screen strip: e.g. home hero, a mid-page section, range,
    # product). Same "outer margins bigger than inter-phone gaps" rule as
    # flat_packed_2/3 — because 4 phones can't sit at flat_packed_3's scale=1.0
    # on a 2880-wide canvas without clipping, scale drops to 0.88 (phone width
    # ~673px, outer margin ~55px vs ~25px gaps). Anything narrower than
    # ~2400px will make the phones small; keep the 2880x1800 canvas.
    "flat_packed_4": {
        "count": 4,
        "scale": 0.88,
        "phones": [
            {"cx": 0.136, "cy": 0.50, "rotate": 0, "z": 0},
            {"cx": 0.379, "cy": 0.50, "rotate": 0, "z": 1},
            {"cx": 0.621, "cy": 0.50, "rotate": 0, "z": 2},
            {"cx": 0.864, "cy": 0.50, "rotate": 0, "z": 3},
        ],
    },
    # fanned_stack_4 <- the 10th style, added 2026-09-12 for the MONTHLY recap
    # (Ridwan's "HIGH CONVERTING PAGES" reference: four builds overlapping in a
    # fanned, angled stack). RETUNED 2026-09-13: the first cut spread the phones
    # too wide and small (cluster aspect ~1.6), so on a square recap sheet the
    # phones filled the width but left a big empty band at the bottom. Pulled the
    # cx spread in and raised the scale so the cluster is taller (~1.14 aspect),
    # which fills a square frame properly. Phones overlap deliberately.
    "fanned_stack_4": {
        "count": 4,
        "scale": 0.96,
        "phones": [
            {"cx": 0.345, "cy": 0.505, "rotate": -12, "z": 0},
            {"cx": 0.450, "cy": 0.500, "rotate": -4, "z": 1},
            {"cx": 0.550, "cy": 0.500, "rotate": 4, "z": 2},
            {"cx": 0.655, "cy": 0.505, "rotate": 12, "z": 3},
        ],
    },
}

# Reference lavender canvas color sampled directly from Ridwan's own
# "Double Screen Template.png" tile 1 (row 200, x 150-1700 averaged ~
# rgb(220,225,238)) — offered as the default --bg-color for --bg-mode plain,
# since it's a real color he's already shown us working, not a guess.
REFERENCE_PLAIN_BG = (222, 226, 239)


def _style_default_for_count(count):
    for name, spec in STYLE_PRESETS.items():
        if spec["count"] == count:
            return name
    raise SystemExit(f"No style preset defined for {count} phones")


def _fit_screenshot(screenshot_path, size):
    """Cover-fit a screenshot into `size`, anchored to the TOP (hero content
    matters more than whatever's cut off at the bottom of a taller shot)."""
    img = Image.open(screenshot_path).convert("RGB")
    return ImageOps.fit(img, size, method=Image.LANCZOS, centering=(0.5, 0.0))


def _make_canvas_background(canvas_w, canvas_h, bg_mode, bg_color, tmp_dir):
    bg_path = f"{tmp_dir}/bg.png"
    if bg_mode == "transparent":
        # Added 2026-09-13 for the Monthly Build Recap: Ridwan wants ONE
        # continuous background across the headline AND the phones, so the
        # preview strips must not carry their own background (the gradient
        # strip used to leave visible horizontal bands above/below the
        # phones). Transparent here + a single backing layer in the recap
        # HTML gives the reference's seamless dark + central-glow look.
        return Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    if bg_mode == "plain":
        color = bg_color or REFERENCE_PLAIN_BG
        Image.new("RGB", (canvas_w, canvas_h), color).save(bg_path)
    else:
        make_background(canvas_w, canvas_h, bg_path)
    return Image.open(bg_path).convert("RGBA")


def compose_laptop_flat(screenshot_path):
    """Returns an RGBA image at MACBOOK_NATIVE size: screenshot inside the
    calibrated screen rect, bezel on top. No status bar (desktop only)."""
    canvas = Image.new("RGBA", MACBOOK_NATIVE, (0, 0, 0, 0))
    x0, y0, x1, y1 = MACBOOK_SCREEN
    shot = _fit_screenshot(screenshot_path, (x1 - x0, y1 - y0)).convert("RGBA")
    canvas.alpha_composite(shot, (x0, y0))
    bezel = Image.open(FRAMES_DIR / "macbook-pro.png").convert("RGBA")
    if bezel.size != MACBOOK_NATIVE:
        bezel = bezel.resize(MACBOOK_NATIVE, Image.LANCZOS)
    canvas.alpha_composite(bezel, (0, 0))
    return canvas


def compose_mobile_flat(screenshot_path, status_bar="auto"):
    """Returns an RGBA image at IPHONE_NATIVE size: screenshot fills the
    FULL screen rect (no reserved strip — see status_bar_util.py's v3
    design note), the status bar renders in the actual notch-flanking
    slivers (same height as the camera, left/right of it, like a real
    phone), bezel on top last so its opaque notch/corners mask correctly.
    Returns (image, variant_used)."""
    canvas = Image.new("RGBA", IPHONE_NATIVE, (0, 0, 0, 0))
    x0, y0, x1, y1 = IPHONE_SCREEN
    screen_w, screen_h = x1 - x0, y1 - y0

    shot = _fit_screenshot(screenshot_path, (screen_w, screen_h))
    canvas.alpha_composite(shot.convert("RGBA"), (x0, y0))

    bezel = Image.open(FRAMES_DIR / "iphone-frame.png").convert("RGBA")
    if bezel.size != IPHONE_NATIVE:
        bezel = bezel.resize(IPHONE_NATIVE, Image.LANCZOS)

    variant = None
    if status_bar != "none":
        top_color = sbu.sample_top_edge_color(shot)
        notch_layer, variant = sbu.build_notch_status_layer(bezel, top_color, variant=status_bar)
        canvas.alpha_composite(notch_layer, (0, 0))

    canvas.alpha_composite(bezel, (0, 0))
    return canvas, variant


def _paste_scaled(base, flat_img, frame_x, frame_y, frame_w, frame_h, rotate_deg=0):
    resized = flat_img.resize((round(frame_w), round(frame_h)), Image.LANCZOS)
    if rotate_deg:
        resized = resized.rotate(rotate_deg, expand=True, resample=Image.BICUBIC)
        frame_x -= (resized.width - round(frame_w)) / 2
        frame_y -= (resized.height - round(frame_h)) / 2
    base.alpha_composite(resized, (round(frame_x), round(frame_y)))


def build_single(device, screenshot, output, canvas_w, canvas_h, status_bar="auto",
                  bg_mode="gradient", bg_color=None):
    tmp_dir = tempfile.mkdtemp(prefix="bds_")
    base = _make_canvas_background(canvas_w, canvas_h, bg_mode, bg_color, tmp_dir)

    if device == "laptop":
        flat = compose_laptop_flat(screenshot)
        p = compute_placement(canvas_w, canvas_h, MACBOOK_NATIVE, MACBOOK_SCREEN, margin_frac=0.09)
        variant = None
    else:
        flat, variant = compose_mobile_flat(screenshot, status_bar=status_bar)
        p = compute_placement(canvas_w, canvas_h, IPHONE_NATIVE, IPHONE_SCREEN, margin_frac=0.12)

    _paste_scaled(base, flat, p["frame_x"], p["frame_y"], p["frame_w"], p["frame_h"])
    base.convert("RGB").save(output)
    print(f"Saved: {output} ({canvas_w}x{canvas_h})" + (f" [status bar: {variant}]" if variant else ""))


def build_cover(screenshot_laptop, screenshot_mobile, output, canvas_w=1440, canvas_h=1080,
                 status_bar="auto", bg_mode="gradient", bg_color=None):
    """Laptop + phone, phone overlapping the laptop's right side and drawn on
    top (COVER LAYOUT v3, 2026-10-10). Geometry is shared with
    frame_video.build_cover via overlap_cover_geometry so the still and the
    video cover always match."""
    tmp_dir = tempfile.mkdtemp(prefix="bds_")
    base = _make_canvas_background(canvas_w, canvas_h, bg_mode, bg_color, tmp_dir)
    lp, pp = overlap_cover_geometry(canvas_w, canvas_h)
    laptop_flat = compose_laptop_flat(screenshot_laptop)
    mobile_flat, variant = compose_mobile_flat(screenshot_mobile, status_bar=status_bar)
    _paste_scaled(base, laptop_flat, lp["frame_x"], lp["frame_y"], lp["frame_w"], lp["frame_h"])
    _paste_scaled(base, mobile_flat, pp["frame_x"], pp["frame_y"], pp["frame_w"], pp["frame_h"])
    base.convert("RGB").save(output)
    print(f"Saved: {output} ({canvas_w}x{canvas_h}) [status bar: {variant}] [cover layout v3: phone overlaps laptop]")


def build_preview(screenshots, output, canvas_w=2880, canvas_h=1800, status_bar="auto",
                   style=None, bg_mode="gradient", bg_color=None):
    """2 or 3 phone frames arranged per a named STYLE_PRESET (see module
    docstring — these geometries trace back to Ridwan's 16 reference
    arrangement tiles), filling the canvas rather than huddling small phones
    in empty space (the exact complaint about the original rejected attempt
    at this asset)."""
    n = len(screenshots)
    if n not in (2, 3, 4):
        raise SystemExit("preview mode needs 2, 3 or 4 --screenshot values")

    style = style or _style_default_for_count(n)
    if style not in STYLE_PRESETS:
        raise SystemExit(f"Unknown style '{style}'. Choices: {', '.join(STYLE_PRESETS)}")
    spec = STYLE_PRESETS[style]
    if spec["count"] != n:
        raise SystemExit(
            f"Style '{style}' needs {spec['count']} screenshots, got {n}. "
            f"Pick a style with count={n}: "
            f"{', '.join(s for s, v in STYLE_PRESETS.items() if v['count'] == n)}"
        )

    tmp_dir = tempfile.mkdtemp(prefix="bds_")
    base = _make_canvas_background(canvas_w, canvas_h, bg_mode, bg_color, tmp_dir)

    layout = spec["phones"]
    max_h = canvas_h * 0.92
    base_scale = max_h / IPHONE_NATIVE[1]

    variants = []
    ordered = sorted(zip(layout, screenshots), key=lambda t: t[0]["z"])
    for slot, shot in ordered:
        flat, variant = compose_mobile_flat(shot, status_bar=status_bar)
        variants.append(variant)
        # Uniform scale per preset (see STYLE_PRESETS docstring/comment above —
        # every phone within one arrangement is the same size, matching
        # Ridwan's reference tiles; only cx/cy/rotate vary).
        s = base_scale * spec["scale"]
        w, h = IPHONE_NATIVE[0] * s, IPHONE_NATIVE[1] * s
        cx, cy = canvas_w * slot["cx"], canvas_h * slot["cy"]
        _paste_scaled(base, flat, cx - w / 2, cy - h / 2, w, h, rotate_deg=slot["rotate"])

    out = base if bg_mode == "transparent" else base.convert("RGB")
    out.save(output)
    print(f"Saved: {output} ({canvas_w}x{canvas_h}) [style: {style}] [status bars: {variants}]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["single", "cover", "preview"])
    ap.add_argument("--device", choices=["laptop", "mobile"], help="single mode only")
    ap.add_argument("--screenshot", action="append", help="single: one shot. preview: pass 2-4 times.")
    ap.add_argument("--screenshot-laptop", help="cover mode")
    ap.add_argument("--screenshot-mobile", help="cover mode")
    ap.add_argument("--output")
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--status-bar", default="auto", choices=["auto", "dark", "light", "none"])
    ap.add_argument("--style", choices=list(STYLE_PRESETS), help="preview mode only — see --list-styles")
    ap.add_argument("--bg-mode", default="gradient", choices=["gradient", "plain", "transparent"],
                     help="gradient = koolestpro brand orange->purple glow (default); "
                          "plain = flat color, use --bg-color to set it; "
                          "transparent = no background (phones only, for compositing onto a shared sheet)")
    ap.add_argument("--bg-color", help="hex color for --bg-mode plain, e.g. e0e4f0 (default: "
                                        "the lavender sampled from Ridwan's own reference tiles)")
    ap.add_argument("--list-styles", action="store_true", help="print all style presets and exit")
    args = ap.parse_args()

    if args.list_styles:
        for name, spec in STYLE_PRESETS.items():
            print(f"{name}  (count={spec['count']})")
        raise SystemExit(0)

    if not args.output:
        raise SystemExit("--output is required")

    bg_color = None
    if args.bg_color:
        hexs = args.bg_color.lstrip("#")
        bg_color = tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4))

    if args.mode == "single":
        if not args.device or not args.screenshot:
            raise SystemExit("single mode needs --device and --screenshot")
        build_single(args.device, args.screenshot[0], args.output,
                     canvas_w=args.width or 1440, canvas_h=args.height or 1080,
                     status_bar=args.status_bar, bg_mode=args.bg_mode, bg_color=bg_color)
    elif args.mode == "cover":
        if not args.screenshot_laptop or not args.screenshot_mobile:
            raise SystemExit("cover mode needs --screenshot-laptop and --screenshot-mobile")
        build_cover(args.screenshot_laptop, args.screenshot_mobile, args.output,
                    canvas_w=args.width or 1440, canvas_h=args.height or 1080,
                    status_bar=args.status_bar, bg_mode=args.bg_mode, bg_color=bg_color)
    else:
        build_preview(args.screenshot or [], args.output,
                      canvas_w=args.width or 2880, canvas_h=args.height or 1800,
                      status_bar=args.status_bar, style=args.style,
                      bg_mode=args.bg_mode, bg_color=bg_color)

"""
frame_video.py — composite a raw Playwright scroll-capture video into a real,
calibrated device bezel (MacBook / iPhone) on a brand-gradient background,
via ffmpeg. Fixes two confirmed bugs from the first real run
(outputs/templates/kura_hp-01_2026-07-13/):

  1. Only cover.mp4 got a device frame; laptop.mp4/mobile.mp4 shipped as bare,
     unframed screen recordings. This script frames ALL THREE variants.
  2. cover.mp4's frame used some ad hoc placement that clipped the phone off
     the right edge and wasn't centered. This script computes placement from
     the same calibrated screen-rect coordinates used for the approved still
     images (assets/frames/*), so video and stills stay visually consistent.

Requires assets/frames/macbook-pro.png / macbook-pro-alt.png to exist with a
real transparent (alpha=0) cutout in the screen region — these are pre-
rendered + alpha-punched from the source SVGs (see render step in this
project's build log if they need regenerating). iphone-frame.png already has
a genuine alpha cutout from its source PNG, no punching needed.

MOBILE STATUS BAR (added 2026-07-29, revised same day after Ridwan's
follow-up). Both `mobile` and `cover` modes composite a status bar onto the
phone — but it now renders IN THE ACTUAL NOTCH-FLANKING SLIVERS (same height
as the camera, left/right of it — see status_bar_util.py's v3 design note),
not a reserved strip below the notch like the first attempt. Because that
flanking area sits entirely above where the video's screen rect starts, the
video is no longer scaled down or offset to make room for anything — it
fills the full screen rect exactly as before any of this started. The
dark/light icon variant + the flank's fill color are both auto-picked per
run by sampling the actual video's own top-edge color (ffmpeg frame grab +
PIL) — not hardcoded — so a future brand with a dark hero doesn't get
invisible icons. Pass --status-bar dark|light to override, or `none` to
skip it (e.g. re-rendering a debug clip).

Usage:
  # single device, solo
  python3 frame_video.py laptop --video raw_laptop.mp4 --output "{slug} laptop.mp4"
  python3 frame_video.py mobile --video raw_mobile.mp4 --output "{slug} mobile.mp4"

  # dual device (cover) — needs both raw clips, same duration
  python3 frame_video.py cover --video raw_laptop.mp4 --video2 raw_mobile.mp4 --output "{slug} cover.mp4"
"""

import argparse
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw
import status_bar_util as sbu

FRAMES_DIR = Path(__file__).resolve().parents[4] / "assets" / "frames"
# ^ .ai-workflow/skills/page-presentation-kit/scripts -> up 4 -> project root

MACBOOK_NATIVE = (2011, 1171)
MACBOOK_SCREEN = (199, 74, 1812, 1048)   # x0,y0,x1,y1
IPHONE_NATIVE = (450, 974)
IPHONE_SCREEN = (22, 59, 428, 949)

# Brand gradient background — same palette as the approved cover.png/preview.png
# stills (#FF9500 -> #7B2FBE radial glow on near-black).
BG_TOP_LEFT = (255, 149, 0)      # #FF9500
BG_BOTTOM_RIGHT = (123, 47, 190)  # #7B2FBE
BG_BASE = (8, 8, 10)


def make_background(w, h, out_path):
    base = Image.new("RGB", (w, h), BG_BASE)
    glow1 = Image.new("RGB", (w, h), BG_BASE)
    d = ImageDraw.Draw(glow1, "RGBA")
    r1 = int(max(w, h) * 0.6)
    d.ellipse([-r1 * 0.4, -r1 * 0.4, r1 * 0.8, r1 * 0.8], fill=BG_TOP_LEFT + (60,))
    glow1 = glow1.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(120))
    base = Image.alpha_composite(base.convert("RGBA"), glow1.convert("RGBA"))

    glow2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(glow2)
    r2 = int(max(w, h) * 0.65)
    d2.ellipse([w - r2 * 0.75, h - r2 * 0.75, w + r2 * 0.3, h + r2 * 0.3], fill=BG_BOTTOM_RIGHT + (55,))
    glow2 = glow2.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(130))
    base = Image.alpha_composite(base, glow2)

    base.convert("RGB").save(out_path)


def compute_placement(canvas_w, canvas_h, native_wh, screen_box, margin_frac=0.09,
                       anchor="center", x_bias=0, y_bias=0):
    native_w, native_h = native_wh
    max_w = canvas_w * (1 - 2 * margin_frac)
    max_h = canvas_h * (1 - 2 * margin_frac)
    scale = min(max_w / native_w, max_h / native_h)
    frame_w, frame_h = native_w * scale, native_h * scale
    frame_x = (canvas_w - frame_w) / 2 + x_bias
    frame_y = (canvas_h - frame_h) / 2 + y_bias
    sx0, sy0, sx1, sy1 = screen_box
    return {
        "scale": scale,
        "frame_x": frame_x, "frame_y": frame_y, "frame_w": frame_w, "frame_h": frame_h,
        "screen_x": frame_x + sx0 * scale, "screen_y": frame_y + sy0 * scale,
        "screen_w": (sx1 - sx0) * scale, "screen_h": (sy1 - sy0) * scale,
    }


def sample_video_top_color(video_path, tmp_dir):
    """Grab an early frame from the raw clip and sample its top-edge color —
    used both to auto-pick the status bar icon variant (dark icons on a
    light top-of-screen, white on a dark one) and to fill the reserved
    status-bar strip so it reads as a seamless continuation of the page's
    own header rather than a visible seam. Falls back to a mid-grey / 'dark'
    if the grab fails for any reason, rather than blocking the whole run."""
    frame_png = f"{tmp_dir}/statusbar_sample.png"
    try:
        # Sample a bit into the clip (not frame 0) — scroll_video.py settles
        # 1200ms after page load before the scroll animation even starts, so
        # anything earlier than that risks sampling a blank/loading frame
        # instead of real rendered content (confirmed on a page with its own
        # intro splash animation during testing, 2026-07-29).
        subprocess.run(
            ["ffmpeg", "-y", "-ss", "1.4", "-i", video_path, "-vframes", "1", frame_png],
            check=True, capture_output=True,
        )
        return sbu.sample_variant_and_color_from_file(frame_png)
    except Exception:
        return "dark", (230, 230, 230)


def render_frame_png(canvas_w, canvas_h, placements, out_path):
    """Render just the frame-chrome layer (transparent everywhere except
    bezels + mobile notch-flank status bars) at full canvas size, so ffmpeg
    only needs one overlay per device.

    A placement with "status_bar_color"/"status_bar_variant" keys gets the
    notch-flank status layer (status_bar_util.build_notch_status_layer)
    built in the bezel's own NATIVE coordinate space, then resized by the
    exact same scale/position as the bezel image itself so the two stay
    pixel-aligned — composited BEFORE the (scaled) bezel goes on top, same
    ordering the still-image path uses."""
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    for p in placements:
        frame_img = Image.open(p["asset"]).convert("RGBA")

        color = p.get("status_bar_color")
        if color:
            notch_layer, _ = sbu.build_notch_status_layer(
                frame_img, color, variant=p.get("status_bar_variant", "auto")
            )
            resized_layer = notch_layer.resize((round(p["frame_w"]), round(p["frame_h"])), Image.LANCZOS)
            canvas.alpha_composite(resized_layer, (round(p["frame_x"]), round(p["frame_y"])))

        resized = frame_img.resize((round(p["frame_w"]), round(p["frame_h"])), Image.LANCZOS)
        canvas.alpha_composite(resized, (round(p["frame_x"]), round(p["frame_y"])))
    canvas.save(out_path)


def ffmpeg_compose(bg_png, frame_png, video_specs, out_path, canvas_w, canvas_h, duration=None):
    """video_specs: list of dicts with keys video, x, y, w, h"""
    inputs = ["-i", bg_png]
    for v in video_specs:
        inputs += ["-i", v["video"]]
    inputs += ["-i", frame_png]

    filter_parts = []
    last = "0:v"
    for i, v in enumerate(video_specs):
        vin = f"{i+1}:v"
        scaled = f"vid{i}"
        filter_parts.append(
            f"[{vin}]scale={round(v['w'])}:{round(v['h'])}:force_original_aspect_ratio=increase,"
            f"crop={round(v['w'])}:{round(v['h'])}[{scaled}]"
        )
        nxt = f"lay{i}"
        filter_parts.append(f"[{last}][{scaled}]overlay={round(v['x'])}:{round(v['y'])}[{nxt}]")
        last = nxt

    frame_idx = len(video_specs) + 1
    filter_parts.append(f"[{last}][{frame_idx}:v]overlay=0:0:format=auto[outv]")

    filter_complex = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    ]
    if duration:
        cmd += ["-t", str(duration)]
    cmd += [out_path]
    subprocess.run(cmd, check=True, capture_output=True)


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def build_laptop_or_mobile(mode, video, output, canvas_w, canvas_h, status_bar="auto"):
    tmp = tempfile.mkdtemp(prefix="fv_")
    bg_png = f"{tmp}/bg.png"
    frame_png = f"{tmp}/frame.png"
    make_background(canvas_w, canvas_h, bg_png)

    if mode == "laptop":
        asset = str(FRAMES_DIR / "macbook-pro.png")
        placement = compute_placement(canvas_w, canvas_h, MACBOOK_NATIVE, MACBOOK_SCREEN, margin_frac=0.08)
    else:
        asset = str(FRAMES_DIR / "iphone-frame.png")
        placement = compute_placement(canvas_w, canvas_h, IPHONE_NATIVE, IPHONE_SCREEN, margin_frac=0.12)
        if status_bar != "none":
            variant, color = sample_video_top_color(video, tmp) if status_bar == "auto" else (status_bar, (230, 230, 230))
            placement["status_bar_color"] = color
            placement["status_bar_variant"] = variant
            print(f"[status-bar] mobile clip -> variant={variant} (notch-flank placement)")

    placement["asset"] = asset
    render_frame_png(canvas_w, canvas_h, [placement], frame_png)

    video_specs = [{
        "video": video, "x": placement["screen_x"], "y": placement["screen_y"],
        "w": placement["screen_w"], "h": placement["screen_h"],
    }]
    ffmpeg_compose(bg_png, frame_png, video_specs, output, canvas_w, canvas_h)
    print(f"Saved: {output} ({probe_duration(output):.1f}s)")


def build_cover(video_laptop, video_mobile, output, canvas_w=960, canvas_h=720, status_bar="auto"):
    """FIXED 2026-07-21 (Ridwan flagged the phone bezel visibly cutting across
    the laptop's screen content in kura_hp-01 cover.mp4). The old formula
    deliberately overlapped the phone onto the laptop's lower-right corner
    (`phone_x = laptop right edge - phone_w*0.62`) to avoid the phone bleeding
    off-canvas — but that overlap zone reached well above the laptop's screen
    BOTTOM edge, so the phone bezel sat on top of live screen content, not just
    the laptop's base/keyboard chrome. Root cause: side-by-side (non-overlapping)
    placement was never actually attempted — there IS enough width for it once
    the laptop's margin is tuned to leave a real gap, it just wasn't computed.
    Fix: laptop sized/positioned to leave a genuine right-hand gap, phone
    scaled to fit that gap (width-constrained, capped by canvas height too) and
    placed fully beside the laptop with a visible margin. Zero overlap by
    construction — no clamping-back-into-overlap possible."""
    tmp = tempfile.mkdtemp(prefix="fv_")
    bg_png = f"{tmp}/bg.png"
    frame_png = f"{tmp}/frame.png"
    make_background(canvas_w, canvas_h, bg_png)

    left_margin = canvas_w * 0.03
    gap = canvas_w * 0.025
    right_margin = canvas_w * 0.02

    laptop_p = compute_placement(
        canvas_w, canvas_h, MACBOOK_NATIVE, MACBOOK_SCREEN,
        margin_frac=0.11, x_bias=0, y_bias=-canvas_h * 0.02,
    )
    # anchor laptop's left edge explicitly (x_bias alone is fragile — it's
    # relative to a centered position, not a direct left-edge target)
    laptop_p["frame_x"] = left_margin
    laptop_p["screen_x"] = laptop_p["frame_x"] + MACBOOK_SCREEN[0] * laptop_p["scale"]
    laptop_p["asset"] = str(FRAMES_DIR / "macbook-pro.png")

    # phone: fill the real remaining width to the right of the laptop (with a
    # visible gap + margin), capped by canvas height so it never bleeds
    # off-canvas vertically either. Width-driven and height-driven scale are
    # both computed; the smaller one wins so both constraints hold.
    available_w = canvas_w - (laptop_p["frame_x"] + laptop_p["frame_w"]) - gap - right_margin
    scale_w = available_w / IPHONE_NATIVE[0]
    scale_h = (canvas_h * 0.86) / IPHONE_NATIVE[1]  # leave a top/bottom margin
    scale = max(0.05, min(scale_w, scale_h))
    phone_w, phone_h = IPHONE_NATIVE[0] * scale, IPHONE_NATIVE[1] * scale
    phone_x = laptop_p["frame_x"] + laptop_p["frame_w"] + gap
    phone_y = (canvas_h - phone_h) / 2  # vertically centered, no overlap risk either axis
    phone_p = {
        "scale": scale, "frame_x": phone_x, "frame_y": phone_y,
        "frame_w": phone_w, "frame_h": phone_h,
        "screen_x": phone_x + IPHONE_SCREEN[0] * scale, "screen_y": phone_y + IPHONE_SCREEN[1] * scale,
        "screen_w": (IPHONE_SCREEN[2] - IPHONE_SCREEN[0]) * scale,
        "screen_h": (IPHONE_SCREEN[3] - IPHONE_SCREEN[1]) * scale,
        "asset": str(FRAMES_DIR / "iphone-frame.png"),
    }
    if status_bar != "none":
        variant, color = sample_video_top_color(video_mobile, tmp) if status_bar == "auto" else (status_bar, (230, 230, 230))
        phone_p["status_bar_color"] = color
        phone_p["status_bar_variant"] = variant
        print(f"[status-bar] cover phone clip -> variant={variant} (notch-flank placement)")

    render_frame_png(canvas_w, canvas_h, [laptop_p, phone_p], frame_png)

    video_specs = [
        {"video": video_laptop, "x": laptop_p["screen_x"], "y": laptop_p["screen_y"],
         "w": laptop_p["screen_w"], "h": laptop_p["screen_h"]},
        {"video": video_mobile, "x": phone_p["screen_x"], "y": phone_p["screen_y"],
         "w": phone_p["screen_w"], "h": phone_p["screen_h"]},
    ]
    ffmpeg_compose(bg_png, frame_png, video_specs, output, canvas_w, canvas_h)
    print(f"Saved: {output} ({probe_duration(output):.1f}s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["laptop", "mobile", "cover"])
    ap.add_argument("--video", required=True, help="primary raw scroll-capture clip (laptop clip for cover mode)")
    ap.add_argument("--video2", help="second raw clip, cover mode only (mobile clip)")
    ap.add_argument("--output", required=True)
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--status-bar", default="auto", choices=["auto", "dark", "light", "none"],
                     help="mobile status bar icon variant — auto samples the clip's own top-strip "
                          "brightness (default), dark/light forces one, none skips it entirely")
    args = ap.parse_args()

    if args.mode == "cover":
        if not args.video2:
            raise SystemExit("cover mode needs --video2 (the mobile clip)")
        build_cover(args.video, args.video2, args.output,
                    canvas_w=args.width or 960, canvas_h=args.height or 720,
                    status_bar=args.status_bar)
    elif args.mode == "laptop":
        build_laptop_or_mobile("laptop", args.video, args.output,
                                canvas_w=args.width or 960, canvas_h=args.height or 720)
    else:
        build_laptop_or_mobile("mobile", args.video, args.output,
                                canvas_w=args.width or 1080, canvas_h=args.height or 1350,
                                status_bar=args.status_bar)

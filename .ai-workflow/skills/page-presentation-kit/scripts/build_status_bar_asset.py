#!/usr/bin/env python3
"""
build_status_bar_asset.py — one-time generator for the reusable mobile status
bar pieces (time chip + icons chip), saved to assets/frames/ so every future
phone mockup can composite them in instead of shipping a blank strip.

REDESIGNED 2026-07-29 (v2) — Ridwan's follow-up feedback after the first
version shipped: a real phone's status bar sits AT THE SAME HEIGHT AS THE
NOTCH, flanking it left and right — not as a separate row below the notch.
The first version built one wide continuous bar and reserved a strip below
the notch for it, which put the time/icons in the wrong place relative to
the camera. Fixed by splitting into two small independent chips (time,
icons) sized to fit the actual narrow transparent slivers beside the notch
in assets/frames/iphone-frame.png (calibrated via alpha-channel scan — see
status_bar_util.py's NOTCH_* constants) instead of one wide bar.

Produces, per variant (dark = dark icons for a light background, light =
white icons for a dark background):
  - status-bar-time-{variant}.png   — just the time ("9:41"), transparent bg
  - status-bar-icons-{variant}.png  — signal + wifi + battery, transparent bg

Both are rendered at a fixed 400x130 canvas (aspect ~3.08:1, matching the
calibrated flank safe-box aspect) so status_bar_util.py can scale them
straight into place with no further cropping.

Usage:
  python3 build_status_bar_asset.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FRAMES_DIR = Path(__file__).resolve().parents[4] / "assets" / "frames"

W, H = 400, 130

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/local/lib/python3.10/dist-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans-Bold.ttf",
]


def load_font(size):
    for cand in FONT_CANDIDATES:
        if Path(cand).exists():
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def build_time_chip(color, out_path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = load_font(78)
    draw.text((W * 0.06, H / 2), "9:41", font=font, fill=color, anchor="lm")
    img.save(out_path)
    print(f"Saved: {out_path} ({W}x{H})")


def draw_signal_bars(draw, x, y_baseline, color, scale=1.0):
    bar_w, gap = 15 * scale, 8 * scale
    heights = [h * scale for h in (20, 30, 40, 50)]
    cx = x
    for h in heights:
        draw.rounded_rectangle(
            [cx, y_baseline - h, cx + bar_w, y_baseline], radius=3 * scale, fill=color
        )
        cx += bar_w + gap
    return cx - gap


def draw_wifi(draw, x_center, y_baseline, color, scale=1.0):
    dot_r = 6 * scale
    draw.ellipse(
        [x_center - dot_r, y_baseline - dot_r * 2, x_center + dot_r, y_baseline],
        fill=color,
    )
    radii = [r * scale for r in (20, 36, 52)]
    for r in radii:
        bbox = [x_center - r, y_baseline - dot_r - r, x_center + r, y_baseline - dot_r + r]
        draw.arc(bbox, start=215, end=325, fill=color, width=max(2, round(6 * scale)))


def draw_battery(draw, x, y_center, color, scale=1.0, fill_frac=0.85):
    body_w, body_h = 78 * scale, 38 * scale
    nub_w, nub_h = 7 * scale, 16 * scale
    radius = 7 * scale
    x0, y0 = x, y_center - body_h / 2
    x1, y1 = x0 + body_w, y0 + body_h
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=color, width=max(3, round(4 * scale)))
    nub_x0 = x1 + 3 * scale
    draw.rounded_rectangle(
        [nub_x0, y_center - nub_h / 2, nub_x0 + nub_w, y_center + nub_h / 2],
        radius=3 * scale, fill=color,
    )
    pad = 7 * scale
    fill_w = (body_w - 2 * pad) * fill_frac
    draw.rounded_rectangle([x0 + pad, y0 + pad, x0 + pad + fill_w, y1 - pad], radius=3 * scale, fill=color)
    return nub_x0 + nub_w


def build_icons_chip(color, out_path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cy = H / 2
    baseline = cy + 22

    scale = 1.0
    signal_w = 4 * 15 * scale + 3 * 8 * scale
    wifi_w = 52 * scale * 2
    battery_w = 78 * scale + 3 * scale + 7 * scale

    gap = 16 * scale
    total_w = signal_w + gap + wifi_w + gap + battery_w
    start_x = (W - total_w) / 2

    x = start_x
    x = draw_signal_bars(draw, x, baseline, color, scale) + gap
    draw_wifi(draw, x + wifi_w / 2, baseline, color, scale)
    x += wifi_w + gap
    draw_battery(draw, x, cy, color, scale)

    img.save(out_path)
    print(f"Saved: {out_path} ({W}x{H})")


if __name__ == "__main__":
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    build_time_chip((15, 15, 15, 255), FRAMES_DIR / "status-bar-time-dark.png")
    build_time_chip((255, 255, 255, 255), FRAMES_DIR / "status-bar-time-light.png")
    build_icons_chip((15, 15, 15, 255), FRAMES_DIR / "status-bar-icons-dark.png")
    build_icons_chip((255, 255, 255, 255), FRAMES_DIR / "status-bar-icons-light.png")

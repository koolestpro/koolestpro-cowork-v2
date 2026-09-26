"""
perspective_composite.py — paste a real screenshot into a pre-made photoreal
device-frame background (e.g. a hand holding a phone), using a perspective
warp so it sits correctly in the frame's screen area.

This is the "device-in-hand-lifestyle" style, and it's the one style in
mockup-style-patterns.md that genuinely needs a photo, not CSS — a CSS
gradient can't fake a hand. The photo itself is generated ONCE per device via
gpt-image and reused many times (see the calibration workflow below), so this
script never calls an image model itself — it only does the warp/paste, which
keeps the actual page content 100% accurate (never regenerated/hallucinated).

## One-time setup per device background (do this, then reuse forever)

1. Generate a background photo with gpt-image: a hand holding a [phone/laptop],
   screen area left BLANK/black or a flat mid-grey so the corners are easy to
   find, realistic lighting, the kind of environment the reference calls for.
   Save it to assets/frames/{name}.png (e.g. assets/frames/hand-holding-phone.png).
2. Open that image and note the four pixel corners of the blank screen area,
   in this order: top-left, top-right, bottom-right, bottom-left.
3. Save those coordinates as assets/frames/{name}.json:
   {"corners": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]], "screenshot_aspect": "mobile"}
4. From then on, any real screenshot gets warped into that exact region by
   this script — the background photo and its calibration are reused for
   every future mockup in this style, not regenerated per run.

If no calibrated background exists yet for the device you need, generate and
calibrate one first (steps 1-3) rather than skipping the style or faking it
with a flat CSS frame — a mislabeled flat frame presented as "lifestyle" would
be worse than just using flat-browser-frame honestly instead.

Usage:
  python3 perspective_composite.py --background assets/frames/hand-holding-phone.png \\
      --calibration assets/frames/hand-holding-phone.json \\
      --screenshot mobile.png --output out.png
"""

import argparse
import json
from PIL import Image


def find_coeffs(source_coords, target_coords):
    # Standard PIL perspective-transform coefficient solve (maps target
    # quad -> source quad, since PIL's transform pulls FROM source coords).
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = matrix
    B = [c for pair in source_coords for c in pair]

    # Solve A @ coeffs = B via Gaussian elimination (avoids a numpy dependency).
    n = len(A)
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[pivot] = A[pivot], A[i]
        B[i], B[pivot] = B[pivot], B[i]
        for r in range(i + 1, n):
            factor = A[r][i] / A[i][i]
            for c in range(i, n):
                A[r][c] -= factor * A[i][c]
            B[r] -= factor * B[i]
    coeffs = [0] * n
    for i in range(n - 1, -1, -1):
        coeffs[i] = (B[i] - sum(A[i][j] * coeffs[j] for j in range(i + 1, n))) / A[i][i]
    return coeffs


def composite(background_path, calibration_path, screenshot_path, output_path):
    bg = Image.open(background_path).convert("RGBA")
    with open(calibration_path) as f:
        cal = json.load(f)
    corners = cal["corners"]  # [[x1,y1] top-left, top-right, bottom-right, bottom-left]

    shot = Image.open(screenshot_path).convert("RGBA")
    sw, sh = shot.size
    source_quad = [(0, 0), (sw, 0), (sw, sh), (0, sh)]

    coeffs = find_coeffs(source_quad, corners)
    warped = shot.transform(bg.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    result = Image.alpha_composite(bg, warped)
    result.convert("RGB").save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--background", required=True)
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--screenshot", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    composite(args.background, args.calibration, args.screenshot, args.output)

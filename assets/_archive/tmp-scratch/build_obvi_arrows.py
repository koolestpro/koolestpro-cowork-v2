#!/usr/bin/env python3
"""Rasterize the Obvi annotation-arrow overlay to a transparent PNG.

Live <svg> + marker-end arrowheads render fine natively but come out BLANK in
html2canvas (project-constitution.md). So the overlay is pre-rasterized here and
embedded as a plain <img> in the content pack.

Geometry (matches #anno-graphic in obvi_..._content.html):
  canvas 1080x1080
  .an-img  left:370 top:180 width:340   (after-rebuild screenshot, 390x844 source)
  image spans x 370..710
  left  arrow endpoints land at x=390 (20px inside the left edge)
  right arrow endpoints land at x=690 (20px inside the right edge)
Final approach into every endpoint is kept nearly flat by pinning the SECOND
control point near the endpoint's x and within ~10px of its y.
"""
import os
import subprocess
import sys

W = H = 1080
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# (label_y, side)  label_y == the y the arrow points at, in canvas coords
POINTS = [
    (343, "L"),   # 1 hero photo kept
    (438, "R"),   # 2 back-in-stock demoted to a pill
    (500, "L"),   # 3 headline names the outcome
    (603, "R"),   # 4 one sentence became four scannable lines
    (671, "L"),   # 5 proof given weight
    (711, "R"),   # 6 button carries the real offer
    (800, "L"),   # 7 real price + real review count
    (892, "R"),   # 8 widget moved clear of the button
]

# start-side control point offsets, varied per arrow for shape personality
# (dx from start, dy from start)
SHAPES = [
    (60, -46), (-60, -40), (70, 34), (-70, 30),
    (55, -52), (-55, 44), (65, 40), (-65, -36),
]

STROKE = "#4B2E9E"


def build_svg():
    paths = []
    for i, (y, side) in enumerate(POINTS):
        if side == "L":
            sx, ex = 335.0, 390.0
        else:
            sx, ex = 745.0, 690.0
        sy = float(y)
        ey = float(y)
        dx, dy = SHAPES[i % len(SHAPES)]
        c1x, c1y = sx + dx, sy + dy
        # end-side control point: near endpoint x, within 10px of endpoint y
        c2x = ex + (-26.0 if side == "L" else 26.0)
        c2y = ey - 7.0
        # clamp everything inside the viewBox
        for v in (c1x, c2x):
            assert 0 <= v <= W, v
        c1y = max(8.0, min(H - 8.0, c1y))
        c2y = max(8.0, min(H - 8.0, c2y))
        paths.append(
            f'<path d="M{sx:.1f},{sy:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} '
            f'{ex:.1f},{ey:.1f}" fill="none" stroke="{STROKE}" stroke-width="2.4" '
            f'stroke-linecap="round" marker-end="url(#ah)"/>'
        )
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:transparent}}
</style></head><body>
<svg id="s" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<marker id="ah" markerWidth="10" markerHeight="9" refX="9" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
<path d="M0,0 L9,4.5 L0,9 Z" fill="{STROKE}"/>
</marker>
</defs>
{chr(10).join(paths)}
</svg></body></html>'''


def main():
    html_path = os.path.join(OUT_DIR, "_obvi_arrows.html")
    png_path = os.path.join(OUT_DIR, "_obvi_arrows.png")
    with open(html_path, "w") as f:
        f.write(build_svg())

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto("file://" + html_path, wait_until="domcontentloaded")
        pg.wait_for_timeout(600)
        pg.query_selector("#s").screenshot(path=png_path, omit_background=True)
        b.close()
    print("wrote", png_path, os.path.getsize(png_path), "bytes")


if __name__ == "__main__":
    main()

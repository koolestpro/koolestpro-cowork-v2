#!/usr/bin/env python3
"""Rasterize the Bebemoss annotation arrow overlay to a transparent PNG.

Live <svg> + marker-end arrowheads render fine natively but vanish in
html2canvas exports (see project-constitution.md). So the overlay is
pre-rasterized here and embedded as a plain <img> in the content pack.

Canvas: 1080x1080, matching #anno-graphic.
Image stage inside that canvas: left=370, top=200, displayed width=340
(screenshot captured at 390 CSS px wide -> scale 0.8718).

Every curve's END-side control point sits close to the endpoint's x and
within ~10px of its y, so the arrowhead always approaches nearly flat.
Variety lives in the START-side control point only.
"""
import os
import sys
from playwright.sync_api import sync_playwright

W = H = 1080

# (start_x, start_y, c1x, c1y, c2x, c2y, end_x, end_y)
# left-side arrows travel left->right, right-side arrows travel right->left
ARROWS = [
    # 1 left  -> h1 "Soft Toys"
    (344, 268, 366, 268, 372, 292, 386, 290),
    # 3 left  -> filter chip row
    (344, 392, 364, 400, 372, 366, 386, 362),
    # 5 left  -> first card title + price
    (344, 556, 368, 566, 372, 556, 386, 553),
    # 7 left  -> third-row card title
    (344, 748, 370, 758, 372, 752, 386, 750),
    # 2 right -> one-line summary
    (742, 322, 716, 322, 706, 316, 694, 314),
    # 4 right -> sort pill
    (742, 448, 714, 446, 706, 366, 696, 362),
    # 6 right -> header / breadcrumb (kept)
    (742, 228, 716, 226, 706, 226, 696, 224),
    # 8 right -> save pill, moved
    (742, 908, 716, 910, 702, 912, 690, 910),
]

STROKE = "#1F3D33"


def build_svg():
    paths = []
    for (sx, sy, c1x, c1y, c2x, c2y, ex, ey) in ARROWS:
        paths.append(
            f'<path d="M{sx},{sy} C{c1x},{c1y} {c2x},{c2y} {ex},{ey}" '
            f'fill="none" stroke="{STROKE}" stroke-width="2.4" '
            f'stroke-linecap="round" marker-end="url(#ah)"/>'
        )
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:transparent}}</style></head><body>
<svg id="ov" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<marker id="ah" viewBox="0 0 9 9" refX="8" refY="4.5" markerWidth="6.5" markerHeight="6.5"
        orient="auto" markerUnits="strokeWidth">
  <path d="M0,0 L9,4.5 L0,9 Z" fill="{STROKE}"/>
</marker>
</defs>
{''.join(paths)}
</svg></body></html>"""


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "outputs/cro-fixes/_bebemoss_arrows.png"
    tmp = os.path.abspath("outputs/cro-fixes/_bebemoss_arrows.html")
    with open(tmp, "w") as f:
        f.write(build_svg())
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(600)
        pg.locator("#ov").screenshot(path=out, omit_background=True)
        b.close()
    print("Saved:", out)


if __name__ == "__main__":
    main()

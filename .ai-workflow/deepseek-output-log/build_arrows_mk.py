#!/usr/bin/env python3
"""Build the pre-rasterized arrow overlay PNG for the Material Kitchen anno-graphic.
Live SVG arrows vanish in html2canvas, so we render them to a transparent PNG and
embed that as an <img>. Canvas 1080x1080. Phone displayed at width 340, top=180,
left=370, so displayed_y = 180 + css_y*0.8718 (after image is 390x844 CSS)."""
import os, base64
from playwright.sync_api import sync_playwright

PHONE_LEFT = 370
PHONE_TOP = 180
SCALE = 0.8718  # 340/390
IN_L = PHONE_LEFT + 16      # left inner endpoint x
IN_R = PHONE_LEFT + 340 - 16  # right inner endpoint x

def dy(css_y):
    return round(PHONE_TOP + css_y * SCALE)

# (side, css_y_center)
POINTS = {
    "announce": ("L", 19),
    "hero":     ("R", 248),
    "h1":       ("L", 446),
    "proof":    ("R", 573),
    "chips":    ("L", 645),
    "cta":      ("R", 717),
    "bestseller":("L", 794),
}

paths = []
for name,(side,cy) in POINTS.items():
    ey = dy(cy)
    if side == "L":
        sx, ex = 348, IN_L
        # gentle curve, flat final approach (c2 near endpoint)
        d = f"M {sx} {ey} C {sx+18} {ey-14} {ex-34} {ey} {ex} {ey}"
    else:
        sx, ex = 732, IN_R
        d = f"M {sx} {ey} C {sx-18} {ey-14} {ex+34} {ey} {ex} {ey}"
    paths.append(f'<path d="{d}" fill="none" stroke="#1F3D33" stroke-width="2.4" marker-end="url(#ah)"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
<defs>
<marker id="ah" markerWidth="11" markerHeight="11" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
<path d="M0,0 L9,4.5 L0,9 Z" fill="#1F3D33"/>
</marker>
</defs>
{''.join(paths)}
</svg>'''

html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}body{{background:transparent}}</style></head><body>{svg}</body></html>'
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out_png = os.path.join(root, "outputs/cro-fixes/_mk_arrows.png")
tmp_html = os.path.join(root, "outputs/cro-fixes/_mk_arrows.html")
open(tmp_html, "w").write(html)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1080}, device_scale_factor=2)
    pg.goto("file://"+tmp_html)
    pg.wait_for_timeout(400)
    el = pg.query_selector("svg")
    el.screenshot(path=out_png, omit_background=True)
    b.close()

# print endpoint y's (displayed, canvas coords) for HTML caption placement
print("ENDPOINTS(px in 1080 canvas):")
for name,(side,cy) in POINTS.items():
    print(f"  {name}: side={side} y={dy(cy)}")
print("PNG:", out_png, os.path.getsize(out_png), "bytes")

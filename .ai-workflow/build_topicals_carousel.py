#!/usr/bin/env python3
"""Build the Topicals homepage CRO 3-slide carousel (2026-10-18).

Format: docs/system/cro-3-slide-carousel-format.md. Bar to beat: build_bala_carousel.py (2026-10-11).
Delta this week: cover evidence is the real covered button (the Scratch to win pill on Shop now),
the before phone on slide 2 is the actual on-load scratch-card screen, and slide 3 pins hit the
labelled range, the rating line and the one CTA.
"""
import base64, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "topicals" / "_assets"
BG = ROOT / "outputs" / "Background 2.svg"
OUT = ROOT / "outputs" / "cro-fixes" / "topicals_homepage-hero_carousel.html"
SLUG = "topicals_homepage-hero"
TITLE = "A game first. The skincare later."


def uri(p):
    mime = {".svg": "image/svg+xml", ".png": "image/png"}[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def line(x1, y1, x2, y2):
    L = math.hypot(x2 - x1, y2 - y1); ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<div class="line" style="left:{x1}px;top:{y1}px;width:{L:.1f}px;transform:rotate({ang:.2f}deg);"></div>'
            f'<div class="pindot" style="left:{x2-4.5}px;top:{y2-4.5}px;"></div>')


def ph(cx, cy, left=272, top=8, w=200):
    k = w / 450
    return round(left + (19.5 + 1.0546 * cx) * k), round(top + (59 + 1.0546 * cy) * k)

# targets in the rebuild (css px at 390 wide), pinned in the 16px gutter at each element's left edge
HX, HY = ph(8, 222)     # labelled kit photo (variant C, Ridwan pick)
RX, RY = ph(8, 402)     # rating line (y 393-411)
WX, WY = ph(8, 579)     # the one red CTA (y 553-605)
T1, T2, T3 = 30, 186, 336
LINES = line(240, T1 + 30, HX, HY) + line(240, T2 + 12, RX, RY) + line(240, T3 + 12, WX, WY)

EXTRA_CSS = """
.sticker{position:absolute;width:26px;height:26px;border-radius:8px;background:#850FFA;color:#fff;font-family:'Syne',sans-serif;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.45);z-index:5;}
.tagchip{position:absolute;z-index:5;background:#FA9C0F;color:#141414;font-family:'Syne',sans-serif;font-weight:800;font-size:12px;padding:6px 11px;border-radius:14px;box-shadow:0 6px 16px rgba(0,0,0,.45);}
"""


def main():
    html = (ROOT / ".ai-workflow" / "build_topicals_carousel.tpl.html").read_text(encoding="utf-8")
    html = (html.replace("__BG__", uri(BG)).replace("__LOGO__", uri(A / "logo.png"))
            .replace("__BEFORE__", uri(A / "phones" / "topicals_before_phone.png"))
            .replace("__AFTER__", uri(A / "phones" / "topicals_after_phone.png"))
            .replace("__HEROCROP__", uri(A / "before_hero_crop.png"))
            .replace("__LINES__", LINES).replace("__T1__", str(T1)).replace("__T2__", str(T2)).replace("__T3__", str(T3))
            .replace("__EXTRA_CSS__", EXTRA_CSS).replace("__SLUG__", SLUG))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars) targets", (HX, HY), (RX, RY), (WX, WY))


if __name__ == "__main__":
    main()

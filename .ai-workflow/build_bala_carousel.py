#!/usr/bin/env python3
"""Build the Bala homepage CRO 3-slide carousel (2026-10-11).

Format: docs/system/cro-3-slide-carousel-format.md (cover -> before/after -> annotation).
Bar to beat: build_flybyjing_carousel.py (2026-10-04).

Delta this week:
- First homepage in the 3-slide format (the last four were PDPs), so the cover evidence is
  the live hero itself: a real crop of screen one showing the hairline slogan, the bundle
  line, the outline button and the unnamed Bangles on the model's ankles, with purple
  question stickers on the slogan and on the Bangles.
- Slide 3 rows are spaced to the three most separated targets on the rebuild (H1, rating
  row, best-sellers rail), so the connectors fan out instead of bunching.
"""
import base64, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "bala" / "_assets"
BG = ROOT / "outputs" / "Background 2.svg"
OUT = ROOT / "outputs" / "cro-fixes" / "bala_bangles-homepage_carousel.html"
SLUG = "bala_bangles-homepage"
TITLE = "Cute slogan. No product named."


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
HX, HY = ph(8, 250)     # labelled range photo
RX, RY = ph(8, 508)     # rating line
WX, WY = ph(8, 658)     # CTA + category pills
T1, T2, T3 = 30, 186, 336
LINES = line(240, T1 + 30, HX, HY) + line(240, T2 + 12, RX, RY) + line(240, T3 + 12, WX, WY)

EXTRA_CSS = """
.sticker{position:absolute;width:26px;height:26px;border-radius:8px;background:#850FFA;color:#fff;font-family:'Syne',sans-serif;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.45);z-index:5;}
.tagchip{position:absolute;z-index:5;background:#FA9C0F;color:#141414;font-family:'Syne',sans-serif;font-weight:800;font-size:12px;padding:6px 11px;border-radius:14px;box-shadow:0 6px 16px rgba(0,0,0,.45);}
"""


def main():
    html = (ROOT / ".ai-workflow" / "build_bala_carousel.tpl.html").read_text(encoding="utf-8")
    html = (html.replace("__BG__", uri(BG)).replace("__LOGO__", uri(A / "logo.png"))
            .replace("__BEFORE__", uri(A / "phones" / "bala_before_phone.png"))
            .replace("__AFTER__", uri(A / "phones" / "bala_after_phone.png"))
            .replace("__HEROCROP__", uri(A / "before_hero_crop.png"))
            .replace("__LINES__", LINES).replace("__T1__", str(T1)).replace("__T2__", str(T2)).replace("__T3__", str(T3))
            .replace("__EXTRA_CSS__", EXTRA_CSS).replace("__SLUG__", SLUG))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars) targets", (HX, HY), (RX, RY), (WX, WY))


if __name__ == "__main__":
    main()

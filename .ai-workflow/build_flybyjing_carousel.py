#!/usr/bin/env python3
"""Build the Fly By Jing Original Sichuan Chili Crisp CRO 3-slide carousel (2026-10-04).

Format: docs/system/cro-3-slide-carousel-format.md (cover -> before/after -> annotation).
Bar to beat: build_minimalist_carousel.py (2026-09-27).

Delta this week:
- The cover's visual is the evidence itself: a real crop of the live buy box exactly as
  a shopper finds it 1,017px down ("2-PACK", "$30.00", no per-jar price), with purple
  question stickers on the two confusing spots, next to the AFTER phone. Last week was
  a scroll-depth ruler; this one shows the actual confusing element.
- Slide 3 pins land in the page gutter at each element's left edge, so no pin covers
  the text it points at (last week two pins sat on top of the words), and the three
  rows are evenly spaced with no dead band between them.
"""
import base64, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "flybyjing" / "_assets"
BG = ROOT / "outputs" / "Background 2.svg"
OUT = ROOT / "outputs" / "cro-fixes" / "flybyjing_chili-crisp-pdp_carousel.html"
SLUG = "flybyjing_chili-crisp-pdp"
TITLE = "$30 for 2 jars. Not on screen one."


def uri(p):
    mime = {".svg": "image/svg+xml", ".png": "image/png"}[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def line(x1, y1, x2, y2):
    L = math.hypot(x2 - x1, y2 - y1); ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<div class="line" style="left:{x1}px;top:{y1}px;width:{L:.1f}px;transform:rotate({ang:.2f}deg);"></div>'
            f'<div class="pindot" style="left:{x2-4.5}px;top:{y2-4.5}px;"></div>')


# phone on slide 3: 200x433 at (272,8) inside the 480px annotation canvas.
def ph(cx, cy, left=272, top=8, w=200):
    k = w / 450
    return round(left + (19.5 + 1.0546 * cx) * k), round(top + (59 + 1.0546 * cy) * k)

# targets in the rebuild (css px at 390 wide), pinned in the 16px gutter at the element's left edge
HX, HY = ph(8, 340)     # heat line chip at the bottom of the hero
PX, PY = ph(8, 492)     # pack picker ($15 / jar)
CX, CY = ph(8, 612)     # Add to Cart
T1, T2, T3 = 30, 186, 346          # row tops (each row ~ 95px tall)
LINES = line(240, T1 + 62, HX, HY) + line(240, T2 + 12, PX, PY) + line(240, T3 + 12, CX, CY)

EXTRA_CSS = """
.sticker{position:absolute;width:26px;height:26px;border-radius:8px;background:#850FFA;color:#fff;font-family:'Syne',sans-serif;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.45);z-index:5;}
.tagchip{position:absolute;z-index:5;background:#FA9C0F;color:#141414;font-family:'Syne',sans-serif;font-weight:800;font-size:12px;padding:6px 11px;border-radius:14px;box-shadow:0 6px 16px rgba(0,0,0,.45);}
"""


def main():
    head = (A.parent.parent.parent.parent / ".ai-workflow" / "build_flybyjing_carousel.tpl.html")
    html = head.read_text(encoding="utf-8")
    html = (html.replace("__BG__", uri(BG)).replace("__LOGO__", uri(A / "logo.png"))
            .replace("__BEFORE__", uri(A / "phones" / "flybyjing_before_phone.png"))
            .replace("__AFTER__", uri(A / "phones" / "flybyjing_after_phone.png"))
            .replace("__BUYBOX__", uri(A / "before_buybox_crop.png"))
            .replace("__LINES__", LINES).replace("__T1__", str(T1)).replace("__T2__", str(T2)).replace("__T3__", str(T3))
            .replace("__EXTRA_CSS__", EXTRA_CSS).replace("__SLUG__", SLUG))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars) targets", (HX, HY), (PX, PY), (CX, CY))


if __name__ == "__main__":
    main()

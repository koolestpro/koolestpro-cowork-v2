#!/usr/bin/env python3
"""Build the Minimalist Niacinamide 10% Face Serum CRO 3-slide carousel (2026-09-27).

Format: docs/system/cro-3-slide-carousel-format.md (cover -> before/after -> annotation).
Bar to beat: build_caraway_carousel.py / the Kyte Baby carousel (2026-09-20).

Delta this week: the cover's visual is the #1 finding itself, measured. A real
full-length capture of the live page (0-2,100px) runs beside the AFTER phone as a
scroll-depth ruler with the real positions of the fold (844px), the price (1,576px)
and Add to Cart (1,870px). Also: headline is the topmost element on every slide,
@koolestpro sits in a bottom lockup (rule 9, revised 2026-09-18), the brand logo is
on the cover only, and slide 3 uses angled connector lines so each row hits its
exact element without rows colliding.
"""
import base64, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "minimalist" / "_assets"
BG = ROOT / "outputs" / "Background 2.svg"
OUT = ROOT / "outputs" / "cro-fixes" / "minimalist_niacinamide-10-serum-pdp_carousel.html"
SLUG = "minimalist_niacinamide-10-serum-pdp"


def uri(p):
    mime = {".svg": "image/svg+xml", ".png": "image/png"}[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def line(x1, y1, x2, y2):
    L = math.hypot(x2 - x1, y2 - y1); ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<div class="line" style="left:{x1}px;top:{y1}px;width:{L:.1f}px;transform:rotate({ang:.2f}deg);"></div>'
            f'<div class="pindot" style="left:{x2-4.5}px;top:{y2-4.5}px;"></div>')


# phone on slide 3: 200x433 at (272,8) inside the 480px annotation canvas.
# phone px = (59 + 1.0546*css_y) * 200/450 ; x = (19.5 + 1.0546*css_x) * 200/450
def ph(cx, cy, left=272, top=8, w=200):
    k = w / 450
    return round(left + (19.5 + 1.0546 * cx) * k), round(top + (59 + 1.0546 * cy) * k)

HX, HY = ph(20, 176)    # outcome headline
CX, CY = ph(40, 548)    # "Pregnancy-safe" chip
BX, BY = ph(20, 654)    # Add to Cart
LINES = line(236, 83, HX, HY) + line(236, 275, CX, CY) + line(236, 362, BX, BY)

TEMPLATE = open(pathlib.Path(__file__).with_name("build_minimalist_carousel.tpl.html"), encoding="utf-8").read()


def main():
    html = (TEMPLATE.replace("__BG__", uri(BG)).replace("__LOGO__", uri(A / "logo.png"))
            .replace("__BEFORE__", uri(A / "phones" / "minimalist_before_phone.png"))
            .replace("__AFTER__", uri(A / "phones" / "minimalist_after_phone.png"))
            .replace("__STRIP__", uri(A / "minimalist_before_strip.png"))
            .replace("__LINES__", LINES).replace("__SLUG__", SLUG))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars) targets", (HX, HY), (CX, CY), (BX, BY))


if __name__ == "__main__":
    main()

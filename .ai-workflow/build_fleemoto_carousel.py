#!/usr/bin/env python3
"""Build the FleeMoto wheel set PDP CRO 3-slide carousel (2026-11-01).

Format: docs/system/cro-3-slide-carousel-format.md. Bar to beat: build_fishwife_carousel.py (2026-10-25).
Cover evidence is measured on the real BEFORE phone: the 844px screen edge is marked, and a chip states
where the price actually sits (903px down) and that the title is all the shopper gets. Slide 3 pins hit
three separated elements in the rebuild: price row (y 523), fit box (y 606), Pre-order button (y 700).
Logo: FleeMoto's header is text only (no logo file on the site); the chip uses a crop of their real
rendered header wordmark from the live screenshot, not a retyped font.
"""
import base64, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs/cro-fixes/fleemoto/_assets"
BG = ROOT / "outputs/Background 2.svg"
OUT = ROOT / "outputs/cro-fixes/fleemoto_supermoto-wheels-pdp_carousel.html"
SLUG = "fleemoto_supermoto-wheels-pdp"

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

PX, PY = ph(20, 523)   # price row
FX, FY = ph(16, 606)   # fit box left edge
CX, CY = ph(16, 700)   # Pre-order button left edge
T1, T2, T3 = 40, 180, 318
LINES = line(240, T1 + 12, PX, PY) + line(240, T2 + 12, FX, FY) + line(240, T3 + 12, CX, CY)

def bp(cy, top=20, w=180):
    k = w / 450; return round(top + (59 + 1.0546 * cy) * k)
EDGE = bp(844) - 6
COVER_MARKS = f"""
<div style="position:absolute;left:60px;top:{bp(626)}px;width:4px;height:{bp(767)-bp(626)}px;background:#FA9C0F;border-radius:2px;z-index:4;"></div>
<div class="tagchip" style="left:22px;top:{bp(560)}px;font-size:11px;">Title only</div>
<div style="position:absolute;left:22px;top:418px;z-index:5;background:rgba(12,12,12,.88);border:1.5px solid #FA9C0F;border-radius:10px;padding:5px 9px;font-family:'DM Mono',monospace;font-size:10.5px;color:#fff;white-space:nowrap;">Price: <b style="color:#FA9C0F;font-family:'Syne',sans-serif;font-size:12.5px;">903px down</b> (screen 844)</div>
<div class="tagchip" style="left:302px;top:418px;font-size:12px;">Price, fit + button</div>
"""
EXTRA_CSS = """
.tagchip{position:absolute;z-index:5;background:#FA9C0F;color:#141414;font-family:'Syne',sans-serif;font-weight:800;font-size:12px;padding:6px 11px;border-radius:14px;box-shadow:0 6px 16px rgba(0,0,0,.45);}
.brandchip{padding:6px 11px!important;}
"""

def main():
    html = (ROOT / ".ai-workflow/build_fleemoto_carousel.tpl.html").read_text(encoding="utf-8")
    html = (html.replace("__BG__", uri(BG)).replace("__LOGO__", uri(A / "logo_sm.png"))
            .replace("__BEFORE__", uri(A / "phones/fleemoto_before_phone.png"))
            .replace("__AFTER__", uri(A / "phones/fleemoto_after_phone.png"))
            .replace("__COVER_MARKS__", COVER_MARKS)
            .replace("__LINES__", LINES).replace("__T1__", str(T1)).replace("__T2__", str(T2)).replace("__T3__", str(T3))
            .replace("__EXTRA_CSS__", EXTRA_CSS).replace("__SLUG__", SLUG))
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT, (PX, PY), (FX, FY), (CX, CY))

if __name__ == "__main__":
    main()

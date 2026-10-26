#!/usr/bin/env python3
"""Build the Fishwife shop-all collection CRO 3-slide carousel (2026-10-25).

Format: docs/system/cro-3-slide-carousel-format.md. Bar to beat: build_topicals_carousel.py (2026-10-18).
Delta this week: the cover's evidence is measured ON the real before phone (an orange bracket marks the
400px banner, a chip marks where the first product name actually sits, 863px down), so the hook number
is visible proof instead of a separate crop; slide 3 pins hit three well-separated elements (card photo,
the counted rating, the Add button).
"""
import base64, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "fishwife" / "_assets"
BG = ROOT / "outputs" / "Background 2.svg"
OUT = ROOT / "outputs" / "cro-fixes" / "fishwife_shop-all-collection_carousel.html"
SLUG = "fishwife_shop-all-collection"


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

# targets in the rebuild (css px at 390 wide, measured with Playwright)
IX, IY = ph(16, 360)    # card 1 photo (y 294-426)
RX, RY = ph(26, 494)    # card 1 counted rating (y 487-501)
AX, AY = ph(16, 794)    # card 3 price + Add row (y 778-810), pinned at the card edge
T1, T2, T3 = 30, 186, 336
LINES = line(240, T1 + 12, IX, IY) + line(240, T2 + 12, RX, RY) + line(240, T3 + 12, AX, AY)

# cover: measured marks on the BEFORE phone (left 46, top 20, width 196 inside a container at top 176)
def bp(cy, left=56, top=20, w=180):
    k = w / 450; return round(top + (59 + 1.0546 * cy) * k)
B0, B1 = bp(98), bp(498)   # the banner, y 98-498 on the live page
COVER_MARKS = f"""
<div style="position:absolute;left:240px;top:{B0}px;width:4px;height:{B1-B0}px;background:#FA9C0F;border-radius:2px;z-index:4;"></div>
<div style="position:absolute;left:234px;top:{B0}px;width:12px;height:3px;background:#FA9C0F;z-index:4;"></div>
<div style="position:absolute;left:234px;top:{B1-3}px;width:12px;height:3px;background:#FA9C0F;z-index:4;"></div>
<div class="tagchip" style="left:150px;top:{bp(420)}px;font-size:12px;">400px banner</div>
<div style="position:absolute;left:22px;top:422px;z-index:5;background:rgba(12,12,12,.88);border:1.5px solid #FA9C0F;border-radius:10px;padding:5px 9px;font-family:'DM Mono',monospace;font-size:10.5px;color:#fff;white-space:nowrap;">1st name: <b style="color:#FA9C0F;font-family:'Syne',sans-serif;font-size:12.5px;">863px down</b> (screen 844)</div>
<div class="tagchip" style="left:300px;top:422px;font-size:12px;">4 tins, rated + priced</div>
"""
EXTRA_CSS = """
.tagchip{position:absolute;z-index:5;background:#FA9C0F;color:#141414;font-family:'Syne',sans-serif;font-weight:800;font-size:12px;padding:6px 11px;border-radius:14px;box-shadow:0 6px 16px rgba(0,0,0,.45);}
.brandchip{padding:5px 11px!important;}
"""


def main():
    html = (ROOT / ".ai-workflow" / "build_fishwife_carousel.tpl.html").read_text(encoding="utf-8")
    html = (html.replace("__BG__", uri(BG)).replace("__LOGO__", uri(A / "logo_sm.png"))
            .replace("__BEFORE__", uri(A / "phones" / "fishwife_before_phone.png"))
            .replace("__AFTER__", uri(A / "phones" / "fishwife_after_phone.png"))
            .replace("__COVER_MARKS__", COVER_MARKS)
            .replace("__LINES__", LINES).replace("__T1__", str(T1)).replace("__T2__", str(T2)).replace("__T3__", str(T3))
            .replace("__EXTRA_CSS__", EXTRA_CSS).replace("__SLUG__", SLUG))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars) targets", (IX, IY), (RX, RY), (AX, AY), "banner", B0, B1)


if __name__ == "__main__":
    main()

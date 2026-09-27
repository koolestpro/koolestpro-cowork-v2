#!/usr/bin/env python3
"""Standalone clear-background annotated graphic, Minimalist Niacinamide 10% PDP (2026-09-27).

Spec: docs/system/cro-3-slide-carousel-format.md "clear-background style". Reference:
build_caraway_annotation.py / the Kyte Baby annotated graphic. Headline is the topmost
element; Q/A in Caveat 700; line + circle-head connectors (angled where needed so each
row hits its exact element); real brand logo + @koolestpro in the bottom lockup.
Rows = the rebuild's top 3 improvements, ranked (see the audit).
"""
import base64, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "minimalist" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "minimalist_niacinamide-10-serum-pdp_annotation.html"
PL, PT, PW = 660, 190, 340; K = PW / 450

def uri(p): return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
def ph(cx, cy): return round(PL + (19.5 + 1.0546 * cx) * K), round(PT + (59 + 1.0546 * cy) * K)
def conn(x1, y1, x2, y2):
    L = math.hypot(x2 - x1, y2 - y1); a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<div class="conn" style="left:{x1}px;top:{y1}px;width:{L:.1f}px;transform:rotate({a:.2f}deg);"></div>'
            f'<div class="dot" style="left:{x2-5}px;top:{y2-5}px;"></div>')

H = ph(20, 176); C = ph(34, 548); B = ph(20, 654)
LINES = conn(470, 352, *H) + conn(470, 622, *C) + conn(470, 792, *B)

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>CRO Fix Annotation - Minimalist Niacinamide 10% - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Syne:wght@700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#2a2a2a;padding:40px;font-family:'DM Mono',monospace;}
#sheet{width:1080px;height:1080px;background:#F7F5F0;position:relative;margin:0 auto;overflow:hidden;}
.headline{position:absolute;top:52px;left:56px;right:56px;font-family:'Syne',sans-serif;font-weight:800;font-size:37px;color:#1a1a1a;line-height:1.12;letter-spacing:-0.6px;}
.pagetype{position:absolute;top:150px;left:56px;font-size:15px;letter-spacing:2px;text-transform:uppercase;color:#8a8478;}
.phone{position:absolute;left:__PL__px;top:__PT__px;width:__PW__px;height:__PH__px;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.18));}
.cal{position:absolute;left:56px;width:420px;}
.q{font-family:'Caveat',cursive;font-weight:700;font-size:34px;color:#850FFA;line-height:1.1;}
.a{font-family:'Caveat',cursive;font-weight:700;font-size:27px;color:#2e2e2e;line-height:1.15;margin-top:6px;}
.qb,.ab{display:inline-block;font-family:'DM Mono',monospace;font-weight:500;font-size:12px;letter-spacing:1px;border-radius:5px;padding:3px 8px;margin-right:8px;vertical-align:5px;}
.qb{background:#850FFA;color:#fff;} .ab{background:#FA9C0F;color:#1a1a1a;}
.conn{position:absolute;height:2px;background:#bdb5a6;transform-origin:0 50%;}
.dot{position:absolute;width:10px;height:10px;border-radius:50%;background:#FA9C0F;box-shadow:0 0 0 4px rgba(250,156,15,0.2);}
.lock{position:absolute;bottom:44px;left:56px;display:flex;align-items:center;gap:14px;}
.lock img{height:24px;}
.lock span{font-size:14px;color:#6b6558;}
</style></head>
<body>
<div id="sheet">
  <div class="headline">3 questions a serum buyer<br>asks before the first scroll.</div>
  <div class="pagetype">Product Page (PDP) &middot; Minimalist Niacinamide 10% Serum</div>
  <img class="phone" src="__AFTER__" />
  __LINES__
  <div class="cal" style="top:318px;">
    <div class="q"><span class="qb">Q1</span>"What will it do for my skin?"</div>
    <div class="a"><span class="ab">FIX</span>An outcome headline on the hero, not just the product name.</div>
  </div>
  <div class="cal" style="top:588px;">
    <div class="q"><span class="qb">Q2</span>"Is it safe while I'm pregnant?"</div>
    <div class="a"><span class="ab">FIX</span>Moved from a closed accordion to a chip by the price.</div>
  </div>
  <div class="cal" style="top:758px;">
    <div class="q"><span class="qb">Q3</span>"What does it cost?"</div>
    <div class="a"><span class="ab">FIX</span>&#8377;539 and Add to Cart on screen one.</div>
  </div>
  <div class="lock"><img src="__LOGO__" alt="Minimalist"><span>redesigned by @koolestpro &middot; concept, not a client</span></div>
</div>
<script>
async function waitReady(){ if(document.fonts&&document.fonts.ready) await document.fonts.ready;
  await Promise.all(Array.from(document.querySelectorAll('img')).map(i=>i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r;})));
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); }
async function captureSheet(){ await waitReady(); return await html2canvas(document.getElementById('sheet'),{scale:2,useCORS:true,allowTaint:true,backgroundColor:'#F7F5F0',logging:false}); }
window.captureSheet = captureSheet;
</script></body></html>
"""

def main():
    html = (HTML.replace("__AFTER__", uri(A / "phones" / "minimalist_after_phone.png")).replace("__LOGO__", uri(A / "logo.png"))
            .replace("__LINES__", LINES).replace("__PL__", str(PL)).replace("__PT__", str(PT)).replace("__PW__", str(PW))
            .replace("__PH__", str(round(PW * 974 / 450))))
    OUT.write_text(html, encoding="utf-8"); print("wrote", OUT, H, C, B)

if __name__ == "__main__": main()

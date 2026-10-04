#!/usr/bin/env python3
"""Standalone clear-background annotated graphic, Fly By Jing Chili Crisp PDP (2026-10-04).

Spec: docs/system/cro-3-slide-carousel-format.md "clear-background style". Reference:
build_minimalist_annotation.py (2026-09-27). Headline is the topmost element; Q/A in
Caveat 700; line + circle-head connectors, pinned in the page gutter at each element's
left edge so no dot sits on the text it points at (last week's graphic put dots on the
words); real brand logo + @koolestpro in the bottom lockup.
Rows = the rebuild's top 3 improvements by impact, ranked in the audit: pack + per-jar
price on screen one, the 4.9 rating moved up from ~5,750px, and the heat level.
"""
import base64, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "flybyjing" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "flybyjing_chili-crisp-pdp_annotation.html"
PL, PT, PW = 640, 196, 380; K = PW / 450

def uri(p): return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
def ph(cx, cy): return round(PL + (19.5 + 1.0546 * cx) * K), round(PT + (59 + 1.0546 * cy) * K)
def conn(x1, y1, x2, y2):
    L = math.hypot(x2 - x1, y2 - y1); a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<div class="conn" style="left:{x1}px;top:{y1}px;width:{L:.1f}px;transform:rotate({a:.2f}deg);"></div>'
            f'<div class="dot" style="left:{x2-6}px;top:{y2-6}px;"></div>')

H = ph(8, 352); R = ph(8, 411); P = ph(8, 492)
ROWS = (300, 520, 740)
LINES = conn(500, ROWS[0] + 40, *H) + conn(500, ROWS[1] + 40, *R) + conn(500, ROWS[2] + 40, *P)

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>CRO Fix Annotation - Fly By Jing Chili Crisp - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Syne:wght@700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#2a2a2a;padding:40px;font-family:'DM Mono',monospace;}
#sheet{width:1080px;height:1080px;background:#F7F5F0;position:relative;margin:0 auto;overflow:hidden;}
.headline{position:absolute;top:52px;left:56px;right:56px;font-family:'Syne',sans-serif;font-weight:800;font-size:37px;color:#1a1a1a;line-height:1.12;letter-spacing:-0.6px;}
.headline em{font-style:normal;color:#AB2328;}
.pagetype{position:absolute;top:160px;left:56px;font-size:15px;letter-spacing:2px;text-transform:uppercase;color:#8a8478;}
.phone{position:absolute;left:__PL__px;top:__PT__px;width:__PW__px;height:__PH__px;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.18));}
.cal{position:absolute;left:56px;width:440px;}
.q{font-family:'Caveat',cursive;font-weight:700;font-size:40px;color:#850FFA;line-height:1.05;}
.a{font-family:'Caveat',cursive;font-weight:700;font-size:29px;color:#2e2e2e;line-height:1.15;margin-top:8px;}
.qb,.ab{display:inline-block;font-family:'DM Mono',monospace;font-weight:500;font-size:13px;letter-spacing:1px;border-radius:5px;padding:3px 8px;margin-right:8px;vertical-align:7px;}
.qb{background:#850FFA;color:#fff;} .ab{background:#FA9C0F;color:#1a1a1a;vertical-align:4px;}
.conn{position:absolute;height:2px;background:#bdb5a6;transform-origin:0 50%;}
.dot{position:absolute;width:12px;height:12px;border-radius:50%;background:#FA9C0F;box-shadow:0 0 0 4px rgba(250,156,15,0.22);}
.lock{position:absolute;bottom:44px;left:56px;display:flex;align-items:center;gap:14px;}
.lock .chip{background:#AB2328;border-radius:8px;padding:8px 12px;display:flex;}
.lock img{height:20px;display:block;}
.lock span{font-size:14px;color:#6b6558;}
</style></head>
<body>
<div id="sheet">
  <div class="headline">Any good? How much? How hot?<br>Answered <em>before</em> the scroll.</div>
  <div class="pagetype">Product Page (PDP) &middot; Fly By Jing Original Sichuan Chili Crisp</div>
  <img class="phone" src="__AFTER__" />
  __LINES__
  <div class="cal" style="top:__R1__px;">
    <div class="q"><span class="qb">Q1</span>"How hot is it?"</div>
    <div class="a"><span class="ab">FIX</span>Their own words, on the hero: intensely flavorful, not off-the-charts spicy.</div>
  </div>
  <div class="cal" style="top:__R2__px;">
    <div class="q"><span class="qb">Q2</span>"Is it any good?"</div>
    <div class="a"><span class="ab">FIX</span>4.9 stars from 2,459 reviews, under the photo. It sat about 5,750px down.</div>
  </div>
  <div class="cal" style="top:__R3__px;">
    <div class="q"><span class="qb">Q3</span>"What does $30 get me?"</div>
    <div class="a"><span class="ab">FIX</span>2 jars at $15 each. Every pack shows its per-jar price.</div>
  </div>
  <div class="lock"><span class="chip"><img src="__LOGO__" alt="Fly By Jing"></span><span>redesigned by @koolestpro &middot; concept, not a client</span></div>
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
    html = (HTML.replace("__AFTER__", uri(A / "phones" / "flybyjing_after_phone.png")).replace("__LOGO__", uri(A / "logo.png"))
            .replace("__LINES__", LINES).replace("__PL__", str(PL)).replace("__PT__", str(PT)).replace("__PW__", str(PW))
            .replace("__PH__", str(round(PW * 974 / 450)))
            .replace("__R1__", str(ROWS[0])).replace("__R2__", str(ROWS[1])).replace("__R3__", str(ROWS[2])))
    OUT.write_text(html, encoding="utf-8"); print("wrote", OUT, H, R, P)

if __name__ == "__main__": main()

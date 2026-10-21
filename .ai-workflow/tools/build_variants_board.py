#!/usr/bin/env python3
"""Build the X "variants board" debate post (added 2026-10-11, Ridwan's rule).

Every CRO Fix run builds 3-4 hero directions before picking one (see
docs/system/homepage-hero-patterns.md and docs/system/variants-board-post.md). This
tool turns those directions into a NEUTRAL 1600x900 X post: same brand, same
products, A/B/C/D side by side, "which one would you ship?". It never marks our
pick; the real carousel (which reveals the choice) always posts after it.

Usage:
  python3 .ai-workflow/tools/build_variants_board.py \
    --slug bala_bangles-homepage --brand-dir bala --page-type "Homepage" --brand "Bala" \
    --phones outputs/cro-fixes/bala/_variants/v1_phone.png ... (3 or 4, compose_mobile_flat output) \
    --labels "Range + labels" "Lifestyle first" "Full-bleed mood" "Headline first" \
    --headline "Same brand. 4 homepage heroes." --question "Which one would you ship?"
Then export with the page's own captureSheet() (see .ai-workflow/tools/export_sheet.py) to
outputs/cro-fixes/{brand-dir}/koolestpro_{slug}_variants-board.png
"""
import argparse, base64, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BG = ROOT / "outputs" / "Background 2.svg"


def uri(p):
    p = pathlib.Path(p)
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg"}[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


TPL = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Variants board - __BRAND__ - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0b0b0b;padding:30px;font-family:'DM Mono',monospace;}
#sheet{width:1600px;height:900px;position:relative;overflow:hidden;background:#121212;margin:0 auto;}
#sheet .bg{position:absolute;inset:0;background-image:url(__BG__);background-size:cover;background-position:center;}
.glow{position:absolute;left:50%;top:62%;transform:translate(-50%,-50%);width:1300px;height:620px;border-radius:50%;filter:blur(60px);background:radial-gradient(ellipse,rgba(250,156,15,0.22),rgba(133,15,250,0.18) 45%,transparent 70%);}
.head{position:absolute;top:44px;left:0;right:0;text-align:center;z-index:2;}
.head h1{font-family:'Syne',sans-serif;font-weight:800;font-size:54px;line-height:1.05;letter-spacing:-1px;color:#fff;}
.head h1 em{font-style:normal;color:#FA9C0F;}
.head .pt{margin-top:14px;font-size:15px;letter-spacing:2.4px;text-transform:uppercase;color:rgba(255,255,255,.55);}
.row{position:absolute;top:286px;left:0;right:0;display:flex;justify-content:center;gap:__GAP__px;z-index:2;}
.col{display:flex;flex-direction:column;align-items:center;}
.letter{width:58px;height:58px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:32px;color:#141414;background:#FA9C0F;box-shadow:0 8px 22px rgba(0,0,0,.45);margin-bottom:-22px;position:relative;z-index:3;}
.phone{display:block;width:__PW__px;height:__PH__px;filter:drop-shadow(0 22px 40px rgba(0,0,0,.7));}
.lab{margin-top:10px;font-size:15px;letter-spacing:.5px;color:rgba(255,255,255,.82);background:rgba(10,10,10,.55);border-radius:12px;padding:5px 12px;}
.lock{position:absolute;left:40px;right:40px;bottom:26px;display:flex;justify-content:space-between;align-items:center;z-index:3;}
.handle{font-size:16px;letter-spacing:1px;color:rgba(255,255,255,.78);background:rgba(10,10,10,.55);border-radius:12px;padding:6px 12px;}
.askpill{display:inline-block;margin-top:14px;font-family:'Syne',sans-serif;font-weight:800;font-size:19px;color:#fff;background:rgba(10,10,10,.6);border:1.5px solid rgba(250,156,15,.55);border-radius:20px;padding:7px 18px;}
.askpill b{color:#FA9C0F;}
</style></head><body>
<div id="sheet">
  <div class="bg"></div><div class="glow"></div>
  <div class="head"><h1>__HEADLINE__<br><em>__QUESTION__</em></h1><div class="pt">__PAGETYPE__ &middot; __BRAND__ &middot; concept, not a client</div><div class="askpill">Reply <b>__LETTERS__</b></div></div>
  <div class="row">__COLS__</div>
  <div class="lock"><div class="handle">@koolestpro</div></div>
</div>
<script>
async function waitReady(){ if(document.fonts&&document.fonts.ready) await document.fonts.ready;
  await Promise.all(Array.from(document.querySelectorAll('img')).map(i=>i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r;})));
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); }
async function captureSheet(){ await waitReady(); return await html2canvas(document.getElementById('sheet'),{scale:2,useCORS:true,allowTaint:true,backgroundColor:'#121212',logging:false}); }
window.captureSheet = captureSheet;
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--brand-dir", required=True)
    ap.add_argument("--brand", required=True)
    ap.add_argument("--page-type", required=True)
    ap.add_argument("--phones", nargs="+", required=True)
    ap.add_argument("--labels", nargs="+", required=True)
    ap.add_argument("--headline", required=True)
    ap.add_argument("--question", default="Which one would you ship?")
    a = ap.parse_args()
    assert 3 <= len(a.phones) <= 4 and len(a.phones) == len(a.labels), "need 3-4 phones, one label each"
    n = len(a.phones)
    pw = 238 if n == 4 else 280
    ph = round(pw * 974 / 450)
    gap = 78 if n == 4 else 100
    letters = "ABCD"[:n]
    cols = "".join(
        f'<div class="col"><div class="letter">{letters[i]}</div><img class="phone" src="{uri(ROOT / p)}">'
        f'<div class="lab">{html.escape(l)}</div></div>' for i, (p, l) in enumerate(zip(a.phones, a.labels)))
    out = (TPL.replace("__BG__", uri(BG)).replace("__COLS__", cols).replace("__PW__", str(pw)).replace("__PH__", str(ph))
           .replace("__GAP__", str(gap)).replace("__HEADLINE__", html.escape(a.headline))
           .replace("__QUESTION__", html.escape(a.question)).replace("__PAGETYPE__", html.escape(a.page_type))
           .replace("__BRAND__", html.escape(a.brand)).replace("__LETTERS__", ", ".join(letters[:-1]) + " or " + letters[-1]))
    dest = ROOT / "outputs" / "cro-fixes" / f"{a.slug}_variants-board.html"
    dest.write_text(out, encoding="utf-8")
    print("wrote", dest)


if __name__ == "__main__":
    main()

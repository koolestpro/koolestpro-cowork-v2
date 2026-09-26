#!/usr/bin/env python3
"""Build the Monthly Build Recap graphic (one post a month).

Ridwan's definition (2026-09-12): take the last four builds across brands
(CRO rebuilds + replo-rebuilds), show them OVERLAPPING in a fanned/angled
stack like his "HIGH CONVERTING PAGES" reference, with a headline and a
humanized promo caption. NOT four screens of one template.

2026-09-13 revision (Ridwan's corrections):
  * Caraway is dropped until its product image is fixed. The 4th build is
    swapped for OBVI (vibrant, strong above-the-fold hero).
  * ONE CONTINUOUS BACKGROUND. The old version pasted a `fanned_stack_4`
    strip that carried its own gradient, which left visible horizontal
    bands above and below the phones. The strip is now exported with
    `--bg-mode transparent` (see build_device_still.py) and laid over a
    single dark sheet with one central purple/orange glow, so the headline
    and the phones share the same background exactly like the reference.
  * Headline now uses the reference's heavy condensed-italic treatment
    (Archivo 900 italic, uppercase) instead of the wide Syne face.

Caption lives in docs/system/monthly-template-showcase-format.md.
Strip is regenerated with:
  build_device_still.py preview --style fanned_stack_4 --bg-mode transparent \\
    --screenshot <tapro_after_raw.png> --screenshot <gainful_after_raw.png> \\
    --screenshot <obvi_after_raw.png> --screenshot <materialkitchen_after.png> \\
    --output recap-4builds.png --width 2880 --height 1800
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "outputs" / "cro-fixes" / "_recap9"
STRIP = DIR / "recap-4builds.png"
OUT = DIR / "monthly-build-recap.html"

HANDLE = "@koolestpro | Shopify CRO &amp; UX"
HEAD = "HIGH CONVERTING PAGES"
# Kept configurable: swap for "RECENTLY SHIPPED" for a strictly time-boxed recap.
POST_SLUG = "monthly-build-recap"
POST_FOLDER = "outputs/cro-fixes/_recap9/monthly-build-recap.html"
POST_TITLE = "Monthly build recap: four high-converting pages"


def data_uri(path: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Monthly Build Recap - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#1b1b1b;padding:30px;font-family:'DM Mono',monospace;}
#sheet{position:relative;width:1080px;height:1080px;overflow:hidden;background:#0B0B0C;isolation:isolate;}

/* ONE background for heading + phones: base dark + a single central glow. */
#sheet .base{position:absolute;inset:0;background:#0B0B0C;}
#sheet .glow{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:1500px;height:1080px;border-radius:50%;
  background:radial-gradient(circle at 50% 46%,rgba(133,15,250,0.46),rgba(133,15,250,0.20) 38%,rgba(250,156,15,0.13) 64%,transparent 78%);
  filter:blur(64px);}
#sheet .glow-b{position:absolute;left:22%;top:74%;transform:translate(-50%,-50%);width:820px;height:560px;border-radius:50%;
  background:radial-gradient(circle,rgba(250,156,15,0.20),transparent 70%);filter:blur(70px);}

.handle{position:absolute;left:0;right:0;top:46px;text-align:center;font-family:'DM Mono',monospace;
  font-size:15px;letter-spacing:2.6px;text-transform:uppercase;color:rgba(255,255,255,0.52);}
.head{position:absolute;left:0;right:0;top:96px;text-align:center;font-family:'Anton',sans-serif;
  font-weight:400;font-size:102px;line-height:0.9;letter-spacing:0.5px;text-transform:uppercase;
  color:#fff;white-space:nowrap;transform:skewX(-8deg);text-shadow:0 12px 50px rgba(0,0,0,0.6);}

/* Transparent phone strip (autocropped to the phone cluster) — shares the sheet background. */
.strip{position:absolute;left:50%;top:170px;transform:translateX(-50%);width:1024px;height:auto;}

#dl-panel{max-width:1080px;margin:18px auto 0;display:flex;gap:10px;flex-wrap:wrap;}
.dl-btn{font-family:'DM Mono',monospace;font-size:13px;padding:10px 18px;border-radius:8px;border:1px solid #555;background:transparent;color:#ddd;cursor:pointer;}
.dl-btn:hover{border-color:#FA9C0F;color:#FA9C0F;}
#status{max-width:1080px;margin:10px auto;font-family:'DM Mono',monospace;font-size:12px;color:#999;}
</style>
</head>
<body>
<div id="sheet">
  <div class="base"></div>
  <div class="glow"></div>
  <div class="glow-b"></div>
  <div class="handle">__HANDLE__</div>
  <div class="head">__HEAD__</div>
  <img class="strip" src="__STRIP__" alt="Four recent builds">
</div>
<div id="dl-panel">
  <button class="dl-btn" onclick="dlSlide(0)">Download recap PNG</button>
  <button class="dl-btn" onclick="sendToPipeline()">Send to Content Pipeline</button>
</div>
<div id="status" aria-live="polite"></div>
<script>
const POST_BRAND  = 'Koolestpro';
const POST_SLUG   = '__POST_SLUG__';
const POST_TYPE   = 'Case Study';
const POST_FOLDER = '__POST_FOLDER__';
const TOTAL = 1;

async function waitAssets(el){
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const imgs=Array.from(el.querySelectorAll('img'));
  await Promise.all(imgs.map(i=>(i.complete&&i.naturalWidth>0)?Promise.resolve():(i.decode?i.decode().catch(()=>{}):new Promise(r=>{i.onload=r;i.onerror=r;}))));
}
async function dlSlide(idx){
  const el=document.getElementById('sheet');
  await waitAssets(el);
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  const canvas=await html2canvas(el,{scale:2,useCORS:true,allowTaint:true,backgroundColor:'#0B0B0C',logging:false});
  const a=document.createElement('a');
  a.href=canvas.toDataURL('image/png');
  a.download='koolestpro_monthly-build-recap.png';
  a.click();
  document.getElementById('status').textContent='Downloaded.';
}
function sendToPipeline(){
  const now=new Date();
  const dateStr=now.toISOString().slice(0,10).replace(/-/g,'');
  const data={
    id:POST_TYPE.toLowerCase()+'-'+POST_SLUG+'-'+dateStr,
    type:POST_TYPE, title:'__POST_TITLE__', slug:POST_SLUG, status:'Created', day:'',
    created:now.toISOString(), folder:POST_FOLDER,
    week:'Week of '+now.toLocaleDateString('en-US',{month:'long',day:'numeric'}),
    month:now.toLocaleDateString('en-US',{month:'long',year:'numeric'}),
    monthSlug:now.toISOString().slice(0,7)
  };
  console.log('EXPORT_POST_JSON',JSON.stringify(data));
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=POST_SLUG+'_pipeline.json';
  document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(a.href);
  document.getElementById('status').textContent='Exported. Open ridwan_content_system_updated.html and sync.';
}
</script>
</body>
</html>
"""


def main() -> None:
    html = (TEMPLATE.replace("__STRIP__", data_uri(STRIP))
            .replace("__HANDLE__", HANDLE).replace("__HEAD__", HEAD)
            .replace("__POST_SLUG__", POST_SLUG).replace("__POST_FOLDER__", POST_FOLDER)
            .replace("__POST_TITLE__", POST_TITLE))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()

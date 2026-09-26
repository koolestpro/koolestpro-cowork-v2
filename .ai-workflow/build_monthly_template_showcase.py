#!/usr/bin/env python3
"""Build a Monthly Template Showcase social graphic.

Format (2026-09-12): one post a month that shows a whole store template across a
4-phone strip, with a headline and a promo caption. The 4-phone image comes from
`build_device_still.py preview --style flat_packed_4` (2880x1800). This script
composes the feed graphic (1080x1350) around it.

Rules baked in (see CLAUDE.md standing hard rules):
  - headline is the topmost element; brand + @koolestpro are NOT at the top
  - @koolestpro appears once
  - concept brands are labelled as fictitious demo brands
  - headlines follow docs/system/cro-headline-system.md
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "outputs" / "templates" / "lumora_store-template_2026-08-28"
PREVIEW = SHOWCASE / "lumora_store-template-4phone.png"
OUT = SHOWCASE / "lumora_store-template_monthly-showcase.html"

# Headline (2 lines max, humanized). Angle: plain statement of the offer.
HEAD_L1 = "A full storefront,"
HEAD_L2 = "ready for your brand."
PAGETYPE = "STORE TEMPLATE &middot; SKINCARE / BEAUTY"
SPEC = "Home &middot; Range &middot; Product &middot; 12 products &middot; reskin from one file"
CTA = "See the live sample: koolestpro.com/live/lumora"
NOTICE = "Lumora Skin is a fictitious demo brand. Nothing here is a real client or a real result."
HANDLE = "@koolestpro"


def data_uri(path: pathlib.Path) -> str:
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}[path.suffix.lower()]
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Monthly Template Showcase - Lumora Skin - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#222;padding:30px;font-family:'DM Mono',monospace;}
#sheet{position:relative;width:1080px;height:1240px;overflow:hidden;background:#0E0E0E;}
#sheet .glow{position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);width:900px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(250,156,15,0.20),rgba(133,15,250,0.16) 46%,transparent 72%);filter:blur(46px);}
.head{position:absolute;left:0;right:0;top:62px;text-align:center;font-family:'Syne',sans-serif;font-weight:800;font-size:50px;line-height:1.06;letter-spacing:-1.2px;color:#fff;}
.head .accent{color:#FA9C0F;}
.pagetype{position:absolute;left:0;right:0;top:192px;text-align:center;font-family:'DM Mono',monospace;font-size:18px;letter-spacing:2.2px;text-transform:uppercase;color:rgba(255,255,255,0.5);}
.shot{position:absolute;left:50%;top:252px;transform:translateX(-50%);width:1052px;height:658px;border-radius:16px;border:1px solid rgba(255,255,255,0.09);box-shadow:0 30px 70px rgba(0,0,0,0.55);object-fit:cover;}
.spec{position:absolute;left:0;right:0;top:942px;text-align:center;font-family:'DM Mono',monospace;font-size:17px;color:rgba(255,255,255,0.62);}
.cta{position:absolute;left:0;right:0;top:1014px;text-align:center;font-family:'Syne',sans-serif;font-weight:700;font-size:23px;color:#FA9C0F;}
.cta .url{color:#fff;}
.lock{position:absolute;left:0;right:0;bottom:46px;text-align:center;}
.lock .notice{font-family:'DM Mono',monospace;font-size:14px;color:rgba(255,255,255,0.34);line-height:1.5;}
.lock .handle{margin-top:12px;font-family:'Syne',sans-serif;font-weight:700;font-size:22px;color:#fff;letter-spacing:0.5px;}
#dl-panel{max-width:1080px;margin:18px auto 0;display:flex;gap:10px;}
.dl-btn{font-family:'DM Mono',monospace;font-size:13px;padding:10px 18px;border-radius:8px;border:1px solid #555;background:transparent;color:#ddd;cursor:pointer;}
.dl-btn:hover{border-color:#FA9C0F;color:#FA9C0F;}
.dl-pipe{background:rgba(123,47,190,0.14);border-color:#7B2FBE;color:#c79bff;}
#status{max-width:1080px;margin:10px auto;font-family:'DM Mono',monospace;font-size:12px;color:#999;}
</style>
</head>
<body>
<div id="sheet">
  <div class="glow"></div>
  <div class="head">__HL1__<br><span class="accent">__HL2__</span></div>
  <div class="pagetype">__PAGETYPE__</div>
  <img class="shot" src="__PREVIEW__" alt="Lumora Skin store template across four screens">
  <div class="spec">__SPEC__</div>
  <div class="cta">__CTA__</div>
  <div class="lock">
    <div class="notice">__NOTICE__</div>
    <div class="handle">__HANDLE__</div>
  </div>
</div>

<div id="dl-panel">
  <button class="dl-btn" onclick="dlSlide(0)">Download monthly showcase PNG</button>
  <button class="dl-btn dl-pipe" onclick="sendToPipeline()">Send to Content Pipeline</button>
</div>
<div id="status" aria-live="polite"></div>

<script>
const POST_BRAND  = 'Koolestpro';
const POST_SLUG   = 'lumora_store-template-monthly';
const POST_TYPE   = 'Template Showcase';
const POST_FOLDER = 'outputs/templates/lumora_store-template_2026-08-28/lumora_store-template_monthly-showcase.html';
const TOTAL = 1;
function setStatus(m){ const s=document.getElementById('status'); if(s) s.textContent=m||''; }
async function waitAssets(el){
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const imgs=Array.from(el.querySelectorAll('img'));
  await Promise.all(imgs.map(i=>(i.complete&&i.naturalWidth>0)?Promise.resolve():(i.decode?i.decode().catch(()=>{}):new Promise(r=>{i.onload=r;i.onerror=r;}))));
}
async function dlSlide(idx){
  const el=document.getElementById('sheet');
  await waitAssets(el);
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  const canvas=await html2canvas(el,{scale:2,useCORS:true,allowTaint:true,backgroundColor:'#0E0E0E',logging:false});
  const a=document.createElement('a');
  a.href=canvas.toDataURL('image/png');
  a.download='koolestpro_lumora_monthly-template-showcase.png';
  a.click(); setStatus('Downloaded.');
}
function sendToPipeline(){
  const now=new Date();
  const data={
    id:'template-showcase-lumora-store-template-monthly-'+now.toISOString().slice(0,10).replace(/-/g,''),
    type:'Template Showcase',
    title:'A full storefront, ready for your brand.',
    slug:'lumora_store-template-monthly',
    status:'Created', day:'', created:now.toISOString(),
    folder:POST_FOLDER,
    week:'Week of '+now.toLocaleDateString('en-US',{month:'long',day:'numeric'}),
    month:now.toLocaleDateString('en-US',{month:'long',year:'numeric'}),
    monthSlug:now.toISOString().slice(0,7),
    assets:{images:['outputs/templates/lumora_store-template_2026-08-28/koolestpro_lumora_monthly-template-showcase.png',
                    'outputs/templates/lumora_store-template_2026-08-28/lumora_store-template-4phone.png']}
  };
  console.log('EXPORT_POST_JSON', JSON.stringify(data));
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download=POST_SLUG+'_pipeline.json'; document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(a.href); setStatus('Exported.');
}
</script>
</body>
</html>
"""


def main() -> None:
    html = (TEMPLATE
            .replace("__PREVIEW__", data_uri(PREVIEW))
            .replace("__HL1__", HEAD_L1).replace("__HL2__", HEAD_L2)
            .replace("__PAGETYPE__", PAGETYPE).replace("__SPEC__", SPEC)
            .replace("__CTA__", CTA.replace("koolestpro.com/live/lumora", "<span class='url'>koolestpro.com/live/lumora</span>"))
            .replace("__NOTICE__", NOTICE).replace("__HANDLE__", HANDLE))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()

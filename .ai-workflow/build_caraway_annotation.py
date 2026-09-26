#!/usr/bin/env python3
"""Build the standalone CRO annotated graphic — the "previous style" reference:
clear light background, big bold headline, centered phone, Q/A callouts around it,
each connected by a line + circle head to the exact element it changes.

This is separate from the carousel (track 1). It is the annotation post for X /
LinkedIn / Instagram, and the Q/A rows are drawn from the rebuild's TOP improvements.

Standing rules baked in:
  - brand + @koolestpro are NOT at the top (headline leads; lockup sits at the bottom)
  - @koolestpro appears once
  - real brand logo, rasterized from the brand's own SVG
  - real phone screenshot via compose_mobile_flat()
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "outputs" / "cro-fixes" / "caraway" / "_assets"
LOGO = ASSETS / "logo.png"
AFTER = ASSETS / "phones" / "caraway_after_phone.png"
OUT = ROOT / "outputs" / "cro-fixes" / "caraway_fry-pan-pdp_annotation.html"


def data_uri(path: pathlib.Path) -> str:
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg"}[path.suffix.lower()]
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CRO Annotation - Caraway Fry Pan PDP - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#222;padding:30px;font-family:'DM Mono',monospace;}
#stage{width:1080px;margin:0 auto;}
#sheet{position:relative;width:1080px;height:1080px;background:#F7F5F0;overflow:hidden;}
.head{position:absolute;left:0;right:0;top:36px;text-align:center;font-family:'Syne',sans-serif;font-weight:800;font-size:48px;line-height:1.08;letter-spacing:-1px;color:#14120E;}
.pagetype{position:absolute;left:0;right:0;top:156px;text-align:center;font-family:'DM Mono',monospace;font-size:19px;letter-spacing:2px;text-transform:uppercase;color:#8A8578;}
.phone{position:absolute;left:378px;top:250px;width:323px;height:700px;filter:drop-shadow(0 30px 46px rgba(20,18,14,0.22));}
.cal{position:absolute;width:292px;text-align:left;}
.q{display:flex;align-items:center;gap:9px;}
.a{display:flex;align-items:flex-start;gap:9px;margin-top:4px;}
.qb{width:30px;height:30px;border-radius:50%;background:#850FFA;color:#fff;font-family:'Syne',sans-serif;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.ab{width:30px;height:30px;border-radius:50%;background:#FA9C0F;color:#191919;font-family:'Syne',sans-serif;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.qt{font-family:'Caveat',cursive;font-weight:700;font-size:40px;line-height:1;color:#14120E;}
.at{font-family:'Caveat',cursive;font-weight:600;font-size:32px;line-height:1.05;color:#4A463C;}
.conn{position:absolute;height:3px;background:#2A2720;transform-origin:0 50%;}
.dot{position:absolute;width:13px;height:13px;border-radius:50%;background:#2A2720;border:3px solid #F7F5F0;}
.lock{position:absolute;left:0;right:0;bottom:38px;display:flex;align-items:center;justify-content:center;gap:16px;}
.lock img{height:30px;display:block;}
.lock .sep{width:1px;height:26px;background:#CFCABF;}
.lock .hd{font-family:'DM Mono',monospace;font-size:19px;color:#6E695E;}
#dl-panel{max-width:1080px;margin:18px auto 0;display:flex;gap:10px;flex-wrap:wrap;}
.dl-btn{font-family:'DM Mono',monospace;font-size:13px;padding:10px 18px;border-radius:8px;border:1px solid #555;background:transparent;color:#ddd;cursor:pointer;}
.dl-btn:hover{border-color:#FA9C0F;color:#FA9C0F;}
.dl-pipe{background:rgba(123,47,190,0.14);border-color:#7B2FBE;color:#c79bff;}
#status{max-width:1080px;margin:10px auto;font-family:'DM Mono',monospace;font-size:12px;color:#999;}
</style>
</head>
<body>
<div id="stage">
  <div id="sheet">
    <div class="head">How this page answers<br>the questions buyers ask.</div>
    <div class="pagetype">Product Page (PDP) &middot; Caraway Fry Pan</div>

    <img class="phone" src="__AFTER__" alt="">

    <!-- connector lines: text edge -> phone edge, circle head at the target.
         Targets are measured from the real composed phone (price y487,
         reviews y509, photo y708, add-to-cart y906 on the 1080 canvas). -->
    <div class="conn" style="left:326px;top:486px;width:52px;"></div>
    <div class="dot" style="left:371px;top:481px;"></div>
    <div class="conn" style="left:326px;top:905px;width:52px;"></div>
    <div class="dot" style="left:371px;top:900px;"></div>
    <div class="conn" style="left:701px;top:508px;width:53px;"></div>
    <div class="dot" style="left:695px;top:503px;"></div>
    <div class="conn" style="left:701px;top:707px;width:53px;"></div>
    <div class="dot" style="left:695px;top:702px;"></div>

    <!-- left: price + CTA -->
    <div class="cal" style="left:34px;top:449px;">
      <div class="q"><span class="qb">Q</span><span class="qt">How much is it?</span></div>
      <div class="a"><span class="ab">A</span><span class="at">Price sits right under the title.</span></div>
    </div>
    <div class="cal" style="left:34px;top:868px;">
      <div class="q"><span class="qb">Q</span><span class="qt">How do I buy?</span></div>
      <div class="a"><span class="ab">A</span><span class="at">Add to cart stays in reach.</span></div>
    </div>

    <!-- right: reviews + photo -->
    <div class="cal" style="left:754px;top:471px;">
      <div class="q"><span class="qb">Q</span><span class="qt">Is it any good?</span></div>
      <div class="a"><span class="ab">A</span><span class="at">Stars and reviews show inline.</span></div>
    </div>
    <div class="cal" style="left:754px;top:670px;">
      <div class="q"><span class="qb">Q</span><span class="qt">What is it?</span></div>
      <div class="a"><span class="ab">A</span><span class="at">The product photo fills the fold.</span></div>
    </div>

    <div class="lock">
      <img src="__LOGO__" alt="Caraway">
      <div class="sep"></div>
      <div class="hd">@koolestpro &middot; Shopify CRO &amp; UX</div>
    </div>
  </div>
</div>

<div id="dl-panel">
  <button class="dl-btn" onclick="dlSlide(0)">Download annotated PNG</button>
  <button class="dl-btn dl-pipe" onclick="sendToPipeline()">Send to Content Pipeline</button>
</div>
<div id="status" aria-live="polite"></div>

<script>
const POST_BRAND  = 'Koolestpro';
const POST_SLUG   = 'caraway_fry-pan-pdp';
const POST_TYPE   = 'CRO Fix';
const POST_FOLDER = 'outputs/cro-fixes/caraway_fry-pan-pdp_annotation.html';
const TOTAL = 1;

function setStatus(m){ const s=document.getElementById('status'); if(s) s.textContent=m||''; }
async function waitAssets(el){
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const imgs = Array.from(el.querySelectorAll('img'));
  await Promise.all(imgs.map(i => (i.complete && i.naturalWidth>0) ? Promise.resolve() : (i.decode ? i.decode().catch(()=>{}) : new Promise(r=>{i.onload=r;i.onerror=r;}))));
}
async function captureSheet(){
  const el = document.getElementById('sheet');
  await waitAssets(el);
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  return await html2canvas(el, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#F7F5F0', logging: false });
}
async function dlSlide(idx){
  try {
    setStatus('Preparing annotated PNG...');
    const canvas = await captureSheet();
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = 'koolestpro_caraway_fry-pan-pdp_annotated.png';
    a.click();
    setStatus('Annotated PNG downloaded.');
  } catch (e) { console.error(e); setStatus('Failed: ' + e.message); }
}
function sendToPipeline(){
  const now = new Date();
  const dateStr = now.toISOString().slice(0,10).replace(/-/g,'');
  const data = {
    id: POST_TYPE.toLowerCase().replace(/\s+/g,'-') + '-' + POST_SLUG + '-annotation-' + dateStr,
    type: POST_TYPE,
    title: 'How this page answers the questions buyers ask.',
    slug: POST_SLUG + '-annotation',
    status: 'Created',
    day: '',
    created: now.toISOString(),
    folder: POST_FOLDER,
    week: 'Week of ' + now.toLocaleDateString('en-US',{month:'long',day:'numeric'}),
    month: now.toLocaleDateString('en-US',{month:'long',year:'numeric'}),
    monthSlug: now.toISOString().slice(0,7),
    assets: { images: ['outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_annotated.png'] }
  };
  console.log('EXPORT_POST_JSON', JSON.stringify(data));
  const blob = new Blob([JSON.stringify(data,null,2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = POST_SLUG + '-annotation_pipeline.json';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
  setStatus('Exported. Open ridwan_content_system_updated.html and sync.');
}
</script>
</body>
</html>
"""


def main() -> None:
    html = TEMPLATE.replace("__LOGO__", data_uri(LOGO)).replace("__AFTER__", data_uri(AFTER))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()

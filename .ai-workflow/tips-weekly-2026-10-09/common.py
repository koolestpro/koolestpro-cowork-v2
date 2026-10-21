"""Shared V4 shell for the 2026-10-09 Tips week pack.

Slide CSS follows .ai-workflow/tips-v4/build_tips_v4.py (native 1080x1350, Syne 800 headlines,
DM Sans body >= 40px, pill labels, @koolestpro footer on every slide). Export JS keeps the
project's captureSlide/dlSlide/sendToPipeline mechanics so export_tip_slides.py drives it.
"""
import base64, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
O, P, M = "#FF9500", "#7B2FBE", "#E040A0"
AV = "https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2"


def icon(name, size=60, color=None, opacity=None):
    s = open(os.path.join(HERE, "icons", name + ".svg")).read()
    s = s.replace('width="1em" height="1em"', f'width="{size}" height="{size}"')
    if color:
        s = s.replace('stroke="#FF9500"', f'stroke="{color}"')
    if opacity is not None:
        s = s.replace("<svg ", f'<svg style="opacity:{opacity}" ', 1)
    return s


def img64(name):
    b = open(os.path.join(HERE, "ev", name), "rb").read()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode()


CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#111;color:#fff;font-family:'DM Sans',sans-serif;padding:32px 16px 80px}}
.wrap{{max-width:1120px;margin:0 auto}}
.chrome-h{{font-family:'Syne',sans-serif;font-weight:800;font-size:28px;margin-bottom:6px}}
.chrome-p{{color:rgba(255,255,255,.55);font-size:15px;line-height:1.5;margin-bottom:22px;max-width:760px}}
#viewport{{position:relative;width:540px;height:675px;overflow:hidden;border-radius:14px;margin:0 auto;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
#stage{{width:1080px;height:1350px;transform:scale(.5);transform-origin:top left}}
#track{{display:flex;width:max-content;transition:transform .35s ease}}
.navrow{{display:flex;align-items:center;justify-content:center;gap:16px;margin:16px 0 4px}}
.navbtn{{background:#222;border:1px solid #333;color:#fff;border-radius:30px;padding:8px 18px;cursor:pointer;font-size:14px}}
#pager{{font-size:14px;color:rgba(255,255,255,.6);min-width:60px;text-align:center}}
#dots{{display:flex;gap:8px;justify-content:center;margin:8px 0 18px}}
.dot{{width:8px;height:8px;border-radius:50%;background:#444;cursor:pointer}}.dot.active{{background:{O}}}
.swb{{position:absolute;right:10px;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;
  background:rgba(0,0,0,.55);color:#fff;font-size:26px;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:5}}
#download-panel{{max-width:760px;margin:0 auto 30px;background:#0a0a0a;border:1px solid #222;border-radius:12px;padding:18px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}
#download-panel button{{background:#1c1c1c;border:1px solid #333;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:13px}}
#download-status{{width:100%;text-align:center;font-size:12px;color:rgba(255,255,255,.45)}}
.section-label{{font-family:'Syne';font-weight:800;font-size:18px;margin:36px 0 12px;color:{O}}}
.section-divider{{height:1px;background:#222;margin:30px 0}}
.tabs-wrap{{max-width:760px;margin:0 auto}}
.tab-buttons{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}}
.tab-btn{{background:#1c1c1c;border:1px solid #333;color:#ccc;border-radius:8px;padding:7px 12px;cursor:pointer;font-size:13px}}
.tab-btn.active{{background:{O};color:#000;border-color:{O}}}
.tab-panel{{display:none;background:#0a0a0a;border:1px solid #222;border-radius:10px;padding:16px}}.tab-panel.active{{display:block}}
.tab-panel pre{{white-space:pre-wrap;font-family:'DM Sans',sans-serif;font-size:14px;line-height:1.55;color:#ddd}}
.copy-btn{{margin-top:10px;background:#222;border:1px solid #333;color:#fff;border-radius:6px;padding:6px 12px;cursor:pointer}}
.notes{{max-width:760px;margin:0 auto;font-size:14px;line-height:1.6;color:rgba(255,255,255,.65)}}
.notes b{{color:#fff}}
/* ---- V4 slide system (native 1080x1350) ---- */
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;background:#0B0B0D;color:#fff;font-family:'DM Sans',sans-serif;flex:none}}
.glowA{{position:absolute;width:900px;height:900px;border-radius:50%;left:-380px;top:-300px;
  background:radial-gradient(circle,rgba(255,149,0,.30),rgba(224,64,160,.10) 45%,transparent 70%);filter:blur(40px)}}
.glowB{{position:absolute;width:900px;height:900px;border-radius:50%;right:-420px;bottom:-360px;
  background:radial-gradient(circle,rgba(123,47,190,.38),transparent 70%);filter:blur(40px)}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.035) 1.5px,transparent 1.5px);background-size:44px 44px}}
.wm{{position:absolute;right:-60px;top:330px;line-height:0}}
.in{{position:absolute;inset:0;padding:88px 80px 128px;display:flex;flex-direction:column}}
.h{{font-family:'Syne',sans-serif;font-weight:800;letter-spacing:-3px;line-height:1.02}}
.o{{color:{O}}}
.eyebrow{{font-family:'Syne',sans-serif;font-weight:800;font-size:34px;letter-spacing:4px;color:{O}}}
.pill{{align-self:flex-start;font-family:'Syne',sans-serif;font-weight:800;font-size:34px;letter-spacing:1px;
  padding:14px 34px;border-radius:60px;color:#fff;background:linear-gradient(90deg,{O},{P})}}
.pill.ghost{{background:transparent;border:3px solid {O}}}
.tag{{font-family:'Syne',sans-serif;font-weight:800;font-size:28px;letter-spacing:1px;padding:8px 22px;border-radius:40px}}
.body{{font-size:42px;line-height:1.3;color:#C9C9CF;font-weight:500}}
.cap{{font-size:28px;color:rgba(255,255,255,.55);font-weight:500}}
.foot{{position:absolute;left:80px;right:80px;bottom:52px;display:flex;justify-content:space-between;align-items:center;
  font-size:27px;color:rgba(255,255,255,.62);font-weight:500}}
.foot b{{color:#fff;font-weight:700}}
.count{{background:rgba(11,11,13,.72);border:1px solid rgba(255,255,255,.18);border-radius:40px;padding:8px 22px;color:#fff}}
.card{{min-height:0;overflow:hidden;background:rgba(255,255,255,.035);border:2px solid rgba(255,255,255,.10);border-radius:32px}}
.icon{{width:104px;height:104px;border-radius:50%;background:rgba(255,149,0,.10);border:2px solid rgba(255,149,0,.35);
  display:flex;align-items:center;justify-content:center;flex:none}}
.row{{display:flex;align-items:center;justify-content:space-between}}
.shot{{display:block;width:100%;height:100%;object-fit:contain}}
"""


def foot(n, total):
    # no website on single graphics (Ridwan, 2026-10-09); carousels keep the n / N counter
    cnt = f'<span class="count">{n} / {total}</span>' if total > 1 else ''
    return f'<div class="foot"><span><b>@koolestpro</b> | Shopify CRO &amp; UX</span>{cnt}</div>'


def shell(inner, n, total, wm_icon=None, extra_bg=""):
    wm = f'<div class="wm">{icon(wm_icon, 520, "#FF9500", .06)}</div>' if wm_icon else ""
    return (f'<div class="slide" data-n="{n}"><div class="glowA"></div><div class="glowB"></div><div class="dots"></div>'
            f'{extra_bg}{wm}<div class="in">{inner}</div>{foot(n, total)}</div>')


def cta_slide(n, total, headline_html, line, save_line):
    return f"""<div class="slide" data-n="{n}"><div class="glowA"></div><div class="glowB"></div><div class="dots"></div>
<div style="position:absolute;inset:48px;border-radius:40px;padding:4px;background:linear-gradient(135deg,{O},{M},{P})">
 <div style="width:100%;height:100%;border-radius:36px;background:#0B0B0D"></div></div>
<div class="in" style="align-items:center;justify-content:center;text-align:center;padding:100px 110px 170px">
  <div style="width:240px;height:240px;border-radius:50%;padding:6px;background:linear-gradient(135deg,{O},{P})">
    <img src="{AV}" crossorigin="anonymous" style="width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:center top;background:#222"></div>
  <div class="h" style="font-size:92px;margin-top:52px">{headline_html}</div>
  <div class="body" style="margin-top:40px;max-width:840px">{line}</div>
  <div style="margin-top:48px;padding:30px 64px;border-radius:80px;background:linear-gradient(90deg,{O},{M},{P});font-family:Syne;font-weight:800;font-size:46px">Get a CRO audit &#8594;</div>
  <div style="margin-top:38px;font-size:40px;font-weight:700;color:{O}">koolestpro.com/services/cro-audit</div>
  <div style="margin-top:22px;font-size:34px;color:rgba(255,255,255,.65)">{save_line}</div>
</div>{foot(n, total)}</div>"""


JS = r"""
const TOTAL = __TOTAL__;
let current = 0;
const track = document.getElementById('track');
const stage = document.getElementById('stage');
const vp = document.getElementById('viewport');
const pager = document.getElementById('pager');
const dotsEl = document.getElementById('dots');
const slides = document.querySelectorAll('.slide');
function buildDots(){dotsEl.innerHTML='';slides.forEach((_,i)=>{const d=document.createElement('div');d.className='dot'+(i===0?' active':'');d.onclick=()=>goTo(i);dotsEl.appendChild(d);});}
function goTo(n){
  current=Math.max(0,Math.min(n,TOTAL-1));
  track.style.transform=`translateX(-${current*1080}px)`;
  pager.textContent=`${current+1} / ${TOTAL}`;
  document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('active',i===current));
  const s=document.getElementById('main-swb'); if(s) s.style.display=current>=TOTAL-1?'none':'';
}
buildDots(); goTo(0);
let startX=0;
vp.addEventListener('touchstart',e=>{startX=e.touches[0].clientX;});
vp.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-startX;if(Math.abs(dx)>40)goTo(current+(dx<0?1:-1));});
vp.addEventListener('mousedown',e=>{startX=e.clientX;});
vp.addEventListener('mouseup',e=>{const dx=e.clientX-startX;if(Math.abs(dx)>40)goTo(current+(dx<0?1:-1));});

async function waitForSlideAssets(slide){
  if(document.fonts&&document.fonts.ready) await document.fonts.ready;
  const images=Array.from(slide.querySelectorAll('img'));
  await Promise.all(images.map(img=>{
    if(img.complete&&img.naturalWidth>0) return Promise.resolve();
    if(img.decode) return img.decode().catch(()=>{});
    return new Promise(r=>{img.onload=r;img.onerror=r;});
  }));
}
function setDownloadStatus(m){const s=document.getElementById('download-status');if(s)s.textContent=m||'';}
async function captureSlide(idx){
  const slide=slides[idx]; if(!slide) throw new Error(`Slide ${idx+1} was not found.`);
  const toHide=document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
  toHide.forEach(el=>el.style.visibility='hidden');
  const prev={t:track.style.transform,tr:track.style.transition,st:stage.style.transform,w:vp.style.width,h:vp.style.height};
  track.style.transition='none'; track.style.transform=`translateX(-${idx*1080}px)`;
  stage.style.transform='none'; vp.style.width='1080px'; vp.style.height='1350px';
  try{
    await waitForSlideAssets(slide);
    await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
    return await html2canvas(slide,{scale:1,useCORS:true,allowTaint:false,backgroundColor:'#0B0B0D',logging:false,width:1080,height:1350});
  } finally {
    track.style.transform=prev.t; track.style.transition=prev.tr; stage.style.transform=prev.st; vp.style.width=prev.w; vp.style.height=prev.h;
    toHide.forEach(el=>el.style.visibility='');
  }
}
async function dlSlide(idx){
  try{
    setDownloadStatus(`Preparing slide ${idx+1}...`);
    const canvas=await captureSlide(idx);
    const a=document.createElement('a'); a.href=canvas.toDataURL('image/png');
    a.download=`koolestpro_${POST_SLUG}_slide${idx+1}.png`; a.click();
    setDownloadStatus(`Slide ${idx+1} downloaded.`);
  }catch(err){console.error(err);setDownloadStatus(`Slide ${idx+1} failed: ${err.message}`);}
}
async function dlAll(){for(let i=0;i<TOTAL;i++){await dlSlide(i);await new Promise(r=>setTimeout(r,300));}}
async function dlPDF(){
  try{
    const {jsPDF}=window.jspdf;
    const pdf=new jsPDF({orientation:'portrait',unit:'px',format:[1080,1350],compress:true});
    for(let i=0;i<TOTAL;i++){
      setDownloadStatus(`Adding slide ${i+1} of ${TOTAL} to PDF...`);
      const c=await captureSlide(i); if(i>0) pdf.addPage([1080,1350],'portrait');
      pdf.addImage(c.toDataURL('image/jpeg',0.92),'JPEG',0,0,1080,1350);
    }
    pdf.save(`koolestpro_${POST_SLUG}.pdf`); setDownloadStatus('PDF downloaded.');
  }catch(err){console.error(err);setDownloadStatus(`PDF failed: ${err.message}`);}
}
function openTab(el,id){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));el.classList.add('active');document.getElementById(id).classList.add('active');}
function copyText(id){const t=document.getElementById(id).querySelector('pre').innerText;navigator.clipboard.writeText(t).then(()=>{const b=document.querySelector(`[onclick="copyText('${id}')"]`);if(b){b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1800);}});}
function sendToPipeline(){
  const now=new Date();
  const data={id:POST_ID,type:POST_TYPE,title:POST_TITLE,slug:POST_SLUG,status:'Created',day:'',created:now.toISOString(),folder:POST_FOLDER,
    week:'Week of '+now.toLocaleDateString('en-US',{month:'long',day:'numeric'}),month:now.toLocaleDateString('en-US',{month:'long',year:'numeric'}),monthSlug:now.toISOString().slice(0,7)};
  console.log('EXPORT_POST_JSON',JSON.stringify(data));
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=POST_SLUG+'_pipeline.json';a.click();URL.revokeObjectURL(a.href);
  const s=document.getElementById('pipeline-status'); if(s) s.textContent='Exported. Open ridwan_content_system_updated.html and sync.';
}
"""


def page(meta, slides, tabs, notes_html):
    total = len(slides)
    tab_btns = "".join(
        f'<button class="tab-btn{" active" if i == 0 else ""}" onclick="openTab(this,\'{tid}\')">{html.escape(lbl)}</button>'
        for i, (tid, lbl, _) in enumerate(tabs))
    tab_panels = "".join(
        f'<div id="{tid}" class="tab-panel{" active" if i == 0 else ""}"><pre>{html.escape(txt)}</pre>'
        f'<button class="copy-btn" onclick="copyText(\'{tid}\')">Copy</button></div>'
        for i, (tid, lbl, txt) in enumerate(tabs))
    dl_btns = "".join(f'<button onclick="dlSlide({i})">Slide {i + 1}</button>' for i in range(total))
    swb = '<div class="swb" id="main-swb" onclick="goTo(current+1)">&#8250;</div>' if total > 1 else ""
    consts = (f"const POST_BRAND='Koolestpro';const POST_SLUG='{meta['slug']}';const POST_TYPE='Tip';"
              f"const POST_FOLDER='{meta['folder']}';const POST_ID='{meta['id']}';const POST_TITLE={meta['title']!r};")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(meta['page_title'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>{CSS}</style></head><body><div class="wrap">
<div data-chrome><div class="chrome-h">{html.escape(meta['page_title'])}</div>
<div class="chrome-p">{meta['lane']} &middot; Tips week pack 2026-10-09 &middot; status Created, waiting for Ridwan's review. Native 1080&times;1350 per slide, preview shown at 50%.</div></div>
<div class="section-label">&#9312; Post</div>
<div id="viewport"><div id="stage"><div id="track">{''.join(slides)}</div></div>{swb}</div>
<div class="navrow" data-chrome><button class="navbtn" onclick="goTo(current-1)">&#8249; Prev</button><span id="pager">1 / {total}</span><button class="navbtn" id="nav-next" onclick="goTo(current+1)">Next &#8250;</button></div>
<div id="dots" data-chrome></div>
<div id="download-panel">{dl_btns}<button onclick="dlAll()">All slides</button><button onclick="dlPDF()">PDF</button><div id="download-status"></div></div>
<div class="section-divider"></div><div class="section-label">&#9313; Notes and sources</div><div class="notes">{notes_html}</div>
<div class="section-divider"></div><div class="section-label">&#9314; Post Copy</div>
<div class="tabs-wrap"><div class="tab-buttons">{tab_btns}</div>{tab_panels}</div>
<div class="section-divider"></div>
<div style="max-width:760px;margin:0 auto"><div style="background:#0a0a0a;border:1px solid rgba(255,149,0,.18);border-radius:12px;padding:22px">
<div style="font-size:12px;font-weight:700;letter-spacing:2px;color:{O};margin-bottom:8px">CONTENT PIPELINE</div>
<div style="font-size:13px;color:rgba(255,255,255,.45);margin-bottom:14px">Downloads a .json for ridwan_content_system_updated.html. Status is always Created.</div>
<button onclick="sendToPipeline()" style="background:linear-gradient(90deg,{O},{M},{P});color:#fff;font-family:Syne;font-weight:700;font-size:14px;padding:12px 26px;border:none;border-radius:8px;cursor:pointer">Send to Content Pipeline &#8594;</button>
<div id="pipeline-status" style="font-size:12px;color:rgba(255,255,255,.4);margin-top:10px"></div></div></div>
</div>
<script>{consts}{JS.replace('__TOTAL__', str(total))}</script>
</body></html>"""

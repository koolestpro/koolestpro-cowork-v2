#!/usr/bin/env python3
"""Build the Caraway Fry Pan CRO 3-slide carousel.

New format (2026-09-10, Ridwan):
  Slide 1 = cover (real brand logo + brand asset, gradient glow, phone hero)
  Slide 2 = the before/after we have always made -> now IS the before/after post
  Slide 3 = the annotation -> now IS the annotated post
The separate ba-graphic.png / anno-graphic.png deliverables are retired; the
gradient glow background stays. Each of slide 2 and slide 3 must read as a
standalone post (brand bar + full title + handle), not just a carousel slide.

Claude authors the HTML here; assets are inlined as data URIs so the file is
self-contained for html2canvas.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "outputs" / "cro-fixes" / "caraway" / "_assets"

BG = ROOT / "outputs" / "Background 2.svg"
LOGO = ASSETS / "logo.png"  # rasterized from the real logo.svg (html2canvas cannot size an SVG data URI)
CUTOUT = ASSETS / "hero_cutout.png"
BEFORE = ASSETS / "phones" / "caraway_before_phone.png"
AFTER = ASSETS / "phones" / "caraway_after_phone.png"
OUT = ROOT / "outputs" / "cro-fixes" / "caraway_fry-pan-pdp_carousel.html"


def data_uri(path: pathlib.Path) -> str:
    mime = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }[path.suffix.lower()]
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CRO Fix - Caraway Fry Pan PDP - @koolestpro</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0e0e0e;color:#fff;font-family:'DM Mono',monospace;padding:40px 20px 80px;}
.lk-frame{max-width:588px;margin:0 auto;background:#1a1a1a;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);}
.lk-header{display:flex;align-items:flex-start;gap:10px;padding:14px 16px 10px;}
.lk-av{width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:16px;color:#fff;flex-shrink:0;overflow:hidden;padding:0;}
.lk-meta{flex:1;}
.lk-name{font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:#e0e0e0;display:flex;align-items:center;gap:6px;}
.lk-badge{background:#FF9500;color:#000;font-family:'DM Mono',monospace;font-size:8px;font-weight:700;padding:2px 6px;border-radius:3px;}
.lk-sub{font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.4);margin-top:2px;}
#viewport{width:540px;height:680px;overflow:hidden;position:relative;cursor:grab;margin:0 auto;background:#121212;}
#viewport:active{cursor:grabbing;}
#track{display:flex;transition:transform 0.32s cubic-bezier(0.4,0,0.2,1);will-change:transform;}
.slide{width:540px;height:680px;flex-shrink:0;position:relative;overflow:hidden;background:#121212;}
.slide .bg{position:absolute;inset:0;background-image:url(__BG__);background-size:cover;background-position:center;}
.glow{position:absolute;border-radius:50%;filter:blur(38px);pointer-events:none;}
.swb{position:absolute;right:0;top:50%;transform:translateY(-50%);width:32px;height:80px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,0.35);font-size:22px;cursor:pointer;z-index:20;background:linear-gradient(to right,transparent,rgba(0,0,0,0.25));user-select:none;}
#dots{display:flex;justify-content:center;gap:6px;padding:12px 0;}
.dot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.18);cursor:pointer;transition:all 0.2s;}
.dot.active{background:#FF9500;width:20px;border-radius:3px;}
#pager{text-align:center;font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.28);padding-bottom:8px;}
.lk-actions{display:flex;gap:20px;padding:10px 16px;border-top:1px solid rgba(255,255,255,0.06);}
.lk-action{font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.4);display:flex;align-items:center;gap:5px;cursor:pointer;}
.lk-action:last-child{margin-left:auto;}
.lk-caption{padding:10px 16px 16px;font-family:'DM Mono',monospace;font-size:12px;line-height:1.65;color:rgba(255,255,255,0.45);}
.lk-caption strong{color:#e0e0e0;}
#download-panel{max-width:588px;margin:20px auto 0;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;}
#download-panel h3{font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:rgba(255,255,255,0.45);margin-bottom:14px;letter-spacing:1.5px;text-transform:uppercase;}
#dl-buttons{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px;}
.dl-btn{font-family:'DM Mono',monospace;font-size:11px;padding:7px 14px;border-radius:6px;border:1px solid rgba(255,255,255,0.1);background:transparent;color:rgba(255,255,255,0.55);cursor:pointer;transition:all 0.2s;}
.dl-btn:hover{border-color:#FF9500;color:#FF9500;}
.dl-all{background:rgba(255,149,0,0.08);border-color:rgba(255,149,0,0.28)!important;color:#FF9500!important;}
.dl-pdf{background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);border:none!important;color:#fff!important;font-weight:700;}
.dl-pipe{background:rgba(123,47,190,0.14);border-color:rgba(123,47,190,0.4)!important;color:#c79bff!important;}
#download-panel p{font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.18);}
#download-status,#pipeline-status{font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.32);margin-top:10px;min-height:14px;}
.phone{display:block;filter:drop-shadow(0 26px 54px rgba(0,0,0,0.75));}
.brandbar{position:absolute;top:24px;left:34px;right:34px;display:flex;align-items:center;justify-content:space-between;z-index:6;}
.bb-left{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:1.2px;color:rgba(255,255,255,0.5);}
.bb-right{background:#F5F1E8;border-radius:8px;padding:7px 12px;display:flex;align-items:center;}
.brandlogo{height:17px;display:block;}
.content{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;text-align:center;}
h1.st{font-family:'Syne',sans-serif;font-weight:800;color:#fff;letter-spacing:-0.6px;line-height:1.08;}
.pagetype{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:1.6px;text-transform:uppercase;color:rgba(255,255,255,0.45);}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;}
.chip{display:inline-flex;align-items:center;gap:5px;border:1px solid rgba(250,156,15,0.4);background:rgba(250,156,15,0.08);color:rgba(255,255,255,0.85);font-family:'DM Mono',monospace;font-size:10px;padding:4px 10px;border-radius:20px;}
.chip b{color:#FA9C0F;}
.footer{font-family:'DM Mono',monospace;font-size:12.5px;color:rgba(255,255,255,0.72);display:flex;align-items:center;gap:8px;justify-content:center;}
.footer .arw{color:#FA9C0F;}
.badge-pill{font-family:'Syne',sans-serif;font-weight:800;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;}
.line{position:absolute;height:2px;background:linear-gradient(to right,rgba(250,156,15,0.12),rgba(250,156,15,0.9));transform-origin:0 50%;z-index:3;}
.pindot{position:absolute;width:9px;height:9px;border-radius:50%;background:#FA9C0F;box-shadow:0 0 0 3px rgba(250,156,15,0.22);z-index:4;}
.anno{position:absolute;left:0;width:228px;text-align:left;}
.anno .q{display:flex;align-items:center;gap:9px;}
.q-badge{width:22px;height:22px;border-radius:7px;background:linear-gradient(135deg,#850FFA,#B15CFF);color:#fff;font-size:13px;}
.q-text{font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#fff;line-height:1.2;}
.anno .a{display:flex;align-items:flex-start;gap:9px;margin-top:6px;margin-left:2px;}
.fix-badge{font-size:8.5px;letter-spacing:1px;background:#FA9C0F;color:#1a1a1a;border-radius:5px;padding:3px 6px;margin-top:1px;}
.a-text{font-family:'DM Mono',monospace;font-size:12px;color:rgba(255,255,255,0.66);line-height:1.4;}
.q-conn{position:absolute;left:11px;width:2px;background:rgba(255,255,255,0.16);}
</style>
</head>
<body>

<div class="lk-frame">
  <div class="lk-header">
    <div class="lk-av"><img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" onerror="this.style.display='none'"></div>
    <div class="lk-meta">
      <div class="lk-name">Ridwan Adekunle <span class="lk-badge">CRO</span></div>
      <div class="lk-sub">Shopify CRO &amp; UX - @koolestpro</div>
    </div>
  </div>

  <div id="viewport">
    <div id="track">

      <!-- ===== SLIDE 1 - COVER ===== -->
      <div class="slide">
        <div class="bg"></div>
        <div class="glow" style="left:50%;top:58%;transform:translate(-50%,-50%);width:430px;height:430px;background:radial-gradient(circle,rgba(250,156,15,0.30),rgba(133,15,250,0.20) 45%,transparent 70%);"></div>
        <div class="content" style="padding:76px 40px 30px;">
          <div class="brandbar">
            <div class="bb-left">@koolestpro</div>
            <div class="bb-right"><img class="brandlogo" src="__LOGO__" alt="Caraway"></div>
          </div>
          <h1 class="st" style="font-size:34px;">Price and proof,<br>reconnected.</h1>
          <div class="pagetype" style="margin-top:14px;">Product Page (PDP) &middot; Caraway Fry Pan</div>

          <div style="flex:1;width:100%;display:flex;align-items:center;justify-content:center;position:relative;">
            <img class="phone" src="__AFTER__" style="width:208px;height:450px;" />
            <div style="position:absolute;right:6px;top:14px;display:flex;align-items:center;gap:8px;background:rgba(12,12,12,0.55);border:1px solid rgba(250,156,15,0.35);border-radius:30px;padding:7px 14px;z-index:3;">
              <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:17px;color:#FA9C0F;">3</span>
              <span style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.82);line-height:1.15;">targeted<br>fixes</span>
            </div>
          </div>

          <div class="footer" style="margin-top:8px;font-size:14px;color:rgba(255,255,255,0.8);">Swipe to see the new look <span class="arw">&rarr;</span></div>
        </div>
      </div>

      <!-- ===== SLIDE 2 - BEFORE / AFTER (also stands alone) ===== -->
      <div class="slide">
        <div class="bg"></div>
        <div class="glow" style="left:50%;top:58%;transform:translate(-50%,-50%);width:470px;height:390px;background:radial-gradient(circle,rgba(250,156,15,0.20),rgba(133,15,250,0.15) 45%,transparent 70%);"></div>
        <div class="content" style="padding:74px 30px 26px;">
          <div class="brandbar">
            <div class="bb-left">@koolestpro</div>
          </div>
          <h1 class="st" style="font-size:29px;">Same product.<br>Different impression.</h1>
          <div class="pagetype" style="margin-top:11px;">Product Page (PDP) &middot; Caraway Fry Pan</div>
          <div class="chips" style="margin:13px 0 2px;">
            <div class="chip"><b>&#10003;</b>Price up front</div>
            <div class="chip"><b>&#10003;</b>Reviews inline</div>
            <div class="chip"><b>&#10003;</b>Photo in view</div>
          </div>
          <div style="flex:1;display:flex;align-items:center;justify-content:center;gap:18px;">
            <div style="display:flex;flex-direction:column;align-items:center;">
              <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:13px;letter-spacing:2px;color:rgba(255,255,255,0.5);margin-bottom:8px;">BEFORE</div>
              <img class="phone" src="__BEFORE__" style="width:196px;height:424px;" />
            </div>
            <div style="display:flex;flex-direction:column;align-items:center;">
              <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:13px;letter-spacing:2px;color:#FA9C0F;margin-bottom:8px;">AFTER</div>
              <img class="phone" src="__AFTER__" style="width:196px;height:424px;" />
            </div>
          </div>
        </div>
      </div>

      <!-- ===== SLIDE 3 - THE ANNOTATION ===== -->
      <div class="slide">
        <div class="bg"></div>
        <div class="glow" style="left:64%;top:56%;transform:translate(-50%,-50%);width:420px;height:500px;background:radial-gradient(circle,rgba(250,156,15,0.22),rgba(133,15,250,0.18) 48%,transparent 72%);"></div>
        <div class="brandbar">
          <div class="bb-left">@koolestpro</div>
        </div>
        <div class="content" style="padding:60px 30px 20px;">
          <h1 class="st" style="font-size:28px;">Every change<br>answers a question.</h1>
          <div class="pagetype" style="margin-top:8px;">Product Page (PDP) &middot; Caraway Fry Pan</div>

          <!-- legend: teaches the Q -> FIX psychology -->
          <div style="display:flex;align-items:center;justify-content:center;gap:9px;margin-top:13px;">
            <span class="q-badge badge-pill" style="width:20px;height:20px;border-radius:6px;">?</span>
            <span style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.72);">what they ask themselves</span>
            <span style="color:#FA9C0F;font-size:13px;">&rarr;</span>
            <span class="fix-badge badge-pill">FIX</span>
            <span style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.72);">the change I made</span>
          </div>

          <!-- phone centered as before; annotations on the left, line + dot connected -->
          <div style="position:relative;flex:1;width:480px;margin-top:4px;">
            <img class="phone" src="__AFTER__" style="position:absolute;left:272px;top:8px;width:200px;height:433px;" />

            <div class="line" style="left:236px;top:156px;width:36px;"></div>
            <div class="pindot" style="left:270px;top:152px;"></div>
            <div class="line" style="left:236px;top:272px;width:36px;"></div>
            <div class="pindot" style="left:270px;top:268px;"></div>
            <div class="line" style="left:236px;top:402px;width:36px;"></div>
            <div class="pindot" style="left:270px;top:398px;"></div>

            <div class="anno" style="top:136px;">
              <div class="q"><span class="q-badge badge-pill">Q</span><span class="q-text">"Is the price clear?"</span></div>
              <div class="a"><span class="fix-badge badge-pill">FIX</span><span class="a-text">Price pinned under the title.</span></div>
            </div>
            <div class="anno" style="top:252px;">
              <div class="q"><span class="q-badge badge-pill">Q</span><span class="q-text">"What is it?"</span></div>
              <div class="a"><span class="fix-badge badge-pill">FIX</span><span class="a-text">The product photo fills the fold.</span></div>
            </div>
            <div class="anno" style="top:382px;">
              <div class="q"><span class="q-badge badge-pill">Q</span><span class="q-text">"How do I buy?"</span></div>
              <div class="a"><span class="fix-badge badge-pill">FIX</span><span class="a-text">Add to cart stays in reach.</span></div>
            </div>
          </div>

          <div class="footer" style="font-size:12px;">Fewer decisions. Each one easy.</div>
        </div>
      </div>

    </div><!-- /track -->
    <div class="swb" id="main-swb" onclick="goTo(current+1)">&rsaquo;</div>
  </div><!-- /viewport -->

  <div id="dots"></div>
  <div id="pager">1 / 3</div>

  <div class="lk-actions" data-chrome>
    <div class="lk-action">&#128077; Like</div>
    <div class="lk-action">&#128172; Comment</div>
    <div class="lk-action">&#9851; Repost</div>
    <div class="lk-action">&#8599; Send</div>
  </div>

  <div class="lk-caption" data-chrome>
    <strong>Price and proof, reconnected.</strong><br>
    A $125 pan with 18,886 reviews can still read as unsure of itself. The fix did not add proof. It put the proof where the decision gets made.<br>
    <span class="lk-see-more">...see more</span>
  </div>
</div><!-- /lk-frame -->

<!-- Download Panel -->
<div id="download-panel">
  <h3>Export</h3>
  <div id="dl-buttons">
    <button class="dl-btn" onclick="dlSlide(0)">Slide 1</button>
    <button class="dl-btn" onclick="dlSlide(1)">Slide 2 (before/after)</button>
    <button class="dl-btn" onclick="dlSlide(2)">Slide 3 (annotation)</button>
    <button class="dl-btn dl-all" onclick="dlAll()">Download All PNGs</button>
    <button class="dl-btn dl-pdf" onclick="dlPDF()">Export PDF</button>
    <button class="dl-btn dl-pipe" onclick="sendToPipeline()">Send to Content Pipeline</button>
  </div>
  <p>PNG exports at 2x resolution (1080x1360px). Slide 2 and Slide 3 each work as a standalone post.</p>
  <div id="download-status" aria-live="polite"></div>
  <div id="pipeline-status" aria-live="polite"></div>
</div>

<script>
const POST_BRAND  = 'Koolestpro';
const POST_SLUG   = 'caraway_fry-pan-pdp';
const POST_TYPE   = 'CRO Fix';
const POST_FOLDER = 'outputs/cro-fixes/caraway_fry-pan-pdp_carousel.html';
const TOTAL = 3;

let current = 0;
const track = document.getElementById('track');
const pager = document.getElementById('pager');
const dotsEl = document.getElementById('dots');
const slides = document.querySelectorAll('.slide');

function buildDots() {
  dotsEl.innerHTML = '';
  slides.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'dot' + (i === 0 ? ' active' : '');
    d.onclick = () => goTo(i);
    dotsEl.appendChild(d);
  });
}
function goTo(n) {
  current = Math.max(0, Math.min(n, TOTAL - 1));
  track.style.transform = `translateX(-${current * 540}px)`;
  pager.textContent = `${current + 1} / ${TOTAL}`;
  document.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === current));
  document.getElementById('main-swb').style.display = current >= TOTAL - 1 ? 'none' : '';
}
buildDots();

let startX = 0;
const vp = document.getElementById('viewport');
vp.addEventListener('touchstart', e => { startX = e.touches[0].clientX; });
vp.addEventListener('touchend', e => { const dx = e.changedTouches[0].clientX - startX; if (Math.abs(dx) > 40) goTo(current + (dx < 0 ? 1 : -1)); });
vp.addEventListener('mousedown', e => { startX = e.clientX; });
vp.addEventListener('mouseup', e => { const dx = e.clientX - startX; if (Math.abs(dx) > 40) goTo(current + (dx < 0 ? 1 : -1)); });

async function waitForSlideAssets(slide) {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const images = Array.from(slide.querySelectorAll('img'));
  await Promise.all(images.map(img => {
    if (img.complete && img.naturalWidth > 0) return Promise.resolve();
    if (img.decode) return img.decode().catch(() => {});
    return new Promise(resolve => { img.onload = resolve; img.onerror = resolve; });
  }));
}
function setDownloadStatus(message) { const s = document.getElementById('download-status'); if (s) s.textContent = message || ''; }

async function captureSlide(idx) {
  const slide = slides[idx];
  if (!slide) throw new Error(`Slide ${idx + 1} was not found.`);
  const toHide = document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
  toHide.forEach(el => el.style.visibility = 'hidden');
  const prevTransform = track.style.transform;
  const prevTransition = track.style.transition;
  track.style.transform = `translateX(-${idx * 540}px)`;
  track.style.transition = 'none';
  try {
    await waitForSlideAssets(slide);
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    return await html2canvas(slide, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#121212', logging: false });
  } finally {
    track.style.transform = prevTransform;
    track.style.transition = prevTransition;
    toHide.forEach(el => el.style.visibility = '');
  }
}
async function dlSlide(idx) {
  try {
    setDownloadStatus(`Preparing slide ${idx + 1}...`);
    const canvas = await captureSlide(idx);
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = `koolestpro_caraway_fry-pan-pdp_carousel_slide${idx + 1}.png`;
    a.click();
    setDownloadStatus(`Slide ${idx + 1} downloaded.`);
  } catch (err) { console.error(err); setDownloadStatus(`Slide ${idx + 1} failed: ${err.message}`); }
}
async function dlAll() { for (let i = 0; i < TOTAL; i++) { await dlSlide(i); await new Promise(r => setTimeout(r, 300)); } }
async function dlPDF() {
  try {
    if (!window.jspdf || !window.jspdf.jsPDF) throw new Error('PDF library did not load.');
    if (!window.html2canvas) throw new Error('Canvas export library did not load.');
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [540, 680], compress: true });
    for (let i = 0; i < TOTAL; i++) {
      setDownloadStatus(`Adding slide ${i + 1} of ${TOTAL} to PDF...`);
      const canvas = await captureSlide(i);
      const imgData = canvas.toDataURL('image/jpeg', 0.92);
      if (i > 0) pdf.addPage([540, 680], 'portrait');
      pdf.addImage(imgData, 'JPEG', 0, 0, 540, 680);
    }
    setDownloadStatus('Saving PDF...');
    pdf.save('koolestpro_caraway_fry-pan-pdp.pdf');
    setDownloadStatus('PDF downloaded.');
  } catch (err) { console.error(err); setDownloadStatus(`PDF failed: ${err.message}`); }
}
function sendToPipeline() {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const data = {
    id:        POST_TYPE.toLowerCase().replace(/\s+/g, '-') + '-' + POST_SLUG + '-' + dateStr,
    type:      POST_TYPE,
    title:     'Price and proof, reconnected.',
    slug:      POST_SLUG,
    status:    'Created',
    day:       '',
    created:   now.toISOString(),
    folder:    POST_FOLDER,
    week:      'Week of ' + now.toLocaleDateString('en-US', { month: 'long', day: 'numeric' }),
    month:     now.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }),
    monthSlug: now.toISOString().slice(0, 7),
    assets: {
      images: [
        'outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_carousel_slide1.png',
        'outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_carousel_slide2.png',
        'outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_carousel_slide3.png'
      ]
    }
  };
  console.log('EXPORT_POST_JSON', JSON.stringify(data));
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = POST_SLUG + '_pipeline.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
  const s = document.getElementById('pipeline-status');
  if (s) s.textContent = 'Exported. Open ridwan_content_system_updated.html and sync.';
}
</script>
</body>
</html>
"""


def main() -> None:
    html = (
        TEMPLATE
        .replace("__BG__", data_uri(BG))
        .replace("__LOGO__", data_uri(LOGO))
        .replace("__CUTOUT__", data_uri(CUTOUT))
        .replace("__BEFORE__", data_uri(BEFORE))
        .replace("__AFTER__", data_uri(AFTER))
    )
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()

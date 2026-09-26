# Koolestpro-Cowork-V2 — Project Constitution

OpenCode + DeepSeek must follow these rules on every task. No exceptions.

**REFERENCE OUTPUT:** `outputs/tips/funnel-awareness-framework_2026-05-10.html`
This is the gold-standard output. Every new carousel MUST match its structure, JS patterns, and design quality.

---

## Stack
- Vanilla HTML + CSS + JavaScript — no frameworks
- `html2canvas` for PNG/PDF export (loaded via CDN)
- `jsPDF` for PDF export (loaded via CDN)
- Google Fonts: Syne (headings), DM Mono (labels/code/body)
- All styles inline — no external CSS files

CDN links (always use these exact versions):
```html
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
```

---

## Page Structure (3 Sections + Pipeline)

Every output HTML must have exactly this structure:

```
Section ① — LinkedIn Carousel Preview    (.lk-frame with #viewport)
Section ② — Individual Graphic Cards     (.gcard-wrap / .posts-shell)
Section ③ — Post Copy                    (.tabs-wrap with tab panels)
             Pipeline Export Panel        (sendToPipeline button)
```

Use `class="section-label"` and `class="section-divider"` between sections.
Both are hidden during export via `visibility:'hidden'`.

---

## Slide Dimensions

Slides are PORTRAIT (not square):
- Width:  **540px**
- Height: **680px**

```css
#viewport { width:540px; height:680px; overflow:hidden; position:relative; cursor:grab; margin:0 auto; background:#080808; }
.slide    { width:540px; height:680px; flex-shrink:0; position:relative; overflow:hidden; }
```

Do NOT use 1080×1080 square slides. Portrait is the standard.

---

## Page & Frame CSS

```css
body { background:#0e0e0e; color:#fff; font-family:'DM Mono',monospace; padding:40px 20px 80px; }

.lk-frame { max-width:588px; margin:0 auto; background:#1a1a1a; border-radius:14px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); }
.lk-header { display:flex; align-items:flex-start; gap:10px; padding:14px 16px 10px; }
.lk-av { width:42px; height:42px; border-radius:50%; overflow:hidden; flex-shrink:0; }

#track { display:flex; transition:transform 0.32s cubic-bezier(0.4,0,0.2,1); will-change:transform; }

/* Dots */
#dots { display:flex; justify-content:center; gap:6px; padding:12px 0; }
.dot { width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,0.18); cursor:pointer; transition:all 0.2s; }
.dot.active { background:#FF9500; width:20px; border-radius:3px; }

/* Pager */
#pager { text-align:center; font-family:'DM Mono',monospace; font-size:11px; color:rgba(255,255,255,0.28); padding-bottom:8px; }
```

---

## Swipe Button (.swb)

Each slide contains a `.swb` with `onclick="goTo(current+1)"`.
One additional `#main-swb` sits on the viewport itself.

```css
.swb { position:absolute; right:0; top:50%; transform:translateY(-50%); width:32px; height:80px; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.35); font-size:22px; cursor:pointer; z-index:20; background:linear-gradient(to right,transparent,rgba(0,0,0,0.25)); user-select:none; }
```

---

## Slide Design Standards

### Every slide MUST have:
1. **Dot grid texture** — `background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px`
2. **Glow blobs** — `position:absolute`, `radial-gradient`, `filter:blur(60-80px)`, `pointer-events:none`
3. **Top accent bar** — `position:absolute;top:0;left:0;right:0;height:3px` (gradient or solid color)
4. **Slide counter** — bottom-left: `N / TOTAL` in DM Mono 10px `rgba(255,255,255,0.2)`
5. **Handle** — bottom-right: `@koolestpro` in DM Mono 9px `rgba(255,255,255,0.15)`
6. **swb** — `<div class="swb" onclick="goTo(current+1)">›</div>`

### Cover slide extras:
- Large decorative number (`"01"`) as background watermark: `font-size:100px;color:rgba(255,255,255,0.04)`
- Eyebrow tag with border
- Main headline in Syne 800, 40-44px
- Sub-text in DM Mono
- "SWIPE →" footer with arrow line
- Top gradient bar using brand gradient

### Content slides:
- Accent color per slide (e.g. blue for cold, green for warm, orange/pink for hot)
- Large decorative number top-right: `position:absolute;right:28px;top:28px;font-size:80px;color:rgba(accent,0.08)`
- Colored dot + uppercase label at top-left
- Syne 800 headline, 32-36px
- Short colored rule bar below headline (`height:2px;width:40px`)
- DM Mono body text, 14-16px, `rgba(255,255,255,0.45-0.5)`

### CTA slide (always last):
- Avatar: **180px circle** with `border:2px solid rgba(255,149,0,0.4)`
- Syne 800 headline, 28-30px, centered
- DM Mono sub, 14-15px
- Gradient CTA button: `background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE)`
- Follow line + handle at bottom

---

## Gradient Rules (CRITICAL — export compatibility)

**CSS gradients on backgrounds: ALLOWED**
```css
background: linear-gradient(90deg, #FF9500, #7B2FBE);   /* ✅ works */
background: radial-gradient(circle, rgba(255,149,0,0.15), transparent 70%);  /* ✅ works */
```

**Gradient text — CSS OR SVG: FORBIDDEN**
```css
/* ❌ CSS gradient text — BREAKS html2canvas, text goes transparent */
background: linear-gradient(...);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```
```html
<!-- ❌ SVG gradient text — also banned. Too complex, inconsistent across files. -->
<text fill="url(#grad-...)">...</text>
```

**Text color rule: SOLID COLORS ONLY**
Use `color:#FF9500`, `color:#fff`, or themed accent colors directly. No gradients on text, ever.
```css
/* ✅ Correct — solid brand orange for highlighted text */
color: #FF9500;
/* ✅ Correct — themed accent for slide-specific text */
color: #3b82f6;   /* blue for cold/unaware slides */
color: #22c55e;   /* green for warm slides */
```

---

## Export System (CANONICAL — match reference file exactly)

### Hide method: `visibility:'hidden'` (NOT `display:'none'`)
Using `display:'none'` causes layout shift. Use `visibility` only.

### captureSlide function (use this exact pattern):
```javascript
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
    return await html2canvas(slide, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#080808',
      logging: false
    });
  } finally {
    track.style.transform = prevTransform;
    track.style.transition = prevTransition;
    toHide.forEach(el => el.style.visibility = '');
  }
}
```

### waitForSlideAssets (use this exact pattern):
```javascript
async function waitForSlideAssets(slide) {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const images = Array.from(slide.querySelectorAll('img'));
  await Promise.all(images.map(img => {
    if (img.complete && img.naturalWidth > 0) return Promise.resolve();
    if (img.decode) return img.decode().catch(() => {});
    return new Promise(resolve => { img.onload = resolve; img.onerror = resolve; });
  }));
}
```

### setDownloadStatus (use this exact pattern):
```javascript
function setDownloadStatus(message) {
  const status = document.getElementById('download-status');
  if (status) status.textContent = message || '';
}
```

### dlSlide / dlAll / dlPDF (always include try/catch + status messages):
```javascript
async function dlSlide(idx) {
  try {
    setDownloadStatus(`Preparing slide ${idx + 1}...`);
    const canvas = await captureSlide(idx);
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = `koolestpro_${POST_SLUG}_slide${idx + 1}.png`;
    a.click();
    setDownloadStatus(`Slide ${idx + 1} downloaded.`);
  } catch (err) {
    console.error(err);
    setDownloadStatus(`Slide ${idx + 1} failed: ${err.message}`);
  }
}

async function dlAll() {
  for (let i = 0; i < TOTAL; i++) {
    await dlSlide(i);
    await new Promise(r => setTimeout(r, 300));
  }
}

async function dlPDF() {
  try {
    if (!window.jspdf || !window.jspdf.jsPDF) throw new Error('PDF library did not load.');
    if (!window.html2canvas) throw new Error('Canvas library did not load.');
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [540, 680], compress: true });
    for (let i = 0; i < TOTAL; i++) {
      setDownloadStatus(`Adding slide ${i + 1} of ${TOTAL} to PDF...`);
      const canvas = await captureSlide(i);
      if (i > 0) pdf.addPage([540, 680], 'portrait');
      pdf.addImage(canvas.toDataURL('image/jpeg', 0.92), 'JPEG', 0, 0, 540, 680);
    }
    setDownloadStatus('Saving PDF...');
    pdf.save(`koolestpro_${POST_SLUG}.pdf`);
    setDownloadStatus('PDF downloaded.');
  } catch (err) {
    console.error(err);
    setDownloadStatus(`PDF failed: ${err.message}`);
  }
}
```

### Download status element (inside #download-panel):
```html
<div id="download-status" aria-live="polite"></div>
```

---

## Post Copy Tabs (MANDATORY — Section ③)

Every output HTML must include a tabbed post copy section with these 5 tabs:

```html
<div class="tabs-wrap">
  <div class="tab-buttons">
    <button class="tab-btn active" onclick="openTab(this,'tab-linkedin')">LinkedIn</button>
    <button class="tab-btn" onclick="openTab(this,'tab-ig')">Instagram</button>
    <button class="tab-btn" onclick="openTab(this,'tab-hook')">Hook Variations</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-angles')">Twitter Angles</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-thread')">Twitter Thread</button>
  </div>
  <!-- tab panels with <pre> content and Copy button per tab -->
</div>
```

Tab JS:
```javascript
function openTab(el, id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById(id).classList.add('active');
}
function copyText(id) {
  const text = document.getElementById(id).querySelector('pre').innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector(`[onclick="copyText('${id}')"]`);
    if (btn) { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1800); }
  });
}
```

---

## Pipeline Export (MANDATORY — after Section ③)

Required constants at top of script block:
```js
const POST_BRAND  = 'Koolestpro';
const POST_SLUG   = 'slug-from-topic';
const POST_TYPE   = 'Tip';   // 'Tip' | 'CRO Fix' | 'Case Study' | 'Personal'
const POST_FOLDER = 'outputs/tips/' + POST_SLUG + '_YYYYMMDD.html';
const TOTAL = N;  // total slide count
```

sendToPipeline function:
```javascript
function sendToPipeline() {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const data = {
    id:        POST_TYPE.toLowerCase() + '-' + POST_SLUG + '-' + dateStr,
    type:      POST_TYPE,
    title:     'ACTUAL POST TITLE HERE',  // never 'Brand — Type' — always the real title
    slug:      POST_SLUG,
    status:    'Created',
    day:       '',
    created:   now.toISOString(),
    folder:    POST_FOLDER,
    week:      'Week of ' + now.toLocaleDateString('en-US', { month: 'long', day: 'numeric' }),
    month:     now.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }),
    monthSlug: now.toISOString().slice(0, 7)
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
  if (s) s.textContent = '✓ Exported — open ridwan_content_system_updated.html and sync.';
}
```

Status is always `"Created"`. Day field always `""`. Never auto-set `"Published"`.

---

## Ridwan's Photos (CLOUDINARY — MANDATORY)

NEVER use local relative paths like `../../assets/ridwan/`. They break html2canvas.
Always use these Cloudinary URLs — CORS-enabled, work in every export.

| Use | URL |
|---|---|
| LK header + serious CTA | `https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss` |
| Smiling / warmer CTA | `https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2` |

**LK header avatar (42px):**
```html
<div class="lk-av">
  <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss"
       style="width:100%;height:100%;object-fit:cover;border-radius:50%;"
       onerror="this.style.display='none'">
</div>
```

**CTA slide avatar (180px with border ring):**
```html
<div style="width:180px;height:180px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">
  <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2"
       style="width:100%;height:100%;object-fit:cover;object-position:center top;"
       onerror="this.style.display='none'">
</div>
```

---

## Output Location
All generated files: `outputs/{type}/{slug}_{YYYYMMDD}.html`
- Tips: `outputs/tips/`
- CRO Fixes: `outputs/cro-fixes/`
- Case Studies: `outputs/case-studies/`

---

## Prioritization Order
1. Match reference file: `funnel-awareness-framework_2026-05-10.html`
2. Export compatibility — captureSlide/waitForSlideAssets pattern exactly
3. Gradient rule — backgrounds only, NO gradient text (CSS or SVG)
4. Cloudinary avatar URLs — never local paths
5. All 3 sections + pipeline export button present
6. Post copy tabs (all 5 platforms)

---

## Real Before/After & Annotation Graphics (Playwright Screenshots) — CANONICAL

When real visual evidence is available (a live URL for "before" + a local rebuild HTML for "after"), use **real Playwright screenshots**, not Figma mockups or invented graphics. See `.ai-workflow/tools/screenshot.py` + `.ai-workflow/tools/README.md` for the capture recipe (this sandbox is ARM64 — Playwright works, Puppeteer does not).

### Brand assets — real files only, never recreated (added 2026-09-04, hard rule — see CLAUDE.md's "REAL BRAND ASSETS ONLY — NEVER RECREATE A LOGO" for the full writeup)

The "after" rebuild's logo, and any other brand mark (badge, seal, icon set), must be the target's real file downloaded from their live site — locate it via the header `<img>`'s actual `src`/`srcset`, not a guessed favicon path or a stale schema.org `logo` field. Embed it as-is (base64), resized/cropped/background-removed if needed, but never redrawn as CSS text or shapes. **This applies to text-based/wordmark logos too** — a name set in a distinctive custom typeface is still an image asset, not something to retype in whatever web font happens to be loaded; the specific typeface is the brand identity, and a close-but-wrong font is a worse tell than an icon mismatch. Product photos follow the same real-asset-first logic (see "Prioritization Order" and the product-photo rules in CLAUDE.md). A rebuild whose logo doesn't match the real one — even subtly — undermines the whole "this is genuinely your page, fixed" CRO Fix pitch. If the real logo truly can't be retrieved, say so in the run summary rather than inventing one.

### Typography — big, bold, mobile-legible (upgraded 2026-07-12, applies to BOTH `#ba-graphic` and `#anno-graphic`)

**Why this exists:** GPT-image was tested (see "GPT-Image Alternative" below) and produced visually strong before/after and annotation graphics — but at real production volume (weekly `koolestpro-weekly-cro-fix`), the per-image API cost adds up fast. Ridwan confirmed 2026-07-12 he liked GPT-image's visual quality but wants the coded template to close that gap instead, since it's free to render and stays editable/pixel-consistent (the coded version's whole reason for existing per the tradeoffs list below). The actual V1CE build (2026-07-07) shipped its headline at `font-size:32px` on a ~1060px-wide canvas — that's roughly 3% of canvas width, which reads as an afterthought at mobile feed-thumbnail scale, not a scroll-stopping hook. That undersizing is the real gap versus GPT-image's output, not the coded approach itself.

**Corrected sizes (canvas ~1000-1100px wide — scale proportionally if canvas width changes materially):**

| Element | Font | Size | Weight | Notes |
|---|---|---|---|---|
| Headline (`.ba-sub` headline / `.an-headline`) | Syne | **52-60px** (was 32px) | 800 | Solid color only — `#fff` on dark `#ba-graphic`, `#151312` on light `#anno-graphic`. Never gradient text (hard rule below). Max 2 lines — if it wraps to 3, the copy is too long, cut it, don't shrink the font. |
| Sub-line / credit line (`.ba-sub2` / `.an-sub`) | DM Mono | **15-16px** (was 12px) | 400-500 | Still clearly secondary to the headline, just no longer squint-to-read. |
| Annotation caption labels (`.an-cap`) | Caveat (or current handwritten font) | 22-24px | 600 | These are auxiliary per-point labels, not the hook — current size is fine, don't inflate these, it clutters the arrow overlay. |
| Optional headline stat (if the audit surfaced a real, specific number — never fabricated) | Syne | 130-160px | 800 | Same treatment as the Tips carousel's "Big stat number" — only add this when there's a genuine verified number to show, not as decoration. |

**Test before shipping:** shrink the exported PNG to roughly phone-thumbnail size (a few hundred px wide, like it'd appear mid-scroll in a feed) and confirm the headline is still readable at a glance — that's the actual bar, not "readable at full size on a desktop monitor."

### Before/After template (`#ba-graphic`) — locked spec

- **1:1 square canvas.** Target ~1000×1000 (`box-sizing:border-box` so `width` already includes padding — makes hitting square trivial). Verify actual rendered aspect via Playwright `bounding_box()` after building; tune padding, don't guess.
- **BEFORE / AFTER labels sit top-center of their own image column, not rotated/slanted.** No diagonal arc-stamp corners, no pill badges, no long paragraph caption underneath — keep it to a short 1-line headline + small credit sub-line if there's room, nothing else. Headline uses the upgraded Typography sizing above, not a shrink-to-fit guess.
- **Numbered pins go on the AFTER image only**, for the **real fixes only** (not the "already working" wins — those belong on the separate annotation graphic). 3 pins is normal. Each pin = small circle + short horizontal leader line touching the image edge. No in-graphic text legend for what each number means — the numbers alone are the graphic; the meaning lives in the post caption/copy, not baked into the image.
- Reserve dedicated width for the pin+leader zone next to the AFTER column (e.g. after-column = image width + ~60px), not overflow past the container — keeps `overflow:hidden` (needed for the corner glow blobs) from clipping the pins.

### Annotation template (`#anno-graphic`) — locked spec

- **1:1 square canvas**, same box-sizing/verify-via-Playwright approach as above. Headline uses the upgraded Typography sizing above (52-60px, not 32px) — this graphic gets undersized just as often as `#ba-graphic` since it shares the same headline pattern.
- Up to **~8 points**, mixing the **real fixes** with genuine **pre-existing above-the-fold wins** — don't limit annotations to only what changed. Never fabricate a "win"; every point must trace to real, visible content in the actual screenshot.
- **Arrowheads, not dot markers.** A real triangular arrowhead (`M0,0 L9,4.5 L0,9 Z`), not a filled circle.
- **Vary the curve shapes, but keep the FINAL approach into the endpoint nearly flat/horizontal.** `marker-end` with `orient="auto"` rotates the arrowhead to match the path's tangent at the very last control point → endpoint segment. If that final segment is steep (e.g. an "elbow" curve whose last control point is bunched near the *start* rather than the end), the arrowhead points up/down instead of intuitively "into" the target and looks broken even though it's technically correctly rendered. Fix: for every curve, regardless of its earlier shape, always place the *second* (end-side) control point close to the endpoint's x AND within ~10px of its y — that alone guarantees a clean ~10-20° arrowhead approach. Vary the *first* (start-side) control point instead for visual variety (gentle arc, S-curve, steep dip, hook) — that's where the "different curve shapes" personality should live, not in the final approach.
- **Extend endpoints past the image's outer edge into the actual UI content**, not just to the raw screenshot boundary. Stopping exactly at the image edge (x=0 / x=full-width) reads as "pointing at nothing"; real page content is typically inset ~16-20px from the edge. Push the arrow endpoint roughly to where the real element starts (e.g. `x=20` instead of `x=0` on the left, `x=width-20` instead of `x=width` on the right) so it visibly touches the thing it's labeling.
- Anchor the overlay and caption divs to the **image stage element itself** (not the outer padded container) so `top:0/left:0` in the overlay's coordinate space lines up exactly with the image's own top-left corner — sidesteps the padding-box-vs-content-box offset bug entirely (see `feedback_verify_before_annotating` project memory).
- **1:1 coordinate mapping trick:** display the screenshot `<img>` at `width:390px` CSS. If the screenshot was captured at `device_scale_factor=2` and viewport width 390 (then possibly trimmed a few px off the top for cropping cleanup), a real element's Playwright `bounding_box()` page-y maps to displayed-y as `displayed_y ≈ page_y − (top_trim_px / 2)`. Sanity-check this empirically by sampling pixel colors in the actual cropped PNG at the predicted raw-y (raw_y = displayed_y × 2) before trusting it — don't ship on pure arithmetic.
- **Numbered pins on the before/after AFTER image should split across both sides** (left and right of the image), using the same left/right assignment as the annotation graphic for consistency — not all clustered on one side. Give the AFTER column dedicated pin-zones on both edges (e.g. 70px each) with the image offset via `margin-left`, and — same as above — extend leader lines a bit past the image's raw edge to touch the actual element rather than just the screenshot boundary.
- **The direct parent you anchor pins/leaders to MUST have `position:relative` itself — moving the DOM nodes into the right parent is not enough.** Confirmed bug (2026-07-07): pins were moved to be children of `.ba-img-wrap` (the pure image element, no sibling label) to fix a padding-box offset, but `.ba-img-wrap` had no `position` set, so its `position:absolute` children kept escaping to the *next* positioned ancestor up the tree (`.ba-col-after`, the same wrong box as before) — same visual bug, silently reintroduced. Any element you intend as an absolute-positioning anchor needs `position:relative` explicitly on itself, every time, not just "be the semantically correct box."
- **Don't assume a row's content spans edge-to-edge of the image — check where the real content actually sits before assigning it a left/right pin.** Confirmed bug (2026-07-07): a "Quantity: − 1 +" stepper is a compact, left-clustered control that sits nowhere near the image's right edge (unlike the full-width price/rating/delivery rows above it), so a RIGHT-side pin's leader floated in empty space past the control instead of touching it. Fix was reassigning that row to a LEFT pin to match where its label actually starts. Rule of thumb: full-width cards/banners (price, rating+badge, delivery notice) usually reach both edges and tolerate either side; compact left-aligned controls (labeled steppers, short pill rows) only reach the left — pin them left regardless of what side would otherwise balance the layout. Verify by cropping and looking at the actual exported PNG, not by assuming symmetry.

### Headlines must be scope-specific per post, never a reused generic template

Every `#ba-graphic` and `#anno-graphic` headline must describe what THIS specific audit actually found/fixed — never a fill-in-the-blank phrase like "Same Product, N Things Changed" or "Above The Fold, Annotated" reused across posts. Write the headline only after the caption list is finalized, so it can name the real, specific narrative (e.g. what the fixes have in common — trust signals, information order, missing proof — not just "stuff changed"). Two headlines in the same post (ba-graphic + anno-graphic) should also read as distinct from each other, not restate the same idea twice.

### CRITICAL — never ship curved arrows as a live `<svg>` element (html2canvas breaks it silently)

Confirmed by testing (2026-07-07): a live `<svg>` with `<path>` curves + `marker-end` arrowheads renders **perfectly in a real browser** (including Playwright's own `page.screenshot()`) but comes out **completely blank — the connecting curves vanish entirely, only bare caption text remains** — in the actual `html2canvas`-rendered PNG that the download button produces. This is a known `html2canvas` SVG-fidelity gap, not a coordinate or viewBox bug. Verifying with `page.screenshot()` alone is **not sufficient** — it bypasses html2canvas entirely and will pass even when the real export is broken.

**Fix: pre-rasterize the arrow overlay into a real PNG and embed it as a plain `<img>`,** exactly like the screenshots:
1. Build a standalone HTML file containing only the `<svg>` (transparent background) at the exact same `viewBox`/pixel dimensions used in the final graphic.
2. Render it with Playwright at `device_scale_factor=2` and screenshot the `<svg>` element with `omit_background=True` to get a transparent PNG.
3. Base64-embed that PNG and swap it in for the live `<svg>` (`<img class="an-svg" style="position:absolute;top:0;left:-310px;width:1010px;height:760px;" src="data:image/png;base64,...">` — same position/size the SVG had).

**Always verify against the ACTUAL html2canvas output, not a native screenshot.** Call the real `captureFixed()`/`captureSlide()` function via `page.evaluate()`, get `canvas.toDataURL()`, decode and save it as a real file, and *look at that exact file* before telling the user an export is fixed. This is the same class of mistake as the file:// canvas-tainting bug below — a check that passes for the wrong reason (native rendering vs. the real export pipeline) is worse than no check, because it creates false confidence.

### SVG export clipping rule (only matters if you're rasterizing the SVG per above)

Browsers (and Playwright's native screenshot, used only for the rasterization step) clip SVG content strictly to the element's declared `width`/`height` (its `viewBox` must match) — `overflow:visible` does nothing here either. Every arrow's `M`/`Q`/`C` coordinates, including control points, must stay inside the declared `viewBox` bounds. Clamp near-edge curve amplitudes (e.g. near y=0 or the bottom of a cropped screenshot) rather than letting a control point go negative or past the max.

### CRITICAL — local images + `file://` = broken downloads (canvas tainting)

If the HTML references screenshots or slide images via **relative local paths** (`src="../../assets/..."` or `src="outputs/.../slide.png"`) and the user opens the file directly by double-clicking it (`file://` protocol), every `html2canvas` capture in that file becomes a **tainted canvas**. `canvas.toBlob()` / `toDataURL()` then throw `SecurityError: Tainted canvases may not be exported`, and the download buttons silently do nothing — no console error visible to a non-technical user, just "nothing happens."

**Fix: base64-embed every local raster image used inside any exportable capture target** (`data:image/png;base64,...` inline `src`) before delivering the file. Remote images from a CORS-enabled host (e.g. Cloudinary) are fine as-is. This does inflate file size significantly (a handful of screenshots/slides can push the HTML to 10MB+) — that's an acceptable tradeoff for a local working file where "downloads actually work" matters more than file size.

**Always verify the fix, don't assume it.** Test via Playwright: `page.goto("file://" + path)`, then `page.evaluate()` calling the actual `captureFixed()`/`captureSlide()` function used by the real download button and attempting `canvas.toBlob()` inside a try/catch — confirm no `SecurityError` before telling the user downloads work.

---

## GPT-Image Alternative for Before/After & Annotation Graphics

Tested 2026-07-07 as an alternative to the coded `#ba-graphic`/`#anno-graphic` templates above, using the `gpt-image` skill's `edit.py` on the real "after" screenshot with a prompt describing each of the 8 target UI elements by name and top-to-bottom order (not coordinates — the model doesn't take pixel positions, only descriptions).

**Result:** surprisingly accurate at `--quality low` — all 8 numbered badges landed on the correct real elements (header, hero photo, title, rating+trust badge, price/benefit, delivery banner, style pills, quantity), with the underlying screenshot preserved unmodified. Output is a single flattened PNG, so it has no html2canvas/SVG/canvas-tainting risk at all — whatever the model draws is exactly what ships.

**Tradeoffs vs. the coded template:**
- No live coordinates to fix if the layout shifts — every regeneration re-infers placement from the prompt, so a re-run isn't guaranteed identical to the last one.
- Can't cheaply tweak a single label's wording or position after the fact — regenerating risks shifting other badges too. The coded version's individual `top`/`left` values are trivially editable.
- `--quality medium`/`high` edits reliably exceeded this sandbox's ~45s single-command ceiling and could not be backgrounded (background processes here do not survive past the invoking tool call, unlike the filesystem). `--quality low` completed in ~35s and looked clean; only fall back to background-polling patterns if a future sandbox actually persists processes across calls.
- Best used as a fast, low-effort comparison or a one-off social post image, not as the primary pipeline output — the coded template remains canonical for anything that needs to stay editable or pixel-consistent across regenerations.

**Decision (2026-07-12):** at weekly production volume (one `koolestpro-weekly-cro-fix` run every Saturday), GPT-image's per-image cost isn't worth it — the coded template is the default going forward, upgraded per the Typography section above to close the visual gap Ridwan noticed. GPT-image stays available as a manual fallback for a specific post that needs something the coded template genuinely can't do (e.g. a real photographic composite), not as the routine choice.

---
name: koolestpro-cro-content-maker-skill-e
description: "creates the graphics for the cro redesign, includes the before after, the carousel case study and also anotations showing what's been made"
---

# Koolestpro — CRO Content Maker (Skill E)

You are the **Koolestpro CRO Content Maker** — the final skill in Ridwan's CRO content pipeline. You take all upstream outputs and produce one complete, self-contained HTML file ready to use.

---

## WHAT YOU NEED TO START

1. **Skill A Audit Brief** — for numbered annotations, buyer psychology questions, decision guide points, and carousel story arc
2. **Skill D Captions** — all captions + tweets
3. If Skill D was not run as a separate step, derive captions from the Skill A brief directly

---

## OUTPUT: ONE HTML FILE — 4 SECTIONS

```
Section 01 — Figma Annotation Reference table (8 rows)
Section 02 — CRO Carousel (6 slides, downloadable)
Section 03 — Post Captions (6 tabs)
Section 04 — Export Everything (carousel slide downloads)
```

The file title: `Koolestpro — CRO Content Pack · [Brand Name]`

All sections use the **Koolestpro brand system**: `#030303` page background, `#080808` card background, orange→pink→purple gradient bar, Syne 800 headings, DM Mono body.

---

## SECTION 01 — FIGMA ANNOTATION REFERENCE

This replaces the old Angle 1 / Angle 2 / Angle 3 graphic sections.

**Purpose:** A reference table the user opens alongside Figma when building the 3 graphics manually. Does NOT generate the graphics — provides all data needed to build them in one place.

> **Supersedes/skip this whole section when real screenshots are available.** If there's a live "before" URL and a local rebuild HTML "after," don't send the user to Figma at all — build real, coded `#ba-graphic` (before/after) and `#anno-graphic` (annotation) sections directly in the HTML, using actual Playwright screenshots. The full locked spec (1:1 square canvas, top-center non-slanted labels, numbered pins on real fixes only, arrowhead SVG markers with varied curve shapes, and — critical — base64-embedding local images so downloads don't silently break on `file://`) lives in `.ai-workflow/project-constitution.md` under "Real Before/After & Annotation Graphics (Playwright Screenshots) — CANONICAL." Read that section before building either graphic. Only fall back to the Figma table below when no real before/after evidence exists to screenshot.

### Table structure (4 columns)

| # | Points to (page element) | Psychology question | Decision guide (what it achieves) |
|---|---|---|---|
| 1 | [element name] + [fix description] | "[buyer question]" italic | [what the change does for buyer's decision] |
| … | | | |
| 8 | | | |

### Implementation pattern

```html
<!-- ══ SECTION 01 ══ -->
<div class="wrap"><div class="sec-label">01 &nbsp;Figma Annotation Reference</div></div>
<div style="max-width:600px;margin:0 auto;padding:0 20px 0;">
<div style="width:540px;margin:0 auto;">

  <!-- Intro card -->
  <div style="background:#0d0d0d;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px 24px;margin-bottom:16px;">
    <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px;">Figma Design Reference</div>
    <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;">Use the table below to build your 3 graphics in Figma. Each row = one annotation number. The same numbered point covers all 3 graphic types — Before/After, Psychology Map, and Decision Guide — from a different angle.</div>
  </div>

  <!-- Table -->
  <div style="background:#0a0a0a;border:1px solid rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;">
    <!-- Header row -->
    <div style="display:grid;grid-template-columns:32px 1fr 1fr 1fr;gap:0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <div style="padding:10px 12px;font-family:'DM Mono',monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.25);border-right:1px solid rgba(255,255,255,0.06);">#</div>
      <div style="padding:10px 12px;font-family:'DM Mono',monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,149,0,0.7);border-right:1px solid rgba(255,255,255,0.06);">Points to (page element)</div>
      <div style="padding:10px 12px;font-family:'DM Mono',monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,149,0,0.7);border-right:1px solid rgba(255,255,255,0.06);">Psychology question</div>
      <div style="padding:10px 12px;font-family:'DM Mono',monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,149,0,0.7);">Decision guide (what it achieves)</div>
    </div>
    <!-- ODD data row (white bg): -->
    <div style="display:grid;grid-template-columns:32px 1fr 1fr 1fr;gap:0;border-bottom:1px solid rgba(255,255,255,0.05);">
      <div style="padding:14px 12px;font-family:'Syne',sans-serif;font-weight:800;font-size:13px;color:#FF9500;border-right:1px solid rgba(255,255,255,0.05);">1</div>
      <div style="padding:14px 12px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.7);line-height:1.55;border-right:1px solid rgba(255,255,255,0.05);"><strong style="color:#fff;display:block;margin-bottom:3px;">[Element name]</strong>[Fix description]</div>
      <div style="padding:14px 12px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.55);line-height:1.55;font-style:italic;border-right:1px solid rgba(255,255,255,0.05);">"[Buyer question]"</div>
      <div style="padding:14px 12px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.55);line-height:1.55;">[What it achieves]</div>
    </div>
    <!-- EVEN row: add background:rgba(255,255,255,0.01) to the row div -->
    <!-- Last row: no border-bottom -->
  </div>

  <!-- How to use note -->
  <div style="background:#0d0d0d;border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:14px 18px;margin-top:12px;display:flex;gap:12px;align-items:flex-start;">
    <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;flex-shrink:0;margin-top:1px;">How to use</div>
    <div style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);line-height:1.7;">In Figma, use annotation numbers 1–8 pointing to the same elements across all 3 graphics. <strong style="color:rgba(255,255,255,0.55);">Before/After</strong> — numbered dots on the After screenshot. <strong style="color:rgba(255,255,255,0.55);">Psychology Map</strong> — curved arrows from each question to the element. <strong style="color:rgba(255,255,255,0.55);">Decision Guide</strong> — curved arrows from each "what it achieves" label to the element. Column 2 = dot target. Column 3 = Psychology label. Column 4 = Decision Guide label.</div>
  </div>

</div>
</div>
<div class="divider"></div>
```

### Data source
- **Column 2:** `NUMBERED ANNOTATIONS FOR ANGLE 1` in Skill A — element name as `<strong>`, description as body
- **Column 3:** `BUYER PSYCHOLOGY MAP` in Skill A — Q1→Q8, italic, in quotes
- **Column 4:** `DECISION GUIDE ANNOTATIONS FOR ANGLE 3` in Skill A

Build as many rows as the Skill A brief specifies (typically 8). Alternate row background: even rows get `background:rgba(255,255,255,0.01)`. Last row: no `border-bottom`.

---

## SECTION 02 — CRO CAROUSEL (6 SLIDES)

```html
<!-- ══ SECTION 02 ══ -->
<div class="wrap" style="padding-top:0;padding-bottom:0;"><div class="sec-label">02 &nbsp;CRO Carousel — 6 Slides</div></div>
<div style="max-width:600px;margin:0 auto;padding:0 20px;">
  <!-- LK frame here -->
</div>
<div class="divider"></div>
```

### LinkedIn frame — CRITICAL IDs

```html
<div class="lk-frame-wrap">
  <div class="lk-chrome">
    <div class="lk-hdr">
      <div class="lk-av">
        <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss"
             alt="Ridwan Adekunle" onerror="this.style.display='none'">
      </div>
      <div>
        <div class="lk-name">Ridwan Adekunle</div>
        <div class="lk-meta">Shopify CRO &amp; UX · @koolestpro</div>
      </div>
      <div class="lk-dtag">#CROBreakdown</div>
    </div>

    <div id="lk-vp" style="width:540px;height:540px;overflow:hidden;cursor:grab;position:relative;user-select:none;">
      <div id="lk-track" style="display:flex;width:calc(540px*6);height:540px;transition:transform .32s cubic-bezier(.4,0,.2,1);">
        <div id="slide-1" class="slide">…</div>
        <div id="slide-2" class="slide">…</div>
        <div id="slide-3" class="slide">…</div>
        <div id="slide-4" class="slide">…</div>
        <div id="slide-5" class="slide">…</div>
        <div id="slide-6" class="slide">…</div>
      </div>
    </div>

    <div style="display:flex;justify-content:center;gap:5px;padding:10px 0 4px;background:#0a0a0a;border-top:1px solid rgba(255,255,255,0.04);">
      <div class="slide-ctr" id="sdots">
        <div class="sdot on"></div><div class="sdot"></div><div class="sdot"></div>
        <div class="sdot"></div><div class="sdot"></div><div class="sdot"></div>
      </div>
    </div>

    <div class="lk-ftr">
      <div class="lk-reactions">👍 ❤️ &nbsp;Like · Comment · Repost</div>
      <button class="lk-cta-btn">Follow @koolestpro</button>
    </div>
  </div>
</div>
```

**ID rules (JS depends on these exact values):**
- Viewport: `id="lk-vp"` · Track: `id="lk-track"` · Dots: `id="sdots"` · Slides: `id="slide-1"` – `id="slide-6"`

### Slide download row (below LK frame, inside wrapper div)

```html
<div class="slide-dl-row">
  <button class="btn-g" onclick="dlSlide(0,'[brand]_cro_s1_cover')">S1 ↓</button>
  <button class="btn-g" onclick="dlSlide(1,'[brand]_cro_s2_problem')">S2 ↓</button>
  <button class="btn-g" onclick="dlSlide(2,'[brand]_cro_s3_diagnosis')">S3 ↓</button>
  <button class="btn-g" onclick="dlSlide(3,'[brand]_cro_s4_fix')">S4 ↓</button>
  <button class="btn-g" onclick="dlSlide(4,'[brand]_cro_s5_result')">S5 ↓</button>
  <button class="btn-g" onclick="dlSlide(5,'[brand]_cro_s6_cta')">S6 ↓</button>
  <button class="btn-grad" onclick="dlCarouselZip()">↓ All Slides ZIP</button>
  <button class="btn-grad" onclick="dlCarouselPDF()">↓ All Slides PDF</button>
</div>
```

### Slide content — use Skill A `CAROUSEL STORY ARC FOR ANGLE 4`

| Slide | `.ep` tag | Structure |
|---|---|---|
| 1 | CRO BREAKDOWN | `.sh1` large hook headline + glow |
| 2 | THE PROBLEM | `.sh2` + `.slist` issue bullets |
| 3 | THE DIAGNOSIS | `.sh2` + `.sb` explanation |
| 4 | THE FIX | `.sh2` + numbered fix rows |
| 5 | THE RESULT | `.stat-num` key stat + outcome |
| 6 | WORK WITH ME | Avatar + "DM me AUDIT →" gradient button |

Every slide requires: `.s-gbar` top bar · `.sctr` `@koolestpro` · `.sattr` `koolestpro.com` · `.swb` chevron `›` · `#080808` bg + glow blobs

Slide 6 avatar:
```html
<div style="width:56px;height:56px;border-radius:50%;overflow:hidden;margin:0 auto 20px;flex-shrink:0;">
  <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss"
       style="width:100%;height:100%;object-fit:cover;object-position:center top;"
       onerror="this.style.display='none'">
</div>
```

---

## SECTION 03 — POST CAPTIONS (6 TABS)

```html
<!-- ══ SECTION 03 ══ -->
<div class="wrap" style="padding-top:0;padding-bottom:0;"><div class="sec-label">03 &nbsp;Post Captions</div></div>
<div style="max-width:600px;margin:0 auto;padding:0 20px;">
<div class="posts-shell">

  <div class="tnav">
    <button class="tbtn active" onclick="st('ba',this)">LI Before/After A</button>
    <button class="tbtn" onclick="st('bb',this)">LI Before/After B</button>
    <button class="tbtn" onclick="st('ps',this)">Psychology</button>
    <button class="tbtn" onclick="st('dg',this)">Decision Guide</button>
    <button class="tbtn" onclick="st('ca',this)">Carousel</button>
    <button class="tbtn" onclick="st('tw',this)">Tweets ×3</button>
  </div>

  <div class="tpanel active" id="tab-ba">
    <div class="plabel">LinkedIn · Before/After — Variation A (Locked Format)</div>
    <div class="plnote">Template: numbered questions → solution. Hook and conclusion customised per project. Middle locked.</div>
    <button class="cpbtn" onclick="cp('ba-t')">Copy</button>
    <div class="pcontent" id="ba-t">[caption BA]</div>
  </div>

  <div class="tpanel" id="tab-bb">
    <div class="plabel">LinkedIn · Before/After — Variation B</div>
    <div class="plnote">Same structure, different hook/conclusion — for A/B reach testing.</div>
    <button class="cpbtn" onclick="cp('bb-t')">Copy</button>
    <div class="pcontent" id="bb-t">[caption BB]</div>
  </div>

  <div class="tpanel" id="tab-ps">
    <div class="plabel">LinkedIn + Instagram · Customer Psychology</div>
    <div class="plnote">Lead with solution (what redesign answers), mention what was there before. Not problem-first.</div>
    <button class="cpbtn" onclick="cp('ps-t')">Copy</button>
    <div class="pcontent" id="ps-t">[psychology caption]</div>
  </div>

  <div class="tpanel" id="tab-dg">
    <div class="plabel">LinkedIn + Instagram · Decision Guide</div>
    <div class="plnote">Bold principle → element-by-element explanation of outcomes.</div>
    <button class="cpbtn" onclick="cp('dg-t')">Copy</button>
    <div class="pcontent" id="dg-t">[decision guide caption]</div>
  </div>

  <div class="tpanel" id="tab-ca">
    <div class="plabel">LinkedIn + Instagram · Carousel Caption</div>
    <button class="cpbtn" onclick="cp('ca-t')">Copy</button>
    <div class="pcontent" id="ca-t">[carousel caption]</div>
  </div>

  <div class="tpanel" id="tab-tw">
    <div class="plabel">Twitter/X · 3 Single Tweets</div>
    <div class="twvar">THREE VARIATIONS</div>
    <button class="cpbtn" onclick="cp('tw-t')">Copy all</button>
    <div class="pcontent" id="tw-t">[tweets separated by ────────────────────]</div>
  </div>

</div>
</div>
<div class="divider"></div>
```

### Caption content rules

**BA — LI Before/After A (locked format):**
Custom hook (1–2 lines) → numbered list 1️⃣–8️⃣ (`"[Buyer question]" → [change + why]`) → `Same product. Better answers. Better conversions.` + lesson → 5–6 hashtags

**BB — LI Before/After B:**
Audit-report hook ("I audited [brand] this week...") + same numbered structure + different close. Purpose: A/B reach test.

**PS — Psychology:**
`Your customer lands on [product] with [N] questions.` → each Q as paragraph (answer + what was there before) → `The proof was already there. The page just wasn't using it.` + follow CTA

**DG — Decision Guide:**
`High-converting pages don't ask for trust. They remove every reason not to give it.` → each element → bold name → outcome for buyer's decision (no questions, only outcomes) → `Design isn't decoration. It's direction.` + DM CTA

**CA — Carousel:** 5–8 lines. Opens with single most striking insight. Ends: swipe CTA + DM CTA.

**TW — Tweets:** The Rule / The Contrast / The Hot Take. Each under 280 chars. Separated by `────────────────────`

---

## SECTION 04 — EXPORT EVERYTHING

```html
<!-- ══ SECTION 04 ══ -->
<div class="wrap" style="padding-top:0;padding-bottom:0;"><div class="sec-label">04 &nbsp;Export Everything</div></div>
<div style="max-width:600px;margin:0 auto;padding:0 20px 0;">

  <!-- PIPELINE EXPORT — always first in this section -->
  <div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px;margin-bottom:20px;">
    <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px;">Content Pipeline</div>
    <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px;">Export this post to the content system. Downloads a <code>.json</code> file — open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
    <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px;">Send to Content Pipeline →</button>
    <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px;"></div>
  </div>

  <!-- CAROUSEL DOWNLOAD -->
  <div id="dlpanel">
    <div class="dltitle">Carousel Export</div>
    <div id="dlbtns"></div>
    <div class="dlnote">Carousel slides at 1080×1080px · ZIP bundles all slide PNGs · PDF bundles all slides as pages</div>
  </div>
</div>
```

`#dlbtns` populated by JS `DOMContentLoaded` — see JS section below.
Pipeline button calls `sendToPipeline()` — see JS section below.

---

## CSS (paste into `<style>` in `<head>`)

```css
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#030303;font-family:'DM Mono',monospace;color:#fff;min-height:100vh;padding-bottom:60px;}
.wrap{max-width:600px;margin:0 auto;padding:52px 20px 0;}
.sec-label{font-family:'DM Mono',monospace;font-size:9px;font-weight:500;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.2);margin-bottom:22px;display:flex;align-items:center;gap:12px;}
.sec-label::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.06);}
.divider{height:1px;background:linear-gradient(to right,rgba(255,149,0,0.25),rgba(123,47,190,0.18),transparent);margin:48px auto;max-width:600px;}
.lk-frame-wrap{width:540px;margin:0 auto;}
.lk-chrome{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,0.5);}
.lk-hdr{padding:12px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #f0f0f0;}
.lk-av{width:40px;height:40px;border-radius:50%;overflow:hidden;flex-shrink:0;background:linear-gradient(135deg,#FF9500,#7B2FBE);}
.lk-av img{width:100%;height:100%;object-fit:cover;border-radius:50%;}
.lk-name{font-family:'DM Mono',monospace;font-size:12px;font-weight:700;color:#111;line-height:1.2;}
.lk-meta{font-family:'DM Mono',monospace;font-size:10px;color:#888;}
.lk-dtag{margin-left:auto;font-family:'DM Mono',monospace;font-size:9px;color:#666;background:rgba(0,0,0,0.06);padding:3px 9px;border-radius:20px;border:1px solid rgba(0,0,0,0.07);}
.lk-ftr{padding:8px 14px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid #f0f0f0;}
.lk-reactions{font-family:'DM Mono',monospace;font-size:11px;color:#888;}
.lk-cta-btn{background:linear-gradient(90deg,#FF9500,#7B2FBE);color:#fff;border:none;border-radius:4px;font-family:'DM Mono',monospace;font-size:10px;font-weight:700;padding:5px 12px;cursor:pointer;}
.slide{width:540px;height:540px;flex-shrink:0;position:relative;background:#080808;overflow:hidden;}
.swb{position:absolute;right:0;top:50%;transform:translateY(-50%);width:32px;height:64px;background:rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;border-radius:4px 0 0 4px;cursor:pointer;z-index:20;color:#fff;font-size:18px;user-select:none;}
.swb:hover{background:rgba(255,149,0,0.4);}
.slide-ctr{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:5px;z-index:10;}
.sdot{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,0.3);transition:all .2s;}
.sdot.on{background:#fff;width:14px;border-radius:3px;}
.slide-dl-row{display:flex;gap:6px;padding:6px 0;justify-content:center;flex-wrap:wrap;}
.s-gbar{position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);z-index:10;}
.posts-shell{width:540px;margin:0 auto;background:#0d0d0d;border:1px solid rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;}
.tnav{display:flex;border-bottom:1px solid rgba(255,255,255,0.07);overflow-x:auto;scrollbar-width:none;}
.tnav::-webkit-scrollbar{display:none;}
.tbtn{flex-shrink:0;padding:10px 14px;font-family:'DM Mono',monospace;font-size:10px;font-weight:500;color:rgba(255,255,255,0.3);background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;white-space:nowrap;transition:color .2s;}
.tbtn.active{color:#FF9500;border-bottom-color:#FF9500;}
.tpanel{display:none;padding:22px 24px 26px;}
.tpanel.active{display:block;}
.plabel{font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:6px;}
.plnote{font-family:'DM Mono',monospace;font-size:9px;color:rgba(255,255,255,0.22);margin-bottom:14px;line-height:1.6;}
.cpbtn{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.09);border-radius:6px;padding:6px 14px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.4);cursor:pointer;margin-bottom:14px;transition:background .2s;}
.cpbtn:hover{background:rgba(255,149,0,0.12);border-color:rgba(255,149,0,0.3);color:#FF9500;}
.pcontent{font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.55);line-height:1.8;white-space:pre-wrap;background:rgba(0,0,0,0.3);padding:16px;border-radius:8px;border:1px solid rgba(255,255,255,0.05);}
.twvar{font-family:'DM Mono',monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.2);margin-bottom:8px;}
#dlpanel{width:540px;margin:0 auto;background:#0d0d0d;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:22px 24px;}
.dltitle{font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:16px;}
#dlbtns{display:flex;flex-wrap:wrap;gap:8px;}
.dlnote{font-family:'DM Mono',monospace;font-size:9px;color:rgba(255,255,255,0.14);margin-top:10px;line-height:1.6;}
.btn-g{padding:7px 12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.09);border-radius:7px;color:rgba(255,255,255,0.4);font-family:'DM Mono',monospace;font-size:10px;cursor:pointer;transition:background .2s;}
.btn-g:hover{background:rgba(255,255,255,0.1);}
.btn-grad{padding:7px 14px;background:linear-gradient(90deg,#FF9500,#7B2FBE);border:none;border-radius:7px;color:#fff;font-family:'DM Mono',monospace;font-size:10px;font-weight:700;cursor:pointer;transition:opacity .2s;}
.btn-grad:hover{opacity:.82;}
.sc{position:relative;z-index:5;padding:40px 40px 54px;height:100%;display:flex;flex-direction:column;}
.sctr{position:absolute;bottom:15px;left:24px;font-family:'Syne',sans-serif;font-size:10px;font-weight:300;letter-spacing:1.5px;color:rgba(255,255,255,0.18);z-index:10;}
.sattr{position:absolute;bottom:15px;right:22px;font-family:'DM Mono',monospace;font-size:9px;color:rgba(255,255,255,0.16);z-index:10;}
.ep{display:inline-block;background:#FF9500;color:#000;font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;margin-bottom:16px;width:fit-content;}
.sh1{font-family:'Syne',sans-serif;font-weight:800;font-size:54px;line-height:0.92;letter-spacing:-2px;color:#fff;}
.sh2{font-family:'Syne',sans-serif;font-weight:800;font-size:32px;line-height:1.0;letter-spacing:-0.8px;color:#fff;}
.sh3{font-family:'Syne',sans-serif;font-weight:700;font-size:22px;line-height:1.15;letter-spacing:-0.3px;color:#fff;}
.sb{font-family:'DM Mono',monospace;font-size:15px;color:rgba(255,255,255,0.55);line-height:1.65;margin-top:14px;}
.stag{display:inline-block;border:1px solid rgba(255,149,0,0.4);border-radius:20px;padding:4px 12px;font-family:'DM Mono',monospace;font-size:9px;color:#FF9500;margin-bottom:14px;}
.slist{list-style:none;margin-top:12px;}
.slist li{font-family:'DM Mono',monospace;font-size:14px;color:rgba(255,255,255,0.65);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);display:flex;gap:10px;align-items:baseline;line-height:1.5;}
.slist li::before{content:'→';color:#FF9500;flex-shrink:0;font-size:10px;}
.stat-num{font-family:'Syne',sans-serif;font-weight:800;font-size:114px;line-height:1;letter-spacing:-4px;color:#FF9500;}
.stat-lbl{font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.35);margin-top:4px;letter-spacing:1px;}
```

---

## JAVASCRIPT (use verbatim — paste before `</body>`)

```javascript
// ── POST IDENTITY (set these per brand before anything else) ──
const POST_BRAND  = 'Brand Name';                                 // e.g. 'Eco Bio Boutique'
const POST_SLUG   = 'brandslug_product-name';                     // e.g. 'ecobioboutique_cellulite-remover'
const POST_TYPE   = 'CRO Fix';
const POST_FOLDER = 'outputs/cro-fixes/' + POST_SLUG + '_content.html';

// ── PIPELINE EXPORT ──
function sendToPipeline() {
  const now = new Date();
  const dateStr = now.toISOString().slice(0,10).replace(/-/g,'');
  const data = {
    id:         POST_TYPE.toLowerCase().replace(/ /g,'-') + '-' + POST_SLUG + '-' + dateStr,
    type:       POST_TYPE,
    title:      POST_BRAND + ' — ' + POST_TYPE,
    slug:       POST_SLUG,
    status:     'Created',
    day:        '',
    created:    now.toISOString(),
    folder:     POST_FOLDER,
    week:       'Week of ' + now.toLocaleDateString('en-US',{month:'long',day:'numeric'}),
    month:      now.toLocaleDateString('en-US',{month:'long',year:'numeric'}),
    monthSlug:  now.toISOString().slice(0,7)
  };
  console.log('EXPORT_POST_JSON', JSON.stringify(data));
  const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = POST_SLUG + '_pipeline.json';
  a.click();
  URL.revokeObjectURL(a.href);
  const s = document.getElementById('pipeline-status');
  if(s) s.textContent = '✓ Exported — open ridwan_content_system_updated.html and sync.';
}

// ── TABS ──
function st(id,btn){
  document.querySelectorAll('.tpanel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tbtn').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  btn.classList.add('active');
}
// ── COPY ──
function cp(id){
  const el=document.getElementById(id);
  navigator.clipboard.writeText(el.innerText).catch(()=>{
    const r=document.createRange();r.selectNode(el);
    window.getSelection().removeAllRanges();window.getSelection().addRange(r);
    document.execCommand('copy');window.getSelection().removeAllRanges();
  });
}
// ── CAROUSEL (requires id="lk-vp", id="lk-track", id="sdots") ──
const TOTAL=6,W=540;let cur=0,startX=0,dragging=false;
const track=()=>document.getElementById('lk-track');
const vpEl=()=>document.getElementById('lk-vp');
const allDots=()=>document.querySelectorAll('#sdots .sdot');
function swipe(i){
  cur=Math.max(0,Math.min(TOTAL-1,i));
  const t=track();if(!t)return;
  t.style.transition='transform .32s cubic-bezier(.4,0,.2,1)';
  t.style.transform=`translateX(${-cur*W}px)`;
  allDots().forEach((d,idx)=>d.classList.toggle('on',idx===cur));
}
window.addEventListener('DOMContentLoaded',()=>{
  const vp=vpEl();const t=track();if(!vp||!t)return;
  vp.addEventListener('mousedown',e=>{dragging=true;startX=e.clientX;t.style.transition='none';});
  vp.addEventListener('touchstart',e=>{dragging=true;startX=e.touches[0].clientX;t.style.transition='none';},{passive:true});
  vp.addEventListener('mousemove',e=>{if(!dragging)return;t.style.transform=`translateX(${-cur*W+e.clientX-startX}px)`;});
  vp.addEventListener('touchmove',e=>{if(!dragging)return;t.style.transform=`translateX(${-cur*W+e.touches[0].clientX-startX}px)`;},{passive:true});
  const end=ex=>{if(!dragging)return;dragging=false;const diff=ex-startX;if(Math.abs(diff)>40)swipe(diff<0?cur+1:cur-1);else swipe(cur);};
  vp.addEventListener('mouseup',e=>end(e.clientX));
  vp.addEventListener('mouseleave',e=>end(e.clientX));
  vp.addEventListener('touchend',e=>end(e.changedTouches[0].clientX));
  // Populate #dlbtns
  const db=document.getElementById('dlbtns');if(!db)return;
  const labels=[['Cover',0],['Problem',1],['Diagnosis',2],['Fix',3],['Result',4],['CTA',5]];
  labels.forEach(([label,i])=>{
    const b=document.createElement('button');b.className='btn-g';
    b.textContent=`↓ Slide ${i+1} — ${label}`;
    b.onclick=()=>dlSlide(i,`cro_s${i+1}_${label.toLowerCase()}`);
    db.appendChild(b);
  });
  const bz=document.createElement('button');bz.className='btn-grad';
  bz.textContent='↓ Download All — ZIP';bz.onclick=dlCarouselZip;db.appendChild(bz);
  const bp=document.createElement('button');bp.className='btn-grad';
  bp.textContent='↓ Download All — PDF';bp.onclick=dlCarouselPDF;db.appendChild(bp);
});
// ── HQ CAPTURE (4× oversample → 1080×1080) ──
async function captureHQ(el){
  await document.fonts.ready;
  const toHide=document.querySelectorAll('.swb,.slide-ctr,.lk-ftr,.lk-hdr,.slide-dl-row,[data-chrome]');
  toHide.forEach(e=>e.style.visibility='hidden');
  const isPortrait=el.offsetHeight>550;
  const slW=540,slH=isPortrait?680:540;
  const outW=1080,outH=isPortrait?1360:1080;
  const raw=await html2canvas(el,{scale:4,useCORS:true,allowTaint:true,width:slW,height:slH,backgroundColor:'#080808',logging:false,imageTimeout:8000});
  toHide.forEach(e=>e.style.visibility='');
  const out=document.createElement('canvas');out.width=outW;out.height=outH;
  const ctx=out.getContext('2d');ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
  ctx.drawImage(raw,0,0,outW,outH);return out;
}
// ── dlSlide(i, name) — called by slide-dl-row buttons ──
async function dlSlide(i,name){
  const slide=document.getElementById(`slide-${i+1}`);if(!slide)return;
  const c=await captureHQ(slide);
  const a=document.createElement('a');a.href=c.toDataURL('image/png');
  a.download=`${name||'carousel_s'+(i+1)}.png`;a.click();
}
// ── dlCarouselZip() — called by slide-dl-row ZIP button ──
async function dlCarouselZip(){
  const zip=new JSZip();
  const names=['cover','problem','diagnosis','fix','result','cta'];
  for(let i=0;i<TOTAL;i++){
    const slide=document.getElementById(`slide-${i+1}`);if(!slide)continue;
    const c=await captureHQ(slide);
    zip.file(`carousel_s${i+1}_${names[i]}.png`,c.toDataURL('image/png').split(',')[1],{base64:true});
  }
  const blob=await zip.generateAsync({type:'blob'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='koolestpro_cro_carousel.zip';a.click();
}
// ── dlCarouselPDF() — called by slide-dl-row PDF button ──
async function dlCarouselPDF(){
  const {jsPDF}=window.jspdf;
  const pdf=new jsPDF({unit:'px',format:[1080,1080]});
  for(let i=0;i<TOTAL;i++){
    if(i>0)pdf.addPage();
    const slide=document.getElementById(`slide-${i+1}`);if(!slide)continue;
    const c=await captureHQ(slide);
    pdf.addImage(c.toDataURL('image/png'),'PNG',0,0,1080,1080);
  }
  pdf.save('koolestpro_cro_carousel.pdf');
}
```

---

## CDN SCRIPTS (before `</body>`, in this order)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
```

---

## TEXT COLOUR RULES (CRITICAL)

❌ NEVER CSS gradient text (`-webkit-background-clip:text`) — invisible in html2canvas exports
❌ NEVER SVG `<text>` wrappers for numbers or highlights
✅ ALL stats, accents, highlights: `color:#FF9500` plain CSS only

```html
<div style="font-family:'Syne',sans-serif;font-weight:800;font-size:114px;line-height:1;letter-spacing:-4px;color:#FF9500;">78%</div>
<span style="color:#FF9500;">word</span>
```

SVG allowed for decorative rule bars and arrow paths only — never for text.

---


---

## CANVAS FORMAT OPTIONS

The default CRO carousel uses **540×540px square** slides. A portrait option (540×680px) is available for breakdowns that benefit from more vertical breathing room.

### When to use portrait (540×680):
- Brand audit with 5+ distinct CRO fixes being shown
- Before/after comparisons with detailed annotations
- Any slide where content feels cramped at square dimensions

### When to keep square (540×540):
- Standard 6-slide CRO story arc
- Single-stat result slides
- When the brand's pages are predominantly desktop-focused and square looks better

**Portrait capture output:** `out.width=1080; out.height=1360;`
Detect in `captureHQ()`: `const isPortrait = el.offsetHeight > 550;`

---

## SLIDE VISUAL PATTERNS — OPTIONAL UPGRADES

These patterns can be added to any slide to break visual monotony across the 6-slide sequence. Use selectively — not every slide needs all patterns.

### Pattern A — Dot Grid Texture
Add to any slide for subtle depth:
```html
<div style="position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.018) 1px,transparent 1px);background-size:24px 24px;z-index:0;"></div>
```

### Pattern B — Watermark Slide Number
Add a faint large number behind content on diagnosis/fix slides:
```html
<div style="position:absolute;top:-10px;right:16px;font-family:'Syne',sans-serif;font-weight:800;font-size:80px;color:rgba(255,149,0,0.07);line-height:1;z-index:0;pointer-events:none;user-select:none;">3</div>
```

### Pattern C — Contextual Accent Color for CRO Element Slides
Instead of all slides using orange-only, each CRO element type gets a contextual color. Cover + CTA always use brand gradient — only middle slides use per-element accents.

```
Problem / UX friction  → Blue    #4099FF
Fix / Solution         → Green   #34C759
Result / Stat          → Orange  #FF9500  (brand — stays consistent)
CTA / Action           → Magenta #E040A0
```

Explanation card for colored concept slides:
```html
<div style="background:rgba(64,153,255,0.07);border:1px solid rgba(64,153,255,0.15);border-radius:8px;padding:14px 16px;margin-top:12px;">
  <!-- fix / problem description -->
</div>
```

### Pattern D — Single-Color Accent Top Bar (concept slides)
Replace the brand gradient bar with a single accent color on middle slides:
```html
<!-- Blue accent bar (problem / diagnosis slides) -->
<div style="position:absolute;top:0;left:0;right:0;height:3px;background:#4099FF;z-index:10;"></div>
<!-- Green accent bar (fix slides) -->
<div style="position:absolute;top:0;left:0;right:0;height:3px;background:#34C759;z-index:10;"></div>
```

### Layout Flexibility
Slides do **not** need identical structure. The brand consistency comes from Syne + DM Mono + black backgrounds, not from every slide following the same grid. Let the content determine the layout:
- Problem slide with bullets: `.sh2` + `.slist`
- Diagnosis slide with prose: `.sh2` + `.sb`  
- Fix slide with numbered rows: `.sh2` + numbered flex rows
- Result slide: `.stat-num` hero — less text, more number

## OUTPUT FILE

- Filename: `{brand-slug}_{product-slug}_content.html`
- Save to: `outputs/cro-fixes/`
- Single self-contained file — no external assets except Google Fonts + 3 CDN scripts above
- Zero Notion references anywhere in the file

---

## QUALITY CHECKLIST

- [ ] Section 01: Figma table — correct row count, 4 columns, data from Skill A, alternating row backgrounds
- [ ] Section 02: Carousel — 6 slides, `id="slide-1"`–`"slide-6"`, `id="lk-track"`, `id="lk-vp"`, `id="sdots"`
- [ ] Section 03: Captions — exactly 6 tabs (BA, BB, PS, DG, CA, TW), IDs match, copy buttons functional
- [ ] Section 04: Export — `#dlbtns` populated by JS, ZIP and PDF buttons functional
- [ ] Zero Notion references anywhere in file
- [ ] No CSS gradient text anywhere — `color:#FF9500` only
- [ ] `.swb` in `toHide` selector in `captureHQ`
- [ ] Body text `.sb` at 15px — never 13px
- [ ] Dot grid texture on at least 3 of 6 slides (Pattern A) — optional but recommended
- [ ] Watermark slide number on diagnosis/fix slides (Pattern B) — optional
- [ ] Contextual accent colors on middle slides if topic has distinct CRO phases (Pattern C) — optional
- [ ] Slide download buttons: `dlSlide(i, name)` signature
- [ ] ZIP/PDF buttons: `dlCarouselZip()` and `dlCarouselPDF()` — exactly these names
- [ ] Every slide has `.sctr` `@koolestpro` watermark
- [ ] Section 04: Pipeline Export panel present — `sendToPipeline()` button above carousel downloads
- [ ] `POST_BRAND`, `POST_SLUG`, `POST_TYPE`, `POST_FOLDER` constants set at top of script
- [ ] `pipeline-status` div exists in DOM for confirmation message
- [ ] If real before/after evidence exists: `#ba-graphic` + `#anno-graphic` built per `.ai-workflow/project-constitution.md`, not the Figma table — 1:1 square, non-slanted top-center BEFORE/AFTER labels, numbered pins split across BOTH sides of the AFTER image (not clustered on one side), arrowhead (not dot) markers with a flat final approach so they visibly point at the labeled element, leader lines/arrow endpoints extended into the actual UI content rather than stopping at the raw screenshot edge
- [ ] Every local raster image used inside any exportable capture target is base64-embedded (`data:image/png;base64,...`), not a relative path — verify with an actual Playwright `file://` + `toBlob()` test, not just a visual render, before calling downloads "done"
- [ ] **Any curved arrow / annotation overlay is a pre-rasterized `<img>`, never a live `<svg>`** — `html2canvas` silently drops SVG path curves in the real export even though they render fine in a normal browser or `page.screenshot()`. Verify by decoding the actual `canvas.toDataURL()` output from `captureFixed()`, not just a native screenshot — see "never ship curved arrows as a live `<svg>` element" in `.ai-workflow/project-constitution.md`
- [ ] GPT-image is NOT the default for these graphics — Ridwan tested and explicitly rejected it (2026-07-07, "the GPT image is not good enough, so we have to stick with our initial plan"). The coded `#ba-graphic`/`#anno-graphic` templates are canonical; only mention GPT-image if asked for a comparison.
- [ ] Every element you anchor pins/leaders to has `position:relative` set on itself explicitly — moving the overlay divs into the "correct" semantic parent is not enough if that parent has no `position` declared, its absolutely-positioned children will escape to the next positioned ancestor up the tree and silently reintroduce the same offset bug
- [ ] For each pinned row, check where the real content actually sits before choosing left vs. right — full-width cards/banners (price, rating+badge, delivery notice) reach both edges; compact left-aligned controls (labeled steppers, short pill rows) only reach the left and must be pinned left regardless of layout balance. Confirm by cropping the actual exported PNG, don't assume symmetry.
- [ ] Headline on both `#ba-graphic` and `#anno-graphic` is written AFTER the caption list is finalized and names this specific audit's actual finding — never a reused fill-in-the-blank phrase like "Same Product, N Things Changed." The two headlines in one post must also read as distinct from each other.

# CRO Fix — 3-Slide Carousel Format (updated 2026-09-10)

The CRO Fix post is a **3-slide story deck** (replaces the old 6-7 slide narrative
carousel). Reference implementation: `.ai-workflow/build_caraway_carousel.py` (the builder,
authored by Claude) → `outputs/cro-fixes/caraway_fry-pan-pdp_carousel.html` → exported
`outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_carousel_slide{1,2,3}.png`.

**Headlines on every slide follow `docs/system/cro-headline-system.md`** (one #1 finding,
a different angle per surface, max 2 lines).

## One CRO audit = multiple posts (updated 2026-09-12)

**Slide 2 and slide 3 each double as a standalone post**, plus there is a separate
clear-background annotated graphic. Together these feed Twitter's 3-posts-a-day floor and
give Instagram/LinkedIn variants:

**Posting rule (2026-09-27, Ridwan's instruction, every CRO Fix from now on):**
1. The **3-slide carousel** is always posted as one multi-image post on **LinkedIn, Instagram AND X**.
2. **Each of the four graphics** (cover = slide 1, before/after = slide 2, dark annotation = slide 3,
   clear-background annotated graphic) is **also posted on its own on X**.

That is 3 carousel posts + 4 X singles = 7 posts per audit, so every run writes **5 X captions**,
one per X post, each under 280 characters, never recycled between posts. In the review pack
(`{slug}_content.html`) they live in `div.tab-panel` blocks with these ids, which is what
`harvest_content.py` reads and `populate_sheet.py` schedules:

| Post | Image(s) | Tab id -> caption key | Slot (ET) |
|---|---|---|---|
| Carousel, LinkedIn | slides 1-3 | `tab-linkedin` -> `linkedin` | Wed 09:00 |
| Carousel, Instagram | slides 1-3 | `tab-ig` -> `instagram` | Wed 12:00 |
| Carousel, X | slides 1-3 | `tab-x-carousel` -> `x_carousel` | Wed 13:00 |
| Cover, X single | slide 1 | `tab-x-cover` -> `x_cover` | Thu 09:00 |
| Before/after, X single | slide 2 | `tab-x-ba` -> `x_ba` | Fri 09:00 |
| Dark annotation, X single | slide 3 | `tab-x-anno` -> `x_anno` | Sat 13:00 |
| Clear-bg annotation, X single | `*_annotated.png` | `tab-x-anno-graphic` -> `x_anno_graphic` | Sun 18:00 |

Social-content keys: `CRO-{BRAND}-X-CAROUSEL`, `-X-COVER`, `-X-BA`, `-X-ANNO`, `-X-ANNO-GRAPHIC`, each with `assetPath` (the image it posts with) and `captionKey`.

**Caption = image (Ridwan, 2026-09-28).** Write each X single while looking at the exact PNG it posts with. What each one says:
- **Cover:** the hook shown on slide 1.
- **Before/after:** the contrast, before vs after.
- **Annotations:** the numbered changes the image points at.
- **Single images:** never mention "carousel", "swipe" or "slides".

Since 2026-09-28 the four single keys have **no fallback**. If `tab-x-ba` (etc.) is missing, `populate_sheet.py` writes that row empty and holds it as Draft instead of borrowing another image's tweet. Run `python3 .ai-workflow/tools/caption_fit.py` before finishing and fix anything flagged for this item.
Reference run: Minimalist Niacinamide 10% PDP (2026-09-27), `outputs/cro-fixes/minimalist_niacinamide-10-serum-pdp_content.html`.

**Retired:** the standalone `ba-graphic.png` (slide 2 replaces it). **Back by request
(2026-09-12):** a standalone annotated graphic in the old "clear light background" style
(below). The old gradient glow background carries over to slides 2 and 3.

## The standalone annotated graphic — clear-background style (2026-09-12)

Ridwan wants the previous-style annotated image kept as its own post. Reference build:
`.ai-workflow/build_caraway_annotation.py` → `outputs/cro-fixes/caraway_fry-pan-pdp_annotation.html`
→ `outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_annotated.png` (1080×1080, scale 2).

Requirements (from the reference + the 2026-09-12 notes):

1. **Clear, light background** (e.g. `#F7F5F0`). Nothing busy behind the callouts.
2. **Big bold headline at the top**, max 2 lines (Syne 800 ≈48px). The headline is the
   topmost element.
3. **Centered real phone mockup** (`compose_mobile_flat()` output).
4. **Callouts around the phone, left and right, in a bold handwriting/marker font**
   (`Caveat` 700) large enough to read at feed size. Q/A style is required: a `Q` badge
   (purple) for the visitor's question and an `A` badge (orange) for the change we made.
5. **Connector = a straight line + a circle head.** Do NOT rely on a rendered SVG
   arrowhead (html2canvas drops live SVG / curves). A line div plus a filled circle at the
   target is the reliable, clear option. Point each callout at a **vertically well-separated**
   element (price / reviews / photo / cart).
6. **Content = the rebuild's TOP improvements**, one Q/A per improvement (see rule below).
7. **The headline leads** (topmost element). `@koolestpro` is allowed on every slide
   in a small lockup (revised 2026-09-18). The audited brand's real logo is on the cover only.

## Standing rules added 2026-09-12 (apply to every future build)

1. **The headline is always the topmost element.** `@koolestpro` may appear on every slide
   (small lockup, never a top bar). The audited brand's real logo appears on the **cover
   slide only**. (Revised 2026-09-18: the "handle once" limit was dropped.)
   (Track 1's current carousel predates this rule and is left as-is; do not copy its top
   brand bar into new builds.)
2. **The annotation must always be based on the rebuild's top improvements.** Before
   writing any Q/A, open the rebuild and rank the changes by impact; the annotation's rows
   are those top changes, each tied to the exact element it affects. Do not annotate minor
   or reworded tweaks, and do not reuse a previous audit's questions.


For slide 2 / slide 3 to work standalone, each carries the top-left `@koolestpro` handle,
its full headline, and the page-type line. Do not rely on the cover for context. The brand
logo itself stays on the cover only.

## The three slides

| # | Slide | Layout |
|---|---|---|
| 1 | Cover | Top-left `@koolestpro` + centered 2-line headline + page-type line + **real brand logo** (top-right) + one REAL iPhone mockup + "3 targeted fixes" chip + "Swipe to see the new look" |
| 2 | Before / After (standalone) | Top-left `@koolestpro` + centered 2-line headline + page-type line + change pills + two REAL iPhone mockups labelled BEFORE / AFTER |
| 3 | The Annotation (standalone) | Top-left `@koolestpro` + centered 2-line headline + page-type line + **Q→FIX legend** + Q&A rows on the left, phone centered on the right exactly as the before/after slide, each row line/dot-connected to its exact element + one closing line |

**The brand (Caraway) logo lives ONLY on the cover.** Slides 2 and 3 carry no brand logo. `@koolestpro` is fine on every slide (revised 2026-09-18).

## The Q→FIX device (why a stranger understands it)

The annotation's job is to teach the psychology: *the question is what the visitor is
silently thinking; the fix is the action we took.* A new viewer will not infer that, so
the slide makes it explicit:

- A **legend** under the headline: `[?] what they ask themselves → [FIX] the change I made`.
- Each row: a purple **`?` badge** + the question in quotes, then an orange **`FIX` badge**
  + the answer. Purple = the question in their head, orange = our change. Never render the
  question and the fix in the same style.

## Brand assets on the cover (2026-09-10)

- **Use the business's real logo on the cover** (rule: never recreate a logo). Caraway's
  real `logo.svg` is on a cream chip in the top-right of the cover only. Slides 2 and 3
  carry no brand logo.
- **Rasterize the SVG logo to PNG before embedding.** html2canvas cannot size an SVG data
  URI that has no intrinsic width/height, so the logo renders as an empty chip. Rasterize
  once (Playwright element screenshot at 3× with a transparent background) and embed the
  PNG. See `/tmp/raster_logo.py` pattern.
- Only add a product/brand cutout if it earns its place. A large blurred cutout behind the
  phone reads as a grey smudge; the real logo lockup + a strong phone hero is the clean
  default.

## Non-negotiables learned the hard way (do not regress)

1. **Background = the brand SVG PLUS the gradient glow.** Use `outputs/Background 2.svg`
   (base `#121212`, soft diagonal purple `#850FFA` → orange `#FA9C0F` band, faint white
   sheen, orange diamond top-right, purple diamond bottom-left), embedded as a data URI and
   set `background-size:cover`. On top of it keep a soft radial **gradient glow** behind
   the phone on every slide (it is the glow "always in the background"). Do not drop the
   glow on slide 3.

2. **Mobile mockup = `compose_mobile_flat()`, never a hand-built frame+screenshot.** From
   `.ai-workflow/skills/page-presentation-kit/scripts/build_device_still.py`:
   ```python
   from build_device_still import compose_mobile_flat
   phone, variant = compose_mobile_flat("path/to/screenshot.png")  # RGBA, 450x974, transparent bg
   phone.save("phone.png")
   ```
   Fills the FULL screen rect (no letterboxing) and renders the status bar in the
   notch-flanking slivers, exactly like the Template Showcase workflow. Embed the composed
   PNG as an `<img>` (aspect 450:974).

3. **Everything centered** on the cover and slide headings. Left-align only the Q&A
   annotation rows on slide 3.

4. **Headlines are max 2 lines.** Syne 800 is a wide face, check the render not the markup.
   Cover ≈34px; slide headings ≈29px. If it wraps to 3 lines, shorten the copy.

5. **Slide 3: the phone is centered in the same position as slide 2's AFTER phone** (do NOT
   shift it right or bleed it off the edge). Q&A rows sit on the left as a fixed canvas, a
   thin orange line + dot pin points each row to its exact target on the screenshot. Pick
   targets that are vertically well-separated (price block / product photo / Add to Cart) so
   the rows do not collide. Do NOT force two annotations onto adjacent elements.

6. **No generic AI-looking eyebrow badge at the top.** State the page type as a quiet
   centered line under the headline (e.g. `PRODUCT PAGE (PDP) · CARAWAY FRY PAN`). Satisfies
   the "state the page type" rule without looking templated.

7. **Watch the flex container width for floating chips.** A `flex:1` child inside
   `align-items:center` shrinks to content width, which is what made the "3 targeted fixes"
   chip overlap the phone once. Give it `width:100%` (or `position:relative` with the chip
   absolutely placed).

## Determinants (capture)

- Slide size `540×680`; `scale:2`; no downsample. `html2canvas({scale:2,useCORS:true,allowTaint:true,backgroundColor:'#121212',logging:false})`.
- Chrome-hiding via `visibility:'hidden'` on `[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap`; save/restore track transform+transition in `try/finally`; `waitForSlideAssets` + double rAF.
- Branding: Koolestpro orange `#FF9500` / reference orange `#FA9C0F` / purple `#850FFA`; Syne 800 display, DM Mono body; `@koolestpro` handle; real brand logo chip.
- Real assets only: real screenshots (base64-embedded), real brand product cutouts where used, **real logo rasterized from the brand's own SVG**. Never recreate a logo. No em dashes. Run captions through `humanizer`.
- Every output HTML still carries the mandated **Send to Content Pipeline** button + `sendToPipeline()` (status `Created`, day `""`, `POST_FOLDER` = the real carousel file).

## Export (local Mac)

```bash
python3 .ai-workflow/build_caraway_carousel.py     # writes the carousel HTML with inlined assets
python3 -m venv /tmp/cw_venv                       # once
/tmp/cw_venv/bin/python -m pip install playwright Pillow numpy
/tmp/cw_venv/bin/python -m playwright install chromium
/tmp/cw_venv/bin/python /tmp/export_carousel.py \
  outputs/cro-fixes/<slug>_carousel.html outputs/cro-fixes/<brand>/_new
```
Then copy `_new/slide{1,2,3}.png` to the final names and **look at every slide** before
calling it done. Cloud export needs `sandbox_cdn_route.py` (the sandbox blocks cdnjs/Google
Fonts); the Mac driver above does not.

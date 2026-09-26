TASK: Build the Template Showcase companion review page for KURA "The KURA Complete Board System" social-proof PDP (kura_pdp-02)

CONTEXT:
This is a Template Showcase content package (Step 5 of the content operating plan). The page showcased is `replo-rebuilds/brands/kura/pages/kura-pdp-02/index.html` — a social-proof product detail page ("The KURA Complete Board System") for KURA, a CONCEPT brand (not a real client) selling a stainless steel cutting board bundle. All 7 real deliverable assets already exist on disk in `outputs/templates/kura_pdp-02_2026-09-19/`:

1. `kura_pdp-02 cover.mp4` (video, 48.3s, laptop+phone side by side scrolling)
2. `kura_pdp-02 laptop.mp4` (video, 48.3s, desktop scroll-through)
3. `kura_pdp-02 mobile.mp4` (video, 41.6s, mobile scroll-through)
4. `kura_pdp-02 cover.png` (image, 1440x1080, laptop+phone still)
5. `kura_pdp-02-preview.png` (image, 2880x1800, 3-phone flat_packed_3 preview at hero/mid/footer scroll depths)
6. `kura_pdp-02-full-page.png` (image, 3148x5989, two-column full-page split)
7. `kura_pdp-02-mobile-strip.png` (image, 1080x1350, 2-column post-mode mobile strip — MANDATORY asset)

Build ONE self-contained HTML file: `outputs/templates/kura_pdp-02_2026-09-19/index.html`. Match the exact structural pattern of the existing reference file at `outputs/templates/kura_pdp-01_2026-08-31/index.html` (dark #050505 background, Syne + DM Mono fonts, orange #FF9500 accent, card grid for the 3 videos + 4 images, copy-block sections for source note / LinkedIn caption / X posts, pipeline export panel at the bottom). Do NOT invent new visual styling — copy this file's CSS structure faithfully, just swap the content and add a 7th card for the mobile-strip image (that reference file only had 6 cards; add card "07 · Mobile Strip (Full Page At A Glance)" as a 7th grid item).

FILES:
- outputs/templates/kura_pdp-02_2026-09-19/index.html

RULES:
- All 7 asset filenames above must be referenced with EXACT relative filenames. The video/cover.png filenames contain a literal space before "cover"/"laptop"/"mobile" — URL-encode that space as %20 in the src/href attribute, exactly like the reference file does (`kura_pdp-01%20cover.mp4` style). The four dash-named image files (preview, full-page, mobile-strip) have no spaces, reference them plainly.
- The 3 videos go in `<video controls src="...">` cards, the 4 images go in `<img src="..." alt="...">` cards, 7 cards total in the grid: 01 Cover Video, 02 Desktop Scroll-through, 03 Mobile Scroll-through, 04 Cover Image, 05 Preview Collage, 06 Full-Page Split, 07 Mobile Strip (Full Page At A Glance).
- Include a badge line: "Brand: KURA - Page: Product Detail Page (pdp-02, social-proof) - Source: replo-rebuilds live subfolder (replo-rebuilds/brands/kura/pages/kura-pdp-02/index.html)"
- Include an honesty-note div stating plainly: KURA is a concept/demo brand built to showcase page-building work, not a real client, and this page's testimonials, review counts, third-party lab test claims, and comparison-table figures are placeholder page copy written for the concept build, not real data.
- Include a "Source Note" copy-block: brand = KURA, page = Product Detail Page (pdp-02, social-proof structure), source = replo-rebuilds live subfolder, tier used = primary active pick (sortOrder 5, lowest eligible unused entry in replo-rebuilds-pages.json — not a fallback; kura-pdp-02 is active despite being a KURA page because it postdates the 2026-07-18 KURA retirement, which applied only to the five pre-cutoff KURA pages).
- Include the LinkedIn Caption copy-block and X Posts copy-block using EXACTLY the caption text provided below in NOTES — do not rewrite, paraphrase, or shorten it. Preserve real line breaks via `white-space: pre-wrap` on the LinkedIn caption paragraph, same as the reference file. Each X post is its own `.x-post` div, numbered 1-4 (there are 4 this run, one more than the reference file's 3, because the mobile-strip asset needs its own "full page at a glance" post distinct from the full-page-split post).
- Standard Pipeline Export Button: include the exact `.pipeline-panel` block and `sendToPipeline()` script from the reference file, with the constants given in NOTES below. The `dateStr` constant must be the literal string '2026-09-19' (real dashes, not '20260919').
- No em dashes anywhere in any text you write on the page (the caption copy given in NOTES already has none — preserve that, don't introduce any).
- This is a companion REVIEW page for Ridwan to check the build, not a live customer-facing page — keep it in the established dark/orange showcase-page style, not the KURA PDP's own light commerce style.

OUTPUT:
Complete self-contained HTML file, single file, no external JS dependencies beyond Google Fonts.

NOTES:
Pipeline constants:
```javascript
const dateStr    = '2026-09-19';
const POST_BRAND  = 'KURA';
const POST_SLUG   = 'kura_pdp-02';
const POST_TYPE   = 'Template Showcase';
const POST_FOLDER = 'outputs/templates/' + POST_SLUG + '_' + dateStr + '/index.html';
```
Pipeline record title field: 'KURA Complete Board System - Social-Proof PDP Showcase'

Header h1: "KURA Complete Board System - Social-Proof PDP Showcase"
Header sub-paragraph: "Complete product detail page for KURA's Complete Board System bundle, a stainless steel cutting board brand. Proof-stacking layout instead of a villain/hero story: bundle hero and pricing first, then trust reasons, an independent lab comparison against wood and plastic, a feature table against generic boards, a named testimonial, a wall of reviews, real customer photos, FAQs, then an email capture. Built from scratch as portfolio work. All assets rendered live from replo-rebuilds/brands/kura/pages/kura-pdp-02."

LinkedIn Caption (use verbatim, preserve line breaks exactly as shown):
Built KURA a second product page, this time leading with proof instead of a before-and-after story.

The Complete Board System bundles four pieces into one order. The page stacks its case in order: hero and bundle pricing first, then reasons to trust it (non-porous steel, dishwasher-safe, no warping), an independent lab comparison against wood and plastic, a feature-by-feature table against "the board you're using now," a named testimonial from a culinary instructor, a wall of 6,200-plus five-star reviews, real customer photos, then FAQs before the email capture.

Different structure than the villain/hero PDP I built for KURA a few weeks back. Same brand, different way of making the sale.

Portfolio build, not a live client site.

Need a product page like this for your store? DM me and I'll walk you through what a build would look like.

#ecommerce #webdesign #shopify #replo #CRO #uidesign

X Posts (use verbatim, 4 posts, preserve line breaks exactly, no hashtags on any of them):

X1:
KURA's second product page. This one leads with proof, not a story.

Bundle price up front, then a lab comparison vs wood and plastic, a feature table, 6,200+ reviews, real customer photos, FAQs, then the close.

Portfolio build, not a client site.

Want one built? DM me.

X2:
Three scroll depths of the same KURA product page: the bundle hero, a wall of reviewer photos and quotes, then the full footer nav.

Every fold has a different job: hero sells, mid-page proves it, footer closes it.

Portfolio build. DM if you want one for your store.

X3:
KURA's "Complete Board System" page, split into two columns to read the flow top to bottom.

Bundle pricing, why steel beats wood and plastic, a lab test callout, a comparison table, 6,200+ reviews, FAQs, then the email capture.

Building pages like this. DM if you want one.

X4:
Every section of KURA's product page, sliced into columns so the whole responsive build fits in one image.

This is what "no dead space, every fold works" actually looks like on a real phone screen, not just in theory.

Need your store built this way? DM me.

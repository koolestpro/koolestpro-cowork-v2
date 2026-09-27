## 🚀 QUALITY RATCHET — every output must be BETTER than the last, never the same or worse

This is the standing bar. It overrides "produce an acceptable output." The user is not satisfied with "good"; the deliverable must improve run over run. Rule: **before you call a build done, name the specific way this version is better than the previous one for that stream/brand, and make that improvement real — not stated.**

**For each stream, there is a known reference file that is the current best. You must beat it:**

| Stream | Current best reference (the bar to beat) | Original seed (never regress below this intent) |
|---|---|---|
| Tips carousel | **V4 (2026-09-27): `references-for-posts/tips-v4-prototype-2026-09-27/`, spec `docs/system/tips-v4-format.md`** (1080×1350, headline ≥88px, body ≥40px sans, one dominant visual per slide). Built on the old-style format (2026-09-18, `docs/system/tips-old-style-format.md`): the three `references-for-posts/5 … fix …` sets (1080×1080 dark + glow, heavy headline, gradient `FIX #n` pill, 1-2 line body, real store screenshot as proof, `@koolestpro \| Shopify CRO & UX` on every slide). Cover per standing rule 1. | `outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html` (export/JS mechanics only) |
| CRO Fix rebuild | `outputs/cro-fixes/caraway_fry-pan-pdp_rebuild.html` + `caraway_fry-pan-pdp_content.html` (the latest corrected run; graphics in `outputs/cro-fixes/caraway/`). Quality bar: `docs/system/cro-redesign-standard.md`. | `templates/eddie_bauer_cro_content_v2 (1).html` (the external CRO-content seed this stream was built from) + `outputs/cro-fixes/ecobioboutique_cellulite-remover_content.html` (your first own CRO file, Apr 28) |
| CRO Fix carousel + standalone posts (3-slide format) | `.ai-workflow/build_caraway_carousel.py` → `outputs/cro-fixes/caraway_fry-pan-pdp_carousel.html` → exported `outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_carousel_slide{1,2,3}.png` — cover (real brand logo, cover only) → **slide 2 = the before/after post** → **slide 3 = the annotation post** (Q→FIX legend, phone centered, standalone). Headlines per `docs/system/cro-headline-system.md`. One audit = 3 posts. THE bar to beat for CRO posts from here. | the old 6-7 slide narrative carousel |
| CRO standalone annotated graphic (clear bg, Q/A, circle heads) | `.ai-workflow/build_caraway_annotation.py` → `outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_annotated.png` (1080×1080) — headline top, brand+handle in a bottom lockup, every Q/A from the rebuild's top improvements | the old clear-background `anno-graphic` (ecobioboutique reference) |
| CRO standalone before/after graphic | **RETIRED 2026-09-10** — slide 2 IS the before/after; only the shared **gradient glow background** carried over. | (was `build_caraway_graphics.py`; do not regenerate) |
| Static Ad | `outputs/static-ads/obvi_super-collagen-protein_20260711/` | same |
| Template Showcase companion page | `outputs/templates/kura_pdp-01_2026-08-31/index.html` | same |
| Store template post set | latest Lumora/Meridian package | same |
| Monthly Build Recap | `outputs/cro-fixes/_recap9/koolestpro_monthly-build-recap.png` via `.ai-workflow/build_monthly_recap.py` — ONE continuous background (single sheet glow, strip exported `--bg-mode transparent` and autocropped), condensed-italic single-line headline, last four builds overlapping (`fanned_stack_4`, retuned taller). Caraway excluded until its product image is fixed. | Ridwan's "HIGH CONVERTING PAGES" reference (fanned overlapping phones) |

**The quality-ratchet checklist, every build, before it is done (not after):**

1. **Open the current best for that stream** — read the reference file, not just its name. (But do not load every stream's reference — only the one for the task you're on. That keeps context lean.)
2. **Build to beat it, not to match it.** Pick at least one concrete dimension to raise every run — clearer visual hierarchy, stronger cover, tighter copy, better spacing rhythm, more persuasive CTA, more readable slide density, a better export. Then actually do it, not just say it.
3. **Verify by exporting, not by reading markup.** Drive the page's own capture function (see `.ai-workflow/tools/README.md`) and look at the result. A build that is correct in source but flat on screen is not better.
4. **State the delta out loud** in the run summary: "this version is better because X". If you cannot name a genuine X, keep iterating — do not ship "acceptable."

**Never ship a regression.** "It is the same or worse" is a fail by definition. If the current run would come out at or below the reference bar, iterate before shipping.

**The temptation to copy the reference verbatim is the trap.** Copying the reference CSS/JS mechanics is good; copying its *concept* is how you get a stream that plateaus. What must keep moving: the visual idea, the copy strength, and the freshness of the treatment — not the structural backbone, which should be stable and proven.

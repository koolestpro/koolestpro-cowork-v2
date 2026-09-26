---
name: koolestpro-weekly-template-build
description: Weekly build for the replo-rebuilds portfolio system, Wednesdays ~09:21: builds one real brand-specific page for whichever brand needs one next, plus its mandatory mobile-strip presentation asset. A neutral [TOKEN] template is only created when no existing structure fits. No brand gets a second page in the same category.
---

You build for Ridwan's `replo-rebuilds` portfolio system at `replo-rebuilds/` inside the connected `koolestpro-cowork-v2` folder. This replaces a manual OpenCode + DeepSeek workflow — build everything yourself, directly, in this session. No DeepSeek/OpenCode calls.

Read `replo-rebuilds/README.md` first for the folder structure, template naming conventions, and the 6-phase brand pipeline (Product Found → Brand Identity → Image Prompts → AI Images → Page Build → Case Study) before starting.

═══════════════════════════════════════════════
CORE PRINCIPLE (Ridwan's correction, 2026-08-28 — read this before doing anything else)
═══════════════════════════════════════════════

**The job is always to build a real page for a real brand. A neutral template is a byproduct, never the goal.**

Earlier versions of this task ran two separate jobs — one building real brand pages, one building a standalone neutral template library. Ridwan corrected this directly: "The aim of this scheduled task is not just to create templates. Creating a template is part of it, but we want to always create new pages. When that new page is different from any template that we already have in the past, that's when we convert it to a template." He also corrected the brand-cycling logic: "we don't want to have a duplicate page, we don't want to have two versions of a page — instead we go to another brand." KURA ending up with 7 pages (including a second PDP) was accepted as roughly the natural ceiling, not a target to keep repeating.

So there is now ONE job per run, not two:

1. Figure out which brand needs a page next.
2. Figure out which category that brand is missing.
3. Build that page for real, with real brand copy and real (or genuinely reused) images.
4. Only if no existing template structurally fits what this brand/category needs, do the Path B research work to define a new structure — and since you're defining it fresh anyway, save it as a reusable template too, so the next brand that needs something similar doesn't repeat the research. If an existing template already fits well, just reuse it directly (token-substitution build) — do not invent a new structure for novelty's sake.

There is no more separate "grow the homepage template library" job. Homepage is just one of the six categories in the one list below, same as any other.

═══════════════════════════════════════════════
STEP 1 — Pick the target brand
═══════════════════════════════════════════════

The six core categories every brand should eventually have one real page in, in this fixed order: **PDP, Homepage, Landing Page, Advertorial, Listicle, Post-Purchase.**

Read every `brands/{brand}/README.md` (currently `kura` and `halos`; there may be more by the time this runs, check `brands/` for any created after those two). For each brand, check its "Pages Built" table against the six categories above. A brand counts as having a category "filled" if it has AT LEAST ONE real page there — do not count a second page in the same category, and do not build one. A brand is "complete" once all six categories have one real page each.

Process brands in this fixed order: `kura`, then `halos`, then any brand created after those two, in creation order. Pick the first incomplete brand. If every existing brand is complete, go to Step 1b.

**Step 1b — New brand (only when every existing brand is complete).** Auto-pick a new, plausible dropship-style product in a niche none of the existing brands already cover (check every `brands/*/README.md`'s opening line for what's taken). Run the brand-identity phase the way `brands/kura/README.md` and `brands/halos/README.md` show: a distinct color palette, a font pairing, a one-line voice description, a tagline, and a brand name. Write `brands/{new-brand}/README.md` in the same format as those two files (Brand Identity table, Pages Built table starting empty, Pipeline Status table). This becomes the active brand for the rest of this run.

═══════════════════════════════════════════════
STEP 2 — Pick the target category
═══════════════════════════════════════════════

For the active brand, find categories with zero real pages, walking the fixed order (PDP → Homepage → Landing Page → Advertorial → Listicle → Post-Purchase). Pick the first missing one. That is this run's target category.

═══════════════════════════════════════════════
STEP 3 — Decide: reuse an existing template, or build a new structure
═══════════════════════════════════════════════

Look at `templates/{category}/README.md` and its subfolders. For each already-built template in that category (status "Built" — has a real `index.html`, not just a `BUILD-NOTES.md` spec), judge honestly whether its structure and persuasion angle genuinely fit the active brand's product. Examples: a review-forward, UGC-heavy PDP (`pdp-02-social-proof`) fits a product with strong social proof potential; a villain/hero narrative PDP (`pdp-01-story-arc`) fits a product solving a clear, nameable problem. Don't force a mismatch just because a template already exists.

**If a good-fit built template exists:** reuse it directly. Build the real brand page via token-substitution (read the neutral `templates/{category}/{id}/index.html`, replace every `[TOKEN]` with real brand copy, reuse or generate real images). This is the fast path and should be the common case once the library has a few templates in each category.

**If no built template fits well** (either the category has none built yet — only a `BUILD-NOTES.md` spec or nothing at all — or the ones that exist don't suit this brand's product): do the Path B research yourself. Find a real, currently-live reference site that matches the category and a persuasion angle this brand's product genuinely needs. Catalogue its real structure section-by-section, the same format as `templates/homepage/hp-02-product-hero/BUILD-NOTES.md` or `templates/pdp/pdp-02-social-proof/BUILD-NOTES.md`. Then build TWO things from that one audit, in the same run:
  - the reusable neutral template at `templates/{category}/{new-id}/index.html` (brand-neutral, `[TOKEN]`-based, following `.ai-workflow/project-constitution.md` exactly), plus its `BUILD-NOTES.md`
  - the real branded page for the active brand, built from that same structure with real copy and images

Naming for a new template ID: follow the pattern already established in that category's README (e.g. `pdp-03-comparison`, `ad-02-comparison-editorial` — check the root `README.md`'s Template Naming Conventions table for the planned name and positioning before inventing a new one).

**Whenever you fix a real bug in a page you built from a reused template, patch the neutral template too** so the next brand inherits the fix, and record it in that category's `templates/{category}/README.md`. This is established practice (see the 2026-08-26, 2026-08-28 and 2026-09-02 fixes) — a fix that lives only in one brand page will be re-introduced by the next build.

═══════════════════════════════════════════════
STEP 4 — Build the real page
═══════════════════════════════════════════════

Read the brand's identity file (`brands/{brand}/{brand}-brand-identity-complete.html` or equivalent) plus 1-2 of its already-built pages for voice/palette/asset conventions. Follow `.ai-workflow/project-constitution.md` exactly (mobile-first only, CSS vars, no `!important`, no inline `style=""`, inline SVG icons only). Write real, specific brand copy, no `[TOKEN]` placeholders anywhere in the final file, no em dashes anywhere in the copy (rewrite as two sentences or a comma/colon instead — this is a standing project-wide rule, not new). Generate any new product/lifestyle images needed via the `gpt-image` skill, following the same generation pattern already used for this brand's existing pages, or reuse existing brand assets where they genuinely fit instead of regenerating — check the brand's `assets/images/` folder first. Output to `brands/{brand}/pages/{brand}-{category-shortcode}-{template-id}/index.html` with its own `images/` folder, matching the existing page-folder naming pattern already in use for that brand.

**Substitute the real brand palette and fonts into `:root`, don't just leave the template's placeholder values with the brand hexes in comments beside them.** The 2026-08-28 `halos-ad-01` build made exactly this mistake and shipped a page that renders in the neutral template's blue/orange instead of HALOS's amber/warm-black. Check the rendered screenshot actually looks like the brand.

**Resize copied images to sensible delivery dimensions rather than dropping in 1024×1536 originals for an 80px avatar.** The 2026-09-02 listicle build cut its image payload from 1646KB to 1068KB this way, and it also makes the Playwright captures in Step 5/5b far less likely to crash the renderer.

**`html, body { overflow-x: hidden; }` is mandatory from the start** on every new build, template or brand page — a real mobile bug shipped without it on 2026-08-26 (peek-carousels with no clipping safety net scrolled the whole page ~4.8x wider than the viewport on mobile). Also give every multi-item grid an explicit column count at the 1280px breakpoint matching its real item count (a grid without one wrapped into an unwanted extra row on 2026-08-23's `hp-02` build).

═══════════════════════════════════════════════
STEP 5 — Verify
═══════════════════════════════════════════════

Balance-check the file (`<div>`/`<svg>`/`<section>` open vs close counts must match — watch for false positives from code comments that happen to contain a literal `<section>` or similar). Then render it: set up Playwright per `.ai-workflow/tools/README.md`'s ARM64 recipe (download chromium + chromium-headless-shell zips via resumable `curl -L -C -`, extract into `~/.cache/ms-playwright/`, `apt-get download libxdamage1` + extract + `export LD_LIBRARY_PATH=...` — re-export every bash call, it does not persist; check `/tmp` first, a prior session's downloaded zips often still exist there even if `~/.cache` itself was reset — note the extracted cache can be wiped mid-session while the `/tmp` zips survive, so just re-extract rather than re-downloading). Screenshot at 390×844 and 1440×900, full page, running `document.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'))` via `page.evaluate()` immediately before each screenshot so scroll-triggered sections aren't invisible in the capture. Also do a non-full-page (viewport-clipped) screenshot at 390 width and check `document.documentElement.scrollWidth === 390` directly — Playwright's `full_page` screenshot mode has a known quirk of capturing wider than the true viewport on pages with `will-change: transform` carousels even when the page itself is not actually broken, so don't trust `full_page` width alone as evidence of a horizontal-scroll bug either way.

**Two capture gotchas confirmed 2026-09-02, don't waste a run rediscovering them:** (1) `full_page=True` can crash the renderer outright on image-heavy pages even with `--disable-dev-shm-usage`, and the crash lands partway down the page rather than at the screenshot call — fall back to scrolling and stitching viewport tiles, keeping already-captured tiles across retries. (2) Lazy-loaded images report as broken if you check `naturalWidth` immediately after a tile capture, so run a full pre-warm scroll first; otherwise you will chase a phantom bug (a reviewer avatar rendered as alt text in two consecutive stitches and was fine all along).

Actually look at the rendered screenshots: check for broken/overlapping layout, unwanted extra grid rows, huge unexplained blank gaps, missing/broken images (cross-check referenced `images/*.jpg` paths against what's actually in the page's `images/` folder), leftover `[TOKEN]` text, doubled currency symbols or similar token/hardcoded-text collisions (check the raw template markup for characters like `$` sitting immediately before a price token before assuming a value should include its own `$`), and em dashes in any visible text (code comments are fine, rendered copy is not). Fix anything wrong and re-render before moving on.

═══════════════════════════════════════════════
STEP 5b — Build the mobile strip (MANDATORY, added 2026-09-02)
═══════════════════════════════════════════════

⚠️⚠️⚠️ **This step is not optional and must never be skipped.** Ridwan's standing instruction: "I need this updated everywhere we do something related to it, so that this will always get to X calendar... anywhere we are building new pages and anywhere we are doing template showcase, we want to make sure this does not escape."

Every page you build here eventually becomes a Template Showcase (via `replo-rebuilds-pages.json`), and the showcase package now ships a `{slug}-mobile-strip.png` that gets its own X post. Building it here, at page-build time, means the Saturday `koolestpro-template-showcase-weekly` task can simply reuse it and it can never go missing.

```bash
python3 .ai-workflow/skills/page-presentation-kit/scripts/build_mobile_strip.py \
  "replo-rebuilds/brands/{brand}/pages/{page}/index.html" \
  "replo-rebuilds/brands/{brand}/pages/{page}/presentation/{page}-mobile-strip.png" --file
```

Save it to that page's own `presentation/` subfolder (create it). Defaults are correct and deliberate — 6 columns, mobile width 390, flush `pad=0`/`gap=0`. Do NOT add outer margins to "match" `preview.png`: the flush composition is the one Ridwan approved, and preview.png's margin-bigger-than-gap rule is a different asset's rule. Full spec: CLAUDE.md "⚠️⚠️ CORRECTED v8".

Then look at the result and confirm: no column boundary cuts through the middle of a section, the bottom edge reads as continuous per-column background rather than hard white voids, and no image anywhere in it rendered as alt text. If the script reports unloaded images, look at the actual pixels before believing it (see the lazy-load gotcha above).

If the strip genuinely cannot be built, say so loudly at the top of the report rather than quietly finishing without it.

═══════════════════════════════════════════════
STEP 5c — Present the work
═══════════════════════════════════════════════

**Present the screenshots** using `mcp__cowork__present_files` (load via ToolSearch if deferred) so Ridwan sees the actual page, not just a text description.

**Always also present the built HTML file itself (2026-09-01, Ridwan's standing instruction, project-wide — every output skill, every run):** in the same `present_files` call (or a second one), include the real `brands/{brand}/pages/{...}/index.html` file just written — not just its screenshots. Ridwan's own words: "after every successful build I need to see the html preview... same thing you save into the outputs folder so that I can check quick." Screenshots show the render; the HTML file is what he wants to be able to open and check directly. This is mandatory every run, including fully unsupervised ones.

**Present `{page}-mobile-strip.png` too** (2026-09-02) — Ridwan asked specifically to see this asset in the preview every time it is produced.

═══════════════════════════════════════════════
STEP 6 — Update docs
═══════════════════════════════════════════════

Add the new page as a row in `brands/{brand}/README.md`'s "Pages Built" table (Page / Template / Status / Built date / Case Study "Not started" / Social "Not started" — matching the existing row format exactly), and update that brand's Pipeline Status table. Note in the page's build entry that its mobile strip exists at `presentation/{page}-mobile-strip.png` so the showcase run knows to reuse rather than regenerate it. If Step 3 required a fresh Path B audit and new template, also add a row to `templates/{category}/README.md`'s status table for the new template ID, and update the root `README.md`'s Current Brands table if relevant.

═══════════════════════════════════════════════
Report
═══════════════════════════════════════════════

End with a short summary: which brand and category got built, whether an existing template was reused or a new one had to be created (and if new, what real reference site it was audited from), any layout bug found and fixed during verification (and whether the fix was also patched upstream into the neutral template), an explicit MOBILE STRIP line confirming the strip was built and where it was saved (or stating loudly that it failed), and what's next (which brand/category is next in the fixed order, or "brand X is now complete, moving to brand Y next week" / "every existing brand is complete, a new brand will be created next run" as applicable).

Do not touch anything outside `replo-rebuilds/`, except for the `presentation/` strip described in Step 5b and any neutral-template fix described in Step 3. Do not deploy or publish anything. Do not touch the koolestpro-cowork-v2 content pipeline (a separate system inside the same connected folder).
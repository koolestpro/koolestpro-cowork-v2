---
name: koolestpro-weekly-template-build
description: Weekly build for the replo-rebuilds portfolio system, Wednesdays ~09:21: builds TWO real brand-specific pages per run (two different brands, two different page types), rotating brand AND page type every run (never the same brand or category as the last two runs; a new brand beats a recent one), plus its mandatory mobile-strip presentation asset. A neutral [TOKEN] template is only created when no existing structure fits. No brand gets a second page in the same category.
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

⚠️⚠️ CONTACTABLE STORES ONLY (Ridwan, 2026-10-26). A real store is only designed, rebuilt or posted about if we can actually email it. The list is `outreach/scrapers/state/contactable_stores.json` (written hourly on the Mac by `outreach/scrapers/redesign_sync.py` from the cold email Sheet: sendable confirmed email, not Lost/Bounced/Unsubscribed/Won). A target whose domain is not on that list is NOT eligible for this run, whatever its other fields say. If the file is older than 3 days, run `python3 outreach/scrapers/redesign_sync.py pull` first (it reaches the Sheet from the Mac shell); if that fails, say so at the top of the summary. FALLBACK (Ridwan, 2026-10-26): when the Sheet cannot be reached, or no contactable target is eligible, do not skip the run: use the best eligible target already in `targets_pool.json` under the normal rotation rules, even though we cannot email it. Say "FALLBACK: not a contactable store" at the top of the summary, add `"fallback": true` to its usedFor note, and write no outreach hook for it. Contactable stores always win when there is one. Concept brands (HALOS, MOULT, KURA and new ones) are not affected.

⚠️⚠️ NO TEMPLATE CEILING (Ridwan, 2026-10-26). Past templates and past pages are a starting point and the bar to BEAT, never the structure to copy. For every page: (1) decide what this business needs first (what it sells, price point, how buyers arrive, what they doubt, the brand's own look), (2) look at 3 or more real, live, well-converting pages for that kind of business and page type (homepage and hero inspiration roundups, competitors, strong DTC stores; not award showpieces, pages that sell) and note what each does that ours never has, (3) pick a structure and a hero idea for THIS brand, then build. Write the choice and the references in the build notes. A page that reads like a cheap theme or like our last page with new colours is not done. Bar: the latest CRO Fix (`outputs/cro-fixes/fishwife_shop-all-collection_rebuild.html`) and `docs/system/cro-redesign-standard.md` "No template ceiling".

⚠️⚠️ EVERY REAL-STORE PAGE IS POSTABLE BOTH WAYS (Ridwan, 2026-10-26). A full-page redesign of a real store is one asset with two posts: the CRO Fix post (live page = before, our first screen = after) and the Template Showcase package (the whole page). Whichever task builds it, the other reuses it: a CRO Fix rebuild goes to the showcase manifest, and a Wednesday Page B redesign is eligible as the Sunday CRO Fix (capture the live page as the before, audit per `cro-finding-rules.md`, then make the carousel and graphics from the redesign's first screen) instead of building a new page. Concept brand pages have no real "before", so they are never posted as a CRO Fix.

═══════════════════════════════════════════════
PAGE B = A REAL-STORE REDESIGN (Ridwan, 2026-10-26). Read this before Step 1.
═══════════════════════════════════════════════

Ridwan: "instead of inventing products all the time, I want us to also make a redesign of some of those Shopify sites." So the two pages per run are now split:
  - **Page A = concept brand page**, picked and built exactly as Steps 1 to 6 below describe (HALOS, MOULT, or a new concept brand).
  - **Page B = a full-page CRO redesign of a REAL Shopify store** from `targets_pool.json` (most of these now come from the outreach directory scrape, `source: "outreach-directory-scrape"`). It is NOT a concept brand and NOT a client.

⚠️⚠️ WHAT TO BUILD = THE BUILD QUEUE (Ridwan, 2026-10-26). Real-store pages are built for the leads most likely to reply, not at random. Read `buildQueue` in `outreach/scrapers/state/contactable_stores.json` and take the first entry that passes the content rules (`cro-finding-rules.md`, no vape/nicotine/tobacco/kratom/replica/weapons, not a big chain):
  - tier 1 = they said yes to the mockup offer: build this week, before anything else.
  - tier 2 = emailed, no reply yet, strongest problem first: the page lands as their next follow-up.
  - tier 3 = not emailed yet, strongest problem first: their first email is written around the page.
**Build the page the email is about** (`buildPage`, from the lead's problem page). The page-type rotation rules give way to this. Only when `buildPage` is empty choose the type yourself (prefer the page with the strongest visible problem). If the store is not in `targets_pool.json` yet, add it there first (live mobile check, record schema, `source: "outreach-directory-scrape"`, `outreachLead: true`). If the queue is empty or nothing in it passes, use the pool FALLBACK.
**Page mismatch:** if a store already has a redesign of a DIFFERENT page than the one its email is about (for example we built its PDP from the pool, but the email is about its homepage), that is fine: the email code says so honestly (it offers the built page as proof of the approach and offers to do the problem page, and never claims one fixes the other). When that store reaches tier 1, build the page it actually asked about.
Every real-store build writes its `outreach/redesign-hooks.json` entry with `pageType`, `problemPage` (from the queue), `compareImagePath` and `compareFullPath`. `redesign_sync.py push` (hourly) then hands it to the Sheet, which: rewrites email 1 if they have not been emailed; turns the next follow-up into the "I rebuilt it, want to see it?" email if they are mid-sequence; queues one extra email in the old thread if the sequence ended with no reply; or emails Ridwan to send it himself if they are already talking.

How to pick Page B:
  1. Eligible targets: domain on `contactable_stores.json`, `status: "Available"`, `isClient: false`, `visualPotential` not "Unrated", and no `usedFor` entry with stream "template-showcase" or "cro-fix" in the last 14 days. Prefer zero "template-showcase" entries.
  2. Page type: the queue's `buildPage` when it has one (see above). Otherwise choose from Homepage, Product Page, Collection Page, Advertorial, Listicle. Never the same page type as Page A, and never the page type of the last real-store redesign (check `replo-rebuilds/build-rotation-log.json`, entries with `kind: "real-redesign"`). Homepage, PDP and collection are redesigns of the store's real page. Advertorial and listicle are NEW pages for that store (it usually has none), built around its real products.
  3. Rotate category away from the last two real redesigns.

How to build Page B (CLAUDE.md "AI Workflow Architecture" path 1 applies, because this is a real business's page):
  - Audit the live page first at mobile and desktop with `docs/system/cro-finding-rules.md`. Write the findings to `replo-rebuilds/real-redesigns/{brand-slug}/AUDIT.md` (MEASURED / SEEN evidence lines). For an advertorial or listicle, write the angle and the real product facts it uses instead.
  - Build the WHOLE page, not a hero: every section a real page of that type needs (see `docs/system/cro-redesign-standard.md`, "Full page rule"), CRO optimized, with the first screen still carrying the whole decision.
  - Real assets only: the store's real logo file, real product photos, real prices and product names from the live site. Never invent reviews, ratings, review counts, press logos, guarantees or stats the store does not show. If the store shows none, design the section without a number.
  - Builder: Lovable first (kept PRIVATE, never `deploy_project`, per the "Rebuilds of real businesses stay PRIVATE" rule), then Figma Make / v0, then Claude-authored HTML from the same brief if no builder is available. Either way the final file lands at `replo-rebuilds/real-redesigns/{brand-slug}/pages/{brand-slug}-{type}-01/index.html` with its own `images/` folder, and Steps 5 and 5b (verify + mobile strip) apply exactly as for Page A.
  - No brand README, no brand-identity phase, no neutral template conversion for Page B. Its identity is the real store's.

After Page B is built:
  - Add it to `replo-rebuilds-pages.json` with `kind: "real-redesign"`, `isRealBrand: true`, `isClient: false`, `targetId` (the targets_pool id), `liveUrl`, `active: true`, `usedForTemplateShowcase: false`, and the next free `sortOrder`.
  - Append to `replo-rebuilds/build-rotation-log.json` with `kind: "real-redesign"`.
  - **Comparison image for the email (2026-10-26):** also save `presentation/{page}-compare.png`: the store's LIVE page and our redesign side by side at the same mobile width (390), same first screen, captured the same day, labelled "Your page today" / "Concept redesign", plus up to 3 numbered notes naming what changed and why. A second image `{page}-compare-full.png` puts the full live mobile page next to the full redesign. These are what the store gets after it says yes, so it can check our version against its own site in seconds. Record both paths in the redesign-hooks entry (`compareImagePath`, `compareFullPath`).
  - Append a `usedFor` entry to that target in `targets_pool.json`: `{stream: "template-showcase", date, pipelineItemId: null, note: "Real-store full-page redesign built (Wed), awaiting Saturday showcase"}`.
  - If the target has `outreachLead: true` (or the domain is in the Outreach Sheet), append a row to `outreach/redesign-hooks.json` (domain, brand, pageType, page path, mobile-strip path, date, status "ready"). Ridwan's decision 2026-10-26: the redesign becomes the hook in that store's cold email. Screenshots or the mobile strip go in the email; never a public link to the page.

If no target is eligible for Page B, build two concept pages as before, say so at the top of the report, and flag that the target pool needs a refresh.

═══════════════════════════════════════════════
STEP 1 — Pick the brand AND category together: ROTATE, never run one brand to completion (Ridwan, 2026-10-10)
═══════════════════════════════════════════════

⚠️⚠️ This REPLACES the old "fill one brand's six categories in order, then move to the next brand" rule. Ridwan: "it will not just focus on a single brand. After it is done there, it goes to the next brand. No, we want to mix things up... PDP for brand A, then landing page for brand B, then listicle for brand C, then advertorial for brand D." Back-to-back builds for the same brand (MOULT PDP on 2026-09-30, then MOULT homepage on 2026-10-07) are exactly what this rule stops.

The six categories are still the target set for every brand: **PDP, Homepage, Landing Page, Advertorial, Listicle, Post-Purchase**, one real page per category per brand, never a second page in a filled category.

**TWO PAGES PER RUN (Ridwan, 2026-10-10).** Every run builds two pages: Page A and Page B. Pick Page A with the rules below. Then pick Page B with the same rules, treating Page A as the most recent build, so Page B is always a different brand AND a different page type from Page A. Steps 3 to 6 (template choice, build, verify, mobile strip, present, docs) run once for each page; finish Page A completely (including its mobile strip) before starting Page B, so a timeout never leaves two half-built pages. Why: the distribution queue keeps any one brand 5+ days apart, so a week of showcase posts needs several brands with fresh pages, and the Saturday showcase task now packages two pages a week. If the run genuinely cannot fit the second page, ship Page A, say so at the top of the report, and name what Page B would have been.

**Build history.** Read `replo-rebuilds/build-rotation-log.json` (one entry per build: date, brand, category, page). If it is missing or stale, rebuild it from every `brands/*/README.md` "Pages Built" table (the Built column has the dates). Append this run's build to it at the end (Step 6).

**Rules, in priority order:**
1. **Brand:** never the brand built in either of the last 2 runs. Among the remaining brands that still have an empty category, pick the one whose most recent build is OLDEST.
2. **Category:** never the category built in either of the last 2 runs, for any brand. From the chosen brand's empty categories that pass this, take the first in the list order above. If every empty category of that brand was built in the last 2 runs, try the next brand from rule 1 before relaxing this rule.
3. **New brand:** if no existing brand passes rules 1 and 2 (for example, the only brands with gaps were built in the last two runs, or every brand is complete), start a NEW brand (Step 1b) and give it a category that passes rule 2. Do this rather than giving a recent brand another page. Variety across brands beats finishing a brand.
4. State the pick and the reason in the report ("built X for brand Y because last two runs were A/B and Z/W").

Worked example from the state on 2026-10-10: KURA and HALOS are complete, MOULT has PDP (2026-09-30) and Homepage (2026-10-07). MOULT was the last run's brand, so it is excluded. No other existing brand has gaps, so the next run creates a new brand and builds a category other than PDP or Homepage (for example a Landing Page). The run after that can go back to MOULT, with any category except the last two built.

**Step 1b — New brand.** Auto-pick a new, plausible dropship-style product in a niche none of the existing brands already cover (check every `brands/*/README.md`'s opening line for what's taken). Run the brand-identity phase the way `brands/kura/README.md` and `brands/halos/README.md` show: a distinct color palette, a font pairing, a one-line voice description, a tagline, and a brand name. Write `brands/{new-brand}/README.md` in the same format as those files (Brand Identity table, Pages Built table starting empty, Pipeline Status table). Concept brand, never presented as a client.

═══════════════════════════════════════════════
STEP 3 — Decide: reuse an existing template, or build a new structure
═══════════════════════════════════════════════

Look at `templates/{category}/README.md` and its subfolders. For each already-built template in that category (status "Built" — has a real `index.html`, not just a `BUILD-NOTES.md` spec), judge honestly whether its structure and persuasion angle genuinely fit the active brand's product. Examples: a review-forward, UGC-heavy PDP (`pdp-02-social-proof`) fits a product with strong social proof potential; a villain/hero narrative PDP (`pdp-01-story-arc`) fits a product solving a clear, nameable problem. Don't force a mismatch just because a template already exists.

**2026-10-26 override (Ridwan): token-substitution builds are no longer the common case.** Run the NO TEMPLATE CEILING research above for every page, including when a template fits. An existing template may be the skeleton, but the hero, section order and at least the sections that carry this brand's argument are designed for this brand, and the result has to beat the template it started from. Save the new structure back as a template when it is genuinely different.

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

Append this build to `replo-rebuilds/build-rotation-log.json` (date, brand, category, page). Add the new page as a row in `brands/{brand}/README.md`'s "Pages Built" table (Page / Template / Status / Built date / Case Study "Not started" / Social "Not started" — matching the existing row format exactly), and update that brand's Pipeline Status table. Note in the page's build entry that its mobile strip exists at `presentation/{page}-mobile-strip.png` so the showcase run knows to reuse rather than regenerate it. If Step 3 required a fresh Path B audit and new template, also add a row to `templates/{category}/README.md`'s status table for the new template ID, and update the root `README.md`'s Current Brands table if relevant.

═══════════════════════════════════════════════
Report
═══════════════════════════════════════════════

End with a short summary for EACH of the two pages: which brand and category got built, whether an existing template was reused or a new one had to be created (and if new, what real reference site it was audited from), any layout bug found and fixed during verification (and whether the fix was also patched upstream into the neutral template), an explicit MOBILE STRIP line confirming the strip was built and where it was saved (or stating loudly that it failed), and what's next under the rotation rule (which brand and category the next run should pick, and why).

Do not touch anything outside `replo-rebuilds/`, except for the `presentation/` strip described in Step 5b, any neutral-template fix described in Step 3, and Page B's three registration writes (`replo-rebuilds-pages.json`, the target's `usedFor` in `targets_pool.json`, and `outreach/redesign-hooks.json`). Do not deploy or publish anything. Do not touch the koolestpro-cowork-v2 content pipeline (a separate system inside the same connected folder).
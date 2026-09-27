# Koolestpro Cowork System — Rulebook & Task Router

**Start here: `SYSTEM-MAP.md` is the inventory (what exists, what state, where a new thing goes).** This file is the rulebook (live rules + how to route a task) and `SYSTEM-STATUS.html` is the live generated counts. Do not restate the inventory, the strategy plans, or the history here.

**Three docs, don't confuse them:**

| Doc | Answers | Read it when |
|---|---|---|
| `SYSTEM-MAP.md` | "What exists, what state, where does a new thing go?" | You're about to build/re-file something |
| `docs/koolestpro-content-operating-plan.md` + `docs/koolestpro-growth-operating-plan.md` | "What is the strategy and sequence?" | You're planning, not executing |
| **This file** + the per-sub-project doc it routes you to | "What are the rules for this one task, right now?" | You're executing a task |

**📚 History / decision-log = `docs/system/00-claude-md-archive-2026-09-08.md`.** Every dated correction, "confirmed bug", "corrected v3/v4/v5…" narrative and the reasoning behind a rule lives there verbatim. Do NOT re-derive a rule from that narrative; if a rule still stands it is stated here, and the archive is where you look up *why*. This file is deliberately slim so every task only pays for the context it uses.

---

## The seven sub-projects

Cut by function (matches how files + scheduled tasks already cluster). Full detail in `docs/system/01-…` through `07-…`.

| # | Sub-project | One line | Owns |
|---|---|---|---|
| 1 | Content Production | Turns a topic/target into finished post packages | `outputs/`, Tips/CRO/Static Ad generation |
| 2 | Distribution | Gets finished packages posted on a schedule | `.ai-workflow/tools/`, the Google Sheet |
| 3 | Prospect Intelligence | Finds + qualifies businesses | bridge scripts, KoolestFlow leads |
| 4 | Outbound / KoolestFlow | Turns a qualified lead into a sent message | **`cold-email-app/`** (its own project) |
| 5 | Build Assets | The real pages, templates, mockups, caption libs | **`replo-rebuilds/`**, `store-templates/`, `{brand}-social-content.*` |
| 6 | Web Presence | The destination CTAs land on | **`site/`** (its own Next.js project) |
| 7 | Infrastructure | Tooling, scheduling, credentials, sandbox limits | `.ai-workflow/` |

**Standalone projects reachable from here (they are themselves projects):** `replo-rebuilds/` (Build Assets), `cold-email-app/` (KoolestFlow / Outbound backend), `site/` (Web Presence / Next.js). Each has its own `CLAUDE.md`; when you need to work inside one, read *its* rulebook, not this one. This file only holds the cross-project rules and the router.

---

## 🔎 TASK ROUTER — read only the row that applies

Every task reads its own scoped doc instead of this whole file. When a task is dispatched, find its row here and follow the `→` pointer; do NOT read the whole rulebook, and do NOT read other rows.

| Task | Sub-project | Read |
|---|---|---|
| Tips carousel (`koolestpro-tips-weekly`, content engine) | 1 | **`docs/system/tips-v4-format.md`** (the format, 2026-09-27; bar = `references-for-posts/tips-v4-prototype-2026-09-27/`), `docs/system/tips-old-style-format.md` (the 2025 references it builds on), `.ai-workflow/tools/README.md`, `docs/system/01-content-production.md` |
| CRO Fix weekly (`koolestpro-weekly-cro-fix`) | 1 | `docs/system/cro-3-slide-carousel-format.md` (the post format), `docs/system/cro-headline-system.md` (the headline), `docs/system/cro-redesign-standard.md` (the rebuild quality bar), `docs/system/rebuild-tooling-and-quality.md` (where the rebuild gets made), `docs/system/page-build-brief.md` (the Lovable/Figma input brief), `docs/system/redesign-tool-api-integration.md` (which tool, and how to connect it), `docs/system/x-caption-playbook.md` (the X caption), `.ai-workflow/weekly-pipeline.md`, `docs/system/01-content-production.md` |
| Static Ad weekly (`koolestpro-static-ad-weekly`) | 1 | `.ai-workflow/skills/static-ad-image/`, `docs/system/01-content-production.md` |
| Template Showcase weekly (`koolestpro-template-showcase-weekly`) | 1 + 5 | `docs/system/template-showcase-ig-carousel.md` (Instagram = always a carousel), `.ai-workflow/skills/page-presentation-kit/`, `replo-rebuilds/CLAUDE.md`, `docs/system/01-content-production.md` |
| Weekly template build (`koolestpro-weekly-template-build`) | 5 | `replo-rebuilds/CLAUDE.md` |
| Distribution assembly + health check (`koolestpro-weekly-distribution-assembly`, `koolestpro-distribution-health-check`) | 2 | `.ai-workflow/tools/DISTRIBUTION.md`, `docs/system/02-distribution.md` |
| Target pool refresh (`koolestpro-target-pool-refresh`) | 1/3 | `docs/system/03-prospect-intelligence.md`, `targets_pool.json` |
| Staleness check (`koolestpro-replo-cache-staleness-check`) | 5 | `docs/system/05-build-assets.md` |
| BrowserAct/Maps + Ad Library lead gen (Tue/Wed) | 3 + 4 | `.ai-workflow/tools/README.md`, `docs/system/03-prospect-intelligence.md` |
| Trend radar (`koolestpro-trend-radar-weekly`) | 1 | `.ai-workflow/skills/koolestpro-trend-radar/`, `trend-radar-config.json` |
| TikTok drafts / Instagram publishing | 2 | `.ai-workflow/tiktok-weekly-procedure.md`, `.ai-workflow/tools/README.md` |
| System status weekly (`koolestpro-system-status-weekly`) | 7 | `.ai-workflow/tools/build_system_status.py` |

---

## The four project-wide rules (highest stakes)

1. **Every content CTA points at a real destination** — a service page or case study on the domain, not at engagement.
2. **Never invent a client result, and never imply a concept brand was a client.** KURA, HALOS, MERIDIAN, Lumora are concept builds and must always be labelled as such. Highest-stakes rule in the project.
3. **Local-first, including the CRM.** `outreach_tracker.json` is the outbound system of record. No Notion.
4. **Two prospect pools, never merged, never given a `segment` field.** Which file a prospect is in already says market + motion:
   - **`targets_pool.json`** = content-production pool. International DTC/Shopify brands with a real, live, auditable `url`. Every entry has one; that is what makes it eligible. Rotation tracked in `usedFor`, not `status`.
   - **KoolestFlow** = outbound pool. Fed by browseract/Maps (Tue) + Meta Ad Library (Wed) through the hybrid cloud-scores/Mac-imports pipeline, with `.ai-workflow/taken-brands-ledger.json` preventing double-push. `dm_leads_pool.json` is a historical staging log, not a third pool.

---

## AI Workflow Architecture (who builds what) — updated 2026-09-18

**Two build paths, split by what is being built:**

1. **CRO Fix rebuilds and any redesign of a real business's page (NOT store templates)** are built in an **external page builder**: Lovable (primary, via its MCP), Figma Make, Claude Design, or v0. Claude is the operator, not the page author: Claude writes the facts file and the build brief (`docs/system/page-build-brief.md`), drives the builder over MCP, iterates until the page reaches `docs/system/cro-redesign-standard.md`, then captures it with `capture_page.py` and turns the capture into the post (carousel, captions, registration). The page itself is the builder's output; everything around it (brief, capture, composition, copy, QA, registration) is Claude's. If no builder is available or all are out of credits, fall back to Claude authoring the page HTML directly from the same brief.
2. **Everything else** (Tips carousels, Static Ad pages, Template Showcase companion pages, store templates in `replo-rebuilds/` + `store-templates/`, post graphics) is authored by Claude in this project, as before.

**Rebuilds of real businesses stay PRIVATE (hard rule, 2026-09-18).** Never deploy a rebuild to a public URL. In Lovable: do not call `deploy_project` for a real brand's rebuild; set project visibility to private (`set_project_visibility`) and capture from the authenticated preview. In v0/Figma Make/Claude Design: keep the chat/file private and never publish a share link. If a capture genuinely needs a public URL, publish, capture, and unpublish in the same run, and log that it was taken down. A public copy of someone's branded page reads as impersonation.

**Claude owns end-to-end for each build:** content strategy, the brief, the visual design decisions (or, on path 1, the direction given to the builder and the accept/reject call on its output), the copy, the export-ready QA, and final approval. Where a build has an established reusable script (e.g. `build_split_page.py`, `build_device_still.py`, `build_caraway_*.py`, the region-swap Tips build), use the script and accept its output — but for everything that is authored HTML, author it here. Reference the existing gold-standard files and reuse their proven CSS/JS patterns rather than reinventing per run.

**When you may delegate:** only purely mechanical, fully-specified, high-volume HTML scaffolding where the intent is already fully pinned down and a script does not already exist. If in doubt, author it yourself. When you do delegate, write `.ai-workflow/deepseek-task.md` and run `node run_deepseek_task.js` — but this is the exception, not the default. Say **"delegate this one"** explicitly; otherwise Claude writes it.

---

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

---

## ⚠ PROJECT-WIDE GENERATED-COPY RULES (apply to EVERY skill/task, not just one)

These apply to every LinkedIn caption, X post, carousel slide, static ad text, CRO fix caption, and anything else this project generates:

1. **No em dashes, anywhere.** Scan for "—" / `&mdash;`; rewrite as two sentences, a comma, or a colon.
2. **Run every piece of copy through the `humanizer` skill** before treating it as final. That means the **full v3.0 eleven-pass pipeline** (writer, editor, fact-checker, anti-AI style, AI-word check, AI-pattern check, voice match, humanizer, red pen, self-critique, final blocklist), anchored in `VOICE.md`. This covers **all** written output: carousels, static ads, website/page copy, mockups, post captions, outbound email, and content-system titles. Full routing and per-stream checklists: **`docs/system/humanizer-guideline.md`**. Headlines additionally follow `docs/system/cro-headline-system.md`. **X/Twitter captions additionally follow `docs/system/x-caption-playbook.md`** (the anatomy and four proven patterns drawn from Ridwan's own best-performing posts).
3. **Export-ready formatting:** real line breaks (never markdown `\n` literals or asterisk stand-ins), and the X-vs-LinkedIn convention — no hashtags on X, hashtags fine on LinkedIn/Instagram.
4. **X caption hard 280-char limit, always counted.** Count the real string (newlines included) against 280 before calling it done, independent of `populate_sheet.py`'s automated flag. A caption at/over 280 chars is not postable; shorten it before shipping. Check every time a Twitter caption is produced or re-touched.

**The eleven passes are not optional and not per-stream.** If a system produces text a human will read, it runs the pipeline. The only hard block is `VOICE.md`'s blocklist (e.g. `unlock`, `digital journey`, `comprehensive post`, `valuable insights`, `synergize`, `holistic`, `conversion excellence`, "it's important to note"). Never fabricate a result, quote, number, or source; never imply a concept brand was a client.

---

## Local-first source of truth

* Notion is NOT used. The single source of truth is `ridwan_content_system_updated.html`, and all data lives inside `<script id="cowork-sync-data" type="application/json">`. Cowork must ONLY read and write that JSON block.
* Structure: `meta` / `months` / `items`.
* Every content-generating HTML file must (1) export structured JSON, (2) save to `/outputs/...`, (3) provide the file path inside the JSON.

### JSON Standard (MANDATORY)

```json
{
  "id": "unique-id",
  "type": "Tip | CRO Fix | Case Study | Personal | Static Ad | Template Showcase",
  "title": "Post title",
  "slug": "url-friendly-slug",
  "status": "Created",
  "day": "Monday | Wednesday | Friday",
  "created": "ISO timestamp",
  "folder": "outputs/{type}/{slug}_{date}.html",
  "week": "Week label",
  "month": "Month label",
  "monthSlug": "YYYY-MM",
  "captions": { "linkedin": "string, optional", "x": ["string, optional"] },
  "assets": { "images": ["path, optional"], "video": "path, optional" }
}
```

Rules: `id` unique, `slug` matches filename, `folder` points at a real file, no missing core fields. `captions`/`assets` are optional autopost-ready conveniences. Status only ever reaches `"Ready"` in Cowork — never `"Published"`.

* **"Static Ad" type:** 4-angle ad showcases. `folder` → `outputs/static-ads/{slug}_{date}/index.html`.
* **"Template Showcase" type:** desktop/mobile mockups of a real built page. `folder` → `outputs/templates/{slug}_{date}/index.html`.

---

## 🔗 PIPELINE EXPORT BUTTON (MANDATORY in all output skills)

Every HTML file from any output skill MUST include a "Send to Content Pipeline" button (the `.ai-workflow/project-constitution.md` has the exact `sendToPipeline()` JS + button HTML). Defines `POST_BRAND`/`POST_SLUG`/`POST_TYPE`/`POST_FOLDER` before the function. Downloads `{slug}_pipeline.json`, logs `EXPORT_POST_JSON`, status always `"Created"`, `day` always `""`.

---

## 🖼️ STANDING HARD RULES (project-wide, enforced in review)

These override anything narrower in a skill/cache when they conflict. Cowork cannot edit the underlying skill source (read-only cache); these are the enforced spec. For reference implementations see `.ai-workflow/build_caraway_*.py` (corrected 2026-09-07).

1. **Carousel covers are never boring.** Either a strong visual sized to dominate the frame, or (Tips especially) a designed type-led cover in the style of `references-for-posts/90 content ideas in 9 slides/` cover: huge bold type as the visual, with thin line-art diagrams/icons and a frame blended into it over a rich gradient background. A plain headline on a flat background fails. Verify on the exported PNG. (2026-09-01, widened 2026-09-18)
2. **The CRO Fix 3-slide carousel IS the before/after and the annotation.** Slide 2 is the before/after post; slide 3 is the annotated post (Q→FIX legend + connector lines). Both must read as standalone posts (brand bar + full title + handle). The separate ba/anno graphics are retired (2026-09-10); keep only the gradient glow background. **Posting (2026-09-27):** the carousel always posts on LinkedIn, Instagram AND X, and each of the 4 graphics (3 slides + clear-bg annotated graphic) also posts alone on X, so every run writes 5 X captions. Table in `docs/system/cro-3-slide-carousel-format.md`.
3. **Product photos: background-removed cutouts over raw studio photos, never cropped** — composite the cutout against a contrasting background; never crop the product.
4. **Build above the fold — no dead space at the bottom** — shift lower elements down / enlarge the product image so the frame genuinely fills. Check on the render, not the CSS.
5. **Image aspect-ratio integrity** — never ship `object-fit:cover` on a container whose rendered aspect you haven't checked against the source image. Prefer `object-fit:contain` on a deliberate plinth.
6. **Every CRO Fix graphic + caption must state the page type visibly** (e.g. PRODUCT PAGE (PDP), HOMEPAGE, LANDING PAGE). Badge on the graphics and in the caption opening line.
7. **Carousel slides use the full frame; large redundant labeling over small reliant tags** — fold the label (Myth/Reality/The Pattern/Before/After) into a bold 20px+ pill badge, not just a tiny eyebrow. No slide ends with a big empty band; fill with a real "so what". Counter/handle overlays get a semi-opaque backdrop chip.
8. **Empty carousel space gets contextual icons/imagery, never generic/templated visuals** — Iconify public API (`https://api.iconify.design/{prefix}/{icon}.svg?color=%23HEX`, no key), inlined as real SVG, specific to that slide's finding, at both watermark + badge size. Never a generic "idea bulb".
9. **Headline is the topmost element; `@koolestpro` may appear on every slide.** Tips: `@koolestpro | Shopify CRO & UX` footer on EVERY slide (the old-style format). CRO Fix: `@koolestpro` is allowed on every slide, in a small bottom lockup, never as a top bar. **The audited business's real brand logo goes on the CRO cover slide only**, never on slides 2-3. (2026-09-12, revised 2026-09-18)
10. **Annotations are drawn from the rebuild's TOP improvements.** Rank the rebuild's changes by impact and annotate only those, each tied to the exact element it affects. Never reuse a previous audit's questions. (2026-09-12)
11. **CRO headlines follow `docs/system/cro-headline-system.md`.** Derive from the single #1 finding; use a different angle per surface (cover / before-after / annotation / graphic); max 2 lines; never reuse last week's line. (2026-09-12)
12. **CRO rebuilds must reach `docs/system/cro-redesign-standard.md`.** The first screen carries the whole decision (outcome headline + proof + benefit + CTA + trust on a real hero). A rebuild that only fixes the audit findings, but still splits the pretty image from the reason to buy, is not done. (2026-09-12)
13. **Post graphics share ONE continuous background.** Never paste a mockup strip that carries its own gradient (it leaves visible bands). Export the strip transparent (`build_device_still.py --bg-mode transparent`), autocrop it, and back the whole sheet with a single background + glow so the headline and the phones sit on the same surface. (2026-09-13)
14. **A rebuild is not postable until its hero product image survives phone size.** The Caraway build reads badly because the product photo is a dark studio shot on a dark page. The GetFit winner worked because its product image was AI-regenerated and blended. Regenerate or cut out the hero image, place it on a contrasting plinth, verify the composite at 390×844, then it can be used. See `docs/system/rebuild-tooling-and-quality.md`. (2026-09-13)
15. **Decide the hero image after the plan, not before.** Every rebuild (product page or homepage) starts with a clear plan of what is being built, then an image decision: (a) look for a usable hero photo on the site and use it if it is genuinely great, (b) if there is no good photo, or nothing is good enough, generate a suitable version with AI, and (c) build the page on that image. Never build first and bolt on a weak image. This is the "image decision" block in the page build brief. (2026-09-13)
16. **Assume the operator is Claude Code or Codex, and keep the pipeline agent-drivable.** Ridwan runs this project through an agent, not by hand. Page builds go through the **Lovable MCP server** (`https://mcp.lovable.dev`, driven from Claude/Codex: `create_project` → `send_message` → `set_project_visibility` private → capture from preview; no public `deploy_project` for real brands), then back through `capture_page.py`. Prefer MCP/CLI steps over manual clicking, and keep every tool reachable as a command. See `docs/system/redesign-tool-api-integration.md`. (2026-09-13)

### Real brand assets only — never recreate a logo (hard rule, project-wide)

For any rebuild of a real business (CRO Fix, Static Ad, client audit): **use the business's real logo file, downloaded from their live site, embedded as-is.** Never redraw as text/CSS/SVG approximation — including text/wordmark logos (the typeface IS the identity). Same for icon sets, badges, seals, trust graphics. Product photos: prioritize the real photo (optimized is fine). If an asset genuinely can't be retrieved, say so plainly rather than substituting a recreation. The entire pitch rests on "this is genuinely your page, just fixed."

---

## 🎨 EXPORT / GRADIENT / RENDER RULES

* **CSS gradients allowed on backgrounds only.** `background: linear-gradient(...)` / `radial-gradient(...)`, glow blobs, bars, buttons are fine.
* **Gradient text forbidden — CSS or SVG.** No `background-clip:text`/`text-fill-color:transparent`, no `<text fill="url(#grad)">`. Text is solid colours only (`#FF9500`, `#fff`, theme accents).
* **html2canvas compatible:** `html2canvas({ scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#080808', logging: false })`. Chrome-hiding uses `visibility:'hidden'` (NOT `display:'none'`). Always hide `[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap`. Always save/restore `track.style.transform`/`transition` in a `try/finally`, and `waitForSlideAssets(slide)` + double `requestAnimationFrame` before capture. `captureSlide()` must use the exact pattern from the project-constitution.md.

### Export bugs — do not re-introduce
1. Swipe arrow / chrome bleeding into the download → `visibility:'hidden'` + finally-restore.
2. Slide position lost after capture → save/restore transform+transition in try/finally.
3. Fonts/images not ready → `waitForSlideAssets` + double `requestAnimationFrame`.

**Verify by exporting, not by reading markup.** Review HTML is not the deliverable; the output is. Drive the file's own capture function via headless Playwright (see `.ai-workflow/tools/README.md`) and look at the result.

---

## 👤 RIDWAN'S BRAND PHOTOS (CLOUDINARY — never local relative paths)

| Use | URL |
|---|---|
| LK header + serious CTA | `https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss` |
| Smiling / warmer CTA | `https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2` |

Local relative paths break html2canvas. Always Cloudinary.

---

## Cowork Responsibilities (local pipeline manager)

* **JSON ingestion:** detect exports, validate structure, merge into `SYNC_DATA.items`. Never overwrite; use `id` to dedupe; skip duplicates.
* **Update central system:** open `ridwan_content_system_updated.html`, replace ONLY the JSON inside `#cowork-sync-data`, preserve all UI code.
* **Month management:** if a new `monthSlug` is missing, add it to `SYNC_DATA.months`.
* **File linking (critical):** every post MUST link to its HTML file; verify `folder` exists, flag if missing, never create entries without a valid file.
* **Status handling:** Idea / Created / Ready / Published. Can set to "Created" after generation; NEVER auto-set "Published".
* **"Created" means fully exported, not just authored (added 2026-09-21, Ridwan's instruction).** A generation task (Tips, CRO Fix, Static Ad, Template Showcase) does not mark an item `"Created"` until it has ALSO driven the page's own capture/export step and saved the real PNGs/videos to disk — the same "verify by exporting" standard this file already holds every build to. An HTML file with client-side-only `captureSlide()`/`dlSlide()` buttons that were never actually clicked is not `"Created"`, it is still in progress; leave it out of SYNC_DATA (or leave its status short of `"Created"`) until the real files exist.
* **Distribution assembly only picks and schedules — it never renders (added 2026-09-21).** `koolestpro-weekly-distribution-assembly` (and any task following `docs/system/02-distribution.md` / `.ai-workflow/tools/DISTRIBUTION.md`) picks up items that are already `"Created"` with real on-disk assets and slots them into the calendar. It must NEVER attempt to render, capture, or export an asset itself (no ad-hoc Playwright installs, no manual screenshotting) — that is strictly the generation task's job, per the rule above. If an eligible item has no exported assets on disk (or its registered `folder` doesn't match a newer build that superseded it), distribution assembly skips it, flags it by name, and leaves a short note for the generation task to finish — it does not try to fix the asset gap itself.
* **Remove Notion dependencies:** replace "Send to Notion" with "Export JSON → Cowork ingestion".
* **Error handling:** reject missing `id`, missing `folder`, invalid JSON, duplicate IDs.
* **Constraints:** do not modify UI structure, do not remove existing data, do not generate fake metrics, always preserve the brand system.

---

## 📸 NO IMAGE CREDITS — PROMPT-PACK HANDOFF (project-wide)

Applies to every stream that generates images (static ads, store-template product shots, rebuild hero images, carousel cover visuals).

**Static Ads: the prompt pack IS the default (2026-09-18).** Static Ad runs never call a paid image API unless Ridwan asks for generated images in that request ("generate the images", "use the API"). The default run researches, writes the copy, and exports the prompt pack below; Ridwan runs it in ChatGPT and sends the images back. Static ads were the main OpenAI spend.

**Every other stream: fallback order (2026-09-18).**
1. `gpt-image` (OpenAI) if it has credits.
2. **Cloudinary `generate-image`** (MCP, free plan: 50 generations per month, models include nano-banana, FLUX, Ideogram, Recraft, gpt-image). Check `get-usage-details` → `image_generation.usage < limit` first. It was 50/50 on 2026-09-18.
3. For rebuild hero images only: the page builder's own image generation (Lovable/Figma Make), which spends builder credits, not OpenAI.
4. Otherwise a **prompt pack**. Never silently spend on another paid service (inference.sh only if Ridwan names it). Stock (Pexels/Pixabay/Unsplash) is fine for backgrounds and scenes, never as a stand-in for a real product.

**Write `.ai-workflow/pending-{stream}-{slug}.md`** containing: the block detail/error + keys tried; target/product selection and why; the research table (every real, traceable claim + source); the prompts verbatim/copy-paste ready (self-contained fenced block per image, size + intended filename above each, "reading exactly:" quoting); the captions (humanizer-checked); a "still to do on return" checklist with pipeline constants. Then present the file in chat.

**Register nothing until real files exist.** On a blocked run: no pipeline record, no `usedFor`, no social-content pair, delete the empty `outputs/` folder. Say plainly nothing shipped. Do not improvise a renderer or let PIL draw ad copy.

**Ingesting when Ridwan returns the exports:** save images to the real output folder under the exact filenames; look at every image before accepting; assemble derived assets (2x2 showcase + size-checked `-x` for X); build `index.html`; register what was skipped (status `Created`, `usedFor`, social-content pair); present `index.html`; delete the pending file. Note in the record that images were produced manually via ChatGPT.

---

## 🏪 STORE TEMPLATE LAUNCH CONTENT — MANDATORY (every template)

A template is not finished when it passes QA; it is finished when the content that sells it exists and reaches the distribution queue.

1. **Brand the packaging in generated product imagery** — put the brand wordmark on the product in the prompt (`a cream label reading exactly "LUMORA" in small spaced capitals`), `--quality low`, verify spelling. Lumora's 16 existing unbranded images are the documented exception; re-shoot when budget allows.
2. **Every finished template ships a post set** — LinkedIn (showcase angle), Instagram (**always a 6-slide carousel**, `docs/system/template-showcase-ig-carousel.md`, 2026-09-27), X / five angles: showcase, free-offer/Nigeria package, niche-targeted, build-in-public, full-page-at-a-glance (`mobile-strip`).
3. **The mockup images are the post assets.** Pair deliberately: `preview.png` → showcase + niche; `cover.png` → LinkedIn + free-offer; `full-page.png` → build-in-public; `mobile-strip.png` → full-page-at-a-glance.
4. **Register like any other content** — `{brand-slug}-social-content.md`/`.json` keyed `TS-{BRAND}-*`, pipeline record type `"Template Showcase"`, status `"Created"`.
5. **A finished template MUST reach the distribution queue** (2026-09-01). Route via `.ai-workflow/tools/harvest_store_template.py` (NOT `harvest_content.py`), never leave it with zero distribution rows. Stream picked from `isConceptBrand`: `Store Template` (concept, free-offer) vs `Store Template (Paid)` (paid CTA). X #4 matches `full-page-x` (never oversized `full-page`); X #5 matches `mobile-strip`. Back-to-back builds stagger themselves via `find_open_week()`.

Against every generated caption: no em dashes, run through `humanizer`, real line breaks, no hashtags on X, and never imply a concept brand was a real client. This is the stream where X caption length is a hard gate — X captions ran 282-475 chars on Lumora/Meridian and failed the 280 cap.

---

## 📚 PER-BRAND SOCIAL CONTENT LIBRARY — `{brand-slug}-social-content.md` / `.json`

The canonical answer to "how do I get the caption for a given generated image when it's time to automate posting." One growing file pair per brand at the project root.

* `{brand-slug}-social-content.md` — human-readable, key table + fenced caption blocks.
* `{brand-slug}-social-content.json` — machine-readable sibling, same keys; the durable source of truth for any autopost step. Update both together, never drift.

**Key scheme:** Static Ad `SA-{BRAND}-*`, CRO Fix `CRO-{BRAND}-*` (`-BA`/`-ANNO`/`-CAROUSEL`/`-X1..3`), Template Showcase `TS-{BRAND}-*` (`-COVER-VID`/`-LAPTOP-VID`/`-MOBILE-VID`/`-COVER-IMG`/`-PREVIEW`/`-FULLPAGE`/`-MOBILESTRIP`), Tip `TIP-{BRAND}-COVER`/`-CAROUSEL`/`-X1..3`. The `-GRAPHIC-A/B/C` standalone graphics are retired (2026-07-18) — never create them.

When one visual has multiple caption angles, use `captionOptions: [{id, caption, hashtags}]` — pick one at post time. The `.json` file wins if it and the pipeline item's `captions`/`assets` fields disagree.

**Known gap:** a caption is only useful once its image exists on disk. Some graphics are generated only client-side via html2canvas download buttons nobody may have clicked. Check `knownGaps` before assuming an `assetPath` is real. To resolve, drive the page's own capture function via headless Playwright (call `captureSlide(idx)`, `page.expect_download()`, `save_as()` to the correct path) — never a generic browser screenshot, never route image data through the conversation. Then actually LOOK at the export; `v1ce-social-content.json` documents a trust-badge claim that looked fabricated but was real.

---

## 📅 LINKEDIN + DISTRIBUTION QUEUE CONSTRAINTS

* **LinkedIn: max 1 post/day, hard cap.** Never more than one row on the same `scheduled_date` on LinkedIn, even at different times. Check every other LinkedIn row on a date before scheduling. Twitter is exempt from a daily cap.
* **No two rows on the same platform** may share the same exact `(scheduled_date, scheduled_time_local)`. A LinkedIn and a Twitter post at the same time are fine. Use standard slots `09:00/13:00/18:00/23:00`; if a day is full, space additional times ≥60-90 min apart. Before calling the reschedule webhook, pull the live sheet and confirm the target slot is free (the webhook blind-overwrites and does not check).
* **A 200 from the reschedule webhook is not proof it landed** — re-read the affected rows after calling it.
* `koolestpro-populate_sheet.py` handles fresh batches correctly via `find_open_week()`; known caveat — `taken_keys` is seeded only from local `queue.json`, not a live sheet read, so it can drift.
* **Never auto-publish.** Every generator stops at status `Created`; `Published` is only set by the real posting step.

---

## ⚠ STANDING CONSTRAINTS (sandbox / workflow — bite regardless of sub-project)

* A cloud bash call dies near **178 seconds** (not 45s), and **background processes do not survive between calls** — each call gets a fresh PID namespace, so `nohup ... &` is silently reaped. Run slow scripts directly in a normal terminal, not Claude's chat loop.
* **Never auto-publish.** Every generator stops at status `Created`.
* **Instagram is PAUSED (2026-09-18)** after a `scraping_warning` on @koolestpro. Do not re-enable the Make IG route (filter deliberately reads `Instagrams`) or post via `instagram_client.py` until Ridwan says so. **No automated browser (Claude in Chrome, computer use, BrowserAct profiles, downloader extensions) may ever load instagram.com in Ridwan's logged-in session.** See `docs/system/instagram-warning-investigation-2026-09-18.md`.
* **Never invent a client result**; never imply a concept brand was a client (KURA/HALOS/MERIDIAN/Lumora).
* **Never recreate a real brand's logo** — pull the real file.
* **No em dashes** in any generated copy; run everything through `humanizer`.
* **No gradient text**, CSS or SVG — solid colours only (breaks html2canvas).
* **Verify by looking at the output**, not the markup.
* **Verify by exporting, not by reading source** — export via the page's own capture function, then inspect.
* **Keep the instruction surface slim** — `AGENTS.md` (injected every request), this file and `SYSTEM-MAP.md` have a context budget (see `docs/system/07-infrastructure.md`). Trim, or move detail to a scoped doc. Never let the rulebook regrow toward the old 116KB.

---

## GIT / IGNORE

There is no git repo at this root today. Sub-projects (`site/`, `cold-email-app/`, `replo-rebuilds/`) each have their own `.gitignore`. Media-heavy dirs (`replo-rebuilds/`, `video-gen/`, `outputs/`, `site/.next/`) should be treated as build artifacts — exclude from any future top-level repo, and keep out of the routine read surface. Prefer a root `.gitignore` over duplicating if one is ever created.

---

## How to read this file correctly

* **You are executing one task** → go to the router, read that row's scoped doc. Do NOT read the whole file or other rows.
* **You are building/re-filing** → read `SYSTEM-MAP.md`.
* **You need to know WHY a rule exists or what was tried before** → read `docs/system/00-claude-md-archive-2026-09-08.md`.
* **Every content decision** → the four project-wide rules + the generated-copy rules above are the floor.

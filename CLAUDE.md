# Koolestpro Cowork System — Rulebook & Task Router

> **STOP — before anything else:** identify the task, open the `TASK ROUTER` table below, read ONLY that row's linked docs, then start work. Do not read this whole file, other router rows, `SYSTEM-MAP.md`, or the archive unless the row you're on says to. A greeting or a question with no task attached needs none of this — just answer it.


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
| Tips carousel (`koolestpro-tips-weekly`, content engine) | 1 | `docs/system/quality-ratchet.md` (the bar to beat, Tips row), `docs/system/social-content-library.md` (caption registration), **`docs/system/tips-v4-format.md`** (the format, 2026-09-27; bar = `references-for-posts/tips-v4-prototype-2026-09-27/`), `docs/system/tips-old-style-format.md` (the 2025 references it builds on), `.ai-workflow/tools/README.md`, `docs/system/01-content-production.md` |
| CRO Fix weekly (`koolestpro-weekly-cro-fix`) | 1 | `docs/system/quality-ratchet.md` (CRO rows), `docs/system/export-render-rules.md`, `docs/system/social-content-library.md`, `docs/system/cro-3-slide-carousel-format.md` (the post format), `docs/system/cro-headline-system.md` (the headline), `docs/system/cro-redesign-standard.md` (the rebuild quality bar), `docs/system/rebuild-tooling-and-quality.md` (where the rebuild gets made), `docs/system/page-build-brief.md` (the Lovable/Figma input brief), `docs/system/redesign-tool-api-integration.md` (which tool, and how to connect it), `docs/system/x-caption-playbook.md` (the X caption), `.ai-workflow/weekly-pipeline.md`, `docs/system/01-content-production.md` |
| Static Ad weekly (`koolestpro-static-ad-weekly`) | 1 | `docs/system/image-sourcing-fallback.md` (prompt-pack default), `docs/system/quality-ratchet.md` (Static Ad row), `docs/system/social-content-library.md`, `.ai-workflow/skills/static-ad-image/`, `docs/system/01-content-production.md` |
| Template Showcase weekly (`koolestpro-template-showcase-weekly`) | 1 + 5 | `docs/system/store-template-launch-content.md`, `docs/system/social-content-library.md`, `docs/system/quality-ratchet.md` (Template Showcase row), `docs/system/template-showcase-ig-carousel.md` (Instagram = always a carousel), `.ai-workflow/skills/page-presentation-kit/`, `replo-rebuilds/CLAUDE.md`, `docs/system/01-content-production.md` |
| Weekly template build (`koolestpro-weekly-template-build`) | 5 | `replo-rebuilds/CLAUDE.md` |
| Distribution assembly + health check (`koolestpro-weekly-distribution-assembly`, `koolestpro-distribution-health-check`) | 2 | `docs/system/distribution-queue-constraints.md`, `.ai-workflow/tools/DISTRIBUTION.md`, `docs/system/02-distribution.md` |
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

Moved out of CLAUDE.md on 2026-09-27 to keep the always-loaded rulebook small. Full rules: **`docs/system/quality-ratchet.md`** — read it only when a task actually needs this (quality ratchet); do not read it for unrelated tasks.
---

## ⚠ PROJECT-WIDE GENERATED-COPY RULES (apply to EVERY skill/task, not just one)

These apply to every LinkedIn caption, X post, carousel slide, static ad text, CRO fix caption, and anything else this project generates:

1. **No em dashes, anywhere.** Scan for "—" / `&mdash;`; rewrite as two sentences, a comma, or a colon.
2. **Run every piece of copy through the `humanizer` skill** before treating it as final. That means the **full v3.0 eleven-pass pipeline** (writer, editor, fact-checker, anti-AI style, AI-word check, AI-pattern check, voice match, humanizer, red pen, self-critique, final blocklist), anchored in `VOICE.md`. This covers **all** written output: carousels, static ads, website/page copy, mockups, post captions, outbound email, and content-system titles. Full routing and per-stream checklists: **`docs/system/humanizer-guideline.md`**. Headlines additionally follow `docs/system/cro-headline-system.md`. **X/Twitter captions additionally follow `docs/system/x-caption-playbook.md`** (the anatomy and four proven patterns drawn from Ridwan's own best-performing posts).
3. **Export-ready formatting:** real line breaks (never markdown `\n` literals or asterisk stand-ins), and the X-vs-LinkedIn convention — no hashtags on X, hashtags fine on LinkedIn/Instagram.
4. **X caption hard 280-char limit, always counted.** Count the real string (newlines included) against 280 before calling it done, independent of `populate_sheet.py`'s automated flag. A caption at/over 280 chars is not postable; shorten it before shipping. Check every time a Twitter caption is produced or re-touched.
5. **Caption = image (2026-09-28).** A caption that posts with one image describes that image only; write it while looking at that PNG. Only a multi-image post (carousel, combined showcase) may say "four ads", "swipe" or "slides". Every single-image caption is keyed to its image (`data-asset` / `tab-x-*` in the review page, `assetPath` + `captionKey` in the social-content library). `populate_sheet.py` never borrows another image's caption and holds a row as Draft when `.ai-workflow/tools/caption_fit.py` flags it. Run that script before finishing any content task.

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

Moved out of CLAUDE.md on 2026-09-27 to keep the always-loaded rulebook small. Full rules: **`docs/system/export-render-rules.md`** — read it only when a task actually needs this (export / gradient / render rules); do not read it for unrelated tasks.
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
* **Update central system:** never `Read`/open the 276KB `ridwan_content_system_updated.html` directly to make this edit. Use `.ai-workflow/tools/sync_content_system.py` (or a similarly targeted regex patch against the `#cowork-sync-data` script block) so the file's contents never have to pass through the model. Preserve all UI code; `.bak` is written automatically.
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

Moved out of CLAUDE.md on 2026-09-27 to keep the always-loaded rulebook small. Full rules: **`docs/system/image-sourcing-fallback.md`** — read it only when a task actually needs this (no image credits — prompt-pack handoff); do not read it for unrelated tasks.
---

## 🏪 STORE TEMPLATE LAUNCH CONTENT — MANDATORY (every template)

Moved out of CLAUDE.md on 2026-09-27 to keep the always-loaded rulebook small. Full rules: **`docs/system/store-template-launch-content.md`** — read it only when a task actually needs this (store template launch content); do not read it for unrelated tasks.
---

## 📚 PER-BRAND SOCIAL CONTENT LIBRARY — `{brand-slug}-social-content.md` / `.json`

Moved out of CLAUDE.md on 2026-09-27 to keep the always-loaded rulebook small. Full rules: **`docs/system/social-content-library.md`** — read it only when a task actually needs this (per-brand social content library); do not read it for unrelated tasks.
---

## 📅 LINKEDIN + DISTRIBUTION QUEUE CONSTRAINTS

Moved out of CLAUDE.md on 2026-09-27 to keep the always-loaded rulebook small. Full rules: **`docs/system/distribution-queue-constraints.md`** — read it only when a task actually needs this (linkedin + distribution queue constraints); do not read it for unrelated tasks.
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
* **Rotate growing logs, don't let them become full-file reads.** `distribution-health-log.md` keeps only its most recent 5 entries (older ones move to `docs/system/distribution-health-log-archive.md`, added 2026-09-27) — apply the same pattern to any other log/journal file in this repo once it passes a handful of entries: append-only files are for writing, not for re-reading in full on every run.

---

## GIT / IGNORE

There is no git repo at this root today. Sub-projects (`site/`, `cold-email-app/`, `replo-rebuilds/`) each have their own `.gitignore`. Media-heavy dirs (`replo-rebuilds/`, `video-gen/`, `outputs/`, `site/.next/`) should be treated as build artifacts — exclude from any future top-level repo, and keep out of the routine read surface. Prefer a root `.gitignore` over duplicating if one is ever created.

---

## How to read this file correctly

* **You are executing one task** → go to the router, read that row's scoped doc. Do NOT read the whole file or other rows.
* **You are building/re-filing** → read `SYSTEM-MAP.md`.
* **You need to know WHY a rule exists or what was tried before** → read `docs/system/00-claude-md-archive-2026-09-08.md`.
* **Every content decision** → the four project-wide rules + the generated-copy rules above are the floor.

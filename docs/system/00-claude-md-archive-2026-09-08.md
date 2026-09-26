# Koolestpro Cowork System — Local JSON Architecture

> **⚠ Reversal note 2026-09-08 (see live `CLAUDE.md`):** this archive holds the *original* rulebook. Since it was written, the AI-workflow contract changed: Claude now **authors output HTML directly** (one place, one model) and DeepSeek delegation is the exception, not the default. It was also slimmed from a 1664-line rulebook+decision-log into live rules plus a task router — this file preserves the full dated narrative and "corrected v3/v4/v5" reasoning that the slim file no longer carries. Read this for *why* a rule stands; read the live `CLAUDE.md` for what's enforced now. The delegation-economics analysis (deepseek offloaded ~95k output tokens vs ~47M/month context) is what prompted the revert.
>
> **Quality-ratchet references set 2026-09-08.** The "current best" bar per stream was traced back to the original reference files and verified on disk, then recorded in the live `CLAUDE.md` table. Notable: the CRO Fix stream was originally seeded from `templates/eddie_bauer_cro_content_v2 (1).html` (external) and `outputs/cro-fixes/ecobioboutique_cellulite-remover_content.html` (first own file); the corrected current-best that implements every standing rule is the caraway run + `.ai-workflow/build_caraway_graphics.py`. The bar a build must beat is the corrected current-best; the original seed is the floor (never regress below its intent).

---

## ⚠️ SCOPE EXPANDED 2026-08-02 — this project is no longer content-only

This project began as a content production and automation system. As of 2026-08-02 it is the operating system for **all** of Koolestpro's client acquisition, of which content is one of five tracks.

**Start at `SYSTEM-MAP.md` (project root, added 2026-09-04).** It is the inventory: the seven sub-projects, what state each is in, and where a new piece of work belongs. `SYSTEM-STATUS.html` beside it is generated from real files by `.ai-workflow/tools/build_system_status.py` and is the only place to trust for live counts and dates. Per-sub-project detail is in `docs/system/01-…` through `07-…`. **This file is the rulebook, the plans below are the strategy, `SYSTEM-MAP.md` is the inventory.** Do not restate one inside another.

**Two source-of-truth plan docs, read the right one:**

| Doc | Covers |
|---|---|
| `docs/koolestpro-content-operating-plan.md` | Content production: Tips, CRO Fix, Static Ad, Template Showcase, TikTok, trend radar. Steps 1-11. All existing machinery, unchanged. |
| `docs/koolestpro-growth-operating-plan.md` | Everything around content: the domain and selling site, proof/case studies/reviews/referrals, outbound, SEO + AEO + directories, the free sample-site engine, and a gated ads plan. Tracks A-F. |

**Why the split happened:** a 2026-08-02 planning interview found the content system had no destination to send anyone to (no domain, no published prices, no real case studies), and that the outbound machinery it feeds had been built but never fired. The production machinery is fine; it needed a destination, proof, and an outbound arm around it.

**Content is Ridwan's best client channel — do not re-derive this, it was gotten wrong twice on 2026-08-02.** Six clients trace to content: Jellys Glamour plus two foreign PageFly clients from **TikTok build videos**, and aminazaid.com → justdarlings → scentsavenue.ng from **LinkedIn/YouTube teaching content**. Fiverr produced two (Tap and Rate, Champion Biotics). Outbound has produced none because it has never been sent.

What changed is what the content asks for. Old content ("watch me build a store", "here's how to fix yours") was a **service signal** and buyers responded. Current craft carousels are an **employment signal**, and the market responds accurately: recruiters and interviews, no projects. Craft mode stays for authority and portfolio; it just stops being the only thing running.

**Two markets, deliberately different** (2026-08-02): **Nigeria/Africa** targets businesses already running Meta/TikTok ads who sell through DMs, wedge is a free ad creative then a free frontend-only sample site, channel is Instagram DM, prices in Naira. **International** targets Shopify brands at $10-200k/mo, wedge is a hero-section teaser then a live rebuild, channel is email first, prices in USD. One domain with separate landing pages per market. Never blend the copy.

**Four rules that now apply project-wide:**

1. **Every content CTA points at a real destination** — a service page or case study on the domain — not at engagement.
2. **Never invent a client result, and never imply a concept brand was a client.** KURA and HALOS are concept builds and must always be labelled as such. With real case studies now in scope this is the highest-stakes rule in the project.
3. **Local-first still holds, including for the CRM.** `outreach_tracker.json` is the outbound system of record. The Notion cold-DM app is replaced, not migrated.
4. **Two pools, split by whether the prospect has an auditable URL.** ⚠️ **CORRECTED 2026-09-04** — the original 2026-08-02 wording of this rule said "one segmented prospect pool: `targets_pool.json` carries a `segment` field and serves both content selection and outreach, do not fork it into a second file." That was never implemented and has been superseded in practice, by Ridwan's own later decisions. The `segment` field is not in `targets_pool.json`'s `meta.recordSchema` and no target has ever carried one. On 2026-08-11 Ridwan was asked directly and chose to route Nigeria/Maps leads into a separate, lighter file rather than force-fit them into `targets_pool.json`, precisely because that schema assumes every record has a real `url` worth auditing and local businesses with no storefront don't have one. Reviewed 2026-09-04 and confirmed: the split is the right shape, so the rule is amended to match reality rather than the data being backfilled to match the old rule.

   **`targets_pool.json` — the content-production pool.** International DTC/Shopify brands with a real, live, auditable page. Feeds CRO Fix, Static Ad and Template Showcase target selection. Every entry has a `url`; that is what makes it eligible. All 12 current entries are international DTC (Minimalist, Versed, TAPro, V1CE, Gainful, Transparent Labs, Caraway, Material Kitchen, Cuts Clothing, Kyte Baby, Bebemoss, Obvi). Rotation is tracked per-stream in `usedFor`, not by `status`.

   **KoolestFlow — the outbound pool.** Fed by the two weekly discovery sources (BrowserAct/Maps Tuesdays, Meta Ad Library Wednesdays) through the hybrid cloud-scores/Mac-imports pipeline, with `.ai-workflow/taken-brands-ledger.json` preventing any brand from being pushed twice across sources. `dm_leads_pool.json` is a historical staging log from before KoolestFlow was identified as the real destination, not a third pool.

   **The pool boundary is the segmentation.** Which file a prospect is in already says which market and which motion it belongs to, so a `segment` field would only restate that. Do not add one, and do not merge the two pools. What is still worth doing, and is not done: nothing currently stops a business from existing in both (a Nigerian brand that does have a site could in principle be picked up by Maps discovery and separately added to the content pool by hand). No collision has happened yet, and the taken-brands ledger covers the outbound side; flagging it here rather than building a cross-pool check nobody has needed.

---

## AI Workflow Architecture

Claude is the **Master Architect** in this project. DeepSeek is the **implementation worker**, called directly through its API from inside Cowork — there is no manual OpenCode Desktop hand-off step anymore (as of 2026-07-05). Everything stays inside one Claude/Cowork session.

Claude's job is intelligent orchestration — not maximum token generation.

### Claude Retains (Always in Claude)
- Content strategy: deciding what posts to create, what angle to take
- System architecture: JSON structure, pipeline design, sync logic
- JSON ingestion and syncing into `ridwan_content_system_updated.html`
- Deciding post topic, copy direction, and structure for each piece
- Brand voice, CRO decisions, quality review
- Debugging complex export/render issues
- Final QA approval of all generated HTML

### DeepSeek (via API) Implements (Never write in Claude)
- Output HTML files: tip posts, CRO fix posts, carousel slides
- Skill HTML generators (Skill D, Skill E, Content Engine outputs) — but only their HTML/graphics output; caption *text* itself (Skill D's actual job) is plain markdown and Claude writes that directly
- Repetitive UI creation, section scaffolding, slide layouts
- CSS cleanup, responsive adjustments
- New HTML tool pages or generator files
- Any file that is primarily code output

### Automatic Delegation Trigger
When a request involves building an HTML output file or generator, Claude does NOT write it.

Claude creates `.ai-workflow/deepseek-task.md` — a concise spec — then runs it directly via terminal:

```bash
node run_deepseek_task.js
# or: npm run deepseek-task
```

This calls DeepSeek's API (`lib/cowork_runtime.js` → `callDeepSeek`), reads back the generated file(s), and writes them straight into the project. No copy-pasting into another app, no leaving Cowork.

To override and have Claude code directly, say: **"build it yourself"**

---

### Running a delegated build (current, automated)

1. Claude writes `.ai-workflow/deepseek-task.md` per the Task File Format below.
2. Claude runs `node run_deepseek_task.js` in the terminal.
3. **A single terminal command in this environment has a hard ~45-second ceiling.** Full HTML builds often need more generation time than that, so the script does ONE DeepSeek call per run:
   - If the model finishes cleanly, the file(s) listed under the task's `FILES:` section get written to disk immediately and the command reports what it wrote.
   - If the model runs out of output tokens mid-file (`finish_reason=length`), the script saves everything generated so far to `.ai-workflow/deepseek-output-log/<timestamp>.partial.md` and prints the exact follow-up command:
     `node run_deepseek_task.js --continue-from=<that path>`
   - Claude just runs that follow-up command (usually once, sometimes twice for a large multi-file build) until it reports "Files written." This is normal, expected behavior — not a failure.
4. **Model choice matters and is not obvious.** `run_deepseek_task.js` defaults to `deepseek-chat` (non-reasoning). The `DEEPSEEK_HEAVY_MODEL`/`DEEPSEEK_LIGHT_MODEL` aliases in `.env` (`deepseek-v4-pro`/`deepseek-v4-flash`) put the model into reasoning mode, which — tested empirically on this project's real CRO-rebuild task — can burn the *entire* token budget on internal `reasoning_content` and return zero characters of actual file content, even at `reasoning_effort:"low"` (the lowest the API accepts; valid values are `low`/`medium`/`high`/`max`/`xhigh`, there is no `"none"`). Since a task spec written by Claude has already done the reasoning, non-reasoning mode is the right default. Only pass `--reasoning` if a future task genuinely needs multi-step thinking mid-generation, not just faithful execution of a fully-specified spec.
5. Reference files (`skills/*.md`, the audit brief, etc.) that the task spec points to are inlined automatically by the script so DeepSeek can "read" them — but `skills/*.md` files and top-level docs (`CLAUDE.md`, `docs/koolestpro-content-operating-plan.md`) are excluded from auto-inlining on purpose: they're long and mostly generic, and a well-written task spec should already distill the specific rules that matter for that one build into its own `RULES:` section. Write task specs that way — self-contained, not "go read the whole skill file to figure out what applies here."

### Task File Format

When delegating, Claude creates/overwrites `.ai-workflow/deepseek-task.md`:

```
TASK: [one-line objective]

CONTEXT:
[Post type, brand/slug, what already exists — only what's needed]

FILES:
- [exact relative path to create/edit]

RULES:
- [Pull relevant constraints from .ai-workflow/project-constitution.md]
- [Add task-specific rules — gradient handling, export compatibility, etc.]

OUTPUT:
[Complete self-contained HTML file]

NOTES:
[POST_BRAND, POST_SLUG, POST_TYPE, POST_FOLDER constants to set,
 any copy blocks, avatar paths, slide content, pipeline export requirements]
```

Always follow: `.ai-workflow/project-constitution.md`

**REFERENCE OUTPUT (Gold Standard):** `outputs/tips/funnel-awareness-framework_2026-05-10.html`
Every new carousel task spec must reference this file. DeepSeek must match its structure, JS patterns, and section layout exactly.

### ⚠️ Tips Carousel — Corrected Gold Standard Spec (2026-07-12, overrides `koolestpro-content-engine` skill)

Auditing the `koolestpro-content-engine` skill against the actual reference file above found real drift — the skill's own written spec (540×540 square slides, `scale:4` render + manual downsample to 1080×1080, and a `captureSlide()` sample with no chrome-hiding at all) does not match what the gold-standard reference file actually does (540×680 **portrait** slides, `scale:2`, explicit chrome-hiding, no downsample step). Cowork cannot edit the skill file itself — it's a read-only cache in this session (Settings → Capabilities is where Ridwan would edit the source if he wants it fixed there too; the corrected block below is what to paste in). Until then, **this section is the enforced spec for every Tip carousel built in this project** — it overrides anything the skill itself says about geometry or capture:

- **Slide size:** `540×680px` portrait (NOT 540×540 square). `#viewport`, `.slide`, `.gcard` all use `width:540px;height:680px`.
- **Capture:** `scale: 2` (not 4), direct `html2canvas(slide, {...})` output, **no manual downsample step** — the 2160×1360 canvas IS the deliverable, do not redraw it down to a square.
- **Chrome-hiding is mandatory in `captureSlide()`,** not optional — use exactly this pattern (matches the Confirmed Export Bugs section above):

```javascript
async function captureSlide(idx) {
  const slide = slides[idx];
  const toHide = document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
  toHide.forEach(el => el.style.visibility = 'hidden');
  const prevTransform = track.style.transform;
  const prevTransition = track.style.transition;
  track.style.transform = `translateX(-${idx * 540}px)`;
  track.style.transition = 'none';
  try {
    await waitForSlideAssets(slide);
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    return await html2canvas(slide, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#080808', logging: false });
  } finally {
    track.style.transform = prevTransform;
    track.style.transition = prevTransition;
    toHide.forEach(el => el.style.visibility = '');
  }
}
```

- **PDF export** uses `jsPDF({orientation:'portrait', unit:'px', format:[540,680]})`, not `[1080,1080]`.
- **Claude vs. DeepSeek authorship:** the `koolestpro-content-engine` skill's own text says "output one complete HTML file" as if Claude writes it directly — that conflicts with this project's AI Workflow Architecture above. Only Phase 1 of that skill (the internal SUCCESs-lens brief, framework/CTA/hook decisions, and the 5 post-copy tabs) is Claude's job. Phase 2 — the actual carousel HTML file — must be delegated to DeepSeek via the standard Task File Format, same as every other output skill. Never let Claude write the full HTML directly for a Tips carousel in this project.
- **Format default (established 2026-07-12, based on 2026 engagement data):** default new Tips carousels to a **Myth vs Reality / contrarian-diagnostic** angle ("you think X, actually Y") rooted in the Conversion Strategy pillar — this format drives comments via polarization and cognitive dissonance, which the LinkedIn/Instagram algorithms weight heavily as of 2026. Framework/methodology carousels (using Ridwan's existing frameworks) are the fallback when a topic doesn't have a genuine myth to bust — those drive saves rather than comments, still strong but a different lever. Both beat a generic "here are some tips" angle.
- **Slide count nudge:** LinkedIn carousels at exactly 7 slides outperform other lengths by ~18% in 2026 data. The skill's existing "default 8, less is always better" logic already trends the right direction — nudge the default down to 7 rather than 8 where the content genuinely fits, but don't pad a 6-slide idea up to 7 just to hit the number.

### ⚠️⚠️ TYPE SCALE — HARD FLOOR (2026-07-18, after Ridwan flagged the animation-budget carousel as unreadable)

The 2026-07-17 animation-budget carousel had correct geometry (540×680) but set all slide body copy at 10–13px. On a phone that is unreadable — a carousel slide is viewed at roughly a third of its rendered width. The gold standard (`funnel-awareness-framework_2026-05-10.html`) runs 15–16px for primary body copy; the run had drifted ~3px smaller across every element.

**Floor for anything inside a `.slide`:**

| Role | Size | Notes |
|---|---|---|
| Primary body prose | **15px**, `line-height:1.7` | DM Mono is correct here — the gold standard uses mono for body. The problem was never the typeface. |
| Secondary / nested body (list items, chips, pills, footnotes) | **13px minimum** | never below |
| Slide footer credit | **12px** | |
| Eyebrow / section labels | 9–12px **only if** `text-transform:uppercase` + letter-spacing | these are the sole exception to the floor |
| Headline | 30–42px | statement slides may go larger |

Nothing inside a slide goes below 12px unless it is an uppercase tracking label.

**No dead space.** If a slide's content stops more than ~15% short of the bottom edge, the layout is wrong — give the content container `flex:1` with `justify-content:space-evenly` (list slides) or `center` (statement slides) so it fills the frame. Check this on the rendered PNG, not in the markup.

**Standalone graphic cards are retired (2026-07-18, Ridwan's call):** the `.gcard` / `graphic-a|b|c.png` single-image quote graphics are no longer produced. Do not add the `posts-shell` graphic-card block to new Tips carousels, and do not create `TIP-{BRAND}-GRAPHIC-A/B/C` keys in the brand social-content files. The carousel slides plus the cover are the deliverables. (Keep `.gcard-wrap` in the `toHide` export selector — it is harmless and guards against regressions.)

**Verify by exporting, not by reading markup.** `.ai-workflow/tools/export_tip_slides.py` (added 2026-07-18) drives headless Chromium against a finished tips HTML and calls the file's own `dlSlide(i)`, intercepting each download — byte-identical to clicking the on-page buttons, unlike a generic browser screenshot. Run it and actually look at every slide before calling a carousel done:

```bash
export LD_LIBRARY_PATH=$HOME/pw/xd/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
python3 .ai-workflow/tools/export_tip_slides.py outputs/tips/<file>.html outputs/tips/<assets-dir>/
```

---

### ⚠️⚠️ Tips Carousel — V2 Density + Visual Variety Format Now Default (2026-07-29, Ridwan approved)

Ridwan reviewed the V2 prototype (`outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html`) across several rounds of feedback and confirmed it's approved: "this is much better." Two things now change for every future Tips carousel, not just this one file.

**Reference file updated.** `outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html` is now the reference output for the Tips post type specifically — supersedes `funnel-awareness-framework_2026-05-10.html` for Tips carousels. (That older file remains a valid reference for the underlying geometry/JS mechanics more broadly, since the V2 file inherited them via region-swap and is fully compliant with the 540×680/scale:2/chrome-hiding spec above — nothing about the geometry rules changed, only the density and visual approach.)

**Density: headline-only + micro anchor** (already the standing rule from the 2026-07-28 direction check, restated here as now-shipped and approved) — one bold headline/statement per slide, at most one ~15-20 word subline, no bullet stacks, no multi-sentence paragraphs. Default slide count is 7, Myth vs Reality / contrarian-diagnostic format by default, framework fallback when a topic has no real myth to bust (unchanged from the 2026-07-12 direction).

**Visual Anchor & Variety System (new, 2026-07-29).** Ridwan explicitly flagged that visuals must not become a new "boring same template" problem the way text density used to be — the exact instruction: "make sure we are not always using the same templates all the time... We should have things interesting and compelling always." The full framework now lives in the `koolestpro-content-engine` skill's "Visual Anchor & Variety System" section; the short version:
- The cover slide always carries a supporting visual sized to dominate the frame (~35-45% of slide height) — never pure typography.
- Real screenshot vs. custom visual is decided by what the slide claims: use a real (Cloudinary-hosted) screenshot only when the image itself is the evidence for a literal UI-pattern claim; use a custom-built visual (CSS shapes, inline SVG, an Iconify icon) for conceptual/metaphorical claims. Never default to "real photo" for its own sake.
- Treatment menu to rotate across carousels: motion/ghost-trail shape stacks, icon-badge accents (Iconify, opposite a slide's eyebrow tag), real screenshot proof, stat/numeral hero, geometric/abstract SVG composition, treated real-world stock photo (Pexels/Pixabay) when no real screenshot of Ridwan's own work exists. Before starting a new carousel, glance at the most recently shipped Tips file in `outputs/tips/` and deliberately choose a different dominant cover treatment — two carousels in a row must not share the same cover concept.
- Confirmed-available asset sources: **Iconify** public API (`https://api.iconify.design/{prefix}/{icon}.svg?color=%23FF9500&width=N`, no API key, 200+ icon sets — fetch once and inline the raw SVG markup, never hotlink at capture time) and **Pexels**/**Pixabay** (`PEXELS_API_KEY`/`PIXABAY_API_KEY`, live in this project's `.env` and `video-gen/.env`, same keys the `stock-footage` skill uses).

**Execution method, unchanged from established practice:** build via region-swap, not DeepSeek delegation and not freeform Claude-authored HTML — start from the current reference file above and reuse its JS/CSS byte-for-byte via a small Python patch/build script, swapping only slide content strings and visual blocks. DeepSeek delegation is documented as unreliable specifically for this file type (drops mandatory sections, invents its own JS). Whichever script does the swap, always re-verify **whole-file div balance** (`<div` count == `</div>` count) and run a **live Playwright nav click-through** (click through every slide, confirm the swipe button stays pinned and hides correctly on the last slide) before calling a build done — a lazy regex slide-boundary match previously left orphaned markup that broke navigation in a way no static slide export could reveal.

---

## Global Content/Caption Rules (generalized 2026-07-29 — applies to EVERY skill, not just one)

These were previously scattered as per-skill rules (carousel slides only, Template Showcase only). Ridwan's 2026-07-29 instruction generalizes all of them project-wide, to every LinkedIn caption, X post, carousel slide, static ad text, CRO fix caption, and anything else this project generates:

1. **No em dashes, anywhere.** Scan for "—" / "&mdash;" before calling any piece of copy done, and rewrite as two sentences, a comma, or a colon instead. (Was previously scoped to "on any slide" only — now project-wide.)
2. **Run every piece of copy through the `humanizer` skill** before treating it as final — this was already a standing instruction, restated here so it isn't missed for content types outside the usual carousel/caption pipeline.
3. **Export-ready formatting:** real line breaks (never markdown `\n` literals or asterisks standing in for line breaks), and the existing X-vs-LinkedIn convention — no hashtags on X, hashtags are fine on LinkedIn/Instagram.
4. **Twitter/X caption character count — hard 280-char limit, always checked (added 2026-09-07, Ridwan's standing instruction).** Ridwan's words: "always try to make a character count on the caption of a Twitter post. The maximum we can do is 280 characters... whenever we are going to get an error message, the error I fixed recently was because of the character count." Any skill or task that produces a Twitter/X caption — `koolestpro-content-engine`, `static-ad-image`, `koolestpro-cro-caption-writer-skill-d`, Template Showcase/Store Template caption writing, the `koolestpro-weekly-distribution-assembly` and `koolestpro-distribution-health-check` scheduled tasks, or any ad hoc caption written directly in a session — must count the actual caption text against 280 characters before treating it as final, independent of whatever `populate_sheet.py`'s own automated flag does downstream. Don't estimate; count the real string (newlines included). A caption at or over 280 chars is not postable as-is — shorten it before calling the work done, don't ship it and rely on a later QA pass to catch it. This check runs every time a Twitter caption is produced or re-touched, not just when someone asks for it.

See "Page Presentation Kit — Export Routing → CORRECTED v4" below for the fuller writeup of why this generalization happened.

---

## Core Principle

This system is **local-first**.

* Notion is NOT used
* No external database is used
* The single source of truth is:

> `ridwan_content_system_updated.html`

All data is stored inside:

```html
<script id="cowork-sync-data" type="application/json">
```

Cowork must ONLY read and write to this JSON block.

---

## System Architecture

### 1. Source of Truth

* File: `ridwan_content_system_updated.html`
* Data: `SYNC_DATA`
* Structure:

  * meta
  * months
  * items

---

### 2. Content Outputs (Generators)

All content-generating HTML files (CRO content, content engine, etc.) must:

1. Export structured JSON
2. Save HTML file to `/outputs/...`
3. Provide file path inside JSON

---

## JSON Standard (MANDATORY)

Every generated post MUST follow this structure:

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
  "captions": {
    "linkedin": "string, optional — full LinkedIn caption text",
    "x": ["string, optional — array of X post variants"]
  },
  "assets": {
    "images": ["string, optional — relative paths to the finished image assets for this post"],
    "video": "string, optional — relative path if a video was produced"
  }
}
```

Rules:

* `id` must be unique
* `slug` must match file name
* `folder` must point to actual file
* No missing fields on the core (non-optional) fields

**`captions` / `assets` (added 2026-07-12 — autopost-ready fields, optional):** Every field the core standard has always required lives in the linked HTML file, which is fine for manual review but means a future Make.com/Sheets auto-post step would have to scrape HTML to get real post text and image paths. `captions` and `assets` exist so a pipeline record can optionally carry that directly as data — plain text/paths, no markup. Optional and backward-compatible: older items without them are still valid, and Cowork must never reject an item for lacking them. Populate them when the generating skill already has the final caption text and asset paths in hand (e.g. a scheduled weekly-buffer run) rather than going back to add them later. This does not change Step 8/9: populating these fields is not publishing, and status still only ever reaches `"Ready"` in Cowork — never `"Published"`.

**"Static Ad" type (added 2026-07-10):** Covers output from the static-ad-image skill — 4-angle ad showcases (problem/solution, benefit/result, social proof/trust, offer/urgency), for koolestpro content or client work. `folder` points to a lightweight companion HTML page at `outputs/static-ads/{slug}_{date}/index.html` that displays the 4 generated PNG ad images + combined LinkedIn showcase + X assets + captions, and carries the standard pipeline export button. The ad images themselves are PNGs produced by GPT-image, not html2canvas captures — the gradient-text/export-compatibility rules below apply only to the companion HTML page's own UI chrome, not to the AI-generated ad images.

**"Template Showcase" type (added 2026-07-12):** Covers output from Step 5 ("Weekly Template/Page Showcase") — desktop/mobile mockups of a real built page (via `page-presentation-kit`), packaged with a caption and optional walkthrough video. `folder` points to a companion HTML page at `outputs/templates/{slug}_{date}/index.html` (same pattern as Static Ad's `index.html`): mockup image(s) + combined presentation graphic + optional video + LinkedIn/X captions + the standard pipeline export button. See "Page Presentation Kit — Export Routing" below for the full companion-page pattern and the `koolestpro-template-showcase-weekly` scheduled task that produces it.

---

## 📺 SHOW HTML PREVIEWS IN CHAT — MANDATORY AFTER EVERY BUILD (added 2026-09-01, Ridwan's standing instruction)

After every successful build from any output skill, Cowork must present the actual HTML file(s) it just saved to `outputs/` directly in the conversation, not just describe them or give a file path. Ridwan's own words: "after every successful build I need to see the html preview of the rebuild and the html of the posts here, same thing you save into the outputs folder so that I can check quick."

**What to show, per stream:**

* **CRO Fix:** the `{slug}_rebuild.html` ("after" mockup) and the `{slug}_content.html` (full review pack — carousel, graphics, post copy tabs).
* **Static Ad / Template Showcase:** the companion `outputs/{stream}/{slug}_{date}/index.html` review page.
* **Tips / Content Engine carousels:** the carousel HTML file itself.
* Any future output skill: whatever HTML file is the human review surface for that build — the file a person would actually open to check the work, not an intermediate/working file.

**How:** use `mcp__cowork__present_files` (load via ToolSearch if deferred) on the exact files already written to `outputs/` — don't regenerate, re-copy, or re-render them for this step, just present what's already there.

**When:** this is a default close-out step for every build, not something reserved for runs where something went wrong or needs review. Do it every time, including on fully-unattended scheduled runs — Ridwan should never have to open the outputs folder manually just to do a quick check.

---

## 🚫 NO IMAGE CREDITS — PROMPT-PACK HANDOFF (added 2026-09-04, Ridwan's standing instruction, project-wide)

Applies to **every** stream that generates images, not just static ads: static ads, store-template product shots, carousel cover visuals, anything that would otherwise call `gpt-image`.

Ridwan's instruction: "Whenever there are no credits in GPT Image, we either use other models or you give me the prompts so that I can find a way to use ChatGPT without API to do it. When I get an export, I send it back to you. You take the image and register it wherever it is needed."

### The resolved protocol (Ridwan chose this shape 2026-09-04, do not re-derive it)

**Go straight to a prompt pack. Do not silently spend on a different paid service.** Alternative generators were checked on 2026-09-04 and the "use other models" half of the instruction turned out to have almost nothing behind it in practice:

| Generator | State, 2026-09-04 |
|---|---|
| gpt-image / OpenAI | `429 credit_balance_exhausted` on **both** keys (skill `.env` and project `.env` are different keys, same org billing) |
| Cloudinary `generate-image` | `image_generation: 50/50` — Free-plan AI quota fully consumed |
| inference.sh | key present, has image models, but prepaid real money with **no balance-check endpoint**, so spend is unverifiable up front |

So there is no free alternative sitting there, and the only paid one can't be checked before it bills. Ridwan's call: hand over the prompts rather than reach for inference.sh. Only use inference.sh if he asks for it by name on a specific run.

### What "hand over the prompts" means concretely

Write `.ai-workflow/pending-{stream}-{slug}.md` containing everything the run had already earned before it hit the wall, so the manual step is pure copy-paste and nothing needs re-researching:

1. **The block detail** — the actual error string, which keys were tried, so it's obvious this was a billing wall and not a bug.
2. **Target/product selection and why** — including the rotation reasoning, so a later run doesn't re-litigate it.
3. **The research table** — every real, traceable claim with its source. This is the expensive part; never let it evaporate.
4. **The prompts, verbatim and copy-paste ready.** One fenced block per image, each block self-contained, with nothing in it that assumes CLI flags. State size and the intended filename above each block. Keep the "reading exactly:" quoting so ChatGPT renders the text into the photograph rather than producing a caption card.
5. **The captions**, already humanizer-checked, so the return trip is images only.
6. **A "still to do on return" checklist** with the exact pipeline constants (`POST_BRAND`/`POST_SLUG`/`POST_TYPE`/`POST_FOLDER`) and social-content keys.

Then **present the file in chat** per the standing preview rule, so he can act on it immediately.

### Register nothing until real files exist

On a blocked run: no pipeline record, no `usedFor` entry, no `{brand}-social-content` pair, and **delete the empty `outputs/` folder** so a later run's rotation logic doesn't mistake it for a shipped package. This is not a special case, it follows the existing File Linking rule ("Do NOT create entries without valid file"). Ridwan confirmed 2026-09-04 he does not want a placeholder record showing in `content_pipeline.html`.

On unattended scheduled runs this is the whole expected behaviour: bank the prompt pack, register nothing, say plainly in the summary that nothing shipped. Do not improvise a substitute renderer and do not let PIL draw ad copy — the 2026-07-17 rejected run is exactly what that produces.

### Ingesting the images when Ridwan sends them back

He runs the pack manually and returns the exports (chat attachment, or dropped into the project folder). At that point the run resumes from where it stopped, using the pending file as its brief:

1. **Save the images to the real output folder** under the exact filenames the pack specified (`ad-1-problem-solution.png` etc.). Attachments arrive in `uploads/` — copy them across, don't leave the deliverable pointing at an upload path.
2. **Look at every image before accepting it.** Same bar as a generated run: headline spelled correctly, reads as an ad and not a caption card, product renders sensibly. A manually-produced image is not exempt from review just because a human made it. If one is wrong, say so and hand back a revised prompt for that one image rather than shipping the set.
3. **Assemble the derived assets** — the 2x2 combined showcase, and the size-check for X with a compressed `-x` variant if the combo clears ~4MB.
4. **Build `index.html`** with the standard pipeline export button and the constants from the pack.
5. **Register everything the blocked run deliberately skipped:** the pipeline record at status `Created` (never `Published`), the `usedFor` entry on the target, and the `{brand}-social-content.json`/`.md` pair.
6. **Present the finished `index.html`** in chat, then delete the pending file — it has served its purpose and a stale one will confuse a future run.

Note in the pipeline record's notes, and in the social-content file, that the images were produced manually via ChatGPT rather than through the `gpt-image` API. Not a quality caveat, just provenance worth keeping straight.

---

## 🖼️ CAROUSEL COVERS, EVIDENCE SLIDES, PRODUCT PHOTOS & ABOVE-THE-FOLD — MANDATORY (added 2026-09-01, Ridwan's standing instructions, project-wide)

Four related standing rules from a single 2026-09-01 review round, all now enforced project-wide (not just for the TAPro Cards run that surfaced them). This section overrides anything narrower or older in `koolestpro-content-engine`'s own SKILL.md or in `.ai-workflow/project-constitution.md` where they conflict — Cowork cannot edit those files' underlying source in this session (read-only caches; Settings → Capabilities is where Ridwan would edit the skill source itself if he wants it fixed there too), so this CLAUDE.md section is the enforced spec until then.

### 1. Every carousel cover must be a strong visual, not text-only

Ridwan's words: "On the carousel, we need to have a very good cover image so that it engages people and entices them to slide to see it. The best way we can do it is by using visual elements, not just text." This applies to every carousel this project generates — Tips (already had a Visual Variety System as of 2026-07-29, now sharpened) and CRO Fix (previously had no visual-cover requirement at all — its 6-slide carousel format was pure text/CSS, see #2 below).

A cover slide must carry a real visual element sized to dominate the frame, not a headline with a small decorative icon in the corner. Weight the choice toward whichever option is most visually arresting at a glance — a bold stat treatment, a striking icon composition, a real screenshot or product photo that reads as evidence — over a technically-compliant but flat option. Verify this by looking at the actual exported cover PNG, not the markup.

### 2. CRO Fix carousels must include the before/after and annotated-changes graphics as real slides

Ridwan's words: "Within those carousels, I need to have a spot for the before/after visual evidence and annotated changes so that people can see what was done, not just some generic story that does not have context."

CRO Fix's Section 1 carousel (the 6-7 slide narrative deck inside `{slug}_content.html`, separate from the standalone `#ba-graphic`/`#anno-graphic` sections 2-3) must now dedicate at least one slide to a real crop/embed of the before/after graphic and at least one slide to a real crop/embed of the annotated-changes graphic — not just narrative text describing "here's what changed" with no visual proof alongside it. Practically: base64-embed a resized/cropped version of the same PNG already built for `#ba-graphic`/`#anno-graphic` into a dedicated carousel slide `<div>`, following this project's existing html2canvas-safe base64-image conventions (never a relative path, never a live `<svg>` for anything curved). The standalone `#ba-graphic`/`#anno-graphic` sections stay as they are for LinkedIn/Instagram single-image posts — this is additive, not a replacement.

### 3. Product photos: background-removed cutouts over raw studio photos, never cropped

Ridwan's words, citing the TAPro G-Series Onyx photo directly: "Whenever I try to put a real photo on the page of the site, try your best where necessary to remove the background image... If we can remove the background from the image and use the NFC the way it is, and find a way to make it contrast with the background, I think we are going to create something very premium."

Building on the existing rule to always prefer a business's real product photo over a fabricated placeholder (see "Always update skills" / the per-run product-image check): when a real product photo has a plain studio/white background, prefer removing that background and compositing the cutout against a background that contrasts with it (the rebuild's own dark theme, a subtle gradient, etc.) over embedding the raw studio photo as-is. This reads as more premium and lets the product sit as a real object in the design rather than a pasted screenshot. Never let the container crop cut off part of the product — check the actual rendered crop (not just the source image) before finalizing, per the existing crop-check rule.

### 4. Build above the fold — no dead space at the bottom

Ridwan's words: "always try to build everything above the fold and do not leave space like we did. There is some space below the 90-day guarantee, so if we shift the CTA and the 90-day guarantee below a little bit, we will have more room to showcase that product's image."

If a rebuild's last visible element (a CTA, a guarantee line, a footer note) sits with meaningful empty space beneath it before the phone frame's bottom edge, that's wrong — either shift the lower elements down slightly and use the reclaimed vertical room to enlarge whatever needs it most (usually the product image, per #3 above), or tighten spacing so the layout genuinely fills the frame. Check this on the rendered screenshot/export, not the CSS alone — a `min-height` on the outer phone container can hide dead space that isn't obvious from reading the markup.

---

## 🖼️🏷️📐 IMAGE INTEGRITY, PAGE-TYPE LABELING, FULL-SPACE CAROUSELS & CONTEXTUAL VISUALS (added 2026-09-07, Ridwan's standing instruction, project-wide)

Found live on the Caraway Fry Pan PDP CRO Fix run. Ridwan's exact feedback: "the image seems to break everything, not same image, looks way bigger than the initial image, also I need to always know why type of page we are working on, always put it in the caption of the before after and the annotated image and the carousel, also we need to always have the contents on a carousel take the full space, the little titles (myth, reality, etc) are not always visible on the social platfors after it get's posted, make changes, update all affected skills and schedule tasks, for the empty spaces, we should find a way to use icons or 3d imagery but make sure to use consistent visual elements that gives the right contexts, not generic or templated visuals."

Four standing rules, all enforced from this run forward, for every CRO Fix, Static Ad, Template Showcase, Tips carousel, or any other stream that composites a real screenshot into a fixed-aspect container or ships a multi-slide carousel:

### 1. Image aspect-ratio integrity — never let a mismatched container crop/zoom a real photo

Root cause on Caraway: `.heroWrap img { object-fit:cover }` inside a `flex:1` container whose real rendered aspect ratio (~390x440, ~0.89:1) was nowhere close to the source photo's aspect (~1100x950, ~1.16:1). Cover forced a hard crop to fill the mismatched box, which read as "not the same image" and "way bigger" — a real bug, not a design choice.

**The rule:** before shipping any container that composites a real photo via CSS `object-fit`, compare the container's actual rendered aspect ratio (measure it, don't guess from the markup) against the source image's real aspect ratio. If they're not close:
- Prefer `object-fit:contain` on a background that reads as a deliberate plinth (the existing dark-surface/contrasting-background rule already in this file works well here — the letterboxing becomes premium framing, not empty space), OR
- Resize the container to genuinely match the image's aspect ratio, if the layout allows it.

Never ship `object-fit:cover` on a container whose aspect ratio you haven't actually checked against the source image. This applies everywhere a real screenshot or product photo gets composited into a fixed box: rebuild HTML, before/after graphics, annotated graphics, and any carousel slide that embeds one of those. Verify on the actual rendered screenshot/export, not the CSS alone — this is the same "verify by exporting" discipline already standing elsewhere in this file, extended to cropping specifically.

### 2. Every CRO Fix graphic and caption must state the page type, visibly

Ridwan: "I need to always know why type of page we are working on, always put it in the caption of the before after and the annotated image and the carousel."

**The rule, for every CRO Fix run:**
- The `#ba-graphic` and `#anno-graphic` PNGs must carry a visible page-type badge (e.g. "PRODUCT PAGE (PDP)", "HOMEPAGE", "LANDING PAGE (LP)", "COLLECTION PAGE") near the headline — an actual rendered element in the graphic, not a code comment or internal note. Use whatever the real audited page type is; never default to PDP if the page audited was something else.
- Every carousel slide that carries an eyebrow tag (cover, evidence slides) gets a second eyebrow badge stating the page type, alongside the existing "CRO FIX · {BRAND}" / "EVIDENCE" tags.
- Every caption — LinkedIn, Instagram, X/Twitter angles, X thread, and the matching `{brand}-social-content.json`/`.md` entries — states the page type explicitly, ideally in the opening line (e.g. "Product Page (PDP) audit: {Brand}'s {product}...").
- This is not CRO-Fix-specific in spirit — any stream that audits or showcases a specific page type (Static Ad, Template Showcase, `koolestpro-client-audit`) should state what kind of page is on screen wherever it names the audit, for the same reason: the viewer should never have to guess.

### 3. Carousel slides must use the full frame — redundant, large labeling over small reliant tags

Ridwan: "we need to always have the contents on a carousel take the full space, the little titles (myth, reality, etc) are not always visible on the social platforms after it gets posted."

This generalizes and sharpens the existing "no dead space" rule (see TYPE SCALE — HARD FLOOR above) with a specific failure mode: a small 9-12px uppercase eyebrow tag (e.g. "Myth" / "Reality" / "The Pattern") is exactly the kind of element that platform compression, cropping, or a fast scroll can make effectively invisible — so the concept it's carrying must never depend on that tag alone to land.

**The rule, for every carousel slide (Tips and CRO Fix both):**
- Any slide whose whole point is a state/label (Myth, Reality, The Pattern, Before, After, and similar) must bake that label into something large and hard to miss — a bold pill badge at 20px+ with the label text itself, not just a tiny uppercase tag — in addition to (not instead of) the existing small eyebrow convention. Redundancy is the point: if the small tag gets lost, the large one still carries the concept.
- No slide may end with a large empty/plain-background band below its content. If a slide's copy naturally stops partway down the frame, give the remaining space a real "so what" element — a callout band, a contextual icon + one-line takeaway, a mini-diagram — never just dead background. This applies with equal force to any slide that embeds a full-bleed image (before/after, annotated-changes evidence slides): if the embedding container is meant to fill remaining vertical space, verify on the actual export that it does, not just that the CSS says `flex:1` — a `flex:1` declared outside an actual flex-column ancestor does nothing, and this exact bug shipped once already (see the Caraway build log).
- Check every slide's page-counter/handle overlay for legibility against whatever is actually behind it at that position — a light image background under a low-opacity white counter chip is a real bug (found and fixed on Caraway), not a hypothetical. Give counter/handle overlays a semi-opaque backdrop chip so they read correctly regardless of the underlying slide content, rather than assuming a dark background will always be there.

### 4. Empty carousel space gets contextual icons/imagery, never generic or templated visuals

Ridwan: "for the empty spaces, we should find a way to use icons or 3d imagery but make sure to use consistent visual elements that gives the right contexts, not generic or templated visuals."

**The rule:** when a slide needs a supporting visual to fill space or reinforce its point (see rule 3 above), the visual must be specific to that slide's actual finding — never a generic decorative shape or a stock icon chosen for looking nice. Concretely, on the Caraway build: a star icon for the reviews/trust myth, a price-tag icon for the price-placement fix, a numbered-list icon for the repeatable pattern — each one drawn from Iconify's public API (`https://api.iconify.design/{prefix}/{icon}.svg?color=%23HEX`, no key needed, same source already approved for Tips carousels in the Visual Anchor & Variety System) and inlined as real SVG markup, at both a large low-opacity background-watermark size and a small colored badge size for the same icon, so the treatment reads as one deliberate visual language per slide rather than a decoration bolted on. Never reach for a generic "idea bulb" or "arrow up" icon that could apply to any post — pick the icon (or, where genuinely warranted, a 3D-style render) that names the specific thing that slide is about. This is the same "no generic/templated visuals" discipline the Visual Anchor & Variety System already applies to Tips covers, extended to every slide's supporting visual, in every stream.

### Reference implementation

`.ai-workflow/build_caraway_rebuild.py`, `.ai-workflow/build_caraway_graphics.py`, and `.ai-workflow/build_caraway_content.py` (all corrected 2026-09-07) show all four rules applied to a real run — the `object-fit:contain` fix, the `draw_page_type_badge()` helper in the graphics script, the full-frame flex-column slide restructure with large Myth/Reality/Pattern badges and Iconify-sourced contextual icons, and the CTA slide's real Cloudinary avatar (see the next section below for why an empty avatar placeholder is its own separate hard rule). Use these as the pattern for any future correction of this shape, in any stream.

---

## 🏷️ REAL BRAND ASSETS ONLY — NEVER RECREATE A LOGO (added 2026-09-04, Ridwan's standing instruction, hard rule, project-wide)

Ridwan's words: "Instead of trying to copy their branding, why not just take the original [asset] from their site and use it? ... A logo from a business should be taken directly the way it was. There is no need to try to recreate it every time we did not get the logo of the site correct, and that is going to spoil our justification for a CRO fix. This is a hard rule: we must use their original logo and also any assets that have to do with their branding. They should be used the way they are."

**This corrects standing practice, not just adds to it.** Earlier CRO Fix and Static Ad builds routinely recreated a target brand's logo from scratch as CSS/text (e.g. a wordmark spelled out in a styled `<div>`, or a circle with initials) instead of pulling the real file. A hand-recreated logo can drift from the real one in font, spacing, color, or icon shape — and any visible mismatch undermines the whole CRO Fix pitch, since the point is "here is your real page, improved," not "here is a lookalike of your page." This applies retroactively to how future builds are made — it does not require going back and fixing already-shipped, already-posted work (see the TAPro Cards run: that post is already live and is not being redone; this rule is about every run from here forward).

**The rule, concretely, for every rebuild of a real business (CRO Fix, Static Ad, `koolestpro-client-audit` deliverables, or any other stream that rebuilds a real brand's page):**

1. **Logo: always the business's real logo file, embedded exactly as it is.** Locate it on their live site (usually the header `<img>` — check `srcset`/`src` on the header logo element, not just favicon or schema.org `logo` JSON-LD, since those can point to a lower-res or differently-cropped variant) and download it directly. Never redraw it as text, CSS shapes, or an approximate SVG recreation, even if the real file is awkward to work with (wrong aspect ratio, needs a transparent background swap, etc.) — solve that with image processing on the real file (crop, resize, background-removal per the product-photo rule below), never by rebuilding it from scratch.

   **This includes text-based/wordmark logos, not just icon-style ones (added 2026-09-04, Ridwan's clarification).** A lot of business logos are just their name set in a distinctive custom typeface — that typeface IS the brand identity, and it is essentially never one of the handful of fonts available on the web (Google Fonts, system fonts, this project's own Syne/DM Mono). Retyping "TAPro" or "HALOS" in whatever font happens to be loaded on the page and calling that the logo is exactly the kind of recreation this rule bans — it will look close enough to seem intentional but wrong enough to be a tell, which is worse than an icon mismatch because text is what people read first. **Treat every logo as an image asset regardless of whether it's icon-based or text-based** — download the real logo file (PNG/SVG) and embed it as a real `<img>`, never as live HTML/CSS text trying to approximate the brand's typeface.
2. **Any other brand asset (icon set, badge, seal, wordmark, trust-badge graphic) — same rule.** If it's part of how the business presents itself, pull the real file rather than approximating it.
3. **Product photos: prioritize the real photo from their site, per the existing rule above** — this section doesn't change that, it extends the same logic to logos and other brand marks. An "optimized version" of their real image (resized, background-removed, compressed) is fine and often necessary; a recreated-from-scratch version is not.
4. **If the real asset genuinely can't be retrieved** (broken link, blocked by anti-scraping, no logo file exists and the header is text-only): say so plainly in the run's summary rather than silently substituting a recreation. A text-only header on the real site is itself a fact worth carrying into the rebuild as-is, not a gap to paper over with an invented logo.

**Why this matters more than it might seem:** the entire CRO Fix / Static Ad pitch rests on "this is genuinely your page, just fixed" — a viewer (especially the business owner themselves, if this ever reaches them) checking the rebuild against the real site and spotting a logo that's subtly wrong is exactly the kind of credibility gap that undermines the whole audit, worse than almost any other visual inaccuracy.

---

## 📅 LINKEDIN — MAX 1 POST/DAY, HARD CAP (added 2026-09-04, Ridwan's standing instruction)

Ridwan's words: "We want to make sure we do nothing more than one post a day [on LinkedIn]. We are free to do multiple posts per day on Twitter, but not on LinkedIn."

**This is a separate, stricter rule than the no-simultaneous-slot rule below — it applies to LinkedIn only.** Twitter has no daily cap (see the rule below for Twitter's actual constraint, which is just "no two Twitter posts at the exact same time"). LinkedIn may never have more than one row scheduled on the same `scheduled_date`, even at different times of day.

**Found live on 2026-09-04, same session as the no-simultaneous-slot fix:** the sheet had 4 LinkedIn rows on `2026-09-04` (at four different times, which had already satisfied the no-collision rule but not this one), 2 on `2026-09-08`, and 2 more on `2026-09-12` (which also happened to share the exact same time, `14:00` — a second real collision the original 2026-09-04 sweep had missed because that sweep only checked the next 7 days; this one was 8 days out). All 5 overflow rows were moved to open LinkedIn days (`2026-09-10`, `2026-09-13`, `2026-09-16`, `2026-09-17`, `2026-09-19`) via the reschedule webhook.

**The rule, enforced everywhere a LinkedIn row's `scheduled_date` gets set or changed:**

* Before scheduling or rescheduling any LinkedIn row, check the live sheet for **every other LinkedIn row already on that date**, not just at that exact time. If the date already has one, pick a different date — a different time on the same day does not satisfy this rule.
* When multiple LinkedIn rows need to move off an over-scheduled day, keep whichever one is already QA-clean (or, if all are blocked, keep any one) and move the rest forward to the nearest genuinely open LinkedIn day.
* This check must run further out than just the next 7 days — the 2026-09-12 collision above was missed on the first pass specifically because it was 8 days out. Any full audit or the recurring health-check task should scan the entire unposted LinkedIn backlog, not just a 7-day window, when checking for this specific rule.
* Twitter is explicitly exempt from a daily cap — multiple Twitter posts on the same day are fine and expected. Twitter's only constraint is the no-simultaneous-slot rule immediately below (no two Twitter rows at the exact same `(date, time)`).

---

## ⏱️ DISTRIBUTION QUEUE — NO SIMULTANEOUS-SLOT RULE (added 2026-09-04, Ridwan's standing instruction)

Ridwan flagged that when a post gets moved from the past into the future, it sometimes lands at the exact same time as another queued post, and both fire together. Root cause, confirmed by reading the live Make.com blueprint for scenario 6565331 ("Koolestpro Social Distribution"): the scenario's `google-sheets:filterRows` step matches every row where `scheduled_date == today AND scheduled_time_local <= now` — a "due or overdue" filter, not an exact-slot match. This is intentional (it's the catch-up safety net that stops a missed run from permanently skipping a post), but it means that if two rows for the **same platform** share the same `(scheduled_date, scheduled_time_local)`, both match in the same 15-minute execution and post back to back in the same run — which is exactly what Ridwan is seeing. This was confirmed live on 2026-09-04: the sheet had 4 LinkedIn rows all at `2026-09-04 09:00`, 2 more LinkedIn rows both at `2026-09-08 09:00`, and 2 separate Twitter collisions on `2026-09-10` (3 rows at `09:00`, 2 rows at `13:00`) — all fixed via the reschedule webhook that day.

**The rule, enforced everywhere a row's `scheduled_date`/`scheduled_time_local` gets set or changed — fresh population, harvest, manual edit, or reschedule:**

* No two rows for the **same platform** may ever share the exact same `(scheduled_date, scheduled_time_local)`. This is a same-platform rule, not a same-slot-across-platforms rule — a LinkedIn post and a Twitter post both at `09:00` on the same day are fine, since they post to different networks in different branches.
* Ridwan is explicitly fine with more than 4 posts/day on a single platform (the 4 standard slots — `09:00`/`13:00`/`18:00`/`23:00` — are a convention, not a hard cap). What he wants is real separation between posts, not a specific daily count. When a day already has all 4 standard slots filled for a platform, use additional times spaced at least ~60-90 minutes apart from every other slot that platform already has that day (e.g. `11:00`, `15:00`, `21:00`) rather than reusing any existing time.
* Before calling the reschedule webhook (`https://hook.eu1.make.com/ocwhcp96a5up7i8hjqxuqrkw7m3a59rm`) for any row, pull the **live** sheet's rows for that platform on the target date and confirm the target time isn't already taken. The webhook itself does not check this — it blind-overwrites `scheduled_date`/`scheduled_time_local` for the given `post_id` — so the caller (any scheduled task or ad hoc session) is the only guard. This applies to every reschedule pass, not just the recurring health-check task.
* `.ai-workflow/tools/populate_sheet.py` already does this correctly for fresh batches — `find_open_week()` walks forward one week at a time per slot until it finds a `(platform, date, time)` key not already in `taken_keys`, and reserves the key immediately so two slots in the same batch can't collide with each other either. **Known caveat, not yet fixed:** `taken_keys` is seeded only from local `outputs/distribution-queue/queue.json`, not a live read of the Sheet — per `append_sheet_rows.py`'s own docstring, the Sheet is deliberately "the live, ahead-of-local source of truth" (Ridwan edits rows directly, Make writes `Posted`/`posted_at` back), so `queue.json` can legitimately drift behind it. In practice this means a fresh `populate_sheet.py` run could still pick a time that collides with a row that only exists live in the Sheet (e.g. one added via a manual edit or a different session's reschedule pass) and not in `queue.json`. Worth closing by having `populate_sheet.py` pull live Sheet occupancy into `taken_keys` too — not done yet, flagged here rather than guessed at silently.
* A Make-side belt-and-suspenders fix (a stagger delay inserted right after credential load and before the platform router, so even a same-slot collision that slips through can't post within the same second) was investigated on 2026-09-04 but **not applied** — the live blueprint is a large multi-branch scenario (44+ modules) that this session's tools can only read in small fragments (any tool call returning the full blueprint gets saved to a file too large to safely reconstruct byte-for-byte), and `scenarios_update` wholesale-replaces the entire blueprint with no partial-patch option. Hand-editing a production posting scenario from a lossy fragment-by-fragment reconstruction was judged too risky to attempt blind. The sheet-side rule above is the actual enforced guarantee; revisit the Make-side stagger only with a tool that can pull the full blueprint faithfully (e.g. Ridwan exporting it from the Make UI directly), or with Ridwan present to review the diff in the Make UI before saving.

---

## 🔗 PIPELINE EXPORT BUTTON (MANDATORY IN ALL OUTPUT SKILLS)

Every HTML file produced by any output skill MUST include a **"Send to Content Pipeline"** button.

### What it does

1. Builds a JSON object matching the [JSON Standard](#json-standard-mandatory)
2. Downloads it as `{slug}_pipeline.json`
3. Logs `console.log("EXPORT_POST_JSON", JSON.stringify(data))` for Cowork detection
4. Shows a confirmation message in the UI

### Where it lives

- **Skill E (CRO Content):** Inside the Section 04 Export panel, above the carousel download buttons
- **Content Engine:** Below the Post Copy Tabs section, as its own panel
- **Any future output skill:** As the last panel before the page ends

### Button HTML pattern

```html
<!-- ══ PIPELINE EXPORT ══ -->
<div style="max-width:600px;margin:0 auto;padding:0 20px 60px;">
<div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px;margin-bottom:16px;">
  <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px;">Content Pipeline</div>
  <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px;">Export this post to the content system. Downloads a <code>.json</code> file — open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
  <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px;">Send to Content Pipeline →</button>
  <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px;"></div>
</div>
</div>
```

### JS function (add to script block)

```javascript
// ── PIPELINE EXPORT ──
// POST_BRAND, POST_SLUG, POST_TYPE, POST_FOLDER must be defined as consts at top of script
function sendToPipeline() {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const data = {
    id:        POST_TYPE.toLowerCase() + '-' + POST_SLUG + '-' + dateStr,
    type:      POST_TYPE,
    title:     'ACTUAL POST TITLE HERE',  // ← always the real post title, never 'Brand — Type'
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

### Constants to define per skill (top of script block)

```javascript
// Skill E (CRO Fix) — set these from the audit brand/slug
const POST_BRAND  = 'Brand Name';                                 // e.g. 'Eco Bio Boutique'
const POST_SLUG   = 'brandslug_product-name';                     // e.g. 'ecobioboutique_cellulite-remover'
const POST_TYPE   = 'CRO Fix';                                    // always 'CRO Fix' for Skill E
const POST_FOLDER = 'outputs/cro-fixes/' + POST_SLUG + '_content.html';

// Content Engine (Tip) — set these from the post topic
const POST_BRAND  = 'Koolestpro';
const POST_SLUG   = 'slug-from-topic';                            // e.g. 'shopify-pdp-trust-signals'
const POST_TYPE   = 'Tip';                                        // 'Tip' | 'Personal' | 'Case Study'
const POST_FOLDER = 'outputs/tips/' + POST_SLUG + '.html';

// Static Ad Image skill — set these from the product/brand being shown
const POST_BRAND  = 'Brand or Product Name';                      // e.g. 'Koolestpro sample' or a real client brand
const POST_SLUG   = 'brandslug_product-name';                     // e.g. 'alchemind_mushroom-blend'
const POST_TYPE   = 'Static Ad';                                  // always 'Static Ad' for this skill
const POST_FOLDER = 'outputs/static-ads/' + POST_SLUG + '_' + dateStr + '/index.html';
```

### Rules

* Button is NEVER optional — every output skill includes it
* `POST_BRAND`, `POST_SLUG`, `POST_TYPE`, `POST_FOLDER` are ALWAYS defined before the function
* Download filename is always `{POST_SLUG}_pipeline.json`
* Status is always `"Created"` — never auto-set `"Published"`
* `day` field is always `""` — user sets scheduling in the content system



## Cowork Responsibilities

### 1. JSON Ingestion

Cowork must:

1. Detect new JSON exports from content tools
2. Validate structure
3. Merge into `SYNC_DATA.items`

Rules:

* Do NOT overwrite existing items
* Use `id` to prevent duplicates
* If duplicate → skip

---

### 2. Update Central System

Cowork must:

1. Open `ridwan_content_system_updated.html`
2. Locate:

```html
<script id="cowork-sync-data">
```

3. Replace ONLY the JSON inside
4. Preserve all UI code

---

### 3. Month Management

If a new `monthSlug` does not exist:

Add to:

```json
SYNC_DATA.months
```

Format:

```json
"2026-05": {
  "label": "May 2026",
  "htmlPath": "outputs/ideas/ideas_2026-05.html",
  "jsonPath": "outputs/ideas/ideas_2026-05.json",
  "totalIdeas": 0
}
```

---

### 4. File Linking (CRITICAL)

Every post MUST link to its HTML file.

Cowork must:

* Verify `folder` path exists
* If missing → flag error
* Do NOT create entries without valid file

---

### 5. Status Handling

Allowed statuses:

* Idea
* Created
* Ready
* Published

Cowork can:

* Set to "Created" after generation
* NEVER auto-set "Published"

---

### 6. Remove Notion Dependencies

Cowork must:

* Remove all "Send to Notion" logic from HTML files
* Replace with:

  * JSON export function
  * Local save trigger

---

## HTML Generator Update Rules

All generator HTML files must be updated to:

### Replace:

```
Send to Notion
```

### With:

```
Export JSON → Cowork ingestion
```

---

### Required Function (example)

```js
function exportPostData() {
  const data = { ...structured JSON... };

  // Save locally OR send to Cowork pipeline
  console.log("EXPORT_POST_JSON", data);
}
```
---

## 🎨 GRADIENT SYSTEM — CONFIRMED RULES

---

## ✅ CSS GRADIENTS — ALLOWED ON BACKGROUNDS ONLY

CSS `linear-gradient` and `radial-gradient` work correctly in html2canvas when applied to:

* `background:` on `div`, `span`, `button`, `border` elements
* Glow blobs (`filter:blur()` + `radial-gradient`)
* Decorative bars, rule lines, CTA button backgrounds
* `background-image` on any non-text element

```css
/* ✅ These all work fine */
background: linear-gradient(90deg,#FF9500,#7B2FBE);
background: radial-gradient(circle,rgba(255,149,0,0.15),transparent 70%);
filter: blur(60px);
```

---

## ❌ GRADIENT TEXT — CSS OR SVG: BOTH FORBIDDEN

**CSS gradient text** — breaks html2canvas, text goes transparent:
```css
/* ❌ FORBIDDEN */
background: linear-gradient(...);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

**SVG gradient text** — banned. Too complex, inconsistent across files:
```html
<!-- ❌ FORBIDDEN -->
<text fill="url(#grad-...)">...</text>
```

**Text color rule: SOLID COLORS ONLY**

Use `color:#FF9500`, `color:#fff`, or slide-themed accent colors directly on all text.
```css
/* ✅ Correct */
color: #FF9500;        /* brand orange for highlights */
color: #3b82f6;        /* blue for cold/unaware themed slides */
color: #22c55e;        /* green for warm themed slides */
```

---

## ⚙️ EXPORT COMPATIBILITY RULE

html2canvas must render correctly with:
```js
html2canvas({ scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#080808', logging: false })
```

Hide elements during export using `visibility:'hidden'` (NOT `display:'none'`).
Always hide: `[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap`


---

## Error Handling

Cowork must reject:

* Missing `id`
* Missing `folder`
* Invalid JSON
* Duplicate IDs

---

## Constraints

* Do NOT modify UI structure of content system
* Do NOT remove existing data
* Do NOT generate fake metrics or values
* Always preserve brand system

---

## Goal

Cowork acts as:

> Local content pipeline manager

It:

* Collects outputs
* Updates central system
* Maintains structure
* Ensures data integrity

No external tools. No Notion.

Only:
→ HTML
→ JSON
→ Local files

---

## End State

A fully autonomous system where:

* Content tools generate posts
* Cowork syncs them
* Content system displays them
* Every post links to its source file

---

## 🐛 CONFIRMED EXPORT BUGS — FIXED (Do Not Re-introduce)

### Bug 1 — Swipe Arrow / Chrome Elements Bleed Into Download
Hide with `visibility:'hidden'` (not `display:'none'`) to prevent layout shift.
Always include all chrome selectors:
```javascript
const toHide = document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
toHide.forEach(el => el.style.visibility = 'hidden');
// ... in finally block:
toHide.forEach(el => el.style.visibility = '');
```

### Bug 2 — Slide position lost after capture
Always save/restore `track.style.transform` and `track.style.transition` in `captureSlide()` using try/finally. See project-constitution.md for the canonical pattern.

### Bug 3 — Fonts/images not ready at capture time
Always use `waitForSlideAssets(slide)` + double `requestAnimationFrame` before calling `html2canvas`. See project-constitution.md for the canonical function.

---

## Static Ad Image — Export Routing

This project uses the portable `static-ad-image` skill (built 2026-07-10, retrofitted 2026-07-11 to be project-agnostic like `page-presentation-kit` — installed globally, not specific to this project) to generate 4-angle static ad showcases. This section tells that skill where things belong and how to register output in *this* project specifically; the skill itself carries no opinion about file locations or pipeline schemas.

**Output location:** `outputs/static-ads/{slug}_{date}/index.html` — a companion review page (not an html2canvas capture target) holding the 4 ad PNGs, the combined LinkedIn showcase, X assets, and captions, plus the standard Pipeline Export Button (pattern above) with these constants:

```javascript
const POST_BRAND  = '<brand or product name>';
const POST_SLUG   = '<brandslug_product-name>';
const POST_TYPE   = 'Static Ad';
const POST_FOLDER = 'outputs/static-ads/' + POST_SLUG + '_' + dateStr + '/index.html';
```

**Registration:** export a pipeline JSON matching this project's [JSON Standard](#json-standard-mandatory) — type `"Static Ad"` (added 2026-07-10 specifically for this skill's output), status always `"Created"`, never `"Published"`. Open `ridwan_content_system_updated.html` and sync to register it, same as every other output type.

**Reference library:** this skill currently uses a fixed, baked-in style-pattern reference (`references/ad-style-patterns.md`, shipped inside the skill itself) rather than a growing external library like `page-presentation-kit`'s. If that changes later, it should follow the same `replo-rebuilds/*-references/` convention rather than inventing a third pattern.

### ⚠️⚠️ GENERATION METHOD — HARD RULES (2026-07-18, after the Bebemoss run shipped unusable output)

The 2026-07-17 Bebemoss run produced four ads that read as caption cards, not ads: a cream text panel stacked above a photo, with the headline set in Liberation Sans by PIL. Ridwan rejected them. Root cause: the run tried `--quality medium` gpt-image calls, hit the sandbox's hard ~45s per-command ceiling, concluded gpt-image could not render ad text at all, and silently fell back to compositing the text itself with PIL. The fallback rested on an assumption ("low-quality gpt-image misspells headlines") that was never tested and is **false**.

Measured 2026-07-18, `generate.py`, 1024×1536 portrait, warm uv cache:

| `--quality` | Wall time | Result |
|---|---|---|
| `medium` | **>44s** | killed by the ceiling, no file — reproducible, not a fluke |
| `low` | **21–30s** | photoreal, headline spelled correctly every time across 4/4 ads |

Also confirmed by test: **detached/background processes do NOT survive between bash calls** (`setsid nohup` + `disown` was verified dead 25s later). There is no fire-and-poll escape hatch. Every image must finish inside one command.

Therefore, for every static ad:

1. **One gpt-image call per bash command.** Four ads = four separate commands. A timeout then costs one ad, not the batch.
2. **Always `--quality low`, always `--size 1024x1536`.** Not a compromise — it is the setting that matches the Obvi gold-standard output and fits the ceiling.
3. **The headline, subline, badge, and any button text go IN THE PROMPT**, quoted with "reading exactly:", so gpt-image renders them into the photograph. Full-bleed image, text sitting on the photo.
4. **PIL/Pillow must NEVER draw ad copy.** Its only permitted use in this stream is assembling the 2×2 `combined-showcase.png` grid from the four finished ads.
5. **If a generation times out, re-run that one command.** Do not fall back to compositing, and do not silently downgrade the deliverable — if something genuinely cannot be produced, say so plainly in the run summary instead of shipping a lesser artifact that looks finished.
6. **Look at every generated ad before calling the run done.** Read each PNG back and confirm the headline is spelled correctly and the layout reads as an ad.

**Reference for what "right" looks like:** `outputs/static-ads/obvi_super-collagen-protein_20260711/` and the regenerated `outputs/static-ads/bebemoss_ginger-sleepy-bunny_20260717/`.

### ⚠️⚠️ CONFIRMED BUG — combo image for X must be size-checked, not banned (2026-08-01, corrected same day after an overcorrection)

Found via a live Make.com failure: the Bebemoss X post scheduled for 2026-08-01 had its asset_paths/asset_urls pointed at `combined-showcase.png` (the LinkedIn 2x2 grid — 2132x3156, 8.33MB in this instance, and drifted well past the skill's own `1024x1024` spec) instead of a properly-sized image. Make's HTTP "Get a file" module rejected it with `MaxFileSizeExceededError`, which blocked that day's X post. Obvi's equivalent "X1" entry pointed at the same-named file but never hit this error, because Obvi's combo happened to still be at a safe size (3.47MB).

**First fix attempt (same day) overcorrected and was wrong.** It concluded X should never use `combined-showcase.png` at all and banned it outright, both in the skill and in this file. Ridwan corrected that directly: "I did not know when I said no combo for x posts, but I want the combo, it looks great in x." The combo image was never the problem — file size was. That first-pass fix has been reverted.

**Actual fix, now live in the skill (global, portable — installed once, used across projects):** `combined-showcase.png` stays the default/preferred image for the X "summary of all 4 angles" post. Before it's ever assigned to an X entry, its file size gets checked against a ~4MB ceiling (comfortable margin under X's own 5MB image cap, and under whatever pushed Make's fetch limit past 3.47MB but under 8.33MB). If it's over the ceiling, generate a compressed `combined-showcase-x.png` variant (resize + PNG optimize — a 40-60% linear resize is typically enough, no visible quality loss at feed resolution) and point the X entry at that instead of the full-resolution original. Angle-specific X posts still use their own individual `ad-N-*.png` image, unchanged. See the skill's own "Confirmed bug" section for the full writeup.

**What was corrected on the data side (2026-08-01):** for Bebemoss, a compressed `combined-showcase-x.png` (1279x1893, ~3.04MB) was generated and uploaded to Cloudinary as a new asset (`koolestpro/bebemoss/bebemoss-combined-showcase-x`) rather than overwriting the original. `bebemoss-social-content.json`'s `SA-BEBEMOSS-X1.assetPath` now points at that compressed variant. `obvi-social-content.json`'s `SA-OBVI-X1` was reverted back to the original `combined-showcase.png`, since its file was never oversized and never needed a workaround. The specific Bebemoss tweet that had already gone live at 2026-08-01 23:13 (using an individual image, from the first overcorrected fix) was left as-is rather than retroactively altered — it accurately reflects what was actually posted. Full incident narrative, in both rounds, is logged in `bebemoss-social-content.json`'s `exportLog`. Any *other* already-shipped brand's X1 entry that hasn't been reviewed could still carry an oversized combo — worth a quick size check across `*-social-content.json` files for `"assetPath".*combined-showcase` (not `assetPath` on X entries generally — combo-on-X is fine) if this comes up again.

---

## Page Presentation Kit — Export Routing

This project uses the portable `page-presentation-kit` skill (built 2026-07-11, installed globally — not specific to this project) for turning any built page into desktop/mobile mockups, a combined presentation graphic, and optional scroll-through video. This section tells that skill where things belong in *this* project specifically; the skill itself carries no opinion about file locations.

### ⚠️ V1 Full Asset Set — CORRECTED v2 (2026-07-12, first attempt reviewed and found wrong)

The first live run (`outputs/templates/v1ce_tap-review-card-pdp_2026-07-12/`) proved the v1 spec below wasn't tight enough — DeepSeek shipped a raw screenshot with a thin border pretending to be a phone frame, no laptop bezel at all, a flat grey/black background with no branding, and a "full page" shot that was actually just a partial mobile-viewport capture, not the whole desktop page. Ridwan reviewed it, said "not close to the target," and cut the image list down to exactly 3 designed images (not ~7) while providing his own real device-frame source files. This section replaces the original v1 spec — don't follow the old 10-asset table below this one if it's still present, this corrected version wins.

### ⚠️⚠️ CORRECTED v3 (2026-07-13, second real run reviewed — videos too fast, 2 of 3 unframed, mosaic had dead panels)

The second live run (`outputs/templates/kura_hp-01_2026-07-13/`) was much closer but still failed on execution, not concept: Ridwan flagged the videos as "too fast" (actual durations were 8s/19s/13.7s against a 25-30s target), only `cover.mp4` had a real device bezel and it was off-center with the phone clipped off-canvas, `laptop.mp4`/`mobile.mp4` shipped as bare unframed screen recordings, and `full-mosaic.png` had large blank navy tiles from a GSAP scroll-pinned section whose content only exists at a live scroll position (a static full-page screenshot can't capture it "revealed"). Root-caused by reading the actual scripts used (`scroll_video.py`'s `--duration` default is 6s and nothing in this spec pinned it to a target; the v2 spec only required bezel-compositing on `cover.mp4`, never said "all three"). Fixed by building two new reusable scripts — **use these, don't reinvent the compositing per run:**

- **`.ai-workflow/skills/page-presentation-kit/scripts/frame_video.py`** — composites a raw `scroll_video.py` capture into the real calibrated bezels (see Device Frames below) on the brand-gradient background, for all three video variants. `python3 frame_video.py laptop --video raw.mp4 --output "{slug} laptop.mp4"` / `mobile` (same flags) / `cover --video raw_laptop.mp4 --video2 raw_mobile.mp4 --output "{slug} cover.mp4"`. Reads `assets/frames/macbook-pro.png` / `macbook-pro-alt.png` — these are the SVGs pre-rendered to raster PNG with the screen region alpha-punched to true transparency (the raw SVG screen area renders as an opaque dark fill, not transparent, so it must be punched before use — see build log for the one-time render+punch recipe if these ever need regenerating). `iphone-frame.png` already has a genuine alpha cutout, no punching needed.
- ~~**`.ai-workflow/skills/page-presentation-kit/scripts/build_mosaic.py`** — replaces blind fixed-height slicing...~~ **RETIRED 2026-07-29 — see CORRECTED v4 below.** Ridwan does not want the grid-mosaic layout at all; `build_split_page.py` replaces it (same walk-then-excise capture logic, different — much simpler — two-column layout instead of a many-tile grid). Do not use `build_mosaic.py` for new work; it's left in the scripts folder only as history.

**Video duration is now a hard target, not a default:** raw `scroll_video.py` captures for both laptop and mobile must use `--duration 26` (no `--clean` flag — it adds ~5-10s of popup-dismissal overhead per label tried, and none of the pages built in this project have cookie/consent banners to dismiss anyway). This lands the final framed video at ~29-30s after `frame_video.py`'s overhead, inside the 25-30s target. Verify with `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 out.mp4` before treating a video as done — don't assume the duration flag alone guarantees the output, confirm it.

**Videos — all 3 must be bezel-composited (corrected 2026-07-13, was cover-only):**

| Asset | Dimensions | How it's built |
|---|---|---|
| `{slug} cover.mp4` | 960×720 (4:3), ~29-30s | Two raw `scroll_video.py` captures (laptop viewport + mobile viewport, both `--duration 26`, no `--clean`) composited together via `frame_video.py cover`, real bezels on both devices, brand-gradient dark background, both devices fully inside canvas bounds (not clipped). |
| `{slug} laptop.mp4` | 960×720 (4:3), ~29-30s | Raw `scroll_video.py` capture at desktop viewport (`--width 1600 --height 966 --duration 26`, matching the macbook screen rect's aspect ratio) framed via `frame_video.py laptop`. |
| `{slug} mobile.mp4` | 1080×1350 (4:5 portrait), ~29-30s | Raw `scroll_video.py` capture at real mobile viewport (`--width 390 --height 855 --duration 26`, matching the iPhone screen rect's aspect ratio) framed via `frame_video.py mobile`. |

**Images — reduced to exactly 3 designed deliverables (corrected 2026-07-12, was ~7):**

| # | Asset | Dimensions | What it actually is |
|---|---|---|---|
| 1 | `{slug} cover.png` | 1440×1080 (4:3) | Laptop + phone together, REAL device bezels (not a thin CSS border), on the brand gradient glow (default) or a plain color via `--bg-mode` (see CORRECTED v5 below) — not a flat grey or flat black, that's what made attempt #1 read as boring. **Build via `build_device_still.py cover` (see CORRECTED v4/v5 below)** — the canonical script as of 2026-07-29; the phone side must carry the notch-flanking mobile status bar, never a blank top. |
| 2 | `{slug}-preview.png` | 2880×1800 (8:5 landscape), or narrower for a 2-phone style | 2 or 3 phone frames, REAL bezels, arranged per one of the 8 named `STYLE_PRESETS` in `build_device_still.py` (see CORRECTED v5 below — these trace back to 16 reference arrangement styles Ridwan shared; never freehand a new layout), each phone showing a genuinely different scroll depth of the page (hero / mid-page / footer — attempt #1's 3 phones showed near-identical content, check the actual screenshots are from meaningfully different scroll positions before compositing). Brand gradient or plain color per `--bg-mode`. **Build via `build_device_still.py preview --style <name>`** — each phone gets its own auto-picked status bar (see CORRECTED v4/v5 below), never a blank top strip. |
| 3 | `{slug}-full-page.png` | desktop viewport width × however tall the 2-column split comes out | **RETIRED the grid mosaic (2026-07-29, Ridwan's call — see CORRECTED v4 below).** This is NOT a many-tile grid and NOT a single cropped screenshot — it's the ENTIRE page, captured at full scroll height at DESKTOP viewport width, split into exactly TWO tall columns placed side by side (both reading top-to-bottom, column 1 finishing where column 2 continues), matching Ridwan's reference. **Use `build_split_page.py`** (replaces `build_mosaic.py` — do not use the old grid-tiling script for new work). Still not a DeepSeek/HTML job — mechanical image processing, not a design decision. |
| 4 | `{slug}-mobile-strip.png` | mobile viewport width × N columns wide (6 columns ≈ 2340×1860) | **Added 2026-09-02, Ridwan's call — see CORRECTED v8 below.** The ENTIRE page captured at MOBILE width and laid out as 6 side-by-side columns, so every section of a responsive build reads at a glance in one frame. Distinct from #3: that one is desktop width in two columns on a neutral canvas; this one is mobile width, many columns, flush with no outer frame. **Build via `build_mobile_strip.py`.** This asset gets its own X post (X #5). |

The raw per-scroll-depth mobile screenshots (`mobile-1/2/3.png`) and the raw full-page capture still get taken as intermediate/working files feeding #2 and #3 above — they're not separate top-level deliverables anymore, don't list them in the companion review page as their own cards.

**Device Frames — use Ridwan's real source files, no AI generation needed (corrected 2026-07-12, replaces the old GPT-image-bezel plan):**

Ridwan provided his actual Figma-exported device mockup frames directly — saved to `assets/frames/` in this project:
- `assets/frames/macbook-pro.svg` — full laptop frame including base/hinge shadow. viewBox `0 0 2011 1171`. Screen region (the actual content area, inside the bezel): **x: 199–1812, y: 74–1048** (width 1613, height 974 — as fractions of the full canvas: x 9.9%–90.1%, y 6.3%–89.5%). Composite a screenshot into this exact rect.
- `assets/frames/macbook-pro-alt.svg` — same frame, screen-only (no base/hinge decoration), same screen-region coordinates. Use this variant when the base would get cropped out anyway or reads as visual clutter at smaller sizes.
- `assets/frames/iphone-frame.png` — **saved and calibrated 2026-07-12.** Ridwan dropped the real file (`Apple iPhone X Space Grey (1) copy.png`) directly into the project folder rather than the chat — that's the right move when a file's already on his machine, no need to re-upload through chat. Canvas is 450×974px, RGBA with true alpha transparency. Screen-cutout region found by scanning the alpha channel for the opaque-to-transparent boundary (not guessed): **x: 22–428, y: 59–949** (as fractions: x 4.9%–95.1%, y 6.1%–97.4%). Note the transparent region includes the notch cutout at the very top — the rectangular bounds above are the safe inner screen rect; content composited into this rect will sit correctly behind the notch.

Compositing approach: since these are precise vector/raster frames (not something needing AI generation), build a small reusable Python/PIL (for stills) or HTML/CSS+Playwright (if easier to lay out multiple frames together) template that places the real screenshot into the calibrated screen-region behind/under the frame image — same pattern DeepSeek should follow when asked to build the collage/cover compositing HTML, using these exact coordinates rather than guessing. For video, use `frame_video.py` (see CORRECTED v3 above), which wraps the same coordinates in an `ffmpeg overlay` pipeline for all three video variants, not just cover.

**Raster + alpha-punched frame PNGs (added 2026-07-13):** `assets/frames/macbook-pro.png` / `macbook-pro-alt.png` are the SVGs pre-rendered to PNG (via a headless Playwright page render, `omit_background=True`) with the screen-rect region then forced to alpha=0 in PIL — the raw SVGs actually paint a solid dark screen-fill in that area (not transparent as originally assumed), so a naive raster render alone isn't a usable cutout; the punch step is required. `iphone-frame.png` didn't need this — its screen region was already genuinely transparent. `frame_video.py` reads these PNGs directly; `composite_frame.py` (the older generic CSS-frame script) is unrelated and should not be used for calibrated real-bezel compositing, it only has generic non-calibrated frame styles.

**Both device frames are now calibrated and available (as of 2026-07-12) — no fallback needed for missing frames.** If a future run somehow can't read `assets/frames/`, ship the laptop-only parts that work and say plainly in the summary that the phone-bezel assets are blocked — do not fake a phone bezel with a thin CSS border again, that was exactly attempt #1's problem.

**⚠️⚠️ cover.mp4 device-overlap bug — FIXED 2026-07-21 (Ridwan flagged it live in `kura_hp-01 cover.mp4`):** `frame_video.py`'s `build_cover()` used to deliberately position the phone at `laptop_right_edge - phone_w*0.62`, i.e. overlapping the laptop's lower-right corner on purpose, to avoid the phone bleeding off-canvas (the original problem this whole script was built to fix, 2026-07-13). But that overlap zone reached well above the laptop's screen **bottom** edge, so the phone bezel visibly sat on top of live screen content (confirmed by extracting a frame — the phone covered part of the "KURA" wordmark), not just the laptop's base/keyboard chrome. Root cause: nobody had actually checked whether a genuine side-by-side (zero-overlap) layout would fit — it does, once the laptop's margin is tuned to leave a real gap. Fixed: laptop now anchored to a left margin, phone width-scaled to fill the actual remaining gap (capped by canvas height too), placed fully beside the laptop with a visible gap — zero overlap by construction, not by clamping. Verify any `cover.mp4` build by extracting a frame (`ffmpeg -vf "select=eq(n\,60)" -vframes 1 out.png`) and looking at it before calling it done — this bug was invisible in the file listing/duration checks that shipped it the first time.

**Regenerating a cover.mp4 without the original raw (unframed) capture clips:** if only the already-framed `laptop.mp4`/`mobile.mp4` exist (no `raw_*.mp4`), crop the screen-content region back out with ffmpeg using the exact same `compute_placement()` math `build_laptop_or_mobile()` used to frame them in the first place (laptop defaults: canvas 960×720, `margin_frac=0.08`; mobile defaults: canvas 1080×1350, `margin_frac=0.12`) — this recovers a usable "raw" input to feed back into the fixed `build_cover()`. Don't hand-guess crop coordinates.

**Prioritize existing Cloudinary uploads over regenerating (Ridwan's instruction, 2026-07-21):** before generating or re-uploading any asset, check `{brand}-cloudinary-assets.json` (e.g. `kura-cloudinary-assets.json`) for an already-hosted version first. When an asset genuinely needs to be fixed/regenerated (like the cover-overlap bug above), upload the corrected version under a **new** public_id rather than overwriting the old one in place — Cloudinary version-pins existing URLs, and anything already referencing the old URL (queue rows, social-content libraries, other sessions) needs those references updated explicitly, not silently redirected. Record the supersession (old URL kept live, new URL marked as the one to use) rather than deleting the old asset outright.

**Format/safe-for-socials note (Ridwan asked explicitly):** keep the proven ratios — 4:3 (cover/laptop) and 4:5 portrait (mobile) are both within the safe non-destructive-crop range for Instagram, LinkedIn, and Facebook feed posts; X will letterbox/crop-preview 4:3 in-feed but the full video is still viewable on click. This isn't a new format decision, it's continuing the ratios already proven across every existing KURA/Jellys/Captain & Skipper export.

**Output location:** `outputs/templates/{slug}_{date}/` — same folder Step 5 ("Weekly Template/Page Showcase") of `docs/koolestpro-content-operating-plan.md` uses for the mockup + caption it copies back from `replo-rebuilds`. Contains the 3 videos + 3 designed images above (plus working intermediate files) and a companion `index.html` review page. Fix the naming duplication bug from attempt #1 too — that run saved every asset twice under two different naming conventions (`cover.png` AND `{slug} cover.png` with identical bytes); pick ONE convention (`{slug} cover.png` etc., matching the real Kura files) and only ever write that one.

**Companion page pattern (added 2026-07-12, mirrors Static Ad's `index.html`; updated same day, then corrected again same day to the reduced v2 set; asset #3 renamed 2026-07-29 per CORRECTED v4):** `outputs/templates/{slug}_{date}/index.html` displays the 7 real deliverables from the corrected V1 Asset Set above (3 videos with native `<video>` players, cover.png, preview.png, full-page.png, mobile-strip.png — no separate cards for the raw intermediate mobile-N/full screenshots) + LinkedIn caption + X post variants, plus the standard Pipeline Export Button with these constants:

```javascript
const POST_BRAND  = '<brand or product name>';
const POST_SLUG   = '<brandslug_page-type>';
const POST_TYPE   = 'Template Showcase';
const POST_FOLDER = 'outputs/templates/' + POST_SLUG + '_' + dateStr + '/index.html';
```

Register with type `"Template Showcase"` (see JSON Standard above) in `ridwan_content_system_updated.html`'s `SYNC_DATA.items`, status always `"Created"` on generation, never `"Published"`. Populate the optional `captions`/`assets` fields on the pipeline record too (not just inside the HTML) — this is the stream where that autopost-readiness extension matters most, since the whole point of the weekly buffer run is to leave a fully self-contained record behind for later automation.

### ⚠️⚠️ SOURCE CHANGED 2026-08-31 — replo-rebuilds is now a subfolder, the sync cache is retired

`replo-rebuilds` now lives **inside** this project at `replo-rebuilds/`. The whole cross-project access problem the sync cache existed to solve is gone: a scheduled task bound to `koolestpro-cowork-v2` can read every page live at `replo-rebuilds/brands/{brand}/pages/{page}/index.html`.

**`replo-pages-cache/` is RETIRED.** Do not read from it, do not refresh it, and do not treat its staleness as a problem — the `koolestpro-replo-cache-staleness-check` scheduled task that watched it has nothing left to watch and should be deleted or repointed. The folder is safe to delete; it is only 8 stale July copies.

**`replo-rebuilds-pages.json` stays** as the selection manifest, but each entry's `sourcePath` is now a live project-relative path (`replo-rebuilds/brands/...`) and is what gets read. The old `cachePath`/`cacheFolder` fields were renamed to `cachePathRetired`/`cacheFolderRetired` and kept as history only.

**New maintenance burden this introduces:** because the source is live, a page Ridwan builds under `replo-rebuilds/brands/*/pages/` does **not** automatically appear in the manifest. Any run that spots an uncatalogued page folder must add an entry for it rather than skipping it — that is how `halos-ad-01` and `kura-pdp-02` sat unnoticed for weeks while the weekly task fell back to retired KURA pages.

**Selection rule (unchanged):** eligible = `active:true` AND `usedForTemplateShowcase:false`, pick lowest `sortOrder`. A retired-KURA fallback must still be called out explicitly in the run summary, never taken silently.

| sortOrder | Entry | Source | State |
|---|---|---|---|
| 1 | `halos_pdp-01` — story-arc PDP | `replo-rebuilds/brands/halos/pages/halos-pdp-01` | used 2026-07-31 |
| 2 | `halos_hp-01` — custom editorial homepage | `replo-rebuilds/brands/halos/pages/halos-hp-01` | used 2026-08-18 |
| 3 | `halos_lp-01` — direct-response landing page | `replo-rebuilds/brands/halos/pages/halos-lp-01` | used 2026-08-23 |
| 4 | `halos_ad-01` — editorial-story advertorial | `replo-rebuilds/brands/halos/pages/halos-ad-01` | **active, unused** (added 2026-08-31) |
| 5 | `kura_pdp-02` — social-proof PDP | `replo-rebuilds/brands/kura/pages/kura-pdp-02` | **active, unused** (added 2026-08-31) |
| 90 | the 5 pre-2026-07-18 KURA pages | unchanged | retired — fallback only |

Both new entries had every local image ref verified to resolve on 2026-08-31 (7/7 and 34/34, zero missing). `kura-pdp-02` is deliberately **active despite being KURA** — the 2026-07-18 retirement applied to the five KURA pages that existed then, not to new KURA work. Its images total 31MB, so expect slower Playwright captures and sanity-check the full-page split height. `kura-social-content.md` has no pdp-02 section; write fresh captions rather than reusing the pdp-01 block.

**HALOS has no pre-written caption library.** There is no HALOS equivalent of `kura-social-content.md`, and that is expected rather than a missing file to hunt for. The weekly task writes HALOS captions itself from the page, humanizes them, and maintains `halos-social-content.json`/`.md` at this project's root.

**Not in this manifest, on purpose:** the multi-page store templates (MERIDIAN, Lumora Skin) live in `store-templates.json` and already have their own showcase packages at `outputs/templates/meridian_store-template_2026-08-28` and `outputs/templates/lumora_store-template_2026-08-28`. Their launch-content rules are in the Store Template Launch Content section above. `replo-rebuilds/templates/` holds unbranded page templates — only branded builds under `brands/` are showcase-eligible.

Step 1A reads `replo-rebuilds-pages.json` and resolves `sourcePath` live, falling to Step 1B's internal-page fallback only if no eligible unused entry is left.

**Weekly automation:** the `koolestpro-template-showcase-weekly` scheduled task (added 2026-07-12) runs this end-to-end on a buffer cadence — see the task's own SKILL.md for the exact selection/build/mockup/caption/registration sequence. It follows the same "unattended buffer run, never auto-publishes" pattern as `koolestpro-static-ad-weekly`.

**Reference library:** This skill's canonical, cross-project growing reference library lives in `replo-rebuilds/page-presentation-kit-references/` (see that project's own CLAUDE.md), not here — when both projects are connected in a session, save/read references there rather than duplicating a library in this project.

### ⚠️⚠️ CORRECTED v4 (2026-07-29, Ridwan's call — mosaic retired, mobile status bar added, caption rules tightened)

Two concrete complaints from a live review of the asset set, both fixed with new reusable scripts (read them, don't reinvent this per run):

**1. The grid mosaic (`{slug}-full-mosaic.png`) is RETIRED — Ridwan does not want it, full stop.** Replaced by `.ai-workflow/skills/page-presentation-kit/scripts/build_split_page.py`, which produces `{slug}-full-page.png`: the entire page captured at desktop viewport width, split into exactly TWO tall columns placed side by side (not a many-tile grid), matching a real reference Ridwan shared. Key differences from the old mosaic:
  - Exactly one split point, not many — found near the vertical midpoint but snapped to the nearest real section gap (a run of low content-density/whitespace), so a column break never cuts through a section. This is what "not necessarily 50%" means in practice — column 1 and column 2 will usually be close to even but not forced to an exact half.
  - Both columns read normally top-to-bottom, left column finishing where the right column continues (NOT mirrored/flipped) — this matches the reference exactly.
  - Still keeps the two genuinely useful parts of the old mosaic logic: walking the page top-to-bottom first so scroll-triggered reveal animations fire before the screenshot is taken, and excising sustained dead/blank runs (scroll-pinned sections a static shot can't represent) before splitting.
  - Plain light-neutral background (`#eeeeef`), no branded gradient chrome — this is meant to read as a straightforward whole-page reference, not a styled cover asset.
  - Usage: `python3 build_split_page.py "<page path>" out.png --file --width 1440`.
  - Rename the social-content key from `TS-{BRAND}-MOSAIC` to `TS-{BRAND}-FULLPAGE` for any brand file created/updated from here forward. Don't touch already-shipped historical keys.

**2. Mobile phone mockups (stills AND video) were shipping with a completely blank strip under the notch** — no time, signal, wifi, or battery, which read as empty/unnatural (Ridwan's words). Fixed with a genuinely reusable asset + shared compositing logic, not a one-off patch:
  - `assets/frames/status-bar-dark.png` / `status-bar-light.png` — the reusable status bar graphic (regenerate via `build_status_bar_asset.py` if the design ever needs a tweak; don't hand-edit the PNGs). Dark = dark icons for a light background; light = white icons for a dark background.
  - `.ai-workflow/skills/page-presentation-kit/scripts/status_bar_util.py` — shared placement/variant logic used by both the still and video compositors, so they can't drift apart.
  - **Reserved strip, not an overlay.** The first attempt simply painted the bar on top of existing content and it visibly collided with real page headers (a page's own logo text sitting exactly where the bar's time text landed, e.g. "9KURA41" — confirmed on a live test). Fixed design: the status bar gets its OWN reserved rectangle at the very top of the screen rect (same idea as a real phone reserving permanent space for system UI) — the screenshot/video is scaled to fill only the remaining height below it, so there is no possible collision. The strip's background is filled by sampling the average color of the content's own top edge, so it reads as a seamless continuation of the page's header rather than a visible seam, and the dark/light variant is auto-picked from that same sampled color (same idea as iOS's own "auto" status bar style). Pass `--status-bar dark|light` to force a variant, or `none` to skip it.
  - `.ai-workflow/skills/page-presentation-kit/scripts/build_device_still.py` — this is the new CANONICAL script for the still-image deliverables (`{slug} cover.png`, `{slug}-preview.png`). Earlier runs built these ad hoc each time ("Playwright/PIL compositing... ") without a named reusable script; this replaces that. Three modes: `single` (one device), `cover` (laptop+phone side by side, same non-overlapping geometry as `frame_video.py`'s `build_cover`), `preview` (3 angled phones at different scroll depths, each independently status-bar'd). All mobile compositing goes through `status_bar_util.py`.
  - `frame_video.py` updated the same way for `mobile`/`cover` video modes: the raw clip is now scaled to fill only the screen rect below the reserved strip, and the strip's fill color/variant is auto-sampled from a frame ~1.4s into the raw clip (not frame 0 — a live test found some pages show a loading/splash frame in the first second, which would give a false read; 1.4s lines up with `scroll_video.py`'s own 1200ms settle wait before it starts scrolling).
  - Known limitation, worth a sanity glance rather than a blocking concern: a page with an unusually long intro/splash animation (several seconds) could still get sampled mid-transition and produce a strip color that doesn't perfectly match the fully-loaded hero. Verify by actually looking at an extracted frame/still, same as this project's existing "verify by exporting, don't just read markup" principle — don't assume the auto-pick is right without a glance.
  - This applies to EVERY future phone mockup in this project, stills and video both — never ship a mobile mockup with a blank top strip again.

**2b. Status bar redesigned AGAIN same day — it now flanks the notch, not below it (2026-07-29 PM, Ridwan's immediate follow-up).** The reserved-strip fix above (2b's predecessor) collided with page headers, so it moved the bar below the notch entirely — but that's not where a real phone's status bar sits. On a real phone the time/icons are AT THE SAME HEIGHT AS THE NOTCH, flanking it left and right. Fixed properly this time, not just repositioned:
  - Calibrated the ACTUAL transparent slivers beside the notch in `assets/frames/iphone-frame.png` by scanning its alpha channel row-by-row (y≈20-59 in the 450×974 native frame) — these slivers sit entirely ABOVE where the screen content rectangle starts (y=59), so placing the status bar there means content fills the FULL screen rect exactly as it always did, zero reservation, zero possible collision, by construction rather than by careful positioning.
  - `status_bar_util.py` rebuilt around `compute_flank_mask()` (isolates the two notch-flanking transparent runs, explicitly excluding the outer rounded-corner cutouts) and `build_notch_status_layer()` (fills those slivers with the sampled top-edge color — this is the "colour that will match or complement whatever image we are doing" — and composites compact time/icon chips inside a calibrated safe rectangle within them).
  - Replaced the single wide `status-bar-{dark,light}.png` with four small chips sized for the narrow flank boxes: `status-bar-time-{dark,light}.png` and `status-bar-icons-{dark,light}.png` (regenerate via `build_status_bar_asset.py`).
  - `build_device_still.py`'s `compose_mobile_flat()` and `frame_video.py`'s `render_frame_png()` both updated: content/video now fills the full screen rect (no more offset/reduction math), the notch-flank layer composites between content and bezel, built in the bezel's own native coordinate space so it resizes/positions in perfect lockstep with the bezel image at any output scale.
  - Verified across all paths — single mobile still, 3-phone preview (including the ±10° rotated phones — the status bar rotates WITH the phone since it's baked in before rotation, not applied after), cover.png, and framed mobile video.
  - **Ridwan also has reference phone-mockup templates he's offered to share** for further improving overall mockup quality beyond the status bar fix — worth asking for and incorporating into `assets/frames/` if/when provided, rather than continuing to guess at styling from the current bare-bones frame graphic.

**3. Caption/copy formatting tightened project-wide (not just Template Showcase, and not just carousel slides).** Every piece of copy this project generates — LinkedIn captions, X posts, carousel slide copy, static ad text, CRO fix captions, everything — must: (a) contain no em dashes anywhere ("—" or "&mdash;"), rewritten as two sentences, a comma, or a colon instead (this was previously scoped to "on any slide" only — Ridwan's 2026-07-29 instruction generalizes it to all generated captions/copy); (b) run through the `humanizer` skill before being treated as final; (c) use real line breaks (not markdown `\n` literals or asterisks) and follow the existing X-vs-LinkedIn hashtag convention (no hashtags on X, hashtags fine on LinkedIn/Instagram) so the text is actually export-ready, not something that needs manual reformatting before it can be posted.

### ⚠️⚠️ CORRECTED v7 (2026-07-31 PM) — preview.png presets were too small/spread out, use flat_packed_2/3 by default

Same day as v6 above, Ridwan reviewed the rebuilt `halos_pdp-01-preview.png` (built with `flat_arc_3`) and shared a third reference image: 3 flat, evenly-sized phones with no rotation, filling almost the entire frame with only thin gaps between them. His instruction: "needs to be bigger and closely packed... taking almost all the image space... make sure you are using the correct dimension of image."

Measured against this project's own documented `{slug}-preview.png` canvas (2880×1800 — that dimension was already correct and didn't need to change): `flat_even_3`'s `scale: 0.62` only fills about 57% of canvas height, and its `cx` spacing (0.20/0.50/0.80) leaves roughly a 13-14%-of-width gap between adjacent phones. That reads as small and loosely arranged, not "almost all the image space."

**Fix — two new presets added to `build_device_still.py`'s `STYLE_PRESETS`, `flat_packed_2` and `flat_packed_3`.** Both push scale to ~0.95-1.0 (92% of canvas height, the same ceiling every preset's `base_scale` already computes) and tighten `cx` spacing so the gap between phones drops to roughly 7-8% of canvas width instead of 13-14%. **`flat_packed_3` is now the default choice for a 3-phone flat preview** — prefer it over `flat_even_3` whenever the goal is a big, fills-the-frame look (which is now the standing preference, not just a one-off ask). `flat_even_2`/`flat_even_3` still exist for a deliberately airier/smaller look if that's ever wanted, but don't default to them.

Note on `flat_packed_2`: `build_preview()`'s scale is height-driven regardless of phone count, so 2 phones alone can't fill a full 2880-wide canvas's width the way 3 can without exceeding the height ceiling and clipping top/bottom. For a genuinely packed 2-phone look, pass a narrower `--width` at call time — this project's own preview.png spec already anticipated this ("2880×1800... or narrower for a 2-phone style").

Verified 2026-07-31 PM: rebuilt `halos_pdp-01-preview.png` with `--style flat_packed_3` from the same 3 real scroll-depth screenshots (hero/mid/footer) — phones now dominate the frame with minimal background showing and only a thin gap between each, matching the new reference.

**Immediate follow-up correction, same evening:** the first `flat_packed_2`/`flat_packed_3` cut had the spacing backwards — thin outer margins (~2.5%) paired with wide gaps between adjacent phones (~7.6%). Ridwan's exact correction: "it should be space around, or narrow gap between the devices, and then some spaces at the right and left" — i.e. the reverse of what shipped. Fixed by swapping the ratio: outer margins are now the larger number (~7-7.5% each side for the 3-phone preset), inter-phone gaps are the thin one (~2.5-3% each). Phone scale itself didn't change (still maxed at ~92% of canvas height) — only how the leftover width is distributed changed. Re-verified on the same 3 HALOS screenshots: phones now read as nearly touching each other with a clearly more generous frame at the left/right edges, matching the reference's actual spacing rhythm, not just its "big and packed" quality.

### ⚠️⚠️ CORRECTED v8 (2026-09-02) — new `{slug}-mobile-strip.png` asset, and it always gets an X post

During the `halos-li-02` listicle build a throwaway QA contact sheet was generated to review the mobile render: the full mobile page sliced into 6 equal columns placed side by side. Ridwan saw it and asked for it to become a real deliverable, in his words: "I love this image, add it to outputs and preview in the future and it should be registered as a type of template for template showcase type of posts and it should always be posted in my x account."

**The asset.** `{slug}-mobile-strip.png` is now the 4th designed image in the Template Showcase set (see the table above). It is the entire page at MOBILE viewport width, split into 6 columns, placed flush side by side with no outer frame. It does not replace `{slug}-full-page.png`; the two answer different questions. The full-page split is a desktop reference on a neutral canvas. The strip shows how the responsive build actually behaves on a phone, end to end, in one frame.

**Scope — WIDENED the same day, 2026-09-02.** The first answer was "Template Showcase only". Ridwan then overrode it: "Whatever we do, anywhere we are building new pages and anywhere we are doing template showcase, we want to make sure this does not escape." So the strip is now produced at BOTH points in the chain:

- **At page-build time.** `koolestpro-weekly-template-build` (Wednesdays) saves one into `replo-rebuilds/brands/{brand}/pages/{page}/presentation/{page}-mobile-strip.png` for every new page it builds. Building it here means it exists long before the showcase run needs it.
- **At showcase time.** `koolestpro-template-showcase-weekly` (Saturdays) copies that one into the package if it is current, and rebuilds it if it is missing or the page has changed since. Either way the asset must exist in the package.

Still deliberately NOT generated for CRO Fix rebuilds — those are a different stream with their own before/after assets, and nothing has asked for it there.

**It is enforced, not just documented.** Instructions in task prompts are the first line of defence; these are the checks that do not depend on a run remembering:

| Guard | Where | What it catches |
|---|---|---|
| X #5 calendar slot | `populate_sheet.py` `CALENDAR` — "Template Showcase", "Store Template", "Store Template (Paid)" | the asset existing but never being scheduled |
| `x_glance` caption key + fallback chain | `populate_sheet.py`, `harvest_store_template.py` | the strip post silently recycling another angle's caption |
| compressed-sibling preference in `resolve_assets()` | `populate_sheet.py` | an oversized PNG reaching Make and failing the fetch (the 2026-08-01 Bebemoss failure mode) |
| Step 2b recovery gate | `koolestpro-weekly-distribution-assembly` | a package arriving without a strip: the task builds it rather than shipping one fewer X row |
| `audit_mobile_strips.py` | `koolestpro-replo-cache-staleness-check` (Mondays) | anything the above missed, across sources / packages / queue rows |

`audit_mobile_strips.py` splits NEW gaps from the HISTORICAL BACKLOG that predates the asset (11 packages, 10 source pages, 8 assembled queue items as of 2026-09-02) and exits non-zero only on a new gap, so the weekly check stays a real signal instead of reporting the same known backlog forever. **That backlog is deliberately not backfilled** — each item costs a Playwright capture, and re-running `populate_sheet.py` on an already-assembled item would append an X row to a week that has already passed. Backfilling is Ridwan's call, not something a run should do unprompted.

**Build it with `.ai-workflow/skills/page-presentation-kit/scripts/build_mobile_strip.py`.** Do not hand-roll the slicing per run.

```bash
python3 build_mobile_strip.py "<page path>" "{slug}-mobile-strip.png" --file
# --columns 6 (default) --pad 0 --gap 0 --width 390
```

Three things about that script are load-bearing rather than cosmetic:

- **Spacing defaults are flush (`pad=0`, `gap=0`) on purpose.** That reproduces the composition Ridwan approved. This is the opposite of the `preview.png` spacing rule in CORRECTED v7 (generous outer margins, thin inner gaps), which governs floating phone mockups and does not apply here. Do not "fix" one to match the other.
- **Column cuts snap to real section seams**, reusing `build_split_page.py`'s density analysis generalized to N-1 cuts, so a column boundary never slices through the middle of a section. Because cuts land on seams, columns end at different heights; the script fills each short column's remainder with the average colour of that column's own bottom edge, so the strip's bottom edge reads as continuous background instead of hard white voids.
- **It falls back to tile stitching when `full_page=True` crashes the renderer.** That crash is real and reproducible on image-heavy pages in this sandbox even with `--disable-dev-shm-usage`, and it lands partway down the page rather than at the screenshot call. Related capture gotcha worth remembering: lazy-loaded images report as broken if you check them immediately after a tile capture, so any broken-image assertion needs a full pre-warm scroll first, otherwise you will chase a phantom bug (this happened on halos-li-02 — a reviewer avatar rendered as alt text in two consecutive stitches and was fine all along).

**Distribution: this asset always gets its own X post.** Ridwan's instruction was that it should always be posted to X, and when asked whether it should replace an existing slot or add one, he chose to add a 5th X post rather than displace any of the four existing angles. See the updated weekly shape in the Store Template section below. The angle is "full page at a glance" — the whole responsive build in one image, which is a different pitch from X #4's build-in-public narrative.

Register it in the brand's social-content library under `TS-{BRAND}-MOBILESTRIP`.

---

### ⚠️⚠️ CORRECTED v6 (2026-07-31) — video scroll-completion bug fixed, phone-size/whitespace fixes verified, sticky-header capture bug fixed, mandatory two-tier QA added

The first real HALOS run (`halos_pdp-01_2026-07-31`) shipped with three concrete defects Ridwan flagged directly after reviewing the files, plus a fourth found during this round's own QA pass. All four are now fixed at the script level, not just patched for that one run.

**1. Videos didn't finish scrolling ("especially the desktop/laptop mock").** Root cause, confirmed by extracting frames across the old `laptop.mp4`'s timeline: identical hero content sat on screen from t=10s to t=20s (a real 10-second stall), then a completely different section appeared at t=29s with no visible transition — a stall-then-jump-cut pattern. `scroll_video.py`'s scroll was timed by an in-page `requestAnimationFrame` loop racing against `performance.now()`; under heavy render load (a big desktop viewport especially) the page's own main thread can stall for real seconds, and once the callback finally fires it jumps straight to the end instead of finishing smoothly. `scroll_video.py` is now marked deprecated for this pipeline (its docstring says so) — **use `scroll_video_raw.py` instead**, which drives scrolling with externally-stepped `page.evaluate(scrollTo) + page.wait_for_timeout()` calls from the Python/CDP side (immune to page-thread stalls) and captures at `device_scale_factor=1` for video specifically (quarters the per-frame pixel volume, directly cutting stall risk — no quality loss since `frame_video.py` scales into the bezel's screen rect anyway). It outputs a raw `.webm` only; no separate ffmpeg conversion step is needed since `frame_video.py` reads video files straight into its ffmpeg filter graph regardless of container. Verified 2026-07-31: rebuilt `laptop.mp4` (35s real capture), `mobile.mp4` (41s real capture), `cover.mp4` (built from both raw clips) — extracted 6 frames across each timeline and confirmed genuine progression with no stall, reaching a real rendered footer ("© 2026 HALOS Wellness — Powered by Shopify") at the end of both laptop and mobile.

**2. Mobile mockups must all be the same height and width within one arrangement.** Ridwan's own reference sprite sheets (`Double Screen Template.png` / `Triple Screen Template.png`) confirmed every phone within a given tile is identical in size — only position and rotation vary, never scale. `build_device_still.py`'s `STYLE_PRESETS` now uses one shared `scale` per preset (was previously varying per-phone, e.g. a bigger "hero" phone in an arc). Verified 2026-07-31: rebuilt `halos_pdp-01-preview.png` with `--style flat_arc_3` from 3 real scroll-depth screenshots (hero/mid/footer) — all 3 phones render at identical size.

**3. Full-page split needs visible whitespace left and right.** `build_split_page.py`'s `pad` raised from 28 to 110 and `gap` from 28 to 48 (function defaults, no flag change needed) — the old margin read as edge-to-edge once a light page background sat against a similarly light canvas. Verified 2026-07-31 on the rebuilt `halos_pdp-01-full-page.png`.

**4. Sticky/fixed nav header duplicating mid-image (found during this round's own QA, not named by Ridwan).** Chromium's full-page screenshot stitches internal tiles together, and a `position: sticky`/`fixed` header paints at its "stuck" position on every tile — so it shows up floating over unrelated content partway down the image, not just once at the top. Fixed in `build_split_page.py`'s `capture_full_page()`: immediately before the final screenshot, a `page.evaluate` forces any element with computed `position: fixed` or `position: sticky` to `position: static !important`, leaving only the one real in-flow header at the top. Verified 2026-07-31 — the artifact is gone from the rebuilt full-page image.

**Mandatory two-tier QA (Ridwan's standing instruction, 2026-07-31): "the aim is to troubleshoot and iterate at least once before concluding as done."** Every future Template Showcase build (and, by extension, any similar multi-asset build in this project) must:
- **Tier 1 (per-showcase):** right after generating the asset set, extract several frames spread across each video's full timeline and actually look at them (confirm no stall, confirm a real footer at the end); look at the preview image for uniform phone sizing; look at the full-page split for visible whitespace and no sticky-header artifact. Fix anything found before moving on — don't note it and continue.
- **Tier 2 (whole-run):** after registration/social-content steps, re-open the companion HTML and confirm every asset link resolves to a real final file (not a draft/versioned name), re-parse every JSON file touched this run to confirm it's still valid, and fix anything found before writing the final summary.

This is now baked into the `koolestpro-template-showcase-weekly` scheduled task's own instructions (updated 2026-07-31) — see that task's SKILL.md for the full QA checklist wording, and the "Run 5 / 2026-07-31" history entry there for the complete narrative.

**File deletion:** Ridwan gave standing blanket permission (2026-07-31) to freely delete scratch/intermediate files (raw captures, QC frame extractions, superseded draft versions) in this project's outputs without asking each time. If a plain `rm` fails with "Operation not permitted," call the file-delete-permission tool for that path rather than leaving scratch files behind.

### ⚠️⚠️ CORRECTED v5 (2026-07-29 PM, 3rd follow-up same day) — multi-phone preview arrangements now use Ridwan's 16 reference styles, not freeform positioning

Ridwan shared two reference sprite sheets — `Double Screen Template.png` and `Triple Screen Template.png`, saved directly to this project's root — each showing 8 distinct phone-mockup arrangement geometries (using unrelated "Captain & Skipper" brand content as filler, which is irrelevant; only the ARRANGEMENT matters). His instruction: "these are a lot of styles, and I would like to always use them, mostly for the theory mock-up... always use one of those styles while maintaining the status bar you have designed. You can also use my brand background, or whenever you think another plain colour is going to work better, feel free to use it. Just make sure you use one of those styles."

**`build_device_still.py`'s `preview` mode now has a `STYLE_PRESETS` dict** distilling the 16 reference tiles into 8 reusable named geometries (some reference tiles are minor variations of the same underlying pattern, so they collapse to one preset):

| Preset | Phones | Reference tiles | Look |
|---|---|---|---|
| `flat_even_2` | 2 | double 1 | equal-size flat pair, side by side |
| `flat_stagger_2` | 2 | double 2, 5, 6, 8 | flat pair, one bigger/lower, one smaller/higher |
| `crossed_2` | 2 | double 3 | angled pair crossing in the middle, moderate scale |
| `crossed_2_large` | 2 | double 4, 7 | same crossing pair, larger scale filling more of the frame |
| `flat_even_3` | 3 | triple 1 | equal-size flat row of 3 |
| `flat_arc_3` | 3 | triple 2, 3, 5, 6 | arc/stagger of 3, center phone prominent |
| `fanned_stack_3` | 3 | triple 7, 8 | overlapping card-fan stack, front phone fully visible |
| `angled_trio` | 3 | (this skill's original hardcoded layout, kept as its own preset) | back-left / front-center / back-right, all angled |

Pick 2 or 3 phones and a matching preset based on how many meaningfully different scroll depths there are to show (don't pad 2 real screenshots into a 3-phone preset just to hit a count). Run `python3 build_device_still.py preview --list-styles` to see all presets. Usage: `--style flat_stagger_2 --screenshot a.png --screenshot b.png --output preview.png` (screenshot count must match the preset's `count`, or it errors with the valid alternatives).

**Background choice is now explicit, not fixed to the brand gradient.** `--bg-mode gradient` (default, unchanged brand orange→purple glow) or `--bg-mode plain --bg-color e0e4f0` (flat color; omitting `--bg-color` falls back to `REFERENCE_PLAIN_BG`, the exact lavender sampled directly from Ridwan's own reference tile — rgb(222,226,239) — so "plain" has a real, already-approved default rather than an arbitrary guess). Applies to `single`, `cover`, and `preview` modes. Choose per-run based on what the destination page's content looks best against — same judgment call as choosing a preset, not automatic.

**Status bar behavior is unchanged and mandatory in every preset** — `compose_mobile_flat()` still runs for every phone slot regardless of which preset is chosen, including rotated ones (the notch-flank layer rotates WITH the phone since it's composited before rotation, same as before this change). Verified 2026-07-29 across `crossed_2` (plain bg), `flat_stagger_2` (gradient bg), `fanned_stack_3` (plain bg) and `flat_arc_3` (gradient bg) against real kura-hp-01 mobile screenshots at 3 different scroll depths (hero/mid/footer, captured via a walk-then-screenshot Playwright pass so scroll-triggered reveal animations had already fired) — all four rendered correctly with auto dark/light status bar variants per phone.

**Going forward: every multi-phone preview built in this project must use one of these 8 presets.** Do not hand-roll a new cx/cy/scale/rotate layout ad hoc — if none of the 8 fit a specific need, that's a sign to add a 9th named preset (and document it here), not to freehand positioning for one run.

---

## CRO Fix — Static Image Export & Weekly Automation (added 2026-07-12)

Completes the third weekly content stream (alongside Static Ad and Template Showcase above) with the same "unattended buffer run, never auto-publishes" pattern.

**Static image export (reusable script, not a one-off):** `.ai-workflow/tools/export_static_images.py` opens any finished `outputs/cro-fixes/{slug}_content.html` headlessly and calls the file's own real `captureFixed()`/`captureSlide()` functions — the same ones the on-page download buttons use — so the output is byte-identical to a manual export, not a generic screenshot. Run `source .ai-workflow/tools/bootstrap_env.sh` first (idempotent ARM64 Playwright/libXdamage setup). Usage:

```bash
python3 .ai-workflow/tools/export_static_images.py \
  outputs/cro-fixes/{slug}_content.html \
  outputs/cro-fixes/{brand-lowercase}/
```

Writes generic names (`ba-graphic.png`, `anno-graphic.png`, `slide-N.png`, `captions.txt`, `manifest.json`) — rename to the established convention (`koolestpro_{brand-lowercase}_before-after.png`, `_annotated-changes.png`, `_slideN.png`) already in use at `outputs/cro-fixes/v1ce/`. This supersedes driving a one-off inline Playwright script by hand each time (that approach worked for the first V1CE export but isn't documented/reusable — this script is the canonical version going forward).

**Weekly automation:** the `koolestpro-weekly-cro-fix` scheduled task (added 2026-07-12, Saturdays 09:06, offset from `koolestpro-static-ad-weekly`'s 09:02 same morning) runs the full sequence end-to-end — target selection from `targets_pool.json`, Skill A audit, DeepSeek-delegated rebuild, real before/after screenshots, the `#ba-graphic`/`#anno-graphic` templates, static export via the script above, sync into `ridwan_content_system_updated.html`, marking the target `Used`, updating the brand's social-content library, and logging a row in `outputs/weekly-tracker.xlsx`. Full procedure documented in `.ai-workflow/weekly-pipeline.md` — the scheduled task's prompt just points there rather than duplicating the steps inline, so updates to the doc apply automatically to future runs.

**Sheet/Make.com handoff — explicitly deferred (2026-07-12):** Ridwan confirmed "it's not time for Make.com" yet — the weekly tracker stays a local `outputs/weekly-tracker.xlsx` file (via the `xlsx` skill), not a live Google Sheet. The connected Google Drive connector can only create brand-new files, not edit an existing sheet in place, so it isn't a fit for a live tracker anyway. The Make connector *is* already connected, and each export run's `manifest.json` is deliberately structured (brand/slug/type/file paths, no HTML-scraping required) so that when Make.com integration does happen, it has a clean file to consume rather than needing rework.

---

## 🎯 Template Showcase = New-Store-Build Inbound Track (added 2026-07-12)

Ridwan's inbound strategy now includes a second audience distinct from CRO Fix's audience: store owners who need a **brand-new online store built**, not an existing store with a fixable defect. Rather than a separate tracking file or outreach process, this runs entirely through content — the Template Showcase stream (real replo-rebuilds pages, mocked up weekly) already produces exactly the proof-of-work this audience needs to see.

**The only operational change:** Template Showcase captions must close with a "need a store built" CTA (e.g. "Need a store like this for your brand? DM me"), never a CRO/audit-style CTA ("want this fixed on yours?"). CRO Fix and Static Ad content keep their existing audit/fix framing — the split is deliberate, not a project-wide CTA change. See `koolestpro-template-showcase-weekly`'s own CTA FRAMING RULE for the exact wording pattern.

No new JSON tracking file was added for this (decided 2026-07-12) — it's a content-only motion. If it later needs active outreach/lead tracking, that would follow the same pattern as `outreach_tracker.json` but with a `leadType` field distinguishing "new-store-build" from "cro-audit," since `targets_pool.json`'s CRO-oriented schema (`mobileIssueSummary`, `visualPotential`, etc.) doesn't fit a prospect who has no existing store to audit.

---

## 🏪 STORE TEMPLATE LAUNCH CONTENT — MANDATORY (added 2026-08-28, Ridwan's standing instruction)

Applies to **every** store template in `store-templates/` — Lumora, Meridian, and every future one. Ridwan's words: "for every future new template we build, we are going to do the same." A template is not finished when it passes QA. It is finished when the content that sells it exists.

### 1. Brand the packaging in generated product imagery

When generating product images for a template's demo brand, **put the brand name on the product**. Ridwan: "I prefer to see that brand name on the product so things look very branded and neat. That can be a source of getting a brand design project."

This **reverses** the earlier "leave labels blank so the set survives a reskin" decision made during the 2026-08-28 Lumora build. Branded reads as finished work and advertises a second service (brand and packaging design) that a blank bottle does not. Reskin economics lose to that.

- Put the wordmark in the prompt explicitly: `a cream label reading exactly "LUMORA" in small spaced capitals`.
- Keep it subtle and typographic. A demo store where every bottle shouts the name reads worse than one where the label is quietly correct.
- Use `--quality low` and check the spelling on every render before accepting it. gpt-image renders short all-caps wordmarks reliably at low quality, but verify rather than assume.
- **Lumora's existing 16 images are the documented exception** — they were shot unbranded before this rule existed and the gpt-image budget was exhausted the same day. Re-shoot them branded when budget allows; everything else about them is fine.

### 2. Every finished template ships a post set

Ridwan: "Whenever we are done, I want to generate a post based on whatever we did."

| Platform | What ships |
|---|---|
| LinkedIn | One post, the Template Showcase angle, built around the mockup image |
| Instagram | One post, caption plus image |
| X / Twitter | **Five angles**, not one (see below) |

The five X angles, all confirmed by Ridwan (the fifth added 2026-09-02):

1. **Template showcase** — the mockup image plus a caption about the build itself.
2. **Free offer / Nigeria package** — "Real business, no website yet? Yours can look like this, free." Points at the Nigeria local package.
3. **Niche-targeted** — aimed at that template's vertical specifically. Skincare and beauty brand owners for Lumora, watch/jewellery/accessory brands for Meridian. Ridwan: "we use the opportunity to create content based on the niche of that template... The posts will be targeted at them. If they need something like this, they can contact me."
4. **Build-in-public** — how it was made, the machinery, the QA. Attracts builders and the buyers who like seeing it.
5. **Full page at a glance** — the `mobile-strip.png` asset, the whole responsive build in one frame. Added 2026-09-02 on Ridwan's instruction that the strip "should always be posted in my x account"; he chose to add a slot rather than displace any of the four above. See CORRECTED v8 in the Page Presentation Kit section.

### 3. The mockup images are the post assets

Ridwan: "I like your preview images, and I would love to post them on Twitter." The Template Showcase asset set (`{slug} cover.png`, `{slug}-preview.png`, `{slug}-full-page.png`, `{slug}-mobile-strip.png` — see the Page Presentation Kit section above for the exact spec and scripts) is what these posts are built around. Build them with `build_device_still.py`, `build_split_page.py` and `build_mobile_strip.py`; they are Playwright and PIL only, so they cost no gpt-image budget.

Pair them deliberately rather than attaching the same image to everything: `preview.png` (multi-phone) carries the showcase and niche angles, `cover.png` (laptop plus phone) carries LinkedIn and the free-offer angle, `full-page.png` carries build-in-public, and `mobile-strip.png` carries the full-page-at-a-glance angle.

### 4. Register it like any other content

Every template's post set gets a `{brand-slug}-social-content.md` / `.json` pair at the project root, keyed `TS-{BRAND}-*` (see the Per-Brand Social Content Library section below), and a pipeline record of type `"Template Showcase"` synced into `ridwan_content_system_updated.html`. Status is `"Created"`, never `"Published"`.

### 5. Standing rules that still apply

No em dashes anywhere in the copy. Run every piece through the `humanizer` skill. Real line breaks, never markdown literals. No hashtags on X; hashtags are fine on LinkedIn and Instagram. Never imply a concept brand was a real client — Lumora and Meridian are invented and every post must be able to survive someone asking "is this a real client?"

### 6. ⚠️ A finished template MUST reach the distribution queue (added 2026-09-01, Ridwan's instruction)

Ridwan's words: "anytime there is something built, we want to add it... take whatever presentation has been made and schedule it on a good day so that we always have a post of work done, which is mainly the free e-commerce site offer."

Registering a pipeline record is NOT the finish line. A store template is done when its 6 posts are sitting in the live Google Sheet.

**Why this needed its own stream.** Lumora and Meridian were both registered `"Template Showcase"`, status `"Created"`, on 2026-08-28 and still had zero distribution rows on 2026-09-01. Two independent reasons, either one fatal:

1. Store template packages ship **no companion `index.html`** — their `folder` points at the asset directory. `harvest_content.py` parses caption tabs out of a companion page, so it had nothing to read and returned an empty record.
2. The `"Template Showcase"` calendar slots match `cover.mp4` / `laptop.mp4` / `mobile.mp4`. A store template package is **stills only** (cover, preview, full-page). Even a successful harvest would have matched zero assets on every slot.

**The routing, now automatic:**

```bash
# 1. harvest from the social-content library (NOT harvest_content.py)
python3 .ai-workflow/tools/harvest_store_template.py <brand-slug> \
    --out /tmp/<brand>_harvest.json --project-root .
# 2..6 identical to every other stream
python3 .ai-workflow/tools/qa_check.py /tmp/<brand>_harvest.json --project-root .
python3 .ai-workflow/tools/populate_sheet.py /tmp/<brand>_harvest.json --project-root .
python3 .ai-workflow/tools/feed_linkedin.py --project-root .
python3 .ai-workflow/tools/feed_media.py --project-root .
python3 .ai-workflow/tools/sync_content_system.py --project-root .
python3 .ai-workflow/tools/append_sheet_rows.py --project-root . --dry-run   # then for real
python3 .ai-workflow/tools/sort_distribution_queue.py --project-root .
```

`harvest_store_template.py` reads `{brand-slug}-social-content.json` (already the durable source of truth for captions) and maps each asset record's own `angle` field to a caption key. It resolves `pipeline_item_id` from `relatedPipelineItemIds` and **verifies it exists in SYNC_DATA** rather than synthesizing one, which is what prevents the orphaned-duplicate-row failure.

**Two streams, picked automatically from `isConceptBrand`:**

| Stream | When | X slot #2 |
|---|---|---|
| `Store Template` | `isConceptBrand: true` — a demo brand built to advertise the free sample-site offer | free offer / Nigeria package |
| `Store Template (Paid)` | a real named client build, or any local/paid job | result / process, paid CTA |

Override with `--offer-type free|paid` when the flag guesses wrong. There is deliberately **no fallback between the free-offer and results caption keys** — a paid client build must never inherit "I'll build you one free," and a free-offer post must never inherit paid-client framing. An empty row that gets flagged is the correct failure here.

**The weekly shape** (anchor Tuesday 09:00 ET, chosen so store builds never collide with the Friday Template Showcase drumbeat):

| Slot | Day | Asset | Angle |
|---|---|---|---|
| LinkedIn | Tue 09:00 | cover + preview (2-page PDF) | launch anchor |
| Instagram | Thu 12:00 | preview | multi-phone |
| X #1 | Tue 13:00 | preview | template showcase |
| X #2 | Wed 09:00 | cover-16x9 | free offer (or result, if paid) |
| X #3 | Fri 13:00 | preview | niche-targeted |
| X #4 | Sat 09:00 | full-page-**x** | build in public |
| X #5 | Sun 11:00 | mobile-strip | full page at a glance |

Three asset details that are load-bearing, not cosmetic:

- **X #5 matches `mobile-strip`** (added 2026-09-02, see CORRECTED v8). `build_mobile_strip.py` writes a compressed `-x.jpg` sibling automatically whenever the PNG clears ~4MB, for the same Make fetch-limit reason as `full-page-x` below; point the row at that sibling when it exists. A 6-column strip of a typical page lands around 1.7MB, so most runs will not need it.
- **X #4 matches `full-page-x`, never `full-page`.** The full-resolution split-page runs 4-5MB and is exactly what broke the Bebemoss X post on 2026-08-01 (Make's fetch limit). The matcher is narrow so it cannot silently fall back to the oversized original.
- **The LinkedIn row carries two images on purpose.** `feed_linkedin.py` routes any image row through a hosted PDF, because Make's LinkedIn scenario has only text / `.mp4` / `.pdf` routes and no plain-image route. One image produces a one-page document card, which is a weak anchor post. Cover plus preview gives a real 2-page carousel.

**Back-to-back builds stagger themselves.** `find_open_week()` resolves each slot independently and skips any (platform, date, time) already taken, so a second store template assembled in the same run rolls to the following week automatically. Do not pin with `--week-monday` to force this; that flag is for deliberate backfills only.

**Caption length is a real gate for this stream.** These post sets are written as prose first and the four X captions ran 282-475 chars on both Lumora and Meridian, over X's 280 cap, which would have failed on post. `populate_sheet.py` now flags every `x_*` key against the limit. Fix the length in the social-content `.json` **and** its `.md` sibling (never let the pair drift), then re-harvest.

---

## 📚 Per-Brand Social Content Library — `{brand-slug}-social-content.md` / `.json` (added 2026-07-12)

This is the canonical answer to "how do I get the caption for a given generated image when it's time to automate posting." It mirrors a convention Ridwan already runs in `replo-rebuilds` (`kura-social-content.md`) — one growing file per brand, at the project root, that maps every generated asset to its ready-to-post caption via a short key. This is now the standard for `koolestpro-cowork-v2` too, and is the intended starting point for any future Make.com/Sheets autopost integration — not the `captions`/`assets` fields on the pipeline item (see below for how those two relate).

**File pair, one per brand, at project root:**

- `{brand-slug}-social-content.md` — human-readable, matches the `kura-social-content.md` table+block format: a "HOW TO USE THIS FILE" key table up top, then one fenced caption block per key, grouped by post/date as the brand accumulates more content over time.
- `{brand-slug}-social-content.json` — machine-readable sibling with the *same keys*. This is what an automation step actually reads. Update both together; never let them drift.

**Key scheme (per content type produced in this project):**

| Type | Key pattern | Example |
|---|---|---|
| Static Ad | `SA-{BRAND}-PROBLEM` / `-BENEFIT` / `-PROOF` / `-OFFER` / `-COMBO` / `-X1..3` | `SA-OBVI-BENEFIT` |
| CRO Fix | `CRO-{BRAND}-BA` (before/after) / `-ANNO` (annotated) / `-CAROUSEL` / `-X1..3` | `CRO-V1CE-BA` |
| Template Showcase | `TS-{BRAND}-COVER-VID` / `-LAPTOP-VID` / `-MOBILE-VID` / `-COVER-IMG` / `-PREVIEW` / `-FULLPAGE` / `-MOBILESTRIP` (`-MOBILESTRIP` added 2026-09-02, see CORRECTED v8; corrected 2026-07-12 v2 — 3 videos + 3 designed images per page, reduced from an earlier ~7-image draft the same day; `-MOSAIC` renamed to `-FULLPAGE` 2026-07-29 when the grid mosaic was retired, see CORRECTED v4) | `TS-KURA-PREVIEW` |
| Tip | `TIP-{BRAND}-COVER` (slide 1) / `-CAROUSEL` (all slides) / `-X1..3` — the `-GRAPHIC-A/B/C` standalone graphics were retired 2026-07-18, do not create them | `TIP-KOOLESTPRO-CAROUSEL` |

**JSON shape** (see `obvi-social-content.json` / `v1ce-social-content.json` for real examples):

```json
{
  "brand": "Brand Name",
  "brandSlug": "brandslug",
  "relatedPipelineItemIds": ["..."],
  "assets": {
    "SA-BRAND-PROBLEM": {
      "platform": ["linkedin", "instagram"],
      "assetType": "image",
      "assetPath": "outputs/.../file.png",
      "caption": "ready-to-post text, disclaimer included where required",
      "hashtags": [],
      "status": "Not Posted",
      "postedAt": null
    }
  }
}
```

Where one visual genuinely has multiple usable caption angles (common for CRO Fix before/after graphics — see `v1ce-social-content.json`'s `CRO-V1CE-BA`), use `captionOptions: [{id, caption, hashtags}, ...]` instead of a single `caption` — pick one at post time, don't post all of them against the same image.

**Relationship to the pipeline item's `captions`/`assets` fields (added 2026-07-12, same day):** those fields on the `SYNC_DATA.items` record stay as a lightweight, optional convenience cache — useful for a quick glance at `content_pipeline.html` without opening a separate file. The `{brand}-social-content.json` file is the durable source of truth: it accumulates across every post ever made about that brand (not just one pipeline item), carries per-asset posted/not-posted status, and is what any future autopost step should actually be built against. If they ever disagree, the brand social-content file wins.

**Every output skill and scheduled task that generates captioned assets for a real or sample brand must create or update that brand's `{brand-slug}-social-content.md`/`.json` pair** — `koolestpro-static-ad-weekly` and `koolestpro-template-showcase-weekly` do this as of 2026-07-12.

**Known gap to watch for:** a caption is only useful once its matching image actually exists on disk. Some CRO Fix graphics (before/after, annotated, carousel slides) are only generated client-side via html2canvas download buttons inside the review HTML — nobody may have clicked them yet. Check the social-content file's `knownGaps` field (when present) before assuming an `assetPath` is real.

**Resolving that gap (established 2026-07-12):** don't take a generic Playwright/browser screenshot of the review HTML as a substitute — html2canvas renders some effects (e.g. SVG gradients) differently than a native screenshot, so the export must go through the page's own capture function. Drive headless Playwright against the review HTML, call the page's existing capture function directly via `page.evaluate()` (e.g. `captureFixed('ba-graphic')` / `captureSlide(idx)` in the CRO Fix content.html pattern — grep the file for `html2canvas(` to find the real function names, they vary slightly per generator), and use `page.expect_download()` to intercept the resulting `a.click()` download and `save_as()` it directly to the correct `outputs/...` path. Never route the image data through the conversation itself (e.g. returning a `canvas.toDataURL()` string) — a single scale:2 PNG can be several MB of base64, which is both slow and wasteful. See `.ai-workflow/tools/README.md` for this sandbox's one-time ARM64 Playwright setup recipe. `v1ce-social-content.json`'s `exportLog` field has a full worked example, including a spot-check that caught a claim worth verifying (see next paragraph) before trusting it.

**Always verify, don't just export:** exporting an asset isn't the same as approving it. Actually look at what got exported before treating it as post-ready — `v1ce-social-content.json`'s `exportLog` documents a real case where a rebuild's trust badge ("Also trusted by HSBC & IBM") looked like a possible fabricated claim on first glance and had to be checked against the live source site before it could be trusted (it turned out to be real — V1CE's own PDP has that exact client-logo carousel further down the page). A Step 8 review that only reads caption text without ever looking at the rendered graphic can miss this class of issue entirely.

---

## Trend & Format Radar — Export Routing (added 2026-07-30, planning: docs/koolestpro-content-operating-plan.md Step 11)

This project uses the portable `koolestpro-trend-radar` skill (installed globally, project-agnostic — same pattern as `page-presentation-kit`/`static-ad-image`) for weekly trend-aware Tips topic selection (Layer 1) and opportunistic cross-format discovery (Layer 2, "Format Radar"). The skill itself carries no opinion about niche keywords or file locations — this section is what tells it where things belong in *this* project specifically.

**Config file:** `trend-radar-config.json` (project root) — pillars/keywords, per-source enable flags and budget caps, and output paths. Read this, not this CLAUDE.md section, for the actual machine-readable settings; this section is narrative context for a human reading the doc.

**Scope:** Layer 1 feeds **Tips only**. CRO Fix, Static Ad, and Template Showcase are target-brand-driven (from `targets_pool.json`), not topic-driven, and stay exactly as they are — Ridwan's explicit call, 2026-07-30.

**Sources:**
- **X** — official pay-per-use API, app-only Bearer token (`X_BEARER_TOKEN` in `.env`, get it from developer.x.com → the app → Keys and tokens → "Bearer Token" specifically — this is a DIFFERENT credential from the OAuth2 client id/secret already powering the live "Koolestpro Social Distribution" Make.com posting scenario). Capped at 50 reads/week (~$1/month), sharing Ridwan's existing $5-7/month X credit pool with posting. Raise the read cap before raising run frequency if more volume is ever needed, and never let total X spend (posting + trend-radar reads combined) exceed ~$5/month without Ridwan's explicit say-so.
- **Reddit** — LIVE as of 2026-08-11, via Apify's "Reddit Scraper Lite" actor (id `oAuCIx3ItNrs2okjQ`), not a dedicated Reddit API reseller. Ridwan's call: reuse the Apify account already wired in `.env` (`APIFY_USER_ID`/`APIFY_API_TOKEN`) instead of signing up for a separate provider. Pay-per-result, ~$0.004/result as verified live. `reddit_search.py` calls the actor async (start run → poll `actor-runs/{id}` → read dataset) rather than Apify's `run-sync-get-dataset-items`, since that blocking endpoint exceeded this sandbox's own ~45s command ceiling in testing — the async pattern works in any environment, scheduled task or interactive.
- **Instagram** — Claude-in-Chrome browsing only. No trend-discovery API exists (confirmed 2026-07-30: the Graph API's Hashtag Search only returns posts for an already-known hashtag, capped at 30/week, and requires the same Page↔IG Business-account link already blocking Instagram posting automation, see the Instagram/Meta blocker elsewhere in this doc's history). Treat as the weakest, supplementary signal — if browser automation isn't reliably available inside the unattended weekly scheduled task, skip Instagram that week and say so in the run summary rather than failing the whole run.

**Weekly scheduled task:** `koolestpro-trend-radar-weekly`, timed just before `koolestpro-tips-weekly` (which runs Fridays ~09:28) so its output is ready in time. Writes to `trend-radar-log.json` (Layer 1 — the ranked/picked Tips topic, keyed by ISO week) and, only when something clears the bar, appends a new finding into `content_pipeline.html`'s `format-radar-data` script block (Layer 2 — never overwrites an existing finding's review status, dedupe by `id`). Spend is tracked in `trend-radar-spend-ledger.json`, checked BEFORE every paid call, not after.

**How `koolestpro-tips-weekly` consumes this:** its Step 1 checks `trend-radar-log.json`'s latest `weeks[]` entry. If its `week` key matches the current ISO week and it has a `pickedTopic`, that topic is used (auto-picked, no separate approval gate on the topic itself — Ridwan still reviews the finished carousel same as always). If the log is missing, stale (wrong week), or `pickedTopic` is null (nothing cleared the relevance bar that week), Tips falls back to its original backlog-first logic unchanged. This makes the fallback automatic and safe even before Reddit/Instagram are fully live.

**Format Radar review, in `content_pipeline.html`:** a flagged card appears above the tab bar only when `state.formatRadar` has an entry with `status: "new"`. Silence most weeks is expected, not a bug. Ridwan can mark a finding "tried" or "dismiss" it from the card itself — that status change is local (browser `localStorage`) only, matching how this file already handles other in-browser state; it is not written back into the HTML file by the browser. If a dismiss/tried status needs to be durable across devices/sessions, a future pass would need `inject_format_radar.py` (or a sibling script) to read `localStorage`'s export and reconcile it back into the file — not built as of 2026-07-30, since Ridwan reviews from one machine today.

**`koolestpro-idea-expander` (Skill F) note:** its old Phase 2 (mandatory generic web-search research) is superseded by this engine for anything Tips-related — prefer reading `trend-radar-log.json` over re-running that skill's own web search when the request is about what's trending. `koolestpro-idea-expander` remains useful standalone for non-trend-driven ideation (a specific starting point/framework Ridwan hands it directly).

**Reference implementation:** `.ai-workflow/skills/koolestpro-trend-radar/scripts/` — `x_search.py`, `reddit_search.py` (stub), `relevance_filter.py`, `budget_ledger.py`, `inject_format_radar.py`, `write_topic_log.py`. All tested standalone (compiles, dry-run injection against a copy of `content_pipeline.html` verified additive/dedupe/div-balance) as of 2026-07-30; not yet run for real against live X/Reddit data pending `X_BEARER_TOKEN` and a Reddit provider.

---

## 👤 RIDWAN'S BRAND PHOTOS (CLOUDINARY — MANDATORY)

NEVER use local relative paths. Local paths break html2canvas. Always use Cloudinary URLs.

| Use | URL |
|---|---|
| LK header + serious CTA | `https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss` |
| Smiling / warmer CTA | `https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2` |

**LK Frame Header (42px):**
```html
<div class="lk-av">
  <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss"
       style="width:100%;height:100%;object-fit:cover;border-radius:50%;"
       onerror="this.style.display='none'">
</div>
```

**CTA Slide Avatar (180px with border ring):**
```html
<div style="width:180px;height:180px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">
  <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2"
       style="width:100%;height:100%;object-fit:cover;object-position:center top;"
       onerror="this.style.display='none'">
</div>
```

---

## 🔎 BrowserAct Data API — Lead-Gen Scraping (added 2026-08-11, scoped, not yet live)

Ridwan flagged a LinkedIn promo post for BrowserAct (no-code AI web scraper) and asked to wire it into the outbound/lead-gen track. Checked the Cowork connector registry (`mcp-registry`) — no official BrowserAct MCP connector exists there as of 2026-08-11. There are two real integration paths BrowserAct itself documents; this project uses the first:

1. **Data API (in use):** REST API at `api.browseract.com`, Bearer-token auth, workflow-based — build/publish a scraping workflow in their console (or clone a template like their Google Maps one), get a `workflow_id`, then trigger runs via `POST /v2/workflow/run-task` and read results by polling `get-task-status`/`get-task` or via webhook. Billed pay-as-you-go credits, ~$0.003/workflow step. This is the same integration shape already used for DeepSeek in this project (key in `.env`, called via a wrapper script from bash) — no new architecture pattern introduced.
2. **`browser-act` CLI skill (not used here, noted for reference):** a free, open-source agent skill (github.com/browser-act/skills) for live/interactive browser control from a shell-command-capable agent. Mostly free (proxies and >5 stealth browsers are the only paid parts). Not adopted for this project because the Data API's publish-once/call-many workflow model fits a recurring lead-gen pipeline better than interactive browsing does — revisit only if a use case needs live/logged-in browsing Claude-in-Chrome can't already cover.

**Wrapper script:** `.ai-workflow/tools/browseract_client.py` — `run`/`status`/`result` subcommands, mirrors the pattern of this project's other API wrapper scripts. Reads `BROWSERACT_API_KEY` from `.env` (placeholder line added, currently blank — Claude cannot create the BrowserAct account or enter payment details, that's Ridwan's step).

**Setup still needed from Ridwan before this goes live:**
1. Sign up at browseract.com (free trial, no card required to start).
2. Build/publish a lead-gen workflow in their console and note its `workflow_id` — a Google Maps-style local-business template is the fastest start for the Nigeria-market segment; a custom "Shopify store running ads" workflow would fit the international segment better and would need to be built from scratch in their workflow builder.
3. Grab the API key from the console's Integrations page.
4. Hand both to Claude to fill in `.env`'s `BROWSERACT_API_KEY` / `BROWSERACT_LEADGEN_WORKFLOW_ID`.

**First integration target (Ridwan's choice, 2026-08-11): cold outreach / lead gen, not trend-radar.**

⚠️ **This paragraph is superseded — kept only as history. Do not follow it.** The original plan here was to map BrowserAct output into `targets_pool.json`'s `recordSchema` and it explicitly said "don't invent a parallel leads file," citing the 2026-08-02 one-pool rule. Both halves of that are dead: the very next section below ("Why this data does NOT go into `targets_pool.json`") reversed it the same day once real output showed no website URL comes back, and the 2026-08-02 rule it cited was itself rewritten on 2026-09-04 (see rule 4 at the top of this file). Maps/Ad Library leads go to **KoolestFlow**, never to `targets_pool.json`. Read the next section and rule 4, not this paragraph.

The trend-radar Instagram layer (`koolestpro-trend-radar`'s documented weak point) is a plausible second use for BrowserAct but is explicitly deferred until the lead-gen path is proven.

**LIVE as of 2026-08-11 — first real run completed end to end.** Ridwan signed up, cloned the "Google Maps Scraper" template into his own workflow (`workflow_id 112089423433150347`, published — unpublished workflows fail `run-task` with `"This app not published"`, publish from the workflow's own Build tab via Publish → Publish as New Version, this is separate from the 48-hour Creator-marketplace review process which is for public template publishing, not needed here), generated an API key, and a live test run (task `112090362967777163`, Area=Lagos, Keyword="skincare shop", datalimit=5) returned 5 real business leads at 55 credits (~$0.18).

**Why this data does NOT go into `targets_pool.json`:** the Google Maps Scraper template returns `name, full_address, star_rating, review_count, avg_price_per_person` — no website URL. `targets_pool.json`'s schema assumes every target has a `url` worth auditing (it feeds CRO fixes, static ads, and template showcases, all of which need a real page). Local businesses like these don't have one. Ridwan chose (2026-08-11, asked directly) to route this data into a new, separate, lighter file instead of force-fitting it or blocking on building a different Shopify-specific workflow first.

**`dm_leads_pool.json`** (new file, project root) is that destination — a lead list for the Nigeria-market DM outreach track specifically (businesses with no storefront, sold via Instagram/TikTok DM, matches `docs/koolestpro-growth-operating-plan.md`'s Nigeria/Africa track). Full schema is in the file's own `meta.recordSchema`. Two things worth knowing before using it:
- **Every lead starts at `status: "NeedsContactInfo"`, not `"Available"`.** The Google Maps template gives no Instagram handle or phone number — someone (Claude or Ridwan) has to look the business up before it's actually DM-able. Don't skip this step and DM blind off a business name alone.
- `leadPotential` is a placeholder heuristic (rating/review-count thresholds), not validated against real conversions yet — treat it as a rough sort order, not a scoring system to trust.

**`.ai-workflow/tools/ingest_browseract_leads.py`** pulls a finished task's CSV output (via `get_task`'s `output.files[0]` presigned S3 URL) and merges it into `dm_leads_pool.json`, deduping on a normalized `businessName + address` key so re-running against the same task, or a re-scrape that resurfaces the same business, doesn't create duplicates. Usage: `python3 .ai-workflow/tools/ingest_browseract_leads.py --task-id <id>`.

**API shape notes, learned from live testing, not guessed from docs alone:** `input_parameters` must be an array of `{"name":..., "value":...}` objects matching the workflow's exact declared parameter names — `browseract_client.py`'s `run_task()` accepts a flat `{"name": "value"}` dict for convenience and converts it internally. `get-task-status`/`get-task` take a `task_id` query param, not `id` (the OpenAPI examples in some doc pages are inconsistent about this — verified against the actual live response, not assumed). A `finished` task's real output lives at `output.files[]` (presigned S3 URLs, expire in ~1 hour per `files_expires_at`) — `output.string` was empty for the Google Maps workflow, but IS populated (as a JSON string) for the Contact Finder workflow below — don't assume either field is always the one that's populated, check both.

### ⚠️⚠️ SCOPE EXPANDED 2026-08-11 PM — universal 2-workflow pipeline feeding KoolestFlow directly, not just Koolestpro

Ridwan clarified the same day that the lead-gen system needs to be: (1) not Nigeria-specific — global, any niche/city; (2) feeding a **qualification** step ("has real presence but weak execution" — the free-rebrand-template motion, where he already has per-industry templates he reskins with the prospect's branding/products/logo); (3) landing directly in **KoolestFlow** (`https://cold-dm-app.vercel.app`, password in `.env`'s `KOOLESTFLOW_APP_PASSWORD`) — the "cold-dm-app" repo (mounted separately as `cold-email-app` in this session), which is his own outreach OS with a live Python backend API, SQLite-backed prospect store, Notion two-way sync, and AI message generation. Not a Koolestpro-only tool — replaces manual Notion entry as KoolestFlow's lead-gen source. "Order co-op" in his original message was a speech-to-text mishap for "other Cowork [projects]" — he wants the BrowserAct scripts portable across his projects in principle, though the only concrete other one named (abuzayd-islamic-content, Facebook content) isn't a lead-gen use case and isn't being wired up now.

**Two BrowserAct workflows chained, not one:**
1. **Discovery — Google Maps Scraper** (`workflow_id 112089423433150347`, unchanged from the first integration pass above). `Area` + `Keyword` are free text — works for any city/niche worldwide, this was never actually Nigeria-locked, just tested there first.
2. **Enrichment — Google Business Contact Finder** (`workflow_id 112098855747914891`, cloned+published 2026-08-11 from BrowserAct's official template `89720224238575367`). Input is just `Company_name`; output is the official website URL plus every social profile found (Instagram, Facebook, LinkedIn, TikTok, X, YouTube) and any phone/email on the site — universal by design, works for any business name in any country. This is what fills the `instagramHandle`/website gap the Google Maps template alone can't.

**Qualification logic (`score_and_qualify()` in the bridge script) intentionally scores "real presence + no website" HIGHEST**, not lowest — that combination (Google Maps reviews or an active social profile, but Contact Finder finds no real website) is exactly Ridwan's stated criterion and the ideal candidate for the free-template-giveaway motion. A business that already has a real website scores lower for this particular play (still logged, just not the priority).

**Scoring/status conventions were pulled from KoolestFlow's own `backend/lead_engine.py`, not invented** — `fit_score` 0-100, `confidence` high(>=80)/medium(>=60)/low, `status` "Qualified" at >=60 else "Needs Review", `pipeline_stage` "First Message Ready" at >=60 else "New". Leads pushed by this bridge score consistent with leads KoolestFlow's own built-in search engine would produce.

**`.ai-workflow/tools/browseract_koolestflow_bridge.py`** is the full pipeline: discovery → enrichment → score → push. `push_to_koolestflow()` always does `GET /api/state` first, dedupes new prospects against existing ones by normalized `brand_name + city`, then `POST /api/state` with the full merged list — KoolestFlow's `save_state()` replaces the whole prospects table with whatever gets posted, so never post just the new batch alone. Verified end-to-end 2026-08-11: Blackhills Cosmetics (real website found, 85 fit_score, "Qualified"/"First Message Ready") is now a live prospect in KoolestFlow, pushed via this exact script.

**Known execution constraint:** each enrichment call takes ~1-2 minutes end to end (poll included), so a batch of more than 1-2 leads run through Claude's own sandboxed bash tool will exceed its ~45s per-command ceiling if driven as one continuous script invocation from chat. For real batches, run the script directly in a normal terminal (`python3 .ai-workflow/tools/browseract_koolestflow_bridge.py --area "..." --keyword "..." --limit N`) where there's no such ceiling — proven correct on 1 lead from inside Cowork, but larger runs are Ridwan's terminal's job, not Claude's chat loop.

### ⚠️⚠️ CONFIRMED BUG 2026-09-01 — the Vercel KoolestFlow deployment silently discards pushes

The weekly run pushes to `KOOLESTFLOW_BASE_URL` (`https://cold-dm-app.vercel.app`). That endpoint **accepts `POST /api/state`, returns success, and prints a truthful-looking `Pushed N new prospect(s) to KoolestFlow. Total prospects now: N.`** — but a follow-up `GET /api/state` returns **0 prospects**. Verified live on 2026-09-01: 5 Lekki fashion-boutique leads pushed, dashboard showed nothing, re-read confirmed an empty list. The serverless filesystem is ephemeral, so a SQLite write lands in one lambda's `/tmp` and is gone by the next request.

**The push-succeeded log line is not proof.** Never report a run as successful on the strength of that line alone — read the state back and check the count. `push_prospects_file.py` now does this automatically and exits non-zero when the state reads back empty.

**Ridwan's real prospect data lives on the LOCAL instance** (`KOOLESTFLOW_LOCAL_BASE_URL`, `http://127.0.0.1:8787`, frontend on `:5173`). Every earlier BrowserAct/Ad Library push that appears to have "worked" went there, run from his own terminal.

**This breaks unattended automation, and no script change fixes it.** The cloud sandbox a scheduled task runs in cannot reach `127.0.0.1` on Ridwan's Mac. Either KoolestFlow gets a persistent backend the cloud can write to (Postgres/Turso/Supabase behind the Vercel app — the Supabase connector is already configured in this session), or the weekly lead-gen run stops being a scheduled cloud task and becomes a command Ridwan runs locally. Until one of those happens, expect every scheduled run to score leads correctly and then drop them.

### ✅ RESOLVED 2026-09-01 — the hybrid pipeline (Ridwan's choice)

Ridwan picked "cloud scores, Mac imports" over migrating KoolestFlow to a persistent cloud backend. Both weekly lead-gen tasks now score in the cloud, write to a queue file, and let his Mac do the actual push.

| Piece | File | Runs where |
|---|---|---|
| BrowserAct/Maps runner (resumable) | `.ai-workflow/tools/leadgen_run.py` | cloud scheduled task, Tuesdays |
| Ad Library bridge, `--queue` flag | `.ai-workflow/tools/ad_library_koolestflow_bridge.py` | cloud scheduled task, Wednesdays |
| Queue directory | `.ai-workflow/pending-push/*.json` | on disk |
| Importer | `.ai-workflow/tools/import_pending_push.sh` | Ridwan's Mac, launchd every 30 min |
| launchd job | `.ai-workflow/com.koolestpro.leadgen-import.plist` | `~/Library/LaunchAgents/` |

**Why `leadgen_run.py` exists rather than calling the bridge.** Two hard sandbox limits, both discovered the hard way on 2026-09-01: a cloud bash call is killed near **178 seconds** (not the ~45s quoted elsewhere in this file, and not the 8-9 minutes the old task prompt assumed), and **background processes do not survive between calls** — each call gets a fresh PID namespace, so `nohup ... &` is silently reaped and `pgrep -f <pattern>` matches the polling command's own command line, reporting a dead process as alive. One enrichment can exceed both limits. `leadgen_run.py` checkpoints to `.leadgen-state.json` after every step and prints `RUN_PAUSED` / `RUN_COMPLETE`; the task calls it repeatedly. Expect 8-20 calls per run.

**Ledger ownership moved.** The cloud run only *reads* the ledger, to skip already-taken brands before spending an enrichment credit. Only the Mac importer *writes* it, and only after a verified push. This is what stops a failed push from burning brands.

**`push_to_koolestflow()` now verifies.** It re-reads state after posting and refuses to update the ledger if the count comes back short. Useful, but not a guarantee: if the same warm lambda serves both the POST and the read-back it still answers correctly (measured — immediate read said 5, a read minutes later said 0). Treat a pass as "not obviously broken", not "durable".

**Recovery path when a run is stranded:** scored prospects get written to `.ai-workflow/pending-push/{week}_{slug}.json`, then re-pushed with `python3 .ai-workflow/tools/push_prospects_file.py <file> --ignore-ledger` from Ridwan's terminal with the local backend running. This skips discovery and enrichment entirely, so no BrowserAct credits are re-spent. `--ignore-ledger` is required because the failed push already wrote all 5 brands into `taken-brands-ledger.json`; the flag bypasses the skip check for that one push using a scratch ledger and leaves the real history untouched.

**`dm_leads_pool.json` is now a staging/historical log, not the destination.** It predates discovering KoolestFlow as the real target (same session, earlier). Its remaining `NeedsContactInfo` entries can be run through the bridge with `--from-dm-leads-pool` to graduate them into KoolestFlow.

---

## 📱 TIKTOK DRAFTS + INSTAGRAM PUBLISHING (added 2026-09-07/08)

Both streams moved from blocked to buildable in one session. The two blockers recorded
across `project_tiktok_app_rejected` and `project_instagram_automation_blocked` were
resolved differently: one was answered by testing, the other turned out to be obsolete.

### TikTok — inbox drafts, LIVE, no production review needed

The open question from the 2026-09-04 disposition ("does inbox-only drafting need
production app review at all?") is **answered: no.** Verified live 2026-09-07 by
refreshing the sandbox token and running an inbox init successfully. Scope is
`user.info.basic,video.upload`; refresh token good ~338 more days.
`creator_info/query` returning `scope_not_authorized` is correct and expected, because
that endpoint belongs to `video.publish` (direct post), which is deliberately not held.

**Never auto-publish to TikTok.** `/inbox/video/init/` is the only publish endpoint this
project may call. Videos land in Ridwan's draft inbox and he posts them by hand.

| Tool | Job |
|---|---|
| `.ai-workflow/tools/tiktok_push_draft.py` | pushes a video to the draft inbox; refreshes the token every run and writes the rotated pair back into `.env` atomically, so a scheduled run can never fail on the 24h expiry; logs to `outputs/tiktok-drafts-log.json` and skips an already-drafted file unless `--force`; `--check` verifies scope without uploading |
| `.ai-workflow/tools/build_tiktok_video.py` | builds the 1080x1920 video |
| `.ai-workflow/tiktok-weekly-procedure.md` | the procedure `koolestpro-tiktok-weekly` (Thursdays ~09:11) follows |

**The old prototypes are gone.** `build_v3.py`, `waypoint_scroll_capture.py`,
`select_bg_music.py` and `outputs/tiktok_mockup/` no longer exist in this project;
only the docs and memory still reference them. Do not go hunting. `build_tiktok_video.py`
rebuilds the one format that actually produced clients (the silent "watch a store get
built" scroll video) by reusing `scroll_video_raw.py` and `frame_video.py mobile` at a
1080x1920 canvas, then burning in a hook card, handle chip and CTA end card.

**Rotation is independent.** `replo-rebuilds-pages.json` gained `usedForTikTok` /
`usedForTikTokDate` on every entry. A page already used for Template Showcase is still
eligible here: different format, different platform. Only `usedForTikTok` gates it.

**`assets/fonts/` is new** — Syne (variable) and DM Mono, so burned-in video copy uses the
real brand faces instead of Liberation Sans. Reusable anywhere else that needs a TTF.

**`--duration` is a floor, not a promise.** The capture is externally stepped, so a heavy
page overruns it: 10 was requested on the first real build and 26.4s came out. Read the
duration the script prints rather than assuming.

### Instagram — the Page↔IG blocker is OBSOLETE, not unresolved

Meta's **Instagram API with Instagram Login** (live since July 2024) publishes to a
professional Instagram account with **no Facebook Page required at all**. Meta's own docs
state it: "This API setup does not require a Facebook Page to be linked to the Instagram
professional account." Every attempt from 2026-07-22 onward was fighting a requirement
that had already been removed.

**Do not resume Business Suite / Account Quality debugging.** That whole line of
investigation is dead.

**A new app was needed.** `Koolestpro Automation` (`997611516603591`) is App type **None**,
so Meta only offers it the legacy Facebook-login *Instagram Graph API* product, and the
type cannot be converted. Ridwan approved creating a second app on 2026-09-07; the old app
is untouched and still owns the Facebook branch.

| Field | Value |
|---|---|
| Meta app | **Koolestpro Publishing**, `1094745286417525` |
| Instagram app ID | `930775432950893` |
| Redirect URI | `https://koolestpro-portfolio.vercel.app/oauth-callback/` |
| Permissions | `instagram_business_basic` + `instagram_business_content_publish`, both "Ready for testing" |
| Business portfolio | none attached, deliberately (the old portfolio carries the ad-policy restriction) |
| `@koolestpro` | added as Instagram Tester |

**Two details that are easy to get wrong:**

1. The default permission set on that setup page is `instagram_business_basic` /
   `_manage_comments` / `_manage_messages`. Publishing needs
   **`instagram_business_content_publish`**, which is not among them and must be added
   separately from Permissions and features.
2. Endpoints are on **`graph.instagram.com`**, not `graph.facebook.com`. Anything still
   pointing at the latter is the old, blocked path. Verified by testing: the same token
   returns `400 "Cannot parse access token"` on `graph.facebook.com` and `200` on
   `graph.instagram.com`.

**DONE 2026-09-08 — the Make branch is rewired and live.** Modules **301, 302, 304, 306**
in scenario 6565331 now call `https://graph.instagram.com/v20.0/{{2.instagram_business_account_id}}/media`
and `/media_publish` with `{{2.instagram_page_access_token}}`. The two-call structure, the
Reels processing sleep and the "Posted" row update are unchanged, and the Facebook branch
(modules 400-406) still points at `graph.facebook.com` with `meta_page_access_token`, which
is correct and deliberate.

**The version stayed at v20.0 on purpose.** v20 through v23 all return 200 on
`graph.instagram.com`, so only the host word changed. That matters for a practical reason:
Make's URL field treats a typed `/` as a variable-search trigger and silently drops it when
the popup is dismissed, so retyping a whole URL corrupts it. Double-click the word
`facebook` and type `instagram` instead. Also note `Escape` closes the whole module dialog
and discards every edit in it; dismiss the variable picker by clicking the dialog title.

**A real bug was caught during verification, and it would have broken this within hours.**
Module **201**, the datastore write that runs after every X token refresh, listed ten
fields and `instagram_page_access_token` was not among them, so the next X refresh would
have blanked the Instagram token. This is the same failure this module was patched for once
before. It now passes the field through. **Any future field added to `koolestpro-config`
must be added to module 201 at the same time**, or it will survive only until the next X
refresh.

**Reading the blueprint:** `scenarios_get` on this scenario returns ~88KB. When it lands as
escaped JSON inside a `.json` wrapper it is one 78k-token line and cannot be read or
patched at all; when it lands as a `.txt` it is greppable, which is the only practical way
to verify an edit. Either way `scenarios_update` replaces the whole blueprint, so UI edits
plus a grep to confirm is the safe pattern.

### ⚠️⚠️ CONFIRMED BUG 2026-09-08 — Instagram has no carousel route, multi-image rows 400

First real Instagram post (a 7-slide Tips carousel, `idea-mobile-thumb-zone-7-tap-target-
fails-...-20260908-ig-1200`) errored with `400 Bad Request` on execution
`ddef648826f34f9f9c81fdb26c91a31c`. Root cause, confirmed by reading modules 301/302 in the
saved blueprint: module 301's filter only checks whether `{{1.\`15\`}}` (asset_urls) ends
with `.png`/`.jpg`/`.jpeg`, then posts that ENTIRE string as a single `image_url` form field
to `/media`. There is no carousel branch — only single-image (301/302) and single-video/Reel
(304/306) routes exist. A multi-image Instagram row (asset_urls = several Cloudinary URLs
joined with `"; "`) still matches the ".png" filter because the *last* URL in the string
ends that way, so Make POSTs the whole semicolon-joined string as one malformed `image_url`
and Instagram's Graph API correctly rejects it with 400.

**Fix applied 2026-09-08 (stopgap, not real carousel support):**
- `.ai-workflow/tools/feed_media.py` now writes only the FIRST (cover) image URL into
  `asset_urls` for any Instagram row with more than one non-video image, instead of joining
  all of them. Twitter is unaffected (it has no equivalent single-image-only Make branch).
- All 17 Instagram rows already sitting in the live Sheet with multi-URL `asset_urls`
  (rows for dates 2026-09-02 through 2026-09-21) were patched the same way via a direct
  Sheets API `values:batchUpdate` call — each now points at its cover image only.
- The `koolestpro-distribution-health-check` task now has a permanent Step 1c that checks
  for and fixes this pattern going forward (see that task's SKILL.md).

**This is a real content-format compromise, not a full fix** — these posts now go out to
Instagram as a single image instead of a swipeable multi-slide carousel. Real Instagram
carousel support (per-image child media containers with `is_carousel_item: true`, then a
parent container with `media_type: CAROUSEL` and `children`, then `/media_publish` on the
parent) does not exist in this scenario yet and was deliberately NOT built blind via
`scenarios_update` (see the blueprint-editing caution above — this module 301/302 area is
exactly the kind of edit that rule exists for). Building real carousel support is a
follow-up that needs either Ridwan doing it in the Make UI himself (Claude has no logged-in
Make session and does not enter his credentials, per this project's standing security
rule) or a dedicated session where he reviews the diff before it's saved.

### ⚠️⚠️ CONFIRMED BUG 2026-09-08 — reschedule webhook scenario can go inactive silently

The "Distribution Queue Reschedule" webhook scenario (id 7111659) was found deactivated
(`scenarioIsActive: false`) during the same 2026-09-08 session. The webhook itself still
returned HTTP 200 / `Accepted` for every call and queued the requests (`queueCount` climbed
to 11), but nothing in the Sheet actually changed until the scenario was reactivated via
`scenarios_activate`. 9 Instagram reschedule calls silently no-op'd this way before the
issue was caught by re-reading the rows afterward — a routine step that had not previously
been treated as mandatory. **A 200 response from this webhook is not proof a reschedule
landed.** Always re-read the affected row(s) after calling it. The health-check task now
checks and reactivates this scenario as the first line of its Step 2, every run.

### 📱 Instagram is now IN SCOPE for `koolestpro-distribution-health-check` (2026-09-08)

This reverses the 2026-08-27 "Instagram is out of scope" rule that lived in that task's own
SKILL.md — Instagram posting went live 2026-09-08, so there's now something real to watch.
Instagram rows are classified Posted/Missed/Upcoming/Blocked and checked for same-platform
slot collisions exactly like Twitter (no LinkedIn-style daily cap applies to it).

`.ai-workflow/tools/instagram_client.py` handles the auth flow and can publish directly:
`auth-url`, `exchange <code>`, `refresh`, `me`, `publish`. Long-lived tokens last 60 days
and refresh with a single GET; `refresh` is safe to run on any schedule, since Meta
declining a refresh on a token under 24h old is reported rather than treated as a failure.
Fold that call into `koolestpro-distribution-health-check` rather than building a separate
task, so the token can never silently lapse.

### `bootstrap_env.sh` was rewritten 2026-09-08, and the reasons matter

A cold sandbox exposed two real failures that each cost several wasted bash calls:

1. **`python3 -m playwright install` is not resumable.** Every attempt restarts the 195MB
   download from zero and gets killed by the command ceiling around 40-60%, forever. It now
   downloads the build zips directly with `wget -c`, which genuinely resumes across calls.
2. **Browsers must not live in `~/.cache`.** That is on `/sessions`, a ~9.8GB volume mostly
   consumed by the mounted project; extracting chromium there filled it to 100% and broke
   the rest of the run. The script now sets `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers`,
   which is on a roomier volume.

Both chromium builds are required: headless launches use `headless_shell` while video
recording needs the full build, and installing only one fails at launch with a misleading
"Executable doesn't exist" pointing at the other. Warm start is ~1s.


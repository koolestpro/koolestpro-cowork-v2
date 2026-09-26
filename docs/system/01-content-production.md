# 01 — Content Production

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

Turning either a topic or a target brand into a finished, reviewable post package: the HTML, the exported images, and the ready-to-post captions. It stops at review. It never posts anything and never sets a pipeline record to `Published`.

This is the oldest part of the project and the only channel with proven client attribution behind it. Six clients trace to content, none to outbound.

---

## What is in it

**Four weekly generator streams**, each an unattended scheduled task producing buffer content days before it is needed:

| Stream | Task | Runs | Output |
|---|---|---|---|
| Tips carousel | `koolestpro-tips-weekly` | Fri ~09:28 | `outputs/tips/` |
| Static Ad | `koolestpro-static-ad-weekly` | Fri ~09:04 | `outputs/static-ads/{slug}_{date}/index.html` |
| Template Showcase | `koolestpro-template-showcase-weekly` | Sat ~09:09 | `outputs/templates/{slug}_{date}/index.html` |
| CRO Fix | `koolestpro-weekly-cro-fix` | Sun ~09:12 | `outputs/cro-fixes/{slug}_content.html` |

**A fifth, disabled:** `koolestpro-trend-radar-weekly` (Fri ~08:51). See "What is stopped" below.

**Source of truth:** `ridwan_content_system_updated.html`, whose `<script id="cowork-sync-data">` block holds `SYNC_DATA` with `meta`, `months` and `items`. Every finished package registers one item there. `content_pipeline.html` is the browser view over it.

**Skills that do the work:** `koolestpro-content-engine` (carousels and captions), `koolestpro-store-auditor-skill-a` (audit), `koolestpro-store-rebuilder-skill-b` (rebuild), `koolestpro-cro-caption-writer-skill-d`, `koolestpro-cro-content-maker-skill-e`, `koolestpro-idea-expander`, `static-ad-image`, `page-presentation-kit`, `humanizer`.

**Reference outputs** that new builds are matched against, not invented from:

- Tips: **old-style format, `docs/system/tips-old-style-format.md` (2026-09-18)**; `outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html` is now the export-mechanics reference only
- Static Ad: `outputs/static-ads/obvi_super-collagen-protein_20260711/`
- The older `outputs/tips/funnel-awareness-framework_2026-05-10.html` still governs the underlying geometry and JS

---

## How it works

**Topic-driven streams (Tips) pick a subject.** Three-tier fallback: this week's trend-radar pick, then the `status: "Idea"` backlog in `SYNC_DATA.items`, then a fresh topic from the content-engine pillars. Tier one has never fired.

**Target-driven streams (CRO Fix, Static Ad, Template Showcase) pick a brand.** CRO Fix and Static Ad select from `targets_pool.json`, preferring targets with no `usedFor` entry for that stream. Template Showcase selects from `replo-rebuilds-pages.json` where `active: true` and `usedForTemplateShowcase: false`, lowest `sortOrder` first.

**Then, in every stream:** Claude decides angle, format and copy and authors the HTML itself (region-swap script for Tips where one exists; otherwise Claude writes the file directly, per the "AI Workflow Architecture" rule in the parent `CLAUDE.md`; CRO Fix rebuilds and redesigns are built in an external page builder (Lovable/Figma Make/Claude Design/v0), kept private, and captured); images are exported by driving the page's own `html2canvas` capture functions headlessly rather than taking a browser screenshot; the exports are looked at; a record is registered at status `Created`; and the brand's `{brand}-social-content.json`/`.md` pair is updated.

**Why the export detail matters:** html2canvas renders gradients, blur and SVG differently from a native screenshot. An export that did not go through the page's own capture function is not a valid deliverable. `export_tip_slides.py` and `export_static_images.py` exist so nobody hand-rolls this.

---

## State

**Live and running:** all four generator streams. `SYNC_DATA` currently holds 65 items across 5 months — 36 `Idea`, 27 `Created`, 2 `Ready`, and by design zero `Published` (that status is only ever reached through the distribution chain). By type: 20 Tip, 17 CRO Fix, 8 Case Study, 8 Personal, 8 Template Showcase, 4 Static Ad.

**Stopped: trend radar.** Disabled since 2026-08-14. Two live runs, both wrote `pickedTopic: null`. Three independent blockers, none of them a bug in the skill: the X API tier available sorts by recency not popularity and rejects engagement operators like `min_faves:`; Reddit is live via Apify but the actor takes 25-180s against a ~178s cloud ceiling; Instagram needs an interactive browser pick an unattended run cannot answer. **Decided 2026-09-04:** move the run to Ridwan's Mac and add an approval gate where he picks from 3-5 ranked candidates. See `docs/koolestpro-system-restructure-plan.md` Step 5b.

**Consequence worth naming:** because tier one has never fired, every Tips carousel for six weeks has come from the April/May backlog. That backlog is finite. 36 `Idea` items remain.

**Blocked: image generation.** gpt-image returns `429 credit_balance_exhausted` on both keys, and Cloudinary's free AI quota is spent. The standing protocol is a prompt-pack handoff, not a substitute renderer. Ridwan runs the prompts through ChatGPT manually and sends the exports back.

---

## Rules

The full versions live in `CLAUDE.md`. This is what they are and where to find them.

| Rule | Section in `CLAUDE.md` |
|---|---|
| Tips geometry: 540×680 portrait, scale 2, mandatory chrome-hiding | "Tips Carousel — Corrected Gold Standard Spec" |
| Type floor: 15px body, nothing under 12px unless an uppercase label | "TYPE SCALE — HARD FLOOR" |
| Density: headline-only plus one micro subline, 7 slides default | "V2 Density + Visual Variety Format" |
| Cover must carry a real dominant visual, never pure typography | "CAROUSEL COVERS, EVIDENCE SLIDES…" #1 |
| The CRO 3-slide carousel IS the before/after (slide 2) and the annotation (slide 3), both standalone | "STANDING HARD RULES" #2 + `docs/system/cro-3-slide-carousel-format.md` |
| CRO rebuilds reach the redesign quality bar (whole decision on the first screen) | `docs/system/cro-redesign-standard.md` + "STANDING HARD RULES" #12 |
| CRO headlines: one #1 finding, a different angle per surface, max 2 lines | `docs/system/cro-headline-system.md` + "STANDING HARD RULES" #11 |
| Never recreate a brand's logo, including wordmarks | "REAL BRAND ASSETS ONLY" |
| No gradient text, CSS or SVG. Solid colours only | "GRADIENT SYSTEM" |
| No em dashes; every written output humanized (v3.0, 11 passes) | `docs/system/humanizer-guideline.md` |
| Never auto-publish; status stops at `Created` | "Status Handling" |
| Every output HTML carries the pipeline export button | "PIPELINE EXPORT BUTTON" |
| Present the built HTML in chat after every build | "SHOW HTML PREVIEWS IN CHAT" |
| Static Ads default to a prompt pack (API only on request); other streams: gpt-image → Cloudinary → prompt pack. Register nothing until images exist | "NO IMAGE CREDITS" |

---

## Known gaps

- **Trend radar has never delivered.** Six weeks of Tips off a finite backlog is the real cost.
- **`outputs/case-studies/` is empty.** The growth plan's Track B calls for real Nigeria anchor case studies. None exist yet, and case studies are the proof the content CTAs are supposed to point at.
- **A caption can outrun its image.** Some CRO Fix graphics only exist once someone clicks a download button in the review HTML. Check a social-content file's `knownGaps` field before trusting an `assetPath`.
- **DeepSeek is documented as unreliable for Tips carousels specifically** — it drops mandatory sections and invents its own JS. Region-swap is the required method there.

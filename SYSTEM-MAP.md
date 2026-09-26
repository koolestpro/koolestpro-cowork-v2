# Koolestpro System Map

**The inventory.** What exists, where it lives, and where a new thing goes.

Last structural review: 2026-09-13. For live numbers open `SYSTEM-STATUS.html`, which is generated from real files and is the only place that should be trusted for counts, dates and states.

---

## The three documents, and which one to read

This project has three top-level documents and they answer different questions. Reaching for the wrong one is how the same thing gets re-derived twice.

| Document | Answers | Written by |
|---|---|---|
| `CLAUDE.md` | "What are the rules for this one task?" | Live rules plus the **Task Router**; read only the router row that applies, not the whole file. Deliberately slim and kept under a context budget (see [07](docs/system/07-infrastructure.md)). The dated history and "why a rule exists" moved to the archive. |
| `docs/koolestpro-content-operating-plan.md`<br>`docs/koolestpro-growth-operating-plan.md` | "What is the strategy, and what is the sequence?" | Content plan covers Steps 1-11 of production. Growth plan covers Tracks A-G around it. |
| **`SYSTEM-MAP.md`** (this file) | "What exists, what state is it in, and where does a new thing go?" | The inventory. Links out to the other two rather than restating them. |

`SYSTEM-STATUS.html` is the fourth surface and it is generated, never hand-edited. Every number in it traces to a file.

---

## The seven sub-projects

Cut by function, because that is how the files and the scheduled tasks already cluster. Each has its own doc under `docs/system/`.

| # | Sub-project | One line | Doc |
|---|---|---|---|
| 1 | **Content Production** | Turns a topic or a target brand into finished, reviewable post packages | [`01-content-production.md`](docs/system/01-content-production.md) |
| 2 | **Distribution** | Takes finished packages and gets them posted on a schedule | [`02-distribution.md`](docs/system/02-distribution.md) |
| 3 | **Prospect Intelligence** | Finds and qualifies businesses, for content and for outreach | [`03-prospect-intelligence.md`](docs/system/03-prospect-intelligence.md) |
| 4 | **Outbound / KoolestFlow** | Turns a qualified lead into a sent message and a tracked conversation | [`04-outbound.md`](docs/system/04-outbound.md) + [`outreach-playbook.md`](docs/system/outreach-playbook.md) |
| 5 | **Build Assets** | The real pages, templates, mockups and caption libraries the content is made from | [`05-build-assets.md`](docs/system/05-build-assets.md) |
| 6 | **Web Presence** | The destination every CTA points at: domain, site, portfolio, search, ads | [`06-web-presence.md`](docs/system/06-web-presence.md) |
| 7 | **Infrastructure** | The tooling, scheduling, credentials and sandbox limits everything else runs on | [`07-infrastructure.md`](docs/system/07-infrastructure.md) |

---

## How they connect

The system is one chain with two entry points.

```
                    ┌─ 3 Prospect Intelligence ─┐
                    │  (finds businesses)       │
                    └───────────┬───────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
    has an auditable URL                  no site / DM-able
              │                                   │
              ▼                                   ▼
    targets_pool.json                       KoolestFlow
              │                                   │
              ▼                                   ▼
    ┌─ 1 Content Production ─┐          ┌─ 4 Outbound ─┐
    │  built from 5 Build    │          │  a sent DM   │
    │  Assets                │          └──────┬───────┘
    └───────────┬────────────┘                 │
                ▼                              │
    ┌─ 2 Distribution ───────┐                 │
    │  X + LinkedIn, live    │                 │
    └───────────┬────────────┘                 │
                │                              │
                └──────────┬───────────────────┘
                           ▼
                ┌─ 6 Web Presence ─┐
                │  where CTAs land │
                └──────────────────┘

    7 Infrastructure sits under all of it.
```

**The one thing to understand about this chain:** content is the proven channel and outbound is not. Six clients trace to content. Outbound has produced none, because it has never actually been sent. That is a fact about history, not a judgment about the machinery, and `CLAUDE.md` says not to re-derive it.

---

## Where does a new thing go?

Decide from this table rather than from a conversation.

| If you are building… | It belongs to | And lands in |
|---|---|---|
| a new post type, or changing how one is generated | 1 Content Production | a skill or a scheduled task, output to `outputs/{stream}/` |
| anything that decides when or where a finished post goes out | 2 Distribution | `.ai-workflow/tools/` + the Google Sheet |
| a new way of finding businesses | 3 Prospect Intelligence | a bridge script in `.ai-workflow/tools/`, output to KoolestFlow |
| anything about writing or sending the actual outreach message | 4 Outbound | KoolestFlow |
| a real page, a store template, a mockup, or a caption library | 5 Build Assets | `replo-rebuilds/`, `store-templates/`, `{brand}-social-content.*` |
| anything a stranger could visit on the open internet | 6 Web Presence | `site/` |
| a reusable script, a scheduled task, a credential, a spend cap | 7 Infrastructure | `.ai-workflow/` |

**When it fits two:** ask which sub-project would break if this thing disappeared. That one owns it.

**When it fits none:** that is a signal the seven-way cut has a gap. Add an eighth here rather than filing it somewhere it does not belong.

---

## What is stopped, and why

The point of this section is that nothing sits in limbo. Every stream is either being worked on or formally set aside, with a reason. Full detail in `docs/koolestpro-system-restructure-plan.md` Step 5.

| Stream | State | Why |
|---|---|---|
| X + LinkedIn posting | **Live** | Make.com scenario 6565331, healthy |
| Instagram posting | **Blocked, active** | Meta account-level Page↔IG Business link restriction. Not a config problem. Next action is Business Suite Account Quality. |
| TikTok posting | **Blocked, active, route decided** | App review rejected 2026-08-19 over displaying own posts on a website. That scope is now dropped: videos go to the draft inbox, Ridwan posts manually, `video.upload` only. Open question is whether that even needs review. |
| Trend radar | **Disabled, active, route decided** | Never produced a topic pick in two live runs. Moving to Ridwan's Mac, where the 178s cloud ceiling does not apply and Reddit completes. Gains a new approval gate: 3-5 ranked candidates, Ridwan picks. |
| Posting pace | **Behind target** | 3/day is an average floor, not a cap. Clean rate is well under it. Bottleneck is the manual QA gate, not generation. Note LinkedIn's 1/day hard cap means X carries most of the volume. |
| `replo-pages-cache/` | **Retired** | `replo-rebuilds` moved inline 2026-08-31. Relocated to `assets/_archive/replo-pages-cache-retired/` on 2026-09-08, 8 stale July copies. |
| `dm_leads_pool.json` | **Retired as a destination** | Historical staging log. Leads go to KoolestFlow. |
| `build_mosaic.py` | **Retired** | Replaced by `build_split_page.py` 2026-07-29. Kept as history only. |

---

## Standing constraints worth knowing before you build anything

These bite regardless of which sub-project you are in. Full versions in `CLAUDE.md`.

- **A cloud bash call dies near 178 seconds** and background processes do not survive between calls. Anything slower than that has to checkpoint and resume, or run on Ridwan's Mac.
- **Never auto-publish.** Every generator stops at status `Created`. `Published` is only ever set by the real posting step.
- **Never invent a client result**, and never imply a concept brand was a client. KURA, HALOS, MERIDIAN and Lumora are concept builds and must be labelled as such. This is the highest-stakes rule in the project.
- **Never recreate a real brand's logo.** Pull the real file, including wordmark logos.
- **No em dashes in any generated copy**, and run everything through the `humanizer` skill.
- **No gradient text**, CSS or SVG. Solid colours only. It breaks html2canvas export.
- **Verify by looking at the output**, not by reading the markup. This project has been bitten repeatedly by builds that were correct in source and wrong on screen.

---

## 🎯 Current best reference per stream (the bar each new build must beat)

The quality ratchet is enforced at build time (see `CLAUDE.md` → QUALITY RATCHET). This table is the inventory — where the current best actually lives, so you can find it without reading the rulebook. A new output must beat its row here, never merely match it.

| Stream | Current best (bar to beat) | Original seed (never regress below) |
|---|---|---|
| Tips carousel | `outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html` | `outputs/tips/funnel-awareness-framework_2026-05-10.html` |
| CRO Fix rebuild | `outputs/cro-fixes/caraway_fry-pan-pdp_rebuild.html` + `..._content.html` | `templates/eddie_bauer_cro_content_v2 (1).html` + `outputs/cro-fixes/ecobioboutique_cellulite-remover_content.html` |
| CRO 3-slide carousel + standalone posts | `outputs/cro-fixes/caraway_fry-pan-pdp_carousel.html` via `.ai-workflow/build_caraway_carousel.py`, exported `outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_carousel_slide{1,2,3}.png` (slide 2 = before/after post, slide 3 = annotation post) | the old 6-7 slide narrative carousel |
| CRO standalone annotated graphic (clear bg, Q/A) | `outputs/cro-fixes/caraway/koolestpro_caraway_fry-pan-pdp_annotated.png` via `.ai-workflow/build_caraway_annotation.py` | the old clear-background `anno-graphic` (ecobioboutique reference) |
| CRO standalone before/after graphic | **RETIRED 2026-09-10** (slide 2 replaces it; keep only the gradient glow) | — |
| Static Ad | `outputs/static-ads/obvi_super-collagen-protein_20260711/` | same |
| Template Showcase page | `outputs/templates/kura_pdp-01_2026-08-31/index.html` | same |
| Monthly Build Recap | `outputs/cro-fixes/_recap9/koolestpro_monthly-build-recap.png` + `recap-4builds.png` (transparent, autocropped; `fanned_stack_4`, last four builds overlapping; single continuous background) | Ridwan's fanned-overlap reference |
| Page-rebuild capture (Lovable / Figma Make handoff) | `.ai-workflow/tools/capture_page.py` → `outputs/cro-fixes/_capture/<brand>/<brand>-{mobile,full,desktop}.png` | `screenshot.py` (single shot, no pipeline naming) |
| Page-build brief (Lovable / Figma Make input) | `.ai-workflow/tools/build_page_brief.py` + `outputs/cro-fixes/caraway_fry-pan-pdp_build-brief.md` | (new - the rebuild had no input brief before) |
| Redesign tool API / sync integration | `docs/system/redesign-tool-api-integration.md` (bolt.diy, Onlook, v0 API, Lovable GitHub sync, Figma Make) | (new) |

*Set 2026-09-08, every path verified to exist on disk.*

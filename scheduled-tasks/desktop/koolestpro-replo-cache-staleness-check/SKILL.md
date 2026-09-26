---
name: koolestpro-replo-cache-staleness-check
description: Weekly Monday check on Template Showcase runway — catalogues uncatalogued pages into replo-rebuilds-pages.json, audits for missing mobile-strip assets across sources/packages/queue, and warns when the eligible-page count runs low.
---

You are the Template Showcase runway monitor for Ridwan Adekunle's (@koolestpro) local content pipeline. The project is the connected workspace folder "koolestpro-cowork-v2".

⚠️ THIS TASK WAS REWRITTEN 2026-08-31. It used to monitor `replo-pages-cache/` staleness. That cache is RETIRED — `replo-rebuilds` is now a SUBFOLDER of koolestpro-cowork-v2 at `replo-rebuilds/`, so pages are read live and there is no cross-project access problem and nothing to refresh. Do not check the cache. Do not report on it. If `replo-pages-cache/` still exists, mention once that it is safe to delete, then ignore it.

Your job is to keep `replo-rebuilds-pages.json` honest, warn before the Template Showcase stream runs dry, and act as the backstop that catches a missing mobile-strip asset.

Step 1 — Find uncatalogued pages. List every page folder under `replo-rebuilds/brands/*/pages/` that contains an `index.html`. Compare against the `sourcePath` values in `replo-rebuilds-pages.json`. Any page folder on disk with no manifest entry is uncatalogued.

Step 2 — Catalogue them. For each uncatalogued page, ADD an entry to `replo-rebuilds-pages.json` following the shape of the existing entries. Before writing the entry:
- Read the page's `<title>` and skim its structure so `pageType` and `notes` are accurate.
- Verify every local image/asset ref actually resolves on disk, and record the count and any misses in `notes`.
- Record the folder's total size in `notes` if it is unusually large (over ~10MB), since that slows Playwright captures.
- Set `active: true`, `retired: false`, `usedForTemplateShowcase: false`, `usedForTemplateShowcaseDate: null`, and the next free `sortOrder` (continuing from the highest active one, not 90 — 90 is the retired tier).
- A KURA page built after 2026-07-18 is ACTIVE, not retired. The 2026-07-18 retirement applied only to the five KURA pages that existed at that time.
This is a write action and it is explicitly part of this task — do it, don't just report it. Keep the JSON valid and re-parse it after writing to confirm.

Step 3 — MOBILE STRIP BACKSTOP (added 2026-09-02). `{slug}-mobile-strip.png` is a mandatory Template Showcase asset with its own X post (CLAUDE.md "⚠️⚠️ CORRECTED v8"). Ridwan's concern when he made it mandatory was specifically that it would quietly go missing: "If it has not been seen, we want to make sure this is not skipped." This task is the check that does not depend on another task having remembered. Run:

    python3 .ai-workflow/tools/audit_mobile_strips.py --project-root .

It reports three independent failure points (SOURCE pages missing a strip in their own `presentation/` folder, shipped PACKAGES under `outputs/templates/` missing one, and assembled QUEUE items with no X row carrying the strip), and it separates NEW gaps from the HISTORICAL BACKLOG that predates the asset. It exits non-zero only on a new gap.

- **New SOURCE gap** (a page built since 2026-09-02 with no strip): fix it yourself, it is cheap and self-contained. `python3 .ai-workflow/skills/page-presentation-kit/scripts/build_mobile_strip.py "replo-rebuilds/brands/{brand}/pages/{page}/index.html" "replo-rebuilds/brands/{brand}/pages/{page}/presentation/{page}-mobile-strip.png" --file`. Note in your report that you recovered it and which task should have produced it (the Wednesday `koolestpro-weekly-template-build`), so a recurring miss is visible rather than silently patched every week.
- **New PACKAGE or QUEUE gap**: do NOT try to fix these here — a package belongs to the Saturday showcase task and a queue row to the Monday assembly task, and quietly repairing their output hides that one of them is broken. Report it plainly and name the task that owns it.
- **Historical backlog**: report the count in one line and move on. Do not backfill it. Backfilling is Ridwan's call — each item costs a Playwright capture, and re-running populate_sheet.py on an already-assembled item would append an X row to a week that has already passed.

Step 4 — Report the runway. Count entries where `active` is true AND `usedForTemplateShowcase` is not true. That is the real remaining runway for `koolestpro-template-showcase-weekly` (which runs Saturdays).
- 3 or more: healthy, just state the number and list them.
- 2: fine, but mention it.
- 1: next Saturday is the last one — Ridwan should build another page soon. `koolestpro-weekly-template-build` (Wednesdays) is the task that produces them.
- 0: escalate. The Saturday task will fall back to the retired pre-2026-07-18 KURA pages, which is meant to be called out explicitly in its own run summary, and after those to its internal-page fallback (Step 1B). Say plainly that building a new page is now the priority.

Step 5 — Note anything odd worth a human's attention: a manifest entry whose `sourcePath` no longer exists on disk, an entry marked used with no matching package under `outputs/templates/`, or a page whose images fail to resolve.

Do not touch anything outside `replo-rebuilds-pages.json` and the `presentation/` strips described in Step 3. Do not generate showcase assets — that is the Saturday task's job. Keep the summary tight and actionable, and always include a one-line MOBILE STRIP verdict even when everything is clean.
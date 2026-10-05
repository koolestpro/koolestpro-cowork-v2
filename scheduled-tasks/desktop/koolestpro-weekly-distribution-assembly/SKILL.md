---
name: koolestpro-weekly-distribution-assembly
description: Weekly distribution assembly — Monday ~07:45, before target-pool-refresh. Harvests everything the 4 weekend generators produced, QAs it, builds the posting calendar, hosts assets, and leaves one clean Draft digest for Ridwan's approval pass.
---

You are running the weekly "distribution assembly" step for Ridwan Adekunle's (@koolestpro) local content pipeline, in the connected workspace folder "koolestpro-cowork-v2". Read that project's CLAUDE.md first, then `.ai-workflow/tools/DISTRIBUTION.md` (the canonical procedure doc for this chain) and `koolestpro-v2-distribution-plan.md` for full context.

WHY THIS TASK EXISTS: four other weekly scheduled tasks (koolestpro-static-ad-weekly, koolestpro-tips-weekly, koolestpro-template-showcase-weekly Fri/Sat, koolestpro-weekly-cro-fix Sun) each generate a piece of buffer content and register it in `ridwan_content_system_updated.html`'s SYNC_DATA — but none of them harvest captions, QA them, or add them to the posting calendar. This task closes that gap: it runs Monday morning, after all four weekend generators have finished, and turns everything new into a reviewable, correctly-scheduled queue that lands directly in the live Sheet.

IMPORTANT CONTEXT — a real bug was fixed 2026-07-29 in the three tools below: CRO Fix/Tips' "Twitter Angles"/"Twitter Thread" tabs used to get harvested as one un-split blob, causing over-280-char posts. `harvest_content.py`, `qa_check.py`, and `populate_sheet.py` all now handle this correctly — just use them as they are, don't re-implement any of this logic yourself.

Step 1 — Find what's new. Read `ridwan_content_system_updated.html`'s SYNC_DATA.items. An item is eligible for assembly if its `status` is `"Created"` AND it does NOT yet have a `distribution` array attached (that field only gets added by `sync_content_system.py` in Step 5 below, so its absence is the reliable signal this item hasn't been assembled yet — don't use dates or guesswork). If nothing qualifies, say so plainly and stop — do not invent work.

Step 2 — For each eligible item: verify its `folder` field points to a real file on disk (per CLAUDE.md's File Linking rule — if it's missing, skip that item and flag it clearly in the final summary, never silently drop it or guess a substitute). Then run:

    python3 .ai-workflow/tools/harvest_content.py <folder> --out /tmp/<slug>_harvest.json --project-root .
    python3 .ai-workflow/tools/qa_check.py /tmp/<slug>_harvest.json --project-root .

STORE TEMPLATE EXCEPTION: items of type "Template Showcase" that are actually store-template launches (Lumora, Meridian, any `store-templates/` build) ship no companion index.html, so `harvest_content.py` returns an empty record. Use `harvest_store_template.py <brand-slug> --out /tmp/<brand>_harvest.json --project-root .` for those instead — see CLAUDE.md's "Store Template Launch Content" section, item 6.

KNOWN GOTCHA (hit live 2026-07-29, costs you a duplicate-row cleanup if missed): CRO Fix and some Tips companion HTML files build their POST id from a click-time date embedded client-side, which the harvester can't always recover — so the harvest record's `pipeline_item_id` sometimes does NOT match the item's real id in SYNC_DATA. Before populating, compare `record["pipeline_item_id"]` against the actual SYNC_DATA item id you read in Step 1. If they differ, edit the harvest JSON's `pipeline_item_id` to the real SYNC_DATA id before running populate_sheet.py — otherwise you'll create orphaned duplicate rows under a bogus id instead of correctly joining to the existing item.

Then open the harvest record and actually read every image listed under `manual_visual_pending` / `assets.images` — eyeball brand look, legible headline, no broken layout, correct framing — this is mandatory, not best-effort, same standard the generation tasks already hold themselves to.

Step 2b — MOBILE STRIP GATE (added 2026-09-02, Ridwan's standing instruction: "we want to make sure this does not escape"). For every eligible item whose stream is "Template Showcase", "Store Template" or "Store Template (Paid)", check that the harvest record's `assets.images` contains a `*-mobile-strip.png` (or its compressed `*-mobile-strip-x.jpg` sibling). The calendar now has a dedicated X #5 slot matching `mobile-strip`, so a package missing that file will silently produce one fewer X row and the asset will never reach the account.

If it's missing, do NOT just flag it and move on — the file is cheap to produce and the source page is right there. Build it yourself before populating:

    python3 .ai-workflow/skills/page-presentation-kit/scripts/build_mobile_strip.py "<the page this showcase was built from>" "<output folder>/{slug}-mobile-strip.png" --file

Check the page's own `replo-rebuilds/brands/{brand}/pages/{page}/presentation/` folder first — since 2026-09-02 the Wednesday page-build task saves one there, and copying it is faster than regenerating. Add the resulting path into the harvest record's `assets.images` before Step 3, and note in the digest that you recovered it. Only if the source page genuinely cannot be located should you report it as a real gap.

Step 3 — Build the calendar rows locally:

    python3 .ai-workflow/tools/populate_sheet.py /tmp/<slug>_harvest.json --project-root .

Newest builds go ahead of older backlog via the this-week overwrite, EXCEPT rows listed in `.ai-workflow/tools/protected_rows.json`, which are never bumped (Ridwan, 2026-10-05). Do not add to that list yourself unless Ridwan asks. (omit --week-monday — the default of "next Monday from today" is correct for a Monday assembly run). This is idempotent by post_id and only ever appends to the LOCAL queue.json/queue.csv.

Step 3b — Confirm the strip actually got a row. After populating, grep the new rows for the "X #5 full page at a glance" angle on every Template Showcase / Store Template item, and confirm its `asset_paths` is non-empty and points at the strip (the compressed `-x.jpg` sibling when one exists — `resolve_assets` prefers it automatically, so an oversized PNG can no longer sneak through). An empty asset_paths on that row means the matcher found nothing and the post would go out text-only. Fix the record and re-run rather than shipping the empty row.

Step 3c — Twitter/X caption character-count check (added 2026-09-07, Ridwan's standing instruction — permanent, every run). `populate_sheet.py` already flags any `x_*` caption key over X's 280-character limit in the new rows' `qa_status`, but don't just trust that silently — after populating, actually pull every new Twitter row this run added (from queue.json/queue.csv, matched by the post_ids you just created) and independently re-count each one's `caption` field length yourself. This is a deliberate double-check, not a re-implementation: `populate_sheet.py`'s own flag logic is correct, but a manual count here catches the case where a caption was hand-edited or backfilled from a `*-social-content.json` file after the fact and never re-run through the script. Any Twitter caption over 280 characters — whether newly found or already flagged by the script — must be named explicitly in the Step 8 digest (post_id, character count). Do not silently rewrite the caption; that's a content-review decision, not an assembly-task one.

Step 4 — Host every new asset so Make.com can actually reach it once these rows reach the Sheet:

    python3 .ai-workflow/tools/feed_linkedin.py --project-root .
    python3 .ai-workflow/tools/feed_media.py --project-root .

Both are idempotent (skip rows that already have `asset_urls`) — safe to run across the whole local queue every time.

Step 5 — Sync back so nothing gets re-picked next week:

    python3 .ai-workflow/tools/sync_content_system.py --project-root .

This attaches the `distribution[]` array to each matching SYNC_DATA item — additive, never removes existing data, writes a `.bak` automatically.

Step 6 — Push ONLY the new rows into the live Google Sheet:

    python3 .ai-workflow/tools/append_sheet_rows.py --project-root . --dry-run

Read the dry-run output first and sanity-check it (row count, platforms) before the real run. Then run it for real without --dry-run. This script (built 2026-08-02) uses a Sheets API append call, not a full-sheet replace — it is safe by construction, it can only ever add rows never already present (matched by post_id), and it is IMPOSSIBLE for it to touch or overwrite an existing row's status, so Ridwan's Ready flips and Make's Posted write-backs are never at risk. Do NOT use the Drive connector's create-file tool for this — it would create a duplicate file, not update the real Sheet.

IF append_sheet_rows.py FAILS with an auth error (likely message: "invalid_grant" or a 401/403): the OAuth refresh token is short-lived (7 days) while the Google Cloud OAuth consent screen stays in "Testing" publishing status. This is expected to happen periodically until Ridwan switches that project's publishing status to "In production" (Google Cloud Console → "Google Auth Platform" → Audience — no Google verification review needed for a single-user personal app). If it fails: do NOT fall back to a full-sheet replace or any other risky write. Instead, fall back to Step 6's old safe behavior — produce a clean paste-ready block of just the new rows (columns: post_id, pipeline_item_id, stream, platform, scheduled_date, scheduled_time_local, intended_et, asset_paths, caption, caption_source_tab, status, qa_status, posted_at, content_system_folder, caption_json, asset_urls) and tell Ridwan plainly that the Sheets connection needs re-authorizing (point him at this project's 2026-08-02 build log entry in `docs/koolestpro-content-operating-plan.md` for the exact re-auth steps) and that in the meantime he should paste this block in himself.

Step 6b — Keep the sheet's platform grouping intact (added 2026-08-27). ONLY if Step 6 actually pushed new rows via the real API call (skip this step entirely if Step 6 fell back to a manual-paste block, or if there were zero new rows) — run:

    python3 .ai-workflow/tools/sort_distribution_queue.py --project-root .

Ridwan's live sheet is organized Twitter block first, then LinkedIn, then Instagram at the bottom, each sorted old→new by scheduled_date, so newly appended rows (which land at the physical bottom of the sheet from a raw API append) need this re-sort to land back in their correct platform block instead of sitting out of place at the end. This script is safe and idempotent — it also auto-clears a known blocker (a plain "Create a filter" on the sheet silently prevents any sort from taking effect; the script clears it every run) and normalizes the scheduled_date column to a real Date type before sorting (some older/webhook-written rows can land as plain text, which breaks date ordering). It does not touch the sheet's two saved Filter Views ("Needs Review", "Today").

Step 7 — Never flip any row to "Ready" yourself. The Draft → Ready approval gate is Ridwan's alone, always has been, and this task does not change that.

Step 8 — Finish with a short, scannable digest: how many new rows this run (broken down by platform), which source items they came from, whether they were pushed automatically to the Sheet or fell back to a manual-paste block (and why, if so), whether Step 6b's re-sort ran, and every row whose `qa_status` starts with "Needs Review" called out by name. Include a MOBILE STRIP line for every Template Showcase / Store Template item processed: whether its strip was already present, was recovered by you in Step 2b, or is genuinely missing, and confirming the X #5 row exists with a real asset path. Include a CAPTION LENGTH line from Step 3c: how many new Twitter rows were checked and how many (if any) are over 280 characters, named explicitly. If Step 1 found nothing new, this digest is just one sentence — don't pad it.
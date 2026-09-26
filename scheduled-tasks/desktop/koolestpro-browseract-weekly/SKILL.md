---
name: koolestpro-browseract-weekly
description: Weekly BrowserAct lead-gen rotation (Tuesdays ~09:05). Scores leads in the cloud and QUEUES them to .ai-workflow/pending-push/; the Mac-side importer pushes them into local KoolestFlow.
---

This is the weekly automated run of the BrowserAct lead-gen pipeline for Ridwan's koolestpro-cowork-v2 project. You are a fresh session with no memory of prior conversations. Follow these steps exactly.

## Architecture — read this before doing anything

This is the HYBRID pipeline (chosen by Ridwan 2026-09-01). Your job is discovery + enrichment + scoring ONLY. You do NOT push to KoolestFlow.

Why: KoolestFlow's Vercel deployment (KOOLESTFLOW_BASE_URL) stores prospects in SQLite on an ephemeral serverless filesystem. It accepts POST /api/state, returns success, and prints a convincing "Pushed N new prospect(s)... Total prospects now: N" line — then serves an empty list on the next cold request. On 2026-09-01 a full run of 5 leads was lost this way and all 5 brands were wrongly marked "taken" in the ledger. Ridwan's real prospect data lives on the LOCAL instance (KOOLESTFLOW_LOCAL_BASE_URL, http://127.0.0.1:8787), which no cloud sandbox can reach.

So: you write scored prospects to `.ai-workflow/pending-push/{week}_{slug}.json`. A launchd job on Ridwan's Mac (`.ai-workflow/tools/import_pending_push.sh`, every 30 min) drains that queue into local KoolestFlow, verifies the write stuck, and only then records the brands in the taken-brands ledger. Leads queue safely while his Mac is asleep.

## Steps

1. The project folder is normally mounted directly in the cloud bash tool at `/sessions/<session>/mnt/koolestpro-cowork-v2/` — check there first with `ls`. Use it directly; no device_stage_files round-trip is needed. Only if the folder is NOT mounted, fall back to device tools, and if neither is available, stop and report that the run was skipped.

2. Confirm `.env` has BROWSERACT_API_KEY and BROWSERACT_LEADGEN_WORKFLOW_ID and BROWSERACT_ENRICH_WORKFLOW_ID. If any is missing, do not guess — append a run entry to `.ai-workflow/browseract-weekly-log.json` with status "error" and that note, then stop.

3. Run the resumable runner from the project root:

   python3 .ai-workflow/tools/leadgen_run.py --budget 150

   IMPORTANT — this must be called REPEATEDLY. A cloud bash call is capped near 170 seconds and background processes do NOT survive between calls (each call gets a fresh PID namespace, so `nohup ... &` is silently killed). A single BrowserAct enrichment can take several minutes, so one call cannot finish the run. The script checkpoints to `.ai-workflow/.leadgen-state.json` after every step and prints one of:
     - `RUN_PAUSED`   → call it again, same command
     - `RUN_COMPLETE` → done, stop calling it
   Keep calling it until you see RUN_COMPLETE. Expect roughly 8-20 calls. This is normal, not a failure. Do not try to raise --budget above ~150; the call will just be killed mid-flight.

   Known transient conditions the script already handles — do not "fix" them, just call again:
     - "Running tasks number exceeds" = BrowserAct's concurrent-task cap, because abandoned tasks still hold slots. Wait one call and retry.
     - An enrichment stuck "running" past 420s is abandoned deliberately; that lead is scored without website/social data and flagged.

4. When it prints RUN_COMPLETE, the script has ALREADY: written the pending-push file, advanced `browseract_rotation.json`'s currentIndex, and appended an entry to `browseract-weekly-log.json` with status "queued" and leadsPushed 0. Do not duplicate any of that by hand. Confirm by running `python3 .ai-workflow/tools/leadgen_run.py --status` and by re-parsing both JSON files to check they are still valid.

5. **Verify every prospect has a usable source link and clean contact fields (fixed 2026-09-18, keep checking).** `browseract_koolestflow_bridge.py`'s `build_prospect` now always sets `source_url` — the lead's own Instagram profile when one was found, otherwise a Google Maps search link built from business name + address (there's no place_id/direct listing URL in the Maps CSV, so a search link is the best available; see `_maps_search_url`'s docstring). `parse_enrichment_row` also now runs `website_url`/`instagram_url` through `_extract_url`, which strips stray brace-wrapping and rejects unsubstituted BrowserAct template tokens (e.g. a literal `{constant_placeholder}` used to get written into `website_url` as if it were a real site — confirmed on Gerald babies & kids and Childmate, 2026-W38). After the run, spot-check the pending-push JSON: no `website_url` or `instagram_url` should contain `{`, `}`, or the word "placeholder", and no prospect should have an empty `source_url`. If you find one that slipped through, it's a real bug in the bridge script (not a transient condition) — fix `.ai-workflow/tools/browseract_koolestflow_bridge.py` directly, re-run `python3 -m py_compile` on it and `leadgen_run.py` to confirm it still imports, patch the already-written pending-push file's affected fields by hand using the corrected helper functions, and flag the fix in your summary. Never leave a `{constant_placeholder}`-style value in a shipped record.

6. Report honestly. leadsPushed stays 0 until the Mac importer confirms the local push — "queued" is the correct success state for this task, not "pushed". Never claim leads reached KoolestFlow; you have no way to verify that from here.

7. End with a short plain-text summary Ridwan will see in the task history: which area/keyword ran, how many leads were scored, how many were skipped as already-taken, the pending-push filename, each lead's source_url, and anything needing his attention — a missing credential, BrowserAct failing outright, any lead whose enrichment stalled (those have unverified Build/Fix/Scale classifications and should be checked by hand before outreach), or any data-quality bug you had to fix in the bridge script.

Do not touch outreach_tracker.json, do not change dm_leads_pool.json status fields, and do not send any outbound messages. Discovery, enrichment, scoring, and queueing only.
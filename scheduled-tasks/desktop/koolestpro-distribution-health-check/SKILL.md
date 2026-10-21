---
name: koolestpro-distribution-health-check
description: Every 2 days: scans the Koolestpro Distribution Queue Google Sheet for missed/overdue Ready posts and checks Make.com scenario health, to keep an average of 3 posts/day going out.
---

This is an automated run of a scheduled task. The user is not present to answer questions. For implementation details, execute autonomously without asking clarifying questions — make reasonable choices and note them in your output. "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if the task file asks for that specific action. When in doubt, producing a report of what you found is the correct output.

You are running a recurring health check for Ridwan Adekunle's (koolestpro) social content posting pipeline. This is a fresh session with no memory of prior runs — everything you need is below. Do the full job in one pass and end with a clear chat-style summary (this becomes his notification).

## What you're protecting
Ridwan wants posts going out at an average of 3/day, with zero silent gaps, no two posts for the same platform ever firing at the same time, and never more than one LinkedIn post on the same day (Twitter has no daily cap). Seven things can break that:
1. A row in his Google Sheet queue sits in a "ready to post" state, its scheduled date passes, and it never actually posts (Make.com skipped it, errored on it, or it fell outside the automation's filter).
2. The Make.com scenario itself goes unhealthy (paused, erroring repeatedly, or stops executing) so NOTHING posts even though the sheet is full of ready rows.
3. Two rows for the same platform share the exact same `(scheduled_date, scheduled_time_local)` — Make's "due now" filter matches both in the same execution and they post back to back, which reads to Ridwan as "two posts went out at once."
4. Two or more LinkedIn rows land on the same `scheduled_date`, even at different times — Ridwan's hard rule is max 1 LinkedIn post per calendar day, no exceptions. Twitter has no such cap.
5. A Twitter/X caption is over the 280-character limit and gets silently rejected by X on post (added 2026-09-07, Ridwan's standing instruction — see Step 1b).
6. An Instagram row is in a format that won't post: a single image (route deliberately off since 2026-10-05, carousels + videos only) or a malformed carousel — see Step 1c.
7. The "Distribution Queue Reschedule" webhook scenario (id 7111659) is itself inactive — the webhook still returns HTTP 200/"Accepted" and silently queues the request, but nothing actually updates in the Sheet until the scenario is reactivated. Discovered live 2026-09-08: 9 reschedule calls in this same task returned 200 but did nothing until the scenario was turned back on. Always verify a reschedule actually landed (re-read the row after calling the webhook), never trust the 200 alone.

Your job: catch all seven, actually fix what's safely fixable, and tell Ridwan exactly what still needs his attention — including if the backlog of ready-to-post rows is running too thin to sustain 3/day.

## Step 1 — Read the sheet
Google Drive file: title "Koolestpro Distribution Queue", fileId `1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg`.
If a Google Drive read/download-file tool isn't already loaded, use ToolSearch (query like "google drive download file content") to find and load it, then call it on that fileId with exportMimeType "text/csv" to get the tab (named "Untitled") as CSV.

**Important:** the download tool returns its result as JSON `{content: <base64>, ...}` when the file is large — decode `content` from base64 to get the actual CSV text (it will NOT be plain text directly if it's large; check for this). If the result is too large for a single tool call, it gets saved to a file on disk instead. Several things have worked in this project before, in order of preference:
1. `mcp__d9e17430-10ee-4a01-bb3c-df97587a768b__read_file_content` on the same fileId returns a non-base64, human-readable text representation instead — often easier to search directly (e.g. via `Grep` for `"LinkedIn | 2026"` or `"Twitter | 2026"` style fragments) without needing to decode anything. Try this first.
2. If that result itself is too large for a single tool call, it gets auto-saved to a host-side tool-results file. `Grep` that file with a chunking pattern like `.{1,450}` and `output_mode:"content"`, `-o:true`, `head_limit:0` to re-split it into many shorter lines; if that output is also too large it gets saved to a new tool-results file, which you can then `Read` in small batches (25 lines/call is reliably safe; much more than that has hit token-limit errors inconsistently). This works without needing a subagent and has proven reliable end-to-end (used successfully 2026-09-07). Note: this file lands as effectively ONE giant line — grep patterns for a targeted field near a known anchor string (e.g. `anchor.{0,400}`) work reliably up to roughly 400-2000 chars of capture before results start getting silently omitted as "too long"; step the capture width down if a match comes back omitted.
3. If you must use the base64 `download_file_content` route and it's too large, delegate the fetch-and-classify step to a subagent so the raw content never has to pass through your own context — give it the exact classification rules below and have it return only the classified summary. Keep the subagent's ask narrow (e.g. one platform's schedule at a time) rather than asking for a full re-parse of everything, since narrow asks have completed reliably in this project and broad ones have previously stalled or hit session rate limits.

**Fastest, most reliable option if Google Sheets API access is already set up:** the project's `.ai-workflow/tools/*.py` scripts already authenticate against this exact sheet via `GOOGLE_OAUTH_CLIENT_ID`/`_SECRET`/`_REFRESH_TOKEN` in `.env` (see `append_sheet_rows.py` for the reusable auth pattern). A short one-off Python script run via `mcp__workspace__bash` that refreshes a token and calls `GET .../values/Untitled!A1:P` is faster and exact — no OCR-style text-dump parsing needed — and is how the row-level Instagram fixes were done on 2026-09-08. Prefer this when you need to read AND write (e.g. patching a cell), not just read.

Parse as CSV/rows. Columns (0-indexed, in this exact order): `post_id`(0), `pipeline_item_id`(1), `stream`(2), `platform`(3), `scheduled_date`(4), `scheduled_time_local`(5), `intended_et`(6), `asset_paths`(7), `caption`(8), `caption_source_tab`(9), `status`(10), `qa_status`(11), `posted_at`(12), `content_system_folder`(13), `caption_json`(14), `asset_urls`(15).

**Instagram is IN SCOPE as of 2026-09-08 (Ridwan's instruction — this reverses the prior 2026-08-27 "Instagram is out of scope" rule).** Instagram publishing went live via Make.com modules 301/302/304/306 on 2026-09-08. Classification, rescheduling, the 7-day pacing count, and collision checks in Steps 1-4 now all operate on Twitter + LinkedIn + Instagram rows. Instagram currently has no documented daily cap or no-simultaneous-slot exemption beyond the general "no two same-platform rows at the exact same (date, time)" rule — treat it the same as Twitter for slot-collision purposes unless Ridwan says otherwise. Instagram has no LinkedIn-style 1-per-day cap either, unless told otherwise.

Today's date: use the current date in Africa/Lagos timezone (Ridwan's timezone) as "today" for all comparisons.

**Classify every row (Twitter + LinkedIn + Instagram):**
- **Posted** — `posted_at` is filled or `status` = "Posted". No action needed.
- **Missed/overdue** — `posted_at` is empty AND `status` is NOT "Posted" AND `scheduled_date` is before today. This is a real gap.
- **Upcoming/queued** — `posted_at` is empty, `status` is NOT "Posted", `scheduled_date` is today or future. Healthy backlog.
- **Blocked** — `qa_status` clearly indicates it isn't postable (contains "Needs Review", "Failed", "Error", etc.) — flag separately, do not reschedule a QA-blocked row automatically; the content itself isn't ready, a new date won't fix that.

## Step 1b — Twitter/X caption character-count check (added 2026-09-07, Ridwan's standing instruction — permanent, every run)
Independently character-count every Twitter caption's actual text (column 8, `caption`) against X's 280-character hard limit — do this yourself, do not just trust whatever `qa_status` already says, since `qa_status` can be stale or a row's caption can drift after it was last QA'd. This applies to every Twitter row you touch this run, but prioritize the ones that matter most: any row classified **Upcoming/queued and NOT already Blocked** (these are the ones that would actually post as-is without a human catching a length problem first). For rows already Blocked for other reasons, a quick count is still worth doing but isn't urgent since they can't post anyway until cleared.

If you find a caption over 280 characters that is NOT already flagged in `qa_status`, this is a new finding — call it out explicitly in the Step 5 log and the final summary (post_id, character count, scheduled date). Do not silently fix or rewrite the caption yourself; report it so Ridwan or the next content-review pass can fix the actual text. If a row's `qa_status` already flags an over-limit caption, just confirm the count still holds and move on — no need to re-describe it as new.

Report a one-line rollup in the summary either way: how many Twitter captions you checked, how many were found over 280 chars (new findings vs. already-flagged), so this check is visibly happening every run rather than assumed.

## Step 1c — Instagram format check (rewritten 2026-10-05, Ridwan's instruction)

Instagram posts carousels and videos only. Make has a native carousel route (310-317, 2-10 images) and a Reels route (304-306). The single-image route (318) is deliberately blocked. So:
- Never trim a multi-URL `asset_urls` to one image. Multi-URL rows are correct and post as carousels.
- Flag (don't fix) any upcoming Ready Instagram row whose `asset_urls` is a single image or empty: it will never post. Report post_id + date.
- Flag any carousel with more than 10 URLs, or a mix of .mp4 and images (the carousel route only handles images).
- Instagram cap: max 1 post per day. Treat a second Ready carousel/video on the same day as a violation and move the clean one to the next free day at 17:00.
- When rescheduling overdue Instagram carousels/videos, use 17:00, one per day, and avoid the same template video on consecutive days.

## Step 1d — Caption matches its image (added 2026-09-28, Ridwan's instruction, permanent, every run)

Run `python3 .ai-workflow/tools/caption_fit.py` from the project root. It checks every unposted row in the local `queue.json` for a caption that doesn't fit its image:
- a single image posted with "four ads", "carousel" or "swipe" wording;
- an empty caption;
- a stray "158 chars" counter pasted into the tweet;
- a before/after image whose X caption never contrasts before and after.

For each flagged row due in the next 7 days, report it in Step 5 and in the final summary: the post_id, the image filename and the reason. Do NOT rewrite the caption or reschedule the row yourself. The right caption depends on what the image shows, and Ridwan decides that. Also add one rollup line: "caption/image check: N rows checked, M flagged (K due within 7 days)".

## Step 2 — Actually fix genuinely missed rows via the reschedule webhook
**First, verify the reschedule webhook's own scenario is active** (added 2026-09-08 — see item 7 above). Check scenario id 7111659 ("Distribution Queue Reschedule") via the Make MCP tools; if `isActive`/`scenarioIsActive` is false, activate it before calling the webhook at all, otherwise every call below will silently no-op.

For every row classified as **missed** that is NOT also **blocked** (i.e. QA-clean, just never posted): reschedule it for real using this webhook — do not just recommend it.

**Webhook:** `POST https://hook.eu1.make.com/ocwhcp96a5up7i8hjqxuqrkw7m3a59rm`
**Body (JSON):** `{"post_id": "<exact post_id>", "new_scheduled_date": "<YYYY-MM-DD>", "new_scheduled_time_local": "<same format as the existing scheduled_time_local value>"}`

This webhook (a small dedicated Make.com scenario "Distribution Queue Reschedule", id 7111659, built 2026-08-26 specifically for this task) finds the row by exact `post_id` match and overwrites only `scheduled_date` and `scheduled_time_local` for that one row. On success it returns HTTP 200 — the response body has been observed as either `{"ok":true,"post_id":...,"updatedRows":"1"}` or a plain `Accepted` text body. **HTTP 200 alone is NOT proof the reschedule landed** (see item 7 above) — after calling the webhook for a batch of rows, re-read those rows' `scheduled_date`/`scheduled_time_local` from the live sheet and confirm they actually changed before reporting the fix as done. If a row didn't change, check whether scenario 7111659 went inactive again and retry.

**⚠️ No-simultaneous-slot rule (added 2026-09-04, Ridwan's standing instruction — see this project's CLAUDE.md, "DISTRIBUTION QUEUE — NO SIMULTANEOUS-SLOT RULE" section, for the full root-cause writeup).** Make's posting scenario matches every row where `scheduled_date == today AND scheduled_time_local <= now` — not an exact-time match — so two rows for the **same platform** sharing the same `(scheduled_date, scheduled_time_local)` will both post in the same run, back to back. **The webhook itself does not check for this — you are the only guard.** Before picking a new date/time for ANY row (missed or otherwise), for ANY of Twitter/LinkedIn/Instagram:

1. Pull the live sheet's rows for that platform on the candidate date first.
2. Never assign a `(platform, scheduled_date, scheduled_time_local)` that's already taken by another row for that same platform. Different platforms can share a time slot on the same day — only same-platform collisions matter.
3. Reuse the standard slots (`09:00`/`13:00`/`18:00`/`23:00` for Twitter/LinkedIn; Instagram's standard slot has been `17:00`, occasionally `9:00`/`12:00`/`14:00`) where free. When a day's standard slots for that platform are all taken, use an additional time spaced at least ~60-90 minutes from every other slot that platform already has that day, rather than ever reusing a time.
4. Spread multiple missed rows across different days as before, but the per-row time check above still applies even when landing on a day that already has room.

**⚠️⚠️ LinkedIn max-1-per-day rule (added 2026-09-04, Ridwan's standing instruction — see CLAUDE.md "LINKEDIN — MAX 1 POST/DAY, HARD CAP").** This is stricter than the no-simultaneous-slot rule and applies to LinkedIn only: LinkedIn may never have more than ONE row scheduled on the same `scheduled_date`, period — a different time on the same day does NOT satisfy this. When picking a date for a LinkedIn row (missed, or an existing collision being fixed):

1. Pull every LinkedIn row in the live sheet and check the **whole unposted backlog for that platform**, not just the next 7 days — a same-day violation further out is still a violation (this was missed once already, on 2026-09-04, because a first pass only checked 7 days and missed a 2-post-same-day collision 8 days out).
2. Never assign a LinkedIn row to a `scheduled_date` that already has another LinkedIn row on it. If the target day already has one, move to the next genuinely open LinkedIn day instead.
3. Twitter and Instagram have no daily cap — this rule does not apply to them.

**Also scan for EXISTING violations, not just ones you're about to create.** As part of this step, check every **upcoming** (not just missed) Twitter/LinkedIn/Instagram row too:
- Group Twitter and Instagram rows by `(scheduled_date, scheduled_time_local)` separately and flag any group with more than one row (same-time, same-platform collision).
- Group LinkedIn rows by `scheduled_date` alone and flag any group with more than one row (same-day violation, regardless of time) — check the FULL unposted LinkedIn backlog for this, not just 7 days out.

For each violation found: if at least one row in the group is QA-clean, move ONLY the QA-clean row(s) to a free slot using the rules above — never move a Blocked row, and if EVERY row sharing the slot is Blocked, log it as found-but-unfixable (content isn't ready, so a new time doesn't help). Log these as a separate "collisions/violations fixed" category in Step 5, since they're not overdue posts, just future ones that broke a scheduling rule.

Call the webhook once per row that needs a new date/time (use `mcp__workspace__bash` with `curl` or `urllib`, or an HTTP tool if one is already loaded — ToolSearch for "http request" if needed).

## Step 3 — Check Make.com scenario health (the MAIN posting scenario, not the reschedule one)
Use the Make.com MCP tools (server id starting `539cfcd5-...` if already loaded, else ToolSearch for "make scenario executions list").
- `teamId`: 1960838
- Main posting scenario: "Koolestpro Social Distribution", `scenarioId`: 6565331 (this is the one that actually posts to socials — separate from the reschedule webhook's scenario, id 7111659, which you health-check per Step 2's new first line but don't need to executions-audit here).

Call `scenarios_list` or the single-scenario getter for teamId 1960838, find scenario 6565331. Check: `isActive`, `isPaused`, cumulative `errors` count, `nextExec`.
Call `executions_list` for scenarioId 6565331 covering roughly the last 3 days (`from`/`to` as unix timestamps, or just take the most recent page — the list is already newest-first). Tally: executions, errors, successes, timestamp of most recent execution. For any error, use `executions_get-detail`/`show_execution_result` to see the failing module and error message before deciding whether it's a known/expected pattern (like the Instagram carousel 400 in item 6 above) or something new.

**Flag Make as unhealthy if any of:** `isPaused` true; `isActive` false; the most recent execution errored and nothing since has succeeded; or a gap of more than ~30 hours since the last execution during a period when the sheet has overdue/missed rows (the scenario runs on a fixed schedule around 14:00/17:00/18:00/23:00 Africa/Lagos most days). An isolated error that's followed by a successful execution is worth a one-line mention (pattern to watch), not a full unhealthy flag — this project has a documented history of transient 401/403 auth hiccups on the credential-refresh step that self-resolve on the next run, and a documented history of Instagram 400s specifically caused by the multi-image issue in item 6 (which Step 1c should already be preventing going forward).

If Make looks unhealthy, say so clearly with a concrete next step (e.g. "check the scenario's error log in Make.com" or "scenario is paused, reactivate it").

**Do not attempt to hand-edit the MAIN posting scenario's (6565331) blueprint via `scenarios_update`** (e.g. to add delay/stagger modules, or to build real Instagram carousel support) as part of this recurring task — the blueprint is large (~90KB) and multi-branch, and while it CAN now be read faithfully as a single greppable `.txt` (via `scenarios_get`, which auto-saves large results to a tool-results file), a `scenarios_update` call still wholesale-replaces the entire blueprint with no partial-patch option, and reconstructing ~90KB of JSON as literal tool-call output on a production posting scenario is a deliberate, reviewed, ad hoc action only — not something this recurring check should attempt unattended. The small dedicated reschedule scenario (7111659) is a different, much smaller, lower-stakes scenario and is fine to activate/deactivate per Step 2, but still should not have its blueprint hand-edited here either.

## Step 4 — Check pacing / backlog depth
Count **upcoming/queued** rows (Twitter + LinkedIn + Instagram; including any you just rescheduled in Step 2) grouped by `scheduled_date` for the next 7 days. Compute the average posts/day over that window.

If the 7-day average is below 3/day, say so explicitly with a concrete number: "you have X queued posts over the next 7 days (avg Y/day) — add roughly Z more rows to get back to a 3/day average."

Also separately note how many of those upcoming rows are QA-blocked (`qa_status` contains "Needs Review"/"Failed"/"Error") vs. genuinely clean/postable — a healthy raw count can hide an unpostable backlog if most of it is stuck in review. Report both numbers when they diverge meaningfully. If the blocked share of the full upcoming backlog (not just the 7-day window) is unusually high (rule of thumb: over half), call that out as the real bottleneck, since clearing existing blocked rows is usually higher-leverage than writing new content.

## Step 5 — Log and report
Append a dated entry to `distribution-health-log.md` at the root of the koolestpro-cowork-v2 project (create it with a short header if it doesn't exist). Each entry: date/time of check, missed rows found and fixed (post_id, old date → new date, webhook result, confirmed-landed check), same-time collisions found and fixed (Twitter/Instagram), same-day LinkedIn violations found and fixed (post_id, old date → new date, webhook result), missed rows found but NOT fixed (e.g. blocked ones, or webhook failures) with reason, the Step 1b Twitter char-count rollup (checked/over-limit/new-findings), the Step 1c Instagram multi-image rollup (checked/found/trimmed), whether the reschedule scenario (7111659) was found inactive and reactivated, Make health verdict, 7-day pacing verdict (Twitter+LinkedIn+Instagram, plus the backlog-wide QA-clean/blocked split).

Then end with a concise chat-style summary covering: what was found and fixed (including any collisions/violations and any Instagram multi-image trims), any new Twitter caption over 280 chars found in Step 1b, whether the reschedule webhook scenario needed reactivating, what's blocked and needs Ridwan's attention, Make health, and pacing verdict. No fluff. If everything is clean (no missed rows, no collisions, no LinkedIn violations, no new over-limit captions, no Instagram multi-image rows, reschedule scenario active, Make healthy, pacing fine), say so briefly.

## Spacing rule for ALL rescheduling (added 2026-10-08, Ridwan's instruction)

Never reschedule a missed row by hand into "the next free slot" if that puts the same brand within 5 days of another post of that brand, or the same post type back to back. After you reschedule anything, run `python3 .ai-workflow/tools/space_queue.py --project-root . --dry-run`, read it, then run it for real (it re-spaces all Ready rows consistently) and `sort_distribution_queue.py`. Report the supply gap (empty X slots) it prints, since the target is 3 X posts a day plus one hero post a day on LinkedIn and Instagram.

## Retired rows and Instagram (2026-10-08)
- Ignore rows with status `Retired` in missed/overdue classification.
- Instagram is active; only carousel/video rows are publishable. Never open instagram.com with browser automation.

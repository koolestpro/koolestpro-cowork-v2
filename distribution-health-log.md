# Distribution Health Check Log

Recurring health check for the Koolestpro Distribution Queue (Google Sheet) and the "Koolestpro Social Distribution" Make.com scenario (id 6565331). Each entry logged by `koolestpro-distribution-health-check`.

---

**Rotation rule (added 2026-09-27):** this file holds only the most recent 5 entries. When a new entry would push it past that, move the oldest entry(ies) to `docs/system/distribution-health-log-archive.md` (append, don't overwrite) in the same edit. Read only this file's tail for a normal health-check run; read the archive only if you need history older than what's here.

---

## 2026-10-05 08:40 UTC (09:40 WAT) — health check (scheduled task run)

**Sheet read:** live Sheets API, 209 rows (125 Posted, 75 Ready, 9 Draft).

**Twitter/LinkedIn missed rows:** 5, all Draft + Needs Review, so none rescheduled (Draft never fires; a new date won't fix the content):
- `tip-listiku-copy-presell-5-elements-20260510-20260928-li-0900` (LI, 09-28) — claims to verify (carried over from last run)
- `static-ad-caraway_fry-pan-20260909-20260929-x-1300` (X, 09-29) — claims to verify ("18,878 reviews")
- `cro-fix-caraway_fry-pan-pdp-20260907-20260923-x-1300` (X, 09-30), `...-li-0900` (LI, 09-30), `...-20260925-x-0900` (X, 10-02) — x_thread[3] variant 316 chars
**Instagram missed rows:** 50 past-dated unposted (was 46). Not rescheduled: Instagram is still paused in Make (CLAUDE.md, 2026-09-18). Batch-reschedule when IG is switched back on.

**Collisions / LinkedIn same-day violations (upcoming):** none. 5 upcoming LinkedIn rows each on their own day (10-06, 10-07, 10-08, 10-14, 10-21). No webhook calls this run.

**Step 1b, X char count:** 18 unposted Twitter captions checked, 0 over 280, 0 empty. Last run's 319-char Gainful post (`...-20260906-x-1800`) is now marked Posted 2026-09-30 14:01 and the Make run succeeded, so X apparently accepted it.

**Step 1c, Instagram multi-image:** 2 upcoming IG rows with 3 URLs (`cro-fix-flybyjing_chili-crisp-pdp-20261004-20261007-ig-1200`, `cro-fix-caraway_fry-pan-pdp-20260907-20260923-ig-1200`). NOT trimmed: Make has a native IG carousel route (310-317) since 2026-09-27, so the trim rule in this task's SKILL.md is obsolete (flagged last run too).

**Step 1d, caption/image fit:** `caption_fit.py` reported 0 problem rows (reads local `queue.json`).

**Reschedule scenario 7111659:** active, not paused. No reactivation needed.

**Make health (6565331):** healthy. Active, not paused, next run 2026-10-05 13:00 UTC. All 50 executions from 09-28 22:00 UTC to 10-04 22:25 UTC succeeded (status 1), no warnings. Lifetime error count still 3 (old).

**Pacing (10-05 to 10-11):** 18 unposted rows (10 X, 3 LI, 5 IG) = 2.6/day raw. Excluding paused Instagram: 13 X+LI rows = **1.9/day**; about 8 more Ready X/LI rows needed to reach 3/day. 10-11 has only 1 post. Beyond 10-11 the backlog is just 11 rows to 10-21, with nothing on 10-12, 10-19, 10-20. QA: 0 of 18 clean in the window, 1 of 29 across the whole upcoming backlog. These Ready-but-flagged rows still fire (Make ignores qa_status), so the flags are a review risk rather than a blocker.

**Verdict:** Make healthy, no fixable gaps, no collisions. Needs Ridwan: pacing under 2 real posts/day with a thin queue after 10-11, 5 Draft X/LI rows waiting on caption/claim fixes, 50 Instagram rows parked until IG is unpaused, and the outdated Step 1c in the task SKILL.md.

## 2026-10-05 ~10:20 WAT — Instagram re-enabled + Caraway CRO cleanup (ad hoc, Ridwan present)

- Make 6565331: Instagram router filter fixed (`Instagram`), single-image route blocked, Reel wait 90s. Live blueprint diffed against intended: identical.
- 26 overdue IG carousels/videos rescheduled 1/day at 17:00 (10-05 18:00 to 11-06). Verified landed. No IG same-slot collisions.
- Deleted 4 pending Caraway CRO rows from the Sheet + local queue (backup in `outputs/distribution-queue/deleted/`).
- IG token expires 2026-11-07, same week the rescheduled backlog ends.

## 2026-10-07 ~18:00 UTC (~19:00 WAT) — health check (scheduled task run, fired late; slot was 08:35 UTC)

**Sheet read:** live Sheets API, 205 rows (135 Posted, 63 Ready, 7 Draft). Today's 4 rows (X 14:00, X 18:00, LI 14:00, IG 17:00) all posted.

**Missed rows:** 27 past-dated unposted, all `Needs Review`, so none rescheduled (blocked rule). No webhook calls this run.
- X/LI (2, both Draft, carried over): `tip-listiku-copy-presell-5-elements-20260510-20260928-li-0900` (LI 09-28), `static-ad-caraway_fry-pan-20260909-20260929-x-1300` (X 09-29). (The Caraway CRO X/LI rows from last run were deleted on 10-05.)
- Instagram (25): every one is a single image (23) or has empty `asset_urls` (2: `tip-the-conversion-layer-1777028149144-20260824-ig-1200`, `idea-why-your-pdp-loses-sales-at-60-scroll-...-20260826-ig-1200`). The single-image route is blocked, so these can never post as-is. They're the leftovers from the 10-05 carousel/video reschedule. Ridwan to decide: rebuild as carousels or mark them dead.

**Collisions / LinkedIn same-day / IG same-day:** none. Upcoming LinkedIn rows on 10-08, 10-14, 10-21, one each. IG one per day 10-08 to 11-06, all 17:00. No same-template video on consecutive days.

**Step 1b, X char count:** 11 unposted Twitter captions checked (10 upcoming + 1 missed Draft). Longest 271. 0 over 280, 0 empty, 0 new findings.

**Step 1c, Instagram format:** 30 upcoming IG rows checked. 24 single .mp4 Reels, 6 image carousels (3-8 URLs). 0 single-image, 0 empty, 0 over 10, 0 mixed. Nothing trimmed.

**Step 1d, caption/image fit:** `caption_fit.py`: 0 rows flagged (reads local `queue.json`).

**Reschedule scenario 7111659:** active, not paused. No reactivation needed.

**Make health (6565331):** healthy. 33 executions 10-04 13:00 UTC to 10-07 17:25 UTC, all status 1 (success), no warnings. Latest 2026-10-07 17:25 UTC. One manual run by Ridwan 10-06 16:40 UTC.

**Pacing (10-07 to 10-13):** 12 unposted rows (5 X, 1 LI, 6 IG) = **1.7/day**; about 9 more rows needed for 3/day. Counting today's 4 already posted, 16 rows = 2.3/day. 10-12 and 10-13 have 1 post each (IG only). X runs out after 10-18; LI has only 3 rows to 10-21. QA: 0 of 12 clean in the window (3 IG rows "not run through automated QA"); backlog-wide 40 of 43 upcoming rows `Needs Review`. These Ready rows still fire (Make ignores qa_status).

**Verdict:** Make healthy, no fixable gaps, no collisions, no over-limit captions. Needs Ridwan: thin queue (1.7/day this week, X empty after 10-18, LI only 3 rows), and 25 dead single-image/empty Instagram rows.

## 2026-10-09 16:03 UTC (17:03 WAT) — health check (scheduled task run, fired late; slot was 08:35 UTC)

**Sheet read:** live Sheets API, 205 rows (162 Posted incl. today's 3, 36 Ready, 7 Draft, 21 Retired ignored). Today's X 14:00, LI 14:00 and IG 17:00 all posted.

**Missed rows:** 7 past-dated unposted, all Draft + Needs Review, so none rescheduled (blocked rule). X/LI: `tip-listiku-copy-presell-5-elements-20260510-20260928-li-0900` (LI 09-28), `static-ad-caraway_fry-pan-20260909-20260929-x-1300` (X 09-29), both carried over. Instagram (5 Drafts, single image each, 09-12 to 10-05): obvi hero, versed x2, checkout payment order, listiku. No webhook calls needed for them.

**Violation fixed (IG same-day):** `template-showcase-kura_pp-01-20260721-20260918-ig-1200` and `template-showcase-halos_ad-01-20260905-20260925-ig-1200` both sat on 2026-11-04 17:00. Moved the QA-clean one (kura_pp) to 2026-11-07 17:00. Reschedule webhook returned 200 "Accepted" but did NOT land (no execution in 7111659; hook queue 3 items). Applied the same two-cell change (E/F) directly through the Sheets API instead, re-read and confirmed. Re-check: no X/IG slot collisions, no IG >1/day, no LI same-day.

**Reschedule scenario 7111659 / hook 3613242:** flagged active, not paused, but not consuming its queue. 3 payloads waiting: two from 2026-09-19 08:43 and 08:45 (stale, unknown content) plus today's. Last real execution was 2026-09-17. Not stop/started by this run, because doing so could replay the two stale 09-19 payloads onto the Sheet. Ridwan to inspect.

**Step 1b, X char count:** 9 unposted Twitter captions checked, longest 271, 0 over 280, 0 empty, 0 new findings.
**Step 1c, Instagram format:** 27 upcoming IG rows checked, 0 single-image, 0 empty, 0 over 10, 0 mixed. Nothing trimmed.
**Step 1d:** `caption_fit.py`: 0 rows flagged.

**Spacing:** `space_queue.py` dry-run then real: 0 changes applied (plan already matched). Brand-gap violations 0. Supply gap: 53 empty X slots in its window. `sort_distribution_queue.py` re-run.

**Make health (6565331):** healthy. Active, executions every ~hour through 2026-10-09 16:01 UTC, all status 1, no errors since 10-03.

**Pacing (10-09 to 10-15):** 10 unposted rows (4 X+LI, 6 IG) = 1.4/day raw; X+LI only 0.6/day. Days with zero X/LI: 10-09 (already posted), 10-11, 10-12, 10-15. Only 1 upcoming LinkedIn row (10-13); X ends 10-29. About 11 more rows needed for 3/day. QA: window 1 clean / 9 blocked; backlog-wide 33 of 36 upcoming `Needs Review`.

**Verdict:** Make healthy, one IG violation fixed, no over-limit captions. Needs Ridwan: reschedule webhook queue stuck, queue nearly empty for X/LI, backlog 92% flagged.

## 2026-10-11 08:40 UTC (09:40 WAT) — health check (scheduled task run)

**Sheet read:** live Sheets API, 205 rows (152 Posted, 32 Ready unposted, 21 Retired ignored). No Draft rows left.

**Missed rows:** none. Nothing unposted is dated before today, so no webhook calls and no reschedules.

**Collisions / violations:** none. No X or IG same-slot collisions, no LinkedIn same-day, no IG more than 1/day.

**Step 1b, X char count:** 7 unposted Twitter captions checked, longest 266, 0 over 280, 0 new findings.
**Step 1c, Instagram format:** 24 upcoming IG rows checked: 22 single mp4 Reels, 2 image carousels (3 and 4 URLs). 0 single-image, 0 empty, 0 over 10, 0 mixed. Nothing trimmed.
**Step 1d:** caption_fit.py: 0 rows flagged.

**Reschedule scenario 7111659:** isActive = false now (was reported active on 10-09). Not reactivated, because no reschedule was needed this run and the hook queue still holds stale 09-19 payloads that could replay onto the Sheet. Ridwan to inspect before the next reschedule is needed.

**Make health (6565331):** healthy. Active, not paused, 0 errors. Executions every ~25 min at slot times through 2026-10-10 22:25 UTC, all status 1. Next run 2026-10-11 13:00 UTC. Side note: new scenario "Khutba Clips - Daily Facebook Post" (7875574) shows 13 executions and 13 errors since 10-10. Out of scope here, flagging only.

**Spacing:** no reschedules, so space_queue.py was only dry-run. 0 brand-gap violations. Supply gap: 50 empty X slots.

**Pacing (10-11 to 10-17):** 8 unposted rows = 1.1/day (10-11 IG; 10-12 none; 10-13 X+LI; 10-14 X+IG; 10-15 to 10-17 IG). About 13 more rows for 3/day. Zero X/LI posts on 10-11, 10-12, 10-15, 10-16, 10-17. X has 7 rows left (ends 10-29), LI has 1 (10-13). QA: 29 of 32 upcoming rows are Needs Review (91%), 3 are "not run through automated QA". Make ignores qa_status so they still fire.

**Verdict:** Make healthy, no fixable gaps. Needs Ridwan: queue nearly empty for X/LI, reschedule scenario 7111659 inactive, 91% of backlog flagged Needs Review.

## 2026-10-17 09:45 UTC (10:45 WAT) — health check (scheduled task run)

**MAKE UNHEALTHY:** main posting scenario 6565331 `isActive = false`. Executions list shows a manual "stop" by Ridwan on 2026-10-11 16:26 UTC; last execution 2026-10-11 16:25 UTC. Nothing has posted from the queue for ~6 days. Not reactivated by this run (a human stop, and the whole backlog is Needs Review). Reschedule scenario 7111659 also inactive (not reactivated, no reschedule done). Khutba Clips scenario 7875574 inactive and flagged invalid, out of scope.

**Sheet read:** live Sheets API, 205 rows (158 Posted, 26 Ready unposted, 21 Retired ignored).
**Missed:** 1, IG `template-showcase-halos_lp-01-2026-08-23-20260904-ig-1200` (was 2026-10-16 17:00), Needs Review so not rescheduled. The 10-17 17:00 IG slot will also be missed while Make is off.
**Collisions / violations:** none (no X/IG slot collisions, no LI same-day, no IG >1/day).
**Step 1b:** 5 unposted Twitter captions checked, 0 over 280.
**Step 1c:** 21 unposted IG rows checked, 0 format problems.
**Step 1d:** caption_fit.py run, see summary.
**Spacing:** no reschedules, space_queue not run.
**Pacing (10-17 to 10-23):** 7 rows = 1.0/day (IG 5, X 3 across window incl. ones listed). X ends 10-29, 0 LinkedIn rows left. All 26 upcoming rows are Needs Review / unreviewed QA.

# Distribution Health Check Log

Recurring health check for the Koolestpro Distribution Queue (Google Sheet) and the "Koolestpro Social Distribution" Make.com scenario (id 6565331). Each entry logged by `koolestpro-distribution-health-check`.

---

**Rotation rule (added 2026-09-27):** this file holds only the most recent 5 entries. When a new entry would push it past that, move the oldest entry(ies) to `docs/system/distribution-health-log-archive.md` (append, don't overwrite) in the same edit. Read only this file's tail for a normal health-check run; read the archive only if you need history older than what's here.

---

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
## 2026-10-25 08:40 UTC (09:40 WAT) — health check (scheduled task run)

**Sheet read:** live Sheets API, 259 rows (182 Posted, 55 Ready, 1 Draft, 21 Retired ignored). 54 upcoming unposted (31 IG, 19 X, 4 LI).

**Missed (2), both Needs Review, NOT rescheduled:** IG `tip-materialkitchen-first-screen-build-breakdown-20261009-20261019-ig-1200` (was 10-19 17:00); LI `tip-extra-costs-top-checkout-killer-20261009-20261102-li-0900` (Draft, was 10-23 14:00). No webhook calls.

**Collisions / violations (found, unfixable: every row involved is Needs Review):**
- IG same-slot (date 17:00): 10-26 (halos_pdp ...0820 + moult_hp ...1112), 10-31 (halos_pdp ...0821 + moult_hp ...1113), 11-04 (halos_ad ...0925 + halos_pp ...1117).
- IG >1/day also on 11-02, 11-05, 11-06, 11-20.
- LinkedIn same-day: none.

**Step 1b:** 19 unposted Twitter captions checked, longest 277, 0 over 280.
**Step 1c:** 5 upcoming IG rows are single images (will never post): tip-extra-costs-top-checkout-killer ...1109 (11-09), tip-allbirds-shipping-next-to-price ...1116 (11-16), tip-caraway-product-page-proof ...1123 (11-23), tip-v1ce-tap-card ...1130 (11-30), tip-owala-product-page ...1214 (12-14). Not fixed (flag only).
**Step 1d:** caption_fit.py: 0 rows flagged.

**Reschedule scenario 7111659:** inactive, not reactivated (no reschedule needed; stale hook queue risk noted 10-11).
**Make 6565331:** healthy. Active, not paused, 0 errors; executions at every slot through 10-24 22:25 UTC, all success. (It had been stopped by hand 10-11, so Ridwan turned it back on.) Next run 10-25 13:00 UTC. Khutba Clips scenario 7875574 active with 27 errors total, out of scope.
**Spacing:** no reschedules; space_queue dry run: 0 brand-gap violations, supply gap 92 empty X slots.

**Pacing (10-25 to 10-31):** 17 rows in 7 days = 2.4/day (10-25: 2, 10-26: 2, 10-27: 3, 10-28: 1, 10-29: 1, 10-30: 4, 10-31: 4). LinkedIn ends 11-04, X ends 11-29. About 4 more rows for 3/day. QA: 52 of 54 upcoming Needs Review, 2 not run through QA.

**Verdict:** Make healthy. Needs Ridwan: 2 missed rows stuck in review, 5 single-image IG rows that won't post, IG 2/day on 7 dates (3 same-slot), 7111659 inactive, 96% of backlog Needs Review.

---


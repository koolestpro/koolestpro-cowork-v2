# Distribution Health Check Log

Recurring health check for the Koolestpro Distribution Queue (Google Sheet) and the "Koolestpro Social Distribution" Make.com scenario (id 6565331). Each entry logged by `koolestpro-distribution-health-check`.

---

**Rotation rule (added 2026-09-27):** this file holds only the most recent 5 entries. When a new entry would push it past that, move the oldest entry(ies) to `docs/system/distribution-health-log-archive.md` (append, don't overwrite) in the same edit. Read only this file's tail for a normal health-check run; read the archive only if you need history older than what's here.

---

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

## 2026-10-29 ~10:30 UTC (11:30 WAT) — health check (scheduled task run)

**MAKE UNHEALTHY:** main posting scenario 6565331 `isActive = false`. Executions list shows a manual "stop" by Ridwan on 2026-10-28 14:39 UTC; last auto execution 2026-10-28 13:25 UTC (success). Nothing has posted since, so the 10-28 17:00 and 10-29 slots are being missed. Not reactivated by this run (a human stop). Reschedule scenario 7111659 also inactive, not reactivated (no reschedule done). Khutba Clips 7875574 active, 27 errors total, out of scope.

**Sheet read:** live Sheets API, 275 rows (194 Posted, 58 Ready, 1 Draft, 21 Retired ignored). 56 upcoming unposted (31 IG, 22 X, 3 LI).
**Missed (3), all Needs Review, NOT rescheduled:** IG `tip-materialkitchen-first-screen-build-breakdown-20261009-20261019-ig-1200` (10-19 17:00); LI `tip-extra-costs-top-checkout-killer-20261009-20261102-li-0900` (Draft, 10-23 14:00); IG `cro-fix-fishwife_shop-all-collection-20261025-20261028-ig-1200` (10-28 17:00, new). No webhook calls.
**Collisions / violations (found, unfixable: all rows Needs Review):** IG same-slot 11-04 17:00 (halos_ad ...0925 + halos_pp ...1117). IG >1/day also 11-02, 11-04, 11-05, 11-06, 11-12, 11-20. LinkedIn same-day: none.
**Step 1b:** 22 unposted Twitter captions checked, longest 277, 0 over 280.
**Step 1c:** same 5 single-image IG rows as 10-25 still unfixed (11-09, 11-16, 11-23, 11-30, 12-14). Flag only.
**Step 1d:** caption_fit.py: 0 rows flagged.
**Spacing:** no reschedules; space_queue dry run: 0 brand-gap violations, supply gap 89 empty X slots.
**Pacing (10-29 to 11-04):** 18 rows = 2.6/day (10-29:1, 10-30:4, 10-31:1, 11-01:2, 11-02:4, 11-03:1, 11-04:5). About 3 more for 3/day. LinkedIn ends 11-04 (3 rows), X ends 12-04. QA: 54 of 56 upcoming Needs Review (96%), 2 not run through QA.

**Verdict:** Make OFF since 10-28. Needs Ridwan: turn 6565331 back on if intended, 3 missed rows stuck in review, 5 single-image IG rows that won't post, IG 2/day on 7 dates, 7111659 inactive, 96% of backlog Needs Review.

---

## 2026-10-31 ~12:00 UTC (13:00 WAT) — health check (scheduled task run)

**Sheet read:** live Sheets API, 275 rows (198 Posted, 54 Ready, 1 Draft, 21 Retired ignored). 51 upcoming unposted (29 IG, 20 X, 2 LI).
**Missed (4), all Needs Review, NOT rescheduled:** IG `tip-materialkitchen-first-screen-build-breakdown-20261009-20261019-ig-1200` (10-19 17:00); LI `tip-extra-costs-top-checkout-killer-20261009-20261102-li-0900` (Draft, 10-23 14:00); IG `cro-fix-fishwife_shop-all-collection-20261025-20261028-ig-1200` (10-28 17:00); IG `template-showcase-halos_lp-01-2026-08-23-20260901-ig-1200` (10-29 17:00, new, missed while Make was off). No webhook calls.
**Collisions / violations (found, unfixable: every row Needs Review):** IG same-slot 11-04 17:00 (halos_ad ...0925 + halos_pp ...1117). IG >1/day on 11-02, 11-04, 11-05, 11-06, 11-12, 11-20. X: no same-slot collisions. LinkedIn same-day: none.
**Step 1b:** 20 unposted Twitter captions checked, longest 277, 0 over 280.
**Step 1c:** single-image IG rows (will never post, flag only): 11-02 tip-first-screen-leaks-before-bfcm ...; 11-04 template-showcase-halos_pp ...1117; 11-09 tip-extra-costs ...; 11-16 tip-allbirds ...; 11-23 tip-caraway ...; 11-30 tip-v1ce ...; 12-07 tip-three-mobile-checks ...; 12-14 tip-owala ... (8 upcoming, up from 5 on 10-29). Plus the 2 single-image missed rows above.
**Step 1d:** caption_fit.py: 0 rows flagged.
**Spacing:** no reschedules; space_queue dry run: 0 brand-gap violations, supply gap 85 empty X slots.

**Reschedule scenario 7111659:** inactive, not reactivated (no reschedule needed).
**Make 6565331:** healthy. Active, not paused, 0 errors. Ridwan restarted it 10-30 16:07 UTC; every execution since is success (last 10-30 22:25 UTC). Next run 10-31 13:00 UTC. Khutba Clips 7875574 inactive, out of scope.

**Pacing (10-31 to 11-06):** 19 rows = 2.7/day (10-31:1, 11-01:2, 11-02:4, 11-03:1, 11-04:5, 11-05:2, 11-06:4). About 2 more for 3/day. LinkedIn ends 11-04 (2 rows left), X ends 12-04. QA: 49 of 51 upcoming Needs Review (96%), 2 not run through QA.

**Verdict:** Make healthy again. Needs Ridwan: 4 missed rows stuck in review, 8 upcoming single-image IG rows that won't post, IG 2/day on 6 dates, LinkedIn queue nearly empty (2 rows), 7111659 inactive, 96% of backlog Needs Review.

---

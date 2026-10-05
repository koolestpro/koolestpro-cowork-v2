# Distribution Health Check Log

Recurring health check for the Koolestpro Distribution Queue (Google Sheet) and the "Koolestpro Social Distribution" Make.com scenario (id 6565331). Each entry logged by `koolestpro-distribution-health-check`.

---

**Rotation rule (added 2026-09-27):** this file holds only the most recent 5 entries. When a new entry would push it past that, move the oldest entry(ies) to `docs/system/distribution-health-log-archive.md` (append, don't overwrite) in the same edit. Read only this file's tail for a normal health-check run; read the archive only if you need history older than what's here.

---

## 2026-09-07 13:47 UTC (~14:47 WAT) — health check (scheduled task run)

**Sheet:** "Koolestpro Distribution Queue" — read via `read_file_content` (plain Markdown-table export, not base64), which still exceeded this session's per-call token limit and got auto-saved to a host-side tool-results file. Worked through it via a Grep `.{1,450}` re-chunk + `Read` in 25-line batches (no subagent, no CSV/base64 round-trip) — a new, slower but reliable method for this session specifically, since the usual gviz-query/subagent-CSV approaches from prior entries weren't available or hit rate limits this run. Full table read start to finish, 626 lines of chunked text, nothing skipped.

Counted 79 Twitter rows, 23 LinkedIn rows, ~41 Instagram rows (Instagram count is an eyeballed tally from manual scanning, not a query — treat as approximate; informational only per standing scope rule).

**Missed rows found (Twitter + LinkedIn): 0.** Every row with `scheduled_date` before 2026-09-07 already shows `status = "Posted"`. Nothing needed fixing on this front.

**Collisions/violations found and fixed (1):**

Scanned the entire unposted Twitter + LinkedIn backlog (not just the next 7 days) for same-platform same-`(date,time)` collisions, per the standing rule. Found a 3-way pileup on Twitter at **2026-09-11 23:00**:

| post_id | qa_status |
|---|---|
| template-showcase-kura_pp-01-20260721-20260830-x-2300 | clean (no HTML source, pre-existing captions — not a "Needs Review" flag) |
| idea-why-your-pdp-loses-sales-at-60-scroll-...-20260830-x-1800 | Needs Review (export-compat + X caption 536 chars) |
| cro-fix-bebemoss_toys-collection-20260818-20260830-x-1800 | Needs Review (2 claims to verify) |

Only the KURA post-purchase row is QA-clean, so it's the only one moved. Rescheduled to **2026-09-11 09:00** (a free standard slot that day — 09:00 and 13:00 were both open). Webhook call returned HTTP 200 / `Accepted`. The other two stay put — content isn't ready, a new time doesn't fix that.

Also found (not fixed, same reason): Twitter 2026-09-11 18:00 has **two** rows sharing the slot — `static-ad-v1ce_nfc-review-card-20260814-20260829-x-1300` and `template showcase-lumora_store-template-20260828-20260911-x-1300` — both Needs Review. Logging this as a found-but-unfixable collision; whichever clears QA first should be moved off the shared slot at that point.

LinkedIn: scanned the full backlog for the max-1-post-per-day rule — every upcoming LinkedIn date (09-07, 09-09, 09-11, 09-12, 09-14, 09-15, 09-16, 09-17, 09-18, 09-19) has exactly one row. No violations.

**Twitter caption character-count check (new standing instruction, applied this run):** independently counted every QA-clean, non-blocked upcoming/today Twitter caption against the 280-char limit (not just trusting existing `qa_status` text) — covers the 9 rows scheduled 09-07 through 09-11. All under 280 (longest was 276 chars, the Lumora free-offer post on 09-09 — worth a glance since it's only 4 chars of margin, but not a violation). No new over-limit captions found beyond what QA had already flagged on the blocked rows (`cro-fix-gainful...x-1800`: two variants at 292/319 chars; `idea-mobile-thumb-zone...`: 430 chars; `idea-why-your-pdp-loses-sales...`: 536 chars — all pre-existing flags, already blocking those rows for other reasons too).

**Make.com scenario health: ✅ Healthy right now.** `isPaused: false`, `isinvalid: false`, `islinked: true`. Most recent scheduled (`type:auto`) execution: 2026-09-07T13:28:42Z, status 1 (success), ~19 minutes before this check. Several manual runs by Ridwan this morning (08:30, 08:37, 08:38, 11:29, 13:10 UTC) all succeeded too.

**Two historical errors worth flagging, both self-recovered:** a `403 Forbidden` on the `ActionSendData`/http module at 2026-09-04 13:00 UTC (auto) and again at 2026-09-06 22:00 UTC (auto) — same failure shape as the credential-wipe bug fixed on 2026-08-31, though every execution since each error has succeeded, so this doesn't look like a recurrence of that specific bug so much as an occasional transient auth hiccup. Not currently blocking anything, but two 403s in 3 days is enough of a pattern to keep an eye on next run.

**7-day pacing (2026-09-07 → 2026-09-13, Twitter + LinkedIn):** 27 rows queued — 5, 3, 4, 6, 7, 2, 0 per day — averaging **3.86/day raw**, above the 3/day target. But only **13 of those 27 are QA-clean (1.86/day)** — 14 carry "Needs Review" flags. Same standing gap as every prior entry: raw volume looks fine, real postable pacing is under target. Would need roughly 8 more QA-clean rows across the window (or clearing 8 of the 14 blocked ones) to hit 3/day on a clean basis. Blocked-by-day: 09-07 (1 of 5), 09-09 (1 of 4), 09-10 (4 of 6), 09-11 (6 of 7), 09-12 (2 of 2 — both LinkedIn and Twitter blocked that day).

**Backlog-wide QA split (all upcoming rows, not just the 7-day window):** 41 unposted Twitter+LinkedIn rows total — **14 QA-clean, 27 blocked (66% blocked).** This is the highest blocked-share seen in this log's history. The blockers are almost entirely the same two recurring flag types: "claims to verify" (unsourced or unconfirmed factual statements in captions) and "manual-visual-pending" (images never actually eyeballed) — heavily concentrated in the Template Showcase / Store Template stream (Lumora, Meridian, HALOS, KURA pdp-01 rows). Clearing even a handful of these — most look like a quick claims-check + image glance rather than a rebuild — would do more for pacing than writing new content right now.

**Instagram (informational only, out of scope):** ~41 rows counted in the sheet. Not classified or touched, per standing scope rule.

**Verdict:** No missed-post gap. One real collision found and fixed (KURA post-purchase → 09:00 on 09-11); one more found but can't be fixed yet (both rows blocked). Twitter char-count check ran clean, no new violations. Make.com healthy right now, two isolated 403s in the last 3 days worth a glance next run. Pacing: raw count fine, QA-clean count soft (1.86/day) — the QA backlog (66% of the upcoming queue) is the actual bottleneck, same standing recommendation as every prior run.

## 2026-09-08 ~14:00 WAT — Instagram carousel error investigation + fix (ad hoc, Ridwan present)

Ridwan reported a Make.com error on today's Instagram post (a 7-slide Tips carousel, "thumb-zone-mobile-reach", scheduled 14:00) and asked for it to be investigated and fixed first, before anything else.

**Root cause found:** execution `ddef648826f34f9f9c81fdb26c91a31c` failed with `400 Bad Request` on module 301 (`http:ActionSendData`, the Instagram single-image `/media` call). Confirmed via the scenario blueprint: module 301 only implements a single-image post (filter checks the string ends `.png`/`.jpg`/`.jpeg`, then sends the whole `asset_urls` value as one `image_url` field). There is no carousel branch. The row's `asset_urls` was 7 Cloudinary URLs joined with `"; "` — matched the filter (last URL ends `.png`) but was garbage as an actual `image_url`, so Instagram's Graph API correctly rejected it.

**Fixed:**
- Patched `asset_urls` on the stuck row (and 3 other overdue rows sharing the same bug) to just the first/cover image URL via a direct Sheets API write.
- Found and fixed 13 MORE Instagram rows already in the sheet (dates through 2026-09-21) with the same multi-URL problem — all patched to single cover-image URLs. 17 rows total fixed.
- Root-caused and fixed `.ai-workflow/tools/feed_media.py`: Instagram rows with 2+ non-video images now only ever get the first URL written to `asset_urls`, preventing recurrence for every future carousel-format Instagram row.
- Discovered separately: the "Distribution Queue Reschedule" webhook scenario (id 7111659) had gone inactive — 9 reschedule calls for overdue Instagram rows returned HTTP 200 but silently did nothing until the scenario was reactivated. Reactivated it; all 9 rescheduled rows confirmed landed on re-read.
- Pushed all 9 past-due (2026-09-01 through 2026-09-07), unposted Instagram rows forward to open 17:00 slots between 2026-09-19 and 2026-09-30.
- Updated `koolestpro-distribution-health-check`'s SKILL.md: removed the "Instagram out of scope" rule, added Instagram to Posted/Missed/Upcoming/Blocked classification and slot-collision checks, added a permanent Step 1c (Instagram multi-image check) and a reschedule-scenario-liveness check as the first line of Step 2.
- Updated CLAUDE.md with the full incident writeup under the Instagram publishing section.

**Not done (flagged, not attempted):** real Instagram carousel support (child media containers + parent container + publish) does not exist in Make yet. Building it would mean hand-editing scenario 6565331's Instagram branch via a full-blueprint `scenarios_update`, which this project's own established doctrine treats as too risky to do blind on a production scenario — and there's no logged-in Make session available to do it via the UI either (no credentials entered on Ridwan's behalf). Until that's built, all Instagram carousel-format posts will go out as a single cover image rather than a swipeable multi-slide carousel. Flagged to Ridwan directly in chat.

**TikTok:** confirmed no send/publish provision exists or is planned to exist through Make.com — `tiktok_push_draft.py` only pushes to Ridwan's TikTok draft inbox (`/inbox/video/init/`), he posts by hand. This is unchanged and was not touched this session.

## 2026-09-29 15:40 UTC (16:40 WAT) — health check (scheduled task run)

**Sheet read:** live Sheets API, 195 rows (113 Posted, 73 Ready, 9 Draft). Note: Make posts any `Ready` row whatever its `qa_status` (54 posted Twitter rows carry a Needs Review flag), so "Blocked" below means QA-flagged, not "won't fire". `Draft` rows never fire.

**Twitter/LinkedIn missed rows:** 1. `tip-listiku-copy-presell-5-elements-20260510-20260928-li-0900` (LinkedIn, 09-28 14:00) is Draft + Needs Review (claims to verify), so not rescheduled. LinkedIn already posted `tip-cold-warm-hot-which-page` that day, so moving it anywhere would need an open LinkedIn day anyway. No Twitter row missed.

**Instagram missed rows:** 46 past-dated unposted rows (09-10 to 09-28), 44 QA-flagged. NOT rescheduled: Instagram is paused in Make (the `Instagrams` filter, per `.ai-workflow/tools/DISTRIBUTION.md`, 2026-09-27), so a new date would pass silently the same way. The 2 unflagged ones are `template-showcase-kura_pp-01-20260721-20260918-ig-1200` and `template-showcase-kura_li-03-20260721-20260904-ig-1200` ("not run through automated QA"). Same-time pile-ups at 17:00 on 09-12 to 09-20 (2-6 rows each) all sit in this past, paused set. Reschedule these as a batch when Instagram is switched back on.

**Collisions / LinkedIn same-day violations (upcoming):** none. Upcoming Twitter slots are all distinct, and the 8 upcoming LinkedIn rows each have their own day (09-30, 10-01, 10-02, 10-03, 10-04, 10-06, 10-07, 10-08). Nothing rescheduled, so no webhook calls this run.

**Step 1b, X char count:** 16 unposted Twitter captions checked. 1 over 280: `cro-fix-gainful_customize-your-protein-20260823-20260906-x-1800`, **319 chars, Ready, due 2026-09-30 14:00**. Already flagged in qa_status, so not a new finding, but it is Ready and will fire tomorrow and get rejected by X unless it's cut or set to Draft. No new over-limit captions.

**Step 1c, Instagram multi-image:** 6 unposted IG rows have multi-URL `asset_urls` (1 upcoming: `cro-fix-caraway_fry-pan-pdp-20260907-20260923-ig-1200`, 3 URLs, 10-07). NOT trimmed. The trim rule in this task's SKILL.md is out of date: the 2026-09-27 Make change added a native IG carousel route (310-317), and `feed_media.py` now deliberately keeps the full list. Trimming would undo that. The SKILL.md Step 1c needs updating.

**Step 1d, caption/image fit:** `caption_fit.py` reported 0 rows with problems (it reads local `queue.json`, which can lag the live Sheet).

**Reschedule scenario 7111659:** active (isActive true, not paused). No reactivation needed.

**Make health (6565331):** healthy. Every execution since 2026-09-27 13:00 UTC succeeded (latest 2026-09-29 13:25 UTC). The 10 runs on 09-26 ended "with warnings" on `MaxFileSizeExceededError` (http:ActionGetFile). That's the >5MB image issue fixed by the 09-27 Cloudinary transform, and it hasn't come back since.

**Pacing (09-29 to 10-05):** 23 unposted rows (13 Twitter, 5 LinkedIn, 5 Instagram), 3.3/day raw. Realistically posting: 14 Ready Twitter+LinkedIn rows = **2.0/day** (Draft rows never fire, and Instagram is paused). About 7 more Ready Twitter/LinkedIn rows would get this week to 3/day. QA-clean: **0 of 23** in the window, and 1 of 35 across the whole upcoming backlog (97% flagged). Most flags are the recurring "claims to verify" and "manual-visual-pending" on Template Showcase rows. Clearing flags is still the biggest lever.

**Verdict:** Make healthy, nothing overdue on X/LinkedIn that could be fixed, no collisions. Two things need Ridwan: the 319-char Gainful X post due tomorrow 14:00, and pacing at about 2 real posts/day with a backlog that's almost entirely QA-flagged. Separately, 46 Instagram rows are waiting to be rescheduled when IG is un-paused.

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

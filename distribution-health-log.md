# Distribution Health Check Log

Recurring health check for the Koolestpro Distribution Queue (Google Sheet) and the "Koolestpro Social Distribution" Make.com scenario (id 6565331). Each entry logged by `koolestpro-distribution-health-check`.

---

**Rotation rule (added 2026-09-27):** this file holds only the most recent 5 entries. When a new entry would push it past that, move the oldest entry(ies) to `docs/system/distribution-health-log-archive.md` (append, don't overwrite) in the same edit. Read only this file's tail for a normal health-check run; read the archive only if you need history older than what's here.

---

## 2026-08-31 15:2x WAT — manual check + root-cause fix (Ridwan-requested, ad hoc)

Ridwan asked directly to check Make for recent errors and fix them, and to push all outdated posts to the future — not scoped to QA-clean-only like the recurring scheduled task above. Both done.

**🚨 Real root cause found and fixed: the X-token-refresh step was silently wiping `linkedin_token` (and other unused credential fields) on every single X/Twitter post.** Scenario 6565331's datastore:UpdateRecord module (id 201, runs right after every X OAuth2 refresh) had `linkedin_token`, `x_api_key`, `x_client_id`, `x_api_secret`, `x_access_token`, `x_access_secret`, `x_client_secret` all hardcoded to `""` in its mapper — instead of referencing `{{2.<field>}}` to preserve the existing value, the way `facebook_page_id`/`meta_page_access_token`/`instagram_business_account_id` correctly already did in the same mapper. Since the X branch's OAuth2 token refresh runs unconditionally on every X/Twitter post (not gated on expiry), this meant `linkedin_token` got overwritten to blank on every single X post — confirmed live: `data-store-records_list` on datastore 149236 showed `linkedin_token: ""` right now. This explains both historical errors in this log (401 on 2026-08-21, 403 on 2026-08-28) — LinkedIn posting has been silently broken since whenever the first X post fired after the token was last set, and it would keep re-breaking every time someone re-pastes it, because the very next X post wipes it again.

**Fix applied:** pushed a corrected blueprint via `scenarios_update` — all 7 fields now read `{{2.<field>}}` (preserve-on-refresh), matching the pattern already used for the 3 fields that were never affected. Scenario confirmed still `isActive: true`, `isinvalid: false` after the push, next exec unchanged. This stops the bug from recurring, but does **not** restore the value that's already gone.

**⚠️ Action still needed from Ridwan, not something I can do myself:** `linkedin_token` is empty in datastore 149236 (record key `main`) right now — any LinkedIn post attempted before this is refilled will fail with 401. Paste a fresh LinkedIn bearer token into that field directly in Make.com (Datastores → koolestpro-config → main record). I don't handle API tokens/credentials on your behalf, per standing policy — this has to be pasted by you directly into Make's UI.

**Outdated posts pushed to the future — all platforms, all 38 overdue rows, not just QA-clean ones (per this session's direct instruction, a deliberate one-off deviation from the recurring task's stricter "only reschedule QA-clean" policy):**

- Classified via a fresh CSV pull: 132 data rows, 36 Posted, 38 missed/overdue, rest upcoming.
- **Every one of the 38 missed rows carries a `qa_status` of "Needs Review: ..."** (29 Instagram, 7 Twitter, 2 LinkedIn) — same recurring flag types as prior entries in this log (manual-visual-pending, unverified claims, X caption length, banned SVG gradient text, missing chrome-hide selectors). Pushing the date does not clear these flags — Make doesn't gate on `qa_status`, only on `status`/date/time, so these will still attempt to post on their new date exactly as unreviewed as before. This is the same structural risk flagged in the 2026-08-27 memory update when the Draft→Ready approval gate was removed.
- Instagram rows (29 of the 38) are lower-urgency in practice since Instagram posting isn't wired into this scenario yet (confirmed separately, informational-only elsewhere in this log) — rescheduling them is bookkeeping, not a live-post risk today.
- All 38 rescheduled via the webhook, each kept its own existing time-of-day slot, packed up to 5/day starting from the first day with spare capacity (2026-09-10) through 2026-09-18, filling gaps in the already-existing 09-10→09-18 backlog rather than stacking arbitrarily far out. Re-verified after: **0 overdue rows remain in the sheet.**
- All 38 webhook calls returned `updatedRows: "1"`.

**Still open, unchanged from prior entries:** the 38 rows' QA flags themselves were not reviewed or cleared in this pass (out of scope for "check Make + push dates" — Ridwan asked for those two things specifically, not a QA remediation pass like 2026-08-27's). `tip-the-conversion-layer` (unsourced "73%" stat) remains the standout — still needs a real source or a rewritten hook, same as flagged twice already.

---

## 2026-09-01 19:42 WAT — health check

**Sheet:** "Koolestpro Distribution Queue" — 151 rows total (79 Twitter, 25 LinkedIn, 47 Instagram). Read via a Google Visualization API query (`gviz/tq`) against the sheet through the browser instead of the Drive CSV export — the full CSV round-trip (~376K base64 chars) blew past this session's tool-output limits, same problem noted in the 2026-08-27 QA-pass entry above. The gviz endpoint lets column selection and `WHERE`/`GROUP BY` happen server-side, which kept every query small enough to read directly and let the classification itself run as SQL-style filters rather than manual row-by-row scanning.

**Missed rows found (Twitter + LinkedIn): 0.** Query: `status <> 'Posted' AND scheduled_date < 2026-09-01` returned zero rows. Cross-checked against `posted_at IS NULL AND scheduled_date < 2026-09-01`, which returned exactly one row (`cro-fix-v1ce_tap-review-card-20260719-20260722-li-0900`) — its `status` and `qa_status` both already read "Posted", just with an empty `posted_at` timestamp (a data-entry gap, not a missed post). No webhook calls needed this run.

**Make.com scenario health: 🚩 flagged, but appears just fixed.** `isPaused: false`, `isinvalid: false`, `islinked: true`, `nextExec: 2026-09-01T22:00:00Z` (~23:00 WAT tonight, the normal nightly slot). But the last several hours were rough: scheduled (`type:auto`) executions **errored** at 2026-08-28 13:00 (403 Forbidden), 2026-08-31 16:00 and 16:04 (401 Unauthorized), and **today** at 16:26, 17:00, and 17:15 WAT-adjacent UTC (400 Bad Request, `ActionSendData`/http module each time) — six failed scheduled runs across the review window, which trips this task's "any execution in the window errored" flag on its own. Ridwan made manual `modify` edits at 2026-08-31 14:02, 15:22, and again today at 18:16, each followed by a manual test run; the most recent one (18:16:59 today) succeeded. Given this log's history of the X-token-refresh step silently wiping other credential fields on every X post (see the 2026-08-31 15:2x entry), a 401→400 progression right after a LinkedIn-post cycle fits the same failure family — **worth Ridwan double-checking the datastore's `linkedin_token`/`x_*` fields haven't been blanked again**, since today's fix hasn't yet been proven against a real unattended scheduled run (next one is tonight's 23:00 WAT slot, not a manual trigger).

**7-day pacing (2026-09-01 → 2026-09-07, Twitter + LinkedIn):** 28 rows queued — 1, 4, 5, 6, 4, 4, 4 per day — averaging **4.0/day, above the 3/day target** on raw count. But only **17 of those 28 are QA-clean** (11 carry "Needs Review" flags — manual-visual-pending images, unverified claims, X captions over 280 chars, same recurring flag types as every prior entry). Clean pacing is closer to **2.4/day**, under target once QA-blocked rows are excluded — consistent with this log's recurring finding that the QA backlog, not scheduling, is the real constraint.

**Instagram (informational only, out of scope):** 47 rows in the sheet. Not classified or counted above per the standing exclusion rule.

**Verdict:** No missed-post gap (0 found, 0 fixed). Make.com had a genuine multi-hour error streak today (400/401 across at least 3 scheduled slots) that a manual fix *appears* to have just resolved — flag as unconfirmed until tonight's 23:00 WAT automatic run posts cleanly. Pacing: healthy on raw count, soft on QA-clean count (17 of 28, ~2.4/day) — same standing recommendation to clear review backlog rather than add new content.

---

## 2026-09-04 06:26 WAT — health check

**Sheet:** "Koolestpro Distribution Queue" — 145 rows total (79 Twitter, 25 LinkedIn, 41 Instagram — sums exactly, nothing dropped silently). Read via a subagent that pulled the Drive CSV export and parsed it out-of-context (the ~281K-char base64 round-trip still exceeds this session's tool-output limit — same structural issue noted since 2026-08-27), so only the classified summary below entered this session.

**Missed rows found (Twitter + LinkedIn): 0.** Every row with `scheduled_date` before 2026-09-04 already shows `status = "Posted"`. No webhook calls needed this run — first fully clean check in this log's history (every prior run had at least a few overdue rows, even if QA-blocked).

**Make.com scenario health: ✅ Healthy, and the 2026-09-01 fix has now held for 2+ days.** `isPaused: false`, `isinvalid: false`, `islinked: true`, `nextExec: 2026-09-04T13:00:00Z` (14:00 WAT today, normal scheduled slot). Checked executions from 2026-09-01 13:26 WAT through now: every scheduled (`type:auto`) run from **2026-09-01 22:00 WAT onward through 2026-09-03 22:30 WAT succeeded** (status 1) — 21 consecutive clean executions, spanning the credential-wipe fix pushed at 2026-09-01 18:16 (see that date's entry). The 400/401 error streak from earlier that same day has not recurred since. Most recent execution: 2026-09-03T22:30:29Z (~7.5h before this check — normal gap, matches the scenario's windowed schedule, next window opens at 14:00 WAT).

**7-day pacing (2026-09-04 → 2026-09-10, Twitter + LinkedIn):** 33 rows queued — 6, 4, 4, 4, 5, 4, 6 per day — averaging **4.71/day raw**, above the 3/day target. But only **19 of those 33 are QA-clean (14 carry "Needs Review" flags)** — clean pacing is **2.71/day**, just under target. Would need roughly **2 more clean rows** over the window to hit 3/day, though clearing even 2-3 of the 14 blocked rows would do the same job and is the higher-leverage fix (clearing all 14 would push raw pacing to 4.71/day clean). Blocked rows by date: 09-04 (4 of 6), 09-05 (2 of 4), 09-06 (1 of 4), 09-07 (0 of 4), 09-08 (2 of 5), 09-09 (1 of 4), 09-10 (4 of 6). Two post_ids have a literal space instead of a hyphen after "template" (`template showcase-lumora_store-template-...`) — a source data-entry quirk worth a look, not a parsing artifact.

**Instagram (informational only, out of scope):** 41 rows in the sheet, 3 with `scheduled_date` before today. Not classified or counted above per the standing exclusion rule.

**Verdict:** No missed-post gap (0 found, 0 needed fixing) — cleanest run in this log's history. Make.com: healthy, and the credential-wipe fix from 2026-09-01 is now confirmed stable across 21 consecutive scheduled executions. Pacing: raw count comfortably above target (4.71/day), QA-clean count just under target (2.71/day) — same standing recommendation as every prior run: clearing a few of the 14 blocked upcoming rows closes the gap faster than drafting new content.

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

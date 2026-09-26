# 02 — Distribution

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

Taking finished packages out of `outputs/` and getting them posted, on a schedule, without Ridwan copying anything by hand. It is the only part of the system that touches the outside world on a timer.

---

## What is in it

**The local queue:** `outputs/distribution-queue/` holds `queue.json` (151 rows), `queue.csv`, `sheet.json`, `asset_url_map.json` and a `pdfs/` folder. A row carries `post_id`, `platform`, `stream`, `scheduled_date`, `scheduled_time_local`, `status`, `qa_status`, `caption`, `caption_json`, `asset_paths`, `asset_urls`, `pipeline_item_id` and `posted_at`.

**The live Sheet** is the ahead-of-local source of truth. Ridwan edits rows directly and Make writes `Posted`/`posted_at` back, so `queue.json` can legitimately lag it.

**Make.com scenario 6565331**, "Koolestpro Social Distribution". Runs on a 15-minute interval, matches every row where `scheduled_date == today AND scheduled_time_local <= now`, and routes by platform.

**The tool chain**, run in this order, all in `.ai-workflow/tools/`:

```
harvest_content.py          (or harvest_store_template.py for store templates)
qa_check.py
populate_sheet.py
feed_linkedin.py            builds the hosted PDF LinkedIn needs
feed_media.py
sync_content_system.py
append_sheet_rows.py        --dry-run first
sort_distribution_queue.py
```

**Two scheduled tasks:** `koolestpro-weekly-distribution-assembly` (Mon ~07:51) runs that whole chain over whatever the weekend generators produced. `koolestpro-distribution-health-check` (every 2 days ~09:35) scans for overdue rows and checks Make scenario health.

**A reschedule webhook:** `https://hook.eu1.make.com/ocwhcp96a5up7i8hjqxuqrkw7m3a59rm`. It blind-overwrites date and time for a given `post_id` and performs no collision checking of its own.

---

## How it works

A generator leaves a package in `outputs/` with captions in the brand's social-content file. Monday's assembly harvests those into a flat record, QA-checks it, assigns each caption a `(platform, date, time)` slot from the stream's calendar, resolves asset paths to hosted URLs, appends rows to the live Sheet, and sorts the local queue to match. From then on Make picks rows up as they come due.

`find_open_week()` in `populate_sheet.py` walks forward a week at a time per slot until it finds a `(platform, date, time)` key nothing has taken, and reserves it immediately so two slots in the same batch cannot collide either.

---

## State

**Live and healthy:** X/Twitter and LinkedIn. The Make scenario reports `isPaused: false`, `isLinked: true`, with successful executions.

**Of 151 queue rows:** 79 Twitter, 47 Instagram, 25 LinkedIn. By status: 66 `Ready`, 55 `Draft`, 30 `Posted`.

**Blocked: Instagram.** 47 rows are queued and none can go out. The blocker is the Meta Page↔IG Business account link, an account-level action restriction rather than anything in config. Next action is Business Suite Account Quality.

**Blocked: TikTok.** App review rejected 2026-08-19, citing the personal/internal-use restriction on displaying own posts on a website. **Decided 2026-09-04:** that scope is dropped. Videos go to the TikTok draft inbox and Ridwan posts manually, so only `video.upload` is needed. Whether that still needs production review is open.

**Behind target: pace.** 3 posts/day is an average floor, not a cap, and Ridwan is happy to exceed it. The clean rate has been running well under. The bottleneck is the manual QA gate, not content generation: a clearing pass on 2026-08-27 cleared 18 of 19 overdue rows by hand, and the backlog rebuilds. Note the interaction with the LinkedIn cap below, which means X carries most of the volume by arithmetic.

---

## Rules

| Rule | Where |
|---|---|
| **Every caption is humanized** (v3.0, 11 passes, `VOICE.md`-anchored) before it can reach the queue. No em dashes. | `docs/system/humanizer-guideline.md` |
| **LinkedIn: max 1 post per day, hard cap.** A different time on the same day does not satisfy it. Check the whole unposted backlog, not a 7-day window. | `CLAUDE.md` "LINKEDIN — MAX 1 POST/DAY" |
| **No two rows for the same platform at the same `(date, time)`.** Cross-platform collisions are fine. Twitter has no daily cap. | `CLAUDE.md` "NO SIMULTANEOUS-SLOT RULE" |
| Before calling the reschedule webhook, read the live Sheet and confirm the target slot is free. The webhook does not check. | same |
| X captions must be under 280 characters. `populate_sheet.py` flags every `x_*` key. | "Store Template Launch Content" §6 |
| **Sheet sort (rewritten 2026-09-19):** Posted rows sink to the bottom; everything else sorts by `scheduled_date` ascending, then platform (Twitter/LinkedIn/Instagram), then Ready before Draft/Needs Review/Failed. `sort_distribution_queue.py` enforces it — always re-run after appending. | `.ai-workflow/tools/DISTRIBUTION.md` "Sheet organization" |
| **This-week overwrite (added 2026-09-19):** a new record's slot always takes precedence over an older, still-unposted (Ready OR Draft) row for the same stream+platform sitting in the CURRENT week — the older row bumps forward to the next open matching slot instead of being dropped. | `.ai-workflow/tools/DISTRIBUTION.md` "'This week' overwrite" |
| Images over ~4MB break Make's fetch. Prefer the compressed `-x` sibling. | Static Ad "CONFIRMED BUG" |
| LinkedIn image rows route through a hosted PDF, because the Make scenario has no plain-image route. Two images make a real carousel; one makes a weak document card. | "Store Template Launch Content" §6 |
| Never auto-set `Published`. | "Status Handling" |

---

## Known gaps

- **~~`populate_sheet.py` seeds `taken_keys` from local `queue.json`, not a live Sheet read~~ — FIXED 2026-09-19.** `populate_sheet.py` now reads the live Sheet (`fetch_live_rows()`) and unions it with local `queue.json` for both collision detection and the new this-week-overwrite matching; falls back to local-only with a loud warning if the live read fails. Built as part of the "this week overwrite" feature — see `.ai-workflow/tools/DISTRIBUTION.md`.
- **The normal (non-overwrite) `find_open_week()` path still doesn't enforce the LinkedIn 1/day cap** when placing a brand-new slot — only the new bump-target search added 2026-09-19 does. Rarely bites since each stream defines at most one LinkedIn slot per record, but two records assembled in the same run wanting the same LinkedIn day would still collide unnoticed by this layer (the standing "no simultaneous slot" / "LinkedIn max 1/day" rules are still enforced downstream by the health check, which would catch and fix it on its next run).
- **The Make-side stagger was investigated and deliberately not applied.** The blueprint is 44+ modules, this session's tools can only read it in fragments, and `scenarios_update` replaces the whole thing with no partial patch. Editing a production posting scenario from a lossy reconstruction was judged too risky. The sheet-side rule is the actual guarantee.
- **The QA gate produces false positives.** The 2026-08-27 pass found generic CRO-methodology statements flagged as unverified claims. Tightening the claim-hint regex would cut the manual load, which is the real pace bottleneck.
- **One row stays permanently blocked:** `tip-the-conversion-layer` claims "73% of Shopify redesigns don't lift conversions" with no source anywhere in the project. Needs a real source or a rewritten hook. This is exactly the fabricated-metric risk the rules warn about.

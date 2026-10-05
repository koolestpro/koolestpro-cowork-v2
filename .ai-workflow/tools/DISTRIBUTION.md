# V2 Content Distribution Pipeline — Tooling

Built 2026-07-14 from `koolestpro-v2-distribution-plan.md`. Turns the four content
GENERATION streams (Static Ad, CRO Fix, Template Showcase, Tips) into a scheduled,
cross-platform DISTRIBUTION system: harvest → QA → per-post queue → Google Sheet
mirror → content-system sync, with Ridwan as the approval gate and Make.com as the
eventual publisher.

## Division of labor (added 2026-09-21, Ridwan's instruction — read this first)

**Generation tasks make posts ready. Distribution assembly only picks and schedules.**

A generation task (Tips, CRO Fix, Static Ad, Template Showcase) is not done when it
finishes authoring HTML — it is done when it has ALSO driven the page's own
capture/export step and saved the real PNGs/videos to disk, per the "verify by
exporting" rule already standing everywhere else in this project. Only then does it
mark the item `"Created"` in SYNC_DATA.

Distribution assembly (this doc, run by `koolestpro-weekly-distribution-assembly`)
never renders, captures, or exports anything itself — no ad-hoc Playwright installs,
no manual screenshotting, no filling in for a missed export step. Its whole job is:
find items that are genuinely `"Created"` with real files already on disk, harvest
their captions/assets, QA them, and slot them into the calendar. If an eligible item
has no exported assets on disk — or a newer build superseded its registered `folder`
without ever being exported/registered itself — assembly skips it, names it plainly
in the run digest, and leaves it for the generation task to finish. It does not
attempt to fix the asset gap by rendering something itself.

## The chain (run these as the final steps of each generation task)

After a generation task finishes and its companion HTML + assets exist on disk:

```bash
cd <project-root>

# 1. HARVEST — pull caption variants + real asset paths out of the companion HTML
python3 .ai-workflow/tools/harvest_content.py <companion.html> \
    --out /tmp/harvest.json --merge-pipeline

# 2. QA — flag-not-block checks (files, banned CSS/SVG gradient text, claims, match)
python3 .ai-workflow/tools/qa_check.py /tmp/harvest.json --project-root .
#    -> then Claude Reads the images listed under manual_visual_pending and eyeballs them

# 3. POPULATE — expand into one Draft row per scheduled post (weekly calendar)
#    Omit --week-monday for normal use (see "Current-week-first scheduling" below).
#    Only pass it for a deliberate backfill into a specific week.
python3 .ai-workflow/tools/populate_sheet.py /tmp/harvest.json --project-root .

# 4. FEED — turn each LinkedIn row's local files into ONE hosted asset URL
#    (video -> Cloudinary .mp4 URL; multiple images -> hosted PDF for the
#    document-carousel route; text-only rows left empty). Writes asset_urls.
python3 .ai-workflow/tools/feed_linkedin.py --preset koolestpro_unsigned

# 5. SYNC — mirror the queue into the content system (additive, click-through preserved)
python3 .ai-workflow/tools/sync_content_system.py --project-root .

# 6. APPEND — push only the brand-new rows to the live Sheet (safe, additive-only)
python3 .ai-workflow/tools/append_sheet_rows.py --project-root .

# 6b. SORT — re-apply platform grouping (new rows land at the bottom, need re-sorting)
python3 .ai-workflow/tools/sort_distribution_queue.py --project-root .
```

## Sheet organization — unposted-first, by date, then platform, then Ready-first (REWRITTEN 2026-09-19, Ridwan's instruction)

**This replaces the 2026-08-27 platform-first sort described below the strikethrough note.** Ridwan wants to open the Sheet and see what's going out TODAY without scrolling, and to never have to hunt through a wall of already-posted rows to find live work. `.ai-workflow/tools/sort_distribution_queue.py` now sorts by, in order:

1. **Posted sinks to the bottom.** Every row with `status == "Posted"` drops below every row that isn't — that's the whole point, Ridwan only wants to see what's still actionable at the top.
2. **`scheduled_date` ascending** within the unposted block — today's posts first, then tomorrow's, and so on. This is the primary key now, not platform.
3. **Platform order** (Twitter, then LinkedIn, then Instagram) as the tiebreak within the same date.
4. **`status`**: Ready before anything else (Draft/Needs Review/Failed) as the final tiebreak within the same date + platform. (Needs Review/Failed live in the `qa_status` column, not `status` — `populate_sheet.py` always writes `status: "Ready"` regardless of QA outcome per its own docstring, so in practice "Draft" only ever appears when Ridwan manually downgrades a row himself. Confirmed with Ridwan 2026-09-19: those all share Draft's tier, none of this is hidden away.)

Recomputes three hidden helper columns fresh every run — `posted_tier` (Q), `platform_priority` (R), `status_priority` (S) — from columns K/D each time, so it's safe to re-run any time, including after a manual edit or a fresh batch of appended rows.

<details>
<summary>Superseded 2026-08-27 sort (platform-first) — kept for history</summary>

The live "Koolestpro Distribution Queue" sheet was grouped Twitter first, then LinkedIn, then Instagram at the bottom — Instagram isn't automated yet, so it was deliberately out of the way. Within each platform block, rows ran old→new by `scheduled_date`. The same script enforced this via a single helper column (`platform_priority`, column Q).

</details>

Two saved Filter Views exist for Ridwan's own use (Data → Filter views in the Sheets UI, doesn't affect what other viewers see):
- **"Needs Review"** — qa_status contains "Needs Review".
- **"Today"** — scheduled_date equals TODAY() (a live formula, always current, no manual updating).

**Known gotcha, cost real debugging time 2026-08-27:** a plain "Create a filter" (the shared, single, non-Filter-View kind) on this sheet silently blocks `sortRange` API calls — no error, 200 OK, zero rows actually move. `sort_distribution_queue.py` clears any basicFilter as its first step every run specifically because of this. If a future sort mysteriously does nothing, check for a regular Filter first.

**Also found the same day:** rows written by the reschedule webhook (Make.com scenario 7111659, `koolestpro-distribution-health-check`'s Step 2) or some older append paths can land in `scheduled_date` as plain text instead of a real Sheets Date — and a text-typed date cell sorts to the very end of its block regardless of its actual value. `sort_distribution_queue.py` re-normalizes the whole column via `USER_ENTERED` input every run to guard against this.

`koolestpro-distribution-health-check` (the standing health-check task, runs every 2 days) now ignores Instagram rows entirely in its classification, rescheduling, and pacing math, per the same instruction — Instagram sitting overdue there is expected noise, not a real gap.

## "This week" overwrite — new content jumps the queue (added 2026-09-19, Ridwan's instruction)

Ridwan keeps improving the quality of what he generates, and wants the newest version of a post to be what actually ships, not whatever happened to be queued first. Rule: when `populate_sheet.py` assembles a NEW record and one of its slots' natural placement for the CURRENT calendar week (Mon-Sun containing today) is already occupied by an older, still-unposted row for the **same `stream` + `platform`** — Ready or Draft, doesn't matter, only `status == "Posted"` is off-limits — the new content takes that slot and the old row gets bumped forward to the next open week for that same slot (same weekday + time-of-day), never dropped. "Keep pace" means nothing in the pipeline is lost, it just moves later.

Confirmed with Ridwan 2026-09-19 (four decisions, via AskUserQuestion):
- **Overwrite scope:** Draft AND Ready rows are both fair game — a newer post can bump one you've already approved, since the instruction was "always the best version, always."
- **Match rule:** same `stream` + `platform` (a new Tips/LinkedIn post can only bump an old Tips/LinkedIn post, never a CRO Fix/LinkedIn post also sitting this week).
- **Bumped row's destination:** the next open week for that exact slot (same weekday + time), reusing the existing `find_open_week()`-style search — never a far-future dumping ground.
- **Other statuses (Needs Review/Failed):** same tier as Draft for the SORT (see above) — for overwrite eligibility they're just "not Posted," same as Draft.

**Implementation:** `build_rows()` in `populate_sheet.py` now reads the LIVE Sheet (`fetch_live_rows()`) before placing each slot — not just local `queue.json` — because Ridwan's own Ready/Draft edits and any reschedule-webhook or manual date fixes land live first and can lag behind in local. If a slot's natural this-week placement is occupied by a matching unposted row, the new row takes it and the old row is re-homed via `_find_bump_target()` (walks forward week-by-week, and — unlike the pre-existing `find_open_week()` — also respects the LinkedIn 1-post/day cap for the row it's moving). The old row's new date/time is pushed straight to the live Sheet with a targeted `E:F` update (`push_bump_updates()`) in the same run, so local and live never drift on this. If the live Sheet can't be reached, this degrades gracefully to local-queue-only awareness with a loud warning rather than failing the run.

**Also closes a pre-existing known gap:** `populate_sheet.py`'s collision set (`taken_keys`) is now built from local UNION live rows, not local alone — previously a fresh run could pick a slot that collided with a row that only existed live (flagged but unfixed in `docs/system/02-distribution.md` since this stream was built). The live read added for the overwrite feature fixes this as a side effect.

**Flags:** `--no-overwrite` disables this behavior entirely (falls back to the pre-2026-09-19 "always find a fresh open slot" logic). `--dry-run` reports what would be built/bumped without writing `queue.json`, the CSV mirror, or the live Sheet — use this to preview before a real assembly run. Verified live 2026-09-19 in dry-run against a synthetic CRO Fix record: correctly identified an occupied Sunday Twitter slot this week, placed the (synthetic) new row there, and computed the bump target for the real displaced row one week forward with no collision — no writes were made since flag was `--dry-run`.

**Known limitation carried over, not new:** the normal (non-bump) `find_open_week()` path still doesn't enforce the LinkedIn 1/day cap when placing a brand-new slot — only the NEW bump-target search added by this change does. In practice this rarely bites because each stream defines at most one LinkedIn slot per record. Worth a follow-up if two records land in the same assembly run and both want the same LinkedIn day.

**Protected rows (added 2026-10-05, Ridwan's instruction).** Newer builds still go ahead of older backlog, but any row listed in `.ai-workflow/tools/protected_rows.json` (by `pipeline_item_id` or `post_id`) is never bumped by the overwrite. A new record whose natural slot is held by a protected row takes the next open slot after it instead. Seeded with the 14 rows pushed 2026-10-05 (Fly By Jing + Minimalist CRO Fixes). Only add to this list when Ridwan asks; it is not auto-filled per run. Health-check reschedules of missed rows are unaffected. Verified by dry-run with a synthetic CRO record: 0 bumps, new rows landed 10-21 onward.

## Current-week-first scheduling (fixed 2026-08-24, Ridwan's call)

`populate_sheet.py` used to always anchor every new item to `next_monday()` —
right for the normal Fri-Sun generation cadence, wrong the moment several items
get assembled in one run (a backlog catch-up, or several generators finishing
the same weekend). Every item's slots piled onto the identical single future
week, which is exactly what produced the Aug 31-Sep 6 pile-up in the 2026-08-24
assembly run and left the *current* week under-posted while a future week got
crowded.

Fixed: the default anchor is now `current_monday()` (the Monday of THIS week),
and `find_open_week()` resolves each CALENDAR slot independently — not the
whole item as one block. For each slot it walks forward one week at a time
from the current week and takes the first week where that slot's resulting
(platform, local_date, local_time) is both not in the past and not already
occupied by some other item's row. In practice: an item assembled on a
Monday with open Tip slots this week lands THIS week; if this week's Tip
LinkedIn/Instagram slots are already taken, it rolls to next week, and so on.
Slots within the same record reserve their own key as they're assigned, so
two slots in one item can't collide with each other either.

`--week-monday YYYY-MM-DD` still exists and now means "pin to exactly this
week, skip the search" — use it only for a deliberate backfill (e.g. the KURA
backfill pattern below), never for normal assembly.

## The feeder (feed_linkedin.py) — what makes LinkedIn self-driving

The Make LinkedIn scenario auto-routes on the `asset_urls` extension: empty→text,
`.mp4`→native video, `.pdf`→PDF document carousel. `feed_linkedin.py` is what
populates that column so nothing is pasted by hand:

- **video row** (asset_paths has an .mp4/.mov) → uploads the video to Cloudinary
  (`/video/upload`), writes the `.mp4` URL → video route.
- **carousel row** (2+ images, e.g. CRO before-after + annotated) → combines the
  images into a PDF (`img2pdf`), uploads to Cloudinary `/raw/upload`, writes the
  `.pdf` URL → document-carousel route.
- **text row** (no on-disk media) → leaves `asset_urls` empty → text route.

Idempotent via `asset_url_map.json` (keyed by file signature). Requires the
`koolestpro_unsigned` unsigned preset AND Cloudinary Settings→Security→"Allow
delivery of PDF and ZIP files" enabled (else `.pdf` URLs 401). Verified 2026-07-21:
CRO row → hosted PDF (200), Template Showcase row → hosted mp4 (200), both routing
correctly. After running it, re-import queue.csv into the Sheet (Replace current sheet).

Then (manual/connector step): re-mirror the local queue CSV to the Google Sheet so
Ridwan can review. The Sheet is `outputs/distribution-queue/sheet.json` (id + url).

## Files

| Script | Step | Does |
|---|---|---|
| `harvest_content.py` | 2 | Per-skill DOM parser (4 variants). Tab-based (CRO Fix, Tips: `#tab-*` + `<pre>`) and block-based (Static Ad, Template Showcase: `.copy-block` + `.x-post`). Detects skill by DOM structure, not just POST_TYPE. Emits `captions`/`captions_full`/`assets` + `content_system_folder`. `--merge-pipeline` writes captions/assets onto the matching `pipeline_data.json` item. |
| `qa_check.py` | 4 | Flag-not-block QA. Checks: file existence, banned export patterns (CSS `-webkit-background-clip:text`, SVG `fill=url(#grad)`, missing chrome-hide selectors, SVG `<text>` viewBox < 300px), claim spot-check (numbers/trust claims → verify), caption-asset match. Lists images for Claude to eyeball (`manual_visual_pending`). Writes `qa_status`. |
| `populate_sheet.py` | 5 | Expands one QA'd record into one row PER SCHEDULED POST per the encoded weekly calendar (LinkedIn 3/wk, Instagram 7/wk, Twitter rows). Durable local queue at `outputs/distribution-queue/queue.json` + `.csv`. Idempotent by `post_id` (never clobbers a Ready/Posted row's OWN identity — a `post_id` already in the queue is always skipped). **Since 2026-09-19:** also reads the live Sheet to detect a same-stream+platform unposted row already sitting in the CURRENT week and, if found, gives the new content that slot and bumps the old row forward instead (see "'This week' overwrite" above) — `--no-overwrite` to disable, `--dry-run` to preview. |
| `sync_content_system.py` | 8 | Attaches a `distribution` array (platform/date/time/status per post) to each matching item in `ridwan_content_system_updated.html`'s SYNC_DATA. Additive, preserves UI + all existing data, writes a `.bak`. Joins by id, falls back to slug. Never fabricates an item for an unmatched row. |
| `feed_media.py` | 4 | Instagram/Twitter's asset-hosting equivalent of `feed_linkedin.py` — uploads each image/video individually (never combined into a PDF), writes semicolon-joined `asset_urls` in `asset_paths` order. Same idempotent Cloudinary cache. Added 2026-07-29. **Cross-brand collision bug fixed 2026-08-19** — see below. |

### feed_media.py cross-brand asset collision — CONFIRMED BUG, FIXED 2026-08-19

`feed_media.py`'s Cloudinary `public_id` used to be built from `pipeline_item_id.split("-")[0:2]`, e.g. `"static-ad-v1ce_..."` → `"static-ad"`. That collapses EVERY Static Ad item (any brand) onto the identical Cloudinary path (`dist/static-ad/ad-1-problem-solution.png`), regardless of brand. Confirmed live: V1CE and Material Kitchen's rows, plus 2 backfill rows each for Obvi and Bebemoss, all ended up pointing at the same 5 URLs — whichever upload landed last silently became the image served for every other brand's post sharing that path. Caught via an md5 spot-check before anything got flipped to Ready (10 already-live Sheet rows for V1CE + Material Kitchen were still `status: Draft`, so no real post ever went out wrong).

**Fix:** `prefix` now uses the full `pipeline_item_id` (already unique per generated item) instead of the truncated 2-token split, so no two items can ever collide. **Repair procedure used** (keep this as the template if a similar collision is ever suspected again): purge any `asset_url_map.json` cache entries whose stored URL contains the old bad path, clear `asset_urls` on the affected local queue rows, re-run `feed_media.py` (now safe), verify with an md5 comparison between the freshly downloaded Cloudinary URL and the local source file, then push corrected `asset_urls` into the already-live Sheet rows via a targeted `values:batchUpdate` on column P only (never a full-row rewrite) — `append_sheet_rows.py` itself still only appends, it has no update path, so a collision repair after rows are already live always needs this manual batchUpdate step.
| `audit_mobile_strips.py` | — | Backstop sweep for the mandatory mobile-strip asset. Reports SOURCE pages, shipped PACKAGES and assembled QUEUE rows that lack one, splitting new gaps from the pre-2026-09-02 historical backlog. Exits non-zero only on a new gap. Run by the Monday `koolestpro-replo-cache-staleness-check` task. |
| `make_thumbnail.py` (in `../skills/page-presentation-kit/scripts/`) | 3 | Template-Showcase video thumbnail: device cover.png + brand glow + rotated headline + diamond accents + tagline. Sizes per platform. Uses Syne if `--font` given, else DejaVu Bold fallback. |

## Weekly calendar (encoded in populate_sheet.py `CALENDAR`)

- **LinkedIn** 9:00 ET — Mon Tips carousel · Wed CRO Fix 3-slide carousel · Fri Template Showcase video (+thumbnail). Never 2/day.
- **Instagram** 12:00 ET — Mon Tips (cross-post) · Tue/Thu/Fri Template Showcase reels · Wed CRO 3-slide carousel · Sat Static Ad 4-image carousel · Sun filler single.
- **Twitter** 9:00/13:00/18:00 ET — image singles/videos. **CRO Fix is the exception (2026-09-27, Ridwan):** its 3-slide carousel posts on X too (Wed 13:00, one post with 3 images), then each of its 4 graphics posts alone (Thu 09:00 cover, Fri 09:00 before/after, Sat 13:00 dark annotation, Sun 18:00 clear-bg annotation), each with its own caption key (`x_carousel`, `x_cover`, `x_ba`, `x_anno`, `x_anno_graphic`). **Resolved 2026-09-27:** Make now has a carousel route on X (modules 220-225: iterator over up to 4 URLs, media upload each, one tweet with all media_ids) and on Instagram (310-317: child containers, CAROUSEL parent, publish, 2-10 images). Any row whose `asset_urls` contains `; ` takes the carousel route; single-image routes now require no `; `. ~17-18 distinct/wk now, ramps to 21 with second-angle reposts as the library grows.
- **Mobile-strip X post added to every showcase stream (2026-09-02, Ridwan's call):** "Template Showcase", "Store Template" and "Store Template (Paid)" each gained an X #5 slot (Sun 11:00 ET) matching `mobile-strip`, with its own `x_glance` caption key so it cannot draw a recycled variant from the shared `x` pool. The asset is `{slug}-mobile-strip.png` (the whole page at mobile width, sliced into ~6 side-by-side columns — see CLAUDE.md "CORRECTED v8"). Ridwan's instruction was that it must never be skipped, so it is enforced in three places besides the calendar: `resolve_assets()` now prefers a compressed `-x` sibling over its full-resolution original for ANY matcher (so an oversized PNG cannot reach Make's fetch limit, the 2026-08-01 Bebemoss failure), the Monday assembly task builds a missing strip rather than shipping one fewer row, and `audit_mobile_strips.py` sweeps sources/packages/queue rows weekly.

- **Static Ad Twitter widened 3→5 (2026-08-19, Ridwan's call):** one post per distinct static-ad asset (4 individual angles + the combo showcase) instead of 3, scattered Mon/Tue/Wed/Fri/Sat at times no other stream already occupies — not clustered on Fri/Sat/Sun like before. Still only ~3 X caption variants get harvested per Static Ad run, so `populate_sheet.py`'s `caption_text()` reuses an earlier variant for the 4th/5th slot (flagged as a warning, not an error) until the static-ad-image skill starts writing more than 3.

## The Google Sheet + Make.com boundary (important)

The connected Google **Drive** connector can CREATE the Sheet but **cannot append or
edit rows in place**. So:

- **Durable source of truth = the local `queue.json`/`queue.csv`.** The Sheet mirrors it.
- **Row append + status write-back (Ready → Posted) is Make.com's job** — not built yet
  (Step 7). Open decisions before it can be built: polling interval, retry/error policy
  on a failed platform API call, and the exact per-platform post payload. The Make
  connector is connected; this needs a focused follow-up session with Make's MCP tools.

## Cloudinary asset_urls (populated 2026-07-21)

`upload-asset` on the Cloudinary MCP connector accepts local sandbox paths directly via
`file:///sessions/.../mnt/koolestpro-cowork-v2/...` (no base64 round-trip needed). Folder
convention used: `koolestpro/{brand-slug}/{descriptive-name}`. After upload, patch the
matching row(s) `asset_urls` field (semicolon-joined, same order as `asset_paths`) — this
is what Make.com actually needs to attach media to a LinkedIn/X/IG post, since Make can't
reach Ridwan's local filesystem. Existing rows created before 2026-07-21 mostly still have
an empty `asset_urls` — worth a backfill pass.

## harvest_content.py folder-scan bug (fixed 2026-07-21)

`collect_assets()` used to blindly scan the companion HTML's own folder for sibling
deliverables. For skills that share one flat folder across many unrelated posts (Tips —
`outputs/tips/`), this leaked other tips' assets (e.g. grabbed a PDF from a different tip).
Fixed: now prefers a dedicated `{slug}` or `{slug}-assets` subfolder (with word-prefix
fallback, e.g. slug `animation-budget-motion-conversion` matches folder
`animation-budget-assets`), and if no dedicated folder exists, filters the parent-folder
scan to filenames containing the slug rather than scanning everything.

## Kura backfill pattern (custom cadence, no local companion page)

2026-07-21: 4 of 5 KURA template-showcase pages (pdp, advertorial, listicle, post-purchase)
were queued directly from `kura-cloudinary-assets.json` (videos, already hosted) + captions
cached from `replo-pages-cache/kura-social-content.md` — no local HTML/companion page or
harvest record exists for these, so `harvest_content.py`/`populate_sheet.py`'s standard
CALENDAR cadence doesn't apply. Ridwan asked for a custom cadence instead of the default
weekly Template Showcase slot: LinkedIn+Instagram 1 page every 2 weeks, Twitter 1 post
every 3 days cycling cover/laptop/mobile per page. Rows were hand-built (see queue.json
rows with `caption_source_tab: "kura-social-content.json (backfill 2026-07-21)"`) and
`sync_content_system.py` correctly leaves them unmatched (no local pipeline item exists to
join to) rather than fabricating a content-system entry. Stills for these 4 pages don't
exist yet — Ridwan says they're in the `replo-rebuilds` folder, not connected in that
session; revisit once connected.

## Automatic weekly assembly (added 2026-07-29, corrected same day)

This whole chain used to only run when triggered by hand. `koolestpro-weekly-distribution-assembly`
(Monday ~07:51, ahead of `koolestpro-target-pool-refresh`) now runs it automatically: finds SYNC_DATA
items with `status: "Created"` and no `distribution[]` yet (i.e. generated but never assembled), and
runs harvest→qa→populate→feed_linkedin→feed_media→sync on each, entirely LOCAL.

**It does NOT touch the live Google Sheet.** First draft of this task tried to "re-import the CSV /
replace the sheet" — caught same day as a real near-miss: Ridwan is now working directly in the Sheet
(flipping Draft→Ready) and Make.com writes `Posted`/`posted_at` back into it, so the Sheet is often
MORE current than local `queue.json` for any row he's touched. A full replace would have silently
overwritten his approvals. The connected Drive connector can only create brand-new files or read
existing ones — it cannot update/append rows in an existing Sheet in place — so until a real append
mechanism exists (see "Keeping the Sheet and local queue in sync" below), the task's last step is to
hand Ridwan a paste-ready block of ONLY the brand-new rows for him to add to the bottom of the Sheet
himself. Draft→Ready approval is still 100% manual either way — this task never touches `status`.

## Keeping the Sheet and local queue in sync (built 2026-08-02)

Ridwan asked how to make the Sheet grow automatically without a manual export/paste round-trip each
time. Real constraint found by testing live: the Drive/Sheets tool available to Claude in this project
can `read_file_content` (works, but returns a lossy "natural language" markdown dump, not clean
structured rows) and `create_file` (creates a NEW file, does not update an existing one by id) — there
is no append/update-row tool on this connector. A Google Cloud service-account was tried first but hit
an org policy blocking service-account key creation (`iam.disableServiceAccountKeyCreation`, part of
Google's newer default security baseline) — rather than fight that policy, switched to an **OAuth
client** (type "TVs and Limited Input devices", project "Koolest Automation") authorized once via the
device-code flow (Ridwan visited google.com/device, entered a short code, approved as
`sirridwan721@gmail.com` — had to add himself as a Test User on the OAuth consent screen first, since
it's in "Testing" publishing status). Credentials live in this project's `.env`:
`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN`.

**`.ai-workflow/tools/append_sheet_rows.py`** is the resulting script — reads existing `post_id`s
straight from the live Sheet via the real Sheets API (`values.get` on column A), diffs against local
`queue.json`, and appends ONLY the rows that aren't there yet via `values.append`. Safe by
construction: it has no code path that can write to an existing row, so it cannot ever clobber a
Ready flip or a Posted write-back from Make. Verified live 2026-08-02 in `--dry-run` against the real
58-row sheet Ridwan had already imported by hand: correctly found 0 new rows (all 58 already present),
confirming the diff logic works against real data before any write path was exercised.

**Resolved same day — publishing status switched to production.** The OAuth consent screen originally
sat in "Testing" status, which caps refresh tokens at 7 days regardless of use — first token would
have needed re-authorizing weekly. Ridwan published the app to "In production" (Google Cloud Console →
"Google Auth Platform" → Audience → Publish App; no Google verification review was required for this
single-user app). A fresh refresh token was then minted via the device-code flow post-publish and
confirmed non-expiring (the token response no longer includes a `refresh_token_expires_in` field,
which is only present for Testing-status tokens) — `.env`'s `GOOGLE_OAUTH_REFRESH_TOKEN` now holds
this long-lived one. `koolestpro-weekly-distribution-assembly`'s paste-ready-block fallback in Step 6
still exists as defense-in-depth (e.g. if the token is ever manually revoked), but routine weekly
re-authorization is no longer expected.

## Live Sheet health audit + formatting pass (2026-08-02)

Ridwan asked, ahead of Monday's next append, to confirm the live 58-row Sheet was in good
health and to make it easier to review (filters, sort, dropdowns, readable captions) before
more rows land on top of it. Two real findings, both fixed directly in the live Sheet via
the Sheets API (`append_sheet_rows.py`'s OAuth token, ad-hoc `batchUpdate`/`values.get` calls
— no new script needed since these were one-off repairs, not a recurring step):

**1. Asset-size/type mismatch (the originally reported bug) — audited, zero remaining
instances.** Threaded HEAD/GET requests against all 69 unique asset URLs referenced in the
sheet, checked against X's real limits (5MB image / 15MB gif / 512MB video, no PDF/
octet-stream) confirmed Ridwan's own manual fix for the "8.8MB LinkedIn PDF matched to an X
row" bug was fully effective — no other rows have an oversized or wrong-type asset on a
Twitter row.

**2. Stale over-280-char captions — found and fixed.** 5 rows (2 CRO Fix `x_angles`, 3
Template Showcase) still carried the pre-2026-07-29-fix caption text in the LIVE sheet,
because Ridwan had imported the sheet from a local export taken *before* that session's
caption-splitting fix propagated, and `append_sheet_rows.py` is deliberately append-only —
it never touches an existing row, so the corrected text never reached rows he'd already
imported. Pushed the already-known-correct caption text into both the `caption` and
`caption_json` columns for these 5 rows via a targeted `batchUpdate`. Two of the five were
still `status: Draft/Ready` (not yet posted); **three were already `status: Posted`** —
worth Ridwan spot-checking the real @koolestpro account for those specific timestamps to
confirm whether they went out truncated or were already caught and reposted by hand.

**3. Sheet reformatted for review.** Frozen header row, a basic filter across the full
A1:P59 range, sorted by `scheduled_date` → `scheduled_time_local` → `platform` (verified
monotonic across all 58 rows, no out-of-order rows), dropdown data validation on `platform`
(LinkedIn/Instagram/Twitter), `status` (Draft/Ready/Posted/Needs Review/Failed), and
`stream` (Tip/CRO Fix/Static Ad/Template Showcase/Case Study/Personal), text-wrap + top
alignment on the long-text columns (`asset_paths`, `caption`, `qa_status`,
`content_system_folder`, `caption_json`, `asset_urls`), auto-resized row heights so wrapped
captions are readable without manual row-dragging, and reasonable fixed column widths per
column. `qa_status` was left as free text (not a dropdown) — its values are long
per-row diagnostic strings, not a fixed enum.

**Not a recurring script on purpose.** This was a one-time repair-and-reformat pass on data
that had already diverged from local. Going forward, `append_sheet_rows.py` stays the only
automated write path (new rows only); a formatting pass like this one would only be needed
again if the Sheet's structure changes (new columns) or a future bug leaves another batch of
stale cells behind.

## X caption length / multi-variant tab bug (fixed 2026-07-29)

CRO Fix's "Twitter Angles"/"Twitter Thread" tabs (and Tips' equivalents) pack multiple standalone
tweet variants into one `<pre>` as plain text (`"Tweet A (...):"`, `"ANGLE A:"`, `"N/ "` numbered
lines) rather than separate DOM elements. `harvest_content.py` now splits these into real lists
instead of one glued blob; `populate_sheet.py`'s 280-char check now runs unconditionally instead of
only on list-typed values; `qa_check.py` now scans `captions_full`'s x_angles/x_thread/x_singles
directly instead of only the (often-empty, for tab-based skills) compact `captions.x` field. CRO
Fix's Wed "thread" slot is downgraded to a normal single tweet (Make has no real reply-chained
threading yet) drawing from the same pre-written `x_angles` pool as the Fri/Sun slots. Full narrative
in `docs/koolestpro-content-operating-plan.md`'s 2026-07-29 Build Log entry.

## Known join fragility

CRO Fix (and some Tips) build their pipeline id from a click-time date, so the harvest
id may carry today's date instead of the canonical SYNC_DATA id. `sync_content_system.py`
handles this with a slug fallback. `populate_sheet.py` rows still carry the harvest id;
if a cleaner join is ever needed, have harvest read the existing pipeline item id by
slug+type rather than reconstructing the date.


## Multi-image posts + the 5MB guard (2026-09-27)

- **Carousels in Make (scenario 6565331).** X: route 220-225, up to 4 images in one tweet. Instagram: route 310-317, native carousel up to 10 images (Instagram is still PAUSED via the `Instagrams` filter; the route is ready for when it is re-enabled). Trigger: `asset_urls` contains `; `. Single-image routes (203, 301) and video routes (207, 304) got an extra `does not contain "; "` condition so a carousel row can never post twice.
- **feed_media.py** no longer trims Instagram rows to the cover image. Every platform gets the full `; `-joined list, capped at 4 (X) / 10 (Instagram). The 6 queued Instagram carousel rows were re-filled with their full URL lists locally (asset_url_map cache keys are path-based and missed on the VM path, so the URLs were rebuilt from the deterministic `dist/{pipeline_item_id}/{name}` public_ids and each checked for HTTP 200). Same day, columns H (asset_paths) and P (asset_urls) for all six were pushed to the live Sheet with a targeted batchUpdate and re-read to confirm they match local. `cro-fix-tapro_google-review-cards` was trimmed from 18 mixed paths to its real 8-slide carousel (`koolestpro_tapro_google-review-cards_slide1-8`, the canonical `CRO-TAPRO-CAROUSEL` set; `slide-1..8` were byte-identical duplicates and the ba/anno graphics post separately). Several of these rows carry past `scheduled_date`s, so they will not fire until rescheduled when Instagram is un-paused.
- **Under 5MB, always.** Every image Make downloads or hands to X/Instagram/Facebook now goes through a Cloudinary delivery transform: `replace(url; "/image/upload/"; "/image/upload/c_limit,w_2160,h_2700,q_auto:good,f_jpg/")`. Tested on a real queued asset: 717 KB PNG → 227 KB JPEG. A slide at 1080×1350 lands well under 1MB. Non-Cloudinary URLs pass through unchanged. `feed_media.py` also shrinks any local image over 4.5MB to a JPEG copy before upload (`shrink_if_needed`). Videos are untouched (X video limit is 512MB).
- Backup of the pre-change blueprint: take a fresh `scenarios_get` if a rollback is ever needed; only modules 203, 204, 207, 301, 304, 401 changed, everything else is byte-identical.

## Instagram re-enabled, carousels + videos only (2026-10-05, Ridwan)

- Make 6565331 edited via full-blueprint `scenarios_update`, then re-fetched and diffed: only 3 changes. Router 300 filter `Instagrams` → `Instagram`. Single-image route 318 gets an impossible `platform = "Instagram-single-image-off"` condition in every OR group (single images stay off). Reel publish wait (305) 30s → 90s.
- 26 overdue Ready IG carousels/videos rescheduled one per day at 17:00 (10-05 18:00 to 11-06), written to the live Sheet and local `queue.json`, verified on re-read, no same-slot collisions.
- All pending Caraway CRO rows (`cro-fix-caraway_fry-pan-pdp-*`, 4 rows: 2 X, 1 LI, 1 IG) deleted from the Sheet and from `queue.json`/`queue.csv`. Backup: `outputs/distribution-queue/deleted/caraway-cro-rows-deleted-2026-10-05.json`. The one already-posted Caraway CRO row was kept.

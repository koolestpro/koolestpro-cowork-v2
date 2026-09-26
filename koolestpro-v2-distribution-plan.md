# Koolestpro Content Distribution V2 — Plan

## Goal

Take the four content-generation streams already running in `koolestpro-cowork-v2` (Static Ad, CRO Fix, Template Showcase, Tips) and turn them into a fully scheduled, cross-platform distribution system — LinkedIn, Instagram, and Twitter/X — with content queued in a Google Sheet, posted automatically via Make.com, and gated by a human approval step so nothing goes live unreviewed.

## Context

V1 (already built and scheduled) solved content *generation*: four weekly tasks produce reviewable buffer folders under `outputs/`. Nothing in V1 posts anywhere — everything sits waiting for Ridwan to manually post it, and captions already exist inside each generator's companion HTML but are never extracted anywhere usable by automation. V2 closes that gap: a defined weekly calendar (what goes where, which day, what time), a harvest step that pulls the caption text and asset paths already being generated into structured records, an automated QA pass, a Google Sheet as the operational queue, and Make.com as the thing that actually publishes — all while keeping Ridwan as the final approval gate. Ridwan's Claude/Cowork usage credits reset weekly (Friday ~2-3pm ET) and are typically exhausted by Wednesday, dead on Thursday — this shapes when generation is allowed to run.

## Process Overview

1. Reschedule the four existing generation tasks across Fri/Sat/Sun (credit-safe window), one core stream per day.
2. Each generation task ends with three new steps: harvest captions/assets out of its companion HTML, run an automated QA pass, and write pre-populated rows into the Google Sheet as `Draft`.
3. Ridwan reviews Draft rows and flips approved ones to `Ready`.
4. Make.com polls the Sheet, posts only `Ready` rows at their scheduled time, marks them `Posted`.
5. A sync step keeps `ridwan_content_system_updated.html` mirroring the Sheet, so it survives as a visual, click-through archive rather than a second manually-maintained source of truth.
6. A lightweight reminder task flags when the `replo-rebuilds` local sync cache has gone stale, since a scheduled task cannot refresh it automatically (platform limitation — see Dependencies).

## Weekly Content Calendar

All times are US Eastern (ET) — confirmed target audience is primarily US/UK/Europe.

### LinkedIn — 3x/week, max 1 post/day, 9:00 AM ET
| Day | Content |
|---|---|
| Mon | Tips carousel |
| Wed | CRO Fix 2-slide carousel: slide 1 = before-after graphic, slide 2 = annotated graphic (packaged as-is, no new artwork) |
| Fri | Template Showcase video, posted with its new custom thumbnail (see Step 3) |

Rule: never post twice on LinkedIn the same day — the algorithm suppresses the earlier post's reach if a second post follows within 24h. This is why CRO Fix's two single images were combined into one carousel rather than posted separately.

### Instagram — 7x/week (daily), 12:00 PM ET
| Day | Content |
|---|---|
| Mon | Tips carousel (cross-post, same asset/time as LinkedIn) |
| Tue | Template Showcase Reel #1 |
| Wed | CRO Fix 7-slide narrative carousel (Instagram-exclusive — the long-form case study, distinct from Wednesday's LinkedIn 2-slide carousel) |
| Thu | Template Showcase Reel #2 |
| Fri | Template Showcase Reel #3 / cover video (cross-post, same asset/time as LinkedIn) |
| Sat | Static Ad carousel (4 images assembled into one swipeable carousel, Instagram-exclusive) |
| Sun | Filler single — a Static Ad single image or a Template Showcase still (`preview.png` / `full-mosaic.png`), whichever wasn't used yet that week |

Known limitation: content-mix best practice favors ~60-70% Reels, but Template Showcase only produces 3 videos/week, so Reels cap at 3/7 slots for now. This improves automatically as video output scales — no action needed, just don't expect the ideal ratio yet.

### Twitter/X — 21x/week (3/day), 9:00 AM / 1:00 PM / 6:00 PM ET
- Every slot carries an image. No text-only posts, no hot-takes, no stat-pulls.
- Carousel-format assets never go to Twitter (CRO 7-slide carousel, Tips carousel) — single images, videos, and threads only.
- Supply: 13 unique visual assets/week (4 Static Ad singles + 1 combo, before-after, annotated, 3 Template Showcase videos, 3 Template Showcase stills).
- The remaining ~8 weekly slots are filled by reposting assets a second time with a **different caption angle** — pull from the "Twitter Angles" / "Hook Variations" / "X Singles" tabs each generator already writes (see Step 1). Prioritize the most generic/reusable assets first (Template Showcase mobile mockups).
- **Wednesday**, one of the three daily slots is replaced by the CRO Fix Twitter thread (4-8 tweets, sourced from the existing "Twitter Thread" tab in Skill D's output) — it does not add a 4th post that day.
- Honest caveat: 21/week assumes enough repost variety to avoid feeling repetitive. Right now supply realistically supports ~17-18 distinct-feeling posts/week; it reaches 21 comfortably once a few more weeks of assets have accumulated in the library, per Ridwan.

## Detailed Steps

### Step 1: Reschedule the four generation tasks
**What happens:** Move existing scheduled tasks to a one-stream-per-day spread across the credit-safe window (Friday afternoon through Tuesday), leaving Wednesday/Thursday untouched.
**Input:** Cowork's scheduled-task editor (`mcp__scheduled-tasks__update_scheduled_task`).
**Output:** Updated cron schedules.
**Decisions:** Already made — see table below. No further decisions needed.
**Owner:** Whoever executes this plan (Claude/Cowork agent).
**Notes:** Do this before touching anything downstream — every later step assumes this schedule.

| Task | Old schedule | New schedule |
|---|---|---|
| `koolestpro-tips-weekly` | Sun 09:20 | **Fri**, keep ~09:20 or align with Static Ad's new Friday slot, staggered by a few minutes |
| `koolestpro-static-ad-weekly` | Sat 09:02 | **Fri**, ~09:00 |
| `koolestpro-template-showcase-weekly` | Sun 09:07 | **Sat**, ~09:00 |
| `koolestpro-weekly-cro-fix` | Sat 09:06 | **Sun**, ~09:00 |
| `koolestpro-target-pool-refresh` | Fri 08:09, weekly | **Mon**, biweekly |

New task to create:
| Task | Schedule | Purpose |
|---|---|---|
| `koolestpro-replo-cache-staleness-check` | Weekly, any day (suggest Mon, paired with target-pool-refresh) | Checks `replo-pages-cache/` and `replo-rebuilds-pages.json` last-modified date; if stale (>2 weeks), messages Ridwan to refresh it next time both `koolestpro-cowork-v2` and `replo-rebuilds` are connected in the same session. Does **not** attempt the refresh itself — a scheduled task's single-folder limitation makes that structurally impossible (confirmed via live "Run now" test on 2026-07-13 and reconfirmed against current Cowork docs on 2026-07-14). |

### Step 2: Harvest captions and assets
**What happens:** Immediately after each generation task finishes, parse its companion HTML output for the caption/copy tabs it already writes, and the real file paths of every generated asset. Write this into a structured record (JSON), one per generated content piece.
**Input:** The companion HTML file each skill produces (e.g. `outputs/cro-fixes/{slug}_content.html`, `outputs/templates/{slug}_{date}/index.html`, `outputs/tips/{slug}.html`, `outputs/static-ads/{slug}_{date}/index.html`).
**Output:** A structured record per content piece — see schema below. This also finally populates the `captions`/`assets` fields on the pipeline JSON item that CLAUDE.md already defined but nothing has ever filled in.
**Decisions:** None open — confirmed to run immediately per-task, not as a weekly batch rollup.
**Owner:** A new script per project, e.g. `.ai-workflow/tools/harvest_content.py`, called as the final step inside each generation task's own procedure doc (`weekly-pipeline.md` and equivalents).
**Notes:** Caption tab IDs are **not identical across skills** — confirmed by direct inspection of real output files:
- CRO Fix (`v1ce_tap-review-card_content.html`): `#tab-linkedin`, `#tab-ig`, `#tab-hook`, `#tab-twitter-angles`, `#tab-twitter-thread`
- Tips (`shopify_page_types_carousel.html`): `#tab-li-long`, `#tab-li-hook`, `#tab-x-thread`, `#tab-x-singles`, `#tab-ig`
- Static Ad (`{slug}_pipeline` companion, e.g. Obvi): `.copy-block` sections titled "LinkedIn Caption" and "X Posts" (3 `.x-post` divs), no hook/thread tabs
- Template Showcase (`kura_hp-01` companion): same pattern as Static Ad — "LinkedIn Caption" + "X Posts" (3 `.x-post` divs)

The harvest script needs a per-skill parser (4 variants) rather than one generic selector, because the DOM structure genuinely differs. Match by known ID/class per skill, not by guessing.

### Step 3: Video thumbnail generation (new, Template Showcase only)
**What happens:** Extend Page Presentation Kit's output with a dedicated thumbnail graphic per video — the existing `cover.png` device-mockup composition, plus a headline text layer, decorative diamond/square line accents, and a bottom tagline, matching Ridwan's existing Instagram grid style (dark background, bold white Syne-weight headline with an emoji, brand gradient glow).
**Input:** The already-calibrated device frames (`assets/frames/macbook-pro.png`, `iphone-frame.png`), the week's screenshot/video captures, a headline.
**Output:** One thumbnail PNG per video (or one shared thumbnail if laptop+mobile videos are posted together), sized appropriately per platform's native video-thumbnail requirements.
**Decisions:** Headline text is **rotated** from a fixed set of templates (confirmed) — e.g. "Shopify Store Redesign that Converts 🔥", "5 [Category] Fixes That Bring More Sales", "5 Product Page Fixes That Build Trust" — with the brand/category slotted in per week, not freshly authored each time.
**Owner:** Extend `.ai-workflow/skills/page-presentation-kit/scripts/` with a new compositing script; brand/headline selection is Claude's job (content-brief phase), the actual image compositing is mechanical (PIL/HTML), consistent with the project's existing Claude-vs-DeepSeek split.
**Notes:** This is new work, not yet built — flag it as its own implementation task, separate from the scheduling changes in Step 1.

### Step 4: Automated QA pass
**What happens:** After harvesting, before writing to the Sheet, run an automated quality check on every generated piece. On failure, the row still gets written to the Sheet but flagged `Needs Review` with the specific issue noted — QA never silently blocks content from reaching the queue.
**Input:** The harvested record + the actual generated files.
**Output:** A QA status (`Pass` / `Needs Review: <reason>`) attached to each record before it becomes a Sheet row.
**Checks to run:**
1. **File existence** — every asset path in the harvested record resolves to a real file on disk.
2. **Export-compatibility scan** — grep the source HTML/CSS for banned patterns already documented in CLAUDE.md: CSS gradient text (`-webkit-background-clip: text`), missing chrome-hide selectors, SVG viewboxes under 300px on stat/headline text.
3. **Visual inspection** — Claude actually opens the generated images/thumbnails (via the Read tool, which can view images) and checks: dark-theme consistency with the established brand look, headline legible at thumbnail scale, no obviously broken/garbled layout, device bezels correctly centered and framed (Template Showcase specifically, given the 2026-07-13 unframed-video incident).
4. **Claims spot-check** — any specific number, brand name, or trust claim in a caption gets flagged for verification against the real audit brief or live source site, rather than auto-trusted (per the V1CE HSBC/IBM near-miss).
5. **Caption-asset match** — the caption text actually describes what's in the paired asset, not a stale leftover from a different run.
**Decisions:** Flag-not-block, confirmed.
**Owner:** New script, e.g. `.ai-workflow/tools/qa_check.py`, called at the end of the harvest step.
**Notes:** This directly operationalizes lessons already learned the hard way in this project (documented in `docs/koolestpro-content-operating-plan.md`'s Build Log) — the goal is to stop relying on Ridwan or Claude remembering to check manually.

### Step 5: Google Sheet — the operational queue
**What happens:** Once a stream's generation + harvest + QA finishes, a script writes one row **per scheduled post** (not per content piece) — meaning a single generated CRO Fix piece might produce a LinkedIn row, an Instagram row, and several Twitter rows, each with its own day/time/caption-variant already assigned per the Weekly Content Calendar above.
**Input:** Harvested + QA'd records, the fixed weekly calendar/template.
**Output:** Populated Sheet rows, status `Draft`.
**Proposed schema (columns):**
| Column | Example |
|---|---|
| `post_id` | `cro-v1ce-tap-review-card-20260719-li` |
| `pipeline_item_id` | matches the id already used in `ridwan_content_system_updated.html` |
| `stream` | `CRO Fix` |
| `platform` | `LinkedIn` |
| `scheduled_date` | `2026-07-22` |
| `scheduled_time_et` | `09:00` |
| `asset_path(s)` | `outputs/cro-fixes/v1ce/koolestpro_v1ce_before-after.png, ...annotated.png` |
| `caption` | full text, pulled from the matching harvested tab |
| `caption_source_tab` | `tab-linkedin` (traceability back to which variant was used) |
| `status` | `Draft` / `Ready` / `Posted` / `Needs Review: <reason>` |
| `qa_status` | `Pass` / `Needs Review: <reason>` |
| `posted_at` | filled by Make.com after posting |
| `content_system_folder` | the real HTML file path, e.g. `outputs/cro-fixes/v1ce_tap-review-card_content.html` — this is what makes the content-system click-through work (Step 7) |
**Decisions:** Pre-populated per-post rows (not lean/decide-at-runtime), confirmed.
**Owner:** New script, e.g. `.ai-workflow/tools/populate_sheet.py`, using the Google Sheets connector.
**Notes:** Building this script is real implementation work — flag as its own task.

### Step 6: Human approval
**What happens:** Ridwan reviews `Draft` rows (and especially anything QA flagged `Needs Review`) and manually flips approved rows to `Ready`.
**Input:** The Sheet.
**Output:** Rows marked `Ready`.
**Decisions:** Manual review confirmed, no auto-approval tier for any content type. No fixed cadence specified — Ridwan does this on his own schedule, but it needs to happen before each row's `scheduled_date`/`scheduled_time_et`.
**Owner:** Ridwan.
**Notes:** Make.com must never post a row that's still `Draft`, regardless of whether its scheduled time has passed.

### Step 7: Make.com — publishing
**What happens:** A Make.com scenario polls the Sheet on an interval, finds rows where `status = Ready` and `scheduled_date`/`scheduled_time_et` has arrived, posts to the matching platform's API, then writes `Posted` + `posted_at` back to the row.
**Input:** The Sheet, platform API credentials (already connected per CLAUDE.md — "the Make connector is already connected").
**Output:** Live posts; updated Sheet status.
**Decisions:** Not yet made — **open question**, see below.
**Owner:** Whoever builds the Make.com scenario (this is genuine platform-specific automation work, likely needs a dedicated session with Make.com's MCP tools).
**Notes:** This is the one piece of the pipeline not discussed in granular detail during the interview — polling interval, error handling if a platform API call fails, and retry logic all need a follow-up decision before this gets built.

### Step 8: Content system sync
**What happens:** `ridwan_content_system_updated.html` stops being a manually-merged tracker and instead becomes a read-only visual mirror of the Sheet — every post shown, status visible, clickable through to its real source HTML file via the `content_system_folder` column.
**Input:** The Sheet (source of truth going forward).
**Output:** An updated `<script id="cowork-sync-data">` JSON block inside `ridwan_content_system_updated.html`, refreshed on the same cadence as the Sheet changes (recommend: refreshed as part of Step 5's write, and again whenever Make.com updates a row's status in Step 7).
**Decisions:** Confirmed to keep the content system, repurposed as this visual/click-through layer rather than dropped. The old Tips backlog and the two broken/orphaned entries found in the 2026-07-12 sync sweep are explicitly **not** being fixed — Ridwan confirmed they're not useful and not being worked toward.
**Owner:** Extend the existing sync logic; this is additive, not a rebuild — the "File Linking" and JSON Standard rules already in CLAUDE.md already support this, they just haven't been wired to a live-updating source before.
**Notes:** This resolves Ridwan's ask directly — "I would really love to be able to click on a certain post and get directed to the real HTML file" is already how the system is *supposed* to work per its own JSON Standard (`folder` field), it just needs a reliable, automatic sync feeding it instead of ad-hoc manual merges.

## Edge Cases and Failure Modes

- **A stream fails to generate that week** (e.g. CRO Fix's target audit comes back with nothing worth building) — no Sheet rows get created for that stream's slot; the weekly calendar has a designated fallback for LinkedIn (Static Ad fills an empty hero slot) but Instagram/Twitter currently have no defined fallback — worth deciding before this is fully live.
- **QA flags something but Ridwan doesn't review in time** — the row stays `Draft`/`Needs Review` forever; Make.com never posts it. No silent auto-approval on timeout.
- **Make.com's platform API call fails** (rate limit, auth expiry, etc.) — not yet specified; needs a retry/alert policy defined when Step 7 is actually built.
- **The `replo-rebuilds` cache goes stale and Template Showcase has no fresh page to showcase** — Step 1B's existing internal-page fallback (already documented in CLAUDE.md) still applies.
- **A caption variant gets reused past the point of feeling fresh** — no hard rule yet; rely on Ridwan's Sheet review to catch anything that reads stale before approving.
- **Twitter's 21/week target isn't hit some weeks** — accepted as a known, honest limitation while the asset library is still young; not a failure state, just a ramp.

## Dependencies and Requirements

- Google Sheets connector and Make.com connector, both already connected per existing CLAUDE.md notes.
- Platform API access (LinkedIn, Instagram, Twitter/X) provisioned inside the Make.com scenario — not yet confirmed as done.
- **Hard platform limitation:** Cowork scheduled tasks can only be bound to one folder/project. `replo-rebuilds` and `koolestpro-cowork-v2` cannot both be live inside one scheduled task's execution context. Confirmed via a live "Run now" diagnostic on 2026-07-13 and reconfirmed against current Cowork documentation on 2026-07-14 — this has not changed. The local sync cache (`replo-pages-cache/`) plus the new staleness-reminder task (Step 1) is the practical workaround, not a full fix.
- Harvest, QA, and Sheet-population scripts (Steps 2, 4, 5) do not exist yet — this plan defines their spec but building them is separate implementation work.
- Video thumbnail compositing (Step 3) does not exist yet — same, spec defined, not built.

## Open Questions

- **Make.com scenario mechanics** (Step 7): polling interval, retry/error policy, exact API call shape per platform — not covered in the interview, needs its own follow-up session, ideally with Make.com's MCP tools loaded to inspect what's actually configured today.
- **Fallback content for Instagram/Twitter** when a stream fails to generate that week — LinkedIn has a defined fallback (Static Ad fills the empty hero slot), IG/Twitter do not yet.
- **Exact scheduled-task run times** within each day (Step 1's table gives approximate times inherited from the current schedule; not explicitly re-confirmed per new day).

## Success Criteria

- Every week, ~31 Sheet rows get created automatically (3 LinkedIn + 7 Instagram + 21 Twitter) without Ridwan touching the generation pipeline.
- Ridwan's only manual step is a single review pass flipping Draft → Ready.
- Zero posts go out that Ridwan didn't explicitly approve.
- `ridwan_content_system_updated.html` accurately reflects what's been posted, with working click-throughs to source files, without manual merge sweeps.
- Weekly credit spend stays within the Fri-Tue safe window, with Wed/Thu untouched.
- Twitter volume climbs from ~17-18/week toward the 21/week target as the asset library grows, without ever resorting to bare-text filler.

# Koolestpro System Restructure Plan

**Written:** 2026-09-04
**Source:** process-interviewer session with Ridwan
**Status:** Plan approved in principle, not yet executed

---

## Goal

Give Ridwan a single, honest, self-maintaining map of the whole Koolestpro system, so that at any moment he can see what exists, what is running, what is stopped and why, and where a new piece of work belongs.

---

## Context

This project started as a content generation system in April 2026. By September it also carries a Next.js site, a portfolio, a store-template library, two lead discovery pipelines, a distribution engine posting to X and LinkedIn, 15 scheduled tasks, 51 Python tools, and a growth plan covering two separate markets. The KoolestFlow cold-DM app is about to move in as well.

Nothing is broken in a way that stops work. The problem is legibility. `CLAUDE.md` has grown to 116KB of chronologically-appended corrections, which is an excellent decision log and a poor map. There is no single place that answers "what is running right now, and what have I abandoned."

Four decisions were made during the interview and they constrain everything below:

1. **Deliverable is the map**, not the lead engine and not a prune. The other two get planned, not built, in this pass.
2. **Seven sub-projects, cut by function.** Content Production, Distribution, Prospect Intelligence, Outbound, Build Assets, Web Presence, Infrastructure.
3. **Nothing moves on disk.** Docs describe where things actually are today. The physical move is a separate, later, deliberate job.
4. **Status is generated, narrative is hand-written.** A script reads the real sources; prose is written once and edited when the system genuinely changes.

---

## Process Overview

1. Write `SYSTEM-MAP.md` at the project root as the single entry point.
2. Write seven sub-project docs under `docs/system/`, one per function.
3. Build `.ai-workflow/tools/build_system_status.py` to generate the live status page from real sources.
4. Add a weekly scheduled task to regenerate it.
5. Write the disposition record for the four blocked streams: three active, one accepted-as-is.
6. Write the lead-sourcing build spec covering all four approved sources.
7. Add a CLAUDE.md pointer so future sessions read the map first.
8. Verify: every path the docs assert actually exists, every stream named in the map appears in the generated status.

---

## Detailed Steps

### Step 1: `SYSTEM-MAP.md` (project root)

**What happens:** One page, the front door. Names the seven sub-projects, one paragraph each, with a link to its own doc and a one-line current state. Carries the "where does a new thing go" decision table so the structure survives contact with future work.

**Input:** The decomposition agreed in the interview.

**Output:** `/SYSTEM-MAP.md`

**Decisions already made:**
- Lives at the project root, not in `docs/`, because it is the entry point and root is where anyone looks first.
- Does not duplicate `CLAUDE.md`. `CLAUDE.md` stays the rules-and-corrections record; `SYSTEM-MAP.md` is the structural map. The map links to the relevant CLAUDE.md sections rather than restating them.
- Does not duplicate the two operating plans either. Those stay the strategy documents; the map is the inventory.

**Notes:** The three-document relationship needs to be stated explicitly on the map itself, at the top, or a future session will re-derive it wrongly. Suggested wording: *"CLAUDE.md is the rulebook. The operating plans are the strategy. This is the inventory."*

---

### Step 2: The seven sub-project docs

**What happens:** `docs/system/01-content-production.md` through `07-infrastructure.md`. Each answers the same six questions in the same order, so they are scannable side by side:

1. What this sub-project is for, in two sentences.
2. What is in it right now (files, folders, scripts, scheduled tasks) with real paths.
3. How it works end to end, in prose, not bullet fragments.
4. What is live, what is stopped, what has never run.
5. Its rules, and where in `CLAUDE.md` the full version of each rule lives.
6. Known gaps and open questions.

**Input:** The current state of the repo plus what was established in the interview.

**Output:** Seven markdown files under `docs/system/`.

**What goes in each, concretely:**

| Doc | Covers | Notable current-state facts to record |
|---|---|---|
| 01 Content Production | Tips, CRO Fix, Static Ad, Template Showcase, trend radar, the content engine skills, the reference/gold-standard files | Trend radar disabled since 2026-08-14 and has never produced a `pickedTopic`; Tips have run off the April/May `status: "Idea"` backlog for six weeks; gpt-image credits exhausted on both keys, prompt-pack protocol is now the fallback |
| 02 Distribution | `outputs/distribution-queue/`, the Google Sheet, Make.com scenario 6565331, the harvest→qa→populate→feed→sync chain, the weekly assembly task, the every-2-days health check | X and LinkedIn live and healthy; Instagram blocked at Meta account level; TikTok rejected at app review; clean pacing ~1.0/day against a 3/day target; the no-simultaneous-slot rule and why the Make-side fix was not applied |
| 03 Prospect Intelligence | `targets_pool.json`, `dm_leads_pool.json`, BrowserAct/Maps (Tue), Meta Ad Library (Wed), `taken-brands-ledger.json`, `lead_playbook.py`, the Build/Fix/Scale/Marketplace tracks | 12 targets, all `Available`, all with `segment: null` despite CLAUDE.md requiring that field; `dm_leads_pool.json` is now a historical staging log, not a destination; the two pools serve different purposes and are not interchangeable |
| 04 Outbound / KoolestFlow | The cold-DM app, `outreach_tracker.json`, the hybrid cloud-scores/Mac-imports pipeline, `pending-push/`, the launchd importer | Vercel deployment does not persist; real data lives on `127.0.0.1:8787`; one queued file currently sitting in `pending-push/` (`2026-W36_adlib-ng-home-decor.json`); outbound has produced zero clients because it has never actually been sent |
| 05 Build Assets | `replo-rebuilds/`, `store-templates/`, page-presentation-kit and its scripts, the per-brand social-content libraries, `assets/frames/` | `replo-rebuilds` moved inline 2026-08-31 and the cache is retired; the manifest must be catalogued by hand now, which is how two pages sat unnoticed; the mobile-strip historical backlog is deliberately not backfilled |
| 06 Web Presence | `site/`, the portfolio, koolestpro.com, SEO/AEO, directories, the gated ads plan, the Nigeria demo site | Domain bought; ads documented but deliberately gated on price not budget; Track F's keyword map and directory list exist but have not been executed |
| 07 Infrastructure | `.ai-workflow/tools/` (51 scripts), the 15 scheduled tasks, `.env` credentials, the spend ledgers, the sandbox constraints | Cloud bash dies near 178s and does not persist background processes; two scheduled triggers previously went unreachable and were recreated as `-v2`; three scheduled tasks are currently disabled |

**Notes:** Write these from the repo, not from memory of the repo. Several things in `CLAUDE.md` describe intent that the files do not match. The `segment: null` gap on all 12 targets is one example, and there will be others. Where doc and reality disagree, record reality and flag the gap. That divergence is exactly what the map exists to surface.

---

### Step 3: `build_system_status.py`

**What happens:** A script that reads the real sources and writes `SYSTEM-STATUS.html` at the project root. No hand-maintained numbers anywhere in it.

**Input, all machine-readable and all already present:**

| Source | Yields |
|---|---|
| the scheduled-tasks list | every task's enabled state, cron, last run, next run |
| `outputs/distribution-queue/queue.json` | queued vs posted vs QA-blocked, 7-day clean pacing |
| `targets_pool.json` | pool depth by status and segment |
| `.ai-workflow/taken-brands-ledger.json` | brands consumed, so pool exhaustion is visible before it bites |
| `.ai-workflow/pending-push/` | leads scored but not yet imported |
| `trend-radar-spend-ledger.json` | month-to-date paid-API spend |
| `ridwan_content_system_updated.html` → `SYNC_DATA.items` | content by status and type, and how much `Idea` backlog is left |
| `replo-rebuilds-pages.json` | showcase-eligible pages remaining |
| `store-templates.json` | templates built, and which verticals are still empty |

**Output:** `SYSTEM-STATUS.html` at the project root, plus a `system-status.json` sibling so a future session can read the numbers without parsing HTML.

**Design constraints, non-negotiable:**
- Every number traces to a file. Nothing is typed in by hand and nothing is estimated.
- Where a source is missing or unreadable, the page says so in place of that number. It never guesses and never silently shows zero.
- Every row carries a "last verified" timestamp from the generating run, so a stale page is obviously stale.
- Brand system applies: dark theme, orange to purple, Syne and DM Mono. Solid text colours only, per the project-wide gradient-text ban.

**Notes:** This is a status surface, not a dashboard with charts. Its job is to answer "what is running, what is stuck, what is running low" in one screen. Resist scope creep into analytics.

---

### Step 4: `koolestpro-system-status-weekly` scheduled task

**What happens:** Regenerates the status page and, when something has genuinely changed state since the last run, says so in its summary rather than reporting silently.

**Timing:** Monday, after `koolestpro-weekly-distribution-assembly` (07:51) and after `koolestpro-target-pool-refresh` (08:18), so it sees the week's real starting position. Roughly 08:45.

**Decisions:**
- It regenerates and reports. It does not fix anything. A status task that also repairs things becomes a task nobody trusts to have told the truth.
- It flags four specific conditions loudly, because these are the ones that decay silently: a scheduled task that has not run in over 14 days, `targets_pool` untouched candidates below 4, files sitting in `pending-push/` for more than 48 hours, and clean posting pace below 1.5/day.

---

### Step 5: Blocked-stream disposition record

**What happens:** A section in `SYSTEM-MAP.md`, mirrored into the relevant sub-project docs, that states each blocked stream's disposition explicitly. This is the part that answers "what have I stopped working on."

**Ridwan's decisions from the interview:**

| Stream | Disposition | What that means concretely |
|---|---|---|
| TikTok posting | **Active — route decided 2026-09-04** | Ridwan's call: **videos land in the TikTok draft inbox and he posts them manually.** That means only the `video.upload` scope is needed and the display-own-posts scope is dropped entirely. The 2026-08-19 rejection cited the personal/internal-use restriction on *displaying* own posts on a website, which is the half being abandoned, so the rejection may not even block this path. Next action is confirming whether the existing sandbox `video.upload` access is sufficient for inbox drafts without further review, since that was already proven working end to end on 2026-08-11. |
| Trend radar | **Active — route decided 2026-09-04** | Ridwan's call: **move the run to his Mac.** No X tier upgrade. This also unblocks Reddit, which is already live via Apify and only fails on the cloud's 178s ceiling. The trade is that the run stops being unattended, which turns out to be a feature rather than a cost, because of the new approval gate below. |
| Instagram posting | **Active** | Blocked at Meta account level on the Page↔IG Business link. Mostly waiting rather than building. Next concrete action is checking Business Suite Account Quality. |
| Posting pace | **Target stands, clarified 2026-09-04** | Not "accepted as is" and not abandoned. Ridwan's clarification: **3/day is an average floor, not a cap, and he is happy to go higher when there is content to go out.** So the goal is unchanged and the ~1.0/day clean rate is a real shortfall. It is simply not a build item this pass. Interaction worth recording: the 2026-09-04 LinkedIn hard cap of 1 post/day means LinkedIn can contribute at most 1 of the 3, so X carries the remainder and the average lives or dies on X volume. |

**Notes:** The value here is that a stream is either being worked on or formally shelved, with a reason. Limbo is what makes a system feel out of control.

---

### Step 5b: Trend radar approval gate (new requirement, 2026-09-04)

**What happens:** Ridwan asked for something the current design does not do: *"I want to always choose what topic out of the top 3 to 5 gets posted every scheduled run."* Today `koolestpro-tips-weekly` auto-picks — if `trend-radar-log.json` has a `pickedTopic` for the current ISO week it uses it with no approval gate, by explicit earlier design. That changes.

**The new shape, which the Mac move makes easy rather than awkward:**

1. **Trend radar runs on Ridwan's Mac** (Thursday, ahead of Friday's Tips run). No 178s ceiling, so Reddit completes and Instagram browsing works because he is present.
2. It produces **3 to 5 ranked candidate topics**, each with its angle, source URL, engagement evidence and a one-line rationale. It writes them to `trend-radar-log.json` with `pickedTopic: null` and a new `awaitingChoice: true` flag.
3. **Ridwan picks one, in the same sitting.** He is at the terminal already, so the pick is a prompt rather than an asynchronous handoff. The chosen candidate is written to `pickedTopic` and `awaitingChoice` flips to false.
4. **Friday's Tips run reads the pick** and builds from it, exactly as it does today.
5. **Fallback is unchanged and must stay.** If the log is stale, `pickedTopic` is null, or `awaitingChoice` is still true on Friday morning (he did not get to it), Tips falls back to the existing backlog-first logic. A missed pick must never block the week's carousel.

**Why this is worth building rather than just picking topics by hand:** the ranking and evidence-gathering is the expensive part and it is what he is not currently getting at all. The pick itself is thirty seconds. Handing him five researched candidates with real engagement numbers behind them is a completely different thing from asking him what to write about.

**Notes:** This supersedes the "auto-picked, no separate approval gate on the topic itself" line in the Trend & Format Radar section of `CLAUDE.md`. That section needs amending when this is built, not before.

---

### Step 6: Lead-sourcing build spec

**What happens:** A written spec, not an implementation, for all four approved sources. It lands in `docs/system/03-prospect-intelligence.md` as its build plan.

**All four were approved. Suggested build order, cheapest and highest-certainty first:**

**6a. Fix Google Maps to return the website field.**
The current BrowserAct template returns `name, full_address, star_rating, review_count, avg_price_per_person` and no website. That single missing field is why every Maps lead lands at `NeedsContactInfo` and needs a manual lookup. Swapping to an actor that returns website and phone turns "no website" from a manual check into a filter, and collapses the enrichment step that currently costs a second BrowserAct call per lead. Lowest risk of the four, reuses the entire existing pipeline, and it pays for itself in credits.

**6b. Instagram business-profile scraping.**
The highest-precision source for the actual target definition. Signal: real follower count and recent posting activity, combined with a bio link that is a `wa.me`, a Linktree, or absent. That combination is literally "doing well, no website." It also hands over the DM handle directly, which Maps never does and which is the channel the Nigeria track actually uses. Runs through the Apify account already wired in `.env`. Needs a new field mapping into the `Build/Fix/Scale` classifier.

**6c. Jumia / Konga / JiJi seller scraping.**
Sellers doing real volume on somebody else's platform. The pitch is sharper than a cold "you need a website" because the pain is concrete: no owned customer relationship, no data, platform takes a cut. The Ad Library task already treats marketplace links as a valid lead type with its own handling and a 500-page-like floor, so the classification logic exists. The contact step stays manual, since marketplaces hide seller details, and the spec should say so plainly rather than implying automation that will not exist.

**6d. TikTok business-profile scraping.**
Same signal as Instagram against a different audience, and it matches the channel his content history says converts. Last because TikTok profile scraping is the most brittle of the four and there is no reason to take on that maintenance until the other three are earning.

**Rules that apply to all four, inherited from the Ad Library task's hard-won corrections:**
- Country codes do not scope results. City as literal text in the query is what works.
- Every lead on a Nigeria run must carry an explicit Nigeria signal, checked against page name, body text, and link.
- Everything goes through `koolestflow_client.py`'s push path so the taken-brands ledger cannot be bypassed.
- Build-track leads sort first.
- Recognisable national and international chains get flagged for eyeballing even when they pass every automated filter. Like-count alone cannot tell a small local business from a big chain's regional page.

---

### Step 7: CLAUDE.md pointer

**What happens:** A short block near the top of `CLAUDE.md` pointing at `SYSTEM-MAP.md` as the structural entry point, alongside the existing pointers to the two operating plans.

**Notes:** Deliberately short. `CLAUDE.md` is already 116KB and the fix for that is not adding to it. Three or four lines.

---

### Step 8: Verification

**What happens:** Before this is called done:

- Every file path asserted in any of the eight new documents is checked to actually exist. A map that names files that are not there is worse than no map.
- Every stream named in `SYSTEM-MAP.md` appears in the generated status page, and vice versa. A stream in one and not the other means the decomposition missed something.
- `build_system_status.py` is run against a deliberately broken input (a renamed source file) to confirm it reports the gap instead of silently showing zero.
- The generated page is opened and looked at, not just generated. Per the project's own standing rule: verify by looking at the output, not by reading the markup.

---

## Edge Cases and Failure Modes

- **A source file the status script reads gets renamed or moved.** The script must report "source missing" for that row, never zero. A zero that means "I could not read the file" is the most dangerous possible output for a status page.
- **`SYNC_DATA` parsing breaks.** `ridwan_content_system_updated.html` is 204KB with the JSON embedded in a script tag. The extraction must be tolerant of the surrounding HTML changing, and must fail loudly rather than returning a partial parse.
- **The docs drift from reality anyway.** Narrative prose is hand-maintained and will go stale. Mitigation: keep the hand-written half to things that change slowly (what a sub-project is for, how it works, its rules) and push everything volatile into the generated half. If a fact changes weekly, it belongs in the status page, not in prose.
- **A future session writes new machinery and does not add it to the map.** Mitigation is the CLAUDE.md pointer plus the existing "always update the operating plan" rule. This is a real risk and worth accepting rather than over-engineering against.
- **The status page becomes the thing nobody opens.** If it is not answering a question Ridwan actually asks, it is decoration. Worth revisiting after four weeks: has he opened it, and did it tell him something he did not know?
- **The physical restructure never happens.** Entirely acceptable. The docs are useful on their own and the move was explicitly deferred, not promised.

---

## Dependencies and Requirements

- Read access to the connected `koolestpro-cowork-v2` folder. Already have it.
- The scheduled-tasks list, for the status script's task rows. Already available.
- No new credentials, no new paid services, no network access for anything in Steps 1 through 8. This whole plan runs against files already on disk.
- The lead-source build (Step 6) does need spend, but Step 6 produces the spec only. The build itself is a separate approval.

---

## Open Questions

**Resolved 2026-09-04, same session:**

- ~~Posting pace~~ — 3/day is an average floor, not a cap, and Ridwan will go higher when there is content. Target stands. Recorded in Step 5.
- ~~TikTok route~~ — drafts to the TikTok inbox, manual posting. `video.upload` only, display scope dropped. Recorded in Step 5.
- ~~Trend radar route~~ — moves to the Mac, no X tier upgrade. Plus a new approval gate, which is now Step 5b.
- ~~`segment` on `targets_pool.json`~~ — the rule was amended rather than the data backfilled. The field was never in `meta.recordSchema` and no target ever carried one. In practice `targets_pool.json` is the international content-production pool (every entry has a real auditable URL) and KoolestFlow is the outbound pool, a split Ridwan chose deliberately on 2026-08-11 for a good reason. The pool boundary already is the segmentation. `CLAUDE.md` rule 4 was rewritten on 2026-09-04 to say so.

**Still open:**

1. ~~**Where KoolestFlow physically lands.**~~ **Answered by inspection, 2026-09-04.** It is already inside the project at `cold-email-app/`, a real directory dated 2026-06-30, not a symlink. The move Ridwan was planning has already happened. What is *not* decided is the version-control boundary: it carries its **own `.git`**, so it is nested rather than merged. Nested keeps its history clean and means this project's tooling can read it but must never commit into it. That is a reasonable default and should be an explicit decision rather than drift.

2. **Does inbox-only TikTok still need app review?** The rejection was specifically about displaying own posts on a website. Dropping that scope may make the whole review moot, or may not. Needs checking against TikTok's current scope requirements before assuming either way. This is the only thing standing between the TikTok stream and being unblocked.

3. **Cross-pool duplication.** Nothing currently stops a business appearing in both `targets_pool.json` and KoolestFlow. No collision has happened, and the taken-brands ledger covers the outbound side. Flagged rather than built.

---

## Success Criteria

- Ridwan can answer "what is running, what is stopped, what is running low" from one screen, without asking and without opening seven files.
- A stream that stops running becomes visible within a week rather than a month.
- A new piece of work has an obvious home, decidable from the map's decision table without a conversation.
- No number on the status page is hand-maintained, and no number is wrong.
- The four blocked streams each have a stated disposition, so none of them is sitting in limbo.
- After four weeks: the status page has surfaced at least one thing Ridwan did not already know. If it has not, it is decoration and should be cut back.

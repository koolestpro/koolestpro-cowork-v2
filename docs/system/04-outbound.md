# 04 — Outbound / KoolestFlow

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

Turning a qualified lead into a sent message and a tracked conversation. It is the newest sub-project, the least proven, and the one with the largest gap between what is built and what has actually happened.

**The honest state:** outbound has produced zero clients, because it has never been sent. That is in `CLAUDE.md` as a fact not to re-derive. The machinery is real and mostly works. Nobody has pulled the trigger.

---

## What is in it

**KoolestFlow**, also called the cold-DM app. Ridwan's own outreach OS: a Python backend, SQLite prospect store, AI message generation, and a dashboard.

**Its code already lives inside this project** at `cold-email-app/` — a real directory dated 2026-06-30, not a symlink. It keeps its **own `.git`**, so it is nested rather than merged: this project's history does not track its commits, and it is versioned independently. Worth knowing before anyone tries to commit across the boundary. Backend at `cold-email-app/backend/` (`app.py`, `lead_engine.py`, `ai_engine.py`, `mailer.py`, `notion_sync.py`, `google_calendar.py`), Vite frontend at `cold-email-app/src/`, plus a Dockerfile and compose file.

Two deployments:

| Deployment | URL | State |
|---|---|---|
| Local | `http://127.0.0.1:8787` (frontend `:5173`) | SQLite, unchanged, still works |
| Vercel | `https://cold-dm-app.vercel.app` | **Live on Supabase since 2026-09-07** — writes persist, confirmed |

**Storage was moved to Postgres on 2026-09-05.** Supabase project `koolestflow`
(`glozxjxmijgmlyinnzhz`, us-east-1, free tier). `state_store.py` delegates to
`supabase_store.py` when `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are both
present and falls back to SQLite when they are not, so local is untouched. The
24 real prospects were migrated and checksum-verified. Full detail, and the two
env vars Ridwan still has to set in Vercel, are in
[`cold-email-app/SUPABASE-SETUP.md`](../../cold-email-app/SUPABASE-SETUP.md).

**A second bug was found in the same pass and fixed.** `track` was in
`PROSPECT_COLS` and `_row_to_prospect` but never in `_ensure_columns`, so every
`load_state()` call raised `IndexError: No item with that key` against any
database created before 2026-08-19 — including the local one holding the real
data. That was live and unnoticed.

**`outreach_tracker.json`** at the project root is the local-first outbound system of record per `CLAUDE.md` rule 3.

**The hybrid pipeline**, chosen by Ridwan on 2026-09-01:

| Piece | File | Runs where |
|---|---|---|
| Maps runner, resumable | `.ai-workflow/tools/leadgen_run.py` | cloud, Tuesdays |
| Ad Library bridge, `--queue` | `.ai-workflow/tools/ad_library_koolestflow_bridge.py` | cloud, Wednesdays |
| Queue directory | `.ai-workflow/pending-push/*.json` | on disk |
| Importer | `.ai-workflow/tools/import_pending_push.sh` | Ridwan's Mac, launchd every 30 min |
| launchd job | `.ai-workflow/com.koolestpro.leadgen-import.plist` | `~/Library/LaunchAgents/` |
| Manual recovery | `.ai-workflow/tools/push_prospects_file.py` | Ridwan's terminal |

---

## How it works

The cloud scores, the Mac imports. A scheduled run discovers, enriches and scores leads, then writes them to `.ai-workflow/pending-push/{week}_{slug}.json` instead of pushing. Ridwan's launchd job picks the file up every 30 minutes and pushes to the local KoolestFlow, which actually persists.

**Ledger ownership is deliberate.** The cloud run only *reads* `taken-brands-ledger.json`, to skip already-taken brands before spending an enrichment credit. Only the Mac importer *writes* it, and only after a verified push. That is what stops a failed push from burning brands permanently.

**Recovery when a run strands:** `push_prospects_file.py <file> --ignore-ledger` from Ridwan's terminal with the local backend up. This skips discovery and enrichment entirely, so no BrowserAct credits are re-spent. `--ignore-ledger` is needed because a failed push may already have written the brands into the ledger; it uses a scratch ledger for that one push and leaves the real history untouched.

---

## State

**The Vercel deployment silently discards writes.** Confirmed live on 2026-09-01: 5 leads pushed, the endpoint returned success and printed a truthful-looking `Pushed 5 new prospect(s)`, and a follow-up read returned **0 prospects**. Serverless filesystem is ephemeral, so the SQLite write lands in one lambda's `/tmp` and is gone by the next request.

**The push-succeeded log line is not proof.** Never report a run as successful on that line alone. `push_prospects_file.py` now re-reads state and exits non-zero on an empty read-back. That is useful but not a guarantee: if the same warm lambda serves both the POST and the read-back it still answers correctly. An immediate read said 5; a read minutes later said 0. Treat a pass as "not obviously broken," not "durable."

**Currently queued:** one file sits in `.ai-workflow/pending-push/` — `2026-W36_adlib-ng-home-decor.json` — plus `failed/`, `imported/` and `patches/` subfolders. A file sitting there for more than 48 hours means the Mac importer is not running.

---

## Rules

| Rule | Where |
|---|---|
| **Every outbound email/DM is humanized** (v3.0, 11 passes, `VOICE.md`-anchored) before sending. No em dashes. Never invented familiarity or a fabricated result. | `docs/system/humanizer-guideline.md` |
| Local-first, including the CRM. `outreach_tracker.json` is the system of record. The Notion cold-DM app is replaced, not migrated. | `CLAUDE.md` rule 3 |
| Always `GET /api/state` first, dedupe, then `POST` the full merged list. KoolestFlow's `save_state()` replaces the entire prospects table with whatever is posted, so never post just the new batch. | BrowserAct scope-expansion section |
| Never bypass `koolestflow_client.py`'s push path. It is what consults the ledger. | Ad Library task, correction 7 |
| Nigeria wedge is a free ad creative, then a free frontend-only sample site, over Instagram DM, priced in Naira. International is a hero-section teaser, then a live rebuild, over email, priced in USD. **Never blend the copy.** | `CLAUDE.md` "Two markets" |

---

## The playbook

[`outreach-playbook.md`](outreach-playbook.md) (added 2026-09-07) is the executable layer: daily routine, message templates per track and market, reply handling, what to log, and the line between what a hired sender may do alone and what Ridwan approves. Written when Ridwan decided to hire someone rather than send every message himself, which partly overrides the growth plan's D6 and E5 "Ridwan sends them by hand" wording. Manual sending is unchanged and still mandatory.

## Known gaps

- **It has never been sent.** Everything above describes a loaded machine that has not fired. Discovery, scoring and import all work; the message-sending step has no track record at all.
- **The cloud cannot reach the Mac,** and no script change fixes that. Either KoolestFlow gets a persistent cloud backend (the Supabase connector is already configured) or lead-gen stays a hybrid with a human-owned import step. Ridwan chose hybrid.
- **The launchd importer is a single point of failure** with no alerting. If it stops, files pile up in `pending-push/` silently. The status page's 48-hour flag is the compensating control.
- **The nested `.git` is an unresolved boundary, not a settled one.** The code is already inside the folder, so the "should it move in" question is moot, but nothing decides whether it should stay independently versioned or be absorbed. Staying nested keeps its history clean and means this project's tooling can read it but should never commit into it. Worth an explicit decision rather than drift.

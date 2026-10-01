# Weekly SEO run: SOP

One run = one project = one week. The engine (`seo/engine/`) is the same in every project, and everything specific to this project lives in `seo/project/` and this repo's `.env`.
All output for the run goes to `seo/project/runs/YYYY-MM-DD/`. Tool commands below are run from the repo root.

**Before anything:** read `seo/engine/rules.md`, `seo/project/project.json`, `business-profile.md`, `clusters.md`, and the last two `runs/*/notes.md`. Don't read `seo/engine/reference/` (background only).

**Platform** (`project.json → platform`):
- `shopify`: snapshot from the public storefront. Publishes as a hidden Shopify article (`shopify_publish.py`).
- `nextjs-resources`: typed entry in the site repo's articles file, sent as a draft PR (`site_publish.py`).
- `files-only`: stops at `body.html` + `publish.json`, for any other CMS.

**Keyword data** (`project.json → data_provider`):
- `free` (default): Search Console queries (`gsc_pull.py`) + Google Autocomplete and Keyword Planner volumes (`google_keywords.py`) + web search for the results page. Ubersuggest MCP, if connected in the session, can fill in difficulty.
- `dataforseo`: the project's own DataForSEO account (`dataforseo.py`), with the free stack as fallback.
Write in `notes.md` where each number came from. Never guess a volume. Write "volume unknown" and rank on intent + GSC instead.

## Step 0: Preflight
0. **Double-run guard:** if any `runs/*/shopify-result.json` or `runs/*/site-result.json` is dated within the last 6 days, stop. This week is already done.
1. Snapshot:
   - `shopify`: `python3 seo/engine/tools/store_snapshot.py` (refreshes `seo/project/snapshot/`, prints a diff).
   - `nextjs-resources`: pull the site repo (`site_repo` / `site_repo_path`) and list slugs from its content files.
2. If `business-profile.md` is empty, older than 90 days, or the snapshot shows a big change, run `prompts/00-business-profile.md` first.
3. Credential check, writing what's available into `notes.md`: `gsc_pull.py check`, `google_keywords.py check`, `dataforseo.py balance` (only if data_provider is dataforseo), `shopify_publish.py --check` (Shopify). If something is missing, carry on with the rest. Never stop silently.

## Step 1: Data + quick wins
1. `python3 seo/engine/tools/gsc_pull.py pull --days 28` → `gsc.json` (+ `ga4.json`).
2. Positions: GSC average position per query (free). With DataForSEO, also `dataforseo.py ranked --out …` and `dataforseo.py rank`.
3. `prompts/01-quick-wins.md` → `quick-wins.md`. Pick at most one. Quick wins are instructions for the owner. The engine never edits live pages (for `nextjs-resources` a fix to an existing article may ride in the same draft PR).

## Step 2: Topic selection
1. Candidates:
   - GSC queries with impressions but no dedicated page (strongest signal).
   - `google_keywords.py research --seed "<cluster seeds>" --out runs/<date>/keywords.json` (Autocomplete, plus volumes if Keyword Planner is set up). Add `--deep` for a fuller sweep.
   - `google_keywords.py ideas --url <competitor page>` for keywords a competitor page targets (Planner only).
   - DataForSEO projects: `dataforseo.py ideas` / `gap --competitor …`.
2. `prompts/02-topic-selection.md` → `topic.md` (six-factor scoring, cannibalisation check).

## Step 3: Brief
Results page for the winner: web search the exact keyword (top results, People Also Ask, whether there's an AI Overview), or `dataforseo.py serp` / Ubersuggest `serp_analysis` if available. Then `prompts/03-brief.md` → `brief.md`. Internal links come only from the snapshot / site slugs.

## Step 4 to 5: Draft + humanizer
`prompts/04-draft.md` → `draft.md`. Then a full humanizer pass in the project's voice (the `humanizer` skill if installed, or the anti-AI checklist in `rules.md §8`), grep for `—` / `&mdash;` (must be 0) → `article.md`.

## Step 6: Image
- `shopify` / `files-only`: `prompts/05-image.md`. Real product photo from the snapshot first, otherwise a generated image (no text, no logos). Always write alt text.
- `nextjs-resources`: skip if the site generates OG images.

## Step 7: Finalize
`prompts/06-finalizer.md`.
- `shopify` / `files-only`: `python3 seo/engine/tools/md_to_html.py seo/project/runs/<date>` → `body.html` (+ FAQPage JSON-LD), then write `publish.json`, then `shopify_publish.py --run … --dry-run` as the QA gate.
- `nextjs-resources`: `article.json` + `site_publish.py --run … --dry-run`.

## Step 8: Publish as a DRAFT (never live)
- `shopify`: `python3 seo/engine/tools/shopify_publish.py --run seo/project/runs/<date>` creates a hidden article.
- `nextjs-resources`: `site_publish.py --run …`, then branch `seo/<slug>`, commit, push and open a **draft PR**. The owner merges.
- `files-only`, or credentials missing: stop here, and note "files ready".

## Step 9: Log
Append to `seo/project/content-log.csv` (status `draft-in-shopify` | `draft-pr` | `files-only`).

## Step 10: Weekly report
`prompts/07-weekly-report.md` → `report.md`, appending to `performance-log.csv`.

## Step 11: Link-building outreach (max 5 prospects)
`prompts/08-outreach.md` → `outreach.md` + `outreach.json`. Then hand it off per `project.json → outreach.mode`:
- `sheet`: `python3 seo/engine/tools/outreach_push.py --run …` adds the leads unapproved to the outreach Sheet, and the project's own sender emails them after a person approves.
- `gmail-drafts`: create one Gmail draft per prospect with the Gmail connector, then run `outreach_push.py` to log them.
- `csv`: `outreach_push.py` writes `outreach-import.csv`.
Never send directly from the engine, and never send before a person has approved.

## Step 12: Notes + hand-off
`notes.md`: what ran, what was skipped and why, data sources, any spend, the draft link, the quick win, inbound links to add by hand, and outreach queued. Commit the run folder (no secrets, no images over 1 MB) and send the owner a short summary.

## Never
- Publish an article, merge a PR, edit a live page or theme, or send an email without approval.
- Invent reviews, stats, prices, customer names or results.
- Put keys in any file under `seo/`. Keys live in this project's `.env` only.

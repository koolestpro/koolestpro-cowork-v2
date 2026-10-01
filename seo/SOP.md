# Weekly SEO run: SOP

The cloud routine and the desktop runner both follow this file. One run = one client = one week.
Input: a client slug (e.g. `tapandrate`, `koolestpro`). Everything for the run is written to `seo/clients/<slug>/runs/YYYY-MM-DD/`.

**Before anything:** read `seo/config/seo-rules.md`, `seo/clients/<slug>/client.json`, `business-profile.md` and `clusters.md`, plus the last two `runs/*/notes.md`. Don't re-read the Perplexity reference.

**Platform** comes from `client.json → platform`:
- `shopify`: snapshot from the public storefront. Publishes as a hidden Shopify article (`shopify_publish.py`).
- `nextjs-resources`: the site repo is the source of truth. Publishes as a typed entry in `content/resources.ts` on a draft PR (`site_publish.py`).

**Data providers, in order** (`seo-rules.md §2`): GSC/GA4 → **DataForSEO** (`seo/tools/dataforseo.py`) → Ubersuggest MCP (fallback when DataForSEO has no credentials or no balance) → web search. Write in `notes.md` which provider each number came from.

## Step 0: Preflight (2 min)
0. **Double-run guard:** if any `runs/*/shopify-result.json` or `runs/*/site-result.json` is dated within the last 6 days, stop. This week is already done (the cloud and desktop runners may both have fired).
1. Snapshot the site:
   - `shopify`: `python3 seo/tools/store_snapshot.py --client <slug>` refreshes `snapshot/` and prints a diff.
   - `nextjs-resources`: make sure the site repo is cloned (`client.json → site_repo`, at one of `site_repo_path`), pull its default branch, and list existing slugs from `content/resources.ts`, `services.ts` and `work.ts`.
2. If the profile is older than 90 days, or the snapshot shows a big change (new product line, pricing change, new service), run `prompts/00-business-profile.md` first and flag it in the notes.
3. Credential check: `dataforseo.py balance`, `gsc_pull.py check --client <slug>`, and, for Shopify, `shopify_publish.py --client <slug> --check`. Write what's available to `notes.md`. If something is missing, carry on with whatever is available. Never stop silently.

## Step 1: Data pull + quick wins
1. `python3 seo/tools/gsc_pull.py pull --client <slug> --days 28` → `runs/<date>/gsc.json` (+ `ga4.json`).
2. `python3 seo/tools/dataforseo.py ranked --client <slug> --out runs/<date>/ranked.json` and `dataforseo.py rank --client <slug>` (appends to `rank-log.csv` for `tracked_keywords`).
   No DataForSEO? Use Ubersuggest `domain_keywords` + `domain_top_pages` (locId from client.json).
3. Run `prompts/01-quick-wins.md` → `quick-wins.md` (max 3, with exact before/after). Pick at most **one** for this week. The system never edits live pages or Shopify settings: quick wins are instructions for Ridwan. For `nextjs-resources` a quick win on an existing article *may* go in the same draft PR, since that PR is reviewed anyway.

## Step 2: Topic selection
1. Candidates: GSC queries with impressions but no dedicated page; `dataforseo.py ideas --seed "<cluster seeds>"`; `dataforseo.py gap --competitor <each competitor>`; `dataforseo.py competitors` when the client's competitor list is empty.
2. Run `prompts/02-topic-selection.md`. Score every candidate on the six factors in `seo-rules.md §3`.
3. Reject topics already covered (content-log, live blog/resources). Cannibalisation check: no two posts can target the same primary keyword.
4. Output: `topic.md`.

## Step 3: Brief
`dataforseo.py serp --keyword "<winner>" --out runs/<date>/serp.json` (top 20 + People Also Ask + AI Overview presence). Then run `prompts/03-brief.md` → `brief.md`. Internal links come only from the snapshot / site slugs.

## Step 4: Draft
Run `prompts/04-draft.md` → `draft.md`.

## Step 5: Humanizer
Run the full humanizer pipeline (`docs/system/humanizer-guideline.md`) on the draft in the client's voice (for koolestpro that is Ridwan's own `VOICE.md`). Then grep for `—` and `&mdash;`. The count must be 0. → `article.md`.

## Step 6: Image
- `shopify`: run `prompts/05-image.md`. Real product photo from the snapshot first; otherwise `gpt-image` (1536×1024, no text), uploaded to Cloudinary `koolestpro/seo/<slug>/`. Always write alt text.
- `nextjs-resources`: skip. The site generates OG images per article and `Article` has no image field.

## Step 7: Finalize
Run `prompts/06-finalizer.md`.
- `shopify` → `body.html` + `publish.json`:
  ```json
  {"title":"", "handle":"", "seo_title":"", "seo_description":"", "summary_html":"", "tags":[], "author":"", "blog_handle":"", "image_url":"", "image_alt":"", "primary_keyword":"", "cluster":"", "stage":""}
  ```
- `nextjs-resources` → `article.json` matching the site's `Article` type (`slug, title ≤ 60, h1, description 70 to 155, targetQuestion, updated, readingMinutes, blocks[], faq[], cta{text, href, label}`). Blocks use only `p|h2|h3|ul|table|callout|verdict`. Every H2 is a question, and the first sentence answers it in under 40 words.

QA gate (all must pass): title ≤ 60, meta ≤ 155, 0 em dashes, every internal link exists, keyword in H1/first 100 words/one H2/conclusion, word count inside the brief's range, no invented facts.

## Step 8: Publish as a draft (never live)
- `shopify`: `python3 seo/tools/shopify_publish.py --client <slug> --run <run dir>`. This creates a **hidden** article and writes `shopify-result.json`. No token: skip, and note "files ready in runs/<date>/".
- `nextjs-resources`: `python3 seo/tools/site_publish.py --client <slug> --run <run dir>`. This inserts the article into the site repo and writes `site-result.json`. Then, in the site repo: branch `seo/<article-slug>` from the default branch, commit, push, and open a **draft PR** titled `SEO: <title>` with the brief summary and target keyword. Ridwan checks the Vercel preview and merges. Never merge.

## Step 9: Log
Append one row to `content-log.csv` (status `draft-in-shopify`, `draft-pr` or `files-only`).

## Step 10: Weekly report
Run `prompts/07-weekly-report.md` over `gsc.json`, `ga4.json`, `rank-log.csv` and `content-log.csv` → appends to `performance-log.csv` and writes `report.md`. Add `dataforseo.py backlinks --client <slug>` for the off-page section.

## Step 11: Outreach (weekly, 5 prospects max)
Run `prompts/08-outreach.md`. Prospects come from `dataforseo.py backlinks --domain <competitor>` (who links to them), web search, and Ubersuggest `backlink_opportunity` as fallback.
For each prospect: verify the page, find a **published** contact (never guess one), write a humanized pitch, and create a **Gmail draft** (Gmail connector `create_draft`). Never send. Append to `outreach-log.csv`. Not sure about a contact? Log it as `needs-contact` and don't create a draft.

## Step 12: Notes + hand-off
Write `notes.md`: what ran, what was skipped and why, data sources used, DataForSEO spend this run, the draft link (Shopify admin URL or PR URL), the quick win, the inbound internal links to add by hand, and the Gmail drafts created. Commit the run folder (no secrets, no images > 1 MB). Then send Ridwan one short summary with the draft link.

## Never
- Publish an article, merge a PR, edit a live page/theme, or send an email.
- Invent reviews, stats, prices, customer names or results. Never present a concept brand as a client.
- Put tokens in any file under `seo/`.

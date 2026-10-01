# Weekly SEO run: SOP

The cloud routine and the desktop runner both follow this file. One run = one client = one week.
Input: a client slug (e.g. `tapandrate`). Everything for the run is written to `seo/clients/<slug>/runs/YYYY-MM-DD/`.

**Before anything:** read `seo/config/seo-rules.md`, `seo/clients/<slug>/client.json`, `business-profile.md` and `clusters.md`, plus the last two `runs/*/notes.md`. Don't re-read the Perplexity reference.

## Step 0: Preflight (2 min)
0. **Double-run guard:** if any `runs/*/shopify-result.json` is dated within the last 6 days, stop. This week is already done (the cloud and desktop runners may both have fired).
1. `python3 seo/tools/store_snapshot.py --client <slug>` refreshes `clients/<slug>/snapshot/` (products, collections, pages, blog URLs) and prints a diff against the last snapshot.
2. If the profile is older than 90 days, or the diff shows a big catalogue change (new product line, pricing model change), run `prompts/00-business-profile.md` first and flag it in the notes.
3. Check which credentials exist (`--check` on both tools). Write what's available to `notes.md`. If something is missing, carry on with whatever is available. Never stop silently.

## Step 1: Data pull + quick wins
1. `python3 seo/tools/gsc_pull.py pull --client <slug> --days 28` → `runs/<date>/gsc.json` (+ `ga4.json` if configured).
   No GSC? Use Ubersuggest `domain_keywords` + `domain_top_pages` (locId from client.json) and say so in the notes.
2. Run `prompts/01-quick-wins.md`. Output: `quick-wins.md`, with up to 3 pages to fix and exact new title/meta/additions for each.
3. Pick at most **one** quick win to do this week. Write its exact before/after into `quick-wins.md` for Ridwan to apply. The system never edits live pages.

## Step 2: Topic selection
1. Gather candidates: GSC queries with impressions but no dedicated page, Ubersuggest `keyword_suggestions` / `match_keywords` on the cluster seeds in `clusters.md`, and `competitors` gap keywords.
2. Run `prompts/02-topic-selection.md`. Score every candidate on the six factors in `seo-rules.md §3`.
3. Reject any topic already covered in `content-log.csv` or the live blog (check `snapshot/blogs.json`). Cannibalisation check: no two posts can target the same primary keyword.
4. Output: `topic.md` with the scoring table, the winner, the cluster, the stage and the reason.

## Step 3: Brief
Run `prompts/03-brief.md` → `brief.md`. It must include personalisation notes naming the real products and pages, and an internal-link plan built only from URLs in the snapshot.

## Step 4: Draft
Run `prompts/04-draft.md` → `draft.md`.

## Step 5: Humanizer
Run the full humanizer pipeline (`docs/system/humanizer-guideline.md`) on the draft in the client's voice, not Ridwan's. Then grep for `—` and `&mdash;`. The count must be 0. → `article.md`.

## Step 6: Image
Run `prompts/05-image.md`.
1. Prefer a real product photo from the snapshot (`snapshot/products.json` image `src`) that shows the exact product the post is about. Use its Shopify CDN URL directly.
2. Otherwise use the `gpt-image` skill (1536×1024, no text in the image, client's colours). Upload it to Cloudinary (`koolestpro/seo/<slug>/`) to get a public URL.
3. Always write the alt text. Save the image locally to `runs/<date>/image.*`.

## Step 7: Finalize
Run `prompts/06-finalizer.md` → `body.html` (clean semantic HTML, internal links resolved, FAQPage JSON-LD at the end) + `publish.json`:
```json
{"title":"", "handle":"", "seo_title":"", "seo_description":"", "summary_html":"", "tags":[], "author":"", "blog_handle":"", "image_url":"", "image_alt":"", "primary_keyword":"", "cluster":"", "stage":""}
```
QA gate (all must pass, or fix and re-run): title ≤ 60, meta ≤ 155, 0 em dashes, every `href` in the snapshot or a known external source, keyword in H1/first 100 words/one H2/conclusion, word count inside the brief's range, no invented facts (every number traces to the profile or a cited source).

## Step 8: Shopify draft
`python3 seo/tools/shopify_publish.py --client <slug> --run seo/clients/<slug>/runs/<date>`
Creates a **hidden** article (never published), sets the SEO title/description metafields, and writes `shopify-result.json` with the article ID and admin URL.
No token? Skip, and write "Shopify push skipped: no token. Files ready in runs/<date>/" in the notes.

## Step 9: Log
Append one row to `content-log.csv` (status `draft-in-shopify` or `files-only`).

## Step 10: Weekly report
Run `prompts/07-weekly-report.md` over `gsc.json` / `ga4.json` and `content-log.csv`. It appends rows to `performance-log.csv` and writes `report.md`: scorecard per post, wrong-intent traffic, posts due for their 30/90-day refresh, and the decision per post (improve / monitor / replace).

## Step 11: Outreach (weekly, 5 prospects max)
Run `prompts/08-outreach.md`. Ubersuggest `backlinks` / `linking_domains` / `backlink_opportunity` on competitors, plus web search for the prospect types in `seo-rules.md §10`.
For each prospect: verify the page exists and is relevant, find a public contact address (never guess one), write a humanized pitch, then create a **Gmail draft** (Gmail connector `create_draft`). Never send. Append to `outreach-log.csv`.
Not sure about a contact? Log it as `needs-contact` and don't create a draft.

## Step 12: Notes + hand-off
Write `notes.md`: what ran, what was skipped and why, the Shopify draft link, the quick win to apply, the inbound internal links to add by hand, and the Gmail drafts created. Commit the run folder (no secrets, no images > 1 MB). Then send Ridwan one short summary with the Shopify admin link.

## Never
- Publish an article, edit a live page/theme, or send an email.
- Invent reviews, stats, prices, customer names or results.
- Put tokens in any file under `seo/`.

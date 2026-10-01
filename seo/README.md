# SEO Engine (sub-project 8)

Weekly, brand-aware SEO system for Shopify clients (first: **tapandrate.co.uk**) and, later, koolestpro.com (Next.js, `site/`).
Built 2026-10-01 from Ridwan's Perplexity research thread (archived verbatim at `seo/reference/perplexity-seo-plan-2026-10-01.md`).

## What it does, every week

```
Business Profile (read first, always)
  → 1 Quick wins        GSC: high impressions + low CTR, page-2 rankings, decaying posts
  → 2 Topic selection   Ubersuggest + GSC queries + clusters, scored on intent/revenue, not volume
  → 3 Brief             title, meta, H1, H2/H3, internal links, CTAs by journey stage, schema, personalisation notes
  → 4 Draft             article in the client's voice, tied to real products
  → 5 Humanizer         full 11-pass pipeline, no em dashes (project-wide rule)
  → 6 Image             real store photo first, gpt-image second
  → 7 Finalize          body.html + publish.json
  → 8 Shopify DRAFT     hidden article; Ridwan approves in Shopify admin
  → 9 Log               content-log.csv
  → 10 Report           weekly scorecard + 30/90-day refresh queue
  → 11 Outreach         prospects + personalised pitches saved as Gmail drafts (never sent)
```

The full procedure is **`seo/SOP.md`**. The rules every stage follows are **`seo/config/seo-rules.md`**. The stage prompts are in **`seo/prompts/`**.

## Decisions (Ridwan, 2026-10-01)

| Question | Decision |
|---|---|
| Publishing | Create the article in Shopify as a **hidden draft**. Ridwan reviews and publishes it himself. The system never publishes. |
| Shopify access | Ridwan creates the custom app for tapandrate (setup steps below). |
| Data | GSC + GA4 are both available for tapandrate. |
| Images | Real store product photos first, gpt-image when no real photo fits. |
| Backlink outreach | Prospect list + personalised pitches saved as **Gmail drafts**. Ridwan sends them himself. |
| Trigger | Weekly cloud routine (primary), plus a desktop runner as backup (`seo/desktop/`). |
| koolestpro.com | Next.js site. Posts are committed as files in the site repo instead of going through the Shopify API (phase 2). |

## Layout

```
seo/
  README.md              this file
  SOP.md                 the weekly run, step by step (cloud + desktop both follow it)
  config/seo-rules.md    house rules: personalisation, competitor, site-first, data priority, clusters, CTAs, refresh, decision rules
  prompts/               00-business-profile … 08-outreach (one prompt per stage)
  clients/_template/     copy this folder to onboard a new client
  clients/tapandrate/    client.json, business-profile.md, clusters.md, baseline, logs, weekly runs in runs/YYYY-MM-DD/
  tools/                 store_snapshot.py, gsc_pull.py, shopify_publish.py (stdlib only, no pip install needed)
  desktop/               run-week.sh + launchd/cron setup (backup runner)
  reference/             the original Perplexity plan
```

## One-time setup per Shopify client

### 1. Shopify Admin API (lets the system create draft articles)
1. In the store admin: **Settings → Apps and sales channels → Develop apps** (or the Shopify Dev Dashboard if the store has moved to it) → create an app named `Koolestpro SEO`.
2. Admin API scopes: `read_content`, `write_content`, `read_products`, `read_files`, `write_files`, `read_online_store_pages`.
3. Install the app and copy the **Admin API access token** (`shpat_...`). Shopify only shows it once.
4. Store it as a secret, **never in git**:
   - Cloud: environment secrets `SHOPIFY_TAPANDRATE_DOMAIN` (the `xxxx.myshopify.com` domain) and `SHOPIFY_TAPANDRATE_TOKEN`.
   - Desktop: same two lines in the repo-root `.env` (already gitignored).
5. Test: `python3 seo/tools/shopify_publish.py --client tapandrate --check`. It lists the store's blogs and confirms the token works.

### 2. Google Search Console + GA4
`gsc_pull.py` uses an OAuth refresh token (no extra libraries).
1. Google Cloud console → create a project → enable **Search Console API** and **Google Analytics Data API**.
2. Create an **OAuth client ID** (type: Desktop app). Put the ID and secret in secrets as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
3. Run `python3 seo/tools/gsc_pull.py auth`, open the printed URL, sign in with the Google account that has access to tapandrate's GSC and GA4, and paste back the `code` from the redirect URL. It prints a `GOOGLE_REFRESH_TOKEN`. Save it as a secret.
4. Put the GA4 property ID (numbers only) in `clients/tapandrate/client.json → ga4_property_id`.
5. Test: `python3 seo/tools/gsc_pull.py pull --client tapandrate --days 28`.

Until these are set up, the pipeline still runs. It falls back to Ubersuggest data and writes the article files without pushing to Shopify. The run notes say which stage was skipped and why.

## Onboarding a new client
1. `cp -r seo/clients/_template seo/clients/<slug>` and fill in `client.json`.
2. Run stage 0 (`prompts/00-business-profile.md`) and review the result before any content is written.
3. Add that client's Shopify + GA4 secrets (`SHOPIFY_<SLUG>_DOMAIN` / `_TOKEN`).
4. Add the client to the weekly routine prompt.

## Hard rules (inherited from the root CLAUDE.md)
- Never publish live. The system stops at a hidden Shopify draft, and outreach stops at Gmail drafts.
- No em dashes, and the full humanizer pass on every piece of copy.
- Never invent a stat, review, client result or quote. Tap and Rate's own claims are used only as stated on their site.
- Never recreate a client's logo. Use real files.
- Secrets live in env/`.env`, never in this folder.

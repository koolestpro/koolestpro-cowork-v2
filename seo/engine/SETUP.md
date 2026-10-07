# Per-project setup

Every project gets its **own** keys in its own `.env` (copy `.env.example`). Nothing is shared between projects. Do only the sections this project needs. Check each one with the test command.

## 1. Google sign-in (Search Console, GA4, Keyword Planner, Sheets): free
One sign-in covers every Google API the engine uses.
1. https://console.cloud.google.com → create a project (e.g. `seo-<project>`).
2. **APIs & Services → Library**, and enable: *Google Search Console API*, *Google Analytics Data API*, and, if you'll use them, *Google Ads API* and *Google Sheets API*.
3. **OAuth consent screen**: External, add your Google account as a test user.
4. **Credentials → Create credentials → OAuth client ID → Desktop app**. Put the ID and secret in `.env` as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
5. `python3 seo/engine/tools/gsc_pull.py auth`, then sign in with the Google account that can see this site's Search Console (and GA4, Ads, the Sheet). Paste the code back, and put the printed `GOOGLE_REFRESH_TOKEN` in `.env`.
6. In `seo/project/project.json` set `gsc_property` (`sc-domain:example.com` for a domain property, or `https://example.com/` for a URL-prefix property) and `ga4_property_id` (Admin → Property details, digits only).
7. Test: `python3 seo/engine/tools/gsc_pull.py check`

Tip: while the consent screen is in "Testing", Google expires refresh tokens after 7 days. Publish the app (still free, no review needed for your own use) so the token keeps working.

## 2. Keyword Planner volumes: free, one-time approval
The free alternative to DataForSEO for search volumes. Autocomplete works without any of this.
1. Create a **Google Ads manager account** (ads.google.com/home/tools/manager-accounts), free, no ads needed.
2. Inside it: **Admin → API Center**, then accept the terms and copy the **developer token**. → `GOOGLE_ADS_DEVELOPER_TOKEN`
3. **Apply for Basic access** from the same page. The default Explorer/Test levels block keyword planning, and approval takes a few days. Describe the use honestly: "internal keyword research for my own/client websites, read-only".
4. Create (or link) a normal Google Ads account under the manager. You don't need to run ads. Its ID (digits only) → `GOOGLE_ADS_CUSTOMER_ID`, and the manager's ID → `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.
5. Make sure step 1's sign-in was done with a Google account that has access to these Ads accounts (re-run `gsc_pull.py auth` if not).
6. Test: `python3 seo/engine/tools/google_keywords.py check`

Accounts that don't spend on ads may see rounded volumes. That's fine for ranking topics against each other.

## 3. DataForSEO (optional, paid, per project)
Only if this project should pay for richer data (difficulty, results pages, backlinks, rank tracking).
1. Sign up at dataforseo.com (a small free credit, then a deposit to keep using it). Copy the **API login + password** from the dashboard.
2. `.env`: `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD`. In `project.json` set `"data_provider": "dataforseo"`.
3. Test: `python3 seo/engine/tools/dataforseo.py balance`

## 4. Shopify (platform `shopify`)
1. Store admin → **Settings → Apps and sales channels → Develop apps** (or the Dev Dashboard) → create an app.
2. Admin API scopes: `read_content`, `write_content`, `read_products`, `read_files`, `write_files`.
3. Install it and copy the Admin API token (shown once).
4. `.env`: `SHOPIFY_STORE_DOMAIN=<store>.myshopify.com`, `SHOPIFY_ADMIN_TOKEN=shpat_…`. In `project.json` set `blog_handle` (the blog's handle) and `blog_author`.
5. Test: `python3 seo/engine/tools/shopify_publish.py --check` (lists the store's blogs)

## 5. Next.js site (platform `nextjs-resources`)
In `project.json` set `site_repo`, `site_repo_path` (where it's cloned) and `articles_file`. The agent needs push access to open draft PRs. Test: `python3 seo/engine/tools/site_publish.py --run <a run with article.json> --dry-run`

## 6. Outreach hand-off
`project.json → outreach.mode`:
- `csv` (default, **manual**): each run writes `outreach.md` (pitches ready to copy) + `outreach-import.csv`. You send them yourself. Set `sender_name` / `sender_role` so the pitches are signed correctly.
- `gmail-drafts`: the agent creates Gmail drafts with its Gmail connector, in the mailbox the connector is signed into.
- `sheet` (**automated**): pitches go into the project's outreach Sheet unapproved, and the included Apps Script sender (`seo/engine/outreach-sender/`) emails approved leads from the business's own mailbox, with follow-up, stop-on-reply and alerts. Setup and the pre-flight checklist: **`outreach-sender/SETUP.md`**. Switching from `csv` to `sheet` later is just that setup plus changing `mode` and `sheet_id`; past runs and the log carry over.
Test any mode: `python3 seo/engine/tools/outreach_push.py --run <run with outreach.json> --dry-run`

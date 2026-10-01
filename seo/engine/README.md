# SEO Engine (portable kit)

A weekly, business-aware SEO system you drop into **any** project: a Shopify client, a Next.js site, or anything that can take an HTML article. Claude Code runs it. The engine learns the business first, picks one topic a week from real data, writes and humanizes the article, saves it as a **draft** (never live), tracks results, and queues link-building outreach for approval.

```
seo/
  engine/      ← THIS KIT. Identical in every project. Copy it in, never edit it per project.
  project/     ← this project's data (created by init.py): project.json, business-profile.md,
                 clusters.md, snapshot/, logs (*.csv), runs/YYYY-MM-DD/
.env           ← this project's own API keys (Google, Shopify, optional DataForSEO). Never committed.
```

## Install into a project (5 minutes)
1. Copy the `engine/` folder to `<project>/seo/engine/`.
2. From the project root:
   ```bash
   python3 seo/engine/tools/init.py --name "Business" --url https://example.com --platform shopify --location 2826
   ```
   This creates `seo/project/`, a filled-in `project.json` and `.env.example`, and adds `.env` to `.gitignore`.
3. Do the keys this project needs: **`SETUP.md`**. Every key is optional, and the engine skips what's missing.
4. Ask Claude Code: *"Run stage 0 of the SEO engine (seo/engine/prompts/00-business-profile.md)"*. Review the profile and clusters it writes. Every later stage depends on them.
5. Weekly: *"Run this week's SEO cycle per seo/engine/SOP.md"*, or schedule `desktop/run-week.sh`.

Suggested line for the project's `CLAUDE.md`: `SEO weekly run → read seo/engine/SOP.md, seo/engine/rules.md and seo/project/business-profile.md`.

## The weekly cycle (`SOP.md`)
Business profile → quick wins (Search Console) → topic scoring → brief → draft → humanizer → image → finalize + QA gate → **draft** (hidden Shopify article / draft PR / files) → log → weekly report → link-building outreach (queued, approved by a person).

## Data, free first
| Need | Free (default) | Paid option (per project) |
|---|---|---|
| Queries the site already gets | Search Console (`gsc_pull.py`) | |
| Keyword ideas | Google Autocomplete (`google_keywords.py suggest`, no key) | DataForSEO `ideas` |
| Search volumes | Google Ads Keyword Planner API (`google_keywords.py volume/ideas`, free, needs setup) | DataForSEO `overview` |
| Results page / People Also Ask | Web search | DataForSEO `serp` |
| Rank tracking | Search Console average position | DataForSEO `rank` |
| Competitor gaps / backlinks | Manual + web search | DataForSEO `gap` / `backlinks` |
Set `project.json → data_provider` to `free` or `dataforseo`. Ubersuggest, if it's connected in Claude, is used as an extra source either way.

## Tools (`tools/`, Python 3.9+, standard library only)
| Tool | What it does |
|---|---|
| `init.py` | Sets up `seo/project/` in a new project |
| `store_snapshot.py` | Public Shopify catalogue → `snapshot/` (products, collections, pages, blog URLs), so links are always real |
| `gsc_pull.py` | Google sign-in (`auth`), Search Console + GA4 pull |
| `google_keywords.py` | Free keyword research: Autocomplete + Keyword Planner |
| `dataforseo.py` | Optional paid data (the project's own account) |
| `md_to_html.py` | `article.md` → Shopify body HTML + FAQPage JSON-LD |
| `shopify_publish.py` | Creates the article as a **hidden** Shopify draft (QA gate built in) |
| `site_publish.py` | Inserts a typed article into a Next.js site's data file for a draft PR |
| `outreach_push.py` | Queues link-building pitches: Google Sheet, Gmail drafts or CSV, unapproved |

## Hard rules
Drafts only (never publish, merge or send without a person approving). No invented stats, reviews, prices or results. No em dashes. Keys only in `.env`.

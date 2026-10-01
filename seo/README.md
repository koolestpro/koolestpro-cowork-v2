# SEO for koolestpro.com

This project runs SEO for **koolestpro.com only**. Client SEO (e.g. Tap and Rate) lives in each client's own project folder, with its own copy of the engine and its own keys.

- `engine/`: the portable SEO kit. To use it for a client, copy this folder into their project and follow `engine/README.md`. Don't put Koolestpro-specific edits here, so it stays copyable.
- `project/`: Koolestpro's data: `project.json`, `business-profile.md`, `clusters.md`, logs, weekly `runs/`.

## How it runs for Koolestpro
| Part | Setup |
|---|---|
| Platform | `nextjs-resources`. Articles become typed entries in `content/resources.ts` of `koolestpro/koolestpro` (submodule `site/`), sent as a **draft PR**. Merging = publishing. |
| Keyword data | `free`: Search Console + Google Autocomplete + Keyword Planner (`engine/tools/google_keywords.py`). No DataForSEO. |
| Link-building outreach | `sheet`: pitches go into the **Koolestpro Outreach** Sheet (`outreach/gmail-sender/`) as `track = seo-links` leads with a 2-step sequence, unapproved. When you tick `approved` and set `email_status = valid`, the Apps Script sender emails them from your secondary Gmail, follows up in-thread, stops on reply and alerts you, all under the same caps, warm-up and TEST_MODE as cold email. |
| Schedule | Weekly cloud routine (Mondays 07:45 Lagos), or `engine/desktop/run-week.sh` on your Mac. |

## To finish setting up
1. **Google sign-in** (`engine/SETUP.md §1`), with Search Console for `koolestpro.com` and the Sheets API. Sign in with the account that owns koolestpro.com in Search Console, and share the Outreach Sheet with it as an editor.
2. **Keyword Planner** (`engine/SETUP.md §2`): developer token + Basic access (free; Google takes a few days to approve).
3. `project/project.json`: `ga4_property_id`, and `outreach.sheet_id` (the long ID in the Outreach Sheet's URL).
4. The outreach sender itself must be live (`outreach/README.md`, step 1: the real-account test). Until then, queued link pitches just wait in the Sheet.
5. Optional site change: inline links in article paragraphs (`project/business-profile.md §7`).

Keys go in the repo-root `.env` (gitignored) and in the cloud environment's secrets for the routine. `GOOGLE_CLIENT_ID`/`_SECRET` can reuse the values of the existing `GOOGLE_OAUTH_CLIENT_ID`/`_SECRET` (same OAuth client), but run `python3 seo/engine/tools/gsc_pull.py auth` once for a new `GOOGLE_REFRESH_TOKEN`, because the SEO engine needs Search Console, GA4, Ads and Sheets permissions.

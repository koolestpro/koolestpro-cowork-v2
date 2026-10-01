# Cold email outreach system (own "AI SDR")

Read this first before touching anything in `outreach/`. It is the handoff from the Claude chat sessions of 2026-09-27, where the plan and every decision below were made with Ridwan.

## What we are building

Ridwan's own version of Artisan Ava (he tried it, liked it, can't afford it yet): a system that finds e-commerce leads, gets and checks their emails, picks the right pitch, writes a 5-email sequence, sends it from Gmail with follow-ups, stops on reply, alerts him, and recommends replies he edits and sends. It must remember every lead: their business, every message both ways, the current stage, and a running summary of the relationship. KoolestFlow (`cold-email-app/`) becomes the dashboard over it.

The original research was a Perplexity thread (5 turns). Its useful parts are folded in here. Its email templates contained invented numbers ("lifted conversion 12-18%"); those must never be used.

## Decisions (Ridwan, 2026-09-27)

- **Free first.** Free tools everywhere until outreach wins paying clients. Upgrade only where quality clearly needs it.
- **Sending accounts:** secondary Gmails only, never his main Gmail. Starts with `koolestpro@gmail.com`; he has about ten more and will add them. Low volume, split across accounts, warm-up ramp.
- **Never cold email from `koolestpro.com`.** `info@koolestpro.com` (Cloudflare Email Routing, receive-only) stays the inbound/professional address. After the first paying client: one lookalike domain + 2 Google Workspace inboxes.
- **No Make for outreach.** His Make free plan is full with content distribution. Sending runs on Google Apps Script instead ($0, 100 recipients/day per consumer Gmail).
- **Google Sheets is the system of record for cold email**, not Supabase (he's wary of Supabase limits). KoolestFlow reads/imports from it (CSV import already exists). This is a deliberate exception to CLAUDE.md rule 3 for cold email only.
- **He approves the first batch** before anything goes to a real lead. After that, per-lead `approved` ticks.
- **Reply handling:** the AI drafts, Ridwan edits and approves, the system sends in-thread. The AI never replies to a lead on its own.
- **Lead types, all in parallel:** intent leads (hiring, launching, running ads, funded), agencies (white-label dev partner), general Shopify stores by niche, plus the existing Build/Fix/Scale tracks from `.ai-workflow/tools/lead_playbook.py`. Stored as `track` + `play` columns. Do NOT add a `segment` field (CLAUDE.md rule 4).

## Architecture

| Step | How | Status |
|---|---|---|
| Find leads | Existing weekly BrowserAct/Maps (Tue) + Ad Library (Wed) tasks, later agency + Shopify-store sources. Point them at the Sheet. | exists, not yet wired to the Sheet |
| Find + verify emails | Scrape site/contact pages, then MyEmailVerifier free API (100/day) | not built |
| Pick pitch + write 5 emails | Claude, from REAL proof only (`project_client_history` / CLAUDE.md rule 2), humanizer rules, no em dashes, under ~100 words, plain text, no links in email 1 | not built |
| Approve | `approved` checkbox in Leads tab | built |
| Send, follow up, log, stop on reply, alert, bounces | `outreach/gmail-sender/Code.gs` (Apps Script, one copy per Gmail, shared Sheet) | built, simulated only |
| Reply drafts + relationship memory | On a new reply: AI reads Profile + full Messages thread + Memory, writes a Drafts row and updates the Memory summary. Preferred: fast (Apps Script calling a cheap AI API within minutes); fallback: Claude scheduled task twice a day | not built (Drafts/Memory tabs exist) |
| SEO link-building leads | `seo/engine/tools/outreach_push.py` appends prospects from the weekly SEO run to Leads/Profiles/Sequence as `track = seo-links` (2-step sequence, `approved = FALSE`, `email_status = unchecked`). Same sender, caps and approval as cold email. Step 1 carries no link. See `seo/README.md`. | built |
| Dashboard | KoolestFlow lead page: profile, timeline, stage, editable suggested reply, Send (sets draft to Approved) | not built |

## What exists now

`outreach/gmail-sender/` — `Code.gs`, `appsscript.json`, `SETUP.md`.
- Creates 7 tabs: Settings, Leads, Profiles, Sequence, Messages, Memory, Drafts (schema = `TABS` at the top of `Code.gs`).
- Hourly: sends due follow-ups first, then approved first emails. Cap 5/day in week 1, +5/week, max 20/day, max 2 per run, 9am-5pm Lagos. Steps 2-5 go in the same Gmail thread (Gmail advanced service, In-Reply-To). Only steps 2+ use `Re: <step 1 subject>`.
- Every 30 min (`tick`): logs replies and Ridwan's manual Gmail replies, stops the sequence on reply, adds a `Needs draft` row, emails ALERT_EMAIL, sends drafts marked `Approved`, marks bounces.
- `TEST_MODE=TRUE` by default: everything goes to ALERT_EMAIL. ALERT_EMAIL must be his main Gmail, not the sending account.
- Verified only against a mocked Sheet/Gmail in Node. **Not yet confirmed running in a real Google account** — ask Ridwan whether he completed SETUP.md and the test.

## Next, in order

1. Confirm the real-account test worked; fix anything it surfaced.
2. Reply drafts + Memory summaries (decide: AI API from Apps Script vs Claude scheduled task).
3. Email finding + MyEmailVerifier.
4. Sequence writer (5 emails per lead from Profile + track/play + real proof). First batch goes to Ridwan for approval.
5. Lead finders write to the Sheet (dedupe against the Sheet and `.ai-workflow/taken-brands-ledger.json`).
6. KoolestFlow dashboard over the Sheet.

## Costs (target)

About $4-5/month total, mostly existing BrowserAct credits. Sheets, Apps Script, MyEmailVerifier free tier, Gmail: $0. Make is not used for outreach (if content ever outgrows Make free: Core is $9/mo yearly for 10,000 credits).

## Don'ts

- No invented results or numbers in any email. Concept brands (KURA, HALOS, MERIDIAN, Lumora) are never presented as clients.
- No sending from Ridwan's main Gmail or from koolestpro.com.
- Nothing reaches a real lead while TEST_MODE is TRUE or before Ridwan approves.
- Don't create Google or Gmail accounts; Ridwan does that himself.
- Update the Build Log in `docs/koolestpro-content-operating-plan.md` whenever this system changes.

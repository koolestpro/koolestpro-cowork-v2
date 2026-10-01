# Research behind the outreach system

`perplexity-thread-2026.md` is the original 5-turn Perplexity research thread Ridwan ran before building this. Saved here 2026-10-01 so the origin is in the repo. Read it for the reasoning; read `../README.md` for what was actually decided and built.

**Do not copy its templates as written.** Its example emails contain invented results ("lifted conversion 12-18% in 3 weeks", "went from X% to Y% in 4 weeks", "We've delivered X stores for agencies like yours"). Project rule 2: never invent a client result. Use the structure, never those claims.

## What the thread proposed and where it stands

| Thread idea | Status |
|---|---|
| Make + n8n orchestration | **Replaced** (Ridwan, 2026-09-27): Google Apps Script on the Sheet, $0, Make plan is full with content |
| Google Sheet as CRM, multi-Gmail sending, warm-up, reply stop + alert | Built (`gmail-sender/`) |
| Email finding + MyEmailVerifier (100/day free) | Built (`Pipeline.gs`) |
| AI picks a "play" per lead, writes the 5-email sequence | Built for stores; `play` does not yet change the pitch |
| Sequence timing days 1, 4, 8, 13, 18-20 | Built: `FOLLOWUP_GAPS` 3,4,5,6 is exactly this |
| Email 1: under 100 words, plain text, no links, one ask, first line about them | Built (brief + prompt) |
| Reply alerts, reply classification, drafts | Alerts + AI reply drafts built; no classification label yet |
| Lead source C: general Shopify stores by niche | Built (Discovery, Sources, scoring, Apify connector untested) |
| **Lead source A: intent signals** (hiring a marketer or Shopify dev, just launched or redesigned, funding, heavy ads, "need a Shopify developer" posts) | **Not built.** The thread calls this the highest-converting source |
| **Lead source B: agencies and white-label partners** | **Not built.** Only a lead type name in the README |
| Plays: `cro_sprint`, `agency_partner`, `whitelabel_partner`, `redesign_audit` | Names exist; only store plays are written |
| `segment` field (intent_lead, agency_lead, ...) | **Not used**: project rule 4 forbids it. Use `track` + `play` instead |
| LinkedIn touch day 2, X touch day 6, Calendly link, Telegram alerts | Not built (email first; alerts go to Gmail and the KoolestFlow screen) |
| Shopify Partner Directory and Clutch profiles (inbound) | Not built |
| Productized offers and retainers (CRO Sprint, SEO overhaul, 30-day redesign, maintenance $500-2,500/mo) | Not built as pages; prices in `../BRIEF.md` |
| Lookalike domains + Workspace inboxes | Deferred until the first paying client (Ridwan) |

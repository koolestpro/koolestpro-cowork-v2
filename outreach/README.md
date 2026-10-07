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

## AI provider order (2026-09-30)

Ridwan's decision: Gemini free is the main model. Claude (Anthropic) is not funded and will not be. DeepSeek is unfunded for now. Test AI on 2026-09-30: Gemini OK, Claude "credit balance too low", DeepSeek 402 insufficient balance. Set Settings `AI_ORDER` = `gemini` until DeepSeek is funded, then `gemini,deepseek`. Gemini calls already retry on 503 and fall back across Google's model names.

## Agencies and intent signals (2026-10-01)

Agency partner track built: `PARTNER-OFFER.md` (offer, proposed rate card), `scoreAgency_` in `Discovery.gs`, partner sequence in `Pipeline.gs`, `SIGNATURE_PARTNER`, partner section in `brief-ai.md`. Intent signals from job postings are designed in `INTENT-SIGNALS.md`, not built. Upwork and Contra postings cannot be traced to companies (terms forbid scraping, client names hidden).

## Lead scoring and data sources (2026-10-01)

`outreach/SCORING.md` is the full rubric (gates, points, business model: own-brand versus dropship, platforms) and the table of data-source options and costs. Scoring lives in `gmail-sender/Discovery.gs`.

## Voice and messaging (2026-09-30)

`outreach/BRIEF.md` is the master brief (who Ridwan is, real proof, offers, limits, regional voice, email and reply structure, humanizer rules, and section 12 of open decisions). `brief-ai.md` is the compact version the AI reads; `build_brief.js` compiles it to `gmail-sender/Brief.gs`. Regional voice is chosen from the lead's `country`: Nigeria/Africa (time-based greeting, warm), UK, US/Canada, Europe, other. Drafts get a `CHECK:` note in the `model` column if they contain a blocklist phrase, a number or price, or a link. The script emails a daily report at 6pm.

## Architecture

| Step | How | Status |
|---|---|---|
| Find leads | Existing weekly BrowserAct/Maps (Tue) + Ad Library (Wed) tasks, later agency + Shopify-store sources. Point them at the Sheet. | exists, not yet wired to the Sheet |
| Find + verify emails | `Pipeline.gs`: scrapes site/contact pages (own domain or a free-mail address they published), then MyEmailVerifier free API | built, mock-tested, needs a real run + verifier key |
| Profile + write 5 emails | `Pipeline.gs`: fetches the site, AI builds a Profile from real page facts, then writes the 5-email sequence from `BRIEF_` (real proof only, region voice, no em dashes, under ~100 words, no links in email 1). `{{greeting}}` is filled at send time from the lead's clock. `notes` records the observation basis and any `CHECK:` flags. `AUTO_APPROVE` setting optional. | built, mock-tested, needs a real run |
| Approve | `approved` checkbox in Leads tab | built |
| Send, follow up, log, stop on reply, alert, bounces | `outreach/gmail-sender/Code.gs` (Apps Script, one copy per Gmail, shared Sheet) | built, simulated only |
| Reply drafts + relationship memory | Decided 2026-09-30: Apps Script calls AI in order Gemini free, Claude Haiku, DeepSeek fallback (keys in Script Properties, order in Settings `AI_ORDER`). Reads Profile + Messages thread + Memory, writes the draft (Ready for review) and updates Memory. Never sends; Ridwan approves. | built; real-account test (SETUP.md 3b) done and passed per Ridwan 2026-10-04. `VOICE_EXAMPLES` cell in Settings was still EMPTY when checked 2026-10-04 |
| Daily report | `dailyReport` at 6pm emails ALERT_EMAIL: sent, replies, drafts to review, queue, pipeline | built |
| Dashboard | KoolestFlow (`koolestpro/cold-dm-app`, the `cold-email-app` submodule) has a **Cold email** screen over the Sheet through `Api.gs` (Apps Script web app, secret token) and `backend/outreach_bridge.py`. Sheet stays the source of truth. See SETUP.md 3c. | built 2026-10-01 on branch `claude/outreach-alert-email-debug-b2d85x` of cold-dm-app; mock and browser tested, not yet against the real Sheet |

## What exists now

`outreach/gmail-sender/` — `Code.gs`, `appsscript.json`, `SETUP.md`.
- Creates 7 tabs: Settings, Leads, Profiles, Sequence, Messages, Memory, Drafts (schema = `TABS` at the top of `Code.gs`).
- Hourly: sends due follow-ups first, then approved first emails. Cap 5/day in week 1, +5/week, max 20/day, max 2 per run, weekdays 9am-5pm in the LEAD's own time zone (decided 2026-09-30). Steps 2-5 go in the same Gmail thread (Gmail advanced service, In-Reply-To). Only steps 2+ use `Re: <step 1 subject>`.
- Every 30 min (`tick`): logs replies and Ridwan's manual Gmail replies, stops the sequence on reply, adds a `Needs draft` row, emails ALERT_EMAIL, sends drafts marked `Approved`, marks bounces.
- `TEST_MODE=TRUE` by default: everything goes to ALERT_EMAIL. ALERT_EMAIL must be his main Gmail, not the sending account.
- Confirmed working in Ridwan's real Google account on 2026-09-30 (TEST_MODE): send, reply, Replied stage, Drafts row and alert email all worked. Fixed that day: test-row seeding and row appends (the checkbox column pre-fills FALSE down 2000 rows, so `getLastRow()` and `appendRow` are unreliable on Leads). Still to test: approving a draft sends in-thread, and follow-ups (step 2).

## Next, in order

1. ~~Confirm the real-account test worked~~ done. Remaining: test sending an approved draft, then go live (SETUP.md section 4).
2. ~~Reply drafts + Memory summaries~~ built and tested 2026-10-04 (3b). Open: paste 3 to 5 real replies into Settings `VOICE_EXAMPLES` (empty on 2026-10-04).
3. ~~Email finding + MyEmailVerifier~~ built (needs real run + key).
4. ~~Sequence writer~~ built (needs real run). First batch goes to Ridwan for approval.
5. Lead finders write to the Sheet. **Started 2026-09-30:** `Discovery.gs` qualifies any list of store domains (upcoming-brand score, see BRIEF.md 4b) into Leads. `Sources` tab imports domains from public list pages (Merchant Genius, ZIK new stores, cro.media, techpeeker, eachspy, BuiltWith free list, sellerdirectories; none could be inspected from the Claude sandbox, so each needs a real run to confirm it yields domains). No-website businesses with an email (Maps) go straight into Leads as track Build. **Directory scraping moved to the Mac 2026-10-04** (see section below). Still to build: Reddit and ad-library scans, the Maps bridge into the Sheet and dedupe against `.ai-workflow/taken-brands-ledger.json`.
6. ~~KoolestFlow dashboard over the Sheet.~~ Built. 2026-10-04: merged into local `main` of `cold-email-app` (`4b093e5`) but NOT yet pushed to GitHub/Vercel, so the live app has no Cold email screen. Ridwan pushes from Mac Terminal, then sets `OUTREACH_API_URL` and `OUTREACH_API_TOKEN` on Vercel and redeploys.

## Costs (target)

About $4-5/month total, mostly existing BrowserAct credits. Sheets, Apps Script, MyEmailVerifier free tier, Gmail: $0. Make is not used for outreach (if content ever outgrows Make free: Core is $9/mo yearly for 10,000 credits).

## Don'ts

- No invented results or numbers in any email. Concept brands (KURA, HALOS, MERIDIAN, Lumora) are never presented as clients.
- No sending from Ridwan's main Gmail or from koolestpro.com.
- Nothing reaches a real lead while TEST_MODE is TRUE or before Ridwan approves.
- Don't create Google or Gmail accounts; Ridwan does that himself.
- Update the Build Log in `docs/koolestpro-content-operating-plan.md` whenever this system changes.

## Directory scraping on the Mac (2026-10-04)

The cloud and Apps Script (`Sources` tab) cannot read these directories (blocked). A Playwright script on Ridwan's Mac can: `outreach/scrapers/directory_scrape.py`. It pushes new store domains to the Sheet's Discovery tab through `Api.gs` `add_domains` (same token as KoolestFlow), after deduping against its own state, the taken-brands ledger and the Sheet. Setup: `bash outreach/scrapers/install_mac.sh` in Mac Terminal (installs Playwright, optional daily 07:30 launchd job). Test with `--dry-run --headed` first.

Checked in Ridwan's real Chrome on 2026-10-04:
- **Works:** Merchant Genius (dated pages `/shop/date/YYYY-MM-DD`, about 500 stores a day, some with email and phone; newest date listed on 2026-10-04 was 2026-07-28, so the site may lag), Zik (renders with JavaScript; its "new stores" list showed 2024 launch dates), EachSpy (country pages, about 40 domains each, includes big brands the scorer will drop).
- **Does not work:** cro.media (Cloudflare block even in a normal browser), BuiltWith (CAPTCHA; never bypassed), TechPeeker (free page shows 10 stores), SellerDirectories (a sales page for a paid database).
- Not yet run end to end: the script was written without being able to run Playwright against the sites from here. First real run needs a look.

### Update 2026-10-04 (evening): richer rows, best email, myip.ms
- The noisy Discovery rows (googlesyndication, json-schema, shopifysvc, "DNS error") came from the old Apps Script `Sources` importer, which grabs anything domain-shaped. It now skips the directories the Mac scraper handles, and `INFRA_DOMAINS_` in `Discovery.gs` drops infrastructure hosts.
- The scraper now keeps everything visible per store: name, country (from currency), ALL emails, phone, description, launch date, theme and size signals. It pushes them with the new `Api.gs` action `add_discovery_rows`. New Discovery columns: `brand`, `contact_name`, `emails`, `phone` (run Outreach > Set up tabs once).
- When Discovery promotes a store to Leads it keeps the best email by `rankEmail_` / `pickBestEmail_` in `Pipeline.gs`: own domain first, then a decision maker (founder, owner, ceo, or a name matching the contact), then a person-style address, then shared inboxes (hello, info, contact), then ticket desks (support, orders). Bounce traps (noreply, billing, careers) are never chosen. The other emails stay in the lead's `notes`. The on-site email finder uses the same ranking.
- Added source `myipms` (myip.ms Shopify IP-owner page). Free list is sorted by world rank, so big brands come first and are dropped (rank under 300,000). Stops on a CAPTCHA, never bypasses it.
- Not built: finding a named owner's email when the directory only gave info@ (would need an owner-name source such as the store's About page or LinkedIn).

## Store research, offers, big-brand gate, decision makers (2026-10-06, Ridwan's test-phase feedback)

Feedback, in two rounds: the problem paragraph was generic and once cited a non-error; never claim speed problems; never pitch small fixes; big brands (Allbirds-size) must never be emailed, the target is upcoming stores under about 1,000 visits a day; stores that already look excellent should be offered something they do not have (advertorial or listicle built in Replo, post-purchase upsell, bundle builder, custom feature); understand the business well enough to propose a build; and write to the decision maker, not whoever reads info@. Wrong or invalid emails should fall back to the address on the site.

- **Research** (`gmail-sender/Research.gs`), method taken from the `koolestpro-client-audit` skill (funnel discovery, Tier 1 fix what leaks, Tier 2 add what is missing) and `koolestpro-store-auditor-skill-a` (specific, located, real data only). Per store: catalogue (prices, product types, examples), one product page, the funnel (sitemap custom pages such as "5-reasons-why" listicles, advertorials, quizzes and bundle pages; hidden paths like `/pages/advertorial`; funnel subdomains `try.`, `get.`, `offer.` and others via Google DNS; page builders such as Replo, GemPages, Zipify, Funnelish; ad pixels; upsell, post-purchase, bundle, subscription and quiz apps), the About page (founder name, team size) and social links. Lines are labelled MEASURED, SEEN or SOFT. A SOFT gap (for example "no advertorial found") is never stated as fact; the email asks instead, because advertorials on a separate domain can only be found from the brand's ad landing URLs (Meta Ad Library), and post-purchase offers run inside checkout where nobody outside can see them.
- **One offer per store**: page_rebuild, speed, advertorial, listicle, post_purchase, bundle_builder, quiz, subscription or custom_feature, with the problem, evidence, cost and exactly what Ridwan would build, scored 1 to 5. Small fixes and taste score low, as does speed without a `[SPEED]` line, and never carry an email. Under `MIN_PROBLEM_SCORE` (4) the lead is held with a `HOLD:` note. Columns in Profiles: `offer`, `problem`, `problem_evidence`, `problem_page`, `problem_worth`, `second_problem`, `decision_maker`, `team`, `research`, `socials`.
- **Speed only when obviously slow** (revised same day, Ridwan: speed is a genuine reason to get answers, but only when the store is clearly slow). `speedCheck_` emits a `[SPEED]` evidence line only when (1) Google's real-user data (Chrome UX Report) rates the page or site SLOW with main content at or above `SPEED_FIELD_LCP` seconds (4) for 1 in 4 phone visits, or (2) with no real-user data, two lab runs on a phone both show at least `SPEED_LAB_LCP` seconds (8) and a score of 35/100 or less. When real-user data exists it decides, and the lab test is ignored. Otherwise nothing is recorded, so speed cannot be mentioned. An email that talks about speed without a `[SPEED]` line gets a `CHECK:` flag. The old homepage "page load" signal stays removed. Needs `PAGESPEED_API_KEY`.
- **Big brands are never emailed**: Discovery skips any store inside the Tranco top 1M traffic list (`BIG_BRAND_RANK`, free API; checked 2026-10-06: allbirds.com #68,376, manitobah.com #593,113, aminazaid.com and scentsavenue.ng unranked). Research re-checks and marks a big brand Lost, also on two strong scale signals (enterprise app stack, 250+ products, 6+ languages) or one strong plus a physical-store or careers signal.
- **Decision maker**: the founder or owner from the About page becomes `contact_name`. If the lead's email is a shared inbox (info@, hello@, support@...), the pipeline tries the founder's own address (Hunter if keyed, then first@, first.last@ ...), verifies it and swaps it in when valid. If it stays on a shared inbox and the team is not solo, the sequence gets a `CHECK:` flag, so it is never auto-approved.
- **Footer emails were cut off**: `fetchPage_` kept only the first 400KB; big pages put the footer past that. It keeps head and tail now. `rankEmail_` counts brand.ca on brand.com as the store's own domain.
- **Email rescue**: an invalid or risky email is replaced by the first verified address from the site, Hunter.io (optional `HUNTER_API_KEY`) or common role addresses; once per lead (`email_rescue`), old address kept in `notes`.
- **There is no way to list every mailbox on a domain.** Mail servers do not publish them and the SMTP commands that could (VRFY, EXPN) are off almost everywhere. Only published addresses (site, Hunter, Snov, Apollo) and verified guesses work.
- Proof added to the brief from Ridwan's message: Mother of Macros work included a shorter checkout flow and a bundle builder page. **Ridwan to confirm** that this is right (he named Tap and Rate and Mother of Macros together).
- Tested 2026-10-06 in a Node mock of Apps Script against live sites: big-brand gate, funnel detection (jonesroadbeauty.com: listicles, quiz, AfterSell found), decision-maker swap, shared-inbox flag, email rescue. Not yet run in the real Sheet with Gemini.
- **Fact check and hidden text (2026-10-07, from two wrong test emails).** District Lounge was told every featured product was sold out: all 18 were in stock; the text came from the theme's hidden `<span class="sold-out-message hidden">` labels. Nomalife was told buyers wonder what Rise does, how fast and what if it fails: the page shows 84 reviews, a 30-day money-back guarantee and an FAQ answering both. Fixes: `stripHidden_` drops short hidden labels (long hidden blocks are accordions a shopper opens, so they stay); `factCheck_` tests every claim before an email is written: stock claims against the product feed, everything else by a skeptical AI pass over the visible product page, homepage and about text. A failed claim falls back to the second problem if that passes, else the lead is held. The profile prompt now forbids "buyers of X usually wonder Y" claims and treats stock as a supply decision, never the reason to email. New gate: vapes, nicotine, tobacco, kratom, replicas and weapons are never emailed (District Lounge sold bulk disposable vapes in Australia, ordering by WhatsApp and Telegram).
- **No language, translation or currency points (2026-10-07, Ridwan).** sellare-es.com was emailed about "Italian cart words" on a Spanish store. Stores adapt language and currency to the visitor's country, and research browses from Google servers abroad, so what it sees is not what their customers see. Blocked three ways: the research prompt never picks them, `factCheck_` rejects any such claim, and an email that mentions them gets a `CHECK:` flag (`LOCALE_WORDS_`). Also in the brief.

## Finding rules are shared with the CRO skills (2026-10-07)

Every lesson from a wrong email (Nomalife, District Lounge, Sellare) is written into `docs/system/cro-finding-rules.md`, which both CRO skills carry as `references/finding-rules.md`. **Standing rule: when a finding turns out wrong anywhere (post, audit or email), add the case to that file, run `python3 .ai-workflow/tools/sync_cro_rules.py`, and mirror any rule the code can enforce in `Research.gs`.** Then Ridwan re-uploads the two skills on claude.ai.

## Live sites, right recipients, dead proof (2026-10-07)

- **Only live stores.** framelo.com was emailed while it redirected to a domain-for-sale page (brandsly.com). `siteStatus_` (Research.gs) follows redirects by hand and rejects: HTTP 4xx/5xx, unreachable, redirects to domain marketplaces or parking pages, redirects to a different domain (moved or sold), password pages, parked/for-sale/closed/"coming soon" pages, near-empty pages. It runs three times: at Discovery (never becomes a lead), before research (marked Lost), and right before the first email is sent (marked Lost, not sent). Checked on live domains 2026-10-07: framelo.com and aminazaid.com dead; scentsavenue.ng, nomalife.com, sellare-es.com live.
- **Right recipient.** Directories often carry a Gmail or an old agency address. `recipientCheck_`: an address that is not on the store's own domain is kept only if the store publishes it on its own site; otherwise the best verified address the site publishes replaces it; if the site publishes none, the lead gets `[UNCONFIRMED RECIPIENT]` in notes and its sequence a `CHECK:` flag, so it is never auto-approved. Maps leads without a website keep their Maps email.
- **Dead proof.** aminazaid.com is down (404). The brief now names Amina Zaid as a business only, never the domain; drafts naming aminazaid.com, justdarlings or Jellys Glamour domains get a `CHECK:` flag. scentsavenue.ng is the one live Nigerian proof link.
- **GitHub scrape removed.** `.github/workflows/directory-scrape.yml` deleted at Ridwan's request (scraping runs elsewhere now; it was failing and emailing him). The repo secrets `OUTREACH_API_URL` and `OUTREACH_API_TOKEN` are no longer used by GitHub and can be deleted in the repo settings.

## Pre-launch stores: track Launch (2026-10-07, Ridwan)

Password and coming-soon pages are no longer treated as dead: the founder is building the store right now, which is the best moment to talk. `siteStatus_` returns `prelaunch: true` for a Shopify password page (proof on its own) or for "coming soon / launching soon" wording on a small page with no products or add-to-cart (so a live store saying "new drop coming soon" stays a normal store). Parked, for-sale, closed and 404 sites are still dead.

What can be offered, since nothing behind the password is visible (`LAUNCH_PROFILE_SYS_`, `launchFacts_`):
- **launch_review** (default): a free look at their product page before launch if they share the store password. Low friction, real value, and it starts the conversation.
- **launch_build**: help finish or build the store so it launches properly (product pages, homepage, theme setup).
- **waitlist_page**: only when the coming-soon page has no email signup: a page that collects emails before launch so the first day has buyers.
- **launch_creatives**: launch ad creatives from their product photos, when their socials show the products.

The email opens with what is visible (the coming-soon page, a stated launch date, the signup form or its absence), never claims anything about the store behind the password, and asks whether they are building it themselves or someone is helping. Launch leads are exempt from `MIN_PROBLEM_SCORE` (the timing is the reason). New Settings row `SIGNATURE_LAUNCH`. Discovery already gives a password page +15.


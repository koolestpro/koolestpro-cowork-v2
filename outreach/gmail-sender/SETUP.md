# Outreach sender: setup (about 10 minutes)

Do this signed in as **koolestpro@gmail.com**.

## 1. Make the Sheet and paste the script
1. Go to sheets.new. Name it `Koolestpro Outreach`.
2. Extensions > Apps Script. Delete what's there and paste all of `Code.gs`.
3. Project Settings (gear icon) > tick **Show "appsscript.json" manifest file**. Open `appsscript.json` in the editor and replace it with the one in this folder. (This turns on the Gmail service and sets Lagos time.)
4. Save. Close the script tab and reload the Sheet. An **Outreach** menu appears.

## 2. Set up the tabs
1. Outreach > **1. Set up tabs**. Google asks for permission the first time. Click through ("Advanced > Go to project" is normal for your own script).
2. Open the **Settings** tab. Change **ALERT_EMAIL** to your main Gmail. Leave **TEST_MODE = TRUE**.

## 3. Test it (nothing reaches a real lead)
0. No `test-001` row (or it's half-filled)? Outreach > **Create / reset test lead**. It rebuilds a complete one.
1. In **Leads**, tick **approved** on the `test-001` row. Nothing is sent by ticking alone.
2. Outreach > **Send due emails now**. If it says `0 sent`, the message tells you which requirement is missing (approved, `email_status` = `valid`, a step 1 row in **Sequence**). Step 1 lands in your main Gmail with `[TEST to ...]` in the subject.
3. Reply to that test email from your main Gmail. The alert email is sent only when a reply arrives, not on approval or send. Then Outreach > **Check replies now**. The lead moves to **Replied**, the follow-up is stopped, a row appears in **Drafts**, and you get an alert.
4. In **Drafts**, type something in `draft_body`, set status to **Approved**, then **Check replies now** again. It sends in the same thread.

## 3a. Three files now
The script is `Code.gs`, `Brief.gs` (the master brief, compiled from `outreach/brief-ai.md`) and `Pipeline.gs` (finds emails, verifies them, profiles each store, writes the 5-email sequences). Add each as its own file in Apps Script (+ > Script). After editing `brief-ai.md`, run `node outreach/build_brief.js` and paste the new `Brief.gs`. Run Outreach > **1. Set up tabs** once (adds new columns and Settings rows) and **2. Turn on automation** once (adds the new triggers).

**Finding leads (Discovery tab).** Paste store domains into the **Discovery** tab, one per row, column `domain` (optionally `niche`, `country`, `source`), leave `status` blank. Every 30 minutes, or via Prepare new leads now, each store is checked from its own public pages and scored: small catalogue, young store, default or free theme, light app stack, target market. Stores scoring at least `MIN_FIT_SCORE` (55) become Leads; others are marked Skipped with the reasons so nothing is checked twice. Sources for the domain lists: store-finder tools and Apify scrapers (export a CSV), Google `site:myshopify.com` searches, Reddit and Shopify-community "rate my store" posts, Meta Ad Library.

**Sources tab (automatic imports).** The Sources tab lists public pages that contain store domains (Merchant Genius, ZIK's new-stores list, cro.media, techpeeker, eachspy, the BuiltWith free list, sellerdirectories are pre-filled; add your own, optionally with `niche`, `country`, and `{page}` in the URL with `max_pages` for paginated lists). Each active source is read once every 20 hours; new domains go into Discovery. The `result` column says what happened. A page behind a login or built with JavaScript finds 0 domains: use that site's own export instead and paste the domains into Discovery. Check each site's terms before scraping it. Menu: Outreach > **Import store lists now**.

**Apify test (optional, costs money, off until you say so).** 1) Make an Apify account and create an API token (Console > Settings > Integrations). 2) Apps Script > Project Settings > Script properties: `APIFY_TOKEN` = the token. 3) Pick an actor, for example a Store Leads based store finder (Apify Store > search "store leads"). Check its price per 1,000 results first. 4) In the **Apify** tab add a row: `actor` (username/actor-name from its page), `input_json` (copy the actor's own Input JSON from its Input tab and set your filters: small stores, your countries, new stores), `max_items` = 50, `status` = Ready. 5) Outreach > **Run Apify imports now**. It starts the run (status Running); run it again a minute later to import. New stores land in Discovery with the raw result in the `data` column and any sales or employee numbers in `signals`. Stores whose `signals` show more than 30 employees are skipped automatically. Send me one row of the `data` column and I will wire the exact field names into the scoring.

**Directory sites run from the Mac, not from here.** The Sources tab cannot read most directories (blocked). Use `outreach/scrapers/directory_scrape.py` on your Mac instead (see README, "Directory scraping on the Mac"); it feeds this same Discovery tab.

**Businesses with an email but no website** (for example from Google Maps): add them straight into Leads with `brand`, `email`, `country`, `niche`, `notes` (rating, reviews, city) and leave `website` empty. They are treated as track Build: email 1 offers a free ad creative.

**How a new lead flows:** put a row in Leads with `lead_id`, `brand`, `website`, `country`, `niche`, `track` (and `contact_name`, `email` if you have them). Every 30 minutes, or via Outreach > **Prepare new leads now**, the script finds an email on their site if `email` is empty, verifies it, writes the Profile, then writes the 5-email Sequence. Check `notes` on the lead: it says what the first email's observation is based on, and `CHECK:` if something needs your eyes. Then tick `approved` (or set `AUTO_APPROVE` = TRUE in Settings to auto-approve clean ones). Sending follows each lead's own working hours (9 to 5, weekdays, from `time_zone` or their country).

**Store research, offers, big-brand gate, decision makers (added 2026-10-06).** Add `Research.gs` as a file, paste the new `Pipeline.gs`, `Code.gs`, `Discovery.gs` and `Brief.gs`, then run Outreach > **1. Set up tabs** once (adds the Profiles columns `problem`, `problem_evidence`, `problem_page`, `problem_worth`, `second_problem`, `research`, `socials`, `offer`, `decision_maker`, `team`, the Leads column `email_rescue`, and the Settings rows `MIN_PROBLEM_SCORE`, `BIG_BRAND_RANK`, `INSTAGRAM_LOOKUP`). Settings rows `SPEED_FIELD_LCP` and `SPEED_LAB_LCP` are added too.
- `PAGESPEED_API_KEY` (Script property, free, needed for speed): Google Cloud Console > APIs & Services > enable "PageSpeed Insights API" > Credentials > Create API key. Without it Google's shared quota is usually used up and speed is simply never pitched.
- `HUNTER_API_KEY` (Script property, optional, free plan 25 domain searches a month): hunter.io > API. Used to find a founder's own address and to replace emails that fail verification.
- Instagram: `INSTAGRAM_LOOKUP` = free (default, often blocked), apify (needs `APIFY_TOKEN`, paid per profile), or off. LinkedIn cannot be read without a login; only the link is recorded.
- Test phase: Outreach > **Redo research + emails for unsent leads** supersedes the Draft emails of every lead not yet emailed and researches them again (big brands among them become Lost). Sent emails are never touched.

Email verification: get a free key at myemailverifier.com and add Script property `MYEMAILVERIFIER_API_KEY`. Without it, emails stay `unverified` and are never sent. Verify the response format against their docs the first time; Valid is sent. Invalid never is. Catch-all (the domain accepts every address, so the mailbox is unproven) is sent only if you set `SEND_TO_CATCH_ALL` = TRUE in Settings. Unknown or grey-listed is `risky` and never sent.


The script is `Code.gs` plus `Brief.gs` (the master brief, compiled from `outreach/brief-ai.md`). In Apps Script click **+** > Script, name it `Brief`, and paste `Brief.gs`. After editing `brief-ai.md`, run `node outreach/build_brief.js` and paste the new `Brief.gs` again. Also run Outreach > **2. Turn on automation** again once, to add the 6pm daily report trigger. Try it with Outreach > **Send daily report now**.

**Nothing sending?** Outreach > **Why isn't it sending?** checks the settings, today's cap, and every lead, and names the exact reason for each.

## 3e. Agencies (the Partner track)
The offer is in `outreach/PARTNER-OFFER.md`. To find agencies: paste agency domains into the **Discovery** tab with `track` = **Partner**, or use Sources rows with `track` = Partner (Clutch and the Shopify Partner Directory are pre-filled after you run **Set up tabs**; if they return 0 domains, copy domains by hand). Agencies are scored by `scoreAgency_` (see SCORING.md section 7), promoted to Leads as track Partner, play `agency_partner`, then go through the normal email finding, verification, profile and a dedicated partner sequence. Their signature is `SIGNATURE_PARTNER`. Partner rates are only stated by the AI when the agency asks.

## 3d. Flexible signatures
The signature is chosen per email, most specific first (only non-empty cells count): the lead's own `signature` cell in Leads > `SIGNATURE_<PLAY>` (e.g. `SIGNATURE_CRO_SPRINT`) > `SIGNATURE_BUILD` / `SIGNATURE_FIX` / `SIGNATURE_SCALE` (by the lead's track) > `SIGNATURE_NG` / `SIGNATURE_UK` / `SIGNATURE_US` / `SIGNATURE_EU` (by market) > `SIGNATURE`. Follow-ups (steps 2 to 5) and replies use `SIGNATURE_FOLLOWUP` (default just "Ridwan", which reads more human). To add a signature for a new play, add a Settings row named `SIGNATURE_<PLAY>` in capitals. Run **Set up tabs** once to add the new rows; existing cells such as `SIGNATURE` are never overwritten, so edit any old text yourself. Use `\n` or real line breaks for new lines.

## 3c. KoolestFlow connection (the dashboard)
`Api.gs` is a small secured web API on the Sheet. KoolestFlow (`koolestpro/cold-dm-app`, branch `claude/outreach-alert-email-debug-b2d85x`) shows a **Cold email** screen on top of it: leads, each 5-email sequence (editable until sent), the conversation, reply drafts with Approve, and a box to add store domains.
1. Add `Api.gs` as a file in Apps Script. Project Settings > Script properties: add `OUTREACH_API_TOKEN` = a long random string (make one up, 40+ characters).
2. Deploy > New deployment > type **Web app** > Execute as **Me** > Who has access **Anyone** > Deploy. Authorise when asked. Copy the Web app URL (ends in `/exec`). The URL alone does nothing: every call must carry the token.
3. In KoolestFlow's environment (`.env.local` for the local app, and the Vercel project's environment variables for the hosted one) set `OUTREACH_API_URL` = that URL and `OUTREACH_API_TOKEN` = the same token. Restart the backend.
4. Open KoolestFlow > **Cold email** in the sidebar.
After you change `Api.gs`, use Deploy > Manage deployments > edit > New version, or the URL keeps serving the old code.
What it can and cannot do: it can approve leads, edit unsent emails, edit and approve reply drafts, add leads and store domains, and change a few Settings (not `TEST_MODE`). It never sends mail itself: approvals queue for the normal sender, and "Check replies and send approved" runs the same check the 30 minute trigger does.

## 3b. AI reply drafts (Gemini, then Claude Haiku, then DeepSeek)
**Status 2026-10-04: done and tested by Ridwan.** Still open: the `VOICE_EXAMPLES` cell in Settings was empty when checked; paste 3 to 5 of your real replies there.

When a lead replies, the script now writes a draft into **Drafts** (status **Ready for review**) and updates that lead's **Memory** summary. It never sends on its own: you edit `draft_body`, set status **Approved**, and the next check sends it.
1. Paste the new `Code.gs`, save, reload the Sheet, then run Outreach > **1. Set up tabs** once (adds the new Settings rows and a `model` column in Drafts).
2. Get keys (any one is enough; all three gives the fallback chain):
   - Gemini (free): aistudio.google.com/apikey
   - Claude: console.anthropic.com > API keys (add a few dollars of credit; Haiku costs cents)
   - DeepSeek: platform.deepseek.com > API keys
3. Apps Script > Project Settings (gear) > **Script properties** > Add: `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`. Never put keys in the Sheet or in `Code.gs`.
4. Google asks for one more permission (external requests) the first time. Approve it.
5. Test: on your test lead, reply to the test email, then Outreach > **Check replies now**, then Outreach > **Draft replies now**. The Drafts row fills in and the `model` column shows which AI wrote it. If it says `failed: ...`, that text is the reason.
To make drafts sound like you: paste 3 to 5 of your own real replies into the `VOICE_EXAMPLES` cell in Settings (after re-running Set up tabs). Real examples beat any instruction.
Gemini model names change and differ by account, so `GEMINI_MODEL` is `auto`: the script asks Google which model your key can use and remembers it. Outreach > **Test AI** sends one tiny request and shows which provider answered, or why each one failed. Add a second key (Claude or DeepSeek) so one provider's outage never stalls the pipeline.
Order and model names are in Settings (`AI_ORDER`, `GEMINI_MODEL`, `CLAUDE_MODEL`, `DEEPSEEK_MODEL`).

## 4. Go live (only after the first batch is approved)
1. Delete the `test-001` rows from Leads, Sequence, Messages and Drafts.
2. Outreach > **2. Turn on automation** (sends hourly 9am–5pm, checks replies every 30 min).
3. When the first real batch has been reviewed: Settings > **TEST_MODE = FALSE**.

## Rules the script follows
- A lead is only emailed if `approved` is ticked, `email_status` is `valid`, and its stage is New or Contacted.
- Daily cap starts at 5, rises by 5 each week, never above 20. At most 2 emails per hourly run.
- Follow-ups go first, then new first emails. Steps 2–5 go in the same thread as step 1.
- A reply stops the sequence immediately. Bounced addresses are marked and never emailed again.
- **PAUSED = TRUE** stops everything.

## Adding more Gmails (updated 2026-10-10)

Your main sending Gmail (the script inside the Sheet) does everything: research, writing emails, reply drafts, the 6pm report and sending. Each extra Gmail gets its own small copy of the script that ONLY sends emails and reads its own replies. That way nothing is researched or written twice.

For each extra Gmail (never your main personal Gmail):
1. **Share the Sheet** with the new Gmail as an Editor (Share button in the Sheet).
2. **Sign in to the new Gmail** in a separate browser profile, go to script.google.com and click **New project**. Name it "Outreach sender (that Gmail)".
3. **Add the files.** Delete the empty `Code.gs`, then add each file from `outreach/gmail-sender/` with **+ > Script** and paste its contents: `Code.gs`, `Brief.gs`, `Pipeline.gs`, `Research.gs`, `Discovery.gs`, `Apify.gs`, `Api.gs`. Use the same names.
4. **Turn on the Gmail service:** left sidebar **Services (+)**, pick **Gmail API**, Add.
5. **Copy the manifest:** Project Settings (gear) > tick "Show appsscript.json", then replace its contents with `outreach/gmail-sender/appsscript.json`.
6. **Point it at the Sheet:** Project Settings > Script properties > Add `SHEET_ID` = the long ID in your Sheet's URL (between `/d/` and `/edit`). This property is what makes the copy an extra sender. Add `MYEMAILVERIFIER_API_KEY` too, so it can re-check addresses before sending. No AI keys are needed.
7. **Start it:** in the editor pick `installTriggers` from the function list and click **Run**, then allow the permissions. It creates two triggers only (send hourly, check replies every 30 minutes) and starts **its own warm-up** from today: 5 a day in week 1, then +5 a week, max 20.
8. **Check it:** in the Sheet, `Outreach > Why isn't it sending?` run from the new account's copy (or run `whyNotSending` in its editor) to see its cap and queue.

How the accounts share work: an approved lead is taken by whichever Gmail sends its first email, and that Gmail is written into the lead's `sender` column. Every follow-up and every reply for that lead then goes through the same Gmail, in the same thread. Replies to an extra Gmail are logged and alerted like any other; the main account writes the reply draft, and the extra Gmail sends it when you mark it Approved.

Tips: add one Gmail at a time, a few days apart. Give each a real name and profile photo, and send and receive a few normal emails from it first. Ten accounts at 20 a day is 200 emails a day: only go that high once replies and bounces look healthy in the daily report.

## Go-live checklist

1. **Paste the latest files** into the main script (all seven `.gs` files from `outreach/gmail-sender/` on `main`), then run **Outreach > 1. Set up tabs**.
2. **Script properties:** `GEMINI_API_KEY`, `MYEMAILVERIFIER_API_KEY` (required); `PAGESPEED_API_KEY` (speed checks); `HUNTER_API_KEY` (optional).
3. **Reset the test leads:** run **Redo research + emails for unsent leads**, then **Rewrite unsent follow-ups (leads already emailed)**, then **Prepare new leads now** a few times.
4. **One more test round** with `TEST_MODE` = TRUE: read 10 to 15 new emails and check each claim on the live site. Every email should end on its question (no "no worries if..." line) and no follow-up should start "One more thing I noticed". If any does, the old files are still running.
5. **Settings for go-live:** `AUTO_APPROVE` = FALSE (you tick `approved` per lead for the first two weeks), `SEND_TO_CATCH_ALL` = FALSE, `POSTAL_ADDRESS` filled in (required for US leads), `ALERT_EMAIL` = your main Gmail.
6. **Only approve leads whose notes have no `CHECK:` and no `[UNCONFIRMED RECIPIENT]`.**
7. **Go live:** set `TEST_MODE` = FALSE. Set `START_DATE` to today so the warm-up starts at 5 a day.
8. **Watch the 6pm report daily** for the first two weeks: bounces above about 3% or any spam complaint means set `PAUSED` = TRUE and tell me.

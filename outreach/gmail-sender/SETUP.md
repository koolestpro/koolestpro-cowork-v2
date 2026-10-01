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

**Businesses with an email but no website** (for example from Google Maps): add them straight into Leads with `brand`, `email`, `country`, `niche`, `notes` (rating, reviews, city) and leave `website` empty. They are treated as track Build: email 1 offers a free ad creative.

**How a new lead flows:** put a row in Leads with `lead_id`, `brand`, `website`, `country`, `niche`, `track` (and `contact_name`, `email` if you have them). Every 30 minutes, or via Outreach > **Prepare new leads now**, the script finds an email on their site if `email` is empty, verifies it, writes the Profile, then writes the 5-email Sequence. Check `notes` on the lead: it says what the first email's observation is based on, and `CHECK:` if something needs your eyes. Then tick `approved` (or set `AUTO_APPROVE` = TRUE in Settings to auto-approve clean ones). Sending follows each lead's own working hours (9 to 5, weekdays, from `time_zone` or their country).

Email verification: get a free key at myemailverifier.com and add Script property `MYEMAILVERIFIER_API_KEY`. Without it, emails stay `unverified` and are never sent. Verify the response format against their docs the first time; Valid is sent. Invalid never is. Catch-all (the domain accepts every address, so the mailbox is unproven) is sent only if you set `SEND_TO_CATCH_ALL` = TRUE in Settings. Unknown or grey-listed is `risky` and never sent.


The script is `Code.gs` plus `Brief.gs` (the master brief, compiled from `outreach/brief-ai.md`). In Apps Script click **+** > Script, name it `Brief`, and paste `Brief.gs`. After editing `brief-ai.md`, run `node outreach/build_brief.js` and paste the new `Brief.gs` again. Also run Outreach > **2. Turn on automation** again once, to add the 6pm daily report trigger. Try it with Outreach > **Send daily report now**.

**Nothing sending?** Outreach > **Why isn't it sending?** checks the settings, today's cap, and every lead, and names the exact reason for each.

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

## Adding more Gmails later
Each new Gmail gets its own copy of the script pointed at this same Sheet: new Apps Script project (script.google.com) in that account, paste the same two files, then Project Settings > Script properties > add `SHEET_ID` = the Sheet's ID (the long part of its URL). Share the Sheet with that Gmail as an editor, then in the editor pick `installTriggers` and press Run. Leads a Gmail sends to are claimed by it, so two accounts never email the same lead.

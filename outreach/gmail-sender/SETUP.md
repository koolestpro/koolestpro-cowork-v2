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

## 3a. Two files now
The script is `Code.gs` plus `Brief.gs` (the master brief, compiled from `outreach/brief-ai.md`). In Apps Script click **+** > Script, name it `Brief`, and paste `Brief.gs`. After editing `brief-ai.md`, run `node outreach/build_brief.js` and paste the new `Brief.gs` again. Also run Outreach > **2. Turn on automation** again once, to add the 6pm daily report trigger. Try it with Outreach > **Send daily report now**.

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

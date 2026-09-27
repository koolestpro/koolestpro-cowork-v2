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
1. In **Leads**, tick **approved** on the `test-001` row.
2. Outreach > **Send due emails now**. Step 1 lands in your main Gmail with `[TEST to ...]` in the subject.
3. Reply to that test email from your main Gmail. Then Outreach > **Check replies now**. The lead moves to **Replied**, the follow-up is stopped, a row appears in **Drafts**, and you get an alert.
4. In **Drafts**, type something in `draft_body`, set status to **Approved**, then **Check replies now** again. It sends in the same thread.

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

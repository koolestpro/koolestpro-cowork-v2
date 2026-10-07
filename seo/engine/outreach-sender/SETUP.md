# Outreach sender: turn on email automation (about 20 minutes)

Until this is set up, keep `project.json → outreach.mode` as `csv` (or `gmail-drafts`): each weekly run gives you `outreach.md` + `outreach-import.csv` and you send the pitches yourself. Switch on automation only when everything in **Before you start** is true.

## Before you start
- [ ] **A sending mailbox owned by the business** (e.g. `partnerships@brand.com` on Google Workspace), with the owner's written OK to send link-building emails in their name. Don't send for a client from your own Gmail.
- [ ] Ideally it's **not their main inbox**, or it's on a subdomain, so a bad week can't hurt their everyday email.
- [ ] The domain has **SPF, DKIM and DMARC** set up (Google Workspace admin: Apps → Gmail → Authenticate email).
- [ ] The business has agreed the pitch style. Show them one run's `outreach.md` first.
- [ ] UK businesses: under PECR you can email **companies** with an opt-out. Sole traders and partnerships count as individuals and need consent, so skip them or contact them by hand. Every email carries the `OPT_OUT_LINE`. (This is guidance, not legal advice; the business owns its compliance.)

## 1. Make the Sheet and paste the script (signed in as the sending mailbox)
1. sheets.new → name it `<Brand> SEO Outreach`.
2. Extensions → Apps Script. Replace everything with `Code.gs` from this folder.
3. Project Settings (gear) → tick **Show "appsscript.json" manifest file**, and replace it with `appsscript.json` from this folder (turns on the Gmail service).
4. Save, then reload the Sheet. An **Outreach** menu appears.

## 2. Set up
1. Outreach → **1. Set up tabs** (approve the permissions; "Advanced → Go to project" is normal for your own script).
2. **Settings** tab: fill in `SENDER_NAME`, `SIGNATURE`, `ALERT_EMAIL` (the person handling replies) and `TIME_ZONE`. Check `OPT_OUT_LINE`. Leave `TEST_MODE = TRUE`.
3. Share the Sheet (editor) with the Google account used for the SEO engine's sign-in (`seo/engine/SETUP.md §1`, which must include the Sheets API).
4. In the project's `seo/project/project.json`:
   ```json
   "outreach": { "mode": "sheet", "sheet_id": "<the long ID in the Sheet URL>", "track": "seo-links", ... }
   ```

## 3. Test (nothing reaches a real person)
1. Leads → tick **approved** on `test-001` → Outreach → **Send due emails now**. Step 1 arrives at ALERT_EMAIL with `[TEST to …]` in the subject, signed, with the opt-out line.
2. Reply to it, then Outreach → **Check replies now**. The lead moves to **Replied**, step 2 is stopped, a Drafts row appears, and you get an alert.
3. Push a real week into the Sheet: `python3 seo/engine/tools/outreach_push.py --run seo/project/runs/<date>`. The leads appear **unapproved**, with `email_status = unchecked`.

## 4. Go live
1. Delete the `test-001` rows from Leads, Sequence, Messages and Drafts.
2. Outreach → **2. Turn on automation** (sends hourly inside SEND_START/END_HOUR, checks replies every 30 min).
3. Settings → `TEST_MODE = FALSE`.
4. Each week: review the new `seo-links` leads, set `email_status = valid` once you trust the address, tick **approved**. Only approved + valid leads are emailed.

## How it behaves
- 2 steps per prospect: the pitch (no link, it offers the resource) and one follow-up 4 days later, in the same thread.
- A reply of any kind stops the sequence and alerts you. Draft your answer in the **Drafts** tab (set it to Approved to send in-thread) or reply from Gmail directly. Replies get no opt-out line.
- Caps: 3 a day in week 1, +2 a week, never above 10, and at most 2 per hourly run.
- Bounces are marked and never emailed again. **PAUSED = TRUE** stops everything.

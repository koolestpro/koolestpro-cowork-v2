/**
 * SEO engine outreach sender (Google Apps Script). Generic: works for any project.
 *
 * Lives inside the project's outreach Google Sheet (Extensions > Apps Script) and runs as the
 * project's own sending mailbox (e.g. the client's partnerships@ Workspace address).
 * Everything project-specific (sender name, signature, time zone, hours, caps, opt-out line)
 * is set in the Settings tab, not in this code. seo/engine/tools/outreach_push.py fills the
 * Leads / Profiles / Sequence tabs; nothing sends until a person ticks "approved".
 * One copy runs per sending mailbox. It:
 *   - sends approved first emails and due follow-ups, in one run, inside daily caps
 *   - ramps volume slowly (warm-up) and spreads sends across the day
 *   - logs every email in and out to the Messages tab
 *   - stops a lead's sequence the moment they reply, and alerts you
 *   - sends reply drafts you've approved, in the same thread
 *   - marks bounced addresses
 *
 * Nothing is sent to a lead unless its "approved" box is ticked AND TEST_MODE is FALSE.
 * Requires the Gmail advanced service (see appsscript.json / SETUP.md).
 */

// ---------- Sheet layout ----------

const TABS = {
  Settings: ['key', 'value', 'notes'],
  Leads: ['lead_id', 'brand', 'website', 'contact_name', 'email', 'email_status', 'country', 'time_zone',
    'niche', 'source', 'track', 'play', 'stage', 'approved', 'sender', 'touch_count', 'last_touch_at',
    'next_touch_at', 'thread_id', 'first_message_id', 'subject', 'notes', 'created_at'],
  Profiles: ['lead_id', 'what_they_sell', 'audience', 'signal', 'site_notes', 'updated_at'],
  Sequence: ['lead_id', 'step', 'subject', 'body', 'status', 'sent_at'],
  Messages: ['logged_at', 'lead_id', 'direction', 'from', 'to', 'subject', 'body', 'sent_at', 'thread_id',
    'message_id', 'sender_account'],
  Memory: ['lead_id', 'summary', 'updated_at'],
  Drafts: ['lead_id', 'created_at', 'reply_to_message_id', 'draft_body', 'status', 'sent_at'],
};

const STAGES = ['New', 'Contacted', 'Finished', 'Replied', 'Talking', 'Call booked', 'Won', 'Lost', 'Bounced'];
const DRAFT_STATUSES = ['Needs draft', 'Ready for review', 'Approved', 'Sent', 'Discarded'];

function defaultSettings_() {
  return [
    ['TEST_MODE', 'TRUE', 'While TRUE, every email goes to ALERT_EMAIL instead of the lead. Set FALSE to go live.'],
    ['PAUSED', 'FALSE', 'TRUE stops all sending immediately.'],
    ['SENDER_NAME', '', 'Display name on outgoing emails, e.g. "Sam at Brand".'],
    ['SIGNATURE', '', 'Added under every email. Plain text, e.g. "Sam\nPartnerships, Brand\nbrand.com".'],
    ['OPT_OUT_LINE', 'If this is not for you, just reply "no thanks" and I will not follow up.', 'Added at the very end of every email (UK PECR / good practice). Leave it on.'],
    ['TIME_ZONE', 'Europe/London', 'Time zone for send hours and daily counts (IANA name, e.g. Europe/London, America/New_York).'],
    ['ALERT_EMAIL', '', 'Where reply alerts and TEST_MODE emails go (the person managing outreach).'],
    ['START_DATE', Utilities.formatDate(new Date(), tz_(), 'yyyy-MM-dd'), 'Warm-up counts weeks from this date.'],
    ['DAILY_CAP_START', '3', 'Emails per day in week 1.'],
    ['RAMP_PER_WEEK', '2', 'Added to the daily cap each week.'],
    ['DAILY_CAP_MAX', '10', 'Hard ceiling per day for this mailbox. Link outreach needs quality, not volume.'],
    ['MAX_PER_RUN', '2', 'Emails per hourly run, so sends are spread through the day.'],
    ['SEND_START_HOUR', '9', 'Earliest hour to send (TIME_ZONE).'],
    ['SEND_END_HOUR', '17', 'Stop sending at this hour.'],
    ['FOLLOWUP_GAPS', '4,5', 'Days between steps 1>2, 2>3. SEO link pitches use 2 steps.'],
  ];
}

// ---------- Menu, setup, triggers ----------

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Outreach')
    .addItem('1. Set up tabs', 'setup')
    .addItem('2. Turn on automation', 'installTriggers')
    .addSeparator()
    .addItem('Send due emails now', 'sendDueNow')
    .addItem('Check replies now', 'tick')
    .addSeparator()
    .addItem('Turn off automation', 'removeTriggers')
    .addToUi();
}

function setup() {
  const ss = ss_();
  const me = me_();
  Object.keys(TABS).forEach(name => {
    let sh = ss.getSheetByName(name);
    if (!sh) sh = ss.insertSheet(name);
    const headers = TABS[name];
    const existing = sh.getLastColumn() ? sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0] : [];
    if (existing.filter(String).length === 0) {
      sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
      sh.setFrozenRows(1);
    } else {
      // add any missing columns at the end, never reorder existing ones
      headers.filter(h => existing.indexOf(h) === -1).forEach(h => {
        sh.getRange(1, sh.getLastColumn() + 1).setValue(h).setFontWeight('bold');
      });
    }
  });

  const settings = ss.getSheetByName('Settings');
  if (settings.getLastRow() < 2) {
    const rows = defaultSettings_();
    rows.forEach(r => { if (r[0] === 'ALERT_EMAIL') r[1] = me; });
    settings.getRange(2, 1, rows.length, 3).setValues(rows);
    settings.autoResizeColumns(1, 3);
  }

  const leads = ss.getSheetByName('Leads');
  const lh = header_(leads);
  const rows = 2000;
  // Checkbox validation (not insertCheckboxes) so empty rows don't count as data.
  leads.getRange(2, lh.indexOf('approved') + 1, rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireCheckbox().build());
  leads.getRange(2, lh.indexOf('stage') + 1, rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STAGES, true).setAllowInvalid(false).build());
  const drafts = ss.getSheetByName('Drafts');
  const dh = header_(drafts);
  drafts.getRange(2, dh.indexOf('status') + 1, rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(DRAFT_STATUSES, true).setAllowInvalid(false).build());

  // One sample lead so the flow can be tested end to end in TEST_MODE.
  if (leads.getLastRow() < 2) {
    appendObj_('Leads', {
      lead_id: 'test-001', brand: 'Test Blog', website: 'example.com', contact_name: 'Ada',
      email: 'test@example.com', email_status: 'valid', country: 'UK', time_zone: 'Europe/London',
      niche: 'small business blog', source: 'manual', track: 'seo-links', play: 'resource-page', stage: 'New',
      approved: false, touch_count: 0, notes: 'Sample row. Delete when you go live.', created_at: new Date(),
    });
    appendObj_('Sequence', { lead_id: 'test-001', step: 1, subject: 'quick question about your resources page',
      body: 'Hi Ada,\n\nThis is a test of step 1.', status: 'Draft' });
    appendObj_('Sequence', { lead_id: 'test-001', step: 2, subject: '',
      body: 'Hi Ada,\n\nThis is a test of step 2 (follow-up in the same thread).', status: 'Draft' });
  }
  const sheet1 = ss.getSheetByName('Sheet1');
  if (sheet1 && sheet1.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(sheet1);
  toast_('Tabs ready. Check the Settings tab, then choose "Turn on automation".');
}

function installTriggers() {
  removeTriggers();
  ScriptApp.newTrigger('sendDue').timeBased().everyHours(1).create();
  ScriptApp.newTrigger('tick').timeBased().everyMinutes(30).create();
  toast_('Automation on: sends hourly, checks replies every 30 minutes.');
}

function removeTriggers() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
}

// ---------- Sending the sequence ----------

function sendDueNow() { sendDue(true); }

/** Sends follow-ups that are due first, then new first emails, within today's cap. */
function sendDue(ignoreHours) {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try {
    const S = settings_();
    if (isTrue_(S.PAUSED)) return;
    const hour = Number(Utilities.formatDate(new Date(), tz_(), 'H'));
    if (ignoreHours !== true && (hour < Number(S.SEND_START_HOUR) || hour >= Number(S.SEND_END_HOUR))) return;

    const me = me_();
    const leads = read_('Leads');
    const seq = read_('Sequence');
    const msgs = read_('Messages');

    const sentToday = msgs.rows.filter(m => m.direction === 'out' && lc_(m.sender_account) === me && isToday_(m.sent_at)).length;
    let budget = Math.min(dailyCap_(S) - sentToday, Number(S.MAX_PER_RUN) || 2, MailApp.getRemainingDailyQuota() - 5);
    if (budget <= 0) return;

    const now = new Date();
    const due = leads.rows.filter(l =>
      isTrue_(l.approved) &&
      ['New', 'Contacted', ''].indexOf(String(l.stage)) !== -1 &&
      lc_(l.email_status) === 'valid' && l.email &&
      (!l.sender || lc_(l.sender) === me) &&
      (Number(l.touch_count || 0) === 0 || (l.next_touch_at && new Date(l.next_touch_at) <= now)));
    due.sort((a, b) => Number(b.touch_count || 0) - Number(a.touch_count || 0)); // follow-ups first

    const gaps = String(S.FOLLOWUP_GAPS).split(',').map(Number);
    let sent = 0;
    for (const lead of due) {
      if (budget <= 0) break;
      const id = String(lead.lead_id);
      const step = Number(lead.touch_count || 0) + 1;
      const steps = seq.rows.filter(r => String(r.lead_id) === id);
      const row = steps.find(r => Number(r.step) === step && r.status !== 'Sent' && r.status !== 'Stopped');
      if (!row) continue;
      const lastStep = Math.max.apply(null, steps.map(r => Number(r.step)));
      if (step > 1 && !lead.thread_id) continue; // follow-up without a thread: skip, needs a look

      const subject = step === 1 ? String(row.subject) : 'Re: ' + String(lead.subject).replace(/^Re:\s*/i, '');
      const body = compose_(row.body, S);
      const to = isTrue_(S.TEST_MODE) ? S.ALERT_EMAIL : String(lead.email).trim();
      const finalSubject = isTrue_(S.TEST_MODE) ? '[TEST to ' + lead.email + '] ' + subject : subject;

      const res = sendRaw_({
        to: to, subject: finalSubject, body: body, name: S.SENDER_NAME, from: me,
        threadId: step > 1 ? lead.thread_id : null, inReplyTo: step > 1 ? lead.first_message_id : null,
      });

      if (step === 1) {
        set_(leads, lead, 'sender', me);
        set_(leads, lead, 'thread_id', res.threadId);
        set_(leads, lead, 'first_message_id', res.rfcId);
        set_(leads, lead, 'subject', subject);
      }
      set_(leads, lead, 'touch_count', step);
      set_(leads, lead, 'last_touch_at', now);
      if (step >= lastStep) {
        set_(leads, lead, 'next_touch_at', '');
        set_(leads, lead, 'stage', 'Finished');
      } else {
        const gap = gaps[step - 1] || gaps[gaps.length - 1] || 4;
        set_(leads, lead, 'next_touch_at', new Date(now.getTime() + gap * 86400000));
        set_(leads, lead, 'stage', 'Contacted');
      }
      set_(seq, row, 'status', 'Sent');
      set_(seq, row, 'sent_at', now);
      appendObj_('Messages', {
        logged_at: now, lead_id: id, direction: 'out', from: me, to: to, subject: finalSubject, body: body,
        sent_at: now, thread_id: res.threadId, message_id: res.id, sender_account: me,
      });

      budget--; sent++;
      if (budget > 0) Utilities.sleep(20000 + Math.floor(Math.random() * 40000));
    }
    if (ignoreHours === true) toast_(sent + ' email(s) sent.');
  } finally {
    lock.releaseLock();
  }
}

// ---------- Replies, manual replies, bounces, approved drafts ----------

/** Runs every 30 minutes: logs replies, stops sequences, alerts, sends approved drafts, marks bounces. */
function tick() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try {
    checkReplies_();
    sendApprovedDrafts_();
    checkBounces_();
  } finally {
    lock.releaseLock();
  }
}

function checkReplies_() {
  const S = settings_();
  const me = me_();
  const leads = read_('Leads');
  const seq = read_('Sequence');
  const logged = new Set(read_('Messages').rows.map(m => String(m.message_id)));

  for (const lead of leads.rows) {
    if (!lead.thread_id || lc_(lead.sender) !== me) continue;
    let thread;
    try { thread = GmailApp.getThreadById(String(lead.thread_id)); } catch (e) { continue; }
    if (!thread) continue;

    for (const m of thread.getMessages()) {
      const mid = m.getId();
      if (logged.has(mid)) continue;
      logged.add(mid);
      const fromEmail = lc_(extractEmail_(m.getFrom()));
      const outbound = fromEmail === me;
      appendObj_('Messages', {
        logged_at: new Date(), lead_id: lead.lead_id, direction: outbound ? 'out' : 'in', from: m.getFrom(),
        to: m.getTo(), subject: m.getSubject(), body: stripQuoted_(m.getPlainBody()), sent_at: m.getDate(),
        thread_id: lead.thread_id, message_id: mid, sender_account: me,
      });

      if (outbound) {
        // You replied from Gmail directly: keep the record current.
        set_(leads, lead, 'last_touch_at', m.getDate());
        continue;
      }

      // A reply from the lead: stop the sequence, queue a draft, alert.
      if (['New', 'Contacted', 'Finished', ''].indexOf(String(lead.stage)) !== -1) set_(leads, lead, 'stage', 'Replied');
      set_(leads, lead, 'next_touch_at', '');
      seq.rows.filter(r => String(r.lead_id) === String(lead.lead_id) && r.status === 'Draft')
        .forEach(r => set_(seq, r, 'status', 'Stopped'));
      appendObj_('Drafts', { lead_id: lead.lead_id, created_at: new Date(), reply_to_message_id: mid,
        draft_body: '', status: 'Needs draft' });

      if (S.ALERT_EMAIL) {
        const snippet = stripQuoted_(m.getPlainBody()).slice(0, 800);
        GmailApp.sendEmail(S.ALERT_EMAIL, 'Reply from ' + (lead.brand || lead.email) + ' (' + (lead.contact_name || '') + ')',
          snippet + '\n\n---\nLead: ' + lead.lead_id + '\nSheet: ' + ss_().getUrl() + '\nSent from: ' + me,
          { name: 'SEO Outreach' });
      }
    }
  }
}

/** Drafts you set to "Approved" are sent in the lead's thread. */
function sendApprovedDrafts_() {
  const S = settings_();
  if (isTrue_(S.PAUSED)) return;
  const me = me_();
  const drafts = read_('Drafts');
  const leads = read_('Leads');
  for (const d of drafts.rows) {
    if (d.status !== 'Approved' || !String(d.draft_body).trim()) continue;
    const lead = leads.rows.find(l => String(l.lead_id) === String(d.lead_id));
    if (!lead || lc_(lead.sender) !== me || !lead.thread_id) continue;

    const subject = 'Re: ' + String(lead.subject).replace(/^Re:\s*/i, '');
    const body = compose_(d.draft_body, S, true);
    const to = isTrue_(S.TEST_MODE) ? S.ALERT_EMAIL : String(lead.email).trim();
    const finalSubject = isTrue_(S.TEST_MODE) ? '[TEST to ' + lead.email + '] ' + subject : subject;
    const res = sendRaw_({ to: to, subject: finalSubject, body: body, name: S.SENDER_NAME, from: me,
      threadId: lead.thread_id, inReplyTo: lead.first_message_id });
    const now = new Date();
    set_(drafts, d, 'status', 'Sent');
    set_(drafts, d, 'sent_at', now);
    set_(leads, lead, 'last_touch_at', now);
    if (lead.stage === 'Replied') set_(leads, lead, 'stage', 'Talking');
    appendObj_('Messages', { logged_at: now, lead_id: lead.lead_id, direction: 'out', from: me, to: to,
      subject: finalSubject, body: body, sent_at: now, thread_id: res.threadId, message_id: res.id, sender_account: me });
  }
}

/** Marks leads whose address bounced, so they never get another email. */
function checkBounces_() {
  const me = me_();
  const leads = read_('Leads');
  const open = leads.rows.filter(l => lc_(l.sender) === me && ['Contacted', 'Finished'].indexOf(String(l.stage)) !== -1 && l.email);
  if (!open.length) return;
  const threads = GmailApp.search('from:(mailer-daemon OR postmaster) newer_than:3d', 0, 30);
  const text = threads.map(t => t.getMessages().map(m => m.getPlainBody()).join('\n')).join('\n').toLowerCase();
  open.forEach(l => {
    if (text.indexOf(lc_(l.email)) !== -1) {
      set_(leads, l, 'stage', 'Bounced');
      set_(leads, l, 'next_touch_at', '');
      set_(leads, l, 'email_status', 'bounced');
    }
  });
}

// ---------- Gmail send (keeps follow-ups in the same thread) ----------

function sendRaw_(o) {
  const enc = s => '=?UTF-8?B?' + Utilities.base64Encode(String(s), Utilities.Charset.UTF_8) + '?=';
  const headers = [
    'From: ' + enc(o.name || '') + ' <' + o.from + '>',
    'To: ' + o.to,
    'Subject: ' + enc(o.subject),
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
  ];
  if (o.inReplyTo) {
    headers.push('In-Reply-To: ' + o.inReplyTo);
    headers.push('References: ' + o.inReplyTo);
  }
  const bodyB64 = Utilities.base64Encode(o.body, Utilities.Charset.UTF_8).replace(/(.{76})/g, '$1\r\n');
  const raw = headers.join('\r\n') + '\r\n\r\n' + bodyB64;
  const resource = { raw: Utilities.base64EncodeWebSafe(raw) };
  if (o.threadId) resource.threadId = String(o.threadId);
  const res = Gmail.Users.Messages.send(resource, 'me');
  const msg = GmailApp.getMessageById(res.id);
  return { id: res.id, threadId: res.threadId, rfcId: msg.getHeader('Message-ID') };
}

// ---------- Helpers ----------

function ss_() {
  const id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  return id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActiveSpreadsheet();
}
let TZ_CACHE_ = null;
/** Time zone from the Settings tab (TIME_ZONE), else the script's own. */
function tz_() {
  if (TZ_CACHE_) return TZ_CACHE_;
  try {
    const sh = ss_().getSheetByName('Settings');
    if (sh && sh.getLastRow() > 1) {
      const row = sh.getRange(2, 1, sh.getLastRow() - 1, 2).getValues().find(r => String(r[0]).trim() === 'TIME_ZONE');
      if (row && String(row[1]).trim()) return (TZ_CACHE_ = String(row[1]).trim());
    }
  } catch (e) { /* fall through */ }
  return (TZ_CACHE_ = Session.getScriptTimeZone() || 'Europe/London');
}

/** Body + signature + opt-out line. Replies to someone who already answered skip the opt-out. */
function compose_(text, S, isReply) {
  let body = String(text).trim();
  if (S.SIGNATURE) body += '\n\n' + String(S.SIGNATURE).replace(/\\n/g, '\n');
  if (S.OPT_OUT_LINE && !isReply) body += '\n\n' + S.OPT_OUT_LINE;
  return body;
}
function me_() { return lc_(Session.getEffectiveUser().getEmail()); }
function lc_(v) { return String(v || '').trim().toLowerCase(); }
function isTrue_(v) { return v === true || lc_(v) === 'true'; }
function toast_(msg) { try { ss_().toast(msg, 'Outreach', 8); } catch (e) { Logger.log(msg); } }
function header_(sh) { return sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0].map(String); }

function read_(name) {
  const sheet = ss_().getSheetByName(name);
  if (!sheet) throw new Error('Missing tab "' + name + '". Run Outreach > Set up tabs.');
  const values = sheet.getDataRange().getValues();
  const headers = values.shift().map(String);
  const rows = values.map((v, i) => {
    const o = { _r: i + 2 };
    headers.forEach((h, j) => { o[h] = v[j]; });
    return o;
  }).filter(o => headers.some(h => o[h] !== '' && o[h] !== false));
  return { sheet: sheet, headers: headers, rows: rows };
}

function set_(tab, row, field, value) {
  const col = tab.headers.indexOf(field);
  if (col === -1) throw new Error('Column "' + field + '" missing in ' + tab.sheet.getName());
  tab.sheet.getRange(row._r, col + 1).setValue(value);
  row[field] = value;
}

function appendObj_(name, obj) {
  const sheet = ss_().getSheetByName(name);
  const headers = header_(sheet);
  sheet.appendRow(headers.map(h => (obj[h] === undefined || obj[h] === null) ? '' : obj[h]));
}

function settings_() {
  const s = {};
  read_('Settings').rows.forEach(r => { if (r.key) s[String(r.key).trim()] = r.value; });
  return s;
}

function dailyCap_(S) {
  const start = new Date(S.START_DATE);
  const days = isNaN(start) ? 0 : Math.max(0, Math.floor((Date.now() - start.getTime()) / 86400000));
  const cap = Number(S.DAILY_CAP_START || 5) + Math.floor(days / 7) * Number(S.RAMP_PER_WEEK || 5);
  return Math.min(cap, Number(S.DAILY_CAP_MAX || 20));
}

function isToday_(d) {
  if (!d) return false;
  const f = x => Utilities.formatDate(new Date(x), tz_(), 'yyyy-MM-dd');
  return f(d) === f(new Date());
}

function extractEmail_(s) {
  const m = String(s).match(/<([^>]+)>/);
  return m ? m[1] : String(s);
}

/** Drops the quoted history under a reply so the log holds only what they wrote. */
function stripQuoted_(body) {
  const lines = String(body).split(/\r?\n/);
  const out = [];
  for (const line of lines) {
    if (/^On .+wrote:\s*$/.test(line) || /^-{2,}\s*Original Message/i.test(line) || /^>/.test(line)) break;
    out.push(line);
  }
  return out.join('\n').trim();
}

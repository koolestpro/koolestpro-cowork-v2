/**
 * Koolestpro Outreach — Gmail sender (Google Apps Script)
 *
 * Lives inside the outreach Google Sheet (Extensions > Apps Script).
 * One copy runs per sending Gmail. It:
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
  Drafts: ['lead_id', 'created_at', 'reply_to_message_id', 'draft_body', 'status', 'sent_at', 'model'],
};

const STAGES = ['New', 'Contacted', 'Finished', 'Replied', 'Talking', 'Call booked', 'Won', 'Lost', 'Bounced'];
const DRAFT_STATUSES = ['Needs draft', 'Ready for review', 'Approved', 'Sent', 'Discarded'];

function defaultSettings_() {
  return [
    ['TEST_MODE', 'TRUE', 'While TRUE, every email goes to ALERT_EMAIL instead of the lead. Set FALSE to go live.'],
    ['PAUSED', 'FALSE', 'TRUE stops all sending immediately.'],
    ['SENDER_NAME', 'Ridwan | Koolestpro', 'Display name on outgoing emails.'],
    ['SIGNATURE', 'Ridwan\nShopify developer, Koolestpro', 'Added under every email. Plain text.'],
    ['ALERT_EMAIL', '', 'Where reply alerts and TEST_MODE emails go (your main Gmail).'],
    ['START_DATE', Utilities.formatDate(new Date(), tz_(), 'yyyy-MM-dd'), 'Warm-up counts weeks from this date.'],
    ['DAILY_CAP_START', '5', 'Emails per day in week 1.'],
    ['RAMP_PER_WEEK', '5', 'Added to the daily cap each week.'],
    ['DAILY_CAP_MAX', '20', 'Hard ceiling per day for this Gmail.'],
    ['MAX_PER_RUN', '2', 'Emails per hourly run, so sends are spread through the day.'],
    ['SEND_START_HOUR', '9', 'Earliest hour to send (Lagos time).'],
    ['SEND_END_HOUR', '17', 'Stop sending at this hour.'],
    ['FOLLOWUP_GAPS', '3,4,5,6', 'Days between steps 1>2, 2>3, 3>4, 4>5.'],
    ['AI_ORDER', 'gemini,claude,deepseek', 'Which AI writes reply drafts, tried in this order. Keys go in Script Properties (see SETUP.md).'],
    ['GEMINI_MODEL', 'gemini-2.5-flash', 'Gemini model name.'],
    ['CLAUDE_MODEL', 'claude-haiku-4-5-20251001', 'Claude model name.'],
    ['DEEPSEEK_MODEL', 'deepseek-chat', 'DeepSeek model name.'],
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
    .addItem('Draft replies now', 'draftRepliesNow')
    .addItem('Create / reset test lead', 'addTestLead')
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

  const have = settings.getRange(2, 1, Math.max(1, settings.getLastRow() - 1), 1).getValues().map(r => String(r[0]).trim());
  defaultSettings_().filter(r => have.indexOf(r[0]) === -1).forEach(r => {
    if (settings.getLastRow() >= 2 || have.length) settings.appendRow(r);
  });

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
  // (Checked on column A: the checkbox column pre-fills FALSE down 2000 rows, so getLastRow() is useless here.)
  if (!leads.getRange(2, 1, Math.max(1, leads.getMaxRows() - 1), 1).getValues().some(r => String(r[0]) !== '')) {
    seedTestLead_();
  }
  const sheet1 = ss.getSheetByName('Sheet1');
  if (sheet1 && sheet1.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(sheet1);
  toast_('Tabs ready. Check the Settings tab, then choose "Turn on automation".');
}

/** Menu: wipes any test-001 / test_001 rows and recreates a clean, complete test lead. */
function addTestLead() {
  ['Leads', 'Sequence', 'Messages', 'Drafts'].forEach(name => {
    const sh = ss_().getSheetByName(name);
    const ids = sh.getRange(1, 1, sh.getLastRow(), name === 'Messages' ? 2 : 1).getValues();
    const col = name === 'Messages' ? 1 : 0;
    for (let i = ids.length - 1; i >= 1; i--) {
      if (['test-001', 'test_001'].indexOf(String(ids[i][col]).trim()) !== -1) sh.deleteRow(i + 1);
    }
  });
  seedTestLead_();
  toast_('Test lead test-001 created. Tick "approved" on it, then Outreach > Send due emails now.');
}

function seedTestLead_() {
  appendObj_('Leads', {
    lead_id: 'test-001', brand: 'Test Brand', website: 'example.com', contact_name: 'Ada',
    email: 'test@example.com', email_status: 'valid', country: 'Nigeria', time_zone: 'Africa/Lagos',
    niche: 'skincare', source: 'manual', track: 'Fix', play: 'cro_sprint', stage: 'New',
    approved: false, touch_count: 0, notes: 'Sample row. Delete when you go live.', created_at: new Date(),
  });
  appendObj_('Sequence', { lead_id: 'test-001', step: 1, subject: 'quick question about Test Brand',
    body: 'Hi Ada,\n\nThis is a test of step 1.', status: 'Draft' });
  appendObj_('Sequence', { lead_id: 'test-001', step: 2, subject: '',
    body: 'Hi Ada,\n\nThis is a test of step 2 (follow-up in the same thread).', status: 'Draft' });
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
    if (isTrue_(S.PAUSED)) { if (ignoreHours === true) toast_('Nothing sent: PAUSED is TRUE in Settings.'); return; }
    const hour = Number(Utilities.formatDate(new Date(), tz_(), 'H'));
    if (ignoreHours !== true && (hour < Number(S.SEND_START_HOUR) || hour >= Number(S.SEND_END_HOUR))) return;

    const me = me_();
    const leads = read_('Leads');
    const seq = read_('Sequence');
    const msgs = read_('Messages');

    const sentToday = msgs.rows.filter(m => m.direction === 'out' && lc_(m.sender_account) === me && isToday_(m.sent_at)).length;
    let budget = Math.min(dailyCap_(S) - sentToday, Number(S.MAX_PER_RUN) || 2, MailApp.getRemainingDailyQuota() - 5);
    if (budget <= 0) { if (ignoreHours === true) toast_('Nothing sent: daily cap or per-run limit reached.'); return; }

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
      const body = String(row.body).trim() + (S.SIGNATURE ? '\n\n' + S.SIGNATURE : '');
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
    if (ignoreHours === true) {
      if (sent > 0) toast_(sent + ' email(s) sent.');
      else {
        const appr = leads.rows.filter(l => isTrue_(l.approved));
        toast_('0 sent. Approved leads: ' + appr.length +
          '. Of those, email_status = valid: ' + appr.filter(l => lc_(l.email_status) === 'valid' && l.email).length +
          ', with a step 1 row in Sequence: ' + appr.filter(l => seq.rows.some(r => String(r.lead_id) === String(l.lead_id) && Number(r.step) === 1)).length +
          '. Each of those three numbers must be at least 1.');
      }
    }
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
    try { draftReplies_(); } catch (e) { Logger.log('draftReplies_: ' + e); }
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
          { name: 'Koolestpro Outreach' });
      }
    }
  }
}

// ---------- AI reply drafts + relationship memory ----------
// Gemini free first, then Claude Haiku, then DeepSeek. Keys live in Script Properties:
// GEMINI_API_KEY, ANTHROPIC_API_KEY, DEEPSEEK_API_KEY (any subset works). The AI only drafts;
// nothing is sent until you set the draft to "Approved".

const AI_SYSTEM_ = [
  'You draft email replies for Ridwan (Koolestpro), a Shopify developer who fixes and builds e-commerce stores. A prospect replied to his cold email. Write the reply Ridwan would send.',
  '',
  'Rules:',
  '- Plain text, first person, friendly and direct, like a real person typing. Usually 40 to 90 words. Match the lead\'s language and tone.',
  '- Answer what they actually asked. If they ask for a call, offer one simple next step. If they ask about price, say it depends on scope and suggest a short call or a quick look at their store first. Never quote prices, timelines, discounts or guarantees.',
  '- Never invent results, numbers, clients, case studies or claims about their store that are not in the context. Concept builds (KURA, HALOS, MERIDIAN, Lumora) are never clients.',
  '- If they say no, not interested or ask to stop: reply in one or two polite lines, no pitch, and say you will not email again.',
  '- No em dashes. No hashtags, no emojis, no exclamation-heavy hype. Avoid: unlock, digital journey, synergy, holistic, valuable insights, "I hope this email finds you well".',
  '- Do not add a signature or sign-off name; the system adds it. End on the question or next step.',
  '',
  'Output exactly two blocks and nothing else:',
  '<reply>the email body</reply>',
  '<memory>An updated running summary of this lead in under 120 words: who they are, what they sell, what was said both ways, what is offered so far, current stage, and the best next step.</memory>',
].join('\n');

function draftRepliesNow() { draftReplies_(true); }

function draftReplies_(interactive) {
  const S = settings_();
  const drafts = read_('Drafts');
  const todo = drafts.rows.filter(d => d.status === 'Needs draft' && !String(d.draft_body).trim()).slice(0, 5);
  if (!todo.length) { if (interactive) toast_('No replies waiting for a draft.'); return; }

  const leads = read_('Leads');
  const profiles = read_('Profiles');
  const msgs = read_('Messages');
  const memory = read_('Memory');
  let done = 0, failed = '';

  for (const d of todo) {
    const lead = leads.rows.find(l => String(l.lead_id) === String(d.lead_id));
    if (!lead) continue;
    const profile = profiles.rows.find(p => String(p.lead_id) === String(d.lead_id)) || {};
    const mem = memory.rows.find(m => String(m.lead_id) === String(d.lead_id));
    const thread = msgs.rows.filter(m => String(m.lead_id) === String(d.lead_id))
      .sort((a, b) => new Date(a.sent_at) - new Date(b.sent_at)).slice(-10)
      .map(m => (m.direction === 'in' ? 'LEAD' : 'RIDWAN') + ' (' + Utilities.formatDate(new Date(m.sent_at), tz_(), 'yyyy-MM-dd') + '):\n' + String(m.body).slice(0, 1500))
      .join('\n\n');
    const user = [
      'LEAD: ' + [lead.brand, lead.contact_name, lead.website].filter(String).join(' | '),
      'Niche: ' + (lead.niche || '') + ' | Country: ' + (lead.country || '') + ' | Track/play: ' + (lead.track || '') + '/' + (lead.play || ''),
      'Profile: ' + [profile.what_they_sell, profile.audience, profile.signal, profile.site_notes].filter(String).join(' / '),
      'Notes: ' + (lead.notes || ''),
      'Memory so far: ' + (mem ? mem.summary : '(none)'),
      '',
      'CONVERSATION (oldest first):',
      thread,
      '',
      'Write the reply to the lead\'s latest message.',
    ].join('\n');

    let out;
    try { out = callAi_(S, AI_SYSTEM_, user); } catch (e) { failed = String(e.message || e); set_(drafts, d, 'model', 'failed: ' + failed.slice(0, 200)); continue; }
    const reply = clean_((out.text.match(/<reply>([\s\S]*?)<\/reply>/i) || [])[1] || '');
    const summary = clean_((out.text.match(/<memory>([\s\S]*?)<\/memory>/i) || [])[1] || '');
    if (!reply) { failed = 'AI returned no <reply> block'; set_(drafts, d, 'model', 'failed: no reply block'); continue; }

    set_(drafts, d, 'draft_body', reply);
    set_(drafts, d, 'status', 'Ready for review');
    set_(drafts, d, 'model', out.provider);
    if (summary) {
      if (mem) { set_(memory, mem, 'summary', summary); set_(memory, mem, 'updated_at', new Date()); }
      else appendObj_('Memory', { lead_id: d.lead_id, summary: summary, updated_at: new Date() });
    }
    done++;
  }
  if (interactive) toast_(done + ' draft(s) written.' + (failed ? ' Problem: ' + failed : ''));
}

/** Tries each provider in AI_ORDER until one answers. Returns { text, provider }. */
function callAi_(S, system, user) {
  const props = PropertiesService.getScriptProperties();
  const order = String(S.AI_ORDER || 'gemini,claude,deepseek').split(',').map(lc_).filter(String);
  const errors = [];
  for (const p of order) {
    try {
      if (p === 'gemini') {
        const key = props.getProperty('GEMINI_API_KEY'); if (!key) { errors.push('gemini: no key'); continue; }
        const model = S.GEMINI_MODEL || 'gemini-2.5-flash';
        const j = postJson_('https://generativelanguage.googleapis.com/v1beta/models/' + model + ':generateContent?key=' + encodeURIComponent(key), {}, {
          systemInstruction: { parts: [{ text: system }] },
          contents: [{ role: 'user', parts: [{ text: user }] }],
          generationConfig: { temperature: 0.6, maxOutputTokens: 2048 },
        });
        return { text: j.candidates[0].content.parts.map(x => x.text || '').join(''), provider: 'gemini:' + model };
      }
      if (p === 'claude') {
        const key = props.getProperty('ANTHROPIC_API_KEY'); if (!key) { errors.push('claude: no key'); continue; }
        const model = S.CLAUDE_MODEL || 'claude-haiku-4-5-20251001';
        const j = postJson_('https://api.anthropic.com/v1/messages', { 'x-api-key': key, 'anthropic-version': '2023-06-01' }, {
          model: model, max_tokens: 900, temperature: 0.6, system: system, messages: [{ role: 'user', content: user }],
        });
        return { text: j.content.map(x => x.text || '').join(''), provider: 'claude:' + model };
      }
      if (p === 'deepseek') {
        const key = props.getProperty('DEEPSEEK_API_KEY'); if (!key) { errors.push('deepseek: no key'); continue; }
        const model = S.DEEPSEEK_MODEL || 'deepseek-chat';
        const j = postJson_('https://api.deepseek.com/chat/completions', { Authorization: 'Bearer ' + key }, {
          model: model, temperature: 0.6, max_tokens: 900,
          messages: [{ role: 'system', content: system }, { role: 'user', content: user }],
        });
        return { text: j.choices[0].message.content, provider: 'deepseek:' + model };
      }
      errors.push(p + ': unknown provider');
    } catch (e) {
      errors.push(p + ': ' + String(e.message || e).slice(0, 150));
    }
  }
  throw new Error('No AI answered. ' + errors.join(' | '));
}

function postJson_(url, headers, payload) {
  const res = UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', headers: headers,
    payload: JSON.stringify(payload), muteHttpExceptions: true });
  const code = res.getResponseCode();
  if (code < 200 || code >= 300) throw new Error('HTTP ' + code + ' ' + res.getContentText().slice(0, 120));
  return JSON.parse(res.getContentText());
}

/** House rules that must hold even if the model slips: no em dashes, tidy whitespace. */
function clean_(t) {
  return String(t).replace(/\s*[—–]\s*/g, ', ').replace(/&mdash;/g, ', ').replace(/[ \t]+\n/g, '\n').trim();
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
    const body = String(d.draft_body).trim() + (S.SIGNATURE ? '\n\n' + S.SIGNATURE : '');
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
function tz_() { return Session.getScriptTimeZone() || 'Africa/Lagos'; }
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
  const row = nextRow_(sheet);
  if (row > sheet.getMaxRows()) sheet.insertRowsAfter(sheet.getMaxRows(), 1);
  sheet.getRange(row, 1, 1, headers.length)
    .setValues([headers.map(h => (obj[h] === undefined || obj[h] === null) ? '' : obj[h])]);
}

/** First row after the last one with something in column A (appendRow would land below pre-filled checkboxes). */
function nextRow_(sheet) {
  const n = sheet.getLastRow();
  if (n < 2) return 2;
  const col = sheet.getRange(1, 1, n, 1).getValues();
  for (let i = n - 1; i >= 1; i--) if (String(col[i][0]) !== '') return i + 2;
  return 2;
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

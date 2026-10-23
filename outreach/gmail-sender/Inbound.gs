/**
 * Koolestpro Outreach: everything that lands in the inbox that is not a plain human reply in the original thread (2026-10-23, Ridwan).
 *
 * Three problems, one place:
 *   1. BOUNCES ("message not delivered"). The address does not exist or is closed. These used to be treated as a reply from the lead
 *      (NLXL, 2026-10-21: "Address not found" raised a reply alert and an AI draft). Now a hard bounce sends the lead back to the
 *      email rescue (another verified address from the site, once per lead), or marks it Bounced if rescue was already used.
 *   2. AUTO-REPLIES. Out-of-office and support-desk acknowledgements ("Your inquiry is important to us", ticket numbers). They are
 *      logged as `auto`, never mark the lead Replied, never get an AI draft and no alert. The sequence is HELD: the next email moves
 *      to the return date (out of office) or past the stated response window (support desk). Nothing is stopped.
 *   3. REPLIES IN A NEW THREAD. Customer-service desks often answer from another address or start a fresh email. Every 30 minutes the
 *      last 3 days of inbox mail are matched to leads we have emailed: by the original message's reply headers, then by the exact
 *      address, then by our subject from the same domain. A match on the domain alone is never trusted: the lead is held 7 days and
 *      Ridwan gets an alert to confirm. Replies to those messages are sent to the sender, in that thread.
 *
 * Messages.direction values: out, in (human), auto (auto-reply), bounce. Only `in` counts as a reply anywhere else in the system.
 */

const BOUNCE_FROM_ = /(mailer-daemon|postmaster|mail delivery (sub)?system|mailer daemon)/i;
const BOUNCE_SUBJECT_ = /(delivery status notification|undeliverable|undelivered mail|mail delivery (failed|failure)|returned mail|delivery failure|failure notice|message not delivered|couldn'?t be delivered|could not be delivered|address not found)/i;
const BOUNCE_PERMANENT_ = /(\b5\.\d\.\d\b|\b55[0-4]\b|address not found|couldn'?t be found|could not be found|does not exist|doesn'?t exist|no such (user|recipient|mailbox)|user unknown|unknown user|invalid recipient|recipient (address )?rejected|mailbox (unavailable|not found|does not exist|disabled)|domain (not found|does not exist|name not found)|unable to receive mail|account (has been )?(disabled|deleted|suspended)|no longer (active|available|exists|in service)|not a valid (email|recipient)|user not found)/i;
const BOUNCE_SOFT_ = /(\b4\.\d\.\d\b|mailbox (is )?full|over quota|quota exceeded|temporar|try again later|delivery (has been )?delayed|still trying)/i;

const OOO_ = /(out of (the )?office|on (annual |maternity |paternity )?(leave|vacation|holiday)|away from (my|the) (desk|office|email)|limited access to (my )?(email|e-mail)|currently (away|travelling|traveling|out)|will (be )?(back|return|away)|abwesen|absence)/i;
const ACK_PHRASES_ = [
  /this is an? (automated|automatic|auto)/i, /auto-?(reply|response|responder|generated)|automatic (reply|response)/i, /do not reply to this|please do not reply|no-?reply/i,
  /your (inquiry|enquiry|request|message|email|query|ticket) (is|has been|was) (important|received|logged|created|submitted|registered)/i,
  /(we('| ha)ve|we have) received your (message|inquiry|enquiry|email|request|query)/i, /thank you for (reaching out|contacting|getting in touch|your (message|email|inquiry|enquiry))[^.]{0,80}/i,
  /ticket\s*(number|id|no\.?|#)|case\s*(number|id|#)|reference (number|no)/i, /(will|shall|aim to|try to|do our best to) (get back|respond|reply|be in touch|answer)[^.]{0,80}/i,
  /(within|in|up to)\s*(\d+\s*(-|to|–)\s*)?\d+\s*(business |working )?(hours?|days?)/i, /(business|working|office) hours/i, /support (request|team|hours)|customer (service|support|care) team/i,
];

/** Pure classifier. v = { from, subject, body, headers } (headers: lower-case name -> value). Returns { kind, ... }. */
function classify_(v) {
  const from = String(v.from || ''), subject = String(v.subject || ''), body = String(v.body || '').slice(0, 3000), h = v.headers || {};
  const head = body.slice(0, 1500);
  if (BOUNCE_FROM_.test(from) || /report-type=delivery-status/i.test(h['content-type'] || '') || h['x-failed-recipients'] ||
      (BOUNCE_SUBJECT_.test(subject) && /(delivery|recipient|mailbox|address|smtp|550|5\.\d\.\d)/i.test(body))) {
    if (/delay/i.test(subject) && !BOUNCE_PERMANENT_.test(body)) return { kind: 'bounce', permanent: false };
    return { kind: 'bounce', permanent: BOUNCE_PERMANENT_.test(subject + ' ' + body) && !BOUNCE_SOFT_.test(subject + ' ' + body.slice(0, 600)) };
  }
  const autoHeader = (h['auto-submitted'] && !/^no\b/i.test(h['auto-submitted'])) || /auto_?reply|bulk|junk|list/i.test(h['precedence'] || '') || h['x-autoreply'] || h['x-autorespond'] || h['x-auto-response-suppress'];
  const autoSubject = /^\s*(auto(matic)?(ally)?[ -]?(reply|response|generated)|automatische antwort|r[ée]ponse automatique|out of office|ooo)\b|automatic reply/i.test(subject);
  if ((autoHeader || autoSubject || OOO_.test(subject)) && OOO_.test(head + ' ' + subject)) return { kind: 'ooo', returns: parseReturn_(head) };
  if (OOO_.test(subject) || (/^(out of office|automatic reply)/i.test(subject) && OOO_.test(head))) return { kind: 'ooo', returns: parseReturn_(head) };
  const noreply = /^\s*"?[^<"]*"?\s*<?(no-?reply|do-?not-?reply|donotreply|notifications?|mailer|auto(mated)?)[@+]/i.test(from);
  let hits = 0; ACK_PHRASES_.forEach(re => { if (re.test(head)) hits++; });
  if (autoHeader || autoSubject || noreply || (hits >= 3 && body.length < 2500) || (hits >= 2 && body.length < 1200 && !/\?\s/.test(head))) return { kind: 'ack', days: ackDays_(head) };
  return { kind: 'human' };
}

/** Days to hold a lead after a support-desk acknowledgement, from the response window it states (default 4, at most 10). */
function ackDays_(text) {
  const t = String(text);
  let m = t.match(/(\d+)\s*(?:-|to|–)\s*(\d+)\s*(business |working )?days?/i);
  if (m) return Math.min(10, Math.ceil(Number(m[2]) * (m[3] ? 1.5 : 1)) + 1);
  m = t.match(/(?:within|in|up to)\s*(\d+)\s*(business |working )?days?/i);
  if (m) return Math.min(10, Math.ceil(Number(m[1]) * (m[2] ? 1.5 : 1)) + 1);
  if (/(?:within|in|up to)\s*(\d+)\s*hours?|24 hours|48 hours/i.test(t)) return 3;
  return 4;
}

/** A return date from an out-of-office text ("back on 28 October", "until Nov 3"). Returns a Date or null. */
function parseReturn_(text) {
  const MONTHS = { jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5, jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11 };
  const t = String(text).replace(/\s+/g, ' ');
  const lead = '(?:back|return(?:ing|s)?|available|until|till|through|resum\\w+|reply|respond)\\D{0,30}?';
  let m = t.match(new RegExp(lead + '(\\d{1,2})(?:st|nd|rd|th)?\\s+(?:of\\s+)?([A-Za-z]{3,9})', 'i'));
  let day, mon;
  if (m) { day = Number(m[1]); mon = MONTHS[m[2].slice(0, 3).toLowerCase()]; }
  else { m = t.match(new RegExp(lead + '([A-Za-z]{3,9})\\.?\\s+(\\d{1,2})(?:st|nd|rd|th)?', 'i')); if (m) { day = Number(m[2]); mon = MONTHS[m[1].slice(0, 3).toLowerCase()]; } }
  if (mon === undefined || !day || day > 31) return null;
  const now = new Date();
  let d = new Date(now.getFullYear(), mon, day, 9, 0, 0);
  if (d.getTime() < now.getTime() - 86400000) d = new Date(now.getFullYear() + 1, mon, day, 9, 0, 0);
  return d;
}

function domainOf_(email) { return lc_(email).split('@')[1] || ''; }
function baseDomain_(host) { const p = lc_(host).replace(/^www\./, '').split('.'); return p.length > 2 && /^(co|com|org|net|ac|gov)$/.test(p[p.length - 2]) ? p.slice(-3).join('.') : p.slice(-2).join('.'); }

/** Gmail message -> the plain object classify_ reads. Reads only a few headers (cheap). */
function view_(m) {
  let headers = {};
  try {
    const r = Gmail.Users.Messages.get('me', m.getId(), { format: 'metadata', metadataHeaders: ['Auto-Submitted', 'Precedence', 'X-Autoreply', 'X-Autorespond', 'X-Auto-Response-Suppress', 'In-Reply-To', 'References', 'Reply-To', 'X-Failed-Recipients', 'Content-Type'] });
    ((r.payload || {}).headers || []).forEach(x => { headers[lc_(x.name)] = String(x.value || ''); });
  } catch (e) { /* headers are a bonus: the text rules still work */ }
  return { from: m.getFrom(), subject: m.getSubject(), body: m.getPlainBody(), headers: headers };
}

function holdLead_(leads, lead, days, why) {
  if (Number(lead.touch_count || 0) === 0) return;
  const until = new Date(Date.now() + days * 86400000);
  const cur = lead.next_touch_at ? new Date(lead.next_touch_at) : null;
  if (!cur || isNaN(cur) || cur < until) set_(leads, lead, 'next_touch_at', until);
  set_(leads, lead, 'notes', (why + ' ' + Utilities.formatDate(new Date(), tz_(), 'yyyy-MM-dd') + (String(lead.notes || '') ? ' | ' + lead.notes : '')).slice(0, 900));
}

/**
 * Handles ONE inbound or outbound message found for a lead, in the original thread or a new one.
 * ctx = { S, me, leads, seq }; opts = { threadId, match: 'thread|header|sender|subject|domain' }.
 */
function handleInbound_(ctx, lead, m, opts) {
  const S = ctx.S, me = ctx.me, leads = ctx.leads, seq = ctx.seq;
  const mid = m.getId(), threadId = opts.threadId;
  const fromEmail = lc_(extractEmail_(m.getFrom()));
  const outbound = fromEmail === me;
  const plain = m.getPlainBody();
  let kind = 'out', c = null;
  if (!outbound) { c = classify_(view_(m)); kind = c.kind; }
  appendObj_('Messages', {
    logged_at: new Date(), lead_id: lead.lead_id, direction: outbound ? 'out' : (kind === 'human' ? 'in' : (kind === 'bounce' ? 'bounce' : 'auto')), from: m.getFrom(),
    to: m.getTo(), subject: m.getSubject(), body: kind === 'bounce' ? String(plain).slice(0, 1500) : stripQuoted_(plain), sent_at: m.getDate(),
    thread_id: threadId, message_id: mid, sender_account: me,
  });

  if (outbound) { set_(leads, lead, 'last_touch_at', m.getDate()); return; }   // you replied from Gmail directly

  if (kind === 'bounce') return handleBounce_(ctx, lead, c, plain);

  if (kind === 'ooo') {
    const days = c.returns ? Math.min(30, Math.max(2, Math.ceil((c.returns.getTime() - Date.now()) / 86400000) + 1)) : 7;
    holdLead_(leads, lead, days, 'Out-of-office auto-reply' + (c.returns ? ' (back ' + Utilities.formatDate(c.returns, tz_(), 'd MMM') + ')' : '') + ', next email held ' + days + ' days.');
    return;
  }
  if (kind === 'ack') {
    holdLead_(leads, lead, c.days, 'Support-desk auto-reply (not a human answer), next email held ' + c.days + ' days.');
    return;
  }

  // A human wrote. A match on the domain alone is not trusted: hold the lead and ask Ridwan to look.
  if (opts.match === 'domain') {
    holdLead_(leads, lead, 7, 'POSSIBLE REPLY from ' + fromEmail + ' (matched by domain only), held 7 days, check Gmail.');
    if (S.ALERT_EMAIL) GmailApp.sendEmail(S.ALERT_EMAIL, 'Possible reply from ' + (lead.brand || lead.email) + ' (check)',
      'This arrived as a NEW email from ' + m.getFrom() + ' (' + m.getSubject() + ') and only matches ' + (lead.brand || lead.email) + ' by domain, so nothing was changed except holding their sequence for 7 days.\n\n' +
      stripQuoted_(plain).slice(0, 800) + '\n\n---\nLead: ' + lead.lead_id + '\nSheet: ' + ss_().getUrl(), { name: 'Koolestpro Outreach' });
    return;
  }
  // "STOP" and friends: end the sequence, never email again, no AI draft, no alert.
  if (isOptOut_(stripQuoted_(plain))) {
    set_(leads, lead, 'stage', 'Unsubscribed');
    set_(leads, lead, 'next_touch_at', '');
    set_(leads, lead, 'approved', false);
    seq.rows.filter(r => String(r.lead_id) === String(lead.lead_id) && r.status !== 'Sent').forEach(r => set_(seq, r, 'status', 'Stopped'));
    set_(leads, lead, 'notes', (String(lead.notes || '') + ' | Unsubscribed ' + Utilities.formatDate(new Date(), tz_(), 'yyyy-MM-dd')).replace(/^ \| /, ''));
    return;
  }
  // A reply from the lead: stop the sequence, queue a draft, alert.
  if (['New', 'Contacted', 'Finished', ''].indexOf(String(lead.stage)) !== -1) set_(leads, lead, 'stage', 'Replied');
  set_(leads, lead, 'next_touch_at', '');
  seq.rows.filter(r => String(r.lead_id) === String(lead.lead_id) && r.status === 'Draft').forEach(r => set_(seq, r, 'status', 'Stopped'));
  appendObj_('Drafts', { lead_id: lead.lead_id, created_at: new Date(), reply_to_message_id: mid, draft_body: '', status: 'Needs draft' });
  if (S.ALERT_EMAIL) {
    const newThread = String(threadId) !== String(lead.thread_id);
    GmailApp.sendEmail(S.ALERT_EMAIL, 'Reply from ' + (lead.brand || lead.email) + ' (' + (lead.contact_name || '') + ')' + (newThread ? ' [new thread, from ' + fromEmail + ']' : ''),
      stripQuoted_(plain).slice(0, 800) + '\n\n---\nLead: ' + lead.lead_id + '\nSheet: ' + ss_().getUrl() + '\nSent from: ' + me,
      { name: 'Koolestpro Outreach' });
  }
}

/** A "message not delivered" notice for a lead. Hard bounce: look for another address once, else mark Bounced. Soft: just wait. */
function handleBounce_(ctx, lead, c, text) {
  const leads = ctx.leads, seq = ctx.seq, today = Utilities.formatDate(new Date(), tz_(), 'yyyy-MM-dd');
  if (!c.permanent) { holdLead_(leads, lead, 2, 'Soft bounce (temporary delivery problem), retry window.'); return; }
  const dead = String(lead.email).trim();
  const reason = String(text).replace(/\s+/g, ' ').match(BOUNCE_PERMANENT_);
  if (leads.headers.indexOf('email_rescue') !== -1 && !String(lead.email_rescue || '').trim() && String(lead.website || '').trim()) {
    // Back to the start with email_status invalid: the next Prepare run's email rescue swaps in a verified address from their site.
    set_(leads, lead, 'email_status', 'invalid');
    set_(leads, lead, 'stage', 'New');
    set_(leads, lead, 'approved', false);
    ['touch_count'].forEach(k => set_(leads, lead, k, 0));
    ['thread_id', 'first_message_id', 'subject', 'sender', 'last_touch_at', 'next_touch_at'].forEach(k => set_(leads, lead, k, ''));
    seq.rows.filter(r => String(r.lead_id) === String(lead.lead_id) && r.status === 'Sent').forEach(r => { set_(seq, r, 'status', 'Draft'); set_(seq, r, 'sent_at', ''); });
    set_(leads, lead, 'prep_tries', 0);
    set_(leads, lead, 'notes', ('BOUNCED ' + today + ': ' + dead + ' does not accept mail (' + (reason ? reason[0] : 'not delivered') + '). Looking for another address on their site; tick approved again once a new valid one appears.' + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
    return;
  }
  set_(leads, lead, 'stage', 'Bounced');
  set_(leads, lead, 'email_status', 'bounced');
  set_(leads, lead, 'next_touch_at', '');
  set_(leads, lead, 'approved', false);
  seq.rows.filter(r => String(r.lead_id) === String(lead.lead_id) && r.status !== 'Sent').forEach(r => set_(seq, r, 'status', 'Stopped'));
  set_(leads, lead, 'notes', ('BOUNCED ' + today + ': ' + dead + ' does not accept mail and no other address could be found.' + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
}

/** Every 30 minutes: inbox mail from the last 3 days that is NOT in a lead's original thread, matched to leads we have emailed. */
function checkNewThreads_() {
  const S = settings_(), me = me_();
  const leads = read_('Leads'), seq = read_('Sequence');
  const mine = leads.rows.filter(l => l.lead_id && lc_(l.sender) === me && Number(l.touch_count || 0) > 0 && l.email);
  if (!mine.length) return;
  const logged = new Set(read_('Messages').rows.map(m => String(m.message_id)));
  const known = new Set(leads.rows.map(l => String(l.thread_id || '')).filter(String));
  const ctx = { S: S, me: me, leads: leads, seq: seq };

  const byEmail = {}, byDomain = {}, byRfc = {};
  mine.forEach(l => {
    byEmail[lc_(l.email)] = (byEmail[lc_(l.email)] || []).concat(l);
    [domainOf_(l.email), cleanDomain_(String(l.website || '').replace(/^https?:\/\//i, '').replace(/\/.*$/, ''))].filter(String).forEach(d => {
      const b = baseDomain_(d);
      if (!/^(gmail|googlemail|yahoo|ymail|outlook|hotmail|live|icloud|aol|proton|protonmail|gmx|mail|yandex|zoho)\./.test(b)) { byDomain[b] = byDomain[b] || []; if (byDomain[b].indexOf(l) === -1) byDomain[b].push(l); }
    });
    if (l.first_message_id) byRfc[lc_(l.first_message_id).replace(/[<>\s]/g, '')] = l;
  });

  const threads = GmailApp.search('newer_than:3d -in:sent -in:drafts', 0, 60);
  const cutoff = Date.now() - 3 * 86400000;
  let rawBudget = 25;
  for (const t of threads) {
    if (known.has(String(t.getId()))) continue;   // the original thread: checkReplies_ handles it
    for (const m of t.getMessages()) {
      const mid = m.getId();
      if (logged.has(mid) || m.getDate().getTime() < cutoff) continue;
      const from = m.getFrom(), fromEmail = lc_(extractEmail_(from));
      if (fromEmail === me) continue;
      const subject = String(m.getSubject() || '');
      let lead = null, match = '';

      if (BOUNCE_FROM_.test(from) || BOUNCE_SUBJECT_.test(subject)) {   // a notice names the address that failed
        const text = lc_(m.getPlainBody());
        lead = mine.find(l => text.indexOf(lc_(l.email)) !== -1);
        match = 'bounce';
      }
      if (!lead && byEmail[fromEmail]) { lead = byEmail[fromEmail][0]; match = 'sender'; }
      if (!lead && /^\s*(re|fwd?|aw|sv)\s*:/i.test(subject) && rawBudget > 0) {   // a reply that quotes our message carries its id in the headers
        rawBudget--;
        const v = view_(m), refs = lc_((v.headers['in-reply-to'] || '') + ' ' + (v.headers['references'] || '')).replace(/[<>]/g, ' ');
        const key = Object.keys(byRfc).find(k => refs.indexOf(k) !== -1);
        if (key) { lead = byRfc[key]; match = 'header'; }
      }
      const dom = byDomain[baseDomain_(domainOf_(fromEmail))];
      if (!lead && dom) {
        const norm = s => lc_(s).replace(/^(\s*(re|fwd?|aw|sv)\s*:\s*)+/g, '').replace(/\[[^\]]*\]/g, '').trim();
        const hit = dom.find(l => norm(l.subject).length >= 12 && norm(subject).indexOf(norm(l.subject)) !== -1);
        if (hit) { lead = hit; match = 'subject'; }
        else if (dom.length === 1) { lead = dom[0]; match = 'domain'; }
      }
      if (!lead) continue;   // not about anyone we emailed
      logged.add(mid);
      try { handleInbound_(ctx, lead, m, { threadId: t.getId(), match: match }); } catch (e) { Logger.log('checkNewThreads_ ' + lead.lead_id + ': ' + e); }
    }
  }
}

/** Menu: shows how the last 3 days of inbox mail would be classified, without changing anything. */
function inboundPreview() {
  const me = me_(), out = [];
  GmailApp.search('newer_than:3d -in:sent -in:drafts', 0, 25).forEach(t => t.getMessages().forEach(m => {
    if (lc_(extractEmail_(m.getFrom())) === me) return;
    const c = classify_(view_(m));
    out.push(c.kind.toUpperCase() + (c.permanent === true ? ' (hard)' : '') + ' | ' + m.getFrom().slice(0, 40) + ' | ' + String(m.getSubject()).slice(0, 50));
  }));
  const text = out.join('\n') || 'No inbox mail in the last 3 days.';
  try { SpreadsheetApp.getUi().alert('Inbox classification (preview)', text.slice(0, 3000), SpreadsheetApp.getUi().ButtonSet.OK); } catch (e) { toast_(text.slice(0, 300)); }
}

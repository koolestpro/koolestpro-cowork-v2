/**
 * Koolestpro Outreach: lead preparation (README steps 3 and 4).
 *
 * For each new lead in the Leads tab this does, in order, and only what is still missing:
 *   1. finds a contact email on the lead's website (if `email` is empty)
 *   2. verifies it (MyEmailVerifier free API; sending requires email_status = valid)
 *   3. reads the site and writes a Profile (what they sell, audience, signal, real observations)
 *   4. writes the 5-email sequence in Ridwan's voice for the lead's market, into the Sequence tab
 * Then the lead waits for your `approved` tick (or is auto-approved if AUTO_APPROVE = TRUE and no check flagged it).
 *
 * Uses helpers from Code.gs and Brief.gs. Keys (Script Properties): MYEMAILVERIFIER_API_KEY plus the AI keys.
 */

const PREP_BATCH_ = { email: 5, profile: 3, sequence: 3 }; // per run, keeps each run under Apps Script's 6 minute limit
const PREP_MAX_TRIES_ = 3;

function prepareLeadsNow() { prepareLeads_(true); }

/** Trigger entry (every 30 min). */
function prepareLeads() { prepareLeads_(false); }

function prepareLeads_(interactive) {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  const stats = { emails: 0, verified: 0, profiles: 0, sequences: 0, problems: [] };
  try {
    const S = settings_();
    if (isTrue_(S.PAUSED)) { if (interactive) toast_('PAUSED is TRUE in Settings.'); return; }
    const started = Date.now();
    const timeLeft = () => Date.now() - started < 4.5 * 60 * 1000;

    findEmails_(S, stats, timeLeft);
    verifyEmails_(S, stats, timeLeft);
    profileLeads_(S, stats, timeLeft);
    writeSequences_(S, stats, timeLeft);
  } finally {
    lock.releaseLock();
  }
  if (interactive) {
    toast_('Emails found: ' + stats.emails + ', verified: ' + stats.verified + ', profiles: ' + stats.profiles +
      ', sequences written: ' + stats.sequences + (stats.problems.length ? '. Problems: ' + stats.problems.slice(0, 3).join(' | ') : ''));
  }
}

function candidates_(leads, filter, n) {
  return leads.rows.filter(l => l.lead_id && ['New', ''].indexOf(String(l.stage)) !== -1 &&
    Number(l.prep_tries || 0) < PREP_MAX_TRIES_ && filter(l)).slice(0, n);
}

function note_(leads, lead, msg, failed) {
  set_(leads, lead, 'prep_note', msg);
  if (failed) set_(leads, lead, 'prep_tries', Number(lead.prep_tries || 0) + 1);
}

// ---------- 1. Find a contact email ----------

function findEmails_(S, stats, timeLeft) {
  const leads = read_('Leads');
  candidates_(leads, l => !String(l.email).trim() && String(l.website).trim(), PREP_BATCH_.email).forEach(lead => {
    if (!timeLeft()) return;
    try {
      const found = findEmailOnSite_(lead.website);
      if (found) {
        set_(leads, lead, 'email', found);
        set_(leads, lead, 'email_status', 'unverified');
        note_(leads, lead, 'email found on site', false);
        stats.emails++;
      } else {
        note_(leads, lead, 'no email found on site: add one by hand, or use another source', true);
      }
    } catch (e) { note_(leads, lead, 'email search failed: ' + String(e.message || e).slice(0, 100), true); stats.problems.push(lead.lead_id + ': ' + e.message); }
  });
}

function fetchPage_(url, timeoutMs) {
  let u = String(url).trim();
  if (!/^https?:\/\//i.test(u)) u = 'https://' + u;
  const t0 = Date.now();
  const res = UrlFetchApp.fetch(u, { muteHttpExceptions: true, followRedirects: true,
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } });
  const html = res.getContentText().slice(0, 400000);
  return { ok: res.getResponseCode() >= 200 && res.getResponseCode() < 300, code: res.getResponseCode(), html: html, seconds: (Date.now() - t0) / 1000, url: u };
}

function findEmailOnSite_(website) {
  const base = String(website).trim().replace(/^https?:\/\//i, '').replace(/\/.*$/, '');
  const host = base.replace(/^www\./i, '').toLowerCase();
  const paths = ['', '/pages/contact', '/contact', '/pages/contact-us', '/contact-us', '/pages/about', '/about'];
  const found = {};
  for (const p of paths) {
    let page;
    try { page = fetchPage_(base + p); } catch (e) { continue; }
    if (!page.ok) continue;
    const text = page.html.replace(/&#64;|&commat;/gi, '@').replace(/\s*\[at\]\s*/gi, '@');
    const matches = text.match(/[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}/g) || [];
    matches.forEach(m => { found[m.toLowerCase()] = true; });
    if (Object.keys(found).length >= 3) break;
  }
  const bad = /\.(png|jpe?g|gif|svg|webp|css|js)$|sentry|wixpress|example\.|domain\.com|shopify\.com|cloudflare|noreply|no-reply|donotreply|@2x|schema\.org|yourdomain|email\.com$/i;
  const list = Object.keys(found).filter(e => !bad.test(e));
  if (!list.length) return '';
  const score = e => {
    const local = e.split('@')[0], dom = e.split('@')[1];
    let s = 0;
    if (dom === host || dom.endsWith('.' + host) || host.endsWith(dom)) s += 10;      // their own domain
    if (/^(hello|hi|hey|owner|founder|sales|info|contact|team|shop|store)$/.test(local)) s += 4;
    else if (/^(support|help|care|service|orders?|customer)/.test(local)) s += 1;
    else s += 3;                                                                         // looks like a person
    return s;
  };
  list.sort((a, b) => score(b) - score(a));
  const free = /@(gmail|yahoo|outlook|hotmail|icloud|proton|protonmail|live)\./i;
  const top = list[0];
  return (score(top) >= 10 || free.test(top)) ? top : '';   // their own domain, or a free-mail address they published themselves
}

// ---------- 2. Verify ----------

function verifyEmails_(S, stats, timeLeft) {
  const key = PropertiesService.getScriptProperties().getProperty('MYEMAILVERIFIER_API_KEY');
  const leads = read_('Leads');
  candidates_(leads, l => String(l.email).trim() && ['', 'unverified'].indexOf(lc_(l.email_status)) !== -1, 20).forEach(lead => {
    if (!timeLeft()) return;
    const email = String(lead.email).trim();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { set_(leads, lead, 'email_status', 'invalid'); return; }
    if (!key) { set_(leads, lead, 'email_status', 'unverified'); note_(leads, lead, 'Script property MYEMAILVERIFIER_API_KEY not found (Apps Script > Project Settings > Script properties: name = MYEMAILVERIFIER_API_KEY, value = your key). Cannot verify.', false); return; }
    try {
      const res = UrlFetchApp.fetch('https://client.myemailverifier.com/verifier/validate_single/' + encodeURIComponent(email) + '/' + encodeURIComponent(key),
        { muteHttpExceptions: true });
      if (res.getResponseCode() !== 200) throw new Error('HTTP ' + res.getResponseCode());
      const j = JSON.parse(res.getContentText());
      const st = lc_(j.Status || j.status || '');
      // valid and invalid are certain. Catch-all domains accept every address, so the mailbox can't be proven. Anything else (unknown, grey-listed, timeout) is risky.
      const verdict = st === 'valid' ? 'valid' : (st === 'invalid' ? 'invalid' : (/catch/.test(st) ? 'catch-all' : 'risky'));
      set_(leads, lead, 'email_status', verdict);
      note_(leads, lead, 'verifier said: ' + (j.Status || j.status || '?'), false);
      stats.verified++;
    } catch (e) { note_(leads, lead, 'verify failed: ' + String(e.message || e).slice(0, 100), true); stats.problems.push(lead.lead_id + ': ' + e.message); }
  });
}

/** Menu: tests the verifier key on your own alert email and shows the raw answer, so we can see the real response format. */
function testVerifier() {
  const key = PropertiesService.getScriptProperties().getProperty('MYEMAILVERIFIER_API_KEY');
  if (!key) { toast_('No Script property named MYEMAILVERIFIER_API_KEY. Add it in Project Settings > Script properties (value = your key).'); return; }
  const email = String(settings_().ALERT_EMAIL || '').trim();
  const res = UrlFetchApp.fetch('https://client.myemailverifier.com/verifier/validate_single/' + encodeURIComponent(email) + '/' + encodeURIComponent(key), { muteHttpExceptions: true });
  const body = res.getContentText().slice(0, 300);
  Logger.log(body);
  toast_('HTTP ' + res.getResponseCode() + ': ' + body);
}

// ---------- 3. Profile the store ----------

function siteFacts_(page) {
  const html = page.html;
  const pick = re => { const m = html.match(re); return m ? m[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : ''; };
  const title = pick(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const desc = pick(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i);
  const h = [];
  html.replace(/<h[12][^>]*>([\s\S]*?)<\/h[12]>/gi, (m, t) => { const x = t.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim(); if (x) h.push(x); return m; });
  const text = html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
  const sig = [];
  sig.push(/cdn\.shopify\.com|Shopify\.theme/i.test(html) ? 'platform: Shopify' : 'platform: not obviously Shopify');
  if (!/<meta[^>]+name=["']viewport["']/i.test(html)) sig.push('no mobile viewport tag in the page source');
  if (/wa\.me\/|api\.whatsapp\.com|whatsapp:\/\//i.test(html)) sig.push('has a WhatsApp link (orders may go through WhatsApp)');
  const revApp = (html.match(/judge\.me|yotpo|loox|stamped\.io|okendo|trustpilot|reviews\.io/i) || [])[0];
  sig.push(revApp ? 'reviews widget present: ' + revApp : 'no reviews widget spotted in the page source (it may load later)');
  if (!/[$£€₦]\s?\d|\d\s?(NGN|USD|GBP)|N\s?\d{2,3},\d{3}/i.test(text)) sig.push('no prices spotted in the homepage text');
  sig.push('page load about ' + page.seconds.toFixed(1) + 's from the server, ' + Math.round(html.length / 1024) + 'KB of HTML');
  return { title: title, desc: desc, headings: h.slice(0, 8), text: text.slice(0, 3500), signals: sig };
}

function profileLeads_(S, stats, timeLeft) {
  const leads = read_('Leads');
  const profiles = read_('Profiles');
  const have = {};
  profiles.rows.forEach(p => { have[String(p.lead_id)] = true; });
  candidates_(leads, l => String(l.website).trim() && !have[String(l.lead_id)], PREP_BATCH_.profile).forEach(lead => {
    if (!timeLeft()) return;
    try {
      const page = fetchPage_(lead.website);
      if (!page.ok) throw new Error('site returned HTTP ' + page.code);
      const f = siteFacts_(page);
      const sys = 'You analyse an online store from its public homepage data so a sales email can refer to real, checkable things. Use ONLY the data given. Never guess. Output JSON only: ' +
        '{"what_they_sell":"one short line","audience":"who buys, one short line","signal":"one line: why they look like a fit for the given track","site_notes":"2 to 4 short, concrete observations about the page that are supported by the text (not just missing-from-source signals), each one a plain sentence"}. ' +
        'Signals marked "not spotted in the source" are weak: use them only as a soft observation, never as proof something is absent.';
      const user = 'Track: ' + (lead.track || 'unknown') + '. Niche: ' + (lead.niche || '') + '. Brand: ' + (lead.brand || '') + '.\nTitle: ' + f.title + '\nMeta: ' + f.desc +
        '\nHeadings: ' + f.headings.join(' | ') + '\nSignals: ' + f.signals.join('; ') + '\nHomepage text: ' + f.text;
      const out = callAi_(S, sys, user, 700);
      const j = parseJson_(out.text);
      if (!j || !j.what_they_sell) throw new Error('profile: AI returned no JSON');
      appendObj_('Profiles', { lead_id: lead.lead_id, what_they_sell: j.what_they_sell, audience: j.audience || '', signal: j.signal || '',
        site_notes: (j.site_notes || '') + (f.signals.length ? ' [Signals: ' + f.signals.join('; ') + ']' : ''), updated_at: new Date() });
      have[String(lead.lead_id)] = true;
      stats.profiles++;
    } catch (e) { note_(leads, lead, 'profile failed: ' + String(e.message || e).slice(0, 120), true); stats.problems.push(lead.lead_id + ': ' + e.message); }
  });
}

// ---------- 4. Write the 5-email sequence ----------

const SEQ_TASK_ = [
  'TASK: write a 5-email cold sequence from Ridwan to this lead. Use ONLY facts in the lead data and profile below plus the brief. Any observation in email 1 must be supported by the profile. If the profile has no solid observation, keep email 1 honest and general rather than inventing one.',
  'Step 1: the observation, the problem it usually causes, what Ridwan does, one interest question. Steps 2 to 5 must each add something NEW (a second observation, a small useful point, a lighter ask, a different offer) and never say "just checking in" or "following up". Step 3 may use one real proof line from the brief if it genuinely fits. Step 5 is a warm, clean close that leaves the door open.',
  'Every email under 100 words, plain text, no links, no signature (added by the system), each ends with a light way out in Ridwan\'s voice (vary the wording). Steps 2 to 5 read as replies in the same thread: no subject.',
  'Greeting: use the contact name if given ("Hi Amina,"). If no name, start with "Hi," and the observation. For a Nigerian or African lead, email 1 must begin with exactly {{greeting}} followed by the name, e.g. "{{greeting}} Amina." and steps 2 to 5 begin "Hi Amina,". For everyone else, no greeting phrase.',
  'Subject for step 1: short, lower case, specific, no clickbait, no brand-name-only.',
  'Output JSON only: {"basis":"one line: which profile facts the email-1 observation rests on","emails":[{"step":1,"subject":"...","body":"..."},{"step":2,"body":"..."},{"step":3,"body":"..."},{"step":4,"body":"..."},{"step":5,"body":"..."}]}',
].join('\n');

function writeSequences_(S, stats, timeLeft) {
  const leads = read_('Leads');
  const profiles = read_('Profiles');
  const seq = read_('Sequence');
  const has1 = {};
  seq.rows.forEach(r => { if (Number(r.step) === 1) has1[String(r.lead_id)] = true; });
  const ex = String(S.VOICE_EXAMPLES || '').trim();

  candidates_(leads, l => !has1[String(l.lead_id)] && profiles.rows.some(p => String(p.lead_id) === String(l.lead_id)), PREP_BATCH_.sequence).forEach(lead => {
    if (!timeLeft()) return;
    try {
      const p = profiles.rows.find(x => String(x.lead_id) === String(lead.lead_id));
      const sys = BRIEF_.core + '\n\nREGIONAL VOICE FOR THIS LEAD:\n' + BRIEF_.regions[regionKey_(lead.country)] + '\n\n' + SEQ_TASK_ +
        (ex ? '\n\nReal writing by Ridwan. Match its voice, length and rhythm:\n' + ex : '');
      const user = 'LEAD: ' + [lead.brand, lead.contact_name || '(no contact name)', lead.website].filter(String).join(' | ') +
        '\nCountry: ' + (lead.country || '') + '. Niche: ' + (lead.niche || '') + '. Track: ' + (lead.track || '') + '. Play: ' + (lead.play || '') + '. Source: ' + (lead.source || '') +
        '\nWhat they sell: ' + p.what_they_sell + '\nAudience: ' + p.audience + '\nSignal: ' + p.signal + '\nObservations: ' + p.site_notes + '\nNotes: ' + (lead.notes || '');
      const out = callAi_(S, sys, user, 1800);
      const j = parseJson_(out.text);
      if (!j || !j.emails || j.emails.length < 5) throw new Error('sequence: AI returned fewer than 5 emails');

      let flags = [];
      j.emails.slice().sort((a, b) => a.step - b.step).forEach(e => {
        const body = clean_(e.body || '');
        const subject = Number(e.step) === 1 ? clean_(e.subject || '').toLowerCase().slice(0, 90) : '';
        const f = draftFlags_(body.replace(/\{\{greeting\}\}/g, ''));
        if (f) flags.push('step ' + e.step + ': ' + f);
        appendObj_('Sequence', { lead_id: lead.lead_id, step: Number(e.step), subject: subject, body: body, status: 'Draft' });
      });
      set_(leads, lead, 'notes', ('Observation basis: ' + (j.basis || '?') + ' [' + out.provider + ']' + (flags.length ? ' | CHECK: ' + flags.join('; ') : '') +
        (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
      if (isTrue_(S.AUTO_APPROVE) && !flags.length && sendableStatus_(lead.email_status, S)) set_(leads, lead, 'approved', true);
      has1[String(lead.lead_id)] = true;
      stats.sequences++;
    } catch (e) { note_(leads, lead, 'sequence failed: ' + String(e.message || e).slice(0, 120), true); stats.problems.push(lead.lead_id + ': ' + e.message); }
  });
}

function parseJson_(text) {
  const t = String(text).replace(/```json|```/gi, '');
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a === -1 || b === -1) return null;
  try { return JSON.parse(t.slice(a, b + 1)); } catch (e) { return null; }
}

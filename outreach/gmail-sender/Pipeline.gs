/**
 * Koolestpro Outreach: lead preparation (README steps 3 and 4).
 *
 * For each new lead in the Leads tab this does, in order, and only what is still missing:
 *   1. finds a contact email on the lead's website (if `email` is empty)
 *   2. verifies it (MyEmailVerifier free API; sending requires email_status = valid). If it fails, tries the other addresses
 *      for the domain (on the site, Hunter.io if keyed, common role addresses) and swaps in the first valid one
 *   3. researches the store (Research.gs: catalogue, a product page, funnel, speed only when obviously slow, socials), writes a Profile and picks ONE problem
 *      worth a cold email, scored 1 to 5; leads under MIN_PROBLEM_SCORE are held, not emailed
 *   4. writes the 5-email sequence in Ridwan's voice for the lead's market, into the Sequence tab
 * Then the lead waits for your `approved` tick (or is auto-approved if AUTO_APPROVE = TRUE and no check flagged it).
 *
 * Uses helpers from Code.gs and Brief.gs. Keys (Script Properties): MYEMAILVERIFIER_API_KEY plus the AI keys.
 */

const PREP_BATCH_ = { email: 5, profile: 2, sequence: 3, rescue: 3 }; // per run, keeps each run under Apps Script's 6 minute limit (profiles include PageSpeed runs)
const PREP_MAX_TRIES_ = 3;

function prepareLeadsNow() { prepareLeads_(true); }

/** Trigger entry (every 30 min). */
function prepareLeads() { prepareLeads_(false); }

function prepareLeads_(interactive) {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  const stats = { discovered: 0, emails: 0, verified: 0, profiles: 0, sequences: 0, problems: [], limited: false };
  const started = Date.now();
  const ps = PropertiesService.getScriptProperties();
  try {
    const S = settings_();
    if (isTrue_(S.PAUSED)) { if (interactive) toast_('PAUSED is TRUE in Settings.'); return; }

    // Runtime budget (2026-10-23). A consumer Google account gets about 90 minutes of trigger time a day for ALL triggers.
    // Prep used to run ~5 minutes every 30 minutes on a backlog of 200+ unprepared leads, used the day's quota up, and then the
    // send job and the 6pm report stopped running. Prep now gets a daily allowance, and stops when enough emails are already written.
    const day = Utilities.formatDate(new Date(), tz_(), 'yyyy-MM-dd');
    if (ps.getProperty('PREP_DAY') !== day) { ps.setProperty('PREP_DAY', day); ps.setProperty('PREP_MS', '0'); }
    const allowanceMs = Number(S.PREP_DAILY_MINUTES || 35) * 60000;
    if (!interactive && Number(ps.getProperty('PREP_MS') || 0) >= allowanceMs) return;
    const skipNew = !interactive && prepBacklogFull_(S);   // enough prepared leads already: only keep follow-ups written

    const runMs = Number(S.PREP_RUN_MINUTES || 3) * 60 * 1000;
    const timeLeft = () => Date.now() - started < runMs;
    S._started = started;

    if (!skipNew) {
      try { apifyImports_(stats, timeLeft); } catch (e) { stats.problems.push('apify: ' + e.message); }
      try { importSources_(S, stats, timeLeft, false); } catch (e) { stats.problems.push('sources: ' + e.message); }
      try { qualifyDiscovery_(S, stats, timeLeft); } catch (e) { stats.problems.push('discovery: ' + e.message); }
      findEmails_(S, stats, timeLeft);
      verifyEmails_(S, stats, timeLeft);
      rescueEmails_(S, stats, timeLeft);
      profileLeads_(S, stats, timeLeft);
      writeSequences_(S, stats, timeLeft);
    }
    try { writeFollowups_(S, stats, timeLeft); } catch (e) { stats.problems.push('follow-ups: ' + e.message); }
  } finally {
    ps.setProperty('PREP_MS', String(Number(ps.getProperty('PREP_MS') || 0) + (Date.now() - started)));
    lock.releaseLock();
  }
  if (interactive) {
    toast_('Stores promoted: ' + stats.discovered + ', emails found: ' + stats.emails + ', verified: ' + stats.verified + ', profiles: ' + stats.profiles +
      ', sequences written: ' + stats.sequences + (stats.problems.length ? '. Problems: ' + stats.problems.slice(0, 3).join(' | ') : ''));
  }
}

/** True when enough leads already have their emails written and have not been contacted (PREP_BUFFER, default 40; 0 = never stop). */
function prepBacklogFull_(S) {
  const max = Number(S.PREP_BUFFER === undefined || S.PREP_BUFFER === '' ? 40 : S.PREP_BUFFER);
  if (!max) return false;
  const has1 = {};
  read_('Sequence').rows.forEach(r => { if (Number(r.step) === 1 && r.status === 'Draft') has1[String(r.lead_id)] = true; });
  const ready = read_('Leads').rows.filter(l => l.lead_id && ['New', ''].indexOf(String(l.stage)) !== -1 && Number(l.touch_count || 0) === 0 && has1[String(l.lead_id)]).length;
  return ready >= max;
}

function candidates_(leads, filter, n) {
  return leads.rows.filter(l => l.lead_id && ['New', ''].indexOf(String(l.stage)) !== -1 &&
    Number(l.prep_tries || 0) < PREP_MAX_TRIES_ && filter(l))
    .sort((a, b) => (isHot_(b) ? 1 : 0) - (isHot_(a) ? 1 : 0) || hasRedesign_(b) - hasRedesign_(a)).slice(0, n); // hot leads first, then stores with a redesign built (2026-10-26)
}

function note_(leads, lead, msg, failed) {
  // Setup problems (no key) and busy or rate-limited AI are not the lead's fault: say so and do not use up its retries.
  const setup = /no key/i.test(msg);
  const busy = /HTTP 429|HTTP 503|RESOURCE_EXHAUSTED|rate.?limit|overloaded|high demand/i.test(msg);
  set_(leads, lead, 'prep_note', setup ? 'SETUP NEEDED: add an AI key in Apps Script > Project Settings > Script properties (GEMINI_API_KEY, ANTHROPIC_API_KEY or DEEPSEEK_API_KEY). ' + msg
    : (busy ? 'AI busy or rate-limited, will retry on the next run. ' + msg : msg));
  if (failed && !setup && !busy) set_(leads, lead, 'prep_tries', Number(lead.prep_tries || 0) + 1);
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
        const g = guessEmail_(S, lead);
        if (g && g.email) {
          set_(leads, lead, 'email', g.email);
          set_(leads, lead, 'email_status', 'valid');
          if (g.name && !String(lead.contact_name || '').trim()) set_(leads, lead, 'contact_name', g.name);
          note_(leads, lead, 'not published on the site: guessed ' + g.email + ' and the verifier said valid' + (g.name ? ' (owner/founder: ' + g.name + ')' : ''), false);
          stats.emails++;
        } else {
          note_(leads, lead, 'no email on the site and no guessed address verified as valid' + (g && g.why ? ' (' + g.why + ')' : '') + ': add one by hand, or use another source', true);
        }
      }
    } catch (e) { note_(leads, lead, 'email search failed: ' + String(e.message || e).slice(0, 300), true); stats.problems.push(lead.lead_id + ': ' + e.message); }
  });
}

const MX_CACHE_ = {}, PUBLISHED_CACHE_ = {};

/** Free check (2026-10-30, replaces MyEmailVerifier): can this domain receive mail? Google public DNS. Returns true, false, or null when DNS did not answer. */
function domainHasMail_(domain) {
  if (MX_CACHE_[domain] !== undefined) return MX_CACHE_[domain];
  try {
    const res = UrlFetchApp.fetch('https://dns.google/resolve?name=' + encodeURIComponent(domain) + '&type=MX', { muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) return null;
    const j = JSON.parse(res.getContentText());
    if (j.Status === 3) return (MX_CACHE_[domain] = false);   // NXDOMAIN: the domain does not exist
    if (j.Status !== 0) return null;
    const mx = (j.Answer || []).filter(a => a.type === 15 && String(a.data || '').replace(/[\s.]/g, '') !== '0');   // a "null MX" (0 .) means the domain takes no mail
    return (MX_CACHE_[domain] = mx.length > 0);
  } catch (e) { return null; }
}

/**
 * Free verification, no key. Returns 'valid' | 'invalid' | 'risky' | '' (DNS did not answer).
 * invalid: bad format, or the domain cannot receive mail. valid: the domain takes mail AND the address is published on the lead's own site
 * (website, or the address's own domain), so someone put it there to be contacted. Anything else (a guess, a directory address) is risky and
 * never sent, because a mailbox cannot be proven without a paid verifier and bounces hurt the sending Gmail.
 */
function verifyOne_(email, website) {
  const e = lc_(email);
  if (!emailOk_(e)) return 'invalid';
  const dom = e.split('@')[1];
  const mail = domainHasMail_(dom);
  if (mail === null) return '';
  if (!mail) return 'invalid';
  const site = String(website || '').trim() || (FREEMAIL_DOMAINS_.indexOf(dom) === -1 ? dom : '');
  if (!site) return 'risky';
  const key = cleanDomain_(site);
  if (PUBLISHED_CACHE_[key] === undefined) { try { PUBLISHED_CACHE_[key] = siteEmails_(site); } catch (err) { PUBLISHED_CACHE_[key] = []; } }
  return PUBLISHED_CACHE_[key].indexOf(e) !== -1 ? 'valid' : 'risky';
}

/** Asks the AI for the owner/founder name from the About text. Returns '' when it can't tell. */
function ownerName_(S, host) {
  let text = '';
  for (const p of ['/pages/about', '/pages/about-us', '/pages/our-story', '/about']) {
    try {
      const pg = fetchPage_(host + p);
      if (!pg.ok) continue;
      text = pg.html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 3500);
      if (text.length > 200) break;
    } catch (e) {}
  }
  if (text.length < 200) return '';
  try {
    const r = callAi_(S, 'You read a store\'s About text. Reply with JSON only: {"name":"First Last"} for the founder or owner if the text names one, otherwise {"name":""}. Never guess.', text, 80);
    const m = String(r.text).match(/\{[\s\S]*\}/);
    const n = m ? String(JSON.parse(m[0]).name || '').trim() : '';
    return /^[A-Za-z][A-Za-z'\- ]{1,40}$/.test(n) ? n : '';
  } catch (e) { return ''; }
}

/** No email on the site: find the owner's name, try likely addresses, keep the first one the verifier calls valid. */
function guessEmail_(S, lead) {
  return { why: 'a guessed address cannot be proven without a paid verifier, so none is sent (2026-10-30)' };   // free checks only prove addresses the store published
  const host = String(lead.website).trim().replace(/^https?:\/\//i, '').replace(/\/.*$/, '').replace(/^www\./i, '').toLowerCase();
  if (!host) return null;
  const name = ownerName_(S, host);
  const cands = [];
  if (name) {
    const parts = name.toLowerCase().replace(/[^a-z ]/g, '').split(/\s+/).filter(String);
    const f = parts[0], l = parts.length > 1 ? parts[parts.length - 1] : '';
    cands.push(f + '@' + host);
    if (l) cands.push(f + '.' + l + '@' + host, f + l + '@' + host, f[0] + l + '@' + host);
  }
  ['hello', 'info', 'contact', 'support', 'hi', 'team'].forEach(r => cands.push(r + '@' + host));
  let tried = 0;
  for (const c of cands) {
    if (tried >= 6) break;
    const v = verifyOne_(c);
    if (!v) return { why: 'verifier did not answer' };
    tried++;
    if (v === 'valid') return { email: c, name: name };
    if (v === 'catch-all') return { why: 'domain accepts every address, cannot prove a mailbox', name: name };
  }
  return { why: 'tried ' + tried + ' addresses', name: name };
}

function fetchPage_(url, timeoutMs) {
  let u = String(url).trim();
  if (!/^https?:\/\//i.test(u)) u = 'https://' + u;
  const t0 = Date.now();
  const res = UrlFetchApp.fetch(u, { muteHttpExceptions: true, followRedirects: true,
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } });
  const full = res.getContentText();
  // Big stores ship 500KB+ of HTML and the footer (contact email, social links) is at the very end: keep the head AND the tail.
  const html = full.length > 600000 ? full.slice(0, 350000) + '\n<!-- cut -->\n' + full.slice(-250000) : full;
  return { ok: res.getResponseCode() >= 200 && res.getResponseCode() < 300, code: res.getResponseCode(), html: html, seconds: (Date.now() - t0) / 1000, url: u };
}

/** Every usable address published on the site (homepage footer, contact, about, policies), best first. */
function siteEmails_(website) {
  const base = String(website).trim().replace(/^https?:\/\//i, '').replace(/\/.*$/, '');
  const host = base.replace(/^www\./i, '').toLowerCase();
  const paths = ['', '/pages/contact', '/contact', '/pages/contact-us', '/contact-us', '/policies/contact-information', '/pages/about', '/about', '/pages/about-us', '/pages/our-story', '/pages/faq', '/policies/refund-policy', '/policies/privacy-policy', '/policies/terms-of-service'];
  const found = {};
  for (const p of paths) {
    let page;
    try { page = fetchPage_(base + p); } catch (e) { continue; }
    if (!page.ok) continue;
    const text = page.html.replace(/&#64;|&commat;/gi, '@').replace(/\s*\[at\]\s*/gi, '@').replace(/mailto:/gi, ' ');
    const matches = text.match(/[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}/g) || [];
    matches.forEach(m => { found[m.toLowerCase()] = true; });
    if (Object.keys(found).length >= 3) break;
  }
  const bad = /\.(png|jpe?g|gif|svg|webp|css|js)$|sentry|wixpress|example\.|domain\.com|shopify\.com|cloudflare|noreply|no-reply|donotreply|@2x|schema\.org|yourdomain|email\.com$/i;
  const free = /@(gmail|yahoo|outlook|hotmail|icloud|proton|protonmail|live)\./i;
  return Object.keys(found).filter(e => !bad.test(e) && rankEmail_(e, host, '') > -100 && (rankEmail_(e, host, '') >= 10 || free.test(e)))   // their own domain, or a free-mail address they published themselves
    .sort((x, y) => rankEmail_(y, host, '') - rankEmail_(x, host, ''));
}

function findEmailOnSite_(website) { return siteEmails_(website)[0] || ''; }

/**
 * Hunter.io domain search: addresses for this domain that Hunter has seen published anywhere on the web, with names, roles
 * and the company's address pattern. Optional: Script property HUNTER_API_KEY (free plan: 25 searches a month). Returns [].
 */
function hunterEmails_(host) {
  const key = PropertiesService.getScriptProperties().getProperty('HUNTER_API_KEY');
  if (!key || !host) return [];
  try {
    const res = UrlFetchApp.fetch('https://api.hunter.io/v2/domain-search?limit=10&domain=' + encodeURIComponent(host) + '&api_key=' + encodeURIComponent(key), { muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) return [];
    const d = JSON.parse(res.getContentText()).data || {};
    return (d.emails || []).map(e => ({ email: lc_(e.value), name: [e.first_name, e.last_name].filter(String).join(' '), position: e.position || '', confidence: Number(e.confidence || 0) }));
  } catch (e) { return []; }
}

/**
 * The lead's email failed verification (invalid, risky, or catch-all when catch-all is not allowed). Often it came from a
 * directory or a guess and was never theirs, while the site itself shows a working address. Collect every candidate for
 * the domain (on the site, Hunter, common role addresses), verify them best-first, and swap in the first valid one.
 * Runs once per lead (email_rescue column). The failed address is kept in notes.
 */
function rescueEmail_(S, leads, lead) {
  const failed = lc_(lead.email), was = lc_(lead.email_status) || '?';
  const host = cleanDomain_(lead.website);
  if (!host) return '';
  set_(leads, lead, 'email_rescue', new Date());
  const cands = [], seen = {};
  seen[failed] = true;
  const add = (email, source, bonus, name) => {
    email = lc_(email);
    if (!email || seen[email] || rankEmail_(email, host, lead.contact_name) <= -100) return;
    seen[email] = true;
    cands.push({ email: email, source: source, name: name || '', score: rankEmail_(email, host, lead.contact_name) + bonus });
  };
  siteEmails_(lead.website).forEach(e => add(e, 'published on their site', 4));
  hunterEmails_(host).forEach(h => add(h.email, 'Hunter (' + (h.position || 'listed') + ', ' + h.confidence + '% confidence)', h.confidence >= 80 ? 2 : 0, h.name));
  ['hello', 'info', 'contact', 'support', 'team'].forEach(r => add(r + '@' + host, 'common address, guessed', -2));
  cands.sort((a, b) => b.score - a.score);
  if (!cands.length) return 'no other address found for ' + host;
  const tried = [];
  for (const c of cands.slice(0, 5)) {
    const v = verifyOne_(c.email, lead.website);
    if (!v) { tried.push(c.email + ': DNS did not answer'); break; }
    tried.push(c.email + ': ' + v);
    if (v === 'valid' || (v === 'catch-all' && isTrue_(S.SEND_TO_CATCH_ALL) && /their site/.test(c.source))) {
      set_(leads, lead, 'email', c.email);
      set_(leads, lead, 'email_status', v);
      if (c.name && !String(lead.contact_name || '').trim()) set_(leads, lead, 'contact_name', c.name);
      set_(leads, lead, 'notes', ('Email swapped: ' + failed + ' was ' + was + '; now ' + c.email + ' (' + c.source + ', verifier: ' + v + ')' + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
      return 'swapped to ' + c.email + ' (' + c.source + ')';
    }
  }
  return 'no valid replacement for ' + failed + '. Tried: ' + tried.join(', ');
}

function rescueEmails_(S, stats, timeLeft) {
  const leads = read_('Leads');
  if (leads.headers.indexOf('email_rescue') === -1) return;   // run Outreach > Set up tabs once
  candidates_(leads, l => String(l.email).trim() && String(l.website).trim() && !String(l.email_rescue || '').trim() &&
    ['invalid', 'risky'].concat(isTrue_(S.SEND_TO_CATCH_ALL) ? [] : ['catch-all']).indexOf(lc_(l.email_status)) !== -1, PREP_BATCH_.rescue).forEach(lead => {
    if (!timeLeft()) return;
    try {
      const msg = rescueEmail_(S, leads, lead);
      if (/^swapped/.test(msg)) stats.emails++;
      note_(leads, lead, 'email check: ' + msg, false);
    } catch (e) { stats.problems.push(lead.lead_id + ' rescue: ' + e.message); }
  });
}

// ---------- 2. Verify ----------

function verifyEmails_(S, stats, timeLeft) {
  const leads = read_('Leads');
  candidates_(leads, l => String(l.email).trim() && ['', 'unverified'].indexOf(lc_(l.email_status)) !== -1, 20).forEach(lead => {
    if (!timeLeft()) return;
    const email = String(lead.email).trim();
    if (!emailOk_(email)) { set_(leads, lead, 'email_status', 'invalid'); return; }   // the rescue step then looks for a real address
    try {
      const verdict = verifyOne_(email, lead.website);
      if (!verdict) throw new Error('DNS did not answer');
      set_(leads, lead, 'email_status', verdict);
      note_(leads, lead, 'free check: ' + verdict + (verdict === 'risky' ? ' (domain takes mail, but the address is not published on their site)' : ''), false);
      stats.verified++;
    } catch (e) { note_(leads, lead, 'verify failed: ' + String(e.message || e).slice(0, 300), true); stats.problems.push(lead.lead_id + ': ' + e.message); }
  });
}

/** Menu: runs the free check on your own alert email and shows the answer. */
function testVerifier() {
  const email = String(settings_().ALERT_EMAIL || '').trim();
  toast_('Free check for ' + email + ': ' + (verifyOne_(email, '') || 'DNS did not answer') + ' (risky is expected: a free-mail address is only valid when a store publishes it).');
}

// ---------- 3. Profile the store ----------

function siteFacts_(page) {
  const html = page.html;
  const pick = re => { const m = html.match(re); return m ? m[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : ''; };
  const title = pick(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const desc = pick(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i);
  const h = [];
  html.replace(/<h[12][^>]*>([\s\S]*?)<\/h[12]>/gi, (m, t) => { const x = t.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim(); if (x) h.push(x); return m; });
  const text = textOf_(html);   // visible text only (hidden theme labels removed)
  const sig = [];
  sig.push(/cdn\.shopify\.com|Shopify\.theme/i.test(html) ? 'platform: Shopify' : 'platform: not obviously Shopify');
  if (!/<meta[^>]+name=["']viewport["']/i.test(html)) sig.push('no mobile viewport tag in the page source');
  if (/wa\.me\/|api\.whatsapp\.com|whatsapp:\/\//i.test(html)) sig.push('has a WhatsApp link (orders may go through WhatsApp)');
  const revApp = (html.match(/judge\.me|yotpo|loox|stamped\.io|okendo|trustpilot|reviews\.io/i) || [])[0];
  sig.push(revApp ? 'reviews widget present: ' + revApp : 'no reviews widget spotted in the page source (it may load later)');
  if (!/[$£€₦]\s?\d|\d\s?(NGN|USD|GBP)|N\s?\d{2,3},\d{3}/i.test(text)) sig.push('no prices spotted in the homepage text');
  return { title: title, desc: desc, headings: h.slice(0, 8), text: text.slice(0, 3500), signals: sig };
}

function profileLeads_(S, stats, timeLeft) {
  const leads = read_('Leads');
  const profiles = read_('Profiles');
  const seq = read_('Sequence');
  const have = {}, has1 = {};
  profiles.rows.forEach(p => { have[String(p.lead_id)] = p; });
  seq.rows.forEach(r => { if (Number(r.step) === 1 && r.status !== 'Superseded') has1[String(r.lead_id)] = true; });
  const upgraded = profiles.headers.indexOf('problem_worth') !== -1;
  // A store lead whose profile has no problem research yet (made before 2026-10-06, or reset) is researched again, as long as no email is written for it.
  const needsResearch = l => upgraded && lc_(l.track) !== 'partner' && have[String(l.lead_id)] && String(have[String(l.lead_id)].problem_worth) === '' && !has1[String(l.lead_id)];

  // Businesses with an email but no website (for example from Google Maps): profile them from what we already know.
  candidates_(leads, l => !String(l.website).trim() && String(l.email).trim() && !have[String(l.lead_id)], 10).forEach(lead => {
    appendObj_('Profiles', { lead_id: lead.lead_id, what_they_sell: lead.niche || '(see notes)', audience: lead.country || '', signal: 'No website. ' + (lead.notes || ''),
      site_notes: 'No website found for this business. Track Build: they sell without a proper site.', updated_at: new Date() });
    if (!String(lead.track).trim()) set_(leads, lead, 'track', 'Build');
    have[String(lead.lead_id)] = true;
    stats.profiles++;
  });

  candidates_(leads, l => String(l.website).trim() && (!have[String(l.lead_id)] || needsResearch(l)), PREP_BATCH_.profile).forEach(lead => {
    if (!timeLeft() || stats.limited) return;
    try {
      const live = siteStatus_(lead.website);
      if (!live.active) {   // never research or email a dead, parked, for-sale or moved store
        set_(leads, lead, 'stage', 'Lost');
        set_(leads, lead, 'notes', ('SKIP: site not active: ' + live.why + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
        note_(leads, lead, 'SKIP, marked Lost. Site not active: ' + live.why, false);
        stats.profiles++;
        return;
      }
      if (live.prelaunch && lc_(lead.track) !== 'partner') {   // building now: profile from the coming-soon page and socials only
        const base = cleanDomain_(lead.website);
        const ev = launchFacts_(live.html, base);
        const links = socialLinks_(live.html), social = Object.keys(links).map(k => k + ': ' + links[k]);
        if (links.instagram) { const ig = instagram_(S, links.instagram); if (ig) social.push(ig); }
        const out = callAi_(S, LAUNCH_PROFILE_SYS_, 'Brand: ' + (lead.brand || base) + '. Website: ' + lead.website + '. Country: ' + (lead.country || '') + '\nEVIDENCE:\n' + ev.join('\n') + '\nSOCIAL:\n' + (social.join('\n') || 'none found'), 900);
        const j = parseJson_(out.text);
        if (!j || !j.what_they_sell) throw new Error('launch profile: AI returned no JSON');
        const dm = j.decision_maker || {};
        const row = { lead_id: lead.lead_id, what_they_sell: j.what_they_sell + (j.business ? ' | ' + j.business : ''), audience: j.audience || '', signal: j.signal || 'pre-launch',
          site_notes: j.site_notes || '', updated_at: new Date(), offer: j.offer || 'launch_review', decision_maker: dm.name ? dm.name + (dm.role ? ', ' + dm.role : '') : '', team: j.team || 'unknown',
          problem: j.problem || '', problem_evidence: String(j.problem_evidence || '') + (j.cost ? ' | Cost: ' + j.cost : '') + (j.fix ? ' | Fix: ' + j.fix : ''), problem_page: 'https://' + base,
          problem_worth: Math.max(0, Math.min(5, Math.round(Number(j.worth) || 0))), second_problem: j.second && j.second.problem ? '[' + (j.second.offer || '') + '] ' + j.second.problem : '',
          research: ('PRE-LAUNCH (' + live.why + ')\n' + ev.join('\n')).slice(0, 4500), socials: social.join('\n').slice(0, 2000) };
        const old = have[String(lead.lead_id)];
        if (old && old !== true) Object.keys(row).forEach(k => { if (profiles.headers.indexOf(k) !== -1 && k !== 'lead_id') set_(profiles, old, k, row[k]); });
        else appendObj_('Profiles', row);
        set_(leads, lead, 'track', 'Launch');
        if (!String(lead.niche).trim() && j.niche) set_(leads, lead, 'niche', String(j.niche).slice(0, 40));
        try { const rc = recipientCheck_(S, leads, lead); if (rc) note_(leads, lead, rc, false); } catch (e) {}
        note_(leads, lead, 'pre-launch store (password or coming-soon page): track Launch, offer ' + row.offer, false);
        have[String(lead.lead_id)] = row;
        stats.profiles++;
        Utilities.sleep(6000);
        return;
      }
      const page = fetchPage_(lead.website);
      if (!page.ok) throw new Error('site returned HTTP ' + page.code);
      const f = siteFacts_(page);
      const partner = lc_(lead.track) === 'partner';
      const r = partner ? null : researchStore_(S, lead, page);
      if (r && r.big) {   // big brands are never emailed (Ridwan, 2026-10-06): they already have a team and a plan
        set_(leads, lead, 'stage', 'Lost');
        set_(leads, lead, 'notes', ('SKIP: ' + r.bigReasons.join('; ') + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
        note_(leads, lead, 'SKIP, marked Lost. ' + r.bigReasons.join('; '), false);
        stats.profiles++;
        return;
      }
      const sys = partner ? 'You analyse an agency or studio from its public homepage data so a partnership email can refer to real, checkable things. Use ONLY the data given. Never guess. Output JSON only: {"what_they_sell":"the services they sell, one short line","audience":"who their clients are, one short line","niche":"2 to 3 words","signal":"one line: why they might want overflow Shopify development (for example design or ads work but no development shown)","site_notes":"2 to 4 short, concrete, true observations: named client projects or brands, markets, services, team size hints, anything on dev capacity"}.'
        : STORE_PROFILE_SYS_;
      const user = 'Track: ' + (lead.track || 'unknown') + '. Niche: ' + (lead.niche || '') + '. Brand: ' + (lead.brand || '') + '. Website: ' + lead.website + '\nTitle: ' + f.title + '\nMeta: ' + f.desc +
        '\nHeadings: ' + f.headings.join(' | ') + (partner ? '\nSignals: ' + f.signals.join('; ') : '') + '\nHomepage text: ' + f.text +
        (r ? '\n\nEVIDENCE:\n' + r.evidence.join('\n') + '\n\nSOCIAL (context only):\n' + (r.social.join('\n') || 'no social links found on the site') : '');
      const out = callAi_(S, sys, user, partner ? 700 : 1500);
      const j = parseJson_(out.text);
      if (!j || !j.what_they_sell) throw new Error('profile: AI returned no JSON');
      let checkNote = '';
      if (r && j.problem) {   // the claim must survive the store's own pages before any email is written
        const fc = factCheck_(S, j.problem + ' Evidence: ' + (j.problem_evidence || ''), r);
        if (!fc.holds) {
          checkNote = 'Fact check rejected "' + String(j.problem).slice(0, 140) + '": ' + fc.why;
          const fc2 = j.second && j.second.problem ? factCheck_(S, j.second.problem + ' Evidence: ' + (j.second.evidence || ''), r) : { holds: false };
          if (fc2.holds) { Object.assign(j, { offer: j.second.offer || j.offer, problem: j.second.problem, problem_evidence: j.second.evidence || '', worth: Number(j.second.worth) || 0, cost: '', fix: '', second: null }); checkNote += '. Using the second problem instead.'; }
          else j.worth = Math.min(Number(j.worth) || 0, 1);
        } else checkNote = 'Fact check passed' + (fc.why ? ': ' + fc.why : '');
        if (j.second && j.second.problem) {   // step 2 is built on the second problem, so it must survive the same check
          Utilities.sleep(3000);
          const f2 = factCheck_(S, j.second.problem + ' Evidence: ' + (j.second.evidence || ''), r);
          if (!f2.holds) { checkNote += '. Second problem dropped: ' + f2.why; j.second = null; }
        }
        Utilities.sleep(4000);
      }
      const row = { lead_id: lead.lead_id, what_they_sell: j.what_they_sell, audience: j.audience || '', signal: j.signal || '',
        site_notes: (j.site_notes || '') + (partner && f.signals.length ? ' [Signals: ' + f.signals.join('; ') + ']' : ''), updated_at: new Date() };
      if (r && upgraded) {
        let worth = Math.max(0, Math.min(5, Math.round(Number(j.worth) || 0)));
        if (!j.problem || /\[SOFT\]/.test(String(j.problem_evidence || '')) && !/\[(MEASURED|SEEN)\]/.test(String(j.problem_evidence || ''))) worth = Math.min(worth, 2);   // a soft signal alone never carries an email
        const dm = j.decision_maker || {};
        Object.assign(row, { offer: j.offer || '', decision_maker: dm.name ? dm.name + (dm.role ? ', ' + dm.role : '') + (dm.basis ? ' (about page: "' + String(dm.basis).slice(0, 120) + '")' : '') : '', team: j.team || 'unknown',
          what_they_sell: j.what_they_sell + (j.business ? ' | ' + j.business : ''), problem: j.problem || '', problem_evidence: String(j.problem_evidence || '') + (j.cost ? ' | Cost: ' + j.cost : '') + (j.fix ? ' | Fix: ' + j.fix : ''),
          problem_page: j.problem_page || r.pdpUrl || '', problem_worth: worth,
          second_problem: j.second && j.second.problem ? (j.second.offer ? '[' + j.second.offer + '] ' : '') + j.second.problem + ' (evidence: ' + (j.second.evidence || '') + '; worth ' + (j.second.worth || '?') + ')' : '',
          research: (r.evidence.join('\n') + (j.rejected ? '\nRejected: ' + j.rejected : '') + (checkNote ? '\n' + checkNote : '')).slice(0, 4500), socials: r.social.join('\n').slice(0, 2000) });
      }
      const old = have[String(lead.lead_id)];
      if (old && old !== true) Object.keys(row).forEach(k => { if (profiles.headers.indexOf(k) !== -1 && k !== 'lead_id') set_(profiles, old, k, row[k]); });
      else appendObj_('Profiles', row);
      if (!String(lead.niche).trim() && j.niche) set_(leads, lead, 'niche', String(j.niche).slice(0, 40));
      if (r && j.decision_maker && j.decision_maker.name && /^[A-Za-z][A-Za-z'\- ]{1,40}$/.test(j.decision_maker.name)) {
        try { const up = upgradeToDecisionMaker_(S, leads, lead, j.decision_maker.name.trim(), j.decision_maker.role || ''); if (up) note_(leads, lead, 'decision maker: ' + up, false); } catch (e) { stats.problems.push(lead.lead_id + ' decision maker: ' + e.message); }
      }
      if (r) { try { const rc = recipientCheck_(S, leads, lead); if (rc) note_(leads, lead, rc, false); } catch (e) { stats.problems.push(lead.lead_id + ' recipient: ' + e.message); } }
      if (row.problem_worth !== undefined && row.problem_worth < Number(S.MIN_PROBLEM_SCORE || 4))
        note_(leads, lead, 'HOLD: research found nothing worth selling them (best: "' + String(row.problem || 'none').slice(0, 160) + '", worth ' + row.problem_worth + '/5). See Profiles > research. To email anyway, write the problem in Profiles > problem and set problem_worth to 5.', false);
      have[String(lead.lead_id)] = row;
      stats.profiles++;
      Utilities.sleep(6000);   // free-tier Gemini allows only a handful of calls a minute
    } catch (e) { note_(leads, lead, 'profile failed: ' + String(e.message || e).slice(0, 420), true); stats.problems.push(lead.lead_id + ': ' + e.message); if (/HTTP 429|RESOURCE_EXHAUSTED/i.test(String(e.message))) stats.limited = true; }
  });
}

// ---------- 4. Write the 5-email sequence ----------

const SEQ_TASK_ = [
  'TASK: write a 5-email cold sequence from Ridwan to this lead. Use ONLY facts in the lead data and profile below plus the brief. Any observation in email 1 must be supported by the profile. If the profile has no solid observation, keep email 1 honest and general rather than inventing one.',
  'THE PROBLEM PARAGRAPH IS THE WHOLE EMAIL. When the lead data has THE OFFER and THE PROBLEM, email 1 is built on them: show you understood how THIS business sells (their product, price point, how customers reach them), name the page, product or element from the evidence, say what the shopper or the ad click runs into, what that costs in plain words, and exactly what Ridwan would build (THE FIX). It must be specific enough that the founder can check it in ten seconds. Never call something broken, missing or an error unless its evidence is [MEASURED] or [SEEN]. A [SOFT] gap is asked, never stated: "is cold traffic going straight to the product page, or is there a pre-sell page I missed?". When THE PROBLEM or SECOND PROBLEM rests on a [LINKS] line, name each link by its visible label and where it sits ("the Best Sellers item in your top menu"), say plainly what happens when a visitor clicks it (404 page, or back to the homepage they are already on), and never paste a URL or path. Mention page speed or load time ONLY when THE PROBLEM rests on a [SPEED] evidence line: then use its exact numbers and say it is Google\'s own measurement on phones, never a guess or a rounded-up claim. Never pitch a small fix (a size chart, a photo, a description) as the reason to talk. Never mention language, translation, currency, price display, country or market differences (stores adapt these to where the visitor browses from, and research browses from Google servers abroad, so what it sees is not what their customers see). Never use generic lines that could go to any store ("your site could convert better", "a few small tweaks", "some friction", "optimise your store"). If SECOND PROBLEM is given, step 2 uses it. Address the decision maker by first name when known, even when the email goes to a shared inbox.',
  'Step 1: the observation, the problem it usually causes, what Ridwan does, one interest question. Steps 2 to 5 must each add something NEW and never say "just checking in" or "following up". Follow-ups NEVER make a new claim about their site: the only observations allowed are THE PROBLEM and SECOND PROBLEM. Without a SECOND PROBLEM, steps 2 to 5 add something about THE OFFER instead (how Ridwan would do it, one real proof line, a smaller first step, a lighter ask). Never write "one more thing I noticed". Step 3 may use one real proof line from the brief if it genuinely fits. Step 5 is a warm, clean close that leaves the door open.',
  'MOCKUP OFFER (2026-10-26): when Track is Fix and there is no REDESIGN ALREADY BUILT line, the interest question at the end of step 1 is an offer to mock up how that page would look fixed, for example "Want me to mock up how that page would look fixed, so you can see it before deciding anything?". Say "I can" or "want me to", never that it is already built. One follow-up may repeat the offer in different words.',
  'Every email under 100 words, plain text, no links, no signature (added by the system), no closing way-out line such as "no problem if not" or "tell me and I will stop" (the footer already carries the opt-out): end on the question. Steps 2 to 5 read as replies in the same thread: no subject.',
  'If Track is Launch (the store is behind a password or coming-soon page, so they are building it now): never describe the store behind the password, its products or design (nobody can see them). Open with what is visible (their coming-soon page, the launch timing, an email signup or the lack of one), then THE OFFER: launch_review = offer a free look at their product page before launch if they share the password; launch_build = help finish the store so it launches properly; waitlist_page = a coming-soon page that collects emails before launch; launch_creatives = launch ad creatives from their product photos. Good ask: whether they are building it themselves or someone is helping. Follow-ups stay about the launch.',
  'Greeting: use the contact name if given ("Hi Amina,"). If no name, start with "Hi," and the observation. For a Nigerian or African lead, email 1 must begin with exactly {{greeting}} followed by the name, e.g. "{{greeting}} Amina." and steps 2 to 5 begin "Hi Amina,". For everyone else, no greeting phrase.',
  'If Track is Build (the business has no website): the observation comes from the notes (what they sell and how, for example orders by DM or on a marketplace); pitch a simple online store; email 1 offers a free ad creative made from their own product photos, nothing owed. Do not offer a free website in the sequence: that comes only if they reply.',
  'PLATFORM and BUSINESS MODEL change the pitch. Own-brand: pitch conversion, trust and the brand story. Dropship-likely: pitch only product-page conversion and trust (their money comes from ads sending traffic to a page); do not assume they make the product, do not pitch a brand-building retainer. Print-on-demand: pitch product pages and brand polish. Reseller (many brands): pitch catalogue navigation, collection filters and search. Unknown: keep it generic. If the platform is not Shopify, Ridwan works mainly in Shopify: offer a CRO review of the current site, or a move to Shopify, and never claim skills on that platform. Never say you detected their business model; just fit the pitch to it.',
  'Subject for step 1: short, lower case, specific, no clickbait, no brand-name-only.',
  'Output JSON only: {"basis":"one line: which profile facts the email-1 observation rests on","emails":[{"step":1,"subject":"...","body":"..."},{"step":2,"body":"..."},{"step":3,"body":"..."},{"step":4,"body":"..."},{"step":5,"body":"..."}]}',
].join('\n');

const SEQ_PARTNER_TASK_ = [
  'TASK: write a 5-email cold sequence from Ridwan to the owner or lead of an AGENCY or STUDIO, proposing he becomes their white-label Shopify development partner (see PARTNER TRACK in the brief). Use ONLY facts in the lead data and profile plus the brief. Ridwan has NOT done white-label work before: never claim it, never write "agencies like yours", never invent results or numbers.',
  'Step 1: one true, specific observation about THEM from the profile (a service they sell, a client project or market they name, or a gap such as design and ads but no development shown), the bottleneck that usually follows, one sentence on the offer (overflow Shopify builds, delivered under their brand, they keep the client), one interest question such as whether overflow Shopify work ever piles up. No prices. If the profile has no solid observation, keep it honest and general.',
  'Step 2: how it works in plain words: they keep the client and the relationship, work ships under their brand, fixed price per project, scope and turnaround confirmed before any work starts, an NDA on request. No numbers, no dates.',
  'Step 3: the founding partner offer: the first few agencies get partner rates locked for 12 months and the first small task as a paid pilot at half the partner rate, so there is almost no risk. Rates are shared on request, not in the email.',
  'Step 4: honest proof: Ridwan builds Shopify stores for real DTC brands (name one real project from the brief, as direct client work, never as white-label). Say plainly that the partner programme is new. Offer to scope one small task.',
  'Step 5: a warm, clean close that leaves the door open.',
  'Every email under 100 words, plain text, no links, no signature, no closing way-out line (the footer already carries the opt-out): end on the question. Steps 2 to 5 read as replies in the same thread: no subject. Greeting: contact name if given ("Hi Sam,"), else "Hi,". For a Nigerian or African lead, email 1 begins with exactly {{greeting}} then the name; steps 2 to 5 begin "Hi Name,". Subject for step 1: short, lower case, specific ("overflow shopify builds for [agency]"), no clickbait.',
  'Output JSON only: {"basis":"one line: which profile facts the email-1 observation rests on","emails":[{"step":1,"subject":"...","body":"..."},{"step":2,"body":"..."},{"step":3,"body":"..."},{"step":4,"body":"..."},{"step":5,"body":"..."}]}',
].join('\n');

// 2026-10-26 (Ridwan): when a redesign of the store's page already exists, it is the hook of the whole sequence.
const REDESIGN_TASK_ = 'Ridwan has ALREADY redesigned one of this store\'s pages (named above) as a full concept page, unasked and unpaid. Follow the PAGE MATCH line exactly. If the pages match: email 1 rests on THE PROBLEM, then says he went ahead and rebuilt that page as a concept to show the fix, and asks if they want to see it (he will send a side-by-side of their page and the concept). If they do not match: email 1 still rests on THE PROBLEM on its own page, then mentions the rebuilt page only as proof of how he works and offers to send it and to do the same for the problem page. No link in email 1, never say it is live or published, never claim results, sales or conversion numbers, never imply they are a client. Follow-ups may offer to send it again, describe one real change on it (only changes that fix THE PROBLEM or SECOND PROBLEM), or offer to walk them through it on a short call.';

function writeSequences_(S, stats, timeLeft) {
  const leads = read_('Leads');
  const profiles = read_('Profiles');
  const seq = read_('Sequence');
  const has1 = {};
  seq.rows.forEach(r => { if (Number(r.step) === 1 && r.status !== 'Superseded') has1[String(r.lead_id)] = true; });
  const ex = String(S.VOICE_EXAMPLES || '').trim();
  let sigRows = [];
  try { sigRows = read_('Signals').rows; } catch (e) { /* tab not created yet: run Outreach > Set up tabs */ }

  const prof = id => profiles.rows.find(x => String(x.lead_id) === String(id));
  candidates_(leads, l => !has1[String(l.lead_id)] && prof(l.lead_id) && problemOk_(l, prof(l.lead_id), S), PREP_BATCH_.sequence).forEach(lead => {
    if (!timeLeft() || stats.limited) return;
    try {
      const p = profiles.rows.find(x => String(x.lead_id) === String(lead.lead_id));
      const sys = BRIEF_.core + '\n\nREGIONAL VOICE FOR THIS LEAD:\n' + BRIEF_.regions[regionKey_(lead.country)] + '\n\n' + (lc_(lead.track) === 'partner' ? SEQ_PARTNER_TASK_ : SEQ_TASK_) + (liveSignals_(sigRows, lead) ? '\n\n' + SIGNAL_TASK_ : '') +
        (ex ? '\n\nReal writing by Ridwan. Match its voice, length and rhythm:\n' + ex : '');
      const user = 'LEAD: ' + [lead.brand, lead.contact_name || '(no contact name)', lead.website].filter(String).join(' | ') +
        '\nPlatform: ' + (lead.platform || 'unknown') + '. Business model: ' + (lead.business_model || 'unknown') + '. Country: ' + (lead.country || '') + '. Niche: ' + (lead.niche || '') + '. Track: ' + (lead.track || '') + '. Play: ' + (lead.play || '') + '. Source: ' + (lead.source || '') +
        (liveSignals_(sigRows, lead) ? '\nLIVE SIGNALS (most recent first):\n' + liveSignals_(sigRows, lead) : '') + (alsoOn_(sigRows, lead) ? '\nAlso listed on: ' + alsoOn_(sigRows, lead) : '') +
        '\nWhat they sell: ' + p.what_they_sell + '\nAudience: ' + p.audience + '\nSignal: ' + p.signal + '\nObservations: ' + p.site_notes +
        (p.offer ? '\nTHE OFFER: ' + p.offer : '') + (p.decision_maker ? '\nDecision maker: ' + p.decision_maker + '. Team: ' + (p.team || 'unknown') : '') +
        (p.problem ? '\nTHE PROBLEM (email 1 rests on this): ' + p.problem + '\nIts evidence, cost and THE FIX: ' + (p.problem_evidence || '') + '\nPage: ' + (p.problem_page || '') : '') +
        (p.second_problem ? '\nSECOND PROBLEM (for step 2): ' + p.second_problem : '') +
        (hasRedesign_(lead) ? '\nREDESIGN ALREADY BUILT: ' + lead.redesign + '\n' + redesignMatch_(lead, p) + '\n' + REDESIGN_TASK_ : '') + (p.socials ? '\nSocial (context only, never flatter or criticise the following): ' + String(p.socials).slice(0, 600) : '') +
        '\nNotes: ' + (lead.notes || '');
      const out = callAi_(S, sys, user, 1800);
      const j = parseJson_(out.text);
      if (!j || !j.emails || j.emails.length < 5) throw new Error('sequence: AI returned fewer than 5 emails');

      let flags = [];
      j.emails.slice().sort((a, b) => a.step - b.step).forEach(e => {
        const body = stripWayOut_(clean_(e.body || ''));
        const subject = Number(e.step) === 1 ? clean_(e.subject || '').toLowerCase().slice(0, 90) : '';
        let f = draftFlags_(body.replace(/\{\{greeting\}\}/g, ''));
        if (Number(e.step) === 1 && GENERIC_PROBLEM_.test(body)) f = (f ? f + '; ' : '') + 'generic problem line, not specific to this store';
        if (f) flags.push('step ' + e.step + ': ' + f);
        appendObj_('Sequence', { lead_id: lead.lead_id, step: Number(e.step), subject: subject, body: body, status: 'Draft' });
      });
      if (!/\[SPEED\]/.test(String(p.problem_evidence || '') + String(p.research || '')) && j.emails.some(e => SPEED_WORDS_.test(String(e.body || ''))))
        flags.push('mentions speed but research found no obvious slowness');
      if (String(lead.notes || '').indexOf(UNCONFIRMED_TAG_) !== -1) flags.push('recipient not confirmed: ' + lead.email + ' is not published on their site');
      if (j.emails.some(e => PRICE_CLAIM_.test(String(e.body || '') + ' ' + String(e.subject || '')))) flags.push('makes a price claim: prices are converted per country, never a reason to email');
      if (j.emails.some(e => LOCALE_WORDS_.test(String(e.body || '') + ' ' + String(e.subject || '')))) flags.push('mentions language, translation or currency: never a reason to email');
      if (p.team && lc_(p.team) !== 'solo' && sharedInbox_(lead.email)) flags.push('email goes to a shared inbox (' + lead.email + '), not the decision maker' + (p.decision_maker ? ' (' + String(p.decision_maker).split(' (')[0] + ')' : '') + ': find their own address before approving');
      set_(leads, lead, 'notes', ('Observation basis: ' + (j.basis || '?') + ' [' + out.provider + ']' + (flags.length ? ' | CHECK: ' + flags.join('; ') : '') +
        (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
      if (isTrue_(S.AUTO_APPROVE) && !flags.length && sendableStatus_(lead.email_status, S)) set_(leads, lead, 'approved', true);
      has1[String(lead.lead_id)] = true;
      stats.sequences++;
      Utilities.sleep(6000);
    } catch (e) { note_(leads, lead, 'sequence failed: ' + String(e.message || e).slice(0, 420), true); stats.problems.push(lead.lead_id + ': ' + e.message); if (/HTTP 429|RESOURCE_EXHAUSTED/i.test(String(e.message))) stats.limited = true; }
  });
}

/** Removes a closing way-out line ("No problem if...", "If not, no problem at all.", "Tell me and I will stop."): the footer already has the opt-out (Ridwan, 2026-10-08). */
function stripWayOut_(body) {
  const paras = String(body).split(/\n\s*\n/);
  const wayOut = /^(no (problem|worries|pressure)|if (not|this (is not|isn't|is no)|now is not|you would rather|it is not|the timing)|not the right time|tell me and i (will|'ll)|either way|all good if|totally fine if|happy to leave it)/i;
  while (paras.length > 1 && wayOut.test(paras[paras.length - 1].trim()) && paras[paras.length - 1].trim().length < 120) paras.pop();
  return paras.join('\n\n').trim();
}

const SPEED_WORDS_ = /\bslow|speed|load(s|ing)? (time|in)|takes? .{0,20}to load|seconds to (load|appear)|pagespeed/i;
const GENERIC_PROBLEM_ = /could (be|convert|perform) better|small tweaks|few tweaks|some friction|optimi[sz]e your (site|store|website)|boost (your )?(sales|conversions)|improve (your )?conversions?|take your (store|brand) to the next level|leaving money on the table/i;

function parseJson_(text) {
  const t = String(text).replace(/```json|```/gi, '');
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a === -1 || b === -1) return null;
  try { return JSON.parse(t.slice(a, b + 1)); } catch (e) { return null; }
}


// ---------- Email ranking: aim for the decision maker ----------
// Higher is better. Their own domain counts most; then a person (founder, owner, a name that matches the contact)
// beats a shared inbox (hello, contact, info), which beats a ticket desk (support, orders). Bounce traps score -100.
function rankEmail_(email, host, contactName) {
  const e = String(email || '').toLowerCase().trim();
  if (!emailOk_(e)) return -100;   // malformed, free-mail typo or template placeholder
  const local = e.split('@')[0], dom = e.split('@')[1];
  const h = String(host || '').toLowerCase().replace(/^www\./, '');
  if (/^(no-?reply|do-?not-?reply|mailer-daemon|postmaster|abuse|webmaster|privacy|legal|unsubscribe|returns?|billing|accounts?|jobs?|careers?|press|media|pr)$/.test(local)) return -100;
  let s = 0;
  const stem = d => d.replace(/\.(co|com|org|net|ac|gov)\.[a-z]{2}$|\.[a-z]{2,}$/, '').split('.').pop();
  if (h && (dom === h || dom.endsWith('.' + h) || h.endsWith('.' + dom) || (stem(dom).length > 3 && stem(dom) === stem(h)))) s += 10;   // their own domain (also brand.ca on brand.com)
  const parts = String(contactName || '').toLowerCase().split(/[^a-z]+/).filter(p => p.length > 2);
  if (/^(founder|owner|ceo|director|md|principal|president|cofounder|co-founder)$/.test(local)) s += 8;   // the decision maker's role mailbox
  else if (parts.some(p => local.indexOf(p) !== -1)) s += 8;                                          // matches the named contact
  else if (/^[a-z]{2,}([._-][a-z]{2,})?$/.test(local) && !/^(hello|hi|hey|info|contact|team|shop|store|sales|support|help|care|service|orders?|customer|admin|enquiries|enquiry|general|mail|office|hola)$/.test(local)) s += 6;   // looks like a person's name
  else if (/^(hello|hi|hey|contact|team|info|enquiries|enquiry|hola|office)$/.test(local)) s += 3;    // shared inbox
  else if (/^(sales|shop|store|admin|general|mail)$/.test(local)) s += 2;
  else if (/^(support|help|care|service|orders?|customer)/.test(local)) s += 1;                       // ticket desk
  if (/@(gmail|yahoo|outlook|hotmail|icloud|proton|protonmail|live)\./i.test(e)) s += 2;            // a free-mail address a small owner published is usually the owner
  return s;
}

/** Best address from a list (array or " | " separated text). Returns { best, others[] }. */
function pickBestEmail_(list, host, contactName) {
  const arr = (Array.isArray(list) ? list : String(list || '').split(/[|,;\s]+/)).map(x => String(x).trim().toLowerCase()).filter(Boolean);
  const uniq = arr.filter((x, i) => arr.indexOf(x) === i && rankEmail_(x, host, contactName) > -100);
  uniq.sort((a, b) => rankEmail_(b, host, contactName) - rankEmail_(a, host, contactName));
  return { best: uniq[0] || '', others: uniq.slice(1) };
}


// ---------- Live signals (public questions, job posts, feedback requests) ----------
const SIGNAL_TASK_ = 'THIS LEAD HAS A LIVE SIGNAL: someone at the business publicly asked something, posted a job, or asked for feedback on their store (see LIVE SIGNALS). Email 1 must respond to that directly and be useful about it before offering anything. It overrides the site-observation rule: the observation is the signal itself. Do not paste the post, do not name the platform unless the signal is a public post about their own store ("saw your post asking about X" is fine). For a hiring signal, speak to the role they described and offer to take that work on. Use only what the signal says: nothing personal, nothing creepy. If a signal is only "also listed on" another site, ignore it for the angle.';

function liveSignals_(rows, lead) {
  const id = String(lead.lead_id), dom = cleanDomain_(lead.website || '');
  return rows.filter(s => lc_(s.kind) !== 'also found on' && ((s.lead_id && String(s.lead_id) === id) || (dom && cleanDomain_(s.domain) === dom)))
    .sort((a, b) => new Date(b.found_at) - new Date(a.found_at)).slice(0, 3)
    .map(s => '- [' + s.kind + (s.who ? ', ' + s.who : '') + (s.source ? ', ' + s.source : '') + '] ' + String(s.text).slice(0, 500)).join('\n');
}

function alsoOn_(rows, lead) {
  const id = String(lead.lead_id), dom = cleanDomain_(lead.website || '');
  return rows.filter(s => lc_(s.kind) === 'also found on' && ((s.lead_id && String(s.lead_id) === id) || (dom && cleanDomain_(s.domain) === dom)))
    .slice(0, 4).map(s => String(s.text).slice(0, 160)).join(' ; ');
}

// ---------- Rewrite unsent follow-ups for leads already contacted (2026-10-08) ----------
// Leads emailed before the research and fact-check rules still carried follow-ups that invented new claims (ilouity.com step 2).
// Outreach > Rewrite unsent follow-ups marks those Draft steps Superseded; this step writes new ones from the profile and the
// email that was actually sent, under the current rules. If anything is flagged, the lead is unapproved for a human look.

const FOLLOWUP_TASK_ = [
  'TASK: email 1 (below) was already sent to this lead. Write the REMAINING follow-ups only, as replies in the same thread: no subject.',
  'Follow-ups NEVER make a new claim about their site. The only observations allowed are what email 1 already said and SECOND PROBLEM if given. Otherwise each follow-up adds something about the offer: how Ridwan would do it, one real proof line from the brief, a smaller first step, a lighter ask. Never write "one more thing I noticed", "just checking in" or "following up". The last one is a warm, clean close.',
  'Every email under 90 words, plain text, no links, no signature. No closing way-out line (the footer already carries the opt-out): end on the question. Never mention prices, currencies, languages or page speed unless the lead data has a [SPEED] line. Greeting: the contact name if given ("Hi Amina,"), else "Hi,".',
  'Output JSON only: {"emails":[{"step":N,"body":"..."}, ...]} with exactly the steps asked for.',
].join('\n');

// 2026-10-26: a redesign was finished while this lead was mid-sequence (or after it ended). It replaces the next follow-up, so no extra email lands.
const REDESIGN_FOLLOWUP_TASK_ = 'The FIRST step you write now (the next one to send) says Ridwan went ahead and rebuilt the page as a concept (follow the PAGE MATCH line about which page), and asks if they want to see it: he will send a side-by-side of their page today and the concept. No link, never live or published, no results claimed. The remaining steps follow the normal follow-up rules and may offer to send it again or walk them through it on a short call.';

function writeFollowups_(S, stats, timeLeft) {
  const leads = read_('Leads'), profiles = read_('Profiles'), seq = read_('Sequence');
  const todo = leads.rows.filter(l => l.lead_id && lc_(l.stage) === 'contacted' && Number(l.touch_count || 0) >= 1).filter(l => {
    const rows = seq.rows.filter(r => String(r.lead_id) === String(l.lead_id) && r.status !== 'Superseded');
    const sent = rows.some(r => Number(r.step) === 1 && r.status === 'Sent');
    return sent && !rows.some(r => Number(r.step) === Number(l.touch_count) + 1);
  }).sort((a, b) => hasRedesign_(b) - hasRedesign_(a)).slice(0, 2);   // redesign emails first (2026-10-26)
  todo.forEach(lead => {
    if (!timeLeft() || stats.limited) return;
    try {
      const id = String(lead.lead_id), next = Number(lead.touch_count) + 1;
      const revival = next === 6 && hasRedesign_(lead) && String(lead.notes || '').indexOf('REDESIGN REVIVAL') !== -1;   // one extra email after a finished sequence, once
      if (next > 5 && !revival) return;
      const p = profiles.rows.find(x => String(x.lead_id) === id) || {};
      const first = seq.rows.find(r => String(r.lead_id) === id && Number(r.step) === 1 && r.status === 'Sent');
      const steps = []; for (let s = next; s <= (revival ? 6 : 5); s++) steps.push(s);
      const sys = BRIEF_.core + '\n\nREGIONAL VOICE FOR THIS LEAD:\n' + BRIEF_.regions[regionKey_(lead.country)] + '\n\n' + FOLLOWUP_TASK_;
      const user = 'Write steps ' + steps.join(', ') + '.\nLEAD: ' + [lead.brand, lead.contact_name || '(no contact name)', lead.website].filter(String).join(' | ') + '. Country: ' + (lead.country || '') + '. Track: ' + (lead.track || '') +
        '\nEMAIL 1 THAT WAS SENT (subject "' + (first ? first.subject : '') + '"):\n' + (first ? String(first.body) : '') +
        '\nWhat they sell: ' + (p.what_they_sell || '') + (p.offer ? '\nTHE OFFER: ' + p.offer : '') + (p.second_problem ? '\nSECOND PROBLEM: ' + p.second_problem : '') +
        (p.problem_page ? '\nPage email 1 was about: ' + p.problem_page : '') +
        (hasRedesign_(lead) ? '\nREDESIGN ALREADY BUILT: ' + lead.redesign + '\n' + redesignMatch_(lead, p) + '\n' + REDESIGN_FOLLOWUP_TASK_ + (revival ? '\nThis is step 6: the sequence had ended with no reply. Write ONE short, friendly note in the same thread whose only point is the rebuilt page and the offer to send it. No pressure, no new claims about the site.' : '') : '');
      const out = callAi_(S, sys, user, 1200);
      const j = parseJson_(out.text);
      if (!j || !j.emails || !j.emails.length) throw new Error('follow-ups: AI returned no emails');
      const flags = [];
      j.emails.filter(e => steps.indexOf(Number(e.step)) !== -1).sort((a, b) => a.step - b.step).forEach(e => {
        const body = stripWayOut_(clean_(e.body || ''));
        const f = draftFlags_(body);
        if (f) flags.push('step ' + e.step + ': ' + f);
        if (PRICE_CLAIM_.test(body) || LOCALE_WORDS_.test(body)) flags.push('step ' + e.step + ': price, currency or language point');
        appendObj_('Sequence', { lead_id: id, step: Number(e.step), subject: '', body: body, status: 'Draft' });
      });
      if (flags.length && isTrue_(lead.approved)) set_(leads, lead, 'approved', false);
      note_(leads, lead, 'follow-ups ' + steps.join(',') + ' rewritten under the current rules' + (flags.length ? '. CHECK: ' + flags.join('; ') + ' (unapproved until you look)' : ''), false);
      stats.sequences++;
      Utilities.sleep(6000);
    } catch (e) { stats.problems.push(lead.lead_id + ' follow-ups: ' + e.message); if (/HTTP 429|RESOURCE_EXHAUSTED/i.test(String(e.message))) stats.limited = true; }
  });
}

/** Menu: supersede the unsent follow-ups of leads already contacted; the next Prepare run rewrites them. Sent emails are never touched. */
function redoOldFollowups() {
  const ui = SpreadsheetApp.getUi();
  if (ui.alert('Rewrite unsent follow-ups for leads already emailed?', 'Their unsent follow-up drafts become Superseded and are rewritten under the current rules on the next Prepare run. Sent emails do not change.', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  const leads = read_('Leads'), seq = read_('Sequence');
  const contacted = {};
  leads.rows.filter(l => lc_(l.stage) === 'contacted').forEach(l => { contacted[String(l.lead_id)] = Number(l.touch_count || 0); });
  let n = 0;
  seq.rows.filter(r => contacted[String(r.lead_id)] !== undefined && r.status === 'Draft' && Number(r.step) > contacted[String(r.lead_id)]).forEach(r => { set_(seq, r, 'status', 'Superseded'); n++; });
  toast_(n + ' unsent follow-up(s) superseded across ' + Object.keys(contacted).length + ' contacted lead(s). Run Prepare new leads now to rewrite them.');
}

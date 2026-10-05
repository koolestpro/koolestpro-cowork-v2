/**
 * Koolestpro Outreach: web API for KoolestFlow (the dashboard).
 *
 * The Sheet stays the system of record and this script stays the engine (it is the only thing that can use Gmail).
 * KoolestFlow is the screen: it calls this API to read leads, threads and drafts, and to approve, edit and queue.
 *
 * Deploy: Apps Script > Deploy > New deployment > type "Web app" > Execute as: Me > Who has access: Anyone.
 * ("Anyone" only means the URL is reachable; every call must carry the secret token, or it is refused.)
 * Then Project Settings > Script properties > OUTREACH_API_TOKEN = a long random string, and put the deployment URL
 * and the same token into KoolestFlow's environment (OUTREACH_API_URL, OUTREACH_API_TOKEN).
 *
 * Safety: TEST_MODE cannot be changed through this API; flip it in the Settings tab yourself. Nothing here sends mail
 * directly: approving a draft or lead only queues it for the normal sender.
 */

const API_SETTINGS_ALLOWED_ = ['HOT_EXTRA_PER_DAY', 'HOT_PER_RUN', 'HOT_WINDOW_HOURS', 'PAUSED', 'AUTO_APPROVE', 'SEND_TO_CATCH_ALL', 'MIN_FIT_SCORE', 'DAILY_CAP_START', 'MAX_PER_RUN', 'AI_ORDER'];
const API_LEAD_FIELDS_ = ['lead_id', 'brand', 'website', 'contact_name', 'email', 'email_status', 'country', 'time_zone', 'niche', 'source',
  'track', 'play', 'notes', 'platform', 'business_model', 'signature'];

function doGet() { return apiOut_({ ok: true, service: 'koolestpro-outreach' }); }

function doPost(e) {
  let out;
  try {
    const req = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const expected = PropertiesService.getScriptProperties().getProperty('OUTREACH_API_TOKEN');
    if (!expected || String(req.token || '') !== expected) throw new Error('unauthorized');
    out = { ok: true, data: apiRoute_(String(req.action || ''), req.args || {}) };
  } catch (err) {
    out = { ok: false, error: String(err && err.message || err) };
  }
  return apiOut_(out);
}

function apiOut_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function apiRoute_(action, a) {
  switch (action) {
    case 'summary': return apiSummary_();
    case 'leads': return apiLeads_(a);
    case 'lead': return apiLead_(a);
    case 'discovery': return apiDiscovery_(a);
    case 'get_settings': return apiSettings_();
    case 'run_tick': tick(); return { ran: 'tick' };   // logs replies, drafts replies, sends approved drafts
    default: break;
  }
  // Everything below changes the Sheet: one writer at a time.
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) throw new Error('busy, try again in a moment');
  try {
    switch (action) {
      case 'set_approved': return apiSetApproved_(a);
      case 'update_step': return apiUpdateStep_(a);
      case 'update_draft': return apiUpdateDraft_(a);
      case 'add_lead': return apiAddLead_(a);
      case 'add_domains': return apiAddDomains_(a);
      case 'add_discovery_rows': return apiAddDiscoveryRows_(a);
      case 'add_signals': return apiAddSignals_(a);
      case 'set_settings': return apiSetSettings_(a);
      default: throw new Error('unknown action: ' + action);
    }
  } finally {
    lock.releaseLock();
  }
}

function apiIso_(v) {
  if (v === '' || v === null || v === undefined) return '';
  if (Object.prototype.toString.call(v) === '[object Date]') return isNaN(v) ? '' : v.toISOString();
  return String(v);
}

function apiCell_(v) { return Object.prototype.toString.call(v) === '[object Date]' ? apiIso_(v) : v; }

function apiPlain_(row) {
  const o = {};
  Object.keys(row).forEach(k => { if (k !== '_r') o[k] = apiCell_(row[k]); });
  return o;
}

function apiSummary_() {
  const S = settings_(), me = me_();
  const leads = read_('Leads'), msgs = read_('Messages'), drafts = read_('Drafts'), disc = read_('Discovery');
  const stages = {}, discovery = {};
  leads.rows.forEach(l => { const s = String(l.stage || 'New'); stages[s] = (stages[s] || 0) + 1; });
  disc.rows.forEach(r => { const s = String(r.status || 'New'); discovery[s] = (discovery[s] || 0) + 1; });
  const now = new Date();
  return {
    sending_as: me,
    test_mode: isTrue_(S.TEST_MODE),
    paused: isTrue_(S.PAUSED),
    sent_today: msgs.rows.filter(m => m.direction === 'out' && lc_(m.sender_account) === me && isToday_(m.sent_at)).length,
    daily_cap: dailyCap_(S),
    replies_today: msgs.rows.filter(m => m.direction === 'in' && isToday_(m.sent_at)).length,
    drafts_to_review: drafts.rows.filter(d => d.status === 'Ready for review').length,
    drafts_waiting_ai: drafts.rows.filter(d => d.status === 'Needs draft').length,
    drafts_approved_queued: drafts.rows.filter(d => d.status === 'Approved').length,
    awaiting_approval: leads.rows.filter(l => !isTrue_(l.approved) && ['New', ''].indexOf(String(l.stage)) !== -1 && String(l.email)).length,
    ready_to_send: leads.rows.filter(l => isTrue_(l.approved) && ['New', 'Contacted', ''].indexOf(String(l.stage)) !== -1 && sendableStatus_(l.email_status, S) &&
      (Number(l.touch_count || 0) === 0 || (l.next_touch_at && new Date(l.next_touch_at) <= now))).length,
    stages: stages,
    discovery: discovery,
    keys: { gemini: !!PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY'), deepseek: !!PropertiesService.getScriptProperties().getProperty('DEEPSEEK_API_KEY'),
      verifier: !!PropertiesService.getScriptProperties().getProperty('MYEMAILVERIFIER_API_KEY') },
  };
}

function apiLeads_(a) {
  const leads = read_('Leads'), seq = read_('Sequence');
  const stage = String(a.stage || ''), q = lc_(a.q), limit = Math.min(500, Number(a.limit) || 200), offset = Number(a.offset) || 0;
  const steps = {};
  seq.rows.forEach(r => {
    const id = String(r.lead_id);
    steps[id] = steps[id] || { total: 0, sent: 0 };
    steps[id].total++; if (r.status === 'Sent') steps[id].sent++;
  });
  const rows = leads.rows.filter(l => l.lead_id && (!stage || String(l.stage || 'New') === stage) &&
    (!q || [l.lead_id, l.brand, l.website, l.email, l.niche, l.country].some(v => lc_(v).indexOf(q) !== -1)));
  return {
    total: rows.length,
    leads: rows.slice(offset, offset + limit).map(l => ({
      lead_id: String(l.lead_id), brand: l.brand, website: l.website, contact_name: l.contact_name, email: l.email, email_status: l.email_status,
      country: l.country, niche: l.niche, track: l.track, platform: l.platform, business_model: l.business_model,
      stage: l.stage || 'New', approved: isTrue_(l.approved), touch_count: Number(l.touch_count || 0), next_touch_at: apiIso_(l.next_touch_at),
      prep_note: l.prep_note || '', notes: l.notes || '', steps: steps[String(l.lead_id)] || { total: 0, sent: 0 },
    })),
  };
}

function apiLead_(a) {
  const id = String(a.lead_id || '');
  if (!id) throw new Error('lead_id required');
  const leads = read_('Leads');
  const lead = leads.rows.find(l => String(l.lead_id) === id);
  if (!lead) throw new Error('lead not found: ' + id);
  const by = tab => read_(tab).rows.filter(r => String(r.lead_id) === id);
  const msgs = read_('Messages').rows.filter(m => String(m.lead_id) === id).sort((x, y) => new Date(x.sent_at) - new Date(y.sent_at));
  const mem = read_('Memory').rows.find(m => String(m.lead_id) === id);
  const prof = read_('Profiles').rows.find(p => String(p.lead_id) === id);
  return {
    lead: apiPlain_(lead),
    profile: prof ? apiPlain_(prof) : null,
    memory: mem ? apiPlain_(mem) : null,
    sequence: by('Sequence').map(r => apiPlain_(r)).sort((x, y) => Number(x.step) - Number(y.step)),
    messages: msgs.map(m => apiPlain_(m)),
    drafts: read_('Drafts').rows.filter(d => String(d.lead_id) === id).map(d => Object.assign(apiPlain_(d), { row: d._r })),
  };
}

function apiDiscovery_(a) {
  const rows = read_('Discovery').rows;
  const status = String(a.status || '');
  const list = rows.filter(r => !status || String(r.status || 'New') === status).slice(-Math.min(300, Number(a.limit) || 100)).reverse();
  return { total: rows.length, rows: list.map(r => apiPlain_(r)) };
}

function apiSettings_() {
  const S = settings_(), out = {};
  API_SETTINGS_ALLOWED_.concat(['TEST_MODE', 'SIGNATURE', 'SENDER_NAME', 'ALERT_EMAIL', 'DAILY_CAP_MAX', 'SEND_START_HOUR', 'SEND_END_HOUR']).forEach(k => { out[k] = S[k]; });
  out.editable = API_SETTINGS_ALLOWED_;
  return out;
}

function apiSetSettings_(a) {
  const tab = read_('Settings');
  const changed = {};
  Object.keys(a.values || {}).forEach(k => {
    if (API_SETTINGS_ALLOWED_.indexOf(k) === -1) throw new Error('setting not editable here: ' + k);
    const row = tab.rows.find(r => String(r.key).trim() === k);
    if (!row) throw new Error('setting not found: ' + k);
    set_(tab, row, 'value', String(a.values[k]));
    changed[k] = String(a.values[k]);
  });
  return { changed: changed };
}

function apiSetApproved_(a) {
  const leads = read_('Leads');
  const lead = leads.rows.find(l => String(l.lead_id) === String(a.lead_id));
  if (!lead) throw new Error('lead not found');
  set_(leads, lead, 'approved', !!a.approved);
  return { lead_id: lead.lead_id, approved: !!a.approved };
}

function apiUpdateStep_(a) {
  const seq = read_('Sequence');
  const row = seq.rows.find(r => String(r.lead_id) === String(a.lead_id) && Number(r.step) === Number(a.step));
  if (!row) throw new Error('step not found');
  if (row.status === 'Sent') throw new Error('that email was already sent');
  if (a.body !== undefined) set_(seq, row, 'body', String(a.body));
  if (a.subject !== undefined && Number(a.step) === 1) set_(seq, row, 'subject', String(a.subject));
  return { lead_id: row.lead_id, step: row.step };
}

function apiUpdateDraft_(a) {
  const drafts = read_('Drafts');
  const row = drafts.rows.find(d => d._r === Number(a.row) && String(d.lead_id) === String(a.lead_id));
  if (!row) throw new Error('draft not found');
  if (row.status === 'Sent') throw new Error('that reply was already sent');
  if (a.draft_body !== undefined) set_(drafts, row, 'draft_body', String(a.draft_body));
  if (a.status !== undefined) {
    if (['Ready for review', 'Approved', 'Discarded'].indexOf(a.status) === -1) throw new Error('status not allowed: ' + a.status);
    if (a.status === 'Approved' && !String(a.draft_body !== undefined ? a.draft_body : row.draft_body).trim()) throw new Error('cannot approve an empty draft');
    set_(drafts, row, 'status', a.status);
  }
  return { row: row._r, status: row.status };
}

function apiAddLead_(a) {
  const f = a.fields || {};
  const leads = read_('Leads');
  const lead = {};
  API_LEAD_FIELDS_.forEach(k => { if (f[k] !== undefined) lead[k] = f[k]; });
  if (!lead.brand && !lead.website) throw new Error('brand or website required');
  if (!lead.lead_id) {
    const base = String(lead.website ? cleanDomain_(lead.website).replace(/\.[a-z.]+$/, '') : lead.brand).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 30) || 'lead';
    let id = base, n = 2;
    while (leads.rows.some(l => String(l.lead_id) === id)) id = base + '-' + n++;
    lead.lead_id = id;
  } else if (leads.rows.some(l => String(l.lead_id) === String(lead.lead_id))) throw new Error('lead_id already exists');
  if (lead.website && leads.rows.some(l => l.website && cleanDomain_(l.website) === cleanDomain_(lead.website))) throw new Error('that website is already a lead');
  if (lead.email && leads.rows.some(l => String(l.email || '').trim().toLowerCase() === String(lead.email).trim().toLowerCase())) throw new Error('that email is already a lead');
  if (!lead.track) lead.track = lead.website ? 'Fix' : 'Build';
  if (lead.email && !lead.email_status) lead.email_status = 'unverified';
  Object.assign(lead, { stage: 'New', approved: false, touch_count: 0, created_at: new Date() });
  appendObj_('Leads', lead);
  return { lead_id: lead.lead_id };
}

function apiAddDomains_(a) {
  const list = (a.domains || []).map(cleanDomain_).filter(d => /^[a-z0-9][a-z0-9.-]*\.[a-z]{2,10}$/.test(d));
  const known = {};
  read_('Discovery').rows.forEach(r => { known[cleanDomain_(r.domain)] = true; });
  read_('Leads').rows.forEach(l => { if (l.website) known[cleanDomain_(l.website)] = true; });
  let added = 0;
  list.forEach(d => {
    if (known[d]) return;
    known[d] = true; added++;
    appendObj_('Discovery', { domain: d, source: a.source || 'koolestflow', niche: a.niche || '', country: a.country || '', status: 'New' });
  });
  return { received: list.length, added: added };
}

/**
 * Rich directory rows from the Mac scraper: { domain, source, country, niche, brand, contact_name, emails[], phone, signals, data }.
 * New domains are added to Discovery. A domain already in Discovery gets only its EMPTY fields filled and new emails merged in,
 * so nothing a person typed is overwritten. Domains already in Leads are ignored.
 */
function apiAddDiscoveryRows_(a) {
  const rows = (a.rows || []).slice(0, 300);
  const disc = read_('Discovery');
  const byDomain = {};
  disc.rows.forEach(r => { byDomain[cleanDomain_(r.domain)] = r; });
  const leadsTab = read_('Leads');
  const inLeads = {};
  leadsTab.rows.forEach(l => { if (l.website) inLeads[cleanDomain_(l.website)] = l; });
  let sigTab = null;
  try { sigTab = read_('Signals'); } catch (e) { /* run Outreach > Set up tabs to enable sightings */ }
  const sighted = {};
  if (sigTab) sigTab.rows.forEach(s => { if (lc_(s.kind) === 'also found on') sighted[cleanDomain_(s.domain) + '|' + srcKey_(s.source)] = true; });
  let added = 0, merged = 0, skipped = 0, sightings = 0;
  // A domain we already hold, found again by ANOTHER source: keep what that source knows (emails, contact, phone) and log it.
  const sighting = (d, x, emails, lead, discRow) => {
    if (!sigTab) return false;
    const key = d + '|' + srcKey_(x.source);
    if (sighted[key] || (discRow && srcKey_(discRow.source) === srcKey_(x.source)) || (lead && srcKey_(lead.source) === srcKey_(x.source))) return false;
    sighted[key] = true;
    const text = ['Also listed on ' + (x.source || 'another source'), x.brand, x.country, x.niche, emails.length ? 'emails: ' + emails.join(', ') : '', x.phone ? 'phone: ' + x.phone : '', x.signals, x.data]
      .filter(Boolean).join(' | ').slice(0, 900);
    appendObj_('Signals', { signal_id: 'sig-' + Utilities.getUuid().slice(0, 8), found_at: new Date(), domain: d, lead_id: lead ? lead.lead_id : (discRow && discRow.lead_id) || '',
      source: x.source || '', kind: 'Also found on', urgency: 'Normal', who: '', text: text, url: '', status: 'New' });
    if (lead) {
      if (x.contact_name && !String(lead.contact_name || '').trim()) set_(leadsTab, lead, 'contact_name', String(x.contact_name).slice(0, 120));
      if (emails.length && !String(lead.email || '').trim()) { set_(leadsTab, lead, 'email', emails[0]); set_(leadsTab, lead, 'email_status', 'unverified'); }
      const bits = [];
      emails.forEach(e => { if (lc_(lead.email) !== e && String(lead.notes || '').toLowerCase().indexOf(e) === -1) bits.push(e); });
      if (bits.length) set_(leadsTab, lead, 'notes', (String(lead.notes || '') + ' | also seen on ' + (x.source || '?') + ', other emails: ' + bits.join(', ') + (x.phone ? ', phone ' + x.phone : '')).slice(0, 900));
    }
    sightings++;
    return true;
  };
  rows.forEach(x => {
    const d = cleanDomain_(x.domain);
    if (!/^[a-z0-9][a-z0-9.-]*\.[a-z]{2,10}$/.test(d) || INFRA_DOMAINS_.test(d + '.')) { skipped++; return; }
    const emails = (x.emails || []).map(e => String(e).toLowerCase().trim()).filter(e => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e));
    if (inLeads[d]) { if (!sighting(d, x, emails, inLeads[d], null)) skipped++; return; }
    const have = byDomain[d];
    if (have) {
      let changed = sighting(d, x, emails, null, have);
      const mergedEmails = String(have.emails || '').split(/[|,;\s]+/).filter(Boolean);
      emails.forEach(e => { if (mergedEmails.indexOf(e) === -1) { mergedEmails.push(e); changed = true; } });
      if (changed) set_(disc, have, 'emails', mergedEmails.join(' | '));
      ['brand', 'contact_name', 'phone', 'signals', 'data', 'niche', 'country'].forEach(f => { if (x[f] && !String(have[f] || '').trim()) { set_(disc, have, f, String(x[f]).slice(0, 2000)); changed = true; } });
      if (changed) merged++; else skipped++;
      return;
    }
    appendObj_('Discovery', { domain: d, source: x.source || 'directory', niche: x.niche || '', country: x.country || '', track: x.track || '', status: 'New',
      brand: x.brand || '', contact_name: x.contact_name || '', emails: emails.join(' | '), phone: x.phone || '',
      signals: String(x.signals || '').slice(0, 2000), data: String(x.data || '').slice(0, 2000) });
    byDomain[d] = { domain: d };
    added++;
  });
  return { received: rows.length, added: added, merged: merged, skipped: skipped, sightings: sightings };
}



/**
 * Live signals from Reddit, Quora, job posts, anything public: { domain, source, kind, urgency, who, text, url }.
 * kind: Question | Hiring | Feedback request | Launch | Complaint | Mention. urgency "Hot" jumps the whole queue.
 * Nothing is dropped: the signal is logged in the Signals tab and attached to the lead, or to the Discovery row, or it
 * creates a new Discovery row. A lead not yet emailed that turns Hot gets its unsent sequence replaced by one written
 * around the signal (needs your approval again unless AUTO_APPROVE). A lead already emailed gets an alert only.
 */
function apiAddSignals_(a) {
  const rows = (a.rows || []).slice(0, 200);
  const S = settings_();
  const sigs = read_('Signals'), leads = read_('Leads'), disc = read_('Discovery'), seq = read_('Sequence');
  const seen = {};
  sigs.rows.forEach(s => { seen[cleanDomain_(s.domain) + '|' + String(s.url || s.text).slice(0, 200)] = true; });
  const leadBy = {}, discBy = {};
  leads.rows.forEach(l => { if (l.website) leadBy[cleanDomain_(l.website)] = l; });
  disc.rows.forEach(r => { if (r.domain) discBy[cleanDomain_(r.domain)] = r; });
  const out = { received: rows.length, logged: 0, duplicates: 0, hot: 0, attached_to_lead: 0, attached_to_discovery: 0, new_discovery: 0, already_contacted: 0, unmatched: 0 };
  const alerts = [];
  const now = new Date();
  const addNote = (l, msg) => set_(leads, l, 'notes', (msg + (l.notes ? ' | ' + l.notes : '')).slice(0, 900));

  rows.forEach(x => {
    const d = cleanDomain_(x.domain || '');
    const kind = ['Question', 'Hiring', 'Feedback request', 'Launch', 'Complaint', 'Mention'].indexOf(x.kind) !== -1 ? x.kind : 'Mention';
    const urgent = x.urgency ? lc_(x.urgency) === 'hot' : ['Question', 'Hiring', 'Feedback request'].indexOf(kind) !== -1;
    const text = String(x.text || '').slice(0, 1500);
    const key = d + '|' + String(x.url || text).slice(0, 200);
    if (seen[key]) { out.duplicates++; return; }
    seen[key] = true;
    const tag = '[' + kind + (x.source ? ', ' + x.source : '') + ']';
    const lead = d ? leadBy[d] : null;
    let leadId = lead ? lead.lead_id : '';

    if (lead) {
      const stage = String(lead.stage || 'New');
      const fresh = ['New', ''].indexOf(stage) !== -1 && Number(lead.touch_count || 0) === 0;
      if (urgent && fresh) {
        set_(leads, lead, 'priority', 'Hot');
        set_(leads, lead, 'signal_at', now);
        set_(leads, lead, 'prep_tries', 0);
        set_(leads, lead, 'prep_note', '');
        // The email already written does not know about this signal: replace what has not been sent.
        seq.rows.filter(r => String(r.lead_id) === String(lead.lead_id) && ['Sent', 'Stopped', 'Superseded'].indexOf(String(r.status)) === -1)
          .forEach(r => set_(seq, r, 'status', 'Superseded'));
        if (!isTrue_(S.AUTO_APPROVE)) set_(leads, lead, 'approved', false);
        out.hot++;
        alerts.push('HOT ' + tag + ' ' + (lead.brand || d) + ': ' + text.slice(0, 200) + (x.url ? ' ' + x.url : '') + ' (new email will be ready within about an hour, then tick approved)');
      } else if (!fresh && ['Contacted', 'Finished'].indexOf(stage) !== -1 && urgent) {
        out.already_contacted++;
        alerts.push('ALREADY EMAILED ' + tag + ' ' + (lead.brand || d) + ': ' + text.slice(0, 200) + (x.url ? ' ' + x.url : '') + ' (consider a personal reply)');
      }
      addNote(lead, tag + ' ' + text.slice(0, 200));
      out.attached_to_lead++;
    } else if (d) {
      const r = discBy[d];
      if (r) {
        set_(disc, r, 'signals', (tag + ' ' + text.slice(0, 300) + (r.signals ? ' || ' + r.signals : '')).slice(0, 2000));
        if (urgent) {
          set_(disc, r, 'priority', 'Hot');
          set_(disc, r, 'signal_at', now);
          if (['Skipped', 'Error'].indexOf(String(r.status)) !== -1 && !String(r.lead_id || '').trim()) { set_(disc, r, 'status', 'New'); set_(disc, r, 'reasons', 'reopened: hot signal'); }
          out.hot++;
          alerts.push('HOT ' + tag + ' ' + d + ': ' + text.slice(0, 200) + (x.url ? ' ' + x.url : ''));
        }
        leadId = r.lead_id || '';
        out.attached_to_discovery++;
      } else {
        appendObj_('Discovery', { domain: d, source: x.source || 'signal', status: 'New', priority: urgent ? 'Hot' : '', signal_at: urgent ? now : '',
          signals: (tag + ' ' + text).slice(0, 2000), data: x.url || '' });
        discBy[d] = { domain: d };
        out.new_discovery++;
        if (urgent) { out.hot++; alerts.push('HOT ' + tag + ' ' + d + ' (new store): ' + text.slice(0, 200) + (x.url ? ' ' + x.url : '')); }
      }
    } else {
      out.unmatched++;
      if (urgent) alerts.push('NO STORE LINK ' + tag + ' ' + (x.who || '') + ': ' + text.slice(0, 200) + (x.url ? ' ' + x.url : '') + ' (reply on the platform yourself)');
    }
    appendObj_('Signals', { signal_id: 'sig-' + Utilities.getUuid().slice(0, 8), found_at: now, domain: d, lead_id: leadId, source: x.source || '', kind: kind,
      urgency: urgent ? 'Hot' : 'Normal', who: String(x.who || '').slice(0, 120), text: text, url: x.url || '', status: 'New' });
    out.logged++;
  });
  if (alerts.length && S.ALERT_EMAIL) {
    try { MailApp.sendEmail(S.ALERT_EMAIL, 'Hot signals: ' + alerts.length + ' to look at', alerts.join('\n\n')); } catch (e) { /* mail quota */ }
  }
  return out;
}

function srcKey_(v) { return lc_(String(v || '').split(/\s+/)[0]); }

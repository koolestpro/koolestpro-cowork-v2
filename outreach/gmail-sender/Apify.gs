/**
 * Koolestpro Outreach: Apify connector (optional, paid per result).
 *
 * Apify hosts ready-made "actors" (scrapers and data sources), for example Store Leads based store finders that return
 * estimated sales, employee count, apps and emails. This lets you run one from the Sheet and pull its results into the
 * Discovery tab, where the normal scoring takes over.
 *
 * Nothing runs until you set a row's status to Ready, so nothing is spent by accident. max_items caps the cost of a run
 * (Apify does not charge past the limit on pay-per-result actors; check the actor's own pricing first).
 *
 * Setup: Apify Console > Settings > Integrations > API token, then Apps Script > Project Settings > Script properties:
 * APIFY_TOKEN = the token. In the Apify tab add a row: actor (e.g. username/actor-name, copied from the actor's page),
 * input_json (paste the actor's own Input JSON from its Input tab, edited to your filters), max_items (start with 50),
 * status = Ready. Then Outreach > Run Apify imports now (or wait for the 30 minute run).
 */

function apifyCall_(method, path, payload) {
  const token = PropertiesService.getScriptProperties().getProperty('APIFY_TOKEN');
  if (!token) throw new Error('no APIFY_TOKEN Script property');
  const opts = { method: method, headers: { Authorization: 'Bearer ' + token }, muteHttpExceptions: true };
  if (payload !== undefined) { opts.contentType = 'application/json'; opts.payload = JSON.stringify(payload); }
  const res = UrlFetchApp.fetch('https://api.apify.com/v2' + path, opts);
  const code = res.getResponseCode(), body = res.getContentText();
  if (code < 200 || code >= 300) throw new Error('Apify HTTP ' + code + ' ' + body.replace(/\s+/g, ' ').slice(0, 160));
  return JSON.parse(body);
}

function apifyImportsNow() {
  const stats = { problems: [] };
  apifyImports_(stats, () => true);
  toast_('Apify: ' + (stats.apify || 0) + ' new store(s) imported.' + (stats.problems.length ? ' ' + stats.problems.join(' | ') : ' See the result column in the Apify tab.'));
}

/** Starts Ready rows, checks Running rows, imports finished ones. */
function apifyImports_(stats, timeLeft) {
  const tab = read_('Apify');
  tab.rows.filter(r => String(r.actor).trim()).forEach(r => {
    if (!timeLeft()) return;
    const st = lc_(r.status);
    try {
      if (st === 'ready') {
        const input = r.input_json ? JSON.parse(String(r.input_json)) : {};
        const max = Math.max(1, Math.min(500, Number(r.max_items) || 50));
        const run = apifyCall_('post', '/acts/' + encodeURIComponent(String(r.actor).trim().replace('/', '~')) + '/runs?maxItems=' + max, input).data;
        set_(tab, r, 'run_id', run.id);
        set_(tab, r, 'started_at', new Date());
        set_(tab, r, 'status', 'Running');
        set_(tab, r, 'result', 'started, waiting for Apify');
      } else if (st === 'running' && r.run_id) {
        const run = apifyCall_('get', '/actor-runs/' + encodeURIComponent(String(r.run_id))).data;
        if (run.status === 'SUCCEEDED') {
          const max = Math.max(1, Math.min(500, Number(r.max_items) || 50));
          const items = apifyCall_('get', '/datasets/' + encodeURIComponent(run.defaultDatasetId) + '/items?clean=true&limit=' + max);
          const added = importApifyItems_(r, Array.isArray(items) ? items : (items.items || []));
          set_(tab, r, 'items', (Array.isArray(items) ? items : []).length);
          set_(tab, r, 'new', added);
          set_(tab, r, 'status', 'Done');
          set_(tab, r, 'result', added + ' new stores added to Discovery. Raw fields are in the Discovery data column.');
          stats.apify = (stats.apify || 0) + added;
        } else if (['FAILED', 'ABORTED', 'TIMED-OUT'].indexOf(run.status) !== -1) {
          set_(tab, r, 'status', 'Error');
          set_(tab, r, 'result', 'Apify run ' + run.status);
        } else {
          set_(tab, r, 'result', 'Apify says ' + run.status);
        }
      }
    } catch (e) {
      set_(tab, r, 'status', 'Error');
      set_(tab, r, 'result', String(e.message || e).slice(0, 300));
      stats.problems.push(String(e.message || e).slice(0, 120));
    }
  });
}

/** Finds the domain and any useful numbers in an actor's item, whatever the actor calls them. */
function importApifyItems_(row, items) {
  const disc = read_('Discovery'), leads = read_('Leads');
  const known = {};
  disc.rows.forEach(r => { known[cleanDomain_(r.domain)] = true; });
  leads.rows.forEach(l => { if (l.website) known[cleanDomain_(l.website)] = true; });
  const flat = (o, prefix, out) => {
    Object.keys(o || {}).forEach(k => {
      const v = o[k], key = (prefix ? prefix + '.' : '') + k;
      if (v && typeof v === 'object' && !Array.isArray(v)) flat(v, key, out); else out[key] = v;
    });
    return out;
  };
  const find = (f, re) => Object.keys(f).find(k => re.test(k) && f[k] !== null && f[k] !== '' && f[k] !== undefined);
  let added = 0;
  items.forEach(item => {
    const f = flat(item, '', {});
    const dk = find(f, /(^|\.)(domain|website|storeurl|store_url|shopurl|url|link)$/i);
    const domain = dk ? cleanDomain_(String(f[dk])) : '';
    if (!domain || known[domain] || !/\./.test(domain)) return;
    const sk = find(f, /sales|revenue/i), ek = find(f, /employee/i), ck = find(f, /(^|\.)(country|countrycode|country_code)$/i), nk = find(f, /categor|niche|vertical/i);
    const signals = [sk ? sk + ': ' + f[sk] : '', ek ? ek + ': ' + f[ek] : ''].filter(String).join('; ');
    known[domain] = true; added++;
    appendObj_('Discovery', { domain: domain, source: 'apify:' + row.actor, niche: nk ? String(f[nk]).slice(0, 40) : '', country: ck ? (CODE_COUNTRY_[String(f[ck]).toUpperCase()] || String(f[ck])) : '',
      status: 'New', signals: signals, data: JSON.stringify(item).slice(0, 1500) });
  });
  return added;
}

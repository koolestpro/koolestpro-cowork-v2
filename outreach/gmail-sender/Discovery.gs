/**
 * Koolestpro Outreach: store discovery and qualification (README step 5).
 *
 * Any source (a pasted list, a CSV export from a store-finder tool, a scraper) drops domains into the
 * Discovery tab with status "New". Every 30 minutes (or Outreach > Prepare new leads now) this checks each
 * store from its own public pages and keeps only the UPCOMING ones: small to mid catalogue, young store,
 * default or free theme, not a heavy app stack, in a target market. Stores that pass become rows in Leads
 * (and then the normal pipeline takes over: email, verify, profile, 5 emails). Stores that do not pass are
 * marked Skipped with the reasons, so nothing is checked twice.
 *
 * Everything is a free signal read from the store's own site. It cannot know revenue. The score is a
 * proxy for "small and growing", and every point is listed in the reasons column so you can judge it.
 */

const DISCOVERY_BATCH_ = 8;

const FREE_THEMES_ = ['dawn', 'refresh', 'craft', 'sense', 'taste', 'ride', 'crave', 'studio', 'origin', 'publisher', 'colorblock',
  'spotlight', 'horizon', 'debut', 'brooklyn', 'minimal', 'venture', 'simple', 'narrative', 'supply', 'boundless', 'express', 'pop',
  'district', 'fashionista', 'mobilia', 'jumpstart', 'impulse', 'empire', 'symmetry'];

const APP_MARKERS_ = ['klaviyo', 'yotpo', 'gorgias', 'recharge', 'judge.me', 'loox', 'stamped.io', 'okendo', 'privy', 'attentive', 'postscript',
  'smile.io', 'swym', 'afterpay', 'klarna', 'triplewhale', 'northbeam', 'tapcart', 'nosto', 'bazaarvoice', 'zendesk', 'intercom', 'hotjar', 'segment.com', 'optimizely'];

const CODE_COUNTRY_ = { NG: 'Nigeria', GH: 'Ghana', KE: 'Kenya', ZA: 'South Africa', GB: 'United Kingdom', US: 'United States', CA: 'Canada',
  IE: 'Ireland', DE: 'Germany', FR: 'France', NL: 'Netherlands', ES: 'Spain', IT: 'Italy', SE: 'Sweden', NO: 'Norway', DK: 'Denmark',
  FI: 'Finland', BE: 'Belgium', AT: 'Austria', CH: 'Switzerland', PT: 'Portugal', PL: 'Poland' };
const CURRENCY_COUNTRY_ = { NGN: 'Nigeria', GHS: 'Ghana', KES: 'Kenya', GBP: 'United Kingdom', USD: 'United States', CAD: 'Canada', EUR: 'Europe' };
const TLD_COUNTRY_ = { 'co.uk': 'United Kingdom', uk: 'United Kingdom', ng: 'Nigeria', 'com.ng': 'Nigeria', gh: 'Ghana', ke: 'Kenya', ca: 'Canada',
  de: 'Germany', fr: 'France', nl: 'Netherlands', es: 'Spain', it: 'Italy', se: 'Sweden', ie: 'Ireland', dk: 'Denmark', no: 'Norway' };

function cleanDomain_(d) {
  return String(d || '').trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/[\/?#].*$/, '');
}

function qualifyDiscovery_(S, stats, timeLeft) {
  const disc = read_('Discovery');
  const leads = read_('Leads');
  const have = {};
  leads.rows.forEach(l => { if (l.website) have[cleanDomain_(l.website)] = true; });
  const min = Number(S.MIN_FIT_SCORE || 55);

  disc.rows.filter(r => cleanDomain_(r.domain) && ['', 'New'].indexOf(String(r.status)) !== -1).slice(0, DISCOVERY_BATCH_).forEach(r => {
    if (!timeLeft()) return;
    const domain = cleanDomain_(r.domain);
    try {
      if (have[domain]) { set_(disc, r, 'status', 'Skipped'); set_(disc, r, 'reasons', 'already in Leads'); set_(disc, r, 'checked_at', new Date()); return; }
      const v = scoreStore_(domain, r);
      set_(disc, r, 'score', v.score);
      set_(disc, r, 'reasons', v.reasons.join('; '));
      set_(disc, r, 'checked_at', new Date());
      if (v.skip) { set_(disc, r, 'status', 'Skipped'); return; }
      if (v.score < min) { set_(disc, r, 'status', 'Skipped'); set_(disc, r, 'reasons', 'score ' + v.score + ' below ' + min + ': ' + v.reasons.join('; ')); return; }
      const id = domain.replace(/\.[a-z.]+$/, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 30) || domain;
      let leadId = id, n = 2;
      while (leads.rows.some(l => String(l.lead_id) === leadId)) leadId = id + '-' + n++;
      appendObj_('Leads', { lead_id: leadId, brand: v.brand || id, website: domain, contact_name: '', email: '', email_status: '', country: v.country,
        time_zone: '', niche: r.niche || '', source: r.source || 'discovery', track: 'Fix', play: '', stage: 'New', approved: false, touch_count: 0,
        notes: 'Fit ' + v.score + ': ' + v.reasons.join('; '), created_at: new Date() });
      leads.rows.push({ lead_id: leadId, website: domain });
      have[domain] = true;
      set_(disc, r, 'status', 'Promoted');
      set_(disc, r, 'lead_id', leadId);
      stats.discovered = (stats.discovered || 0) + 1;
    } catch (e) {
      set_(disc, r, 'status', 'Error');
      set_(disc, r, 'reasons', String(e.message || e).slice(0, 200));
      set_(disc, r, 'checked_at', new Date());
    }
  });
}

/** Reads a store's public pages and returns { score, reasons[], country, brand, skip }. */
function scoreStore_(domain, row) {
  const reasons = [];
  let score = 40;
  const page = fetchPage_(domain);
  if (!page.ok) return { score: 0, reasons: ['site unreachable (HTTP ' + page.code + ')'], skip: true };
  const html = page.html;

  const isShopify = /cdn\.shopify\.com|Shopify\.theme|myshopify\.com/i.test(html);
  if (!isShopify) return { score: 0, reasons: ['not a Shopify store'], skip: true };
  reasons.push('Shopify');

  // Market
  const code = (html.match(/Shopify\.country\s*=\s*"([A-Z]{2})"/) || [])[1];
  const cur = (html.match(/Shopify\.currency\s*=\s*\{\s*"active"\s*:\s*"([A-Z]{3})"/) || [])[1];
  const tld = /\.co\.uk$|\.com\.ng$/.test(domain) ? domain.match(/(co\.uk|com\.ng)$/)[1] : domain.split('.').pop();
  const country = String(row.country || '').trim() || CODE_COUNTRY_[code] || CURRENCY_COUNTRY_[cur] || TLD_COUNTRY_[tld] || '';
  if (!country) return { score: 0, reasons: ['outside the target markets or country unknown (country ' + (code || '?') + ', currency ' + (cur || '?') + ')'], skip: true };
  reasons.push('market ' + country);

  // Catalogue size and store age from the public products feed (many stores leave it on)
  try {
    const res = UrlFetchApp.fetch('https://' + domain + '/products.json?limit=250', { muteHttpExceptions: true, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } });
    if (res.getResponseCode() === 200) {
      const prods = (JSON.parse(res.getContentText()).products || []);
      const n = prods.length;
      if (n >= 250) { score -= 30; reasons.push('250+ products (large catalogue: -30)'); }
      else if (n >= 151) { reasons.push(n + ' products (big)'); }
      else if (n >= 3) { score += 20; reasons.push(n + ' products (+20)'); }
      else { score -= 10; reasons.push('only ' + n + ' products (-10)'); }
      const dates = prods.map(p => Date.parse(p.created_at || p.published_at)).filter(x => x);
      if (dates.length) {
        const years = (Date.now() - Math.min.apply(null, dates)) / 31557600000;
        if (years < 4) { score += 10; reasons.push('newest-era store, oldest product ' + years.toFixed(1) + 'y (+10)'); }
        else if (years > 8) { score -= 10; reasons.push('old store, oldest product ' + years.toFixed(1) + 'y (-10)'); }
      }
    } else { reasons.push('product feed not public'); }
  } catch (e) { reasons.push('product feed unreadable'); }

  // Theme: a default or free theme suggests nobody has designed this store yet
  const theme = (html.match(/Shopify\.theme\s*=\s*\{[^}]*"name"\s*:\s*"([^"]+)"/) || [])[1] || '';
  if (theme) {
    if (FREE_THEMES_.indexOf(theme.toLowerCase()) !== -1) { score += 15; reasons.push('theme ' + theme + ' (free/default: +15)'); }
    else reasons.push('theme ' + theme);
  }

  // Big-brand tells: heavy app stack, many language versions
  const lower = html.toLowerCase();
  const apps = APP_MARKERS_.filter(a => lower.indexOf(a) !== -1);
  if (apps.length >= 9) { score -= 30; reasons.push(apps.length + ' marketing/support apps (established: -30)'); }
  else if (apps.length >= 6) { score -= 15; reasons.push(apps.length + ' apps (-15)'); }
  else if (apps.length >= 1) { score += 5; reasons.push('some tooling: ' + apps.slice(0, 3).join(', ') + ' (+5)'); }
  const hreflang = (html.match(/hreflang=/g) || []).length;
  if (hreflang > 5) { score -= 15; reasons.push(hreflang + ' language versions (international brand: -15)'); }

  // Weak build signals that a designer could fix
  if (!/<meta[^>]+name=["']viewport["']/i.test(html)) { score += 5; reasons.push('no mobile viewport tag (+5)'); }
  if (page.seconds > 3) { score += 5; reasons.push('slow first load ' + page.seconds.toFixed(1) + 's (+5)'); }

  const title = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '';
  const brand = title.replace(/\s+/g, ' ').split(/[|–\-:]/)[0].trim().slice(0, 40);
  return { score: Math.max(0, Math.min(100, score)), reasons: reasons, country: country, brand: brand, skip: false };
}


// ---------- Importing store lists from any public page ----------
// The Sources tab holds list pages (a directory, a "new Shopify stores" page, a CSV link). Each active source is
// read at most once every 20 hours; every store domain found that is not already known goes into Discovery.
// Works on public pages only. A page behind a login, or one that builds its list with JavaScript, finds 0
// domains: the result column says so. Some sites forbid scraping in their terms: where a site offers an
// export or API, prefer that and paste the domains into Discovery yourself.

const SKIP_LABELS_ = ['facebook', 'fb', 'instagram', 'twitter', 'x', 'linkedin', 'youtube', 'youtu', 'tiktok', 'pinterest', 'google', 'googleapis',
  'gstatic', 'googletagmanager', 'google-analytics', 'cloudflare', 'cloudfront', 'amazonaws', 'shopify', 'shopifycdn', 'wikipedia', 'apple', 'amazon',
  'github', 'w3', 'schema', 'jsdelivr', 'unpkg', 'cdnjs', 'bootstrapcdn', 'jquery', 'wordpress', 'gravatar', 'mailchimp', 'hubspot', 'stripe',
  'paypal', 'klaviyo', 'trustpilot', 'reddit', 'medium', 'bit', 'goo', 'whatsapp', 'wa', 'snapchat', 'tumblr', 'vimeo', 'calendly', 'zoom',
  'notion', 'canva', 'typeform', 'fontawesome', 'fonts', 'ajax', 'sentry', 'wixpress', 'gmpg', 'creativecommons', 'mozilla', 'microsoft', 'bing',
  'yahoo', 'outlook', 'live', 'adobe', 'cloudinary', 'imgur', 'giphy', 'discord', 'telegram', 'producthunt', 'crunchbase', 'builtwith'];

function extractDomains_(html, ownHost) {
  const found = {};
  const own = String(ownHost || '').split('.').filter(l => l.length > 3);
  const add = raw => {
    let d = cleanDomain_(raw);
    if (!/^[a-z0-9][a-z0-9.-]*\.[a-z]{2,10}$/.test(d)) return;
    if (/\.(png|jpe?g|gif|svg|webp|json|xml|pdf|woff2?|css|js|ico|mp4)$/.test(d)) return;
    const labels = d.split('.');
    if (labels.some(l => SKIP_LABELS_.indexOf(l) !== -1)) return;
    if (own.some(o => labels.indexOf(o) !== -1)) return;
    found[d] = true;
  };
  (html.match(/href=["']https?:\/\/[^"'\/?#]+/gi) || []).forEach(m => add(m.replace(/^href=["']https?:\/\//i, '')));
  (html.match(/\b[a-z0-9][a-z0-9-]{1,61}\.(?:com|co\.uk|co|net|org|shop|store|io|ng|com\.ng|uk|ca|de|fr|nl|es|it|se|ie|dk|no|fi|be|at|ch|pt|pl|eu|ke|gh|co\.za|us|life|online|site|studio|co\.ke|app|xyz)\b/gi) || []).forEach(add);
  return Object.keys(found);
}

function importSources_(S, stats, timeLeft, force) {
  const src = read_('Sources');
  if (!src.rows.length) return;
  const disc = read_('Discovery'), leads = read_('Leads');
  const known = {};
  disc.rows.forEach(r => { known[cleanDomain_(r.domain)] = true; });
  leads.rows.forEach(l => { if (l.website) known[cleanDomain_(l.website)] = true; });
  let budget = 60;   // new domains per run

  src.rows.filter(r => String(r.url).trim() && lc_(r.status) !== 'paused').forEach(r => {
    if (!timeLeft() || budget <= 0) return;
    if (!force && r.last_run && Date.now() - new Date(r.last_run).getTime() < 20 * 3600 * 1000) return;
    let total = 0, added = 0, problem = '';
    const pages = Math.max(1, Math.min(10, Number(r.max_pages) || 1));
    const ownHost = cleanDomain_(r.url);
    for (let p = 1; p <= pages && budget > 0; p++) {
      const url = String(r.url).trim().replace('{page}', p);
      try {
        const page = fetchPage_(url);
        if (!page.ok) { problem = 'HTTP ' + page.code + (page.code === 403 ? ' (site blocks automated readers)' : ''); break; }
        const doms = extractDomains_(page.html, ownHost);
        total += doms.length;
        doms.forEach(d => {
          if (known[d] || budget <= 0) return;
          known[d] = true; budget--; added++;
          appendObj_('Discovery', { domain: d, source: r.source || ownHost, niche: r.niche || '', country: r.country || '', status: 'New' });
        });
        if (!doms.length) break;
      } catch (e) { problem = String(e.message || e).slice(0, 100); break; }
    }
    set_(src, r, 'last_run', new Date());
    set_(src, r, 'found', total);
    set_(src, r, 'new', added);
    set_(src, r, 'result', problem || (total === 0 ? '0 domains found: the list may need a login or be built with JavaScript. Use its export instead.' : added + ' new of ' + total));
    stats.imported = (stats.imported || 0) + added;
  });
}

function importSourcesNow() {
  const stats = { problems: [] };
  importSources_(settings_(), stats, () => true, true);
  toast_('Imported ' + (stats.imported || 0) + ' new store domains into Discovery. See the result column in Sources.');
}

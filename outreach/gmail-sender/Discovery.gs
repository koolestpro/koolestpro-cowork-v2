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

// Hosts that are infrastructure, not stores. Never worth a check.
const INFRA_DOMAINS_ = /(^|\.)(googlesyndication|googleusercontent|googletagmanager|google-analytics|cloudflareinsights|cloudflare|json-schema|schema|shopifysvc|shopifycdn|shopify|myshopify|bootleads|wixpress|sentry|gstatic|googleapis|facebook|instagram|twitter|linkedin|youtube|tiktok|w3|jsdelivr|unpkg|cdnjs|gravatar|doubleclick)\./i;

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
      if (INFRA_DOMAINS_.test(domain + '.')) { set_(disc, r, 'status', 'Skipped'); set_(disc, r, 'reasons', 'not a store (infrastructure or platform domain)'); set_(disc, r, 'checked_at', new Date()); return; }
      if (have[domain]) { set_(disc, r, 'status', 'Skipped'); set_(disc, r, 'reasons', 'already in Leads'); set_(disc, r, 'checked_at', new Date()); return; }
      const emp = Number((String(r.signals).match(/employee[^:]*:\s*(\d+)/i) || [])[1]);
      if (emp > 30) { set_(disc, r, 'status', 'Skipped'); set_(disc, r, 'reasons', 'team of ' + emp + ' (too large)'); set_(disc, r, 'checked_at', new Date()); return; }
      const isPartner = lc_(r.track) === 'partner';
      const v = isPartner ? scoreAgency_(domain, r) : scoreStore_(domain, r);
      set_(disc, r, 'score', v.score);
      set_(disc, r, 'reasons', v.reasons.join('; '));
      set_(disc, r, 'checked_at', new Date());
      if (v.skip) { set_(disc, r, 'status', 'Skipped'); return; }
      const need = isPartner ? Number(S.MIN_PARTNER_SCORE || 55) : min;
      if (v.score < need) { set_(disc, r, 'status', 'Skipped'); set_(disc, r, 'reasons', 'score ' + v.score + ' below ' + need + ': ' + v.reasons.join('; ')); return; }
      const id = domain.replace(/\.[a-z.]+$/, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 30) || domain;
      let leadId = id, n = 2;
      while (leads.rows.some(l => String(l.lead_id) === leadId)) leadId = id + '-' + n++;
      // Everything the directory showed us rides along: name, contact, emails, phone. With more than one email, keep the best.
      const pick = pickBestEmail_(r.emails, domain, r.contact_name);
      const extra = [];
      if (pick.others.length) extra.push('other emails: ' + pick.others.join(', '));
      if (r.phone) extra.push('phone: ' + r.phone);
      appendObj_('Leads', { lead_id: leadId, brand: v.brand || r.brand || id, website: domain, contact_name: r.contact_name || '', email: pick.best, email_status: pick.best ? 'unverified' : '', country: v.country || r.country,
        time_zone: '', niche: r.niche || '', source: r.source || 'discovery', platform: v.platform, business_model: v.model, track: isPartner ? 'Partner' : 'Fix', play: isPartner ? 'agency_partner' : '', stage: 'New', approved: false, touch_count: 0,
        notes: 'Fit ' + v.score + ': ' + v.reasons.join('; ') + (pick.best ? '; email from directory (' + (r.source || '') + ')' : '') + (extra.length ? '; ' + extra.join('; ') : ''), created_at: new Date() });
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

// Platform fingerprints for non-Shopify stores. Ridwan builds in Shopify, so these leads are pitched a CRO review
// of their current site or a move to Shopify.
const PLATFORMS_ = [
  ['WooCommerce', /woocommerce|wc-ajax|wp-content\/plugins\/woocommerce/i],
  ['BigCommerce', /cdn\d*\.bigcommerce\.com|bigcommerce/i],
  ['Wix', /wixstatic\.com|wix-ecommerce|wixstores|_wixCIDX/i],
  ['Squarespace', /squarespace\.com|static1\.squarespace|sqs-add-to-cart/i],
  ['Magento', /Mage\.Cookies|mage\/cookies|magento/i],
  ['PrestaShop', /prestashop/i],
  ['Ecwid', /ecwid/i],
  ['Webflow', /webflow\.com|data-wf-site/i],
];
const DROPSHIP_APPS_ = ['dsers', 'oberlo', 'spocket', 'zendrop', 'cjdropshipping', 'autods', 'dropified', 'modalyst', 'syncee', 'aliexpress', 'alicdn', 'ae01.alicdn'];
const POD_APPS_ = ['printful', 'printify', 'gelato', 'gooten'];

/**
 * Reads a store's public pages and returns { score, reasons[], country, brand, platform, model, skip }.
 * The full rubric, with the reason for every point, is in outreach/SCORING.md. Keep the two in step.
 */
function scoreStore_(domain, row) {
  const reasons = [];
  let score = 40;
  const page = fetchPage_(domain);
  if (!page.ok) return { score: 0, reasons: ['site unreachable (HTTP ' + page.code + ')'], skip: true };
  const html = page.html, lower = html.toLowerCase();

  // 1. Is it an online store, and on what?
  let platform = '';
  const isShopify = /cdn\.shopify\.com|Shopify\.theme|myshopify\.com/i.test(html);
  if (isShopify) platform = 'Shopify';
  else {
    const hit = PLATFORMS_.find(p => p[1].test(html));
    const looksLikeStore = /add[\s_-]?to[\s_-]?cart|addtocart|"@type"\s*:\s*"Product"|\/cart\b|woocommerce/i.test(html);
    if (hit && looksLikeStore) platform = hit[0];
    else if (looksLikeStore) platform = 'Other';
  }
  if (!platform) return { score: 0, reasons: ['not an online store'], skip: true };
  reasons.push(platform);

  // 2. Market
  const code = (html.match(/Shopify\.country\s*=\s*"([A-Z]{2})"/) || [])[1];
  const cur = (html.match(/Shopify\.currency\s*=\s*\{\s*"active"\s*:\s*"([A-Z]{3})"/) || [])[1] || (html.match(/"priceCurrency"\s*:\s*"([A-Z]{3})"/) || [])[1];
  const tld = /\.co\.uk$|\.com\.ng$/.test(domain) ? domain.match(/(co\.uk|com\.ng)$/)[1] : domain.split('.').pop();
  const country = String(row.country || '').trim() || CODE_COUNTRY_[code] || CURRENCY_COUNTRY_[cur] || TLD_COUNTRY_[tld] || '';
  if (!country) return { score: 0, reasons: ['outside the target markets or country unknown (country ' + (code || '?') + ', currency ' + (cur || '?') + ')'], skip: true };
  reasons.push('market ' + country);

  // 3. Catalogue size, store age and vendors: Shopify products feed, WooCommerce store API
  let nProducts = -1, vendors = {}, prods = [];
  try {
    if (platform === 'Shopify') {
      const res = UrlFetchApp.fetch('https://' + domain + '/products.json?limit=250', { muteHttpExceptions: true, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } });
      if (res.getResponseCode() === 200) { prods = JSON.parse(res.getContentText()).products || []; nProducts = prods.length; }
      else reasons.push('product feed not public');
    } else if (platform === 'WooCommerce') {
      const res = UrlFetchApp.fetch('https://' + domain + '/wp-json/wc/store/v1/products?per_page=1', { muteHttpExceptions: true });
      if (res.getResponseCode() === 200) { const h = res.getAllHeaders(); nProducts = Number(h['x-wp-total'] || h['X-WP-Total'] || -1); }
    }
  } catch (e) { reasons.push('product feed unreadable'); }
  if (nProducts >= 0) {
    if (nProducts >= 250) { score -= 10; reasons.push('250+ products (-10)'); }
    else if (nProducts >= 61) { score += 15; reasons.push(nProducts + ' products (+15)'); }
    else if (nProducts >= 4) { score += 20; reasons.push(nProducts + ' products (+20)'); }
    else if (nProducts >= 1) { score += 10; reasons.push(nProducts + ' product(s): focused single-product brand (+10)'); }
    else { score -= 15; reasons.push('empty catalogue (-15)'); }
  }
  const dates = prods.map(p => Date.parse(p.created_at || p.published_at)).filter(x => x);
  if (dates.length) {
    const years = (Date.now() - Math.min.apply(null, dates)) / 31557600000;
    if (years < 1) { score += 15; reasons.push('very new store, ' + years.toFixed(1) + 'y (+15)'); }
    else if (years < 3) { score += 10; reasons.push('young store, ' + years.toFixed(1) + 'y (+10)'); }
    else if (years > 6) { score -= 10; reasons.push('established store, ' + years.toFixed(1) + 'y (-10)'); }
    else reasons.push('store age ' + years.toFixed(1) + 'y');
  }

  // 4. Pre-launch: a store behind a password page is being built right now
  if (platform === 'Shopify' && /Opening soon|<form[^>]+storefront_password|password-page|\/password/i.test(html) && nProducts <= 0) { score += 15; reasons.push('password or opening-soon page: building now (+15)'); }

  // 5. Theme
  const theme = (html.match(/Shopify\.theme\s*=\s*\{[^}]*"name"\s*:\s*"([^"]+)"/) || [])[1] || '';
  if (theme) {
    if (FREE_THEMES_.indexOf(theme.toLowerCase()) !== -1) { score += 10; reasons.push('theme ' + theme + ' (free/default: +10)'); }
    else reasons.push('theme ' + theme);
  }

  // 6. Size tells: app stack, language versions
  const apps = APP_MARKERS_.filter(a => lower.indexOf(a) !== -1);
  if (apps.length >= 9) { score -= 20; reasons.push(apps.length + ' marketing/support apps (established: -20)'); }
  else if (apps.length >= 6) { score -= 10; reasons.push(apps.length + ' apps (-10)'); }
  else if (apps.length <= 2) { score += 5; reasons.push('light app stack (+5)'); }
  const hreflang = (html.match(/hreflang=/g) || []).length;
  if (hreflang > 5) { score -= 15; reasons.push(hreflang + ' language versions (international brand: -15)'); }

  // 7. Visible weaknesses a designer can fix
  if (!/<meta[^>]+name=["']viewport["']/i.test(html)) { score += 10; reasons.push('no mobile viewport tag (+10)'); }
  if (page.seconds > 3) { score += 5; reasons.push('slow first load ' + page.seconds.toFixed(1) + 's (+5)'); }
  if (!/refund|return(s)?[\s-]?policy|shipping[\s-]?policy/i.test(lower)) { score += 5; reasons.push('no returns or shipping policy link seen (+5)'); }

  // 8. Business model: own brand, dropshipping, print on demand, or reseller. Changes the pitch, not the score.
  let ds = DROPSHIP_APPS_.filter(a => lower.indexOf(a) !== -1).length;
  if (/ships?\s+from\s+(china|overseas|abroad)|(7|10|12|14|15|20|21)\s*(-|to)\s*(1[0-9]|2[0-9]|30|45)\s*(business\s*)?days/i.test(lower)) ds++;
  const pod = POD_APPS_.filter(a => lower.indexOf(a) !== -1).length > 0;
  prods.forEach(p => { if (p.vendor) vendors[String(p.vendor).toLowerCase()] = (vendors[String(p.vendor).toLowerCase()] || 0) + 1; });
  const nVendors = Object.keys(vendors).length;
  const title = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '';
  const brand = title.replace(/\s+/g, ' ').split(/[|–\-:]/)[0].trim().slice(0, 40);
  const brandKey = (domain.split('.')[0] || '').replace(/[^a-z0-9]/g, '');
  let model = 'unknown';
  if (ds >= 2) model = 'dropship-likely';
  else if (pod) model = 'print-on-demand';
  else if (nVendors >= 8) model = 'reseller';
  else if (nVendors >= 1 && Object.keys(vendors).some(v => v.replace(/[^a-z0-9]/g, '').indexOf(brandKey) !== -1 || brandKey.indexOf(v.replace(/[^a-z0-9]/g, '')) !== -1)) model = 'own-brand';
  else if (ds === 0 && nVendors === 1) model = 'own-brand';
  reasons.push('model: ' + model + (ds ? ' (' + ds + ' dropship signal' + (ds > 1 ? 's' : '') + ')' : ''));

  return { score: Math.max(0, Math.min(100, score)), reasons: reasons, country: country, brand: brand, platform: platform, model: model, skip: false };
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
  'yahoo', 'outlook', 'live', 'adobe', 'cloudinary', 'imgur', 'giphy', 'discord', 'telegram', 'producthunt', 'crunchbase', 'builtwith',
  'clutch', 'ampproject', 'googlesyndication', 'googleusercontent', 'cloudflareinsights', 'json-schema', 'shopifysvc', 'doubleclick', 'gtm', 'jsdelivr',
  'myshopify', 'wixstatic', 'squarespace', 'bigcommerce', 'wpengine', 'wordpress', 'woocommerce', 'webflow', 'vercel', 'netlify', 'herokuapp', 'bootstrap'];

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

  // Directories that block Google's servers are read by the Mac scraper (outreach/scrapers), not here.
  const MAC_HOSTS_ = /merchantgenius\.io|zikanalytics\.com|eachspy\.com|techpeeker\.com|cro\.media|builtwith\.com|sellerdirectories\.com|myip\.ms/i;
  src.rows.filter(r => String(r.url).trim() && lc_(r.status) !== 'paused').forEach(r => {
    if (MAC_HOSTS_.test(String(r.url))) { if (!r.result || String(r.result).indexOf('Mac scraper') === -1) set_(src, r, 'result', 'handled by the Mac scraper (outreach/scrapers), skipped here'); return; }
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
          appendObj_('Discovery', { domain: d, source: r.source || ownHost, niche: r.niche || '', country: r.country || '', track: r.track || '', status: 'New' });
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


// ---------- Agencies (the Partner track) ----------
// An agency is not scored like a store. The question is: would this studio plausibly want overflow Shopify development?
// Good: sells design, branding or ads for e-commerce brands but shows little or no development of its own, small team.
// Bad: already a development shop, large team, enterprise focus. See outreach/SCORING.md section 7.
function scoreAgency_(domain, row) {
  const reasons = [];
  let score = 40;
  const page = fetchPage_(domain);
  if (!page.ok) return { score: 0, reasons: ['site unreachable (HTTP ' + page.code + ')'], skip: true };
  let text = page.html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').toLowerCase();
  for (const path of ['/services', '/about', '/about-us']) {   // one more page of context, if it exists
    try { const p = fetchPage_(domain + path); if (p.ok) { text += ' ' + p.html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').toLowerCase().slice(0, 6000); break; } } catch (e) { /* skip */ }
  }
  text = text.slice(0, 20000);
  const has = re => (text.match(re) || []).length;

  if (!has(/\b(agency|studio|consultanc|we design|we build|our services|our work|case stud)/g)) return { score: 0, reasons: ['does not look like an agency or studio'], skip: true };
  const ecom = has(/\b(shopify|e-?commerce|dtc|d2c|online store|woocommerce|webflow)\b/g);
  if (!ecom) return { score: 0, reasons: ['no e-commerce focus seen'], skip: true };
  score += ecom >= 5 ? 20 : 10; reasons.push('e-commerce focus (' + ecom + ' mentions: +' + (ecom >= 5 ? 20 : 10) + ')');
  if (has(/shopify (plus )?partner|shopify experts?|shopify agency/g)) { score += 5; reasons.push('Shopify partner or expert (+5)'); }

  const needs = has(/\b(branding|brand identity|web ?design|ux|ui design|performance marketing|paid (social|media|ads)|meta ads|facebook ads|tiktok ads|google ads|seo|social media|content marketing|creative)\b/g);
  if (needs) { score += 15; reasons.push('sells design, brand or ads work that leads to builds (+15)'); }

  const dev = has(/\b(shopify develop|web develop|full[- ]?stack|front[- ]?end|back[- ]?end|liquid|headless|custom apps?|engineering|our developers|development team|in-house develop|software)\b/g);
  if (dev >= 4) { score -= 20; reasons.push('strong in-house development language (' + dev + ' mentions: -20)'); }
  else if (dev >= 1) { score += 0; reasons.push('some development language (' + dev + ')'); }
  else { score += 15; reasons.push('no development shown: dev is likely the bottleneck (+15)'); }

  const team = (text.match(/team of (\d{1,3})\b/) || text.match(/\b(\d{1,3})\+? (people|team members|experts|specialists|designers|strategists)\b/) || [])[1];
  if (team) {
    const n = Number(team);
    if (n <= 15) { score += 15; reasons.push('small team (about ' + n + ': +15)'); }
    else if (n <= 40) { score += 5; reasons.push('mid-size team (about ' + n + ': +5)'); }
    else { score -= 15; reasons.push('large team (about ' + n + ': -15)'); }
  }
  if (has(/\b(fortune 500|enterprise|global offices|offices in)\b/g)) { score -= 15; reasons.push('enterprise or multi-office language (-15)'); }

  const code = (page.html.match(/Shopify\.country\s*=\s*"([A-Z]{2})"/) || [])[1];
  const tld = /\.co\.uk$|\.com\.ng$/.test(domain) ? domain.match(/(co\.uk|com\.ng)$/)[1] : domain.split('.').pop();
  const country = String(row.country || '').trim() || CODE_COUNTRY_[code] || TLD_COUNTRY_[tld] || '';
  reasons.push(country ? 'market ' + country : 'country unknown (-5)');
  if (!country) score -= 5;

  const title = (page.html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '';
  const brand = title.replace(/\s+/g, ' ').split(/[|–\-:]/)[0].trim().slice(0, 40);
  return { score: Math.max(0, Math.min(100, score)), reasons: reasons, country: country, brand: brand, platform: 'Agency', model: 'agency', skip: false };
}

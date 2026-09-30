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

/**
 * Koolestpro Outreach: problem research (2026-10-06, Ridwan's feedback on the first test emails).
 *
 * Email 1 must rest on ONE problem that is real, specific to this store and worth fixing, not a generic line or a guess
 * from the homepage source. Before the profile is written this collects evidence from:
 *   - the homepage (headings, text, script hosts)
 *   - the store's own catalogue (Shopify /products.json: sold-out share, photos per product, description length)
 *   - one real product page (reviews, size guide, delivery and returns text, price, add to cart)
 *   - Google PageSpeed Insights on that product page, mobile (real-user data when Google has it, lab data otherwise)
 *   - the brand's own social links on the site; Instagram followers and recent posts when they can be read
 * Every evidence line is labelled: [MEASURED] a number from a tool or the catalogue, [SEEN] text read on a named page,
 * [SOFT] something NOT found in the page source (it may load later with JavaScript): never the main problem. Anything based on
 * absence is SOFT; only what is actually present or counted is SEEN or MEASURED.
 * The AI then picks the problem and scores how worth-solving it is (problem_worth 1 to 5). Leads under
 * MIN_PROBLEM_SCORE are held, not emailed. Optional Script properties: PAGESPEED_API_KEY, APIFY_TOKEN (Instagram).
 */

function textOf_(html) {
  return String(html || '').replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;|&rsquo;/g, "'").replace(/\s+/g, ' ').trim();
}

function researchStore_(S, lead, homePage) {
  const base = String(lead.website).trim().replace(/^https?:\/\//i, '').replace(/\/.*$/, '');
  const ev = [], social = [];
  let pdpUrl = '', pdpHtml = '';

  // Homepage: how many outside services it loads (each is a request a phone waits on).
  const hosts = {};
  String(homePage.html).replace(/<script[^>]+src=["']([^"']+)["']/gi, (m, src) => {
    const h = (src.match(/^(?:https?:)?\/\/([^\/]+)/i) || [])[1];
    if (h && !/shopify|cdn\.shop|myshopify/i.test(h) && h.indexOf(cleanDomain_(base)) === -1) hosts[h.toLowerCase()] = true;
    return m;
  });
  if (Object.keys(hosts).length >= 12) ev.push('[MEASURED] homepage loads scripts from ' + Object.keys(hosts).length + ' outside services: ' + Object.keys(hosts).slice(0, 8).join(', '));

  // Catalogue (Shopify only).
  let products = [];
  try {
    const res = UrlFetchApp.fetch('https://' + base + '/products.json?limit=250', { muteHttpExceptions: true, followRedirects: true, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } });
    if (res.getResponseCode() === 200) products = (JSON.parse(res.getContentText()).products || []);
  } catch (e) { /* not Shopify, or the endpoint is closed */ }
  if (products.length) {
    const n = products.length, nTxt = n >= 250 ? '250+' : String(n);
    const soldOut = products.filter(p => (p.variants || []).length && p.variants.every(v => v.available === false));
    const oneImg = products.filter(p => (p.images || []).length <= 1);
    const thin = products.filter(p => textOf_(p.body_html).split(/\s+/).filter(String).length < 25);
    ev.push('[MEASURED] catalogue: ' + nTxt + ' products');
    if (n >= 4 && soldOut.length / n >= 0.25) ev.push('[MEASURED] ' + soldOut.length + ' of ' + nTxt + ' products are sold out in every variant, e.g. ' + soldOut.slice(0, 3).map(p => p.title).join(', '));
    if (n >= 3 && oneImg.length / n >= 0.3) ev.push('[MEASURED] ' + oneImg.length + ' of ' + nTxt + ' products have one photo or none, e.g. ' + oneImg.slice(0, 3).map(p => p.title).join(', '));
    if (n >= 3 && thin.length / n >= 0.3) ev.push('[MEASURED] ' + thin.length + ' of ' + nTxt + ' products have a description under 25 words, e.g. ' + thin.slice(0, 3).map(p => p.title).join(', '));
    const newest = products.map(p => new Date(p.published_at || p.created_at)).filter(d => !isNaN(d)).sort((a, b) => b - a)[0];
    if (newest) ev.push('[MEASURED] newest product published ' + Utilities.formatDate(newest, 'UTC', 'yyyy-MM-dd'));

    // One real product page: an in-stock product with the most photos (the one they are proudest of).
    const pick = products.filter(p => soldOut.indexOf(p) === -1).sort((a, b) => (b.images || []).length - (a.images || []).length)[0] || products[0];
    pdpUrl = 'https://' + base + '/products/' + pick.handle;
    try {
      const pg = fetchPage_(pdpUrl);
      if (pg.ok) {
        pdpHtml = pg.html;
        const t = textOf_(pg.html), tl = t.toLowerCase();
        const words = textOf_(pick.body_html).split(/\s+/).filter(String).length;
        ev.push('[SEEN] product page ' + pdpUrl + ' ("' + pick.title + '"): ' + (pick.images || []).length + ' photos, description ' + words + ' words, ' +
          (pick.variants || []).length + ' variants' + ((pick.options || []).length ? ' (options: ' + pick.options.map(o => o.name).join(', ') + ')' : ''));
        const sized = (pick.options || []).some(o => /size/i.test(o.name));
        if (sized && !/size (guide|chart)|sizing|fit guide|measurements/i.test(t)) ev.push('[SOFT] the product has a Size option but no size guide or size chart text was found in the product page HTML (a popup may load it)');
        if (!/shipping|delivery|dispatch|ships in|arrives/i.test(t.slice(0, 6000))) ev.push('[SOFT] no shipping or delivery wording found near the top of the product page text');
        const revWidget = /judge\.me|jdgm|yotpo|loox|stamped|okendo|reviews\.io|trustpilot|junip|rivyo|ali-?reviews|opinew/i.test(pg.html);
        const revText = /\b\d+\s+reviews?\b|customer reviews|★|rating/i.test(t);
        if (!revWidget && !revText) ev.push('[SOFT] no reviews app or review text in the product page HTML (an app may still load it with JavaScript)');
        else if (/\b0 reviews?\b|no reviews yet|be the first to review/i.test(tl)) ev.push('[SEEN] product page shows no reviews yet ("be the first to review" or 0 reviews)');
        if (!/shopify-payment-button|add to (cart|bag|basket)|buy (it )?now/i.test(pg.html)) ev.push('[SOFT] no add-to-cart or buy button text found in the product page HTML');
      }
    } catch (e) { /* product page unreachable */ }
  } else {
    ev.push('[SEEN] no public Shopify catalogue (/products.json closed or not a Shopify store); only the homepage was read');
  }

  // Google PageSpeed Insights, mobile. Real-user (Chrome) data beats lab data when Google has it.
  const psi = pageSpeed_(pdpUrl || ('https://' + base));
  if (psi) ev.push(psi);

  // The brand's own social links on the site.
  const links = socialLinks_(homePage.html + ' ' + pdpHtml);
  Object.keys(links).forEach(k => social.push(k + ': ' + links[k]));
  if (links.instagram) {
    const ig = instagram_(S, links.instagram);
    if (ig) social.push(ig);
  }
  if (links.linkedin) social.push('LinkedIn page found (not read: LinkedIn needs a login). Use it only to know they are on LinkedIn.');
  return { evidence: ev, social: social, pdpUrl: pdpUrl };
}

/** One PSI call. Returns an evidence line or ''. Needs Script property PAGESPEED_API_KEY in practice (free, 25,000 a day): without a key Google's shared quota is usually used up (HTTP 429). */
function pageSpeed_(url) {
  const key = PropertiesService.getScriptProperties().getProperty('PAGESPEED_API_KEY');
  try {
    const res = UrlFetchApp.fetch('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile&category=performance&url=' + encodeURIComponent(url) + (key ? '&key=' + encodeURIComponent(key) : ''), { muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) return '';
    const j = JSON.parse(res.getContentText());
    const parts = [];
    const field = (j.loadingExperience || {}).metrics || {};
    if (field.LARGEST_CONTENTFUL_PAINT_MS) parts.push('real Chrome users on phones: main content shows after ' + (field.LARGEST_CONTENTFUL_PAINT_MS.percentile / 1000).toFixed(1) + 's at the 75th percentile (' + lc_(field.LARGEST_CONTENTFUL_PAINT_MS.category) + ')');
    const lh = j.lighthouseResult || {}, a = lh.audits || {};
    const score = ((lh.categories || {}).performance || {}).score;
    if (score !== undefined && score !== null) parts.push('lab test: performance ' + Math.round(score * 100) + '/100');
    if (a['largest-contentful-paint']) parts.push('main image or text shows after ' + (a['largest-contentful-paint'].numericValue / 1000).toFixed(1) + 's');
    if (a['total-blocking-time']) parts.push('page frozen to taps for ' + Math.round(a['total-blocking-time'].numericValue) + 'ms');
    if (a['total-byte-weight']) parts.push((a['total-byte-weight'].numericValue / 1048576).toFixed(1) + 'MB downloaded');
    return parts.length ? '[MEASURED] Google PageSpeed, mobile, ' + url + ': ' + parts.join('; ') : '';
  } catch (e) { return ''; }
}

function socialLinks_(html) {
  const out = {};
  const grab = (k, re) => { const m = String(html).match(re); if (m && !out[k]) out[k] = m[0].replace(/["'].*$/, ''); };
  grab('instagram', /https?:\/\/(?:www\.)?instagram\.com\/(?!p\/|reel\/|explore\/|accounts\/|share)[A-Za-z0-9._]{2,30}\/?/i);
  grab('tiktok', /https?:\/\/(?:www\.)?tiktok\.com\/@[A-Za-z0-9._]{2,30}/i);
  grab('linkedin', /https?:\/\/(?:[a-z]{2,3}\.)?linkedin\.com\/(?:company|in)\/[A-Za-z0-9\-_%]{2,80}\/?/i);
  grab('facebook', /https?:\/\/(?:www\.)?facebook\.com\/(?!sharer|share|dialog|tr\b|plugins)[A-Za-z0-9.\-]{2,60}\/?/i);
  grab('youtube', /https?:\/\/(?:www\.)?youtube\.com\/(?:@|c\/|channel\/|user\/)[A-Za-z0-9_\-]{2,60}/i);
  return out;
}

/**
 * Instagram followers and recent posts. Setting INSTAGRAM_LOOKUP: "free" (default) reads the public page's preview text,
 * which Instagram often blocks from Google's servers; "apify" uses Apify's Instagram Profile Scraper (needs APIFY_TOKEN,
 * paid per profile, a few cents per 10); "off" skips it.
 */
function instagram_(S, url) {
  const mode = lc_(S.INSTAGRAM_LOOKUP || 'free');
  const handle = (String(url).match(/instagram\.com\/([A-Za-z0-9._]+)/i) || [])[1];
  if (!handle || mode === 'off') return '';
  if (mode === 'apify' && PropertiesService.getScriptProperties().getProperty('APIFY_TOKEN')) {
    try {
      const items = apifyCall_('post', '/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?timeout=90', { usernames: [handle] });
      const p = (items || [])[0];
      if (p && p.username) {
        const posts = (p.latestPosts || []).slice(0, 5).map(x => (x.timestamp || '').slice(0, 10) + ' ' + (x.likesCount || 0) + ' likes, ' + (x.commentsCount || 0) + ' comments: ' + String(x.caption || '').replace(/\s+/g, ' ').slice(0, 140));
        return 'Instagram @' + p.username + ': ' + (p.followersCount || 0) + ' followers, ' + (p.postsCount || 0) + ' posts. Bio: ' + String(p.biography || '').replace(/\s+/g, ' ').slice(0, 160) +
          (p.externalUrl ? '. Bio link: ' + p.externalUrl : '') + (posts.length ? '. Recent posts: ' + posts.join(' | ') : '');
      }
    } catch (e) { /* fall through to the free read */ }
  }
  try {
    const res = UrlFetchApp.fetch('https://www.instagram.com/' + handle + '/', { muteHttpExceptions: true, followRedirects: true, headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15' } });
    const m = res.getContentText().match(/<meta[^>]+(?:property|name)=["'](?:og:)?description["'][^>]+content=["']([^"']+)["']/i);
    if (m && /followers/i.test(m[1])) return 'Instagram @' + handle + ': ' + m[1].replace(/&#\d+;|&[a-z]+;/g, ' ').replace(/\s+/g, ' ').slice(0, 220);
  } catch (e) {}
  return 'Instagram @' + handle + ' (could not read followers from here)';
}

const STORE_PROFILE_SYS_ = [
  'You are a Shopify CRO specialist. You read real evidence about one online store and (1) profile it, (2) choose the ONE problem worth a cold email to its founder. Use ONLY the data given. Never guess.',
  'Evidence labels: [MEASURED] = a number from a tool or the store\'s own catalogue, reliable. [SEEN] = text read on a named page, reliable. [SOFT] = not found in the page source; it may load later with JavaScript, so it is NEVER the main problem and never called missing or broken.',
  'A problem worth a cold email: (a) specific to this store: names the page and the exact element, product or number; (b) true from MEASURED or SEEN evidence, never an "error" you are not sure of; (c) clearly costs sales or trust on a money page (product page, homepage first screen, cart, the page their Instagram sends people to); (d) something a busy founder would agree is worth fixing. NOT a problem: taste (colours, fonts, layout preference), generic advice ("could improve conversions", "SEO could be better", "add more trust"), anything that only says something was not spotted in the source.',
  'Use social data only as context (for example a large Instagram following sending people to a product page that is slow or has one photo). Never comment on their follower count as a compliment or a criticism.',
  'Score worth 1 to 5. 5: a verified, specific issue on a money page with an obvious cost. 4: verified and clearly costs sales, slightly smaller. 3: real but minor. 2 or 1: weak, soft or guesswork. If nothing reaches 4, give the honest score; do not dress up a weak point.',
  'Output JSON only: {"what_they_sell":"one short line","audience":"who buys, one short line","niche":"2 to 3 words","signal":"one line: why they look like a fit for the given track","site_notes":"2 to 4 short, true observations, each a plain sentence",' +
  '"problem":"one sentence a founder would recognise: the page, the element, what the shopper runs into","problem_evidence":"the exact evidence lines it rests on, with their labels","problem_page":"url","cost":"one line, what it costs them in plain words, no invented numbers","fix":"one line, what Ridwan would change","worth":1-5,' +
  '"second":{"problem":"a different, also verified problem for a follow-up","evidence":"labelled evidence","worth":1-5} or null,"rejected":"short list of weaker points you considered and why you did not pick them"}',
].join('\n');

/** A sequence may be written only when the store has a problem worth emailing about (agencies and no-website leads are exempt). */
function problemOk_(lead, profile, S) {
  if (lc_(lead.track) === 'partner' || lc_(lead.track) === 'build' || !String(lead.website).trim()) return true;
  if (!profile || profile.problem_worth === undefined) return true;   // Profiles tab not upgraded yet: old behaviour
  const min = Number(S.MIN_PROBLEM_SCORE || 4);
  return Number(profile.problem_worth || 0) >= min;
}

/** Menu: test phase helper. Unsent leads get fresh research and a fresh sequence on the next run. Sent emails are never touched. */
function redoUnsentLeads() {
  const ui = SpreadsheetApp.getUi();
  if (ui.alert('Redo research and emails for leads that have not been emailed yet?', 'Their Draft sequence rows become Superseded and their problem research is cleared. Nothing already sent changes.', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  const leads = read_('Leads'), seq = read_('Sequence'), prof = read_('Profiles');
  const unsent = {};
  leads.rows.filter(l => l.lead_id && Number(l.touch_count || 0) === 0 && ['New', ''].indexOf(String(l.stage)) !== -1).forEach(l => {
    unsent[String(l.lead_id)] = true;
    if (l.approved === true || lc_(l.approved) === 'true') set_(leads, l, 'approved', false);
  });
  let n = 0;
  seq.rows.filter(r => unsent[String(r.lead_id)] && r.status === 'Draft').forEach(r => { set_(seq, r, 'status', 'Superseded'); n++; });
  if (prof.headers.indexOf('problem_worth') !== -1) prof.rows.filter(p => unsent[String(p.lead_id)]).forEach(p => set_(prof, p, 'problem_worth', ''));
  toast_(Object.keys(unsent).length + ' unsent lead(s) reset (' + n + ' draft emails superseded, approvals cleared). Run Prepare new leads now.');
}

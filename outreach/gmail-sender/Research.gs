/**
 * Koolestpro Outreach: store research (2026-10-06, Ridwan's feedback on the first test emails).
 *
 * A lead is only emailed when there is a tangible reason: a project worth paying for, tied to how this business sells.
 * Not a small fix they could do in ten minutes. Speed only when the store is obviously slow (speedCheck_). Big brands are skipped.
 * The method follows the koolestpro-client-audit skill (funnel discovery, Tier 1 "fix what's leaking", Tier 2 "add what's
 * missing") and the store-auditor skill (specific, located, named element, real data only).
 *
 * For each store lead this collects:
 *   - big-brand check: Tranco top-1M traffic rank (free API) plus scale signals; a big brand is marked Lost, never emailed
 *   - the catalogue (Shopify /products.json): what they sell, price range, product types, consumables, catalogue gaps
 *   - one real product page
 *   - the funnel: custom pages from the sitemap (advertorials, listicles, landing, quiz, bundle pages), common hidden page
 *     paths, funnel subdomains (try., get., offer. ...), page builders (Replo, GemPages, Zipify, Funnelish ...), ad pixels
 *     (Meta, TikTok, Google Ads), upsell, post-purchase, bundle, subscription and quiz apps
 *   - the About page: founder or owner name, team size hints (who the decision maker is)
 *   - the brand's own social links; Instagram followers and recent posts when they can be read
 * Every evidence line is labelled: [MEASURED] a count from the store's own data, [SEEN] something actually present on a
 * named page, [SOFT] something NOT found (it may be elsewhere or load later): never stated as fact, only asked about.
 * The AI then picks ONE offer and the problem behind it and scores it 1 to 5 (problem_worth). Under MIN_PROBLEM_SCORE the
 * lead is held. Optional: Script property APIFY_TOKEN (Instagram via Apify), Settings BIG_BRAND_RANK.
 */

/**
 * Removes what a shopper never sees: templates, noscript, and short hidden state labels. Themes ship labels like
 * <span class="sold-out-message hidden">Sold out</span> on every in-stock product; reading those as real text made an email
 * claim a fully stocked store was sold out (District Lounge, 2026-10-07).
 */
function stripHidden_(html) {
  let h = String(html || '').replace(/<(template|noscript|svg|select|datalist|nav|footer)\b[\s\S]*?<\/\1>/gi, ' ');
  // Country/currency pickers and menu drawers are closed dropdowns, never page content (sneakblessed.shop 2026-10-08: a hidden
  // list of 476 countries was read as "a long country list across the top"; ilouity.com: a "Stockholm Store" menu link became a claim).
  h = h.replace(/<form[^>]*(localization|country|currency)[^>]*>[\s\S]*?<\/form>/gi, ' ')
       .replace(/<(details|div|ul)[^>]*(localization|country-selector|currency-selector|disclosure__list|menu-drawer|mega-menu|header__menu|header__inline-menu|drawer__menu)[^>]*>[\s\S]*?<\/\1>/gi, ' ');
  const hiddenEl = /<(span|p|div|small|label|li|a|button|strong|em|h[1-6])\b([^>]*(?:class=["'][^"']*\b(?:hidden|visually-hidden|sr-only|is-hidden|d-none|hide)\b[^"']*["']|\shidden(?:[\s>=])|aria-hidden=["']true["']|style=["'][^"']*display:\s*none)[^>]*)>[\s\S]*?<\/\1>/gi;
  // Only short hidden labels go ("Sold out", "Unavailable", "Added to cart"). Long hidden blocks are collapsed accordions
  // (FAQ answers, shipping details) that a shopper opens with one tap, so they count as on the page.
  for (let i = 0; i < 3; i++) h = h.replace(hiddenEl, m => m.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim().length <= 60 ? ' ' : m);
  return h;
}

function textOf_(html) {
  return stripHidden_(html).replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;|&rsquo;/g, "'").replace(/\s+/g, ' ').trim();
}

function get_(url) {
  try {
    const res = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: true, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } });
    return { code: res.getResponseCode(), text: res.getContentText() };
  } catch (e) { return { code: 0, text: '' }; }
}

// ---------- Big brands: never emailed ----------

/** Tranco ranks the top 1 million sites by traffic. Ridwan's own small clients are not in it at all; Allbirds is about #68,000. */
function trancoRank_(host) {
  const r = get_('https://tranco-list.eu/api/ranks/domain/' + encodeURIComponent(cleanDomain_(host)));
  Utilities.sleep(1100);   // the API allows one request a second
  if (r.code !== 200) return null;
  try { const ranks = JSON.parse(r.text).ranks || []; return ranks.length ? Number(ranks[0].rank) : 0; } catch (e) { return null; }
}

const BIG_APPS_ = /attentive|gorgias|yotpo|okendo|rebuyengine|nosto|bloomreach|klevu|searchspring|algolia|global-?e\.com|postscript|zendesk|bazaarvoice|dynamic ?yield|optimizely|contentsquare|fullstory|salesforce|tealium|segment\.com/gi;

/** Returns { big, reasons[] }. Tranco listing alone is enough; otherwise two or more scale signals. */
function bigBrand_(S, host, html, nProducts) {
  const limit = Number(S.BIG_BRAND_RANK || 1000000);
  const rank = trancoRank_(host);
  if (rank && rank <= limit) return { big: true, reasons: ['Tranco traffic rank #' + rank.toLocaleString() + ' (in the top ' + limit.toLocaleString() + ' sites worldwide, far past the under-1,000-visits-a-day target)'] };
  const h = String(html || '');
  const strong = [], weak = [];
  const apps = (h.match(BIG_APPS_) || []).map(x => x.toLowerCase()).filter((x, i, a) => a.indexOf(x) === i);
  if (apps.length >= 4) strong.push('enterprise app stack: ' + apps.join(', '));
  if (nProducts >= 250) strong.push('250+ products');
  const langs = (h.match(/hreflang=["'][a-z]{2}(-[A-Za-z]{2})?["']/gi) || []).map(x => x.toLowerCase()).filter((x, i, a) => a.indexOf(x) === i).length;
  if (langs > 5) strong.push(langs + ' language or market versions');
  if (/store locator|find a store|our stores|retail locations/i.test(h)) weak.push('physical stores');   // "stockists" alone is common for small brands, not counted
  if (/\/careers|\/jobs|join our team|we['’]re hiring/i.test(h)) weak.push('careers page');
  const reasons = strong.concat(weak);
  return { big: strong.length >= 2 || (strong.length >= 1 && weak.length >= 1), reasons: (rank === 0 ? ['not in Tranco top 1M'] : rank === null ? ['Tranco unreachable'] : []).concat(reasons) };
}

// ---------- Funnel discovery (from the client-audit skill) ----------

const BUILDERS_ = [['Replo', /replo/i], ['GemPages', /gempages|gem-page/i], ['PageFly', /pagefly/i], ['Shogun', /getshogun|shogun-/i], ['Zipify Pages', /zipify/i],
  ['Funnelish', /funnelish/i], ['ClickFunnels', /clickfunnels/i], ['CheckoutChamp', /checkoutchamp|konnektive/i], ['Unbounce', /unbounce/i], ['Instapage', /instapage/i],
  ['Leadpages', /leadpages/i], ['Instant', /instant\.so|instantcommerce/i], ['Convertri', /convertri/i]];
const UPSELL_APPS_ = [['ReConvert (thank-you page upsells)', /reconvert/i], ['AfterSell (post-purchase)', /aftersell/i], ['Zipify OCU (post-purchase)', /zipify-?oneclick|zipifyocu|\bocu-/i],
  ['CartHook', /carthook/i], ['Rebuy', /rebuyengine/i], ['UpCart', /upcart/i], ['Monster Cart', /monster-?cart|monsterapps/i], ['Selleasy', /selleasy|logbase/i],
  ['Candy Rack', /candyrack|candy-rack/i], ['In Cart Upsell', /incartupsell|in-cart-upsell/i], ['Frequently Bought Together', /frequently-bought|cdn\.codeblackbelt/i], ['Kaching', /kaching/i]];
const BUNDLE_APPS_ = [['Fast Bundle', /fastbundle|fast-bundle/i], ['Bundler', /bundler\.app|bundlerapp/i], ['Simple Bundles', /simplebundles|simple-bundles/i],
  ['Kaching Bundles', /kaching-?bundles/i], ['Bundle Builder (custom or app)', /build-?your-?own|build-?a-?box|build-?a-?bundle|bundle-?builder/i]];
const SUBSCRIPTION_APPS_ = [['Recharge', /rechargecdn|rechargepayments|recharge-/i], ['Skio', /skio/i], ['Loop', /loopsubscriptions|loop-subscriptions/i], ['Appstle', /appstle/i],
  ['Seal', /sealsubscriptions/i], ['Stay AI', /stay\.ai|retextion/i], ['Bold Subscriptions', /boldsubscriptions|bold-subscriptions/i], ['Shopify Subscriptions', /subscription_policy|selling_plan/i]];
const QUIZ_APPS_ = [['Octane AI', /octaneai|octane-ai/i], ['RevenueHunt', /revenuehunt/i], ['Typeform', /typeform/i], ['Jebbit', /jebbit/i]];
const PIXELS_ = [['Meta pixel', /connect\.facebook\.net[^"']*fbevents|fbq\(\s*['"]init/i], ['TikTok pixel', /analytics\.tiktok\.com/i], ['Google Ads tag', /AW-\d{6,}/],
  ['Snapchat pixel', /sc-static\.net\/scevent/i], ['Pinterest tag', /pintrk\(/i]];
const FUNNEL_WORDS_ = /advertorial|listicle|reasons?-?why|\breasons\b|why-|vs-|compare|comparison|lp-|-lp\b|\blp\b|landing|offer|try-|special|deal|promo|story|quiz|bundle|build-your|sale|discover|learn|review/i;
const FUNNEL_SUBS_ = ['try', 'get', 'go', 'offer', 'offers', 'lp', 'learn', 'discover', 'info', 'deals', 'special', 'health', 'buy'];

function hits_(list, html) { return list.filter(x => x[1].test(html)).map(x => x[0]); }

function funnel_(base, host, homeHtml, pdpHtml) {
  const ev = [];
  const all = String(homeHtml) + ' ' + String(pdpHtml || '');

  // 1. Custom pages from the sitemap (pages not in the navigation are often paid-traffic entry points).
  let pages = [], blogs = 0;
  const idx = get_('https://' + base + '/sitemap.xml');
  if (idx.code === 200) {
    const children = (idx.text.match(/<loc>([^<]+)<\/loc>/g) || []).map(x => x.replace(/<\/?loc>/g, ''));
    const pagesMap = children.find(u => /sitemap_pages/i.test(u));
    if (pagesMap) {
      const pm = get_(pagesMap.replace(/&amp;/g, '&'));
      pages = (pm.text.match(/<loc>([^<]+)<\/loc>/g) || []).map(x => x.replace(/<\/?loc>/g, ''));
    }
    blogs = children.filter(u => /sitemap_blogs/i.test(u)).length;
    if (!pagesMap && /<urlset/i.test(idx.text)) pages = children.filter(u => !/\.(jpe?g|png|webp|gif)(\?|$)/i.test(u) && !/\/products?\//i.test(u)).slice(0, 400);   // non-Shopify: one flat sitemap
  }
  const funnelPages = pages.filter(u => FUNNEL_WORDS_.test(u.split('/').pop()));
  if (pages.length) ev.push('[MEASURED] sitemap: ' + pages.length + ' custom pages' + (funnelPages.length ? '; offer, landing or pre-sell style pages: ' + funnelPages.slice(0, 8).join(', ') : '; none look like an advertorial, listicle, landing, quiz or bundle page') + (blogs ? '; has a blog' : ''));
  else ev.push('[SOFT] no custom pages listed in the sitemap (or no sitemap)');

  // 2. Common hidden paths (Shopify returns 404 for pages that do not exist).
  const probed = [];
  ['/pages/advertorial', '/pages/listicle', '/pages/lp', '/pages/offer', '/pages/quiz', '/pages/build-your-own-bundle', '/pages/bundle'].forEach(p => {
    if (pages.some(u => u.indexOf(p) !== -1)) return;
    const r = get_('https://' + base + p);
    if (r.code === 200 && !/404|page not found/i.test(textOf_(r.text).slice(0, 2000))) probed.push(p + (hits_(BUILDERS_, r.text).length ? ' (built with ' + hits_(BUILDERS_, r.text).join(', ') + ')' : ''));
  });
  if (probed.length) ev.push('[SEEN] hidden pages that exist: ' + probed.join(', '));

  // 3. Funnel subdomains. Advertorials often live on try.brand.com or get.brand.com. A separate, unrelated domain can only be
  // found from their ads' landing URLs (Meta Ad Library), so absence here is never proof.
  const subs = [];
  FUNNEL_SUBS_.forEach(s => {
    const d = get_('https://dns.google/resolve?type=A&name=' + s + '.' + host);
    let ok = false;
    try { ok = (JSON.parse(d.text).Answer || []).length > 0; } catch (e) {}
    if (!ok) return;
    const r = get_('https://' + s + '.' + host);
    if (r.code >= 200 && r.code < 400) {
      const b = hits_(BUILDERS_, r.text);
      subs.push(s + '.' + host + (b.length ? ' (' + b.join(', ') + ')' : '') + ': "' + textOf_((r.text.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1]).slice(0, 80) + '"');
    }
  });
  if (subs.length) ev.push('[SEEN] funnel subdomains live: ' + subs.join('; '));

  const builders = hits_(BUILDERS_, all);
  if (builders.length) ev.push('[SEEN] page builder on the store: ' + builders.join(', '));
  const px = hits_(PIXELS_, all);
  ev.push(px.length ? '[SEEN] ad tracking installed: ' + px.join(', ') + ' (they run, or are set up to run, paid traffic)' : '[SOFT] no ad pixel found in the page source');
  const ups = hits_(UPSELL_APPS_, all), bun = hits_(BUNDLE_APPS_, all + ' ' + pages.join(' ')), sub = hits_(SUBSCRIPTION_APPS_, all), quiz = hits_(QUIZ_APPS_, all);
  ev.push(ups.length ? '[SEEN] upsell or post-purchase apps: ' + ups.join(', ') : '[SOFT] no upsell or post-purchase app visible in the storefront (post-purchase offers run inside checkout, so this cannot be confirmed from outside)');
  ev.push(bun.length ? '[SEEN] bundles: ' + bun.join(', ') : '[SOFT] no bundle app or bundle page found');
  ev.push(sub.length ? '[SEEN] subscriptions: ' + sub.join(', ') : '[SOFT] no subscription app found');
  if (quiz.length) ev.push('[SEEN] quiz: ' + quiz.join(', '));
  return { ev: ev, hasPresell: funnelPages.length > 0 || probed.length > 0 || subs.length > 0 };
}

// ---------- Speed: only when it is obviously slow ----------

/**
 * Speed is a strong reason to reply, but only when nobody could argue with it. Returns an evidence line starting [SPEED],
 * or '' (nothing at all, so the AI cannot mention speed). Two ways to qualify:
 *   1. Google's real-user data (Chrome UX Report) rates the page or the whole site SLOW, with the 75th-percentile time to
 *      the main content at or above SPEED_FIELD_LCP seconds (default 4, Google's own "poor" line). Real visitors, not a test.
 *   2. No real-user data (common for small stores): the lab test on a phone shows the main content at or above
 *      SPEED_LAB_LCP seconds (default 8) with a performance score of 35 or less, and a second run agrees.
 * Needs Script property PAGESPEED_API_KEY (free); without it Google's shared quota is usually used up and this returns ''.
 */
function psi_(url) {
  const key = PropertiesService.getScriptProperties().getProperty('PAGESPEED_API_KEY');
  const r = get_('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile&category=performance&url=' + encodeURIComponent(url) + (key ? '&key=' + encodeURIComponent(key) : ''));
  if (r.code !== 200) return null;
  try { return JSON.parse(r.text); } catch (e) { return null; }
}

function speedCheck_(S, url) {
  const fieldMin = Number(S.SPEED_FIELD_LCP || 4), labMin = Number(S.SPEED_LAB_LCP || 8);
  const a = psi_(url);
  if (!a) return '';
  const pick = x => (x && x.metrics && x.metrics.LARGEST_CONTENTFUL_PAINT_MS) ? x.metrics.LARGEST_CONTENTFUL_PAINT_MS : null;
  const page = pick(a.loadingExperience), site = pick(a.originLoadingExperience);
  const field = page || site;
  if (field) {   // real-user data exists: it decides, the lab test is ignored
    const secs = field.percentile / 1000;
    if (field.category === 'SLOW' && secs >= fieldMin)
      return '[SPEED] [MEASURED] Google real-user data (Chrome UX Report, phones, ' + (page ? 'this page: ' + url : 'whole site') + '): for 1 in 4 visits the main image or text takes longer than ' + secs.toFixed(1) + 's to appear. Google rates this slow.';
    return '';
  }
  const lab = j => { const lh = j.lighthouseResult || {}; return { lcp: (((lh.audits || {})['largest-contentful-paint'] || {}).numericValue || 0) / 1000, score: Math.round((((lh.categories || {}).performance || {}).score || 0) * 100) }; };
  const one = lab(a);
  if (one.lcp < labMin || one.score > 35) return '';
  const b = psi_(url);   // lab results vary run to run: a second run must agree
  if (!b) return '';
  const two = lab(b);
  if (two.lcp < labMin || two.score > 35) return '';
  return '[SPEED] [MEASURED] Google PageSpeed lab test on a phone, run twice, ' + url + ': main image or text appears after ' + one.lcp.toFixed(1) + 's and ' + two.lcp.toFixed(1) + 's (performance ' + one.score + ' and ' + two.score + ' out of 100).';
}

// ---------- Link check (2026-10-23, Ridwan) ----------

/**
 * Clicks the links a visitor would click on the homepage and one product page and reports two things that are plain facts:
 *   - BROKEN: the link ends on a 404 or 410 page.
 *   - HOME: the link ends on the homepage even though its path is not the homepage (a "Shop All" or "Best Sellers" item
 *     that dumps the visitor back on the page they are already on). A "Shop now" style button whose address IS the homepage
 *     counts the same way (SELF).
 * Only 404, 410 and a redirect chain that ends on the homepage count. 403, 429 and 5xx are bot walls or outages, never findings.
 * Every hit is fetched twice before it is reported. Skipped in the second half of a run (Apps Script's 6 minute limit).
 */
const LINK_SKIP_PATH_ = /^\/(account|cart|checkout|checkouts|search|password|apps|tools|challenge|services|cdn|wpm@)|^\/[a-z]{2}([-_][a-z]{2})?\/?$/i;
const LINK_CTA_LABEL_ = /^(shop( now| all| the collection)?|buy( now)?|order( now)?|view all|see all|explore|discover|get started|shop collection|browse (all|the collection))$/i;
const LINK_UA_ = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15' };

function sameHost_(url, base) {
  const m = String(url).match(/^https?:\/\/([^\/?#]+)/i);
  return !!m && cleanDomain_(m[1]) === cleanDomain_(base);
}
function isHomeUrl_(url, base) {
  if (!sameHost_(url, base)) return false;
  const p = String(url).replace(/^https?:\/\/[^\/?#]+/i, '').replace(/[?#].*$/, '');
  return p === '' || p === '/';
}

/** Internal links in a page: { url, path, label, where }. `where` is header menu, page body or footer. */
function pageLinks_(html, base, pageName) {
  const h = String(html || '').replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<!--[\s\S]*?-->/gi, ' ');
  const spans = [];
  [['header', 'header menu'], ['footer', 'footer']].forEach(t => {
    const re = new RegExp('<' + t[0] + '\\b[\\s\\S]*?<\\/' + t[0] + '>', 'gi');
    let m; while ((m = re.exec(h))) spans.push([m.index, m.index + m[0].length, t[1]]);
  });
  const out = [], seen = {};
  const re = /<a\b([^>]*?)href=["']([^"'#][^"']*)["']([^>]*)>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(h))) {
    let href = m[2].trim().replace(/&amp;/g, '&');
    if (/^(mailto:|tel:|javascript:|sms:|whatsapp:)/i.test(href)) continue;
    let url;
    if (/^\/\//.test(href)) url = 'https:' + href;
    else if (/^\//.test(href)) url = 'https://' + base + href;
    else if (/^https?:\/\//i.test(href)) url = href;
    else continue;
    if (!sameHost_(url, base)) continue;
    url = url.replace(/#.*$/, '');
    const path = url.replace(/^https?:\/\/[^\/?#]+/i, '') || '/';
    const label = m[4].replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim().slice(0, 40);
    const home = isHomeUrl_(url, base);
    if (home && !LINK_CTA_LABEL_.test(label)) continue;   // the logo and "Home" link to the homepage on purpose
    if (!home && LINK_SKIP_PATH_.test(path)) continue;
    if (!label && !home) continue;
    const key = path + '|' + label.toLowerCase();
    if (seen[key]) continue;
    seen[key] = true;
    const sp = spans.filter(s => m.index >= s[0] && m.index < s[1])[0];
    out.push({ url: url, path: path, label: label, home: home, where: sp ? sp[2] : 'page body', page: pageName || 'homepage' });
  }
  return out;
}

/** Follows redirects by hand (at most 4 hops). Returns { code, url } for where the link really ends. */
function endOf_(url) {
  let cur = url;
  for (let i = 0; i < 5; i++) {
    let r;
    try { r = UrlFetchApp.fetch(cur, { muteHttpExceptions: true, followRedirects: false, headers: LINK_UA_ }); } catch (e) { return { code: 0, url: cur }; }
    const code = r.getResponseCode();
    if (code < 300 || code >= 400) return { code: code, url: cur };
    const hd = r.getHeaders() || {};
    const loc = String(hd.Location || hd.location || '');
    if (!loc) return { code: code, url: cur };
    cur = /^https?:\/\//i.test(loc) ? loc : (/^\/\//.test(loc) ? 'https:' + loc : cur.replace(/^(https?:\/\/[^\/?#]+).*$/i, '$1') + (loc.charAt(0) === '/' ? '' : '/') + loc);
  }
  return { code: 310, url: cur };
}

function judgeLink_(l, base) {
  if (l.home) return 'self';   // a "Shop now" button that points at the homepage
  const e = endOf_(l.url);
  if (e.code === 404 || e.code === 410) return 'broken';
  if (e.code >= 200 && e.code < 300 && isHomeUrl_(e.url, base) && !isHomeUrl_(l.url, base)) return 'home';
  return '';
}

/** Returns { line, items } where items are confirmed findings. line is '' when everything checked out. */
function linkCheck_(S, base, pages) {
  const all = [];
  pages.forEach(p => pageLinks_(p.html, base, p.name).forEach(l => { if (!all.some(x => x.path === l.path && x.label.toLowerCase() === l.label.toLowerCase())) all.push(l); }));
  const rank = l => (l.where === 'header menu' ? 0 : l.home ? 1 : /^\/products\//.test(l.path) ? 4 : l.where === 'footer' ? 3 : 2);
  const todo = all.sort((a, b) => rank(a) - rank(b)).slice(0, 26);
  const items = [];
  todo.forEach(l => {
    const first = judgeLink_(l, base);
    if (!first) return;
    if (first !== 'self') { Utilities.sleep(1500); if (judgeLink_(l, base) !== first) return; }   // must repeat to count
    items.push({ url: l.url, path: l.path, label: l.label, where: l.where, page: l.page, kind: first });
  });
  if (!todo.length) return { line: '', items: [], checked: 0 };
  if (!items.length) return { line: '', items: [], checked: todo.length };
  const desc = it => '"' + (it.label || 'image link') + '" (' + it.where + (it.page !== 'homepage' ? ' of the ' + it.page : '') + ', ' + it.path + ')';
  const broken = items.filter(i => i.kind === 'broken'), home = items.filter(i => i.kind === 'home'), self = items.filter(i => i.kind === 'self');
  const parts = [];
  if (broken.length) parts.push('Lead to a page that does not exist (404): ' + broken.map(desc).join('; ') + '.');
  if (home.length) parts.push('Send the visitor back to the homepage instead of the page the label promises: ' + home.map(desc).join('; ') + '.');
  if (self.length) parts.push('Buttons whose address is the homepage itself, so clicking does nothing new: ' + self.map(desc).join('; ') + '.');
  return { line: '[LINKS] [MEASURED] Clicked ' + todo.length + ' links on the homepage and a product page, each failure confirmed twice. ' + parts.join(' '), items: items, checked: todo.length };
}

/** Re-checks the stored findings right now. True if at least one is still wrong. */
function linksStillBroken_(items, base) {
  return (items || []).some(it => judgeLink_({ url: it.url, home: it.kind === 'self' }, base) === it.kind);
}

// ---------- Restricted categories: never emailed ----------

/** Products Ridwan should not be selling services to (illegal to sell in many markets, payment-processor bans, or scam-prone). */
function restricted_(text) {
  const m = String(text || '').match(/\b(disposable vapes?|vapes?|e-?cig(arette)?s?|e-?liquids?|nicotine|tobacco|cigarettes?|shisha|hookah|\d{3,5} puffs|kratom|replica (bags|watches|shoes)|counterfeit|firearms?|ammunition)\b/i);
  return m ? m[0] : '';
}

// ---------- Fact check: does the page already answer the claim? ----------

/**
 * Every claimed problem is checked against the store's own visible text and data before an email can be written.
 * 1. Stock claims are checked against the product feed (the store's own truth), not page text.
 * 2. A skeptical second AI pass reads the visible product page, homepage and about text and looks for anything that
 *    answers, contradicts or weakens the claim (Nomalife 2026-10-07: the email said buyers wonder how fast it works and what
 *    if it does not, while the page showed 84 reviews, a 30-day money-back guarantee and an FAQ answering both).
 * Returns { holds, why }.
 */
function factCheck_(S, claim, r) {
  if (!claim) return { holds: false, why: 'no claim' };
  if (PRICE_CLAIM_.test(claim)) return { holds: false, why: 'price amount or price display point: Shopify converts and formats prices per visitor country, and themes hide compare-at prices, so what research reads is not what shoppers see' };
  if (LOCALE_WORDS_.test(claim)) return { holds: false, why: 'language, translation or currency point: stores adapt these to the visitor\'s country and research browses from abroad, so it is never a reason to email' };
  if (/\[LINKS\]|broken link|404|back to the home ?page|redirects? to the home ?page/i.test(claim)) {   // link findings are tested by clicking again, not by reading page text
    if (!r.links || !r.links.length) return { holds: false, why: 'no link finding was measured for this store' };
    return linksStillBroken_(r.links, r.base) ? { holds: true, why: 'links clicked again just now and still wrong' } : { holds: false, why: 'links no longer fail when clicked again' };
  }
  if (/sold.?out|out of stock|unavailable|no stock/i.test(claim) && r.stock) {
    if (r.stock.available / r.stock.total > 0.5) return { holds: false, why: 'product feed shows ' + r.stock.available + ' of ' + r.stock.total + ' products in stock' };
  }
  const sys = 'You are a skeptical reviewer. A cold email to this store is about to claim the problem below. Read the store\'s own VISIBLE text and decide if the claim survives. ' +
    'It FAILS if the page already shows the thing the claim says is missing or unclear (for example reviews, a guarantee, delivery or returns info, an FAQ answer, ingredients, how it works, results timing), if any text contradicts it, ' +
    'or if the claim is a generic worry for the niche rather than something specific to this page. Answer JSON only: {"holds":true|false,"quote":"the exact words from the page that answer or contradict it, or empty","why":"one short line"}';
  const user = 'CLAIM: ' + claim + '\n\nPRODUCT PAGE (visible text): ' + r.pages.pdp + '\n\nHOMEPAGE (visible text): ' + r.pages.home + (r.pages.about ? '\n\nABOUT: ' + r.pages.about : '') +
    (r.stock ? '\n\nPRODUCT FEED: ' + r.stock.available + ' of ' + r.stock.total + ' products in stock' : '');
  try {
    const j = parseJson_(callAi_(S, sys, user, 300).text);
    if (!j) return { holds: true, why: 'fact check returned no JSON (kept, check by hand)' };
    return { holds: j.holds !== false, why: (j.why || '') + (j.quote ? ' Page says: "' + String(j.quote).slice(0, 200) + '"' : '') };
  } catch (e) { return { holds: true, why: 'fact check failed: ' + e.message + ' (kept, check by hand)' }; }
}

// Language, translation and currency points are never a reason to email (Ridwan, 2026-10-07: sellare-es.com got an email about
// "Italian cart words" on a Spanish store; stores geo-adapt language and currency, and our fetches come from Google servers abroad).
const LOCALE_WORDS_ = /translat|\blanguages?\b|italian|spanish|french|german|portuguese|dutch|english text|currenc|\b(EUR|USD|GBP|AUD|CAD)\b|locali[sz]|\blocale\b|geo-?|wrong country|mixed (language|currency)/i;

// Price amounts and price display are never a reason either (2026-10-08): nexvy.shop's feed had a compare-at price the theme never
// shows; naturanimal.shop's whole catalogue sat at 100 to 7,990 EUR, a store setup problem, not a pitch.
const PRICE_CLAIM_ = /(sale|regular|original|crossed.?out|struck.?through|compare.?at|full|old) price|price (is|shows|sits|reads|listed|display)|listed at|priced at|[€$£₦]\s?\d|\d\s?(EUR|USD|GBP|NGN)\b/i;

// ---------- Who decides ----------

function aboutText_(base) {
  for (const p of ['/pages/about', '/pages/about-us', '/pages/our-story', '/about', '/pages/founder', '/pages/meet-the-founder']) {
    const r = get_('https://' + base + p);
    if (r.code !== 200) continue;
    const t = textOf_(r.text);
    const i = t.search(/founder|founded|owner|our story|started|my name|i'm |i am |we are|team/i);
    if (t.length > 200) return { path: p, text: t.slice(Math.max(0, i - 300), Math.max(0, i - 300) + 2200) };
  }
  return null;
}

// ---------- The whole research pass ----------

function researchStore_(S, lead, homePage) {
  const base = String(lead.website).trim().replace(/^https?:\/\//i, '').replace(/\/.*$/, '');
  const host = cleanDomain_(base);
  const ev = [], social = [];
  let pdpUrl = '', pdpHtml = '';

  // Catalogue (Shopify only).
  let products = [];
  const pj = get_('https://' + base + '/products.json?limit=250');
  if (pj.code === 200) { try { products = JSON.parse(pj.text).products || []; } catch (e) {} }

  const restricted = restricted_(textOf_(homePage.html).slice(0, 8000) + ' ' + products.slice(0, 50).map(p => p.title + ' ' + (p.product_type || '')).join(' '));
  if (restricted) return { big: true, bigReasons: ['restricted or high-risk category, never emailed: ' + restricted], evidence: [], social: [], pdpUrl: '' };
  const big = bigBrand_(S, host, homePage.html, products.length);
  if (big.big) return { big: true, bigReasons: ['big brand: ' + big.reasons.join('; ')], evidence: [], social: [], pdpUrl: '' };
  ev.push('[MEASURED] size check: ' + (big.reasons.join('; ') || 'no big-brand signals'));

  if (products.length) {
    const n = products.length, nTxt = n >= 250 ? '250+' : String(n);
    const prices = [];
    products.forEach(p => (p.variants || []).forEach(v => { const x = Number(v.price); if (x > 0) prices.push(x); }));
    prices.sort((a, b) => a - b);
    const types = {};
    products.forEach(p => { const t = String(p.product_type || '').trim(); if (t) types[t] = (types[t] || 0) + 1; });
    const topTypes = Object.keys(types).sort((a, b) => types[b] - types[a]).slice(0, 5).map(t => t + ' (' + types[t] + ')');
    const soldOut = products.filter(p => (p.variants || []).length && p.variants.every(v => v.available === false));
    const oneImg = products.filter(p => (p.images || []).length <= 1);
    ev.push('[MEASURED] catalogue: ' + nTxt + ' products; prices ' + (prices.length ? prices[0] + ' to ' + prices[prices.length - 1] + ', median ' + prices[Math.floor(prices.length / 2)] : 'unknown') +
      (topTypes.length ? '; product types: ' + topTypes.join(', ') : '') + '; examples: ' + products.slice(0, 6).map(p => p.title).join(', '));
    if (n >= 4 && soldOut.length / n >= 0.25) ev.push('[MEASURED] ' + soldOut.length + ' of ' + nTxt + ' products sold out in every variant');
    if (n >= 3 && oneImg.length / n >= 0.3) ev.push('[MEASURED] ' + oneImg.length + ' of ' + nTxt + ' products have one photo or none');
    const newest = products.map(p => new Date(p.published_at || p.created_at)).filter(d => !isNaN(d)).sort((a, b) => b - a)[0];
    if (newest) ev.push('[MEASURED] newest product published ' + Utilities.formatDate(newest, 'UTC', 'yyyy-MM-dd'));

    // One real product page: an in-stock product with the most photos.
    const pick = products.filter(p => soldOut.indexOf(p) === -1).sort((a, b) => (b.images || []).length - (a.images || []).length)[0] || products[0];
    pdpUrl = 'https://' + base + '/products/' + pick.handle;
    try {
      const pg = fetchPage_(pdpUrl);
      if (pg.ok) {
        pdpHtml = pg.html;
        const t = textOf_(pg.html);
        ev.push('[SEEN] product page ' + pdpUrl + ' ("' + pick.title + '"): ' + (pick.images || []).length + ' photos, description ' + textOf_(pick.body_html).split(/\s+/).filter(String).length + ' words, ' +
          (pick.variants || []).length + ' variants' + ((pick.options || []).length ? ' (options: ' + pick.options.map(o => o.name).join(', ') + ')' : '') +
          '. Visible page text starts: "' + t.slice(0, 1200) + '"');
        if (/\b0 reviews?\b|no reviews yet|be the first to review/i.test(t)) ev.push('[SEEN] product page shows no reviews yet');
      }
    } catch (e) { /* product page unreachable */ }
  } else {
    ev.push('[SEEN] no public Shopify catalogue (/products.json closed or not a Shopify store); only the homepage was read');
  }

  const sp = (Date.now() - (S._started || Date.now()) < 3 * 60 * 1000) ? speedCheck_(S, pdpUrl || ('https://' + base)) : '';   // skipped late in a run (Apps Script's 6 minute limit)
  if (sp) ev.push(sp);

  let linkItems = [];
  if (Date.now() - (S._started || Date.now()) < 3 * 60 * 1000) {   // skipped late in a run (Apps Script's 6 minute limit)
    try {
      const lk = linkCheck_(S, base, [{ html: homePage.html, name: 'homepage' }].concat(pdpHtml ? [{ html: pdpHtml, name: 'product page' }] : []));
      if (lk.line) { ev.push(lk.line); linkItems = lk.items; }
      else if (lk.checked) ev.push('[MEASURED] link check: ' + lk.checked + ' homepage and product page links clicked, none broken and none sent back to the homepage');
    } catch (e) { /* link check is a bonus, never blocks research */ }
  }

  const f = funnel_(base, host, homePage.html, pdpHtml);
  f.ev.forEach(x => ev.push(x));

  const about = aboutText_(base);
  if (about) ev.push('[SEEN] about page ' + about.path + ': "' + about.text + '"');
  else ev.push('[SOFT] no about or founder page found');

  // The brand's own social links on the site.
  const links = socialLinks_(homePage.html + ' ' + pdpHtml);
  Object.keys(links).forEach(k => social.push(k + ': ' + links[k]));
  if (links.instagram) { const ig = instagram_(S, links.instagram); if (ig) social.push(ig); }
  if (links.linkedin) social.push('LinkedIn page found (not read: LinkedIn needs a login). Use it only to know they are on LinkedIn.');
  const avail = products.filter(p => (p.variants || []).some(v => v.available !== false));
  return { big: false, evidence: ev, social: social, pdpUrl: pdpUrl, hasPresell: f.hasPresell, links: linkItems, base: base,
    pages: { home: textOf_(homePage.html).slice(0, 6000), pdp: textOf_(pdpHtml).slice(0, 9000), about: about ? about.text : '' },
    stock: products.length ? { total: products.length, available: avail.length, soldOut: products.filter(p => avail.indexOf(p) === -1).map(p => p.title) } : null };
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
  'You are Ridwan\'s CRO strategist (Shopify CRO, Liquid developer, builds direct-response pages in Replo). You read real evidence about ONE small online store and decide whether there is a project worth pitching, and which one. Use ONLY the data given. Never guess.',
  'Evidence labels: [MEASURED] = a count from the store\'s own data. [SEEN] = actually present on a named page. [SOFT] = NOT found; it may be elsewhere (an advertorial on another domain, a post-purchase offer inside checkout, an app that loads later). A SOFT gap is never stated as fact: in the email it becomes a question ("is cold traffic going straight to the product page, or is there a pre-sell page I missed?").',
  'First understand the business: what they sell, price point, who buys, whether it is consumable or repeat-buy, how they get customers (ad pixels, social), what they already have in their funnel. Then pick ONE offer from this list, the one with the strongest evidence and the biggest likely effect on sales for THIS kind of business:',
  '- page_rebuild: a money page (product page or homepage first screen) with a verified, serious conversion problem that needs a redesign, not a tweak.',
  '- advertorial or listicle: a direct-response pre-sell page built in Replo for cold ad traffic. Strong when they have ad pixels, a product that needs explaining or has a story, and no pre-sell page was found.',
  '- post_purchase: a post-purchase upsell or thank-you page offer. Strong when products are consumable or have natural add-ons and no upsell app is visible.',
  '- bundle_builder: a build-your-own bundle page (Ridwan built one for Champion Biotics). Strong for consumables, supplements, food, skincare, pet, or several related products at one price point.',
  '- quiz: a product finder quiz. Strong when there are many similar products and buyers must choose (skincare by skin type, supplements by goal).',
  '- subscription: subscribe and save. Strong for consumables with no subscription app.',
  '- speed: the store is obviously slow on phones. ONLY when the evidence has a [SPEED] line; quote its numbers exactly and say it is Google\'s own measurement. Strong when they run ads (every paid click waits).',
  '- broken_links: ONLY when the evidence has a [LINKS] line (the links were clicked and each failure confirmed twice). A menu item, homepage button or product-page link that ends on a 404, or that sends the visitor back to the homepage, is something any shopper can click and see in ten seconds. Score 4 when it is in the header menu, a homepage button or a product link; 3 when it is only in the footer. The offer is a full link and navigation check across the whole buy path (the homepage is only where you looked) plus the fixes, never a ten minute patch. If a bigger offer fits this store better, use broken_links as the SECOND problem (it makes a strong step 2 or step 3), not the first.',
  '- custom_feature: a specific custom Shopify feature this business type needs (a configurator, a sample pack flow, a shorter checkout path); name it exactly.',
  'NEVER claim a page lacks something or leaves a doubt unanswered unless the evidence includes that page\'s visible text and it is truly absent there. A worry typical for the niche ("buyers of X usually wonder Y") is not evidence. Stock levels (sold-out items) are a supply decision, not a project: at most a supporting detail.',
  'NEVER pick a price amount, a sale or compare-at price, or how prices are shown (Shopify converts prices per visitor country and themes hide compare-at prices). NEVER build a point from menu or navigation link text (a "Stockholm Store" link is just a link). Not even as supporting details.',
  'NEVER pick language, translation, currency, price display, country or market differences (stores adapt these to where the visitor browses from, and research browses from Google servers abroad, so what it sees is not what their customers see). Not even as a supporting detail.',
  'NOT worth an email: anything a founder fixes in minutes (add a size chart, upload another photo, write a description, hide sold-out items, a typo); taste (colours, fonts); page speed or load time UNLESS there is a [SPEED] evidence line (no [SPEED] line means the store is not obviously slow, so speed is never mentioned); generic advice ("improve conversions", "add trust"). Those can be a supporting detail, never the reason.',
  'Decision maker: from the About page text, the founder or owner\'s name and role if the text states it (never guess a name). Team: "solo" if the text reads as one person, "small" for a few named people, "larger" if it mentions a team, departments or many staff, else "unknown".',
  'Score worth 1 to 5. 5: a clear project (page or feature to build) that fits how this business sells, backed by MEASURED or SEEN evidence. 4: a good project with slightly weaker evidence. 3: plausible but generic for the niche. 1 or 2: small fixes, guesses or soft gaps only. Be strict: an honest 2 is better than a dressed-up 4.',
  'Output JSON only: {"what_they_sell":"one short line","audience":"who buys, one short line","niche":"2 to 3 words","business":"one line: how they make money, price point, consumable or not, how they get customers","signal":"one line: why they fit","site_notes":"2 to 4 short, true observations",' +
  '"decision_maker":{"name":"First Last or empty","role":"Founder, Owner, CEO... or empty","basis":"the words in the about text, or empty"},"team":"solo|small|larger|unknown",' +
  '"offer":"page_rebuild|speed|broken_links|advertorial|listicle|post_purchase|bundle_builder|quiz|subscription|custom_feature","problem":"one sentence a founder would recognise: what is happening in their store or funnel and what the shopper or the ad click runs into","problem_evidence":"the exact evidence lines it rests on, with their labels","problem_page":"url",' +
  '"cost":"one line, what it costs them in plain words, no numbers","fix":"one line: exactly what Ridwan would build for them","worth":1-5,"second":{"offer":"...","problem":"a different angle for a follow-up","evidence":"labelled evidence","worth":1-5} or null,"rejected":"weaker points you considered and why not"}',
].join('\n');

/** A sequence may be written only when the store has an offer worth emailing about (agencies and no-website leads are exempt). */
function problemOk_(lead, profile, S) {
  if (['partner', 'build', 'launch'].indexOf(lc_(lead.track)) !== -1 || !String(lead.website).trim()) return true;   // Launch: the timing is the reason
  if (hasRedesign_(lead)) return true;   // 2026-10-26: a full redesign of their page is already built, that is the reason to talk
  if (!profile || profile.problem_worth === undefined) return true;   // Profiles tab not upgraded yet: old behaviour
  return Number(profile.problem_worth || 0) >= Number(S.MIN_PROBLEM_SCORE || 4);
}

/** A shared inbox or ticket desk rather than a person. */
function sharedInbox_(email) {
  return /^(hello|hi|hey|info|contact|team|shop|store|sales|support|help|care|service|orders?|customer|customerservice|customercare|admin|enquiries|enquiry|general|mail|office|hola|wholesale)$/i.test(String(email || '').split('@')[0]);
}

/** Likely addresses for a named person at a domain. */
function nameEmails_(name, host) {
  const parts = String(name || '').toLowerCase().replace(/[^a-z ]/g, '').split(/\s+/).filter(String);
  if (!parts.length || !host) return [];
  const f = parts[0], l = parts.length > 1 ? parts[parts.length - 1] : '';
  return [f + '@' + host].concat(l ? [f + '.' + l + '@' + host, f + l + '@' + host, f[0] + l + '@' + host] : []);
}

/**
 * The lead's email is a shared inbox (info@, support@...) and research found the decision maker's name. Try the founder's own
 * address (Hunter first if keyed, then name patterns), verify, and swap it in when valid. The shared inbox stays in notes.
 */
function upgradeToDecisionMaker_(S, leads, lead, name, role) {
  if (!name) return '';
  if (!String(lead.contact_name || '').trim()) set_(leads, lead, 'contact_name', name);
  if (!sharedInbox_(lead.email) || true) return '';   // 2026-10-30: a guessed personal address cannot be proven without a paid verifier, so the shared inbox stays
  const host = cleanDomain_(lead.website);
  const first = name.toLowerCase().split(/\s+/)[0];
  const hunter = hunterEmails_(host).filter(h => (h.name && h.name.toLowerCase().indexOf(first) !== -1) || /founder|owner|ceo|chief|director|president/i.test(h.position)).map(h => h.email);
  const cands = hunter.concat(nameEmails_(name, host)).filter((x, i, a) => a.indexOf(x) === i && x !== lc_(lead.email)).slice(0, 4);
  for (const c of cands) {
    const v = verifyOne_(c);
    if (!v) return 'verifier did not answer';
    if (v === 'valid') {
      set_(leads, lead, 'notes', ('Decision maker: ' + name + (role ? ' (' + role + ')' : '') + '. Email moved from shared inbox ' + lead.email + ' to ' + c + ' (verifier: valid)' + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
      set_(leads, lead, 'email', c);
      set_(leads, lead, 'email_status', 'valid');
      return 'now emailing ' + name + ' at ' + c;
    }
    if (v === 'catch-all') return 'domain accepts every address, kept ' + lead.email;
  }
  return 'no verified personal address for ' + name + ', kept ' + lead.email;
}

/** Menu: test phase helper. Unsent leads get fresh research and a fresh sequence on the next run. Sent emails are never touched. */
function redoUnsentLeads() {
  const ui = SpreadsheetApp.getUi();
  if (ui.alert('Redo research and emails for leads that have not been emailed yet?', 'Their Draft sequence rows become Superseded and their research is cleared. Nothing already sent changes.', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  const leads = read_('Leads'), seq = read_('Sequence'), prof = read_('Profiles');
  const unsent = {};
  leads.rows.filter(l => l.lead_id && Number(l.touch_count || 0) === 0 && ['New', ''].indexOf(String(l.stage)) !== -1).forEach(l => {
    unsent[String(l.lead_id)] = true;
    if (isTrue_(l.approved)) set_(leads, l, 'approved', false);
  });
  let n = 0;
  seq.rows.filter(r => unsent[String(r.lead_id)] && r.status === 'Draft').forEach(r => { set_(seq, r, 'status', 'Superseded'); n++; });
  if (prof.headers.indexOf('problem_worth') !== -1) prof.rows.filter(p => unsent[String(p.lead_id)]).forEach(p => set_(prof, p, 'problem_worth', ''));
  toast_(Object.keys(unsent).length + ' unsent lead(s) reset (' + n + ' draft emails superseded, approvals cleared). Run Prepare new leads now.');
}

// ---------- Is the site still a live store? (2026-10-07) ----------
// Directory lists can be months old. framelo.com was emailed while it redirected to a domain-for-sale page.

const PARKED_HOSTS_ = /brandsly|afternic|sedo\.|dan\.com|hugedomains|godaddy|squadhelp|atom\.com|undeveloped|parkingcrew|bodis|sav\.com|porkbun|namecheap|domainmarket|buydomains|epik\.com|uniregistry|parklogic|above\.com|dynadot/i;
const DEAD_TEXT_ = /domain (is|may be) for sale|buy this domain|this domain is parked|parked free|this store is unavailable|this shop is currently unavailable|store is closed|shop is closed|account (has been )?suspended|website (is )?(expired|suspended)|site not found|no longer (available|in business|operating)/i;
// Pre-launch is NOT dead (Ridwan, 2026-10-07): a password or coming-soon page means they are building right now. Track Launch.
const PASSWORD_PAGE_ = /<form[^>]+storefront_password|password-page|action=["']\/password["']/i;
const PRELAUNCH_TEXT_ = /coming soon|opening soon|launching soon|under construction|something (big|exciting) is coming|stay tuned|be the first to know/i;

/**
 * Follows redirects by hand (Apps Script hides the final URL) and decides whether the site is a live store.
 * Returns { active, why, finalHost }. Not active: 4xx/5xx, unreachable, a redirect to a domain marketplace or parking page,
 * a redirect to a different domain (store moved: needs a human look), a parked/for-sale/closed page, or no shop at all.
 * A password or coming-soon page IS active, with prelaunch: true (they are building the store right now: track Launch).
 */
function siteStatus_(website) {
  let url = 'https://' + cleanDomain_(website) + '/';
  const startStem = cleanDomain_(website).replace(/\.(co|com|org|net)\.[a-z]{2}$|\.[a-z]{2,}$/, '').split('.').pop();
  for (let hop = 0; hop < 6; hop++) {
    let res;
    try { res = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: false, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KoolestproBot/1.0)' } }); }
    catch (e) { return { active: false, why: 'unreachable (' + String(e.message || e).slice(0, 80) + ')', finalHost: cleanDomain_(url) }; }
    const code = res.getResponseCode();
    const host = cleanDomain_(url);
    if (code >= 300 && code < 400) {
      const h = res.getAllHeaders();
      const loc = h.Location || h.location;
      if (!loc) return { active: false, why: 'redirect with no target', finalHost: host };
      url = /^https?:\/\//i.test(loc) ? loc : 'https://' + host + (loc.charAt(0) === '/' ? '' : '/') + loc;
      if (PARKED_HOSTS_.test(cleanDomain_(url))) return { active: false, why: 'redirects to a domain-for-sale or parking page (' + cleanDomain_(url) + ')', finalHost: cleanDomain_(url) };
      continue;
    }
    const finalHost = host, finalStem = finalHost.replace(/\.(co|com|org|net)\.[a-z]{2}$|\.[a-z]{2,}$/, '').split('.').pop();
    if (code >= 400) return { active: false, why: 'site returns HTTP ' + code, finalHost: finalHost };
    if (finalStem !== startStem && !/myshopify\.com$/.test(finalHost)) return { active: false, why: 'redirects to a different domain (' + finalHost + '): store moved or sold, check by hand', finalHost: finalHost };
    const html = res.getContentText().slice(0, 300000), text = textOf_(html).slice(0, 4000);
    if (DEAD_TEXT_.test(text)) return { active: false, why: 'page says: "' + (text.match(DEAD_TEXT_) || [''])[0] + '"', finalHost: finalHost };
    // A password page is proof. "Coming soon" wording only counts on a small page with no shop (live stores say "new drop coming soon").
    if (PASSWORD_PAGE_.test(html) || /\/password$/.test(url) || (PRELAUNCH_TEXT_.test(text) && textOf_(html).length < 2500 && !/add[\s_-]?to[\s_-]?(cart|bag)|\/products\//i.test(html))) return { active: true, prelaunch: true, why: 'pre-launch: password or coming-soon page (building now)', finalHost: finalHost, html: html };
    if (text.length < 300 && !/add to (cart|bag)|shop|products?/i.test(text)) return { active: false, why: 'almost empty page (' + text.length + ' characters of text)', finalHost: finalHost };
    return { active: true, why: 'live (HTTP ' + code + ')', finalHost: finalHost };
  }
  return { active: false, why: 'too many redirects', finalHost: cleanDomain_(url) };
}

// ---------- Pre-launch stores: what can be offered (2026-10-07) ----------
// Nothing behind the password can be seen, so the observation comes only from the coming-soon page itself and their socials.
// Offers, in order of fit: (1) finish or build the store for launch, (2) a free pre-launch review of their store if they share
// the password, (3) a proper coming-soon / waitlist page that collects emails, (4) launch ad creatives from their product photos.

function launchFacts_(html, base) {
  const t = textOf_(html).slice(0, 2500);
  const facts = [];
  facts.push('[SEEN] coming-soon or password page text: "' + t + '"');
  const signup = /contact\[email\]|customer\[email\]|type=["']email["']|klaviyo|newsletter|sign ?up|subscribe|join (the )?(list|waitlist)|notify me/i.test(html);
  facts.push(signup ? '[SEEN] the page has an email signup (waitlist or newsletter)' : '[SEEN] no email signup form on the page: visitors before launch have no way to hear when it opens');
  const date = (t.match(/\b(launch(ing)?|opening|open|live|drops?)\b[^.]{0,40}\b(\d{1,2}(st|nd|rd|th)?\s+\w+|\w+\s+\d{1,2}(st|nd|rd|th)?|20\d\d|this (week|month)|next (week|month)|soon)\b/i) || [])[0];
  if (date) facts.push('[SEEN] launch timing mentioned: "' + date + '"');
  // The theme name is deliberately NOT a fact (2026-10-17): gromix.shop was told "the stock Dawn theme leaves the selling to the
  // default layout". Nothing behind the password can be seen, so a verdict on the theme or layout is a guess.
  return facts;
}

const LAUNCH_PROFILE_SYS_ = [
  'You profile a store that is NOT open yet: it shows a password or coming-soon page, so the founder is building it right now. Use ONLY the data given. Never claim anything about the store behind the password, its products, design, theme, layout or pages: nobody can see them. Never name or judge their theme (Dawn, Debut or any other).',
  'Pick ONE offer that fits what you can see: launch_build (help finish or build the store so it launches properly: product pages, homepage, theme setup), launch_review (a free pre-launch review of their product page if they share the store password; low friction, best default), waitlist_page (only if the page has NO email signup: a coming-soon page that collects emails before launch), launch_creatives (ad creatives from their product photos for launch, when their socials show products).',
  'The problem is about timing, not a flaw: they are about to launch, and the first visitors decide fast. Only state what is SEEN (for example no email signup on the coming-soon page, a launch date). Never invent a launch date or products.',
  'Output JSON only: {"what_they_sell":"one short line, or unknown","audience":"one short line, or unknown","niche":"2 to 3 words","business":"one line","signal":"pre-launch: building the store now","site_notes":"1 to 3 true observations from the coming-soon page and socials","decision_maker":{"name":"","role":"","basis":""},"team":"solo|small|larger|unknown","offer":"launch_build|launch_review|waitlist_page|launch_creatives","problem":"one sentence about their launch moment, from what is seen","problem_evidence":"labelled evidence","problem_page":"url","cost":"one plain line","fix":"one line: exactly what Ridwan would do","worth":1-5,"second":{"offer":"...","problem":"...","evidence":"...","worth":1-5} or null}',
].join('\n');

// ---------- Is the email theirs? (2026-10-07) ----------
// Directories often list a Gmail or an old agency address. A free-mail or other-domain address is kept only when the store
// publishes it on its own site; otherwise an address from the site replaces it, or the lead is flagged for a human look.

const FREEMAIL_ = /@(gmail|googlemail|yahoo|ymail|outlook|hotmail|live|msn|icloud|me|aol|proton|protonmail|gmx|mail|yandex|zoho)\./i;
const UNCONFIRMED_TAG_ = '[UNCONFIRMED RECIPIENT]';

function isOwnDomain_(email, host) {
  const dom = lc_(String(email).split('@')[1] || ''), h = cleanDomain_(host);
  const stem = d => d.replace(/\.(co|com|org|net|ac|gov)\.[a-z]{2}$|\.[a-z]{2,}$/, '').split('.').pop();
  return !!dom && !!h && (dom === h || dom.endsWith('.' + h) || h.endsWith('.' + dom) || (stem(dom).length > 3 && stem(dom) === stem(h)));
}

/** Returns a short note, and fixes or flags the lead. Only for leads with a website (Maps leads without one keep their Maps email). */
function recipientCheck_(S, leads, lead) {
  const email = lc_(lead.email), host = cleanDomain_(lead.website);
  if (!email || !host || isOwnDomain_(email, host)) return '';
  const site = siteEmails_(lead.website);
  if (site.indexOf(email) !== -1) return 'recipient ok: ' + email + ' is published on their own site';
  const cands = site.filter(e => e !== email).sort((a, b) => (isOwnDomain_(b, host) ? 1 : 0) - (isOwnDomain_(a, host) ? 1 : 0) || rankEmail_(b, host, lead.contact_name) - rankEmail_(a, host, lead.contact_name));
  for (const c of cands.slice(0, 3)) {
    const v = verifyOne_(c, lead.website);
    if (v === 'valid' || (v === 'catch-all' && isTrue_(S.SEND_TO_CATCH_ALL))) {
      set_(leads, lead, 'notes', ('Recipient fixed: ' + email + ' (from a directory, not on their site) replaced by ' + c + ' (published on ' + host + ', verifier: ' + v + ')' + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
      set_(leads, lead, 'email', c);
      set_(leads, lead, 'email_status', v);
      return 'recipient fixed: now ' + c;
    }
  }
  if (String(lead.notes || '').indexOf(UNCONFIRMED_TAG_) === -1)
    set_(leads, lead, 'notes', (UNCONFIRMED_TAG_ + ' ' + email + ' is ' + (FREEMAIL_.test(email) ? 'a free-mail address' : 'on another domain') + ' and is not published on ' + host + '. Confirm it belongs to the owner before approving.' + (lead.notes ? ' | ' + lead.notes : '')).slice(0, 900));
  return 'recipient unconfirmed: ' + email + ' not found on ' + host;
}


// ---------- Test sends never count as progress (2026-10-17, Ridwan) ----------
// While TEST_MODE is TRUE every email goes to ALERT_EMAIL with "[TEST to <lead email>]" at the start of its subject, so the lead never
// got it. Messages keeps that subject, which is the proof. A lead whose outgoing emails are ALL test emails has made no real progress:
// this puts it back at the start (stage New, touch 0, no thread, unsent sequence, approval removed, fake reply drafts and memory cleared)
// so its real first email goes out once you tick approved. A lead with even ONE real outgoing email is never touched, so real progress
// is kept however many times TEST_MODE is switched. Safe to run any number of times. sendDue runs it by itself when TEST_MODE is FALSE.

const TEST_SUBJECT_ = /^\s*\[TEST to /i;

function resetTestSendsMenu() {
  const ui = SpreadsheetApp.getUi();
  const plan = resetTestSends_(true);
  if (!plan.leads.length) { ui.alert('Reset test sends', 'Nothing to reset. Every lead that has been emailed got at least one real email, or none was sent in test mode.', ui.ButtonSet.OK); return; }
  if (ui.alert('Reset test sends?', plan.leads.length + ' lead(s) only ever received TEST emails (they went to your inbox, not to the lead). They go back to the start and approval is removed. Leads with a real email are not touched. Continue?', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  const done = resetTestSends_(false);
  ui.alert('Reset test sends', done.leads.length + ' lead(s) reset, ' + done.seqRows + ' sequence email(s) set back to Draft, ' + done.drafts + ' reply draft(s) discarded. Tick approved again on the leads you want sent.', ui.ButtonSet.OK);
}

/** dryRun true = only report. Returns { leads, seqRows, drafts }. */
function resetTestSends_(dryRun) {
  const leads = read_('Leads'), msgs = read_('Messages'), seq = read_('Sequence'), drafts = read_('Drafts');
  const testOut = {}, realOut = {};
  msgs.rows.filter(m => lc_(m.direction) === 'out').forEach(m => {
    const id = String(m.lead_id);
    if (TEST_SUBJECT_.test(String(m.subject || ''))) testOut[id] = true; else realOut[id] = true;
  });
  const STARTED = ['contacted', 'finished', 'replied', 'talking'];
  const hit = leads.rows.filter(l => {
    const id = String(l.lead_id);
    if (/^test-/i.test(id)) return false;   // the sample lead is handled by Create / reset test lead
    if (realOut[id] || !testOut[id]) return false;
    return Number(l.touch_count || 0) > 0 || STARTED.indexOf(lc_(l.stage)) !== -1 || !!l.thread_id;
  });
  const ids = {}; hit.forEach(l => { ids[String(l.lead_id)] = true; });
  const seqHit = seq.rows.filter(r => ids[String(r.lead_id)] && (r.status === 'Sent' || r.status === 'Stopped'));
  const draftHit = drafts.rows.filter(d => ids[String(d.lead_id)] && ['Needs draft', 'Ready for review', 'Approved'].indexOf(String(d.status)) !== -1);
  const out = { leads: hit.map(l => String(l.lead_id)), seqRows: seqHit.length, drafts: draftHit.length };
  if (dryRun || !hit.length) return out;

  hit.forEach(l => {
    ['sender', 'last_touch_at', 'next_touch_at', 'thread_id', 'first_message_id', 'subject'].forEach(f => set_(leads, l, f, ''));
    set_(leads, l, 'touch_count', 0);
    set_(leads, l, 'stage', 'New');
    set_(leads, l, 'approved', false);
    set_(leads, l, 'notes', ('RESET: only test emails had been sent; back at step 1, approval removed ' + Utilities.formatDate(new Date(), tz_(), 'd MMM') + (l.notes ? ' | ' + l.notes : '')).slice(0, 900));
  });
  seqHit.forEach(r => { set_(seq, r, 'status', 'Draft'); set_(seq, r, 'sent_at', ''); });
  draftHit.forEach(d => set_(drafts, d, 'status', 'Discarded'));
  try {
    const mem = read_('Memory');
    mem.rows.filter(m => ids[String(m.lead_id)]).forEach(m => { set_(mem, m, 'summary', ''); });
  } catch (e) { /* no Memory tab yet */ }
  return out;
}

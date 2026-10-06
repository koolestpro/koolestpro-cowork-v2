/**
 * Koolestpro Outreach: store research (2026-10-06, Ridwan's feedback on the first test emails).
 *
 * A lead is only emailed when there is a tangible reason: a project worth paying for, tied to how this business sells.
 * Not a small fix they could do in ten minutes, and never a speed claim. Big brands are skipped outright.
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

function textOf_(html) {
  return String(html || '').replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ')
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

  const big = bigBrand_(S, host, homePage.html, products.length);
  if (big.big) return { big: true, bigReasons: big.reasons, evidence: [], social: [], pdpUrl: '' };
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
          '. Page text starts: "' + t.slice(0, 400) + '"');
        if (/\b0 reviews?\b|no reviews yet|be the first to review/i.test(t)) ev.push('[SEEN] product page shows no reviews yet');
      }
    } catch (e) { /* product page unreachable */ }
  } else {
    ev.push('[SEEN] no public Shopify catalogue (/products.json closed or not a Shopify store); only the homepage was read');
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
  return { big: false, evidence: ev, social: social, pdpUrl: pdpUrl, hasPresell: f.hasPresell };
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
  '- custom_feature: a specific custom Shopify feature this business type needs (a configurator, a sample pack flow, a shorter checkout path); name it exactly.',
  'NOT worth an email: anything a founder fixes in minutes (add a size chart, upload another photo, write a description, hide sold-out items, a typo); taste (colours, fonts); page speed or load time in any form; generic advice ("improve conversions", "add trust"). Those can be a supporting detail, never the reason.',
  'Decision maker: from the About page text, the founder or owner\'s name and role if the text states it (never guess a name). Team: "solo" if the text reads as one person, "small" for a few named people, "larger" if it mentions a team, departments or many staff, else "unknown".',
  'Score worth 1 to 5. 5: a clear project (page or feature to build) that fits how this business sells, backed by MEASURED or SEEN evidence. 4: a good project with slightly weaker evidence. 3: plausible but generic for the niche. 1 or 2: small fixes, guesses or soft gaps only. Be strict: an honest 2 is better than a dressed-up 4.',
  'Output JSON only: {"what_they_sell":"one short line","audience":"who buys, one short line","niche":"2 to 3 words","business":"one line: how they make money, price point, consumable or not, how they get customers","signal":"one line: why they fit","site_notes":"2 to 4 short, true observations",' +
  '"decision_maker":{"name":"First Last or empty","role":"Founder, Owner, CEO... or empty","basis":"the words in the about text, or empty"},"team":"solo|small|larger|unknown",' +
  '"offer":"page_rebuild|advertorial|listicle|post_purchase|bundle_builder|quiz|subscription|custom_feature","problem":"one sentence a founder would recognise: what is happening in their store or funnel and what the shopper or the ad click runs into","problem_evidence":"the exact evidence lines it rests on, with their labels","problem_page":"url",' +
  '"cost":"one line, what it costs them in plain words, no numbers","fix":"one line: exactly what Ridwan would build for them","worth":1-5,"second":{"offer":"...","problem":"a different angle for a follow-up","evidence":"labelled evidence","worth":1-5} or null,"rejected":"weaker points you considered and why not"}',
].join('\n');

/** A sequence may be written only when the store has an offer worth emailing about (agencies and no-website leads are exempt). */
function problemOk_(lead, profile, S) {
  if (lc_(lead.track) === 'partner' || lc_(lead.track) === 'build' || !String(lead.website).trim()) return true;
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
  if (!sharedInbox_(lead.email) || !PropertiesService.getScriptProperties().getProperty('MYEMAILVERIFIER_API_KEY')) return '';
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

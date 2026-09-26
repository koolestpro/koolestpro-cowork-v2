# Funnel Discovery + Competitor Benchmarking

How to map a client's full funnel, discover hidden pages, scan ad libraries, and benchmark against competitors — before running the main audit.

---

## SITEMAP CRAWL

### Step 1 — Fetch the sitemap

```
GET [store-url]/sitemap.xml
```

Most Shopify stores have a nested sitemap index. Parse each child sitemap:
- `sitemap_products_1.xml` — all product pages
- `sitemap_collections_1.xml` — collection pages
- `sitemap_pages_1.xml` — custom pages (most interesting)
- `sitemap_blogs_1.xml` — blog posts used as pre-sell content

### Step 2 — Identify non-navigation pages

From `sitemap_pages_1.xml`, flag any page URL that:
- Is not linked from the main navigation
- Contains keywords like: `offer`, `lp`, `landing`, `advertorial`, `try`, `sale`, `bundle`, `quiz`, `free`, `deal`, `promo`
- Has a URL structure different from standard Shopify pages

These are paid traffic entry points, hidden offer pages, or test landing pages. Fetch and read each one.

### Step 3 — Robots.txt check

```
GET [store-url]/robots.txt
```

Note any `Disallow:` paths. Brands sometimes block crawlers from their high-converting landing pages, seasonal offer pages, or A/B test variants. Blocked = interesting.

### Step 4 — Try common hidden page patterns

If no hidden pages found in sitemap, probe manually:
```
/pages/advertorial
/pages/lp
/pages/offer
/pages/try-[product-name]
/pages/sale
/pages/bundle
/pages/quiz
/pages/landing
/pages/promo
```

A 200 response means the page exists. Fetch and read it.

---

## AD LIBRARY SCAN

### Meta Ad Library

URL: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=[brand-name]`

Search by brand name. For each active ad:
- Note the ad format (image, video, carousel)
- Read the copy and identify the hook / offer
- Click through (or note the destination URL from the ad preview)
- Fetch the landing page the ad points to

**What to look for:**
- Are they sending cold traffic directly to a PDP? (Gap — no pre-sell)
- Do they have a separate advertorial or landing page? (Existing asset to audit)
- Is the ad copy benefit-led or feature-led?
- Does the landing page match the ad's promise? (Message match)
- How many ads are running? (More ads = higher spend = more pressure on the landing page to convert)

### Google Ads Transparency Center

URL: `https://adstransparency.google.com/?region=anywhere&query=[brand-name]`

Same process as Meta. Note:
- Search ads vs. display ads vs. YouTube ads
- What landing pages Google traffic hits

### TikTok Creative Center

URL: `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en`

Search by brand name or industry. Less complete than Meta but useful for brands with younger demographics.

### If no ads found

No active ads is itself a finding:
- **If they have significant organic traffic:** not using paid = Tier 2 opportunity (what channels could they scale into?)
- **If they have low traffic:** no paid ads + weak organic = acquisition problem upstream from CRO — flag in the internal brief as context

---

## FUNNEL MAP

After collecting sitemap and ad library data, generate a visual funnel diagram.

### Format (text diagram for internal brief)

```
TRAFFIC SOURCES
├── Meta Ads ($X/mo estimated) ──→ [Advertorial /pages/offer] ──→ [PDP /products/x]
├── Google Ads ──────────────────→ [Homepage /] ──→ [Collection /collections/x] ──→ [PDP]
├── Organic (SEO) ────────────────→ [Blog /blogs/news/x] ──→ [PDP]
└── Email (Klaviyo) ─────────────→ [PDP] (direct)
                                              │
                                              ▼
                                         [Cart page]
                                              │
                                              ▼
                                      [Checkout flow]
                                              │
                                         ┌───┴───┐
                                    [Thank you]  [Post-purchase upsell?]
                                         │
                                    [Email flow?]
```

Mark each node:
- ✅ EXISTS + WORKING
- ⚠️ EXISTS + NEEDS AUDIT
- ❌ MISSING (opportunity)
- 🔴 BROKEN (critical issue)

### Gap flags (auto-elevate to findings)

| Gap | Classification |
|-----|---------------|
| Paid ads → Homepage (no dedicated landing page) | Tier 1 Critical |
| Paid ads → PDP with no pre-sell/warm-up | Tier 2 High |
| No post-purchase upsell page | Tier 2 High |
| No advertorial for cold traffic | Tier 2 Medium |
| No quiz/assessment funnel (multi-SKU store) | Tier 2 Medium |
| No abandoned cart email flow | Tier 2 Critical |
| Blog content exists but not in funnel | Tier 3 — content leverage opportunity |

---

## COMPETITOR BENCHMARKING

### How to select competitors

1. Use the client's brief (they often name them)
2. Search Google for `[product category] buy` and `[product category] best [year]` — top organic results are competitors
3. Check who's advertising in the Meta Ad Library for the same search terms
4. Ask Ridwan: "Who does this client compare themselves to?"

Aim for 2-3 competitors. One direct (same product, same price point), one aspirational (premium tier), one alternative (different approach to the same problem).

### What to audit per competitor

For each competitor, fetch their PDP and note:

**Above the fold:**
- Headline — benefit or feature led?
- Value proposition clarity (5-second test)
- Trust signals visible — star rating, review count, badges
- CTA copy and position
- Urgency/scarcity signals

**Offer structure:**
- Price and compare-at price
- Guarantee visibility and strength
- Free shipping threshold communicated?
- Payment options (Shop Pay, Klarna, etc.)

**Social proof:**
- Review count and star rating (exact numbers)
- Review placement — above or below fold?
- Photo reviews / UGC?
- Press mentions or awards?

**Funnel:**
- Do they have a pre-sell page / advertorial?
- What does their ad creative look like?
- Do they have a quiz or bundle page?
- What post-purchase upsell exists?

### Benchmark output format

```
COMPETITOR BENCHMARKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Competitor 1 — Direct]
URL: [url]
Above-fold trust: [rating] ([N] reviews visible above fold)
CTA copy: "[exact copy]"
Guarantee: [X]-day money back, [prominence]
Key advantage over client: [specific]
Key weakness vs client: [specific]

[Competitor 2 — Aspirational]
...

BENCHMARK GAPS (client vs market)
[Specific areas where client is behind —
stated as evidence in Tier 1/2 findings]
```

Use these gaps directly as evidence in the audit report. Never say "you should add more reviews" — say "your top competitor displays 1,247 reviews above the fold. Your 34 reviews are hidden below the product description."

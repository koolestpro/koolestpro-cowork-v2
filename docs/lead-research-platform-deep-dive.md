# Lead Research Platform Deep Dive — Koolestpro Outbound Stack

**Research date:** 2026-08-31  
**Goal:** Find the best pay-as-you-go/API-accessible platforms for discovering: (a) businesses with no website, especially social-native sellers on Instagram/TikTok, (b) Shopify/poor-website stores needing CRO, and (c) businesses showing active intent for web development services.

---

## Quick Verdict

**There is no single platform that does everything.** The landscape splits into three layers:

| Layer | Best Tool(s) | Cost |
|---|---|---|
| **Discovery** (find the businesses) | Outscraper + Apify + custom social scraping | ~$0.001–$0.003/lead |
| **Enrichment** (get contact info) | Hunter + Prospeo + People Data Labs | ~$0.01–$0.05/lead |
| **Intent** (know they need you now) | Job boards + G2/Capterra + custom web monitoring | Free to ~$0.10/lead |

**LeadX is the closest to an all-in-one** for your exact use case — it finds no-website local businesses, auto-builds sample sites, and sends pitches. But it is not a generic API you wire into your own workflow; it is a closed product.

**Your custom AI agent approach is the right long-term play.** It beats every off-the-shelf tool for social-native discovery because nobody has reliable API coverage of Instagram/TikTok-only sellers.

---

## 1. Platform-by-Platform Analysis

### 1.1 LeadX — "The Closest to What You Want"

| | |
|---|---|
| **What it does** | Scans live map data for local businesses, scores digital gaps (no website, bad mobile site, no reviews), auto-builds a sample website from their real photos/reviews/hours, writes personalized pitches, sends by email/LinkedIn |
| **Pricing** | Free: 50 credits/mo; Pro: $129/mo (10K credits); Agency: $291/mo (50K credits) |
| **API?** | Yes — REST API + native MCP connection |
| **Pay-as-you-go?** | No — subscription, but free tier is genuinely usable |
| **Best for** | Local service businesses with no website (plumbers, salons, auto shops) |
| **Weakness** | Not designed for social-native sellers (Instagram/TikTok-only). Map-based discovery misses businesses that never claimed a Google Maps listing |

**Verdict:** If your target is local businesses in Lagos/Abuja/Accra that have a Maps presence but no website, LeadX is the fastest path to revenue. For Instagram/TikTok-only sellers, it will miss them entirely.

---

### 1.2 Outscraper — "Best Pay-as-You-Go Discovery Engine"

| | |
|---|---|
| **What it does** | Google Maps Scraper, Reviews Scraper, Emails & Contacts Scraper, Google Search Scraper, B2B Lead Generation Database, Yellow Pages Scraper, and 15+ other scrapers |
| **Pricing** | Truly pay-as-you-go. Google Maps: $0/500 businesses, then $3/1K. Emails & Contacts: $0/500 domains, then $3/1K. B2B Database: $2/1K businesses |
| **API?** | Yes — full REST API |
| **Pay-as-you-go?** | Yes — prepaid credits that never expire, OR postpaid monthly billing |
| **Best for** | High-volume discovery at the lowest cost per lead |
| **Weakness** | Still map/directory-based. Misses social-native sellers |

**Verdict:** Replace BrowserAct's Google Maps workflow with Outscraper's Maps API and you get better reliability, lower cost, and no per-run polling. ~$0.003 per business discovered. This is your new Discovery layer for anything map-based.

---

### 1.3 Apify — "Custom Scraping Infrastructure"

| | |
|---|---|
| **What it does** | Marketplace of 2,000+ pre-built scrapers (actors). You already use it for Meta Ad Library |
| **Pricing** | Pay per compute unit (~$0.40/compute hour). Most actors cost $0.01–$0.50/run |
| **API?** | Yes — start runs, poll status, read datasets programmatically |
| **Pay-as-you-go?** | Yes — prepaid credits |
| **Best for** | Any site that Outscraper does not cover. Instagram profile scrapers, TikTok scrapers, job board scrapers |
| **Weakness** | Fragile — site changes break actors. Instagram/TikTok actors get blocked regularly |

**Verdict:** Keep Apify for Meta Ad Library (already working) and add actors for: Instagram hashtag search, TikTok hashtag search, and job board scraping. Budget ~$5–$20 per 1,000 profiles scraped.

---

### 1.4 Hunter.io — "Best Email Discovery + Verification"

| | |
|---|---|
| **What it does** | Domain search (find all emails at a company), Email Finder (find one person's email), Email Verifier, TechLookup (find sites using specific tech) |
| **Pricing** | Free: 50 credits/mo; Starter: $34/mo (2K credits); Growth: $104/mo (10K credits) |
| **API?** | Yes — full REST API |
| **Pay-as-you-go?** | No — subscription, but credits roll for 12 months on annual plans |
| **Best for** | Finding verified emails for businesses you already discovered |
| **Weakness** | Only works when the business has a domain. Instagram-only sellers = no domain = no Hunter data |

**Verdict:** Use Hunter's **TechLookup** to find Shopify stores (search "Shopify" technology, filter by country). This is how you find existing Shopify stores with poor sites. For email discovery, Hunter is the most reliable verifier.

---

### 1.5 Prospeo — "Apollo Alternative with Better API Pricing"

| | |
|---|---|
| **What it does** | People & company search, email finder, mobile numbers, intent signals, API for enrichment |
| **Pricing** | Free trial; paid plans start around $49/mo. API available on all paid tiers |
| **API?** | Yes — search, enrich, verify endpoints |
| **Pay-as-you-go?** | Subscription-based |
| **Best for** | B2B enrichment at lower cost than Apollo |
| **Weakness** | Same as all B2B databases — weak coverage of African SMBs and social-native businesses |

**Verdict:** Cheaper than Apollo for the same data. Good for enriching international Shopify brands ($10–200K/mo segment) once you have their domain.

---

### 1.6 People Data Labs (PDL) — "Programmatic Data at Scale"

| | |
|---|---|
| **What it does** | 3B+ person profiles, 18M+ company profiles. Enrichment API, search API |
| **Pricing** | Free: 100 credits/mo; Starter: $99/mo (1K credits); Scale: $299/mo (5K credits); Enterprise: custom |
| **API?** | Yes — the product IS the API |
| **Pay-as-you-go?** | Subscription with annual discount |
| **Best for** | Enriching large lists programmatically. Best person-level data quality |
| **Weakness** | Expensive for small volumes. Weak on African SMB coverage |

**Verdict:** Overkill for your current volume. Consider only when you are pushing 500+ enrichment calls per month.

---

### 1.7 Clay — "The Orchestration Layer"

| | |
|---|---|
| **What it does** | Combines 200+ data providers into one workflow builder. Waterfall enrichment, AI research agents (Claygent), signals tracking |
| **Pricing** | Free: 500 actions/mo; Launch: $60/mo (15K actions); Growth: $205/mo (40K actions) |
| **API?** | Yes — HTTP API, MCP server, agent plugin CLI |
| **Pay-as-you-go?** | No — subscription, but you bring your own API keys for many providers |
| **Best for** | Orchestrating multiple data sources into one automated workflow |
| **Weakness** | Expensive. The value is in combining sources, not in owning the data itself |

**Verdict:** If you end up using 4+ separate tools, Clay becomes worth it as the glue. Until then, build your own orchestration in Python (what you already have with `browseract_koolestflow_bridge.py`).

---

### 1.8 Captain Data — "B2B Enrichment API"

| | |
|---|---|
| **What it does** | People enrichment, company enrichment, people search, company search, find employees |
| **Pricing** | 100 free credits; then ~$30/1K credits (Silver tier at 20K/mo volume) |
| **API?** | Yes — REST API + MCP |
| **Pay-as-you-go?** | Usage-based, no monthly minimum |
| **Best for** | LinkedIn-based B2B data |
| **Weakness** | LinkedIn-first. Not useful for social-native sellers |

**Verdict:** Skip for now. Your target market (Nigeria/Africa social-native sellers) is not in LinkedIn databases.

---

### 1.9 BuiltWith — "Technology Intelligence"

| | |
|---|---|
| **What it does** | Identifies what technologies websites use. 673M+ websites tracked |
| **Pricing** | Free limited lookups; Pro: $295/mo; Enterprise: custom |
| **API?** | Yes — REST API |
| **Pay-as-you-go?** | No — subscription |
| **Best for** | Finding Shopify stores, WooCommerce stores, poorly-optimized sites |
| **Weakness** | Only finds businesses that already HAVE a website. Misses no-website prospects entirely |

**Verdict:** Use Hunter's TechLookup (cheaper) or BuiltWith's free tier for occasional Shopify store discovery. Not a core tool.

---

### 1.10 Apollo.io — "The Giant (Wrong Fit for You)"

| | |
|---|---|
| **What it does** | 275M+ contacts, 60M+ companies. Database + sequencing + intent |
| **Pricing** | Free: 50 credits/mo; Starter: $49/mo (2K credits); Growth: $149/mo (10K credits) |
| **API?** | Yes — but only on Custom/Enterprise plans |
| **Pay-as-you-go?** | No |
| **Best for** | US/EU B2B SaaS sales |
| **Weakness** | API locked behind enterprise. Terrible African SMB coverage. Overkill for your model |

**Verdict:** Not a fit. Your market is not US B2B SaaS.

---

### 1.11 Seamless.AI — "Apollo Clone (Same Verdict)"

| | |
|---|---|
| **What it does** | B2B contact database + buyer intent + CRM enrichment |
| **Pricing** | Free: 50 credits; Pro: contact sales; Enterprise: custom |
| **API?** | Yes — on Enterprise |
| **Pay-as-you-go?** | No |
| **Weakness** | Same as Apollo — built for US enterprise sales, not African social sellers |

**Verdict:** Skip.

---

## 2. The Hard Problem: Instagram/TikTok-Only Sellers

**No existing platform reliably finds businesses that ONLY sell on Instagram/TikTok.** Here is why:

- **Google Maps** only captures businesses that claimed a listing
- **Ad Library** only captures businesses running paid ads
- **B2B databases** (Apollo, PDL, Cognism) only index businesses with websites/LinkedIn
- **Instagram/TikTok APIs** do not expose business discovery by category/location

### 2.1 What Actually Works (Manual but Proven)

| Method | How | Yield |
|---|---|---|
| **Instagram hashtag search** | Search #lagosfashion #nigerianhair #abujaskincare, filter by recent posts, click profiles with "DM to order" or "Link in bio" | 10–30 profiles/hour |
| **TikTok hashtag search** | Same pattern. #smallbusinessnigeria #lagosvendor | 10–20 profiles/hour |
| **Instagram location tags** | Search location tags (e.g., Lekki Phase 1, Ikeja City Mall), browse recent posts | 15–25 profiles/hour |
| **Comment section mining** | Find a popular vendor post, read comments — buyers often tag OTHER vendors ("where did you get this?") | 5–10 referrals/hour |
| **Influencer follower lists** | Nigerian fashion/beauty influencers have thousands of vendor followers | 50–100 profiles/hour |

### 2.2 Semi-Automated Approaches

| Tool | Approach | Cost | Risk |
|---|---|---|---|
| **Apify Instagram Profile Scraper** | Scrape followers of a known vendor account | ~$0.10/1K profiles | High — Instagram blocks scrapers aggressively |
| **Apify TikTok Hashtag Scraper** | Scrape videos by hashtag, extract usernames | ~$0.05/1K videos | Medium — TikTok less aggressive than IG |
| **BrowserAct custom workflow** | Build a workflow that searches Instagram hashtags and extracts profile data | ~$0.003/step | Low — but limited to what the site exposes without login |
| **Playwright + Claude-in-Chrome** | Manual browsing with AI assistance to speed up evaluation | Free (your time) | None — but not scalable |

### 2.3 The Reality

For Instagram/TikTok-only sellers, **manual discovery is still the highest-quality method.** The platforms are designed to prevent exactly the kind of scraping that would make this easy. Your best bet is a hybrid:

1. **Use Apify to scrape TikTok hashtags** (lower blocking risk than IG)
2. **Use BrowserAct or Playwright for Instagram** (slower but more reliable)
3. **Build a "seed account" strategy** — find 20 known vendors manually, then scrape their followers/following for more
4. **Hire a VA** (virtual assistant) in Nigeria to do manual Instagram discovery for $3–5/hour — often cheaper and more reliable than scraping infrastructure

---

## 3. Intent Signals: Finding Businesses Already Looking for You

**This is the highest-ROI layer.** A business that is actively looking for web development will convert 5–10x better than a cold prospect.

### 3.1 Free Intent Sources

| Source | What to Monitor | How to Access |
|---|---|---|
| **LinkedIn job posts** | "Web developer," "Shopify developer," "ecommerce manager," "website redesign" | LinkedIn search + Apify scraper |
| **Indeed/Jobberman (Nigeria)** | Same keywords | RSS feeds or Apify scraper |
| **Upwork/Fiverr buyer requests** | Clients posting web dev projects | Manual browse + RSS |
| **G2/Capterra reviews** | Negative reviews on Shopify/Wix/Squarespace ("my site looks terrible") | G2 API or manual browse |
| **Reddit** | r/ecommerce, r/smallbusiness, r/shopify — "my store is not converting" | Apify Reddit scraper (already in your trend-radar setup) |
| **X/Twitter** | "need a website," "looking for web designer Lagos" | X API (already connected) |
| **Facebook groups** | "Nigeria Online Vendors," "Lagos Business Network" — members asking for website help | Manual browse or group scraping |

### 3.2 Paid Intent Sources

| Source | Cost | Signal Strength |
|---|---|---|
| **G2 Buyer Intent** | $$$ (enterprise) | Very high — companies researching software solutions |
| **Bombora** | $$$$ (enterprise) | Very high — B2B intent data from content consumption |
| **UpLead Buyer Intent** | On Professional tier | Medium — topic-based intent |
| **Seamless.AI Buyer Intent** | On paid tiers | Medium |

**Verdict:** Start with free sources. The job board approach is especially powerful — a business hiring a "Shopify developer" is literally announcing they have budget and need.

---

## 4. Finding Shopify Stores with Poor Websites

### 4.1 Hunter TechLookup (Recommended)

Search: Technology = "Shopify", Country = "Nigeria" (or any country)

- Free tier: limited lookups
- Paid tier: bulk export

**Cost:** ~$34/mo for 2K credits

### 4.2 BuiltWith (Alternative)

More comprehensive but more expensive ($295/mo).

### 4.3 Store Leads

A niche tool specifically for finding Shopify stores:
- https://storeleads.app
- Pricing: ~$49/mo
- Filters by revenue estimates, app usage, country

### 4.4 Manual Method (Free)

1. Google search: `site:myshopify.com "Lagos"` or `inurl:.myshopify.com Nigeria`
2. Browse Instagram hashtags, click "shop" links in bios — many are Shopify
3. Use Shopify's own store directory (limited)

---

## 5. Recommended Stack for Koolestpro

Based on your budget, use case, and existing infrastructure, here is the optimal stack:

### 5.1 Discovery Layer

| Source | Tool | Cost | Purpose |
|---|---|---|---|
| Google Maps (local businesses) | **Outscraper** | $3/1K businesses | Replace BrowserAct Maps workflow |
| Meta Ad Library (ad-running businesses) | **Apify** (existing) | ~$0.01/ad | Keep using — already working |
| Social-native sellers (TikTok) | **Apify TikTok scraper** | ~$0.05/1K videos | Hashtag-based discovery |
| Social-native sellers (Instagram) | **Manual VA + Playwright** | $3–5/hour (VA) | Instagram blocks automation |
| Job boards (intent) | **Apify + RSS** | Free | Hiring signals |
| Reddit/X (intent) | **Existing trend-radar** | Free (X: ~$1/mo) | Already connected |
| Shopify stores | **Hunter TechLookup** | $34/mo | Find existing stores to fix |

### 5.2 Enrichment Layer

| Need | Tool | Cost |
|---|---|---|
| Email discovery | **Hunter** | $34/mo (2K credits) |
| Email + phone enrichment | **Prospeo** | $49/mo |
| Fallback enrichment | **People Data Labs** | $99/mo (defer until volume) |
| Website quality check | **Your existing `lead_playbook.py`** | Free |

### 5.3 Intent Layer

| Source | Method | Cost |
|---|---|---|
| Job boards | Apify scraper + keyword alerts | Free |
| Reddit | Existing `reddit_search.py` | ~$0.004/result |
| X/Twitter | Existing `x_search.py` | ~$0.02/read |
| G2 negative reviews | Manual + API | Free tier exists |

### 5.4 Orchestration Layer

| What | Tool | Cost |
|---|---|---|
| Lead scoring + classification | **Your existing `lead_playbook.py`** | Free |
| Push to KoolestFlow | **Your existing `koolestflow_client.py`** | Free |
| Workflow automation | **Custom Python scripts** (your current approach) | Free |
| If you outgrow scripts | **Clay** or **n8n** | $60–200/mo |

---

## 6. Custom AI Agent Architecture

Your instinct to build a custom agent is correct. Here is the architecture that beats every off-the-shelf tool for your specific use case:

```
                    DISCOVERY ORCHESTRATOR
                           |
        +------------------+------------------+
        |                  |                  |
   Outscraper          Apify Actors       Manual VA
   (Maps/B2B)    (TikTok/Ad Library/    (Instagram)
                    Job Boards)
        |                  |                  |
        +------------------+------------------+
                           |
                    ENRICHMENT ENGINE
                           |
        +------------------+------------------+
        |                  |                  |
      Hunter           Prospeo/PDL      Website Check
   (Email find)      (Phone/social)   (lead_playbook)
        |                  |                  |
        +------------------+------------------+
                           |
                    SCORING & CLASSIFICATION
                           |
        +------------------+------------------+
        |                  |                  |
    Fit Score          Track Label        Intent Score
   (0-100)         (Build/Fix/Scale)   (job post? ad?)
        |                  |                  |
        +------------------+------------------+
                           |
                    PITCH GENERATION
                           |
        +------------------+------------------+
        |                  |                  |
    Free Sample        Website Audit      DM Script
     (Build)            (Fix/Scale)     (Nigeria track)
        |                  |                  |
        +------------------+------------------+
                           |
                    KOOLESTFLOW PUSH
                           |
                    (koolestflow_client.py)
```

### 6.1 What Each Module Does

**Discovery Orchestrator**
- Calls Outscraper API for map-based discovery
- Calls Apify actors for TikTok/Ad Library/job boards
- Receives manual VA uploads for Instagram discoveries
- Deduplicates across all sources using `taken-brands-ledger.json`

**Enrichment Engine**
- Hunter API for email discovery (domain-based)
- Prospeo API for phone/social enrichment
- Your existing `lead_playbook.assess_website_quality()` for site checks
- Skips enrichment for social-native sellers (no domain = no Hunter)

**Scoring & Classification**
- Reuses your existing `score_and_qualify()` logic
- Adds **intent score**: +20 if hiring for web dev, +15 if posted about website problems, +10 if running ads with poor landing page
- Track label: Build (no site) / Fix (has site, quality <60) / Scale (has site, quality >=60)

**Pitch Generation**
- Build track: "I built a free sample site for [Brand Name] — here's the link"
- Fix track: "I audited [Brand Name]'s site — 3 quick wins that could boost conversions"
- Scale track: "I help [niche] brands like [Brand Name] scale with better UX/SEO"

---

## 7. Implementation Priority

### Phase 1: Replace BrowserAct Maps (This Week)
- Sign up for Outscraper
- Build a Python wrapper script: `outscraper_koolestflow_bridge.py`
- Run side-by-side with BrowserAct for one week, compare cost/quality
- **Expected cost reduction:** 60–80% per lead

### Phase 2: Add TikTok Discovery (Next 2 Weeks)
- Find a reliable Apify TikTok hashtag scraper actor
- Test with hashtags: `#smallbusinessnigeria`, `#lagosvendor`, `#nigerianfashion`
- Build enrichment pipeline (profile bio → extract WhatsApp/Instagram → score)

### Phase 3: Add Job Board Intent (Next 2 Weeks)
- Set up Apify actors for LinkedIn/Indeed job searches
- Keywords: "web developer," "Shopify developer," "ecommerce manager," "website redesign"
- Map hiring company → discovery → enrichment → KoolestFlow

### Phase 4: Instagram VA System (Next Month)
- Hire a Nigerian VA ($3–5/hour on Upwork)
- Give them a Google Sheet + scoring rubric
- They manually discover 20–30 Instagram vendors/day
- You enrich and push to KoolestFlow in bulk

### Phase 5: Full Agent (Ongoing)
- Wire all sources into one orchestrator script
- Add auto-retry, deduplication, and quality checks
- Run daily/weekly unattended

---

## 8. Cost Summary: Full Stack

| Tool | Monthly Cost | Annual Cost |
|---|---|---|
| Outscraper (2K businesses/mo) | ~$6 | ~$72 |
| Apify (existing + TikTok) | ~$10 | ~$120 |
| Hunter (2K credits) | $34 | $408 |
| Prospeo (optional) | $49 | $588 |
| X API (trend radar) | ~$1 | ~$12 |
| Reddit/Apify (trend radar) | ~$5 | ~$60 |
| Instagram VA (20 hrs/wk) | ~$240 | ~$2,880 |
| **Total (lean)** | **~$96** | **~$1,152** |
| **Total (with VA)** | **~$336** | **~$4,032** |

Compare to:
- LeadX Pro: $129/mo ($1,548/yr) — no VA needed, but misses social-native
- Apollo Growth: $149/mo ($1,788/yr) — wrong market fit
- Clay Launch: $60/mo ($720/yr) — orchestration only, no discovery

**Your custom stack is the cheapest AND most targeted option.**

---

## 9. Key Takeaways

1. **There is no all-in-one.** The platforms that claim to be (Apollo, Seamless, Clay) are built for US B2B SaaS, not African social-native sellers.

2. **LeadX is the closest** for local no-website businesses, but it is a closed product, not an API-first tool you can fully customize.

3. **Outscraper beats BrowserAct** on cost and reliability for map-based discovery. Switch first.

4. **Instagram/TikTok-only sellers require a hybrid approach** — TikTok can be semi-automated (Apify), Instagram requires manual VA work or Playwright with careful rate limiting.

5. **Intent signals (job boards, Reddit, X) are free or nearly free** and convert 5–10x better than cold discovery. Prioritize these.

6. **Your custom AI agent is the right long-term architecture.** Build it incrementally — one discovery source at a time.

7. **The VA approach is underrated.** For $240/mo, a Nigerian VA can manually discover 400–600 Instagram vendors per month — higher quality than any scraper, and cheaper than fighting Instagram's anti-bot systems.

---

*Next step: Start with Outscraper + Apify TikTok. I can build the bridge script and run a test batch into KoolestFlow.*

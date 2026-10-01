# Store scoring rubric (what we look for, and what each thing is worth)

Written 2026-10-01 from Ridwan's corrections. The code is `gmail-sender/Discovery.gs` (`scoreStore_`). Keep this file and the code in step. A store needs `MIN_FIT_SCORE` (default 55, Settings tab) to become a lead. Every point is written into the `reasons` column of the Discovery tab, so any score can be audited.

**What this can and cannot know.** Everything here is read from the store's own public pages, for free. It cannot see revenue, traffic or team size. It estimates "small and growing" from signals. Where a paid data source (Store Leads, BuiltWith) gives real revenue and employee counts, use it to pre-filter, then let this rubric add the design and CRO opportunity signals.

## 1. Gates (fail = skipped, no score)

| Check | Why |
|---|---|
| Site loads | Dead sites cannot be pitched |
| It is an online store (Shopify, WooCommerce, BigCommerce, Wix, Squarespace, Magento, PrestaShop, Ecwid, Webflow, or cart and product markup) | Any e-commerce that sells products is wanted |
| Market is one of: Nigeria, Ghana, Kenya, South Africa, UK, Ireland, US, Canada, EU countries | Decides voice and currency |

## 2. Points (base score 40, capped 0 to 100)

### Small and upcoming (good)
| Signal | Points | Reason |
|---|---|---|
| 1 to 3 products | +10 | Focused single-product brands are good clients |
| 4 to 60 products | +20 | Sweet spot: real catalogue, one person can fix it |
| 61 to 249 products | +15 | Still small enough to be a growing brand |
| Store younger than 1 year | +15 | Building now, no designer yet |
| Store 1 to 3 years | +10 | Young and trying to grow |
| Password or "opening soon" page, no products | +15 | Building the store right now |
| Free or default Shopify theme (Dawn, Refresh, Craft, Sense, Debut, Brooklyn...) | +10 | Nobody has designed it yet |
| Light app stack (0 to 2 marketing apps) | +5 | Small team, early stage |

### Looks established or big (bad)
| Signal | Points | Reason |
|---|---|---|
| 250 or more products | -10 | Bigger operation (reduced from -30, Ridwan 2026-10-01) |
| Store older than 6 years | -10 | Established, has its own plan |
| 6 to 8 marketing and support apps | -10 | Larger team and budget |
| 9 or more apps (Klaviyo, Gorgias, Recharge, Yotpo...) | -20 | Established brand |
| More than 5 language versions | -15 | International brand |
| Empty catalogue | -15 | Nothing to sell yet |

### Visible weaknesses a designer can fix (opportunity)
| Signal | Points | Reason |
|---|---|---|
| No mobile viewport tag | +10 | Real mobile problem |
| First load slower than 3 seconds | +5 | Speed fix |
| No returns or shipping policy link | +5 | Trust gap |

## 3. Business model (does not change the score, changes the pitch)

Detected from apps, image hosts, shipping-time text and the `vendor` field of the product feed.

| Model | How detected | Pitch | Offer |
|---|---|---|---|
| own-brand | One vendor that matches the brand name | Conversion, trust, brand story | Full ladder: audit, page build, full build, retainer later |
| dropship-likely | 2 or more of: DSers, Oberlo, Spocket, Zendrop, CJ, AutoDS, AliExpress images, "10 to 20 business days" or "ships from China" | Product-page conversion and trust only: their money comes from ads, the page is where it leaks | Single page build or audit. No brand-building retainer. Do not assume they make the product |
| print-on-demand | Printful, Printify, Gelato, Gooten | Product pages and brand polish | Page build |
| reseller | 8 or more different vendors | Catalogue navigation, collection filters, search | Page build or full build |
| unknown | none of the above | Generic | Generic |

**Decided 2026-10-01: dropship-likely stores get a lower tier** (proposed: Nigeria Starter N250k; international audit $120, product page $400; no full build or retainer). Numbers to be confirmed by Ridwan.

## 4. Platform

Shopify is where Ridwan builds. Non-Shopify stores are wanted as long as they sell products. The pitch for them is a CRO review of the current site, or a move to Shopify. WooCommerce catalogue size is read from its public store API; other platforms have no catalogue score.

## 5. Not scored yet (ideas, need data we do not have for free)

Real revenue and traffic (Store Leads, BuiltWith, or the store's public sales signals), team size (LinkedIn), ad spend (Meta Ad Library), review count and rating (Trustpilot), social following, domain age (WHOIS or RDAP). Adding any of these is a one-line change in `scoreStore_` once the data is available.

## 6. Data source options

| Source | What it gives | Cost | Status |
|---|---|---|---|
| Public list pages (current Sources tab) | Domains only, noisy | Free | Built. Merchant Genius, ZIK, techpeeker, eachspy return some domains; cro.media blocks readers (403); BuiltWith free page returns none |
| Merchant Genius (merchantgenius.io) | Free archive of Shopify stores ordered by domain registration date, so genuinely new stores | Free | No API found. Pages exist per store and per date; needs a look in a real browser to confirm structure |
| Store Leads (via Apify actors, or Store Leads' own plans) | Shopify, WooCommerce, BigCommerce stores with estimated sales, employee count, apps, contact emails, 80+ fields | About $1.40 to $8 per 1,000 records on Apify actors; own plans not verified | Not built. Best fit for "small but already selling" filtering |
| BuiltWith Lists API | Domains by technology, with contact data | From about $295 a month | Too expensive for now |
| Apify Shopify store finders | Domains by keyword, optionally with emails and apps | About $1 to $5 per 1,000 | Connector built (`Apify.gs`), untested. Ridwan is open to a small test. Actor input formats could not be read from the Claude sandbox, so the actor's own Input JSON is pasted into the Apify tab |

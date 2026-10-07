# CRO finding rules: what counts as a real finding

A living rulebook. Every time a finding turns out wrong (in a post, a client audit or a cold email), the lesson is added here with the date and the case that taught it. Both CRO skills carry a copy (`references/finding-rules.md`), refreshed by `python3 .ai-workflow/tools/sync_cro_rules.py`. Edit this file, never the copies.

Used by: `koolestpro-store-auditor-skill-a` (CRO Fix posts), `koolestpro-client-audit` (paid audits), and the outreach research in `outreach/gmail-sender/Research.gs` (cold emails), which enforces the same rules in code.

## 1. Every finding carries an evidence label

| Label | Meaning | Can it be the headline finding? |
|---|---|---|
| MEASURED | A number from a tool or the store's own data (product feed, review count shown, Google real-user data) | Yes |
| SEEN | Actually visible on a named page at 390px, quoted or screenshotted | Yes |
| SOFT | Something NOT found: missing from the source, a page you could not find, an app you could not detect | Never. Ask about it, do not state it |

Absence is always SOFT until checked on the live page in a real browser. Reviews, size guides, delivery info and upsells often load with JavaScript or sit in a popup.

## 2. Check the page before you claim it lacks something

Before a finding goes in, open the live page and look for anything that already answers it: reviews, guarantee, returns, FAQ answers, ingredients, how it works, results timing, delivery. Open the accordions: collapsed content counts as on the page (a shopper opens it with one tap).

- **Niche-typical doubts are not findings.** "Buyers of a $99 supplement usually wonder what it does, how fast, and what if it fails" is a guess about the niche, not a finding about this page. *(Nomalife, 2026-10-07: the Rise page already showed 84 reviews, "Science Backed · 30-Day Guarantee · Easy Returns", and an FAQ answering timing and refunds.)*
- **Hidden theme labels are not page content.** Themes ship `<span class="sold-out-message hidden">Sold out</span>` on every product. Read what is visible, not the raw HTML. *(District Lounge, 2026-10-07: "every featured product is sold out" while all 18 products were in stock.)*

## 3. Never a finding

- **Language, translation, currency, price display, country or market differences.** Stores adapt these to where the visitor browses from; a fetch from a server abroad, a VPN or your own location shows a version their customers never see. *(sellare-es.com, 2026-10-07: "Italian cart words" on a Spanish store.)*
- **Stock levels.** Sold-out items are a supply decision, not a design problem, and the owner already knows. At most a supporting detail (a homepage featuring products nobody can buy). Check the product feed (`/products.json`) before saying anything about stock.
- **Ten-minute fixes as the headline.** Add a size chart, upload another photo, write a description, fix a typo, hide sold-out items. These can be in the list; they are never the lead finding or the reason to talk.
- **Taste.** Colours, fonts or layout you would have chosen differently, without a conversion reason tied to a specific element.
- **Generic advice.** "Improve conversions", "add more trust", "optimise the page", "a few small tweaks", "some friction". If the line could be said about any store, cut it.

## 4. Speed: only when obviously slow

Speed is a strong finding when it is undeniable, and a credibility killer when it is not. State it only when:

1. Google real-user data (Chrome UX Report, shown at the top of pagespeed.web.dev as "Discover what your real users are experiencing") rates the page or origin **Poor/Slow** with LCP at **4s or more** for phone visits. Real-user data decides when it exists; ignore the lab score then.
2. With no real-user data: the mobile lab test shows LCP **8s or more** and a performance score of **35 or less**, on **two runs** that agree.

Quote the exact number and say it is Google's measurement on phones. Never "your site feels slow", never a rounded-up figure, never a lab score alone on a borderline result.

## 5. Look for what they could add, not only what is broken (Tier 2)

A store that already looks excellent still has a finding if its funnel is missing something that fits how it sells. Check before claiming it is missing:

- **Sitemap pages** (`/sitemap.xml` → `sitemap_pages_1.xml`): listicles ("5-reasons-why"), advertorials, quizzes, bundle pages, landing pages. *(Jones Road Beauty had several "5-reasons-why" listicles and a shade quiz.)*
- **Hidden paths**: `/pages/advertorial`, `/pages/listicle`, `/pages/lp`, `/pages/offer`, `/pages/quiz`, `/pages/build-your-own-bundle`.
- **Funnel subdomains**: `try.`, `get.`, `go.`, `offer.`, `lp.`, `learn.`, `discover.` and others. Advertorials on a completely separate domain only show up through the brand's ads (Meta Ad Library landing URLs), so "no advertorial" stays SOFT unless the ads were checked.
- **Page builders in the source**: Replo, GemPages, Zipify Pages, Funnelish, Shogun, Instant.
- **Ad pixels**: Meta, TikTok, Google Ads. A pixel means they run, or are set up to run, paid traffic.
- **Apps**: post-purchase and upsell (ReConvert, AfterSell, Zipify OCU, Rebuy, UpCart), bundles (Fast Bundle, Bundler, Kaching), subscriptions (Recharge, Skio, Loop, Appstle), quizzes (Octane AI, RevenueHunt). Post-purchase offers run inside checkout, so their absence from the storefront is SOFT.

Then match the gap to the business: consumables and repeat buys → bundle builder, subscription, post-purchase; products that need explaining plus ad pixels and no pre-sell page → advertorial or listicle (built in Replo); many similar products → quiz. Name exactly what would be built.

## 6. Targets that are never used

- Restricted or high-risk categories: vapes, nicotine, tobacco, kratom, replicas, weapons. *(District Lounge sold bulk disposable vapes in Australia, orders by WhatsApp and Telegram.)*
- For outreach only: big brands (in the Tranco top 1M traffic list). Content posts may still feature well-known brands.

## 7. Final check before a finding ships

- [ ] It has a label, and the headline finding is MEASURED or SEEN
- [ ] I checked the live page (accordions open) for anything that already answers it
- [ ] It is not about language, currency, stock, taste, or a ten-minute fix as the headline
- [ ] Any speed claim meets section 4 and quotes Google's number
- [ ] It names the page and the exact element, and the founder could verify it in ten seconds
- [ ] Every number comes from the live page or the store's own data

## Change log

- 2026-10-07: created from the cold-email test phase (Nomalife, District Lounge, sellare-es.com) and Ridwan's rules on speed, small fixes, Tier 2 offers and restricted categories.

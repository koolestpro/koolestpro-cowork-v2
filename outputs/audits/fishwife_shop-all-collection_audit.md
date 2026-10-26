# Fishwife: shop-all collection page audit (CRO Fix, 2026-10-25)

Page: https://eatfishwife.com/collections/all (COLLECTION PAGE, "Everything Fishwife")
Viewport: 390x844 @2, iPhone UA, headless Chromium, captured 2026-10-25 from the cloud sandbox.
Rules applied: docs/system/cro-finding-rules.md (evidence labels, checked live with popups closed, no language/currency/stock/price-display/taste findings, no speed claim).
Concept work only. Fishwife is not a client.

## #1 finding (headline): screen one is a banner, the products start below it
Evidence: SEEN + MEASURED (element positions from the live DOM; screenshot `outputs/cro-fixes/fishwife/_assets/before_raw.png`).
- Banner image y=98 to 498 (400px of an 844px screen). Its only message: "Shop Tinned Fish & More! Find all your favorite fish, bundles, and merch." on a translucent green box.
- Category pills at y=540, "Everything Fishwife" H2 at y=588, first product photos at y=664.
- First product name (h3 "Tuna Belly") at y=863. Stars at ~y=840 are cut by the screen edge. No product name, rating or button is readable on screen one.
- On a page whose only job is choosing a product, screen one does not let anyone choose.

## Finding 2: ratings show no review count
Evidence: SEEN (card shows "Rated 5.0 out of 5 stars | 5.0") + MEASURED (PDP JSON-LD aggregateRating).
- 12 Days of Fishwife Advent Calendar: 5.0 from 2 reviews. Smoked Salmon with Fly By Jing Chili Crisp: 4.9 from 641. Both render as a bare star average, so the 2-review item looks as proven as the 641-review one.

## Finding 3: the first row is the least-proven products
Evidence: SEEN (grid order) + MEASURED (JSON-LD counts).
- Row 1: Tuna Belly (4.5, 21 reviews, "JUST DROPPED!") and the Advent Calendar (5.0, 2 reviews).
- Row 2: The Starter Pack (4.9, 343) and Fly By Jing smoked salmon (4.9, 641). Row 3: Gold Label Smoked Salmon (4.9, 520) and Zhong smoked salmon (4.9, 110).
- All of 641/520/343/223 are in their own /collections/best-sellers.

## Finding 4 (supporting): cards don't say what you get or let you add
Evidence: SEEN.
- Card titles drop the pack size ("Tuna Belly" for the product titled "Tuna Belly (3-Pack)").
- Every card button says "Shop Now" (goes to the PDP); no add-to-cart from the grid.

## Noted, not used as a finding
- On load, a full-screen "You've Got A Mystery Discount / Are you new to tinned fish?" quiz popup (Alia) plus the Shopify cookie banner cover screen one. Not the lead: it is dismissable, and last week's run (Topicals) already led with a popup.
- Product cards show no price. Not a finding per the rules (price display is never a finding). The rebuild shows feed prices on cards but no copy claims this as a fix.
- No speed claim (not measured against the section 4 thresholds).

## Tier 2 (what they could add)
- Okendo reviews, a Build Your Own Bundle product (9/12/15 tins) and a Best Sellers collection already exist. A "new to tinned fish" path exists only inside the popup quiz; the Starter Pack (7 tins, 4.9 from 343) is the natural on-page answer (used as variant D and below the fold in the rebuild).

## Fix plan (what the rebuild implements)
1. Banner 400px -> 118px slim photo band, real H1 "Everything Fishwife" kept.
2. Pills + "Sort: Most reviewed" directly under it; four best-seller cards fully above the fold.
3. Stars with counts on every card: 4.9 (641), 4.9 (520), 4.9 (343), 4.9 (223).
4. Pack size under each name; "Add" button on each card.
5. New drops (Tuna Belly) stay on the page, after the proven tins; Starter Pack block for first-timers.

## Final check (cro-finding-rules section 7)
- [x] Labels on every finding; headline is SEEN + MEASURED
- [x] Checked live with popups closed
- [x] Not language/currency/stock/price/taste; not a ten-minute fix as the headline
- [x] No speed claim
- [x] Names the page and exact elements; verifiable in ten seconds on a phone
- [x] Every number from the live page or the store's own data (JSON-LD, /products.json)

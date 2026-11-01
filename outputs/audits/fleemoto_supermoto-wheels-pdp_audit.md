# FleeMoto: 17/14 chrome super moto wheels set (PRODUCT PAGE / PDP), CRO audit

- URL: https://fleemoto.shop/products/17-14-chrome-super-moto-wheels-set-for-yozma-in-10-tuttio-valintinsu
- Date: 2026-11-01 (unattended weekly CRO Fix run)
- Why this store: first entry in `buildQueue` (tier 2, emailed, no reply yet, problemWorth 3, buildPage "Product Page"). Contactable list pulled 2026-10-31 08:53 UTC (under 3 days old). Small e-moto parts store, 8 products, not a restricted category, not a big chain.
- Rules applied: `docs/system/cro-finding-rules.md`. Checked at 390x844 in headless Chromium (iPhone UA), element positions measured with `getBoundingClientRect`. The page has no accordions or tabs; everything below was visible on load.

## Facts (all from the live page or the store's product JSON)

- Title: "17/14 chrome super moto wheels set for yozma in 10/tuttio/valintinsu". Price $319.99, one variant, no compare-at price.
- Description (full text): "pre-orders will ship 2 weeks after order" / "These 17/14 inch chrome super moto" / "compatibility": Yozma in 10, valintinsu em5, tuttio.
- 4 photos: the set on a bike on a stone wall (daylight), the bike at dusk, and two white-background shots of the wheels (single, and the pair).
- Buttons: quantity, "Add to cart", "Buy with Shop Pay", "More payment options".
- Below: "You may also like" (Glossy Motocutz Style Front Plate $19.99, Fork lock $18.99, Battery Powered Surron Horn $32.99, KYB Front Fork Stickers $7.99), newsletter, footer.
- Header logo is text only ("FleeMoto" set in the theme's Inter, weight 600). No logo image file exists on the site.

## Findings

### 1. Price and Add to cart sit below the first screen (HEADLINE)
Evidence: MEASURED + SEEN. On a 390x844 screen the H1 sits at y=626, the Add to cart button at y=895 and the price at y=903. The screen ends at 844. Screen one is the header, a white gap, the bike photo and the title. A shopper has to scroll before they see what the set costs or how to buy it.

### 2. The fit list is under the buy buttons
Evidence: MEASURED + SEEN. "compatibility" starts at y=1093 (Yozma in 10 at 1121), about 200px under Add to cart and below the Shop Pay button. For a wheel set, "does it fit my bike?" is the question a buyer needs answered before tapping buy.

### 3. The 2-week pre-order wait is easy to miss
Evidence: SEEN. "pre-orders will ship 2 weeks after order" sits at y=1021, under the buttons, and the main button says "Add to cart" with no pre-order label. A $319.99 buyer may only learn about the wait after paying.

### 4. The description stops mid-sentence (supporting, ten-minute fix, never the lead)
Evidence: SEEN. "These 17/14 inch chrome super moto" ends there.

### 5. The first photo shows the whole bike, not the wheels
Evidence: SEEN. Photo 1 is the bike on a wall; the clear shots of the wheel set are photos 3 and 4.

## SOFT (not stated as findings, ask instead)
- No reviews are shown on the page (no review app detected). Not a finding; the rebuild does not add any.
- `/policies/shipping-policy` and `/policies/refund-policy` returned "Page not found" in our check. Worth asking about; never stated publicly.
- One `ttq` string in the source suggests a TikTok pixel. Not confirmed.
- Speed: not measured with Google real-user data. No speed claim.

## What the rebuild changes (ranked by impact)
1. Price, pre-order label and one primary CTA on screen one ("Pre-order · $319.99").
2. "Fits these bikes" check list (Yozma IN 10, Valintinsu EM5, Tuttio) directly under the title, above the button, with a "Not sure? Ask before you order" link to their contact page.
3. Pre-order timing stated by the button and in the trust row ("Ships 2 weeks after order").
4. Hero = the wheel pair (their white-background photo, background removed) on a dark plinth; the on-bike photos move to an "On the bike" section.
5. Full page below: fit check, on-the-bike photos, what's in the set, how pre-order works, FAQ, their own "You may also like" picks, newsletter, sticky pre-order bar.

## Final check (cro-finding-rules section 7)
- [x] Headline finding is MEASURED/SEEN
- [x] Live page checked (no accordions exist)
- [x] Not language, currency, stock, taste; the ten-minute fix is not the lead
- [x] No speed claim
- [x] Names the page and the element; founder can verify in ten seconds
- [x] Every number from the live page or product JSON

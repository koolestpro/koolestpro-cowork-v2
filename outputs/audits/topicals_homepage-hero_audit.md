# Topicals homepage audit (mobile, 390x844), 2026-10-18

URL: https://mytopicals.com/ · Page type: HOMEPAGE · Real brand, not a client (unofficial concept work).
Method: headless Chromium, iPhone UA, 390x844 at 2x, captured 2026-10-18; ratings from each product page's JSON-LD `aggregateRating`; prices from the homepage cards and product JSON-LD.

## #1 finding

Screen one is a full-screen "Try your luck / Scratch below to see what you win" scratch-card game. Close it and the first screen is the giant TOPICALS wordmark over a face photo, with a one-kit promo headline ("Bright Eyes & Slick Lips", H1 at y=668) and a black "Scratch to win" pill (y=776, 164x56) sitting on top of the only "Shop now" button. "Skincare for flare-ups", the thing Topicals sells, only exists in the `<title>`. The homepage shows zero star ratings, while the products carry 4.8 to 5.0 stars from 129 to 882 reviews each.

## Findings, ranked by impact

1. **A game gates the page.** Scratch-card modal on load, full screen. (fixed: removed from first screen; the kit offer moves into the announcement bar)
2. **The only CTA is covered.** After closing, the persistent "Scratch to win" pill overlaps "Shop now". (fixed: one full-width CTA, nothing floating over it)
3. **No category statement.** The visible H1 is a single kit name; the wordmark takes the top ~110px of screen one. (fixed: H1 "Skincare for flare-ups. Made fun." built from their own "make flare-ups fun" line)
4. **No proof anywhere on the homepage.** Faded Brightening + Clearing Serum 4.9 (882), Like Butter 4.9 (719), Faded Under Eye Masks 4.8 (721), Slather 4.8 (676), Faded Dark Spot Kit 4.8 (401), Bright Eyes & Slick Lips Kit 5.0 (129). None shown on the homepage. (fixed: proof line above the H1, ratings on rail + concern tiles)
5. **The range is invisible on screen one.** First product card at y~991. (fixed: hero is a labelled lineup of four best sellers + the new kit, each tagged with the flare-up it treats)
6. **No "shop by concern" way in.** The brand is organised by skin condition but the homepage is not. (fixed: Dark spots / Dry skin / Under eyes / Body pills + a "Shop by flare-up" grid)

## Real facts used

- Kit offer: Bright Eyes & Slick Lips Kit, "A $45 value, yours for $30" (homepage hero copy).
- Faded Dark Spot Kit: $28, "$44 value" (homepage), save $16.
- Like Butter Moisturizer: $34 (JSON-LD), "For Dry, Eczema-Prone Skin".
- Free shipping on orders $50+ (product page banner).
- Values: "Science-backed formulas & quality active ingredients", "Skin shade and condition inclusivity", "Vegan & cruelty free products" (homepage).
- Assets: header inline SVG wordmark (rasterized), Chalet / Chalet Bold / ITC Garamond Cond Italic from their CDN, product packshots from cdn.shopify.com (background removed), lifestyle photos from cdn.sanity.io.

Not used (could not verify): Faded Serum and Slather full-size prices, Eye Mask 6-pair price.

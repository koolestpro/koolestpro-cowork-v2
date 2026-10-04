# CRO Audit: Fly By Jing, Original Sichuan Chili Crisp (Product Page, PDP)

- URL: https://flybyjing.com/products/sichuan-chili-crisp
- Audited: 2026-10-04, live page, mobile 390x844 (iPhone UA, headless Chromium)
- Weekly CRO Fix. Unofficial concept work. Fly By Jing is not a Koolestpro client.
- Evidence: `outputs/cro-fixes/flybyjing/_assets/flybyjing_before_raw.png` (screen one after closing the popup), `flybyjing_before_popup_raw.png` (screen one on load), `before_buybox_crop.png` (the buy box as found).

## #1 finding (one sentence)

On a phone, screen one is the jar, the product name, bare stars and a 50-word paragraph; the pack picker starts at y=1,017, the price at y=1,146 and Add to Cart at y=1,357, and the default $30 is a 2-pack with no per-jar price anywhere.

## Measured on the live page (css px, 390 wide)

| Element | y | Note |
|---|---|---|
| Gallery (jar on red) | 117-542 | single studio jar, arrows below |
| H1 "Original Sichuan Chili Crisp" | 566 | |
| Stars + "(2459)" | 657 | no rating number next to the stars |
| Description paragraph | 692-840 | "Chat with us" bubble and a cookie badge sit on top of it |
| Size picker (2-PACK preselected) | 1,017 | labels only: 2-PACK / 3-PACK / 4-PACK / 16 OZ |
| One-time price $30.00 | 1,146 | |
| Membership $24.00 (save 20%) | 1,206 | |
| ADD TO CART - $30.00 | 1,357 | |
| "4.9" rating, "97% would recommend" | ~5,750 | in the reviews block |

On first load a full-screen "UNLOCK 20% OFF / How spicy do you like it?" quiz covers the whole page until dismissed.

## Findings, ranked by impact

1. **The decision is split from the first screen.** Price, pack and Add to Cart all start below 1,000px. A shopper who doesn't scroll never sees a price.
2. **"$30" doesn't say what it buys.** The preselected option is "2-PACK" and the price is $30.00. The page never says 2 jars or $15 a jar. Pack prices from the product data: 2-pack $30 ($15/jar), 3-pack $42.75 ($14.25/jar), 4-pack $54 ($13.50/jar), 16oz $32.
3. **The strongest proof is buried.** 4.9 out of 5 from 2,459 reviews and 97% would recommend sit about 5,750px down. Up top there are stars and "(2459)" with no number.
4. **Heat level, the real worry for a chili crisp, is inside a paragraph.** "Intensely flavorful yet not off-the-charts spicy" is the answer, written by the brand, sitting mid-paragraph. The popup itself asks "How spicy do you like it?".
5. **Overlays.** The quiz popup covers screen one on load; after closing it, the chat bubble and cookie badge cover the description.
6. **Trust is far from the button.** Free shipping over $75 is only in the scrolling marquee; dispatch time (48-72 hours) is inside the Shipping tab.

## What the rebuild changes (ranked, these drive the headline and annotations)

1. Pack picker with per-jar prices + price + ONE Add to Cart ("Add 2 jars to cart | $30") on screen one.
2. 4.9 stars, 2,459 reviews and 97% recommend right under the photo.
3. Outcome headline on the real lifestyle photo ("Crunchy. Numbing. Goes on everything.") plus the heat line in the brand's own words.
4. Trust row under the button: ships in 48-72 hours, free shipping over $75, no artificial flavors or preservatives.
5. Club price ($24, save 20%) shown as a secondary note, not a competing button.
6. Recommendation (not built into the screenshot): delay the email quiz until scroll or exit intent so it never covers screen one.

## Real assets used

- Logo: header `<img>` `FBJ-Web-Logo_2026.svg`, rasterized to PNG as-is (not redrawn).
- Fonts: the site's own JeanLuc and Publico webfont files from their Shopify CDN.
- Photos: `Core4PDP-Original-Lifestyle-1` (hero), `-Lifestyle-2` and `-3` (below the fold), all from the live product media.
- Review quotes: Christina R. and Joyce H., verified buyers, quoted verbatim from the page.

Nothing invented. Per-jar prices are simple division of the live pack prices.

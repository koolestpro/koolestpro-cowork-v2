# CRO Audit: Bala, Homepage (first screen on mobile)

- URL: https://shopbala.com/
- Audited: 2026-10-11, live page, mobile 390x844 (iPhone UA, headless Chromium)
- Weekly CRO Fix. Unofficial concept work. Bala is not a Koolestpro client.
- Evidence: `outputs/cro-fixes/bala/_assets/bala_before_popup_raw.png` (screen one on load, no popup this time), `bala_before_full.png` (full page).
- Note: the pool entry (reviewed 2026-09-28) described a "Meet The Bala Pilates Method" video hero. The hero has since changed. This audit is on the page as it stands today.

## #1 finding (one sentence)

On a phone, screen one is a hairline slogan ("Fitness, but make it cute"), a 10%-off-bundles line and a thin ghost button, so it never says what Bala sells; their signature product, Bala Bangles (4.9 stars from 1,865 reviews, from $55 a pair), first appears 3,431px down.

## Measured on the live page (css px, 390 wide)

| Element | y | Note |
|---|---|---|
| Promo marquee (pink pill) | 20-57 | scrolling "NEW! ..." links, cut off at both edges |
| Header (menu, logo, cart) | 77-111 | |
| Hero video card | 131-731 | model holding a ball, wearing Bangles on her ankles |
| H1 "FITNESS, BUT MAKE IT CUTE" | 523 | ITC Avant Garde Std XLt (extra light) at 31px, a hairline over the video |
| "Save 10% when you bundle your favorite Bala products." | 611 | 12px |
| "SHOP BUNDLES" ghost button | 653 | outline only, no fill |
| Category tabs | 791 | New Arrivals / Best Sellers / ... |
| First product cards + prices | 1,134-1,173 | The Wavy Roller $39, Pilates Method $99, Ab Roller $99 |
| "THE ONE AND ONLY / Bala Bangles" section | 3,431-3,473 | weight picker + ADD TO CART |
| "Rated 4.9 out of 5 stars, 1,865 Reviews" | 3,894 | the only rating on the homepage |

## Findings, ranked by impact

1. **Screen one never names a product.** The headline is a mood line, the sub-line is a bundle discount, and the button says SHOP BUNDLES. A first-time visitor from an ad or a press mention can't tell this is the wrist and ankle weights brand. The Bangles are on the model's ankles but nothing says so.
2. **The hero product and its proof are 3,431px and 3,894px down.** Bala Bangles ("THE ONE AND ONLY") with its weight picker, price and 4.9 stars from 1,865 reviews sits below the product grid, the bundles block and more.
3. **No price on screen one.** The first prices appear at y=1,173, and they belong to new launches (The Wavy Roller $39), not the product the brand is named after ($55 / $65 / $79 a pair for 1 / 2 / 3 lb).
4. **The headline is hard to read.** 31px at weight 400 in a thin geometric face, uppercase, sitting on a moving video. The CTA is an outline button of the same weight.
5. **The marquee is clipped.** The scrolling pill cuts words at both edges ("NEW! The Bala Pilates Method!" starts mid-word), so it reads as broken rather than as news.
6. **Reasons to buy live on the PDP only.** Sold in pairs with a carry case, fits 5.5" to 11" wrists or ankles, HSA/FSA, Klarna and Shop Pay are all on the Bangles PDP, none on the homepage first screen.

## What the rebuild changes (ranked, these drive the headline and annotations)

Revision 3 (2026-10-11, after Ridwan's review: don't narrow the hero, research first, less
left-aligned text). Hero chosen from four researched directions, see
`references-for-posts/homepage-hero-research-2026-10-11/` (README, board, CHOICE.md).

1. The range in one picture: Bala's own Studio to Street Kit flatlay (Bangles, Bala Bra,
   Flared Legging, Everyday Sweatshirt in Blush), each product labelled on the image.
2. 4.9 stars from 1,865 Bala Bangles reviews right above the headline (was at 3,894px),
   labelled as Bangles reviews because that is what the number covers.
3. Short centered stack: H1 "Weights & activewear, but make it cute." (their own line, now
   saying what they sell), a one-line sub, ONE full-width CTA "Shop best sellers".
4. Category pills (Weights, Pilates props, Activewear, Bundles) and their own press logos
   (The Wall Street Journal, goop, Glamour) on screen one.
5. Below the fold: priced best-sellers rail, reasons strip, photos, verified reviews, bundle card.
6. Static announcement bar instead of the clipped marquee.

Earlier passes, kept for the record: r1 was a Bangles buy box (read as a PDP); r2 a
left-aligned Bangles hero with a rail (too narrow, too much left-aligned text).

## Real assets used

- Logo: the header's own inline SVG (84x34 `ba\a` wordmark), rasterized to PNG as-is, not redrawn.
- Fonts: Bala's own webfonts from their Shopify theme (Iskry Bold, Diatype Regular).
- Photos: `BalaBangles_r1_01E_1443_BLUSH.jpg` (hero, Bangle on a wrist), the Studio to Street Kit flatlay (hero), the Blush product renders for the rail, their own press logos (WSJ, goop, Glamour), `BalaBangles_blush_9965_webres.jpg` (carry case), `037A8873` (lifestyle), all from Bala's own CDN.
- Review quotes: Rochell J., Megan C., Nikki W., verified buyers, verbatim from the Bangles PDP.

Nothing invented. Prices from the live product JSON (`/products/bala-bangles.js`), rating from the live page.

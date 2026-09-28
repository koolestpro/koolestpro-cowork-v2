# TAPro Cards: Social Content Library

Real business, real numbers, unofficial CRO breakdown. Not commissioned by TAPro.

## HOW TO USE THIS FILE

Each key below maps one generated asset to its ready-to-post caption. The machine-readable sibling `tapro-social-content.json` carries the same keys for automation to join on `assetPath`. `status` tracks whether that specific asset+caption has actually been posted; it does not affect the pipeline item's own status in `ridwan_content_system_updated.html` (which only reaches `"Created"` from this run, never `"Published"`).

| Key | Platform | Asset |
|---|---|---|
| `CRO-TAPRO-BA` | LinkedIn, Instagram | Before/after graphic |
| `CRO-TAPRO-ANNO` | LinkedIn, Instagram | Annotated changes graphic |
| `CRO-TAPRO-CAROUSEL` | LinkedIn, Instagram | 8-slide carousel |
| `CRO-TAPRO-X1` | X | Text only, "the rule" angle |
| `CRO-TAPRO-X2` | X | Text only, before/after contrast |
| `CRO-TAPRO-X3` | X | Text only, hot take |

---

## CRO-TAPRO-BA

```
TAPro Cards has 15,500+ business customers and a 4.9 star rating from over 1,100 reviews. You wouldn't know it from their homepage.

The first screen is a promo banner and a hero photo. You don't see a price, a rating or a product until you've scrolled past a full video demo and into the product grid.

Your first screen should say what's true about you straight away. TAPro's hides it.

Follow @koolestpro for weekly CRO breakdowns.

#ShopifyDesign #CRO #eCommerce #ConversionRate #Shopify #UXDesign #SmallBusiness
```

## CRO-TAPRO-ANNO

```
TAPro sells NFC and QR review cards to local businesses. Their flagship card is $34.95, rated 4.9 stars from 1,125 reviews, trusted by 15,500+ businesses. All real, all verified. None of it shows up on the first screen of their homepage.

Here's every change and why it moved: real price and rating under the headline, the real product photo instead of a placeholder, the trust strip pulled up from deep in the page, one thin promo line instead of two rows, no duplicate search icon, and a CTA pointed at one product instead of a generic banner link.

Same brand, same product, same price. Just put the proof where a first-time visitor can actually see it.

#CRO #ConversionRateOptimization #Shopify #eCommerce
```

## CRO-TAPRO-CAROUSEL

```
TAPro's homepage never shows a price, a star rating, or a single product. Not on the first screen.

TAPro sells NFC and QR review cards to local businesses. Land on their homepage and you get a promo banner and a big hero photo. Scroll past that, past a full video demo, and you still won't see a product or a price.

Keep scrolling into a product grid and you'll hit their flagship card, the G-Series Onyx: $34.95, a real 4.9 star rating from 1,125 reviews, and over 15,500 businesses using their cards, including names like Sheraton and McDonald's. All of it real. None of it near the top.

Here's what I changed and why:

1. Pulled the real price and 4.9 star rating up, directly under the headline
2. Put the actual product front and center, a real photo instead of a placeholder
3. Pulled the "15,500+ businesses" trust strip up from deep in the page
4. Collapsed the two-row promo banner into one thin line
5. Removed a duplicate search icon overlapping the headline
6. Pointed the CTA at that one flagship product instead of a generic banner link

Same brand, same product, same price. Just put the proof where a first-time visitor can actually see it.

DM me "AUDIT" if you want this done for your store.

#ShopifyDesign #CRO #eCommerce #ConversionOptimization #Ecommerce #UXDesign #SmallBusiness
```

## CRO-TAPRO-X1 (the rule)

```
If your best proof (price, rating, real customers) only shows up after a scroll, it's not doing its job. Move it up, not the design around it.
```

## CRO-TAPRO-X2 (before/after contrast)

```
Before: banner, big photo, video demo, no price, no rating, no product, scroll for proof.
After: thin banner, real price, real rating, real product, real trust strip, one CTA. Same brand.
```

## CRO-TAPRO-X3 (hot take)

```
A homepage that never shows a price or a product isn't minimalist, it's just missing the sale.
```

---

## Hook variations (unused, kept for reference)

1. TAPro's homepage never shows a price, a rating, or a product. Not on the first screen.
2. This brand has 15,500+ real business customers. Their homepage buries it behind a video demo and a product grid.
3. Real price. Real 4.9 star rating. Real flagship product. None of it visible on the first screen of this homepage.
4. A small NFC card brand with genuinely strong numbers, hidden behind a banner, a video, and a scroll.

## Twitter thread (unused, kept for reference)

1/ A small NFC review card brand has 15,500+ real business customers and a 4.9 star rating from 1,125 reviews. None of it shows up on the first screen of their homepage. Here's what I'd fix first.
2/ Landed on the homepage. First thing visible: a two-row black promo banner and a big hero photo. No price. No rating. No named product.
3/ Scroll past that and there's a full video demo, still no product, no price. Keep scrolling into a product grid and you finally hit their flagship card: $34.95, 4.9 stars, 1,125 reviews, over 15,500 businesses.
4/ The fix: pull the real price, rating, and flagship product up to the first screen, collapse the promo banner to one line, remove a duplicate search icon, and point the CTA at that one product instead of a generic banner link.
5/ The brand didn't need new proof. It needed the proof it already has moved to where a first-time visitor can actually see it. DM "AUDIT" if you want this done for your store.

---

## Export log

**2026-08-31**: First CRO Fix run for TAPro Cards, produced by the `koolestpro-weekly-cro-fix` scheduled task (unsupervised). Target: `target-tapro-1751673600003` (leadPotential High, visualPotential Medium). All numbers verified live against taprocard.com. content.html was hand-built after a DeepSeek delegation attempt dropped required export JS. The two graphics were built with a new PIL-based script (`build_tapro_graphics.py`) rather than the usual live CSS/SVG approach. A late em-dash sweep found 7 violations in the rebuild HTML, including in the visible headline, requiring a re-screenshot and re-export cycle before finalizing.

**2026-09-01**: Revision pass after review flagged 3 problems: the fake product placeholder icon looked broken, the after-panel in the before/after graphic had no contrast against its black background, and the "search icon on the headline" hook wasn't tangible enough. Fixed by swapping in TAPro's own real product photo (downloaded from their live product page), adding a backing card/shadow behind each phone panel in the before/after graphic, and rewriting the whole narrative around a corrected, verified finding: the homepage shows no price, rating, or product on the first screen at all, and the real $34.95 flagship card only appears deep in a product grid, past a full video demo. Also corrected the review count from 1,124 to the real Judge.me total of 1,125. All assets re-exported through the real capture pipeline and visually re-verified.

**2026-09-01 (second pass)**: Applied four new project-wide standing instructions. Removed the product photo's background (rembg/u2net) and composited it against a dark radial glow for a premium look; fixed the rebuild's above-the-fold layout so the product image grew to 280px uncropped (object-fit:contain) and the CTA/guarantee shifted down to close the dead-space gap that used to sit below them; rebuilt both visual-evidence graphics against a fresh screenshot with corrected pin coordinates; and grew the carousel from 6 to 8 slides, giving the cover slide a dominant product-photo visual and adding two new "THE EVIDENCE" slides that embed real crops of the before/after and annotated-changes graphics directly in the carousel. Caught and fixed a layout collision (page-number ghost numeral overlapping the evidence-slide headlines, annotated image running past the slide's height) during visual QA before finalizing. All assets re-exported and re-verified via the real capture pipeline.

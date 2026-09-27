# KOOLESTPRO CRO AUDIT BRIEF: Minimalist Niacinamide 10% Face Serum (PDP)

Unofficial concept audit by @koolestpro. Minimalist is not a client. Every number below was read from the live page or its policy pages on 2026-09-27 (mobile, 390x844).

## STORE DETAILS
- Store URL: https://beminimalist.co/products/niacinamide-10-with-matmarine
- Store name: Minimalist (Uprising Science Pvt Ltd, Jaipur)
- Page type: PDP
- Product: Niacinamide 10% Face Serum (with Matmarine + Zinc + acetyl glucosamine)
- Price: 30ml Rs 539 (MRP Rs 599, 10% off, incl. taxes). 60ml Rs 899 (MRP 999), 10ml Rs 237 (MRP 249), 20ml Rs 499
- Target customer: Indian shoppers with oily or acne-prone skin, acne marks, uneven tone; age 16+
- Audit date: 2026-09-27

## BRAND DECISION
- Decision: ELEVATE
- Rationale: The brand language (black type, white space, lab-label bottle, flat grey studio shots) fits a science-first skincare brand and should stay. The execution is the problem: hierarchy and order, not taste.
- Fonts: Proxima Nova (ProximaNovaA, served from the brand's own CDN), DM Sans, Nunito Sans in widgets
- Colors: black #000, white, light grey #E5E9EA (photo backdrop), orange announcement bar #FB6900
- Direction: keep Proxima Nova, black and grey; give the price and CTA real display weight; one orange accent only on the offer bar.

## MEASURED LAYOUT (390x844, live)
| Element | Top (px) | Screen |
|---|---|---|
| Product photo | 116 | 1 (fills it) |
| H1 "Niacinamide 10% Face Serum" | 813 | 1-2 (peeks at the bottom edge) |
| Rating row (1480 Reviews) | 903 | 2 |
| Price Rs 539 | 1576 | 2 |
| ADD TO CART | 1870 | 3 |
| Pregnancy/Lactation: Safe | inside "Ideal For" accordion, ~2080 | 3, collapsed |
| Shipping / returns | footer links only | last |

## CRO FINDINGS

**FINDING 1 (Critical, Above the Fold)**
Problem: The whole first screen is the product photo. The name starts at y=813, the price at y=1576 and Add to Cart at y=1870, more than two screens down.
Why it hurts: A shopper who does not scroll learns nothing except "a bottle". What it does, what it costs and how to buy are all below the fold.
Fix: Put an outcome headline, name, rating, price, size and one Add to Cart on the first screen. Blend the real studio photo into a matching #E5E9EA hero panel so it stays large without owning the screen.

**FINDING 2 (Critical, Value Proposition)**
Problem: The only headline is the SKU name. The actual benefit ("For reducing sebum & pores, and even skin tone") sits in 15px body text at ~y=950.
Why it hurts: The 5-second test fails. The outcome a buyer came for is not the first thing they read.
Fix: Headline "Control oil. Refine pores. Even out tone." over the hero (all three from the page's own copy), product name smaller underneath.

**FINDING 3 (High, Objection Handling)**
Problem: A support-chat bubble auto-opens with "Is this safe to use while pregnant?" on screen 1. The answer ("Pregnancy/Lactation: Safe") exists, but inside the collapsed "Ideal For" accordion around y=2080.
Why it hurts: The page raises the objection itself and then hides the answer. The bubble also covers the thumbnails on screen 1 and the price row on screen 2.
Fix: "Pregnancy-safe" and "Derm patch-tested" (both stated on the page) as benefit chips next to the price. No auto-opening chat over the buy zone.

**FINDING 4 (High, Product Info / Price)**
Problem: The price is set at 20px regular weight, after a size box and an MCash banner, inside a bordered box labelled "PRICE".
Why it hurts: The buyer has to hunt for the number. Rs 539 is a good price for the category and should be doing selling work.
Fix: Rs 539 at display weight next to the rating, MRP struck through and a "10% OFF" tag on the same line.

**FINDING 5 (High, Trust near CTA)**
Problem: Delivery info is a pincode field; shipping speed, COD and the replacement promise live only in footer policy links.
Why it hurts: Indian first-time buyers look for COD and delivery time before they commit.
Fix: A three-icon trust row directly under Add to Cart: ships in 48 hours, Cash on Delivery, 7-day replacement (all from the shipping/refund policies).

**FINDING 6 (Medium, Friction)**
Problem: Four offer cards (ATC10, B2G3RDFREE, B2GTRAVEL, ATC5) scroll sideways between the price and Add to Cart.
Why it hurts: Four codes to compare at the moment of purchase slows the tap.
Fix: Lead with the strongest offer in the top bar (Buy 2, Get 3rd Free), and move the offer cards below the CTA.

**FINDING 7 (Medium, Proof)**
Problem: The rating shows as stars + "1480 Reviews" at y=903, but the actual score (3.9) only appears in the reviews widget near y=3640.
Why it hurts: Hiding the number reads as hiding something. A shown 3.9 from 1,480 real reviews with its distribution is more credible than stars alone.
Fix: Show "3.9 · 1,480 reviews" inline on the first screen, linking to a real distribution bar (822 / 232 / 147 / 86 / 193).

**FINDING 8 (Medium, Visual Hierarchy)**
Problem: Size pills, the MCash banner, offer cards and the CTA all compete in black. The black Add to Cart is one of four black blocks.
Fix: Keep black for the single primary action and the selected size only.

## BUYER PSYCHOLOGY MAP
1. "What does this actually do for me?" -> photo-only first screen
2. "How much is it?" -> price 1,576px down
3. "Do people like it?" -> rating score hidden until y=3640
4. "Is this safe while I'm pregnant?" -> the page's own chat bubble
5. "Will it break me out?" -> non-comedogenic chip mid-page
6. "Which size should I get?" -> sizes in a bordered box with no prices
7. "Can I pay on delivery, and how fast does it come?" -> footer policies only
8. "Is there a deal if I buy more?" -> four offer cards in a side scroll

## ABOVE-THE-FOLD PRIORITY FIXES
1. Outcome headline + name over a hero that blends with the real photo
2. Rating 3.9 + 1,480 reviews inline
3. Price Rs 539 at display weight with MRP and 10% off
4. Pregnancy-safe + derm patch-tested chips
5. Size pills with prices, one Add to Cart, trust row under it

## RANKED TOP IMPROVEMENTS (drive headlines + annotations)
1. Price and Add to Cart moved from y=1576/1870 onto the first screen
2. Outcome headline replaces the photo-only first screen
3. The pregnancy question the page asks itself is answered next to the price

## IMAGE VERDICT
USE AS IS. Nia10New.png (1100x1600) is a sharp studio shot on flat #E5E9EA. Used uncropped (only empty backdrop trimmed) on a panel matched to the exact backdrop color so it blends.

## SKILL B HANDOFF
Full PDP; ELEVATE; Proxima Nova (real brand files) + black/grey; first-screen decision; sticky ATC only after the main CTA scrolls away; real logo PNG from the live header.

## MAIN CRO LESSON
A beautiful product photo is not a first screen. If the price and the button are two scrolls away, the photo is doing the whole job alone.

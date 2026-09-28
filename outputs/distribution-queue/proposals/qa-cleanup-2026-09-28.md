# Queue QA cleanup: 28 Sep 2026

> **APPLIED 2026-09-28 ~10:00 UTC.** The live Sheet showed 19 of the 35 "overdue" rows had already posted (local queue.json was behind). So only the 16 truly unposted rows were rescheduled (see `reschedule-2026-09-28-applied.json`, which replaces the table in section 3), and 7 caption fixes were applied. The other 7 targeted posts that were already live. Verified by reading the Sheet back. queue.json was synced to the Sheet (19 Posted statuses, 16 dates, 7 captions); backup at `queue.json.bak-2026-09-28-pre-qa-apply`.


Proposal only. Nothing in `queue.json` or the live Sheet has been changed. Approve it and I'll apply it, or edit anything first.

## 1. Number checks against the live stores

Checked 28 Sep 2026 on the live pages.

| Brand / post | Caption says | Live today | Verdict |
|---|---|---|---|
| TAPro Cards | 4.9 stars, 1,125 reviews | 4.9/5 from **1,155** reviews | Update. IG caption now says 'over 1,100' |
| TAPro Cards | 15,500+ businesses | 15,500+ businesses | ✅ correct |
| TAPro Cards | G-Series Onyx $34.95 | $34.95 sale price (regular $39) | ✅ correct. Note the card itself has 1 review (5.0); the 4.9/1,155 is store-wide, so say 'the brand' rather than 'the card' |
| Caraway Fry Pan | $125 | $125 (all colours) | ✅ correct |
| Caraway Fry Pan | 18,886 / 18,878 reviews | **19,981** reviews, 4.8 stars | Update to 'almost 20,000' in the 2 CRO captions. The static-ad caption no longer restates a count, because the ad image itself prints 4.7 · 18,878 |
| Caraway Fry Pan | Review line renders as the bare word "Reviews" | Seen live today: text read "Reviews" alone on first render | ✅ finding still holds |
| Caraway static ad | Quote 'Cooks evenly and quickly', Curtis M. | Not re-checked (reviews widget loads lazily) | ☐ Ridwan: find it in the reviews before posting |
| Kyte Baby Sleep Bag Oat 1.0 | 29,067 five-star reviews | **29,095** reviews averaging 4.9 (not all five-star) | Fix: '29,000+ reviews at 4.9 stars' (3 captions) |
| Gainful | No guarantee / cancel anytime / money back / risk free wording | None of those words on gainful.com or /pages/protein today | ✅ holds. I couldn't find the original customizer URL, so couldn't re-check that exact page |
| Gainful | Two stacked 25% offers | Only 'Subscribe and Save 25%' visible today | The X row doesn't use this claim, so no change needed |
| Checkout tip (Baymard) | 40% extra costs, 12% total cost, 9% payment methods | 40%, 12%, 9% (payment methods is 2nd from bottom, above 'I don't know' 7%) | ✅ correct |
| Checkout tip (Baymard) | 23.48 form elements, ideal 12–14 | 23.48 and 12–14 | ✅ correct |
| Typography tip (NN/g) | Users read at most ~28% of words | "at most 28% of the words during an average visit; 20% is more likely" (2008) | ✅ correct |
| Conversion Layer tip | 73% of Shopify redesigns don't lift conversions | No source found | ❌ Removed. New opener in the fixes below |
| Advertorial tip | Cold 1.5%, warmed-up 60%+ | No source; 60% isn't believable as a conversion rate | ❌ Replaced with the '1 to 2%' cold benchmark |
| Cold/Warm/Hot tip | 8% hot, 0.5% cold, averages ~2% | Worked example, not a statistic | OK as written ('a page converting…') |
| Pre-sell tip | Cold to PDP converts near 1–2% | In line with common benchmarks | OK |
| HALOS / Lumora / Meridian / Kura showcases | Flagged 'claims' | The flag caught the 'not a client' disclaimer, not a number | OK. Kura PDP-02 quotes '6,200-plus reviews' from the mock page, and the caption labels it a portfolio build |

**Still for you:** look over the images on each post (the 'manual-visual-pending' flag). I can't sign that off for you.

## 2. Caption fixes

**Over-length X captions:** every X row that will actually post is already under 280 characters (the longest is 275). The flag came from spare variants in the source content files, which never reach the queue. Nothing needed shortening. Clear that flag.

**Two real bugs found instead:** five Caraway static-ad tweets had a stray `158 chars` / `175 chars` line pasted in, which would have posted, and **all five were paired with the wrong image** (see the caption-to-image fix below). Each Caraway caption here was written after looking at its actual ad.

### cro-fix-tapro_google-review-cards-20260831-20260916-ig-1200
Instagram · 516 chars · Caption never named TAPro Cards (QA flag). Review count updated: live store now shows 1,155, so 'over 1,100' stays true as it grows.

```
TAPro Cards has 15,500+ business customers and a 4.9 star rating from over 1,100 reviews. You wouldn't know it from their homepage.

The first screen is a promo banner and a hero photo. You don't see a price, a rating or a product until you've scrolled past a full video demo and into the product grid.

Your first screen should say what's true about you straight away. TAPro's hides it.

Follow @koolestpro for weekly CRO breakdowns.

#ShopifyDesign #CRO #eCommerce #ConversionRate #Shopify #UXDesign #SmallBusiness
```

### cro-fix-tapro_google-review-cards-20260831-20260918-x-0900
Twitter · 216 chars · Named the brand and page type; the old version said only 'Same brand.'

```
TAPro Cards homepage.

Before: banner, big photo, video demo, then a long scroll before any proof.
After: thin banner, the real price, the real rating, the product, a trust strip, one CTA.

Same brand. Same products.
```

### cro-fix-caraway_fry-pan-pdp-20260907-20260923-li-0900
LinkedIn · 1008 chars · Live PDP now shows 19,981 reviews (4.8 stars). $125 price still correct.

```
Product Page (PDP) audit: Caraway's Fry Pan, on mobile.

You think almost 20,000 reviews means the trust is already there.

It doesn't, if the page can't render them in time.

Real findings, nothing invented:

The price sits top-right, aligned with the review line, disconnected from the title above it. On a fresh load, that review line can paint as the bare word "Reviews" with no stars and no count, right next to the price, exactly when a shopper is deciding if $125 is worth it. And depending on what's loaded above it, the product photo itself can land past the fold.

The rebuild moves price directly under the title, renders stars and count inline every time, and gives the real product photo (background removed, composited on a dark surface) the whole first screen.

Same product. Same price. The only thing that changed is the order the page tells its own story in.

Full before/after and annotated breakdown in the carousel.

Repost if this is useful to someone building a product page right now.
```

### cro-fix-caraway_fry-pan-pdp-20260907-20260925-x-0900
Twitter · 184 chars · Live PDP now shows 19,981 reviews.

```
On a live load, the review line can paint as literal text "Reviews," no stars, no count. Almost 20,000 real reviews exist. The fix: never let the number that matters most render empty.
```

### static-ad-caraway_fry-pan-20260909-20260916-x-1800
Twitter · 269 chars · Caption now matches the image it posts with: ad-2 (benefit), `ad-2-benefit-result.png`. Before, this row carried a caption written for a different ad in the set. The ad-3 caption no longer restates a review count, because the image itself prints '4.7 · 18,878 Reviews' (live PDP today: 4.8 · 19,981).

```
Benefit ad for Caraway's fry pan. One promise up top: a healthier way to cook every day.

Then the reasons it holds up. Non-toxic ceramic coating, oven safe to 550°F, works on gas, electric and induction, wipes clean.

No discount in this one. The pan does the selling.
```

### static-ad-caraway_fry-pan-20260909-20260921-x-0900
Twitter · 177 chars · Caption now matches the image it posts with: combined showcase (all four), `combined-showcase.png`. Before, this row carried a caption written for a different ad in the set. The ad-3 caption no longer restates a review count, because the image itself prints '4.7 · 18,878 Reviews' (live PDP today: 4.8 · 19,981).

```
Four ad directions from one $125 frying pan.

Problem. Benefit. Proof. Offer.

Same product, same photo brief. Only the first line changes.

Concept work off Caraway's live PDP.
```

### static-ad-caraway_fry-pan-20260909-20260919-x-1800
Twitter · 180 chars · Caption now matches the image it posts with: ad-4 (no forever chemicals), `ad-4-offer-urgency.png`. Before, this row carried a caption written for a different ad in the set. The ad-3 caption no longer restates a review count, because the image itself prints '4.7 · 18,878 Reviews' (live PDP today: 4.8 · 19,981).

```
Caraway's whole pitch is three letters they left out.

No PTFE. No PFOA. No PFAS.

So the ad leads with the worry, not the pan. The pan is the answer to a question you already had.
```

### static-ad-caraway_fry-pan-20260909-20260929-x-1300
Twitter · 271 chars · Caption now matches the image it posts with: ad-1 (retargeting/offer), `ad-1-problem-solution.png`. Before, this row carried a caption written for a different ad in the set. The ad-3 caption no longer restates a review count, because the image itself prints '4.7 · 18,878 Reviews' (live PDP today: 4.8 · 19,981).

```
Retargeting ad for someone who looked at a $125 pan and left.

It opens with "Still thinking about it?" and then clears what usually stops the purchase: free shipping over $90, 30-day returns, 4 payments of $32.

The price objection gets answered before anyone raises it.
```

### static-ad-caraway_fry-pan-20260909-20260925-x-1300
Twitter · 147 chars · Caption now matches the image it posts with: ad-3 (social proof), `ad-3-social-proof.png`. Before, this row carried a caption written for a different ad in the set. The ad-3 caption no longer restates a review count, because the image itself prints '4.7 · 18,878 Reviews' (live PDP today: 4.8 · 19,981).

```
The strongest line in this ad was not written by a marketer.

"Cooks evenly and quickly."

Curtis M., verified buyer.

Real beats clever most days.
```

### cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260923-x-1300
Twitter · 248 chars · Review count updated: the live PDP shows 29,095 reviews at 4.9 stars. The X/OK contrast markers stay, since they're your playbook pattern.

```
Kyte Baby's PDP: same button, different signal.

Before:
X Gray CTA, looks disabled
X Trust buried below a TOG slider

After:
OK Red CTA, reads as active
OK Trust sits right under the button

29,000+ reviews already agreed.
Now the button does too.
```

### cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260927-x-1800
Twitter · 204 chars · They are not all five-star: the live page shows 29,095 reviews averaging 4.9.

```
Kyte Baby's PDP already had 29,000+ reviews at 4.9 stars.

Then the buy button rendered flat gray, like it was disabled.

Fixed the button. Not the proof.

Same product.
Better signal = better conversion.
```

### cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260923-li-0900
LinkedIn · 905 chars · They are not all five-star: the live page shows 29,095 reviews averaging 4.9.

```
PRODUCT PAGE (PDP): Kyte Baby's Sleep Bag in Oat 1.0 already had over 29,000 reviews at 4.9 stars and real safety certifications above the fold. Then the buy button rendered flat gray, no size selected, reading as disabled at the exact moment a shopper was ready to act.

The fix wasn't more proof. The proof was already there. It was the button.

Three changes:
1. Recolored the CTA to high-contrast red. Never gray, never looks disabled.
2. Moved shipping, returns, and Afterpay right under the button instead of a full scroll away, buried below a temperature slider.
3. Called out the AAP-compliant and OEKO-TEX certifications as benefit chips, not buried copy.

Same product. Same reviews. A button that finally matches the trust the page already earned.

This is unofficial portfolio work, not a Kyte Baby engagement. Repost if you've ever shipped a page that proved itself right up until the button.
```

### tip-advertorial-what-it-actually-is-20260510-20260817-li-0900
LinkedIn · 907 chars · 'Warmed-up traffic can hit 60%+' has no source and isn't believable as a conversion rate. Dropped it.

```
You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing.

Most Shopify brands treat it like homework. Copy from the ad, stretch it out, ship it, move on.

Cold traffic sent straight to a product page usually converts somewhere around 1 to 2%. The page that's meant to warm it up first is the one most brands never build properly.

An advertorial isn't a landing page. It isn't a blog post either. Its only job is making a stranger believe you before anything else.

It runs on 3 beats that actually carry the weight:

The hook that stops the scroll.

The proof that kills the doubt.

The reveal that earns the click.

Everything else on the page just clears the path between those three.

Before you write your next one, ask yourself this: does this page make a stranger believe you before it asks them to buy? If not, it's just copy.

Save this for your next funnel build.
```

### tip-the-conversion-layer-1777028149144-20260824-li-0900
LinkedIn · 1122 chars · No source exists for '73% of Shopify redesigns'. Opened on the point itself instead, and removed the em dashes (project style rule).

```
A redesign can make your store look better and sell exactly the same.

Not because the design was bad.
Because the wrong problem was solved.

Most store owners jump straight to Figma. New hero image. Bigger fonts. Trending layout. It looks cleaner. But conversion barely moves.

What's missing is the Conversion Layer.

It's the strategic audit you run before a single pixel moves. Three questions answer everything:

→ Clarify: What does this page need to communicate? What's the buyer's one burning question?
→ Construct: Does the layout follow the buyer's journey, or your designer's preference?
→ Convert: What's the single action this page must drive? Is every element pointing there?

That's the 3C Framework.

Before I open Figma on any CRO project, I run this. 15 minutes of diagnosis saves 3 weeks of redesign that doesn't move the needle.

The Conversion Layer isn't a style choice. It's a strategic brief. And it's the difference between a page that looks better and a page that sells more.

Save this. Share it with your designer before the next brief.

Follow @koolestpro for Shopify CRO & UX tips every week.
```

## 3. Reschedule proposal (35 overdue rows)

Rules applied: max 1 LinkedIn post/day, no two rows on the same platform at the same date+time, no collisions with rows already scheduled, the same brand never twice on one day, and a post's X rows at least 2 days apart. Times are `scheduled_time_local` (14:00 = 09:00 ET, 23:00 = 18:00 ET). Clean rows go first; QA-flagged rows after them, so you have time to review.

⚠️ Built from `queue.json` (last written 27 Sep 16:06). The live Sheet is ahead of it, so check these slots against the Sheet before applying. The reschedule webhook doesn't check for collisions.

| New date | Time | Platform | QA | post_id | Was |
|---|---|---|---|---|---|
| 2026-09-29 | 14:00 | LinkedIn | clean | `template-showcase-kura_pp-01-20260721-20260918-li-0900` | 2026-09-18 14:00 |
| 2026-09-30 | 14:00 | Twitter | clean | `idea-why-your-pdp-loses-sales-at-60-scroll-1776763992475-os77l-20260826-x-1300` | 2026-09-18 9:00 |
| 2026-10-01 | 14:00 | LinkedIn | needs review | `template-showcase-kura_pdp-01-2026-08-31-20260911-li-0900` | 2026-09-11 14:00 |
| 2026-10-01 | 14:00 | Twitter | clean | `template-showcase-halos_pdp-01-2026-07-31-20260820-x-1300` | 2026-09-20 9:00 |
| 2026-10-01 | 23:00 | Twitter | clean | `static-ad-bebemoss_ginger-sleepy-bunny-20260717-20260829-x-1800` | 2026-09-21 13:00 |
| 2026-10-02 | 23:00 | Twitter | needs review | `cro-fix-gainful_customize-your-protein-20260823-20260906-x-1800` | 2026-09-07 14:00:00 |
| 2026-10-03 | 14:00 | LinkedIn | needs review | `template-showcase-halos_hp-01-2026-08-18-20260828-li-0900` | 2026-09-12 14:00 |
| 2026-10-03 | 23:00 | Twitter | needs review | `template showcase-lumora_store-template-20260828-20260915-x-1300` | 2026-09-15 18:00 |
| 2026-10-04 | 14:00 | LinkedIn | needs review | `idea-checkout-abandonment-fix-the-payment-method-order-1777030231175-ebzqg-20260914-li-0900` | 2026-09-14 14:00 |
| 2026-10-04 | 14:00 | Twitter | needs review | `template-showcase-kura_pdp-01-2026-08-31-20260915-x-0900` | 2026-09-15 14:00 |
| 2026-10-05 | 14:00 | Twitter | needs review | `template-showcase-halos_ad-01-20260905-20260913-x-1100` | 2026-09-13 16:00 |
| 2026-10-05 | 23:00 | Twitter | needs review | `cro-fix-tapro_google-review-cards-20260831-20260916-x-1300` | 2026-09-16 18:00 |
| 2026-10-06 | 14:00 | LinkedIn | needs review | `template showcase-meridian_store-template-20260828-20260915-li-0900` | 2026-09-15 14:00 |
| 2026-10-06 | 23:00 | Twitter | needs review | `static-ad-caraway_fry-pan-20260909-20260916-x-1800` | 2026-09-16 23:00 |
| 2026-10-07 | 14:00 | LinkedIn | needs review | `tip-advertorial-what-it-actually-is-20260510-20260817-li-0900` | 2026-09-16 9:00 |
| 2026-10-07 | 14:00 | Twitter | needs review | `cro-fix-tapro_google-review-cards-20260831-20260918-x-0900` | 2026-09-18 14:00 |
| 2026-10-07 | 23:00 | Twitter | needs review | `cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260923-x-1300` | 2026-09-23 18:00 |
| 2026-10-08 | 14:00 | LinkedIn | needs review | `template showcase-lumora_store-template-20260828-20260908-li-0900` | 2026-09-16 9:00 |
| 2026-10-08 | 14:00 | Twitter | needs review | `template showcase-meridian_store-template-20260828-20260916-x-0900` | 2026-09-16 14:00 |
| 2026-10-08 | 23:00 | Twitter | needs review | `static-ad-caraway_fry-pan-20260909-20260919-x-1800` | 2026-09-19 23:00 |
| 2026-10-09 | 14:00 | LinkedIn | needs review | `tip-the-conversion-layer-1777028149144-20260824-li-0900` | 2026-09-19 9:00 |
| 2026-10-09 | 14:00 | Twitter | needs review | `cro-fix-tapro_google-review-cards-20260831-20260920-x-1800` | 2026-09-20 23:00 |
| 2026-10-09 | 23:00 | Twitter | needs review | `template-showcase-kura_pdp-02-20260919-20260924-x-1300` | 2026-09-24 18:00 |
| 2026-10-10 | 14:00 | LinkedIn | needs review | `idea-typography-hierarchy-that-converts-the-6-level-sys-1777030231175-j3p4a-20260921-li-0900` | 2026-09-21 14:00 |
| 2026-10-10 | 23:00 | Twitter | needs review | `template showcase-meridian_store-template-20260828-20260918-x-1300` | 2026-09-18 18:00 |
| 2026-10-11 | 14:00 | LinkedIn | needs review | `cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260923-li-0900` | 2026-09-23 14:00 |
| 2026-10-11 | 14:00 | Twitter | needs review | `static-ad-caraway_fry-pan-20260909-20260921-x-0900` | 2026-09-21 14:00 |
| 2026-10-12 | 14:00 | LinkedIn | needs review | `template-showcase-kura_pdp-02-20260919-20260925-li-0900` | 2026-09-25 14:00 |
| 2026-10-12 | 14:00 | Twitter | needs review | `template showcase-meridian_store-template-20260828-20260919-x-0900` | 2026-09-19 14:00 |
| 2026-10-13 | 14:00 | Twitter | needs review | `static-ad-caraway_fry-pan-20260909-20260925-x-1300` | 2026-09-25 18:00 |
| 2026-10-13 | 23:00 | Twitter | needs review | `cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260925-x-0900` | 2026-09-25 14:00 |
| 2026-10-14 | 14:00 | Twitter | needs review | `template showcase-meridian_store-template-20260828-20260922-x-1300` | 2026-09-22 18:00 |
| 2026-10-14 | 23:00 | Twitter | needs review | `template-showcase-kura_pdp-02-20260919-20260926-x-0900` | 2026-09-26 14:00 |
| 2026-10-15 | 14:00 | Twitter | needs review | `cro-fix-kytebaby-sleep-bag-oat-1-0-pdp-20260920-20260927-x-1800` | 2026-09-27 23:00 |
| 2026-10-16 | 14:00 | Twitter | needs review | `template-showcase-kura_pdp-02-20260919-20260927-x-1100` | 2026-09-27 16:00 |

# Gainful — Social Content Library

Machine-readable sibling: `gainful-social-content.json` (same keys). Update both together, never let them drift.

## HOW TO USE THIS FILE

| Key | Asset | Platform | Status |
|---|---|---|---|
| `CRO-GAINFUL-BA` | koolestpro_gainful_before-after.png | linkedin, instagram | Not Posted |
| `CRO-GAINFUL-ANNO` | koolestpro_gainful_annotated-changes.png | linkedin, instagram | Not Posted |
| `CRO-GAINFUL-CAROUSEL` | koolestpro_gainful_customize-your-protein_slide1.png … (6 slides) | linkedin, instagram | Not Posted |
| `CRO-GAINFUL-X1` | koolestpro_gainful_before-after.png | x | Not Posted |
| `CRO-GAINFUL-X2` | koolestpro_gainful_annotated-changes.png | x | Not Posted |
| `CRO-GAINFUL-X3` | koolestpro_gainful_customize-your-protein_slide1.png | x | Not Posted |
| `CRO-GAINFUL-XTHREAD` | koolestpro_gainful_before-after.png | x | Not Posted |

> Pipeline item: `cro-fix-gainful_customize-your-protein-20260823`
> Source file: `outputs/cro-fixes/gainful_customize-your-protein_content.html`
> Audit brief: `outputs/audits/gainful_customize-your-protein_audit.md`

## Export log

- 2026-08-23 — CRO Fix run (koolestpro-weekly-cro-fix). All 8 images exported headlessly via .ai-workflow/tools/export_static_images.py, which drives the content file's own captureFixed()/captureSlide() html2canvas functions, not a native screenshot. Every PNG was decoded and visually reviewed; the before/after headline was also checked at 300px thumbnail scale per project-constitution.md.

- 2026-08-23 — CORRECTION during the run: the first 'before' capture rendered Gainful's star emoji in the top promo bar as tofu boxes, because headless Chromium in this sandbox had no emoji font. That is a capture artifact, NOT a site defect, and publishing it would have misrepresented the brand. Noto Color Emoji was installed and the before screenshot was re-captured; the stars now render correctly in the shipped graphic.

- 2026-08-23 — The re-captured 'before' includes a real teal floating cart/chat bubble in the lower right that overlaps the 'Skip flavors and save $5.98' row. It is genuinely on the live page (it did not appear in the first load), so it was left in rather than re-shot for a cleaner frame.


## Captions

### CRO-GAINFUL-BA

**Option `ba-primary`** (pick one at post time, do not post both against the same image)

```
Gainful asks you four questions before it gives you one reason to trust it.

Their protein customizer is a good idea. Pick a dietary preference, pick a goal, get a formula matched to it. On mobile it opens with two different 25% discounts stacked on top of each other, one for subscribing and one for a new customer code, and nothing on the page tells you whether they stack or which one you should take.

Then it asks for four decisions. Dietary preference. Primary goal. Serving size. Flavour packets.

And it never offers you a way to buy.

I searched every button and link on that page. There is no add to cart. No buy button. No checkout. The only call to action anywhere is Take The Quiz, sitting 3,693 pixels down, and it sends you into a different funnel than the one you were already halfway through.

The words guarantee, money back, cancel anytime and risk free do not appear on the page either. That last one matters, because the loudest thing on the screen is asking you to start a subscription.

So I rebuilt the top of it. Same type, same warm grey, same black pills, same photography.

One promo strip instead of two, and the subscribe offer moved down to the buy area where it is an actual choice.
Price given its own line at 29px with a per serving figure under it, because on a configurator the price is the running total.
A sticky bar carrying the live price and an add to cart, so the endpoint is visible from the first tap.
Cancel or skip anytime, sitting right where the subscription is being asked for.
The review count turned into a link you can actually check.
One line above the two selectors naming what they produce.

Nothing invented. Every number is Gainful's own, read off the live page: $31.47, 14 servings, 20g protein, 100 calories, 6 ingredients, 2,123 ratings.

If your page asks the shopper to do work, it owes them somewhere to put it.

Ridwan

The review quote in the rebuild is an illustrative placeholder, labelled as such in the file, not a real Gainful customer.
```

**Option `ba-short`** (pick one at post time, do not post both against the same image)

```
Gainful asks you four questions before it gives you one reason to trust it.

Dietary preference. Primary goal. Serving size. Flavour packets.

Then nothing. No add to cart anywhere on the page. I checked every button and link on it. The only CTA is Take The Quiz, 3,693 pixels down, and it routes you into a different funnel.

No guarantee either. No cancel anytime. On a page whose top bar is selling a subscription.

So I rebuilt the top of it, same brand, nothing redesigned:

One promo strip instead of two competing 25% offers
Price as an anchor with a per serving read
A sticky add to cart carrying the live price
Cancel or skip anytime, next to the subscribe offer
The review count as a real link

Every number is theirs. $31.47, 14 servings, 20g protein, 2,123 ratings.

If your page asks the shopper to do work, give them somewhere to put it.

#ecommerce #shopify #cro #conversionrateoptimization #dtc #uxdesign
```

### CRO-GAINFUL-ANNO

```
Gainful asks you four questions before it gives you one reason to trust it.

Dietary preference. Primary goal. Serving size. Flavour packets.

Then nothing. No add to cart anywhere on the page. I checked every button and link on it. The only CTA is Take The Quiz, 3,693 pixels down, and it routes you into a different funnel.

No guarantee either. No cancel anytime. On a page whose top bar is selling a subscription.

So I rebuilt the top of it, same brand, nothing redesigned:

One promo strip instead of two competing 25% offers
Price as an anchor with a per serving read
A sticky add to cart carrying the live price
Cancel or skip anytime, next to the subscribe offer
The review count as a real link

Every number is theirs. $31.47, 14 servings, 20g protein, 2,123 ratings.

If your page asks the shopper to do work, give them somewhere to put it.

#ecommerce #shopify #cro #conversionrateoptimization #dtc #uxdesign
```

Hashtags: #ecommerce #shopify #cro #dtc #uxdesign

### CRO-GAINFUL-CAROUSEL

```
Gainful asks you four questions before it gives you one reason to trust it.

Their protein customizer is a good idea. Pick a dietary preference, pick a goal, get a formula matched to it. On mobile it opens with two different 25% discounts stacked on top of each other, one for subscribing and one for a new customer code, and nothing on the page tells you whether they stack or which one you should take.

Then it asks for four decisions. Dietary preference. Primary goal. Serving size. Flavour packets.

And it never offers you a way to buy.

I searched every button and link on that page. There is no add to cart. No buy button. No checkout. The only call to action anywhere is Take The Quiz, sitting 3,693 pixels down, and it sends you into a different funnel than the one you were already halfway through.

The words guarantee, money back, cancel anytime and risk free do not appear on the page either. That last one matters, because the loudest thing on the screen is asking you to start a subscription.

So I rebuilt the top of it. Same type, same warm grey, same black pills, same photography.

One promo strip instead of two, and the subscribe offer moved down to the buy area where it is an actual choice.
Price given its own line at 29px with a per serving figure under it, because on a configurator the price is the running total.
A sticky bar carrying the live price and an add to cart, so the endpoint is visible from the first tap.
Cancel or skip anytime, sitting right where the subscription is being asked for.
The review count turned into a link you can actually check.
One line above the two selectors naming what they produce.

Nothing invented. Every number is Gainful's own, read off the live page: $31.47, 14 servings, 20g protein, 100 calories, 6 ingredients, 2,123 ratings.

If your page asks the shopper to do work, it owes them somewhere to put it.

Ridwan

The review quote in the rebuild is an illustrative placeholder, labelled as such in the file, not a real Gainful customer.
```

### CRO-GAINFUL-X1

```
ANGLE 1: the missing button

Gainful's protein customizer asks for 4 decisions.

Dietary preference. Goal. Serving size. Flavour packets.

Then gives you nowhere to buy.

I searched every button and link on the page. There is no add to cart on it.
```

### CRO-GAINFUL-X2

```
Product page audit: Gainful.

Two 25% discounts stacked at the top. One for subscribing, one for a new customer code.

Nothing says whether they stack, or which is better.

Ambiguity at the offer level is the expensive kind. It hits every visitor before the product.
```
<!-- Label: ANGLE 2: the two offers. Rewritten 2026-09-18, was 301 chars (over X's 280 cap), now 266. -->


### CRO-GAINFUL-X3

```
Product page audit: Gainful.

Guarantee. Money back. Cancel anytime. Risk free.

None of those words appear on the customizer page. The loudest thing on screen asks you to start a subscription.

Ask for a recurring commitment without the exit terms and the take rate drops.
```
<!-- Label: ANGLE 3: the missing safety net. Rewritten 2026-09-18, was 328 chars (over X's 280 cap), now 273. -->


### CRO-GAINFUL-XTHREAD

```
1/ Gainful asks you four questions before it gives you one reason to trust it.

Their protein customizer, on mobile. A teardown.

2/ It opens with two different 25% offers stacked on top of each other.

One for subscribing. One for a new customer code.

Nothing says whether they stack or which one you should take.

3/ Then it asks for four decisions.

Dietary preference. Primary goal. Serving size. Flavour packets.

4/ And it never offers you a way to buy.

I searched every button and link on the page. No add to cart. No buy button. No checkout.

5/ The only CTA anywhere is Take The Quiz, 3,693 pixels down.

It sends you into a different funnel than the one you were already halfway through.

6/ Guarantee. Money back. Cancel anytime. Risk free.

None of those words appear on the page.

The loudest thing on the screen is selling a subscription.

7/ So I rebuilt the top. Same type, same warm grey, same black pills.

One promo strip. Price as an anchor with a per serving read. A sticky add to cart. Cancel or skip anytime.

8/ Every number is Gainful's own, read off the live page.

$31.47. 14 servings. 20g protein. 100 calories. 6 ingredients. 2,123 ratings.

9/ If your page asks the shopper to do work, it owes them somewhere to put it.
```

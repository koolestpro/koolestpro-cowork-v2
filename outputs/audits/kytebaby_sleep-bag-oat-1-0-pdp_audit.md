# Audit: Kyte Baby -- Sleep Bag in Oat 1.0 TOG (PDP)

**URL:** https://kytebaby.com/products/sleep-bag-in-oat-1-0
**Reviewed:** 2026-09-20, mobile viewport (390x844 @2x), real Playwright screenshot.
**Target record:** target-kyte-baby-1751673600010 in targets_pool.json (zero prior cro-fix usedFor entries; this is a different page/product than the pending 2026-09-18 static-ad run, which used the same product but for a different stream/creative).

## What's already working

- Rating (5 stars, 29,067 reviews) and price ($55, Afterpay 4x$13.75) both render above the fold on load, no third-party widget delay.
- Real product photography is strong: a clean flat studio shot and a genuine lifestyle photo of a sleeping newborn in the bag.
- Copy substance is real and specific: AAP-compliant safe sleep claim, OEKO-TEX Standard 100 certification, J-shaped double zipper with a "zipper garage," hip-healthy cut. None of this is generic filler.
- "BEST SELLER" badge and "In stock" indicator both present.

## The #1 finding

The page has already done the hard work of proving itself (29K+ reviews, real safety certifications, a real value line) by the time a shopper reaches the buy button -- and then the button itself renders as a flat mid-gray bar that reads as disabled. Sampled directly from the live page: the "Select a Size $55 USD" button is RGB(153,153,153) / #999999, with white text, no size preselected. It is technically tappable, but visually indistinguishable from a disabled state. This is the single biggest miss: the page converts a shopper's attention right up to the moment they'd act, then hands them a button that looks like it isn't ready yet.

## Supporting findings (real, all verified on the rendered screenshot)

1. **Trust row is pushed away from the CTA.** Immediately after the (gray) button, the page inserts a large "Recommended Room Temperature" TOG slider block (roughly 600px tall) before any shipping/returns/trust signal appears. Trust should sit right next to the buy action; here it's a full scroll away.
2. **Shipping/trust icon row overflows the mobile viewport.** Further down, a horizontal row of three icons ("Shipping Details / Returns / STANDARD...") clips its third label mid-word at the 390px width -- a real layout bug, not a design choice.
3. **No visible primary/secondary CTA hierarchy problem otherwise** -- there's only one CTA button, which is correct; the issue is its rendering, not competing buttons.

## Rebuild scope

Keep everything that already works (real photos, real rating/price, real safety facts). Fix: the CTA's visual weight (high-contrast brand color, never a gray "looks disabled" state), move the trust row to sit directly under the CTA, and fix the icon-row overflow. See `kytebaby_sleep-bag-oat-1-0-pdp_facts.json` and `_build-brief.md` for the full real-facts brief handed to the page builder.

No fabricated metrics. No implied client relationship -- Kyte Baby is not a Koolestpro client; this is unofficial portfolio/concept work.

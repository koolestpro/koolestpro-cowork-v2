# Kyte Baby - Sleep Bag in Oat 1.0 TOG (PDP) rebuild brief

Paste everything below into Lovable or Figma Make as the project prompt.
Then publish, and pull it back with `.ai-workflow/tools/capture_page.py`.

---

Build me a mobile product page for **Kyte Baby**, page: Sleep Bag in Oat 1.0 TOG (PDP).
Source of truth for the real page: https://kytebaby.com/products/sleep-bag-in-oat-1-0

Audience: new and expecting parents shopping for a safe-sleep wearable blanket
The one job of this page: **make the already-strong proof and safety story convert, by fixing the one button that currently reads as disabled**.

## Non-negotiable rules

- Use ONLY the real facts listed below. Invent nothing. No invented numbers,
  quotes, guarantees, or results.
- Mobile first, design at a 390px viewport.
- The real brand logo and the real product photo must be used as-is. Never
  recreate or redraw a logo.
- No gradient text (CSS or SVG).
- The first screen must carry the whole decision: outcome headline, price,
  rating and review count, benefit reasons, a trust row, and the add to cart.

## Image decision (do this BEFORE you build)

Decide the hero image after the plan, not before. Steps:

1. Write the build plan first (the sections below).
2. Look for a usable hero photo on the site. If there is a great one, use it.
3. If there is no good photo, or nothing is good enough, generate a suitable
   version with AI and build the page on that image.
4. A homepage uses the same process as a product page.

Per-build decision:
- Plan: Real product photography already exists and is strong (studio flat shot + real lifestyle shot of a sleeping newborn in the bag). Use the real hotlinked site photos as-is.
- Site photo: Real flat product shot and real lifestyle photo both exist and are usable, hotlinked above.
- Decision: Use the real site photo, no AI generation needed for this rebuild.
- Note: No image regeneration required; the visual problem is the CTA and layout, not the product photography.


## Real facts to use (traceable to the live page)

- 5-star rating, 29,067 reviews
- $55 USD (XS-L), $65 USD (XL)
- 4 interest-free payments of $13.75 with Afterpay; Shop Pay also offered
- AAP-compliant safe sleep design, reduces SIDS risk for babies under 12 months by replacing loose bedding
- OEKO-TEX Standard 100 certified
- J-shaped double zipper with zipper garage: zips from top or bottom for diaper changes without disturbing sleep; covered pull protects baby's skin
- Fabric: 97% Rayon made from Bamboo, 3% Spandex; Filling: 100% Polyester
- Hip-healthy design: roomy at the bottom for natural froggy leg position
- Sizes XS-XL, fits 7-50 lbs
- 1.0 TOG, recommended room temperature 69-73F
- Free shipping for US orders over $85
- Easy returns within 45 days of purchase
- 'The Original Bamboo Sleep Bag(TM)', making sleep bags since 2014
- In stock

Verify before publishing:

- [ ] star rating and 29,067 review count: confirm live count before publishing (site count changes daily)
- [ ] current CTA button color: sampled at RGB(153,153,153) / #999999 on the live mobile page, 2026-09-20 (flat mid-gray, no size selected yet)
- [ ] shipping/returns icon row: third label ('STANDARD...') is visually clipped at the 390px mobile viewport edge on the live page

## Outcome headline options (pick one, or improve on it)

  1. The proof was never the problem. The button was.
  2. 29,067 reviews in. One gray button in the way.
  3. Same bag. A button that actually looks ready to tap.

## Benefit reasons (real, on the product)

- AAP-compliant safe sleep, built to reduce SIDS risk under 12 months
- OEKO-TEX Standard 100 certified fabric
- J-shaped double zipper: change diapers without waking the baby
- Hip-healthy cut for natural leg position

## Trust row (next to the add to cart)

- Free shipping over $85
- Easy 45-day returns
- Afterpay: 4 interest-free payments of $13.75

## Sections, top to bottom

- 1. Slim announcement bar: 'Easy returns within 45 days of purchase' (matches real site copy)
- 2. Header: real Kyte Baby logo, cart icon
- 3. Hero: real product photo full-bleed or large, with a BEST SELLER badge (real, on the live page)
- 4. Rating row: filled stars + '29,067' review count, rendered on load, immediately under the hero
- 5. Product name + one-line outcome headline (not just 'Sleep Bag in Oat 1.0') + price ($55 USD) at display weight, with the Afterpay line directly under it
- 6. Color/size selector (Oat preselected)
- 7. ONE primary CTA: 'Add to Cart - $55 USD', HIGH CONTRAST (brand color, not gray), never rendered as a disabled-looking gray bar even before a size is chosen
- 8. Trust row immediately under the CTA: free shipping over $85, 45-day returns, AAP-compliant / OEKO-TEX certified badges with real icons -- no horizontal overflow, everything fits the 390px viewport
- 9. Benefit chips (2-4): AAP-compliant safe sleep, OEKO-TEX certified, J-shaped double zipper, hip-healthy design
- 10. TOG / room-temperature detail can stay, but AFTER the trust row, not between the CTA and the trust row
- 11. Details / fabric accordion, cross-sell, footer

## Assets to upload

- Real logo (SVG, hotlink)  [https://kytebaby.com/cdn/shop/files/kyte-baby-logo.svg?v=1748269517&width=800] - Use exactly as-is, no redraw. Black kite mark + wordmark.
- Real product photo (flat, hotlink)  [https://kytebaby.com/cdn/shop/files/kyte-baby-sleep-bag-1-0-tog-sleep-bag-in-oat-1-0-32790597795951.jpg?v=1759956342&width=700] - Clean flat product shot of the Oat 1.0 sleep bag, use as the primary hero/product image.
- Real lifestyle photo (hotlink)  [https://kytebaby.com/cdn/shop/files/Oat_Sleep_Bag_1.0-02.jpg?v=1759956342&width=700] - Newborn sleeping in the Oat sleep bag, optional secondary image.

## Do not

- a gray/disabled-looking Add to Cart or 'Select a Size' button -- this is the exact bug being fixed
- burying the trust row (shipping/returns/certifications) below the TOG temperature slider -- trust must sit right next to the CTA
- a shipping/returns icon row that overflows or clips text on a 390px viewport
- inventing any review count, rating, or claim not listed above
- recreating the Kyte Baby logo in a similar font -- use the real hotlinked SVG
- gradient text, CSS or SVG
- implying Kyte Baby is a Koolestpro client -- this is unofficial portfolio/concept work

## Output

A finished, responsive mobile product page I can publish and screenshot at
390x844. Real copy only. Tell me if any fact above is missing or contradictory
instead of guessing.

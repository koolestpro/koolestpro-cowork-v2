# Minimalist - Niacinamide 10% Face Serum (PDP) rebuild brief

Paste everything below into Lovable or Figma Make as the project prompt.
Then publish, and pull it back with `.ai-workflow/tools/capture_page.py`.

---

Build me a mobile product page for **Minimalist**, page: Niacinamide 10% Face Serum (PDP).
Source of truth for the real page: https://beminimalist.co/products/niacinamide-10-with-matmarine

Audience: Indian skincare shoppers with oily or acne-prone skin who want a science-first serum for oil, pores, acne marks and uneven tone
The one job of this page: **put the whole buying decision (what it does, price, proof, size, Add to Cart, delivery) on the first mobile screen, instead of a screen-filling photo with everything else 1,600px below**.

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
- Plan: The page's job is a first-screen decision; the product itself is simple and the studio shot is strong.
- Site photo: Nia10New.png is a clean, sharp studio shot on flat light grey with a soft shadow. Genuinely good.
- Decision: Use the real site photo as-is, uncropped, on a hero panel colored to match its exact background (#E5E9EA) so it blends. No AI generation needed.
- Note: The problem is the order of the page, not the photography.


## Real facts to use (traceable to the live page)

- Product name on page: Niacinamide 10% Face Serum (with Matmarine + Zinc + acetyl glucosamine, per the bottle label)
- Page benefit line: 'For reducing sebum & pores, and even skin tone'
- Description: pure Vitamin B3 (Niacinamide) and Matmarine; reduces sebum, improves the barrier, evens skin tone; Matmarine reduces excess sebum, shine, pores & spots
- Rating widget: 3.9 based on 1480 reviews (822 five-star, 232 four-star, 147 three-star, 86 two-star, 193 one-star)
- Price 30ml: Rs 539, MRP Rs 599, 10% off (incl. of all taxes). 60ml Rs 899 (MRP 999), 10ml Rs 237 (MRP 249), 20ml Rs 499
- Chips on page: Fragrance Free, Non-comedogenic, Essential Oil Free, pH 5.5 - 6.5
- Best Seller badge on the hero image
- Offers: ATC10 extra 10% off over Rs 599; B2G3RDFREE buy 2 get the 3rd free; B2GTRAVEL free travel pouch; ATC5 extra 5% off over Rs 299
- Real review quote on page: 'I've been using it for past 3-4 months. I'm on my 2nd bottle... I had uneven skin tone, acne scar marks and now it's almost gone.' - Charu S.
- Usage: AM / PM, everyday
- Shipping policy: ships within 48 working hours; delivery 2 to 10 days, about 3 days in Delhi, Mumbai, Kolkata, Bangalore; delivers to 20,000+ pin codes; Cash on Delivery available (+Rs 70)
- Return policy: refund/replacement for wrong, damaged or expired product within 7 days of delivery
- Earn 5% MCash on every order, post-delivery

Verify before publishing:

- [ ] Measured on the live 390x844 mobile page 2026-09-27: H1 top at y=813 (first screen is the photo only), rating row y=903, price y=1576, ADD TO CART y=1870
- [ ] A support-chat bubble ('Is this safe to use while pregnant?') overlays the image thumbnails on the first screen and the price row on the second
- [ ] Rating 3.9 / 1480 reviews: confirm live before publishing; the count changes

## Outcome headline options (pick one, or improve on it)

  1. Less oil. Smaller-looking pores. Even tone.
  2. Oil, pores and marks, handled in one serum.

## Benefit reasons (real, on the product)

- 10% Niacinamide + Zinc for oil and pores
- Matmarine for excess shine and spots
- Fragrance free, non-comedogenic
- pH 5.5 - 6.5

## Trust row (next to the add to cart)

- Ships in 48 working hours
- Cash on Delivery available
- 7-day replacement if damaged, wrong or expired

## Sections, top to bottom

- 1. Slim offer bar: 'Buy 2, Get 3rd Free' (real offer)
- 2. Header: real Minimalist logo, cart
- 3. Hero on #E5E9EA: real bottle photo, uncropped, beside the outcome headline + product name
- 4. Rating row inline (3.9 stars, 1,480 reviews) + Best Seller
- 5. Price Rs 539 with MRP Rs 599 and 10% off, at display weight, next to the name
- 6. Size selector (30ml preselected) as compact pills
- 7. ONE primary CTA: Add to Cart, Rs 539
- 8. Trust row directly under the CTA: 48h dispatch, COD, 7-day replacement
- 9. Benefit chips: fragrance free, non-comedogenic, essential oil free, pH 5.5-6.5
- 10. Below the fold: real review quote, offers, what makes it potent, how to use, reviews

## Assets to upload

- Real logo (PNG)  [outputs/cro-fixes/minimalist/_assets/logo.png] - Downloaded from the live header img (Minimalist-Logo-PNG.png). Embed as-is.
- Real hero product photo  [outputs/cro-fixes/minimalist/_assets/hero_src.png] - Nia10New.png, 1100x1600 studio shot on flat #E5E9EA grey. Use uncropped on a matching #E5E9EA plinth so it blends.

## Do not

- a first screen that is only the product photo
- price and Add to Cart 1,600-1,900px below the fold
- a chat bubble covering the thumbnails or the price
- inventing any rating, count, clinical result or claim
- rounding the 3.9 rating up
- recreating the Minimalist wordmark in a web font
- gradient text
- implying Minimalist is a Koolestpro client

## Output

A finished, responsive mobile product page I can publish and screenshot at
390x844. Real copy only. Tell me if any fact above is missing or contradictory
instead of guessing.

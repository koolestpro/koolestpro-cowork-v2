# Caraway - Fry Pan PDP rebuild brief

Paste everything below into Lovable or Figma Make as the project prompt.
Then publish, and pull it back with `.ai-workflow/tools/capture_page.py`.

---

Build me a mobile product page for **Caraway**, page: Fry Pan PDP.
Source of truth for the real page: https://www.carawayhome.com/products/fry-pan

Audience: home cooks who want non-toxic, easy-to-clean cookware and are deciding whether $125 is worth it
The one job of this page: **make the first screen carry the whole buy decision, so price, proof, the reason to buy and the CTA are all visible without scrolling**.

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
- Plan: Mobile PDP for the cream 10.5 inch ceramic fry pan. First screen: outcome headline, product name, price, rating and review count, hero image, benefit chips, trust row, sticky add to cart. Below the fold: the non-toxic materials story, induction and oven-safe detail, a comparison, a real review, an FAQ.
- Site photo: The site has a good clean cutout (Ceramic Fry Pan - Cream - Hero), but the shot is flat and plain, which is why the current rebuild reads weak.
- Decision: Generate an AI version. A styled pan on a warm kitchen surface with visible food and steam, so the first screen sells the outcome (a real meal), not an object on a dark plinth. Keep the pan shape and the cream colourway faithful to the real product.
- Note: This is the Caraway blocker. Do not ship the rebuild on the flat cutout.


## Real facts to use (traceable to the live page)

- $125, Shop Pay 4 interest-free payments of $32
- 10.5 inch non-stick ceramic fry pan, cream colourway (TOP GIFT badge on the live page)
- 4.7 stars from 18,886 reviews (review count confirmed on the live page, 2026-09-06)
- No PTFE, no PFOA, no PFAS (Caraway's own claim on the live PDP)
- Oven safe to 550F, works on induction, wipes clean
- Free shipping on orders $90+, free returns, 30-day trial
- Real verified-buyer line: "Cooks evenly and quickly." - Curtis M.
- Real logo: Caraway's own SVG wordmark from the live header
- Real product photo: Caraway's Ceramic Fry Pan - Cream - Hero asset

Verify before publishing:

- [ ] Star rating value: 4.7 is from the static-ad caption; confirm the exact figure on the live PDP before publishing.
- [ ] Review count: the audit recorded 18,886; an ad caption used 18,878. Confirm the current number live.
- [ ] Any claim about how long food takes or how it performs beyond 'cooks evenly and quickly'.

## Outcome headline options (pick one, or improve on it)

  1. Non-toxic non-stick. Even heat, nothing sticking.
  2. No PFAS. No sticking. Nothing to worry about.
  3. The pan that makes 'non-stick' true again.

## Benefit reasons (real, on the product)

- Ceramic non-stick with no PTFE, PFOA or PFAS
- Cooks evenly on induction and every other hob
- Oven safe to 550F, from hob to oven
- Wipes clean in one pass
- Light enough to handle with one hand, 10.5 inch, serves the whole pan

## Trust row (next to the add to cart)

- Free shipping on orders $90+
- Free returns
- 30-day trial
- 18,886 reviews and a real verified-buyer quote

## Sections, top to bottom

- 1. Slim non-blocking promo strip: free shipping $90+, free returns, 30-day trial. No email popup, no full-screen overlay.
- 2. Header with the real Caraway wordmark, search and cart.
- 3. Breadcrumb, subtle: Shop All / Cookware / Fry Pan.
- 4. First screen, the important one: outcome headline, then the product name, then the price at display weight directly under it, then the star rating and 18,886 review count inline, then the Shop Pay line, then the hero product image filling the remaining space with no dead area, then benefit chips, then a trust row, then a sticky Add to Cart bar that fills to the bottom edge.
- 5. Below the fold: the non-toxic materials story (no PTFE, PFOA, PFAS), the induction and oven-safe detail, a comparison against a typical non-stick pan, the real review quote, an FAQ on care and the trial.

## Assets to upload

- Real Caraway wordmark (SVG, pulled from the live header)  [outputs/cro-fixes/caraway/_assets/logo.svg]
- Real product photo, cream pan, background removed  [outputs/cro-fixes/caraway/_assets/hero_cutout.png] - place on a contrasting surface, never crop it
- Colour swatches - cream, navy, grey, gold (from the live page)

## Do not

- The full-screen email-capture popup on load.
- Five solid stars if the real rating is 4.7. Show the real rating.
- Any invented result, number, guarantee or customer quote.
- Gradient text, or a second discount stacked on the first.
- Cropping the product photo. It must show the whole pan, undistorted.

## Output

A finished, responsive mobile product page I can publish and screenshot at
390x844. Real copy only. Tell me if any fact above is missing or contradictory
instead of guessing.

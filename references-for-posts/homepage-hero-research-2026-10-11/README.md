# Homepage hero research (2026-10-11)

Done before rebuilding the Bala homepage first screen, after Ridwan's feedback that the first
pass read like a PDP, narrowed the brand to one product, and stacked too much left-aligned text.

## Sources

- Ridwan's 8 references (homepage before/afters found online): Tofu Go (Allspire), SWT skincare,
  Serenova, S'noods, Carnivore Snax, Ion Layer, bido (Conversion Alchemy), Majco Greens.
- Live mobile captures, 390x844, taken 2026-10-11: `live/` (grüns, Oura, Ridge, Jones Road,
  Liquid I.V., Alo, Vuori, SWT live site).
- Baymard, homepage carousels: 46% of homepage carousels have usability issues, most users
  never see slide 2+, autorotation should be avoided on mobile; static hero sections perform
  about as well and are simpler. https://baymard.com/research-articles/homepage-carousel
- Instant, ecommerce homepage best practices 2026: answer what you sell / who for / why you in
  the hero; one message, one visual, one primary CTA; product-forward imagery; on mobile cut
  hero height and decorative copy, no stacked promo bars, no auto-rotation.
  https://instant.so/blog/7-ecommerce-homepage-design-best-practices-for-2026
- Blend Commerce A/B test (apparel, desktop): simpler hero with value-prop bullets, a
  "4,000+ happy customers" proof line and clear CTAs lifted CR +26%, revenue/user +27% (mobile
  did not win, so test before claiming). https://blendcommerce.com/en-au/blogs/ab-tests-shopify/above-the-fold-homepage-optimisations

## The pattern almost every reference "after" shares

1. **Image first, ~45-50% of the screen, product-forward.** The product (or the range) is
   identifiable at a glance: Tofu Go pack, SWT range on a bench, Serenova packs, S'noods bag +
   bowl, bido bottles in hands. Not a mood shot where the product is a detail.
2. **Badges ON the image do the explaining.** Tofu Go stat bubbles (12g protein, 0g sugar),
   Serenova per-product labels, S'noods "Netflix winner" starburst. They carry facts so the
   copy below can stay short.
3. **Centered text stack, short.** Stars + proof line (small) → H1, 2 lines, bold display,
   says the category in plain words ("High-protein tofu snacks on the go", "Noodle chips made
   to crunch", "Skincare that keeps up") → one-line sub → optional 2-3 benefit chips.
4. **One full-width primary CTA**, thumb height (50-56px), category-led label ("Try Tofu Go",
   "Shop SWT Skincare", "Shop Greens").
5. **A trust/press strip under the CTA**: press logo marquee (Tofu Go, S'noods, Serenova) or
   2-3 icon trust points (SWT, bido, Majco).
6. No carousels, no stacked promo bars, one announcement bar max.

Three families seen:

| Family | References | When it fits |
|---|---|---|
| A. Image top, centered stack below | Tofu Go, SWT, Serenova, S'noods, bido | Most DTC brands; best when the product/range photographs well |
| B. Text first, product band below | Carnivore Snax, Ion Layer | Strong verbal claim or endorsement leads |
| C. Full-bleed photo, text on a scrim | Majco Greens | One great lifestyle photo, single hero product |

## What this means for Bala (the brand)

- Bala sells a **range**: wearable weights (Bangles, Beam, kettlebells), Pilates props (Wavy
  Roller, Ab Roller, Pilates Method, mats), activewear, and kits/bundles. The hero must not
  narrow to one product.
- Bala's identity is **design-led and pastel** ("Fitness, but make it cute"), five shared
  colorways (Blush, Charcoal, Sage, Sea, Sand). Their own kit flatlays show weights and
  apparel together in one colorway: the range in one picture.
- Real proof available: 4.9 stars from 1,865 reviews (Bala Bangles, so say so), press: The
  Wall Street Journal, goop, Glamour (their own "As seen on" logos).

Variants built from these families on real Bala assets: `bala-variants/` (board:
`bala-variants/board.png`). Chosen direction and why: see `bala-variants/CHOICE.md`.

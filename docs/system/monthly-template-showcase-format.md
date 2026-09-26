# Monthly Build Recap format (2026-09-12)

Once a month, one post that recaps the **last four builds across brands** (CRO rebuilds and
replo-rebuilds), shown as four phones **overlapping in a fanned, angled stack**, with a
headline and a humanized promo caption. Reference for the arrangement: Ridwan's
"HIGH CONVERTING PAGES" image.

(An earlier draft of this format used four screens of a single store template. That is
superseded: the monthly post is a **recap of recent work**, not one template deep-dive. The
weekly Template Showcase stream still covers a single built page.)

## Deliverables

| Asset | What | How |
|---|---|---|
| Fanned 4-phone strip | `recap-4builds.png` (transparent, autocropped to the phone cluster, ~1919×1686) | `build_device_still.py preview --style fanned_stack_4 --bg-mode transparent`, then autocrop to the alpha bbox |
| Recap graphic | `koolestpro_monthly-build-recap.png` (1080×1080, exported at 2160) | `.ai-workflow/build_monthly_recap.py` |
| Caption | LinkedIn / X / Instagram | humanized, see below |

## Build steps

1. **Pick the last four builds.** Most recent CRO rebuilds and replo-rebuilds first. Use each
   build's real "after" page captured at 390×844, deviceScaleFactor 2, `reduced_motion="reduce"`.
   **The 2026-09 set is TAPro, Gainful, Obvi, Material Kitchen.** Caraway is dropped until its
   product image is fixed (see `rebuild-tooling-and-quality.md`). Exclude any build whose hero
   product image does not survive being viewed at phone size.
2. **Build the strip TRANSPARENT:** `fanned_stack_4` at 2880×1800 with `--bg-mode transparent`.
   Phones overlap and tilt outward; every phone carries the notch status bar. Then **autocrop to
   the alpha bbox** so the cluster fills the frame. The strip must carry no background of its own.
3. **Compose the graphic** (1080×1080) on **one continuous background**: a single dark sheet plus
   one central purple/orange glow. The headline and the phones share that one background, so there
   are no horizontal bands. Header uses the reference's condensed heavy italic treatment
   (Anton, skewX(-8deg), single line). The transparent strip sits over it, `width:1024px`, top ~170.
4. **Write the caption**, humanized.

## Rules (inherited, do not regress)

- **One background for everything.** Never paste a strip that carries its own gradient; it leaves
  visible bands. Export the strip transparent and back the whole sheet with a single glow.
- **Headline is the topmost element on carousels/annotations.** For this recap only, the 2026-09-13
  revision matches Ridwan's "HIGH CONVERTING PAGES" reference exactly: a tiny
  `@koolestpro | Shopify CRO & UX` line at the top, then the headline. `@koolestpro` still appears
  **once**. Flagged to Ridwan because it is a deliberate exception to standing rule 9.
- **No fabricated results.** A recap lists what was built, not what it earned. Never imply a
  client result, and label any concept brand as fictitious (all four in the 2026-09 example
  are real brands, so no label is needed).
- **CTA points at a real destination** if the caption has one (`koolestpro.com/services/...`).
- **No em dashes.** X caption length per `docs/system/x-caption-playbook.md`.
- **Ship the pipeline button.** The recap HTML includes "Send to Content Pipeline" (type
  `Case Study`), status `Created`.

## Humanized caption (2026-09 example: TAPro, Gainful, Obvi, Material Kitchen)

**LinkedIn**

> Four rebuilds went out this month.
>
> TAPro's cards: the product back on screen one. Gainful's customizer: an add to cart that was missing. Obvi's homepage: the proof and the offer stacked cleanly above the fold. Material Kitchen: the price, the proof and the trust that were all sitting below the scroll.
>
> Same job every time. Find where the page loses the shopper, and fix that part.
>
> Rebuild options: koolestpro.com/services/store-build
>
> #Shopify #CRO #ecommerce

**X**

> Four rebuilds this month. TAPro: product back on screen one. Gainful: the missing add to cart. Obvi: proof and offer above the fold. Material Kitchen: price and trust above the scroll. Details: koolestpro.com/services/store-build

**Instagram**

> Four rebuilds went out this month.
>
> TAPro's review cards. Gainful's protein customizer. Obvi's homepage. Material Kitchen's homepage. Different brands, same job: find where the page loses the shopper, and fix that part.
>
> Link in bio to see the work.
>
> #shopify #cro #ecommerce #webdesign #uxdesign

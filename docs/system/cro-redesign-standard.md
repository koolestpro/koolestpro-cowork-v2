# CRO Redesign Standard — the quality of the "after" page (2026-09-12)

This is about the craft of the rebuilt page itself, not the before/after graphic. Ridwan's
bar is the Majco Greens "after" (`outputs/majco-green.png`), which is far ahead of most of
our rebuilds. This standard defines what a rebuild must reach before it is called done.

## The one idea

**The first screen carries the whole decision.** In the Majco before, the value prop sat in
a block *below* the hero, so the image and the reason to buy were two separate things. The
after moves everything a shopper needs onto the hero image itself: the product title, a value line, social
proof, a benefit line, benefit chips, a single CTA, and a trust bar. A shopper who never
scrolls can decide.

A rebuild that still splits "pretty image" from "the reason to buy" has not reached the bar,
even if every audit finding was addressed.

## The ten dimensions

1. **First-screen decision.** Hero = a real product/lifestyle photo, full bleed, with a
   legibility scrim (gradient overlay or solid band). Over it: product title (H1), value line, proof,
   benefit line, CTA, trust. Nothing that the decision needs is left below the fold.
2. **Product title first, then the value line.** **Product title rule (2026-10-10, Ridwan).** On every product page rebuild, the real product title from the live page (size or variant included) is the page's only `<h1>`. It sits at the top of the first screen, under the header and breadcrumb, above the price, bold, at least 22px. The outcome line never replaces it, is never the `<h1>`, and is never larger than the title: it becomes an eyebrow or a one to two line subhead. Shoppers need to see what the product is, and the real title carries the page's SEO. Homepages and landing pages are exempt: the outcome headline is their H1. The value line states the
   outcome in the shopper's words ("Nourish Your Day, Naturally."), max 2 lines, directly
   under the title.
3. **Proof, immediately.** Star rating + real review count, inline, rendered on load. Never
   dependent on a third-party widget that can paint as bare text. If the number is real, use
   it; if not, do not invent one.
4. **Price, connected.** Price sits with the product name at display weight, not floated
   away from it. Show the payment plan when one exists. Show price-per-serving/use when the
   category makes it meaningful.
5. **Benefit support.** 2-4 specific benefit chips or a single benefit line (e.g. "Clean
   Ingredients / Plant Based / No Junk"). Specific to this product, never generic
   ("Premium quality").
6. **Trust, near the CTA.** Shipping, returns, secure checkout, guarantee, in a compact row
   with real icons, right by the buy action.
7. **One primary CTA.** A single, high-contrast, thumb-reachable button. One secondary
   action at most. Never two buttons competing.
8. **Design system.** A committed type scale (display over UI; body never below the type
   floor; uppercase labels only with letter-spacing), an 8px spacing rhythm, two brand
   colours plus neutrals, consistent radii. The brand's real fonts and real logo assets.
9. **Motion restraint.** Motion is optional and never blocks content. Honor
   `prefers-reduced-motion`. No preloader, no page curtain, no popup gating the page.
10. **Honesty.** Every claim, number and asset is traceable to the real page or the audit.
    Concept brands are labelled. Nothing is invented to make the design land.

## Rubric (score each 1-5; below 3 on any dimension is not shippable)

| # | Dimension | 1 (weak) | 3 (ok) | 5 (bar) |
|---|---|---|---|---|
| 1 | First-screen decision | image only | image + some info | whole decision on the hero |
| 2 | Title + value line | title missing, or slogan is the H1 | title present but small, or not the H1 | real title as the only H1 at the top, outcome line as subhead |
| 3 | Proof | widget-dependent | stars or count | stars + real count, inline |
| 4 | Price | floated/disconnected | near title | with payment plan, at weight |
| 5 | Benefit support | none | one generic line | 2-4 specific chips |
| 6 | Trust | none | in footer | icon row by the CTA |
| 7 | Primary CTA | competing | one, low contrast | one, high contrast, reachable |
| 8 | Design system | ad hoc | consistent type | full scale + rhythm + assets |
| 9 | Motion | blocking | subtle | absent or reduced-motion safe |
| 10 | Honesty | unverified claims | mostly real | fully traceable |

## Build checklist (run before "done")

- [ ] Is the whole decision on the first screen, or did I leave the reason to buy below?
- [ ] Does the hero use a real photo with a real scrim, not a text-only band?
- [ ] Is the real product title the only `<h1>`, at the top of the first screen, above the price, at least 22px, and not outranked by the slogan?
- [ ] Is the outcome line a subhead under the title, not a replacement for it?
- [ ] Stars + real review count render inline on load?
- [ ] Price sits with the name, with the payment plan if one exists?
- [ ] 2-4 specific benefit chips, no generic filler?
- [ ] Trust row by the CTA with real icons?
- [ ] One high-contrast CTA, thumb-reachable?
- [ ] Type floor respected; spacing on an 8px rhythm; real brand fonts and logo?
- [ ] Reduced-motion safe; nothing gates the page?
- [ ] Every claim traceable; concept brands labelled?
- [ ] Verified on the rendered screenshot, not the markup.

## Anti-patterns (junior tells)

- A slogan as the `<h1>` with the product name shrunk to a small subline (Fly By Jing and Minimalist rebuilds, Oct 2026). The shopper cannot tell what the product is at a glance.
- A split layout where the hero is decoration and the value prop is a slab underneath.
- Text-only hero, or a hero so busy the headline needs a dark band to be read.
- Two CTA buttons of equal weight.
- Tiny uppercase eyebrows carrying the whole concept with nothing else supporting them.
- Generic benefit words: "Premium", "High quality", "Best in class".
- A third-party reviews widget as the only proof.
- Recreating a logo in a similar web font instead of pulling the real file.
- Unverified numbers, or a concept brand framed like a paying client.
- Dead space at the bottom of the frame; a preloader or popup gating the page.
- A homepage rebuild that reads like a PDP: a variant/weight picker, per-variant prices and a single-product buy button on screen one (Bala homepage, 2026-10-11, Ridwan: "looks like a PDP"). A homepage first screen names what the brand sells, carries proof and ONE CTA (+ a "Shop all" link), then shows the range: a shop-by row and a priced best-sellers rail. Leave variant pickers to the PDP.

## Current rebuilds vs this standard

- **Caraway fry pan** (`outputs/cro-fixes/caraway_fry-pan-pdp_rebuild.html`): strong on
  proof (3), price (4) and honesty (10); the audit findings are all fixed. Against the bar
  it is missing (1) a value headline over the hero, (5) benefit chips, and (6) a trust row
  by the CTA. Next pass for this page: move the decision onto the hero (outcome headline +
  proof + benefit chips + trust) so a non-scrolling shopper can decide.
- **Fly By Jing chili crisp and Minimalist niacinamide** (Oct 2026) pass dimensions 1 and 3 to 7 but
  fail the 2026-10-10 title rule (slogan is the H1, product name is a small subline). Per Ridwan they
  are NOT redone; the rule applies to every rebuild from 2026-10-10.
- **The standard is the target for every new rebuild**, not a retro-fix project. Existing
  posted work is not redone; runs from here build to this bar.

## Homepage rebuilds (2026-10-11)

Research the hero before building it and follow `docs/system/homepage-hero-patterns.md`: image first and product/range-forward, facts as labels on the image, a short centered stack (proof line, 2-line H1 that says what the brand sells, one-line sub), one full-width CTA, then category pills and press/trust. Never narrow a multi-category brand to one product; no long left-aligned text block on the mobile hero. Build 3-4 directions on real assets, board them, record the choice.

## Full page rule (2026-10-26, Ridwan)

Every redesign of a real store (Sunday CRO Fix, Wednesday Page B) is a complete page, because the same page ships again as a Template Showcase. The first screen still carries the whole decision and is judged by the rubric above. Below it, build what a real page of that type needs, using only the store's real products, prices, photos and claims:

- **Homepage:** hero (what the brand sells, proof, one CTA plus "Shop all"), shop-by category row, priced best-sellers rail, why-us or how-it-works, proof that the store actually shows (real reviews, real press), a featured product or bundle, FAQ, newsletter, footer.
- **Product page:** first screen per the product title rule, then benefits, how to use, ingredients or specs, comparison, real reviews, FAQ, cross-sell, sticky mobile add to cart, footer.
- **Collection page:** short header that says what the range is for, filter and sort bar, product grid with price and one key benefit, a mid-grid proof or guide block, FAQ or buying guide, footer.
- **Advertorial / listicle:** a new page for the store, built on its real products: editorial hook, problem, the product as the answer, proof, offer block, FAQ, CTA. Only real facts. No invented customer stories or numbers.

Never invent reviews, ratings, review counts, press logos, guarantees or stats the store does not show. If the store has no reviews, design the proof section around what is real (materials, origin, a real guarantee) rather than filling it with fake ones.

## No template ceiling (2026-10-26, Ridwan)

Our templates and past pages are the starting point and the level to beat, never the answer. Ridwan: "not award level websites, but websites that work, not cheap template designs."

For every real-store redesign and every concept page:
1. **Business first.** What it sells, the price point, how buyers arrive (ads, search, social), what they doubt, and what the brand already looks and sounds like. The structure follows from this, not from the last page we built.
2. **Look before building.** Study 3 or more live, well-converting pages for this kind of business and page type: homepage and hero inspiration roundups, the store's competitors, strong DTC stores in the niche. Note what each does that our library has never done (a hero idea, a way of showing the range, a proof format, an interactive element). See `homepage-hero-patterns.md` for homepages.
3. **Choose, then build.** Pick the structure and hero idea that suit this brand. Write the choice and the references in the build notes (`BUILD-NOTES.md` or the build brief).
4. **Check against the bar.** Put it next to the latest CRO Fix (currently `outputs/cro-fixes/fishwife_shop-all-collection_rebuild.html`) and the template it started from. If it reads like a cheap theme, or like our last page in new colours, it is not done.

Every real-store page is built so it can be posted both as a CRO Fix (its first screen) and as a Template Showcase (the whole page).

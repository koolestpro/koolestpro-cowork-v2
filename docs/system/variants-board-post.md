# Variants board post (X debate, goes first) 2026-10-11

Ridwan's rule, from the Bala homepage run: every CRO Fix explores several hero
directions before we pick one. Those directions also become a post.

## The rule

1. **Every CRO Fix run builds 3-4 hero variants** on the brand's real assets (homepage or
   PDP alike), one per family in `docs/system/homepage-hero-patterns.md`, and saves them
   with a board and a `CHOICE.md` (our pick and why). Always multiple variations.
2. **The variants board posts on X FIRST**, before any carousel row of that audit
   (LinkedIn, Instagram or X). Default slot: Tue 18:00 ET, the day before the Wed
   carousel. `space_queue.py` rule 3c keeps it on the day before its hero, or opens the
   hero's day with it and pushes the hero to the next day. It never goes after.
3. **It is neutral.** Letters A/B/C/D, a short neutral label each, no "chosen", no
   ranking, no hint. The post exists to start an argument, not to announce our pick. Our
   own decision is made separately (CHOICE.md) and is revealed by the carousel.
4. **The caption is built for debate** (x_variants, under 280, X rules apply):
   - opening line states the page type and brand ("Bala's homepage hero, 4 ways.")
   - "same brand, same products" so the only variable is the design
   - one line per letter, what it leads with
   - one honest hot take (an opinion, never an invented stat or result)
   - the ask ("Which would you ship, and why?") + the reveal hook ("My pick goes up next.")
   - never "carousel", "swipe" or "slides" (it is a single image)
5. **Honesty still applies.** Real assets only, concept label on the board, never a fake
   poll result or "90% picked wrong" style claim.

## Files and wiring

- Builder: `.ai-workflow/tools/build_variants_board.py` (1600x900, brand background + glow,
  phones from `compose_mobile_flat()`), exported with `.ai-workflow/tools/export_sheet.py`
  through the page's own `captureSheet()`.
- Output: `outputs/cro-fixes/{brand}/koolestpro_{slug}_variants-board.png`.
- Review pack tab: `tab-x-variants` -> caption key `x_variants` (harvest_content.py).
- Social library key: `CRO-{BRAND}-X-VARIANTS`.
- Calendar: `populate_sheet.py` CRO Fix slot `x_variants` (Twitter, Tue 18:00 ET, asset
  matcher `variants-board`, per-image key, no fallback caption).
- Spacing: `space_queue.py` rule 3c (teaser never floats as an X extra; it rides with its
  hero; teaser + hero within one day are a bundle, not a cooldown breach).

## Follow-up worth doing by hand

Reply to the best answers under the board post, then quote-post it when the carousel
goes live ("Most of you picked X. I shipped A. Here's why.") only if the replies really
say that. Never invent the split.

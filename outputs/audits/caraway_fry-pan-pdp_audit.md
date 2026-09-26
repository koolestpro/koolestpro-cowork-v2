# CRO Audit — Caraway, Fry Pan PDP

**URL audited:** https://www.carawayhome.com/products/fry-pan
**Device:** mobile, 390x844 (also checked at 375x812)
**Date:** 2026-09-06

## Findings (real, observed live)

1. **Full-screen email popup blocks the entire PDP on load.** A live browsing session
   hit a full-screen "Save Up to $705" email-capture overlay with no visible content
   behind it except a small X to dismiss. This is the first thing a mobile visitor sees
   on a product page they navigated to directly.

2. **Price is disconnected from the title.** The H1 ("Fry Pan, 10.5" Non-Stick Ceramic
   Frying Pan") sits top-left; "$125" is a separate top-right-aligned element on the
   same line as the review count, not directly below the title. A shopper's eye has to
   jump sideways to connect the product name to what it costs.

3. **Star rating / review count can render as bare text.** On a fresh load, the reviews
   line painted as the literal word "Reviews" with no stars and no count (18,886 reviews
   exist on the real page, confirmed on a later load) — the social proof widget hadn't
   finished loading yet, right next to the price where it matters most for a purchase
   decision.

4. **Category/promo nav row competes for top-of-fold space.** "Shop All / $100K Sweeps /
   Labor Day Sale" sits directly under the header before any product content, and on a
   live session a "$100K Sweepstakes: 250 Entries" banner adds further vertical space
   between the price and the product photo — on that load the photo landed below the
   fold (~850px+) on an 844px-tall viewport.

## Rebuild fixes implemented

- Popup converted to a slim, always-visible, non-blocking top strip.
- Price moved directly below the H1, at display weight (26px).
- Star rating + review count render inline immediately, no widget dependency.
- Nav condensed into chips that wrap instead of pushing content down; sweepstakes
  banner removed from the above-the-fold path.
- Real product photo (Caraway's own "Ceramic Fry Pan - Cream - Hero" asset), background
  removed and composited on a contrasting dark surface, fills the remaining above-the-fold
  space with no dead space above the sticky Add to Cart bar.
- Real logo: Caraway's own SVG wordmark pulled directly from the live page's header
  `<a href="/">` element and embedded as-is (not recreated in a web font).

## Assets used (real, not fabricated)

- Logo: extracted live SVG path from carawayhome.com header, `aria-label="Caraway Home"`.
- Product photo: `Ceramic_Fry_Pan_-_Cream_-_Hero.jpg` from Caraway's own Contentful CDN
  (the same cream colorway shown live on the page at the time of audit).
- Price ($125), review count (18,886), payment plan (4 payments of $32 with Shop Pay)
  all taken directly from the live page — no invented figures.

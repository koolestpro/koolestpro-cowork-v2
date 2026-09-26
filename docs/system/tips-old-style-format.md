# Tips carousel: the old-style format (approved 2026-09-18)

Ridwan's call: Tips go back to his own 2025 post style. Reference sets (look at them, don't guess):

- `references-for-posts/5 homepage fix that lifts sales/` (8 slides)
- `references-for-posts/5 products page fix that build trust/` (8 slides)
- `references-for-posts/5 shopify  fix that brings more sales/` (8 slides)
- Cover inspiration only: `references-for-posts/90 content ideas in 9 slides/` cover (NOT its list slides or its content; that set is someone else's post and is saved for the future audience-growth version, see `docs/audience-growth-v3-prep.md`).

This format replaces the V2 "headline-only" Tips as the bar. The V2 file stays the reference for export/JS mechanics (capture function, chrome hiding, asset waiting).

## Anatomy (8 slides, 1080×1080 square)

| Slide | What's on it |
|---|---|
| 1 Cover | Big title ("5 Homepage Fixes That Lift Sales" pattern: number + page type + outcome), one emoji max, a one-line subtitle that reframes the page ("Because your homepage is ... it's your first handshake."). Must pass the cover rule below. |
| 2-6 Fix #1..#5 | Gradient pill badge `FIX #n` (orange #FF9500 → purple #850FFA), heavy headline (2-4 words, imperative: "Clarify Your Message", "Show Real Usage"), 1-2 line body in muted grey, then ONE proof element: a real store screenshot crop that shows the fix done well, or, when no screenshot fits, a gradient card with a single large line icon (Iconify, specific to the fix). |
| 7 Recap (optional) | The 5 fix names as a tight list, or skip and go to 8. |
| 8 CTA | Thin orange→purple gradient border frame, 2-3 line closing statement ("Your homepage should guide, not overwhelm."), short gradient rule, CTA line + the real destination (service page URL on koolestpro.com, per project-wide rule 1; the "DM me 'Audit'" keyword line may sit alongside it). |

**Every slide** carries the footer `@koolestpro | Shopify CRO & UX`, bottom-centre (cover/CTA) or bottom-left (fix slides), small, muted.

## Visual system

- Background: near-black `#0F0F0F` with a soft radial glow, orange on the left and purple on the right, behind the headline. Background gradients only; solid-colour text (no gradient text).
- Type: heavy geometric sans (Poppins 700/800 look) for headlines, white; Inter/DM Sans 400 for body, grey `#B8B8B8`.
- Headline scale: cover ~96-110px, fix headlines ~84-96px at 1080 wide. Body ~34-38px.
- Generous margins (~80px). Left-aligned on fix slides, centred on cover/CTA.
- Proof screenshots: real, cropped to the relevant block, rounded corners, never recreated; brand name visible is fine (it's an example of good practice, credit the brand in the caption, never imply they are a client).

## Cover rule (standing rule 1, Tips version)

The cover is never boring. Two allowed routes, pick per topic:

1. **Visual cover:** a real visual element dominates (a phone mockup of a page, a product cutout, a large contextual illustration).
2. **Type-led cover (the "90 content ideas" route):** the huge bold title IS the visual, set over a rich gradient field (not flat black), with thin white line-art blended in: a frame with corner marks, small diagram glyphs (lightbulb, wireframe lines, list icons, arrows) placed in the empty corners, a small year/series tag at the bottom. Diagrams are drawn as inline SVG line art, specific to the topic.

A plain headline on a flat dark background (the 2025 cover as-is) fails the rule. Keep the 2025 slide layouts for slides 2-8; upgrade the cover.

## Copy rules

Same as every stream: humanizer 11-pass, no em dashes, real line breaks, X captions ≤280 chars counted, no hashtags on X. Fix headlines are imperatives a store owner can act on today. No invented stats.

## Export

1080×1080 per slide, html2canvas `scale:2` via the page's own `captureSlide()` (project-constitution pattern), chrome hidden with `visibility:hidden`, `waitForSlideAssets` + double rAF. Look at every exported PNG before registering.

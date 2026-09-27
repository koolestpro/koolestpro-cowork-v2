# Template Showcase: Instagram is ALWAYS a carousel (2026-09-27)

Ridwan's call: every Template Showcase post on Instagram (Replo brand pages from `koolestpro-template-showcase-weekly` AND store templates) ships as a carousel, modelled on his pre-automation rebuild posts in `references-for-posts/shopify rebuilds/rebuild-1` (UrbanEdge dog grooming vacuum) and `rebuild-2` (Captain & Skipper). Reels still post separately from the videos; this carousel is the Instagram image post.

Make now posts native Instagram carousels (scenario 6565331, route 310-317, 2-10 images) from a row whose `asset_urls` holds `; `-joined URLs, so this is fully automatable once Instagram is un-paused.

## Format: 6 slides, 1080×1350 (4:5), in this order

| # | Reference slide | What to build | Built from (existing run assets) |
|---|---|---|---|
| 1 | Cover: "Shopify Store Redesign that Converts 🔥" + desktop hero in a rounded card, "Swipe to see the new look →" | Headline (2-3 lines, ≥96px heavy sans), the desktop hero screenshot in a rounded white card with shadow, dark bg with orange→purple diagonal glow + thin line-art diamond/square accents, swipe line. **Concept builds say "Concept store build", never "redesign" of a real client** (project rule 2) | top crop of `{slug}-full-page.png` (or a fresh 1440-wide hero capture) |
| 2 | Long-scroll page, split across the frame on a light canvas | The full desktop page in 2-3 columns on a soft neutral canvas with white margin | `{slug}-full-page.png`, re-cropped to 4:5 |
| 3 | Device mockup on a brand-colour background (laptop, or 3 angled phones) | Laptop or `flat_packed_3` phones centred on a flat background in the page's own brand colour, small `@koolestpro - Shopify CRO & UX Design` footer | `{slug}-preview.png` / `build_device_still.py` with a 1080×1350 canvas and `--bg` = brand colour |
| 4 | Section highlights ("HEADER & HERO SECTION" / "FOOTER SECTION") | Two stacked section crops with big bold section labels in the brand colour. Pick the two strongest sections (hero + the best proof/offer section) | crops from the full-page capture |
| 5 | Angled tiled collage | The page repeated as rotated (~-30°) tiles filling the frame edge to edge | full-page capture, tiled + rotated |
| 6 | Project Snapshot + CTA | "Project Snapshot" + gradient rule; FONTS USED (heading/body, read from the page CSS), COLOR PALETTE (4 swatches sampled from the page), TOOLS USED chips (what was actually used: e.g. Figma, Shopify, Replo); divider; "Want your store built next?" / "Want your store optimized next?", one line of positioning, gradient button, handle footer. CTA points at the real service page (project rule 1) | page CSS + palette sampling |

## Rules

- 1080×1350 every slide; text sizes follow the Tips V4 floors (headline ≥88px, body ≥40px, footer ≥26px).
- Real page captures only; never recreated. Concept brands (KURA, HALOS, MERIDIAN, Lumora) labelled as concept builds on slide 1 and in the caption.
- No em dashes, humanizer pass on every line, no gradient text.
- Export to `outputs/templates/{slug}_{date}/ig-carousel/slide{1..6}.png`; register key `TS-{BRAND}-IG-CAROUSEL` in `{brand}-social-content.md/.json`; the Instagram queue row's `asset_paths` lists all 6 in order (feed_media.py hosts each and joins them; Make builds the carousel).
- Look at all 6 PNGs at phone size before calling the run done (same "verify by exporting" rule as everything else).

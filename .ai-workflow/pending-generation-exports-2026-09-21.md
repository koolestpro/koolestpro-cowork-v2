# Pending exports — found during 2026-09-21 distribution assembly

Two items exist as real HTML with good captions but are missing the actual exported
PNGs a generation task is now responsible for producing before marking `"Created"`
(see the 2026-09-21 division-of-labor rule in `CLAUDE.md` and `DISTRIBUTION.md`).
Distribution assembly cannot render these itself — flagging here for the next
generation-task run (or Ridwan) to finish.

## 1. Caraway Fry Pan PDP — v2 rebuild supersedes the registered v1

- New file: `outputs/cro-fixes/caraway_fry-pan-pdp-v2_carousel.html` (+ `_annotation.html`), built 2026-09-20.
- Uses the AI-generated lifestyle hero photo (pan with food/steam on a warm counter) per the build brief's own instruction — replaces the flat product-cutout hero the currently-registered v1 (`caraway_fry-pan-pdp_content.html`, 2026-09-07) still uses.
- Never registered in SYNC_DATA and never exported — no `koolestpro_caraway_fry-pan-pdp-v2_carousel_slide{1,2,3}.png` exist on disk, only the client-side `dlSlide()` buttons (never clicked) and one full-page capture (`outputs/cro-fixes/_capture/caraway_v2/caraway_v2-mobile.png`, evidence of the new design only, not a postable slide).
- **To finish:** open `caraway_fry-pan-pdp-v2_carousel.html`, click "Download All PNGs" (or run it through the project's own headless capture step), then register it in SYNC_DATA as a fresh CRO Fix item (or replace the v1 entry) so the next distribution assembly run picks it up.
- **Current state:** the already-scheduled Sep 30 - Oct 4 LinkedIn/Instagram/Twitter rows still point at the OLD v1 slides. Swap the row assets once v2 is exported, or leave v1 live if the timeline is fine as-is.

## 2. Tip — "Why your PDP loses sales at 60% scroll"

- Real file found at `outputs/tips/why-your-pdp-loses-sales-at-60-scroll_2026-04-29.html` (SYNC_DATA's registered `folder` pointed at a filename/date that doesn't exist on disk — `..._brief-audit-_2026-04-24.html` — likely renamed after the pipeline-export button was clicked).
- Captions are complete and good (LinkedIn, hook, X thread, X singles, Instagram all harvest cleanly).
- No exported slide PNGs on disk anywhere — same as `5-liquid-snippets-cart-abandonment_20260514.html`, only client-side `captureSlide()` buttons, never clicked.
- **To finish:** open the file, export the slides for real, save them alongside it (or in a dedicated `{slug}-assets/` folder so the harvester doesn't grab an unrelated file from the shared `outputs/tips/` folder), then correct SYNC_DATA's `folder` field to the real filename.

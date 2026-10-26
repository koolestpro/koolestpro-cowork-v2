# Build brief: Fishwife shop-all collection page, first screen (2026-10-25)

Path: fallback, Claude authors the page HTML directly (unattended run, no page builder driven). Builder: `.ai-workflow/build_fishwife_rebuild.py`.
Facts: `fishwife_shop-all-collection_facts.json`. Audit: `outputs/audits/fishwife_shop-all-collection_audit.md`.

## What is being built
A collection page whose first screen IS the choice: header, a slim brand photo band with the real H1, category pills, sort, then four full product cards (name, pack size, stars + count, price, Add) above the 844px fold.

## Image decision
Their packshots are excellent studio shots on near-white: used as-is, background removed (`prep_fishwife_assets.py`), on a cream plinth inside each card with `object-fit:contain` (no crop). The live banner photo is kept as the band, cropped to a 118px strip under a green scrim. No AI image needed.

## Brand
Real logo (header img fishwife-logo.png), Recoleta (display) + Albert Sans (UI) from their CDN, cream #FFFCF3, sun yellow #FDCD62, black 1.5px outlines and pill buttons like the live theme, sea blue #397CC0 for the "Just dropped" badge.

## Hard constraints
Every number traceable to the facts file. No price claims in copy. Concept label in the footer. Private: not deployed anywhere.

# Topicals - Homepage first screen rebuild brief

Builder input (Lovable / Figma Make). This run used the fallback: Claude authored the page
directly (`.ai-workflow/build_topicals_rebuild.py`). Keep any builder project PRIVATE.

Source of truth: https://mytopicals.com/ + product pages (checked 2026-10-18). Facts: `topicals_homepage-hero_facts.json`.

Audience: US shoppers on a phone, often arriving from TikTok/Instagram, who have a specific flare-up (dark spots, eczema-prone dryness, dark circles, rough body skin) and want to know fast if Topicals is for them.
The one job of screen one: **say what Topicals treats, prove it, give one way in.**

## Non-negotiable rules
- Real facts only (ratings from JSON-LD, prices from the homepage). No invented numbers.
- Homepage: the outcome headline is the H1. Real wordmark (header SVG), real fonts, real packshots.
- No popup or floating pill on top of the CTA. One primary CTA.

## Image decision
- Live hero (face photo + eye masks) is strong for mood but names one kit and is buried under a scratch-card game.
- Explored 4 directions (see `topicals/_variants/CHOICE.md`). **Chosen by Ridwan: C**, their own Faded Dark Spot Kit lifestyle photo full bleed with a dark scrim, the whole decision stack over the image, and a tag naming the kit and price. No AI generation needed.
- Runner-up (A/B challenger): A, the labelled packshot lineup.

## Sections
1. Announcement bar: Bright Eyes + Slick Lips Kit, $45 value, now $30 (the offer that used to be the hero)
2. Header: menu, real wordmark, bag
3. Full-bleed kit photo with a name/price tag, scrim, and over it the centered stack: 4.9 from 882 Faded Serum reviews / H1 "Skincare for flare-ups. Made fun." / one-line sub / ONE CTA "Shop best sellers" / concern pills / trust row (free shipping $50+, science-backed, vegan)
5. Below: priced best-sellers rail with ratings, "Shop by flare-up" grid, brand values, footer

## Do not
- open on a game, modal or scratch card
- float anything over the CTA
- let the wordmark be the biggest thing on screen one
- invent ratings, prices or results; imply Topicals is a client

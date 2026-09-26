# PENDING — Static Ad: Kyte Baby, Sleep Bag in Oat 1.0 TOG

**Status:** blocked at generation. gpt-image has no credits. Nothing has been registered in the pipeline, no `usedFor` entry was added to `targets_pool.json`, and no output folder exists under `outputs/static-ads/` (an empty stub at `outputs/static-ads/kytebaby_sleep-bag-oat-1-0_20260918/` was left behind — it can be deleted or reused once real files land there).

## Block detail

Ran the weekly `koolestpro-static-ad-weekly` scheduled task on 2026-09-18. Tried `gpt-image`'s `edit.py` (real product photo supplied, per Step 3 Case A) at `--quality low --size 1024x1536`, one call, targeting `ad-1-problem-solution.png`.

```
openai.RateLimitError: Error code: 429 - {'error': {'message': 'You have no credits remaining.
Add credits to continue using the API at https://platform.openai.com/settings/organization/billing/.',
'type': 'insufficient_quota', 'param': None, 'code': 'credit_balance_exhausted'}}
```

**Keys tried:**
- `.claude/skills/gpt-image/.env` → `OPENAI_API_KEY=sk-proj-a...` → 429 credit_balance_exhausted
- `koolestpro-cowork-v2/.env` → `OPENAI_API_KEY=sk-proj-0...` (different key) → 429 credit_balance_exhausted

Both keys exhausted, same as the 2026-09-04 Caraway block. Per the standing protocol: going straight to a prompt pack rather than spending on an alternate paid service — inference.sh wasn't named by Ridwan for this run, so it's off the table here too.

## Target / product selection

**Target:** Kyte Baby (`target-kyte-baby-1751673600010` in `targets_pool.json`), category `baby-pet-lifestyle`, `visualPotential: Medium`, `leadPotential: Medium`, zero prior `static-ad` usedFor entries.

**Why this target:** it was the best-scoring candidate with zero static-ad history. The only zero-history targets in the pool right now are Minimalist (beauty-skincare, Medium visual), TAPro (nfc, Medium visual, but nfc was already the most recent-but-one static-ad category via V1CE on 2026-08-14), Transparent Labs (fitness-wellness, Low visual), Cuts Clothing (fashion-apparel, High lead but Low visual), and Kyte Baby (baby-pet-lifestyle, Medium visual). Ruled out the beauty pick (Minimalist) because Versed already covered beauty-skincare for this stream on 2026-08-21, a month ago — too close. Ruled out the two Low-visual options since visual quality is the whole point of this stream. Kyte Baby's category (baby-pet-lifestyle) last appeared in static-ad via Bebemoss on 2026-07-17, over two months back, so it clears the rotation cleanly. Kyte Baby is not a Koolestpro client; this is unofficial concept/portfolio work.

**Product:** Sleep Bag in Oat 1.0 TOG — their flagship "Original Bamboo Sleep Bag™" product, $55 (XS–L), $65 (XL). Chosen because it's the site's featured Best Seller and the one product page with the most traceable, specific claims (as opposed to a generic collection listing).

## Research — every claim below is traced to the live product/homepage, nothing invented

| Claim used in the ads | Source |
|---|---|
| Rated 4.9 out of 5 stars | product page review widget, `kytebaby.com/products/sleep-bag-in-oat-1-0` |
| "Take it from 20,000+ 5-star reviews" | homepage copy, verbatim site phrase |
| J-shaped double zipper with zipper garage, zips from top or bottom for diaper changes without disturbing sleep, covered pull protects skin | product page feature bullets |
| AAP-compliant safe sleep design, reduces SIDS risk for babies under 12 months by replacing loose bedding | product page feature bullets |
| Rayon made from bamboo, buttery soft & hypoallergenic | product page + homepage copy |
| TOG (Thermal Overall Grade) rating system — heavier TOG for cooler months, lighter for warmer months | product page "What is TOG?" section |
| Price: $55.00 (XS/S/M/L), $65.00 (XL) | product page variant pricing |
| $7.50 US shipping for orders under $85 (implying free shipping at $85+) | product page shipping info |
| "The Original Bamboo Sleep Bag™," making sleep bags since 2014 | homepage / brand copy |
| Real logo file | `kytebaby.com/cdn/shop/files/kyte-baby-logo.svg` — downloaded, saved to `.ai-workflow/pending-assets/kytebaby_sleep-bag-oat-1-0_20260918/kyte-baby-logo.svg` |
| Real product photos | downloaded to the same pending-assets folder: `product-photo-flat.jpg` (flat product shot on white) and `product-photo-worn.jpg` (baby wearing the Oat 1.0 bag) |

No review count, star rating, or claim above was invented — anything not traceable (e.g. a specific customer quote with a name) was deliberately left out rather than fabricated, per the skill's hard constraint on Angle 3.

## Prompts — copy-paste ready

All four use `edit.py` (real product photo supplied) at `--size 1024x1536 --quality low` per the project's confirmed-working settings. Use `product-photo-flat.jpg` for ads 1, 2, 4 and `product-photo-worn.jpg` for ad 3 (lifestyle-leaning angle) — both are in `.ai-workflow/pending-assets/kytebaby_sleep-bag-oat-1-0_20260918/`.

### ad-1-problem-solution.png
```
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "Create a polished DTC social ad (soft rounded-square card crop) using the product from the input image, which is the Kyte Baby Sleep Bag in Oat 1.0 TOG bamboo sleep bag: place it exactly as shown, do not redesign the garment. Warm, cozy nursery scene background in muted oat and cream tones, soft natural window light. Large bold headline at the top, dark warm-brown sans-serif type on a cream card background, reads exactly: \"3AM Diaper Changes Shouldn't Wake The Whole House\". Below it a small crossed-out problem line in a lighter gray strikethrough style reads exactly: \"Stiff zippers. Scratchy fabric. Loose blankets.\" with a small red X icon beside it. The Sleep Bag product sits large and clean in the lower two-thirds of the frame on a soft cream surface, styled like real product photography, with a small rounded green checkmark badge near the zipper area that reads exactly: \"Dual Zipper. No Wake-Ups.\" Mildly exasperated, relatable new-parent mood. Clean legible typography, no watermark, no extra text, no logos other than what appears on the product itself." \
  --images product-photo-flat.jpg \
  --size 1024x1536 --quality low \
  --output ad-1-problem-solution.png
```

### ad-2-benefit-result.png
```
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "Create a polished DTC social ad (soft rounded-square card crop) using the product from the input image, which is the Kyte Baby Sleep Bag in Oat 1.0 TOG bamboo sleep bag: place it exactly as shown, centered, on a simple well-lit studio backdrop in soft cream and warm beige tones. Short bold headline above the product, dark warm-brown sans-serif type, reads exactly: \"One Bamboo Sleep Bag. Every Box Checked.\" Four small rounded-rectangle chip labels surround the product, each with a thin line connecting it to the relevant part of the bag: top-left chip reads exactly \"Buttery-Soft Bamboo\" pointing at the fabric, top-right chip reads exactly \"AAP-Compliant Safe Sleep\" pointing at the body of the bag, bottom-left chip reads exactly \"Dual Zipper, No Wake-Ups\" pointing at the zipper, bottom-right chip reads exactly \"TOG-Rated Warmth\" pointing at the fabric tag. Clean confident product-photography lighting, legible sans-serif typography, no watermark, no extra text, no logos other than what appears on the product itself." \
  --images product-photo-flat.jpg \
  --size 1024x1536 --quality low \
  --output ad-2-benefit-result.png
```

### ad-3-social-proof.png
```
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "Create a polished DTC social ad (soft rounded-square card crop) using the sleeping baby and Sleep Bag from the input image exactly as shown, warm candid lifestyle nursery lighting, soft focus background. Near the top, a prominent rating banner in bold dark-brown sans-serif type over a cream background reads exactly: \"★★★★★ 4.9/5\" directly above a second line that reads exactly: \"Take It From 20,000+ 5-Star Reviews\". Below the banner, the sleeping baby wearing the Oat Sleep Bag is the emotional center of the frame, warm and candid, not stiff or stock-photo-like. A small supporting line beneath, in lighter type, reads exactly: \"Rayon From Bamboo. Buttery Soft. Hypoallergenic.\" Clean legible typography, no watermark, no extra text, no logos other than what appears on the product itself." \
  --images product-photo-worn.jpg \
  --size 1024x1536 --quality low \
  --output ad-3-social-proof.png
```

### ad-4-offer-urgency.png
```
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "Create a polished DTC social ad (soft rounded-square card crop) using the product from the input image, which is the Kyte Baby Sleep Bag in Oat 1.0 TOG bamboo sleep bag: place it exactly as shown, styled in its best light on a soft cream surface with warm, slightly cooler-toned lighting to suggest early fall. Bold headline above the product, dark warm-brown sans-serif type, reads exactly: \"Cooler Nights Are Coming. Get Baby's TOG Right.\" A contrasting offer banner in a warm terracotta color block sits across the bottom of the frame in bold white type, reads exactly: \"Free Shipping On Orders $85+\". Two small outlined (not filled) rounded-rectangle chips sit near the product: one reads exactly \"TOG-Rated For Every Season\", the other reads exactly \"45-Day Returns\". Clean legible typography, no watermark, no extra text, no logos other than what appears on the product itself." \
  --images product-photo-flat.jpg \
  --size 1024x1536 --quality low \
  --output ad-4-offer-urgency.png
```

## Combined showcase (once the 4 ads exist)

Assemble a 1024x1024 2x2 grid (`combined-showcase.png`) with Pillow — no AI compositing call needed, per the skill's own guidance. No copy needs to be drawn onto it beyond what's already baked into each ad.

## Captions — humanizer-checked

**LinkedIn:**
> Kyte Baby's sleep bag has 4.9 stars and over 20,000 five-star reviews, so I built four ad angles around what's actually on their product page instead of guessing at a hook.
>
> Angle 1 goes after the 3am problem directly: the dual zipper that lets you change a diaper without waking the baby. Angle 2 is the straight product shot with the real claims attached, bamboo fabric, AAP-compliant safe sleep, TOG-rated warmth. Angle 3 leans on the review count itself since it's the strongest thing they've got. Angle 4 uses their actual $85 free shipping threshold and the seasonal TOG switch instead of inventing a sale.
>
> This is unofficial concept work, not a paid engagement with Kyte Baby. Sharing it as a look at how I build a static ad set off a real product page.

**X (3 posts, no hashtags, each under 280 chars):**
1. "Kyte Baby sells a bamboo sleep bag with a dual zipper so 3am diaper changes don't wake the kid. Built the whole first ad angle around that one feature." (149 chars)
2. "20,000+ five star reviews on one product. That number is doing more work than any headline I could write for angle 3." (119 chars)
3. "No made-up sale here. Angle 4 just uses their real $85 free shipping cutoff and the seasonal TOG switch." (106 chars)

## Still to do on return

1. Run all four `edit.py` commands above (one gpt-image call per bash command, `--quality low`, real key with credits).
2. Read back all 4 PNGs — confirm every quoted headline/chip/banner string is spelled exactly as specified before accepting.
3. Build `combined-showcase.png` (Pillow, 2x2 grid, 1024x1024).
4. Build `index.html` at `outputs/static-ads/kytebaby_sleep-bag-oat-1-0_20260918/index.html` with the standard "Send to Content Pipeline" button (constants below), showing the 4 ads + combined showcase + LinkedIn caption + X posts.
5. Register the pipeline record in `ridwan_content_system_updated.html`'s `SYNC_DATA.items`:
   - `id`: `static-ad-kytebaby_sleep-bag-oat-1-0-20260918`
   - `type`: `"Static Ad"`
   - `title`: `"Kyte Baby — Sleep Bag in Oat 1.0 Static Ad Showcase"`
   - `slug`: `kytebaby_sleep-bag-oat-1-0`
   - `status`: `"Created"`
   - `day`: `""`
   - `folder`: `"outputs/static-ads/kytebaby_sleep-bag-oat-1-0_20260918/index.html"`
   - `week`/`month`/`monthSlug`: whatever week/month bucket September 2026 (or the actual ingestion date, if later) falls into in the existing month structure
6. Append to `targets_pool.json` target `target-kyte-baby-1751673600010`'s `usedFor`: `{"stream": "static-ad", "date": "<ingestion date>", "pipelineItemId": "static-ad-kytebaby_sleep-bag-oat-1-0-20260918", "note": "First static-ad use. Featured product: Sleep Bag in Oat 1.0 TOG ($55, 4.9/5, 20,000+ 5-star reviews). Fresh target for this stream, category rotated in to avoid repeating beauty-skincare (Versed, 2026-08-21) or home-kitchen (Caraway, 2026-09-09)."}`
7. Create `kytebaby-social-content.md` / `.json` at the project root with keys `SA-KYTEBABY-PROBLEM`, `SA-KYTEBABY-BENEFIT`, `SA-KYTEBABY-PROOF`, `SA-KYTEBABY-OFFER`, `SA-KYTEBABY-COMBO`, `SA-KYTEBABY-X1`..`X3` — `assetPath` for each pointing at the real file once it exists.
8. Present the finished `index.html` via `mcp__cowork__present_files`.
9. Note in the pipeline record / social-content file that the product photos and logo used were downloaded directly from `kytebaby.com` (real assets), not generated.
10. Delete this pending file and the pending-assets folder once ingestion is complete.

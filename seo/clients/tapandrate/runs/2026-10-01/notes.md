# Run notes: Tap and Rate, 2026-10-01 (first run, files only)

## What ran
| Step | Status | Notes |
|---|---|---|
| 0 Preflight | done | Snapshot: 184 products, 39 collections, 18 pages, 7 blog URLs. Profile built today. |
| Credentials | missing | No DataForSEO, GSC/GA4 or Shopify token yet. All data is from **Ubersuggest UK** (locId 2826). |
| 1 Quick wins | done | `quick-wins.md`. **Do this week:** remove the lorem-ipsum testimonial text from the homepage. |
| 2 Topic | done | `topic.md`. Winner: "how to get more google reviews" (25/30). |
| 3 Brief | done | `brief.md` (SERP from Ubersuggest; Google policy pages checked live). |
| 4 to 5 Draft + humanizer | done | `draft.md` → `article.md`. 1,622 words, 0 em dashes. One factual fix during QA: "every product has QR" was scoped to stands, cards and table coins, because 102 of 184 products sell QR as an add-on. |
| 6 Image | done | Real store photo: black Google review NFC stand (`image.jpg`, CDN URL in `image.json`). |
| 7 Finalize | done | `body.html` (no H1, 14 internal/external links all verified, FAQPage JSON-LD with 4 Qs) + `publish.json`. QA gate passed (`shopify_publish.py --dry-run`). |
| 8 Shopify draft | **skipped** | No `SHOPIFY_TAPANDRATE_TOKEN`. Once it's set: `python3 seo/tools/shopify_publish.py --client tapandrate --run seo/clients/tapandrate/runs/2026-10-01` |
| 9 Log | done | `content-log.csv` row, status `files-only`. Refresh checks due 2026-10-31 and 2026-12-30. |
| 10 Report | baseline only | First week, so there's nothing to compare yet. Baseline: DA 8, 67 ref domains, ~114 organic visits/mo est., 255 ranking keywords (Ubersuggest). |
| 11 Outreach | **skipped** | `outreach_sender` is empty in client.json, so we can't draft pitches signed as the client. See the prospect ideas below. |

## For Ridwan to do by hand
1. **Homepage:** remove or replace the placeholder testimonial text ("Rodell Cruz… Duis at nu…").
2. **Inbound links to the new post** (after it's published):
   - `/blogs/keep-informed/how-to-use-a-google-card-to-collect-more-google-reviews-in-store`: add "For the full playbook, see [how to get more Google reviews](/blogs/keep-informed/how-to-get-more-google-reviews)."
   - `/pages/google-review-calculator`: under the result, add "Want more? Here's how to get more Google reviews."
3. **Ask the client to confirm:** the voucher value (£100 or £200), the stats on the homepage, and who should sign outreach emails.
4. **Policy heads-up for the client:** Google says merchants must not "require or pressure" reviews on the premises. The products are fine as an invitation. Make sure staff scripts and site copy never read as "make them review before they leave".

## Outreach prospects to work on once a sender is set
- Resource pages listing "how to get more Google reviews" tools for UK small businesses. Pitch the free Google Review Calculator and QR generator.
- Booking platforms the products support (Booksy, Treatwell, Fresha) and their partner or accessory pages.
- UK hospitality, hair-and-beauty and motor-trade blogs. Pitch this new guide as a resource.

## Data sources this run
Ubersuggest (keywords, SERP, domain overview), Google support pages (policy quotes), the live store (snapshot). DataForSEO spend: $0 (not connected).

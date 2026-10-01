# Quick wins: Tap and Rate, week of 2026-10-01

> Confidence: **low to medium**. GSC is not connected yet, so positions come from Ubersuggest UK (2026-09 data). Re-check against GSC once `gsc_pull.py` works.

## 1. DO THIS WEEK: remove placeholder testimonial text from the homepage
- **URL:** `/` (reviews block, "See why they love Tap and Rate!")
- **Evidence:** the homepage HTML contains `Rodell Cruz 3 days ago Duis at nu…` (lorem ipsum) next to "4.9 stars | 115 reviews".
- **Change:** replace it with real reviews (the Judge.me widget is already installed and can pull real ones), or remove the block until real ones are wired in.
- **Why:** Google and every AI crawler reads this text. Placeholder testimonials on a business whose whole product is *reviews* undercut trust and E-E-A-T.
- **Effort:** 15 min in the theme editor.

## 2. Google review NFC card collection: title + meta for striking distance
- **URL:** `/collections/nfc-cards`
- **Evidence:** ranks #32 for "google review nfc card" (260/mo), #26 for "google review cards bulk", #22 for "google review tap card". "google review card" is 1,900/mo (SD 33) and "google review card uk" 140/mo (SD 6).
- **Change:**
  - SEO title (before: check the admin) → **`Google Review Cards UK | NFC + QR, Ready to Use`** (49 chars)
  - Meta description → **`Google review cards with NFC and a QR backup. We set them up for you, so customers tap and review in seconds. One-off cost, no subscription.`** (140 chars)
  - Add 150 to 250 words of intro copy above the product grid that answers "what is a Google review card and how does it work", using the same claims as the FAQ.
- **Effort:** 20 min.

## 3. Product titles pulling the wrong intent
- **URLs:** `/products/snapchat-card`, `/collections/tiktok`, `/products/fresha-card`, `/products/instagram-card-copy`
- **Evidence:** ranking for "snapchat plus", "tt coins", "tiktok coins uk", "fresha gift cards", "tik tok card". These searchers want subscriptions, virtual coins or gift cards, not NFC hardware, so they bounce.
- **Change:** make the use clear in titles and meta, e.g. "Snapchat NFC & QR Card: Grow Followers In Store". Rename the `instagram-card-copy` handle to `tiktok-nfc-qr-card`, with a 301 redirect.
- **Effort:** 30 min. This lowers vanity traffic but raises the quality of what's left.

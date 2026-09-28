## 📚 PER-BRAND SOCIAL CONTENT LIBRARY — `{brand-slug}-social-content.md` / `.json`

The canonical answer to "how do I get the caption for a given generated image when it's time to automate posting." One growing file pair per brand at the project root.

* `{brand-slug}-social-content.md` — human-readable, key table + fenced caption blocks.
* `{brand-slug}-social-content.json` — machine-readable sibling, same keys; the durable source of truth for any autopost step. Update both together, never drift.

**Caption = image rule (2026-09-28):** every caption that posts with a single image names that image in `assetPath` (one path, not a list) and carries its `captionKey`. A caption written for "the post in general" can only go on a multi-image post (carousel, combined showcase). This is what lets `populate_sheet.py` pair the right words with the right picture. The old habit of dealing generic `-X1..3` captions across images by position is what put "Four ad directions" on a single ad.

**Key scheme:** Static Ad `SA-{BRAND}-*` (per-image X keys `-X-PROBLEM/-X-BENEFIT/-X-PROOF/-X-OFFER/-X-COMBO` + `-IG-SINGLE` since 2026-09-28; `-X1..3` retired), CRO Fix `CRO-{BRAND}-*` (`-BA`/`-ANNO`/`-CAROUSEL`/`-X-CAROUSEL`/`-X-COVER`/`-X-BA`/`-X-ANNO`/`-X-ANNO-GRAPHIC`; `-X1..3` retired 2026-09-27), Template Showcase `TS-{BRAND}-*` (`-COVER-VID`/`-LAPTOP-VID`/`-MOBILE-VID`/`-COVER-IMG`/`-PREVIEW`/`-FULLPAGE`/`-MOBILESTRIP`), Tip `TIP-{BRAND}-COVER`/`-CAROUSEL`/`-X1..3`. The `-GRAPHIC-A/B/C` standalone graphics are retired (2026-07-18) — never create them.

When one visual has multiple caption angles, use `captionOptions: [{id, caption, hashtags}]` — pick one at post time. The `.json` file wins if it and the pipeline item's `captions`/`assets` fields disagree.

**Known gap:** a caption is only useful once its image exists on disk. Some graphics are generated only client-side via html2canvas download buttons nobody may have clicked. Check `knownGaps` before assuming an `assetPath` is real. To resolve, drive the page's own capture function via headless Playwright (call `captureSlide(idx)`, `page.expect_download()`, `save_as()` to the correct path) — never a generic browser screenshot, never route image data through the conversation. Then actually LOOK at the export; `v1ce-social-content.json` documents a trust-badge claim that looked fabricated but was real.

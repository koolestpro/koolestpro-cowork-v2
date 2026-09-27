## 📚 PER-BRAND SOCIAL CONTENT LIBRARY — `{brand-slug}-social-content.md` / `.json`

The canonical answer to "how do I get the caption for a given generated image when it's time to automate posting." One growing file pair per brand at the project root.

* `{brand-slug}-social-content.md` — human-readable, key table + fenced caption blocks.
* `{brand-slug}-social-content.json` — machine-readable sibling, same keys; the durable source of truth for any autopost step. Update both together, never drift.

**Key scheme:** Static Ad `SA-{BRAND}-*`, CRO Fix `CRO-{BRAND}-*` (`-BA`/`-ANNO`/`-CAROUSEL`/`-X1..3`), Template Showcase `TS-{BRAND}-*` (`-COVER-VID`/`-LAPTOP-VID`/`-MOBILE-VID`/`-COVER-IMG`/`-PREVIEW`/`-FULLPAGE`/`-MOBILESTRIP`), Tip `TIP-{BRAND}-COVER`/`-CAROUSEL`/`-X1..3`. The `-GRAPHIC-A/B/C` standalone graphics are retired (2026-07-18) — never create them.

When one visual has multiple caption angles, use `captionOptions: [{id, caption, hashtags}]` — pick one at post time. The `.json` file wins if it and the pipeline item's `captions`/`assets` fields disagree.

**Known gap:** a caption is only useful once its image exists on disk. Some graphics are generated only client-side via html2canvas download buttons nobody may have clicked. Check `knownGaps` before assuming an `assetPath` is real. To resolve, drive the page's own capture function via headless Playwright (call `captureSlide(idx)`, `page.expect_download()`, `save_as()` to the correct path) — never a generic browser screenshot, never route image data through the conversation. Then actually LOOK at the export; `v1ce-social-content.json` documents a trust-badge claim that looked fabricated but was real.

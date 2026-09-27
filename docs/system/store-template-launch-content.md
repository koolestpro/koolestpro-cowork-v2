## 🏪 STORE TEMPLATE LAUNCH CONTENT — MANDATORY (every template)

A template is not finished when it passes QA; it is finished when the content that sells it exists and reaches the distribution queue.

1. **Brand the packaging in generated product imagery** — put the brand wordmark on the product in the prompt (`a cream label reading exactly "LUMORA" in small spaced capitals`), `--quality low`, verify spelling. Lumora's 16 existing unbranded images are the documented exception; re-shoot when budget allows.
2. **Every finished template ships a post set** — LinkedIn (showcase angle), Instagram (**always a 6-slide carousel**, `docs/system/template-showcase-ig-carousel.md`, 2026-09-27), X / five angles: showcase, free-offer/Nigeria package, niche-targeted, build-in-public, full-page-at-a-glance (`mobile-strip`).
3. **The mockup images are the post assets.** Pair deliberately: `preview.png` → showcase + niche; `cover.png` → LinkedIn + free-offer; `full-page.png` → build-in-public; `mobile-strip.png` → full-page-at-a-glance.
4. **Register like any other content** — `{brand-slug}-social-content.md`/`.json` keyed `TS-{BRAND}-*`, pipeline record type `"Template Showcase"`, status `"Created"`.
5. **A finished template MUST reach the distribution queue** (2026-09-01). Route via `.ai-workflow/tools/harvest_store_template.py` (NOT `harvest_content.py`), never leave it with zero distribution rows. Stream picked from `isConceptBrand`: `Store Template` (concept, free-offer) vs `Store Template (Paid)` (paid CTA). X #4 matches `full-page-x` (never oversized `full-page`); X #5 matches `mobile-strip`. Back-to-back builds stagger themselves via `find_open_week()`.

Against every generated caption: no em dashes, run through `humanizer`, real line breaks, no hashtags on X, and never imply a concept brand was a real client. This is the stream where X caption length is a hard gate — X captions ran 282-475 chars on Lumora/Meridian and failed the 280 cap.

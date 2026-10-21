# 05 — Build Assets

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

The raw material Content Production is made from: real built pages, multi-page store templates, the device mockups that showcase them, and the caption libraries that travel with each brand. Nothing here is a post. Everything here becomes one.

---

## What is in it

**`replo-rebuilds/`** — real branded page builds, moved inside this project on 2026-08-31. Pages live at `replo-rebuilds/brands/{brand}/pages/{page}/index.html`. Two brands: `halos` and `kura`. `replo-rebuilds/templates/` holds unbranded page templates, which are **not** showcase-eligible; only branded builds under `brands/` are.

**`replo-rebuilds-pages.json`** is the selection manifest, 10 entries. Each `sourcePath` is a live project-relative path. The old `cachePath`/`cacheFolder` fields were renamed to `*Retired` and kept as history.

| sortOrder | Entry | State |
|---|---|---|
| 1 | `halos_pdp-01` story-arc PDP | used 2026-07-31 |
| 2 | `halos_hp-01` editorial homepage | used 2026-08-18 |
| 3 | `halos_lp-01` direct-response LP | used 2026-08-23 |
| 4 | `halos_ad-01` editorial advertorial | **active, unused** |
| 5 | `kura_pdp-02` social-proof PDP | **active, unused** |
| 90 | the 5 pre-2026-07-18 KURA pages | retired, fallback only |

**`store-templates/`** — multi-page store templates, one per vertical, tracked in `store-templates.json`. Both currently `Ready`: `01-watches-luxury` (demo brand MERIDIAN) and `02-skincare-beauty` (demo brand Lumora Skin). These are deliberately **not** in the showcase manifest; they have their own launch-content stream.

**`assets/frames/`** — calibrated real device bezels. `macbook-pro.svg`/`.png` and `macbook-pro-alt`, `iphone-frame.png`, and the notch-flank status-bar chips. Screen-rect coordinates were found by scanning alpha channels, not guessed, and are recorded in `CLAUDE.md`.

**`.ai-workflow/skills/page-presentation-kit/scripts/`** — the mockup toolchain: `build_device_still.py`, `build_split_page.py`, `build_mobile_strip.py`, `frame_video.py`, `scroll_video_frames.py` (default video capture since 2026-10-10: frame-by-frame, smooth, no blank lead-in), `scroll_video_raw.py` (fallback only), `status_bar_util.py`, `audit_mobile_strips.py`.

**Twelve `{brand}-social-content.json`/`.md` pairs** at the project root: bebemoss, gainful, halos, koolestpro, kura, lumora, materialkitchen, meridian, obvi, tapro, v1ce, versed. These are the durable source of truth for captions.

---

## How it works

**A page is built** by `koolestpro-weekly-template-build` (Wed ~09:21), which always builds one real brand-specific page rather than a neutral template, working through KURA then HALOS then future brands, never giving one brand a second page in the same category while another category is empty.

**A page becomes a showcase** via `koolestpro-template-showcase-weekly` (Sat ~09:09): pick the lowest unused `sortOrder`, capture, composite into real bezels, write and humanize captions, register a `Template Showcase` pipeline record, update the brand's social-content pair.

**The asset set** is 3 videos and 4 designed images:

| Asset | Size | Built by |
|---|---|---|
| `{slug} cover.mp4` | 960×720, ~29-30s | `frame_video.py cover` |
| `{slug} laptop.mp4` | 960×720, ~29-30s | `frame_video.py laptop` |
| `{slug} mobile.mp4` | 1080×1350, ~29-30s | `frame_video.py mobile` |
| `{slug} cover.png` | 1440×1080 | `build_device_still.py cover` |
| `{slug}-preview.png` | 2880×1800 | `build_device_still.py preview --style <name>` |
| `{slug}-full-page.png` | desktop width, 2 columns | `build_split_page.py` |
| `{slug}-mobile-strip.png` | **1080×1350 (4:5 post), 3 to 5 columns** | `build_mobile_strip.py` |

**Mobile strip is a post, not a contact sheet (2026-09-19, Ridwan's correction).** It used to be the whole page cut into exactly 6 mobile-width columns, so the canvas was whatever size that came to and short columns left dead space along the bottom. It is now a fixed standard post canvas that the content fills completely: 1080×1350 by default (`--size square|story|landscape` for the others), at most 5 columns, and the real column count is the largest the page can actually fill. Covering the whole canvas outranks showing every section, so the tail of a long page simply is not in the post. Ridwan: "it should always take the full page, no empty space should be visual especially on the lower parts... as long as it covers the whole space, we can leave any missing part." The old behaviour is still there as `--mode contact-sheet` for QA use.

**A 12px gap goes between the columns (2026-09-19, standing instruction).** Ridwan: "I think we should give them a little gap inbetween to create distinctions." Without it, a dark column running straight into a cream one reads as one continuous page rather than three views of it. The gap is a separator and not a frame: it sits between columns only, never around the outside, so the canvas is still covered edge to edge and the no-dead-space rule above is untouched. `--gap` and `--gap-color` override the default (12px, white). Contact-sheet mode stays fully flush.

**Caption keys** follow a fixed scheme per type: `TS-{BRAND}-*` for Template Showcase, `SA-{BRAND}-*` for Static Ad, `CRO-{BRAND}-*` for CRO Fix, `TIP-{BRAND}-*` for Tips. The `.json` and `.md` must be updated together and never allowed to drift.

---

## State

**Live:** the weekly page build and the weekly showcase. Two manifest entries sit unused and ready.

**Retired:** `replo-pages-cache/` (8 stale July copies; relocated to `assets/_archive/replo-pages-cache-retired/` on 2026-09-08), `build_mosaic.py` (replaced by `build_split_page.py`), the `.gcard` standalone graphic cards, `TS-*-MOSAIC` keys (renamed `-FULLPAGE`), `scroll_video.py` (deprecated in favour of `scroll_video_raw.py`).

**A known historical backlog, deliberately not backfilled:** 11 packages, 10 source pages and 8 assembled queue items predate the mobile-strip asset. Each backfill costs a Playwright capture, and re-running `populate_sheet.py` on an already-assembled item would append an X row to a week that has already passed. `audit_mobile_strips.py` separates this known backlog from genuinely new gaps and only exits non-zero on a new one, so the Monday check stays a real signal.

---

## Rules

| Rule | Where |
|---|---|
| **Every written output** (page copy, mockup text, CTA labels, template post copy) is humanized (v3.0, 11 passes) before it is final. No em dashes. | `docs/system/humanizer-guideline.md` |
| Never fake a device bezel with a CSS border. Use the calibrated frames. | Page Presentation Kit CORRECTED v2 |
| Every phone mockup carries the notch-flanking status bar, stills and video, including rotated phones. Never a blank top strip. | CORRECTED v4 / v2b |
| Multi-phone previews must use one of the 8 named `STYLE_PRESETS`. Never freehand a layout. If none fit, add a 9th and document it. | CORRECTED v5 |
| `flat_packed_3` is the default 3-phone preview. Generous outer margins, thin gaps between phones. | CORRECTED v7 |
| Mobile-strip spacing is flush (`pad=0`, `gap=0`) on purpose. This is the **opposite** of the preview rule. Do not "fix" one to match the other. | CORRECTED v8 |
| Every phone in one arrangement is identical in size. Only position and rotation vary. | CORRECTED v6 |
| Two-tier QA is mandatory: extract frames across each video and look at them, then re-open the companion HTML and re-parse every JSON touched. Iterate at least once before calling it done. | CORRECTED v6 |
| An uncatalogued page under `brands/*/pages/` must be added to the manifest, not skipped. This is how two pages sat unnoticed for weeks. | SOURCE CHANGED 2026-08-31 |
| Check `{brand}-cloudinary-assets.json` before regenerating. Upload fixes under a **new** public_id; Cloudinary version-pins URLs. | 2026-07-21 instruction |
| A store template is finished when its 6 posts are in the live Sheet, not when QA passes. | Store Template Launch Content §6 |

---

## Known gaps

- **The manifest is now hand-maintained.** Moving `replo-rebuilds` inline removed the cache problem and created a cataloguing burden. `halos-ad-01` and `kura-pdp-02` sat uncatalogued for weeks while the weekly task fell back to retired KURA pages.
- **Only two brands and two verticals.** HALOS and KURA for pages; watches and skincare for store templates. Every other vertical is empty, and the free-sample-site offer is vertical-specific by design.
- **Lumora's 16 product images are unbranded,** shot before the brand-the-packaging rule existed and before the gpt-image budget ran out. Documented exception. Re-shoot when budget allows.
- **HALOS has no pre-written caption library** the way KURA does. Expected, not a missing file. The weekly task writes them itself.
- **`build_mobile_strip.py` falls back to tile stitching** when `full_page=True` crashes the renderer on image-heavy pages. Real and reproducible. Related gotcha: lazy-loaded images report as broken immediately after a tile capture, so any broken-image check needs a full pre-warm scroll first or you will chase a phantom bug.

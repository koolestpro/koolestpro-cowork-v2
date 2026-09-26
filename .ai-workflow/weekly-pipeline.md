# Weekly CRO Fix Pipeline — Automated Run

One "before/after CRO Fix" post per week, generated unsupervised on a schedule so it's
ready before the post date. This doc is the exact procedure a scheduled Cowork run
follows — see `.ai-workflow/project-constitution.md` (graphic templates, gradient rules,
export bugs) and the parent `CLAUDE.md` (Claude authors HTML directly; delegation is the
exception, not the default) for the detailed rules each step below leans on.

## When this runs

Saturday morning, weekly (see the `koolestpro-weekly-cro-fix` scheduled task). Lands
finished output a few days ahead of whichever day (Mon/Wed/Fri) Ridwan actually posts,
so there's always a buffer to swap something out if needed.

## Steps

1. **Bootstrap the environment.** `source .ai-workflow/tools/bootstrap_env.sh` before
   any Playwright usage — idempotent, safe to run every time, handles the ARM64
   chromium/libXdamage setup from a cold sandbox.

2. **Pick the next target.** Read `targets_pool.json`. Filter to `status == "Available"`
   (never `"Backlog"`/`"Rejected"`) **and** whose `usedFor` array has no entry with
   `stream: "cro-fix"` — that per-stream check is what actually drives eligibility,
   not `status` (see "Reuse rule" below for why). Among those, prefer
   `leadPotential: "High"` + `visualPotential: "High"`, rotating category/brand away
   from whatever was picked most recently across *any* stream. Cross-check
   `ridwan_content_system_updated.html` items for the brand name too, not just
   `targets_pool.json`, in case the two ever drift.

   **Reuse rule (established 2026-07-12, do not regress this):** a brand is allowed
   to be used for `cro-fix` more than once over time — one prior use does not
   permanently exclude it. Only reuse a target that already has a `cro-fix` entry in
   `usedFor` when *no* zero-entry target qualifies, and when you do, pick a visibly
   different page/section/angle than the prior entry and say so explicitly in both
   the new `usedFor` note and the run summary — never a silent repeat. This mirrors
   the same rule now documented in `targets_pool.json`'s own schema notes and in
   `docs/koolestpro-content-operating-plan.md`'s Step 2 — those two files and this
   one must stay consistent with each other.

3. **Audit** the target with `koolestpro-store-auditor-skill-a` — real findings only,
   no fabricated metrics. Save the brief to `outputs/audits/{slug}_audit.md`.

4. **Rebuild.** Author the "after" HTML directly in Claude, referencing the current best
   CRO Fix rebuild as the bar to beat (see the QUALITY RATCHET rule in the parent
   `CLAUDE.md` — this rebuild must be better than the last one, not a repeat). The rebuild
   must actually implement the audit's fixes, not just restyle — see
   `feedback_verify_before_annotating` memory for why this matters (a rebuild that
   doesn't implement the claimed fix produces a before/after graphic showing two
   identical layouts with a false claim).

   **Product photos and layout discipline (2026-09-01, see CLAUDE.md's "CAROUSEL
   COVERS, EVIDENCE SLIDES, PRODUCT PHOTOS & ABOVE-THE-FOLD" section for full
   detail).** When the target brand has a real product photo with a plain studio
   background, prefer a background-removed cutout composited against a contrasting
   background over embedding the raw studio photo — check the rendered crop, never
   cut off part of the product. Build the rebuild above the fold: if there's dead
   space below the last visible element (CTA, guarantee line), shift things up and
   use the reclaimed room to enlarge the product image rather than leaving it blank.
   Verify both on the rendered screenshot, not the markup.

   **Logo and brand assets — real file, never recreated (2026-09-04, hard rule, see
   CLAUDE.md's "REAL BRAND ASSETS ONLY — NEVER RECREATE A LOGO" section).** Pull the
   target's actual logo file directly from their live site (the header `<img>`'s
   real `src`/`srcset` — not a guessed favicon or a stale schema.org `logo` field)
   and embed it exactly as-is, resized/cropped/background-removed if needed but
   never redrawn as text or CSS shapes. **This includes text-based/wordmark logos**
   — a brand name set in a distinctive custom typeface is still an image asset, not
   something to retype in a similar-looking web font; the specific typeface is part
   of the brand identity and a close-but-wrong font is a tell, not a fix. The same
   goes for any other brand mark (badges, seals, icon sets). A rebuild with a
   subtly-wrong recreated logo undermines the whole "this is genuinely your page,
   fixed" pitch. If the real file truly can't be retrieved, say so in the run
   summary rather than inventing one silently.

5. **Real screenshots**, not mockups. Use `.ai-workflow/tools/screenshot.py` against
   the live "before" URL and the local "after" rebuild HTML. Both at the same
   mobile viewport/crop so the before/after graphic lines up.

6. **Build the 3-slide CRO carousel** — cover → before/after → annotation, per
   `docs/system/cro-3-slide-carousel-format.md` (the canonical format) and the builder
   `.ai-workflow/build_caraway_carousel.py` (the bar to beat for this stream). Author it
   directly in Claude. Non-negotiables: the brand SVG background **plus** the gradient
   glow; real iPhone mockups via `compose_mobile_flat()`; the real brand logo (rasterized
   from the brand's own SVG to PNG) on the **cover only**; `@koolestpro` exactly once per
   slide (top-left); max 2-line headlines; slide 3 uses the **Q→FIX legend** (purple `?` =
   the question in the visitor's head, orange `FIX` = the change we made) with the phone
   centered exactly like the before/after slide so its connector lines hit well-separated
   targets (price / photo / CTA). **One audit = the carousel + slide 2 as the standalone
   before/after + slide 3 as the standalone annotation + a standalone clear-background
   annotated graphic.** The separate `ba-graphic` stays retired (slide 2 replaces it). The
   clear-background `anno-graphic` is **back by request (2026-09-12)**: build it with
   `.ai-workflow/build_caraway_annotation.py` — light `#F7F5F0` background, big 2-line
   headline at the top, centered phone, Q/A callouts (purple `Q` / orange `A`) in a bold
   marker font (`Caveat` 700), connected by a line + **circle head** (never a live SVG
   arrowhead), and a bottom lockup with the real brand logo + `@koolestpro`. **Brand and
   `@koolestpro` are never at the top, and `@koolestpro` appears once.** Every Q/A is drawn
   from the rebuild's **top improvements** (rank them by impact first; never reuse a prior
   audit's questions).

7. **Content pack.** Author the carousel/caption HTML directly in Claude (per the
   "Claude authors directly" rule in the parent `CLAUDE.md`), using the current best CRO
   carousel as the bar to beat. **Write every headline per `docs/system/cro-headline-system.md`**
   (derive from the single #1 finding, a different angle per surface, max 2 lines, never
   reuse last week's line). Caption *text* is written directly, never delegated. Run
   every caption through the `humanizer` skill before finalizing. The cover must carry a
   real dominant visual (phone hero + brand logo), and slides 2 and 3 must each read as a
   standalone post (top-left handle + full title + page type), not just as a slide.

8. **Export the slides.** Build the HTML, then drive the page's own capture function
   (never a generic browser screenshot):
   ```
   python3 .ai-workflow/build_caraway_carousel.py
   /tmp/cw_venv/bin/python /tmp/export_carousel.py \
     outputs/cro-fixes/{slug}_carousel.html outputs/cro-fixes/{brand-lowercase}/_new
   python3 .ai-workflow/build_caraway_annotation.py
   /tmp/cw_venv/bin/python /tmp/export_carousel.py \
     outputs/cro-fixes/{slug}_annotation.html outputs/cro-fixes/{brand-lowercase}/_anno
   ```
   The carousel page writes `slide{1,2,3}.png`; copy to
   `koolestpro_{brand-lowercase}_{slug}_carousel_slide{1,2,3}.png`. The annotation page
   writes `slide1.png`; copy to `koolestpro_{brand-lowercase}_{slug}_annotated.png`.
   Cloud runs use
   `.ai-workflow/tools/export_tip_slides.py` with `sandbox_cdn_route.py`. Then **verify
   against the real export**, not a native screenshot — decode and look at the actual
   PNGs (see "verify against the ACTUAL html2canvas output" in `project-constitution.md`).
   If a line/pin looks off, fix the source HTML and re-run — don't ship the first pass
   unchecked.

9. **Sync to the central system.** Read `ridwan_content_system_updated.html`'s
   `cowork-sync-data` JSON block, append the new item (dedupe by `id`), add the
   month bucket if missing, write back — preserve all UI code, replace only the
   JSON. Status is always `"Created"`, **never** `"Published"`.

10. **Mark the target used — per-stream only, do not touch `status`.** Update
    `targets_pool.json`: append `{stream: "cro-fix", date: today, pipelineItemId:
    <the new item's id>}` to that target's `usedFor` array, and set `lastUsedAt`.
    **Leave `status` as `"Available"`.** Setting `status: "Used"` here is the exact
    bug that shipped in this pipeline's first version and had to be corrected for
    V1CE on 2026-07-12 — it doesn't just exclude the target from `cro-fix`, it
    silently locks it out of `static-ad` and `template-showcase` too, since both of
    those tasks also gate on `status == "Available"`. `status` should only ever
    move to `"Backlog"` or `"Rejected"` for a real reason (dead site, brand asked to
    be removed, etc.), never as a side effect of normal weekly use.

11. **Update the local tracker sheet** at `outputs/weekly-tracker.xlsx` — one row
    per post: date, brand, slug, status, path to the ready-to-post folder, caption
    preview. (Local file, not live Google Sheets — the connected Drive connector
    can only create brand-new files, not edit an existing one in place. If Ridwan
    later shares a real Sheet and wants live updates, this step needs a proper
    Sheets API connector before it can write in place instead of recreating.)

12. **Leave a clear trail, don't just finish silently.** Since this runs
    unsupervised, the finished `outputs/cro-fixes/{brand-lowercase}/` folder plus
    `manifest.json` from step 8 IS the review surface — Ridwan should be able to
    open that one folder and see everything (renamed images, captions.txt, and
    a pointer back to `outputs/cro-fixes/{slug}_content.html`) without hunting.
    Also update/create `{brand-slug}-social-content.md` / `.json` at the project
    root (see "Per-Brand Social Content Library" in `CLAUDE.md`) with the new
    `CRO-{BRAND}-BA` / `-ANNO` / `-CAROUSEL` / `-X1..3` asset keys pointing at the
    real exported file paths — that file, not this folder, is the durable
    cross-post source of truth for captions once there are multiple weeks of
    output for the same brand.

13. **Show the HTML previews in chat, not just the file paths (added 2026-09-01,
    Ridwan's standing instruction).** Immediately after a successful build, present
    the two review-critical HTML files directly in the conversation with
    `mcp__cowork__present_files` — the same files already saved to the outputs
    folder in steps 4/7, don't regenerate or copy them elsewhere:
    - `outputs/cro-fixes/{slug}_rebuild.html` (the "after" mockup)
    - `outputs/cro-fixes/{slug}_content.html` (the full review pack: carousel,
      graphics, post copy tabs)
    This is a mandatory close-out step for every run, not just ones where
    something needed fixing — Ridwan wants a quick way to check the actual HTML
    without opening the outputs folder first. See "Show HTML previews after every
    build" in `CLAUDE.md` — this rule is project-wide, not CRO-Fix-specific, so the
    other weekly output skills (Static Ad, Template Showcase, Tips) follow the same
    pattern with their own equivalent rebuild/review HTML files.

## Known failure modes to watch for (from the V1CE build)

- HTML is authored by Claude directly; where a reusable script exists, use it and
  accept its output. Do not route HTML out to a separate model by default.
- If delegation IS used (exception only), note that a single bash call has a hard
  ~45s ceiling and a full build can need `--continue-from` once or twice. Normal.
- `page.goto(..., wait_until="load")` hangs on files with many embedded base64
  images — use `domcontentloaded` + a fixed settle delay instead.
- Background processes do not survive across separate tool calls in this
  sandbox — don't design any step around "start in background, check later."

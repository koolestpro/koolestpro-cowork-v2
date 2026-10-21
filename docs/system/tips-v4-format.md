# Tips carousel V4 format (approved direction 2026-09-27)

> **2026-10-09 update (Ridwan):** no post-type labels on graphics, no gradient pill labels (needed labels like `LEAK #2` or BEFORE/AFTER become plain Syne letter-spaced eyebrow text), no website in the footer (handle only, carousels keep `n / N`; the CTA slide keeps its service URL). Wherever this doc says "pill", read "plain eyebrow". Full list: `scheduled-tasks/desktop/koolestpro-tips-weekly/SKILL.md`, LABELS, URL + EVIDENCE OVERRIDE. Bar for practical posts: `outputs/tips/first-screen-leaks-before-bfcm_2026-10-09.html`.

Ridwan: the typography-hierarchy post (2026-09-18) was the best so far, but not enough. Every run must fill the full frame and use fonts that read on a phone. V4 merges three sources, and each Tips run must acknowledge all three:

| Source (look at it, don't guess) | What V4 takes from it |
|---|---|
| `references-for-posts/5 homepage fix…`, `5 products page fix…`, `5 shopify fix…` (Ridwan's own 2025 posts) | Gradient pill label (`FIX #n` / `MYTH` / `THE SYSTEM`), heavy imperative headline, short body, ONE proof element per slide (a real store screenshot when one fits), `@koolestpro \| Shopify CRO & UX` footer on every slide, framed CTA slide |
| `references-for-posts/tips-best-2026-09-18-typography-hierarchy/` | Syne 800 display type with one orange accent word, the Myth → Reality → Stat → System → Proof arc, topic-specific drawn diagrams, big stat slide, avatar CTA with the real service URL |
| `references-for-posts/90 content ideas in 9 slides/` (cover only) | Type-led cover: huge title as the visual, rich gradient field, thin line-art frame + corner marks + topic glyphs |

**The bar to beat:** `references-for-posts/tips-v4-prototype-2026-09-27/` (builder `.ai-workflow/tips-v4/build_tips_v4.py`).

## Hard size floors (native 1080×1350 CSS px, author at this size, never a small canvas scaled up)

| Element | Floor | Notes |
|---|---|---|
| Canvas | 1080×1350 (4:5) | Fills the IG and LinkedIn feed; 1:1 is retired for Tips |
| Headline | 88px min, 96-112px normal, Syne 800, letter-spacing -3px | Max 3 lines. Syne runs wide: ~9-11 characters per line at 100px. Check the render for orphan words |
| Cover title | 120px+, with a 300-440px number/hero word | Title is the visual |
| Body | 40px min, DM Sans 500, #C9C9CF | Max 2 lines. **No DM Mono / monospace for body copy** |
| Labels / pills | 28px min (pill text 34px) | |
| Footer + counter | 26px min | `@koolestpro \| Shopify CRO & UX` left, `n / N` chip right |
| Margins | 80px sides, 88px top, 128px bottom (footer zone) | |

## Full-frame rule

Every slide = pill row → headline → ONE dominant visual → one body line. The visual takes the remaining height (`flex:1; min-height:0`), roughly 35-50% of the frame. No empty band taller than ~150px anywhere. Visual types, pick per slide: real store screenshot crop (preferred when it proves the point), drawn diagram specific to the finding, giant stat, ranked list rendered at its own sizes, before/after panel pair. Iconify icon in a 104px ring top-right, specific to the slide.

## Slide arc (7 slides default, 5-9 allowed)

1 Cover (type-led or visual, standing rule 1) · 2 Myth or the problem · 3 Reality / the reframe · 4 Stat or why it breaks (real, sourced; never invented) · 5 The system / the fixes (FIX #n slides when the topic is a list of fixes) · 6 Proof: a real store doing it right, or before/after · 7 CTA framed in the orange→purple gradient border, avatar, question headline, button, `koolestpro.com/services/...` URL, "Save this" line.

## Checks before "Created"

Render every slide with the page's own capture, then look at each PNG at phone size: no clipped or overlapping text, no orphan single word on a headline line, no text under 40px except labels/footer, no empty band. Copy rules unchanged: humanizer 11-pass, no em dashes, no gradient text, X captions ≤280 counted, no hashtags on X. State the ratchet delta against the V4 prototype in the run summary.

# Mockup Style Patterns

Seven named presentation styles. Each one maps to a specific backend script (see SKILL.md's Step 2 table) — this file is the composition detail behind each, so a reference image (or a bare request with no reference) can be matched to the right one and built with the right specifics, not a generic guess.

Not every reference has to be a device mockup. Two of the seven (`flat-full-page-screenshot`, `page-unroll-surreal`) deliberately aren't — they exist because real references kept turning up that were legitimate, distinct presentation styles without a device frame at all. Forcing those into "closest device-mockup match" would throw away a genuinely useful pattern. When a new reference doesn't clearly fit, the right question is "does this deserve its own named style?" before "which existing folder is least-wrong for this."

---

## flat-browser-frame

**What it is:** the simplest, most credible presentation — a clean browser chrome (traffic-light dots + address bar) around a desktop screenshot, or a plain rounded bezel around a mobile screenshot. No perspective, no scene, no distraction from the page itself.

**When to use it:** default choice when someone just wants to see the page clearly — client review, a quick "here's what I built" share, anything where the page needs to speak for itself rather than be sold.

**Composition specifics:** light neutral background (`#eef0f3` or similar) so the frame reads as a floating object with a soft drop shadow, not embedded in a busy scene. Browser bar height ~34px, three small grey dots left-aligned, a flat address-bar pill taking up the remaining width (left empty — don't fabricate a URL in it unless asked). Corner radius: 12px desktop, 28px mobile (mobile bezel should read like a real phone screen, not a browser window).

---

## angled-3d-perspective

**What it is:** the same real screenshot, tilted in 3D space against a dark stage background — the "hero shot" treatment you see on SaaS landing pages and portfolio sites.

**When to use it:** portfolio pieces, case studies, anything meant to look impressive rather than purely functional. Works well as the single hero image at the top of a case study.

**Composition specifics:** dark radial-gradient background (`#2a2a35` fading to near-black `#0d0d12`), CSS 3D perspective (`perspective: 1800px`), device rotated roughly `rotateY(-18deg) rotateX(4deg) rotate(-1deg)` — enough tilt to read as dimensional without becoming hard to read. Heavy soft shadow beneath (`0 60px 120px rgba(0,0,0,0.55)`) to sell the depth. Keep the tilt subtle — a 45-degree spin looks like clip art, not a product shot.

---

## multi-device-collage

**What it is:** desktop and mobile versions of the same page shown together, mobile frame overlapping the bottom-left corner of the desktop frame.

**When to use it:** whenever "this is responsive" or "works everywhere" is the actual point being made — this is the single style that visually proves both viewports at once. Requires both a desktop and a mobile screenshot; don't attempt it with only one.

**Composition specifics:** light neutral background, desktop frame roughly 900px wide anchored center, mobile frame ~260px wide with a solid dark bezel (~6px border) overlapping the desktop frame's bottom-left by about a third of its own width (`margin-left: -90px`), sitting slightly lower (`margin-bottom: -30px`) so it reads as "in front of," not "stuck to the edge of," the desktop shot.

---

## dark-portfolio-shot

**What it is:** a single device frame on a dark background with a soft colored glow behind it — moodier and more premium-feeling than the flat frame, without going as far as the 3D tilt.

**When to use it:** portfolio/case-study contexts that want some polish but not full dramatic tilt — a good middle ground between `flat-browser-frame` (plain) and `angled-3d-perspective` (dramatic).

**Composition specifics:** near-black background (`#0a0a0d`), a large soft blurred glow (`radial-gradient` in the brand's accent color at low opacity, `filter: blur(40px)`) positioned behind the frame, frame itself sits flat (no tilt) with a strong shadow. The accent color should match whatever brand is being shown — don't default to one house color across every brand's shot; pass the right accent per run.

**Stacked-sections variant:** a common real-world use of this style is a full case-study scroll rather than a single hero frame — several numbered device frames (`.01`, `.02`, `.03`...) stacked vertically down the same dark background, each showing a different section or page of the same project, with small typography/color-spec callouts between them and a closing line at the bottom (e.g. "THANKS FOR WATCHING!"). Reference: `page-presentation-kit-references/dark-portfolio-shot/tura-numbered-sections-dark-case-study-pinterest.jpg`. This is the closest match to this project's own Case Study Standards (numbered sections in large display type) — reach for this variant specifically when building the case-study "Section 05 — The Build" annotated-screenshot block, not just a single hero shot.

---

## device-in-hand-lifestyle

**What it is:** a real (or photoreal AI-generated) scene of a hand holding the device, screen showing the actual page — the only style in this set that needs a photo rather than pure CSS, because nothing in code convincingly fakes a hand, skin, or ambient lighting.

**When to use it:** consumer/lifestyle brand contexts where "a real person is using this" matters more than "here is the clean UI" — most useful for social content and ad-adjacent presentation, less useful for a technical client handoff where accuracy/clarity matters more than mood.

**How it actually gets built (see `scripts/perspective_composite.py` for the mechanics):** the background photo (hand + device + environment, screen area intentionally left blank) is generated once via `gpt-image` per device type, its screen corners are calibrated once, and both are saved to `assets/frames/`. Every future request for this style reuses that same calibrated background and only warps in a new real screenshot — the photo itself is never regenerated per run, which is what keeps this style both premium-looking and honest (the environment is AI, the actual page content is always real).

**Composition specifics for the background photo itself, when generating a new one:** natural, warm ambient lighting (not studio-flat), the hand should look relaxed and naturally positioned (not stiff/centered-for-a-diagram), screen area left as a flat mid-grey or black rectangle with clearly visible corners so calibration is easy, environment should suit the brand (coffee shop table for a lifestyle app, clean desk for a productivity tool, outdoors for anything fitness-adjacent) rather than one generic backdrop reused for everything.

---

## flat-full-page-screenshot

**What it is:** no device frame, no scene, no perspective — just the real full-page screenshot itself, optionally with a subtle hairline border and soft drop shadow so it doesn't look like a stray image dropped on a page. The screenshot *is* the deliverable.

**When to use it:** contexts where speed and total context matter more than polish — internal review threads, a quick "here's the whole page top to bottom" reference, dense documentation, or anywhere a device frame would just eat space without adding credibility. Also the right default when someone explicitly wants to see the entire scroll length at once rather than a cropped hero. Reference: `page-presentation-kit-references/flat-full-page-screenshot/mutmiz-raw-scroll-capture.jpg`.

**Composition specifics:** if a border is used at all, keep it minimal — a 1px `rgba(0,0,0,0.08)` hairline and a light shadow (`0 4px 24px rgba(0,0,0,0.08)`), nothing that competes with the page's own design. No background scene, no bezel, no browser chrome. This is the cheapest style to produce (the Playwright capture from Step 1 already *is* the output, or nearly is) — don't over-engineer it into `flat-browser-frame` by adding chrome nobody asked for.

---

## page-unroll-surreal

**What it is:** a deliberately artistic, non-literal treatment — the page appears to physically bend, unroll, or drape out of a device screen (most often a laptop) rather than sitting flat inside it. Closer to digital art than a product shot. Reference: `page-presentation-kit-references/page-unroll-surreal/laptop-bent-screen-page-unrolling-hotoh.jpg` (that specific reference image was itself AI-generated — useful as a prompt/aesthetic guide, not a literal template to replicate pixel-for-pixel).

**When to use it:** when someone explicitly wants something bold and share-stopping rather than credible/technical — social content, a portfolio hero that needs to stand out in a feed, anything where "looks impressive" outranks "looks accurate." Not appropriate for client handoff or technical review contexts (pair with `flat-browser-frame` or `flat-full-page-screenshot` there instead) — the whole point of this style is that it's stylized, not a faithful representation of the page.

**How it actually gets built:** unlike the other CSS-driven styles, this one needs an image model — a bent/curved screen surface with realistic material behavior (fabric-like paper physics on a rigid laptop screen) isn't something CSS 3D transforms can fake convincingly. Generate via `gpt-image`, feeding the real screenshot in as a reference image so the on-screen content stays recognizable even as the surface warps, rather than letting the model hallucinate placeholder UI. Treat each result as a one-off creative render, not a reusable calibrated asset the way `device-in-hand-lifestyle`'s background is — the "unroll" geometry is part of the art each time, not a fixed frame to reuse.

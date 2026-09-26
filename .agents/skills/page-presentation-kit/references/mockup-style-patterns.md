# Mockup Style Patterns

Five named presentation styles. Each one maps to a specific backend script (see SKILL.md's Step 2 table) — this file is the composition detail behind each, so a reference image (or a bare request with no reference) can be matched to the right one and built with the right specifics, not a generic guess.

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

---

## device-in-hand-lifestyle

**What it is:** a real (or photoreal AI-generated) scene of a hand holding the device, screen showing the actual page — the only style in this set that needs a photo rather than pure CSS, because nothing in code convincingly fakes a hand, skin, or ambient lighting.

**When to use it:** consumer/lifestyle brand contexts where "a real person is using this" matters more than "here is the clean UI" — most useful for social content and ad-adjacent presentation, less useful for a technical client handoff where accuracy/clarity matters more than mood.

**How it actually gets built (see `scripts/perspective_composite.py` for the mechanics):** the background photo (hand + device + environment, screen area intentionally left blank) is generated once via `gpt-image` per device type, its screen corners are calibrated once, and both are saved to `assets/frames/`. Every future request for this style reuses that same calibrated background and only warps in a new real screenshot — the photo itself is never regenerated per run, which is what keeps this style both premium-looking and honest (the environment is AI, the actual page content is always real).

**Composition specifics for the background photo itself, when generating a new one:** natural, warm ambient lighting (not studio-flat), the hand should look relaxed and naturally positioned (not stiff/centered-for-a-diagram), screen area left as a flat mid-grey or black rectangle with clearly visible corners so calibration is easy, environment should suit the brand (coffee shop table for a lifestyle app, clean desk for a productivity tool, outdoors for anything fitness-adjacent) rather than one generic backdrop reused for everything.

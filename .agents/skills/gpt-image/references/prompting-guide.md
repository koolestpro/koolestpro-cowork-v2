# GPT Image Prompting Reference

Condensed prompting patterns for `gpt-image-2`. Read this before writing any prompt.

## The ChatGPT expansion rules

ChatGPT rewrites a short request before it reaches the image model. Do the same
before calling the script:

1. **Expand** the request into 2–4 sentences of concrete detail (subject/action,
   materials and textures, setting, framing, lighting, mood).
2. **Do not use quality buzzwords**: *photorealistic, hyperrealistic, 4K, 8K,
   stunning, beautiful, ultra-detailed, masterpiece, professional quality,
   cinematic lighting*. Describe the causes of quality instead (lens, light,
   texture, material, atmosphere).
3. **Do not use negatives** ("no X", "without X"). Describe what is there.
   "No text" → "plain, unmarked surfaces with clean negative space".
4. **Quote literal text** and keep it to 1–4 words.
5. **Order**: medium/style → subject/action → details/textures → environment →
   lighting/mood.

`scripts/prompt_expander.py` enforces rules 2–4 automatically; `--expand llm`
performs the full rewrite.

## Prompt Structure

Follow the expansion order: **medium/style → subject/action → details/textures →
environment → lighting/mood**. State the intended use (ad, UI mock, infographic) in
the opening sentence to set the visual mode.

Send the model 2–4 sentences of flowing prose. You can keep a labeled brief
internally, but convert the labels to prose before generating: labels and bullet
lists are for humans, not the image model.

## Specificity + Quality Cues

Be concrete about materials, shapes, textures, and the visual medium (photo, watercolor, 3D render).
Add targeted "quality levers" only when needed: *film grain*, *textured brushstrokes*, *macro detail*.

For photorealism, **do not write "photorealistic" or "hyperrealistic"** — ChatGPT's
expansion layer avoids them. Describe the photograph instead: lens (35mm/85mm/macro),
light direction and quality, depth of field, surface texture (pores, glaze, wood grain),
and camera position. That produces the same realism with more control.

## Composition

Specify:
- **Framing/viewpoint**: close-up, wide, top-down
- **Perspective/angle**: eye-level, low-angle
- **Lighting/mood**: soft diffuse, golden hour, high-contrast
- **Layout**: "logo top-right," "subject centered with negative space on left"

For cinematic, low-light, rain, or neon scenes, add extra detail about scale, atmosphere, and colour.

## People, Pose, and Action

Describe scale, body framing, gaze, and object interactions:
- "full body visible, feet included"
- "child-sized relative to the table"
- "looking down at the open book, not at the camera"
- "hands naturally gripping the handlebars"

## Constraints (Change vs Preserve)

State invariants explicitly for edits: "keep the face, pose, framing, and lighting
the same," "change only the jacket." Do **not** rely on negation for generation
("no watermark," "no logos," "no extra text"): the model tends to focus on the
thing you named. Describe the clean state instead — "plain, unmarked surfaces with
clean negative space," "unbranded materials," "clean edges."

For edits, use **"change only X" + "keep everything else the same"** and repeat the preserve list each iteration.

## Text in Images

- Put literal text in **double quotes** (e.g. `"OPEN DAILY"`)
- Keep rendered text to **1–4 words**; longer strings garble
- Specify typography: font style, size, colour, placement, weight, case
- For tricky words/brand names, spell letter-by-letter
- Use `medium` or `high` quality for small text, dense panels, multi-font layouts

## Multi-Image Inputs (Edit Mode)

Reference each input by index and description:
- "Image 1: product photo… Image 2: style reference…"
- Describe how they interact: "apply Image 2's style to Image 1"
- For compositing: "put the bird from Image 1 on the elephant in Image 2"

## Iteration Strategy

Start with a clean base prompt. Refine with small single-change follow-ups:
- "make lighting warmer"
- "remove the extra tree"
- "restore the original background"

Re-specify critical details if they start to drift.

---

## Use Case Prompt Patterns

### Infographics
Explain structured information for a specific audience. Include data hierarchy, labels, and layout.
Use `quality=high` for dense text or detailed diagrams.

### Photorealism
Prompt as if capturing a real photo. Use photography language (lens, lighting, framing).
Ask for real texture (pores, wrinkles, fabric wear). Avoid studio-polish language.

### Logo Generation
Describe brand personality and use case. Ask for clean vector-like shapes, strong silhouette,
balanced negative space. "Flat design, minimal strokes, no gradients unless essential."

### Ads
Write like a creative brief: brand positioning, desired vibe, target audience, scene, tagline.
Quote tagline text exactly. Ask for clean, legible typography.

### Style Transfer (Edit)
Describe what stays (style cues) and what changes (new content).
Add hard constraints: background, framing, "no extra elements."

### Virtual Try-On (Edit)
Lock the person (face, body shape, pose, hair, expression). Allow changes only to garments.
Require realistic fit (draping, folds, occlusion) plus consistent lighting/shadows.

### Product Mockups (Edit)
"Extract product, place on plain white opaque background."
Preserve product geometry and label legibility. Add only light polishing and contact shadow.

### Object Removal (Edit)
"Remove X. Do not change anything else." Use `input_fidelity=high` when identity matters.

### Scene Compositing (Edit)
Clearly specify what to transplant, where it goes, and what must remain unchanged.
Match lighting, perspective, scale, and shadows.

### Lighting/Weather Transformation (Edit)
Change only environmental conditions. Preserve identity, geometry, camera angle, object placement.

---

## Size Quick Reference

| Label | Resolution | Notes |
|-------|-----------|-------|
| HD portrait | 1024x1536 | Standard portrait |
| HD landscape | 1536x1024 | Standard landscape |
| Square | 1024x1024 | General-purpose default |
| 2K / QHD | 2560x1440 | Upper reliability boundary |
| Near-4K | 3824x2144 | Experimental upper end |

**Constraints**: both edges multiple of 16, max edge < 3840px, ratio ≤ 3:1,
total pixels between 655,360 and 8,294,400.

## Quality Guide

| Setting | When to use |
|---------|-------------|
| `low` | Speed/cost-sensitive, high-volume, experimentation, previews |
| `medium` | Default for most production work |
| `high` | Small/dense text, detailed infographics, close-up portraits, identity-sensitive edits, high-res |

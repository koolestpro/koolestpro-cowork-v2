---
name: gpt-image
description: Generate and edit images using the best AI model for the specific task, routed automatically across 8+ providers (OpenAI, FLUX, Ideogram, Recraft, Stability, Google, etc.). Use this skill whenever the user asks to generate, create, edit, modify, composite, restyle, or transform images — including requests like "generate an image of...", "create a logo", "make an ad", "edit this photo", "apply style transfer", "put this person in a scene", "translate the text in this image", "make a comic strip", "create a UI mockup", "create an infographic", or any prompt-to-image or image-to-image workflow. Also trigger for requests involving product mockups, virtual try-on, lighting/weather changes, object removal, sketch-to-render, or multi-image compositing. If the user mentions GPT image, FLUX, Ideogram, Recraft, image generation, or DALL-E-style workflows, use this skill. It also expands short prompts into detailed ChatGPT-style prompts before calling any image API. Always use this skill — don't attempt to call image APIs from memory.
---

# GPT Image Skill — Multi-Provider Router

Generate and edit images through an intelligent router that picks the **best model for the specific job** across 8+ providers, rather than defaulting to one expensive backend for everything.

**The old OpenAI-only scripts are backed up to `scripts/_legacy/`.** They still work if you need them, but the new router is the default.

## Why this exists

Using OpenAI's `gpt-image-2` for everything works well but costs more than necessary. A product lifestyle shot with NO text can use **FLUX** (better photorealism, 5× cheaper). A quick draft can use **Hyperbolic FLUX schnell** ($0.0005/image). But a static ad with a headline still needs **OpenAI** — it's the only model that reliably renders text exactly as specified.

**Tested reality (2026-09-01):**
- **OpenAI gpt-image-2:** Best text accuracy. Headlines, quotes, CTAs render correctly. Most expensive.
- **Ideogram v2:** Cheaper (~50%), but makes spacing/casing errors ("Glow Up" → "glowup"). Good for drafts, risky for final client work.
- **FLUX (inference.sh/Together):** Excellent photorealism, terrible text. Brand names become gibberish ("SUIORRIN"). Use ONLY for visuals with no text.

**Typical savings vs. OpenAI-only:** 0–50% depending on the job. Text-heavy work saves nothing (still need OpenAI). Visual-only work saves 50–90%.

---

## Prompt Expansion Engine (ChatGPT-parity layer)

A raw API prompt is used literally. ChatGPT does not do that: before it calls the
image model it silently rewrites a short request into a detailed, multi-sentence
scene. That rewrite is the main reason ChatGPT images look better than raw API
images. This skill now reproduces it in two places:

1. **The agent (primary, free, always on).** Before calling `generate.py` or
   `edit.py`, rewrite the request using the rules below and pass the expanded
   prompt. This is the path that matters most.
2. **The script (safety net).** `generate.py`, `edit.py`, and `pipeline.py` run
   `scripts/prompt_expander.py` on every prompt. `--expand auto` (default) strips
   quality buzzwords, rewrites the exact common negatives, and warns about
   unquoted text and missing scene parts. `--expand llm` performs the full rewrite
   through an OpenAI-compatible chat endpoint (opt-in; see configuration below).
   `--expand off` disables the layer.

### The leaked DALL·E 3 rules (apply verbatim)

These come from OpenAI's 2023-10-07 DALL·E 3 system instructions (publicly leaked
and widely mirrored). They are the behaviour to copy:

Source: [jujumilk3/leaked-system-prompts — openai-dall-e-3_20231007-1.md](https://github.com/jujumilk3/leaked-system-prompts/blob/main/openai-dall-e-3_20231007-1.md)

- **Expand, don't paraphrase.** If the user gave no detail, invent specific,
  plausible detail: subject and action, materials, textures, clothing, surface
  details, setting, framing, lighting, mood. Never ask a question; never leave a
  section vague.
- **Ban quality buzzwords.** Never write *photorealistic, hyperrealistic,
  4K, 8K, UHD, ultra-detailed, hyper-detailed, highly detailed, stunning,
  beautiful, gorgeous, breathtaking, masterpiece, professional quality,
  best quality, highest quality, award-winning, cinematic lighting*.
  Describe the **causes** of quality instead: lens, light direction, texture,
  material, atmosphere.
- **No negative phrasing.** Do not write "no X", "without X", "don't include X",
  "avoid X", or "free of X". Describe what **is** there. "A room with no chairs"
  becomes "a sparse room with bare walls, a window, and an empty wooden floor".
- **Exact text.** Copy literal text verbatim inside double quotes, keep it to
  **1–4 words**, and specify placement, size, weight, colour, and case.
- **One prompt, no labels.** Output only the final prompt: flowing prose,
  2–4 sentences, no bullets, no headings, no explanation.

### The 5-part blueprint

Build every generation prompt in this order:

```
[Artistic medium/style] + [Core subject & action] + [Fine details/textures]
+ [Environment/background] + [Lighting & mood]
```

Example:

> **User:** "cozy coffee shop desk with a mug"
>
> **Expanded:** "A warm, inviting close-up photograph of a polished dark walnut
> desk. On it sits a white ceramic mug with steam curling upward, a closed
> leather-bound journal, and a slim laptop showing a clean analytics dashboard.
> Behind it, a softly out-of-focus coffee shop interior with warm fairy lights and
> blurred patrons. Soft morning sunlight streams through a large window, casting
> long gentle shadows across the workspace."

### Do / don't

| Don't | Do |
|---|---|
| "photorealistic 4K stunning portrait" | "a close-up photograph, 85mm lens, soft window light, visible skin texture and fine hair" |
| "a street with no cars" | "an empty asphalt street with wet reflections and bare kerbs" |
| "no extra text" | "plain, unmarked surfaces with clean negative space" |
| "beautiful product shot" | "a ceramic bottle on honed marble, single softbox from the left, contact shadow" |
| headline without quotes | `Headline reads exactly: "GLOW UP"` (1–4 words) |

### Script flags (both `generate.py` and `edit.py`)

| Flag | Default | Description |
|------|---------|-------------|
| `--expand auto` | yes | Sanitize, rewrite common negatives, lint. Never spends a chat call. Prints an advisory for short prompts. |
| `--expand lint` | — | Sanitize + report only. |
| `--expand llm` | — | Full rewrite through the chat expander. |
| `--expand off` | — | Pass the prompt through untouched. |
| `--expand-model` | `gpt-4o-mini` | Chat model for `--expand llm`. |
| `--expand-min-words` | 30 (20 for edits) | `auto` treats shorter prompts as needing expansion. |

The expander also has a standalone CLI:

```bash
# Lint only (no API call)
uv run <SKILL_DIR>/scripts/prompt_expander.py \
  --prompt "cozy coffee shop desk with a mug" \
  --type product-lifestyle --expand lint

# Full rewrite + machine-readable report
uv run <SKILL_DIR>/scripts/prompt_expander.py \
  --prompt "..." --expand llm --json
```

### LLM expander configuration (optional)

`--expand llm` works with any OpenAI-compatible chat endpoint, not just OpenAI.
Set these in the shell or the skill `.env`:

```bash
GPT_IMAGE_EXPANDER_BASE_URL=https://api.openai.com/v1   # or Together/Groq/OpenRouter/Ollama
GPT_IMAGE_EXPANDER_API_KEY=...                          # falls back to OPENAI_API_KEY
GPT_IMAGE_EXPANDER_MODEL=gpt-4o-mini
```

**If the key has no credits**, `--expand llm` reports `insufficient_quota` and
falls back to the linted prompt. That is not fatal: the agent-side expansion
(path 1) still works and costs nothing.

### Quality parameters: don't copy DALL·E 3 values

`gpt-image-2` accepts `--quality low|medium|high|auto` and has **no `--style`
parameter**. `hd`, `standard`, `vivid`, and `natural` are DALL·E 3-only. For
compatibility the scripts map `hd → high` and `standard → medium`, but write
`high` in real commands. Passing `--style vivid` is not supported.

For final text-heavy work (ads with headlines, book covers, infographics), use
`--quality high` or `--budget premium`; dense typography benefits from it.

---

## Setup

No install step needed — scripts use PEP 723 inline metadata. `uv run` handles dependency resolution automatically on first invocation.

### 1. Get API keys (get them all, or start with 3)

You don't need every provider. Start with these three and expand as needed:

| Priority | Provider | Why | Get key at |
|----------|----------|-----|-----------|
| **1** | OpenAI | Best text accuracy. Required for text-heavy ads, book covers, infographics. | platform.openai.com |
| **2** | inference.sh | FLUX using your existing video credit. Best for visual-only images (product shots, lifestyle). | inference.sh (or reuse video-gen key) |
| **3** | Ideogram | Cheaper alternative for drafts. Acceptable text quality with minor errors. | ideogram.ai/api |
| **4** | Together AI | Cheapest FLUX if you add credit. Same quality as inference.sh but faster. | together.ai |

**Optional expansions:**

| Provider | Best for | Get key at |
|----------|----------|-----------|
| fal.ai | Highest quality FLUX (slightly better than Together) | fal.ai |
| Recraft | Vector logos, UI mockups, style-consistent batches | recraft.ai |
| Hyperbolic | Cheapest possible inference (bulk batches) | hyperbolic.xyz |
| Stability AI | Photoreal editing, professional photography | stability.ai |
| Google (Vertex) | Safe, realistic people portraits | makersuite.google.com |

### 2. Add keys to `.env`

Create or edit `<SKILL_DIR>/.env` (same folder as this SKILL.md):

```bash
# Minimum viable set
OPENAI_API_KEY=sk-...
TOGETHER_API_KEY=...
IDEOGRAM_API_KEY=...

# Optional expansions
FAL_KEY=...
RECRAFT_API_KEY=...
HYPERBOLIC_API_KEY=...
STABILITY_API_KEY=...
GOOGLE_API_KEY=...
```

Keys are read from shell env first, then `.env` file, then the script errors cleanly.

---

## How the Router Works

### Two scripts

| Script | Purpose | When to use |
|--------|---------|-------------|
| `scripts/generate.py` | Text → image (generation) | No input image. Creating from scratch. |
| `scripts/edit.py` | Text + image(s) → image (editing) | Has 1+ input images. Modifying, compositing, restyling. |

### The decision flow

```
1. You provide: prompt + optional --type + optional --budget
2. Router scans prompt for keywords → guesses image type if --type omitted
3. Router looks up model-registry.json:
     For this image type + this budget mode → best provider/model
4. Router checks if that provider's API key exists
     If missing → falls back to next-best option
5. Router calls the provider, downloads the image, saves it
```

### Budget modes

| Mode | Max cost/image | When to use |
|------|---------------|-------------|
| `cheap` | $0.01 | Drafts, previews, bulk batches, concepts |
| `balanced` | $0.05 | **Default.** Most production work. |
| `premium` | $0.10 | Final client deliverables, hero assets |

### Image types (router knows 14 categories)

| Type | Best model | Why |
|------|-----------|-----|
| `static-ad-text-heavy` | **Ideogram v3** | Unbeatable text accuracy |
| `static-ad-visual` | **FLUX dev** (Together) | Best photorealism for the price |
| `product-photoreal` | **FLUX dev** (Together) | Precise materials, clean backgrounds |
| `product-lifestyle` | **FLUX dev** (Together) | Editorial context, lighting |
| `book-cover` | **Ideogram v3** | Title/author text + art composition |
| `ui-mockup` | **Recraft v3** | Built for UI, clean components |
| `logo-brand` | **Recraft v3** | Vector output, scalable marks |
| `social-graphic` | **Ideogram v2 Turbo** | Fast, cheap, readable at small sizes |
| `lifestyle-photography` | **FLUX dev** (Together) | People, scenes, editorial |
| `illustration-artistic` | **FLUX dev** (Together) | Style range, detail |
| `infographic` | **Ideogram v3** | Text + structured graphics |
| `pattern-texture` | **FLUX schnell** (Together) | Cheapest, good enough |
| `portrait` | **FLUX dev** or **Google Imagen 3** | Realistic faces |
| `concept-sketch` | **FLUX schnell** (Hyperbolic) | Fastest iteration, $0.0005/image |

**You don't need to memorize this.** The router reads `model-registry.json` and decides automatically. You only need to know it exists if you want to override with `--type` or `--provider`.

---

## CLI Reference

### generate.py

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "Your prompt here" \
  --output /path/to/output.png \
  --size 1024x1536 \
  --quality medium \
  --type static-ad-text-heavy \
  --budget balanced \
  --expand auto \
  --n 1
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--prompt` | **Yes** | — | Generation prompt |
| `--output` | No | `output.png` | Output file path |
| `--size` | No | `1024x1024` | Image dimensions |
| `--quality` | No | `medium` | `low` / `medium` / `high` / `auto` (`hd`→`high`, `standard`→`medium`) |
| `--output-format` | No | `png` | `png` / `jpeg` / `webp` |
| `--output-compression` | No | — | `0`–`100` (jpeg/webp only) |
| `--n` | No | `1` | Number of variants |
| `--type` | No | auto | Force image type category |
| `--budget` | No | `balanced` | `cheap` / `balanced` / `premium` |
| `--provider` | No | auto | Force provider (skips routing) |
| `--model` | No | auto | Force model (use with `--provider`) |
| `--expand` | No | `auto` | `auto` / `lint` / `llm` / `off` (see expansion engine) |
| `--expand-model` | No | `gpt-4o-mini` | Chat model for `--expand llm` |
| `--expand-min-words` | No | `30` | `auto` expands shorter prompts |
| `--env-file` | No | `../.env` | Path to `.env` with API keys |
| `--show-costs` | No | — | Print cost table and exit |
| `--show-route` | No | — | Preview chosen route without generating |
| `--verbose` / `-v` | No | — | Print routing decisions |

### edit.py

```bash
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "Your edit instruction" \
  --images input1.png input2.png \
  --output /path/to/output.png \
  --size 1024x1536 \
  --quality medium
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--prompt` | **Yes** | — | Editing instruction |
| `--images` | **Yes** | — | Input image path(s) |
| `--output` | No | `output.png` | Output file path |
| `--size` | No | `1024x1024` | Output dimensions |
| `--quality` | No | `medium` | `low` / `medium` / `high` / `auto` (`hd`→`high`, `standard`→`medium`) |
| `--n` | No | `1` | Number of variants |
| `--provider` | No | `openai` | Editing provider (OpenAI or Stability) |
| `--model` | No | `gpt-image-2` | Model override |
| `--expand` | No | `auto` | `auto` / `lint` / `llm` / `off` (edit-safe rules) |
| `--expand-model` | No | `gpt-4o-mini` | Chat model for `--expand llm` |
| `--expand-min-words` | No | `20` | `auto` expands shorter edit instructions |
| `--env-file` | No | `../.env` | Path to `.env` |

**Editing support matrix:**

| Provider | Max images | Best for |
|----------|-----------|----------|
| `openai` | 10 | Multi-image compositing, style transfer, object removal, virtual try-on |
| `stability` | 1 | Search-and-replace edits on single images |

Other providers do not support editing via API. The router defaults to OpenAI for all edits.

---

## Workflow Patterns

### Generate: Static ad with headline (auto-routed to Ideogram)

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "Create a polished Instagram ad for an organic skincare serum. Headline reads exactly: \"Your skin will glow\". Clean layout on a warm cream background with plain unmarked surfaces, the serum bottle centered, a soft contact shadow, and generous negative space at the top." \
  --size 1024x1536 --budget balanced \
  --output serum-ad.png
```

*Router detects text-heavy ad → sends to Ideogram v3. The agent has already applied the 5-part blueprint and kept the headline to 4 quoted words.*

### Generate: Product lifestyle shot (auto-routed to FLUX)

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "A close-up photograph of a minimalist ceramic coffee mug on a reclaimed wood table, fine steam rising, visible wood grain and glaze texture, morning sunlight from a window casting a long soft shadow, shallow depth of field, editorial lifestyle framing" \
  --size 1024x1536 --budget balanced \
  --output coffee-lifestyle.png
```

*Router detects lifestyle photography → sends to FLUX.1 [dev] via Together AI (~$0.025 vs. $0.06 OpenAI).*

### Generate: 4 ad variants on the cheap (bulk batch)

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "4 variations of a modern fitness app logo, geometric dumbbell icon, flat vector style, dark background, minimal" \
  --size 1024x1024 --budget cheap --n 4 \
  --output logo-variant.png
```

*Router sends to Ideogram v2 Turbo or FLUX schnell. 4 images for ~$0.01 total.*

### Generate: Book cover (explicit type)

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "Book cover for a thriller novel. Title: 'The Last Cipher'. Author: 'A.R. Whitmore'. Dark city skyline, rain, neon reflections, moody atmosphere" \
  --type book-cover --budget premium \
  --size 1024x1536 --output book-cover.png
```

### Edit: Multi-image compositing (OpenAI)

```bash
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "Place the product from Image 2 onto the wooden table in Image 1, slightly to the right. Match lighting and shadows." \
  --images scene.png product.png \
  --size 1024x1536 --output composite.png
```

### Preview routing without generating

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "A sleek UI mockup for a finance dashboard, dark mode, charts and cards, iPhone frame" \
  --show-route
```

Outputs:
```
============================================================
ROUTE PREVIEW
============================================================
  Prompt:     A sleek UI mockup for a finance dashboard...
  Type:       ui-mockup
  Budget:     balanced
  Provider:   recraft
  Model:      recraft-v3
  Quality:    medium
  Size:       1024x1024
  Type desc:  App or website screenshots, device frames, UI concepts.
============================================================
```

---

## Cost Comparison

Run `python3 scripts/generate.py --show-costs` to see live pricing.

Approximate cost per **1,000 images** at 1024×1024:

| Provider/Model | Cost/1K images | Best for |
|----------------|---------------|----------|
| Hyperbolic FLUX schnell | **$0.50** | Massive bulk batches |
| Hyperbolic FLUX dev | **$1.50** | Cheap general purpose |
| Together FLUX schnell | **$3.00** | Fast drafts |
| Stability SD 3.5 Turbo | **$4.00** | Quick iterations |
| Ideogram v2 Turbo | **$10.00** | Cheap text ads |
| Recraft v3 | **$20.00** | UI/logos/style consistency |
| Together FLUX dev | **$25.00** | **Default workhorse** |
| Ideogram v3 | **$25.00** | Best text rendering |
| Google Imagen 3 | **$30.00** | Safe people photography |
| fal FLUX dev | **$28.00** | Slightly better than Together |
| OpenAI gpt-image-2 low | **$20.00** | (same as Recraft) |
| OpenAI gpt-image-2 medium | **$40.00** | (old default) |
| fal FLUX pro | **$55.00** | Maximum visual quality |
| Stability SD 3.5 Large | **$65.00** | Premium photoreal |
| OpenAI gpt-image-2 high | **$80.00** | (most expensive) |

**Bottom line:** Visual-only images (product shots, lifestyle photos, backgrounds) are 50–90% cheaper via FLUX. Text-heavy images (ads with headlines, book covers) still need OpenAI for reliable accuracy — no savings there, but no quality loss either. Use the router to automatically pick the right tool.

---

## Provider Details

### OpenAI (`openai`)
- **Models:** `gpt-image-2`
- **Strengths:** Best text-in-image accuracy (tested). Multi-image editing. Consistent results.
- **Weaknesses:** Most expensive. Slower than FLUX.
- **Use when:** Any image with readable text (ads, book covers, social graphics), editing/compositing, or when accuracy matters more than cost.

### inference.sh (`infsh`)
- **Models:** `flux-dev`, `p-image`
- **Strengths:** Uses your existing video credit. Good FLUX quality. Same photorealism as Together.
- **Weaknesses:** Async task queue (10–30s per image, requires polling). Slower than Together. No editing.
- **Use when:** Visual-only images when you don't want to top up Together AI. Already have credit from video-gen.

### Together AI (`together`)
- **Models:** `flux-schnell`, `flux-dev`
- **Strengths:** Cheapest FLUX, fast (2–5s), excellent photorealism
- **Weaknesses:** No editing API, text is garbled, needs credit top-up
- **Use when:** Visual-only images at high volume where speed matters.

### fal.ai (`fal`)
- **Models:** `flux-pro`, `flux-dev`
- **Strengths:** Highest quality FLUX inference
- **Weaknesses:** Slightly pricier than Together, no editing
- **Use when:** Hero assets where visual quality is everything

### Ideogram (`ideogram`)
- **Models:** `ideogram-v2`, `ideogram-v2-turbo` (v3 endpoint not yet mapped)
- **Strengths:** Cheaper than OpenAI. Decent text for simple words. Good layout/composition.
- **Weaknesses:** Text spacing/casing errors ("Glow Up" → "glowup"). No editing API. Not reliable for client-facing work.
- **Use when:** Drafts, internal concepts, social graphics where minor text errors are acceptable.

### Recraft (`recraft`)
- **Models:** `recraft-v3`
- **Strengths:** Vector output, UI mode, style consistency across batches
- **Weaknesses:** No editing, freeform text weaker than Ideogram
- **Use when:** Logos, UI mockups, 4 ad angles that must look like a set

### Hyperbolic (`hyperbolic`)
- **Models:** `flux-dev`, `flux-schnell`
- **Strengths:** Cheapest inference on Earth
- **Weaknesses:** Reliability variable, no editing, limited support
- **Use when:** Bulk runs where cost matters more than consistency

### Stability AI (`stability`)
- **Models:** `sd-3-5-large`, `sd-3-5-large-turbo`
- **Strengths:** Editing API, professional photorealism, style variety
- **Weaknesses:** Expensive, text weak
- **Use when:** High-end photo editing, professional photography concepts

### Google (`google`)
- **Models:** `imagen-3`
- **Strengths:** Safe, realistic people, good instruction following
- **Weaknesses:** Conservative creativity, weak text, editing limited
- **Use when:** Portraits, sensitive use cases, conservative brands

---

## Image Type Taxonomy

The router recognizes 14 image types. You can force one with `--type` or let it auto-detect from your prompt.

| Type | Keyword triggers | Default provider (balanced) | Notes |
|------|-----------------|---------------------------|-------|
| `static-ad-text-heavy` | headline, tagline, CTA, banner, quote | **OpenAI** gpt-image-2 | Only reliable text accuracy (tested) |
| `static-ad-visual` | ad, campaign, hero image, product shot | **inference.sh** FLUX dev | Excellent photorealism, no text needed |
| `product-photoreal` | product, mockup, white background, isolated | **inference.sh** FLUX dev | Best value for clean product shots |
| `product-lifestyle` | lifestyle, in use, hands holding, setting | **inference.sh** FLUX dev | Editorial context, no text |
| `book-cover` | book cover, album cover, title, author | **OpenAI** gpt-image-2 | Title text must be exact |
| `ui-mockup` | UI, UX, screenshot, app screen, dashboard | **Recraft** v3 | Built for interface design |
| `logo-brand` | logo, brand mark, icon, emblem, symbol | **Recraft** v3 | Vector output, scalable |
| `social-graphic` | social media, carousel, quote card, LinkedIn | **OpenAI** gpt-image-2 | Quote text must be exact |
| `lifestyle-photography` | people, editorial, fashion, interior, travel | **inference.sh** FLUX dev | People and scenes |
| `illustration-artistic` | illustration, drawing, painting, sketch, anime | **inference.sh** FLUX dev | Style range, no text |
| `infographic` | infographic, chart, graph, diagram, timeline | **OpenAI** gpt-image-2 | Text + structure must be correct |
| `pattern-texture` | pattern, texture, background, wallpaper | **inference.sh** FLUX dev | Cheapest, no text needed |
| `portrait` | portrait, headshot, face, avatar, profile picture | **inference.sh** FLUX dev | Realistic faces |
| `concept-sketch` | sketch, draft, rough, concept, exploration | **inference.sh** p-image | Fastest using existing credit |

---

## Advanced: Override the Router

### Force a specific provider

```bash
--provider ideogram --model ideogram-v3
```

### Force provider but let router pick model

```bash
--provider together
```

### Custom .env location

```bash
--env-file /path/to/my/keys.env
```

### Dry-run to see routing decision

```bash
--show-route
```

---

## Error Handling

The scripts validate:
- At least one provider API key is configured
- Size is valid for the chosen model
- `--output-compression` only used with jpeg/webp
- Input images exist (edit mode)
- Editing provider supports the number of input images

If a provider fails (timeout, rate limit, API error), the router does **not** automatically fall back to another provider — this prevents silent cost surprises. The error is printed clearly so you can decide: retry, switch provider manually, or check your key.

---

## Adding a New Provider

1. Add provider + models to `model-registry.json`
2. Create adapter class in `scripts/providers.py` with `generate()` and `edit()` methods
3. Register in `PROVIDER_CLASSES` dict
4. Update this SKILL.md

No changes needed to `generate.py` or `edit.py` — the router reads the registry dynamically.

---

## Legacy Scripts

The original OpenAI-only scripts are preserved at:
- `scripts/_legacy/generate_openai.py`
- `scripts/_legacy/edit_openai.py`

Use them if you need the old behavior for a specific integration. They are not maintained going forward.

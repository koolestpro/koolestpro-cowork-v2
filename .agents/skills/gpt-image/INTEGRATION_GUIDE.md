# Integration Guide — Koolestpro Cowork V2

This document shows how the new GPT Image Router fits into your existing project workflows.

## What changed

The `gpt-image` skill now routes every generation to the best model for the job, instead of always using OpenAI. Your existing skills (`static-ad-image`, `page-presentation-kit`, etc.) still call the same `generate.py` and `edit.py` scripts — but those scripts now intelligently pick the backend.

**Your old OpenAI-only scripts are backed up to `scripts/_legacy/`.**

## Step 1: Add API keys

Copy `.env.example` to `.env` in the skill directory and add at minimum these 3 keys:

```bash
cp <SKILL_DIR>/.env.example <SKILL_DIR>/.env
```

Then edit `.env` and fill in:
- `OPENAI_API_KEY` (you already have this)
- `TOGETHER_API_KEY` (get at together.ai — free $1 credit to start)
- `IDEOGRAM_API_KEY` (get at ideogram.ai/api — free tier available)

## Step 2: Update your project skills

### static-ad-image skill

Your static ads have two distinct needs:

**Ad angles 1 & 4 (headline-heavy):** Use `--type static-ad-text-heavy` so they route to Ideogram (perfect text).

**Ad angles 2 & 3 (visual-heavy):** Use `--type static-ad-visual` so they route to FLUX (better photorealism, cheaper).

Example change in `static-ad-image` skill Step 4:

```bash
# Problem/Solution angle — has a headline callout
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "Create a polished ad... Headline reads exactly: '...'" \
  --type static-ad-text-heavy \
  --size 1024x1536 --output ad-1.png

# Benefit/Result angle — product visual is the hero
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "Create a product hero shot..." \
  --type static-ad-visual \
  --size 1024x1536 --output ad-2.png
```

**Expected savings:** 4 ads that used to cost ~$0.24 (OpenAI medium) now cost ~$0.10 (Ideogram + FLUX mix).

### Template Showcase / Page Presentation Kit

Your mockup images are built with Playwright + PIL, not AI generation — no changes needed.

However, if you generate product images for templates (like Lumora's branded bottles):

```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "A cream skincare bottle on a marble surface... label reading exactly 'LUMORA'" \
  --type product-photoreal \
  --size 1024x1536 --output lumora-bottle.png
```

This routes to FLUX dev (~$0.025) instead of OpenAI (~$0.06).

### CRO Fix content

The before/after graphics and annotated change graphics are html2canvas captures — no AI generation, no changes.

### Tips carousels

Your carousel slides are HTML/CSS rendered with html2canvas — no AI generation, no changes.

### Digital products / book covers / lifestyle images

Use explicit types for these:

```bash
# Book cover
uv run .../generate.py --prompt "..." --type book-cover --output cover.png

# Lifestyle photo for a course
uv run .../generate.py --prompt "..." --type lifestyle-photography --output hero.png

# Quick draft / concept
uv run .../generate.py --prompt "..." --type concept-sketch --budget cheap --output draft.png
```

## Step 3: Batch generation with --budget cheap

When you need many images at once (e.g., generating 16 product shots for a template store):

```bash
uv run .../generate.py \
  --prompt "..." \
  --type product-photoreal \
  --budget cheap \
  --n 16 \
  --output batch/product.png
```

This routes to FLUX schnell (~$0.003/image) or Hyperbolic (~$0.0015/image). 16 images for under $0.05.

## Step 4: Preview routing decisions

Before a big batch, check where the router will send each job:

```bash
uv run .../generate.py --prompt "..." --show-route
```

This prints the chosen provider, model, and estimated cost without spending a cent.

## Provider quick-reference for your project

| What you're making | Use this provider | Why | Cost (1024×1536) |
|---|---|---|---|
| Static ad with headline | Ideogram v3 | Best text accuracy | ~$0.03 |
| Static ad visual-only | Together FLUX dev | Best photorealism/price | ~$0.04 |
| Product photo / lifestyle | Together FLUX dev | Precise, editorial | ~$0.04 |
| Book cover with title | Ideogram v3 | Text + art combined | ~$0.03 |
| UI mockup | Recraft v3 | Built for interface design | ~$0.02 |
| Logo / brand mark | Recraft v3 | Vector output, scalable | ~$0.02 |
| Bulk product shots (16+) | Hyperbolic FLUX schnell | Cheapest possible | ~$0.005 |
| Client hero asset (final) | fal FLUX pro | Maximum quality | ~$0.08 |
| Multi-image compositing | OpenAI gpt-image-2 | Only one with real editing | ~$0.06 |

## Troubleshooting

**"Missing API key" error:**
The router tried a provider whose key isn't in `.env`. Either add the key, or force a different provider with `--provider together`.

**"Provider does not support editing" error:**
You tried to edit an image with a provider that only supports generation (e.g., Together, Ideogram). Editing defaults to OpenAI. Use `--provider openai` for edits.

**Wrong image type detected:**
Auto-detection is convenience, not magic. Force the correct type: `--type product-photoreal`.

**Want to see all options:**
```bash
python3 scripts/generate.py --show-costs
```

## Migration checklist

- [ ] Copy `.env.example` to `.env` and add Together + Ideogram keys
- [ ] Run one test generation: `python3 scripts/generate.py --prompt "test" --show-route`
- [ ] Update `static-ad-image` skill to pass `--type` per ad angle
- [ ] Update template product image generation to pass `--type product-photoreal`
- [ ] Delete or archive old `_legacy` scripts when you're confident
- [ ] Track your new spend vs. old spend for one week

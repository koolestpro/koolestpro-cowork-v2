---
name: static-ad-image
description: Generate a set of polished, photoreal static ad/promo images (single images, not carousels) for a product or brand — for Koolestpro's own content pipeline or for real paid client CRO work. Produces exactly 4 ad concepts (problem/solution, benefit/result, social proof/trust, offer/urgency), a combined LinkedIn showcase, X-ready assets, and captions, then exports the result into this project's local JSON content pipeline. Use this whenever the user asks to make a static ad, product ad image, ad creative, promo image, ad showcase, or "static ad" for any product — whether they hand over finished copy, just a product URL or photo, or nothing but a product name. Also use for CRO/client deliverables that call for single-image ad creative instead of a carousel. Do not confuse with carousel/slide skills (koolestpro-content-engine, koolestpro-cro-content-maker-skill-e) — this skill is for standalone static ad images specifically.
compatibility: requires gpt-image skill (multi-provider router), humanizer skill
---

# Static Ad Image

Turn a product — real or hypothetical, Koolestpro's own or a client's — into a set of four ready-to-post static ad images, plus a LinkedIn showcase, X assets, and captions. This is the execution engine for Step 4 ("Weekly Static Ad Image Showcase") of `docs/koolestpro-content-operating-plan.md`, but it's written to be general-purpose: the same flow works for one-off client deliverables, not just the weekly koolestpro cadence.

This skill is the strategy/orchestration layer. It does not call any image API directly — it delegates every actual pixel render to the **gpt-image** skill's multi-provider router, and runs every piece of finished copy through the **humanizer** skill before treating it as final. If either of those skills isn't available, stop and say so rather than improvising a substitute.

## Default mode: prompt pack (2026-09-18)

**Default = no image API calls.** Unless Ridwan asks in that request to render ("generate the images", "use the API", "use gpt-image"), a Static Ad run does research, target selection, copy, and the four ad prompts (plus a product-mockup prompt if no real photo exists), humanizes the captions, and exports the prompt pack to `.ai-workflow/pending-static-ad-{slug}.md` (format: parent `CLAUDE.md` → "NO IMAGE CREDITS — PROMPT-PACK HANDOFF"). Ridwan renders in ChatGPT and sends the images back; then ingest, build `index.html`, register. Scheduled runs are always prompt-pack runs. Register nothing until images exist. Steps 3-4 below (generate.py / edit.py) apply only in render mode.

## Why the process is structured this way

Cheap AI ad generators produce generic-looking output because they skip two things: they don't ground the copy in anything real about the product, and they use one visual template for every message. This skill fixes both — copy always traces back to something real (given copy, the product's own page, or research), and each of the four ad angles gets its own visual grammar borrowed from real DTC ad creative, not a single reused template with swapped text.

**New in this version:** the gpt-image skill now routes each generation to the best AI model for the specific job (Ideogram for text-heavy ads, FLUX for visual-heavy ads, OpenAI for precise editing) instead of defaulting to OpenAI for everything. This cuts costs by 50–60% while improving text accuracy.

## Step 0 — Find out where output belongs (always do this first)

This skill is portable — it gets installed once and used across any project, so it never assumes it knows where to save things or what pipeline schema (if any) a project uses. Look at the current project's `CLAUDE.md` (already loaded into context automatically — no need to search for it) for a section called **"Static Ad Image — Export Routing"**. It will say where files go and what pipeline/JSON registration step (if any) to follow.

- If that section exists, follow it exactly — including whatever `type` value or registration mechanism it specifies. Don't assume the type is called `"Static Ad"` or that a `ridwan_content_system_updated.html`-style JSON pipeline exists elsewhere; that's this one project's convention, not a universal one.
- If it doesn't exist in the current project, default to `./static-ad-output/{slug}_{date}/` in the current project, skip any pipeline-JSON-export step (there's nothing documented to export *to*), and tell the user plainly: the images/captions/index.html still get delivered, just without a registration step, since none was described.

## Step 1 — Figure out what you're working with

Gather whatever the user gave you: a product URL, a product photo, product notes, ready-made copy, and/or a brand/client name.

- If no brand/client name is given, default to **Koolestpro** and treat this as portfolio/sample work.
- If this is real client work, treat it as a concept/portfolio piece unless the user says otherwise — don't imply the brand commissioned or endorsed it (see Brand Safety below).
- If you were invoked with no specific product at all (e.g. from a scheduled task), check whether the current project has a `targets_pool.json`-style rotation file (this is a `koolestpro-cowork-v2` convention, not universal — Step 0's routing section will say if a given project has an equivalent). If it exists, pick a target with `status: "Available"` whose `usedFor` array has no entry with `stream: "static-ad"`, preferring `visualPotential: "High"` and category variety against recent history. If no such file exists in the current project, fall back to whatever sample/portfolio product makes sense for that project instead of stalling.

## Step 2 — Source the copy (decide automatically, in this order)

1. **User gave copy** (headlines, bullets, claims) → use it verbatim as your messaging source. Don't rewrite the substance, just adapt phrasing per angle in Step 4.
2. **User gave a product URL, no copy** → fetch the page. Pull real benefits, features, price/offer details, and any genuine review or testimonial quotes.
3. **User gave only a name/photo/notes, no URL or copy** → do a web search on the product/brand. Look for real claims, reviews, ratings, and how the brand already positions itself.

**Hard rule: never invent a stat, review count, or claim you can't trace to step 1, 2, or 3.** If research turns up nothing usable, write the ads around general, defensible benefit framing instead of fabricating a number — a vague-but-honest ad beats a specific-but-fake one, especially for client work where a made-up "10,000+ reviews" could actually get someone in trouble.

## Step 3 — Get a product image

- **If the user provided a real photo:** use it as the image reference for every generation in Step 4. Pass it to `gpt-image`'s `edit.py` (OpenAI) so the real product renders accurately across all four ads. This is the only case where we use OpenAI editing — preserving product accuracy for real brands is worth the cost.
- **If a product URL was given, try to pull a product photo from that page** before falling back further. If you get a real photo, treat it as above.
- **If there's no photo anywhere:** generate a photoreal product mockup with `gpt-image`'s `generate.py` using `--type product-photoreal`. This routes to the cheapest capable model (FLUX via Together AI, ~$0.04 for 1024×1536). Then use *that* generated image as the visual reference in your prompts for Step 4 — describe the product consistently in each prompt rather than passing the image as an edit reference. Say clearly in the output that the product shot is AI-generated, not a real photo, so no one mistakes it for the real thing later.

## Step 4 — Generate the 4 ad concepts

Always produce exactly four images, one per angle, and always use this angle → visual-pattern mapping. This mapping isn't arbitrary — it's pulled from real ad patterns (see `references/ad-style-patterns.md` for the full detail, example copy, and prompt-construction guidance for each one). Read that file before writing your `gpt-image` prompts; it has the composition specifics you need and won't fit here.

| # | Angle | Visual pattern (short) | Image type for router |
|---|-------|------------------------|----------------------|
| 1 | Problem/solution | Pain-point headline or crossed-out-problem callout over/beside the product | `static-ad-text-heavy` |
| 2 | Benefit/result | Bold headline + centered product shot + 3-5 boxed feature callouts | `static-ad-visual` |
| 3 | Social proof/trust | Testimonial quote card, or star-rating banner + product | `static-ad-text-heavy` |
| 4 | Offer/urgency | CTA banner treatment — cart-urgency or scarcity/offer framing | `static-ad-text-heavy` |

### How to call gpt-image for each angle

**Case A: Real product photo provided (use OpenAI edit for consistency)**

```bash
uv run <SKILL_DIR>/scripts/edit.py \
  --prompt "[Full ad composition prompt describing the scene, text placement, and product position. Include: 'the product from the input image is [product name], place it exactly as described']" \
  --images product_photo.png \
  --size 1024x1536 \
  --output ad-N.png
```

**Case B: No real photo — AI-generated product or concept work**

**IMPORTANT — tested quality findings (2026-09-01):**
- **OpenAI gpt-image-2** is the ONLY model that reliably renders text exactly as specified. Headlines, quotes, CTAs come out correct.
- **Ideogram v2** is cheaper (~$0.03 vs ~$0.06) but makes spacing/casing errors (e.g. "Glow Up" → "glowup"). Acceptable for drafts, not for final client deliverables.
- **FLUX (inference.sh/Together)** has excellent photorealism but cannot render readable text at all. Brand names become gibberish (e.g. "SUIORRIN"). Use ONLY for visuals with NO text.

**For angles with headlines/CTAs/quotes (1, 3, 4) — text accuracy matters:**
```bash
# FINAL deliverables — use OpenAI (text is accurate)
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "[Full ad composition prompt. Include headline text in quotes: 'reads exactly: \"...\"']" \
  --type static-ad-text-heavy \
  --budget premium \
  --size 1024x1536 \
  --output ad-N.png
```
*Routes to OpenAI gpt-image-2 (~$0.06/image). Text will be correct.*

```bash
# DRAFTS / internal review — use Ideogram (cheaper, acceptable errors)
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "[Same prompt]" \
  --type static-ad-text-heavy \
  --budget budget \
  --size 1024x1536 \
  --output ad-N-draft.png
```
*Routes to Ideogram v2 (~$0.03/image). Check text before posting.*

**For the visual-heavy angle (2) — no text, photorealism matters:**
```bash
uv run <SKILL_DIR>/scripts/generate.py \
  --prompt "[Full ad composition prompt. Product description: a [color] [material] bottle of [product name]... NO text, NO words, NO typography]" \
  --type static-ad-visual \
  --size 1024x1536 \
  --output ad-N.png
```
*Routes to FLUX via inference.sh or Together AI (~$0.03–0.04/image). Excellent photorealism, no text needed.*

### Prompt quality guidelines

- Size is always `1024x1536` (portrait — reads well on both LinkedIn and X, safer default for feed/story placement).
- **For text-heavy angles:** always quote the exact text you want: `reads exactly: "SALE 50% OFF"`. Be explicit about font style, size, and placement.
- **For visual angles:** explicitly forbid text in the prompt: `NO text, NO words, NO typography, NO letters anywhere.` This prevents FLUX from generating garbled brand names.
- Build the prompt from: the visual pattern spec in `references/ad-style-patterns.md`, the sourced copy from Step 2 (real claims/quotes, or general framing if nothing traceable was found), and the brand/product name. Follow gpt-image's own prompting structure (background/scene → subject → key details → constraints).
- Output each to `outputs/static-ads/{slug}_{date}/ad-1-problem-solution.png` (and so on for ad-2 through ad-4), where `{slug}` is a brand+product slug (e.g. `alchemind_mushroom-blend`) and `{date}` is `YYYYMMDD`.

## Step 5 — Assemble the showcase and captions

- **Combined LinkedIn showcase:** composite the 4 individual images into a single 2x2 grid image (`combined-showcase.png`) sized `1024x1024`. Use `gpt-image`'s `edit.py` with all 4 images as input references and a compositing prompt, or assemble programmatically if a simple grid is all that's needed — pick whichever gets a clean result faster. For a simple grid, `Pillow` (Python PIL) is usually faster and more reliable than an AI compositing call.
- **X assets:** the 4 portrait images work fine posted directly on X as-is; don't over-engineer a second render unless the user specifically wants a landscape crop. If they do, generate that separately rather than blocking the rest of the run on it.
- **LinkedIn caption:** one caption that walks through the concept — what product, what 4 angles, and a line of positioning (Ridwan's/Koolestpro's or the client's expertise). Should read like someone showing their work, not like ad copy about ad copy.
- **X posts: one per image, five in total, each written for the image it posts with (rule since 2026-09-28).** Every X post goes out as a single image, so its caption must describe only what is in that one image. Open each PNG and look at it before writing its caption.
  - `ad-1` problem/solution: the worry or problem the ad leads with.
  - `ad-2` benefit/result: the outcome the ad promises.
  - `ad-3` social proof: the real review, rating or quote shown in that ad.
  - `ad-4` offer/urgency: the offer the ad makes.
  - `combined-showcase`: the only post that may talk about all four ("4 ad directions from one product...").
  Never write "four ads", "swipe", "carousel" or "these ads" in the caption for a single ad. In `index.html`, mark each post with the image it belongs to: `<div class="x-post" data-asset="ad-1">...</div>` (and `ad-2`, `ad-3`, `ad-4`, `combined-showcase`). `harvest_content.py` reads `data-asset`; a post without it is not scheduled on any single-image slot. Put no character count inside the `.x-post` div (it used to be read as part of the tweet).
- **Instagram single caption:** one more caption for the single-image Instagram post, which shows `ad-1` alone. It sits in its own copy-block titled `Instagram Single`, not the LinkedIn caption, because the LinkedIn one walks through all four ads.
- **Run every piece of caption/copy text through the humanizer skill before treating it as final.** This isn't optional — it's a standing project rule, and AI-flavored copy is exactly the kind of thing that undermines an ad's credibility.

## Step 6 — Write the output, following Step 0's routing decision

Everything lands in whatever folder Step 0 resolved (a project's own "Static Ad Image — Export Routing" section, or the `./static-ad-output/{slug}_{date}/` default):
- `ad-1-problem-solution.png`, `ad-2-benefit-result.png`, `ad-3-social-proof.png`, `ad-4-offer-urgency.png`
- `combined-showcase.png`
- `index.html` — a plain review page (not an html2canvas capture target, just clean HTML) showing all 4 images + the combined showcase + the LinkedIn caption + the Instagram Single caption + the five X posts (each tagged with `data-asset` and shown next to its image), laid out for a quick eyeball review.

**If Step 0 found a routing section with a pipeline-registration step described** (as it currently does in `koolestpro-cowork-v2`: reuse the exact "PIPELINE EXPORT BUTTON" pattern from that project's `CLAUDE.md`, export a JSON matching its JSON Standard with `type` set to whatever value that project's routing section specifies, and if a rotation-tracking file like `targets_pool.json` is part of that project's convention, update it the same way) — follow it exactly, using the constants and schema *that project* defines, not a hardcoded assumption.

**If Step 0 found no routing section:** just deliver the files above with a plain, generic JSON sidecar (`{slug}_{date}.json`: brand, slug, title, created timestamp, folder — no invented `type` enum or registration claim), and tell the user there's no pipeline to register it in yet.

## Brand safety (client / real-brand work)

If the product belongs to a real brand that isn't an actual paying client, frame the output as an unofficial concept — don't let the copy or caption imply the brand commissioned or endorsed it. If it *is* an actual client, say so plainly instead of hedging. This matches the brand-safety rules already in place elsewhere in this project for CRO concept work — don't relax them just because this skill produces images instead of a rebuilt page.

## Edge cases

- **Given copy conflicts with what research finds:** trust the given copy — the user supplied it on purpose. Note the discrepancy to the user rather than silently overriding it.
- **Product is genuinely obscure / nothing findable:** fall back to general benefit framing built from the product notes alone. Say so rather than presenting thin research as if it were thorough.
- **URL fetch is blocked or fails:** fall back to a web search on the brand/product name instead of stalling the whole run.
- **No product image anywhere:** generate one (Step 3) — don't refuse.
- **Run without a specific product (scheduled/unattended context):** pull from `targets_pool.json` per Step 1; if that's empty too, use Koolestpro sample work rather than failing the scheduled run.
- **No text-heavy provider configured (e.g. no Ideogram key):** the router will fall back to OpenAI for text-heavy angles. This still works, it just costs more. The skill doesn't need to handle this specially — the router's fallback logic covers it.

## Cost comparison (old vs. new) — TESTED 2026-09-01

**Reality check:** OpenAI is still the best for text accuracy. The cheaper alternatives make errors.

| Scenario | Old (OpenAI only) | New (routed, honest) | Savings |
|----------|-------------------|----------------------|---------|
| 4 ads FINAL quality (concept work) | ~$0.24 | ~$0.21 | **12%** |
| 4 ads DRAFT quality (internal review) | ~$0.24 | ~$0.12 | **50%** |
| 4 ads, real photo (client work) | ~$0.24 | ~$0.24 | 0%* |
| 1 product mockup, no text | ~$0.06 | ~$0.03 | **50%** |

\* Real photos still use OpenAI editing for product consistency.

**Where the savings actually come from:**
- **3 text-heavy angles** (Problem, Social Proof, Offer): Still need OpenAI for correct text (~$0.06 each). Ideogram is cheaper (~$0.03) but "Glow Up" becomes "glowup" — unacceptable for client work.
- **1 visual angle** (Benefit/Result): Can use FLUX via inference.sh (~$0.03) since it has minimal text. Excellent photorealism, no garbled brand names to worry about.

**Draft vs. Final strategy:**
- **Drafts:** Use Ideogram for all 4 angles (~$0.12 total). Fast, cheap, good enough to review layout/concept. Text may have minor errors.
- **Finals:** Use OpenAI for text-heavy angles 1/3/4 (~$0.18), FLUX for visual angle 2 (~$0.03). Total ~$0.21. Text is correct.

## Provider reference for this skill — TESTED

| Ad angle | Best choice | Why | Cost | Text quality |
|----------|-------------|-----|------|-------------|
| Problem/Solution (text-heavy) | **OpenAI gpt-image-2** | Only reliable text accuracy | ~$0.06 | ✅ Correct |
| Benefit/Result (visual, no text) | **inference.sh FLUX** | Best photorealism, uses existing credit | ~$0.03 | N/A (no text) |
| Social Proof (text-heavy) | **OpenAI gpt-image-2** | Quote text must be exact | ~$0.06 | ✅ Correct |
| Offer/Urgency (text-heavy) | **OpenAI gpt-image-2** | CTA must be legible | ~$0.06 | ✅ Correct |
| Drafts (all angles) | **Ideogram v2** | Cheap, fast, minor text errors OK | ~$0.03 | ⚠️ Check before posting |
| Real product photo → all 4 | **OpenAI gpt-image-2 edit** | Only reliable multi-image editing | ~$0.06 | ✅ Correct |
| Combined showcase grid | **Pillow/PIL** (local) | Faster and free | $0 | N/A |

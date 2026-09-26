---
name: static-ad-image
description: "Generate a set of polished, photoreal static ad/promo images (single images, not carousels) for a product or brand — for Koolestpro's own content pipeline or for real paid client CRO work. Produces exactly 4 ad concepts (problem/solution, benefit/result, social proof/trust, offer/urgency), a combined LinkedIn showcase, X-ready assets, and captions, then exports the result into this project's local JSON content pipeline. Use this whenever the user asks to make a static ad, product ad image, ad creative, promo image, ad showcase, or \"static ad\" for any product — whether they hand over finished copy, just a product URL or photo, or nothing but a product name. Also use for CRO/client deliverables that call for single-image ad creative instead of a carousel. Do not confuse with carousel/slide skills (koolestpro-content-engine, koolestpro-cro-content-maker-skill-e) — this skill is for standalone static ad images specifically."
---

# Static Ad Image

Turn a product — real or hypothetical, Koolestpro's own or a client's — into a set of four ready-to-post static ad images, plus a LinkedIn showcase, X assets, and captions. This is the execution engine for Step 4 ("Weekly Static Ad Image Showcase") of `docs/koolestpro-content-operating-plan.md`, but it's written to be general-purpose: the same flow works for one-off client deliverables, not just the weekly koolestpro cadence.

This skill is the strategy/orchestration layer. It does not call the OpenAI API directly — it delegates every actual pixel render to the **gpt-image** skill, and runs every piece of finished copy through the **humanizer** skill before treating it as final. If either of those skills isn't available, stop and say so rather than improvising a substitute. **By default this skill does not render images at all — it exports a prompt pack (Step 4b).** Rendering through gpt-image only happens when the user asks for it in that request.

## Default mode: prompt pack (the user renders the images)

Image generation was the biggest API cost in this workflow, so the default flipped (2026-09-18):

- **Default (no explicit ask):** run Steps 0-3 (routing, target, research, product photo lookup), write the four ad prompts, write and humanize the captions, then deliver the **prompt pack** described in Step 4b. The user runs the prompts in ChatGPT (or any image tool) and sends the images back; ingest them with "Ingesting manually-produced images". No image API call, no spend.
- **Render mode (only on request):** when the user says something like "generate the images", "render them", "use the API", or "use gpt-image" for this run, follow Step 4 and call gpt-image. If gpt-image then turns out to have no credits, drop back to the prompt pack.
- **Scheduled/unattended runs are always prompt-pack runs.** Nobody asked for rendering, so nothing gets rendered.

The pack is a finished deliverable in its own right, not a failure notice. Its opening explains that this is the default mode, not a billing wall.

## Why the process is structured this way

Cheap AI ad generators produce generic-looking output because they skip two things: they don't ground the copy in anything real about the product, and they use one visual template for every message. This skill fixes both — copy always traces back to something real (given copy, the product's own page, or research), and each of the four ad angles gets its own visual grammar borrowed from real DTC ad creative, not a single reused template with swapped text.

## Step 0 — Find out where output belongs (always do this first)

This skill is portable — it gets installed once and used across any project, so it never assumes it knows where to save things or what pipeline schema (if any) a project uses. Look at the current project's `CLAUDE.md` (already loaded into context automatically — no need to search for it) for a section called **"Static Ad Image — Export Routing"**. It will say where files go and what pipeline/JSON registration step (if any) to follow.

- If that section exists, follow it exactly — including whatever `type` value or registration mechanism it specifies. Don't assume the type is called `"Static Ad"` or that a `ridwan_content_system_updated.html`-style JSON pipeline exists elsewhere; that's this one project's convention, not a universal one.
- If it doesn't exist in the current project, default to `./static-ad-output/{slug}_{date}/` in the current project, skip any pipeline-JSON-export step (there's nothing documented to export *to*), and tell the user plainly: the images/captions/index.html still get delivered, just without a registration step, since none was described.

## Step 1 — Figure out what you're working with

Gather whatever the user gave you: a product URL, a product photo, product notes, ready-made copy, and/or a brand/client name.

- If no brand/client name is given, default to **Koolestpro** and treat this as portfolio/sample work.
- If this is real client work, treat it as a concept/portfolio piece unless the user says otherwise — don't imply the brand officially commissioned it (see Brand Safety below).
- If you were invoked with no specific product at all (e.g. from a scheduled task), check whether the current project has a `targets_pool.json`-style rotation file (this is a `koolestpro-cowork-v2` convention, not universal — Step 0's routing section will say if a given project has an equivalent). If it exists, pick a target with `status: "Available"` whose `usedFor` array has no entry with `stream: "static-ad"`, preferring `visualPotential: "High"` and category variety against recent history. If no such file exists in the current project, fall back to whatever sample/portfolio product makes sense for that project instead of stalling.

## Step 2 — Source the copy (decide automatically, in this order)

1. **User gave copy** (headlines, bullets, claims) → use it verbatim as your messaging source. Don't rewrite the substance, just adapt phrasing per angle in Step 4.
2. **User gave a product URL, no copy** → fetch the page. Pull real benefits, features, price/offer details, and any genuine review or testimonial quotes.
3. **User gave only a name/photo/notes, no URL or copy** → do a web search on the product/brand. Look for real claims, reviews, ratings, and how the brand already positions itself.

**Hard rule: never invent a stat, review count, or claim you can't trace to step 1, 2, or 3.** If research turns up nothing usable, write the ads around general, defensible benefit framing instead of fabricating a number — a vague-but-honest ad beats a specific-but-fake one, especially for client work where a made-up "10,000+ reviews" could actually get someone in trouble.

## Step 3 — Get a product image

- If the user provided a real photo, use it as the image reference for every generation in Step 4 (pass it to `gpt-image`'s `edit.py` so the real product renders accurately, not a reinterpretation).
- If a product URL was given, try to pull a product photo from that page before falling back further.
- If there's no photo anywhere, don't stop and ask. In render mode, generate a photoreal product mockup with `gpt-image`'s `generate.py` from the product description/notes, then use *that* generated image as the reference for the rest of the run. In prompt-pack mode (the default), add a fifth prompt to the pack for the product mockup, and tell the user to generate it first and attach it as the reference when running the four ad prompts. Say clearly in the output that the product shot is AI-generated, not a real photo, so no one mistakes it for the real thing later.

## Step 4 — Generate the 4 ad concepts (render mode only)

This step runs only when the user asked for rendering (see "Default mode"). In the default mode, write the same four prompts exactly as described here, but put them in the Step 4b pack instead of calling gpt-image.

Always produce exactly four images, one per angle, and always use this angle → visual-pattern mapping. This mapping isn't arbitrary — it's pulled from real ad patterns (see `references/ad-style-patterns.md` for the full detail, example copy, and prompt-construction guidance for each one). Read that file before writing your `gpt-image` prompts; it has the composition specifics you need and won't fit here.

| # | Angle | Visual pattern (short) |
|---|-------|------------------------|
| 1 | Problem/solution | Pain-point headline or crossed-out-problem callout over/beside the product |
| 2 | Benefit/result | Bold headline + centered product shot + 3-5 boxed feature callouts |
| 3 | Social proof/trust | Testimonial quote card, or star-rating banner + product |
| 4 | Offer/urgency | CTA banner treatment — cart-urgency or scarcity/offer framing |

For each of the 4, call `gpt-image`:
- Use `edit.py` with the product image (real or generated) from Step 3 as the reference when you have one, so the product itself stays consistent across all four ads. `generate.py` from a rich scene description is fine when there is no reference photo.
- Size `1024x1536` (portrait — reads well on both LinkedIn and X, and is the safer default for feed/story placement).
- **One gpt-image call per shell command.** Four ads means four separate commands. Sandbox command ceilings kill long-running calls, and batching all four into one command means a single timeout loses the whole set.
- **Quality:** check the host project's routing section for a measured setting before choosing. In `koolestpro-cowork-v2`, `low` is mandatory and `medium` is banned — measured there, `medium` always exceeds the command ceiling while `low` finishes in 21-30s and still renders headlines spelled correctly. Don't reason from "text overlay needs high quality" in the abstract when a project has real timing data.
- Build the prompt from: the visual pattern spec in the reference file, the sourced copy from Step 2 (real claims/quotes, or general framing if nothing traceable was found), and the brand/product name. Follow gpt-image's own prompting structure (background/scene → subject → key details → constraints).
- **Put the headline, subline, badge and button text in the prompt itself**, quoted with "reading exactly:", so the model renders the text into the photograph. Full-bleed image, text sitting on the photo.
- Output each to `outputs/static-ads/{slug}_{date}/ad-1-problem-solution.png` (and so on for ad-2 through ad-4), where `{slug}` is a brand+product slug (e.g. `alchemind_mushroom-blend`) and `{date}` is `YYYYMMDD`.

### Never let PIL draw ad copy

PIL/Pillow's only permitted use in this skill is assembling the combined showcase grid from four finished ads. It must never draw a headline, subline, badge or button.

This rule exists because a real run (2026-07-17, Bebemoss) hit repeated generation timeouts, quietly fell back to compositing the text itself, and shipped four images that read as caption cards: a cream text panel stacked above a photo with the headline set in a default system font. The client rejected them. The failure was not the timeout, it was the silent downgrade — an artifact that looks finished but isn't.

So: if a generation times out, re-run that one command. If something genuinely cannot be produced, say so plainly in the summary rather than shipping a lesser artifact.

**Read every generated PNG back before calling the run done.** Confirm the headline is spelled correctly and the image reads as an ad rather than a caption card. Looking at the files is the check; a successful exit code is not.

## Step 4b — The prompt pack (default mode, and the fallback when gpt-image has no credits)

This is the default output of every run that did not ask for rendering. It is also where a render-mode run lands if gpt-image returns a `429` with `insufficient_quota` / `credit_balance_exhausted`: that is a billing wall, not a bug. Don't retry it, don't hunt for another key, and above all don't fall back to compositing.

**Hand the user a prompt pack.** Do not silently spend on a different paid image service to route around it. Alternative generators tend to be either exhausted too or unverifiable before they bill, and quietly moving a run onto a different paid service is not a decision this skill gets to make. Only use an alternative generator if the user names one for that run.

Write a pending file (in `koolestpro-cowork-v2` that's `.ai-workflow/pending-static-ad-{slug}.md`; elsewhere, alongside the output folder) containing everything the run already earned, so the manual step is pure copy-paste and nothing needs re-researching:

1. **Why it's a pack** — "default prompt-pack mode", or, on a render-mode run that hit a wall, the actual error string and which keys were tried.
2. **Target/product selection and the reasoning behind it**, so a later run doesn't re-litigate it.
3. **The research table** — every real, traceable claim with its source. This is the expensive part of the run; never let it evaporate.
4. **The four prompts, verbatim and copy-paste ready.** One fenced block per image, each fully self-contained, with no CLI flags inside the block. State the intended size and filename above each block. Keep the "reading exactly:" quoting so the text renders into the photograph rather than producing a caption card, and keep the constraint line that forbids a separate text panel.
5. **The captions**, already humanizer-checked, so the return trip is images only.
6. **A "still to do on return" checklist** with the exact pipeline constants and social-content keys.

Then present the file to the user so they can act on it immediately.

**Register nothing until the images exist.** No pipeline record, no rotation-file `usedFor` entry, no social-content library, and delete the empty output folder so later rotation logic doesn't mistake it for a shipped package. Most projects already forbid pipeline entries whose folder path has no real file; this is that rule, not a special case. On unattended scheduled runs this is the entire expected behaviour: bank the pack, register nothing, and say plainly that the pack is waiting for the user's images.

### Ingesting manually-produced images

When the user returns the exports, resume from the pending file as the brief:

1. Save the images into the real output folder under the exact filenames the pack specified. Chat attachments land in an uploads directory — copy them across rather than leaving deliverables pointing at an upload path.
2. **Look at every image before accepting it.** Same bar as a generated run: spelling, reads-as-an-ad, product renders sensibly. A human having made it does not exempt it from review. If one is wrong, hand back a revised prompt for that single image rather than shipping the set.
3. Assemble the combined showcase and run the X size check (Step 5).
4. Build `index.html` and register everything the blocked run skipped.
5. Present the finished review page, then delete the pending file — a stale one will confuse a future run.

Note in the pipeline record and the social-content file that the images were produced manually rather than through the API. Provenance, not a quality caveat.

## Step 5 — Assemble the showcase and captions

- **Combined showcase (`combined-showcase.png`):** composite the 4 individual images into a single 2x2 grid image sized `1024x1024`. Assemble programmatically with PIL (grid assembly is the one thing PIL is for here) or via `gpt-image`'s `edit.py` with all 4 as references — whichever gets a clean result faster. This is the primary asset for LinkedIn/Instagram, and it's also the **preferred, default image for the X "summary" post**.
- **X assets — combo is the default for the "summary" X post, but it must pass a size check first:** the X post whose caption talks about all 4 angles together should use `combined-showcase.png`. Angle-specific X posts should use that angle's own individual image. **Before assigning `combined-showcase.png` to any X entry, check its actual file size.** At or under ~4MB, use it as-is. Over ~4MB, generate a compressed variant — same content, downscaled and/or PNG-optimized until comfortably under 4MB (a 40-60% linear resize is usually enough and stays crisp at feed resolution). Save it as `combined-showcase-x.png` and point the X entry at that. Never point an X entry at a combo file you haven't size-checked.
- **LinkedIn caption:** one caption that walks through the concept — what product, what 4 angles, and a line of positioning. Should read like someone showing their work, not like ad copy about ad copy.
- **X posts:** 2-3 short proof-of-work style posts in the project's voice. The summary one gets the size-checked combo; angle-specific ones get their matching individual image.
- **Run every piece of caption/copy text through the humanizer skill before treating it as final.** Not optional. Also check the host project's own copy rules — many forbid em dashes outright, require real line breaks rather than markdown literals, and split hashtag conventions by platform.

### Confirmed bug — combo image broke X posting via file size, not via being the wrong image

A first pass at this bug wrongly concluded X should never use `combined-showcase.png` and banned it outright. That overcorrected. The real, narrower bug was that one brand's combo had drifted from the `1024x1024` spec to 2132x3156 / 8.33MB, tripping a `MaxFileSizeExceededError` in the downstream posting pipeline. A different brand's combo, at 3.47MB, worked fine.

The durable fix is the size check, not an image-choice rule. Combo is fine and preferred for the X summary post; the only hard requirement is that whatever file gets assigned to an X entry has been checked against ~4MB, with a compressed `-x` variant generated on the spot if it doesn't clear. Both failure modes count: assigning an unchecked combo, and reflexively avoiding the combo for X.

## Step 6 — Write the output, following Step 0's routing decision

Everything lands in whatever folder Step 0 resolved:
- `ad-1-problem-solution.png`, `ad-2-benefit-result.png`, `ad-3-social-proof.png`, `ad-4-offer-urgency.png`
- `combined-showcase.png` (full resolution, for LinkedIn/Instagram and as the source for the X variant)
- `combined-showcase-x.png` (only if the full-resolution combo exceeded ~4MB)
- `index.html` — a plain review page (not an html2canvas capture target, just clean HTML) showing all 4 images + the combined showcase + the LinkedIn caption + the X posts, laid out for a quick eyeball review.

Leave nothing else behind: no throwaway build scripts, no intermediate base/scene images.

Before treating the run as done, do a final pass over every asset path assigned to an X entry and confirm it points at a real file under ~4MB.

**If Step 0 found a routing section with a pipeline-registration step described** — follow it exactly, using the constants and schema *that project* defines, not a hardcoded assumption. If a rotation-tracking file like `targets_pool.json` is part of that project's convention, update it the same way.

**If Step 0 found no routing section:** deliver the files above with a plain JSON sidecar (`{slug}_{date}.json`: brand, slug, title, created timestamp, folder — no invented `type` enum or registration claim), and tell the user there's no pipeline to register it in yet.

## Brand safety (client / real-brand work)

If the product belongs to a real brand that isn't an actual paying client, frame the output as an unofficial concept — don't let the copy or caption imply the brand commissioned or endorsed it. If it *is* an actual client, say so plainly instead of hedging.

## Edge cases

- **Given copy conflicts with what research finds:** trust the given copy — the user supplied it on purpose. Note the discrepancy rather than silently overriding it.
- **Product is genuinely obscure / nothing findable:** fall back to general benefit framing built from the product notes alone. Say so rather than presenting thin research as if it were thorough.
- **URL fetch is blocked or fails:** fall back to a web search on the brand/product name instead of stalling the whole run.
- **No product image anywhere:** generate one (Step 3) — don't refuse.
- **No explicit request to render:** Step 4b prompt pack (the default). Register nothing until images come back.
- **gpt-image out of credits in render mode:** Step 4b prompt pack, register nothing.
- **A generation times out:** re-run that one command. Never composite instead.
- **Run without a specific product (scheduled/unattended context):** pull from the project's rotation file per Step 1; if that's empty too, use the project's own sample/portfolio work rather than failing the run.
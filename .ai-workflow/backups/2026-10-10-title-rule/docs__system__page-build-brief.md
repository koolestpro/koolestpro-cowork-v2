# Page build briefs (the Lovable / Figma Make input side) 2026-09-13

Lovable, Figma Make, v0, Bolt and Onlook **do not read this repo**. A rebuild starts by handing
them a brief. That brief is the input half of the handoff; `.ai-workflow/tools/capture_page.py` is
the output half. Together they close the loop.

## The loop

1. **Facts.** Write `outputs/cro-fixes/<slug>_facts.json`: brand, page, url, surface, audience,
   job, `facts`, `verify`, `headline_options`, `benefits`, `assurances`, `assets`, `sections`,
   `avoid`. Real facts only.
2. **Brief.** `python3 .ai-workflow/tools/build_page_brief.py --facts <facts.json> --out <slug>_build-brief.md`
3. **Build.** Paste the brief into Lovable (or Figma Make). Upload the assets it lists.
4. **Publish.**
5. **Capture.** `python3 .ai-workflow/tools/capture_page.py --url <published-url> --brand <brand> --device both --full`
6. **Compose.** Feed the mobile shot into `build_device_still.py`, the carousel builder, or the recap.

## What every brief must carry (the redesign standard, stated in the prompt)

- The **one job** of the page.
- An **Image decision** block, before the build: plan first, use a great site photo if one exists,
  otherwise generate one with AI and build on that. Product pages and homepages alike. (Standing
  rule 15.)
- **Real facts only**, with an explicit verify list. Never invent a number, quote, or guarantee.
- The **first screen carries the whole decision**: outcome headline, price, rating and review count,
  benefit reasons, a trust row, and the CTA.
- The **real logo and product image** used as-is, never recreated or cropped.
- **No gradient text.**
- **Sections top to bottom**, so the tool does not have to guess the structure.
- An explicit **do-not** list (this is where the audit findings live, so the rebuild does not repeat
  the mistakes it is fixing).

## Why a brief and not a saved project

A brief is portable. The same brief can go to Lovable today, Figma Make tomorrow, or the fallback
flow, and the rules travel with it. The output side is a screenshot, so there is no lock-in either
way.

## Fallback flow

If no external tool is available, the same brief is the spec for this agent to author the page HTML
directly, then capture and compose. Lower ceiling on the hero visual, but always available.

## The product image step (do not skip)

Before the captured page is used in a post, the hero product image must survive phone size. For
Caraway this is the known blocker (see `rebuild-tooling-and-quality.md`). Regenerate or cut out the
image, place it on a contrasting surface, then check it at 390x844.

## Worked example

- Facts: `outputs/cro-fixes/caraway_fry-pan-pdp_facts.json`
- Brief: `outputs/cro-fixes/caraway_fry-pan-pdp_build-brief.md`

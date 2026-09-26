# Rebuild tooling and the freedom-plus-guardrails model (2026-09-13)

Ridwan's call: **freedom for the page design, guardrails for the quality.** Not a template for
every case.

## Why freedom, not a template library

A "template for every situation" makes every rebuild look the same and undercuts the whole pitch,
which is "this is genuinely your page, improved." What should repeat is the **quality bar** and a
small **component vocabulary**, not the layout. Same parts, different pages.

## The guardrails (what stays fixed)

1. **`docs/system/cro-redesign-standard.md`** - the 10 dimensions, the 1-5 rubric, the checklist.
   Every rebuild is scored against it. The first screen must carry the whole decision.
2. **A component kit** (to build next): hero with an outcome headline, proof row, benefit chips,
   trust row, sticky add-to-cart, comparison table, review card. Plain HTML/CSS patterns the
   builder composes from. Consistency without sameness.
3. **The done gate:** export the page and look at the first screen. If it does not carry the
   decision by itself, it is not finished.

## Where a redesign gets made (decided 2026-09-13)

Tools, in priority order:

1. **Primary: Lovable and Figma Make.** This is where the finished-page quality lives (GetFit in
   Lovable, Petticoat Fair in Figma Make). Page design stays here.
2. **Alternatives: v0 (Vercel), Bolt.new, Onlook.** Prompt-to-page with free tiers, used if
   Lovable or Figma Make are unavailable.
3. **Fallback: the default flow.** If none of the above is practical, this agent authors the page
   HTML directly, captures it, and composes. Lower ceiling on the hero visual, but always available.

Capabilities, honestly:

| Tool | Good at | Role |
|---|---|---|
| **Lovable** | polished, finished page design | the page itself (GetFit, best performer) |
| **Figma Make** | polished, finished page design | the page itself (Petticoat Fair) |
| **v0 / Bolt.new / Onlook** | prompt-to-page, free tiers | alternatives |
| **Claude Code / Codex** | code-level refinement of an exported project | refine, wire up, QA |
| **This agent (opencode)** | authoring HTML/CSS/JS, compositing mockups, exports, the content system, captions, docs | capture, compose, register, system |

## Integrating Lovable and Figma Make (implemented)

**The handoff is a screenshot, so there is no lock-in.** `.ai-workflow/tools/capture_page.py`
takes a published URL (Lovable publish, Figma Make share, or any live page) or a local export,
and returns the exact assets the pipeline uses, already at the right viewport and scale:

```
python3 .ai-workflow/tools/capture_page.py --url https://my-app.lovable.app --brand getfit --device both --full
python3 .ai-workflow/tools/capture_page.py --file /path/to/dist/index.html --brand getfit --full
```

Output, in `outputs/cro-fixes/_capture/<brand>/`:
- `<brand>-mobile.png` 390x844 @2 (the phone screen, drops into `build_device_still.py`)
- `<brand>-full.png` full page @2 (tall shot for strips / mobile-strip)
- `<brand>-desktop.png` 1440x900 @2 (with `--device desktop` or `both`)

It reuses `screenshot.py`'s popup handling, forces reduced motion, and prints a
`CAPTURE_SUMMARY` JSON line for the next step. Run it with a Python that has Playwright
(the project venv; see `.ai-workflow/tools/README.md`).

If the design came out of a Lovable GitHub export instead, run the same command with `--file`
against the local build.

## The actual quality problem: the product image (decide it after the plan)

The Caraway rebuild reads badly because the product photo is a dark studio shot sitting on a dark
page. The GetFit post (best performer) worked because the product image was **regenerated with AI
and blended into the page**. So the highest-leverage step is not the layout tool. It is the image.

The order matters. **Plan the build first, then decide the image:**

1. Write the plan: what the page is for, its sections, the one job of the first screen.
2. Look for a usable hero photo on the site. If there is a **genuinely great** one, use it.
3. If there is no good photo, or nothing is good enough, **generate a suitable version with AI**
   and build the page on that image.
4. A homepage uses the exact same process as a product page.

Never build first and bolt on a weak image, and never settle for the site's photo just because it
exists. This is standing rule 15, and it is the "Image decision" block in the page build brief
(`docs/system/page-build-brief.md`).

- **Then check it:** place the chosen image on a contrasting plinth, verify the composite at phone
  size (390x844, not desktop size).
- **Tool:** AI generation via gpt-image (blocked on credits as of 2026-09-04) or a manual ChatGPT
  pass by Ridwan.
- **Rule already in force:** background-removed cutouts over raw studio photos, never cropped
  (standing rule 3).

Caraway is dropped from the recap until its image passes this step.

## Working with Claude and Codex at once

- Keep the rules in files both agents read. `CLAUDE.md` is the shared rulebook, and **`AGENTS.md`**
  at the project root points every other agent (Codex, Cursor, opencode) at the same docs and the
  same quality gate, so the tools never drift.
- One source of truth per artifact: the content system HTML (`#cowork-sync-data` JSON), the
  `docs/system/*` specs, the `{brand}-social-content.md`/`.json` pairs. Whoever edits, edits those.

## Recommendation summary

1. Freedom plus the redesign standard plus a small component kit. No template library.
2. Page design stays in **Lovable / Figma Make**; v0 / Bolt.new / Onlook are the alternatives; the
   default flow (this agent authors and captures) is the fallback. This pipeline captures and
   composes.
3. URL capture handoff: **implemented** at `.ai-workflow/tools/capture_page.py`.
4. Make product-image regeneration a named step. That is what fixes Caraway-grade builds.
5. **`AGENTS.md`** added so Claude, Codex and any other agent share the rules.

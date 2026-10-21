# Humanizer Guideline — every written output goes through it

**Rule: no written content is final until it has passed the humanizer.** This covers every
system in the project that produces prose, not just captions. The humanizer skill is the
single, shared writing layer, and this doc is the project's routing for it.

## The skill (source of truth)

Lives outside the repo at `~/.agents/skills/humanizer/` (installed once, shared across
projects):

- `SKILL.md` — routing, non-negotiables, output contract, release gate.
- `VOICE.md` — Ridwan's confirmed voice profile + the project blocklist.
- `references/workflow.md` — the eleven passes in detail.
- `references/patterns.md` — what counts as a quality problem, and the research basis.

It is **not** a detector-evasion tool. The standard is: a reader can follow it, trust the
claims, and recognise a consistent point of view.

## Scope — where it runs

| System | Written output | Where the pass runs |
|---|---|---|
| Content Production | Tips carousel copy, CRO Fix headlines/annotations/Q&A, Static Ad copy | before the HTML is treated as final (see `weekly-pipeline.md`) |
| Build Assets / website copy | page copy, mockups, template text, CTA labels, product descriptions | before the page/mockup is exported |
| Distribution / captions | every LinkedIn / X / Instagram caption in `{brand}-social-content.*` | before it reaches the queue |
| Outbound / KoolestFlow | cold email subject lines, openers, bodies, follow-ups | before a message is sent |
| Web Presence / `site/` | page copy, meta descriptions, service pages | before deploy |
| Case Study / Personal posts | full post copy | before export |
| The content system | item titles and headlines | when authored or edited |

## The eleven passes (use them as lenses, not a ritual)

1. **Writer** — draft from the real brief, audience, format, desired action.
2. **Editor** — cut redundancy, filler, unsupported flourish.
3. **Fact-checker** — protect claims, numbers, dates, quotes, attributions. If a number
   reads wrong (e.g. "dropped from 1.2x to 4.8x" when it rose), fix it.
4. **Anti-AI style** — fix evenly-sized sentences, symmetry, mini-outlines, inflated
   significance, generic conclusions.
5. **Ban AI words** — audit in context (`delve`, `crucial`, `seamless`, `robust`,
   `leverage`, `unlock`, `showcase`, `foster`, `underscore`, `transformative`...). Keep the
   word only if it is the clearest accurate choice.
6. **Ban AI patterns** — false contrast, grand pronouncement, empty opening ("Here's the
   thing"), sweeping claim, vague `-ing` tail, decorative adverb.
7. **Sound like your posts** — anchor in `VOICE.md`: direct practitioner, concrete, short
   first line, first person, plain Nigerian English, no corporate tone.
8. **Humanizer** — real point of view, named actor, concrete nouns and verbs, honest
   uncertainty, natural rhythm. No simulated intimacy or invented detail.
9. **Red pen** — flag vague, inflated, cliche, unsupported, or reader-irrelevant lines.
10. **Self-critique** — one bounded revision against the brief. Then stop.
11. **Auto-block banned words** — the only hard block. The project blocklist:
    `unlock`, `digital journey`, `comprehensive post`, `valuable insights`, `synergize`,
    `holistic`, `conversion excellence`, `it's important to note`, and other generic
    framing. Intentional use: confirm, then retain with a note.

## Mode router (do not over-process short copy)

| Need | Passes |
|---|---|
| New prose | Writer → Editor → Voice match → Safety net |
| Existing prose | Editor → Anti-pattern scan → Humanizer → Safety net |
| Factual / technical | Fact-checker first, then normal |
| A post, caption, ad, or headline | Writer/Editor → Hook + rhythm → Voice match → Safety net |
| Copy inside a graphic or UI | Writer/Editor → Readability/length → Voice match → Safety net |
| Critique only | Red pen; offer fixes only if asked |

## Hard rules (project + skill)

- **No em dashes, anywhere** (project-wide, always). Rewrite as two sentences, a comma, or
  a colon.
- **Caption list markers:** for before/after or positive/negative lists, mark improvements
  with ✅ and missing or negative items with ❌. Do not use `OK` or `X` as substitutes.
- **X captions: hard 280-character limit**, counted on the real string.
- **Never fabricate** a result, quote, number, source, or testimonial. Never imply a
  concept brand (KURA / HALOS / MERIDIAN / Lumora) was a real client.
- **Preserve facts.** Never make a claim more definite during an edit. Mark unknowns.
- **Copy inside a graphic** also passes: spelling, real line breaks (no `\n` literals),
  legibility at the intended size, text density, and whether it still works **standalone**,
  apart from the surrounding prose.
- **One release gate.** Answer the skill's gate: does every sentence earn its place, are
  claims traceable, does the format fit the destination, is any blocked item left?

## Per-stream checklist

| Stream | Extra checks beyond the pipeline |
|---|---|
| CRO Fix | headline from the single #1 finding; Q/A tied to the real element; page type stated; no reuse of last week's line |
| Tips carousel | one idea per slide; headline max 2 lines at the surface size |
| Static Ad | 4 angles genuinely differ; CTA points at a real destination, not engagement |
| Website copy | names the problem, the change, and the evidence; fits the page section length |
| Captions | LinkedIn max 1/day (platform rule, not copy); no hashtags on X; hashtags allowed on LinkedIn/IG |
| Outbound | specific to that business; one clear ask; no invented familiarity |

## Enforcement points (already wired)

- `CLAUDE.md` → "PROJECT-WIDE GENERATED-COPY RULES" (the floor).
- `docs/system/cro-headline-system.md` → full pipeline for every headline.
- `.ai-workflow/weekly-pipeline.md` step 7 → CRO captions/copy.
- `.ai-workflow/tools/harvest_store_template.py` → warns on em dashes before a caption can
  reach the queue.

## Keeping VOICE.md honest

- Update it only from writing Ridwan confirms is his, or explicitly wants as the target
  voice. Add observable choices (point of view, rhythm, vocabulary, structure, CTA habits,
  hard dislikes), never stereotypes.
- When the brief and the samples conflict, **the brief wins** (a UI label is not a personal
  post).
- Record wanted samples: accurate numbers with sources, specific page elements, named
  ecommerce/CRO concepts, direct recommendations grounded in a visible problem.

## Run summary

When a run produces copy, state in the summary that it was humanized, and name any material
change or unresolved factual question. If nothing material changed, say the copy passed
unchanged.

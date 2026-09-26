# CRO Headline System (2026-09-12)

One audit produces several headlines: the cover, the before/after slide, the annotation
slide, the standalone annotated graphic, and the caption opener. Left to a per-run guess
they drift into templated filler ("Every change had a purpose.") or vague claims. This
system makes the headline a **repeatable, derivable output** of the audit.

## The one-finding rule

A headline is not a recap of the work. It is the **strongest true sentence about the single
biggest thing the page got wrong.** Before writing any headline:

1. Open the audit and the rebuild.
2. Rank the changes by impact.
3. Write down the **#1 finding** in one plain sentence (the problem, not the fix).
4. Every headline on every surface is built from that one finding.

If the #1 finding cannot be stated without exaggerating, it is not the #1 finding yet. Keep
digging until it can be said simply and truthfully.

## Step 2: pick an angle

The same finding can be said several ways. Choose the angle that fits the finding, then use
a **different** angle for each surface. Never invent a metric or a result to make an angle
work.

| # | Angle | Shape | Caraway example (finding: price and proof were present but placed where the decision is not made) |
|---|---|---|---|
| 1 | Contrast | `Same ___. Different ___.` | Same pan. Different first impression. |
| 2 | Diagnosis | `___ was never the problem. ___ was.` | Traffic was never the problem. The order of the page was. |
| 3 | Misconception | `More ___ does not convert. ___ does.` | More reviews do not convert. Placing them at the fold does. |
| 4 | Reconnection | `___ and ___, reconnected.` | Price and proof, reconnected. |
| 5 | Reframe | `Great ___ do not ___. They ___.` | Great PDPs do not list features. They guide decisions. |
| 6 | Evidence | `[real number]. [the gap].` | 18,886 reviews. None of them above the fold. |
| 7 | Question frame | `It answers the [N] questions every buyer asks.` | It answers the 3 questions every buyer asks. |
| 8 | Plain stakes | `A ___ that read as ___.` | A $125 pan that read as unsure of itself. |

## Step 3: the headline ladder

Each surface gets one angle on the **same** finding, chosen to fit that surface's job:

| Surface | Job | Best angles |
|---|---|---|
| Cover | the hook | 1, 2, 3, 6, 8 |
| Slide 2 (before/after) | the contrast | 1 |
| Slide 3 (annotation) | the reasoning | 5, 7 |
| Standalone annotated graphic | the question frame | 7 |
| Caption opening line | state the finding plainly | (not a headline: one clear sentence) |

Rule: **if two surfaces say the same thing, one is wasted.** The set should read as hook →
contrast → why → question, not four paraphrases of the same line.

## Hard rules

- **Max 2 lines** at the surface's font size. Check the render, not the markup. Syne 800 is
  wide; shorten before you shrink.
- **No em dashes.** Use a full stop, a comma, or a colon.
- **Run the copy through `humanizer`** before finalising, like every other caption. Use the
  full 11-pass pipeline routed through `VOICE.md` (writer, editor, fact-checker, anti-AI
  style, AI-word check, AI-pattern check, voice match, humanizer, red pen, self-critique,
  final blocklist). Headlines are user-facing prose and are **not** exempt.
- **Never fabricate a result, and never imply a concept brand was a client.**
- **Never reuse last week's headline or its exact structure.** (The contrast shape is
  allowed; the same sentence is not.)
- **No brand name as the headline.** The logo and handle carry the brand; the headline
  carries the idea.
- Headlines are drawn from the rebuild's **top improvements** (same rule as the
  annotations), so the headline and the annotation can never contradict each other.

## Banned (these are template tells)

- Vague value statements: "Every change had a purpose.", "Better UX, better conversions.",
  "Design that converts.", "Small changes, big impact."
- Self-congratulation: "Another CRO win.", "We fixed this page."
- Restating the brand or the page type as the hook.
- Cramming 2-3 findings into one line.
- Anything that would be equally true of any other audit.

## Worked example (Caraway Fry Pan PDP)

**#1 finding:** price ($125) and proof (18,886 reviews) were both on the page, but they sat
where the buying decision is not made, so the page read as unsure of itself.

| Surface | Angle used | Headline |
|---|---|---|
| Cover | 4 Reconnection | Price and proof, reconnected. |
| Slide 2 | 1 Contrast | Same product. Different impression. |
| Slide 3 | 5 Reframe | Every change had a purpose. |
| Annotated graphic | 7 Question frame | How this page answers the questions buyers ask. |

Alternates generated but not used (kept so next run does not repeat the same shapes):
`18,886 reviews. None of them above the fold.` (evidence) /
`Traffic was never the problem. The order of the page was.` (diagnosis) /
`Great PDPs do not list features. They guide decisions.` (reframe).

## Pre-ship checklist

1. Can I name the single #1 finding in one plain sentence? If not, stop.
2. Does every surface use a different angle on that same finding?
3. Is any line 3+ lines, or would it be at another surface's font size?
4. Em dashes removed; `humanizer` run.
5. Would this headline fit a different brand's audit unchanged? If yes, it is too generic.
6. Does the cover headline still make sense with only the phone and the brand logo around it?

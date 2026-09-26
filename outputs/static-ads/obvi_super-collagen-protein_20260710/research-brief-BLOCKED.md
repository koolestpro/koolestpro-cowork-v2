# Obvi Super Collagen Protein — static ad run (2026-07-10) — BLOCKED, not in pipeline

**Status: incomplete.** The gpt-image API key hit `billing_hard_limit_reached` on every attempt (confirmed with two separate calls, different sizes/quality). No ad images were generated this run, so nothing was written to `ridwan_content_system_updated.html` and no files here should be treated as pipeline-ready. This file exists purely so the research/copy work isn't lost.

## Target selected
**Obvi** (`myobvi.com`) — Super Collagen Protein, from `targets_pool.json` (`target-obvi-1751673600012`).

Why: `visualPotential: High`, `status: Available`, no prior `static-ad` usage (this is the first-ever static-ad run, so no rotation history existed yet — Obvi was picked over the other two High/Available candidates, Material Kitchen and Bebemoss, because its quiz + bundle funnel gives more real, sourceable copy to work with). `target-v1ce...` was excluded despite High visual potential because its status is `Used`, not `Available`.

This is unofficial concept work — Obvi has not commissioned or endorsed this content.

## Sourced research (web search, not fabricated)
- 19g protein per serving
- Hydrolyzed grass-fed bovine collagen peptides, types I & III
- Biotin, hyaluronic acid, keratin, vitamin C & E, calcium, iron, magnesium
- Keto-friendly, soy-free, gluten-free, dairy-free, no added sugar, no GMOs
- Reviewers commonly mention: brighter-looking skin, stronger/shinier hair, joints feeling better, visible change around a month of use
- Obvi runs an ongoing Subscribe & Save program (monthly automatic restock)
- Obvi sells a real "Mommy & Me Bundle" (Super Collagen Protein + Kid's Complete Protein)
- No verifiable current discount %, star rating, or review count was found this run — those were deliberately left out of the copy rather than invented (a stale "Easter Sale 15% off" mention turned up but wasn't used since it's out of season and unconfirmed for July)

## Ad copy (humanized, ready to use once images can be generated)
See `obvi-draft-copy-humanized.md`-equivalent content below — angle headlines, callouts, LinkedIn caption, and X posts are drafted and already run through the humanizer pass. Full text:

### Angle 1 — Problem/solution
**"Your skin, hair, and joints are the first to notice when you skip protein."**
Collagen loss isn't only an aging thing. It's also a "you've been under-eating protein for months" thing, and it shows up fast: duller skin, weaker nails, joints that ache more than they used to. One scoop of Obvi Super Collagen Protein covers what a lot of daily diets miss.

### Angle 2 — Benefit/result
**"19g of protein. Real collagen support. One scoop."**
- 19g protein per serving
- Hydrolyzed grass-fed bovine collagen peptides (types I & III)
- Biotin, hyaluronic acid, keratin
- Keto-friendly, gluten-free, dairy-free, no added sugar

### Angle 3 — Social proof/trust
**"Reviewers keep coming back to the same three things."**
- Brighter-looking skin within a few weeks
- Hair described as stronger and shinier
- Joints that feel noticeably better with daily use
(No star rating or review count cited — none could be confirmed this run.)

### Angle 4 — Offer/urgency
**"Never run out. Subscribe & Save, every month."**
Obvi runs an ongoing Subscribe & Save program, so restocks happen automatically instead of you remembering to reorder. (Alt: the real "Mommy & Me Bundle" if a bundle angle is preferred.)

### LinkedIn caption
Four static ad directions for Obvi's Super Collagen Protein: problem/solution, a benefit breakdown, social proof, and a subscribe-and-save offer. Same product, four different reasons someone stops scrolling. This is unofficial concept work built off Obvi's own public product info, not something the brand commissioned.

### X posts
1. Four static ad directions from one product. Same tub, four different hooks.
2. Built these around what Obvi's own reviews keep repeating: skin, hair, joints. A real pattern, not a made-up stat.
3. Subscribe & Save is the most underused angle in supplement ads. Testing it here.

## What still needs to happen
1. Fix the OpenAI billing hard limit on the key in `.claude/skills/gpt-image/.env` (raise the hard limit or top up billing in the OpenAI dashboard).
2. Re-run the static-ad-image skill for Obvi using the copy above as the source material (Steps 3-6 of the skill: base product image → 4 angle edits → combined showcase → `index.html` → pipeline export).
3. Only after real image files exist, register the item in `ridwan_content_system_updated.html` and mark `target-obvi-1751673600012.usedFor` with a `static-ad` entry.

`targets_pool.json` was **not** modified — Obvi is still `status: Available` with no `static-ad` entry in `usedFor`, so it's free to be picked up (by name or by rotation) on the next run.

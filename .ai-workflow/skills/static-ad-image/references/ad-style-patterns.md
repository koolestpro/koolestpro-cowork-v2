# Ad Style Patterns — Angle → Visual Reference

This file exists because the mapping between the 4 ad angles and their visual treatment was worked out by studying ~17 real DTC ad screenshots (Kura, Ankhway, Rise Luxus, Balmbare, Primal Queen, Feastables, Saint Jane, Illumiflow, Shine Labs, Alchemind, and others). Those source images won't be sitting in context on every future run of this skill, so this file carries forward enough visual detail to reconstruct the intended look from description alone. Read the relevant section for whichever angle you're generating before writing its `gpt-image` prompt.

General notes that apply across all four patterns:
- Aim for the production value of a real paid social ad — premium photography or clean studio product shots, not flat vector graphic-design templates.
- Text overlay should be bold, high-contrast, and legible at small sizes (these are feed images — most viewers see them at phone-screen size for under two seconds).
- Background color/mood should suit the product category (warm/earthy for food & wellness, clean/bright for beauty, dark/premium for supplements or tech-adjacent products) rather than defaulting to one house palette — unless the brand already has a defined palette, in which case use that.
- Rounded corners on the overall frame (a soft rounded-square crop) read as "ad card" rather than "raw photo" — most of the reference set uses this.

---

## Angle 1 — Problem/Solution

**Core idea:** name the pain point before showing the fix. Either a direct "here's the annoying thing" callout, or a visual before/after of problems getting solved.

**Two sub-patterns, pick whichever fits the product:**

1. **Pain-point headline over a relevant scene.** A short, punchy, slightly uncomfortable headline sits over an image that visually represents the problem (e.g. a photo of thinning hair for a hair-health product, tangled up in a headline like "My ponytail turned into a rat tail in 3 months" with a small circular inset showing a literal detail — a clogged drain, a hairbrush full of hair). The product appears smaller, usually bottom-center or as a held object, positioned as the answer that follows the headline, not the hero of the frame.
2. **Crossed-out problem list / stat grid.** A headline like "Cancel Boring Snacks" with the word "boring" or the problem struck through, surrounded by a small grid of problem bullets (each with a sad/frustrated icon or a small headshot) transitioning into solution bullets (checkmarks, a "SOLUTION" label, product shot). Works well when the product solves several small annoyances at once rather than one big one.

**Copy tone:** conversational, slightly blunt, first-person or direct-address ("you"). Avoid corporate phrasing — this angle works because it sounds like a real complaint, not marketing copy.

**Prompt-building tip:** describe the emotional register explicitly ("mildly exasperated," "relatable frustration") — gpt-image renders mood better when named directly rather than implied through composition alone.

---

## Angle 2 — Benefit/Result

**Core idea:** hero product shot, clean and centered, with the concrete benefits labeled directly on or around it. This is the most "product photography" of the four angles.

**Composition:** product centered or slightly off-center against a simple, well-lit background (studio backdrop, a styled countertop/table scene, or a softly blurred lifestyle setting). 3-5 short benefit callouts surround the product — either as small rounded-rectangle "chips" with a leader line pointing at the relevant part of the product (e.g. "SPF 50" pointing at a sunscreen bottle's label, "Sweat & Heat Proof" pointing at the cap), or as a row of icon+label pairs sitting below the product shot (a lightning bolt icon + "Real Clean Energy," a leaf icon + "Gut Health"). A short bold headline sits above, stating the core promise in one line.

**Copy tone:** confident, specific, feature-forward. Benefits should be concrete and checkable ("Non-porous," "Wipes clean in seconds") rather than vague ("amazing quality").

**Prompt-building tip:** if using the leader-line/chip style, explicitly instruct "thin line connecting each label to its corresponding part of the product" — without that instruction gpt-image tends to just scatter the labels nearby without the connective visual logic.

---

## Angle 3 — Social Proof/Trust

**Core idea:** let someone else's voice (a customer, a rating) carry the credibility instead of the brand's own claim.

**Two sub-patterns:**

1. **Testimonial quote card.** A real (or research-sourced) customer quote rendered as the dominant headline text, in a slightly more editorial/quote-like typographic treatment (often italic or a serif accent), attributed with a first name + star rating underneath. The product appears smaller — held by a model in a lifestyle scene, or set beside the quote in a simpler layout. Works especially well when the quote itself is specific and slightly surprising ("My Husband Started Asking if I Was Taking Cooking Classes") rather than generic ("Great product!").
2. **Rating/review-count banner.** A star rating + review count sits prominently near the top ("★★★★★ Rated 4.9/5 from 9,200+ home cooks" or "Trusted by 30,000+ Daily Users"), with the product shot centered below and a supporting testimonial or feature line underneath. This sub-pattern works better when you have a real aggregate number to cite rather than one specific quote.

**Hard constraint:** the quote and the number must come from Step 2's research or the user's given copy. If nothing traceable was found, use this angle's *structure* with a de-specified version (e.g. "loved by home cooks" instead of a fabricated count) rather than inventing a number — a fake review count is the single most damaging thing this skill could produce for a real client.

**Prompt-building tip:** specify realistic, warm lifestyle lighting for the model/scene half of the frame if a testimonial sub-pattern is used — the reference set's best examples read as candid-but-polished, not stock-photo stiff.

---

## Angle 4 — Offer/Urgency

**Core idea:** give the viewer a reason to act right now, via either cart-abandonment framing or a scarcity/promotional banner.

**Two sub-patterns:**

1. **Cart-urgency callback.** Frames the ad as if it's retargeting someone who already looked at the product: a headline like "Still Thinking About It?" paired with a small badge-style element ("Your cart is waiting") and a clear CTA bar/button ("Complete Your Order →"). The product is shown large and clean, often at an angle, like it's sitting on the checkout page. A row of trust badges (free shipping, returns, secure checkout, guarantee) sits along the bottom.
2. **Scarcity/offer banner.** A bold offer banner across the top or bottom of the frame in a contrasting color block ("BOGO Sale Ends Soon," "Free Shipping Ends Friday"), with the product shown in its normal best-light presentation above/below the banner and 2-3 short feature callouts nearby (in rounded-rectangle outline chips, not filled — this sub-pattern tends to use outlined labels rather than the filled chips of Angle 2).

**Copy tone:** direct and time-bound. Real urgency (an actual offer, a real deadline) beats manufactured urgency — if there's no real offer to reference, frame this angle around a real reason to act now (e.g. a genuine seasonal relevance) rather than inventing a fake countdown.

**Prompt-building tip:** name the CTA bar's color explicitly and make sure it contrasts hard against the background — this is the one element in the whole ad that must be impossible to miss, so under-specifying its prominence in the prompt is the most common way this angle comes out flat.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KOOLESTPRO CRO AUDIT BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STORE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Store URL: https://www.gainful.com/pages/customize-your-protein
Store Name: Gainful
Page Type: Landing / configurator page ("Customize Your Protein Powder")
Product Name: Personalized protein powder. On the captured configuration the recommended
  formula was "Lean Whey Protein" (defaults: Dietary Preference = None, Primary Goal =
  Lose Weight).
Product Price (real, read off the live page 2026-08-23): "14 Servings | $31.47" on the
  default configuration. Serving-size options offered: 14 / 28 / 42 Servings. A "Skip
  flavors and save $5.98" checkbox sits in the flavor-packet section.
Real proof values on page: 5 filled stars with "(2,123)" next to the page title.
  Formula stats shown in the recommendation card: 20g protein per serving, 100 calories
  per serving, 6 ingredients. "Nutrition Facts" link present.
Target Customer: Fitness-minded buyers, mostly mobile, arriving from paid social and quiz
  funnels, who want a protein matched to a specific goal rather than an off-the-shelf tub.
Audit Date: 2026-08-23
Viewport: 390×844, device scale factor 2 (real Chromium capture, not a mockup)
Evidence:
  - outputs/cro-fixes/_gainful_before_raw.png (viewport capture, customizer fully rendered)
  - outputs/cro-fixes/_gainful_before_full.png (full page, 780×15220 @2x)
  - Measured in-page (DOM scan, 2026-08-23): full-page scrollHeight 7610px CSS. A complete
    scan of every <button>, <a> and [role=button] on the page returned NO element whose
    text matches /add to (cart|bag)|checkout|buy now/ anywhere on the page; the highest
    in-page CTA found was "Take The Quiz" at page-y 3693px. The strings "guarantee",
    "money back", "cancel anytime", "risk-free" and "satisfaction" return false against
    the full page innerText; "free shipping" returns true (it appears below the fold).
  - Sticky header measured at 105px tall and contains the top promo bar.

⚠ STALE-NOTE CORRECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
targets_pool.json's mobileIssueSummary for Gainful (written 2026-07-05) describes
"two redundant discount banners" and a customizer "stuck on 'Loading protein
customizer...' with no content for several seconds."

The two stacked discount banners are still accurate and are Finding 1 below.

The loading behaviour needs a correction and a caveat — see the SANDBOX-INCONCLUSIVE
section at the bottom. It is NOT being used as a claim in this week's post.

BRAND DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decision: PRESERVE
Rationale: Gainful's visual system is calm and well built — warm off-white card surface on
white, a single dark ink colour, a humanist sans with generous line height, plenty of
whitespace, and a restrained black/white pill pattern for the serving selector. It reads
premium and it is internally consistent. Nothing here needs a redesign. What is broken is
the ORDER of the page and what is missing from it, not how it looks. Every fix below is a
structural or content change that keeps the existing type, colour and spacing language.
Brand fonts identified: A geometric/humanist sans with a distinctive single-storey "a" and
  wide apertures used for both display and body (Gainful's brand face, GT/Sohne-adjacent).
Brand colors identified: Near-black ink ~#2B2A28; warm light-grey card ~#EDEBE7; pure white
  inner card; a lime/chartreuse accent bar ~#DFF265 used for the promo strip; black pill
  fill for the selected serving state.
If ELEVATE/RETHINK — recommended direction: n/a (PRESERVE)

CRO FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINDING 1
Area: Above the Fold / Offer Clarity
Problem: Two different 25% discount messages stack on top of each other before any product
content appears. A black bar at the very top reads "⭐ Subscribe and Save 25% on every
order ⭐", and immediately below the logo row a lime bar reads "New Customers: 25% off w/
code FLAV25". Together with the header they occupy roughly the first 200px of an 844px
viewport.
Why it hurts: Two offers at the same discount percentage, presented with equal urgency,
force the shopper to work out which one applies to them and whether choosing one forfeits
the other. Nothing on the page answers that. A new customer who subscribes cannot tell if
they get 25%, 50%, or whether FLAV25 is the better deal. Ambiguity at the offer level is
the most expensive kind, because it hits every visitor before they have seen the product.
Fix: Pick one offer for this page and lead with it. Show the new-customer code as the
headline promo, and move subscribe-and-save down to the purchase area where the shopper is
actually choosing a purchase mode — that is where it becomes a decision instead of noise.
State plainly whether the two stack. Same two offers, one at a time, in the place each one
is relevant.
Content angle: Angle 1 (before/after) + Angle 3 (why it works)
Priority: Critical

FINDING 2
Area: Above the Fold / Price Presentation
Problem: The price is the smallest committed piece of information in the hero. "14 Servings
| $31.47" sits right-aligned on the same line as the star rating, at body size and regular
weight — visually subordinate to the page title above it and to every section heading below
it. It is also the one number on the screen that changes as the shopper configures.
Why it hurts: On a configurator, price is the running total. Every choice below (serving
size, flavour packets, the "skip flavors and save $5.98" checkbox) moves it, but it is
rendered as a passing detail rather than an anchor the shopper can watch. Buyers who cannot
see what their choices cost either stop configuring or scroll back repeatedly to check.
Fix: Give price its own line, at display weight, directly under the recommendation card
where the configuration is happening — not tucked into the rating row. Show what changed
("14 servings · $31.47 · $2.25 per serving") so the number is legible as a unit economic,
which is how protein is actually compared.
Content angle: Angle 1 + Angle 2 (buyer psychology)
Priority: Critical

FINDING 3
Area: CTA Effectiveness
Problem: There is no add-to-cart, no buy button, and no primary CTA of any kind in the
first viewport. A full-DOM scan of every button and link on the page found no element
matching "add to cart", "add to bag", "checkout" or "buy now" anywhere on the page at all.
The only in-page CTA the scan returned was "Take The Quiz" at page-y 3693px — more than
four full viewports below the fold, and it sends the shopper into a different funnel rather
than completing this one.
Why it hurts: The page asks for four decisions (dietary preference, primary goal, serving
size, flavour packets) and offers nothing to do with them. A shopper who is already sold
after reading "20g protein, 100 calories, 6 ingredients" has no way to act on that. Effort
spent configuring with no visible endpoint is the classic abandonment pattern on builder
pages — the shopper has invested and been given no exit.
Fix: Add a persistent add-to-cart affordance tied to the configuration — a sticky bottom
bar carrying the live price and the button, so the endpoint is visible from the moment the
first selection is made. This is the single highest-value change on the page.
Content angle: Angle 1 + Angle 4 (quick win)
Priority: Critical

FINDING 4
Area: Trust Signals & Risk Reversal
Problem: There is no risk reversal anywhere on this page. The words "guarantee", "money
back", "cancel anytime", "risk-free" and "satisfaction" do not appear in the page text at
all — verified against the full rendered innerText. This is on a page whose top bar is
actively selling a subscription.
Why it hurts: Two objections go unanswered at the exact moment of decision. First, protein
is a taste-and-tolerance purchase — "what if I don't like it" is the default objection and
nothing addresses it. Second, and worse, the page's most prominent promotional message asks
for a recurring commitment while saying nothing about how to stop one. Asking for a
subscription without stating the exit terms reliably suppresses the subscription take-rate
it is trying to raise.
Fix: Place one short risk-reversal line directly beneath the purchase area. If a guarantee
policy exists elsewhere on the site, surface its real terms here verbatim. If subscription
is cancellable at any time, say so next to the subscribe offer. Do not invent terms — pull
the real policy language.
Content angle: Angle 2 + Angle 3
Priority: High

FINDING 5
Area: Social Proof
Problem: The proof on the page is one row: five filled stars and "(2,123)" beside the
title. There is no numeric average, no link to the reviews, no review excerpt, and no
indication whether those 2,123 ratings are for this formula or for Gainful overall.
Why it hurts: A bare count next to stars is the weakest usable form of social proof. It
carries no voice and answers no specific objection. On a personalisation product the
question is never "is this popular" — it is "did it work for someone with my goal." Gainful
has goal segmentation built into the page and does not use it for proof.
Fix: Make the count a real link to reviews so it is verifiable. Then surface one short
review from a customer with the goal currently selected, so the proof changes as the
configuration changes. Every element needed for this already exists — the goal selector and
the review corpus. Do not render an average rating figure, because the page does not
display one.
Content angle: Angle 2
Priority: High

FINDING 6
Area: Information Hierarchy
Problem: The two configuration dropdowns ("Dietary Preference: None", "Primary Goal: Lose
Weight") are pre-filled with defaults and presented before any explanation of what they
change. The result card that responds to them appears below them, so on first paint the
shopper is looking at controls whose consequence is off-screen or unexplained.
Why it hurts: The page's whole promise is personalisation, but the mechanism is presented
as a form to fill rather than a benefit to receive. "Primary Goal" silently defaulting to
"Lose Weight" also assumes an intent for a shopper who may be here to build muscle, which
mislabels the recommendation before they have touched anything.
Fix: Lead the section with one line naming what the two inputs produce ("Answer two
questions, get your formula"), and either leave Primary Goal unset so the shopper makes a
real choice, or make the default visibly changeable rather than pre-committed.
Content angle: Angle 3
Priority: Medium

FINDING 7
Area: Page Length / Commerce Density
Problem: The page runs 7610px on a 390px viewport — roughly nine viewports — and the
commercial content is confined to the first two. Everything after that is editorial
(numbered brand-story blocks 01/02/03, a quiz block, formula explainers).
Why it hurts: A shopper who scrolls past the configurator has no purchase affordance for
seven straight viewports, and the only CTA they eventually meet routes them out of this
page into the quiz.
Fix: Repeat the purchase affordance after the brand-story section. If the sticky bar from
Finding 3 is implemented, this resolves itself.
Content angle: Angle 4
Priority: Low

SCOPE FOR THIS WEEK'S POST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The rebuild and both graphics cover the above-the-fold configurator only — Findings 1, 2,
3, 4, 5 and 6. That is one screen, which is what keeps a before/after legible at carousel
size. Finding 7 is documented but out of scope for the visual.

Scope-specific headline language for the graphics (never a generic reused phrase):
  Before/after graphic: "Gainful asks for four decisions before it gives you one reason to trust it"
  Annotation graphic:   "The configurator was never the problem. Everything missing around it was."

WHAT MUST NOT BE CLAIMED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- No conversion-lift percentage. No A/B result. Nothing was tested; this is a design critique.
- No invented star rating. The page shows five filled stars and "(2,123)" but NO numeric
  average — do not render "4.8" or similar anywhere.
- Do not invent guarantee or cancellation terms in the rebuild. Finding 4's fix is that a
  risk-reversal line should EXIST; the rebuild must show it as a neutral placeholder tied to
  real policy, never a specific invented promise like "60-day money back guarantee".
- Every price and stat used in the rebuild must be a real value from this brief: $31.47,
  14 / 28 / 42 servings, $5.98 skip-flavors saving, 20g protein, 100 calories, 6 ingredients,
  2,123 ratings. No rounding, no embellishment. The $2.25/serving figure in Finding 2 is
  arithmetic on the real numbers (31.47 ÷ 14 = 2.247) and is fine to show as a derived unit
  price, but must be labelled as per-serving, not presented as a price Gainful advertises.
- Supplement category: keep health claims to what the page itself states. No disease or
  treatment claims.

⚠ SANDBOX-INCONCLUSIVE — DO NOT PUBLISH AS A CLAIM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Across seven headless Chromium loads on 2026-08-23, the protein customizer rendered fully
ONCE (at roughly 6s — that successful load is the "before" capture used for this post) and
remained on the placeholder text "Loading protein customizer..." for the full observation
window on the other six, including three loads observed for 20-22 seconds each.

A network trace on a failing load showed one script request that never completed:
https://polaris.truevaultcdn.com/static/pc/SKBD4EQDW/polaris.js (TrueVault Polaris, a
consent-management script). Every other page script completed; the only other failures were
analytics and ad pixels, which are irrelevant to rendering.

BUT that same script fetches fine from this sandbox outside the browser — curl pulls all
494KB of it with HTTP 200 in 1.6 seconds. So the hang is not a network block, and it cannot
be cleanly attributed to Gainful's site versus this headless environment from here.

This is potentially the single most valuable finding on the page — a core conversion tool
that intermittently never paints is worth more than every layout note above combined. It is
deliberately excluded from the post's claims and graphics because it cannot be verified from
this environment.

ACTION FOR RIDWAN: load this page a few times on a real phone on cellular before mentioning
it anywhere public. If it reproduces, it is a stronger post than the one built this week, and
a genuinely strong outreach opener.

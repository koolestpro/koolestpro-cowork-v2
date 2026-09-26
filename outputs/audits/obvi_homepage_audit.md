━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KOOLESTPRO CRO AUDIT BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STORE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Store URL: https://myobvi.com/
Store Name: Obvi
Page Type: Homepage (above-the-fold hero focus)
Product Name: n/a (homepage) — hero promotes "Collagenic Burn"; on-page best sellers are Collagenic™ Fat Burner Capsules and Collagenic® Burn Fast
Product Price (real, read off the live page 2026-08-02): Collagenic™ Fat Burner Capsules $29.74 (marked "30% off", "#1 Best Seller", 1,489 reviews); Collagenic® Burn Fast $33.99 (1,857 reviews). Autoship option listed at 15% off on both.
Target Customer: Women 25–45 pursuing weight management who also care about hair/skin/nails; price-sensitive, proof-hungry, mostly mobile, mostly arriving from paid social and creator content.
Audit Date: 2026-08-02
Viewport: 390×844, device scale factor 2 (real Chromium capture, not a mockup)
Evidence:
  - outputs/cro-fixes/_obvi_before_raw.png (viewport capture)
  - outputs/cro-fixes/_obvi_before_full.png (full page)
  - outputs/cro-fixes/_obvi_cta_zoom.png (2× crop proving the CTA overlap in Finding 3)
  - outputs/cro-fixes/_obvi_text.txt (full extracted page text)
  - Measured in-page: H1 font-size 30px, hero paragraph font-size 13px; SHOP NOW button 150×44 at (26, 364); TAKE THE QUIZ button 172×47 at (186, 364)

⚠ STALE-NOTE CORRECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
targets_pool.json's mobileIssueSummary for Obvi (written 2026-07-05) says the hero is
"a purely decorative product image ... no headline copy, value prop, or CTA button
overlaid — no clear next action above the fold at all."

That is no longer true. The site has been rebuilt since. As of today the hero has an H1,
a paragraph, two CTA buttons and a social-proof badge. The audit below describes what is
actually on the page today. The pool note should be refreshed (flagged in the run summary).

BRAND DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decision: PRESERVE
Rationale: The brand system does its job. The hot-pink canvas, the rounded purple lockup,
the chunky geometric type and the pill buttons with hard offset borders read as a young,
confident supplement brand and they are consistent site-wide. Nothing here needs a redesign.
What is broken sits on top of the brand: the headline is spending the largest text on the
page announcing inventory, the value proposition is compressed into 13px body copy, and a
third-party accessibility widget is physically sitting on the primary button. Keep every
brand asset, fix the structure.
Brand fonts identified: Wide geometric sans for display/headline and UI labels (Poppins /
Gilroy family), same face at lighter weight for body copy.
Brand colors identified: Hot pink background ~#F97ED6; deep indigo/purple ink and button
fill ~#4B2E9E; white pill surfaces; near-white body text on pink.
If ELEVATE/RETHINK — recommended direction: n/a (PRESERVE)

CRO FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINDING 1
Area: Above the Fold / Value Proposition
Problem: The H1 — the single largest piece of text on the page, set at 30px — reads
"BACK IN STOCK!". That is an inventory status, not a value proposition. The word "Obvi"
appears in the logo and the word "Collagenic Burn" appears only inside the paragraph
beneath, at 13px.
Why it hurts: "Back in stock" is only meaningful to someone who already tried to buy and
found it sold out. For everyone else — and on a homepage fed by paid social and creator
traffic, that is most people — the biggest words on the screen carry zero information about
what Obvi sells or why it would work for them. The five-second test fails: a first-time
visitor can look at the top of this page and still not know what the product does.
Fix: Give the H1 the job of stating the outcome and the mechanism in the brand's own voice,
using claims already made elsewhere on this same page ("Collagen-infused weight support"
/ "metabolism, cravings and collagen in one daily dose"). Demote "Back in stock" to a small
pill or eyebrow above the headline where it still does its urgency job for returning buyers
without stealing the largest slot on the page.
Content angle: Angle 1 (before/after) + Angle 3 (why it works)
Priority: Critical

FINDING 2
Area: Above the Fold / Copy Structure
Problem: The entire value proposition is delivered as one 40-word run-on sentence at 13px,
occupying five lines on a 390px viewport: "Obvi's Collagenic Burn is finally back in stock!
Obvi's Burn combines powerful formulas designed to boost metabolism, control cravings, and
healthy weight loss while nourishing your hair, skin, and nails from within."
Why it hurts: Four separate benefits (metabolism, cravings, weight, hair/skin/nails) are
fused into a single unscannable block, and the type is 2.3× smaller than the headline that
says nothing. Mobile shoppers scan; they do not read paragraphs above the fold. The four
strongest reasons to buy are present on the page and effectively invisible.
Fix: Split the paragraph into three or four short benefit lines with icons or check marks,
one benefit per line, at readable size. Same claims, same words where possible — only the
structure changes. Nothing new is invented.
Content angle: Angle 1 + Angle 2 (buyer psychology)
Priority: Critical

FINDING 3
Area: CTA Effectiveness / Tap Targets
Problem: The third-party accessibility widget button (a ~44px blue circle, bottom-left) is
rendered directly on top of the bottom-left corner of the primary SHOP NOW button. Measured:
SHOP NOW occupies x 26–176, y 364–408; the widget circle sits at roughly x 23–68, y 400–445.
They overlap. Proof crop: outputs/cro-fixes/_obvi_cta_zoom.png.
Why it hurts: Two things at once. Cosmetically it reads as a rendering bug on the single
most important button on the page. Functionally it puts a competing tap target inside the
thumb zone, on the corner of the primary CTA, so a low or left-side tap opens an
accessibility panel instead of the store.
Fix: Move the accessibility launcher's anchor (most of these widgets expose a position
setting) to the bottom-right, below the chat bubble, or add bottom offset so it clears the
hero CTA row entirely. This is a settings change, not a rebuild.
Content angle: Angle 1 + Angle 4 (quick win)
Priority: Critical

FINDING 4
Area: Above the Fold / Product Info
Problem: No product and no price appear above the fold. Real, strong commercial signals do
exist on this page — Collagenic™ Fat Burner Capsules at $29.74 marked 30% off with 1,489
reviews and a "#1 Best Seller" tag, and Collagenic® Burn Fast at $33.99 with 1,857 reviews —
but they sit far down the page, past the category tiles and a marquee band.
Why it hurts: Visitors who arrive ready to buy have nothing concrete to act on early. A
"30% off" on the #1 best seller is a genuinely strong hook and it is buried. "SHOP NOW" as
the only early commerce signal asks the shopper to go looking for what to buy.
Fix: Surface one hero product card above the fold — name, real price, real review count,
and the real 30%-off flag — sitting directly under the CTA row. All four values already
exist on the live page; none need to be invented.
Content angle: Angle 2 + Angle 3
Priority: High

FINDING 5
Area: CTA Effectiveness / Hierarchy
Problem: Two CTAs sit side by side at near-identical visual weight, and the secondary one
is physically bigger than the primary: SHOP NOW is 150×44, TAKE THE QUIZ is 172×47. One is
filled purple, the other is a white outline pill of the same family.
Why it hurts: When two buttons have the same weight, neither is the next action. The
shopper has to make a decision before they have any information, which is the most reliable
way to get no decision at all.
Fix: Make one primary and mean it — full-width filled SHOP NOW carrying the offer ("Shop
the #1 best seller — 30% off"), with the quiz demoted to a text link beneath ("Not sure
which one? Take the 60-second quiz"). Quiz funnels convert well for this brand, so keep it
present, just not competing.
Content angle: Angle 3
Priority: High

FINDING 6
Area: Trust Signals & Social Proof
Problem: The strongest proof above the fold — "OVER 800,000 HAPPY CUSTOMERS" with five
stars — is rendered as the smallest, palest element in the hero: a thin white pill in muted
grey type. Meanwhile the page's hardest proof (1,489 and 1,857 review counts, NON GMO,
SUGAR FREE, GLUTEN FREE, GMP CERTIFIED, THIRD-PARTY TESTED, and a 115,000+ community) all
lives below the fold.
Why it hurts: In supplements, the objection is always "does this actually work and can I
trust it." Obvi has unusually good answers and is whispering them. Proof placed above the
CTA reduces hesitation at the exact moment of decision; proof placed after the scroll gets
read by people who already decided.
Fix: Keep the 800,000 badge but give it weight, and pull one certification row (GMP
certified / third-party tested) up under the CTA. Use the real review count on the hero
product card from Finding 4. Do not invent a rating figure that is not on the page.
Content angle: Angle 2
Priority: Medium

FINDING 7
Area: Layout Polish
Problem: The scrolling marquee band immediately below the hero ("MADE TO SUPPORT YOUR EVERY
NEED", "WE HELP GUIDE YOUR JOURNEY AT ANY STAGE") is clipped mid-word at both viewport edges
in any static frame, so the first thing below the fold reads as broken text.
Why it hurts: Minor on its own, but it lands directly after the CTA row and undercuts the
polish of everything above it. Screenshot-shared pages and paused scrolls both catch it.
Fix: Add edge fade masks to the marquee, or pad the track so a full phrase is legible at
rest on a 390px viewport.
Content angle: Angle 4
Priority: Low

SCOPE FOR THIS WEEK'S POST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The rebuild and both graphics cover the hero above the fold only — Findings 1, 2, 3, 4, 5
and 6. That is one screen, which is what makes a before/after legible at carousel size.
Findings 7 is documented but out of scope for the visual.

Scope-specific headline language for the graphics (never a generic reused phrase):
  Before/after graphic: "The biggest words on Obvi's homepage announce inventory, not results"
  Annotation graphic:   "Six fixes on one screen — and none of them touch the brand"

WHAT MUST NOT BE CLAIMED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- No conversion-lift percentage. No A/B result. Nothing was tested; this is a design critique.
- No invented star rating. The page shows five filled stars next to "OVER 800,000 HAPPY
  CUSTOMERS" but no numeric average — do not render "4.8" or similar anywhere.
- Every price, review count and certification used in the rebuild must be one of the real
  values recorded in this brief. No rounding, no embellishment.
- Supplement category: the FDA statement on the live site applies. Do not write copy that
  makes a disease or treatment claim, and keep the standard disclaimer on any caption that
  repeats a health benefit.

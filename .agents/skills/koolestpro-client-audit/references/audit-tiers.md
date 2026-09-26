# Three-Tier Audit Framework

This file defines what to look for in each tier, which sub-skills to apply, and how to prioritize findings.

**Mobile-first rule:** Run every audit at 390px mobile viewport first. A finding that only appears on desktop is low priority. A finding that breaks the mobile experience is Critical regardless of tier.

**Evidence rule:** Every finding should reference data where available — GA4, Hotjar, competitor benchmark, or behavioral observation. Observation-only findings are valid but clearly flagged.

---

## TIER 1 — FIX WHAT'S LEAKING

**Purpose:** Identify conversion issues actively costing sales right now.
**Client framing:** "These are the fixes that will have the fastest impact on your revenue."

### Sub-skills to apply

**cro-methodology (marketing-cro)**
Run the Quick Diagnostic checklist:
- Is there one clear primary action on each page?
- Have objections been researched (not guessed)?
- Is there an O/CO (Objection/Counter-Objection) map?
- Is the value proposition clear within 5 seconds?
- Are persuasion assets visible — testimonials, awards, guarantees?
- Has the full funnel been mapped for blocked arteries?

**ux-design:ux-heuristics**
Apply Nielsen's 10 heuristics to each page:
- Visibility of system status
- Match between system and the real world
- User control and freedom
- Consistency and standards
- Error prevention
- Recognition rather than recall
- Flexibility and efficiency
- Aesthetic and minimalist design
- Help users recognize, diagnose, recover from errors
- Help and documentation

**ux-design:refactoring-ui**
Audit visual design:
- Visual hierarchy — is there a clear 3-level hierarchy (primary / secondary / tertiary)?
- Typography — modular scale, readable weights, appropriate sizes
- Color — CTA contrast (WCAG AA minimum), coherent palette, accent discipline
- Spacing — consistent scale, related elements grouped, breathing room
- CTA — full width on mobile, min 52px height, value-led copy, high contrast

**sales-influence:influence-psychology**
Audit the six persuasion principles (Cialdini):
- Reciprocity — is there a lead magnet, free value, or gift before the ask?
- Commitment — do micro-conversions build toward purchase?
- Social proof — reviews, ratings, user counts, customer photos visible?
- Authority — credentials, press mentions, expert endorsements present?
- Liking — does the brand feel relatable and human?
- Scarcity — is there genuine urgency or limited availability signalled?

### What a Tier 1 finding looks like

```
FINDING [N]
Element: [specific named element — "the Add to Cart button on the PDP"]
Location: [where on the page — "above the fold, below the price"]
Problem: [what's wrong and why it hurts]
Fix: [specific, implementable — not a direction, a decision]
Impact: Critical / High / Medium
```

### Prioritization
- **Critical** = directly blocking purchase (broken CTA, no trust signals, unclear price)
- **High** = measurably reducing conversion (weak social proof, poor CTA copy, no urgency)
- **Medium** = friction that compounds over time (spacing issues, font weight problems, missing size guide)

When findings exceed 8, include only Critical + High in the client report. Move Medium findings to "Additional Findings."

---

## TIER 2 — UNLOCK WHAT'S MISSING

**Purpose:** Identify conversion assets the store doesn't have that could open new revenue channels or customer segments.
**Client framing:** "These are the opportunities your store isn't using yet."

### Sub-skills to apply

**sales-influence:hundred-million-offers**
Audit the offer structure using the Value Equation:
- Dream outcome — is it clearly stated?
- Perceived likelihood of achievement — is there proof it works?
- Time delay — how fast do they get results? Is this communicated?
- Effort and sacrifice — is the purchase frictionless?
- Bonuses — are there stacked bonuses that increase perceived value?
- Guarantee — is there a risk-reversal guarantee? Is it prominent?
- Naming — does the offer name communicate the transformation?

**marketing-cro:storybrand-messaging**
Check whether the brand script is clear:
- Is the customer positioned as the hero (not the brand)?
- Is there a clear villain (the problem they're solving)?
- Is there a guide (the brand) with a plan?
- Is the CTA direct and specific?
- Is the cost of inaction clear?

**marketing-cro:scorecard-marketing**
Assess whether a quiz/assessment funnel would benefit this store:
- Does the store have multiple customer segments who need different products?
- Is there a "which product is right for me?" question buyers often ask?
- Would a quiz increase average order value or email capture?
- Recommend a quiz funnel if 2+ of these are true

**sales-influence:made-to-stick**
Run the SUCCESs test on key copy (headline, hero text, CTA):
- Simple — is there one clear core message?
- Unexpected — does the opening break a pattern?
- Concrete — are there specific details, not vague claims?
- Credible — is there proof, not just assertion?
- Emotional — does it make the buyer feel something?
- Stories — is there a narrative, not just features?

### Page types to recommend when appropriate

Only recommend these when there's a genuine fit — not as a default list:

| Page type | When to recommend |
|-----------|------------------|
| **Advertorial** | Store runs paid traffic and lands directly on PDP with no warm-up |
| **Listicle landing page** | Product solves a problem that benefits from education before purchase |
| **Quiz funnel** | Multiple customer segments, "which one is right for me?" question exists |
| **Bundle page** | High AOV opportunity, products naturally pair together |
| **Collection landing page** | Traffic going to a generic collection instead of a curated entry point |
| **Post-purchase upsell** | Store has no upsell sequence after checkout |
| **Subscription landing page** | Consumable product with repeat purchase potential |

---

## TIER 3 — FUTURE BETS

**Purpose:** Emerging opportunities the store isn't positioned for yet. These have a longer runway but compound significantly.
**Client framing:** "These are where the smart stores are already moving. Getting ahead now costs less than catching up later."

### Sub-skills to apply

**seo-geo-aeo (advanced angle only)**
These clients already rank. Focus exclusively on:
- **Content gaps** — topics with buying intent where the store has no coverage
- **Schema markup** — product schema, FAQ schema, review schema for rich results
- **AEO (Answer Engine Optimization)** — is the store positioned to appear in featured snippets and voice search?
- **GEO (Generative Engine Optimization)** — is the store cited in AI search responses (ChatGPT, Perplexity, Gemini)?
- **AI search visibility** — does the brand appear when someone asks an AI to recommend products in this category?

Never recommend: title tag optimization, keyword density, basic meta descriptions, internal linking hygiene. These clients are past that.

**marketing-cro:contagious (when relevant)**
Apply STEPPS framework to assess word-of-mouth potential:
- Social Currency — does owning/using this product make customers look good?
- Triggers — are there environmental cues that remind customers to share?
- Emotion — does the product or brand generate high-arousal emotion?
- Public — is the product visible in use?
- Practical Value — is there shareable information or tips?
- Stories — is there a brand story that travels?

Recommend a referral program or viral loop only when 3+ STEPPS factors are strong.

---

## CHECKOUT AUDIT

Run this after Tier 1-3 as a standalone section. Checkout is where the most money disappears and it has its own distinct UX considerations.

**Cart page**
- Is there an upsell or cross-sell offer before entering checkout?
- Is the cart summary clear — product name, variant, price, quantity?
- Are trust signals (security badge, returns policy) visible at this decision point?
- Is there a clear "proceed to checkout" CTA or is it buried?

**Checkout flow**
- How many steps? (Shopify standard: contact → shipping → payment — acceptable. More than 3 steps = friction)
- Is guest checkout the default or is account creation pushed?
- Are there unnecessary form fields? (Company name, address line 2 as required fields)
- Does the checkout feel consistent with the store's brand or does it feel like a generic page?

**Payment page**
- Are trust badges (SSL, secure checkout) visible near the payment form?
- Are payment options complete? Check for: Shop Pay, Apple Pay, Google Pay, Klarna/Afterpay (especially important for higher price points)
- Is the price summary visible without scrolling before paying?

**Post-purchase page (thank you page)**
- Is there a post-purchase upsell offer immediately after purchase? (Shopify allows this natively)
- Or is it a dead end — just an order confirmation?
- Is there a social share prompt or referral incentive?

**Checkout findings format:**
Same structure as Tier 1 findings — element, problem, evidence, fix, priority.
Cart and payment page issues = Tier 1 if blocking purchase.
Post-purchase upsell absence = Tier 2 opportunity.

---

## EMAIL + POST-PURCHASE GAP ASSESSMENT

Even without platform access, assess what standard flows should exist and flag what's missing.

**Standard flows for eCommerce (flag if absent):**

| Flow | Priority | Industry benchmark |
|------|----------|-------------------|
| Abandoned cart (3-email, 24hr) | Tier 2 Critical | 5-15% recovery rate |
| Welcome series (3-5 emails) | Tier 2 High | Sets brand expectation |
| Post-purchase (review request + upsell) | Tier 2 High | 20-30% repeat purchase lift |
| Browse abandonment | Tier 2 Medium | Catches high-intent non-converters |
| Win-back (lapsed customers) | Tier 2 Medium | 10-15% reactivation |
| SMS (for right categories) | Tier 3 | Higher open rates than email |

**If Klaviyo/email data is available:**
- Open rate <20% on a flow = subject line or send timing problem
- Click rate <2% = email content isn't matching offer or landing page
- High open, low purchase = landing page problem, not email problem

**Recommendation format:**
"You have no abandoned cart flow. At your current traffic volume, this is likely leaving [estimated $] on the table monthly. A standard 3-email sequence recovers 5-15% of abandoned carts."

---

## AUDIT SEQUENCING

Run tiers in order — 1 → 2 → 3 → Checkout → Email gaps. Don't jump to Tier 2 opportunities if the store has critical Tier 1 leaks. A great quiz funnel won't save a store with a broken CTA and no social proof.

Exception: if the client explicitly says Tier 1 basics are handled, or the audit confirms it, move directly to Tier 2/3.

Always use competitor benchmarks from the funnel discovery phase as evidence throughout. A finding backed by competitor comparison is significantly more persuasive than one based on best practice alone.

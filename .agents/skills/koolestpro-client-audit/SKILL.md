---
name: koolestpro-client-audit
description: Professional client-facing CRO audit skill for Ridwan Adekunle (@koolestpro). Runs a structured audit on any eCommerce store (primarily Shopify) covering conversion, SEO, speed, checkout, and post-purchase — then delivers branded deliverables. Three modes: PRE-CALL (discovery questions), STANDARD AUDIT (growing/mid-size brands — full report suite), EXPERT REVIEW (large optimized brands with in-house teams — focused strategic memo + experiment hypotheses). Use when Ridwan says "audit this client", "I have a new client", "run a CRO audit", "expert review", "they already have a CRO team", "big brand", "client discovery call", or shares a store URL with intent to deliver paid work. Does NOT use koolestpro content pipeline skills (A, B, D, E).
---

# Koolestpro — Client Audit

You are Ridwan's client audit engine. Your job is to run a rigorous, evidence-based CRO audit and produce professional branded deliverables for paying clients.

**This skill is for paid client work — not content creation.** The koolestpro content pipeline (Skills A, B, D, E) is entirely separate.

**Mobile-first, always.** Audit every page at 390px mobile viewport first. Desktop is secondary.

---

## DETECT MODE FIRST

Three possible modes. Identify which applies before doing anything else.

**MODE A — PRE-CALL**
Ridwan is preparing for a discovery call. Ask: *"Is this a standard brand or a larger brand with an in-house team?"* Then output the matching question set from `references/discovery-questions.md`. Done — no audit runs.

**MODE B — STANDARD AUDIT**
Growing or mid-size brand. No dedicated in-house CRO team. Needs a full audit and clear guidance on what to fix. Run the full 10-step flow below.

**MODE C — EXPERT REVIEW**
Large or well-optimized brand. Has an in-house CRO team, designer, developer — experts actively working on the store. Ridwan is filling a specific gap or providing an external second opinion. Run the Expert Review flow in `references/expert-review.md` instead of the standard flow.

**How to detect Expert Review:**
- Ridwan mentions "they already have a team", "in-house CRO", "big brand", "they're already optimized"
- Client only wants a specific area reviewed, not a full audit
- Client mentions their current test velocity or active experiments
- Store is clearly a scaled brand (large review count, professional design, obvious paid media budget)

If unclear after reading the brief, ask: *"Does this client have an in-house CRO team or developer actively working on the store, or are they mostly running it themselves?"*

---

## AUDIT FLOW

### STEP 1 — INTAKE

Ask Ridwan to fill in:

```
CLIENT BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Store URL:
Pages to audit: (list each)
Product / what they sell:
Target customer:
Traffic sources: (Meta / Google / organic / email / other)
Main complaint or goal:
What they've already tried:
2-3 competitors: (if known)
Any extra context:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### STEP 1.5 — BEHAVIORAL DATA INTAKE

Before touching the site, ask what data the client already has. See `references/behavioral-data.md` for how to request and interpret each source.

```
What behavioral data do you have access to?
Check all that apply:

[ ] GA4 / Google Analytics (can you export or share read access?)
[ ] Hotjar (heatmaps, session recordings, exit surveys)
[ ] Microsoft Clarity (free — check if installed)
[ ] Lucky Orange / Mouseflow / FullStory
[ ] Shopify Analytics (built-in — always available)
[ ] Klaviyo / email platform data (open rates, click rates, flows)
[ ] Customer support tickets or reviews (qualitative)
[ ] None of the above
```

Process whatever is provided before auditing. Behavioral data turns visual observations into evidence. A finding with "78% mobile bounce rate on PDP (GA4)" is worth 10x more than "the page looks cluttered."

---

### STEP 2 — SITE ACCESS + SITEMAP CRAWL

**Access hierarchy:**
1. Direct fetch via web_fetch — always try first
2. Password blocked → ask Ridwan for password, retry
3. Geo-blocked → ask Ridwan to use VPN, retry
4. Last resort → full-page screenshot of each page

**After gaining access, immediately:**

1. Fetch `[store-url]/sitemap.xml` — parse all page URLs, identify:
   - `/pages/` entries not visible in navigation (potential advertorials, landing pages, offer pages)
   - `/blogs/` entries used as editorial pre-sell content
   - Any URL patterns suggesting paid traffic entry points

2. Fetch `[store-url]/robots.txt` — note any disallowed paths. Blocked paths are often the most interesting pages.

3. Try common hidden page patterns:
   `/pages/advertorial`, `/pages/offer`, `/pages/lp`, `/pages/try-[product]`, `/pages/sale`

Flag every non-navigation page found. These are Tier 2 candidates if they don't exist, or audit targets if they do.

---

### STEP 2.5 — FUNNEL DISCOVERY

Map the client's full conversion funnel before auditing individual pages. See `references/funnel-discovery.md` for the full process.

1. **Ad library scan** — search the client's brand in:
   - Meta Ad Library: `facebook.com/ads/library`
   - Google Ads Transparency: `adstransparency.google.com`
   - TikTok Creative Center: `ads.tiktok.com/business/creativecenter`
   Find active ads → identify landing page URLs → fetch those pages

2. **Funnel map** — generate a visual diagram showing the complete path:
   `[Ad creative] → [Entry page] → [PDP/Collection] → [Cart] → [Checkout] → [Post-purchase]`
   Mark what exists, what's missing, and what's broken.

3. **Gap identification** — flag structural gaps immediately:
   - Running paid ads but landing on homepage = Tier 1 Critical
   - No advertorial/pre-sell page for cold traffic = Tier 2 opportunity
   - No post-purchase upsell = Tier 2 opportunity

---

### STEP 2.6 — COMPETITOR BENCHMARKING

Audit 2-3 competitors' stores using the same eye you'll use on the client. See `references/funnel-discovery.md` for the benchmarking framework.

For each competitor, note:
- Above-fold structure and value proposition clarity
- Trust signals and social proof placement
- CTA copy and design
- Page types in their funnel (advertorial? quiz? bundle page?)
- Ad creative and landing page strategy (from ad libraries)
- Offer structure (guarantees, bonuses, urgency)

This creates the benchmark that makes every client finding land harder:
*"Your top competitor shows 847 reviews above the fold. You have 23 hidden below it."*

---

### STEP 3 — THREE-TIER AUDIT (MOBILE-FIRST)

Run all tiers in sequence. Full framework in `references/audit-tiers.md`.

**Tier 1 — Fix what's leaking**
Conversion issues actively costing sales.
Sub-skills: `cro-methodology`, `ux-design:ux-heuristics`, `ux-design:refactoring-ui`, `sales-influence:influence-psychology`

**Tier 2 — Unlock what's missing**
Conversion assets and page types the store doesn't have.
Sub-skills: `sales-influence:hundred-million-offers`, `marketing-cro:storybrand-messaging`, `marketing-cro:scorecard-marketing`, `sales-influence:made-to-stick`

**Tier 3 — Future bets**
Emerging opportunities — advanced SEO, AI search, word-of-mouth.
Sub-skills: `seo-geo-aeo` (advanced angle only), `marketing-cro:contagious`

**Prioritization:** When Tier 1 findings exceed 8, surface only top 5 (Critical + High) in the client report. Move the rest to "Additional Findings."

---

### STEP 3.5 — CHECKOUT AUDIT

Shopify checkout is where the most money disappears. Audit separately from the PDP.

Check:
- **Cart page** — is there an upsell or cross-sell before checkout? Is the cart summary clear? Are trust signals visible at this decision point?
- **Checkout flow** — how many steps? Is guest checkout prominent? Is there unnecessary friction (forced account creation, too many fields)?
- **Payment page** — trust badges near the payment form? Is the security signal visible? Are payment options complete (Shop Pay, Apple Pay, Klarna)?
- **Post-purchase page** — is there an upsell offer immediately after purchase? Or is it a dead end?
- **Abandoned cart rate** — if known from GA4 or Shopify Analytics, cite the number as evidence

Flag checkout findings as Tier 1 if they're blocking purchase, Tier 2 if they're revenue opportunities.

---

### STEP 4 — PAGESPEED

Ask: *"Please paste your PageSpeed Insights results for each page from pagespeed.web.dev — mobile scores are the priority."*

If not provided: flag Speed Report as incomplete, leave placeholder with instructions. Don't block the rest of the audit.

---

### STEP 5 — EMAIL + POST-PURCHASE FUNNEL GAPS

Even without direct access to their email platform, assess what should exist based on their traffic sources and product type. Flag gaps as Tier 2 opportunities.

Ask Ridwan: *"Do you know what email flows they have set up? (abandoned cart, welcome, post-purchase)"*

Assess regardless:
- **Abandoned cart flow** — industry standard is 3-email sequence within 24 hours. If unknown, recommend as standard Tier 2 opportunity.
- **Welcome flow** — does their traffic source (paid ads, organic) suggest a high volume of new subscribers who need nurturing?
- **Post-purchase sequence** — repeat purchase potential? Review request timing? Loyalty program?
- **SMS** — is their product category and customer type suited to SMS marketing?

If Klaviyo or email data was provided in Step 1.5, use open rates and click rates to identify which flows are underperforming.

---

### STEP 6 — RAW INTERNAL BRIEF

Output a complete unfiltered document for Ridwan's eyes only:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERNAL AUDIT BRIEF — [Client/Store Name]
[Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CLIENT CONTEXT + BEHAVIORAL DATA SUMMARY
[Intake brief + key data points from GA4/Hotjar/etc.]

FUNNEL MAP
[Visual or text diagram of the full funnel]

COMPETITOR BENCHMARKS
[Key observations from 2-3 competitors]

TIER 1 FINDINGS — [N] issues
[Numbered — element, problem, evidence, fix, priority]

CHECKOUT FINDINGS — [N] issues
[Same format]

TIER 2 OPPORTUNITIES — [N] items
[Opportunity, rationale, recommended action]

EMAIL/POST-PURCHASE GAPS — [N] items
[What's missing, recommended flow]

TIER 3 FUTURE BETS — [N] items
[Opportunity, why now, action]

SEO ANALYSIS
[Advanced findings — content gaps, schema, AEO, GEO]

PAGESPEED SUMMARY
[Scores + top issues, or PLACEHOLDER]

ADDITIONAL FINDINGS (overflow Tier 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### STEP 7 — APPROVAL GATE

Stop and say:

> *"Here's the full internal brief. Review it, make any edits, remove anything that doesn't fit, and confirm when ready. Client deliverables generate after your sign-off."*

Nothing gets generated until Ridwan confirms.

---

### STEP 8 — CLIENT DELIVERABLES

Invoke the `pdf` skill. Full templates in `references/report-templates.md`.

1. **CRO Report** — Tier 1 + Tier 2 findings, plain English
2. **SEO Report** — Tier 3 advanced SEO/GEO/AEO findings
3. **Speed Report** — PageSpeed scores + fixes (or placeholder)
4. **Priority Action Checklist** — Top 10 actions ranked by impact
5. **Master Navigation Document** — How to read the delivery + CTA

All documents: **@koolestpro · Ridwan Adekunle · Shopify CRO & UX** branding.
All documents end with: *"Ready to implement? Let's talk → [booking link / DM @koolestpro]"*

---

### STEP 9 — DELIVERY FORMAT

Ask Ridwan:
```
How would you like to deliver this?
A — All PDFs in a ZIP
B — HTML master + PDFs in a ZIP
C — Notion delivery page (auto-built)
```

For Option C, use the Notion MCP to build the delivery page automatically.

---

### STEP 10 — HANDOFF SUMMARY

```
DELIVERY READY — [Client/Store Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files: [list]
Top 3 talking points for the client call:
  1. [Most critical finding — with evidence]
  2. [Biggest Tier 2 opportunity]
  3. [Competitor gap that will land hardest]
Suggested upsell: [what to offer for implementation]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## EDGE CASES

| Situation | Response |
|-----------|----------|
| Site totally inaccessible | Escalate access hierarchy. If all fail, pause and ask Ridwan |
| No behavioral data available | Proceed with visual audit only. Note findings are observation-based, not data-backed |
| No competitors known | Use Tier 1 findings to infer category from product type, then find competitors via web search |
| PageSpeed not provided | Flag in Speed Report, placeholder with instructions |
| Minimal Tier 1 findings | Reframe CRO Report as Growth Opportunities audit. Lean into Tier 2/3 |
| Client wants partial audit | Run only requested sections, generate only relevant reports |
| No ads found in ad libraries | Note in funnel map. Absence of paid traffic is itself a finding — Tier 2 opportunity |
| Checkout not accessible | Note as limitation, make standard checkout recommendations based on Shopify defaults |

---

## QUALITY CHECKLIST

Before generating client deliverables:

- [ ] All pages fetched and read (mobile viewport first)
- [ ] Sitemap crawled — hidden pages identified
- [ ] Ad libraries checked — funnel mapped
- [ ] Competitors benchmarked — reference points ready
- [ ] Behavioral data incorporated as evidence where available
- [ ] Checkout audited separately
- [ ] Email/post-purchase gaps assessed
- [ ] Tier 1 findings are specific (named element, evidence, fix)
- [ ] Prioritization applied (≤5 in main report if heavy)
- [ ] SEO section is advanced-only
- [ ] Ridwan has approved the internal brief
- [ ] All PDFs include @koolestpro branding + CTA
- [ ] Delivery format matches Ridwan's selection

---

## REFERENCE FILES

- `references/discovery-questions.md` — Pre-call discovery questions
- `references/behavioral-data.md` — Behavioral data intake + interpretation guide
- `references/funnel-discovery.md` — Sitemap crawl, ad library scan, competitor benchmarking
- `references/audit-tiers.md` — Three-tier audit framework with sub-skill instructions
- `references/report-templates.md` — Exact structure for all client deliverables

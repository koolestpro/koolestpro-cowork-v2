# Behavioral Data Intake Guide

How to request, process, and use each data source to strengthen audit findings with evidence.

The goal: turn visual observations into data-backed findings. "The CTA lacks contrast" becomes "The CTA lacks contrast — consistent with the 74% mobile bounce rate on the PDP (GA4)."

---

## GA4 / GOOGLE ANALYTICS

**What to request:**
Ask Ridwan to get the client to export or share read access. Minimum useful exports:

- **Audience → Overview** — device split (mobile vs desktop %), new vs returning
- **Engagement → Pages and screens** — bounce rate and avg. engagement time per page
- **Monetization → Purchase journey** — funnel drop-off from product view → add to cart → checkout → purchase
- **Monetization → Checkout journey** — step-by-step checkout abandonment
- **Acquisition → Traffic acquisition** — which channels drive the most sessions vs. the most revenue (they often differ)

**What to look for:**

| Signal | What it means for the audit |
|--------|---------------------------|
| Mobile bounce rate >70% on PDP | Above-fold experience failing on mobile — Tier 1 Critical |
| Add-to-cart rate <5% | CTA, trust signals, or value prop issue — Tier 1 High |
| Checkout abandonment >70% | Checkout friction — Tier 1 or checkout audit finding |
| Paid traffic ≠ top revenue source | ROAS problem — funnel mismatch, likely landing page issue |
| High traffic, low conversion on specific page | That page is the priority audit target |
| New visitors <30% | Retention/repeat issue — shift focus to post-purchase |
| Organic >> Paid in revenue contribution | Tier 3 — SEO leverage is strong, double down |

**Use in the report:**
Cite GA4 data as evidence for every finding it supports. Format: `[Metric]: [Value] (GA4, [date range])`

---

## HOTJAR

**What to request:**
Ask for screenshots or exports of:
- **Heatmaps** — click map and scroll map for each audited page (mobile view)
- **Session recordings** — share 5-10 recordings of non-converting sessions on the PDP
- **Exit surveys** — export any responses from "What stopped you from buying today?"
- **Form analysis** — if they have a quiz or multi-step form, where do people drop off?

**What to look for:**

| Signal | What it means |
|--------|--------------|
| Scroll map shows <50% reach the CTA | CTA is too far down — Tier 1 Critical |
| Click map shows rage clicks on non-clickable elements | UX confusion — Tier 1 High |
| Visitors hover on price without clicking | Price/value objection — address with trust signals or payment options |
| Exit survey: "too expensive" | Price objection — Tier 1 — needs risk reversal or value framing |
| Exit survey: "not sure if it'll fit" | Missing size guide or returns clarity — Tier 1 High |
| Sessions show users going back and forth between pages | Navigation confusion or comparison shopping — UX finding |

**Without access:**
Ask Ridwan to watch 5 session recordings himself and note: where do users hesitate? Where do they scroll back up? Where do they leave? These observations count as evidence.

---

## MICROSOFT CLARITY (FREE)

Clarity is free and widely installed — worth checking if the client has it without knowing.

**How to check:** Ask Ridwan to look in the Shopify theme code for `clarity.ms` or check `clarity.microsoft.com` to see if it's set up.

**What Clarity provides:**
- Heatmaps (click, scroll, area)
- Session recordings
- Rage click and dead click detection (automatic)
- JavaScript error detection

Interpret the same way as Hotjar above.

---

## LUCKY ORANGE / MOUSEFLOW / FULLSTORY

Same interpretation as Hotjar. Ask for:
- Scroll depth maps (mobile)
- Top rage click elements
- Funnel reports if set up
- Any exit poll responses

---

## SHOPIFY ANALYTICS (ALWAYS AVAILABLE)

Shopify's built-in analytics are accessible even without GA4. Always check.

Key reports:
- **Online store conversion rate** — site-wide, by device
- **Sessions by traffic source** — which channels send the most traffic
- **Top products by revenue** — which products to prioritize in the audit
- **Cart abandonment rate** — direct signal for checkout friction
- **Average order value** — benchmark for AOV optimization recommendations

Find these in: Shopify Admin → Analytics → Reports

---

## KLAVIYO / EMAIL PLATFORM DATA

**What to request:**
- List of active flows (abandoned cart, welcome, post-purchase, browse abandonment)
- Abandoned cart flow performance: open rate, click rate, recovery rate
- Welcome flow: open rate trend across emails in the sequence
- Post-purchase: what emails go out after purchase and when

**What to look for:**

| Signal | What it means |
|--------|--------------|
| No abandoned cart flow | Tier 2 Critical — immediate revenue recovery opportunity |
| Abandoned cart open rate <20% | Subject line problem — or sending too late |
| No post-purchase sequence | Missing CLV play — Tier 2 High |
| Welcome flow drop-off after email 1 | Value isn't established early enough |
| High open, low click in flows | Email content isn't matching the offer or landing page |

If no email flows exist at all: flag as Tier 2 opportunity with estimated revenue impact (industry standard: abandoned cart recovery is 5-15% of abandoned carts).

---

## CUSTOMER REVIEWS + SUPPORT TICKETS (QUALITATIVE)

Often overlooked but highly valuable. Ask if the client can share:
- Top 20 negative reviews (1-3 star) — these are the objections the page isn't handling
- Top 10 support tickets by category — reveals what buyers are confused or frustrated about
- Any "what almost stopped you from buying?" survey responses

**How to use:**
Extract the exact language customers use. If 8 out of 20 negative reviews mention "sizing was confusing" — that's a Tier 1 finding with customer voice as evidence, not just visual opinion.

Map each complaint category to an O/CO (Objection/Counter-Objection) table and identify which ones the current page addresses and which it ignores.

---

## NO DATA AVAILABLE

If the client has none of the above:

1. Proceed with visual audit only
2. Note in the internal brief: "Findings are observation-based. Recommend installing Microsoft Clarity (free) immediately to begin collecting behavioral data."
3. Add to the Action Checklist as a quick win: "Install Microsoft Clarity — free heatmap and session recording tool. Takes 5 minutes."
4. In the CRO Report, frame findings as: "Based on visual audit — data validation recommended."

A finding without data is still valid. It's just lower confidence.

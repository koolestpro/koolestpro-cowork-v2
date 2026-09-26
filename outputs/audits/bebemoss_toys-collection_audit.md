# CRO Audit — Bebemoss Soft Toys collection page

**Brand:** Bebemoss
**URL audited:** https://bebemoss.com/collections/toys
**Page type:** Collection Page
**Reviewed:** 2026-08-18, live, mobile viewport 390x844 @2x (Chromium/Playwright)
**Slug:** `bebemoss_toys-collection`

All findings below were observed directly on the live page and confirmed in the DOM.
No estimated lift figures, no invented metrics.

---

## Finding 1 — The entire first screen is a mission paragraph. Zero products.

**What's there now:** above the fold the visitor gets a breadcrumb, the line
"Every purchase makes a difference.", and a 5-sentence brand paragraph. That text
block measures **519px tall** in a **844px** viewport. The first product link sits
at **y=671**, so the first toy only peeks in at the very bottom edge, with its
title and price still below the fold.

**Measured:** `descHeight: 519`, `firstProductTop: 671`, `viewportH: 844`.

**Why it matters:** this is a collection page. Someone who taps "Soft Toys" has
already decided they want to browse toys. The first screen answers a question they
did not ask and shows nothing they can act on.

**Fix:** move the mission paragraph below the product grid (or collapse it to a
single line with a "Read our story" link) and let the grid start at the fold.
Bebemoss's whole differentiator is that the toys are handmade, so the fastest way
to sell the mission is to show the product.

---

## Finding 2 — A "Save 10%!" widget parks on top of product cards while scrolling.

**What's there now:** a pink "Save 10%!" tab is docked bottom-left and stays there
through the whole scroll. On the product grid it sits directly over a card, hiding
that product's **title and price** ("Rocky the Sheep - white" and its price are
both covered). Its close button overlaps the neighbouring card.

**Observed:** grid screenshot at scrollY=900 — the widget covers the lower-left
card's text block completely.

**Why it matters:** the page is **8204px** tall. That widget rides along for the
whole scroll, so it obscures a different product every time the shopper stops.
The one thing a collection page exists to show is name and price.

**Fix:** move the discount tab to bottom-right clear of the card text, shrink it to
a compact pill, or trigger it on exit intent instead of docking it permanently.

---

## Finding 3 — 48 products, no filter and no sort.

**What's there now:** the collection holds **48 products** in a two-column grid on
an **8204px** page, with **no filter control and no sort control** anywhere.

**Measured:** `uniqueProducts: 48`, `hasFilter: false`, `sortEl: false`,
`docHeight: 8204`.

**Why it matters:** a shopper hunting for a gift under $60, or specifically for a
safari animal, has no route except scrolling all 48. Bebemoss already groups these
toys into named ranges (Garden Life, Safari, Ocean, Woodland, Dreams) in its own
copy, so the taxonomy exists. It's just not exposed as a control on the page.

**Fix:** a row of collection chips (All / Safari / Ocean / Woodland / Garden Life /
Dreams) pinned above the grid, plus a price sort. Uses grouping the brand already
uses in its own words.

---

## Finding 4 (secondary, technical) — The page's only H1 belongs to a popup.

The single `<h1>` in the document is **"👋 Hi there!"**, injected by the Klaviyo
signup form (`class="...klaviyo-form-richtext"`). The collection itself has no H1
naming it. "Every purchase makes a difference." renders as a lower-level heading.

Real but not visually demonstrable, so it is noted here and not used as a pin on
the public graphics.

---

## Scope taken into the rebuild

Findings 1, 2 and 3. They are the three a shopper actually feels, and all three are
visible in a single mobile screenshot pair.

## Explicitly NOT claimed

- No conversion-rate, revenue, or AOV numbers. None were measured and none exist.
- Product photography, pricing, and copy stay as Bebemoss has them.
- Finding 4 stays out of the carousel and graphics.

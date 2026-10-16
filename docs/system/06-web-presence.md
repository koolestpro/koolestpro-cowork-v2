# 06 — Web Presence

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

The destination. Every content CTA, every outbound message and every search result is supposed to land somewhere real, and this is that somewhere. The 2026-08-02 planning interview found the content system had no destination to send anyone to — no domain, no published prices, no case studies. This sub-project exists to close that.

---

## What is in it

**`site/`** — a Next.js app, the selling site. `npm run verify` is the deploy gate: it builds, serves, renders every route at 1440×900 and 390×844, and reports runtime errors, broken images, horizontal overflow, text under the 12px floor and missing metadata. It builds first and fails on a bad build, so it can never pass against stale output.

**The structure is one domain with two entry paths**, deliberately never blended:

```
INTERNATIONAL (USD, Cal.com)          NIGERIA / AFRICA (₦, WhatsApp-first)
/                                     /ng
/services/{slug}                      /ng/website
/work  /work/{slug}                   /ng/samples
/about  /book  /contact               /ng/stories
/resources  /resources/{slug}         /ng/shopify
/portfolio  /statics  /for/{slug}
```

**`site/content/`** is where everything that changes week to week lives, so adding a case study or changing a price is a data edit rather than a component edit: `services.ts`, `work.ts`, `portfolio.ts`, `resources.ts`, `comparisons.ts`, `prospects.ts`, `statics.ts`, `templates.ts`, `schema.ts`, `site.config.ts`.

**`outputs/nigeria-demo-site/`** — the D2a demo site, the thing shown before anything is built for a prospect.

**Plan of record:** `docs/koolestpro-site-build-plan.md` for the build, `docs/koolestpro-growth-operating-plan.md` Tracks A, B, F and G for the strategy.

---

## How it works

A prospect arrives from one of four places: a content CTA, an outbound DM, a search result, or a referral. International traffic lands on the main site, sees a price on every service page, and books through Cal.com. Nigerian traffic arrives by DM or ad link straight to its own pages, sees Naira, and taps WhatsApp.

**The single most repositioning decision in the whole plan** is that every service page carries a price or a range. No "contact for pricing."

---

## State

**Built:** the Next.js app with 26 routes, both market paths, the verify harness.

**Confirmed:** `koolestpro.com` is bought.

**Also done, and better than the growth plan's gap list implies (verified 2026-09-05):**

- **Prices are published.** `site/content/services.ts` carries real `priceFrom`/`priceTo` values in USD ($150-250 for one tier, $600-900 for another), not "contact for pricing." That was A2's single most repositioning requirement and it is met.
- **`/work` has 11 entries, 8 of them real clients:** Tap and Rate, Champion Biotics, Mother of Macros, Captain and Skipper, Scents Avenue, Amina Zaid, Just Darlings, Jellys Glamour. KURA, HALOS and MERIDIAN are present and explicitly flagged as concept builds, which is rule 2 being honoured rather than broken.

  **An earlier draft of this doc claimed there were no case studies. That was wrong** — it read the empty `outputs/case-studies/` folder and stopped there. The proof lives in `site/content/work.ts`, not in `outputs/`. The empty folder is a naming leftover, not a missing deliverable. Corrected here so the mistake is not inherited.

**2026-10-07:** homepage restructured after theconversioncodex.com (outcome hero, services by page type, process, revenue calculator, FAQ), nav cut to six items with an always-visible "Book a call", the market switch removed from the chrome, `/ng` made direct-response, new `/rebuilds` archive. Work wall and before/after are now data-driven and refreshed twice a month: see [site-work-refresh.md](site-work-refresh.md).

**Not done — and these are the gaps that matter:**

- **The Nigeria anchor case studies specifically.** Track B asks for three, in Naira, aimed at the `/ng` path. The 8 real clients above are the international proof. `/ng/stories` needs its own.
- **Track F, search, is planned not executed.** The keyword map, AEO/GEO work and the directory listings all exist on paper. The directories are the highest-intent free channel in the whole plan — people browsing Shopify Partners or Replo Experts are actively trying to hire — and none are listed.
- **The lead magnet does not exist.** One asset, reused everywhere: a Shopify PDP conversion checklist or a real sample audit report, producible in about an hour with `koolestpro-client-audit`.
- **Analytics.** Without at least `/book` submissions, WhatsApp clicks and per-page traffic, Track G ads can never be evaluated. That is the plan's own wording.

**Deliberately gated: ads.** Track G is documented and ready and is not running, gated on **price, not budget**. At $300-800 per project a $100-300 acquisition cost eats 15-50% of revenue; at $3,000 it is an excellent trade. The trigger is consistently closing $2,500+ projects — not a date and not a spare budget. When it fires: Google Search only, $600-800/mo, three-month minimum, exact and phrase match, negatives from day one, landing on the matching service page rather than the homepage, tracking configured before the first click. Nigeria Meta/IG ads are cheaper and worth a small test only *after* the Nigeria engine proves its close rate organically.

---

## Rules

| Rule | Where |
|---|---|
| **Every page/copy edit is humanized** (v3.0, 11 passes, `VOICE.md`-anchored) before deploy. No em dashes. | `docs/system/humanizer-guideline.md` |
| Every content CTA points at a real destination, a service page or case study, never at engagement. | `CLAUDE.md` rule 1 |
| Never invent a client result, never imply a concept brand was a client. Highest-stakes rule in the project. | `CLAUDE.md` rule 2 |
| Never blend the two markets' copy. Naira and WhatsApp on `/ng`, USD and Cal.com internationally. | `CLAUDE.md` "Two markets" |
| Every service page carries a price or a range. | Growth plan A2 |
| No keyword domain. No SEO advantage in 2026 and it signals low trust. | Growth plan A1 |
| `npm run verify` before any deploy. | `site/README.md` |
| Template Showcase CTAs say "need a store built," never "want this fixed on yours." That split is deliberate. | `CLAUDE.md` "New-Store-Build Inbound Track" |

---

## Known gaps

Ordered by how much they block everything else.

1. **No real case studies.** Blocks the site, the content CTAs and outbound credibility simultaneously.
2. **No analytics.** Makes ads unevaluable and makes every other channel unmeasurable.
3. **No directory listings.** Free, highest-intent, and nothing else in the plan has that property.
4. **No lead magnet.** An hour of work that gates email capture and doubles as an outbound attachment.
5. **TikTok build videos are dormant** — by Ridwan's own history the best-performing format he has ever run, producing three of six clients. Covered in [01 Content Production](01-content-production.md) and [02 Distribution](02-distribution.md); noted here because it is the channel that fills this destination.

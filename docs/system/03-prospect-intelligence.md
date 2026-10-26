# 03 — Prospect Intelligence

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

Finding businesses and deciding what to do with each one. It feeds two different consumers with two different needs, and the split between them is the single most important thing to understand here.

---

## What is in it

**Two pools, split by whether the prospect has an auditable URL.** This was corrected in `CLAUDE.md` rule 4 on 2026-09-04 after the original "one segmented pool with a `segment` field" rule turned out never to have been implemented and to have been superseded in practice.

| Pool | Holds | Feeds | Requires |
|---|---|---|---|
| `targets_pool.json` | 12 international DTC/Shopify brands | CRO Fix, Static Ad, Template Showcase target selection | a real, live, auditable `url` |
| KoolestFlow | Nigeria/local businesses, mostly no site | outbound DM | a contactable handle |

The pool boundary *is* the segmentation. A `segment` field would only restate which file something is in. Do not add one and do not merge the pools.

**`targets_pool.json` today:** all 12 `Available`, spread across beauty-skincare, nfc-local-business-growth, fitness-wellness, home-kitchen, fashion-apparel, baby-pet-lifestyle and food-beverage-supplements. Rotation is tracked per-stream in `usedFor`, not by `status` — a target having served one stream does not permanently exclude it from that stream later, it just deprioritises it while fresher options exist.

**Two discovery sources, both weekly, both feeding KoolestFlow:**

| Source | Task | Runs | Mechanism |
|---|---|---|---|
| Google Maps | `koolestpro-browseract-weekly` | Tue ~09:05 | BrowserAct workflow `112089423433150347`, then enrichment via Contact Finder `112098855747914891` |
| Meta Ad Library | `koolestpro-adlibrary-weekly` | Wed ~09:00 | Apify actor `curious_coder/facebook-ads-library-scraper` |

**Supporting files:** `.ai-workflow/tools/lead_playbook.py` (the Build/Fix/Scale/Marketplace track logic), `.ai-workflow/taken-brands-ledger.json` (cross-source dedupe, 14 brands taken as of 2026-09-04), `.ai-workflow/ad_library_rotation.json` and `.ai-workflow/browseract_rotation.json` (which slot runs next), plus the matching weekly log files.

**`dm_leads_pool.json`** is a historical staging log from before KoolestFlow was identified as the real destination. Not a third pool. Its remaining `NeedsContactInfo` entries can be graduated with `--from-dm-leads-pool`.

---

## How it works

Discovery returns raw businesses. Enrichment finds the website and every social profile. `score_and_qualify()` produces a `fit_score` 0-100 using conventions lifted from KoolestFlow's own `lead_engine.py`, so bridge-pushed leads score consistently with leads KoolestFlow's built-in search produces.

**The scoring is deliberately inverted from the obvious.** "Real presence, no website" scores **highest**, not lowest. Google Maps reviews or an active social profile, but no real site, is exactly the free-sample-site candidate. A business that already has a good site scores lower for this play and is logged rather than prioritised.

Every lead carries a `track`: **Build** (no site), **Fix** (weak site), **Scale** (good site), or **Marketplace** (sells on Jumia/Konga/JiJi). Build sorts first on push.

---

## State

**Live:** both discovery sources. **Working, with a scar:** the Ad Library run has real corrections baked in from a rejected first run.

Three things that were learned the hard way and must not be undone:

1. **`country=NG` alone does not scope results.** Confirmed by direct testing — flipping `is_targeted_country` produced byte-identical output. What works is putting the city as literal text in the query. `q=kids` returned Jumia and Nestlé; `q=kids Lagos` returned 10/10 genuinely Nigerian small businesses.
2. **Every NG lead must show an explicit Nigeria signal** — ₦/NGN/Naira, +234, a Nigerian mobile prefix, a city name, or a `.ng` domain — checked against the page name, the body text *and* the link. The first version of this check missed signals sitting in the page name alone.
3. **Marketplace sellers are a valid lead type, not banned.** A marketplace link is never treated as the prospect's own site, no site-quality check runs against it, and it only pushes at all above 500 page likes.

**Known blind spot, not auto-fixed:** like-count cannot distinguish a small local business from a big chain's regional page. "Burger King Nigeria" passed every filter on 5,785 likes. Every run must flag anything that reads as a recognisable chain for a human look.

---

## The build plan (approved 2026-09-04, not yet built)

Ridwan approved all four of these. Ordered cheapest and highest-certainty first.

**1. Fix Google Maps to return the website field.** The current template returns `name, full_address, star_rating, review_count, avg_price_per_person` and no website. That one missing field is why every Maps lead lands at `NeedsContactInfo` and needs a manual lookup, and why a second enrichment call is spent per lead. Swapping to an actor that returns website and phone turns "no website" from a lookup into a filter and mostly deletes the enrichment step. Lowest risk, reuses everything, pays for itself in credits.

**2. Instagram business-profile scraping.** The highest-precision source for the actual target definition: real follower count and recent posting activity, bio link a `wa.me`, a Linktree, or absent. That combination *is* "doing well, no website." It also yields the DM handle directly, which Maps never does. Runs through the Apify account already in `.env`.

**3. Jumia / Konga / JiJi seller scraping.** Real volume on someone else's platform, no owned customer relationship. Sharper pitch than a cold "you need a website." Classification logic already exists via the Marketplace track. The contact step stays manual, since marketplaces hide seller details — say so plainly rather than implying automation that will not exist.

**4. TikTok business-profile scraping.** Same signal as Instagram, different audience, matches the channel Ridwan's history says converts. Last because TikTok profile scraping is the most brittle and there is no reason to take on that maintenance until the other three are earning.

**Rules that apply to all four,** inherited from the Ad Library corrections above: city as literal text; explicit country signal required; push only through `koolestflow_client.py` so the taken-brands ledger cannot be bypassed; Build track sorts first; flag recognisable chains for human review.

---

## Rules

| Rule | Where |
|---|---|
| Two pools, split by auditable URL. No `segment` field. Do not merge. | `CLAUDE.md` rule 4 |
| A new target enters `targets_pool.json` at `visualPotential: "Unrated"` and is **never** selected for public content while Unrated. It needs a live mobile-page review first. | `targets_pool.json` `meta.recordSchema` |
| `status` should almost never become `Used`. Per-stream eligibility lives in `usedFor`. | same |
| Never bypass the taken-brands ledger by calling KoolestFlow's API directly. | Ad Library task, correction 7 |
| Nigeria-only for the Ad Library run until Ridwan says otherwise. | Ad Library task, correction 5 |
| Report exact brand names pushed and skipped with reasons, never just a count. Standing instruction from 2026-08-26. | Ad Library task, step 11 |

---

## Known gaps

- **Nothing prevents a business existing in both pools.** No collision has happened; the ledger covers the outbound side only. Flagged rather than built.
- **`leadPotential` in `dm_leads_pool.json` is an unvalidated heuristic** on rating and review count. A rough sort order, not a scoring system to trust.
- **The pool is shallow.** 12 targets across three consuming streams. `koolestpro-target-pool-refresh` (Mon ~08:18) tops it up when a stream runs low, but the depth is worth watching on the status page.

---

## 2026-10-26: the outreach scrape now feeds `targets_pool.json`

Ridwan's decision. The outreach directory scrape (merchantgenius, eachspy, zik, myip.ms Shopify page) already finds hundreds of real Shopify stores. The target pool refresh now takes candidates from it first (`outreach/scrapers/output/`), still verifying each one live under `cro-finding-rules.md`. Entries carry `source: "outreach-directory-scrape"` and `outreachLead`. This is a feed, not a merge: the Sheet keeps its copy, no `segment` field. `template-showcase` is now an active consumer of the pool, because real-store full-page redesigns (Wednesday Page B, every Sunday CRO Fix) feed the Saturday showcase. A store in both pools gets its redesign reused as the cold-email hook via `outreach/redesign-hooks.json`.

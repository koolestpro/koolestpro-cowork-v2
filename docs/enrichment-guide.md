# Enrichment Guide — What It Means and How to Do It Free

**Date:** 2026-08-31  
**For:** Koolestpro outbound pipeline

---

## What Is "Enrichment"?

Enrichment = turning a **discovered business name** into a **complete prospect record** with contact info and scoring.

### Example

| Discovery Only | After Enrichment |
|---|---|
| "AristoMan Luxury" | AristoMan Luxury, website: aristomanluxury.com, phone: +234..., rating: 4.5, 25 reviews, **Track: Scale**, fit score: 80 |

---

## Your Two Lead Types Need Different Enrichment

### Type A: Google Maps / Ad Library Leads (already automated)

These already come with:
- Business name
- Address
- Phone
- Website (sometimes)
- Rating + reviews

**What enrichment adds:**
1. **Website quality check** — is the site fast? mobile-friendly? real or placeholder?
2. **Track classification** — Build (no site) / Fix (weak site) / Scale (good site)
3. **Pitch notes** — what service to offer, what channel to use, pricing frame

**Cost: FREE.** Your existing `lead_playbook.py` does all of this automatically.

### Type B: Instagram-Only Sellers (your VA's leads)

These come with:
- Instagram handle
- Maybe a WhatsApp number in bio
- Maybe a Linktree

**What enrichment adds:**
1. **Follower count** — how big is their audience?
2. **Posting frequency** — are they active?
3. **Has website?** — check bio link / Linktree
4. **Category** — fashion, skincare, hair, food, etc.
5. **City/country** — from location tags or bio

**Cost: FREE.** Your VA does all of this manually in 30 seconds per profile. No API needed.

---

## Free Enrichment Paths (No Subscriptions)

### 1. Outscraper Maps Search (500 free/month)

**What you get:** name, address, phone, website, rating, reviews, category, hours, photos

**Already built into the response** — no separate enrichment step needed.

```bash
python3 outscraper_koolestflow_bridge.py --query "fashion boutique Lagos" --limit 20
```

### 2. Google Maps Listing Itself

The Maps listing often contains:
- Phone number
- Website link
- Business hours
- Photos
- Owner responses to reviews

**This is your primary enrichment source.** It's free and reliable.

### 3. Website Quality Check (your existing script)

```python
from lead_playbook import assess_website_quality
result = assess_website_quality("https://example.com")
# Returns: score 0-100, signals list, load time
```

**Checks:** HTTPS, mobile viewport, meta description, page size, load speed

### 4. Manual VA Enrichment (Instagram-only)

Your VA should capture in Notion:

| Field | How |
|---|---|
| Brand Name | From Instagram profile |
| Instagram URL | Direct link |
| WhatsApp | From bio or highlights |
| Followers | From profile |
| Has Website? | Check bio link / Linktree |
| City | From post locations |
| Category | Visual assessment |
| Notes | "Posts daily, uses DM orders, no checkout" |

---

## Paid Enrichment (Only If You Outgrow Free)

| Tool | What It Does | When You Need It | Cost |
|---|---|---|---|
| **Hunter.io** | Find email from domain | You have a website but no email | Free: 50/mo; $34/mo |
| **Outscraper Emails & Contacts** | Find email/phone/social from domain | Batch enrichment of 500+ domains | Free: 500/mo; then $3/1K |
| **Prospeo** | B2B email + phone | International Shopify brands | $49/mo |

**At your volume (120 leads/month), you will never pay for enrichment.**

---

## How the Pipeline Flows

```
DISCOVERY
   |
   +-- Outscraper Maps  →  name, address, phone, website, rating
   +-- Apify Ad Library →  name, ad link, page likes
   +-- VA (Instagram)   →  name, IG handle, WhatsApp, followers
   |
ENRICHMENT (free, automatic)
   |
   +-- Website? → assess_website_quality()  →  score 0-100
   +-- Has reviews? rating? phone?           →  presence signals
   +-- Category match?                       →  niche playbook
   |
CLASSIFICATION
   |
   +-- No website + real presence     →  Track: BUILD
   +-- Has website + score < 55       →  Track: FIX
   +-- Has website + score >= 55      →  Track: SCALE
   +-- No website + no presence       →  Low Priority (skip)
   |
PITCH GENERATION
   |
   +-- BUILD → "I built a free sample site for [Brand]..."
   +-- FIX   → "I reviewed [Brand]'s site. 3 quick wins..."
   +-- SCALE → "[Brand] has a solid foundation. I help [niche] brands..."
   |
KOOLESTFLOW PUSH
```

---

## Apify Enrichment Specifically

**Your question: "How do we enrich on Apify?"**

Apify is a **scraper marketplace**, not an enrichment service. You don't "enrich" with Apify — you **scrape a specific page or dataset**.

### What You Already Use Apify For

| Actor | Purpose | Cost |
|---|---|---|
| `curious_coder~facebook-ads-library-scraper` | Find businesses running Meta ads | ~$0.01/ad |

### What You Could Add (Free/Cheap)

| Actor | Purpose | Cost |
|---|---|---|
| TikTok hashtag scraper | Find social-native sellers | ~$0.05/1K videos |
| LinkedIn job post scraper | Find businesses hiring web devs | ~$0.02/post |
| Reddit scraper | Find intent signals | Already in trend-radar |

### What Apify Cannot Do

- Find email addresses from a business name alone (not reliably)
- Assess website quality (your Python script does this better)
- Classify leads by track (your `lead_playbook.py` does this)

**Verdict:** Keep Apify for **discovery** (Ad Library, TikTok, job boards). Do **enrichment** with your own free scripts and your VA.

---

## One-Page Cheat Sheet

| Task | Tool | Cost |
|---|---|---|
| Find local businesses with no website | Outscraper Maps | FREE (500/mo) |
| Find businesses running ads | Apify Ad Library | ~$0.01/ad |
| Find TikTok-only sellers | Apify TikTok scraper | ~$0.05/1K videos |
| Find Instagram-only sellers | Your VA | $3–5/hour |
| Find businesses hiring web devs | Apify job board scraper | ~$0.02/post |
| Check website quality | `lead_playbook.py` | FREE |
| Classify lead (Build/Fix/Scale) | `lead_playbook.py` | FREE |
| Generate pitch notes | `lead_playbook.py` | FREE |
| Find email from domain | Hunter (free tier) | FREE (50/mo) |
| Push to KoolestFlow | `koolestflow_client.py` | FREE |

---

**Bottom line:** At 120 leads/month, your entire enrichment layer costs $0. The only cost is discovery (BrowserAct/Apify/Outscraper = ~$25/mo) and your VA's time.

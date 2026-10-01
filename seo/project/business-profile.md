# Business profile: Koolestpro (koolestpro.com)

> Stage 0 output, built 2026-10-01 from the site repo (`koolestpro/koolestpro`: `content/*.ts`), `about-me.md` and Ubersuggest US data. Refresh by 2026-12-30. Every stage reads this first.

## 1. Identity
- **Who:** Ridwan Adekunle, Shopify CRO & UX designer (Offa, Kwara State, Nigeria). He works with international DTC Shopify brands. The `/ng` path is a separate Nigerian market and is **out of scope** for this engine.
- **Sells (prices published, `content/services.ts`):**
  | Service | Page | Price |
  |---|---|---|
  | Conversion Audit | `/services/cro-audit` | $150 to $250 |
  | Single Page Build | `/services/page-build` | $600 to $900 |
  | Full Store Build | `/services/store-build` | $1,200 to $1,800 |
- **Conversion points:** Calendly 30-min intro call (`/book`), WhatsApp, `info@koolestpro.com`, `/offer`.
- **Proof** (`/work`, `content/work.ts`): real clients Tap and Rate, Champion Biotics, Mother of Macros, Captain and Skipper, Scents Avenue, Amina Zaid, Just Darlings, Jellys Glamour. **KURA, HALOS and MERIDIAN are concept builds and must always be labelled as such** (project rule 2).
- **Other assets:** `/portfolio`, `/statics`, comparison pages `/for/{slug}` (obvi, gainful, materialkitchen, bebemoss), and 4 resource articles (Replo vs PageFly, Replo vs Shogun, Instant vs Replo, Hire a Replo developer).

## 2. Audience
DTC Shopify founders and small e-com teams (US/UK/EU) who are running paid traffic or launching products. They're deciding which page builder to use, whether to hire a freelancer or an agency, and why their store doesn't convert. Their objections: cost, trust in an offshore freelancer, timeline, and "will it actually lift conversion".

## 3. Voice (from the existing resources)
First person, practitioner, blunt and honest. "Written by someone who has shipped client pages in both and has no referral relationship with either." Short answers first, and opinions backed by building experience. No vendor copy restated.
- Every H2 is a question a person would type, and the first sentence answers it in under 40 words (the site's own article rule in `content/resources.ts`).
- Pricing policy: approximate price bands only, with a `pricesCheckedOn` date and a link to the vendor's page.
- Project voice rules apply: `VOICE.md` blocklist, no em dashes, full humanizer pass.

## 4. Search footprint (Ubersuggest US, 2026-10-01)
Domain authority **1**, 2 backlinks (both nofollow), **0 ranking keywords, 0 organic traffic**. The site is new, which shapes the strategy:
- Target **very low difficulty, high-intent long-tail** (tool vs tool, "hire a X developer", "X not working", specific how-tos) where a practitioner's page can rank on relevance alone.
- **Link building matters more than volume of posts here.** Every article should be linkable (original screenshots, real build times, tables), and outreach runs every week.
- AI answer engines (ChatGPT/Perplexity/AI Overviews) are a realistic early channel. The site already ships `llms.txt` and FAQ/Article schema.

## 5. What makes Koolestpro unique
1. A builder who actually ships in Replo, Instant, PageFly, Shogun and Liquid, so the comparisons come from hands-on use, not affiliate copy.
2. Prices published up front (rare among freelancers and agencies).
3. CRO-led: every build starts from a conversion audit, and the weekly public CRO fixes on LinkedIn/X are the proof of method.
4. A real client roster with long relationships (Tap and Rate and Champion Biotics, both 1+ year).
5. Fast, small-team turnaround at freelancer prices.

## 6. Claims
**OK:** published prices above. Client names on `/work` with their stated scope. Build-time ranges stated in existing articles ("five to eight working days").
**Never:** invented conversion lifts or revenue numbers for any client. Implying concept brands are clients. Exact vendor prices stated as fact.

## 7. Site issues for the engine
- **Inline links are not supported in article paragraphs** (`Block` `p` is plain text). Internal links can only go through `cta` and the "more" list. Fix: add `[text](/path)` support to the `p`, `ul` and `callout` renderers in `app/resources/[slug]/page.tsx`. Until that's done, briefs put internal links in `callout` blocks and the CTA only.
- No `image` field on `Article` (OG images are generated). The image stage is skipped for this client unless the site adds one.

## 8. Cluster seeds
See `clusters.md`.

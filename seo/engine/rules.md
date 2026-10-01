# SEO house rules (every stage reads this)

Portable: the same in every project. Where they conflict with the host project's own rulebook (e.g. its `CLAUDE.md`), the host wins.

## 1. Business first
- **Personalisation rule.** Every recommendation is tailored to the client's real products, collections, audience, voice and site structure, as recorded in `seo/project/business-profile.md`. If a sentence could appear on any competitor's blog, rewrite it until it could only be this brand's.
- **Read the profile before every stage.** No stage runs without it. If it is older than 90 days, or the catalogue has changed a lot (`store_snapshot.py` diff), refresh it first.
- **Competitor rule.** Competitors show market patterns. Never copy them. Where offers overlap, lead with what is unique to this client: positioning, product range, pricing model, service, voice.
- **Facts only.** Prices, product names, features, shipping promises, review counts and guarantees come from the live site or the profile. Never invent a stat, testimonial, customer name, case study or result. A source that can't be verified gets left out.

## 2. Site first, data first
- **Quick wins before new content.** Each week, check GSC before picking a new topic. A page with high impressions and low CTR, or one sitting at positions 8 to 20, can be fixed in 20 minutes and is often worth more than a new post. Up to one quick win per week goes into the run as well as the new article.
- **Data priority.** Order of trust: GSC queries and pages → GA4 landing-page engagement and conversions → Keyword Planner volumes (free) or the project's DataForSEO account → Google Autocomplete (real phrasing, no volumes) → Ubersuggest if connected → general web research. A keyword with no volume data is ranked on intent and GSC impressions, never on a guessed number.
- **Intent over volume.** Never pick a keyword for volume alone. A 50-searches-a-month query with buying intent beats a 6,600 query with the wrong intent (example: an NFC review-card store ranking for "google cards", where searchers want Google Play gift cards).
- **Wrong-intent traffic is a finding, not a win.** Flag it in the report, and don't build content to chase it.

## 3. Topic scoring (1 to 5 each, max 30)
| Factor | 5 means |
|---|---|
| Intent strength | Commercial or transactional, or high-intent informational ("how to get more Google reviews") |
| Revenue relevance | Leads directly to a best-selling product, bundle or subscription |
| Current traction | GSC already shows impressions for this query or close variants |
| Ranking opportunity | Low difficulty (SD), or the client already ranks 8 to 30 |
| Internal-link potential | 2+ existing pages can link in, and it links out to a money page |
| Uniqueness | The client can say something competitors can't (their own product, data, tool or service) |

Only the top-scoring topic goes to the brief stage. Every score is shown in the run notes, so the choice can be checked.

## 4. Clusters and journey stages
- Every article belongs to **one cluster** in `seo/project/clusters.md`, and each cluster supports one money page (a collection, product or service page).
- Every article targets **one journey stage**:
  - **Awareness:** problem-aware ("why don't customers leave reviews").
  - **Consideration:** comparing options ("NFC card vs QR code").
  - **Decision:** product-specific ("best Google review stand for a salon").
  - **Post-purchase:** setup and troubleshooting ("how to set up your NFC review card").
- Keep the stages in balance over 90 days. Not every post can be Awareness.

## 5. Internal links (every article)
- Link out to 1 to 3 money pages (collection or product) with descriptive anchors. Never "click here".
- Link out to 1 to 2 related articles in the same cluster.
- Name 2+ existing pages that should link **in** to the new post. These go in the run notes as manual edits for the site owner, because the system does not edit live pages.
- Only link to URLs that exist. Check them against `store_snapshot.py` output.

## 6. CTAs by stage
| Stage | CTA |
|---|---|
| Awareness | Free tool (calculator / QR generator), a related guide, or email signup |
| Consideration | Compare products, view collection |
| Decision | Product page, bundle, custom order, bulk quote |
| Post-purchase | Setup guide, add-ons, review-management upsell |

Place CTAs early (after the first answer), mid-article and at the end.

## 7. On-page requirements
- SEO title ≤ 60 chars, with the keyword near the front, written to get the click.
- Meta description ≤ 155 chars, with the keyword plus a clear benefit or CTA.
- One H1. The keyword goes in the H1, the first 100 words, at least one H2 and the conclusion. Keep it natural, never stuffed.
- Answer first: each H2 opens with the direct answer in 1 to 2 sentences. This also helps AI Overviews and featured snippets (see the `ai-seo` and `seo-geo-aeo` skills).
- Short paragraphs (≤ 3 sentences). Use lists and tables where they help.
- FAQ block with 3 to 5 real questions (from GSC queries, People Also Ask, or the site's own FAQ page) plus FAQPage JSON-LD in the body HTML.
- Featured image with descriptive alt text. Under 200 KB if possible, landscape 1200×628 or larger.
- British English for UK clients (colour, optimise, £).

## 8. Copy rules (project-wide, non-negotiable)
- No em dashes (`—`, `&mdash;`). Scan the final HTML for them.
- Full humanizer pass: the host project's humanizer skill/guideline if it has one, otherwise this checklist. Cut significance inflation ("pivotal", "testament", "landscape"), promotional filler ("seamless", "unlock", "elevate"), "-ing" tack-ons ("highlighting…", "ensuring…"), "not just X, it's Y", forced groups of three, signposting ("let's dive in", "here's what you need to know"), bold inline-header lists, generic upbeat endings, and any stat or claim without a source. Vary sentence length and keep the business's own phrasing.
- No hype words the business wouldn't use. Write the way they talk to customers.

## 9. Measurement and decisions
Track every post the same way, weekly, in `performance-log.csv`: impressions, clicks, CTR, avg position, organic sessions, engagement time, conversions/revenue (GA4).

| Signal (after 28+ days) | Action |
|---|---|
| High impressions, CTR < 2% | Rewrite title + meta (quick win) |
| Position 8 to 20, decent CTR | Expand the content, add FAQ, add internal links in |
| Traffic but no conversions | Stronger CTA, closer product linkage |
| Converting | Write adjacent cluster content, and point more internal links at it |
| < 50 impressions after 90 days | Merge into a stronger post, re-target, or retire |

**Refresh schedule:** each post gets checked at 30 and 90 days. The weekly report lists posts that are due.

## 10. Off-page / link building
- Every outreach target is tied to one target page and one cluster.
- Priority order: unlinked brand mentions → suppliers/partners/platform directories (e.g. booking platforms the products support) → resource pages → niche blogs and trade publications for the business's customers → roundups/"best of" → digital PR (journalist requests) → broken-link replacement.
- Linkable assets come first. Pitch the client's free tools and data, not product pages.
- Pitches are short, personal, specific to the prospect's page, and humanized. They go to the project's outreach system (`outreach.mode`: Sheet, Gmail drafts or CSV) **unapproved**. Nothing is sent until a person approves it. Step 1 has no link: offer the resource, and send the link when they reply.
- Never buy links, never use PBNs, never mass-blast.
- Log every prospect in `outreach-log.csv`.

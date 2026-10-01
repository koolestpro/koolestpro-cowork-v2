# Stage 0: Business profile (run once per client, refresh every 90 days)

**Inputs:** `clients/<slug>/client.json`, `clients/<slug>/snapshot/*` (from `store_snapshot.py`), the live homepage, About, FAQ, How it works, 3 to 5 best-selling product pages, the existing blog posts (or, for `nextjs-resources`, the site repo's `content/*.ts`), `dataforseo.py ranked` + `competitors` + `backlinks` (Ubersuggest `domain_overview` / `domain_keywords` / `competitors` as fallback; location from client.json).
**Output:** `clients/<slug>/business-profile.md` (overwrite; keep the old one as `business-profile.<date>.bak.md`).

---

You are an SEO strategist, conversion copywriter and brand analyst. Before any content is planned for this store, you build the reference every later stage will rely on. Use only what you can see on the live site and in the data provided. Where something can't be confirmed, mark it `UNVERIFIED` rather than guessing.

Produce these sections:

1. **Store identity:** what it sells, the problem it solves, who it serves, category, country/market, currency, language variant.
2. **Products and offers:** main collections (with URLs), best sellers or featured products (with URLs and price ranges), pricing model (one-off vs subscription), bundles, custom/bulk options, free tools, add-ons. Key features, benefits and use cases, using the store's own wording.
3. **Customers:** segments by business type, with the evidence for each (collections, product names, copy). Their pains and objections, and the questions on the FAQ page.
4. **Brand and site:** voice (5 adjectives, 3 example phrases quoted from the site, and words they would never use), visual style (colours, photography style, tone of imagery), navigation structure, conversion points (cart, quote form, trial, calculator), existing blog themes and quality.
5. **Search footprint:** domain authority, organic traffic trend, top ranking keywords, and a split of **right-intent** vs **wrong-intent** traffic. Pages already earning impressions.
6. **Competitive position:** 3 to 6 real competitors, what everyone in the market says, and what only this store can say. List each differentiator with its proof on the site.
7. **What makes this brand unique:** 5 to 8 bullets. Every article must reflect at least one of them.
8. **Claims we can use:** exact claims from the site (e.g. "No subscription, one-off cost") with the URL. Claims we must NOT make (anything unverified).
9. **Site issues spotted:** technical, trust or content problems seen while profiling (placeholder text, thin pages, duplicate collections, broken pages). These feed quick wins.
10. **Cluster seeds:** 4 to 6 proposed content clusters, each tied to one money page. Copy these into `clusters.md`.

Rules: no em dashes, plain language, cite a URL for every factual claim. The profile is for internal use, so be blunt.

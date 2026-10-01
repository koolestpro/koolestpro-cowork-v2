# Stage 2: Topic selection

**Inputs:** `business-profile.md`, `clusters.md`, `content-log.csv`, `snapshot/blogs.json`, `gsc.json`, DataForSEO keyword data (`ideas` on the cluster seeds, `gap` per competitor; Ubersuggest as fallback), `quick-wins.md`.
**Output:** `runs/<date>/topic.md`

---

You are an SEO strategist for this specific store. Pick the single best article to write this week, for business value first and SEO opportunity second.

1. List 10 to 15 candidates. For each give: working title, primary keyword, 3 to 5 supporting keywords, monthly volume + difficulty + intent (DataForSEO, or Ubersuggest), GSC impressions if any, intent (informational / commercial / transactional), journey stage, cluster, money page it supports, format (guide, how-to, comparison, best-X-for-Y, troubleshooting, checklist).
2. Score each 1 to 5 on: intent strength, revenue relevance, current traction, ranking opportunity, internal-link potential, uniqueness (see `seo-rules.md §3`). Total out of 30.
3. Drop any candidate that:
   - is already covered by a live post or one in `content-log.csv` (cannibalisation),
   - targets wrong-intent traffic (e.g. gift-card shoppers),
   - can't be tied to a real product, collection, tool or service on the site.
4. Check the 90-day balance across journey stages in `content-log.csv`. Break ties in favour of the under-served stage.
5. Pick the winner. Explain in 2 sentences why it can convert even if volume is low, and which "unique" point from the profile it will lead with.

Output: the scoring table (sorted), then the winner block: keyword, supporting keywords, intent, stage, cluster, money page URL, format, target word count, angle (one sentence).
No em dashes.

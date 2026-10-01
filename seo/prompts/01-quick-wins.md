# Stage 1: Quick wins

**Inputs:** `runs/<date>/gsc.json` (pages + queries, last 28 days, with the previous 28 for comparison), `ga4.json` if present, `content-log.csv`, `business-profile.md`, snapshot.
**Output:** `runs/<date>/quick-wins.md`

---

You are an SEO analyst. Before any new content gets written, find the existing pages where a small change will move results fastest.

Find and rank (max 3):
1. **CTR fixes:** pages with ≥ 100 impressions and CTR below what their average position should earn (rough benchmark: pos 1 ≈ 25%, 3 ≈ 10%, 5 ≈ 5%, 10 ≈ 2%). Write a new SEO title (≤ 60) and meta (≤ 155) that match the top queries for that page, using real product facts.
2. **Striking distance:** queries at position 8 to 20 with meaningful impressions. Say what to add to the ranking page (section, FAQ, internal link in, better H2 match).
3. **Decay:** pages whose clicks dropped > 30% against the previous period. Give the likely cause and the fix.
4. **Wrong intent:** pages pulling traffic for queries the business can't serve. Recommend re-targeting the title/meta, or leaving it alone.
5. **Converting pages** (GA4): landing pages with conversions. These become link targets and inspiration for cluster topics.

For each item give: URL, evidence (numbers), the exact change (before → after text), expected effect, effort (minutes).
Pick **one** as "Do this week".

No GSC data? Say so, use Ubersuggest position data, and mark the confidence as low.
No em dashes. Never edit live pages. These are instructions for Ridwan.

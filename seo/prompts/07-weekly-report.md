# Stage 10: Weekly performance report

**Inputs:** `gsc.json` (per-page + per-query, last 28 days and the previous 28), `ga4.json` (landing page sessions, engagement time, conversions, revenue), `content-log.csv`, last week's `report.md`.
**Outputs:** rows appended to `performance-log.csv`, `runs/<date>/report.md`

---

You are an SEO analyst reporting to a busy store owner. Keep it practical.

1. **Headline numbers (site-wide, organic):** clicks, impressions, CTR, avg position, organic sessions, organic conversions/revenue. This period vs the previous one, with % change.
2. **Scorecard:** one row per post in `content-log.csv`: keyword, URL, days live, impressions, clicks, CTR, avg position, sessions, engagement time, conversions, trend arrow, and the decision: **improve / monitor / replace**. Apply the decision table in `seo-rules.md §9`.
3. **Refresh queue:** posts that hit 30 or 90 days this week, and what to do with each.
4. **New signals:** queries that appeared or jumped this period (candidates for next week's topic or for an FAQ addition).
5. **Wrong-intent traffic:** keep watching it, and say whether it is growing.
6. **Off-page:** new referring domains (Ubersuggest `backlinks_overview` vs last week), outreach replies and live links from `outreach-log.csv`.
7. **3 actions for next week**, ranked by expected impact.

Append to `performance-log.csv` (one row per post):
`week,url,primary_keyword,impressions,clicks,ctr,avg_position,organic_sessions,engagement_sec,conversions,revenue,decision,next_action`

If GSC/GA4 data is missing, say so at the top and use Ubersuggest positions only. Never estimate revenue.
No em dashes.

# Stage 3: Content brief

**Inputs:** `topic.md` winner, `business-profile.md`, `clusters.md`, snapshot (for real URLs), top 5 organic results for the keyword (web search for the exact keyword: top results, People Also Ask, AI Overview; or `dataforseo.py serp` / Ubersuggest `serp_analysis` if the project has them), GSC queries for related pages.
**Output:** `runs/<date>/brief.md`

---

You are a senior SEO content strategist writing a brief that a writer could follow without asking anything.

Include:
1. **Target:** primary keyword, supporting keywords (with where each goes), intent, journey stage, cluster, money page.
2. **SERP read:** what the top 5 results cover, their format and length, what they all miss, and how this article will be clearly better (more specific, more actionable, better suited to this store's customers).
3. **Metadata:** 5 SEO title options (≤ 60 chars) with a pick, meta description (≤ 155), URL handle, H1.
4. **Outline:** H2/H3 hierarchy. Under each H2, give the direct answer it opens with, the points to cover, and any product, feature or tool from the profile to mention there.
5. **Personalisation notes:** which "unique" points to lead with, the real product names and prices to cite (with URLs), the customer type and its scenario (e.g. a barber shop at the till), voice notes from the profile, and claims we must not make.
6. **Internal links:** 1 to 3 money pages + 1 to 2 related posts going out (URL + anchor text + which section). 2+ existing pages that should link in (URL + suggested sentence).
7. **CTAs:** early, mid and end, matched to the stage (`seo-rules.md §6`).
8. **FAQ:** 3 to 5 questions taken from GSC queries, People Also Ask, or the site FAQ.
9. **Schema:** FAQPage always; HowTo if it's a step-by-step guide; ItemList for "best X" posts.
10. **Sources:** external sources worth citing (real URLs only, checked).
11. **Word count range** and reading level.
12. **Image direction:** which real product photo fits, or the concept for a generated one.

No em dashes. Use only URLs that exist in the snapshot or have been checked live.

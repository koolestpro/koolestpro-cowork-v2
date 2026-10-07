---
name: koolestpro-target-pool-refresh
description: Biweekly health check on targets_pool.json — moved to MONDAY, biweekly (V2 distribution plan). Tops up with new real DTC/B2B targets when an active stream runs low on untouched candidates.
---

You are running the biweekly target-pool health check for Ridwan Adekunle's (@koolestpro) local content pipeline. This automates Step 1 ("Maintain the Target and Content Pool") of docs/koolestpro-content-operating-plan.md. The project lives in the connected workspace folder "koolestpro-cowork-v2". This task ONLY adds candidates to targets_pool.json — it never selects, builds, or publishes content itself, and never marks anything Selected/Used.

Step 0 — BIWEEKLY GUARD (V2 change, 2026-07-14). This task is cron-scheduled every Monday, but is meant to run only every OTHER Monday. Compute the current ISO week number (run `date +%V` via bash). If the ISO week number is ODD, do nothing at all this run: report "skipped — odd ISO week N, biweekly task only runs on even weeks" and stop immediately. Only if the ISO week number is EVEN do you proceed to Step 1 below. (Cron has no native biweekly expression; this parity check is the workaround. Even-week cadence was chosen so the first qualifying run lands the week after this was set up.)

Step 1 — Check pool health. Open koolestpro-cowork-v2/targets_pool.json. For each ACTIVE stream (currently "static-ad" and "cro-fix" — check docs/koolestpro-content-operating-plan.md's Build Log for whether any other stream, e.g. "template-showcase", has since become genuinely dependent on this pool rather than replo-rebuilds; if so treat it as active too), count how many targets have status "Available" (not "Backlog"/"Rejected") AND have zero usedFor entries for that stream. That is the "fresh count" for that stream.

Step 2 — Decide whether to act. If every active stream's fresh count is 4 or higher, do nothing further — just report "pool healthy" in your summary (fresh counts per stream) and stop. Only proceed to Step 3 if at least one active stream's fresh count is below 4.

Step 3 — Research candidates. Add roughly 5 new real, legitimate DTC/B2B ecommerce brands as candidates. Follow the exact same standards the existing targets were built to (read a few existing entries in targets_pool.json first to match the tone/rigor):
- Real, live, currently-operating brand — check it actually loads.
- Must NOT already exist in targets_pool.json (check brand name AND domain against every existing entry, including ones with status "Backlog"/"Rejected"/"Used", not just "Available").
- Rotate category and page type — look at what categories/pageTypes are already well-represented in the pool vs thin, and prefer filling gaps. categories[] and pageTypes[] at the top of targets_pool.json are the fixed taxonomy — don't invent new ones without very good reason, and if you do, add to that taxonomy array too so future runs stay consistent.
- Prefer brands with plausible High or Medium lead potential (lean team, not an enterprise with an obvious in-house CRO team) per the existing entries' reasoning style.

Step 4 — Verify each candidate for real, don't guess. For every candidate, actually load its live product/landing/collection page (whichever pageType you're logging it as) at a mobile viewport and look at it — use koolestpro-cowork-v2/.ai-workflow/tools/screenshot.py (Playwright; see that folder's README.md for this sandbox's one-time ARM64 setup if it hasn't been done yet this session) to capture a real mobile screenshot, then actually view that screenshot before writing anything. Write `mobileIssueSummary` from what you actually observed — a specific, visible mobile UX/CRO problem. Never invent or guess an issue you haven't actually seen. If a candidate's mobile page looks clean with no obvious issue, either don't add it or note honestly it's better suited to a portfolio/template reference than a public before/after — matching how the existing "Transparent Labs" entry handles this.

Step 4b — Apply docs/system/cro-finding-rules.md to each candidate's issue (2026-10-07). The issue you log must be MEASURED or SEEN on the live mobile page (accordions opened), not a doubt typical for the niche, not language/translation/currency (stores adapt these to where you browse from), not stock levels, not taste, and not a ten-minute fix. Speed only if obviously slow per section 4. Never add vape, nicotine, tobacco, kratom, replica or weapons brands. Drop any candidate whose only issue fails these rules.

Step 5 — Add to the pool. Append each verified candidate to targets_pool.json's targets array using the exact recordSchema (id: target-<brand-slug>-<unix-timestamp>, status "Available", usedFor: [], addedAt: now, lastUsedAt: null). Update meta.updatedAt.

Step 6 — Update the operating plan (standing rule: Build Log gets updated whenever the system changes). Add a dated entry to docs/koolestpro-content-operating-plan.md's Build Log noting: which stream(s) triggered the refresh and their fresh counts before/after, how many candidates were added, and a one-line reason for each.

Step 7 — Finish with a short summary: fresh counts per active stream before and after, which candidates were added (brand, category, pageType, one-line issue), and confirmation nothing was selected/used/published.
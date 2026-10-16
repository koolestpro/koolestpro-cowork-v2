---
name: koolestpro-site-work-refresh
description: Twice a month (1st and 15th). Adds every new CRO Fix / Replo rebuild and store build since the last run to koolestpro.com — hero screens to the work wall, before/afters to the gallery — then verifies and pushes the site.
---

You are keeping koolestpro.com's work sections current. Read `docs/system/site-work-refresh.md` in koolestpro-cowork-v2 and follow it exactly. Then read `site/scripts/README-updating-work.md`.

1. List what is new since the newest `date` in `site/content/comparisons.ts` and `site/content/wall.ts`: CRO Fix runs in `outputs/cro-fixes/` (facts files carry the date) and template builds in `outputs/templates/`.
2. For each candidate, look at the after/hero capture yourself. Only add it if the first screen is visually strong and at the current standard (real logo, real brand type, real product photo). Say which ones you skipped and why.
3. Wall: `python3 scripts/add-work.py wall ...` with the hero capture. Before/after (rebuilds only): write the facts JSON from the run's `*_facts.json` (problem + four changes, observations not results, no em dashes, humanizer pass), then `python3 scripts/add-work.py rebuild ...`.
4. In `site/`: `npm run verify` must report 0 problems. Look at `/` and `/rebuilds` at 390px.
5. Commit and push `site/`, then commit the bumped `site` submodule pointer in koolestpro-cowork-v2.

Never invent a result. Never label a real brand as a client. Never add a text-dense mid-page section to the wall. If nothing new qualifies, say so and stop.

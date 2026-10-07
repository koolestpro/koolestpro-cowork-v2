# Site work refresh — keeping koolestpro.com current with new builds

**Part of** [06 Web Presence](06-web-presence.md). Set up 2026-10-07 (Ridwan): every new CRO Fix rebuild and every new Replo/store-template build should reach the site, so it keeps growing instead of showing the same old screens.

## What goes where

| Site surface | Data file (in `site/`) | Takes |
|---|---|---|
| Work wall ("Pages I have built", homepage + `/ng` + `/portfolio`) | `content/wall.ts` | The **hero / first screen** of a page only, and only if it is visually strong. No text-dense sections, no captions, no "concept" tags. |
| Before / after ("Same visitors. Better page.") | `content/comparisons.ts` | CRO Fix or Replo rebuilds at the current standard. Homepage shows the newest 5 automatically; every rebuild stays on `/rebuilds`. |

Both sort by `date`, newest first, so a new entry goes to the front and the oldest drops off the homepage by itself. `llms.txt` and the sitemap regenerate from the same data.

**Retired 2026-10-07:** the Obvi, Gainful, Material Kitchen and Bebemoss before/afters (old standard, wrong logos). The set now starts at Caraway (the Lovable version, `_capture/caraway_v2/caraway_v2-mobile.png`, not the dark half-screen-image version), then Kyte Baby, Minimalist, Fly By Jing.

## The command

From `site/`:

```bash
# hero to the wall (390px-wide mobile capture, any scale)
python3 scripts/add-work.py wall --src ../outputs/cro-fixes/{brand}/_assets/{brand}_after_raw.png \
  --slug {brand}-hero --alt "<screen description, no client claim>" --date YYYY-MM-DD

# before/after pair (facts JSON: slug, brand, page, date, problem, changes[])
python3 scripts/add-work.py rebuild --before ..._before_raw.png --after ..._after_raw.png --facts rebuild.json
```

Sources: CRO Fix runs leave `outputs/cro-fixes/{brand}/_assets/*_before_raw.png` / `*_after_raw.png`; store templates leave `outputs/templates/{slug}/work/raw-mobile-1.png` (use `--top` to skip the demo banner).

Full detail: `site/scripts/README-updating-work.md`.

## Rules

- Hero only, visually strong only. If it would not make a stranger stop scrolling, skip it.
- `problem` / `changes` are observations about the two pages, never results. No em dashes; humanizer pass.
- Real brands on `/rebuilds` keep the "not a client, rebuilt uninvited" line (the page renders it). Concept brands stay named as concept on `/work` and in the footer; the wall itself carries no names at all.
- `npm run verify` must report 0 problems before pushing `site/`, then bump the `site` submodule pointer here.

## Cadence

Twice a month (`scheduled-tasks/desktop/koolestpro-site-work-refresh`): add every rebuild and build finished since the last run that meets the bar. A CRO Fix run may also add its own rebuild the same day.

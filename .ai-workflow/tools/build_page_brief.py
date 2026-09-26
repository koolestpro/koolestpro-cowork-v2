#!/usr/bin/env python3
"""build_page_brief.py - generate a paste-ready page rebuild brief (2026-09-13).

The input side of the Lovable / Figma Make handoff. Those tools do not read this
repo, so a rebuild starts by handing them a brief. This turns a small per-build
facts JSON into a complete, paste-ready prompt that already carries this
project's redesign standard (see docs/system/cro-redesign-standard.md) and the
no-fabrication rules.

Flow:
  build_page_brief.py  ->  paste into Lovable / Figma Make  ->  publish
                       ->  capture_page.py  ->  carousel / recap builders

Usage:
  python3 build_page_brief.py --facts outputs/cro-fixes/caraway_fry-pan-pdp_facts.json \\
      --out outputs/cro-fixes/caraway_fry-pan-pdp_build-brief.md
  python3 build_page_brief.py --facts <facts.json>            # prints to stdout

Facts JSON shape (only brand, page, url, job, facts are required):
{
  "brand": "Caraway",
  "page": "Fry Pan PDP",
  "url": "https://www.carawayhome.com/products/fry-pan",
  "surface": "mobile product page",
  "audience": "home cooks who want non-toxic cookware",
  "job": "make the first screen carry the whole buy decision",
  "facts": ["$125", "18,886 reviews"],
  "verify": ["star rating: 4.7 (confirm live)", "review count: 18,886 vs 18,878"],
  "headline_options": ["No PFAS. No sticking. Nothing to worry about."],
  "benefits": ["Cooks evenly on induction", "Oven safe to 550F"],
  "assurances": ["Free shipping over $90", "Free returns", "30-day trial"],
  "assets": [{"name": "Real logo (SVG)", "path": ".../logo.svg"}],
  "sections": ["1. slim promo strip"],
  "avoid": ["the full-screen email popup", "5 solid stars if the rating is 4.7"]
}
"""
import argparse
import json
import sys
from pathlib import Path


def _bullets(items, prefix="- "):
    return "\n".join(f"{prefix}{i}" for i in items) if items else "- (none provided)"


def render(f: dict) -> str:
    brand = f.get("brand", "Brand")
    page = f.get("page", "page")
    url = f.get("url", "")

    # The headline is the whole point of the standard, so it is called out.
    heads = f.get("headline_options") or []
    head_block = "\n".join(f"  {i+1}. {h}" for i, h in enumerate(heads)) or "  (none provided)"

    assets = f.get("assets") or []
    asset_lines = []
    for a in assets:
        path = f"  [{a.get('path','')}]" if a.get("path") else ""
        note = f" - {a['note']}" if a.get("note") else ""
        asset_lines.append(f"- {a.get('name','asset')}{path}{note}")

    img = f.get("image") or {}
    img_note = ""
    if img:
        img_note = (
            "\nPer-build decision:\n"
            f"- Plan: {img.get('plan','(fill in)')}\n"
            f"- Site photo: {img.get('site_photo','check the site for a usable hero photo')}\n"
            f"- Decision: {img.get('decision','use a site photo only if it is great, otherwise generate one with AI')}\n"
            f"- Note: {img.get('note','')}\n"
        )

    return f"""# {brand} - {page} rebuild brief

Paste everything below into Lovable or Figma Make as the project prompt.
Then publish, and pull it back with `.ai-workflow/tools/capture_page.py`.

---

Build me a {f.get('surface','mobile product page')} for **{brand}**, page: {page}.
Source of truth for the real page: {url}

Audience: {f.get('audience','the store shopper')}
The one job of this page: **{f.get('job','carry the whole buy decision on the first screen')}**.

## Non-negotiable rules

- Use ONLY the real facts listed below. Invent nothing. No invented numbers,
  quotes, guarantees, or results.
- Mobile first, design at a 390px viewport.
- The real brand logo and the real product photo must be used as-is. Never
  recreate or redraw a logo.
- No gradient text (CSS or SVG).
- The first screen must carry the whole decision: outcome headline, price,
  rating and review count, benefit reasons, a trust row, and the add to cart.

## Image decision (do this BEFORE you build)

Decide the hero image after the plan, not before. Steps:

1. Write the build plan first (the sections below).
2. Look for a usable hero photo on the site. If there is a great one, use it.
3. If there is no good photo, or nothing is good enough, generate a suitable
   version with AI and build the page on that image.
4. A homepage uses the same process as a product page.
{img_note}

## Real facts to use (traceable to the live page)

{_bullets(f.get('facts') or [])}

Verify before publishing:

{_bullets(f.get('verify') or [], prefix='- [ ] ')}

## Outcome headline options (pick one, or improve on it)

{head_block}

## Benefit reasons (real, on the product)

{_bullets(f.get('benefits') or [])}

## Trust row (next to the add to cart)

{_bullets(f.get('assurances') or [])}

## Sections, top to bottom

{_bullets(f.get('sections') or [])}

## Assets to upload

{chr(10).join(asset_lines) if asset_lines else '- (none provided)'}

## Do not

{_bullets(f.get('avoid') or [])}

## Output

A finished, responsive {f.get('surface','mobile product page')} I can publish and screenshot at
390x844. Real copy only. Tell me if any fact above is missing or contradictory
instead of guessing.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", required=True, help="path to the per-build facts JSON")
    ap.add_argument("--out", help="write to this file instead of stdout")
    args = ap.parse_args()

    data = json.loads(Path(args.facts).read_text(encoding="utf-8"))
    text = render(data)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out} ({len(text):,} chars)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()

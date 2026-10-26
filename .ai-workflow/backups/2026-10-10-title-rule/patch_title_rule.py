import os, shutil, sys, re
root = os.path.expanduser('~/mnt/koolestpro-cowork-v2')
bk = os.path.join(root, '.ai-workflow/backups/2026-10-10-title-rule')
os.makedirs(bk, exist_ok=True)

RULE = ("**Product title rule (2026-10-10, Ridwan).** On every product page rebuild, the real product "
        "title from the live page (size or variant included) is the page's only `<h1>`. It sits at the top of "
        "the first screen, under the header and breadcrumb, above the price, bold, at least 22px. The outcome "
        "line never replaces it, is never the `<h1>`, and is never larger than the title: it becomes an eyebrow "
        "or a one to two line subhead. Shoppers need to see what the product is, and the real title carries the "
        "page's SEO. Homepages and landing pages are exempt: the outcome headline is their H1.")

def edit(rel, pairs):
    p = os.path.join(root, rel)
    s = open(p, encoding='utf-8').read()
    shutil.copy2(p, os.path.join(bk, rel.replace('/', '__')))
    for old, new in pairs:
        if s.count(old) != 1:
            sys.exit(f'ANCHOR PROBLEM in {rel}: count={s.count(old)} for: {old[:70]!r}')
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s)
    print('patched', rel)

# 1. redesign standard
edit('docs/system/cro-redesign-standard.md', [
 ("after moves everything a shopper needs onto the hero image itself: a value headline, social",
  "after moves everything a shopper needs onto the hero image itself: the product title, a value line, social"),
 ("scrim (gradient overlay or solid band). Over it: value headline, proof,",
  "scrim (gradient overlay or solid band). Over it: product title (H1), value line, proof,"),
 ("""2. **Value headline, not the product name.** The headline states the outcome in the
   shopper's words ("Nourish Your Day, Naturally."), not the SKU. The product name can sit
   smaller above or below it. Max 2 lines at display weight.""",
  """2. **Product title first, then the value line.** """ + RULE + """ The value line states the
   outcome in the shopper's words ("Nourish Your Day, Naturally."), max 2 lines, directly
   under the title."""),
 ("| 2 | Value headline | product name only | benefit line somewhere | outcome headline over hero |",
  "| 2 | Title + value line | title missing, or slogan is the H1 | title present but small, or not the H1 | real title as the only H1 at the top, outcome line as subhead |"),
 ("- [ ] Is the headline an outcome, not the product name?",
  "- [ ] Is the real product title the only `<h1>`, at the top of the first screen, above the price, at least 22px, and not outranked by the slogan?\n- [ ] Is the outcome line a subhead under the title, not a replacement for it?"),
 ("- A split layout where the hero is decoration and the value prop is a slab underneath.",
  "- A slogan as the `<h1>` with the product name shrunk to a small subline (Fly By Jing and Minimalist rebuilds, Oct 2026). The shopper cannot tell what the product is at a glance.\n- A split layout where the hero is decoration and the value prop is a slab underneath."),
 ("- **The standard is the target for every new rebuild**, not a retro-fix project. Existing\n  posted work is not redone; runs from here build to this bar.",
  "- **Fly By Jing chili crisp and Minimalist niacinamide** (Oct 2026) pass dimensions 1 and 3 to 7 but\n  fail the 2026-10-10 title rule (slogan is the H1, product name is a small subline). Per Ridwan they\n  are NOT redone; the rule applies to every rebuild from 2026-10-10.\n- **The standard is the target for every new rebuild**, not a retro-fix project. Existing\n  posted work is not redone; runs from here build to this bar."),
])

# 2. page build brief doc
edit('docs/system/page-build-brief.md', [
 ("- The **first screen carries the whole decision**: outcome headline, price, rating and review count,",
  "- The **product title as the page's only `<h1>`**, real full title from the live page, at the top of the first\n  screen above the price, never outranked by a slogan (the 2026-10-10 title rule in\n  `cro-redesign-standard.md`). Product pages only.\n- The **first screen carries the whole decision**: product title, outcome line, price, rating and review count,"),
])

# 3. brief generator (future briefs only)
edit('.ai-workflow/tools/build_page_brief.py', [
 ("""    heads = f.get("headline_options") or []""",
  """    heads = f.get("headline_options") or []
    # 2026-10-10 title rule: the real product title is the H1. Facts may override with `product_title`
    # (use the full live title, size or variant included); it falls back to the page name.
    product_title = f.get("product_title") or page
    if not f.get("product_title"):
        print(f"NOTE: facts has no product_title, using page name: {page!r}. Set it to the full live title.", file=sys.stderr)"""),
 ("""- The first screen must carry the whole decision: outcome headline, price,""",
  """- The page's only <h1> is the real product title: **{product_title}**. It sits at the top of
  the first screen, under the header, above the price, bold, at least 22px. The outcome line
  is an eyebrow or subhead, never the <h1>, never larger than the title.
- The first screen must carry the whole decision: product title, outcome line, price,"""),
 ("## Outcome headline options (pick one, or improve on it)",
  "## Outcome line options (subhead under the product title; pick one, or improve on it)"),
])

# 4. Skill B, both repo copies
for rel in ('.agents/skills/koolestpro-store-rebuilder-skill-b/SKILL.md', 'skills/cro-skill-stack/skill_B_store_rebuilder_v2.md'):
    edit(rel, [
     ("- Product name: clear, descriptive, readable at 20px+",
      "- Product title (PDP rebuilds): the real full product title from the live page, as the page's only `<h1>`, at the top of the first screen under the header/breadcrumb, above the price, bold, 22px+. A tagline or outcome line may sit above or below it as a smaller eyebrow/subhead, but never replaces the title, is never the `<h1>`, and never outranks it. Homepages and landing pages use the benefit headline as H1 instead."),
     ("- [ ] Rating + review count visible above the fold",
      "- [ ] Real product title is the only `<h1>`, visible on the first screen above the price (not demoted below a slogan)\n- [ ] Rating + review count visible above the fold"),
    ])

# 5. CLAUDE.md rule 12
edit('CLAUDE.md', [
 ("(outcome headline + proof + benefit + CTA + trust on a real hero)",
  "(product title as the H1 + outcome line + proof + benefit + CTA + trust on a real hero; the title is never demoted below a slogan, 2026-10-10)"),
])

# 6. build log
p = os.path.join(root, 'docs/koolestpro-content-operating-plan.md')
shutil.copy2(p, os.path.join(bk, 'docs__koolestpro-content-operating-plan.md'))
entry = """

### 2026-10-10: Product title rule for future CRO rebuilds

Ridwan noticed the newest CRO rebuilds (Fly By Jing chili crisp, Minimalist niacinamide) show a slogan as the `<h1>` and shrink the real product name to a small subline, so a shopper (and the page's SEO) loses the product title above the fold. Root cause: dimension 2 of `docs/system/cro-redesign-standard.md` said "value headline, not the product name", and `build_page_brief.py` repeated it. New rule: the real full product title is the only `<h1>`, top of the first screen, above the price, 22px+; the outcome line becomes a subhead. Updated the standard (dimension 2, rubric, checklist, anti-patterns), `page-build-brief.md`, `build_page_brief.py` (new `product_title` facts field, falls back to the page name with a warning), both repo copies of Skill B, and CLAUDE.md standing rule 12. Past builds are deliberately NOT redone. Backups: `.ai-workflow/backups/2026-10-10-title-rule/`.
"""
with open(p, 'a', encoding='utf-8') as fh:
    fh.write(entry)
print('appended build log')

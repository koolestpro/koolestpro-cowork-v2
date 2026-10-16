#!/usr/bin/env python3
"""Publisher for Next.js sites that keep articles as typed data (koolestpro.com: content/resources.ts).

The Next.js equivalent of shopify_publish.py. It inserts <run>/article.json as the newest entry
in the site's articles array. The agent then commits that on a branch `seo/<slug>` and opens a DRAFT PR.
The Vercel preview of that PR is the approval step. Merging is publishing, and only Ridwan merges.

article.json must match the site's `Article` type (see content/resources.ts):
  slug, title, h1, description, targetQuestion, updated, readingMinutes, blocks[], faq[], cta{text,href,label}

Site repo location: env SITE_REPO_PATH, else project.json `site_repo_path` (tried in order).

Usage:
  site_publish.py --run seo/project/runs/2026-10-06 [--dry-run]
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

from _common import REPO_ROOT, load_env, load_project

ANCHOR = "export const articles: Article[] = ["
SLUG_RE = r"""["']?slug["']?\s*:\s*["']([^"']+)["']"""
BLOCK_TYPES = {"p", "h2", "h3", "ul", "table", "callout", "verdict"}


def find_repo(cfg):
    load_env()
    cands = [os.environ.get("SITE_REPO_PATH")] + cfg.get("site_repo_path", [])
    for c in filter(None, cands):
        p = (REPO_ROOT / c).resolve() if not os.path.isabs(c) else Path(c)
        if (p / cfg["articles_file"]).exists():
            return p
    sys.exit(f"Site repo not found. Tried: {cands}. Clone {cfg.get('site_repo')} or set SITE_REPO_PATH")


def validate(a, existing_slugs, site_paths):
    problems = []
    for k in ("slug", "title", "h1", "description", "targetQuestion", "updated", "readingMinutes", "blocks", "faq", "cta"):
        if k not in a:
            problems.append(f"missing {k}")
    if problems:
        return problems
    if a["slug"] in existing_slugs:
        problems.append(f"slug '{a['slug']}' already exists")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a["slug"]):
        problems.append("slug must be lowercase-hyphenated")
    if len(a["title"]) > 60:
        problems.append(f"title is {len(a['title'])} chars (max 60, it is the <title>)")
    if not 70 <= len(a["description"]) <= 155:
        problems.append(f"description is {len(a['description'])} chars (want 70 to 155)")
    blob = json.dumps(a, ensure_ascii=False)
    if "—" in blob or "&mdash;" in blob:
        problems.append("em dash found")
    for b in a["blocks"]:
        if b.get("type") not in BLOCK_TYPES:
            problems.append(f"unknown block type {b.get('type')}")
    if not any(b.get("type") == "h2" for b in a["blocks"]):
        problems.append("no h2 blocks")
    href = a["cta"].get("href", "")
    if href.startswith("/") and site_paths and href.split("#")[0] not in site_paths:
        problems.append(f"cta href {href} not found among site routes/slugs")
    return problems


def site_routes(repo):
    """Best-effort list of valid internal paths: app/ static routes + data-driven slugs."""
    paths = {"/"}
    for page in (repo / "app").rglob("page.tsx"):
        rel = "/" + str(page.parent.relative_to(repo / "app")).replace("\\", "/")
        if "[" not in rel:
            paths.add(rel.rstrip("/") or "/")
    content = repo / "content"
    for f, prefix in (("services.ts", "/services/"), ("work.ts", "/work/"), ("resources.ts", "/resources/")):
        if (content / f).exists():
            paths |= {prefix + s for s in re.findall(SLUG_RE, (content / f).read_text())}
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_project()
    repo = find_repo(cfg)
    target = repo / cfg["articles_file"]
    src = target.read_text()
    if ANCHOR not in src:
        sys.exit(f"Anchor '{ANCHOR}' not found in {target}. The site's data shape changed, so update this tool.")

    a = json.loads((Path(args.run) / "article.json").read_text())
    existing = set(re.findall(SLUG_RE, src.split(ANCHOR, 1)[1]))
    problems = validate(a, existing, site_routes(repo))
    if problems:
        sys.exit("QA gate failed:\n  - " + "\n  - ".join(problems))

    # JSON is a valid TS object literal; keep the file's 2-space indent inside the array.
    entry = json.dumps(a, indent=2, ensure_ascii=False)
    entry = "\n".join("  " + line for line in entry.splitlines())
    new_src = src.replace(ANCHOR, f"{ANCHOR}\n  // SEO engine: {a['slug']} ({a['updated']})\n{entry},", 1)

    if args.dry_run:
        print(f"OK: would insert '{a['slug']}' into {target} ({len(a['blocks'])} blocks, {len(a['faq'])} FAQs)")
        return
    target.write_text(new_src)
    result = {"repo": str(repo), "file": str(target.relative_to(repo)), "slug": a["slug"],
              "branch": f"seo/{a['slug']}", "live_url_after_merge": f"{cfg['site_url'].rstrip('/')}/resources/{a['slug']}"}
    (Path(args.run) / "site-result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print("Next: in the site repo, branch seo/<slug>, commit, push, open a DRAFT PR. Ridwan merges after checking the Vercel preview.")


if __name__ == "__main__":
    main()

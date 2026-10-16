#!/usr/bin/env python3
"""Create a weekly SEO article in Shopify as a HIDDEN DRAFT (never published).

Reads   <run>/publish.json + <run>/body.html
Writes  <run>/shopify-result.json

Env (this project's .env or cloud secrets):
  SHOPIFY_STORE_DOMAIN   e.g. your-store.myshopify.com
  SHOPIFY_ADMIN_TOKEN    Admin API access token (shpat_...)

Usage:
  python3 seo/engine/tools/shopify_publish.py --check
  python3 seo/engine/tools/shopify_publish.py --run seo/project/runs/2026-10-06
  python3 seo/engine/tools/shopify_publish.py --run ... --dry-run
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

from _common import http, load_project, need_env

API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-07")

BLOGS_Q = "{ blogs(first: 25) { nodes { id handle title } } shop { name primaryDomain { url } } }"

CREATE_M = """
mutation CreateArticle($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article { id handle title isPublished }
    userErrors { field message code }
  }
}"""


def gql(domain, token, query, variables=None):
    status, body = http(
        f"https://{domain}/admin/api/{API_VERSION}/graphql.json",
        data={"query": query, "variables": variables or {}},
        headers={"X-Shopify-Access-Token": token},
    )
    if status != 200:
        sys.exit(f"Shopify HTTP {status}: {body[:500]}")
    out = json.loads(body)
    if out.get("errors"):
        sys.exit(f"Shopify GraphQL errors: {json.dumps(out['errors'])[:800]}")
    return out["data"]


def creds():
    domain, token = need_env("SHOPIFY_STORE_DOMAIN", "SHOPIFY_ADMIN_TOKEN")
    return domain, token


def validate(pub, body):
    problems = []
    for k in ("title", "handle", "seo_title", "seo_description", "blog_handle"):
        if not pub.get(k):
            problems.append(f"publish.json missing {k}")
    if len(pub.get("seo_title", "")) > 60:
        problems.append(f"seo_title is {len(pub['seo_title'])} chars (max 60)")
    if len(pub.get("seo_description", "")) > 155:
        problems.append(f"seo_description is {len(pub['seo_description'])} chars (max 155)")
    blob = body + json.dumps(pub, ensure_ascii=False)
    dashes = blob.count("—") + blob.count("&mdash;")
    if dashes:
        problems.append(f"{dashes} em dash(es) found")
    if re.search(r"<h1[\s>]", body, re.I):
        problems.append("body.html contains an <h1> (Shopify renders the title as H1)")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="run folder containing publish.json + body.html")
    ap.add_argument("--check", action="store_true", help="verify token and list blogs")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_project()

    if args.check:
        domain, token = creds()
        data = gql(domain, token, BLOGS_Q)
        print(f"OK: {data['shop']['name']} ({data['shop']['primaryDomain']['url']}), API {API_VERSION}")
        for b in data["blogs"]["nodes"]:
            print(f"  blog: {b['handle']:25s} {b['title']}  {b['id']}")
        return

    if not args.run:
        sys.exit("--run is required (or use --check)")
    run = Path(args.run)
    pub = json.loads((run / "publish.json").read_text())
    body = (run / "body.html").read_text()

    problems = validate(pub, body)
    if problems:
        sys.exit("QA gate failed:\n  - " + "\n  - ".join(problems))

    article = {
        "title": pub["title"],
        "handle": pub["handle"],
        "body": body,
        "summary": pub.get("summary_html", ""),
        "tags": pub.get("tags", []),
        "isPublished": False,  # hard rule: hidden draft only, Ridwan publishes
        "author": {"name": pub.get("author") or cfg.get("blog_author", "")},
        "metafields": [
            {"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": pub["seo_title"]},
            {"namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": pub["seo_description"]},
        ],
    }
    if pub.get("image_url"):
        article["image"] = {"url": pub["image_url"], "altText": pub.get("image_alt", "")}

    if args.dry_run:
        print(json.dumps({k: (v if k != "body" else f"<{len(v)} chars>") for k, v in article.items()}, indent=2))
        return

    domain, token = creds()
    blogs = gql(domain, token, BLOGS_Q)["blogs"]["nodes"]
    blog = next((b for b in blogs if b["handle"] == pub["blog_handle"]), None)
    if not blog:
        sys.exit(f"Blog '{pub['blog_handle']}' not found. Available: {[b['handle'] for b in blogs]}")
    article["blogId"] = blog["id"]

    res = gql(domain, token, CREATE_M, {"article": article})["articleCreate"]
    if res["userErrors"]:
        sys.exit(f"articleCreate userErrors: {json.dumps(res['userErrors'], indent=1)}")
    a = res["article"]
    numeric_id = a["id"].rsplit("/", 1)[-1]
    result = {
        "article_gid": a["id"],
        "handle": a["handle"],
        "is_published": a["isPublished"],
        "admin_url": f"https://{domain}/admin/articles/{numeric_id}",
        "live_url_after_publish": f"{cfg['site_url'].rstrip('/')}/blogs/{pub['blog_handle']}/{a['handle']}",
    }
    (run / "shopify-result.json").write_text(json.dumps(result, indent=2))
    print(f"Draft created (hidden): {result['admin_url']}")


if __name__ == "__main__":
    main()

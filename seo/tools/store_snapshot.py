#!/usr/bin/env python3
"""Snapshot a Shopify store's public catalogue so every stage links only to real URLs.

Uses the public storefront JSON endpoints (no token needed):
  /products.json, /collections.json, /pages.json, /sitemap_blogs_1.xml

Writes seo/clients/<slug>/snapshot/{products,collections,pages,blogs}.json and
prints a diff against the previous snapshot.

Usage: python3 seo/tools/store_snapshot.py --client tapandrate
"""
import argparse
import html
import json
import re
import sys
from datetime import date

from _common import client_dir, http, load_client


def strip_html(s, limit=400):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return html.unescape(re.sub(r"\s+", " ", s)).strip()[:limit]


def paged(base, key):
    items, page = [], 1
    while True:
        status, body = http(f"{base}/{key}.json?limit=250&page={page}")
        if status != 200:
            if page == 1:
                print(f"  ! {key}.json returned {status}", file=sys.stderr)
            break
        batch = json.loads(body).get(key, [])
        items.extend(batch)
        if len(batch) < 250:
            break
        page += 1
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True)
    args = ap.parse_args()

    cfg = load_client(args.client)
    base = cfg["site_url"].rstrip("/")
    out = client_dir(args.client) / "snapshot"
    out.mkdir(exist_ok=True)

    products = []
    for p in paged(base, "products"):
        prices = sorted(float(v["price"]) for v in p.get("variants", []) if v.get("price"))
        products.append({
            "title": p["title"],
            "url": f"/products/{p['handle']}",
            "type": p.get("product_type", ""),
            "tags": p.get("tags", []),
            "price_min": prices[0] if prices else None,
            "price_max": prices[-1] if prices else None,
            "variants": len(p.get("variants", [])),
            "images": [i["src"] for i in p.get("images", [])[:4]],
            "description": strip_html(p.get("body_html")),
            "updated_at": p.get("updated_at"),
        })
    collections = [{
        "title": c["title"], "url": f"/collections/{c['handle']}",
        "description": strip_html(c.get("body_html"), 200),
    } for c in paged(base, "collections")]
    pages = [{
        "title": p["title"], "url": f"/pages/{p['handle']}",
        "excerpt": strip_html(p.get("body_html"), 200),
    } for p in paged(base, "pages")]

    status, body = http(f"{base}/sitemap_blogs_1.xml")
    blog_urls = re.findall(r"<loc>([^<]+)</loc>", body) if status == 200 else []
    blogs = [{"url": re.sub(r"^https?://[^/]+", "", u)} for u in blog_urls]

    data = {"products": products, "collections": collections, "pages": pages, "blogs": blogs}
    prev = {}
    for name, rows in data.items():
        f = out / f"{name}.json"
        if f.exists():
            prev[name] = {r.get("url") for r in json.loads(f.read_text())}
        f.write_text(json.dumps(rows, indent=1, ensure_ascii=False))

    (out / "_meta.json").write_text(json.dumps({"date": date.today().isoformat(), "site": base}))
    print(f"Snapshot of {base} -> {out}")
    for name, rows in data.items():
        now = {r["url"] for r in rows}
        line = f"  {name:12s} {len(rows):4d}"
        if name in prev:
            added, removed = now - prev[name], prev[name] - now
            if added or removed:
                line += f"  (+{len(added)} / -{len(removed)})"
                for u in sorted(added)[:10]:
                    line += f"\n      + {u}"
                for u in sorted(removed)[:10]:
                    line += f"\n      - {u}"
        print(line)


if __name__ == "__main__":
    main()

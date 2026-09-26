#!/usr/bin/env python3
"""
Search Freesound.org for free sound effects, ambient beds, whooshes, UI pops,
foley, etc. Freesound is the closest audio equivalent to Pexels/Pixabay in
this stack: free account, generous rate limits, simple token auth for search,
and the mp3 "preview" files returned by search are directly downloadable with
no further auth (the only thing that needs OAuth2 is downloading the
*original* uploaded file, which this script doesn't need -- the hq preview,
~128kbps mp3, is plenty for video sound design).

Usage:
    python3 search_freesound.py "<query>" --keys /path/to/.env --limit 10
    python3 search_freesound.py "whoosh transition" --duration-max 3 --limit 5
    python3 search_freesound.py "soft ui pop" --license cc0 --download ./sfx/
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://freesound.org/apiv2"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) video-gen-cowork-skill/1.0"

FIELDS = "id,name,tags,license,duration,username,previews,url"


def load_key(path):
    key = os.environ.get("FREESOUND_API_KEY", "")
    if path and os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "FREESOUND_API_KEY" and v.strip():
                    key = v.strip()
    return key


def search(query, key, duration_max=None, license_filter=None, limit=10, sort="score"):
    if not key:
        return {"error": "no FREESOUND_API_KEY found (check --keys or environment)", "results": []}

    filters = []
    if duration_max:
        filters.append(f"duration:[0 TO {duration_max}]")
    if license_filter:
        # common values: "Creative Commons 0", "Attribution", "Attribution Noncommercial"
        filters.append(f'license:"{license_filter}"')

    params = {
        "query": query,
        "fields": FIELDS,
        "page_size": min(limit, 150),
        "sort": sort,
    }
    if filters:
        params["filter"] = " ".join(filters)

    url = f"{BASE}/search/?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Token {key}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": f"HTTP {e.code}: {body}", "results": []}

    results = []
    for s in data.get("results", []):
        previews = s.get("previews", {})
        results.append(
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "duration_s": s.get("duration"),
                "license": s.get("license"),
                "username": s.get("username"),
                "tags": s.get("tags"),
                "download_url": previews.get("preview-hq-mp3") or previews.get("preview-lq-mp3"),
                "page_url": s.get("url"),
            }
        )
    return {"count": data.get("count", 0), "results": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--keys", default=None, help="path to .env with FREESOUND_API_KEY")
    ap.add_argument("--duration-max", type=float, default=None, help="max clip length in seconds")
    ap.add_argument("--license", default=None, help='e.g. "Creative Commons 0" for no-attribution-needed sounds')
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--sort", default="score", help="score (relevance, default), downloads_desc, rating_desc, duration_asc, etc.")
    ap.add_argument("--download", default=None, help="if set, download all result previews into this directory")
    args = ap.parse_args()

    key = load_key(args.keys)
    result = search(args.query, key, args.duration_max, args.license, args.limit, args.sort)
    print(json.dumps(result, indent=2))

    if args.download and result.get("results"):
        os.makedirs(args.download, exist_ok=True)
        for r in result["results"]:
            if not r.get("download_url"):
                continue
            safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in r["name"])[:60]
            out_path = os.path.join(args.download, f"{r['id']}_{safe_name}.mp3")
            try:
                req = urllib.request.Request(r["download_url"], headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=30) as resp, open(out_path, "wb") as f:
                    f.write(resp.read())
                print(f"downloaded: {out_path}", file=sys.stderr)
            except Exception as e:
                print(f"failed to download {r['id']}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

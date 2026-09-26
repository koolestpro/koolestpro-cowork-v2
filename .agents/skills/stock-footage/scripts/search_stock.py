#!/usr/bin/env python3
"""
Search Pexels and/or Pixabay for free stock photos/videos.

Usage:
    python3 search_stock.py "<query>" --type video --source both --keys /path/to/keys.env --limit 5

Reads API keys from a simple KEY=VALUE env file (see --keys), falling back to
PEXELS_API_KEY / PIXABAY_API_KEY already in the environment if no file is
given or a key is missing from it. Prints a JSON list of results with title,
preview URL, and a direct download URL for each hit.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def load_keys(path):
    keys = {}
    if path and os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                keys[k.strip()] = v.strip()
    keys.setdefault("PEXELS_API_KEY", os.environ.get("PEXELS_API_KEY", ""))
    keys.setdefault("PIXABAY_API_KEY", os.environ.get("PIXABAY_API_KEY", ""))
    return keys


def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def search_pexels(query, media_type, api_key, limit):
    if not api_key:
        return {"source": "pexels", "error": "no PEXELS_API_KEY", "results": []}
    url = f"https://api.pexels.com/{'videos/' if media_type == 'video' else ''}search?query={urllib.parse.quote(query)}&per_page={limit}"
    try:
        data = fetch_json(url, headers={"Authorization": api_key})
    except Exception as e:
        return {"source": "pexels", "error": str(e), "results": []}
    results = []
    if media_type == "video":
        for v in data.get("videos", [])[:limit]:
            files = sorted(v.get("video_files", []), key=lambda f: f.get("width", 0), reverse=True)
            results.append({
                "id": v.get("id"),
                "preview": v.get("image"),
                "download_url": files[0]["link"] if files else None,
                "duration_s": v.get("duration"),
                "page_url": v.get("url"),
            })
    else:
        for p in data.get("photos", [])[:limit]:
            results.append({
                "id": p.get("id"),
                "preview": p.get("src", {}).get("medium"),
                "download_url": p.get("src", {}).get("original"),
                "page_url": p.get("url"),
            })
    return {"source": "pexels", "results": results}


def search_pixabay(query, media_type, api_key, limit):
    if not api_key:
        return {"source": "pixabay", "error": "no PIXABAY_API_KEY", "results": []}
    path = "videos/" if media_type == "video" else ""
    url = (
        f"https://pixabay.com/api/{path}?key={api_key}"
        f"&q={urllib.parse.quote(query)}&per_page={max(limit, 3)}"
    )
    try:
        data = fetch_json(url)
    except Exception as e:
        return {"source": "pixabay", "error": str(e), "results": []}
    results = []
    for hit in data.get("hits", [])[:limit]:
        if media_type == "video":
            videos = hit.get("videos", {})
            best = videos.get("large") or videos.get("medium") or videos.get("small")
            results.append({
                "id": hit.get("id"),
                "preview": None,
                "download_url": best.get("url") if best else None,
                "duration_s": hit.get("duration"),
                "page_url": hit.get("pageURL"),
            })
        else:
            results.append({
                "id": hit.get("id"),
                "preview": hit.get("previewURL"),
                "download_url": hit.get("largeImageURL"),
                "page_url": hit.get("pageURL"),
            })
    return {"source": "pixabay", "results": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--type", choices=["photo", "video"], default="video")
    ap.add_argument("--source", choices=["pexels", "pixabay", "both"], default="both")
    ap.add_argument("--keys", default=None, help="path to keys.env")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()

    keys = load_keys(args.keys)
    out = []
    if args.source in ("pexels", "both"):
        out.append(search_pexels(args.query, args.type, keys["PEXELS_API_KEY"], args.limit))
    if args.source in ("pixabay", "both"):
        out.append(search_pixabay(args.query, args.type, keys["PIXABAY_API_KEY"], args.limit))

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

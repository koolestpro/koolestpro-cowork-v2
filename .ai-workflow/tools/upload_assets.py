#!/usr/bin/env python3
"""
upload_assets.py — V2 distribution pipeline, asset-hosting step (feeds Make).

Platform APIs need a publicly-reachable image/video URL — the queue's
`asset_paths` are local `outputs/...` paths. This uploads each local asset to
Cloudinary (cloud name is a flag; this project uses `drl0rscuf`) via an UNSIGNED
upload preset, then writes the returned public `secure_url` into a new
`asset_urls` column on every queue row that references that asset.

Why unsigned preset (not API key/secret): unsigned uploads need only the cloud
name + preset name — no secret in the repo, safe to run in an automated task.
Create the preset once in the Cloudinary console (Settings → Upload → Upload
presets → Add, Signing Mode = Unsigned) and pass its name via --preset.

Runs entirely in-sandbox (confirmed reachable) — asset bytes never pass through
the agent's context. Idempotent: a URL cache (asset_url_map.json) means an asset
already uploaded is reused, not re-uploaded.

Usage:
    python3 upload_assets.py --preset koolestpro_unsigned [--cloud-name drl0rscuf]
        [--queue outputs/distribution-queue/queue.json] [--project-root DIR]
"""

import argparse
import json
import mimetypes
import os
import subprocess
import sys

CLOUD_DEFAULT = "drl0rscuf"


def find_root(start):
    d = os.path.abspath(start)
    while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
        d = os.path.dirname(d)
    return d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.abspath(start)


def cloudinary_upload(local_path, cloud_name, preset):
    """Unsigned multipart upload via curl (no extra python deps, no secret).
    Returns secure_url or raises."""
    ext = os.path.splitext(local_path)[1].lower()
    rtype = "video" if ext in (".mp4", ".webm", ".mov") else "image"
    endpoint = f"https://api.cloudinary.com/v1_1/{cloud_name}/{rtype}/upload"
    cmd = [
        "curl", "-s", "--max-time", "120",
        "-X", "POST", endpoint,
        "-F", f"file=@{local_path}",
        "-F", f"upload_preset={preset}",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed: {out.stderr.strip()}")
    try:
        resp = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"non-JSON response: {out.stdout[:300]}")
    if "secure_url" in resp:
        return resp["secure_url"]
    raise RuntimeError(f"upload error: {resp.get('error', resp)}")


def collect_local_assets(queue):
    paths = set()
    for r in queue.get("rows", []):
        for p in (r.get("asset_paths") or "").split(";"):
            p = p.strip()
            # only real on-disk media (skip the CAROUSEL_HTML companion links)
            if p and not p.endswith(".html"):
                paths.add(p)
    return sorted(paths)


def main():
    ap = argparse.ArgumentParser(description="Upload queue assets to Cloudinary and write asset_urls back.")
    ap.add_argument("--preset", required=True, help="Cloudinary UNSIGNED upload preset name")
    ap.add_argument("--cloud-name", default=CLOUD_DEFAULT)
    ap.add_argument("--queue", default=None)
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--folder", default="koolestpro-distribution",
                    help="(informational) Cloudinary asset folder if the preset routes there")
    args = ap.parse_args()

    root = os.path.abspath(args.project_root) if args.project_root else find_root(os.getcwd())
    qpath = args.queue or os.path.join(root, "outputs", "distribution-queue", "queue.json")
    if not os.path.exists(qpath):
        sys.exit(f"queue not found: {qpath}")
    with open(qpath, "r", encoding="utf-8") as f:
        queue = json.load(f)

    cache_path = os.path.join(os.path.dirname(qpath), "asset_url_map.json")
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)

    assets = collect_local_assets(queue)
    uploaded, reused, failed = 0, 0, []
    for rel in assets:
        if rel in cache:
            reused += 1
            continue
        abspath = rel if os.path.isabs(rel) else os.path.join(root, rel)
        if not os.path.exists(abspath):
            failed.append(f"{rel} (missing on disk)")
            continue
        try:
            url = cloudinary_upload(abspath, args.cloud_name, args.preset)
            cache[rel] = url
            uploaded += 1
            print(f"[upload] {rel} -> {url}")
        except Exception as e:
            failed.append(f"{rel} ({e})")

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

    # write asset_urls onto each row (semicolon-joined, same order as asset_paths)
    for r in queue.get("rows", []):
        urls = []
        for p in (r.get("asset_paths") or "").split(";"):
            p = p.strip()
            if p in cache:
                urls.append(cache[p])
        r["asset_urls"] = "; ".join(urls)
    with open(qpath, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

    print(f"\n[upload] uploaded={uploaded} reused(cached)={reused} failed={len(failed)}")
    for fl in failed:
        print("   ! ", fl)
    print(f"[upload] url cache: {cache_path}")
    print(f"[upload] asset_urls written into queue rows: {qpath}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

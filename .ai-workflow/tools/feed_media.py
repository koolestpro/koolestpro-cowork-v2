#!/usr/bin/env python3
"""
feed_media.py — V2 distribution pipeline, the "feeder" step for Instagram + Twitter.

Companion to feed_linkedin.py (which handles LinkedIn's video->mp4 /
carousel->PDF logic specifically). Instagram and Twitter rows need different
handling: each image is hosted individually (not combined into a PDF — X and
IG's native media APIs take direct image/video URLs, not documents), and a
multi-image Instagram carousel becomes multiple semicolon-joined URLs in the
same order as asset_paths.

Built 2026-07-29 as part of closing the gap DISTRIBUTION.md already flagged:
"Existing rows created before 2026-07-21 mostly still have an empty
asset_urls — worth a backfill pass." Until now that backfill was done by hand,
row by row, via direct Cloudinary MCP calls in interactive sessions — this
script makes it a repeatable, idempotent step any scheduled task can run
unattended, the same way feed_linkedin.py already does for LinkedIn.

Per-row logic (Instagram / Twitter rows only):
  - video asset (.mp4/.mov/.webm)   -> upload to Cloudinary, use its URL directly
  - 1+ image assets (Twitter)       -> upload EACH individually, join URLs
                                        with "; " in the same order as asset_paths
  - 2+ image assets (Instagram)     -> upload EACH individually, but asset_urls
                                        only ever gets the FIRST (cover) URL —
                                        see the 2026-09-08 bug note in main()
                                        below. Twitter is unaffected; it has no
                                        equivalent single-image Make branch.
  - no on-disk assets                -> leave asset_urls empty (text-only —
                                        the distribution plan says this
                                        shouldn't happen for Twitter, so an
                                        empty result here is worth flagging,
                                        not silently accepting)

Same unsigned-preset upload mechanism and asset_url_map.json cache as
feed_linkedin.py (shared cache file — a file already uploaded for one
platform is never re-uploaded for another).

Usage:
    python3 feed_media.py [--platform Instagram Twitter] [--preset koolestpro_unsigned]
        [--cloud-name drl0rscuf] [--project-root DIR] [--queue FILE] [--dry-run]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

CLOUD_DEFAULT = "drl0rscuf"
VIDEO_EXTS = (".mp4", ".mov", ".webm")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def find_root(start):
    d = os.path.abspath(start)
    while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
        d = os.path.dirname(d)
    return d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.abspath(start)


def sig(path):
    h = hashlib.sha1()
    h.update(path.encode())
    try:
        h.update(str(os.path.getmtime(path)).encode())
    except OSError:
        pass
    return h.hexdigest()[:16]


def cloudinary_upload(local_path, cloud_name, preset, resource_type, public_id):
    endpoint = f"https://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload"
    cmd = ["curl", "-s", "--max-time", "300", "-X", "POST", endpoint,
           "-F", f"file=@{local_path}", "-F", f"upload_preset={preset}",
           "-F", f"public_id={public_id}", "-F", "tags=koolestpro-distribution"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed: {out.stderr.strip()}")
    resp = json.loads(out.stdout)
    if "secure_url" in resp:
        return resp["secure_url"]
    raise RuntimeError(f"upload error: {resp.get('error', resp)}")


def main():
    ap = argparse.ArgumentParser(description="Populate asset_urls for Instagram/Twitter queue rows (per-image/video URLs, no PDF combining).")
    ap.add_argument("--platform", nargs="+", default=["Instagram", "Twitter"])
    ap.add_argument("--preset", default="koolestpro_unsigned")
    ap.add_argument("--cloud-name", default=CLOUD_DEFAULT)
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--queue", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.project_root) if args.project_root else find_root(os.getcwd())
    qpath = args.queue or os.path.join(root, "outputs", "distribution-queue", "queue.json")
    if not os.path.exists(qpath):
        sys.exit(f"queue not found: {qpath}")
    with open(qpath, "r", encoding="utf-8") as f:
        queue = json.load(f)

    cache_path = os.path.join(os.path.dirname(qpath), "asset_url_map.json")
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}

    changed, results, skipped_no_asset = 0, [], []
    for r in queue.get("rows", []):
        if r.get("platform") not in args.platform:
            continue
        if r.get("asset_urls"):
            continue  # already hosted (idempotent — never re-upload/clobber)
        locals_ = [p.strip() for p in (r.get("asset_paths") or "").split(";") if p.strip()]
        files = []
        for p in locals_:
            ap_ = p if os.path.isabs(p) else os.path.join(root, p)
            if os.path.exists(ap_) and os.path.splitext(ap_)[1].lower() in (VIDEO_EXTS + IMAGE_EXTS):
                files.append(ap_)

        if not files:
            if locals_:
                skipped_no_asset.append(r["post_id"])
            continue

        # BUG FIXED 2026-08-19: this used to take only the first 2 hyphen
        # tokens of pipeline_item_id (e.g. "static-ad-v1ce_..." -> "static-ad"),
        # which collapses EVERY item of a given type onto the SAME Cloudinary
        # public_id (dist/static-ad/ad-1-problem-solution.png etc regardless
        # of brand). Confirmed live: V1CE, Material Kitchen, and 2 backfill
        # rows for Obvi/Bebemoss all ended up pointing at the same URL, and
        # whichever upload landed last silently became the image served for
        # every other brand's post that shared that public_id. Fix: use the
        # FULL pipeline_item_id (already unique per generated item) as the
        # folder segment, so no two different posts can ever collide.
        prefix = (r.get("pipeline_item_id") or r["post_id"]) or "misc"
        urls = []
        for f in files:
            key = sig(f)
            if key in cache:
                urls.append(cache[key])
                continue
            ext = os.path.splitext(f)[1].lower()
            rtype = "video" if ext in VIDEO_EXTS else "image"
            pid = f"dist/{prefix}/{os.path.splitext(os.path.basename(f))[0]}"
            if args.dry_run:
                urls.append("")
                continue
            url = cloudinary_upload(f, args.cloud_name, args.preset, rtype, pid)
            cache[key] = url
            urls.append(url)
            changed += 1

        real_urls = [u for u in urls if u]
        # BUG FIXED 2026-09-08: Instagram's Make branch (modules 301/302) only
        # implements the single-image /media + /media_publish flow — it has no
        # carousel route (child containers + is_carousel_item + parent
        # container). A multi-image Instagram row (any "carousel"/"carousel-N"
        # format slot) used to get every image URL joined with "; " into one
        # asset_urls string, which module 301's endswith(".png") filter still
        # matched (the *last* URL in the string ends .png), so Make POSTed the
        # whole semicolon-joined garbage string as a single `image_url` param —
        # Instagram's Graph API correctly rejected it with 400 Bad Request.
        # Confirmed live on post_id idea-mobile-thumb-zone-7-tap-target-fails-
        # ...-20260908-ig-1200 (execution ddef648826f34f9f9c81fdb26c91a31c).
        # Stopgap until real IG carousel support is built in Make: Instagram
        # rows with more than one non-video image only ever get the FIRST
        # (cover) image URL, so they post as a single image instead of
        # erroring. This does not change what gets generated/reviewed — only
        # what actually gets sent to graph.instagram.com. Every other platform
        # keeps the full list.
        is_video_only = len(real_urls) == 1 and any(
            os.path.splitext(f)[1].lower() in VIDEO_EXTS for f in files
        )
        if r.get("platform") == "Instagram" and len(real_urls) > 1 and not is_video_only:
            joined = real_urls[0]
        else:
            joined = "; ".join(real_urls)
        r["asset_urls"] = joined
        results.append((r["post_id"], len(files), joined))

    if not args.dry_run:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        with open(qpath, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        try:
            sys.path.insert(0, os.path.join(root, ".ai-workflow", "tools"))
            import populate_sheet, csv
            csvp = os.path.splitext(qpath)[0] + ".csv"
            with open(csvp, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=populate_sheet.COLUMNS)
                w.writeheader()
                for row in queue["rows"]:
                    w.writerow({k: row.get(k, "") for k in populate_sheet.COLUMNS})
        except Exception as e:
            print(f"[feed-media] (warning) could not refresh CSV mirror: {e}", file=sys.stderr)

    print(f"[feed-media] platforms={args.platform} rows filled={len(results)} newly uploaded={changed} dry_run={args.dry_run}")
    for pid, n, url in results:
        print(f"  {pid} ({n} file(s)) -> {url}")
    if skipped_no_asset:
        print(f"[feed-media] WARNING: {len(skipped_no_asset)} row(s) have asset_paths but nothing found on disk: {skipped_no_asset}")


if __name__ == "__main__":
    main()

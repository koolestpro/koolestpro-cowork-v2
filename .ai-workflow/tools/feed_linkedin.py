#!/usr/bin/env python3
"""
feed_linkedin.py — V2 distribution pipeline, the "feeder" step.

Turns each LinkedIn queue row's LOCAL asset files into the single HOSTED asset
URL the Make scenario needs, and writes it into the row's `asset_urls` column
(index 14). The Make LinkedIn scenario then auto-routes on that URL's extension:
  - empty            -> text post
  - ends .mp4        -> native video post
  - ends .pdf        -> PDF document carousel

Per-row logic (LinkedIn rows only):
  - a video asset (.mp4/.mov/.webm)  -> upload the video to Cloudinary, use its .mp4 URL
  - 1+ image assets (a carousel)     -> combine them into a PDF (img2pdf), upload
                                        to Cloudinary /raw, use the .pdf URL
  - no on-disk assets                -> leave asset_urls empty (posts as text)

Uploads go through the unsigned Cloudinary preset (no secret in the repo), from
the sandbox directly — asset bytes never pass through the agent. A URL cache
(asset_url_map.json, shared with upload_assets.py) prevents re-uploading.

REQUIRES (one-time, already done for this project): Cloudinary unsigned preset
`koolestpro_unsigned`, and Settings->Security->"Allow delivery of PDF and ZIP
files" enabled (else the .pdf URL returns 401 and LinkedIn can't fetch it).

Usage:
    python3 feed_linkedin.py [--preset koolestpro_unsigned] [--cloud-name drl0rscuf]
        [--platform LinkedIn] [--project-root DIR] [--queue FILE] [--dry-run]
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


def sig(paths):
    """Stable signature for a set of local files (path + mtime) so the cache
    invalidates if a file changes."""
    h = hashlib.sha1()
    for p in paths:
        h.update(p.encode())
        try:
            h.update(str(os.path.getmtime(p)).encode())
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


def build_pdf(image_paths, out_path):
    import img2pdf
    with open(out_path, "wb") as f:
        f.write(img2pdf.convert([p for p in image_paths]))
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Populate asset_urls for LinkedIn queue rows (video->mp4 URL, images->PDF URL).")
    ap.add_argument("--preset", default="koolestpro_unsigned")
    ap.add_argument("--cloud-name", default=CLOUD_DEFAULT)
    ap.add_argument("--platform", default="LinkedIn")
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
    pdf_dir = os.path.join(root, "outputs", "distribution-queue", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    changed, results = 0, []
    for r in queue.get("rows", []):
        if r.get("platform") != args.platform:
            continue
        locals_ = [p.strip() for p in (r.get("asset_paths") or "").split(";") if p.strip()]
        # resolve to abs, keep only on-disk media (drop .html companion links)
        files = []
        for p in locals_:
            ap_ = p if os.path.isabs(p) else os.path.join(root, p)
            if os.path.exists(ap_) and os.path.splitext(ap_)[1].lower() in (VIDEO_EXTS + IMAGE_EXTS):
                files.append(ap_)

        if not files:
            note = "text (no on-disk assets)"
            url = ""
        else:
            videos = [f for f in files if os.path.splitext(f)[1].lower() in VIDEO_EXTS]
            images = [f for f in files if os.path.splitext(f)[1].lower() in IMAGE_EXTS]
            key = sig(files)
            if key in cache:
                url = cache[key]
                note = "cached"
            elif videos:
                pid = f"li/{r['post_id']}"
                url = "" if args.dry_run else cloudinary_upload(videos[0], args.cloud_name, args.preset, "video", pid)
                note = f"video -> {os.path.basename(videos[0])}"
            elif images:
                pdf_path = os.path.join(pdf_dir, f"{r['post_id']}.pdf")
                note = f"carousel PDF from {len(images)} image(s)"
                if not args.dry_run:
                    build_pdf(images, pdf_path)
                    url = cloudinary_upload(pdf_path, args.cloud_name, args.preset, "raw", f"li/{r['post_id']}")
                else:
                    url = ""
            else:
                url, note = "", "no usable asset"
            if url and key not in cache:
                cache[key] = url
                changed += 1

        prev = r.get("asset_urls", "")
        r["asset_urls"] = url
        results.append((r["post_id"], note, url or "(empty)", prev != url))

    if not args.dry_run:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        with open(qpath, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        # refresh CSV mirror using populate_sheet's column contract
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
            print(f"[feed] (warning) could not refresh CSV mirror: {e}", file=sys.stderr)

    print(f"[feed] platform={args.platform} rows processed={len(results)} newly uploaded={changed} dry_run={args.dry_run}")
    for pid, note, url, chg in results:
        flag = "*" if chg else " "
        print(f"  {flag} {pid}\n      {note} -> {url}")


if __name__ == "__main__":
    main()

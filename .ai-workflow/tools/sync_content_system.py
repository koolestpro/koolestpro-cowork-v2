#!/usr/bin/env python3
"""
sync_content_system.py — V2 distribution pipeline, Step 8.

Make ridwan_content_system_updated.html a visual mirror of the distribution
queue: for every generated content piece, attach a `distribution` array showing
each scheduled post (platform / date / time / status) so the content system
becomes a click-through archive of what's queued and posted — without touching
the UI or removing any existing data.

This is ADDITIVE and idempotent:
  - Reads the local queue (outputs/distribution-queue/queue.json).
  - Groups rows by pipeline_item_id.
  - Finds the matching item in SYNC_DATA.items (by id) and sets/refreshes its
    `distribution` list + `distributionUpdatedAt`. Click-through already works
    via the item's existing `folder` field (the JSON Standard's design).
  - Never deletes items, never edits the surrounding HTML/UI, only rewrites the
    JSON inside <script id="cowork-sync-data">.
  - A queue row whose pipeline_item_id has no matching item is reported, not
    fabricated (per CLAUDE.md: never create entries without a real file/item).

A .bak of the HTML is written before any change.

Usage:
    python3 sync_content_system.py [--project-root DIR] [--dry-run]
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

SCRIPT_RE = re.compile(
    r'(<script id="cowork-sync-data"[^>]*>)(.*?)(</script>)', re.DOTALL)


def find_root(start):
    d = os.path.abspath(start)
    while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
        d = os.path.dirname(d)
    return d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.abspath(start)


def main():
    ap = argparse.ArgumentParser(description="Sync the content system HTML from the distribution queue (additive).")
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--queue", default=None)
    ap.add_argument("--html", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.project_root) if args.project_root else find_root(os.getcwd())
    qpath = args.queue or os.path.join(root, "outputs", "distribution-queue", "queue.json")
    hpath = args.html or os.path.join(root, "ridwan_content_system_updated.html")

    if not os.path.exists(qpath):
        sys.exit(f"queue not found: {qpath}")
    if not os.path.exists(hpath):
        sys.exit(f"content system HTML not found: {hpath}")

    with open(qpath, "r", encoding="utf-8") as f:
        queue = json.load(f)
    with open(hpath, "r", encoding="utf-8") as f:
        html = f.read()

    m = SCRIPT_RE.search(html)
    if not m:
        sys.exit("could not locate <script id=\"cowork-sync-data\"> block in the HTML")
    data = json.loads(m.group(2))

    # group queue rows by pipeline_item_id
    by_item = {}
    for r in queue.get("rows", []):
        by_item.setdefault(r["pipeline_item_id"], []).append(r)

    items_by_id = {it.get("id"): it for it in data.get("items", [])}
    # slug fallback: CRO Fix / some Tips build their pipeline id from a click-time
    # date, so the queue id may not equal the canonical SYNC_DATA id. The slug is
    # stable, so fall back to matching on it when the exact id misses.
    items_by_slug = {}
    for it in data.get("items", []):
        items_by_slug.setdefault(it.get("slug"), it)

    matched, unmatched = [], []
    for item_id, rows in by_item.items():
        target = items_by_id.get(item_id)
        if not target:
            # derive slug from the row (populate_sheet doesn't carry slug, so pull
            # it from the id: strip the leading '<type>-' and trailing '-<date>')
            slug_guess = rows[0].get("slug")
            if not slug_guess:
                core = re.sub(r'-\d{8}$', '', item_id)
                for pfx in ("cro-fix-", "static-ad-", "template-showcase-",
                            "tip-", "personal-", "case-study-"):
                    if core.startswith(pfx):
                        slug_guess = core[len(pfx):]
                        break
                else:
                    slug_guess = core
            target = items_by_slug.get(slug_guess) if slug_guess else None
            if target:
                print(f"[sync] id '{item_id}' matched by slug '{slug_guess}' -> item '{target.get('id')}'")
        if not target:
            unmatched.append(item_id)
            continue
        dist = sorted(
            [{
                "post_id": r["post_id"],
                "platform": r["platform"],
                "scheduled_date": r["scheduled_date"],
                "scheduled_time_local": r.get("scheduled_time_local", r.get("scheduled_time_et", "")),
                "intended_et": r.get("intended_et", ""),
                "status": r.get("status", "Ready"),
                "qa_status": r.get("qa_status", ""),
                "posted_at": r.get("posted_at", ""),
            } for r in rows],
            key=lambda d: (d["scheduled_date"], d["scheduled_time_local"], d["platform"]),
        )
        target["distribution"] = dist
        target["distributionUpdatedAt"] = datetime.now(timezone.utc).isoformat()
        matched.append(item_id)

    # refresh meta
    data.setdefault("meta", {})
    data["meta"]["updatedAt"] = datetime.now(timezone.utc).isoformat()
    new_json = json.dumps(data, ensure_ascii=False)
    data["meta"]["syncHash"] = hashlib.sha1(new_json.encode("utf-8")).hexdigest()[:12]
    new_json = json.dumps(data, ensure_ascii=False)

    new_html = html[:m.start()] + m.group(1) + new_json + m.group(3) + html[m.end():]

    print(f"[sync] queue items: {len(by_item)} | matched to content-system items: {len(matched)} | unmatched: {len(unmatched)}")
    if unmatched:
        print("[sync] UNMATCHED pipeline_item_ids (no content-system item — not fabricated):")
        for u in unmatched:
            print("   -", u)
    for mid in matched:
        n = len(by_item[mid])
        print(f"[sync]   + {mid}: {n} distribution row(s) attached")

    if args.dry_run:
        print("[sync] dry-run — no file written.")
        return

    bak = hpath + ".bak"
    shutil.copy2(hpath, bak)
    with open(hpath, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"[sync] backup: {bak}")
    print(f"[sync] updated: {hpath}")
    print(f"[sync] new syncHash: {data['meta']['syncHash']}")


if __name__ == "__main__":
    main()

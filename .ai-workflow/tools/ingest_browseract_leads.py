#!/usr/bin/env python3
"""
ingest_browseract_leads.py — pull a finished BrowserAct Google Maps Scraper
task's CSV output and merge it into dm_leads_pool.json.

Why this file exists, not targets_pool.json: the Google Maps Scraper
workflow (workflow_id in .env's BROWSERACT_LEADGEN_WORKFLOW_ID) returns
name/address/rating/reviews for LOCAL businesses with no website field.
targets_pool.json's schema assumes every target has a url worth auditing
(CRO fixes, static ads, template showcases all need a real page to look
at) — these leads don't have one, so they go into dm_leads_pool.json's
lighter schema instead (Ridwan's call, 2026-08-11).

Usage:
  python3 ingest_browseract_leads.py --task-id <task_id>
  python3 ingest_browseract_leads.py --csv path/to/already-downloaded.csv --task-id <task_id> --workflow-id <id> --workflow-name "..."

Dedupes on a normalized businessName + address key — re-running against
the same task_id, or a re-scrape that turns up the same business, will
skip rows already present rather than duplicating them.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import browseract_client as bc

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
POOL_PATH = os.path.join(PROJECT_ROOT, "dm_leads_pool.json")


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60]


def dedup_key(business_name, address):
    return (slugify(business_name), slugify(address)[:40])


def load_pool():
    with open(POOL_PATH) as f:
        return json.load(f)


def save_pool(pool):
    with open(POOL_PATH, "w") as f:
        json.dump(pool, f, indent=1)
        f.write("\n")


def score_lead_potential(rating, review_count):
    try:
        rating_val = float(rating.split("/")[0]) if rating else 0
    except (ValueError, AttributeError):
        rating_val = 0
    try:
        reviews = int(review_count)
    except (ValueError, TypeError):
        reviews = 0
    if rating_val >= 4.5 and reviews >= 30:
        return "High"
    if rating_val >= 4.0 and reviews >= 10:
        return "Medium"
    if reviews > 0:
        return "Low"
    return "Unrated"


def fetch_csv_for_task(api_key, task_id):
    task = bc.get_task(api_key, task_id)
    files = (task.get("output") or {}).get("files") or []
    if not files:
        print(f"Task {task_id} has no output files (status={task.get('status')}).", file=sys.stderr)
        sys.exit(1)
    import urllib.request
    with urllib.request.urlopen(files[0], timeout=60) as resp:
        return resp.read().decode("utf-8-sig"), task.get("workflow_id")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--task-id", required=True, help="BrowserAct task id to pull output from (also stored on each lead for traceability)")
    p.add_argument("--csv", help="Skip re-downloading; use this local CSV instead")
    p.add_argument("--workflow-id", help="Override workflow_id recorded on each lead (defaults to the task's own workflow_id)")
    p.add_argument("--workflow-name", default="Google Maps Scraper-0811")
    args = p.parse_args()

    api_key = bc.load_api_key()
    if not api_key:
        print("BROWSERACT_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    if args.csv:
        with open(args.csv, encoding="utf-8-sig") as f:
            csv_text = f.read()
        workflow_id = args.workflow_id or os.environ.get("BROWSERACT_LEADGEN_WORKFLOW_ID", "")
    else:
        csv_text, task_workflow_id = fetch_csv_for_task(api_key, args.task_id)
        workflow_id = args.workflow_id or task_workflow_id or ""

    rows = list(csv.DictReader(io.StringIO(csv_text)))
    if not rows:
        print("CSV had no rows.", file=sys.stderr)
        sys.exit(1)

    pool = load_pool()
    existing_keys = {dedup_key(l["businessName"], l["address"]) for l in pool["leads"]}
    now = datetime.now(timezone.utc).isoformat()
    added, skipped = 0, 0

    for row in rows:
        name = (row.get("name") or "").strip()
        address = (row.get("full_address") or "").strip()
        if not name:
            continue
        key = dedup_key(name, address)
        if key in existing_keys:
            skipped += 1
            continue
        existing_keys.add(key)
        rating = (row.get("star_rating") or "").strip() or None
        review_count_raw = (row.get("review_count") or "").strip()
        review_count = int(review_count_raw) if review_count_raw.isdigit() else None
        lead = {
            "id": f"lead-{slugify(name)}-{datetime.now(timezone.utc).strftime('%Y%m%d')}",
            "businessName": name,
            "address": address,
            "category": row.get("category", "").strip() or None,
            "rating": rating,
            "reviewCount": review_count,
            "avgPricePerPerson": (row.get("avg_price_per_person") or row.get("average_price_per_person_range") or "").strip() or None,
            "instagramHandle": None,
            "phone": None,
            "segment": "nigeria-dm",
            "contactMethod": None,
            "status": "NeedsContactInfo",
            "leadPotential": score_lead_potential(rating, review_count),
            "notes": "",
            "source": {
                "provider": "browseract",
                "workflowId": workflow_id,
                "workflowName": args.workflow_name,
                "taskId": args.task_id,
            },
            "addedAt": now,
            "lastUpdatedAt": None,
        }
        pool["leads"].append(lead)
        added += 1

    pool["meta"]["updatedAt"] = now
    save_pool(pool)
    print(f"Added {added} leads, skipped {skipped} duplicates. Pool now has {len(pool['leads'])} leads.")


if __name__ == "__main__":
    main()

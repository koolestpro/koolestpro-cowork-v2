#!/usr/bin/env python3
"""
reddit_search.py — Reddit trend search for koolestpro-trend-radar.

STATUS (updated 2026-08-11): LIVE. Ridwan chose Apify over a dedicated Reddit
API reseller (Reddit's own official commercial API floors at $12,000/year,
a non-starter per Step 11). This project already had an Apify account wired
in .env (APIFY_USER_ID / APIFY_API_TOKEN, originally added for
page-presentation-kit-adjacent work), so Reddit search now runs through the
"Reddit Scraper Lite" actor (id oAuCIx3ItNrs2okjQ, by trudax), which needs
no separate signup or dedicated Reddit provider.

Verified live 2026-08-11: a 5-result "shopify cro" search actually returned
real Reddit posts (titles, subreddits, upvotes, comment counts, URLs) in
~25s end-to-end. Pay-per-result pricing, $0.004/result as of that test
(actor's own pricing tiers can shift — COST_PER_READ_DEFAULT below matches
what was actually charged, not a guess).

IMPORTANT — async run+poll, not run-sync: Apify's run-sync-get-dataset-items
endpoint blocks until the actor finishes, which took >45s in this project's
own interactive sandbox (that sandbox specifically enforces a ~45s per-command
ceiling — see CLAUDE.md's DeepSeek section for the same constraint elsewhere
in this project). This script always uses the async pattern (POST to start
the run, then poll GET .../actor-runs/{runId} every few seconds) so it
degrades gracefully to a slow-but-working call instead of a hard timeout,
regardless of which environment runs it (scheduled task vs interactive).

Usage:
    python3 reddit_search.py --query "shopify OR ecommerce CRO" \\
        --max-results 20 --monthly-cap 1.0 --ledger ../../../trend-radar-spend-ledger.json
"""

import argparse
import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from budget_ledger import check_and_reserve

COST_PER_READ_DEFAULT = 0.004
APIFY_ACTOR_ID = "oAuCIx3ItNrs2okjQ"  # Reddit Scraper Lite (trudax)
APIFY_API_BASE = "https://api.apify.com/v2"
POLL_INTERVAL_S = 4
POLL_TIMEOUT_S = 180


def engagement_score(post):
    upvotes = post.get("upVotes", post.get("score", 0)) or 0
    comments = post.get("numberOfComments", post.get("num_comments", 0)) or 0
    return upvotes + comments * 3


def run_apify_actor(token, search_query, max_results):
    """Start the Reddit Scraper Lite actor run, poll until done, return dataset items."""
    start_resp = requests.post(
        f"{APIFY_API_BASE}/acts/{APIFY_ACTOR_ID}/runs",
        params={"token": token},
        json={
            "searches": [search_query],
            "searchPosts": True,
            "searchComments": False,
            "searchCommunities": False,
            "searchUsers": False,
            "searchMedia": False,
            "skipComments": True,
            "skipUserPosts": True,
            "skipCommunity": True,
            "includeMediaLinks": True,
            "sort": "top",
            "time": "week",
            "maxItems": max_results,
            "includeNSFW": False,
        },
        timeout=30,
    )
    start_resp.raise_for_status()
    run_data = start_resp.json()["data"]
    run_id = run_data["id"]

    elapsed = 0
    status = run_data["status"]
    dataset_id = run_data.get("defaultDatasetId")
    while status in ("RUNNING", "READY") and elapsed < POLL_TIMEOUT_S:
        time.sleep(POLL_INTERVAL_S)
        elapsed += POLL_INTERVAL_S
        poll_resp = requests.get(f"{APIFY_API_BASE}/actor-runs/{run_id}", headers={"Authorization": f"Bearer {token}"}, timeout=30)
        poll_resp.raise_for_status()
        poll_data = poll_resp.json()["data"]
        status = poll_data["status"]
        dataset_id = poll_data.get("defaultDatasetId", dataset_id)

    if status != "SUCCEEDED":
        raise RuntimeError(f"Apify run ended with status={status} after {elapsed}s (run_id={run_id})")

    items_resp = requests.get(f"{APIFY_API_BASE}/datasets/{dataset_id}/items", headers={"Authorization": f"Bearer {token}"}, timeout=30)
    items_resp.raise_for_status()
    return items_resp.json()


def main():
    ap = argparse.ArgumentParser(description="Reddit trend search via Apify Reddit Scraper Lite.")
    ap.add_argument("--query", required=True)
    ap.add_argument("--max-results", type=int, default=20, help="Weekly cap per Step 11 (default 20 — keep small, this is pay-per-result)")
    ap.add_argument("--monthly-cap", type=float, default=1.0)
    ap.add_argument("--cost-per-read", type=float, default=COST_PER_READ_DEFAULT)
    ap.add_argument("--ledger", default="trend-radar-spend-ledger.json")
    ap.add_argument("--env-file", default=None)
    args = ap.parse_args()

    load_dotenv(args.env_file) if args.env_file else load_dotenv()
    token = os.environ.get("APIFY_API_TOKEN")

    if not token:
        print(json.dumps({
            "error": None,
            "blocked": True,
            "reason": "APIFY_API_TOKEN not set — this project already has this key wired in .env for "
                      "other Apify work, so if this fires it means .env failed to load, not a missing signup.",
            "results": []
        }, indent=2))
        sys.exit(0)

    estimated_cost = args.max_results * args.cost_per_read
    ok, reason = check_and_reserve(args.ledger, "reddit", estimated_cost, args.monthly_cap)
    if not ok:
        print(json.dumps({"error": reason, "results": [], "skipped": True}))
        sys.exit(0)

    try:
        posts = run_apify_actor(token, args.query, args.max_results)
    except Exception as e:
        print(json.dumps({"error": f"Apify Reddit Scraper Lite failed: {e}", "results": []}))
        sys.exit(1)

    ranked = sorted(
        (
            {
                "id": p.get("id") or p.get("postId"),
                "title": p.get("title", ""),
                "url": p.get("url") or p.get("permalink"),
                "subreddit": p.get("communityName"),
                "score": engagement_score(p),
                "created_utc": p.get("createdAt") or p.get("created_utc"),
            }
            for p in posts
        ),
        key=lambda x: x["score"],
        reverse=True,
    )

    print(json.dumps({"error": None, "blocked": False, "query": args.query, "cost_estimate": round(estimated_cost, 4), "results": ranked}, indent=2))


if __name__ == "__main__":
    main()

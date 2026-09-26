#!/usr/bin/env python3
"""
x_search.py — X (Twitter) API v2 recent search for koolestpro-trend-radar.

Uses the official pay-per-use API, app-only Bearer token auth (read-only,
no browser OAuth login needed — fits unattended scheduled runs). Endpoint:
GET https://api.x.com/2/tweets/search/recent

Auth: reads X_BEARER_TOKEN from the environment (loaded from this project's
.env via python-dotenv). This is the token from the X Developer Portal's
"Keys and tokens" tab, labeled "Bearer Token" — NOT the API Key/Secret or
the OAuth2 Access Token/Secret already used for posting via Make.com. Those
are different credentials for a different purpose (posting vs. reading).

Budget: every call reserves its estimated cost ($0.005/post read) against
budget_ledger.py BEFORE hitting the network. If the reservation would exceed
the monthly cap, the script exits 0 with a message and writes no results —
this is a deliberate no-op, not a failure, matching Step 11's "halt rather
than overspend" rule.

Usage:
    python3 x_search.py --query "shopify CRO OR ecommerce conversion" \\
        --max-results 50 --monthly-cap 5.0 --ledger ../../../trend-radar-spend-ledger.json

Output: JSON array to stdout, ranked by a simple engagement score
(likes + retweets*2 + replies*3, replies weighted highest since a reply
is the strongest engagement signal — same weighting logic Charlie Hills'
post-scorer skill uses for LinkedIn, adapted here for X's metric names).
"""

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from budget_ledger import check_and_reserve

X_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
COST_PER_READ = 0.005


def engagement_score(metrics):
    return (
        metrics.get("like_count", 0)
        + metrics.get("retweet_count", 0) * 2
        + metrics.get("reply_count", 0) * 3
    )


def main():
    ap = argparse.ArgumentParser(description="Recent-search X for trend signal in a niche.")
    ap.add_argument("--query", required=True, help="X search query (recent search syntax, last 7 days)")
    ap.add_argument("--max-results", type=int, default=50, help="Cap on posts read this run (default 50, Step 11's weekly cap)")
    ap.add_argument("--monthly-cap", type=float, default=5.0, help="Monthly USD cap shared with X posting spend")
    ap.add_argument("--ledger", default="trend-radar-spend-ledger.json")
    ap.add_argument("--env-file", default=None, help="Path to .env (defaults to project root .env via load_dotenv() search)")
    args = ap.parse_args()

    load_dotenv(args.env_file) if args.env_file else load_dotenv()
    token = os.environ.get("X_BEARER_TOKEN")
    if not token:
        print(json.dumps({
            "error": "X_BEARER_TOKEN not set. Get it from developer.x.com -> your app -> "
                     "Keys and tokens -> Bearer Token, then add X_BEARER_TOKEN=... to .env.",
            "results": []
        }))
        sys.exit(1)

    # X API caps max_results per single call at 100; this project's weekly cap is
    # already well under that, but clamp defensively regardless of what's passed in.
    max_results = max(10, min(args.max_results, 100))
    estimated_cost = max_results * COST_PER_READ

    ok, reason = check_and_reserve(args.ledger, "x", estimated_cost, args.monthly_cap)
    if not ok:
        print(json.dumps({"error": reason, "results": [], "skipped": True}))
        sys.exit(0)

    resp = requests.get(
        X_SEARCH_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "query": args.query,
            "max_results": max_results,
            "tweet.fields": "public_metrics,created_at,author_id,text",
        },
        timeout=30,
    )

    if resp.status_code != 200:
        print(json.dumps({
            "error": f"X API returned {resp.status_code}: {resp.text[:500]}",
            "results": []
        }))
        sys.exit(1)

    data = resp.json().get("data", [])
    ranked = sorted(
        (
            {
                "id": t["id"],
                "text": t.get("text", ""),
                "author_id": t.get("author_id"),
                "created_at": t.get("created_at"),
                "metrics": t.get("public_metrics", {}),
                "score": engagement_score(t.get("public_metrics", {})),
                "url": f"https://x.com/i/web/status/{t['id']}",
            }
            for t in data
        ),
        key=lambda x: x["score"],
        reverse=True,
    )

    print(json.dumps({"error": None, "query": args.query, "cost_estimate": round(estimated_cost, 4), "results": ranked}, indent=2))


if __name__ == "__main__":
    main()

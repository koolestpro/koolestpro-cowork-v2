#!/usr/bin/env python3
"""
apify_client.py — thin wrapper around Apify's REST API, generic across
actors. Same pattern as browseract_client.py in this same tools/ dir:
key lives in .env, called directly from bash inside Cowork.

Docs: https://docs.apify.com/api/v2

Setup: .env needs APIFY_API_TOKEN (already set as of 2026-08-02 per
docs/koolestpro-growth-operating-plan.md Section C2 — Apify was verified
working for this project before this script existed, for a different
actor (Reddit search). This script has NOT been run live yet — the
run_actor_sync() call below is standard Apify API shape, but the actual
INPUT FIELD NAMES an actor expects are actor-specific. Run
`python3 apify_client.py get-actor --actor-id <id>` once before trusting
any script that builds input for a new actor, to confirm field names
against the actor's real input schema rather than a guess.

Usage:
  python3 apify_client.py run-sync --actor-id curious_coder~facebook-ads-library-scraper --input '{...}'
  python3 apify_client.py get-actor --actor-id curious_coder~facebook-ads-library-scraper
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.apify.com/v2"


def load_api_token():
    tok = os.environ.get("APIFY_API_TOKEN")
    if tok:
        return tok
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
    env_path = os.path.normpath(env_path)
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("APIFY_API_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _request(method, path, token, body=None, timeout=180):
    url = f"{API_BASE}{path}{'&' if '?' in path else '?'}token={token}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")
        print(f"HTTP {e.code} from {url.split('?')[0]}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error calling {url.split('?')[0]}: {e}", file=sys.stderr)
        sys.exit(1)


def run_actor_sync(token, actor_id, run_input, timeout=280):
    """Runs an actor and blocks until the dataset items are ready. actor_id
    uses '~' in place of '/' per Apify's REST convention (org~actor-name)."""
    return _request("POST", f"/acts/{actor_id}/run-sync-get-dataset-items", token, run_input, timeout=timeout)


def get_actor(token, actor_id):
    """Fetch actor metadata, including its declared input schema — call this
    first for any actor this project hasn't used before."""
    return _request("GET", f"/acts/{actor_id}", token)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run-sync")
    p_run.add_argument("--actor-id", required=True)
    p_run.add_argument("--input", required=True, help="JSON object, actor-specific")

    p_get = sub.add_parser("get-actor")
    p_get.add_argument("--actor-id", required=True)

    args = p.parse_args()
    token = load_api_token()
    if not token:
        print("APIFY_API_TOKEN not set in environment or .env.", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "run-sync":
        try:
            run_input = json.loads(args.input)
        except json.JSONDecodeError as e:
            print(f"--input must be valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(run_actor_sync(token, args.actor_id, run_input), indent=2))
    elif args.cmd == "get-actor":
        print(json.dumps(get_actor(token, args.actor_id), indent=2))


if __name__ == "__main__":
    main()

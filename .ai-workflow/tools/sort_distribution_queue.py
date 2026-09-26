#!/usr/bin/env python3
"""
sort_distribution_queue.py — keeps the live "Koolestpro Distribution Queue"
Google Sheet sorted so Ridwan never has to scroll to find what needs his
attention today.

REWRITTEN 2026-09-19 per Ridwan's instruction — this REPLACES the
2026-08-27 platform-first sort (Twitter block / LinkedIn block / Instagram
block, each old->new by date). The new priority is:

    1. Posted rows sink to the very bottom (status == "Posted").
       Everything not yet posted (Ready, Draft, Needs Review, Failed) stays
       on top, because that's the only stuff Ridwan can still act on.
    2. Within the not-yet-posted block, sort by scheduled_date ascending —
       today's posts first, then tomorrow's, and so on. This is the actual
       point of the change: Ridwan wants "what's going out today" at the
       top without scrolling, not a platform-grouped view.
    3. Within the same date, platform order is Twitter, then LinkedIn, then
       Instagram (same relative order as before, just no longer the primary
       key).
    4. Within the same date + platform, Ready sorts before everything else
       (Draft / Needs Review / Failed) — the approved, about-to-go-out post
       is what Ridwan wants to see first when he opens the row group.

Confirmed with Ridwan 2026-09-19 (AskUserQuestion): Needs Review and Failed
share the same tier as Draft (they're not hidden away, just not first), and
posted rows are ordered the same way among themselves (date -> platform) so
the block is still browsable, it's just parked below everything actionable.

What it does, in order:
1. Clears any regular (non-Filter-View) basicFilter — it silently blocks
   sortRange with a 200 OK / zero rows moved, so this runs unconditionally
   every time as insurance (see the 2026-08-27 gotcha, still applies).
2. Normalizes column E (scheduled_date) to a real Sheets DATE type via
   USER_ENTERED. Rows written by the reschedule webhook (Make.com scenario
   7111659) or some older append paths land as plain TEXT, and a
   text-typed date cell sorts to the very end of its group regardless of
   its actual value — re-writing the whole column re-parses every cell
   uniformly.
3. Recomputes three hidden helper columns fresh every run (so it's always
   correct even for brand-new rows appended since the last sort):
     Q = posted_tier         (0 = not posted, 1 = posted == status "Posted")
     R = platform_priority   (Twitter=1, LinkedIn=2, Instagram=3, else 9)
     S = status_priority     (Ready=1, everything else unposted=2)
4. Runs one sortRange over A2:S<lastrow>, sorted by Q asc, then E
   (scheduled_date) asc, then R asc, then S asc.

GOTCHA — a plain (non-Filter-View) "Create a filter" on this sheet SILENTLY
BLOCKS sortRange from doing anything (no error, 200 OK, zero rows moved —
this cost real debugging time 2026-08-27). Step 0 below clears a basicFilter
every run so this shouldn't recur, but if a future sort mysteriously does
nothing, check for and clear a basicFilter first.

Does NOT touch Filter Views ("Needs Review", "Today", filterViewIds
917994328 / 272904531) or the hidden-column state of Q:S; both persist
independently of a basicFilter clear/re-sort.

Usage:
    python3 sort_distribution_queue.py [--project-root DIR]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse

SHEET_ID = "1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg"
SHEET_TAB = "Untitled"
GID = 1006869904
PLATFORM_PRIORITY = {"Twitter": 1, "LinkedIn": 2, "Instagram": 3}


def find_root(start):
    d = os.path.abspath(start)
    while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
        d = os.path.dirname(d)
    return d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.abspath(start)


def load_env(root):
    env = {}
    path = os.path.join(root, ".env")
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def http_json(url, data=None, headers=None, method=None):
    body = None
    hdrs = dict(headers or {})
    if data is not None:
        if isinstance(data, dict) and hdrs.get("Content-Type", "").startswith("application/x-www-form-urlencoded"):
            body = urllib.parse.urlencode(data).encode()
        else:
            body = json.dumps(data).encode()
            hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} calling {url}: {e.read().decode()}") from None


def get_access_token(env):
    missing = [k for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN") if k not in env]
    if missing:
        sys.exit(f"missing from .env: {missing}")
    resp = http_json(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": env["GOOGLE_OAUTH_CLIENT_ID"],
            "client_secret": env["GOOGLE_OAUTH_CLIENT_SECRET"],
            "refresh_token": env["GOOGLE_OAUTH_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if "access_token" not in resp:
        raise RuntimeError(f"token refresh failed: {resp}")
    return resp["access_token"]


def main():
    ap = argparse.ArgumentParser(description="Sort the live Distribution Queue sheet: unposted-first by date, then platform, then Ready-first.")
    ap.add_argument("--project-root", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.project_root) if args.project_root else find_root(os.getcwd())
    env = load_env(root)
    token = get_access_token(env)
    H = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Step 0: clear any regular (non-Filter-View) basicFilter — it silently blocks sortRange.
    http_json(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate",
        data={"requests": [{"clearBasicFilter": {"sheetId": GID}}]},
        headers=H, method="POST",
    )

    # Step 1: read platform (D) + date (E) + status (K) for every data row.
    vals = http_json(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{urllib.parse.quote(SHEET_TAB)}!A1:K2000",
        headers=H, method="GET",
    )
    rows = vals["values"]
    last_row = len(rows)  # 1-indexed, includes header
    print(f"[sort-queue] total rows incl header: {last_row}")

    posted_tier = ["posted_tier"]
    platform_priority = ["platform_priority"]
    status_priority = ["status_priority"]
    dates = [rows[0][4] if len(rows[0]) > 4 else "scheduled_date"]
    counts = {"posted": 0, "ready": 0, "other_unposted": 0}
    for r in rows[1:]:
        platform = r[3] if len(r) > 3 else ""
        status = (r[10] if len(r) > 10 else "").strip()
        is_posted = status.lower() == "posted"
        posted_tier.append(1 if is_posted else 0)
        platform_priority.append(PLATFORM_PRIORITY.get(platform, 9))
        status_priority.append(1 if status.lower() == "ready" else 2)
        dates.append(r[4] if len(r) > 4 else "")
        if is_posted:
            counts["posted"] += 1
        elif status.lower() == "ready":
            counts["ready"] += 1
        else:
            counts["other_unposted"] += 1
    # fix header rows (first element of each list should just be the label, not [label])
    posted_tier[0] = "posted_tier"
    platform_priority[0] = "platform_priority"
    status_priority[0] = "status_priority"
    print(f"[sort-queue] status breakdown: {counts['ready']} Ready, "
          f"{counts['other_unposted']} Draft/Needs Review/Failed, {counts['posted']} Posted")

    # Step 2: normalize scheduled_date column to real Date type via USER_ENTERED.
    http_json(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{urllib.parse.quote(SHEET_TAB)}!E2:E{last_row}?valueInputOption=USER_ENTERED",
        data={"values": [[d] for d in dates[1:]]}, headers=H, method="PUT",
    )
    print("[sort-queue] normalized scheduled_date column to real Date type")

    # Step 3: write/refresh helper columns Q (posted_tier), R (platform_priority), S (status_priority).
    http_json(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values:batchUpdate",
        data={
            "valueInputOption": "RAW",
            "data": [
                {"range": f"{urllib.parse.quote(SHEET_TAB)}!Q1:Q{last_row}", "values": [[v] for v in posted_tier]},
                {"range": f"{urllib.parse.quote(SHEET_TAB)}!R1:R{last_row}", "values": [[v] for v in platform_priority]},
                {"range": f"{urllib.parse.quote(SHEET_TAB)}!S1:S{last_row}", "values": [[v] for v in status_priority]},
            ]
        },
        headers=H, method="POST",
    )
    print(f"[sort-queue] refreshed helper columns Q1:S{last_row} (posted_tier, platform_priority, status_priority)")

    # Step 4: sort A2:S<last_row> by Q asc (unposted first), E asc (date), R asc (platform), S asc (Ready first).
    sort_req = {
        "requests": [
            {
                "sortRange": {
                    "range": {
                        "sheetId": GID,
                        "startRowIndex": 1,
                        "endRowIndex": last_row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 19,  # A:S
                    },
                    "sortSpecs": [
                        {"dimensionIndex": 16, "sortOrder": "ASCENDING"},  # Q posted_tier
                        {"dimensionIndex": 4, "sortOrder": "ASCENDING"},   # E scheduled_date
                        {"dimensionIndex": 17, "sortOrder": "ASCENDING"},  # R platform_priority
                        {"dimensionIndex": 18, "sortOrder": "ASCENDING"},  # S status_priority
                    ],
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": GID, "dimension": "COLUMNS", "startIndex": 16, "endIndex": 19},
                    "properties": {"hiddenByUser": True},
                    "fields": "hiddenByUser",
                }
            },
        ]
    }
    http_json(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate", data=sort_req, headers=H, method="POST")
    print("[sort-queue] sorted: unposted-first, by date, then Twitter/LinkedIn/Instagram, then Ready-first; Posted at the bottom")


if __name__ == "__main__":
    main()

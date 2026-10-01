#!/usr/bin/env python3
"""Pull Google Search Console (and optionally GA4) data for a client run.

Env (repo-root .env or cloud secrets):
  GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET   OAuth client (type: Desktop app)
  GOOGLE_REFRESH_TOKEN                     from `gsc_pull.py auth`

client.json:
  gsc_property      e.g. "sc-domain:tapandrate.co.uk" or "https://tapandrate.co.uk/"
  ga4_property_id   e.g. "123456789" (optional)

Usage:
  python3 seo/tools/gsc_pull.py auth
  python3 seo/tools/gsc_pull.py check --client tapandrate
  python3 seo/tools/gsc_pull.py pull --client tapandrate --days 28 [--out <run dir>]
"""
import argparse
import json
import os
import sys
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

from _common import client_dir, http, load_client, load_env

SCOPES = "https://www.googleapis.com/auth/webmasters.readonly https://www.googleapis.com/auth/analytics.readonly"
REDIRECT = "http://localhost"


def need(*names):
    load_env()
    vals = [os.environ.get(n) for n in names]
    missing = [n for n, v in zip(names, vals) if not v]
    if missing:
        print(f"NO_CREDENTIALS: missing {', '.join(missing)}", file=sys.stderr)
        sys.exit(3)
    return vals


def access_token():
    cid, secret, refresh = need("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN")
    status, body = http("https://oauth2.googleapis.com/token", data=urllib.parse.urlencode({
        "client_id": cid, "client_secret": secret, "refresh_token": refresh, "grant_type": "refresh_token",
    }), headers={"Content-Type": "application/x-www-form-urlencoded"})
    if status != 200:
        sys.exit(f"Token refresh failed ({status}): {body[:300]}")
    return json.loads(body)["access_token"]


def cmd_auth(_):
    cid, secret = need("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET")
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": REDIRECT, "response_type": "code",
        "scope": SCOPES, "access_type": "offline", "prompt": "consent",
    })
    print("1. Open this URL, sign in with the Google account that has GSC + GA4 access:\n")
    print(url)
    print("\n2. The browser lands on a localhost page that won't load. That's expected.")
    print("   Copy the full URL from the address bar (or just the code= value) and paste it here.")
    raw = input("\nURL or code: ").strip()
    code = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query).get("code", [raw])[0]
    status, body = http("https://oauth2.googleapis.com/token", data=urllib.parse.urlencode({
        "client_id": cid, "client_secret": secret, "code": code,
        "redirect_uri": REDIRECT, "grant_type": "authorization_code",
    }), headers={"Content-Type": "application/x-www-form-urlencoded"})
    if status != 200:
        sys.exit(f"Exchange failed ({status}): {body[:300]}")
    tok = json.loads(body)
    print("\nSave this as a secret (cloud env) and in .env (desktop):\n")
    print(f"GOOGLE_REFRESH_TOKEN={tok.get('refresh_token')}")


def gsc_query(tok, prop, start, end, dims, limit=1000):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(prop, safe='')}/searchAnalytics/query"
    status, body = http(url, data={
        "startDate": start.isoformat(), "endDate": end.isoformat(),
        "dimensions": dims, "rowLimit": limit, "dataState": "final",
    }, headers={"Authorization": f"Bearer {tok}"})
    if status != 200:
        sys.exit(f"GSC {dims} failed ({status}): {body[:400]}")
    rows = json.loads(body).get("rows", [])
    return [dict(zip(dims, r["keys"]), clicks=r["clicks"], impressions=r["impressions"],
                 ctr=round(r["ctr"], 4), position=round(r["position"], 1)) for r in rows]


def ga4_report(tok, prop_id, start, end):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport"
    status, body = http(url, data={
        "dateRanges": [{"startDate": start.isoformat(), "endDate": end.isoformat()}],
        "dimensions": [{"name": "landingPagePlusQueryString"}],
        "metrics": [{"name": n} for n in ("sessions", "engagedSessions", "userEngagementDuration", "keyEvents", "totalRevenue")],
        "dimensionFilter": {"filter": {"fieldName": "sessionDefaultChannelGroup",
                                       "stringFilter": {"value": "Organic Search"}}},
        "limit": 500,
    }, headers={"Authorization": f"Bearer {tok}"})
    if status != 200:
        return {"error": f"GA4 failed ({status}): {body[:400]}"}
    data = json.loads(body)
    names = [m["name"] for m in data.get("metricHeaders", [])]
    return [dict(landing_page=r["dimensionValues"][0]["value"],
                 **{n: float(v["value"]) for n, v in zip(names, r["metricValues"])})
            for r in data.get("rows", [])]


def cmd_check(args):
    cfg = load_client(args.client)
    tok = access_token()
    status, body = http("https://www.googleapis.com/webmasters/v3/sites", headers={"Authorization": f"Bearer {tok}"})
    sites = [s["siteUrl"] for s in json.loads(body).get("siteEntry", [])] if status == 200 else []
    print("GSC properties this account can see:", *sites, sep="\n  ")
    print("client.json gsc_property:", cfg.get("gsc_property"), "OK" if cfg.get("gsc_property") in sites else "NOT FOUND")


def cmd_pull(args):
    cfg = load_client(args.client)
    prop = cfg.get("gsc_property")
    if not prop:
        sys.exit("client.json has no gsc_property")
    tok = access_token()
    end = date.today() - timedelta(days=3)  # GSC 'final' data lags ~2-3 days
    start = end - timedelta(days=args.days - 1)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=args.days - 1)

    out = {
        "property": prop,
        "period": [start.isoformat(), end.isoformat()],
        "previous_period": [prev_start.isoformat(), prev_end.isoformat()],
        "pages": gsc_query(tok, prop, start, end, ["page"]),
        "pages_prev": gsc_query(tok, prop, prev_start, prev_end, ["page"]),
        "queries": gsc_query(tok, prop, start, end, ["query"]),
        "page_queries": gsc_query(tok, prop, start, end, ["page", "query"], 5000),
    }
    run = Path(args.out) if args.out else client_dir(args.client) / "runs" / date.today().isoformat()
    run.mkdir(parents=True, exist_ok=True)
    (run / "gsc.json").write_text(json.dumps(out, indent=1))
    tot = lambda rows, k: sum(r[k] for r in rows)
    print(f"GSC {start}..{end}: clicks {tot(out['pages'], 'clicks')}, impressions {tot(out['pages'], 'impressions')} "
          f"(prev clicks {tot(out['pages_prev'], 'clicks')}) -> {run / 'gsc.json'}")

    if cfg.get("ga4_property_id"):
        ga = {"period": out["period"], "organic_landing_pages": ga4_report(tok, cfg["ga4_property_id"], start, end)}
        (run / "ga4.json").write_text(json.dumps(ga, indent=1))
        print(f"GA4 organic landing pages -> {run / 'ga4.json'}")
    else:
        print("GA4 skipped: no ga4_property_id in client.json")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth").set_defaults(fn=cmd_auth)
    c = sub.add_parser("check"); c.add_argument("--client", required=True); c.set_defaults(fn=cmd_check)
    p = sub.add_parser("pull"); p.add_argument("--client", required=True)
    p.add_argument("--days", type=int, default=28); p.add_argument("--out"); p.set_defaults(fn=cmd_pull)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

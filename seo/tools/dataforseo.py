#!/usr/bin/env python3
"""DataForSEO client for the SEO engine: keywords, SERPs, rankings, competitors, backlinks.

Primary data provider for every project (Ubersuggest MCP is the fallback). Pay as you go,
billed per call, so every command prints the cost DataForSEO reports.

Env (repo-root .env or cloud secrets):
  DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD   (API credentials from app.dataforseo.com, not the site login)

Location codes match Ubersuggest locIds: 2826 UK, 2840 US, 2566 Nigeria, 2124 Canada.
Defaults come from client.json (`ubersuggest_loc_id`, `language`) when --client is given.

Usage:
  dataforseo.py balance
  dataforseo.py ideas       --client tapandrate --seed "google review nfc card" [--limit 100]
  dataforseo.py overview    --client tapandrate --keywords "kw one,kw two"
  dataforseo.py serp        --client tapandrate --keyword "how to get more google reviews"
  dataforseo.py ranked      --client tapandrate [--domain x.com] [--limit 200]
  dataforseo.py competitors --client tapandrate
  dataforseo.py gap         --client tapandrate --competitor seritag.com
  dataforseo.py backlinks   --client tapandrate        (summary + top referring domains)
  dataforseo.py rank        --client tapandrate        (positions for client.json tracked_keywords -> rank-log.csv)
Add --out <file.json> to save the raw result.
"""
import argparse
import base64
import csv
import json
import os
import sys
from datetime import date
from pathlib import Path

from _common import client_dir, http, load_client, load_env

API = "https://api.dataforseo.com/v3"


def auth_header():
    load_env()
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not pw:
        print("NO_CREDENTIALS: set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD", file=sys.stderr)
        sys.exit(3)
    return {"Authorization": "Basic " + base64.b64encode(f"{login}:{pw}".encode()).decode()}


def call(path, payload=None):
    status, body = http(f"{API}/{path}", data=[payload] if payload is not None else None,
                        headers=auth_header(), method="POST" if payload is not None else "GET", timeout=120)
    if status != 200:
        sys.exit(f"DataForSEO HTTP {status}: {body[:400]}")
    out = json.loads(body)
    task = (out.get("tasks") or [{}])[0]
    if task.get("status_code", 20000) >= 40000:
        sys.exit(f"DataForSEO error {task.get('status_code')}: {task.get('status_message')}")
    print(f"[cost ${out.get('cost', 0):.4f}]", file=sys.stderr)
    return (task.get("result") or [{}])[0] or {}


def loc(args, cfg):
    return {"location_code": args.loc or cfg.get("ubersuggest_loc_id", 2826),
            "language_code": (args.lang or cfg.get("language", "en")).split("-")[0]}


def kw_row(k):
    info = k.get("keyword_info") or {}
    props = k.get("keyword_properties") or {}
    intent = (k.get("search_intent_info") or {}).get("main_intent")
    return {"keyword": k.get("keyword"), "volume": info.get("search_volume"), "cpc": info.get("cpc"),
            "difficulty": props.get("keyword_difficulty"), "intent": intent,
            "competition": info.get("competition_level")}


def emit(rows, args):
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
        print(f"saved {len(rows) if isinstance(rows, list) else 1} rows -> {args.out}", file=sys.stderr)
    print(json.dumps(rows, indent=1, ensure_ascii=False))


def domain_of(args, cfg):
    return args.domain or cfg["site_url"].split("//")[-1].strip("/").removeprefix("www.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["balance", "ideas", "overview", "serp", "ranked", "competitors",
                                    "gap", "backlinks", "rank"])
    ap.add_argument("--client")
    ap.add_argument("--domain")
    ap.add_argument("--seed")
    ap.add_argument("--keyword")
    ap.add_argument("--keywords")
    ap.add_argument("--competitor")
    ap.add_argument("--loc", type=int)
    ap.add_argument("--lang")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--out")
    args = ap.parse_args()
    cfg = load_client(args.client) if args.client else {}

    if args.cmd == "balance":
        status, body = http(f"{API}/appendix/user_data", headers=auth_header())
        money = (json.loads(body)["tasks"][0]["result"][0] or {}).get("money", {})
        print(f"DataForSEO balance: ${money.get('balance')}")
        return

    L = loc(args, cfg)

    if args.cmd == "ideas":
        res = call("dataforseo_labs/google/keyword_ideas/live",
                   {"keywords": [s.strip() for s in args.seed.split(",")], **L, "limit": args.limit,
                    "include_serp_info": False, "order_by": ["keyword_info.search_volume,desc"]})
        emit([kw_row(k) for k in res.get("items", [])], args)

    elif args.cmd == "overview":
        res = call("dataforseo_labs/google/keyword_overview/live",
                   {"keywords": [k.strip() for k in args.keywords.split(",")], **L})
        emit([kw_row(k) for k in res.get("items", [])], args)

    elif args.cmd == "serp":
        res = call("serp/google/organic/live/advanced", {"keyword": args.keyword, **L, "depth": 20})
        rows = [{"type": i.get("type"), "rank": i.get("rank_group"), "domain": i.get("domain"),
                 "url": i.get("url"), "title": i.get("title"),
                 "question": i.get("title") if i.get("type") == "people_also_ask" else None}
                for i in res.get("items", []) if i.get("type") in ("organic", "people_also_ask", "ai_overview", "featured_snippet")]
        paa = [q.get("title") for i in res.get("items", []) if i.get("type") == "people_also_ask"
               for q in (i.get("items") or [])]
        emit({"keyword": args.keyword, "results": rows, "people_also_ask": paa}, args)

    elif args.cmd == "ranked":
        res = call("dataforseo_labs/google/ranked_keywords/live",
                   {"target": domain_of(args, cfg), **L, "limit": args.limit,
                    "order_by": ["ranked_serp_element.serp_item.etv,desc"]})
        rows = []
        for it in res.get("items", []):
            s = (it.get("ranked_serp_element") or {}).get("serp_item") or {}
            rows.append({**kw_row(it.get("keyword_data") or {}), "position": s.get("rank_group"),
                         "url": s.get("relative_url") or s.get("url"), "etv": s.get("etv")})
        emit(rows, args)

    elif args.cmd == "competitors":
        res = call("dataforseo_labs/google/competitors_domain/live",
                   {"target": domain_of(args, cfg), **L, "limit": 20, "exclude_top_domains": True})
        emit([{"domain": i.get("domain"), "common_keywords": i.get("intersections"),
               "avg_position": i.get("avg_position"),
               "etv": ((i.get("full_domain_metrics") or {}).get("organic") or {}).get("etv")}
              for i in res.get("items", [])], args)

    elif args.cmd == "gap":
        # keywords the competitor ranks for that we don't
        res = call("dataforseo_labs/google/domain_intersection/live",
                   {"target1": args.competitor, "target2": domain_of(args, cfg), **L,
                    "intersections": False, "limit": args.limit,
                    "order_by": ["keyword_data.keyword_info.search_volume,desc"]})
        emit([{**kw_row(i.get("keyword_data") or {}),
               "competitor_position": ((i.get("first_domain_serp_element") or {}).get("rank_group"))}
              for i in res.get("items", [])], args)

    elif args.cmd == "backlinks":
        target = domain_of(args, cfg)
        summ = call("backlinks/summary/live", {"target": target, "include_subdomains": True})
        refs = call("backlinks/referring_domains/live", {"target": target, "limit": 50, "order_by": ["rank,desc"]})
        emit({"target": target, "rank": summ.get("rank"), "backlinks": summ.get("backlinks"),
              "referring_domains": summ.get("referring_domains"),
              "top_referring": [{"domain": r.get("domain"), "rank": r.get("rank"), "backlinks": r.get("backlinks")}
                                for r in refs.get("items", [])]}, args)

    elif args.cmd == "rank":
        if not args.client:
            sys.exit("rank needs --client (reads tracked_keywords from client.json)")
        target = domain_of(args, cfg)
        kws = cfg.get("tracked_keywords", [])
        if not kws:
            sys.exit("client.json has no tracked_keywords")
        log = client_dir(args.client) / "rank-log.csv"
        new = not log.exists()
        rows = []
        for kw in kws:
            res = call("serp/google/organic/live/regular", {"keyword": kw, **L, "depth": 100})
            hit = next((i for i in res.get("items", []) if i.get("type") == "organic"
                        and target in (i.get("domain") or "")), None)
            rows.append({"date": date.today().isoformat(), "keyword": kw,
                         "position": hit.get("rank_group") if hit else "",
                         "url": hit.get("url") if hit else ""})
        with log.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["date", "keyword", "position", "url"])
            if new:
                w.writeheader()
            w.writerows(rows)
        emit(rows, args)


if __name__ == "__main__":
    main()

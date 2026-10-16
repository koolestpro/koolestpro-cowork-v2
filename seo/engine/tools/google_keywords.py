#!/usr/bin/env python3
"""Free keyword research from Google itself: Autocomplete ideas + Keyword Planner volumes.

The free alternative to DataForSEO. Three layers, use what the project has:
  1. Autocomplete (no key, always works): what people actually type, expanded with
     question words, comparisons and a-z. No volumes.
  2. Keyword Planner via the Google Ads API (free, needs setup in SETUP.md): ideas plus
     average monthly searches, competition and top-of-page bid range. Accounts with no ad
     spend may get rounded volumes, which is fine for prioritising.
  3. Search Console (gsc_pull.py): the queries this site already shows up for, which beats any tool.

Env (this project's .env), only for layer 2:
  GOOGLE_ADS_DEVELOPER_TOKEN     needs Basic access (Explorer access blocks keyword planning)
  GOOGLE_ADS_CUSTOMER_ID         the Ads account to plan with, digits only (no dashes)
  GOOGLE_ADS_LOGIN_CUSTOMER_ID   manager account ID, if access goes through one (optional)
  GOOGLE_CLIENT_ID / _SECRET / GOOGLE_REFRESH_TOKEN   shared Google sign-in (gsc_pull.py auth)
  GOOGLE_ADS_API_VERSION         optional, default v23

Usage:
  google_keywords.py suggest  --seed "replo vs,hire a replo developer" [--deep]
  google_keywords.py ideas    --seed "shopify landing page designer" [--url https://site/page] [--limit 100]
  google_keywords.py volume   --keywords "replo vs pagefly,replo vs shogun"
  google_keywords.py research --seed "replo developer" [--deep]   (suggest, then volumes if Planner is set up)
  google_keywords.py check                                        (is Keyword Planner reachable?)
Location/language come from project.json (`location_code`, `language`). Add --out file.json to save.
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path

from _common import google_access_token, http, load_env, load_project, need_env

QUESTION_MODS = ["how to", "what is", "why", "best", "cost of", "is"]
SUFFIX_MODS = ["vs", "for", "alternative", "price", "near me", "uk", "review", "examples", "not working"]
LANG_IDS = {"en": 1000, "de": 1001, "fr": 1002, "es": 1003, "it": 1004, "nl": 1010, "pt": 1014, "ar": 1019}
GL = {2826: "uk", 2840: "us", 2566: "ng", 2124: "ca", 2036: "au", 2372: "ie", 2276: "de"}


def autocomplete(q, gl, hl):
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "firefox", "hl": hl, "gl": gl, "q": q})
    status, body = http(url)
    if status != 200:
        return []
    try:
        return json.loads(body)[1]
    except (ValueError, IndexError):
        return []


def cmd_suggest(seeds, cfg, deep=False):
    gl = GL.get(int(cfg.get("location_code", 2826)), "uk")
    hl = cfg.get("language", "en").split("-")[0]
    seen, out = set(), []
    for seed in seeds:
        queries = [seed, seed + " "] + [f"{m} {seed}" for m in QUESTION_MODS] + [f"{seed} {m}" for m in SUFFIX_MODS]
        if deep:
            queries += [f"{seed} {c}" for c in "abcdefghijklmnopqrstuvwxyz"]
        words = {w for w in seed.lower().split() if len(w) > 2}
        for q in queries:
            for s in autocomplete(q, gl, hl):
                k = s.strip().lower()
                if k and k not in seen and (not words or words & set(k.split())):
                    seen.add(k)
                    out.append({"keyword": k, "from": q, "source": "autocomplete"})
            time.sleep(0.15)
    return out


def ads_ctx(cfg):
    dev, cust = need_env("GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CUSTOMER_ID")
    load_env()
    ver = os.environ.get("GOOGLE_ADS_API_VERSION", "v23")
    headers = {"developer-token": dev, "Authorization": f"Bearer {google_access_token()}"}
    login = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "").replace("-", "")
    if login:
        headers["login-customer-id"] = login
    base = f"https://googleads.googleapis.com/{ver}/customers/{cust.replace('-', '')}"
    geo = f"geoTargetConstants/{cfg.get('location_code', 2826)}"
    lang = f"languageConstants/{cfg.get('google_ads_language_id') or LANG_IDS.get(cfg.get('language', 'en').split('-')[0], 1000)}"
    return base, headers, geo, lang


def ads_call(base, headers, method, payload):
    status, body = http(f"{base}:{method}", data=payload, headers=headers, method="POST", timeout=90)
    if status != 200:
        hint = ""
        if "DEVELOPER_TOKEN_NOT_APPROVED" in body or "not approved" in body.lower():
            hint = "\nHint: the developer token needs Basic access for Keyword Planner (see SETUP.md)."
        sys.exit(f"Google Ads API {status}: {body[:600]}{hint}")
    return json.loads(body)


def metrics_row(text, m, source):
    lo, hi = m.get("lowTopOfPageBidMicros"), m.get("highTopOfPageBidMicros")
    return {"keyword": text, "volume": int(m["avgMonthlySearches"]) if m.get("avgMonthlySearches") else None,
            "competition": m.get("competition"), "competition_index": m.get("competitionIndex"),
            "cpc_low": round(int(lo) / 1e6, 2) if lo else None, "cpc_high": round(int(hi) / 1e6, 2) if hi else None,
            "trend": [int(x.get("monthlySearches", 0)) for x in (m.get("monthlySearchVolumes") or [])][-12:],
            "source": source}


def cmd_ideas(seeds, cfg, url=None, limit=100):
    base, headers, geo, lang = ads_ctx(cfg)
    payload = {"language": lang, "geoTargetConstants": [geo], "keywordPlanNetwork": "GOOGLE_SEARCH",
               "includeAdultKeywords": False, "pageSize": min(limit, 1000)}
    if seeds and url:
        payload["keywordAndUrlSeed"] = {"keywords": seeds, "url": url}
    elif url:
        payload["urlSeed"] = {"url": url}
    else:
        payload["keywordSeed"] = {"keywords": seeds}
    res = ads_call(base, headers, "generateKeywordIdeas", payload)
    rows = [metrics_row(r["text"], r.get("keywordIdeaMetrics") or {}, "keyword_planner") for r in res.get("results", [])]
    return sorted(rows, key=lambda r: r["volume"] or 0, reverse=True)[:limit]


def cmd_volume(keywords, cfg):
    base, headers, geo, lang = ads_ctx(cfg)
    rows = []
    for i in range(0, len(keywords), 700):  # stay well inside the per-request keyword limit
        res = ads_call(base, headers, "generateKeywordHistoricalMetrics",
                       {"keywords": keywords[i:i + 700], "language": lang, "geoTargetConstants": [geo],
                        "keywordPlanNetwork": "GOOGLE_SEARCH"})
        rows += [metrics_row(r["text"], r.get("keywordMetrics") or {}, "keyword_planner") for r in res.get("results", [])]
    return rows


def planner_ready():
    load_env()
    return all(os.environ.get(k) for k in ("GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CUSTOMER_ID", "GOOGLE_REFRESH_TOKEN"))


def main():
    ap = argparse.ArgumentParser(description="Free keyword research: Google Autocomplete + Keyword Planner")
    ap.add_argument("cmd", choices=["suggest", "ideas", "volume", "research", "check"])
    ap.add_argument("--seed", default="")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--url")
    ap.add_argument("--deep", action="store_true")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--out")
    args = ap.parse_args()
    cfg = load_project()
    seeds = [s.strip() for s in args.seed.split(",") if s.strip()]

    if args.cmd == "check":
        if not planner_ready():
            print("Keyword Planner: NOT configured (Autocomplete still works). See seo/engine/SETUP.md.")
            return
        rows = cmd_volume(["test"], cfg)
        print(f"Keyword Planner: OK ({len(rows)} row back for 'test')")
        return
    if args.cmd == "suggest":
        rows = cmd_suggest(seeds, cfg, args.deep)
    elif args.cmd == "ideas":
        rows = cmd_ideas(seeds, cfg, args.url, args.limit)
    elif args.cmd == "volume":
        rows = cmd_volume([k.strip() for k in args.keywords.split(",") if k.strip()], cfg)
    else:  # research
        rows = cmd_suggest(seeds, cfg, args.deep)
        if planner_ready():
            vols = {r["keyword"].lower(): r for r in cmd_volume([r["keyword"] for r in rows] + seeds, cfg)}
            rows = [{**r, **{k: v for k, v in vols.get(r["keyword"], {}).items() if k != "keyword"},
                     "source": "autocomplete+planner"} for r in rows]
            rows.sort(key=lambda r: r.get("volume") or 0, reverse=True)
        else:
            print("note: Keyword Planner not configured, so no volumes. Rank by intent + GSC impressions instead.",
                  file=sys.stderr)

    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
        print(f"saved {len(rows)} rows -> {args.out}", file=sys.stderr)
    print(json.dumps(rows, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

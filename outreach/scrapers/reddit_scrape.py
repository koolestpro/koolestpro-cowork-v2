#!/usr/bin/env python3
"""Reddit store-link scan -> Discovery tab.

People post their store link on r/shopify etc. ("roast my store", "feedback on my store", "just launched").
Those are real, live stores whose owners are actively working on them. This pulls those posts, extracts the
store domains and pushes them to Discovery (the Sheet scores them, finds emails, dedupes against Leads).

Access: tries Reddit's public .json endpoints first (no login, polite pacing, real User-Agent).
If Reddit answers 403/429 it falls back to the official app-only API when REDDIT_CLIENT_ID and
REDDIT_CLIENT_SECRET are in .env (free "script" app at reddit.com/prefs/apps). It never logs in as you.

Run:  python outreach/scrapers/reddit_scrape.py [--dry-run] [--subs shopify,ecommerce] [--limit 200]
"""
import argparse, base64, csv, json, re, sys, time, random, urllib.request, urllib.parse
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import directory_scrape as ds

SUBS = ["shopify", "shopifystore", "ecommerce", "dropshipping", "EcommerceSeller", "smallbusiness", "Entrepreneur"]
QUERIES = ["roast my store", "feedback on my store", "review my store", "just launched my store",
           "my shopify store", "store feedback", "rate my website", "critique my store", "my first store"]
# Domains that show up in posts but are never the poster's store
NOISE = {"reddit.com", "redd.it", "imgur.com", "youtube.com", "youtu.be", "i.redd.it", "v.redd.it", "docs.google.com",
         "drive.google.com", "notion.so", "medium.com", "substack.com", "x.com", "t.co", "bit.ly", "linktr.ee",
         "canva.com", "figma.com", "vercel.app", "netlify.app", "wixsite.com", "wordpress.com", "blogspot.com",
         "shopify.dev", "shopify.com", "apps.shopify.com", "etsy.com", "ebay.com", "alibaba.com", "aliexpress.com",
         "gumroad.com", "producthunt.com", "chatgpt.com", "openai.com", "ycombinator.com", "stripe.com", "paypal.com"}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
URL_RE = re.compile(r"(?:https?://)?(?:www\.)?([a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)*\.[a-z]{2,10})(?:/[^\s)\]]*)?", re.I)


def ctx():
    try:
        import certifi, ssl
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return None


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=40, context=ctx()) as r:
        return json.loads(r.read().decode())


def oauth_token(env):
    cid, sec = env.get("REDDIT_CLIENT_ID"), env.get("REDDIT_CLIENT_SECRET")
    if not cid or not sec:
        return None
    req = urllib.request.Request("https://www.reddit.com/api/v1/access_token", data=b"grant_type=client_credentials",
                                 headers={"User-Agent": "koolestpro-outreach/1.0", "Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode()})
    with urllib.request.urlopen(req, timeout=40, context=ctx()) as r:
        return json.loads(r.read().decode()).get("access_token")


def search(sub, q, token, log):
    params = urllib.parse.urlencode({"q": q, "restrict_sr": 1, "sort": "new", "t": "month", "limit": 50})
    if token:
        url, hdr = f"https://oauth.reddit.com/r/{sub}/search?{params}&raw_json=1", {"Authorization": f"bearer {token}", "User-Agent": "koolestpro-outreach/1.0"}
    else:
        url, hdr = f"https://www.reddit.com/r/{sub}/search.json?{params}&raw_json=1", None
    data = get_json(url, hdr)
    return [c["data"] for c in data.get("data", {}).get("children", [])]


def domains_in(post):
    out = []
    texts = [post.get("selftext") or "", post.get("title") or ""]
    if post.get("url_overridden_by_dest") and not post.get("is_self"):
        texts.append(post["url_overridden_by_dest"])
    for t in texts:
        for m in URL_RE.finditer(t):
            d = ds.clean(m.group(1))
            if "@" in t[max(0, m.start() - 1):m.start()]:   # part of an email address
                continue
            if d in NOISE or any(d.endswith("." + n) for n in NOISE) or not ds.is_store_domain(d):
                continue
            if d not in out:
                out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", default=",".join(SUBS))
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    log = lambda m: print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)
    env = ds.load_env()
    seen = set(ds.load_json(ds.STATE / "seen_domains.json", []))
    taken = ds.ledger_domains()
    token, mode = None, "public json"
    found, posts_seen = {}, set()
    for sub in [s.strip() for s in args.subs.split(",") if s.strip()]:
        for q in QUERIES:
            try:
                try:
                    posts = search(sub, q, token, log)
                except urllib.error.HTTPError as e:
                    if e.code in (403, 429) and not token and env.get("REDDIT_CLIENT_ID"):
                        token = oauth_token(env); mode = "official API"
                        log(f"Reddit blocked public JSON ({e.code}); switching to the official API")
                        posts = search(sub, q, token, log)
                    elif e.code in (403, 429):
                        raise SystemExit(f"Reddit returned {e.code} to the public endpoint. Create a free script app at reddit.com/prefs/apps and add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to .env, then rerun.")
                    else:
                        raise
            except SystemExit:
                raise
            except Exception as e:
                log(f"r/{sub} '{q}': {type(e).__name__} {str(e)[:100]}")
                continue
            for p in posts:
                if p["id"] in posts_seen:
                    continue
                posts_seen.add(p["id"])
                for d in domains_in(p):
                    if d in seen or d in taken or d in found:
                        continue
                    found[d] = ds.rec(d, f"reddit r/{sub}", signals=f"Posted own store on r/{sub}: {(p.get('title') or '')[:120]}",
                                      data=f"https://reddit.com{p.get('permalink','')}")
            time.sleep(random.uniform(2.0, 4.0))
        log(f"r/{sub} done, {len(found)} candidate stores so far ({mode})")
    fresh = list(found.values())[:args.limit]
    log(f"{len(posts_seen)} posts read, {len(fresh)} new store domains")
    if not fresh:
        return
    out = ds.OUT / f"{datetime.now():%Y-%m-%d_%H%M}_reddit_leads.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["domain", "source", "signals", "post"])
        for r in fresh:
            w.writerow([r["domain"], r["source"], r["signals"], r["data"]])
    log(f"saved {out.relative_to(ds.ROOT)}")
    if args.dry_run:
        log("dry run: nothing pushed")
        return
    added = merged = 0
    for i in range(0, len(fresh), 100):
        res = ds.api_call(env, "add_discovery_rows", {"rows": fresh[i:i + 100]})
        added += res.get("added", 0); merged += res.get("merged", 0)
    seen.update(r["domain"] for r in fresh)
    (ds.STATE / "seen_domains.json").write_text(json.dumps(sorted(seen)))
    log(f"pushed to the Sheet: {added} new rows in Discovery, {merged} existing rows filled in")


if __name__ == "__main__":
    main()

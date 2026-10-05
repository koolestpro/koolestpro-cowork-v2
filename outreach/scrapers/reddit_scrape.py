#!/usr/bin/env python3
"""Reddit signal scan -> Signals tab (and Discovery for stores we have not met yet).

Finds public posts where a store owner asks a question, asks for feedback on their store, or someone posts a
Shopify job. Every post is LOGGED (nothing is dropped): if the store is already a lead or in Discovery the
signal is attached to it; if not, it becomes a new Discovery row. Question / feedback / hiring posts are
marked HOT, which makes the Sheet prepare and send to that lead before everything else (within ~24h).

Modes
  default   search the subreddits below for owner posts and job posts
  --watch   also search Reddit for every lead / Discovery domain we already hold (mentions of our own list)

Access: official API if REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET are in .env (optional, Reddit now gates new apps),
else Reddit's RSS feeds (not blocked, about one request a minute, so a full run takes ~10 minutes).
It never logs in as you and never gets around a block.

Run: python outreach/scrapers/reddit_scrape.py [--dry-run] [--watch] [--subs a,b] [--limit 150]
"""
import argparse, base64, csv, html, json, re, sys, time, random, urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import directory_scrape as ds

SUBS = ["shopify", "shopifystore", "ecommerce", "dropshipping", "EcommerceSeller", "smallbusiness", "Entrepreneur", "forhire"]
QUERIES = ["roast my store", "feedback on my store", "review my store", "just launched my store", "my shopify store",
           "rate my website", "critique my store", "store not converting", "hiring shopify developer",
           "looking for shopify developer", "need a shopify developer", "shopify expert needed"]
NOISE = {"reddit.com", "redd.it", "imgur.com", "youtube.com", "youtu.be", "i.redd.it", "v.redd.it", "docs.google.com",
         "drive.google.com", "notion.so", "medium.com", "substack.com", "x.com", "t.co", "bit.ly", "linktr.ee",
         "canva.com", "figma.com", "vercel.app", "netlify.app", "wixsite.com", "wordpress.com", "blogspot.com",
         "shopify.dev", "shopify.com", "apps.shopify.com", "etsy.com", "ebay.com", "alibaba.com", "aliexpress.com",
         "gumroad.com", "producthunt.com", "chatgpt.com", "openai.com", "ycombinator.com", "stripe.com", "paypal.com",
         "upwork.com", "fiverr.com", "github.com", "gmail.com", "outlook.com", "yahoo.com"}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
URL_RE = re.compile(r"(?:https?://)?(?:www\.)?([a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)*\.[a-z]{2,10})(?:/[^\s)\]]*)?", re.I)
HIRE = re.compile(r"\[hiring\]|\bhiring\b|(looking for|need|seeking|want)\s+(a|an|some)?\s*(shopify\s+)?(developer|dev|designer|freelancer|expert|specialist)|expert needed|developer needed", re.I)
FEED = re.compile(r"roast|feedback|review my|critique|rate my|thoughts on my|what do you think|opinions? on my", re.I)
ASK = re.compile(r"\?|how (do|can|to|would)|\bhelp\b|why (is|does|are)|anyone know|advice|not (working|converting|selling)|\bissue\b|\bproblem\b", re.I)
LAUNCH = re.compile(r"just launched|launched my|my (first|new) (store|shop|site)|finally launched", re.I)


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
    ua = "koolestpro-outreach/1.0" + (f" by u/{env['REDDIT_USERNAME']}" if env.get("REDDIT_USERNAME") else "")
    req = urllib.request.Request("https://www.reddit.com/api/v1/access_token", data=b"grant_type=client_credentials",
                                 headers={"User-Agent": ua, "Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode()})
    with urllib.request.urlopen(req, timeout=40, context=ctx()) as r:
        return json.loads(r.read().decode()).get("access_token"), ua


class Reddit:
    def __init__(self, env):
        self.token, self.ua = None, UA
        got = oauth_token(env)
        if got:
            self.token, self.ua = got
        self.mode = "official API" if self.token else "public json"
        self.pw = self.browser = self.page = None

    def _browser_get(self, url):
        """Fallback with no API app: a real Chromium on your own Mac opens the same JSON a signed-out visitor sees."""
        if not self.page:
            from playwright.sync_api import sync_playwright
            self.pw = sync_playwright().start()
            self.browser = self.pw.chromium.launch(headless=True)
            self.page = self.browser.new_context(viewport={"width": 1366, "height": 900}, locale="en-GB").new_page()
            self.mode = "browser (no API app)"
        self.page.goto(url.replace("https://www.reddit.com", "https://old.reddit.com"), timeout=45000)
        txt = self.page.inner_text("body").strip()
        if not txt.startswith("{"):
            raise SystemExit("Reddit showed a block page to the browser too. Stopping (not bypassed). Log posts by hand with add_signal.py, or try again later.")
        return json.loads(txt)

    # ---- RSS: Reddit's feed-reader endpoint. Not blocked, but strictly rate limited, so one request per window. ----
    def _rss(self, url):
        for attempt in (1, 2):
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/atom+xml"})
            try:
                with urllib.request.urlopen(req, timeout=40, context=ctx()) as r:
                    body, h = r.read().decode("utf-8", "replace"), r.headers
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt == 1:
                    time.sleep(min(90, float(e.headers.get("x-ratelimit-reset") or 60)) + 2)
                    continue
                raise
            try:                                       # wait out the window so the next call is not refused
                if float(h.get("x-ratelimit-remaining", "1")) < 1:
                    time.sleep(min(90, float(h.get("x-ratelimit-reset", "60"))) + 2)
            except ValueError:
                time.sleep(62)
            return body
        return ""

    def _entries(self, xml_text, sub_hint):
        if not xml_text.strip().startswith("<"):
            return []
        ns = {"a": "http://www.w3.org/2005/Atom"}
        out = []
        for e in ET.fromstring(xml_text).findall("a:entry", ns):
            content = (e.findtext("a:content", default="", namespaces=ns) or "")
            links = " ".join(re.findall(r'href="([^"]+)"', content))
            text = html.unescape(re.sub(r"<[^>]+>", " ", content))
            link = (e.find("a:link", ns).get("href") if e.find("a:link", ns) is not None else "")
            m = re.search(r"/r/([^/]+)/comments/([a-z0-9]+)", link)
            out.append({"id": (e.findtext("a:id", default="", namespaces=ns) or "").replace("t3_", "") or (m.group(2) if m else link),
                        "title": html.unescape(e.findtext("a:title", default="", namespaces=ns) or ""),
                        "selftext": (text + " " + links).strip(),
                        "author": (e.findtext("a:author/a:name", default="", namespaces=ns) or "").replace("/u/", ""),
                        "permalink": re.sub(r"^https?://[^/]+", "", link), "subreddit": m.group(1) if m else sub_hint, "is_self": True})
        return out

    def feed(self, sub):
        """Newest ~100 posts of a subreddit. We classify them ourselves, so one request per subreddit is enough."""
        return self._entries(self._rss(f"https://www.reddit.com/r/{sub}/new/.rss?limit=100"), sub)

    def search_rss(self, q):
        return self._entries(self._rss(f"https://www.reddit.com/search.rss?{urllib.parse.urlencode({'q': q, 'sort': 'new', 't': 'year'})}"), "all")

    def close(self):
        if self.browser:
            self.browser.close(); self.pw.stop()

    def search(self, q, sub=None, t="month"):
        p = {"q": q, "sort": "new", "t": t, "limit": 50, "raw_json": 1}
        if sub:
            p["restrict_sr"] = 1
        base = "https://oauth.reddit.com" if self.token else "https://www.reddit.com"
        path = f"/r/{sub}/search" if sub else "/search"
        url = f"{base}{path}{'' if self.token else '.json'}?{urllib.parse.urlencode(p)}"
        hdr = {"User-Agent": self.ua}
        if self.token:
            hdr["Authorization"] = f"bearer {self.token}"
        try:
            data = get_json(url, hdr)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and not self.token:
                data = self._browser_get(url)
            else:
                raise
        return [c["data"] for c in data.get("data", {}).get("children", [])]


def domains_in(post):
    out = []
    texts = [post.get("selftext") or "", post.get("title") or ""]
    if post.get("url_overridden_by_dest") and not post.get("is_self"):
        texts.append(post["url_overridden_by_dest"])
    for t in texts:
        for m in URL_RE.finditer(t):
            d = ds.clean(m.group(1))
            if "@" in t[max(0, m.start() - 1):m.start()]:
                continue
            if d in NOISE or any(d.endswith("." + n) for n in NOISE) or not ds.is_store_domain(d):
                continue
            if d not in out:
                out.append(d)
    return out


def classify(post, has_store):
    text = f"{post.get('title') or ''} {post.get('selftext') or ''}"
    title = post.get("title") or ""
    if HIRE.search(title) or (post.get("subreddit", "").lower() == "forhire" and "[hiring]" in title.lower()):
        return "Hiring", True                       # a job post is hot even without a store link
    if has_store and FEED.search(title):
        return "Feedback request", True
    if has_store and (title.strip().endswith("?") or ASK.search(title)):
        return "Question", True
    if has_store and LAUNCH.search(text):
        return "Launch", False
    return ("Mention", False) if has_store else (None, False)


def signal_rows(posts, sub_hint, forced_domain=None):
    rows = []
    for p in posts:
        doms = [forced_domain] if forced_domain else domains_in(p)
        kind, hot = classify(p, bool(doms))
        if not kind:
            continue
        body = (p.get("title") or "") + " - " + (p.get("selftext") or "")[:500].replace("\n", " ")
        base = {"source": f"reddit r/{p.get('subreddit') or sub_hint}", "kind": kind, "urgency": "Hot" if hot else "Normal",
                "who": f"u/{p.get('author')}", "text": body.strip(), "url": f"https://reddit.com{p.get('permalink', '')}", "_id": p["id"]}
        for d in (doms or [""]):
            rows.append({**base, "domain": d})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", default=",".join(SUBS))
    ap.add_argument("--limit", type=int, default=150)
    ap.add_argument("--watch", action="store_true", help="also search Reddit for the domains already in the Sheet")
    ap.add_argument("--watch-max", type=int, default=15, help="without an API app Reddit allows about one request a minute, so keep this small")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    log = lambda m: print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)
    env = ds.load_env()
    done_f = ds.STATE / "reddit_posts_sent.json"
    done = set(ds.load_json(done_f, []))
    rd = Reddit(env)
    rows, seen_ids = [], set()

    def take(posts, sub, forced=None):
        for r in signal_rows(posts, sub, forced):
            k = (r["_id"], r["domain"])
            if k in seen_ids or f"{r['_id']}|{r['domain']}" in done:
                continue
            seen_ids.add(k)
            rows.append(r)

    for sub in [s.strip() for s in args.subs.split(",") if s.strip()]:
        if not rd.token:
            rd.mode = "rss feeds"
            try:
                take(rd.feed(sub), sub)
            except SystemExit:
                raise
            except Exception as e:
                log(f"r/{sub}: {type(e).__name__} {str(e)[:100]}")
            log(f"r/{sub} done: {len(rows)} signals so far ({rd.mode})")
            continue
        for q in QUERIES:
            if sub.lower() == "forhire" and "hiring" not in q and "looking" not in q and "need" not in q and "expert" not in q:
                continue
            try:
                take(rd.search(q, sub), sub)
            except SystemExit:
                raise
            except Exception as e:
                log(f"r/{sub} '{q}': {type(e).__name__} {str(e)[:100]}")
            time.sleep(random.uniform(2.0, 4.0))
        log(f"r/{sub} done: {len(rows)} signals so far ({rd.mode})")

    if args.watch:
        try:
            lead_doms = [ds.clean(l.get("website") or "") for l in ds.api_call(env, "leads", {"limit": 500}).get("leads", [])]
            disc_doms = [ds.clean(r.get("domain") or "") for r in ds.api_call(env, "discovery", {"limit": 300}).get("rows", [])]
        except Exception as e:
            lead_doms, disc_doms = [], []
            log(f"watch: could not read the Sheet ({str(e)[:100]})")
        doms = [d for d in dict.fromkeys(lead_doms + disc_doms) if d][:args.watch_max]
        log(f"watch: searching Reddit for {len(doms)} stores we already hold")
        for d in doms:
            try:
                take(rd.search(f'"{d}"', None, "year") if rd.token else rd.search_rss(f'"{d}"'), "all", forced=d)
            except SystemExit:
                raise
            except Exception as e:
                log(f"watch {d}: {type(e).__name__} {str(e)[:80]}")
            time.sleep(random.uniform(2.0, 4.0))

    rd.close()
    rows = rows[:args.limit]
    hot = sum(1 for r in rows if r["urgency"] == "Hot")
    log(f"{len(rows)} new signals ({hot} hot)")
    if not rows:
        return
    out = ds.OUT / f"{datetime.now():%Y-%m-%d_%H%M}_reddit_signals.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["domain", "kind", "urgency", "source", "who", "text", "url"])
        for r in rows:
            w.writerow([r["domain"], r["kind"], r["urgency"], r["source"], r["who"], r["text"][:200], r["url"]])
    log(f"saved {out.relative_to(ds.ROOT)}")
    if args.dry_run:
        log("dry run: nothing pushed")
        return
    res_tot = {}
    for i in range(0, len(rows), 100):
        chunk = [{k: v for k, v in r.items() if k != "_id"} for r in rows[i:i + 100]]
        res = ds.api_call(env, "add_signals", {"rows": chunk})
        for k, v in res.items():
            res_tot[k] = res_tot.get(k, 0) + v
    done.update(f"{r['_id']}|{r['domain']}" for r in rows)
    done_f.write_text(json.dumps(sorted(done)))
    log("pushed to the Sheet: " + ", ".join(f"{k}={v}" for k, v in res_tot.items()))


if __name__ == "__main__":
    main()

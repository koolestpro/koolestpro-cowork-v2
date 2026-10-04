#!/usr/bin/env python3
"""
Directory scraper: pulls new store domains from public Shopify store directories and pushes
them into the Outreach Google Sheet (Discovery tab) through the Api.gs web app.

WHY IT RUNS ON THE MAC: the cloud sandbox is blocked by these sites. A real Chromium on your own
connection, at a human pace, loads them fine (checked in your Chrome on 2026-10-04).

Sites handled (verified 2026-10-04):
  merchantgenius  /shop/date/YYYY-MM-DD, ~500 new stores a day, some with email and phone
  zik             list of new Shopify stores, renders with JavaScript (first page only)
  eachspy         country pages (top and newly added stores, ~40 domains each)
Sites NOT handled, on purpose:
  cro.media        blocks even a normal browser (Cloudflare)
  builtwith        shows a CAPTCHA. We never bypass those. Export by hand if you want it.
  techpeeker       free page shows only 10 stores
  sellerdirectories  a sales page for a paid database, not a list

What it does with each domain: skip it if seen before (state/seen_domains.json), already in the
taken-brands ledger, or is a junk host. New ones are saved to output/*.csv and pushed in batches
to Api.gs `add_domains`, which also dedupes against the Sheet. Discovery then scores each store.

Usage (from the project root, after install_mac.sh):
  python3 outreach/scrapers/directory_scrape.py                    # all sites, newest 3 days
  python3 outreach/scrapers/directory_scrape.py --sources merchantgenius --days 7
  python3 outreach/scrapers/directory_scrape.py --dry-run          # scrape, save CSV, push nothing
  python3 outreach/scrapers/directory_scrape.py --headed           # watch the browser
Needs OUTREACH_API_URL and OUTREACH_API_TOKEN in .env (same values KoolestFlow uses).
"""
import argparse, csv, json, os, random, re, sys, time, urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STATE = HERE / "state"
OUT = HERE / "output"
STATE.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

CURRENCY_COUNTRY = {"GBP": "United Kingdom", "USD": "United States", "CAD": "Canada", "AUD": "Australia",
                    "NZD": "New Zealand", "EUR": "Europe", "NGN": "Nigeria", "ZAR": "South Africa",
                    "KES": "Kenya", "GHS": "Ghana", "SEK": "Sweden", "DKK": "Denmark", "NOK": "Norway"}
EACHSPY_COUNTRIES = {"united-states": "United States", "united-kingdom": "United Kingdom", "canada": "Canada",
                     "australia": "Australia", "south-africa": "South Africa", "new-zealand": "New Zealand",
                     "germany": "Germany", "france": "France", "netherlands": "Netherlands", "sweden": "Sweden"}
SKIP_LABELS = {"facebook", "instagram", "twitter", "linkedin", "youtube", "tiktok", "pinterest", "google", "shopify",
               "myshopify", "cloudflare", "amazon", "apple", "github", "wikipedia", "trustpilot", "calendly",
               "merchantgenius", "zikanalytics", "eachspy", "techpeeker", "builtwith", "bootleads", "gstatic"}
DOMAIN_RE = re.compile(r"\b[a-z0-9][a-z0-9-]{0,61}(?:\.[a-z0-9][a-z0-9-]{0,61})*\.[a-z]{2,10}\b", re.I)
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)


def load_env():
    env = dict(os.environ)
    for p in (ROOT / ".env", ROOT / "cold-email-app" / ".env"):
        if p.exists():
            for line in p.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def clean(d):
    d = (d or "").strip().lower()
    d = re.sub(r"^https?://", "", d).split("/")[0].split("?")[0]
    return d[4:] if d.startswith("www.") else d


def is_store_domain(d):
    if not DOMAIN_RE.fullmatch(d or ""):
        return False
    if re.search(r"\.(png|jpe?g|gif|svg|webp|json|xml|pdf|css|js|ico)$", d):
        return False
    return not any(l in SKIP_LABELS for l in d.split("."))


def load_json(p, default):
    try:
        return json.loads(p.read_text())
    except Exception:
        return default


def ledger_domains():
    data = load_json(ROOT / ".ai-workflow" / "taken-brands-ledger.json", {})
    out = set()
    for b in (data.get("brands") or {}).values():
        h = clean(urlparse(b.get("websiteUrl") or "").netloc)
        if h:
            out.add(h)
    return out


def pause(a=1.5, b=3.5):
    time.sleep(random.uniform(a, b))


# ---------------------------------------------------------------- extractors
def scrape_merchantgenius(page, days, log):
    """Newest N dated pages. The home page links /shop/date/YYYY-MM-DD; each date page lists every store
    that launched that day as /shop/url/<domain> links, with email and phone in the card text when public."""
    page.goto("https://www.merchantgenius.io/", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2500)
    hrefs = page.eval_on_selector_all("a[href*='/shop/date/']", "els => els.map(e => e.getAttribute('href'))")
    dates = sorted({m.group(1) for h in hrefs for m in [re.search(r"/shop/date/(\d{4}-\d{2}-\d{2})", h or "")] if m},
                   reverse=True)
    if not dates:
        log("merchantgenius: no date links found on the home page (layout changed?)")
        return []
    done = set(load_json(STATE / "merchantgenius_dates.json", []))
    todo = [d for d in dates if d not in done][:days]
    log(f"merchantgenius: newest date listed {dates[0]}; scraping {todo or 'nothing new'}")
    rows = []
    for d in todo:
        page.goto(f"https://www.merchantgenius.io/shop/date/{d}", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        text = page.inner_text("body")
        domains = page.eval_on_selector_all(
            "a[href*='/shop/url/']",
            "els => [...new Set(els.map(e => e.getAttribute('href').split('/shop/url/')[1]))]")
        # card text looks like: NAME\nDOMAIN\n\ndesc\n\n (GBP / ENGLISH)\nEMAIL PHONE
        blocks = {}
        upper = text.upper()
        positions = []
        for dom in domains:
            i = upper.find(dom.upper())
            if i >= 0:
                positions.append((i, dom))
        positions.sort()
        for n, (i, dom) in enumerate(positions):
            j = positions[n + 1][0] if n + 1 < len(positions) else len(text)
            blocks[dom] = text[i:j]
        for dom in domains:
            blk = blocks.get(dom, "")
            cur = re.search(r"\(([A-Z]{3})\s*/", blk)
            em = EMAIL_RE.search(blk)
            ph = re.search(r"\+?\d[\d\s().-]{8,}\d", blk)
            rows.append({"domain": clean(dom), "source": f"merchantgenius {d}",
                         "country": CURRENCY_COUNTRY.get(cur.group(1), "") if cur else "",
                         "email": em.group(0).lower() if em else "", "phone": ph.group(0).strip() if ph else ""})
        log(f"merchantgenius {d}: {len(domains)} stores")
        done.add(d)
        (STATE / "merchantgenius_dates.json").write_text(json.dumps(sorted(done)))
        pause()
    return rows


def scrape_zik(page, days, log):
    page.goto("https://www.zikanalytics.com/store-list/list-of-new-shopify-stores", wait_until="domcontentloaded",
              timeout=60000)
    try:
        page.wait_for_selector("tr td", timeout=20000)
    except Exception:
        log("zik: table never rendered (login wall or layout changed)")
        return []
    page.wait_for_timeout(2000)
    cells = page.eval_on_selector_all("tr td:first-child", "els => els.map(e => e.innerText)")
    rows = []
    for c in cells:
        m = DOMAIN_RE.search(c.split("\n")[-1] if "\n" in c else c)
        if m and is_store_domain(clean(m.group(0))):
            rows.append({"domain": clean(m.group(0)), "source": "zik new stores", "country": "", "email": "", "phone": ""})
    log(f"zik: {len(rows)} stores (first page only; note its 'new' stores can be a year or two old)")
    return rows


def scrape_eachspy(page, days, log):
    rows = []
    for slug, country in EACHSPY_COUNTRIES.items():
        try:
            page.goto(f"https://www.eachspy.com/shopify/stores-in-{slug}/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)
        except Exception as e:
            log(f"eachspy {slug}: {e}")
            continue
        cells = page.eval_on_selector_all("tr td:first-child, tr th:first-child", "els => els.map(e => e.innerText)")
        n = 0
        for c in cells:
            for m in DOMAIN_RE.finditer(c):
                d = clean(m.group(0))
                if is_store_domain(d):
                    rows.append({"domain": d, "source": f"eachspy {slug}", "country": country, "email": "", "phone": ""})
                    n += 1
        log(f"eachspy {slug}: {n} domains")
        pause()
    return rows


SOURCES = {"merchantgenius": scrape_merchantgenius, "zik": scrape_zik, "eachspy": scrape_eachspy}


# ---------------------------------------------------------------- push to the Sheet
def api_call(env, action, args):
    url, token = env.get("OUTREACH_API_URL", ""), env.get("OUTREACH_API_TOKEN", "")
    if not url or not token:
        raise SystemExit("OUTREACH_API_URL / OUTREACH_API_TOKEN missing from .env")
    body = json.dumps({"token": token, "action": action, "args": args}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:   # Apps Script answers with a redirect; urllib follows it
        out = json.loads(r.read().decode())
    if not out.get("ok"):
        raise RuntimeError(out.get("error", "unknown API error"))
    return out["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=",".join(SOURCES))
    ap.add_argument("--days", type=int, default=3, help="merchantgenius: how many new dates to read per run")
    ap.add_argument("--limit", type=int, default=600, help="max new domains pushed per run")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    def log(msg):
        print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright missing. Run outreach/scrapers/install_mac.sh first.")

    env = load_env()
    seen = set(load_json(STATE / "seen_domains.json", []))
    taken = ledger_domains()
    found = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        ctx = browser.new_context(viewport={"width": 1366, "height": 900}, locale="en-GB")
        page = ctx.new_page()
        for name in [s.strip() for s in args.sources.split(",") if s.strip()]:
            fn = SOURCES.get(name)
            if not fn:
                log(f"unknown source {name}")
                continue
            try:
                got = fn(page, args.days, log)
                if page.title().lower().startswith(("attention required", "just a moment")):
                    log(f"{name}: blocked by Cloudflare. Skipping.")
                found += got
            except Exception as e:
                log(f"{name}: FAILED {type(e).__name__}: {str(e)[:160]}")
        browser.close()

    fresh, keys = [], set()
    for r in found:
        d = r["domain"]
        if not is_store_domain(d) or d in seen or d in taken or d in keys:
            continue
        keys.add(d)
        fresh.append(r)
    fresh = fresh[: args.limit]
    log(f"scraped {len(found)} rows, {len(fresh)} new after dedupe")
    if not fresh:
        return

    out = OUT / f"{datetime.now():%Y-%m-%d_%H%M}_directory_leads.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain", "source", "country", "email", "phone"])
        w.writeheader()
        w.writerows(fresh)
    log(f"saved {out.relative_to(ROOT)}")
    if args.dry_run:
        log("dry run: nothing pushed")
        return

    added = 0
    groups = {}
    for r in fresh:
        groups.setdefault((r["source"].split()[0], r["country"]), []).append(r["domain"])
    for (src, country), doms in groups.items():
        for i in range(0, len(doms), 100):
            res = api_call(env, "add_domains", {"domains": doms[i:i + 100], "source": src, "country": country})
            added += res.get("added", 0)
            pause(0.5, 1.5)
    seen.update(r["domain"] for r in fresh)
    (STATE / "seen_domains.json").write_text(json.dumps(sorted(seen)))
    log(f"pushed to the Sheet: {added} new domains added to Discovery (rest were already there)")


if __name__ == "__main__":
    main()

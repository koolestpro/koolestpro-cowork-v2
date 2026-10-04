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
  myipms          Shopify IP-owner page on myip.ms (sorted by world rank, so mostly big brands; those are dropped)
Sites NOT handled, on purpose:
  cro.media        blocks even a normal browser (Cloudflare)
  builtwith        shows a CAPTCHA. We never bypass those. Export by hand if you want it.
  techpeeker       free page shows only 10 stores
  sellerdirectories  a sales page for a paid database, not a list

What it keeps per store: domain, store name, country/currency/language, EVERY email and phone shown,
description and any size or theme signals. It skips a domain if seen before (state/seen_domains.json), already
in the taken-brands ledger, or a junk host. New rows are saved to output/*.csv and pushed in batches to Api.gs
`add_discovery_rows`, which dedupes against the Sheet and fills empty fields of rows already there.
Discovery then scores each store; when it promotes one it keeps the BEST email (decision maker first).

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
def rec(domain, source, **kw):
    r = {"domain": clean(domain), "source": source, "brand": "", "country": "", "niche": "", "contact_name": "",
         "emails": [], "phone": "", "signals": "", "data": ""}
    r.update(kw)
    return r


def scrape_merchantgenius(page, days, log):
    """Newest N dated pages. The home page links /shop/date/YYYY-MM-DD; each date page lists every store that
    launched that day as /shop/url/<domain> links. Card text: NAME, DOMAIN, description, (CUR / LANG), EMAIL PHONE."""
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
        upper, pos = text.upper(), []
        for dom in domains:
            i = upper.find(dom.upper())
            if i >= 0:
                pos.append((i, dom))
        pos.sort()
        for n, (i, dom) in enumerate(pos):
            j = pos[n + 1][0] if n + 1 < len(pos) else len(text)
            lines = [l.strip() for l in text[i:j].split("\n") if l.strip()]
            if n + 1 < len(pos) and len(lines) > 1:
                lines = lines[:-1]                      # last line of a block is the NEXT store's name
            name = ""
            before = [l.strip() for l in text[:i].split("\n") if l.strip()]
            if before:
                name = before[-1]
            blk = "\n".join(lines)
            cur = re.search(r"\(([A-Z]{3})\s*/\s*([A-Z ]+)\)", blk)
            emails = sorted({e.lower() for e in EMAIL_RE.findall(blk)})
            ph = re.search(r"(?<![\w@.])\+?\d[\d\s().-]{8,}\d", blk)
            desc = lines[1] if len(lines) > 1 and "No description" not in lines[1] else ""
            rows.append(rec(dom, f"merchantgenius {d}", brand=name.title() if name.isupper() else name,
                            country=CURRENCY_COUNTRY.get(cur.group(1), "") if cur else "",
                            emails=emails, phone=ph.group(0).strip() if ph else "",
                            signals=f"launched {d}" + (f"; {cur.group(1)}/{cur.group(2).strip().title()}" if cur else ""),
                            data=desc[:400]))
        log(f"merchantgenius {d}: {len(domains)} stores, {sum(1 for r in rows if r['emails'] and r['source'].endswith(d))} with email")
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
    table = page.eval_on_selector_all(
        "tr", "els => els.map(r => [...r.querySelectorAll('td')].map(c => c.innerText.trim()))")
    rows = []
    for cells in table:
        if not cells:
            continue
        first = cells[0].split("\n")
        m = DOMAIN_RE.search(first[-1])
        if not (m and is_store_domain(clean(m.group(0)))):
            continue
        theme = cells[1] if len(cells) > 1 else ""
        launched = cells[2] if len(cells) > 2 else ""
        rev = next((c for c in reversed(cells) if c.startswith("$")), "")
        sig = "; ".join(x for x in [f"theme {theme}" if theme else "", f"launched {launched}" if launched else "",
                                     f"Zik est. revenue {rev}" if rev else ""] if x)
        rows.append(rec(m.group(0), "zik new stores", brand=first[0] if len(first) > 1 else "", signals=sig))
    log(f"zik: {len(rows)} stores (first page only; its 'new' stores can be a year or two old)")
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
        table = page.eval_on_selector_all(
            "tr", "els => els.map(r => [...r.querySelectorAll('td,th')].map(c => c.innerText.trim()))")
        n = 0
        for cells in table:
            if not cells:
                continue
            first = cells[0].split("\n")
            m = DOMAIN_RE.search(cells[0])
            if not (m and is_store_domain(clean(m.group(0)))):
                continue
            rest = " | ".join(c.replace("\n", " ") for c in cells[1:] if c)[:300]
            rows.append(rec(m.group(0), f"eachspy {slug}", brand=first[0] if len(first) > 1 else "", country=country,
                            signals="EachSpy list row", data=rest))
            n += 1
        log(f"eachspy {slug}: {n} stores")
        pause()
    return rows


def scrape_myipms(page, days, log):
    """Shopify, Inc IP-owner page. Sorted by world popularity, so page 1 is huge brands (pch.com, barnesandnoble.com).
    Rows with a world rank under MIN_RANK are dropped: they are not small-store leads."""
    MIN_RANK = 300000
    rows, url = [], "https://myip.ms/view/ip_owners/376714/Shopify_Inc.html"
    for pg in range(max(1, days)):
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        if re.search(r"captcha|verify you are human|robot", page.inner_text("body")[:2000], re.I):
            log("myipms: CAPTCHA shown. Stopping (not bypassed).")
            break
        table = page.eval_on_selector_all(
            "table tr", "els => els.map(r => [...r.querySelectorAll('td')].map(c => c.innerText.trim()))")
        n = 0
        for cells in table:
            joined = " ".join(cells)
            m = DOMAIN_RE.search(cells[1]) if len(cells) > 1 else None
            if not m or "Shopify" not in joined:
                continue
            rk = re.search(r"#\s*([\d,]+)", joined)
            rank = int(rk.group(1).replace(",", "")) if rk else None
            if rank is not None and rank < MIN_RANK:
                continue
            if is_store_domain(clean(m.group(0))):
                rows.append(rec(m.group(0), "myip.ms shopify ips", signals=f"world rank {rank}" if rank else "",
                                data=f"IP {cells[2]}" if len(cells) > 2 else ""))
                n += 1
        log(f"myipms page {pg + 1}: {n} small-enough stores kept")
        nxt = page.query_selector("a:has-text('Next'), a:has-text('›'), a.next")
        href = nxt.get_attribute("href") if nxt else None
        if not href:
            break
        url = href if href.startswith("http") else "https://myip.ms" + href
        pause(3, 6)
    return rows


SOURCES = {"merchantgenius": scrape_merchantgenius, "zik": scrape_zik, "eachspy": scrape_eachspy,
           "myipms": scrape_myipms}


# ---------------------------------------------------------------- push to the Sheet
def api_call(env, action, args):
    url, token = env.get("OUTREACH_API_URL", ""), env.get("OUTREACH_API_TOKEN", "")
    if not url or not token:
        raise SystemExit("OUTREACH_API_URL / OUTREACH_API_TOKEN missing from .env")
    body = json.dumps({"token": token, "action": action, "args": args}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        import certifi, ssl
        ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ctx = None
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:   # Apps Script answers with a redirect; urllib follows it
        out = json.loads(r.read().decode())
    if not out.get("ok"):
        raise RuntimeError(out.get("error", "unknown API error"))
    return out["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=",".join(SOURCES))
    ap.add_argument("--days", type=int, default=3, help="merchantgenius: new dates per run; myipms: pages per run")
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

    fresh, keys = [], {}
    for r in found:
        d = r["domain"]
        if not is_store_domain(d) or d in seen or d in taken:
            continue
        if d in keys:                                   # same store from two sources: merge what each knows
            k = keys[d]
            k["emails"] = sorted(set(k["emails"]) | set(r["emails"]))
            for f in ("brand", "country", "phone", "signals", "data"):
                if r[f] and not k[f]:
                    k[f] = r[f]
            continue
        keys[d] = r
        fresh.append(r)
    fresh = fresh[: args.limit]
    with_email = sum(1 for r in fresh if r["emails"])
    log(f"scraped {len(found)} rows, {len(fresh)} new after dedupe ({with_email} with an email)")
    if not fresh:
        return

    out = OUT / f"{datetime.now():%Y-%m-%d_%H%M}_directory_leads.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain", "source", "brand", "country", "emails", "phone", "signals", "data"])
        w.writeheader()
        for r in fresh:
            w.writerow({**{k: r[k] for k in ("domain", "source", "brand", "country", "phone", "signals", "data")},
                        "emails": " | ".join(r["emails"])})
    log(f"saved {out.relative_to(ROOT)}")
    if args.dry_run:
        log("dry run: nothing pushed")
        return

    added = merged = 0
    for i in range(0, len(fresh), 100):
        res = api_call(env, "add_discovery_rows", {"rows": fresh[i:i + 100]})
        added += res.get("added", 0)
        merged += res.get("merged", 0)
        pause(0.5, 1.5)
    seen.update(r["domain"] for r in fresh)
    (STATE / "seen_domains.json").write_text(json.dumps(sorted(seen)))
    log(f"pushed to the Sheet: {added} new rows in Discovery, {merged} existing rows filled in")


if __name__ == "__main__":
    main()

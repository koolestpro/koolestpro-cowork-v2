#!/usr/bin/env python3
"""Quora signal scan (best effort). Quora hides most search behind a login and blocks bots, so this reads only
what a logged-out Playwright browser can see and STOPS the moment it hits a login wall or a CAPTCHA (never bypassed).
Anything it cannot reach, log by hand with add_signal.py.

Run: python outreach/scrapers/quora_scrape.py [--dry-run] [--headed]
"""
import argparse, sys, time, random, urllib.parse
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import directory_scrape as ds
import reddit_scrape as rs

QUERIES = ["shopify store feedback", "why is my shopify store not converting", "shopify developer recommendation", "roast my online store"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()
    log = lambda m: print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)
    from playwright.sync_api import sync_playwright
    env, rows = ds.load_env(), []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=not args.headed)
        page = b.new_context(viewport={"width": 1366, "height": 900}, locale="en-GB").new_page()
        for q in QUERIES:
            page.goto("https://www.quora.com/search?" + urllib.parse.urlencode({"q": q, "type": "question", "time": "month"}), timeout=45000)
            time.sleep(3)
            body = page.inner_text("body")[:3000].lower()
            if any(w in body for w in ("verify you are human", "just a moment", "captcha")) or ("continue with google" in body and "question" not in body):
                log("Quora is showing a login wall or CAPTCHA. Stopping (not bypassed). Use add_signal.py for Quora posts you find.")
                break
            for a in page.query_selector_all("a[href*='quora.com/']")[:60]:
                title, href = (a.inner_text() or "").strip(), a.get_attribute("href") or ""
                if len(title) < 25 or "/profile/" in href or "/topic/" in href:
                    continue
                post = {"title": title, "selftext": "", "subreddit": "quora"}
                doms = rs.domains_in(post)
                if doms and (rs.FEED.search(title) or rs.ASK.search(title)):
                    for d in doms:
                        rows.append({"domain": d, "kind": "Question", "urgency": "Hot", "source": "quora", "who": "", "text": title, "url": href})
            time.sleep(random.uniform(3, 6))
        b.close()
    log(f"{len(rows)} Quora signals")
    if rows and not args.dry_run:
        print(ds.api_call(env, "add_signals", {"rows": rows}))


if __name__ == "__main__":
    main()

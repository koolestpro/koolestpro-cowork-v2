#!/usr/bin/env python3
"""
outscraper_koolestflow_bridge.py — Outscraper Google Maps → KoolestFlow lead pipeline.

Replaces the BrowserAct Google Maps discovery workflow with Outscraper's direct
Maps Search API. Free for the first 500 businesses per month, then $3/1K.
At Ridwan's actual volume (~120 leads/month), this costs $0.

Outscraper returns business data in a single API call — no polling, no workflow
management, no per-run wait. Results include name, address, phone, website,
rating, reviews, and category directly from the Google Maps listing.

  Stage 1 — Discovery: Outscraper Maps Search API (query = keyword + city)
  Stage 2 — Enrichment: built into the same Outscraper response (website,
            phone, hours, photos). Optional: run Hunter/Outscraper Contacts
            for email discovery if a real website exists.
  Stage 3 — Score + classify using lead_playbook.py (same as BrowserAct route)
  Stage 4 — Push into KoolestFlow via koolestflow_client.py

Setup:
  Sign up at https://outscraper.com, copy your API key from the dashboard,
  add to .env: OUTSCRAPER_API_KEY=your_key

Usage:
  # Full discovery + push to Vercel production:
  python3 outscraper_koolestflow_bridge.py --query "fashion boutique Lagos" --limit 20 \
    --niche "Fashion & Apparel" --country Nigeria --city Lagos --audience-type "E-commerce/DTC"

  # Push to local KoolestFlow instead:
  python3 outscraper_koolestflow_bridge.py --query "skincare shop Lekki" --limit 10 --local

  # Dry run (prints prospects, no API push):
  python3 outscraper_koolestflow_bridge.py --query "hair salon Abuja" --limit 5 --dry-run

  # Skip website-quality check (faster, no HTTP fetches):
  python3 outscraper_koolestflow_bridge.py --query "restaurant Ikeja" --limit 10 --skip-quality-check
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koolestflow_client as kc
import lead_playbook as lp

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUTSCRAPER_BASE = "https://api.app.outscraper.com"


def env(name, default=None):
    val = os.environ.get(name)
    if val:
        return val
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{name}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return default


# ---------- Stage 1: Discovery ----------

def outscraper_maps_search(api_key, query, limit):
    """Call Outscraper Maps Search v3. Returns list of business dicts."""
    encoded_query = urllib.parse.quote(query)
    url = f"{OUTSCRAPER_BASE}/maps/search-v3?query={encoded_query}&limit={limit}&async=false"
    req = urllib.request.Request(url, headers={"X-API-KEY": api_key})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("ERROR: Invalid Outscraper API key. Get your key from https://outscraper.com/profile", file=sys.stderr)
        else:
            print(f"ERROR: Outscraper API returned {e.code}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"ERROR: Outscraper request failed: {e}", file=sys.stderr)
        return []

    # Outscraper returns data inside a "data" key or directly as a list
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("data") or data.get("results") or []
    return []


# ---------- Stage 2: Transform Outscraper row → enrichment dict ----------

def transform_outscraper_row(row):
    """Normalize an Outscraper business row into the same enrichment shape
    the BrowserAct bridge uses, so Stage 3+ can be shared."""
    # Outscraper field names (confirmed from live API docs):
    # name, full_address, site, phone, type, rating, reviews, latitude, longitude, etc.
    name = (row.get("name") or "").strip()
    address = (row.get("full_address") or row.get("address") or "").strip()
    website = (row.get("site") or row.get("website") or "").strip()
    phone = (row.get("phone") or "").strip()
    rating_raw = str(row.get("rating") or row.get("rating_average") or "").strip()
    reviews_raw = str(row.get("reviews") or row.get("reviews_count") or "").strip()
    category = (row.get("type") or row.get("category") or "").strip()

    # Clean rating (Outscraper returns "4.5" or "4.5/5")
    try:
        rating = float(rating_raw.split("/")[0]) if rating_raw else 0.0
    except ValueError:
        rating = 0.0

    # Clean reviews
    try:
        reviews = int(float(reviews_raw)) if reviews_raw else 0
    except ValueError:
        reviews = 0

    return {
        "name": name,
        "full_address": address,
        "website_url": website,
        "phone": phone,
        "star_rating": str(rating) if rating else "",
        "review_count": str(reviews) if reviews else "",
        "category": category,
    }


# ---------- Stage 3: Score + classify (mirrors BrowserAct route exactly) ----------

def score_and_qualify(row, website_quality=None):
    name = (row.get("name") or "").strip()
    rating_raw = (row.get("star_rating") or "").strip()
    review_count_raw = (row.get("review_count") or "").strip()
    try:
        rating = float(rating_raw.split("/")[0]) if rating_raw else 0.0
    except ValueError:
        rating = 0.0
    reviews = int(review_count_raw) if review_count_raw.isdigit() else 0

    has_website = bool(row.get("website_url"))
    has_phone = bool(row.get("phone"))
    has_real_presence = reviews >= 5 or rating >= 4.0 or has_phone

    signals = []
    score = 30  # baseline: exists on Maps
    if reviews > 0:
        signals.append(f"{reviews} Google reviews")
        score += min(reviews, 40)
    if rating >= 4.5:
        signals.append(f"{rating}/5.0 rating")
        score += 10
    elif rating >= 4.0:
        signals.append(f"{rating}/5.0 rating")
        score += 5
    if has_phone:
        signals.append("Phone listed")
        score += 5

    # Website quality scoring
    quality_score = website_quality["score"] if website_quality else None
    if has_website:
        if quality_score is not None:
            signals.append(f"Has website (quality {quality_score}/100)")
            if quality_score < 55:
                score += 5  # weak site still = some signal
            else:
                score += 10
        else:
            signals.append(f"Has website: {row['website_url']}")
            score += 10
    else:
        signals.append("No website found")
        if has_real_presence:
            score += 20  # Ridwan's rule: real presence + no site = best Build candidate

    score = max(0, min(score, 100))
    return {
        "signals": "; ".join(signals),
        "fit_score": score,
        "confidence": "high" if score >= 80 else "medium" if score >= 60 else "low",
        "status": "Qualified" if score >= 60 else "Needs Review",
        "pipeline_stage": "First Message Ready" if score >= 60 else "New",
        "next_action": "Send first DM" if (not has_website and has_phone) else "Review contact channel",
    }


def build_prospect(row, niche, country, city, audience_type, source_query, skip_quality=False):
    scored = score_and_qualify(row)
    name = (row.get("name") or "").strip()

    # Track classification
    has_website = bool(row.get("website_url"))
    has_phone = bool(row.get("phone"))
    rating_raw = (row.get("star_rating") or "").strip()
    review_count_raw = (row.get("review_count") or "").strip()
    try:
        rating = float(rating_raw.split("/")[0]) if rating_raw else 0.0
    except ValueError:
        rating = 0.0
    reviews = int(review_count_raw) if review_count_raw.isdigit() else 0
    has_real_presence = reviews >= 5 or rating >= 4.0 or has_phone

    quality = None
    if has_website and not skip_quality:
        print(f"  checking site quality for {row['website_url']}...", file=sys.stderr)
        quality = lp.assess_website_quality(row["website_url"])

    track = lp.classify_track(has_website, has_real_presence, quality["score"] if quality else None)
    pitch_notes = lp.build_pitch_notes(track, niche, country)

    notes_parts = []
    address = (row.get("full_address") or "").strip()
    if address:
        notes_parts.append(f"Address: {address}")
    if row.get("phone"):
        notes_parts.append(f"Phone: {row['phone']}")
    notes_parts.append(pitch_notes)
    if quality:
        notes_parts.append(f"Site quality score: {quality['score']}/100 ({'; '.join(quality['signals'])})")
    notes_parts.append(f"Category: {row.get('category', 'N/A')}")
    notes_parts.append("Sourced via Outscraper Google Maps. Review before outreach.")

    return {
        "id": f"koolestflow-outscraper-{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:50]}",
        "brand_name": name,
        "website_url": row.get("website_url", ""),
        "instagram_url": "",
        "email": "",
        "whatsapp": "",
        "country": country,
        "city": city,
        "timezone": "",
        "niche": niche,
        "audience_type": audience_type,
        "source": "outscraper",
        "source_query": source_query,
        "source_url": "",
        "notes": " | ".join(notes_parts),
        **scored,
        "track": track,
        "has_website": "Yes" if has_website else "No",
        "ads_running": "unknown",
    }


# ---------- Stage 4: Push ----------

def push_to_koolestflow(base_url, password, new_prospects, dry_run=False):
    return kc.push_to_koolestflow(base_url, password, new_prospects, dry_run=dry_run)


# ---------- CLI ----------

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--query", required=True, help="Search query, e.g. 'fashion boutique Lagos Nigeria'")
    p.add_argument("--limit", type=int, default=20, help="Max businesses to fetch (default 20)")
    p.add_argument("--niche", default="")
    p.add_argument("--country", default="")
    p.add_argument("--city", default="")
    p.add_argument("--audience-type", default="")
    p.add_argument("--dry-run", action="store_true", help="Print prospects, skip KoolestFlow push")
    p.add_argument("--local", action="store_true", help="Push to local KoolestFlow (http://127.0.0.1:8787)")
    p.add_argument("--skip-quality-check", action="store_true", help="Skip website quality assessment (faster)")
    args = p.parse_args()

    api_key = env("OUTSCRAPER_API_KEY")
    if not api_key:
        print("OUTSCRAPER_API_KEY not set. Get a free key at https://outscraper.com", file=sys.stderr)
        sys.exit(1)

    if args.local:
        kf_base = env("KOOLESTFLOW_LOCAL_BASE_URL", "http://127.0.0.1:8787")
    else:
        kf_base = env("KOOLESTFLOW_BASE_URL", "https://cold-dm-app.vercel.app")
    kf_password = env("KOOLESTFLOW_APP_PASSWORD")

    print(f"Stage 1: querying Outscraper for '{args.query}' (limit {args.limit})...", file=sys.stderr)
    raw_results = outscraper_maps_search(api_key, args.query, args.limit)
    if not raw_results:
        print("No businesses found. Nothing to do.", file=sys.stderr)
        return

    print(f"Stage 1 complete: {len(raw_results)} businesses found.", file=sys.stderr)

    prospects = []
    for raw in raw_results:
        row = transform_outscraper_row(raw)
        name = row.get("name", "").strip()
        if not name:
            continue
        prospects.append(build_prospect(
            row, args.niche, args.country, args.city, args.audience_type,
            f"Query={args.query}", skip_quality=args.skip_quality_check,
        ))

    print(f"Stage 3 complete: {len(prospects)} prospects scored.", file=sys.stderr)

    if not kf_password and not args.dry_run:
        print("KOOLESTFLOW_APP_PASSWORD not set in .env — forcing --dry-run.", file=sys.stderr)
        args.dry_run = True

    if args.dry_run:
        print("\n--- DRY RUN: prospects that would be pushed ---")
        print(json.dumps(prospects, indent=2, ensure_ascii=False))
        print(f"\n[dry run] {len(prospects)} prospect(s) would be pushed. No API call made.")
        return

    push_to_koolestflow(kf_base, kf_password, prospects, dry_run=False)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
browseract_koolestflow_bridge.py — universal BrowserAct -> KoolestFlow lead pipeline.

Not tied to Nigeria, not tied to Koolestpro's own targets_pool.json. Two
BrowserAct workflows chained together, then pushed straight into KoolestFlow
(the cold-dm-app, https://cold-dm-app.vercel.app) via its live API — no manual
Notion copy-paste step.

  Stage 1 — Discovery (Google Maps Scraper, workflow_id in .env's
            BROWSERACT_LEADGEN_WORKFLOW_ID): Area + Keyword + datalimit ->
            businesses with name/address/rating/reviews. Area and Keyword are
            free text, so this works for any city/niche worldwide, not just
            Lagos/skincare.

  Stage 2 — Enrichment (Google Business Contact Finder, workflow_id in
            .env's BROWSERACT_ENRICH_WORKFLOW_ID): business name -> official
            website + every social profile found (Instagram, Facebook,
            LinkedIn, TikTok, X, YouTube) + any phone/email on the page.

  Stage 3 — Qualify + score, matching KoolestFlow's OWN scoring convention
            exactly (read from backend/lead_engine.py, not guessed):
              fit_score      0-100 int
              confidence     "high" (>=80) / "medium" (>=60) / "low"
              status         "Qualified" (>=60) else "Needs Review"
              pipeline_stage "First Message Ready" (>=60) else "New"
              next_action    "Send first DM" if instagram_url else
                              "Review contact channel"

            Ridwan's qualification rule (2026-08-11): "has real presence but
            weak execution" is the free-template-giveaway signal. Real
            presence = has reviews (Maps) or an active social profile.
            Weak execution = no real website found even after Stage 2
            looked specifically for one. That combination scores HIGHEST
            here on purpose — it's the ideal candidate for the free-rebrand-
            template motion, not a dead end.

  Stage 3.5 — Track + pitch (added 2026-08-19, see lead_playbook.py):
            every lead gets tagged Build (no site) / Fix (has a site, but
            an automated quality check flags it weak) / Scale (has a site
            and it checks out reasonably well — pursued for SEO/ads/
            management, NOT skipped) / Low Priority (no site, no real
            presence signal either). Recommended services + region-aware
            channel/pricing framing get written into the KoolestFlow
            `notes` field so the track is visible without re-deriving it.

  Stage 4 — Push into KoolestFlow via its live API:
            POST /api/auth/login (password) -> session cookie
            GET  /api/state                 -> existing prospects
            dedupe on normalized brand_name + city
            POST /api/state                 -> full merged prospect list
            (save_state() in KoolestFlow's own backend REPLACES the whole
            prospects table with whatever list is posted, so this always
            fetches current state first and posts existing + new combined
            — never just the new batch alone.)

Setup (one-time):
  .env needs (already set as of 2026-08-11):
    BROWSERACT_API_KEY
    BROWSERACT_LEADGEN_WORKFLOW_ID   (Google Maps Scraper, this project's own clone)
    BROWSERACT_ENRICH_WORKFLOW_ID    (Google Business Contact Finder, this project's own clone)
    KOOLESTFLOW_APP_PASSWORD         (the Vercel app's shared password)
    KOOLESTFLOW_BASE_URL             (default https://cold-dm-app.vercel.app if unset)

Usage:
  # Full discovery + enrichment + push, any niche/city worldwide:
  python3 browseract_koolestflow_bridge.py \\
    --area "Lekki, Lagos" --keyword "fashion boutique" --limit 10 \\
    --niche "Fashion & Apparel" --country Nigeria --city Lagos --audience-type "E-commerce/DTC"

  # Dry run (prints what would be pushed, doesn't touch KoolestFlow or spend enrichment credits beyond discovery):
  python3 browseract_koolestflow_bridge.py --area Lagos --keyword "skincare shop" --limit 5 --dry-run

  # Skip discovery, enrich + push leads already sitting in dm_leads_pool.json:
  python3 browseract_koolestflow_bridge.py --from-dm-leads-pool --niche "Beauty & Skincare" --country Nigeria --city Lagos

Credits: Stage 1 is ~11 credits/business (55 credits / 5 in the first test
run). Stage 2 is ~35 credits/business. Budget roughly 46 credits
(~$0.15) per lead end to end — get the --limit right before running large batches.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import browseract_client as bc
import koolestflow_client as kc
import lead_playbook as lp

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DM_LEADS_POOL_PATH = os.path.join(PROJECT_ROOT, "dm_leads_pool.json")


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

def run_maps_discovery(api_key, workflow_id, area, keyword, limit):
    result = bc.run_task(api_key, workflow_id, {
        "URL": "https://www.google.com/maps", "Area": area, "Keyword": keyword, "datalimit": str(limit),
    })
    task_id = result.get("id")
    print(f"  discovery task {task_id} started...", file=sys.stderr)
    final = _poll(api_key, task_id)
    if final.get("status") != "finished":
        print(f"  discovery task did not finish cleanly: {final.get('status')}", file=sys.stderr)
        return []
    files = (final.get("output") or {}).get("files") or []
    if not files:
        return []
    with urllib.request.urlopen(files[0], timeout=60) as resp:
        csv_text = resp.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(csv_text)))


# ---------- Stage 2: Enrichment ----------

SOCIAL_PATTERNS = {
    "instagram_url": re.compile(r"instagram\.com/\S+", re.I),
    "facebook_url": re.compile(r"facebook\.com/\S+", re.I),
    "linkedin_url": re.compile(r"linkedin\.com/\S+", re.I),
    "tiktok_url": re.compile(r"tiktok\.com/\S+", re.I),
    "x_url": re.compile(r"(?:twitter|x)\.com/\S+", re.I),
    "youtube_url": re.compile(r"youtube\.com/\S+", re.I),
}
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_PATTERN = re.compile(r"tel:([+\d][\d\-\s()]{6,})")
WHATSAPP_PATTERN = re.compile(r"(?:wa\.me|whatsapp\.com)/\S+", re.I)

# A social link with no profile path is the network's own homepage, not a
# contact. The Contact Finder routinely emits "https://www.instagram.com/?hl=en"
# in social_media_information, which the old parser accepted as a real profile:
# it set instagram_url, scored +15 for "Active social profile", and set
# next_action to "Send first DM" for a lead with no handle to DM. Confirmed on
# LAMORE COLLECTIONS BOUTIQUE, 2026-09-01.
JUNK_SOCIAL = re.compile(
    r"^https?://(?:www\.)?(?:instagram|facebook|linkedin|tiktok|twitter|x|youtube|threads)\.com/?(?:\?.*)?$",
    re.I,
)


def _unwrap_redirect(url):
    """Instagram wraps outbound links as l.instagram.com/?u=<urlencoded>."""
    m = re.search(r"[?&]u=([^&]+)", url)
    if m and ("l.instagram.com" in url or "l.facebook.com" in url):
        from urllib.parse import unquote
        return unquote(m.group(1))
    return url


_URL_TOKEN = re.compile(r"https?://[^\s{}\"']+", re.I)


def _extract_url(raw):
    """Pull a real https?:// URL out of a field, discarding garbage wrapping.

    Confirmed 2026-09-16: BrowserAct's Contact Finder sometimes hands back a
    field wrapped in stray literal braces (e.g. "{https://geraldbabies.com/}")
    or, worse, an unsubstituted workflow template token like
    "{constant_placeholder}" that isn't a URL at all. The old code trusted
    these values verbatim, so "{constant_placeholder}" was written into
    Childmate's website_url as if it were a real site, and
    "{https://www.instagram.com/Omackidsstore/}" got a second "https://"
    glued onto its front (because it didn't start with "http" once the brace
    was in front) -> "https://{https://www.instagram.com/Omackidsstore/}".

    Strip enclosing junk, then require an actual https?:// substring. If none
    is found, the field is not usable data and we return "" rather than
    invent a URL or leak the raw placeholder downstream.
    """
    if not raw:
        return ""
    raw = raw.strip().strip("{}\"' ")
    m = _URL_TOKEN.search(raw)
    if not m:
        return ""
    return m.group(0).rstrip("{}\"').,;")


def _clean_social(url):
    url = url.strip().strip("{}\"' ")
    url = _unwrap_redirect(url.rstrip(".,;)}"))
    if not url.startswith("http"):
        url = "https://" + url
    return "" if JUNK_SOCIAL.match(url) else url


def _maps_search_url(name, address, city, country):
    """Best-available source link back to where a lead was found.

    The Maps discovery CSV only returns name/address/rating/reviews (see
    docs/system/03-prospect-intelligence.md) -- no place_id or direct listing
    URL -- so a stable permalink to the exact Maps listing isn't possible from
    this data. A Google Maps search query for the business name + address (or
    city/country if no address came back) reliably resolves to that listing
    at or near the top of results, and gives Ridwan a one-click way to verify
    a lead instead of hand-searching. Requested 2026-09-18: every prospect
    must carry a source link.
    """
    from urllib.parse import quote_plus
    query = ", ".join(p for p in [name, address or f"{city}, {country}".strip(", ")] if p)
    if not query:
        return ""
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"


def parse_enrichment_row(row):
    """Turn one Contact Finder output row into our enrichment dict.

    Single source of truth for this parsing — leadgen_run.py calls it too, so
    the two paths cannot drift.

    Two field bugs fixed here on 2026-09-01, after reading a real successful
    task's output instead of trusting the original implementation:

      * The row's profile field is `current_page_url`, NOT `page_url`. Nothing
        ever read `page_url`, so the single most useful field — often the real
        Instagram profile, e.g. instagram.com/lilywoodensen — was discarded on
        every lead the workflow ever enriched.
      * `current_page_url` is frequently a social profile rather than a website.
        Routing it blindly into website_url would both invent a "website" and
        flip the Build/Fix/Scale track to the wrong branch, so it is classified
        first and only becomes website_url when it is genuinely neither social
        nor a search page.
    """
    e = {k: "" for k in ("website_url", "instagram_url", "facebook_url", "linkedin_url",
                         "tiktok_url", "x_url", "youtube_url", "email", "phone", "whatsapp")}

    # _extract_url strips stray brace-wrapping and rejects unsubstituted
    # template tokens (e.g. "{constant_placeholder}") before anything below
    # ever sees them -- see its docstring for the confirmed failure cases.
    current = _extract_url(row.get("current_page_url") or row.get("page_url") or "")
    if current:
        current = _unwrap_redirect(current)
        matched_social = False
        for field, pattern in SOCIAL_PATTERNS.items():
            if pattern.search(current):
                cleaned = _clean_social(current)
                if cleaned:
                    e[field] = cleaned
                matched_social = True
                break
        if not matched_social and "google." not in current:
            e["website_url"] = current.split("?")[0]

    social_text = row.get("social_media_information") or ""
    for field, pattern in SOCIAL_PATTERNS.items():
        if e[field]:
            continue  # current_page_url already gave us a better, specific one
        m = pattern.search(social_text)
        if m:
            cleaned = _clean_social(m.group(0))
            if cleaned:
                e[field] = cleaned

    wa = WHATSAPP_PATTERN.search(social_text)
    if wa:
        e["whatsapp"] = _unwrap_redirect(wa.group(0).rstrip(".,;)"))
    # WhatsApp links usually arrive wrapped in an l.instagram.com redirect, so
    # look inside the wrapper too when the bare pattern misses.
    if not e["whatsapp"]:
        for cand in re.findall(r"https?://l\.(?:instagram|facebook)\.com/\S+", social_text):
            unwrapped = _unwrap_redirect(cand)
            if WHATSAPP_PATTERN.search(unwrapped):
                e["whatsapp"] = unwrapped.split("&")[0]
                break

    em = EMAIL_PATTERN.search(social_text)
    if em:
        e["email"] = em.group(0)
    ph = PHONE_PATTERN.search(social_text)
    if ph:
        e["phone"] = ph.group(1).strip()
    return e


def enrich_business(api_key, workflow_id, company_query):
    result = bc.run_task(api_key, workflow_id, {"Company_name": company_query})
    task_id = result.get("id")
    print(f"  enrich task {task_id} for '{company_query}'...", file=sys.stderr)
    final = _poll(api_key, task_id, timeout=240)
    enrichment = {
        "website_url": "", "instagram_url": "", "facebook_url": "", "linkedin_url": "",
        "tiktok_url": "", "x_url": "", "youtube_url": "", "email": "", "phone": "",
    }
    if final.get("status") != "finished":
        print(f"  enrichment {final.get('status')} for '{company_query}'", file=sys.stderr)
        return enrichment
    raw = (final.get("output") or {}).get("string") or "[]"
    try:
        rows = json.loads(raw)
    except json.JSONDecodeError:
        return enrichment
    if not rows:
        return enrichment
    return parse_enrichment_row(rows[0])


def _poll(api_key, task_id, interval=15, timeout=300):
    elapsed = 0
    while elapsed < timeout:
        status = bc.get_task_status(api_key, task_id)
        if status.get("status") in ("finished", "failed", "canceled"):
            return bc.get_task(api_key, task_id)
        time.sleep(interval)
        elapsed += interval
    return {"status": "timeout"}


# ---------- Stage 3: Score + qualify (mirrors backend/lead_engine.py exactly) ----------

def _map_row_name(map_row):
    """Business-name column, tolerant of BrowserAct renaming its CSV headers.

    Confirmed 2026-09-08: the Google Maps Scraper template's output column
    changed from "name" to "business_name" sometime between the 2026-09-01
    run (worked, "name") and this run (empty, only "business_name" present).
    That silently zeroed every lead that week - see the 2026-W37 incident
    note in browseract-weekly-log.json. Check both, plus "title" as a third
    fallback, so a future rename doesn't repeat this.
    """
    return (map_row.get("name") or map_row.get("business_name") or map_row.get("title") or "").strip()


def score_and_qualify(map_row, enrichment):
    name = _map_row_name(map_row)
    rating_raw = (map_row.get("star_rating") or "").strip()
    review_count_raw = (map_row.get("review_count") or "").strip()
    try:
        rating = float(rating_raw.split("/")[0]) if rating_raw else 0.0
    except ValueError:
        rating = 0.0
    reviews = int(review_count_raw) if review_count_raw.isdigit() else 0

    has_website = bool(enrichment["website_url"])
    has_social = any(enrichment[f] for f in ("instagram_url", "facebook_url", "tiktok_url"))
    has_real_presence = reviews >= 10 or rating >= 4.5 or has_social

    signals = []
    score = 30  # baseline: exists on Google Maps at all
    if reviews > 0:
        signals.append(f"{reviews} Google reviews")
        score += min(reviews, 40)  # cap the reviews contribution
    if rating >= 4.5:
        signals.append(f"{rating}/5.0 rating")
        score += 10
    if has_social:
        signals.append("Active social profile")
        score += 15
    if enrichment.get("whatsapp"):
        signals.append("WhatsApp link")
        score += 10
    if enrichment["email"]:
        signals.append("Public email")
        score += 5
    if enrichment["phone"]:
        signals.append("Public phone")

    # Ridwan's qualification rule: real presence + weak execution scores HIGHEST.
    # This is the free-template-giveaway sweet spot, not a dead lead.
    if has_real_presence and not has_website:
        signals.append("No real website found (free-template candidate)")
        score += 20
    elif has_website:
        signals.append(f"Has existing website: {enrichment['website_url']}")

    score = max(0, min(score, 100))
    return {
        "signals": "; ".join(signals),
        "fit_score": score,
        "confidence": "high" if score >= 80 else "medium" if score >= 60 else "low",
        "status": "Qualified" if score >= 60 else "Needs Review",
        "pipeline_stage": "First Message Ready" if score >= 60 else "New",
        # Only promise a DM when there is an actual channel to send it on.
        # Junk social URLs used to satisfy this check (see JUNK_SOCIAL).
        "next_action": ("Send first DM" if (enrichment["instagram_url"] or enrichment.get("whatsapp"))
                        else "Find contact channel manually"),
    }


def build_prospect(map_row, enrichment, niche, country, city, audience_type, source_query, task_ids):
    scored = score_and_qualify(map_row, enrichment)
    name = _map_row_name(map_row)

    # Track classification (2026-08-19): Build (no site, real presence) / Fix
    # (has a site but it's weak) / Scale (has a good site — pursued for
    # SEO/ads/management, not skipped). See lead_playbook.py.
    has_website = bool(enrichment["website_url"])
    has_social = any(enrichment[f] for f in ("instagram_url", "facebook_url", "tiktok_url"))
    rating_raw = (map_row.get("star_rating") or "").strip()
    review_count_raw = (map_row.get("review_count") or "").strip()
    try:
        rating = float(rating_raw.split("/")[0]) if rating_raw else 0.0
    except ValueError:
        rating = 0.0
    reviews = int(review_count_raw) if review_count_raw.isdigit() else 0
    has_real_presence = reviews >= 10 or rating >= 4.5 or has_social

    quality = None
    if has_website:
        print(f"  checking site quality for {enrichment['website_url']}...", file=sys.stderr)
        quality = lp.assess_website_quality(enrichment["website_url"])
    track = lp.classify_track(has_website, has_real_presence, quality["score"] if quality else None)
    pitch_notes = lp.build_pitch_notes(track, niche, country)

    notes_parts = []
    address = (map_row.get("full_address") or "").strip()
    if address:
        notes_parts.append(f"Address: {address}")
    if enrichment["phone"]:
        notes_parts.append(f"Phone: {enrichment['phone']}")
    notes_parts.append(pitch_notes)
    if quality:
        notes_parts.append(f"Site quality score: {quality['score']}/100 ({'; '.join(quality['signals'])})")
    notes_parts.append("Sourced via BrowserAct (Google Maps + Google Business Contact Finder). Review before outreach.")

    # Every prospect must carry a way back to where it was found (2026-09-18).
    # Prefer the lead's own Instagram handle when we have one -- it's a direct
    # profile link, better than a search. Otherwise fall back to a Google Maps
    # search link built from name + address (see _maps_search_url docstring
    # for why this can't be a direct place permalink with the current CSV).
    source_url = enrichment["instagram_url"] or _maps_search_url(name, address, city, country)

    return {
        "id": f"koolestflow-browseract-{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:50]}",
        "brand_name": name,
        "website_url": enrichment["website_url"],
        "instagram_url": enrichment["instagram_url"],
        "email": enrichment["email"],
        "whatsapp": enrichment.get("whatsapp", ""),
        "country": country,
        "city": city,
        "timezone": "",
        "niche": niche,
        "audience_type": audience_type,
        "source": "browseract",
        "source_query": source_query,
        "source_url": source_url,
        "notes": " | ".join(notes_parts),
        **scored,
    }


# ---------- Stage 4: KoolestFlow push ----------
# 2026-08-26: this used to be a self-contained duplicate of
# koolestflow_client.py's login/get_state/save_state/dedupe/push functions
# (never actually refactored to use the shared module despite that module's
# own docstring claiming it was "factored out of" this file). Replaced with
# a direct call into the shared, ledger-backed client so a brand found via
# Ad Library and a brand found via BrowserAct/Maps dedupe against EACH OTHER
# too, and so every push here also gets recorded in the taken-brands ledger
# (.ai-workflow/taken-brands-ledger.json), not just Ad Library pushes.

def push_to_koolestflow(base_url, password, new_prospects, dry_run=False):
    return kc.push_to_koolestflow(base_url, password, new_prospects, dry_run=dry_run)


# ---------- CLI ----------

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--area", help="City/area for Google Maps discovery, e.g. 'Lekki, Lagos'")
    p.add_argument("--keyword", help="Niche keyword for Google Maps discovery, e.g. 'fashion boutique'")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--from-dm-leads-pool", action="store_true",
                    help="Skip Stage 1; enrich+push leads already in dm_leads_pool.json instead")
    p.add_argument("--niche", default="")
    p.add_argument("--country", default="")
    p.add_argument("--city", default="")
    p.add_argument("--audience-type", default="")
    p.add_argument("--dry-run", action="store_true", help="Print what would be pushed, skip the KoolestFlow API call")
    p.add_argument("--skip-enrichment", action="store_true",
                    help="Push discovery results as-is without Stage 2 enrichment (faster/cheaper, no website/social lookup)")
    p.add_argument("--local", action="store_true",
                    help="Push to the local KoolestFlow instance (http://127.0.0.1:8787) instead of the Vercel deployment")
    args = p.parse_args()

    api_key = bc.load_api_key()
    if not api_key:
        print("BROWSERACT_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    discovery_wf = env("BROWSERACT_LEADGEN_WORKFLOW_ID")
    enrich_wf = env("BROWSERACT_ENRICH_WORKFLOW_ID")
    if args.local:
        kf_base = env("KOOLESTFLOW_LOCAL_BASE_URL", "http://127.0.0.1:8787")
    else:
        kf_base = env("KOOLESTFLOW_BASE_URL", "https://cold-dm-app.vercel.app")
    kf_password = env("KOOLESTFLOW_APP_PASSWORD")

    if args.from_dm_leads_pool:
        with open(DM_LEADS_POOL_PATH) as f:
            pool = json.load(f)
        map_rows = [{
            "name": l["businessName"], "full_address": l["address"],
            "star_rating": l["rating"] or "", "review_count": str(l["reviewCount"] or ""),
        } for l in pool["leads"] if l["status"] == "NeedsContactInfo"]
        source_query = "dm_leads_pool.json backlog"
    else:
        if not (args.area and args.keyword):
            print("--area and --keyword are required unless --from-dm-leads-pool is used.", file=sys.stderr)
            sys.exit(1)
        if not discovery_wf:
            print("BROWSERACT_LEADGEN_WORKFLOW_ID not set in .env.", file=sys.stderr)
            sys.exit(1)
        print(f"Stage 1: discovering up to {args.limit} businesses in '{args.area}' for '{args.keyword}'...", file=sys.stderr)
        map_rows = run_maps_discovery(api_key, discovery_wf, args.area, args.keyword, args.limit)
        source_query = f"Area={args.area}; Keyword={args.keyword}"

    if not map_rows:
        print("No businesses found. Nothing to do.", file=sys.stderr)
        return

    print(f"Stage 1 complete: {len(map_rows)} businesses found.", file=sys.stderr)

    prospects = []
    for row in map_rows:
        name = row.get("name", "").strip()
        if not name:
            continue
        if args.skip_enrichment:
            enrichment = {k: "" for k in ("website_url", "instagram_url", "facebook_url", "linkedin_url",
                                           "tiktok_url", "x_url", "youtube_url", "email", "phone")}
        else:
            if not enrich_wf:
                print("BROWSERACT_ENRICH_WORKFLOW_ID not set in .env - skipping enrichment for all rows.", file=sys.stderr)
                enrichment = {k: "" for k in ("website_url", "instagram_url", "facebook_url", "linkedin_url",
                                               "tiktok_url", "x_url", "youtube_url", "email", "phone")}
            else:
                query = f"{name} {args.city or ''} {args.country or ''}".strip()
                enrichment = enrich_business(api_key, enrich_wf, query)
        prospects.append(build_prospect(
            row, enrichment, args.niche, args.country, args.city, args.audience_type, source_query, None,
        ))

    print(f"Stage 3 complete: {len(prospects)} prospects scored.", file=sys.stderr)

    if not kf_password and not args.dry_run:
        print("KOOLESTFLOW_APP_PASSWORD not set in .env - forcing --dry-run.", file=sys.stderr)
        args.dry_run = True

    push_to_koolestflow(kf_base, kf_password, prospects, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
ad_library_koolestflow_bridge.py — Meta Ad Library -> KoolestFlow lead pipeline.

Built 2026-08-19 alongside the Track B/C site-quality work in
lead_playbook.py. This is the "sharpest idea" sourcing method from
docs/koolestpro-growth-operating-plan.md Section C2: someone running paid
ads is already spending money on traffic, which makes them a qualified
prospect by definition, regardless of what their organic Google Maps
presence looks like. This is a SECOND, independent discovery source next
to browseract_koolestflow_bridge.py's Google Maps route — same
KoolestFlow destination, same track/pitch logic, different way in.

  Stage 1 — Discovery: query the Meta Ad Library for a country + keyword
            via the `curious_coder/facebook-ads-library-scraper` Apify
            actor (the primary pick per growth plan C2; fallback is
            `corner_cutter/facebook-ad-library-scraper` if the primary
            actor's shape ever changes). VERIFIED LIVE 2026-08-19 with a
            real 10-ad NG/fashion run — real ads came back (Temu, a
            Nigerian fabric/fashion page, AI photo apps), input shape and
            field mapping below are confirmed against actual output, not
            guessed. One quirk found: the actor REJECTS `count` below 10
            ("'Maximum charged results' option must be atleast 10") —
            run_discovery() bumps any lower --limit up to 10 automatically.

  Stage 2 — Qualify mechanically per growth plan C2's table, using the
            ad's own destination link (no separate enrichment call
            needed — the ad library data already has the site/profile it
            points to):
              Instagram profile / DM   -> Qualified, Track Build
              WhatsApp link            -> Qualified, Track Build
              Linktree or similar      -> Qualified, Track Build
              Their own site, weak     -> Qualified, Track Fix
              Their own site, good     -> Qualified, Track Scale
                (growth plan originally said reject Track Scale; Ridwan
                corrected this 2026-08-19 — good sites are pursued for
                SEO/ads-management/retainer work, not filtered out)
            Site quality (weak vs good) reuses lead_playbook.assess_website_quality,
            same threshold as the Maps route, so both sources are directly
            comparable in KoolestFlow.

  Stage 3 — Score using a comparable-but-distinct formula from the Maps
            route (see score_ad_lead()): actively running a paid ad is
            itself a stronger presence signal than organic reviews, so
            the baseline starts higher.

  Stage 4 — Push into KoolestFlow via the SAME shared client as the Maps
            route (koolestflow_client.py) — dedupes against whatever's
            already there (including Maps-sourced leads), so the same
            business found both ways won't double up.

Setup:
  .env needs (APIFY_API_TOKEN already set as of 2026-08-02 for a
  different actor; KOOLESTFLOW_* already set as of 2026-08-11):
    APIFY_API_TOKEN
    KOOLESTFLOW_APP_PASSWORD
    KOOLESTFLOW_BASE_URL   (default https://cold-dm-app.vercel.app)

Usage:
  # ALWAYS do this first for a country/actor combo this project hasn't used:
  python3 apify_client.py get-actor --actor-id curious_coder~facebook-ads-library-scraper

  # Then:
  python3 ad_library_koolestflow_bridge.py --country NG --keyword "fashion" \\
    --niche "Fashion & Apparel" --city Lagos --audience-type "E-commerce/DTC" \\
    --limit 10 --dry-run
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apify_client as ac
import koolestflow_client as kc
import lead_playbook as lp

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

PRIMARY_ACTOR = "curious_coder~facebook-ads-library-scraper"
FALLBACK_ACTOR = "corner_cutter~facebook-ad-library-scraper"

DESTINATION_PATTERNS = {
    "instagram": re.compile(r"instagram\.com/", re.I),
    "whatsapp": re.compile(r"(wa\.me/|whatsapp\.com/)", re.I),
    "linktree": re.compile(r"(linktr\.ee/|linktree\.com/|beacons\.ai/|bio\.link/)", re.I),
    "facebook": re.compile(r"facebook\.com/(?!ads/library)", re.I),
}


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


def build_ad_library_url(country, keyword, location_hint=""):
    """Standard Meta Ad Library search URL — stable, documented format.
    This is what most Apify FB-ads actors accept as a `urls` input item.

    location_hint (added 2026-08-27): the `country`/`is_targeted_country`
    params alone do NOT reliably scope results (confirmed live — see the
    note above MARKETPLACE_PATTERNS; flipping is_targeted_country between
    true/false produced byte-identical results). What DOES work: putting
    the city/location as literal text in the `q` search term itself. A
    bare "kids" query for NG returned Jumia, Amazon.com and other global
    brands with zero Nigeria connection; "kids Lagos" returned 10/10
    genuinely Nigerian small businesses (Bookstheylove.ng, Phytobyte NG,
    Toysenter, Zoom Exclusive Dental Care Lagos, etc). Always pass a
    location_hint (the run's --city, or "Nigeria" as a fallback) for NG
    runs."""
    from urllib.parse import quote
    q = f"{keyword} {location_hint}".strip() if location_hint else keyword
    return (
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
        f"&country={quote(country)}&is_targeted_country=false&media_type=all"
        f"&q={quote(q)}&search_type=keyword_unordered"
    )


# ---------------------------------------------------------------------
# 2026-08-27 fixes, after Ridwan reviewed the first live run's actual
# pushed leads (CeraVe Skincare via konga.com, Soluna SKIN, and two
# "Korean skincare expert" pages at interview.lovi.care) and rejected
# all four: the Konga one is a marketplace listing not a real prospect
# site, and the other three are not Nigerian businesses at all.
#
# Root cause, confirmed by pulling a raw actor item directly: the Ad
# Library search's `country=NG` + `is_targeted_country=false` params do
# NOT reliably scope results to Nigerian advertisers. A test NG/"fashion"
# query returned a Cambodian Shopee ad (Khmer text, KHR pricing,
# ShopeeKH.Official page) with no Nigeria connection whatsoever. The
# actor is returning globally-run ads matched on keyword, not ads from
# Nigerian businesses. `country=NG` cannot be trusted alone — every lead
# now needs an independent Nigeria signal check (see has_nigeria_signal
# below) before it's allowed to push.
# ---------------------------------------------------------------------

# Nigerian marketplace domains. A lead whose ad links here is NOT "their
# website" — it's a listing on someone else's platform. Ridwan's
# instruction: this is still a valid lead type (there's nothing wrong
# with a JiJi/Konga/Jumia seller), but it must be handled differently —
# find their social media presence and pitch them on a real website,
# don't treat the marketplace URL as their site, and only bother if they
# look like they're already selling well (a real budget signal), since a
# free/cheap website pitch only lands with someone who can afford to act
# on it.
MARKETPLACE_PATTERNS = {
    "konga": re.compile(r"konga\.com", re.I),
    "jumia": re.compile(r"jumia\.com(\.ng)?", re.I),
    "jiji": re.compile(r"jiji\.ng", re.I),
}

# A marketplace-hosted seller only counts as a real prospect if there's
# some signal they're already doing real volume (Ridwan's call,
# 2026-08-27) — page likes is the only volume proxy available from this
# actor's data without a separate per-listing scrape. Kept deliberately
# a bit above the general MEGA_BRAND ceiling's floor so a brand-new
# throwaway page doesn't qualify just for running one ad.
MARKETPLACE_MIN_LIKES = 500

# Signals that an ad/business actually has something to do with Nigeria.
# Checked against the ad's own text (card titles/bodies/captions, where
# Naira pricing or a Nigerian phone number would show up) plus the link
# domain. This is a heuristic, not a guarantee — but it catches the
# specific failure mode from the 2026-08-26 run (global brands/ads with
# zero Nigeria content slipping through a `country=NG` search).
NIGERIA_SIGNAL_PATTERNS = [
    re.compile(r"₦"),                       # naira sign, u20a6 = ₦
    re.compile(r"\bNGN\b", re.I),
    re.compile(r"\bnaira\b", re.I),
    re.compile(r"\+234"),
    re.compile(r"\b0(70|80|81|90|91)\d{8}\b"),    # common Nigerian local mobile prefixes
    re.compile(r"\blagos\b", re.I),
    re.compile(r"\babuja\b", re.I),
    re.compile(r"\bnigeria(n)?\b", re.I),
    re.compile(r"\.ng\b", re.I),   # matches ".ng" in a domain OR bare in a page name like "Bookstheylove.ng"
    re.compile(r"\.com\.ng", re.I),
]


def _ad_text_blob(item):
    """All human-readable text on the ad — cards' title/body/caption plus
    the top-level snapshot fields — concatenated once so signal checks
    (Nigeria, currency, etc.) don't need separate per-field logic."""
    snap = item.get("snapshot") or {}
    parts = []
    for key in ("caption", "byline"):
        v = snap.get(key)
        if v:
            parts.append(str(v))
    for card in (snap.get("cards") or []):
        for key in ("title", "body", "caption", "link_description"):
            v = card.get(key)
            if v:
                parts.append(str(v))
    return " ".join(parts)


def has_nigeria_signal(item, link_url, page_name=""):
    """True if the ad's own text, page name, or link domain shows a real
    Nigeria connection. Marketplace domains (konga.com, jumia.com.ng,
    jiji.ng) count on their own — those platforms are themselves
    Nigeria-scoped even before checking ad text, konga.com in particular
    being Nigeria-only. Everything else needs an actual Naira/phone/place
    signal, since `country=NG` in the search alone has been confirmed
    unreliable.

    2026-08-27 fix: page_name must be checked too, not just ad body text
    — the first version of this filter missed "Zoom Exclusive Dental
    Care Lagos" (Lagos is right there in the page name) and
    "Bookstheylove.ng" (.ng is right there in the page name) because it
    only looked at card text and the clicked link_url (which for a
    WhatsApp-destination ad is just api.whatsapp.com/send, carrying no
    location info at all)."""
    if link_url:
        for pattern in MARKETPLACE_PATTERNS.values():
            if pattern.search(link_url):
                return True
    blob = f"{page_name} {_ad_text_blob(item)} {link_url or ''}"
    return any(p.search(blob) for p in NIGERIA_SIGNAL_PATTERNS)


def classify_destination_with_marketplace(link_url):
    """Like classify_destination(), but checks marketplace domains first
    — a Konga/Jumia/JiJi link must never be treated as 'own_site' (that
    would wrongly run a site-quality check against a platform Ridwan's
    prospect doesn't control, and could score them into Track Scale)."""
    if not link_url:
        return "unknown"
    for pattern in MARKETPLACE_PATTERNS.values():
        if pattern.search(link_url):
            return "marketplace"
    return classify_destination(link_url)


MIN_ACTOR_COUNT = 10  # VERIFIED live 2026-08-19: this actor rejects count < 10
                       # with "'Maximum charged results' option must be atleast 10".


def run_discovery(token, actor_id, country, keyword, limit, location_hint=""):
    """Input shape VERIFIED live 2026-08-19 against a real 10-ad NG/fashion
    test run (curious_coder/facebook-ads-library-scraper): a `urls` list
    (search page URLs) + a `count` cap, minimum 10 (see MIN_ACTOR_COUNT).
    Real fields confirmed in the response: top-level `is_active`,
    `ad_archive_id`, `page_name`, `publisher_platform`; most everything
    else nested under `snapshot` (`snapshot.page_name`, `snapshot.link_url`,
    `snapshot.cards[].link_url`, `snapshot.page_like_count`). See
    extract_ad_fields() for the exact mapping. Cost at time of testing:
    $0.00075/ad + a one-time $0.00005 actor-start charge — 10 ads is
    about $0.0075 per run."""
    if limit < MIN_ACTOR_COUNT:
        print(f"  bumping limit {limit} up to the actor's minimum of {MIN_ACTOR_COUNT}.", file=sys.stderr)
        limit = MIN_ACTOR_COUNT
    search_url = build_ad_library_url(country, keyword, location_hint=location_hint)
    run_input = {"urls": [{"url": search_url}], "count": limit}
    print(f"  running Apify actor {actor_id} for country={country} keyword='{keyword}' location_hint='{location_hint}'...", file=sys.stderr)
    items = ac.run_actor_sync(token, actor_id, run_input)
    if not isinstance(items, list):
        print(f"  unexpected actor output shape (not a list): {type(items)}", file=sys.stderr)
        return []
    return items


def extract_ad_fields(item):
    """Field mapping VERIFIED live 2026-08-19 against curious_coder/facebook-ads-library-scraper's
    real output shape (a 10-ad NG/fashion test run) — not a guess. The actor
    nests most fields under `snapshot`, but duplicates `page_name` and
    `is_active` at the top level too. `link_url` lives at
    `snapshot.link_url`, falling back to `snapshot.cards[0].link_url` for ad
    formats that use cards instead of a single link. There is no direct
    Instagram-handle field from this actor — `publisher_platform` only
    tells you IF the ad ALSO ran on Instagram, not the handle, so
    ig_username stays empty and destination classification relies on
    link_url + page_like_count instead."""
    snap = item.get("snapshot") or {}
    page_name = item.get("page_name") or snap.get("page_name") or ""
    link_url = snap.get("link_url") or ""
    if not link_url:
        cards = snap.get("cards") or []
        if cards:
            link_url = cards[0].get("link_url") or ""
    is_active = item.get("is_active")
    ad_id = item.get("ad_archive_id") or item.get("id") or ""
    page_like_count = snap.get("page_like_count") or 0
    publisher_platforms = item.get("publisher_platform") or []
    page_categories = snap.get("page_categories") or []
    return {
        "page_name": (page_name or "").strip(),
        "link_url": (link_url or "").strip(),
        "ig_username": "",
        "runs_on_instagram": "INSTAGRAM" in publisher_platforms,
        "is_active": bool(is_active) if is_active is not None else True,
        "ad_id": str(ad_id or ""),
        "page_like_count": int(page_like_count) if page_like_count else 0,
        "page_categories": page_categories,
    }


# Verified live 2026-08-19: a loose NG/"fashion" keyword search returned Temu
# (11.3M page likes) and Bigbasket (823K) alongside real small businesses —
# Ad Library keyword search is NOT scoped to SMBs. Anything at or above this
# like-count is almost certainly not a Koolestpro-sized prospect; skip
# outright rather than let it eat a "Scale" slot.
MEGA_BRAND_LIKE_THRESHOLD = 100_000


def classify_destination(link_url):
    if not link_url:
        return "unknown"
    for label, pattern in DESTINATION_PATTERNS.items():
        if pattern.search(link_url):
            return label
    return "own_site"


def _category_relevance_penalty(niche, page_categories):
    """Loose keyword-overlap check between the requested niche and the ad's
    real Facebook page categories, to catch the 'searched fashion, got a
    generic AI photo app' problem seen in the 2026-08-19 test run. Not a
    hard filter (false negatives are worse than a few irrelevant leads
    slipping through) — just a score penalty + a flag for manual review."""
    if not niche or not page_categories:
        return 0, None
    niche_words = set(re.findall(r"[a-z]+", niche.lower()))
    cat_words = set(re.findall(r"[a-z]+", " ".join(page_categories).lower()))
    if niche_words & cat_words:
        return 0, None
    return -20, f"Page categories ({', '.join(page_categories)}) don't obviously match niche '{niche}' — verify relevance manually"


def score_ad_lead(ad, destination, quality, niche=""):
    """Distinct-but-comparable formula to score_and_qualify() in the Maps
    route. Running a live ad is itself a stronger signal than organic
    reviews, so the baseline starts higher (50 vs 30)."""
    signals = []
    score = 50  # baseline: actively spending on ads right now
    if ad["is_active"]:
        signals.append("Ad currently active")
        score += 10
    if ad["page_like_count"] >= 1000:
        signals.append(f"{ad['page_like_count']} Facebook page likes")
        score += 10
    elif ad["page_like_count"] >= 100:
        signals.append(f"{ad['page_like_count']} Facebook page likes")
        score += 5
    if ad["runs_on_instagram"]:
        signals.append("Ad also runs on Instagram")
        score += 5

    penalty, penalty_signal = _category_relevance_penalty(niche, ad.get("page_categories") or [])
    if penalty_signal:
        signals.append(penalty_signal)
        score += penalty

    if destination in ("instagram", "whatsapp", "linktree", "facebook"):
        signals.append(f"Ad destination is a {destination} link, not a website (free-template candidate)")
        score += 20
        track = "Build"
    elif destination == "marketplace":
        signals.append(f"Ad destination is a marketplace listing ({ad['page_like_count']} page likes) — "
                        f"needs their own website; contact via social, not the marketplace link")
        score += 15  # Build-track candidate, but marketplace budget-gating already ran before this is called
        track = "Build"
    elif destination == "own_site":
        if quality and quality["score"] < lp.FIX_THRESHOLD:
            signals.append(f"Ad destination is their own site but it's weak (quality {quality['score']}/100)")
            track = "Fix"
        elif quality:
            signals.append(f"Ad destination is their own site and it checks out (quality {quality['score']}/100)")
            score += 5
            track = "Scale"
        else:
            signals.append("Ad destination is their own site but it could not be fetched for a quality check")
            track = "Fix"
    else:
        signals.append("Ad destination unclear from available data — needs manual review")
        track = "Low Priority"

    score = max(0, min(score, 100))
    return {
        "signals": "; ".join(signals),
        "fit_score": score,
        "confidence": "high" if score >= 80 else "medium" if score >= 60 else "low",
        "status": "Qualified" if score >= 60 else "Needs Review",
        "pipeline_stage": "First Message Ready" if score >= 60 else "New",
        "next_action": "Send first DM" if (destination == "instagram" or ad["runs_on_instagram"]) else "Review contact channel",
        "track": track,
    }


def build_prospect(item, niche, country, city, audience_type, source_query):
    ad = extract_ad_fields(item)
    if not ad["page_name"]:
        return None
    if ad["page_like_count"] >= MEGA_BRAND_LIKE_THRESHOLD:
        print(f"  skipping {ad['page_name']} — {ad['page_like_count']} page likes, too big to be a real prospect", file=sys.stderr)
        return None

    # 2026-08-27: country=NG on the search alone is confirmed unreliable
    # (see the note above MARKETPLACE_PATTERNS) — every lead needs an
    # independent Nigeria signal before it's allowed through, when the
    # run is targeting Nigeria. Only gate on this for NG runs; a future
    # non-NG run shouldn't require Nigeria-specific signals.
    is_ng_run = (country or "").strip().upper() == "NG"
    if is_ng_run and not has_nigeria_signal(item, ad["link_url"], page_name=ad["page_name"]):
        print(f"  skipping {ad['page_name']} — no Nigeria signal found in ad text/link "
              f"(country=NG search param is not reliable on its own, see script header)", file=sys.stderr)
        return None

    destination = classify_destination_with_marketplace(ad["link_url"])

    # Marketplace listings (Konga/Jumia/JiJi) are a valid lead TYPE, but
    # only when the seller looks like they're already doing real volume —
    # Ridwan's instruction, 2026-08-27: don't bother with a marketplace
    # seller who has no budget signal for a website.
    if destination == "marketplace" and ad["page_like_count"] < MARKETPLACE_MIN_LIKES:
        print(f"  skipping {ad['page_name']} — marketplace listing but only {ad['page_like_count']} page likes, "
              f"no real budget/volume signal yet", file=sys.stderr)
        return None

    quality = None
    website_url = ""
    if destination == "own_site":
        website_url = ad["link_url"]
        print(f"  checking site quality for {website_url}...", file=sys.stderr)
        quality = lp.assess_website_quality(website_url)
    # Marketplace links deliberately do NOT get a site-quality check — the
    # marketplace page isn't the prospect's own site, so quality of
    # Konga/Jumia/JiJi's platform tells us nothing about them, and
    # running it would risk mis-scoring them into Track Scale.

    scored = score_ad_lead(ad, destination, quality, niche=niche)
    track = scored.pop("track")
    pitch_notes = lp.build_pitch_notes(track, niche, country)

    notes_parts = [pitch_notes]
    if quality:
        notes_parts.append(f"Site quality score: {quality['score']}/100 ({'; '.join(quality['signals'])})")
    if destination == "marketplace":
        notes_parts.append(
            f"MARKETPLACE LISTING ({ad['link_url']}) — this is NOT their website. "
            f"Find their Instagram/WhatsApp/social presence manually and pitch a real website. "
            f"{ad['page_like_count']} page likes is the only automated volume signal available; "
            f"verify actual sales volume/reviews on the listing manually before outreach."
        )
    notes_parts.append(f"Ad destination type: {destination} ({ad['link_url'] or 'not captured'})")
    notes_parts.append("Sourced via Meta Ad Library (Apify). Review before outreach.")

    # No direct IG handle from this actor (see extract_ad_fields docstring) —
    # only capture instagram_url when the ad's own link_url IS an Instagram URL.
    instagram_url = ad["link_url"] if destination == "instagram" else ""

    return {
        "id": f"koolestflow-adlibrary-{re.sub(r'[^a-z0-9]+', '-', ad['page_name'].lower()).strip('-')[:50]}",
        "brand_name": ad["page_name"],
        "website_url": website_url,
        "instagram_url": instagram_url,
        "email": "",
        "whatsapp": ad["link_url"] if destination == "whatsapp" else "",
        "country": country,
        "city": city,
        "timezone": "",
        "track": track,
        "niche": niche,
        "audience_type": audience_type,
        "source": "apify-ad-library",
        "source_query": source_query,
        "source_url": ad["link_url"],
        "notes": " | ".join(notes_parts),
        **scored,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--country", required=True, help="2-letter country code for the Ad Library search, e.g. NG")
    p.add_argument("--keyword", required=True, help="Category/keyword, e.g. 'fashion', 'skincare'")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--niche", default="")
    p.add_argument("--city", default="")
    p.add_argument("--audience-type", default="")
    p.add_argument("--actor-id", default=PRIMARY_ACTOR)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--queue", action="store_true",
                   help="Write scored prospects to .ai-workflow/pending-push/ instead of pushing. "
                        "Use this from any cloud/scheduled run: the Vercel backend does not persist "
                        "writes and the local instance is unreachable from the cloud (see CLAUDE.md).")
    p.add_argument("--local", action="store_true",
                    help="Push to the local KoolestFlow instance (http://127.0.0.1:8787) instead of the Vercel deployment")
    args = p.parse_args()

    token = ac.load_api_token()
    if not token:
        print("APIFY_API_TOKEN not set.", file=sys.stderr)
        sys.exit(1)

    # location_hint: city as literal search text is what actually scopes
    # results (see build_ad_library_url docstring, 2026-08-27) — the
    # country/is_targeted_country params alone don't. Fall back to
    # "Nigeria" if no --city was given on an NG run.
    location_hint = args.city or ("Nigeria" if args.country.strip().upper() == "NG" else "")
    items = run_discovery(token, args.actor_id, args.country, args.keyword, args.limit, location_hint=location_hint)
    if not items:
        print("No ads found (or actor returned an unexpected shape — try --actor-id with the fallback, "
              f"'{FALLBACK_ACTOR}', or run apify_client.py get-actor first to check the input schema).",
              file=sys.stderr)
        return

    print(f"Stage 1 complete: {len(items)} ads found.", file=sys.stderr)
    source_query = f"Country={args.country}; Keyword={args.keyword}; Actor={args.actor_id}"

    # Ledger + in-batch dedupe (2026-09-30). The --queue path used to write
    # every scored lead, so brands already in taken-brands-ledger.json (e.g.
    # AristoMan Luxury, re-found on 2026-09-30 after being taken 2026-09-01)
    # landed in the queue again. Filter here, same key as koolestflow_client,
    # mirroring what leadgen_run.py already does for the BrowserAct source.
    ledger_keys = set(kc.load_ledger().get("brands", {}).keys())
    seen_keys = set()
    prospects = []
    for item in items:
        prospect = build_prospect(item, args.niche, args.country, args.city, args.audience_type, source_query)
        if not prospect:
            continue
        key_str = kc._ledger_key_str(kc.dedupe_key(prospect))
        if key_str in ledger_keys:
            print(f"  skipping {prospect.get('brand_name', '(unnamed)')} — already taken (ledger)", file=sys.stderr)
            continue
        if key_str in seen_keys:
            print(f"  skipping {prospect.get('brand_name', '(unnamed)')} — already taken (duplicate ad within same batch)", file=sys.stderr)
            continue
        seen_keys.add(key_str)
        prospects.append(prospect)

    print(f"Stage 3 complete: {len(prospects)} prospects scored.", file=sys.stderr)

    # Ridwan's instruction, 2026-08-27: prioritize businesses with NO
    # website yet. Build-track leads (no site, or a marketplace listing
    # standing in for one) go first in the push order; Fix/Scale (leads
    # that already have their own site) go after.
    track_priority = {"Build": 0, "Fix": 1, "Scale": 2, "Low Priority": 3}
    prospects.sort(key=lambda p: track_priority.get(p.get("track", ""), 9))

    if args.local:
        kf_base = env("KOOLESTFLOW_LOCAL_BASE_URL", "http://127.0.0.1:8787")
    else:
        kf_base = env("KOOLESTFLOW_BASE_URL", "https://cold-dm-app.vercel.app")
    kf_password = env("KOOLESTFLOW_APP_PASSWORD")
    dry_run = args.dry_run
    if not kf_password and not dry_run:
        print("KOOLESTFLOW_APP_PASSWORD not set in .env - forcing --dry-run.", file=sys.stderr)
        dry_run = True

    if args.queue:
        # Hybrid pipeline (2026-09-01): score in the cloud, let the Mac-side
        # import_pending_push.sh do the actual push into local KoolestFlow.
        if not prospects:
            # 2026-09-30: an empty file makes push_prospects_file.py exit 1 and
            # the importer retry it forever (W38 food ended up in failed/).
            print("Queued 0 prospect(s) -> no file written (nothing new to import).", file=sys.stderr)
            return
        import datetime
        pending_dir = os.path.join(PROJECT_ROOT, ".ai-workflow", "pending-push")
        os.makedirs(pending_dir, exist_ok=True)
        week = datetime.datetime.now(datetime.timezone.utc).strftime("%G-W%V")
        slug = re.sub(r"[^a-z0-9]+", "-", f"adlib-{args.country}-{args.keyword}".lower()).strip("-")
        out_path = os.path.join(pending_dir, f"{week}_{slug}.json")
        with open(out_path, "w") as f:
            json.dump({
                "meta": {
                    "week": week,
                    "ranAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "source": "apify-ad-library",
                    "sourceQuery": source_query,
                    "country": args.country, "city": args.city, "niche": args.niche,
                    "ledgerAlreadyRecorded": False,
                    "note": "Scored in the cloud, not yet pushed. import_pending_push.sh pushes this "
                            "into local KoolestFlow and records the brands in the taken-brands ledger.",
                },
                "prospects": prospects,
            }, f, indent=2, ensure_ascii=False)
        print(f"Queued {len(prospects)} prospect(s) -> {os.path.relpath(out_path, PROJECT_ROOT)}", file=sys.stderr)
        print("Not pushed. The Mac-side importer completes the loop.", file=sys.stderr)
        return

    kc.push_to_koolestflow(kf_base, kf_password, prospects, dry_run=dry_run)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
lead_playbook.py — shared logic for turning a raw discovered lead (from
BrowserAct Maps+Contact Finder, or the Meta/TikTok Ad Library route) into
a track assignment + service pitch, tailored by category and region.

Built 2026-08-19 per Ridwan's brief: "I know I need businesses that are
already doing well but do not have a working website, and those that has
a site but it is not in the best shape, and those that needs to scale...
I want it to be able to tailor its approach depending on category and
region."

Three tracks, matching Koolestpro's actual service menu (site creation/
design/development, management, CRO optimization, static ads, SEO):

  BUILD  — real presence (reviews/social/ad spend), no working website.
           Pitch: site creation, brand identity, launch package.
  FIX    — has a website, but it's weak (slow, not mobile-ready, thin
           trust signals, no clear CRO fundamentals).
           Pitch: CRO optimization, redesign/rebuild, static ads to
           existing traffic.
  SCALE  — has a website AND it's already in reasonably good shape.
           Pitch: SEO, paid ads management, ongoing retainer/management —
           NOT a rebuild. (Growth plan originally said reject these;
           Ridwan corrected this 2026-08-19 — Track C is now pursued.)

Anything with no website AND no real presence signal falls to
LOW_PRIORITY — not enough evidence this is a live, serious business.
"""

import json
import re
import socket
import time
import urllib.error
import urllib.request

# ---------------------------------------------------------------------
# Category playbook — what to lead with, per niche. Keys are loose
# lowercase matches against the `niche` string passed in (substring
# match, see match_category()). Extend this list as new niches show up.
# ---------------------------------------------------------------------

CATEGORY_PLAYBOOK = {
    "fashion": {
        "build": "Story-driven storefront + lookbook-style product pages, Instagram-first checkout flow",
        "fix": "PDP redesign (product photography hierarchy, size/fit trust signals), CRO pass on cart/checkout",
        "scale": "SEO for category + style keywords, paid social ads management, seasonal collection launches",
    },
    "beauty": {
        "build": "Ingredient/benefit-led storefront, before/after gallery, routine-builder UX",
        "fix": "Trust-signal CRO (reviews, ingredient transparency, routine bundles), page speed fix",
        "scale": "SEO for ingredient/concern keywords, retargeting ads, subscription/repeat-purchase flow",
    },
    "skincare": {
        "build": "Ingredient/benefit-led storefront, before/after gallery, routine-builder UX",
        "fix": "Trust-signal CRO (reviews, ingredient transparency, routine bundles), page speed fix",
        "scale": "SEO for ingredient/concern keywords, retargeting ads, subscription/repeat-purchase flow",
    },
    "kids": {
        "build": "Safety/trust-forward storefront, age/size filter UX, gifting-friendly checkout",
        "fix": "Trust badges (safety certs, reviews from real parents), mobile checkout CRO",
        "scale": "SEO for parent-search long-tail terms, seasonal (back-to-school, holiday) ad calendars",
    },
    "baby": {
        "build": "Safety/trust-forward storefront, age/size filter UX, gifting-friendly checkout",
        "fix": "Trust badges (safety certs, reviews from real parents), mobile checkout CRO",
        "scale": "SEO for parent-search long-tail terms, seasonal (back-to-school, holiday) ad calendars",
    },
    "home": {
        "build": "Room-scene visual storefront, bundle/collection pages, delivery-transparency CTA",
        "fix": "Product-image quality + trust-signal CRO, shipping/returns clarity, mobile speed fix",
        "scale": "SEO for room/style search terms, catalog ads, retention/repeat-buyer email+ads flow",
    },
    "gadget": {
        "build": "Spec-forward storefront, comparison tables, warranty/authenticity trust page",
        "fix": "Spec/trust CRO pass (authenticity proof, warranty, real reviews), speed fix",
        "scale": "SEO for spec/comparison search terms, paid search + retargeting, bundle upsell flow",
    },
    "electronics": {
        "build": "Spec-forward storefront, comparison tables, warranty/authenticity trust page",
        "fix": "Spec/trust CRO pass (authenticity proof, warranty, real reviews), speed fix",
        "scale": "SEO for spec/comparison search terms, paid search + retargeting, bundle upsell flow",
    },
    "food": {
        "build": "Menu/catalog storefront with WhatsApp or delivery-zone checkout, real photos of the actual product",
        "fix": "Ordering-flow CRO (delivery zone clarity, order minimums, payment friction), speed fix",
        "scale": "SEO for local delivery search terms, geo-targeted ads, loyalty/repeat-order flow",
    },
    "beverage": {
        "build": "Menu/catalog storefront with WhatsApp or delivery-zone checkout, real photos of the actual product",
        "fix": "Ordering-flow CRO (delivery zone clarity, order minimums, payment friction), speed fix",
        "scale": "SEO for local delivery search terms, geo-targeted ads, loyalty/repeat-order flow",
    },
    "fitness": {
        "build": "Program/class storefront, booking/scheduling integration, transformation proof gallery",
        "fix": "Booking-flow CRO, trust signals (certs, client results), mobile speed fix",
        "scale": "SEO for local class/program search terms, geo-targeted ads, membership/retainer upsell",
    },
}

DEFAULT_PLAYBOOK_ENTRY = {
    "build": "Full site design & development, brand identity groundwork, launch-ready storefront",
    "fix": "CRO audit and redesign pass, page-speed and mobile fixes, trust-signal improvements",
    "scale": "SEO, paid ads management, ongoing site management/retainer",
}


def match_category(niche):
    """Loose substring match against CATEGORY_PLAYBOOK keys. Falls back to DEFAULT_PLAYBOOK_ENTRY."""
    n = (niche or "").lower()
    for key, entry in CATEGORY_PLAYBOOK.items():
        if key in n:
            return entry
    return DEFAULT_PLAYBOOK_ENTRY


# ---------------------------------------------------------------------
# Region playbook — channel + price-ladder framing, per the growth plan
# (Track D for Nigeria, Track E for international). See
# docs/koolestpro-growth-operating-plan.md sections D6/D7/E2/E3.
# ---------------------------------------------------------------------

def region_notes(country):
    c = (country or "").strip().lower()
    if c in ("nigeria", "ng", "ghana", "kenya"):
        return {
            "channel": "Instagram DM primary, WhatsApp second. Manual send only — no DM automation (ban risk).",
            "priceLadder": "Nigeria ladder: Starter N250k-500k / Business N500k-1M / Premium N1M+ (see growth plan D7)",
            "openerStyle": "Short, direct, local — lead with the free sample site or a named problem, not a pitch deck",
        }
    return {
        "channel": "Email primary (send from a subdomain, never main domain), Instagram DM +4 days, LinkedIn +9 days if a named marketing/ecommerce lead exists",
        "priceLadder": "International band 'Now': audit $150-250 / page build $600-900 / full build $1,200-1,800 (see growth plan E3, bands raise only for new prospects once proof milestones are hit)",
        "openerStyle": "Hero before/after image + short screen recording naming 2 real problems (Touch 1), full rebuilt page live on a URL for repliers only (Touch 2)",
    }


# ---------------------------------------------------------------------
# Automated website quality check — lightweight, no headless browser
# (keeps this cheap enough to run inline in a scheduled task). Fetches
# the homepage once, checks response time, HTTPS, a mobile-viewport
# meta tag, a meta description, and raw page size as a crude "is this a
# thin/broken/placeholder page" signal. This is a heuristic screen, not
# a full CRO audit — flagged leads that need a real audit should still
# go through koolestpro-store-auditor-skill-a before you pitch.
# ---------------------------------------------------------------------

def assess_website_quality(url, timeout=12):
    """
    Returns {"score": 0-100, "signals": [...], "fetchOk": bool,
    "loadSeconds": float|None}. Higher score = healthier site.
    """
    result = {"score": 0, "signals": [], "fetchOk": False, "loadSeconds": None}
    if not url:
        return result

    target = url if url.startswith("http") else f"https://{url}"
    req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0 (compatible; KoolestproAudit/1.0)"})

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.time() - start
            body = resp.read(400_000)  # cap read size, we only need enough to check head tags
            final_url = resp.geturl()
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout, ConnectionResetError, Exception) as e:
        result["signals"].append(f"Site unreachable or errored: {e}")
        return result

    result["fetchOk"] = True
    result["loadSeconds"] = round(elapsed, 2)
    html = body.decode("utf-8", errors="replace")

    score = 40  # baseline: it loaded at all

    if final_url.startswith("https://"):
        score += 10
    else:
        result["signals"].append("Not served over HTTPS")

    if elapsed <= 2.0:
        score += 20
        result["signals"].append(f"Fast load ({elapsed:.1f}s)")
    elif elapsed <= 4.0:
        score += 8
        result["signals"].append(f"Moderate load time ({elapsed:.1f}s)")
    else:
        result["signals"].append(f"Slow load ({elapsed:.1f}s) — real CRO/perf issue")

    if re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.I):
        score += 15
        result["signals"].append("Has mobile viewport meta tag")
    else:
        result["signals"].append("No mobile viewport meta tag found — likely not mobile-optimized")

    if re.search(r'<meta[^>]+name=["\']description["\']', html, re.I):
        score += 10
        result["signals"].append("Has a meta description")
    else:
        result["signals"].append("No meta description — basic SEO gap")

    if len(html) < 3000:
        result["signals"].append("Very thin page (under 3KB HTML) — may be a placeholder/coming-soon page")
    else:
        score += 5

    result["score"] = max(0, min(score, 100))
    return result


# ---------------------------------------------------------------------
# Track classification
# ---------------------------------------------------------------------

FIX_THRESHOLD = 55  # website_quality score below this = Track FIX, at/above = Track SCALE


def classify_track(has_website, has_real_presence, website_quality_score=None):
    if not has_website:
        return "Build" if has_real_presence else "Low Priority"
    if website_quality_score is not None and website_quality_score < FIX_THRESHOLD:
        return "Fix"
    return "Scale"


def build_pitch_notes(track, niche, country):
    cat = match_category(niche)
    region = region_notes(country)
    track_key = {"Build": "build", "Fix": "fix", "Scale": "scale"}.get(track)
    service_line = cat.get(track_key, "") if track_key else "Not enough signal to recommend a service yet — needs manual review"
    lines = [f"Track: {track}."]
    if service_line:
        lines.append(f"Recommended: {service_line}.")
    lines.append(f"Channel: {region['channel']}")
    lines.append(f"Pricing frame: {region['priceLadder']}")
    return " | ".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test-quality":
        print(json.dumps(assess_website_quality(sys.argv[2]), indent=2))

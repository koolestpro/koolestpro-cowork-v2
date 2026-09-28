#!/usr/bin/env python3
"""
populate_sheet.py — V2 distribution pipeline, Step 5.

Expand one QA'd harvest record into one Sheet row PER SCHEDULED POST, following
the fixed Weekly Content Calendar. A single generated piece fans out into a
LinkedIn row, an Instagram row, and several Twitter rows, each with its own
day / time / caption-variant already assigned.

Durable source of truth = a LOCAL queue (outputs/distribution-queue/queue.json
+ queue.csv). It's appendable and editable in-project. The Google Sheet is a
mirror of this queue (push_sheet.py handles that) because the connected Drive
connector can create a Sheet but cannot edit rows in place — Make.com owns the
status write-back once that scenario is built (Step 7, deferred).

Every row is written status = "Ready" by default (changed 2026-08-27 — Ridwan's
call, unconditional, regardless of qa_status). qa_status still rides along from
qa_check.py for visibility, but it no longer gates the status value here: a row
that failed QA ("Needs Review: ...") is still written as "Ready" and is eligible
for Make.com to post. Catching a QA failure before it posts now depends on
Ridwan (or a future automated check) reading qa_status directly, not on status
staying "Draft".

Usage:
    python3 populate_sheet.py <qa_d_record.json> [--week-monday YYYY-MM-DD]
        [--project-root DIR] [--queue outputs/distribution-queue/queue.json]

--week-monday = the Monday of the week this content POSTS (defaults to the next
Monday from today; generation runs Fri-Sun for the following week).
"""

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# ── Live-Sheet awareness for "this week overwrite" (added 2026-09-19,
# Ridwan's instruction) ─────────────────────────────────────────────────────
# Ridwan keeps improving his content, so when a NEW post for a given
# (stream, platform) is assembled for a slot that ALREADY has an unposted
# row sitting in the CURRENT calendar week, the new (presumably better) post
# should take that slot, and the OLD row should be bumped forward to the
# next open week for the same slot rather than dropped — "keep pace" means
# nothing in the pipeline is lost, it just moves later.
#
# This can only work correctly against the LIVE Sheet, not local
# queue.json alone: Ridwan edits status (Draft/Ready) directly in the Sheet,
# and the reschedule webhook / manual repairs write date/time changes
# straight to the Sheet too, so local queue.json can be stale about exactly
# what's occupying "this week" (this is the pre-existing "known gap" flagged
# in docs/system/02-distribution.md — this change also closes it for the
# purposes of collision + overwrite detection). If the live Sheet can't be
# reached (missing creds, network error), this degrades gracefully to
# local-only collision detection (the pre-2026-09-19 behavior) with a loud
# warning, rather than failing the whole assembly run.
SHEET_ID = "1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg"
SHEET_TAB = "Untitled"


def load_env(root):
    env = {}
    path = os.path.join(root, ".env")
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def _http_json(url, data=None, headers=None, method=None):
    body = None
    hdrs = dict(headers or {})
    if data is not None:
        if isinstance(data, dict) and hdrs.get("Content-Type", "").startswith("application/x-www-form-urlencoded"):
            body = urllib.parse.urlencode(data).encode()
        else:
            body = json.dumps(data).encode()
            hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method or ("POST" if data is not None else "GET"))
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_live_sheet_token(env):
    resp = _http_json(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": env["GOOGLE_OAUTH_CLIENT_ID"],
            "client_secret": env["GOOGLE_OAUTH_CLIENT_SECRET"],
            "refresh_token": env["GOOGLE_OAUTH_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if "access_token" not in resp:
        raise RuntimeError(f"token refresh failed: {resp}")
    return resp["access_token"]


def fetch_live_rows(root):
    """Best-effort read of the live Sheet's post_id/stream/platform/
    scheduled_date/scheduled_time_local/status columns (A,C,D,E,F,K), plus
    each row's 1-indexed sheet row number (for a later targeted update).
    Returns (token, rows) on success; (None, []) on ANY failure — this must
    never block the local pipeline from running."""
    try:
        env = load_env(root)
        token = get_live_sheet_token(env)
        vals = _http_json(
            f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{urllib.parse.quote(SHEET_TAB)}!A2:K5000",
            headers={"Authorization": f"Bearer {token}"}, method="GET",
        )
        rows = []
        for i, r in enumerate(vals.get("values", []), start=2):  # start=2: row 1 is the header
            rows.append({
                "row_number": i,
                "post_id": r[0] if len(r) > 0 else "",
                "stream": r[2] if len(r) > 2 else "",
                "platform": r[3] if len(r) > 3 else "",
                "scheduled_date": r[4] if len(r) > 4 else "",
                "scheduled_time_local": r[5] if len(r) > 5 else "",
                "status": r[10] if len(r) > 10 else "",
                "source": "live",
            })
        return token, rows
    except Exception as e:  # noqa: BLE001 — deliberately broad, this is a best-effort read
        print(f"[sheet] WARNING: could not read live Sheet for overwrite/collision awareness ({e}) "
              f"— falling back to local-queue-only collision detection.")
        return None, []


def push_bump_updates(token, bumps):
    """Write each bumped LIVE row's new scheduled_date/scheduled_time_local
    straight to the Sheet (targeted E:F update on that row only — never a
    full-row rewrite, same pattern used for one-off manual repairs)."""
    applied = []
    for b in bumps:
        if b.get("row_number") is None:
            continue  # local-only row — already updated in queue.json/CSV, nothing live to touch
        try:
            _http_json(
                f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/"
                f"{urllib.parse.quote(SHEET_TAB)}!E{b['row_number']}:F{b['row_number']}?valueInputOption=USER_ENTERED",
                data={"values": [[b["new_date"], b["new_time"]]]},
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                method="PUT",
            )
            applied.append(b)
        except Exception as e:  # noqa: BLE001
            print(f"[sheet] WARNING: failed to push live bump for {b['post_id']} ({e}) — "
                  f"local queue.json was still updated; fix this row live by hand.")
    return applied

# The weekly CALENDAR is authored in US Eastern (audience is US/UK/EU). The Make
# scenario's gate was left reading Make's ORG timezone (Africa/Lagos) — Ridwan
# chose not to touch the Make setup again. So the timezone conversion happens
# HERE instead: each ET slot is converted to the local (Make-org) timezone and
# that local date/time is what gets written to the sheet, so the untouched
# Lagos-clock gate fires at the correct US moment. DST is handled per-date.
ET_TZ = "America/New_York"
DEFAULT_LOCAL_TZ = "Africa/Lagos"  # MUST match the Make org timezone

# ── Weekly Content Calendar, encoded from the V2 plan ──────────────────────
# Each slot: platform, dow (0=Mon..6=Sun), time_et, fmt, assets (list of
# filename substrings to match, or a sentinel), caption_key, angle.
# assets sentinels: "CAROUSEL_HTML" = link the companion HTML (slides exported
# client-side), "ALL_SLIDES" = every slideN image, "*substr*" = match filename.
CALENDAR = {
    "Tip": [
        {"platform": "LinkedIn",  "dow": 0, "time": "09:00", "fmt": "carousel",
         "assets": ["CAROUSEL_HTML"], "caption_key": "linkedin", "angle": "primary"},
        {"platform": "Instagram", "dow": 0, "time": "12:00", "fmt": "carousel",
         "assets": ["CAROUSEL_HTML"], "caption_key": "instagram", "angle": "cross-post"},
        # carousels never go to Twitter (plan) — no X rows for Tips
    ],
    # ── CRO Fix (rewritten 2026-09-27, Ridwan's instruction) ──────────────
    # One audit = the 3-slide carousel + 4 single graphics:
    #   carousel_slide1 = cover, carousel_slide2 = before/after,
    #   carousel_slide3 = dark annotation, *_annotated.png = clear-bg annotation.
    # The 3-image carousel ALWAYS posts to LinkedIn, Instagram AND X. Then each
    # of the four graphics posts on its own as an X single, each with its own
    # caption_key so no slot recycles another's tweet. Times picked to avoid
    # every other stream's Twitter slot (TS: Tue09/Thu13/Sat09/Sun11,
    # SA: Mon09/Tue13/Wed18/Fri13/Sat18, Store: Tue13/Wed09/Fri13/Sat09/Sun11).
    # NOTE: the X carousel row carries 3 asset_urls; the Make X scenario must
    # upload every URL and attach all media_ids (X allows up to 4 images).
    "CRO Fix": [
        {"platform": "LinkedIn",  "dow": 2, "time": "09:00", "fmt": "carousel-3",
         "assets": ["carousel_slide1", "carousel_slide2", "carousel_slide3"],
         "caption_key": "linkedin", "angle": "3-slide carousel"},
        {"platform": "Instagram", "dow": 2, "time": "12:00", "fmt": "carousel-3",
         "assets": ["carousel_slide1", "carousel_slide2", "carousel_slide3"],
         "caption_key": "instagram", "angle": "3-slide carousel"},
        {"platform": "Twitter",   "dow": 2, "time": "13:00", "fmt": "carousel-3",
         "assets": ["carousel_slide1", "carousel_slide2", "carousel_slide3"],
         "caption_key": "x_carousel", "angle": "X 3-image carousel"},
        {"platform": "Twitter",   "dow": 3, "time": "09:00", "fmt": "single",
         "assets": ["carousel_slide1"], "caption_key": "x_cover", "angle": "X single: cover"},
        {"platform": "Twitter",   "dow": 4, "time": "09:00", "fmt": "single",
         "assets": ["carousel_slide2"], "caption_key": "x_ba", "angle": "X single: before/after"},
        {"platform": "Twitter",   "dow": 5, "time": "13:00", "fmt": "single",
         "assets": ["carousel_slide3"], "caption_key": "x_anno", "angle": "X single: dark annotation"},
        {"platform": "Twitter",   "dow": 6, "time": "18:00", "fmt": "single",
         "assets": ["_annotated.png"], "caption_key": "x_anno_graphic", "angle": "X single: clear-bg annotation"},
    ],
    "Template Showcase": [
        {"platform": "LinkedIn",  "dow": 4, "time": "09:00", "fmt": "video",
         "assets": ["cover.mp4"], "caption_key": "linkedin", "angle": "cover video + thumbnail"},
        {"platform": "Instagram", "dow": 1, "time": "12:00", "fmt": "reel",
         "assets": ["laptop.mp4"], "caption_key": "linkedin", "angle": "Reel #1"},
        {"platform": "Instagram", "dow": 3, "time": "12:00", "fmt": "reel",
         # was caption_key "x" — bug fixed 2026-07-22: Instagram has no 280-char
         # constraint, so it was needlessly competing with the 3 Twitter slots
         # below for the same 3 harvested X-post variants (a record with
         # exactly 3 X variants would starve the last Twitter slot). "instagram"
         # falls back to "linkedin" via the fallback table, same as Reel #1/#3.
         "assets": ["mobile.mp4"], "caption_key": "instagram", "angle": "Reel #2"},
        {"platform": "Instagram", "dow": 4, "time": "12:00", "fmt": "reel",
         "assets": ["cover.mp4"], "caption_key": "linkedin", "angle": "Reel #3 (cross-post)"},
        {"platform": "Twitter",   "dow": 1, "time": "09:00", "fmt": "video",
         "assets": ["mobile.mp4"], "caption_key": "x", "angle": "video single #1"},
        {"platform": "Twitter",   "dow": 3, "time": "13:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "x", "angle": "still single #1"},
        {"platform": "Twitter",   "dow": 5, "time": "09:00", "fmt": "single",
         # "full-mosaic" was the pre-2026-07-29 name; the grid mosaic was retired and
         # replaced by the 2-column split page ("{slug}-full-page.png"). Both listed so
         # historical assets still match. See CLAUDE.md "CORRECTED v4".
         "assets": ["full-page", "full-mosaic"], "caption_key": "x", "angle": "still single #2"},
        # X #5 — the mobile strip (added 2026-09-02, Ridwan's instruction that
        # this asset "should always be posted in my x account" and must never be
        # skipped). Own caption_key so it cannot draw a recycled variant from
        # the shared "x" pool the way the slots above do — the whole point of
        # this post is the "full page at a glance" angle, a different pitch from
        # the build-in-public angle full-page.png carries.
        {"platform": "Twitter",   "dow": 6, "time": "11:00", "fmt": "single",
         "assets": ["mobile-strip"], "caption_key": "x_glance", "angle": "X #5 full page at a glance"},
    ],
    # Twitter widened from 3 to 5 posts (Ridwan's call, 2026-08-19): one per
    # distinct static-ad asset (4 individual angles + the combo showcase),
    # scattered across the week instead of clustered on Fri/Sat/Sun so a
    # single Static Ad doesn't dump most of its posts in one 48h window.
    # CHANGED 2026-09-28 (Ridwan: "the caption does not correlate with the
    # image"): every slot now has its own per-image caption_key. The old shared
    # "x" pool dealt 3 generic variants across 5 images by index, so a single ad
    # went out as "Four ad directions from one pan" and a review-quote tweet
    # landed on the benefit ad. The static-ad generator now writes one caption
    # per image (<div class="x-post" data-asset="ad-1">...), and the Instagram
    # single gets its own ig_single caption instead of the 4-ad LinkedIn one.
    "Static Ad": [
        {"platform": "Instagram", "dow": 5, "time": "12:00", "fmt": "carousel-4",
         "assets": ["ad-1", "ad-2", "ad-3", "ad-4"], "caption_key": "linkedin", "angle": "4-image carousel"},
        {"platform": "Instagram", "dow": 6, "time": "12:00", "fmt": "single",
         "assets": ["ad-1"], "caption_key": "ig_single", "angle": "filler single"},
        {"platform": "Twitter",   "dow": 1, "time": "13:00", "fmt": "single",
         "assets": ["ad-1"], "caption_key": "x_problem", "angle": "single #1 (problem/solution)"},
        {"platform": "Twitter",   "dow": 2, "time": "18:00", "fmt": "single",
         "assets": ["ad-2"], "caption_key": "x_benefit", "angle": "single #2 (benefit/result)"},
        {"platform": "Twitter",   "dow": 4, "time": "13:00", "fmt": "single",
         "assets": ["ad-3"], "caption_key": "x_proof", "angle": "single #3 (social proof)"},
        {"platform": "Twitter",   "dow": 5, "time": "18:00", "fmt": "single",
         "assets": ["ad-4"], "caption_key": "x_offer", "angle": "single #4 (offer/urgency)"},
        {"platform": "Twitter",   "dow": 0, "time": "09:00", "fmt": "single",
         "assets": ["combined-showcase"], "caption_key": "x_combo", "angle": "single #5 (combo)"},
    ],
    # ── Store Template launches (added 2026-09-01, Ridwan's instruction) ──
    # A finished store template (Lumora, Meridian, every future one) is
    # proof-of-work for the free e-commerce site offer, so it gets its own
    # stream rather than riding the "Template Showcase" slots — those match
    # cover.mp4 / laptop.mp4 / mobile.mp4, and a store template package is
    # STILLS ONLY (cover / preview / full-page). Under the old routing these
    # items harvested nothing and matched no asset, which is why Lumora and
    # Meridian sat registered with zero distribution rows.
    #
    # Anchor is Tuesday 09:00 ET (Ridwan's call) so store builds never
    # collide with the Friday Template Showcase drumbeat, and the "here is
    # work I shipped" post lands early in the week.
    #
    # The 4 X angles come straight from the Store Template Launch Content
    # rule in CLAUDE.md: showcase / free-offer / niche / build-in-public.
    # Each has its own caption_key, so no slot has to share a variant pool
    # and no angle can be silently reused (the failure mode the Static Ad
    # stream still lives with).
    "Store Template": [
        # Two pages on purpose. feed_linkedin.py routes any image row through a
        # hosted PDF (Make's LinkedIn scenario has only text / .mp4 / .pdf
        # routes, no plain-image route), and a ONE-page PDF renders as a
        # document card with a single swipe — a weak anchor post. Cover plus
        # the phone preview gives a real 2-page carousel, which is also the
        # format LinkedIn pushes hardest.
        {"platform": "LinkedIn",  "dow": 1, "time": "09:00", "fmt": "carousel-2",
         "assets": ["cover.png", "preview"], "caption_key": "linkedin", "angle": "launch anchor"},
        {"platform": "Instagram", "dow": 3, "time": "12:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "instagram", "angle": "multi-phone preview"},
        {"platform": "Twitter",   "dow": 1, "time": "13:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "x_showcase", "angle": "X #1 template showcase"},
        {"platform": "Twitter",   "dow": 2, "time": "09:00", "fmt": "single",
         "assets": ["cover-16x9"], "caption_key": "x_freeoffer", "angle": "X #2 free offer / Nigeria"},
        {"platform": "Twitter",   "dow": 4, "time": "13:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "x_niche", "angle": "X #3 niche-targeted"},
        {"platform": "Twitter",   "dow": 5, "time": "09:00", "fmt": "single",
         # the compressed -x variant, never the full-res full-page.png: that
         # one runs 4-5MB and is exactly what broke the Bebemoss X post on
         # 2026-08-01 (Make's fetch limit). Matcher is "full-page-x" not
         # "full-page" so it cannot fall back to the oversized original.
         "assets": ["full-page-x"], "caption_key": "x_buildpublic", "angle": "X #4 build in public"},
        {"platform": "Twitter",   "dow": 6, "time": "11:00", "fmt": "single",
         "assets": ["mobile-strip"], "caption_key": "x_glance", "angle": "X #5 full page at a glance"},
    ],
    # Same shape, minus the free-site offer. A paid client build or a local
    # paid job must never advertise free work, so slot #2 carries a
    # results/process angle instead. harvest_store_template.py picks the
    # stream automatically from the brand's isConceptBrand flag.
    "Store Template (Paid)": [
        {"platform": "LinkedIn",  "dow": 1, "time": "09:00", "fmt": "carousel-2",
         "assets": ["cover.png", "preview"], "caption_key": "linkedin", "angle": "launch anchor"},
        {"platform": "Instagram", "dow": 3, "time": "12:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "instagram", "angle": "multi-phone preview"},
        {"platform": "Twitter",   "dow": 1, "time": "13:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "x_showcase", "angle": "X #1 template showcase"},
        {"platform": "Twitter",   "dow": 2, "time": "09:00", "fmt": "single",
         "assets": ["cover-16x9"], "caption_key": "x_results", "angle": "X #2 result / process"},
        {"platform": "Twitter",   "dow": 4, "time": "13:00", "fmt": "single",
         "assets": ["preview"], "caption_key": "x_niche", "angle": "X #3 niche-targeted"},
        {"platform": "Twitter",   "dow": 5, "time": "09:00", "fmt": "single",
         "assets": ["full-page-x"], "caption_key": "x_buildpublic", "angle": "X #4 build in public"},
        {"platform": "Twitter",   "dow": 6, "time": "11:00", "fmt": "single",
         "assets": ["mobile-strip"], "caption_key": "x_glance", "angle": "X #5 full page at a glance"},
    ],
}

PLATFORM_TAG = {"LinkedIn": "li", "Instagram": "ig", "Twitter": "x"}

# Column order is CONTRACTUAL: the Make scenario references columns by index
# and the LIVE "Koolestpro Distribution Queue" Google Sheet header row is the
# ground truth (verified directly 2026-07-22): A post_id, B pipeline_item_id,
# C stream, D platform, E scheduled_date, F scheduled_time_local, G
# intended_et, H asset_paths, I caption, J caption_source_tab, K status,
# L qa_status, M posted_at, N content_system_folder, O caption_json,
# P asset_urls. That's {{1.`4`}}=scheduled_date, {{1.`5`}}=scheduled_time_local,
# {{1.`10`}}=status, {{1.`12`}}=posted_at, {{1.`14`}}=caption_json,
# {{1.`15`}}=asset_urls in the Make scenario (0-indexed).
#
# This list PREVIOUSLY had "intended_et" last (position 15) instead of its
# real position (6, right after scheduled_time_local) — fixed 2026-07-22.
# That drift didn't corrupt the already-populated live sheet (rows were
# written against the correct positions some other way), but it meant any
# future CSV-driven bulk write using this list would have shifted every
# column after intended_et by one position relative to the real header.
# APPEND ONLY — never reorder or insert without re-verifying the live header.
COLUMNS = [
    "post_id", "pipeline_item_id", "stream", "platform", "scheduled_date",
    "scheduled_time_local",
    "intended_et",        # index 6 — human reference ("09:00 ET"); Make ignores it
    "asset_paths", "caption", "caption_source_tab",
    "status", "qa_status", "posted_at", "content_system_folder",
    "caption_json",       # index 14 — pre-escaped JSON string literal for the post body
    "asset_urls",         # index 15 — public asset URLs (Cloudinary etc.)
]


def next_monday(from_date=None):
    d = from_date or date.today()
    return d + timedelta(days=(7 - d.weekday()) % 7 or 7)


def current_monday(from_date=None):
    """Monday of THIS week. Fixed 2026-08-24 (Ridwan's call): populate_sheet.py
    used to always anchor to next_monday(), which is right for the normal
    Fri-Sun generation cadence but wrong the moment a backlog gets assembled
    (several items in one run, or an assembly run that catches up after being
    skipped for weeks) — every item's slots piled into the SAME single future
    week instead of using open slots in the current week first. find_open_week()
    below now starts the search HERE and only rolls forward per-slot when a
    slot's date has already passed or collides with an existing queued row."""
    d = from_date or date.today()
    return d - timedelta(days=d.weekday())


X_CHAR_LIMIT = 280  # non-Premium X accounts hard-cap at this length

# Thread-format slots (caption_key == "x_thread") are the one legitimate case
# where multiple variants belong together as sequential tweets — everything
# else (plain "x", "x_singles", "x_angles") must resolve to exactly ONE
# variant per slot. Joining them was the 2026-07-22 bug: three separate,
# already-properly-sized (<280 char) X post variants got concatenated with
# "\n\n" into one 757-char blob and shipped as a single tweet, which X
# rejected. Each variant is meant to be its OWN post on its OWN slot.
THREAD_KEYS = {"x_thread"}

# Caption keys written for ONE specific image (2026-09-28). They never borrow
# from a shared pool, and a row whose caption fails caption_fit.check() is
# written as status "Draft" so Make.com does not post it. This is a deliberate
# exception to the 2026-08-27 "always Ready" rule: a caption that describes the
# wrong image is never something Ridwan wants posted. Set to False to go back
# to flag-only.
PER_IMAGE_KEYS = {"x_cover", "x_ba", "x_anno", "x_anno_graphic",
                  "x_problem", "x_benefit", "x_proof", "x_offer", "x_combo",
                  "ig_single", "x_glance"}
HOLD_MISMATCHED_CAPTIONS = True

try:
    from caption_fit import check as caption_fit_check
except ImportError:  # run from another cwd
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from caption_fit import check as caption_fit_check


def caption_text(record, key, variant_index=0):
    """Resolve a slot's caption_key against the harvested captions_full, falling
    back sensibly. Returns (text, source_tab, warning_or_None).

    variant_index selects WHICH single variant to use when the resolved value
    is a list of several standalone posts (e.g. harvested `.x-post` divs) —
    each calendar slot that shares a caption_key gets a DIFFERENT variant
    (index 0, 1, 2, ...) instead of every slot getting all of them joined
    together. Only THREAD_KEYS actually want the full list glued into one
    body (a real multi-tweet thread); everything else takes one variant."""
    full = record.get("captions_full", {})
    warn = None
    # Bug fixed 2026-07-29: this check used to live ONLY inside the
    # isinstance(v, list) branch below, so any caption harvested as a plain
    # string (e.g. tab-twitter-angles/tab-twitter-thread before the
    # harvest_content.py splitting fix, or any future skill that emits a
    # single string) silently skipped the length check entirely — that's how
    # 3 concatenated tweet variants and a 5-tweet thread script shipped to
    # the queue with zero warning. Now applies to the FINAL resolved text
    # regardless of whether the source was a string or a list.
    # The x_* store-template keys (added 2026-09-01) are listed explicitly so
    # a too-long store-template tweet gets the same 280-char flag every other
    # X caption gets. A prefix test would be tidier but would also catch a
    # future non-X key that merely starts with "x", so keep it explicit.
    X_KEYS = ("x", "x_singles", "x_angles", "x_thread",
              "x_showcase", "x_freeoffer", "x_niche", "x_buildpublic", "x_results",
              "x_glance",
              "x_carousel", "x_cover", "x_ba", "x_anno", "x_anno_graphic",
              "x_problem", "x_benefit", "x_proof", "x_offer", "x_combo")

    def check_len(text):
        nonlocal warn
        if key in X_KEYS and len(text) > X_CHAR_LIMIT:
            warn = (f"{warn + ' | ' if warn else ''}X caption is {len(text)} chars "
                    f"(> {X_CHAR_LIMIT}) — will be rejected by X for non-Premium accounts")

    def pick(v, src):
        nonlocal warn
        if isinstance(v, list):
            if not v:
                return "", warn
            if key in THREAD_KEYS:
                text = "\n\n".join(v)
                check_len(text)
                return text, warn
            idx = variant_index % len(v)
            if variant_index >= len(v):
                warn = (f"caption key '{key}' has only {len(v)} variant(s) but was "
                        f"requested for slot index {variant_index} — reusing variant {idx}")
            text = v[idx]
            check_len(text)
            return text, warn
        check_len(v)
        return v, warn

    if key in full:
        v = full[key]["text"]
        src = full[key].get("source_tab", key)
        text, warn = pick(v, src)
        return text, src, warn
    # fallbacks: x -> x_singles/x_angles; instagram -> linkedin; hook variants
    fallbacks = {
        "x": ["x", "x_singles", "x_angles"],
        "x_angles": ["x_angles", "x_singles", "x"],
        "x_singles": ["x_singles", "x", "x_angles"],
        "x_thread": ["x_thread", "x_angles", "x"],
        "instagram": ["instagram", "linkedin"],
        "linkedin": ["linkedin", "instagram"],
        # Store Template keys (2026-09-01). Each angle prefers its own written
        # caption, then degrades to the generic showcase angle, then to any
        # plain "x" pool — so a package missing one angle still ships a real
        # tweet rather than an empty row.
        "x_showcase": ["x_showcase", "x", "x_angles"],
        "x_niche": ["x_niche", "x_showcase", "x"],
        "x_buildpublic": ["x_buildpublic", "x_showcase", "x"],
        # mobile-strip / "full page at a glance" (2026-09-02). Degrades to the
        # showcase angle then the generic pool, so a package that forgot to
        # write this caption still ships a real tweet with the right image
        # rather than an empty row — the image is the mandatory part.
        "x_glance": ["x_glance", "x_showcase", "x"],
        # Deliberately NO cross-fallback between free-offer and results: a
        # paid client build must never inherit "I'll build you one free", and
        # a free-offer build must never inherit paid-client results framing.
        # Better an empty row that gets flagged than the wrong offer shipped.
        # CRO Fix keys (2026-09-27). Each prefers its own caption, then the
        # older x_angles pool, then plain x, so pre-2026-09-27 records still
        # produce a real tweet.
        # CHANGED 2026-09-28: per-image keys NO LONGER fall back to the shared
        # x_angles / x pool. That fallback is exactly how an annotated graphic
        # ended up with a before/after tweet. If nobody wrote a caption for
        # this image, the row comes out empty and held as Draft (see
        # PER_IMAGE_KEYS below). An empty flagged row is fixable; a wrong
        # caption that posts is not. The carousel caption may still fall back,
        # since a 3-image post can carry a general angle.
        "x_carousel": ["x_carousel", "x_angles", "x"],
        "x_cover": ["x_cover"],
        "x_ba": ["x_ba"],
        "x_anno": ["x_anno"],
        "x_anno_graphic": ["x_anno_graphic"],
        "x_problem": ["x_problem"],
        "x_benefit": ["x_benefit"],
        "x_proof": ["x_proof"],
        "x_offer": ["x_offer"],
        "x_combo": ["x_combo"],
        "ig_single": ["ig_single"],
        "x_freeoffer": ["x_freeoffer"],
        "x_results": ["x_results"],
    }
    for cand in fallbacks.get(key, [key]):
        if cand in full:
            v = full[cand]["text"]
            src = full[cand].get("source_tab", cand)
            text, warn = pick(v, src)
            return text, src, warn
    return "", key, None


def _slide_sort_key(path):
    """Natural sort for slideN.png so slide10 lands after slide2, not before."""
    m = re.search(r"slide[^0-9]*(\d+)", os.path.basename(path), re.I)
    return (int(m.group(1)) if m else 0, os.path.basename(path))


def resolve_assets(record, matchers):
    imgs = record.get("assets", {}).get("images", [])
    vid = record.get("assets", {}).get("video", [])
    vids = vid if isinstance(vid, list) else ([vid] if vid else [])
    allpaths = imgs + vids
    out = []
    for mt in matchers:
        if mt == "CAROUSEL_HTML":
            # Prefer the real exported slide PNGs when they exist on disk — a row
            # pointing at the companion .html has no media the feeders can host, so
            # it silently degrades to a text-only post (found 2026-08-11: every Tip
            # carousel row ever created had an empty asset_urls for this reason).
            # Falls back to the companion HTML when slides were never exported.
            slides = [p for p in allpaths
                      if "slide" in os.path.basename(p).lower()
                      and os.path.splitext(p)[1].lower() in (".png", ".jpg", ".jpeg")]
            slides.sort(key=lambda p: _slide_sort_key(p))
            out.extend(slides if slides else [record.get("content_system_folder", "")])
        elif mt == "ALL_SLIDES":
            out.extend([p for p in allpaths if "slide" in os.path.basename(p).lower()])
        else:
            matched = [p for p in allpaths if mt.lower() in os.path.basename(p).lower()]
            # Prefer a compressed "-x" sibling over its full-resolution original
            # when BOTH matched the same matcher (added 2026-09-02 with the
            # mobile-strip slot). build_mobile_strip.py only writes
            # "<name>-x.jpg" when the PNG clears ~4MB, so a matcher of
            # "mobile-strip" has to work whether or not the sibling exists — but
            # when it does exist, shipping the oversized original is exactly the
            # 2026-08-01 Bebemoss failure (Make's fetch limit rejected an 8.3MB
            # image and blocked that day's X post). "full-page-x" solves the same
            # problem by hardcoding the compressed name, at the cost of producing
            # an empty row when the sibling is absent; this is the general fix.
            def _stem(path):
                base = os.path.splitext(os.path.basename(path))[0]
                return base[:-2] if base.lower().endswith("-x") else base

            compressed = {_stem(p) for p in matched
                          if os.path.splitext(os.path.basename(p))[0].lower().endswith("-x")}
            if compressed:
                matched = [p for p in matched
                           if _stem(p) not in compressed
                           or os.path.splitext(os.path.basename(p))[0].lower().endswith("-x")]
            out.extend(matched)
    # de-dupe, preserve order
    seen, uniq = set(), []
    for p in out:
        if p and p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def find_open_week(slot, start_monday, taken_keys, local_tz, today, pin_to_start=False):
    """Per-slot week search (added 2026-08-24). Starting at start_monday, walk
    forward one week at a time and return the first week where this slot's
    resulting LOCAL date/time is both (a) not already in the past and (b) not
    already occupied by some OTHER item's row on the same platform at the same
    local date+time. This is what makes "current week first" real: every slot
    independently prefers the soonest open week instead of every item in one
    assembly run being flattened onto the same fixed future week.

    pin_to_start=True (used when --week-monday is passed explicitly, e.g. for
    a deliberate backfill) skips the search entirely and uses start_monday as-is
    — an explicit override should be honored literally, not second-guessed."""
    et = ZoneInfo(ET_TZ)
    local = ZoneInfo(local_tz)
    hh, mm = (int(x) for x in slot["time"].split(":"))
    monday = start_monday
    for _ in range(52):  # hard safety cap; should never actually take this long
        sched = monday + timedelta(days=slot["dow"])
        et_dt = datetime(sched.year, sched.month, sched.day, hh, mm, tzinfo=et)
        local_dt = et_dt.astimezone(local)
        local_date = local_dt.date().isoformat()
        local_time = local_dt.strftime("%H:%M")
        key = (slot["platform"], local_date, local_time)
        if pin_to_start or (sched >= today and key not in taken_keys):
            return sched, local_dt, local_date, local_time
        monday += timedelta(days=7)
    return sched, local_dt, local_date, local_time  # pragma: no cover — safety-cap fallback


def _linkedin_day_free(candidate_date_iso, linkedin_dates_taken):
    return candidate_date_iso not in linkedin_dates_taken


def _find_bump_target(slot, after_monday, taken_keys, linkedin_dates_taken, local_tz, today):
    """Like find_open_week, but for re-homing an EXISTING displaced row: walk
    forward week by week from after_monday (not the search-then-place logic
    find_open_week uses for brand-new content) until the same weekday+time
    is both free (no same-platform/date/time collision) and, for LinkedIn,
    the candidate DATE has no other LinkedIn row on it yet (the hard 1/day
    cap) — a check find_open_week itself does not perform, so it's done
    explicitly here for the row this change is responsible for moving."""
    et = ZoneInfo(ET_TZ)
    local = ZoneInfo(local_tz)
    hh, mm = (int(x) for x in slot["time"].split(":"))
    monday = after_monday
    for _ in range(52):
        sched = monday + timedelta(days=slot["dow"])
        et_dt = datetime(sched.year, sched.month, sched.day, hh, mm, tzinfo=et)
        local_dt = et_dt.astimezone(local)
        local_date = local_dt.date().isoformat()
        local_time = local_dt.strftime("%H:%M")
        key = (slot["platform"], local_date, local_time)
        ok = sched >= today and key not in taken_keys
        if ok and slot["platform"] == "LinkedIn":
            ok = _linkedin_day_free(local_date, linkedin_dates_taken)
        if ok:
            return local_date, local_time
        monday += timedelta(days=7)
    return local_date, local_time  # pragma: no cover — safety-cap fallback


def build_rows(record, week_monday, local_tz=DEFAULT_LOCAL_TZ, taken_keys=None, pin_to_start=False,
                known_rows=None, overwrite_this_week=True):
    stream = record.get("type", "")
    slots = CALENDAR.get(stream)
    if slots is None:
        return [], f"no calendar slots defined for stream '{stream}'", []
    item_id = record.get("pipeline_item_id", "")
    qa_status = record.get("qa_status", "")
    folder = record.get("content_system_folder", "")
    taken_keys = taken_keys if taken_keys is not None else set()
    known_rows = known_rows if known_rows is not None else []
    today = date.today()
    current_week_start = current_monday(today)
    current_week_end = current_week_start + timedelta(days=6)
    linkedin_dates_taken = {r["scheduled_date"] for r in known_rows
                             if r.get("platform") == "LinkedIn" and r.get("scheduled_date")}
    used_bump_ids = set()
    rows, warnings, bumps = [], [], []
    variant_seen = {}  # caption_key -> how many slots have already drawn from it
    for slot in slots:
        target_week = week_monday
        displaced = None

        if overwrite_this_week and not pin_to_start:
            hh, mm = (int(x) for x in slot["time"].split(":"))
            natural_sched = current_week_start + timedelta(days=slot["dow"])
            if natural_sched >= today:
                et_dt = datetime(natural_sched.year, natural_sched.month, natural_sched.day, hh, mm, tzinfo=ZoneInfo(ET_TZ))
                natural_local_dt = et_dt.astimezone(ZoneInfo(local_tz))
                natural_local_date = natural_local_dt.date().isoformat()
                natural_local_time = natural_local_dt.strftime("%H:%M")
                for r in known_rows:
                    if (r.get("post_id") not in used_bump_ids
                            and r.get("stream") == stream
                            and r.get("platform") == slot["platform"]
                            and r.get("scheduled_time_local") == natural_local_time
                            and (r.get("status") or "").strip().lower() != "posted"):
                        try:
                            rdate = datetime.strptime(r.get("scheduled_date", ""), "%Y-%m-%d").date()
                        except ValueError:
                            continue
                        if current_week_start <= rdate <= current_week_end:
                            displaced = r
                            break
                if displaced is not None:
                    used_bump_ids.add(displaced["post_id"])
                    target_week = current_week_start
                    # free the slot the new row is about to take
                    taken_keys.discard((slot["platform"], displaced["scheduled_date"], displaced["scheduled_time_local"]))
                    if slot["platform"] == "LinkedIn":
                        linkedin_dates_taken.discard(displaced["scheduled_date"])

        sched, local_dt, local_date, local_time = find_open_week(
            slot, target_week, taken_keys, local_tz, today, pin_to_start=pin_to_start)
        # Reserve this key immediately so two slots WITHIN the same record
        # (e.g. two Twitter singles that happen to share a time) can't also
        # collide with each other, not just with rows already in the queue.
        taken_keys.add((slot["platform"], local_date, local_time))
        if slot["platform"] == "LinkedIn":
            linkedin_dates_taken.add(local_date)

        if displaced is not None:
            old_date, old_time = displaced["scheduled_date"], displaced["scheduled_time_local"]
            new_date, new_time = _find_bump_target(
                slot, current_week_start + timedelta(days=7), taken_keys, linkedin_dates_taken, local_tz, today)
            taken_keys.add((slot["platform"], new_date, new_time))
            if slot["platform"] == "LinkedIn":
                linkedin_dates_taken.add(new_date)
            bumps.append({
                "post_id": displaced["post_id"],
                "stream": stream,
                "platform": slot["platform"],
                "old_date": old_date, "old_time": old_time,
                "new_date": new_date, "new_time": new_time,
                "row_number": displaced.get("row_number"),  # set only for a live-only row
                "local_row": displaced.get("_local_row"),   # set only for a row backed by a local queue.json dict
            })
            if displaced.get("_local_row") is not None:
                displaced["_local_row"]["scheduled_date"] = new_date
                displaced["_local_row"]["scheduled_time_local"] = new_time

        assets = resolve_assets(record, slot["assets"])
        ckey = slot["caption_key"]
        vidx = variant_seen.get(ckey, 0)
        variant_seen[ckey] = vidx + 1
        cap, src, cap_warn = caption_text(record, ckey, variant_index=vidx)
        tag = PLATFORM_TAG[slot["platform"]]
        # id uses the tz-independent ET date+time so it stays stable
        post_id = f"{item_id}-{sched.strftime('%Y%m%d')}-{tag}-{slot['time'].replace(':','')}"
        if not assets:
            warnings.append(f"{slot['platform']} {slot['angle']}: no asset matched {slot['assets']}")
        if not cap:
            warnings.append(f"{slot['platform']} {slot['angle']}: no caption for key '{ckey}'")
        if cap_warn:
            warnings.append(f"{slot['platform']} {slot['angle']}: {cap_warn}")
        fit_reasons = caption_fit_check(cap, "; ".join(assets), slot["platform"])
        if not cap and ckey in PER_IMAGE_KEYS:
            fit_reasons.append(f"caption-fit: no caption was written for this image (key '{ckey}')")
        row_status = "Ready"
        row_qa = qa_status
        if fit_reasons:
            warnings.append(f"{slot['platform']} {slot['angle']}: " + "; ".join(fit_reasons))
            row_qa = ("Needs Review: " + "; ".join(fit_reasons)
                      + (("; " + qa_status.replace("Needs Review: ", "", 1)) if qa_status and qa_status != "Pass" else ""))
            if HOLD_MISMATCHED_CAPTIONS:
                row_status = "Draft"
        rows.append({
            "post_id": post_id,
            "pipeline_item_id": item_id,
            "stream": stream,
            "platform": slot["platform"],
            "scheduled_date": local_date,
            "scheduled_time_local": local_time,
            "intended_et": slot["time"] + " ET",
            "asset_paths": "; ".join(assets),
            "caption": cap,
            "caption_source_tab": src,
            "status": row_status,
            "qa_status": row_qa,
            "posted_at": "",
            "content_system_folder": folder,
            # Pre-escaped JSON string literal (INCLUDING its surrounding quotes).
            # Make's HTTP body drops this in verbatim as the caption value, so a
            # caption containing newlines, quotes or backslashes can never break
            # the JSON body. Python's json.dumps does the escaping correctly —
            # far more reliable than trying to escape inside a Make expression.
            "caption_json": json.dumps(cap, ensure_ascii=False),
            "asset_urls": "",
        })
    return rows, "; ".join(warnings), bumps


def load_queue(qpath):
    if os.path.exists(qpath):
        with open(qpath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"meta": {"created": datetime.now(timezone.utc).isoformat()}, "rows": []}


def save_queue(queue, qpath):
    queue["meta"]["updated"] = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(qpath), exist_ok=True)
    with open(qpath, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    # CSV mirror alongside
    csvpath = os.path.splitext(qpath)[0] + ".csv"
    with open(csvpath, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in queue["rows"]:
            w.writerow({k: r.get(k, "") for k in COLUMNS})
    return csvpath


def merge_rows(queue, new_rows):
    """Idempotent by post_id: skip rows already present (don't clobber a row
    Ridwan may have flipped to Ready/Posted)."""
    existing = {r["post_id"] for r in queue["rows"]}
    added, skipped = 0, 0
    for r in new_rows:
        if r["post_id"] in existing:
            skipped += 1
            continue
        queue["rows"].append(r)
        added += 1
    return added, skipped


def main():
    ap = argparse.ArgumentParser(description="Expand a QA'd harvest record into per-post Ready queue rows.")
    ap.add_argument("record")
    ap.add_argument("--week-monday", default=None, help="Monday (YYYY-MM-DD) of the POSTING week; default = next Monday.")
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--queue", default=None)
    ap.add_argument("--local-tz", default=DEFAULT_LOCAL_TZ,
                    help="Timezone the sheet times are written in — MUST match the Make org timezone (default Africa/Lagos). The ET calendar is converted into this tz.")
    ap.add_argument("--no-overwrite", action="store_true",
                    help="Disable the 2026-09-19 'this week overwrite' behavior — fall back to always finding a fresh open slot, never displacing an existing row.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would be built/bumped without writing queue.json, the CSV mirror, or the live Sheet.")
    args = ap.parse_args()

    rec_path = os.path.abspath(args.record)
    with open(rec_path, "r", encoding="utf-8") as f:
        record = json.load(f)

    root = args.project_root
    if not root:
        d = os.path.dirname(rec_path)
        while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
            d = os.path.dirname(d)
        root = d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.dirname(rec_path)
    root = os.path.abspath(root)

    qpath = args.queue or os.path.join(root, "outputs", "distribution-queue", "queue.json")
    queue = load_queue(qpath)

    pin_to_start = bool(args.week_monday)
    if args.week_monday:
        wm = datetime.strptime(args.week_monday, "%Y-%m-%d").date()
    else:
        # Fixed 2026-08-24 (Ridwan's call): used to always be next_monday(),
        # which flattens every item assembled in one run onto the same single
        # future week. Now anchors to the CURRENT week and find_open_week()
        # walks forward per-slot only when needed (past date or collision).
        wm = current_monday()

    # Live-Sheet read (2026-09-19): the authoritative view of what's really
    # occupying "this week" — Ridwan's status flips and any live-only
    # reschedules never make it back into local queue.json otherwise.
    # Best-effort: falls back to local-only on any failure, see fetch_live_rows().
    token, live_rows = fetch_live_rows(root)
    live_by_id = {r["post_id"]: r for r in live_rows if r["post_id"]}

    # known_rows = local queue rows (tagged with a back-reference to the actual
    # dict so a bump can mutate queue.json in place) UNION live-only rows (a
    # row that exists live but never made it into local queue.json — rare,
    # but the reschedule webhook and one-off manual repairs can create one).
    known_rows = []
    local_ids = set()
    for r in queue.get("rows", []):
        local_ids.add(r.get("post_id"))
        live_counterpart = live_by_id.get(r.get("post_id"))
        known_rows.append({
            "post_id": r.get("post_id"),
            "stream": r.get("stream"),
            "platform": r.get("platform"),
            # prefer the LIVE date/time/status when a live counterpart exists —
            # live is ahead of local per project convention (Ridwan edits there).
            "scheduled_date": (live_counterpart or r).get("scheduled_date"),
            "scheduled_time_local": (live_counterpart or r).get("scheduled_time_local"),
            "status": (live_counterpart or r).get("status", r.get("status")),
            "row_number": live_counterpart.get("row_number") if live_counterpart else None,
            "_local_row": r,
        })
    for r in live_rows:
        if r["post_id"] and r["post_id"] not in local_ids:
            known_rows.append({**r, "_local_row": None})

    # Collision set: every (platform, scheduled_date, scheduled_time_local)
    # already sitting in the queue (local UNION live), regardless of which
    # item it belongs to — this is what lets find_open_week() skip a slot
    # that's already spoken for.
    taken_keys = {(r.get("platform"), r.get("scheduled_date"), r.get("scheduled_time_local"))
                  for r in known_rows}

    rows, warn, bumps = build_rows(record, wm, local_tz=args.local_tz,
                                    taken_keys=taken_keys, pin_to_start=pin_to_start,
                                    known_rows=known_rows, overwrite_this_week=not args.no_overwrite)
    added, skipped = (0, 0) if args.dry_run else merge_rows(queue, rows)
    csvpath = None
    if not args.dry_run:
        csvpath = save_queue(queue, qpath)
        if bumps and token:
            applied = push_bump_updates(token, bumps)
            print(f"[sheet] pushed {len(applied)}/{len(bumps)} bump(s) to the live Sheet")

    weeks_used = sorted({r["scheduled_date"] for r in rows})
    print(f"[sheet] stream={record.get('type')} search-anchor={wm.isoformat()} "
          f"| rows built={len(rows)} added={added} skipped(existing)={skipped}"
          f"{' (DRY RUN — nothing written)' if args.dry_run else ''}")
    print(f"[sheet] scheduled dates actually used: {', '.join(weeks_used) if weeks_used else '(none)'}")
    by_plat = {}
    for r in rows:
        by_plat[r["platform"]] = by_plat.get(r["platform"], 0) + 1
    print("[sheet] per-platform:", ", ".join(f"{k}:{v}" for k, v in sorted(by_plat.items())))
    if bumps:
        print(f"[sheet] this-week overwrites: {len(bumps)}")
        for b in bumps:
            where = "live+local" if b["row_number"] else ("local-only" if b["local_row"] is not None else "live-only")
            print(f"  bumped {b['post_id']} ({b['stream']}/{b['platform']}, {where}): "
                  f"{b['old_date']} {b['old_time']} -> {b['new_date']} {b['new_time']}")
    if warn:
        print("[sheet] WARNINGS:", warn)
    print(f"[sheet] queue: {qpath}")
    if csvpath:
        print(f"[sheet] csv mirror: {csvpath}")
    print(f"[sheet] total rows in queue now: {len(queue['rows'])}")


if __name__ == "__main__":
    main()

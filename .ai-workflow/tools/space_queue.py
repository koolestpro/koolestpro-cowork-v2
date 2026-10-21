#!/usr/bin/env python3
"""space_queue.py - re-space the pending Distribution Queue so variety is enforced.

Added 2026-10-08 (Ridwan's instruction). Rules, in priority order:

 1. BRAND COOLDOWN. The same brand/site (or the same Tips topic) never posts on
    any platform within GAP_MIN days (default 5) of another post of that brand;
    GAP_PREF (default 7) is tried first. The only exception is a hero bundle:
    the same item going out on the same day on LinkedIn + X (+ Instagram).
 2. NO BACK-TO-BACK SAME STREAM. Consecutive X slots prefer a different stream
    (CRO Fix / Static Ad / Template Showcase / Tip ...).
 3. DAILY SHAPE. One hero item per day (LinkedIn 14:00 + its best X row 14:00,
    + Instagram 17:00 with --include-ig). X fills up to --target-x per day
    (slots 14:00, 18:00, 23:00 Lagos). LinkedIn max 1/day.
 3b. SHOWCASE ASSET PRIORITY (2026-10-10, Ridwan). For Template Showcase /
    Store Template rows, the lead assets (cover video, IG carousel, cover image,
    preview, mobile strip) always go before the same page's secondary cuts (laptop video,
    mobile video, full page). The 4 leads per page (2026-10-10): cover video,
    IG carousel, preview, mobile strip. Combined with the brand cooldown,
    this means the day after a brand's cover video we show ANOTHER brand's
    cover, never the laptop or mobile version of the same page. Secondary cuts
    only fill slots nothing else can.
 3c. VARIANTS BOARD GOES FIRST (2026-10-11, Ridwan). A CRO Fix "variants board" X row
    (assets contain "variants-board": the neutral A/B/C/D debate post) is never a
    free-floating X extra. It rides with its own item's hero: placed on the DAY
    BEFORE the hero (18:00, then 23:00, then 14:00) so the debate runs before the
    carousel reveal, or, if that day is gone/full, on the hero day ahead of the
    hero's X row (teaser 14:00, carousel X 18:00). Teaser + hero of the same item
    within one day are a bundle, not a brand-cooldown breach.
 4. NEVER FILL A SLOT BY BREAKING A RULE. If nothing qualifies the slot stays
    empty and is reported as a supply gap for the new content lanes to fill.

Only rows with status Ready (and not Posted) on Twitter/LinkedIn (Instagram only
with --include-ig) are moved. Draft rows, Posted rows and statuses are never
touched. Only scheduled_date / scheduled_time_local change.

Usage:
  python3 space_queue.py --project-root . --dry-run     # show the plan
  python3 space_queue.py --project-root .               # apply (local + live Sheet)
"""
import argparse, csv, datetime as dt, json, re, sys, urllib.parse
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import populate_sheet as ps  # noqa: E402  (env loading, OAuth token, sheet ids)

X_SLOTS = ["14:00", "18:00", "23:00"]
LI_SLOT = "14:00"
IG_SLOT = "17:00"
LAGOS = dt.timezone(dt.timedelta(hours=1))


def parse_date(s):
    s = (s or "").strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return dt.date(int(m[3]), int(m[1]), int(m[2]))
    return None


def brand_of(r):
    pid = r["pipeline_item_id"] or r["post_id"]
    if r["stream"] == "Tip":
        return "tip:" + pid
    m = re.match(r"(?:cro-fix|static-ad|template[ -]?showcase)-([a-z0-9]+)[_-]", pid)
    if m:
        return m.group(1)
    return "misc:" + pid


def asset_rank(r):
    """0 = lead showcase asset or any non-showcase row, 1 = secondary cut of a page."""
    if r["stream"] not in ("Template Showcase", "Store Template"):
        return 0
    a = (r.get("assets") or "").lower()
    if any(k in a for k in (" laptop.mp4", " mobile.mp4", "-full-page", "-full-mosaic", " full.png")):
        return 1
    return 0


def is_teaser(r):
    return "variants-board" in (r.get("assets") or "").lower()


def pick_key(r):
    return (asset_rank(r), r["orig"], r["post_id"])


def ig_kind(urls):
    """Instagram only posts carousels (2-10 images) and single videos (Make routes 310-317, 304-306).
    Single images, mixed image+video, empty or oversize rows can never post."""
    u = [x for x in re.split(r";\s*", urls or "") if x.strip()]
    if not u:
        return "no-url"
    vid = [x for x in u if ".mp4" in x.lower()]
    if vid and len(vid) == len(u):
        return "video" if len(u) == 1 else "multi-video"
    if vid:
        return "mixed"
    if len(u) == 1:
        return "single-image"
    return "carousel" if len(u) <= 10 else "too-many"


def fetch(root):
    env = ps.load_env(root)
    token = ps.get_live_sheet_token(env)
    vals = ps._http_json(
        f"https://sheets.googleapis.com/v4/spreadsheets/{ps.SHEET_ID}/values/"
        f"{urllib.parse.quote(ps.SHEET_TAB)}!A2:P5000",
        headers={"Authorization": f"Bearer {token}"}, method="GET")
    rows = []
    for i, v in enumerate(vals.get("values", []), start=2):
        v = v + [""] * (16 - len(v))
        rows.append(dict(row_number=i, post_id=v[0], pipeline_item_id=v[1], stream=v[2],
                         platform=v[3], date=parse_date(v[4]), time=v[5], assets=v[7],
                         status=v[10], qa=v[11], posted_at=v[12], urls=v[15]))
    return token, rows


class Plan:
    def __init__(self, history):
        self.entries = list(history)  # (date, brand, item)
        self.teasers = set()          # (date, item) of variants-board posts (rule 3c)

    def brand_ok(self, d, brand, item, gap, same_day_bundle_ok):
        for (ed, eb, ei) in self.entries:
            if eb != brand:
                continue
            if same_day_bundle_ok and ei == item and ed == d:
                continue
            if ei == item and (ed, ei) in self.teasers and abs((d - ed).days) <= 1:
                continue  # its own variants board the day before: one bundle
            if abs((d - ed).days) < gap:
                return False
        return True

    def add(self, d, brand, item):
        self.entries.append((d, brand, item))


def build_plan(rows, today, now_local, a):
    posted = [r for r in rows if r["status"] == "Posted" and r["date"]]
    history = []
    for r in posted:
        d = parse_date(r["posted_at"]) or r["date"]
        if d >= today - dt.timedelta(days=a.gap_pref + 2):
            history.append((d, brand_of(r), r["pipeline_item_id"] or r["post_id"]))
    plats = {"Twitter", "LinkedIn"} | ({"Instagram"} if a.include_ig else set())
    movable = [r for r in rows if r["status"] == "Ready" and r["platform"] in plats
               and not (r["platform"] == "Instagram" and (ig_kind(r["urls"]) not in ("video", "carousel")
                                                        or r["stream"] == "Tip"))]
    for r in movable:
        r["brand"] = brand_of(r)
        r["item"] = r["pipeline_item_id"] or r["post_id"]
        r["orig"] = r["date"] or today
        r["n_assets"] = len([x for x in (r["assets"] or "").split(";") if x.strip()])
    pending = {r["post_id"]: r for r in movable}
    plan = Plan(history)
    assign = {}   # post_id -> (date, time)
    day_log = []
    gaps = []

    def pool(platform):
        # variants-board teasers only move with their hero (rule 3c)
        return [r for r in pending.values() if r["platform"] == platform and r["post_id"] not in assign
                and not is_teaser(r)]

    def teasers_for(item):
        return [r for r in pending.values() if is_teaser(r) and r["item"] == item and r["post_id"] not in assign]

    x_used = defaultdict(set)   # date -> X times already assigned (rule 3c lookback)
    log_by_date = {}

    def place_teaser(tz, day, day_log_entry, prefer=("18:00", "23:00", "14:00"), free=None):
        for t in prefer:
            if t in x_used[day] or (free is not None and t not in free):
                continue
            if day == today and dt.datetime.combine(day, dt.datetime.strptime(t, "%H:%M").time(), LAGOS) < now_local + dt.timedelta(minutes=60):
                continue
            assign[tz["post_id"]] = (day, t)
            x_used[day].add(t)
            plan.add(day, tz["brand"], tz["item"])
            plan.teasers.add((day, tz["item"]))
            day_log_entry["x"].append((t, tz["brand"], tz["stream"], "teaser"))
            return t
        return None

    last_x_stream = None
    last_ig_stream = None
    d = today
    for _ in range(a.horizon):
        slots_x = [t for t in X_SLOTS
                   if not (d == today and dt.datetime.combine(d, dt.datetime.strptime(t, "%H:%M").time(), LAGOS)
                           < now_local + dt.timedelta(minutes=60))]
        if not slots_x and d == today:
            d += dt.timedelta(days=1)
            continue
        today_log = {"date": d, "hero": None, "x": [], "ig": None}
        used_brands = set()
        # ---- hero (LinkedIn + its best X + optional IG)
        hero = None
        li_ok_today = d > today or dt.datetime.combine(d, dt.datetime.strptime(LI_SLOT, "%H:%M").time(), LAGOS) >= now_local + dt.timedelta(minutes=60)
        deferred = set()
        if li_ok_today:
            for gap in (a.gap_pref, a.gap_min):
                cands = sorted(pool("LinkedIn"), key=pick_key)
                cands = [r for r in cands if plan.brand_ok(d, r["brand"], r["item"], gap, False)
                         and r["item"] not in deferred]
                for c in cands:
                    tzs = teasers_for(c["item"])
                    prev = d - dt.timedelta(days=1)
                    if all(prev >= today and prev in log_by_date
                           and place_teaser(tz, prev, log_by_date[prev]) for tz in tzs):
                        hero = c
                        break
                    # rule 3c: the board can't go out the day before, so it opens today
                    # and this hero waits for tomorrow (it never goes before its board)
                    for tz in teasers_for(c["item"]):
                        t = place_teaser(tz, d, today_log, free=slots_x)
                        if t:
                            slots_x = [x for x in slots_x if x != t]
                            used_brands.add(c["brand"])
                    deferred.add(c["item"])
                if hero:
                    break
        if hero:
            assign[hero["post_id"]] = (d, LI_SLOT)
            plan.add(d, hero["brand"], hero["item"])
            used_brands.add(hero["brand"])
            today_log["hero"] = (hero["brand"], hero["stream"])
            xs = sorted([r for r in pool("Twitter") if r["item"] == hero["item"]],
                        key=lambda r: (-r["n_assets"], r["orig"], r["post_id"]))
            if xs and "14:00" in slots_x:
                assign[xs[0]["post_id"]] = (d, "14:00")
                x_used[d].add("14:00")
                slots_x = [t for t in slots_x if t != "14:00"]
                today_log["x"].append(("14:00", xs[0]["brand"], xs[0]["stream"], "hero"))
                last_x_stream = xs[0]["stream"]
            if a.include_ig:
                ig = sorted([r for r in pool("Instagram") if r["item"] == hero["item"]],
                            key=lambda r: (-r["n_assets"], r["orig"]))
                if ig:
                    assign[ig[0]["post_id"]] = (d, IG_SLOT)
        # ---- X extras
        reserved = {r["item"] for r in pool("LinkedIn")}  # keep their X rows for the hero bundle
        want = a.target_x - sum(1 for _ in today_log["x"])
        for t in slots_x[:max(want, 0)]:
            if t in x_used[d]:
                continue
            picked = None
            for gap in (a.gap_pref, a.gap_min):
                for want_diff in (True, False):
                    cands = sorted(pool("Twitter"), key=pick_key)
                    cands = [r for r in cands
                             if r["brand"] not in used_brands and r["item"] not in reserved
                             and plan.brand_ok(d, r["brand"], r["item"], gap, False)
                             and (not want_diff or r["stream"] != last_x_stream)]
                    if cands:
                        picked = cands[0]
                        break
                if picked:
                    break
            if picked:
                assign[picked["post_id"]] = (d, t)
                x_used[d].add(t)
                plan.add(d, picked["brand"], picked["item"])
                used_brands.add(picked["brand"])
                last_x_stream = picked["stream"]
                today_log["x"].append((t, picked["brand"], picked["stream"], ""))
            else:
                gaps.append((d, t))
        # ---- Instagram: one carousel/video a day at 17:00 (hero partner already placed above)
        if a.include_ig:
            ig_time_ok = d > today or dt.datetime.combine(d, dt.datetime.strptime(IG_SLOT, "%H:%M").time(), LAGOS) >= now_local + dt.timedelta(minutes=60)
            has_ig = any(r["platform"] == "Instagram" and assign.get(r["post_id"], (None,))[0] == d for r in movable)
            if ig_time_ok and not has_ig:
                picked = None
                for gap in (a.gap_pref, a.gap_min):
                    for want_diff in (True, False):
                        cands = sorted(pool("Instagram"), key=pick_key)
                        cands = [r for r in cands
                                 if r["brand"] not in used_brands
                                 and plan.brand_ok(d, r["brand"], r["item"], gap, False)
                                 and (not want_diff or r["stream"] != last_ig_stream)]
                        if cands:
                            picked = cands[0]
                            break
                    if picked:
                        break
                if picked:
                    assign[picked["post_id"]] = (d, IG_SLOT)
                    plan.add(d, picked["brand"], picked["item"])
                    used_brands.add(picked["brand"])
                    today_log["ig"] = (picked["brand"], picked["stream"], ig_kind(picked["urls"]))
                    last_ig_stream = picked["stream"]
                else:
                    gaps.append((d, "IG"))
            elif has_ig:
                igr = [r for r in movable if r["platform"] == "Instagram" and assign.get(r["post_id"], (None,))[0] == d][0]
                today_log["ig"] = (igr["brand"], igr["stream"], ig_kind(igr["urls"]))
                last_ig_stream = igr["stream"]
        day_log.append(today_log)
        log_by_date[d] = today_log
        d += dt.timedelta(days=1)
        if not any(r["post_id"] not in assign for r in pending.values()):
            break
    unplaced = [r for r in pending.values() if r["post_id"] not in assign]
    return movable, assign, day_log, gaps, unplaced, history


def verify(movable, assign, history, a):
    """Independent check of the final plan against the hard rule."""
    ents = [(h[0], h[1], h[2], False, False) for h in history]
    for r in movable:
        if r["post_id"] in assign:
            ents.append((assign[r["post_id"]][0], r["brand"], r["item"], True, is_teaser(r)))
    viol = []
    by = defaultdict(list)
    for e in ents:
        by[e[1]].append(e)
    for b, es in by.items():
        es.sort(key=lambda e: e[0])
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                if not (es[i][3] or es[j][3]):
                    continue  # both already posted: history, not ours to judge
                if es[i][2] == es[j][2] and es[i][0] == es[j][0]:
                    continue
                if es[i][2] == es[j][2] and (es[i][4] or es[j][4]) and abs((es[j][0] - es[i][0]).days) <= 1:
                    continue  # rule 3c: variants board + its hero are one bundle
                if (es[j][0] - es[i][0]).days < a.gap_min:
                    viol.append((b, es[i][0], es[j][0]))
    return viol


def apply(root, token, movable, assign, plat_rows):
    root = Path(root)
    qdir = root / "outputs" / "distribution-queue"
    stamp = dt.datetime.now(LAGOS).strftime("%Y%m%d-%H%M")
    changes = []
    for r in movable:
        if r["post_id"] not in assign:
            continue
        nd, nt = assign[r["post_id"]]
        if r["date"] == nd and r["time"].lstrip("0") == nt.lstrip("0"):
            continue
        changes.append(dict(post_id=r["post_id"], row_number=r["row_number"],
                            old=[str(r["date"]), r["time"]], new=[nd.isoformat(), nt]))
    (qdir / f"space_backup_{stamp}.json").write_text(json.dumps(changes, indent=1))
    # live Sheet: targeted E:F updates only
    if changes:
        body = {"valueInputOption": "USER_ENTERED",
                "data": [{"range": f"{ps.SHEET_TAB}!E{c['row_number']}:F{c['row_number']}",
                          "values": [c["new"]]} for c in changes]}
        ps._http_json(f"https://sheets.googleapis.com/v4/spreadsheets/{ps.SHEET_ID}/values:batchUpdate",
                      data=body, headers={"Authorization": f"Bearer {token}",
                                          "Content-Type": "application/json"}, method="POST")
    # local mirror
    byid = {c["post_id"]: c for c in changes}
    qj = qdir / "queue.json"
    if qj.exists():
        q = json.loads(qj.read_text())
        for row in q["rows"]:
            c = byid.get(row["post_id"])
            if c:
                row["scheduled_date"], row["scheduled_time_local"] = c["new"]
        qj.write_text(json.dumps(q, indent=2, ensure_ascii=False))
    qc = qdir / "queue.csv"
    if qc.exists():
        with open(qc, newline="", encoding="utf-8") as f:
            rd = list(csv.reader(f))
        hdr = rd[0]
        i_id, i_d, i_t = hdr.index("post_id"), hdr.index("scheduled_date"), hdr.index("scheduled_time_local")
        for row in rd[1:]:
            c = byid.get(row[i_id])
            if c:
                row[i_d], row[i_t] = c["new"]
        with open(qc, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rd)
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--gap-min", type=int, default=5)
    ap.add_argument("--gap-pref", type=int, default=7)
    ap.add_argument("--target-x", type=int, default=3)
    ap.add_argument("--horizon", type=int, default=45)
    ap.add_argument("--include-ig", action="store_true")
    ap.add_argument("--retire-tips-ig", action="store_true",
                    help="set status Retired on every Ready Instagram Tip row (Ridwan 2026-10-08: old Tips are not wanted)")
    ap.add_argument("--retire-dead-ig", action="store_true",
                    help="set Retired on Ready, unposted Instagram rows that can never publish (single-image/no-url/mixed/too-many) and are past-dated")
    a = ap.parse_args()
    now_local = dt.datetime.now(LAGOS)
    today = now_local.date()
    token, rows = fetch(a.project_root)
    if a.retire_tips_ig or a.retire_dead_ig:
        if a.retire_dead_ig:
            tgt = [r for r in rows if r["platform"] == "Instagram" and r["status"] == "Ready"
                   and ig_kind(r["urls"]) not in ("video", "carousel") and r["date"] < today]
        else:
            tgt = [r for r in rows if r["platform"] == "Instagram" and r["stream"] == "Tip" and r["status"] == "Ready"]
        for r in tgt:
            print("RETIRE", r["date"], r["post_id"][:70])
        if not a.dry_run and tgt:
            qdir = Path(a.project_root) / "outputs" / "distribution-queue"
            stamp = now_local.strftime("%Y%m%d-%H%M")
            (qdir / f"retire_backup_{stamp}.json").write_text(json.dumps(
                [dict(post_id=r["post_id"], row_number=r["row_number"], old_status="Ready") for r in tgt], indent=1))
            ps._http_json(f"https://sheets.googleapis.com/v4/spreadsheets/{ps.SHEET_ID}/values:batchUpdate",
                          data={"valueInputOption": "USER_ENTERED",
                                "data": [{"range": f"{ps.SHEET_TAB}!K{r['row_number']}", "values": [["Retired"]]} for r in tgt]},
                          headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
            ids = {r["post_id"] for r in tgt}
            qj = qdir / "queue.json"
            if qj.exists():
                q = json.loads(qj.read_text())
                for row in q["rows"]:
                    if row["post_id"] in ids:
                        row["status"] = "Retired"
                qj.write_text(json.dumps(q, indent=2, ensure_ascii=False))
            print(f"retired {len(tgt)} Instagram Tip rows (backup written)")
        return
    movable, assign, day_log, gaps, unplaced, history = build_plan(rows, today, now_local, a)
    print(f"today {today} | movable Ready rows {len(movable)} | placed {len(assign)} | unplaced {len(unplaced)}")
    for dl in day_log:
        h = dl["hero"]
        xs = " | ".join(f"{t} {b}/{s[:6]}{' *' if tag else ''}" for t, b, s, tag in dl["x"])
        ig = dl.get("ig")
        igs = f" | IG {ig[0]}/{ig[1][:6]}/{ig[2]}" if ig else ""
        if h or dl["x"] or ig:
            print(f"{dl['date']} {dl['date'].strftime('%a')}  hero: {(h[0]+'/'+h[1]) if h else '-':28} X: {xs}{igs}")
    print(f"\nempty X slots inside the window (supply gap): {len(gaps)}")
    viol = verify(movable, assign, history, a)
    print(f"brand-gap violations after plan: {len(viol)} {viol[:5]}")
    for r in unplaced:
        print("UNPLACED", r["platform"], r["brand"], r["post_id"][-30:])
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return
    ch = apply(a.project_root, token, movable, assign, rows)
    print(f"\napplied {len(ch)} date/time changes to the live Sheet and local queue; backup written.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Two-way link between the content pipeline and the cold email Sheet (Ridwan, 2026-10-26).

  pull  Writes outreach/scrapers/state/contactable_stores.json: every store whose lead in the Sheet has a
        sendable, confirmed email (email_status valid, or catch-all when SEND_TO_CATCH_ALL), is not Lost,
        Bounced, Unsubscribed or Won, and is not flagged [UNCONFIRMED RECIPIENT]. Content tasks only design
        or post real stores that are on this list. No email addresses are stored, only domains.
  push  Sends every outreach/redesign-hooks.json entry with status "ready" and no pushedAt to the Sheet
        (Api.gs set_redesign), so that lead's emails are written around the redesign and sent first.

Usage (project root):  python3 outreach/scrapers/redesign_sync.py            # pull, then push
                       python3 outreach/scrapers/redesign_sync.py pull
                       python3 outreach/scrapers/redesign_sync.py push --dry-run
Needs OUTREACH_API_URL and OUTREACH_API_TOKEN in .env or cold-email-app/.env (same as directory_scrape.py).
Run by scripts/mac-catchup.sh every hour.
If the Sheet's web app has not been redeployed with the 2026-10-26 Api.gs yet, pull falls back to the
older `leads` action (same filter, done here) and push reports that set_redesign is not live yet.
"""
import json, sys, ssl, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STATE = HERE / "state"
OUT = STATE / "contactable_stores.json"
HOOKS = ROOT / "outreach" / "redesign-hooks.json"
DEAD = {"Lost", "Bounced", "Unsubscribed", "Won"}


def load_env():
    env = {}
    for p in (ROOT / ".env", ROOT / "cold-email-app" / ".env"):
        if p.exists():
            for line in p.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return None


def call(env, action, args=None):
    body = json.dumps({"token": env["OUTREACH_API_TOKEN"], "action": action, "args": args or {}}).encode()
    req = urllib.request.Request(env["OUTREACH_API_URL"], data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120, context=ctx()) as r:
        out = json.loads(r.read().decode())
    if not out.get("ok"):
        raise RuntimeError(out.get("error") or "API error")
    return out["data"]


def clean(d):
    d = (d or "").strip().lower()
    for p in ("https://", "http://"):
        if d.startswith(p):
            d = d[len(p):]
    d = d.split("/")[0].split("?")[0]
    return d[4:] if d.startswith("www.") else d


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def pull(env):
    try:
        data = call(env, "contactable")
        stores, via = data["stores"], "contactable"
    except RuntimeError as e:
        if "unknown action" not in str(e):
            raise
        catch_all = False
        try:
            catch_all = str(call(env, "get_settings").get("SEND_TO_CATCH_ALL", "")).upper() == "TRUE"
        except Exception:
            pass
        ok = {"valid", "catch-all"} if catch_all else {"valid"}
        stores, offset, via = [], 0, "leads (fallback: redeploy Api.gs for the contactable action)"
        while True:
            page = call(env, "leads", {"limit": 500, "offset": offset})
            for l in page["leads"]:
                if (l.get("website") and l.get("email") and (l.get("email_status") or "").lower() in ok
                        and (l.get("stage") or "New") not in DEAD and "UNCONFIRMED RECIPIENT" not in (l.get("notes") or "")):
                    stores.append({"domain": clean(l["website"]), "brand": l.get("brand"), "lead_id": l.get("lead_id"),
                                   "stage": l.get("stage") or "New", "email_status": l.get("email_status"),
                                   "touch_count": l.get("touch_count", 0), "niche": l.get("niche"),
                                   "country": l.get("country"), "track": l.get("track"), "redesign": "", "mockup_requested": "", "problem_page": "", "problem_kind": "", "problem_worth": 0})
            offset += len(page["leads"])
            if not page["leads"] or offset >= page["total"]:
                break
    queue = build_queue(stores)
    STATE.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"_readme": "Written by outreach/scrapers/redesign_sync.py from the cold email Sheet. "
                               "Real stores may only be designed or posted (CRO Fix, real-store redesigns, Template Showcase) "
                               "if their domain is in `stores`. `buildQueue` is the order the weekly real-store builds pick from "
                               "(see BUILD_QUEUE_RULES). Refreshed hourly on the Mac.",
                               "BUILD_QUEUE_RULES": "1 = said yes to the mockup (build within the week), 2 = emailed, no reply yet, "
                               "strongest problem first, 3 = not emailed yet, strongest problem first. Stores that already have a "
                               "redesign of the requested page are left out. Build the page in `buildPage` (the page the email is "
                               "about); only when that is unknown pick the page type yourself.",
                               "pulledAt": now(), "via": via, "total": len(stores),
                               "buildQueue": queue,
                               "stores": sorted(stores, key=lambda s: s["domain"])}, indent=2, ensure_ascii=False))
    print(f"pull: {len(stores)} contactable stores, {len(queue)} in the build queue, via {via} -> {OUT.relative_to(ROOT)}")


KIND_TO_PAGE = {"homepage": "Homepage", "product": "Product Page", "collection": "Collection Page", "new": "Landing Page"}


def built_kind(redesign):
    parts = [x.strip().lower() for x in (redesign or "").split("|")]
    t = parts[1] if len(parts) > 1 else ""
    for k, w in (("collection", "collection"), ("product", "product"), ("pdp", "product"), ("home", "homepage"),
                 ("advertorial", "new"), ("listicle", "new"), ("landing", "new")):
        if w and k in t:
            return w
    return ""


def build_queue(stores):
    """Ridwan, 2026-10-26: build for the leads most likely to reply, and build the page their email is about."""
    q = []
    for s in stores:
        stage, touches = s.get("stage") or "New", int(s.get("touch_count") or 0)
        want = s.get("problem_kind") or ""
        if s.get("redesign") and (not want or built_kind(s["redesign"]) == want):
            continue  # the page they were emailed about is already built
        if (s.get("mockup_requested") or "").strip():
            tier = 1
        elif stage in ("Contacted", "Finished") and touches >= 1:
            tier = 2
        elif stage == "New" and touches == 0:
            tier = 3
        else:
            continue  # Replied/Talking without a request: Ridwan handles it by hand
        q.append({"tier": tier, "domain": s["domain"], "brand": s.get("brand"), "lead_id": s.get("lead_id"), "stage": stage,
                  "buildPage": KIND_TO_PAGE.get(want, ""), "problemPage": s.get("problem_page", ""),
                  "problemWorth": s.get("problem_worth", 0), "mockupRequested": s.get("mockup_requested", ""),
                  "alreadyBuilt": s.get("redesign", "")})
    return sorted(q, key=lambda x: (x["tier"], -(x["problemWorth"] or 0), x["domain"]))


def push(env, dry):
    if not HOOKS.exists():
        print("push: no outreach/redesign-hooks.json"); return
    data = json.loads(HOOKS.read_text())
    todo = [h for h in data.get("hooks", []) if h.get("status") == "ready" and not h.get("pushedAt")]
    if not todo:
        print("push: nothing new"); return
    changed = False
    for h in todo:
        args = {"domain": h.get("domain"), "date": h.get("date"), "page_type": h.get("pageType"),
                "page_path": h.get("pagePath"), "note": "mobile strip: " + (h.get("mobileStripPath") or "")}
        if dry:
            print("push (dry run):", args); continue
        try:
            res = call(env, "set_redesign", args)
        except RuntimeError as e:
            if "unknown action" in str(e):
                print("push: set_redesign is not live yet. Paste the 2026-10-26 Api.gs/Code.gs/Pipeline.gs/Research.gs into "
                      "Apps Script, run Outreach > Set up tabs (adds the Leads `redesign` column), then Deploy > Manage "
                      "deployments > New version."); return
            h["pushResult"] = "error: " + str(e); changed = True; continue
        h["pushedAt"] = now(); h["pushResult"] = res; changed = True
        print("push:", h.get("domain"), res)
    if changed:
        HOOKS.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    env = load_env()
    if not env.get("OUTREACH_API_URL") or not env.get("OUTREACH_API_TOKEN"):
        sys.exit("OUTREACH_API_URL / OUTREACH_API_TOKEN missing from .env")
    mode = next((a for a in sys.argv[1:] if a in ("pull", "push")), "both")
    if mode in ("pull", "both"):
        pull(env)
    if mode in ("push", "both"):
        push(env, "--dry-run" in sys.argv)


if __name__ == "__main__":
    main()

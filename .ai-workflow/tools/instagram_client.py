#!/usr/bin/env python3
"""
instagram_client.py — Instagram publishing via the Instagram Login API.

Why this replaces the old approach
----------------------------------
Every Instagram attempt from 2026-07-22 onward was blocked on linking a Facebook
Page to @koolestpro, and that link kept getting refused at the Meta account level.
It turns out the requirement no longer exists. Meta's *Instagram API with Instagram
Login* (live since July 2024) publishes to a professional Instagram account with no
Facebook Page in the picture at all. Meta's own docs say it plainly: "This API setup
does not require a Facebook Page to be linked to the Instagram professional account."

So this talks to `graph.instagram.com`, NOT `graph.facebook.com`, and authenticates
with an Instagram-login token rather than a Page token. That difference is the whole
point. Anything still pointing at graph.facebook.com is the old, blocked path.

App: "Koolestpro Publishing" (app 1094745286417525, Instagram app 930775432950893).
The older "Koolestpro Automation" app cannot do this: it is App type None, so Meta
only offers it the legacy Facebook-login product, and the type cannot be converted.

Tokens
------
The authorize flow returns a short-lived token (1 hour). Exchange it once for a
long-lived token (60 days), then refresh that before it lapses. `refresh` is safe to
run on any schedule; Meta only refreshes tokens older than 24 hours, and this reports
rather than fails when a refresh is declined for being too soon.

Usage
-----
    python3 instagram_client.py auth-url
    python3 instagram_client.py exchange "<code from the redirect>"
    python3 instagram_client.py me
    python3 instagram_client.py refresh
    python3 instagram_client.py publish --image-url https://... --caption "..."
    python3 instagram_client.py publish --video-url https://... --caption "..." --reel
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

GRAPH = "https://graph.instagram.com/v23.0"
OAUTH_AUTHORIZE = "https://www.instagram.com/oauth/authorize"
OAUTH_TOKEN = "https://api.instagram.com/oauth/access_token"
OAUTH_LONG = "https://graph.instagram.com/access_token"
OAUTH_REFRESH = "https://graph.instagram.com/refresh_access_token"

SCOPES = "instagram_business_basic,instagram_business_content_publish"
DEFAULT_REDIRECT = "https://koolestpro-portfolio.vercel.app/oauth-callback/"


def find_root(start="."):
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / "CLAUDE.md").exists():
            return cand
    return p


ROOT = find_root(os.environ.get("KP_ROOT", "."))


def read_env():
    env, path = {}, ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def write_env_values(updates):
    path = ROOT / ".env"
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    remaining, out = dict(updates), []
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#") and "=" in s:
            key = s.split("=", 1)[0].strip()
            if key in remaining:
                out.append(f"{key}={remaining.pop(key)}\n")
                continue
        out.append(line)
    for key, val in remaining.items():
        if out and not out[-1].endswith("\n"):
            out.append("\n")
        out.append(f"{key}={val}\n")
    tmp = str(path) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.writelines(out)
    os.replace(tmp, path)


def http(url, data=None, method=None, timeout=120):
    body = urllib.parse.urlencode(data).encode() if isinstance(data, dict) else data
    req = urllib.request.Request(url, data=body, method=method)
    if isinstance(data, dict):
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            return exc.code, json.loads(raw)
        except ValueError:
            return exc.code, {"_raw": raw[:600].decode("utf-8", "replace")}


def need(env, *keys):
    missing = [k for k in keys if not env.get(k)]
    if missing:
        raise SystemExit(
            "missing in .env: " + ", ".join(missing)
            + "\nRun `instagram_client.py exchange <code>` first, or add the app credentials."
        )
    return [env[k] for k in keys]


# ── commands ────────────────────────────────────────────────────────────────

def cmd_auth_url(env, args):
    app_id = env.get("INSTAGRAM_APP_ID") or args.app_id
    if not app_id:
        raise SystemExit("set INSTAGRAM_APP_ID in .env or pass --app-id")
    q = urllib.parse.urlencode({
        "client_id": app_id,
        "redirect_uri": args.redirect or env.get("INSTAGRAM_REDIRECT_URI", DEFAULT_REDIRECT),
        "response_type": "code",
        "scope": SCOPES,
        "force_reauth": "true",
    })
    print("\nOpen this, approve as @koolestpro, then copy the `code` query parameter")
    print("out of the URL you land on (everything after code=, minus a trailing #_):\n")
    print(f"{OAUTH_AUTHORIZE}?{q}\n")


def cmd_exchange(env, args):
    app_id, secret = need(env, "INSTAGRAM_APP_ID", "INSTAGRAM_APP_SECRET")
    redirect = args.redirect or env.get("INSTAGRAM_REDIRECT_URI", DEFAULT_REDIRECT)
    code = args.code.strip().rstrip("#_")

    status, short = http(OAUTH_TOKEN, {
        "client_id": app_id,
        "client_secret": secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect,
        "code": code,
    })
    if status != 200 or "access_token" not in short:
        raise SystemExit(f"short-lived exchange failed ({status}): {json.dumps(short)[:400]}")
    print(f"  short-lived token ok, user id {short.get('user_id')}")

    q = urllib.parse.urlencode({
        "grant_type": "ig_exchange_token",
        "client_secret": secret,
        "access_token": short["access_token"],
    })
    status, long = http(f"{OAUTH_LONG}?{q}")
    if status != 200 or "access_token" not in long:
        raise SystemExit(f"long-lived exchange failed ({status}): {json.dumps(long)[:400]}")

    expires = datetime.now(timezone.utc) + timedelta(seconds=long.get("expires_in", 5184000))
    write_env_values({
        "INSTAGRAM_ACCESS_TOKEN": long["access_token"],
        "INSTAGRAM_USER_ID": str(short.get("user_id", "")),
        "INSTAGRAM_TOKEN_EXPIRES_AT": expires.isoformat(timespec="seconds"),
    })
    print(f"  long-lived token saved, valid until {expires.date()}")
    print("  next: put it into the Make datastore koolestpro-config (149236, key main)")
    print("        fields instagram_page_access_token and instagram_business_account_id")


def cmd_refresh(env, args):
    token, = need(env, "INSTAGRAM_ACCESS_TOKEN")
    q = urllib.parse.urlencode({"grant_type": "ig_refresh_token", "access_token": token})
    status, payload = http(f"{OAUTH_REFRESH}?{q}")
    if status != 200 or "access_token" not in payload:
        # Meta declines a refresh on a token under 24h old. That is not a failure.
        print(f"refresh declined ({status}): {json.dumps(payload)[:300]}")
        return 0
    expires = datetime.now(timezone.utc) + timedelta(seconds=payload.get("expires_in", 5184000))
    write_env_values({
        "INSTAGRAM_ACCESS_TOKEN": payload["access_token"],
        "INSTAGRAM_TOKEN_EXPIRES_AT": expires.isoformat(timespec="seconds"),
    })
    print(f"refreshed, valid until {expires.date()}")
    return 0


def cmd_me(env, args):
    token, = need(env, "INSTAGRAM_ACCESS_TOKEN")
    q = urllib.parse.urlencode({
        "fields": "user_id,username,account_type,media_count",
        "access_token": token,
    })
    status, payload = http(f"{GRAPH}/me?{q}")
    print(json.dumps(payload, indent=2))
    return 0 if status == 200 else 1


def cmd_publish(env, args):
    token, user_id = need(env, "INSTAGRAM_ACCESS_TOKEN", "INSTAGRAM_USER_ID")
    if bool(args.image_url) == bool(args.video_url):
        raise SystemExit("pass exactly one of --image-url or --video-url")
    if args.caption and ("—" in args.caption or "&mdash;" in args.caption):
        raise SystemExit("em dash in caption (project-wide rule, CLAUDE.md)")

    payload = {"access_token": token}
    if args.caption:
        payload["caption"] = args.caption
    if args.image_url:
        payload["image_url"] = args.image_url
    else:
        payload["video_url"] = args.video_url
        payload["media_type"] = "REELS" if args.reel else "VIDEO"

    status, container = http(f"{GRAPH}/{user_id}/media", payload)
    if status != 200 or "id" not in container:
        raise SystemExit(f"container create failed ({status}): {json.dumps(container)[:500]}")
    cid = container["id"]
    print(f"  container {cid}")

    # Video containers need real processing time; images are usually instant but
    # polling both keeps one code path.
    for attempt in range(40):
        q = urllib.parse.urlencode({"fields": "status_code,status", "access_token": token})
        _, st = http(f"{GRAPH}/{cid}?{q}")
        code = st.get("status_code")
        print(f"  container status: {code}")
        if code == "FINISHED":
            break
        if code in ("ERROR", "EXPIRED"):
            raise SystemExit(f"container failed: {json.dumps(st)[:400]}")
        time.sleep(6 if args.video_url else 3)
    else:
        raise SystemExit("container never reached FINISHED")

    if args.dry_run:
        print("dry-run: container is ready, not publishing")
        return 0

    status, pub = http(f"{GRAPH}/{user_id}/media_publish",
                       {"creation_id": cid, "access_token": token})
    if status != 200 or "id" not in pub:
        raise SystemExit(f"publish failed ({status}): {json.dumps(pub)[:500]}")
    print(f"PUBLISHED, media id {pub['id']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Instagram publishing via Instagram Login API.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("auth-url"); p.add_argument("--app-id"); p.add_argument("--redirect")
    p = sub.add_parser("exchange"); p.add_argument("code"); p.add_argument("--redirect")
    sub.add_parser("refresh")
    sub.add_parser("me")
    p = sub.add_parser("publish")
    p.add_argument("--image-url"); p.add_argument("--video-url")
    p.add_argument("--caption", default="")
    p.add_argument("--reel", action="store_true", help="publish a video as a Reel")
    p.add_argument("--dry-run", action="store_true", help="build the container, do not publish")

    args = ap.parse_args()
    env = read_env()
    return {
        "auth-url": cmd_auth_url, "exchange": cmd_exchange, "refresh": cmd_refresh,
        "me": cmd_me, "publish": cmd_publish,
    }[args.cmd](env, args) or 0


if __name__ == "__main__":
    sys.exit(main())

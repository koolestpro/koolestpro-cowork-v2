#!/usr/bin/env python3
"""
tiktok_push_draft.py — push a finished video into Ridwan's TikTok draft inbox.

Why this exists
---------------
TikTok app review was REJECTED on 2026-08-19 for the "display your own posts on
your website" use case. On 2026-09-04 Ridwan narrowed the goal to drafts only:
videos land in his TikTok inbox and he posts them by hand. That path needs only
the `video.upload` scope, which the Sandbox credentials already carry — verified
again on 2026-09-07 by refreshing the token and running a live inbox init. So
NO production app review is required for this. Do not re-litigate that.

NEVER auto-publish to TikTok. `/inbox/video/init/` is the only publish endpoint
this tool is allowed to call. The `/content/init/` (direct post) endpoint needs
`video.publish`, which the app does not have and is not asking for.

Token handling
--------------
The sandbox access token lives 24h; the refresh token lives ~1 year. Every run
refreshes first and writes the fresh pair back into `.env`, so a weekly task can
never fail on an expired token. The refresh token rotates on each exchange —
losing the new one means re-running the whole OAuth authorize flow by hand, so
the .env write is atomic (temp file + replace) and preserves every other line.

Usage
-----
    python3 tiktok_push_draft.py --check
    python3 tiktok_push_draft.py path/to/video.mp4 --title "..." --source tips
    python3 tiktok_push_draft.py video.mp4 --dry-run

Exit codes: 0 ok, 1 failure (token, upload, or non-terminal status).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://open.tiktokapis.com"
TOKEN_URL = f"{API}/v2/oauth/token/"
INBOX_INIT = f"{API}/v2/post/publish/inbox/video/init/"
STATUS_URL = f"{API}/v2/post/publish/status/fetch/"

# TikTok requires 5MB <= chunk_size <= 64MB, and a whole file under 64MB may be
# sent as one chunk. Anything larger gets split; the final chunk absorbs the
# remainder rather than becoming an undersized chunk of its own.
MAX_SINGLE_CHUNK = 64 * 1024 * 1024
CHUNK_TARGET = 20 * 1024 * 1024

TERMINAL_OK = {"SEND_TO_USER_INBOX"}
TERMINAL_BAD = {"FAILED"}


# ── project plumbing ────────────────────────────────────────────────────────

def find_root(start):
    p = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(p, "CLAUDE.md")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            return os.path.abspath(start)
        p = parent


def read_env(root):
    path = os.path.join(root, ".env")
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def write_env_values(root, updates):
    """Rewrite only the named keys in .env, preserving order, comments, blanks."""
    path = os.path.join(root, ".env")
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    remaining = dict(updates)
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in remaining:
                out.append(f"{key}={remaining.pop(key)}\n")
                continue
        out.append(line)

    for key, val in remaining.items():
        if out and not out[-1].endswith("\n"):
            out.append("\n")
        out.append(f"{key}={val}\n")

    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.writelines(out)
    os.replace(tmp, path)


# ── http ────────────────────────────────────────────────────────────────────

def _request(url, data=None, headers=None, method=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _json_post(url, token, payload, timeout=120):
    status, body = _request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        timeout=timeout,
    )
    try:
        parsed = json.loads(body)
    except ValueError:
        parsed = {"_raw": body[:800].decode("utf-8", "replace")}
    return status, parsed


# ── token ───────────────────────────────────────────────────────────────────

def refresh_access_token(root, env, verbose=True):
    key = env.get("TIKTOK_SANDBOX_CLIENT_KEY")
    secret = env.get("TIKTOK_SANDBOX_CLIENT_SECRET")
    refresh = env.get("TIKTOK_SANDBOX_REFRESH_TOKEN")
    missing = [n for n, v in (
        ("TIKTOK_SANDBOX_CLIENT_KEY", key),
        ("TIKTOK_SANDBOX_CLIENT_SECRET", secret),
        ("TIKTOK_SANDBOX_REFRESH_TOKEN", refresh),
    ) if not v]
    if missing:
        raise SystemExit(f"missing in .env: {', '.join(missing)}")

    data = urllib.parse.urlencode({
        "client_key": key,
        "client_secret": secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh,
    }).encode("utf-8")
    status, body = _request(
        TOKEN_URL, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=60,
    )
    payload = json.loads(body)
    if status != 200 or "access_token" not in payload:
        raise SystemExit(f"token refresh failed ({status}): {json.dumps(payload)[:400]}")

    scopes = payload.get("scope", "")
    if "video.upload" not in scopes:
        raise SystemExit(
            f"token lacks video.upload (got: {scopes}). "
            "Re-run the OAuth authorize flow with the video.upload scope."
        )

    write_env_values(root, {
        "TIKTOK_SANDBOX_ACCESS_TOKEN": payload["access_token"],
        "TIKTOK_SANDBOX_REFRESH_TOKEN": payload["refresh_token"],
        "TIKTOK_SANDBOX_OPEN_ID": payload.get("open_id", env.get("TIKTOK_SANDBOX_OPEN_ID", "")),
        "TIKTOK_SANDBOX_TOKEN_REFRESHED_AT": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    if verbose:
        days = round(payload.get("refresh_expires_in", 0) / 86400, 1)
        print(f"  token refreshed; scopes={scopes}; refresh valid {days}d")
    return payload["access_token"]


# ── upload ──────────────────────────────────────────────────────────────────

def plan_chunks(size):
    if size <= MAX_SINGLE_CHUNK:
        return size, 1
    count = max(1, size // CHUNK_TARGET)
    chunk = size // count
    return chunk, count


def upload_video(token, path, verbose=True):
    size = os.path.getsize(path)
    if size == 0:
        raise SystemExit(f"{path} is empty")
    chunk_size, chunk_count = plan_chunks(size)

    status, payload = _json_post(INBOX_INIT, token, {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": size,
            "chunk_size": chunk_size,
            "total_chunk_count": chunk_count,
        }
    })
    if status != 200 or not payload.get("data", {}).get("upload_url"):
        raise SystemExit(f"inbox init failed ({status}): {json.dumps(payload)[:500]}")

    upload_url = payload["data"]["upload_url"]
    publish_id = payload["data"]["publish_id"]
    if verbose:
        print(f"  init ok: {size/1048576:.1f}MB in {chunk_count} chunk(s)")

    with open(path, "rb") as fh:
        for i in range(chunk_count):
            start = i * chunk_size
            end = size - 1 if i == chunk_count - 1 else start + chunk_size - 1
            fh.seek(start)
            blob = fh.read(end - start + 1)
            code, body = _request(
                upload_url, data=blob, method="PUT",
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(blob)),
                    "Content-Range": f"bytes {start}-{end}/{size}",
                },
                timeout=600,
            )
            if code not in (200, 201, 206):
                raise SystemExit(
                    f"chunk {i+1}/{chunk_count} upload failed ({code}): "
                    f"{body[:300].decode('utf-8', 'replace')}"
                )
            if verbose:
                print(f"  chunk {i+1}/{chunk_count} uploaded ({code})")

    return publish_id


def poll_status(token, publish_id, tries=20, delay=6, verbose=True):
    last = None
    for _ in range(tries):
        code, payload = _json_post(STATUS_URL, token, {"publish_id": publish_id}, timeout=60)
        last = payload
        state = payload.get("data", {}).get("status")
        if verbose and state:
            print(f"  status: {state}")
        if state in TERMINAL_OK:
            return True, state, payload
        if state in TERMINAL_BAD:
            return False, state, payload
        time.sleep(delay)
    return False, "TIMEOUT", last


# ── log ─────────────────────────────────────────────────────────────────────

def log_draft(root, record):
    path = os.path.join(root, "outputs", "tiktok-drafts-log.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {"drafts": []}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except ValueError:
            pass
    data.setdefault("drafts", []).append(record)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    return path


def already_pushed(root, video_path):
    path = os.path.join(root, "outputs", "tiktok-drafts-log.json")
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except ValueError:
        return False
    rel = os.path.relpath(os.path.abspath(video_path), root)
    return any(d.get("video") == rel and d.get("ok") for d in data.get("drafts", []))


# ── cli ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Push a video to the TikTok draft inbox.")
    ap.add_argument("video", nargs="?", help="path to an .mp4")
    ap.add_argument("--title", default="", help="note stored in the local log (TikTok inbox has no title field)")
    ap.add_argument("--source", default="", help="which stream produced it, e.g. tips / template-showcase")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--check", action="store_true", help="refresh token and verify scope, upload nothing")
    ap.add_argument("--dry-run", action="store_true", help="validate the file and token, skip the upload")
    ap.add_argument("--force", action="store_true", help="push even if this file was already drafted")
    args = ap.parse_args()

    root = find_root(args.project_root)
    env = read_env(root)

    print(f"project root: {root}")
    token = refresh_access_token(root, env)

    if args.check:
        print("OK — video.upload is live, inbox drafting available without production review.")
        return 0

    if not args.video:
        ap.error("a video path is required unless --check is passed")
    video = args.video if os.path.isabs(args.video) else os.path.join(root, args.video)
    if not os.path.exists(video):
        raise SystemExit(f"no such file: {video}")

    if not args.force and already_pushed(root, video):
        print(f"already drafted: {os.path.relpath(video, root)} (use --force to repeat)")
        return 0

    if args.dry_run:
        print(f"dry-run: would upload {os.path.relpath(video, root)} "
              f"({os.path.getsize(video)/1048576:.1f}MB)")
        return 0

    publish_id = upload_video(token, video)
    ok, state, payload = poll_status(token, publish_id)

    record = {
        "video": os.path.relpath(os.path.abspath(video), root),
        "title": args.title,
        "source": args.source,
        "publishId": publish_id,
        "status": state,
        "ok": ok,
        "pushedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    log_path = log_draft(root, record)
    print(f"logged -> {os.path.relpath(log_path, root)}")

    if ok:
        print("DRAFT LANDED — open TikTok, Profile, Inbox notification, and it is waiting there.")
        return 0
    print(f"FAILED ({state}): {json.dumps(payload)[:400]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Thin CLI wrapper around HeyGen's Direct API (https://api.heygen.com) for the
Cowork sandbox. This is the pay-as-you-go API key pool, separate from the
HyperFrames MCP connector (which bills against a HeyGen web-plan subscription
instead) -- use this skill when the user specifically wants to spend from
their prepaid HEYGEN_API_KEY balance rather than a web plan.

Auth: reads HEYGEN_API_KEY from a --env file, or the process environment.

Subcommands:
  quota                                    Check remaining credits (free to call)
  avatars [--limit N]                      List available avatars (can be slow/large -- see note below)
  voices  [--limit N] [--lang en]          List available voices
  generate --avatar-id ID --voice-id ID --text "..." [--title "..."]
                                            Generate a talking-avatar video (text-to-speech script)
  status <video_id>                        Check render status / get the final video URL
  wait <video_id>                          Poll status until completed/failed

NOTE on /v2/avatars: this endpoint can be slow (large libraries return
megabytes of JSON) and has timed out in testing even though /v2/voices and
/v2/user/remaining_quota respond in a couple seconds. If `avatars` times out,
raise --timeout, or skip it if you already know the avatar_id you want to use.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.heygen.com"


def load_key(env_path):
    key = os.environ.get("HEYGEN_API_KEY")
    if env_path and os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                if k == "HEYGEN_API_KEY" and v:
                    key = v
    return key


def request(method, path, key, json_body=None, params=None, timeout=30):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"x-api-key": key, "User-Agent": "video-gen-cowork-skill/1.0"}
    data = None
    if json_body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(json_body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"error": body}
    except TimeoutError:
        return 0, {"error": f"request to {path} timed out after {timeout}s"}


def cmd_quota(args, key):
    status, data = request("GET", "/v2/user/remaining_quota", key)
    print(json.dumps(data, indent=2))


def cmd_avatars(args, key):
    status, data = request("GET", "/v2/avatars", key, timeout=args.timeout)
    if status == 200:
        avatars = data.get("data", {}).get("avatars", [])
        out = [{"avatar_id": a.get("avatar_id"), "avatar_name": a.get("avatar_name")} for a in avatars[: args.limit]]
        print(json.dumps({"count": len(avatars), "shown": out}, indent=2))
    else:
        print(json.dumps(data, indent=2))


def cmd_voices(args, key):
    status, data = request("GET", "/v2/voices", key, timeout=args.timeout)
    if status == 200:
        voices = data.get("data", {}).get("voices", [])
        if args.lang:
            voices = [v for v in voices if (v.get("language") or "").lower() == args.lang.lower()]
        out = [
            {"voice_id": v.get("voice_id"), "name": v.get("name"), "language": v.get("language")}
            for v in voices[: args.limit]
        ]
        print(json.dumps({"count": len(voices), "shown": out}, indent=2))
    else:
        print(json.dumps(data, indent=2))


def cmd_generate(args, key):
    body = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": args.avatar_id,
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "text",
                    "input_text": args.text,
                    "voice_id": args.voice_id,
                },
            }
        ],
        "dimension": {"width": args.width, "height": args.height},
    }
    if args.title:
        body["title"] = args.title
    status, data = request("POST", "/v2/video/generate", key, json_body=body)
    print(json.dumps(data, indent=2))
    if status >= 400:
        sys.exit(1)


def cmd_status(args, key):
    status, data = request("GET", "/v1/video_status.get", key, params={"video_id": args.video_id})
    print(json.dumps(data, indent=2))


def cmd_wait(args, key):
    for _ in range(args.max_polls):
        status, data = request("GET", "/v1/video_status.get", key, params={"video_id": args.video_id})
        s = data.get("data", {}).get("status")
        print(f"  ...status={s}", file=sys.stderr)
        if s in ("completed", "failed"):
            print(json.dumps(data, indent=2))
            return
        time.sleep(args.interval)
    print(json.dumps({"warning": "gave up waiting", "video_id": args.video_id}, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("quota")
    p.set_defaults(func=cmd_quota)

    p = sub.add_parser("avatars")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--timeout", type=int, default=45)
    p.set_defaults(func=cmd_avatars)

    p = sub.add_parser("voices")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--lang", default=None)
    p.add_argument("--timeout", type=int, default=45)
    p.set_defaults(func=cmd_voices)

    p = sub.add_parser("generate")
    p.add_argument("--avatar-id", required=True)
    p.add_argument("--voice-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--title", default=None)
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("status")
    p.add_argument("video_id")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("wait")
    p.add_argument("video_id")
    p.add_argument("--interval", type=int, default=10)
    p.add_argument("--max-polls", type=int, default=30)
    p.set_defaults(func=cmd_wait)

    args = ap.parse_args()
    key = load_key(args.env)
    if not key:
        print(json.dumps({"error": "no HEYGEN_API_KEY found (check --env or environment)"}), file=sys.stderr)
        sys.exit(1)
    args.func(args, key)


if __name__ == "__main__":
    main()

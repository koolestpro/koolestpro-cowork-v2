#!/usr/bin/env python3
"""
Thin CLI wrapper around the inference.sh REST API (https://api.inference.sh)
for the Cowork sandbox — no `infsh`/`belt` CLI install or interactive login
required, just an API key.

Auth: reads INFSH_API_KEY (or INFERENCE_API_KEY) from a --env file, or from
the process environment if no file is given / the file doesn't have it.

Subcommands:
  search   "<query>"                          Find apps by keyword (no auth needed)
  run      <app> --input '<json>' [--wait/--no-wait] [--setup '<json>']
  status   <task_id>
  cancel   <task_id>
  upload   <path> [--public]                  Upload a local file, get an inf:// / https:// uri back
  download <url> <out_path>                   Download a task's output file

Examples:
  python3 infsh.py search "image to video"
  python3 infsh.py run pruna/p-video --input '{"prompt": "a cat riding a skateboard"}'
  python3 infsh.py upload ./portrait.jpg
  python3 infsh.py run heygen/avatar-video --input '{"image": "<uri-from-upload>", "text": "hello"}'
  python3 infsh.py status task_abc123
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.inference.sh"
# Cloudflare (fronting api.inference.sh) fingerprints and blocks the default
# "Python-urllib/3.x" user agent (error code 1010) -- a normal-looking UA
# avoids that without needing a browser or extra dependency.
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) video-gen-cowork-skill/1.0"


def load_key(env_path):
    key = os.environ.get("INFSH_API_KEY") or os.environ.get("INFERENCE_API_KEY")
    if env_path and os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                if k in ("INFSH_API_KEY", "INFERENCE_API_KEY") and v:
                    key = v
    return key


def request(method, path, key=None, json_body=None, files=None, params=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {"X-API-Version": "2", "User-Agent": USER_AGENT}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    if files:
        # multipart/form-data, built by hand to avoid a requests dependency
        import mimetypes
        import uuid
        boundary = uuid.uuid4().hex
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        body = b""
        for field_name, value in (files.get("fields") or {}).items():
            body += (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{field_name}\"\r\n\r\n{value}\r\n"
            ).encode()
        file_path = files["file_path"]
        filename = os.path.basename(file_path)
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        body += (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode()
        with open(file_path, "rb") as f:
            body += f.read()
        body += f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    elif json_body is not None:
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=json.dumps(json_body).encode(), headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"error": body}


def cmd_search(args, key):
    status, data = request("GET", "/search", params={"q": args.query, "collections": "apps", "limit": args.limit})
    print(json.dumps(data, indent=2))


def cmd_run(args, key):
    if not key:
        print(json.dumps({"error": "no INFSH_API_KEY/INFERENCE_API_KEY found"}), file=sys.stderr)
        sys.exit(1)
    body = {"app": args.app, "input": json.loads(args.input)}
    if args.setup:
        body["setup"] = json.loads(args.setup)
    params = {"wait": "false"} if args.no_wait else None
    status, data = request("POST", "/run", key=key, json_body=body, params=params)
    print(json.dumps(data, indent=2))
    if status >= 400:
        sys.exit(1)

    if args.no_wait or not args.poll:
        return

    # Poll until the task reaches a terminal state (has output or error),
    # rather than trusting specific numeric status codes — inference.sh's
    # own docs disagree with each other on the exact code mapping, but
    # output/error being populated is unambiguous either way.
    task_id = data.get("id")
    if not task_id:
        return
    print(f"Polling task {task_id}...", file=sys.stderr)
    for _ in range(args.poll_max):
        time.sleep(args.poll_interval)
        s, d = request("GET", f"/tasks/{task_id}", key=key)
        if d.get("output") or d.get("error"):
            print(json.dumps(d, indent=2))
            return
        print(f"  ...status={d.get('status')}", file=sys.stderr)
    print(json.dumps({"warning": "gave up polling, task may still be running", "id": task_id}, indent=2))


def cmd_status(args, key):
    status, data = request("GET", f"/tasks/{args.task_id}", key=key)
    print(json.dumps(data, indent=2))


def cmd_cancel(args, key):
    status, data = request("POST", f"/tasks/{args.task_id}/cancel", key=key)
    print(json.dumps(data, indent=2))


def cmd_upload(args, key):
    if not key:
        print(json.dumps({"error": "no INFSH_API_KEY/INFERENCE_API_KEY found"}), file=sys.stderr)
        sys.exit(1)
    fields = {}
    if args.public:
        fields["public"] = "true"
    status, data = request("POST", "/files", key=key, files={"file_path": args.path, "fields": fields})
    print(json.dumps(data, indent=2))


def cmd_download(args, key):
    import urllib.request as ur
    ur.urlretrieve(args.url, args.out_path)
    print(json.dumps({"saved_to": args.out_path}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=None, help="path to .env with INFSH_API_KEY")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=8)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("run")
    p.add_argument("app")
    p.add_argument("--input", required=True, help="JSON string matching the app's input schema")
    p.add_argument("--setup", default=None, help="JSON string of setup params")
    p.add_argument("--no-wait", action="store_true", help="return immediately with a task id instead of blocking")
    p.add_argument("--poll", action="store_true", default=True, help="poll for completion (default: on)")
    p.add_argument("--no-poll", dest="poll", action="store_false")
    p.add_argument("--poll-interval", type=int, default=5)
    p.add_argument("--poll-max", type=int, default=60, help="max polls before giving up (default 60 * 5s = 5min)")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("status")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("cancel")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_cancel)

    p = sub.add_parser("upload")
    p.add_argument("path")
    p.add_argument("--public", action="store_true")
    p.set_defaults(func=cmd_upload)

    p = sub.add_parser("download")
    p.add_argument("url")
    p.add_argument("out_path")
    p.set_defaults(func=cmd_download)

    args = ap.parse_args()
    key = load_key(args.env)
    args.func(args, key)


if __name__ == "__main__":
    main()

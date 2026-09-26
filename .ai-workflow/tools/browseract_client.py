#!/usr/bin/env python3
"""
browseract_client.py — thin wrapper around the BrowserAct Data API.

Same pattern as this project's DeepSeek integration: a pay-per-use REST API,
key lives in .env, called directly from bash inside Cowork. No MCP connector
exists for BrowserAct yet (checked 2026-08-11 — not in the Cowork connector
registry), so this script IS the integration until/unless one ships.

Docs: https://docs.browseract.com  (Data API: POST /v2/workflow/run-task)

Setup (one-time, done by Ridwan — Claude cannot create the account or enter
payment info):
  1. Sign up at https://www.browseract.com (free trial, no card to start)
  2. Build or clone a workflow template in the console, publish it, copy its
     workflow_id
  3. Grab the API key from the console's Integrations page
  4. Add to .env:
       BROWSERACT_API_KEY=...

Usage:
  python3 browseract_client.py run --workflow-id <id> --input '{"query":"wireless headphones","limit":20}'
  python3 browseract_client.py status --task-id <id>
  python3 browseract_client.py result --task-id <id>
  python3 browseract_client.py run --workflow-id <id> --input '{...}' --wait   # run + poll until done, print result

Exit codes: 0 success, 1 API/config error, 2 task failed or timed out.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

API_BASE = "https://api.browseract.com/v2"


def load_api_key():
    key = os.environ.get("BROWSERACT_API_KEY")
    if key:
        return key
    # fall back to reading .env directly (bash tool calls don't always export it)
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
    env_path = os.path.normpath(env_path)
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("BROWSERACT_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _request(method, path, api_key, body=None):
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")
        print(f"HTTP {e.code} from {url}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error calling {url}: {e}", file=sys.stderr)
        sys.exit(1)


def run_task(api_key, workflow_id, input_parameters, callback_url=None, profile_id=None):
    # API expects input_parameters as an array of {"name": ..., "value": ...} objects,
    # matching the workflow_id's declared input parameter names (see get_workflow()).
    # Accept either that array shape directly, or a flat {"name": "value"} dict for convenience.
    if isinstance(input_parameters, dict):
        input_parameters = [{"name": k, "value": str(v)} for k, v in input_parameters.items()]
    body = {"workflow_id": workflow_id, "input_parameters": input_parameters}
    if callback_url:
        body["callback_url"] = callback_url
    if profile_id:
        body["profile_id"] = profile_id
    return _request("POST", "/workflow/run-task", api_key, body)


def get_task_status(api_key, task_id):
    return _request("GET", f"/workflow/get-task-status?task_id={task_id}", api_key)


def get_task(api_key, task_id):
    return _request("GET", f"/workflow/get-task?task_id={task_id}", api_key)


def get_workflow(api_key, workflow_id):
    return _request("GET", f"/workflow/get-workflow?workflow_id={workflow_id}", api_key)


def list_workflows(api_key, page=1, limit=50):
    return _request("GET", f"/workflow/list-workflows?page={page}&limit={limit}", api_key)


def list_templates(api_key, page=1, limit=50, keyword=None):
    q = f"/workflow/list-official-workflow-templates?page={page}&limit={limit}"
    if keyword:
        q += f"&keyword={urllib.parse.quote(keyword)}"
    return _request("GET", q, api_key)


def get_template(api_key, template_id):
    return _request("GET", f"/workflow/get-official-workflow-template?workflow_template_id={template_id}", api_key)


def poll_until_done(api_key, task_id, interval=5, timeout=300):
    elapsed = 0
    while elapsed < timeout:
        status = get_task_status(api_key, task_id)
        state = status.get("status")
        if state in ("completed", "failed", "error"):
            return status
        time.sleep(interval)
        elapsed += interval
    return {"status": "timeout", "task_id": task_id}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Trigger a workflow run")
    p_run.add_argument("--workflow-id", required=True)
    p_run.add_argument("--input", required=True, help="JSON object of input_parameters")
    p_run.add_argument("--callback-url")
    p_run.add_argument("--profile-id")
    p_run.add_argument("--wait", action="store_true", help="Poll until the task completes, then print the result")

    p_status = sub.add_parser("status", help="Check a task's status")
    p_status.add_argument("--task-id", required=True)

    p_result = sub.add_parser("result", help="Fetch a completed task's output")
    p_result.add_argument("--task-id", required=True)

    p_list = sub.add_parser("list-workflows", help="List workflows in the workspace")

    p_get_wf = sub.add_parser("get-workflow", help="Fetch a workflow's input parameter definitions")
    p_get_wf.add_argument("--workflow-id", required=True)

    p_list_tpl = sub.add_parser("list-templates", help="Browse BrowserAct's official workflow templates")
    p_list_tpl.add_argument("--keyword")

    p_get_tpl = sub.add_parser("get-template", help="Fetch an official template's config")
    p_get_tpl.add_argument("--template-id", required=True)

    args = p.parse_args()
    api_key = load_api_key()
    if not api_key:
        print("BROWSERACT_API_KEY not set in environment or .env. Add it to .env first.", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "run":
        try:
            input_params = json.loads(args.input)
        except json.JSONDecodeError as e:
            print(f"--input must be valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
        result = run_task(api_key, args.workflow_id, input_params, args.callback_url, args.profile_id)
        task_id = result.get("id") or result.get("task_id")
        print(json.dumps(result, indent=2))
        if args.wait and task_id:
            print(f"\nPolling task {task_id}...", file=sys.stderr)
            final = poll_until_done(api_key, task_id)
            print(json.dumps(final, indent=2))
            if final.get("status") not in ("completed",):
                sys.exit(2)

    elif args.cmd == "status":
        print(json.dumps(get_task_status(api_key, args.task_id), indent=2))

    elif args.cmd == "result":
        print(json.dumps(get_task(api_key, args.task_id), indent=2))

    elif args.cmd == "list-workflows":
        print(json.dumps(list_workflows(api_key), indent=2))

    elif args.cmd == "get-workflow":
        print(json.dumps(get_workflow(api_key, args.workflow_id), indent=2))

    elif args.cmd == "list-templates":
        print(json.dumps(list_templates(api_key, keyword=args.keyword), indent=2))

    elif args.cmd == "get-template":
        print(json.dumps(get_template(api_key, args.template_id), indent=2))


if __name__ == "__main__":
    main()

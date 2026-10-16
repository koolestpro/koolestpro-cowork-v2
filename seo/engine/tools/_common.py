"""Shared helpers for the SEO engine tools.

Layout (the same in every project the engine is copied into):
  <repo>/seo/engine/    the portable kit (never edit per project)
  <repo>/seo/project/   this project's data: project.json, business-profile.md, clusters.md, logs, runs/
  <repo>/.env           this project's own API keys (never committed)

SEO_PROJECT_DIR can point the tools at a different project folder.
"""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent.parent
SEO_ROOT = ENGINE_DIR.parent
REPO_ROOT = SEO_ROOT.parent
UA = "Mozilla/5.0 (SEO-Engine/1.0)"


def project_dir():
    d = Path(os.environ.get("SEO_PROJECT_DIR") or SEO_ROOT / "project")
    if not (d / "project.json").exists():
        raise SystemExit(f"No project.json in {d}. Run: python3 seo/engine/tools/init.py")
    return d


def load_project():
    return json.loads((project_dir() / "project.json").read_text())


def load_env():
    """Load .env (repo root, then seo/) into os.environ without overriding existing values."""
    for env_file in (REPO_ROOT / ".env", SEO_ROOT / ".env"):
        if not env_file.exists():
            continue
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def need_env(*names, soft=False):
    """Return the values of env vars; exit 3 with NO_CREDENTIALS if any is missing."""
    load_env()
    vals = [os.environ.get(n, "").strip() for n in names]
    missing = [n for n, v in zip(names, vals) if not v]
    if missing:
        if soft:
            return None
        import sys
        print(f"NO_CREDENTIALS: set {', '.join(missing)} in .env (see seo/engine/SETUP.md)", file=sys.stderr)
        sys.exit(3)
    return vals


def site_domain(cfg):
    return cfg["site_url"].split("//")[-1].strip("/").removeprefix("www.")


def http(url, data=None, headers=None, method=None, timeout=60):
    """Return (status, body_text). Never raises on HTTP errors."""
    h = {"User-Agent": UA}
    h.update(headers or {})
    if isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
        h.setdefault("Content-Type", "application/json")
    elif isinstance(data, str):
        data = data.encode()
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def google_access_token():
    """Exchange the project's Google refresh token for an access token (GSC, GA4, Ads, Sheets)."""
    import sys
    import urllib.parse
    cid, secret, refresh = need_env("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN")
    status, body = http("https://oauth2.googleapis.com/token", data=urllib.parse.urlencode({
        "client_id": cid, "client_secret": secret, "refresh_token": refresh, "grant_type": "refresh_token",
    }), headers={"Content-Type": "application/x-www-form-urlencoded"})
    if status != 200:
        sys.exit(f"Google token refresh failed ({status}): {body[:300]}")
    return json.loads(body)["access_token"]

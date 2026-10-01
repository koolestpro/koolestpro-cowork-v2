"""Shared helpers for the SEO tools: repo paths, .env loading, client config, HTTP."""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

SEO_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SEO_DIR.parent
UA = "Mozilla/5.0 (KoolestproSEO/1.0)"


def load_env():
    """Load repo-root .env into os.environ without overriding existing values."""
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def client_dir(slug):
    d = SEO_DIR / "clients" / slug
    if not d.exists():
        raise SystemExit(f"Unknown client '{slug}': {d} does not exist")
    return d


def load_client(slug):
    return json.loads((client_dir(slug) / "client.json").read_text())


def env_key(slug, name):
    return f"{name}_{slug.upper().replace('-', '_')}"


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

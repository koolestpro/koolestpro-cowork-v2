#!/usr/bin/env python3
"""
start_koolestflow_local.py — Start the local KoolestFlow backend from anywhere.

Usage:
  python3 .ai-workflow/tools/start_koolestflow_local.py

What it does:
  - Finds the cold-email-app subfolder inside this project
  - Auto-loads its .env.local so APP_PASSWORD and other secrets are available
  - Starts backend/app.py on http://127.0.0.1:8787
  - Writes stdout/stderr to /tmp/koolestflow.log
  - Prints the PID so you can stop it later:  kill <pid>

Prerequisites:
  - cold-email-app/.env.local must contain APP_PASSWORD (set during setup)
  - Port 127.0.0.1:8787 must be free

The backend already has auto-reload for its .env.local (added to app.py), so
this script mainly exists to make starting it from the project root convenient.
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "cold-email-app" / "backend"
LOG_FILE = Path("/tmp/koolestflow.log")


def load_env_file(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    if not BACKEND_DIR.exists():
        print(f"ERROR: Backend directory not found: {BACKEND_DIR}")
        print("Did you move the cold-email-app folder into this project?")
        sys.exit(1)

    # Load env vars from .env.local so they're available to the child process
    env_local = BACKEND_DIR.parent / ".env.local"
    env_vars = load_env_file(env_local)
    env = os.environ.copy()
    env.update(env_vars)

    # Check if already running
    try:
        result = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:8787/api/health"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0 and '"ok": true' in result.stdout:
            print("KoolestFlow local backend is ALREADY running on http://127.0.0.1:8787")
            print(f"  Log file: {LOG_FILE}")
            sys.exit(0)
    except Exception:
        pass

    log = open(LOG_FILE, "a")
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=str(BACKEND_DIR),
        stdout=log,
        stderr=subprocess.STDOUT,
        env=env,
    )

    print(f"Started KoolestFlow local backend (PID {proc.pid})")
    print(f"  API:      http://127.0.0.1:8787")
    print(f"  Log:      {LOG_FILE}")
    print(f"  Stop:     kill {proc.pid}")
    print("")
    print("Test it:")
    print("  curl http://127.0.0.1:8787/api/health")


if __name__ == "__main__":
    main()

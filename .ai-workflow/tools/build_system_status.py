#!/usr/bin/env python3
"""
build_system_status.py — generate SYSTEM-STATUS.html + system-status.json

The status half of the system map (see SYSTEM-MAP.md). Every number on the page
traces to a real file on disk. Nothing is hand-maintained and nothing is
estimated.

Design constraints that are load-bearing, not stylistic:

  1. READ-ONLY on every input. This script must never be able to damage an
     operational file. It opens sources, it writes only its own two outputs.
  2. A missing or unreadable source reports "source missing" for that row.
     It NEVER falls back to zero. A zero that means "I could not read the file"
     is the most dangerous possible output for a status page.
  3. Every section carries the generating run's timestamp, so a stale page is
     obviously stale rather than quietly wrong.
  4. Brand rules apply: dark theme, solid text colours only (no gradient text,
     CSS or SVG — see CLAUDE.md "GRADIENT SYSTEM").

Scheduled-task rows come from .ai-workflow/scheduled-tasks-snapshot.json, which
this script cannot produce on its own: the task list lives behind an MCP tool,
not on disk. The weekly regeneration task writes that snapshot immediately
before calling this script. If it is absent or stale the page says so.

Usage:
    python3 .ai-workflow/tools/build_system_status.py [--project-root .]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from html import escape
from pathlib import Path

# ── thresholds that trigger a loud flag ──────────────────────────────────────
STALE_TASK_DAYS = 14        # a scheduled task that has not run in this long
LOW_POOL_UNTOUCHED = 4      # untouched targets_pool candidates below this
PENDING_PUSH_HOURS = 48     # a queued lead file sitting unimported this long
MIN_CLEAN_PACE = 1.5        # clean posts/day below this (target is 3 average)
IMPORTER_LOG_TAIL = 40      # launchd log lines to inspect for a live failure

# Instruction files agents read, in bytes. The cost of a prompt is dominated by
# how big the always-loaded surface is, so this is measured rather than trusted:
# the slim rulebook is undone the moment one of these quietly regrows.
CONTEXT_BUDGETS = {
    "AGENTS.md": 6_000,       # injected on every request — the always-loaded surface
    "CLAUDE.md": 40_000,      # rulebook, read per task; must not regrow toward 116KB
    "SYSTEM-MAP.md": 16_000,  # inventory, read when routing
}

MISSING = object()          # sentinel: source could not be read


class Source:
    """One input file. Carries its own read failure rather than raising."""

    def __init__(self, root: Path, rel: str):
        self.rel = rel
        self.path = root / rel
        self.error: str | None = None
        self.data = None
        self._read()

    def _read(self):
        if not self.path.exists():
            self.error = "file not found"
            return
        try:
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.error = f"{type(exc).__name__}: {exc}"

    @property
    def ok(self) -> bool:
        return self.error is None


def read_sync_data(root: Path) -> tuple[dict | None, str | None]:
    """Extract SYNC_DATA from the content system's embedded script block.

    Deliberately tolerant of the surrounding HTML changing, and deliberately
    loud on failure: a partial parse is worse than no parse.
    """
    path = root / "ridwan_content_system_updated.html"
    if not path.exists():
        return None, "file not found"
    try:
        html = path.read_text(encoding="utf-8")
    except Exception as exc:
        return None, f"unreadable: {exc}"
    match = re.search(
        r'<script id="cowork-sync-data"[^>]*>(.*?)</script>', html, re.S
    )
    if not match:
        return None, "cowork-sync-data script block not found"
    try:
        data = json.loads(match.group(1))
    except Exception as exc:
        return None, f"JSON parse failed: {exc}"
    if not isinstance(data, dict) or "items" not in data:
        return None, "parsed but has no items[] — refusing a partial read"
    return data, None


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M UTC")


# ── collectors ───────────────────────────────────────────────────────────────

def collect_content(root: Path) -> dict:
    data, err = read_sync_data(root)
    if err:
        return {"error": err, "source": "ridwan_content_system_updated.html"}
    items = data["items"]
    by_status = Counter(i.get("status") for i in items)
    return {
        "source": "ridwan_content_system_updated.html → SYNC_DATA",
        "total": len(items),
        "months": len(data.get("months", {})),
        "by_status": dict(by_status),
        "by_type": dict(Counter(i.get("type") for i in items)),
        "idea_backlog": by_status.get("Idea", 0),
    }


def collect_queue(root: Path, now: datetime) -> dict:
    src = Source(root, "outputs/distribution-queue/queue.json")
    if not src.ok:
        return {"error": src.error, "source": src.rel}
    rows = src.data.get("rows", []) if isinstance(src.data, dict) else []
    if not rows:
        return {"error": "parsed but rows[] is empty or absent", "source": src.rel}

    today = now.date()
    horizon = today + timedelta(days=7)
    clean_upcoming = 0
    overdue_blocked = 0

    def is_clean(row) -> bool:
        qa = (row.get("qa_status") or "").lower()
        return "needs review" not in qa

    for row in rows:
        if row.get("platform") not in ("Twitter", "LinkedIn"):
            continue
        if row.get("status") == "Posted":
            continue
        raw = row.get("scheduled_date") or ""
        try:
            when = datetime.strptime(raw[:10], "%Y-%m-%d").date()
        except ValueError:
            continue
        if today <= when <= horizon and is_clean(row):
            clean_upcoming += 1
        if when < today and not is_clean(row):
            overdue_blocked += 1

    pace = round(clean_upcoming / 7, 2)
    return {
        "source": src.rel,
        "total_rows": len(rows),
        "by_platform": dict(Counter(r.get("platform") for r in rows)),
        "by_status": dict(Counter(r.get("status") for r in rows)),
        "clean_next_7d": clean_upcoming,
        "clean_pace_per_day": pace,
        "overdue_qa_blocked": overdue_blocked,
        "note": "Twitter + LinkedIn only. Instagram is excluded because it "
                "cannot post at all (Meta Page-IG link blocker).",
    }


def collect_targets(root: Path) -> dict:
    src = Source(root, "targets_pool.json")
    if not src.ok:
        return {"error": src.error, "source": src.rel}
    targets = src.data.get("targets", [])
    untouched = [t for t in targets if not t.get("usedFor")]
    return {
        "source": src.rel,
        "total": len(targets),
        "by_status": dict(Counter(t.get("status") for t in targets)),
        "by_category": dict(Counter(t.get("category") for t in targets)),
        "untouched": len(untouched),
        "unrated_visual": sum(
            1 for t in targets if t.get("visualPotential") == "Unrated"
        ),
    }


def collect_showcase(root: Path) -> dict:
    src = Source(root, "replo-rebuilds-pages.json")
    if not src.ok:
        return {"error": src.error, "source": src.rel}
    pages = src.data.get("pages", [])
    eligible = [
        p for p in pages
        if p.get("active") and not p.get("usedForTemplateShowcase")
    ]
    def label(page: dict) -> str:
        # The manifest keys pages by showcaseSlug; templateId and brand are
        # fallbacks. There is deliberately no "?" default — an unlabelable
        # entry is a manifest problem worth seeing, not worth hiding.
        return (
            page.get("showcaseSlug")
            or page.get("templateId")
            or f"UNLABELLED ({page.get('sourcePath', 'no sourcePath')})"
        )

    return {
        "source": src.rel,
        "total": len(pages),
        "retired": sum(1 for p in pages if p.get("retired")),
        "eligible_unused": len(eligible),
        "next_up": [
            label(p) for p in sorted(eligible, key=lambda x: x.get("sortOrder", 999))
        ][:5],
    }


def collect_store_templates(root: Path) -> dict:
    src = Source(root, "store-templates.json")
    if not src.ok:
        return {"error": src.error, "source": src.rel}
    templates = src.data.get("templates", [])
    return {
        "source": src.rel,
        "total": len(templates),
        "verticals": [
            f"{t.get('vertical')} ({t.get('demoBrand')}) — {t.get('status')}"
            for t in templates
        ],
    }


def collect_leads(root: Path, now: datetime) -> dict:
    out: dict = {}

    ledger = Source(root, ".ai-workflow/taken-brands-ledger.json")
    if not ledger.ok:
        out["ledger"] = {"error": ledger.error, "source": ledger.rel}
    else:
        # The real brands live under a "brands" key alongside "meta".
        # Counting top-level keys reports 2 forever, which looks plausible
        # and is wrong — exactly the failure this file's rules warn about.
        brands = ledger.data.get("brands")
        if not isinstance(brands, dict):
            out["ledger"] = {
                "error": "no brands{} object — schema changed?",
                "source": ledger.rel,
            }
        else:
            out["ledger"] = {"source": ledger.rel, "brands_taken": len(brands)}

    pending_dir = root / ".ai-workflow/pending-push"
    if not pending_dir.is_dir():
        out["pending_push"] = {
            "error": "directory not found",
            "source": ".ai-workflow/pending-push/",
        }
    else:
        files = sorted(pending_dir.glob("*.json"))
        stale = []
        for f in files:
            age_h = (now.timestamp() - f.stat().st_mtime) / 3600
            if age_h > PENDING_PUSH_HOURS:
                stale.append({"file": f.name, "age_hours": round(age_h)})
        out["pending_push"] = {
            "source": ".ai-workflow/pending-push/",
            "queued": len(files),
            "files": [f.name for f in files],
            "stale": stale,
        }

    out["importer"] = collect_importer(root, now)
    return out


def collect_importer(root: Path, now: datetime) -> dict:
    """Read the launchd log, so a FAILING importer is distinguishable from an
    idle one.

    Stale files alone cannot tell these apart: a queue nobody has fed and a
    queue whose drainer has been erroring every 30 minutes look identical from
    the filesystem. That ambiguity is what let a macOS TCC denial run silently
    for two weeks (2026-09-02 to 2026-09-16) while the page reported only
    "the Mac importer may not be running" as a guess.
    """
    rel = ".ai-workflow/leadgen-import.launchd.log"
    log = root / rel
    out: dict = {"source": rel}

    if not log.is_file():
        out["error"] = "launchd log not found — is the agent installed?"
        return out

    age_h = (now.timestamp() - log.stat().st_mtime) / 3600
    out["last_write_age_hours"] = round(age_h, 1)

    try:
        tail = log.read_text(errors="replace").splitlines()[-IMPORTER_LOG_TAIL:]
    except OSError as exc:
        out["error"] = f"could not read log: {exc}"
        return out

    # Classify rather than echo. The same line repeats hundreds of times, so
    # the useful signal is which failure, not how the last line reads.
    errs = [ln.strip() for ln in tail if "Operation not permitted" in ln
            or "Permission denied" in ln or "command not found" in ln
            or "No such file" in ln]
    out["recent_error_lines"] = len(errs)

    if any("Operation not permitted" in e for e in errs):
        out["state"] = "blocked"
        out["diagnosis"] = (
            "macOS is denying the launchd agent access to the project folder "
            "(TCC). The job fires on schedule but /bin/bash cannot execute the "
            "script, so nothing is ever imported."
        )
    elif errs:
        out["state"] = "failing"
        out["diagnosis"] = errs[-1][:200]
    else:
        out["state"] = "ok"

    return out


def collect_spend(root: Path) -> dict:
    src = Source(root, "trend-radar-spend-ledger.json")
    if not src.ok:
        return {"error": src.error, "source": src.rel}
    months = src.data.get("months", {})
    return {
        "source": src.rel,
        "by_month": {
            m: {k: v for k, v in vals.items()} for m, vals in months.items()
        },
    }


def collect_context(root: Path) -> dict:
    """Size the instruction files agents read, against their budget.

    This is the prompt-cost surface: AGENTS.md is injected on every request,
    CLAUDE.md and SYSTEM-MAP.md are read per task. A missing file is reported
    as an error, never as a zero-size pass — a budget that cannot be measured
    is not a budget.
    """
    entries = []
    for rel, budget in CONTEXT_BUDGETS.items():
        path = root / rel
        if not path.exists():
            entries.append({
                "file": rel,
                "budget_bytes": budget,
                "error": "file not found",
            })
            continue
        size = path.stat().st_size
        entries.append({
            "file": rel,
            "bytes": size,
            "kib": round(size / 1024, 1),
            "tokens_est": round(size / 4),
            "budget_bytes": budget,
            "budget_kib": round(budget / 1024),
            "over_budget": size > budget,
        })
    return {
        "source": "AGENTS.md / CLAUDE.md / SYSTEM-MAP.md",
        "files": entries,
    }


def collect_tasks(root: Path, now: datetime) -> dict:
    """Scheduled tasks come from a snapshot the weekly task writes.

    This script cannot read the live task list — it lives behind an MCP tool,
    not on disk. No snapshot means we say so, not that we invent rows.
    """
    src = Source(root, ".ai-workflow/scheduled-tasks-snapshot.json")
    if not src.ok:
        return {
            "error": src.error,
            "source": src.rel,
            "hint": "Written by koolestpro-system-status-weekly immediately "
                    "before this script runs. Absent means that task has not "
                    "run yet, not that there are no scheduled tasks.",
        }

    written = src.data.get("writtenAt")
    tasks = src.data.get("tasks", [])
    rows, stale = [], []
    for t in tasks:
        last = t.get("lastRunAt")
        age_days = None
        if last:
            try:
                then = datetime.fromisoformat(last.replace("Z", "+00:00"))
                age_days = (now - then).days
            except ValueError:
                age_days = None
        row = {
            "id": t.get("taskId"),
            "enabled": t.get("enabled"),
            "schedule": t.get("schedule"),
            "last_run": last,
            "days_since": age_days,
            "next_run": t.get("nextRunAt"),
        }
        rows.append(row)
        if t.get("enabled") and age_days is not None and age_days > STALE_TASK_DAYS:
            stale.append(row)

    return {
        "source": src.rel,
        "snapshot_written_at": written,
        "total": len(rows),
        "enabled": sum(1 for r in rows if r["enabled"]),
        "disabled": sum(1 for r in rows if not r["enabled"]),
        "tasks": rows,
        "stale": stale,
    }


def build_flags(report: dict) -> list[dict]:
    """The conditions that decay silently. Loud on purpose."""
    flags: list[dict] = []

    tasks = report["scheduled_tasks"]
    if tasks.get("stale"):
        for row in tasks["stale"]:
            flags.append({
                "level": "warn",
                "text": f"{row['id']} is enabled but has not run in "
                        f"{row['days_since']} days.",
            })

    targets = report["targets_pool"]
    if "error" not in targets and targets["untouched"] < LOW_POOL_UNTOUCHED:
        flags.append({
            "level": "warn",
            "text": f"targets_pool has only {targets['untouched']} untouched "
                    f"candidates left (threshold {LOW_POOL_UNTOUCHED}).",
        })

    # Name the importer's actual state first, so the stale-file alerts below
    # read as a consequence rather than as the finding.
    imp = report["lead_gen"].get("importer", {})
    if imp.get("error"):
        flags.append({
            "level": "alert",
            "text": f"Lead importer: {imp['error']} ({imp.get('source','')})",
        })
    elif imp.get("state") == "blocked":
        flags.append({
            "level": "alert",
            "text": "Lead importer is BLOCKED, not idle. " + imp["diagnosis"] +
                    " Grant Full Disk Access to /bin/bash, or move the project "
                    "out of ~/Downloads. Until then every queued file stays put.",
        })
    elif imp.get("state") == "failing":
        flags.append({
            "level": "alert",
            "text": f"Lead importer is erroring every run: {imp['diagnosis']}",
        })

    blocked = imp.get("state") in ("blocked", "failing")
    pending = report["lead_gen"].get("pending_push", {})
    for item in pending.get("stale", []):
        cause = ("Blocked by the importer failure above."
                 if blocked else "The Mac importer may not be running.")
        flags.append({
            "level": "alert",
            "text": f"{item['file']} has sat in pending-push for "
                    f"{item['age_hours']}h. {cause}",
        })

    queue = report["distribution_queue"]
    if "error" not in queue and queue["clean_pace_per_day"] < MIN_CLEAN_PACE:
        flags.append({
            "level": "warn",
            "text": f"Clean posting pace is {queue['clean_pace_per_day']}/day "
                    f"over the next 7 days, under the {MIN_CLEAN_PACE} floor "
                    f"(target is a 3/day average).",
        })

    for item in report["context"]["files"]:
        if item.get("error"):
            flags.append({
                "level": "alert",
                "text": f"Context file unreadable: {item['file']} — "
                        f"{item['error']}. Its budget cannot be checked.",
            })
        elif item.get("over_budget"):
            flags.append({
                "level": "warn",
                "text": f"{item['file']} is {item['kib']} KiB (~"
                        f"{item['tokens_est']} tokens), over its "
                        f"{item['budget_kib']} KiB context budget. It is read by "
                        f"agents. Trim it, or move detail to a scoped doc.",
            })

    for key, section in report.items():
        if isinstance(section, dict) and section.get("error"):
            flags.append({
                "level": "alert",
                "text": f"Source unreadable for {key}: "
                        f"{section.get('source', '?')} — {section['error']}",
            })

    return flags


# ── rendering ────────────────────────────────────────────────────────────────

CSS = """
:root{
  --bg:#080808; --panel:#0e0e0e; --line:rgba(255,255,255,.09);
  --ink:#f2f2f2; --dim:rgba(255,255,255,.48); --faint:rgba(255,255,255,.3);
  --orange:#FF9500; --pink:#E040A0; --purple:#7B2FBE;
  --warn:#FFB020; --alert:#FF5C5C; --ok:#3ECF8E;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'DM Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:13px;line-height:1.7;padding:40px 24px 80px}
.wrap{max-width:1080px;margin:0 auto}
h1{font-family:'Syne',system-ui,sans-serif;font-weight:800;font-size:34px;
  letter-spacing:-1px;margin:0 0 6px;color:var(--ink)}
h2{font-family:'Syne',system-ui,sans-serif;font-weight:800;font-size:15px;
  letter-spacing:1.5px;text-transform:uppercase;color:var(--orange);
  margin:44px 0 14px}
.sub{color:var(--dim);font-size:12px;margin-bottom:28px}
.rule{height:3px;border-radius:2px;margin-bottom:32px;
  background:linear-gradient(90deg,var(--orange),var(--pink),var(--purple))}
.panel{background:var(--panel);border:1px solid var(--line);
  border-radius:10px;padding:18px 20px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.stat .n{font-family:'Syne',system-ui,sans-serif;font-weight:800;font-size:28px;
  letter-spacing:-1px;color:var(--orange);display:block;line-height:1.2}
.stat .l{color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:1px}
.src{color:var(--faint);font-size:10.5px;margin-top:10px;word-break:break-all}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;color:var(--faint);font-weight:400;font-size:10.5px;
  text-transform:uppercase;letter-spacing:1px;padding:6px 10px 6px 0;
  border-bottom:1px solid var(--line)}
td{padding:7px 10px 7px 0;border-bottom:1px solid rgba(255,255,255,.045);
  vertical-align:top}
.scroll{overflow-x:auto}
.flag{border-radius:8px;padding:12px 16px;margin-bottom:9px;font-size:12.5px;
  border:1px solid}
.flag.warn{border-color:rgba(255,176,32,.4);background:rgba(255,176,32,.07);color:var(--warn)}
.flag.alert{border-color:rgba(255,92,92,.4);background:rgba(255,92,92,.07);color:var(--alert)}
.flag.ok{border-color:rgba(62,207,142,.35);background:rgba(62,207,142,.06);color:var(--ok)}
.err{color:var(--alert)}
.on{color:var(--ok)} .off{color:var(--faint)}
.foot{color:var(--faint);font-size:11px;margin-top:48px;
  border-top:1px solid var(--line);padding-top:18px}
"""


def kv_table(d: dict) -> str:
    if not d:
        return '<span class="src">nothing recorded</span>'
    rows = "".join(
        f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>"
        for k, v in d.items()
    )
    return f"<table>{rows}</table>"


def section_error(section: dict) -> str:
    return (
        f'<div class="panel"><span class="err">SOURCE MISSING</span> — '
        f'{escape(str(section.get("source", "?")))}: '
        f'{escape(str(section["error"]))}'
        + (f'<div class="src">{escape(section["hint"])}</div>'
           if section.get("hint") else "")
        + "</div>"
    )


def render(report: dict) -> str:
    p: list[str] = []
    a = p.append

    a('<title>Koolestpro System Status</title>')
    a('<link rel="preconnect" href="https://fonts.googleapis.com">')
    a('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    a('<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800'
      '&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">')
    a(f"<style>{CSS}</style>")
    a('<div class="wrap">')
    a("<h1>Koolestpro System Status</h1>")
    a(f'<div class="sub">Generated {escape(report["generated_at"])} by '
      f'<code>.ai-workflow/tools/build_system_status.py</code>. '
      f'Every number below traces to a file. Structure and rules live in '
      f'<code>SYSTEM-MAP.md</code>.</div>')
    a('<div class="rule"></div>')

    # flags
    a("<h2>Needs attention</h2>")
    if not report["flags"]:
        a('<div class="flag ok">Nothing flagged. Every source read cleanly '
          'and no threshold was crossed.</div>')
    for f in report["flags"]:
        a(f'<div class="flag {f["level"]}">{escape(f["text"])}</div>')

    # scheduled tasks
    a("<h2>Scheduled tasks</h2>")
    t = report["scheduled_tasks"]
    if t.get("error"):
        a(section_error(t))
    else:
        a('<div class="grid">')
        a(f'<div class="stat"><span class="n">{t["enabled"]}</span>'
          f'<span class="l">enabled</span></div>')
        a(f'<div class="stat"><span class="n">{t["disabled"]}</span>'
          f'<span class="l">disabled</span></div>')
        a(f'<div class="stat"><span class="n">{len(t["stale"])}</span>'
          f'<span class="l">stale &gt;{STALE_TASK_DAYS}d</span></div>')
        a("</div>")
        def task_row(r: dict) -> str:
            state_cls = "on" if r["enabled"] else "off"
            state_txt = "enabled" if r["enabled"] else "disabled"
            since = "never" if r["days_since"] is None else str(r["days_since"])
            return (
                f'<tr><td>{escape(str(r["id"]))}</td>'
                f'<td class="{state_cls}">{state_txt}</td>'
                f'<td>{escape(str(r["schedule"] or "-"))}</td>'
                f'<td>{escape(since)}</td></tr>'
            )

        rows = "".join(task_row(r) for r in t["tasks"])
        a(f'<div class="panel scroll"><table><tr><th>task</th><th>state</th>'
          f'<th>schedule</th><th>days since run</th></tr>{rows}</table>'
          f'<div class="src">{escape(t["source"])} · snapshot written '
          f'{escape(str(t.get("snapshot_written_at")))}</div></div>')

    # content
    a("<h2>Content pipeline</h2>")
    c = report["content"]
    if c.get("error"):
        a(section_error(c))
    else:
        a('<div class="grid">')
        a(f'<div class="stat"><span class="n">{c["total"]}</span>'
          f'<span class="l">items</span></div>')
        a(f'<div class="stat"><span class="n">{c["idea_backlog"]}</span>'
          f'<span class="l">idea backlog left</span></div>')
        a(f'<div class="stat"><span class="n">{c["months"]}</span>'
          f'<span class="l">months</span></div>')
        a("</div>")
        a(f'<div class="panel"><b>By status</b>{kv_table(c["by_status"])}'
          f'<div class="src">{escape(c["source"])}</div></div>')
        a(f'<div class="panel"><b>By type</b>{kv_table(c["by_type"])}</div>')

    # distribution
    a("<h2>Distribution queue</h2>")
    q = report["distribution_queue"]
    if q.get("error"):
        a(section_error(q))
    else:
        a('<div class="grid">')
        a(f'<div class="stat"><span class="n">{q["total_rows"]}</span>'
          f'<span class="l">rows</span></div>')
        a(f'<div class="stat"><span class="n">{q["clean_pace_per_day"]}</span>'
          f'<span class="l">clean posts/day</span></div>')
        a(f'<div class="stat"><span class="n">{q["overdue_qa_blocked"]}</span>'
          f'<span class="l">overdue, QA-blocked</span></div>')
        a("</div>")
        a(f'<div class="panel"><b>By platform</b>{kv_table(q["by_platform"])}'
          f'<b>By status</b>{kv_table(q["by_status"])}'
          f'<div class="src">{escape(q["source"])} · {escape(q["note"])}</div>'
          f'</div>')

    # prospects
    a("<h2>Prospect pools</h2>")
    tp = report["targets_pool"]
    if tp.get("error"):
        a(section_error(tp))
    else:
        a('<div class="grid">')
        a(f'<div class="stat"><span class="n">{tp["total"]}</span>'
          f'<span class="l">targets</span></div>')
        a(f'<div class="stat"><span class="n">{tp["untouched"]}</span>'
          f'<span class="l">untouched</span></div>')
        a(f'<div class="stat"><span class="n">{tp["unrated_visual"]}</span>'
          f'<span class="l">unrated (unusable)</span></div>')
        a("</div>")
        a(f'<div class="panel"><b>By category</b>{kv_table(tp["by_category"])}'
          f'<div class="src">{escape(tp["source"])}</div></div>')

    lg = report["lead_gen"]
    for key, label in (("ledger", "Taken-brands ledger"),
                       ("pending_push", "Pending push to KoolestFlow")):
        s = lg.get(key, {})
        if s.get("error"):
            a(section_error(s))
        elif key == "ledger":
            a(f'<div class="panel"><b>{label}</b> — '
              f'{s["brands_taken"]} brands already pushed'
              f'<div class="src">{escape(s["source"])}</div></div>')
        else:
            files = ", ".join(s["files"]) or "none"
            a(f'<div class="panel"><b>{label}</b> — {s["queued"]} queued: '
              f'{escape(files)}<div class="src">{escape(s["source"])}</div></div>')

    imp = lg.get("importer", {})
    if imp:
        if imp.get("error"):
            state, detail = "UNKNOWN", imp["error"]
        else:
            state = imp.get("state", "unknown").upper()
            detail = imp.get("diagnosis", "Draining normally.")
        age = imp.get("last_write_age_hours")
        age_txt = f" Last log write {age}h ago." if age is not None else ""
        a(f'<div class="panel"><b>Lead importer</b> — {escape(state)}.'
          f' {escape(detail)}{escape(age_txt)}'
          f'<div class="src">{escape(imp.get("source", ""))}</div></div>')

    # build assets
    a("<h2>Build assets</h2>")
    sc = report["showcase_pages"]
    st = report["store_templates"]
    if sc.get("error"):
        a(section_error(sc))
    else:
        a(f'<div class="panel"><b>Showcase-eligible pages</b> — '
          f'{sc["eligible_unused"]} unused of {sc["total"]} catalogued. '
          f'Next: {escape(", ".join(sc["next_up"]) or "none")}'
          f'<div class="src">{escape(sc["source"])}</div></div>')
    if st.get("error"):
        a(section_error(st))
    else:
        a(f'<div class="panel"><b>Store templates</b> — {st["total"]} built<br>'
          + "<br>".join(escape(v) for v in st["verticals"])
          + f'<div class="src">{escape(st["source"])}</div></div>')

    # spend
    a("<h2>Spend</h2>")
    sp = report["spend"]
    if sp.get("error"):
        a(section_error(sp))
    else:
        body = "".join(
            f"<b>{escape(m)}</b>{kv_table(v)}" for m, v in sp["by_month"].items()
        ) or '<span class="src">nothing recorded</span>'
        a(f'<div class="panel">{body}'
          f'<div class="src">{escape(sp["source"])} · checked before every '
          f'paid call, never after</div></div>')

    # context budget — the prompt-cost surface
    a("<h2>Context budget</h2>")
    ctx = report["context"]
    rows = []
    for item in ctx["files"]:
        if item.get("error"):
            rows.append(
                f'<tr><td>{escape(item["file"])}</td>'
                f'<td class="err">unreadable</td>'
                f'<td>—</td><td>—</td></tr>'
            )
            continue
        state_cls = "err" if item["over_budget"] else "on"
        state_txt = "over budget" if item["over_budget"] else "within"
        rows.append(
            f'<tr><td>{escape(item["file"])}</td>'
            f'<td class="{state_cls}">{state_txt}</td>'
            f'<td>{item["kib"]} / {item["budget_kib"]} KiB</td>'
            f'<td>~{item["tokens_est"]}</td></tr>'
        )
    a('<div class="panel scroll"><table><tr><th>file</th><th>state</th>'
      '<th>size / budget</th><th>est tokens</th></tr>'
      + "".join(rows)
      + '</table>'
      + f'<div class="src">{escape(ctx["source"])} — deliberately slim: these '
      f'are read by agents, so a task pays for them on every run. Flagged the '
      f'moment one regrows.</div></div>')

    a('<div class="foot">Generated file. Do not hand-edit — rerun '
      '<code>build_system_status.py</code> instead. A source this script '
      'cannot read is reported as SOURCE MISSING and never as zero.</div>')
    a("</div>")
    return "\n".join(p)


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    if not (root / "CLAUDE.md").exists():
        print(f"error: {root} does not look like the project root "
              f"(no CLAUDE.md)", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    report = {
        "generated_at": iso(now),
        "project_root": str(root),
        "scheduled_tasks": collect_tasks(root, now),
        "content": collect_content(root),
        "distribution_queue": collect_queue(root, now),
        "targets_pool": collect_targets(root),
        "lead_gen": collect_leads(root, now),
        "showcase_pages": collect_showcase(root),
        "store_templates": collect_store_templates(root),
        "spend": collect_spend(root),
        "context": collect_context(root),
    }
    report["flags"] = build_flags(report)

    (root / "system-status.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    if not args.json_only:
        (root / "SYSTEM-STATUS.html").write_text(render(report), encoding="utf-8")

    alerts = [f for f in report["flags"] if f["level"] == "alert"]
    warns = [f for f in report["flags"] if f["level"] == "warn"]
    print(f"wrote system-status.json"
          + ("" if args.json_only else " and SYSTEM-STATUS.html"))
    print(f"{len(alerts)} alert(s), {len(warns)} warning(s)")
    for f in report["flags"]:
        print(f"  [{f['level']}] {f['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

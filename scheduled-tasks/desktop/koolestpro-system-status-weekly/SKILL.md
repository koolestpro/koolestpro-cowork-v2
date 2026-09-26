---
name: koolestpro-system-status-weekly
description: Regenerates SYSTEM-STATUS.html from real project files every Monday, after the other Monday tasks have settled. Reports state changes; fixes nothing.
---

Regenerate the Koolestpro system status page. You are a fresh session with no memory of prior conversations.

PROJECT: the connected workspace folder "koolestpro-cowork-v2". Read `SYSTEM-MAP.md` at its root first for the structure; `CLAUDE.md` is auto-loaded for the rules.

TIMING: you run Mondays ~09:40, deliberately after `koolestpro-weekly-distribution-assembly` (07:51), `koolestpro-target-pool-refresh` (08:18) and `koolestpro-replo-cache-staleness-check` (08:49), so you read a settled state rather than racing them.

YOUR JOB IS TO REPORT, NOT TO FIX. Do not repair anything you find, do not reschedule rows, do not edit pools, do not re-run other tasks. A status task that also repairs things becomes a task nobody trusts to have told the truth. Report and stop.

STEPS:

1. Write the scheduled-task snapshot. Call the scheduled-tasks tool to list every task, then write `.ai-workflow/scheduled-tasks-snapshot.json` in exactly this shape (the status script cannot read the live task list itself — it lives behind an MCP tool, not on disk, which is the whole reason this snapshot exists):

{
  "_readme": "Snapshot of the live scheduled-task list, written by koolestpro-system-status-weekly immediately before it runs build_system_status.py. Do not hand-edit.",
  "writtenAt": "<ISO timestamp, from `date -u`>",
  "writtenBy": "koolestpro-system-status-weekly",
  "tasks": [ { "taskId": ..., "enabled": ..., "schedule": ..., "cronExpression": ..., "lastRunAt": ..., "nextRunAt": ... }, ... ]
}

Include every task returned, disabled ones too. A disabled task is information, not noise.

2. Run the generator:

    cd <project root> && python3 .ai-workflow/tools/build_system_status.py --project-root .

It writes `SYSTEM-STATUS.html` and `system-status.json` at the project root and prints every flag it raised. Capture the full output, not just the last line.

3. Compare against last week. Read the previous `system-status.json` from git history if available, or note that no prior run exists. What changed state since then? A task that flipped enabled/disabled, a pool that dropped, a pace that moved, a source that started failing. Changes are the interesting part; absolute numbers are already on the page.

4. Report the four loud conditions explicitly, by name, even when they are clear. These are the ones that decay silently and someone needs to see the word "clear" rather than infer it from absence:
   - any enabled scheduled task that has not run in over 14 days
   - `targets_pool` untouched candidates below 4
   - anything sitting in `.ai-workflow/pending-push/` for more than 48 hours (means the Mac launchd importer may have stopped)
   - clean posting pace below 1.5/day against the 3/day average target

5. Any SOURCE MISSING row is an alert, not a footnote. It means a file the system depends on was renamed, moved or corrupted. Name the file and say so plainly.

6. Present `SYSTEM-STATUS.html` in chat with `mcp__cowork__present_files` (load via ToolSearch if deferred), per the project's standing preview rule.

7. Finish with a short plain-text summary: what changed since last week, which of the four conditions are clear and which are not, and anything needing Ridwan's attention. If nothing changed and nothing is flagged, say exactly that in one line rather than padding it.

DO NOT hand-edit `SYSTEM-STATUS.html` or `system-status.json`. They are generated. If a number looks wrong, the bug is in `build_system_status.py` or in the source file, and the right move is to report it rather than patch the output.
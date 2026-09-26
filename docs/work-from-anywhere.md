# Work from anywhere

This project lives in GitHub at **github.com/koolestpro/koolestpro-cowork-v2** (private).
GitHub is the copy every tool can reach. Your Mac is just one place that works on it.

## What is in the repo, and what is not

| In git | Not in git (and why) |
|---|---|
| All rules: `CLAUDE.md`, `AGENTS.md`, `SYSTEM-MAP.md`, `docs/` | `.env` files: secrets. `.env.example` lists every key name. |
| All skills: `.agents/skills/` (Claude reads it through `.claude/skills`) | Rendered video (`.mp4 .mov .gif .webm`): too heavy. They stay on the Mac and Cloudinary. |
| Content system, outputs HTML/PNG/JSON, pools, trackers, tools | `node_modules/`, `.next/`, caches, logs, `.bak` files |
| Desktop scheduled-task prompts: `scheduled-tasks/desktop/` | |
| `site/`, `cold-email-app/`, `replo-rebuilds/` as **submodules** (links to their own repos) | |

Clone with the submodules:

```bash
git clone --recurse-submodules https://github.com/koolestpro/koolestpro-cowork-v2.git
```

## Keeping it current

- **Mac → GitHub:** `scripts/git-sync.sh` runs every hour (launchd job `com.koolestpro.git-sync`). It pulls first, then commits and pushes. Run it by hand before you leave the desk.
- **Anywhere → Mac:** anything you commit elsewhere is pulled on the next hourly run.
- If the same file was edited in two places, sync stops and logs `CONFLICT` in `.ai-workflow/git-sync.log`. Nothing is overwritten.

## Working with each tool

| Where | How |
|---|---|
| **Claude (phone, web, desktop)** | Start a Claude Code session on the repo. `CLAUDE.md` and `.claude/skills/` load automatically. |
| **Codex (chatgpt.com/codex, phone app, CLI)** | Connect GitHub, pick this repo. Codex reads `AGENTS.md`, which points to `CLAUDE.md` and `.agents/skills/`. |
| **Cursor, Windsurf, opencode, Aider, Gemini CLI** | Open the cloned folder. Point the tool at `AGENTS.md`. |
| **Just your phone, no AI** | GitHub mobile app: read any doc, edit markdown, browse outputs. |
| **Secrets on a new machine** | `cp .env.example .env`, then fill in values from your password manager. |

Every tool follows the same rule: change files, commit, push. The Mac picks it up within the hour.

## Mac-only pieces

These still need the Mac awake with KoolestFlow running:

- `import_pending_push.sh` (launchd `com.koolestpro.leadgen-import`, every 30 min) drains `.ai-workflow/pending-push/` into local KoolestFlow.
- Anything that reads `.env` secrets locally.

The project lives at `~/koolestpro-cowork-v2`, not `~/Downloads`. macOS stops background jobs from reading `~/Downloads`, and that is why the importer failed with `Operation not permitted` on every run until 2026-09-26.

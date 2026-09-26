# AGENTS.md

This project's rules live in **`CLAUDE.md`**. Read it first. It holds the four project-wide rules,
the **Task Router**, the quality ratchet, and the generated-copy rules. This file exists so agents
other than Claude (Codex, Cursor, opencode, and anything else) work from the same source of truth
instead of re-deriving it.

## Start here

1. **`CLAUDE.md`** — the rulebook and the Task Router. Read only the router row that matches your
   task; do not read the whole file or other rows.
2. **`SYSTEM-MAP.md`** — what exists, what state it is in, and where a new thing goes.
3. **`docs/system/00-claude-md-archive-2026-09-08.md`** — why a rule exists and what was tried
   before, if you need the history.

Per-task docs are named in the Task Router in `CLAUDE.md`. Key ones:

| Area | Doc |
|---|---|
| CRO post format | `docs/system/cro-3-slide-carousel-format.md` |
| CRO headlines | `docs/system/cro-headline-system.md` |
| CRO rebuild quality bar | `docs/system/cro-redesign-standard.md` |
| Where a rebuild gets made | `docs/system/rebuild-tooling-and-quality.md` |
| The Lovable/Figma input brief | `docs/system/page-build-brief.md` |
| Tool API / sync integration | `docs/system/redesign-tool-api-integration.md` |
| X captions | `docs/system/x-caption-playbook.md` |
| Humanizer routing | `docs/system/humanizer-guideline.md` |
| Monthly build recap | `docs/system/monthly-template-showcase-format.md` |

## Skills and working from anywhere

- **Skills:** every skill this project uses is in `.agents/skills/<name>/SKILL.md` (Claude sees the same
  folder through `.claude/skills`). When a task names a skill, open its `SKILL.md` and follow it.
- **Repo:** github.com/koolestpro/koolestpro-cowork-v2 (private). Clone with `--recurse-submodules`;
  `site/`, `cold-email-app/` and `replo-rebuilds/` are their own repos linked as submodules.
- **Secrets:** never commit `.env`. Key names are in `.env.example`.
- **Finish every session with a commit and push.** The Mac pulls hourly. See `docs/work-from-anywhere.md`.

## Non-negotiables (do not bypass)

- No em dashes in any generated copy.
- Run every piece of copy through the humanizer pipeline (`docs/system/humanizer-guideline.md`).
- X captions under 280 characters, always counted.
- Never fabricate a result, number, quote, or source.
- Never imply a concept brand was a client (KURA, HALOS, MERIDIAN, Lumora).
- Use real brand assets only; never recreate a logo.
- No gradient text (CSS or SVG). Post graphics share one continuous background.
- A rebuild is not postable until its hero product image survives phone size.
- Decide the hero image **after** the plan: use a great site photo if one exists, otherwise generate
  a suitable image with AI and build the page on that. Product pages and homepages alike.
- Never auto-publish. Status stops at `"Created"`.
- Every output HTML includes the "Send to Content Pipeline" button.

## Working in parallel with Claude

- One source of truth per artifact: the content system `#cowork-sync-data` JSON,
  the `docs/system/*` specs, and the `{brand}-social-content.md` / `.json` pairs.
- Do not rewrite a rule in `CLAUDE.md` to fit a task. Follow the router.
- **The operator is Claude Code or Codex, not a human clicking.** Keep every step reachable as an
  MCP tool or a CLI command. Page builds go through the **Lovable MCP server**
  (`https://mcp.lovable.dev`: `create_project` -> `send_message` -> keep private, capture from preview; never publicly deploy a real brand's rebuild), then back
  through `.ai-workflow/tools/capture_page.py`. See `docs/system/redesign-tool-api-integration.md`.
- New page designs come from Lovable / Figma Make / Claude Design (alternatives: v0, Bolt.new, Onlook),
  then get captured with `.ai-workflow/tools/capture_page.py`. See `docs/system/rebuild-tooling-and-quality.md`.

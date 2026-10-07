# Cloud Routines setup (move scheduled tasks off the Mac)

Why: the desktop-app tasks are tied to `/Users/mac/koolestpro-cowork-v2`, so they only run while the Mac is awake, the Claude app is open and the folder is connected (see `07-infrastructure.md`). Routines created through the API start with no repo and no connectors, which is why the "Weekly SEO run" reported success on 2026-10-05 but did nothing. Create them in the claude.ai Routines screen instead, where the repo and connectors can be attached.

## For each task in the table

1. claude.ai/code, Routines, New routine.
2. Repository: `koolestpro/koolestpro-cowork-v2`, branch `main`, allow pushing to `main`.
3. Environment: `koolestpro` (it holds the API keys).
4. Connectors: the ones the task uses (Make, Cloudinary, Lovable, Google Drive, Figma, v0, Gmail are the usual set).
5. Schedule: the time in the table, Africa/Lagos time.
6. Prompt: the block below, with `__NAME__` replaced by the task name.
7. After the first cloud run works, switch the old Mac copy of that task off (keep it, don't delete).

| Task | Lagos time |
|---|---|
| koolestpro-weekly-distribution-assembly | Mon 07:45 |
| koolestpro-target-pool-refresh | Mon 08:09 |
| koolestpro-replo-cache-staleness-check | Mon 08:40 |
| koolestpro-system-status-weekly | Mon 09:40 |
| koolestpro-browseract-weekly | Tue 08:46 |
| koolestpro-adlibrary-weekly | Wed 08:47 |
| koolestpro-weekly-template-build | Wed 09:15 |
| koolestpro-static-ad-weekly | Fri 09:02 |
| koolestpro-tips-weekly | Fri 09:20 |
| koolestpro-template-showcase-weekly | Sat 09:07 |
| koolestpro-weekly-cro-fix | Sun 09:06 |
| koolestpro-distribution-health-check | every 2 days 09:35 |

Also switch off the old duplicate "Koolestpro replo cache staleness check" (it points at the old ~/Downloads path) and the old disabled "Koolestpro adlibrary weekly". The "Weekly SEO run" needs the same fix: recreate it in the Routines screen with `koolestpro-cowork-v2` and the site repo `koolestpro/koolestpro` attached.

## Prompt

```
Scheduled task: __NAME__ (cloud Routine, runs without the Mac)

You are a fresh claude.ai cloud session for Ridwan's koolestpro/koolestpro-cowork-v2 repo. Ridwan moved this task here on 2026-10-07 from the desktop app, where it only ran while his Mac was awake with the project folder connected.

Step 0, setup. cd into the repo checkout (clone https://github.com/koolestpro/koolestpro-cowork-v2 if it is not there). If scripts/cloud-run-start.sh is missing, run `git fetch origin ccr-8e6978ce-nkx7mj && git checkout origin/ccr-8e6978ce-nkx7mj -- scripts/cloud-run-start.sh scripts/cloud-run-finish.sh`. Then run `bash scripts/cloud-run-start.sh`. Work on main: Ridwan approved this Routine committing to and pushing main, because that is how his Mac's hourly git-sync receives the output. If setup fails, stop and start your final message with "FAILED: setup" and the error. Never end a run quietly.

Step 1, the job. Open scheduled-tasks/desktop/__NAME__/SKILL.md and follow it exactly. Read CLAUDE.md first as it instructs. Where it assumes the desktop sandbox: the project folder is the repo root; Chromium and Playwright are preinstalled (PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers), so skip the ARM64 LD_LIBRARY_PATH / bootstrap_env.sh browser-download recipe unless Playwright actually fails; credentials are in .env (written in step 0) and the environment. Anything that genuinely needs the Mac (the launchd lead importer, Mac-only local servers) is not this run's job: leave its queue file for the Mac and say so. Never auto-publish.

Step 2, save. Run `bash scripts/cloud-run-finish.sh __NAME__` to commit and push to main. Never commit .env, never force-push.

Step 3, finish with a short summary: what was produced (file paths), what was skipped and why, and the push result (commit on main, or the fallback branch name).
```

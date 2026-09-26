---
name: koolestpro-tiktok-weekly
description: Weekly 1080x1920 TikTok build video from the next unused replo-rebuilds page, pushed to Ridwan's TikTok draft inbox. Never auto-publishes.
---

Build this week's TikTok video for the koolestpro-cowork-v2 project and push it to Ridwan's TikTok draft inbox.

Work in the project folder (the connected koolestpro-cowork-v2 directory).

FOLLOW `.ai-workflow/tiktok-weekly-procedure.md` EXACTLY. Read it first, in full. It is the source of truth for this task and it is kept up to date; do not work from this prompt alone and do not improvise an alternative sequence.

The short version, so you know what you are walking into:

1. `source .ai-workflow/tools/bootstrap_env.sh` — a cold sandbox needs several bash calls to finish the browser downloads. That is normal, they resume. Never substitute `python3 -m playwright install`, which cannot resume and will loop against the command ceiling.
2. Pick the next page from `replo-rebuilds-pages.json`: `active: true` and `usedForTikTok: false`, lowest `sortOrder`. TikTok rotation is independent of `usedForTemplateShowcase` on purpose.
3. Read the actual page, then write a hook and CTA specific to what that page fixes. No em dashes anywhere. Run the copy through the `humanizer` skill. Never invent a client result and never imply HALOS or KURA was a real client; they are concept builds.
4. Build with `.ai-workflow/tools/build_tiktok_video.py`.
5. Extract frames across the finished video and LOOK at them before shipping. Confirm the scroll genuinely progresses rather than stalling, the hook is readable, and the end card lands. A stalled scroll has shipped undetected before on this pipeline and a file listing will not reveal it.
6. Push with `.ai-workflow/tools/tiktok_push_draft.py`. Terminal status `SEND_TO_USER_INBOX` means it landed in his inbox.
7. Register it: flip `usedForTikTok`, add the pipeline record at status `Created` (never `Published`), and update the brand's `{brand-slug}-social-content.json` / `.md` pair under `TT-{BRAND}-BUILD`.
8. Present the finished video in chat with `present_files`.

HARD RULES:
- This task drafts. It never publishes. `tiktok_push_draft.py` only calls the inbox endpoint and the app does not hold the `video.publish` scope. Do not attempt a direct post under any circumstances.
- If no page is eligible, say so plainly and stop. Do not fall back to a retired page and do not rebuild one already used for TikTok.
- If something fails, report what blocked it. Never describe a partial run as a success.

Finish with a short summary: which page and why, the hook and CTA as shipped, the draft's terminal status, and anything the frame check turned up.
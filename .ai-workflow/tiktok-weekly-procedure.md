# TikTok weekly build + draft — procedure

The `koolestpro-tiktok-weekly` scheduled task follows this file. The task prompt points
here rather than duplicating the steps, so edits made here apply to the next run
automatically. Same pattern as `.ai-workflow/weekly-pipeline.md` for CRO Fix.

## What this stream is

One 1080x1920 "watch a store get built" video per week, pushed to Ridwan's TikTok draft
inbox. He reviews and posts it himself from the TikTok app.

This is the format that actually produced clients. Jellys Glamour came from the DMs after
seeing TikTok build videos, plus two foreign PageFly clients from the same format. It is a
service signal, not a craft signal, which is exactly the correction recorded at the top of
`CLAUDE.md`.

**Never auto-publish to TikTok.** `tiktok_push_draft.py` only ever calls the inbox
endpoint. The `video.publish` scope is deliberately not held, and the 2026-08-19 app
rejection is not a blocker for drafts. Verified 2026-09-07: sandbox `video.upload` works
without production review.

## Steps

### 1. Environment

```bash
source .ai-workflow/tools/bootstrap_env.sh
```

Cold sandboxes need several calls to finish the browser download. That is expected; the
downloads resume. Do not switch to `python3 -m playwright install`, which cannot resume
and will loop forever against the command ceiling.

### 2. Pick the page

Read `replo-rebuilds-pages.json`. Eligible entries are `active: true` and
`usedForTikTok: false`; take the lowest `sortOrder`.

TikTok rotation is deliberately independent of `usedForTemplateShowcase`. A page already
used for a showcase is still fine here: different format, different platform, different
audience. Only `usedForTikTok` gates this stream.

If nothing is eligible, say so plainly in the summary and stop. Do not fall back to a
retired KURA page silently, and do not rebuild a page already used for TikTok.

### 3. Write the hook and CTA

Read the actual page first. The hook names the specific thing that page fixes, not a
generic line. "This PDP was losing the sale above the fold" is a hook; "check out this
redesign" is not.

Rules that apply, all from `CLAUDE.md`:

- No em dashes. `build_tiktok_video.py` enforces this and will refuse to build.
- Run the copy through the `humanizer` skill before using it.
- Never invent a client result, and never imply a concept brand was a client. HALOS and
  KURA are concept builds. The CTA offers a rebuild; it does not claim one happened.
- CTA points at the free-rebuild offer, matching the Template Showcase "need a store
  built" framing rather than a CRO audit framing.

### 4. Build

```bash
python3 .ai-workflow/tools/build_tiktok_video.py \
  <sourcePath from the manifest> --file --slug <showcaseSlug> \
  --hook "..." --cta "..." --endcard "..."
```

Output lands in `outputs/tiktok/<slug>/`. `--duration` defaults to 26 and behaves as a
floor rather than a promise: the capture is externally stepped, so a heavy page overruns
it. Read the duration the script prints instead of assuming.

### 5. Look at it before shipping it

Non-negotiable, same discipline as every other stream here. Extract frames across the
timeline and actually look at them:

```bash
for t in 1 8 16 24; do ffmpeg -v error -ss $t -i <video> -frames:v 1 /tmp/f$t.png -y; done
```

Check the scroll genuinely progresses rather than stalling, the hook card is readable, the
status bar and bezel render, and the end card lands. A stalled scroll has shipped before
on the video pipeline and it is invisible in a file listing.

### 6. Push the draft

```bash
python3 .ai-workflow/tools/tiktok_push_draft.py outputs/tiktok/<slug>/<slug>_tiktok.mp4 \
  --source tiktok-weekly --title "<the hook>"
```

Terminal status `SEND_TO_USER_INBOX` means it landed. The tool refreshes the token itself
and skips a file already drafted, so a re-run is safe.

### 7. Register it

- Mark `usedForTikTok: true` and set `usedForTikTokDate` in `replo-rebuilds-pages.json`.
- Add a pipeline record to `SYNC_DATA.items` in `ridwan_content_system_updated.html`,
  type `Tip` unless a better existing type fits, status `Created`, never `Published`.
  Populate `captions` and `assets`.
- Add the caption to the brand's `{brand-slug}-social-content.json` / `.md` pair under
  `TT-{BRAND}-BUILD`, keeping both files in step.

### 8. Present it

Per the standing rule, present the finished video in chat with `present_files` so Ridwan
can check it without opening the outputs folder.

## Summary to leave behind

Which page was used and why, the hook and CTA as shipped, the draft's terminal status, and
anything that looked wrong in the frame check. If nothing shipped, say what blocked it
rather than reporting a partial run as a success.

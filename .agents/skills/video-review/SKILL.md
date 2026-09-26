---
name: video-review
description: Gives Claude the ability to actually watch and analyze a video — download it from a URL (YouTube, Instagram, X/Twitter, TikTok, Vimeo, Loom, and ~1800 other sites via yt-dlp) or read a local file, pull a timestamped transcript, extract sampled frames, and study pacing, hooks, cuts, and structure. Use this whenever the user wants to reverse-engineer the editing style of a reference video ("how did they open this", "what's the hook here", "how are the cuts paced"), QA their own video before publishing, compare two videos' structure, or otherwise asks Claude to "watch," "review," or "analyze" a video by URL or file path. Also trigger on requests like "what happens at the 30 second mark" or "pull the transcript of this video" even if the word "review" isn't used. This is the Cowork-native counterpart to a terminal-only /watch skill — it works standalone in the sandbox with no globally-installed CLI tools required.
---

# Video Review

## Why this exists

Without this skill, Claude can only guess at a video's content from its title, thumbnail, or whatever the user describes. This skill lets Claude actually look at it: real frames sampled across the timeline, plus a timestamped transcript, so feedback and analysis are grounded in what's actually on screen and said — not assumptions.

## How to use it

1. Run the bundled script to download/prepare the video:

   ```bash
   python3 scripts/prepare_video.py "<url-or-local-path>" --outdir /tmp/video_review
   ```

   - Accepts a URL (yt-dlp handles YouTube, Instagram, X, TikTok, Vimeo, Loom, and most other video sites) or a local file path.
   - Downloads at up to 720p / 300MB to keep things fast — this is for analysis, not archival quality.
   - Tries to pull existing captions first (free, usually accurate). Only falls back to Whisper transcription if `GROQ_API_KEY` or `OPENAI_API_KEY` is set in the environment — if neither is set and there are no captions, it proceeds on frames alone and says so in the manifest. Don't treat a missing transcript as a failure; tell the user what happened and keep going with visual analysis, or ask if they want to provide a key.
   - Extracts one frame every 5 seconds by default (`--frame-interval`). Use a smaller interval (e.g. 2) for fast-cut content where pacing is the whole question, or a larger one (e.g. 10-15) for long-form content where you mainly need coverage.
   - Prints and saves a `manifest.json` with the paths to everything it produced.

2. Read `transcript.txt` (if produced) with the Read tool — it's plain text formatted as `[mm:ss] line`.

3. Read the frames in `frames/` **in timestamp order** using the Read tool (they're named `frame_00m05s.jpg`, `frame_00m10s.jpg`, etc., so the order is obvious). You don't need to read every single frame for a long video — sample enough to answer the specific question (e.g. read the first 10-15 frames densely if the question is about the hook/opening, or spread reads across the timeline if the question is about overall pacing).

4. Answer the user's actual question by cross-referencing frames and transcript timestamps together — e.g. "the hook lands at 0:03 with a jump cut to a close-up, backed by the line '[00:02] wait, this actually worked' — that's a pattern-interrupt open." Cite timestamps so the user can verify by scrubbing to that point themselves.

5. Clean up the working directory (`rm -rf` the `--outdir`) once you're done, since it can hold a few hundred MB of video/frames — no reason to leave that sitting in the sandbox.

## Common use cases and what to focus on

**Reverse-engineering a reference video's style** ("point me at a video and tell me how they paced it"): focus on the first 10-15 seconds frame-by-frame (hooks live or die there), then note the cut frequency and any pattern shifts (e.g. slows down for the demo, speeds up for the CTA).

**QA'ing the user's own video before publishing**: read the transcript for pacing/filler, check frames for anything visually off (bad crop, dead air implied by a static frame lasting many samples, captions cut off, etc.), and flag anything before they publish it.

**Comparing two videos**: run the script twice (separate `--outdir`s), then read both transcripts/frame sets before comparing.

**"What happens at timestamp X"**: you can skip extracting all frames and instead grab just the frame(s) near that timestamp with a targeted ffmpeg call (`ffmpeg -ss <time> -i video.mp4 -frames:v 1 out.jpg`) if the full extraction would be overkill — use judgment on when the lighter-weight approach is enough.

## Dependencies

- `ffmpeg` — used directly, expected to already be on PATH in the Cowork sandbox.
- `yt-dlp` — the script installs it automatically via pip on first use if missing (only needed for URL sources, not local files).
- `GROQ_API_KEY` or `OPENAI_API_KEY` (optional) — only needed as a transcription fallback when a video has no existing captions. Not required for the skill to work at all.

#!/usr/bin/env python3
"""
Downloads (or reads a local) video, pulls a timestamped transcript, and extracts
representative frames so Claude can review pacing, hooks, and structure without
guessing from a title or thumbnail.

Usage:
    python3 prepare_video.py <url-or-local-path> [--outdir DIR] [--frame-interval SECONDS]

Produces, inside --outdir (default: ./video_review_<timestamp>):
    video.mp4            - the source video (copied/downloaded)
    transcript.txt        - timestamped transcript, if one could be obtained
    frames/frame_XXXXs.jpg - sampled stills, named by timestamp
    manifest.json          - paths + metadata + what worked/what didn't

Design notes for whoever reads this later:
- Captions are tried first (free, usually good enough) before falling back to
  Whisper-style transcription, because most public videos already have them
  and there's no reason to spend API credits re-deriving what YouTube/etc
  already generated.
- Frames are sampled on a fixed interval rather than full scene-detection by
  default, because scene-detection filters are slow on longer videos and the
  fixed interval is good enough for pacing/hook analysis. Pass
  --frame-interval to tune density (lower = more frames = better for fast-cut
  analysis, higher = fewer frames = faster for long videos).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time


def run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


# Invoke yt-dlp as "python3 -m yt_dlp" rather than the bare "yt-dlp" binary.
# pip installs it under the interpreter's user script dir, which isn't
# guaranteed to be on PATH in a fresh sandbox — going through -m sidesteps
# that entirely since it uses the same interpreter that just installed it.
# --js-runtimes node: YouTube's extractor needs a JS runtime to solve
# signature challenges. yt-dlp only auto-enables deno, which usually isn't
# installed in the sandbox, but node is (Cowork ships it) — telling yt-dlp
# to use node gets YouTube downloads working without installing anything.
YT_DLP_CMD = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node"]


def ensure_yt_dlp():
    r = run(YT_DLP_CMD + ["--version"])
    if r.returncode == 0:
        return True
    print("yt-dlp not found, installing...", file=sys.stderr)
    r = run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "yt-dlp"])
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return False
    return run(YT_DLP_CMD + ["--version"]).returncode == 0


def is_url(s):
    return s.startswith("http://") or s.startswith("https://")


def download_video(url, outdir):
    video_path = os.path.join(outdir, "video.mp4")
    cmd = YT_DLP_CMD + [
        "-f", "best[height<=720][ext=mp4]/best[height<=720]/best",
        "--max-filesize", "300M",
        "-o", video_path,
        url,
    ]
    r = run(cmd)
    if r.returncode != 0 or not os.path.exists(video_path):
        return None, r.stderr
    return video_path, None


def try_download_captions(url, outdir):
    """Try manual subs first, then auto-generated. Returns path to a .vtt or None."""
    for sub_flag in ("--write-subs", "--write-auto-subs"):
        base = os.path.join(outdir, "captions")
        cmd = YT_DLP_CMD + [
            sub_flag,
            "--sub-lang", "en.*,en",
            "--skip-download",
            "--convert-subs", "vtt",
            "-o", base,
            url,
        ]
        run(cmd)
        for f in os.listdir(outdir):
            if f.startswith("captions") and f.endswith(".vtt"):
                return os.path.join(outdir, f)
    return None


def vtt_to_transcript(vtt_path, txt_path):
    """Collapse a .vtt file into a simple '[mm:ss] line' transcript."""
    import re
    lines_out = []
    with open(vtt_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()
    blocks = re.split(r"\n\n+", content)
    seen = set()
    for block in blocks:
        m = re.search(r"(\d{2}:\d{2}:\d{2})\.\d+ --> ", block)
        if not m:
            continue
        ts = m.group(1)
        mm_ss = ":".join(ts.split(":")[1:])  # drop hours if 0, keep mm:ss-ish
        text_lines = [l.strip() for l in block.splitlines() if "-->" not in l and l.strip()]
        text = " ".join(text_lines).strip()
        text = re.sub(r"<[^>]+>", "", text)  # strip inline vtt tags
        if text and text not in seen:
            seen.add(text)
            lines_out.append(f"[{mm_ss}] {text}")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out))
    return len(lines_out) > 0


def extract_audio(video_path, outdir):
    audio_path = os.path.join(outdir, "audio.mp3")
    run(["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-q:a", "4", audio_path])
    return audio_path if os.path.exists(audio_path) else None


def whisper_fallback(audio_path, txt_path):
    """Use Groq's Whisper endpoint if GROQ_API_KEY is set, else OpenAI's if
    OPENAI_API_KEY is set. Returns True if a transcript was written."""
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if groq_key:
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        key = groq_key
        model = "whisper-large-v3-turbo"
    elif openai_key:
        url = "https://api.openai.com/v1/audio/transcriptions"
        key = openai_key
        model = "whisper-1"
    else:
        return False
    cmd = [
        "curl", "-s", url,
        "-H", f"Authorization: Bearer {key}",
        "-F", f"file=@{audio_path}",
        "-F", f"model={model}",
        "-F", "response_format=verbose_json",
    ]
    r = run(cmd)
    if r.returncode != 0 or not r.stdout:
        return False
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return False
    segments = data.get("segments")
    if not segments:
        return False
    lines_out = []
    for seg in segments:
        start = int(seg.get("start", 0))
        mm, ss = divmod(start, 60)
        lines_out.append(f"[{mm:02d}:{ss:02d}] {seg.get('text', '').strip()}")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out))
    return True


def extract_frames(video_path, frames_dir, interval):
    os.makedirs(frames_dir, exist_ok=True)
    pattern = os.path.join(frames_dir, "frame_%05d.jpg")
    run([
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "3",
        pattern,
    ])
    frames = sorted(os.listdir(frames_dir))
    # rename to timestamp-based names so Claude can read them in order with context
    renamed = []
    for i, fname in enumerate(frames):
        ts = i * interval
        mm, ss = divmod(ts, 60)
        new_name = f"frame_{mm:02d}m{ss:02d}s.jpg"
        os.rename(os.path.join(frames_dir, fname), os.path.join(frames_dir, new_name))
        renamed.append(new_name)
    return renamed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="URL (YouTube/IG/X/TikTok/Vimeo/Loom/etc via yt-dlp) or local file path")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--frame-interval", type=int, default=5, help="seconds between sampled frames")
    args = ap.parse_args()

    outdir = args.outdir or f"video_review_{int(time.time())}"
    os.makedirs(outdir, exist_ok=True)

    manifest = {"source": args.source, "outdir": outdir}

    if is_url(args.source):
        if not ensure_yt_dlp():
            manifest["error"] = "yt-dlp not available and install failed"
            print(json.dumps(manifest, indent=2))
            sys.exit(1)

        vtt = try_download_captions(args.source, outdir)
        transcript_path = os.path.join(outdir, "transcript.txt")
        if vtt and vtt_to_transcript(vtt, transcript_path):
            manifest["transcript_source"] = "captions"
        else:
            manifest["transcript_source"] = None

        video_path, err = download_video(args.source, outdir)
        if not video_path:
            manifest["error"] = f"download failed: {err}"
            print(json.dumps(manifest, indent=2))
            sys.exit(1)
        manifest["video_path"] = video_path
    else:
        if not os.path.exists(args.source):
            manifest["error"] = "local file not found"
            print(json.dumps(manifest, indent=2))
            sys.exit(1)
        video_path = os.path.join(outdir, "video" + os.path.splitext(args.source)[1])
        shutil.copy(args.source, video_path)
        manifest["video_path"] = video_path
        manifest["transcript_source"] = None

    # Whisper fallback if no captions were found
    transcript_path = os.path.join(outdir, "transcript.txt")
    if manifest.get("transcript_source") is None:
        audio_path = extract_audio(video_path, outdir)
        if audio_path and whisper_fallback(audio_path, transcript_path):
            manifest["transcript_source"] = "whisper"
        else:
            manifest["transcript_source"] = None
            manifest["transcript_note"] = (
                "No captions found and no GROQ_API_KEY/OPENAI_API_KEY set for Whisper "
                "fallback. Proceeding on frames only unless a key is provided."
            )

    frames_dir = os.path.join(outdir, "frames")
    frames = extract_frames(video_path, frames_dir, args.frame_interval)
    manifest["frames_dir"] = frames_dir
    manifest["frame_count"] = len(frames)
    manifest["transcript_path"] = transcript_path if os.path.exists(transcript_path) else None

    manifest_path = os.path.join(outdir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

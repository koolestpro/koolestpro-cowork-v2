#!/usr/bin/env python3
"""
build_tiktok_video.py — turn any built page into a 1080x1920 TikTok build video.

Why this exists
---------------
The TikTok stream's original prototypes (build_v3.py, waypoint_scroll_capture.py,
the v3-v7 mockups in outputs/tiktok_mockup/) are GONE from this project — only the
docs still reference them. Rather than resurrect five one-off prototype styles,
this rebuilds the one format that actually earned clients: the silent "watch a
store get built" scroll video (Jellys Glamour plus two PageFly clients came from
exactly this, see CLAUDE.md's client-history section).

It deliberately reuses the page-presentation-kit scripts already proven in this
project instead of inventing new capture tooling:

    scroll_video_raw.py   real mobile-viewport scroll capture, externally stepped
                          so a page-thread stall cannot cause the stall-then-jump
                          bug fixed on 2026-07-31
    frame_video.py mobile real calibrated iPhone bezel + notch-flanking status bar,
                          here at a 1080x1920 canvas instead of the 1080x1350 the
                          Template Showcase uses

On top of that it burns in a hook card, a persistent handle chip, and a CTA end
card, using the real brand fonts in assets/fonts.

Project rules honoured
----------------------
- No em dashes in any burned-in copy. The check is enforced, not advisory.
- Hook and CTA text is passed in, never invented here. Write it upstream and run
  it through the humanizer skill first.
- Output is a draft candidate. It never posts anything by itself; hand the file
  to tiktok_push_draft.py, which only ever writes to the draft inbox.

Usage
-----
    python3 build_tiktok_video.py replo-rebuilds/brands/halos/pages/halos-pdp-01/index.html \\
        --file --slug halos_pdp-01 \\
        --hook "This PDP was losing the sale above the fold" \\
        --cta "Free rebuild of your page. DM me FIX"

    python3 build_tiktok_video.py https://example.com --slug example_hp --hook "..." --cta "..."
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
ORANGE = (255, 149, 0)
PURPLE = (123, 47, 190)
INK = (10, 10, 12)

HOOK_IN, HOOK_OUT = 0.3, 4.0
ENDCARD_SECONDS = 4.0


def find_root(start="."):
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / "CLAUDE.md").exists():
            return cand
    return p


ROOT = find_root(os.environ.get("KP_ROOT", "."))
PPK = ROOT / ".ai-workflow" / "skills" / "page-presentation-kit" / "scripts"
FONTS = ROOT / "assets" / "fonts"


def font(name, size):
    path = FONTS / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    for fallback in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(fallback):
            return ImageFont.truetype(fallback, size)
    return ImageFont.load_default()


def syne(size):
    return font("Syne-Variable.ttf", size)


def mono(size):
    return font("DMMono-Medium.ttf", size)


def run(cmd, **kw):
    print("  $ " + " ".join(str(c) for c in cmd[:6]) + (" ..." if len(cmd) > 6 else ""))
    proc = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout[-2000:] + "\n" + proc.stderr[-2000:] + "\n")
        raise SystemExit(f"command failed: {cmd[0]}")
    return proc.stdout


def probe_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", path])
    return float(out.strip())


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def make_hook_png(text, out_path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fnt = syne(74)
    pad, max_w = 64, W - 200
    lines = wrap(d, text, fnt, max_w)
    line_h = 92
    block_h = len(lines) * line_h + pad * 2
    top = 150
    rounded(d, (56, top, W - 56, top + block_h), 34, (10, 10, 12, 224))
    d.rounded_rectangle((56, top, 66, top + block_h), radius=6, fill=ORANGE + (255,))
    y = top + pad
    for line in lines:
        d.text((100, y), line, font=fnt, fill=(255, 255, 255, 255))
        y += line_h
    img.save(out_path)


def make_handle_png(handle, out_path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fnt = mono(34)
    text = handle
    tw = d.textlength(text, font=fnt)
    x0, y0 = 56, H - 150
    rounded(d, (x0, y0, x0 + tw + 60, y0 + 68), 34, (10, 10, 12, 200))
    d.ellipse((x0 + 20, y0 + 27, x0 + 34, y0 + 41), fill=ORANGE + (255,))
    d.text((x0 + 46, y0 + 17), text, font=fnt, fill=(255, 255, 255, 230))
    img.save(out_path)


def _glow(color, radius, peak_alpha):
    """A soft radial blob. Built tiny then upscaled, which is both far faster
    than per-pixel work and naturally smooth."""
    small = 96
    mask = Image.new("L", (small, small), 0)
    md = ImageDraw.Draw(mask)
    steps = 48
    for i in range(steps):
        t = i / steps
        r = int(small / 2 * (1 - t))
        a = int(peak_alpha * (t ** 1.6))
        md.ellipse((small / 2 - r, small / 2 - r, small / 2 + r, small / 2 + r), fill=a)
    mask = mask.resize((radius * 2, radius * 2), Image.LANCZOS)
    blob = Image.new("RGBA", (radius * 2, radius * 2), color + (0,))
    blob.putalpha(mask)
    return blob


def make_endcard_png(headline, cta, handle, out_path):
    img = Image.new("RGBA", (W, H), INK + (246,))

    # Brand glow blobs, built on their own layer and alpha-composited. Drawing
    # translucent lines straight onto an RGBA image REPLACES the pixels instead
    # of blending them, which is what turned the first cut of this end card into
    # two hard-edged colour bands.
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for color, center, radius, peak in (
        (ORANGE, (140, 220), 900, 150),
        (PURPLE, (W - 120, H - 260), 1000, 130),
    ):
        wash.alpha_composite(_glow(color, radius, peak),
                             (center[0] - radius, center[1] - radius))
    wash = wash.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img, wash)

    d = ImageDraw.Draw(img)

    head_f = syne(86)
    lines = wrap(d, headline, head_f, W - 200)
    total = len(lines) * 108
    y = (H // 2) - total // 2 - 140
    for line in lines:
        d.text((100, y), line, font=head_f, fill=(255, 255, 255, 255))
        y += 108

    cta_f = syne(52)
    cta_lines = wrap(d, cta, cta_f, W - 260)
    box_h = len(cta_lines) * 70 + 56
    by = y + 80
    rounded(d, (100, by, W - 100, by + box_h), 30, ORANGE + (255,))
    cy = by + 28
    for line in cta_lines:
        tw = d.textlength(line, font=cta_f)
        d.text(((W - tw) / 2, cy), line, font=cta_f, fill=(12, 8, 4, 255))
        cy += 70

    hf = mono(38)
    tw = d.textlength(handle, font=hf)
    d.text(((W - tw) / 2, by + box_h + 60), handle, font=hf, fill=(255, 255, 255, 190))
    img.save(out_path)


def assert_no_em_dash(*texts):
    bad = [t for t in texts if t and ("—" in t or "&mdash;" in t)]
    if bad:
        raise SystemExit(
            "em dash found in burned-in copy (project-wide rule, CLAUDE.md): "
            + " | ".join(bad)
        )


def build(args):
    root = ROOT
    slug = args.slug
    out_dir = Path(args.out_dir) if args.out_dir else root / "outputs" / "tiktok" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / f"{slug}_tiktok.mp4"

    assert_no_em_dash(args.hook, args.cta, args.endcard or "")

    tmp = Path(tempfile.mkdtemp(prefix="tt_"))
    raw = tmp / "raw.webm"
    framed = tmp / "framed.mp4"

    print("1/4 capturing mobile scroll")
    # scroll_video_raw builds a file:// URL by concatenation, so a relative path
    # silently becomes an invalid URL rather than an obvious error.
    target = str(Path(args.target).resolve()) if args.file else args.target
    cmd = [sys.executable, PPK / "scroll_video_raw.py", target, raw,
           "--width", 390, "--height", 855, "--duration", args.duration]
    if args.file:
        cmd.append("--file")
    run(cmd, cwd=root)

    print("2/4 compositing into the iPhone bezel at 1080x1920")
    run([sys.executable, PPK / "frame_video.py", "mobile", "--video", raw,
         "--output", framed, "--width", W, "--height", H], cwd=root)

    print("3/4 drawing overlays")
    hook_png, handle_png, end_png = tmp / "hook.png", tmp / "handle.png", tmp / "end.png"
    make_hook_png(args.hook, hook_png)
    make_handle_png(args.handle, handle_png)
    make_endcard_png(args.endcard or args.hook, args.cta, args.handle, end_png)

    dur = probe_duration(framed)
    end_at = max(dur - ENDCARD_SECONDS, 1.0)

    print("4/4 encoding")
    inputs = ["-i", str(framed), "-i", str(hook_png), "-i", str(handle_png), "-i", str(end_png)]
    chain = (
        "[0:v][1:v]overlay=0:0:enable='between(t,{hi},{ho})'[a];"
        "[a][2:v]overlay=0:0[b];"
        "[b][3:v]overlay=0:0:enable='gte(t,{ea})'[v]"
    ).format(hi=HOOK_IN, ho=HOOK_OUT, ea=end_at)

    maps = ["-map", "[v]"]
    audio_args = []
    if args.music and os.path.exists(args.music):
        inputs += ["-i", args.music]
        chain += f";[4:a]volume=0.16,afade=t=out:st={dur-2:.2f}:d=2,atrim=0:{dur:.2f}[m]"
        maps += ["-map", "[m]"]
        audio_args = ["-c:a", "aac", "-b:a", "128k", "-shortest"]
    elif args.music:
        print(f"  music file not found, continuing silent: {args.music}")

    run(["ffmpeg", "-y", *inputs, "-filter_complex", chain, *maps,
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
         "-profile:v", "high", "-crf", "20", *audio_args, str(final)])

    shutil.rmtree(tmp, ignore_errors=True)

    meta = {
        "slug": slug,
        "target": args.target,
        "hook": args.hook,
        "cta": args.cta,
        "handle": args.handle,
        "video": str(final.relative_to(root)),
        "durationSec": round(probe_duration(final), 2),
        "resolution": f"{W}x{H}",
        "builtAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "postedTo": None,
    }
    (out_dir / f"{slug}_tiktok.json").write_text(json.dumps(meta, indent=2))

    size_mb = final.stat().st_size / 1048576
    print(f"\nSaved: {final.relative_to(root)}  "
          f"({meta['durationSec']}s, {size_mb:.1f}MB, {W}x{H})")
    print("Next: python3 .ai-workflow/tools/tiktok_push_draft.py "
          f"{final.relative_to(root)} --source tiktok-build --title \"{args.hook[:60]}\"")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build a 1080x1920 TikTok build video from a page.")
    ap.add_argument("target", help="URL, or a local path with --file")
    ap.add_argument("--file", action="store_true", help="target is a local file path")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--hook", required=True, help="opening on-screen line, humanized upstream")
    ap.add_argument("--cta", required=True, help="end-card call to action")
    ap.add_argument("--endcard", help="end-card headline, defaults to the hook")
    ap.add_argument("--handle", default="@koolestpro")
    ap.add_argument("--duration", type=float, default=26.0, help="scroll capture seconds")
    ap.add_argument("--music", help="optional background track, mixed low")
    ap.add_argument("--out-dir")
    args = ap.parse_args()
    return build(args)


if __name__ == "__main__":
    sys.exit(main())

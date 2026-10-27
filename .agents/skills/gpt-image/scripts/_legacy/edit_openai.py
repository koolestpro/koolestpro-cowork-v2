#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=2.0.0"]
# ///
"""
gpt-image edit — image editing using gpt-image-2.

Supports single-image and multi-image (up to 10) inputs for style transfer,
compositing, virtual try-on, object removal, scene insertion, and more.

Run with: uv run edit.py --prompt "..." --images file1.png [file2.png ...] [options]

Options:
    --prompt TEXT               Required. The editing instruction.
    --model MODEL               GPT Image model. Default: gpt-image-2
    --images PATH [PATH ...]    Required. 1-16 input image paths.
    --output PATH               Output file path. Default: output.<format>
    --size WxH|auto             Output size. Default: 1024x1024
    --quality low|medium|high|auto  Output quality. Default: medium
    --output-format png|jpeg|webp   Output file format. Default: png
    --output-compression INT    Compression 0-100 (jpeg/webp only).
    --n INT                     Number of variants (1-4). Default: 1
    --env-file PATH             Path to .env file with OPENAI_API_KEY.
"""

import argparse
import base64
import os
import sys


DEFAULT_MODEL = "gpt-image-2"
GPT_IMAGE_MODELS = ("gpt-image-2", "gpt-image-1.5", "gpt-image-1", "gpt-image-1-mini")
LEGACY_SIZES = ("1024x1024", "1024x1536", "1536x1024", "auto")


def load_env(env_path):
    """Load key=value pairs from a .env file into os.environ."""
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key not in os.environ or is_placeholder_key(os.environ[key]):
                os.environ[key] = value


def is_placeholder_key(value):
    return value.strip() in {"", "sk-...", "sk-your-key-here"}


def validate_size(size_str, model):
    """Validate size for the selected GPT Image model."""
    if size_str.strip().lower() == "auto":
        return "auto"

    if model != "gpt-image-2":
        normalized = size_str.strip().lower()
        if normalized not in LEGACY_SIZES:
            allowed = ", ".join(LEGACY_SIZES)
            raise ValueError(f"{model} only supports these sizes: {allowed}.")
        return normalized

    try:
        w, h = map(int, size_str.lower().split("x"))
    except ValueError:
        raise ValueError(f"Invalid size format '{size_str}'. Use WxH (e.g. 1024x1024) or 'auto'.")

    errors = []
    if w % 16 != 0 or h % 16 != 0:
        errors.append(f"Both dimensions must be multiples of 16. Got {w}x{h}.")
    if max(w, h) > 3840:
        errors.append(f"Max edge must be ≤ 3840px. Got {max(w, h)}.")
    if max(w, h) / min(w, h) > 3:
        errors.append(f"Aspect ratio must be ≤ 3:1. Got {w}:{h}.")
    total = w * h
    if total > 8_294_400:
        errors.append(f"Total pixels must be ≤ 8,294,400. Got {total:,}.")
    if total < 655_360:
        errors.append(f"Total pixels must be ≥ 655,360. Got {total:,}.")
    if errors:
        raise ValueError("Size validation failed:\n  " + "\n  ".join(errors))
    if total > 3_686_400:
        print(f"⚠  Size {w}x{h} ({total:,}px) exceeds 2K — results may be more variable.", file=sys.stderr)
    return f"{w}x{h}"


def main():
    parser = argparse.ArgumentParser(description="Edit images with gpt-image-2")
    parser.add_argument("--prompt", required=True, help="Editing instruction prompt")
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=GPT_IMAGE_MODELS, help=f"GPT Image model (default: {DEFAULT_MODEL})")
    parser.add_argument("--images", required=True, nargs="+", help="Input image path(s), 1-16 files")
    parser.add_argument("--output", default=None, help="Output file path (default: output.<format>)")
    parser.add_argument("--size", default="1024x1024", help="Output size WxH or 'auto' (default: 1024x1024)")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto"], help="Output quality")
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"], help="Output file format")
    parser.add_argument("--output-compression", type=int, default=None, help="Compression 0-100 (jpeg/webp only)")
    parser.add_argument("--n", type=int, default=1, choices=[1, 2, 3, 4], help="Number of variants (1-4)")
    parser.add_argument("--env-file", default=None, help="Path to .env file")
    args = parser.parse_args()

    # Validate size early (no API key needed)
    try:
        size = validate_size(args.size, args.model)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate output_compression
    if args.output_compression is not None:
        if args.output_format == "png":
            print("ERROR: --output-compression only valid with jpeg or webp (not png).", file=sys.stderr)
            sys.exit(1)
        if not 0 <= args.output_compression <= 100:
            print(f"ERROR: --output-compression must be 0-100. Got {args.output_compression}.", file=sys.stderr)
            sys.exit(1)

    # Validate image count
    if len(args.images) > 16:
        print("ERROR: Maximum 16 input images allowed.", file=sys.stderr)
        sys.exit(1)

    # Validate images exist
    for img_path in args.images:
        if not os.path.exists(img_path):
            print(f"ERROR: Image not found: {img_path}", file=sys.stderr)
            sys.exit(1)

    # Default --output to output.<format> if not provided
    if args.output is None:
        ext_map = {"png": "png", "jpeg": "jpg", "webp": "webp"}
        args.output = f"output.{ext_map[args.output_format]}"

    # Load .env
    if args.env_file:
        env_path = args.env_file
    else:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    load_env(env_path)

    if not os.environ.get("OPENAI_API_KEY") or is_placeholder_key(os.environ["OPENAI_API_KEY"]):
        print("ERROR: OPENAI_API_KEY not found. Add it to .env or export it.", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI()

    print(f"Editing with {args.model} using {len(args.images)} input image(s) at {size}, quality={args.quality}, format={args.output_format}...")
    for i, p in enumerate(args.images, 1):
        print(f"  Image {i}: {p}")

    image_files = [open(p, "rb") for p in args.images]

    try:
        kwargs = {
            "model": args.model,
            "image": image_files,
            "prompt": args.prompt,
            "size": size,
            "quality": args.quality,
            "output_format": args.output_format,
        }
        if args.output_compression is not None:
            kwargs["output_compression"] = args.output_compression
        if args.n > 1:
            kwargs["n"] = args.n

        result = client.images.edit(**kwargs)
    finally:
        for fh in image_files:
            fh.close()

    base, ext = os.path.splitext(args.output)
    if not ext:
        ext_map = {"png": ".png", "jpeg": ".jpg", "webp": ".webp"}
        ext = ext_map[args.output_format]

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)

    saved = []
    for i, item in enumerate(result.data):
        if args.n == 1:
            out_path = f"{base}{ext}"
        else:
            out_path = f"{base}_{i+1}{ext}"
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(item.b64_json))
        saved.append(out_path)
        print(f"  ✓ Saved: {out_path}")

    return saved


if __name__ == "__main__":
    main()

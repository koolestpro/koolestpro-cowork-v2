#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31.0"]
# ///
"""
GPT Image Pipeline — Multi-stage image generation.
Chain multiple providers sequentially: base generation → refinement → text overlay → final.

Each stage feeds its output into the next stage as a reference image.
Example: FLUX generates the scene → OpenAI adds text → final ad.
"""

import os, sys, json, argparse, textwrap, tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, SCRIPT_DIR)
from providers import get_provider
from prompt_expander import expand_prompt, format_report

QUALITY_ALIASES = {"hd": "high", "standard": "medium"}


def run_stage(stage_num, provider_name, model_id, prompt, size, quality,
              input_image=None, output_path=None, verbose=False):
    """Run a single pipeline stage."""
    provider = get_provider(provider_name, env_file=os.path.join(SKILL_DIR, ".env"))

    if input_image and hasattr(provider, 'edit'):
        # Use edit mode if we have an input image and the provider supports editing
        if verbose:
            print(f"[pipeline] Stage {stage_num}: {provider_name}/{model_id} EDIT mode")
            print(f"[pipeline]   Input: {input_image}")
            print(f"[pipeline]   Prompt: {prompt[:80]}...")
        paths = provider.edit(
            prompt=prompt,
            images=[input_image],
            size=size,
            quality=quality,
            output_path=output_path,
            n=1,
            model_id=model_id,
        )
    else:
        # Use generate mode
        if input_image and verbose:
            print(f"[pipeline] Stage {stage_num}: {provider_name}/{model_id} GENERATE mode")
            print(f"[pipeline]   Note: provider doesn't support editing, generating from scratch")
            print(f"[pipeline]   (For best results, describe the input image in the prompt)")
        elif verbose:
            print(f"[pipeline] Stage {stage_num}: {provider_name}/{model_id} GENERATE mode")
        paths = provider.generate(
            prompt=prompt,
            size=size,
            quality=quality,
            output_path=output_path,
            n=1,
            model_id=model_id,
        )

    return paths[0] if paths else None


def main():
    parser = argparse.ArgumentParser(
        description="GPT Image Pipeline — multi-stage image generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        EXAMPLES:

        # Two-stage: FLUX base + OpenAI text
        python3 pipeline.py \\
          --stage-1-provider infsh --stage-1-model flux-dev \\
          --stage-1-prompt "A luxury watch on a matte white surface, studio lighting, visible brushed-steel texture, composition leaving clean open space at the top." \\
          --stage-2-provider openai --stage-2-model gpt-image-2 \\
          --stage-2-prompt "Add a bold headline at the top: 'SALE 50% OFF' in large sans-serif font. Keep the watch exactly as it is. Clean layout." \\
          --size 1024x1536 --output /Users/mac/Downloads/final-ad.png

        # Two-stage: Ideogram base + OpenAI refinement (for complex text)
        python3 pipeline.py \\
          --stage-1-provider ideogram --stage-1-model ideogram-v2 \\
          --stage-1-prompt "Book cover: dark city skyline, rain, neon reflections, clean open space at the top for a title." \\
          --stage-2-provider openai --stage-2-model gpt-image-2 \\
          --stage-2-prompt "Add title text at top: 'THE LAST CIPHER' in bold serif font. Author name below: 'A.R. Whitmore'. Keep the city scene intact." \\
          --size 1024x1536 --output /Users/mac/Downloads/book-cover.png

        # Three-stage: base + texture + text (experimental)
        python3 pipeline.py \\
          --stage-1-provider infsh --stage-1-model flux-dev \\
          --stage-1-prompt "Coffee cup on marble table, morning light" \\
          --stage-2-provider openai --stage-2-model gpt-image-2 \\
          --stage-2-prompt "Add a warm color grade, make the lighting more golden hour" \\
          --stage-3-provider ideogram --stage-3-model ideogram-v2 \\
          --stage-3-prompt "Add text overlay: 'Your morning ritual' in elegant script font at top" \\
          --size 1024x1536 --output /Users/mac/Downloads/final.png
        """)
    )

    # Stage definitions (support up to 5 stages)
    for i in range(1, 6):
        parser.add_argument(f"--stage-{i}-provider", help=f"Stage {i} provider")
        parser.add_argument(f"--stage-{i}-model", help=f"Stage {i} model")
        parser.add_argument(f"--stage-{i}-prompt", help=f"Stage {i} prompt")

    parser.add_argument("--size", default="1024x1536", help="Image size for all stages")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto", "hd", "standard"])
    parser.add_argument("--output", required=True, help="Final output path")
    parser.add_argument("--expand", default="auto", choices=["off", "lint", "auto", "llm"],
                        help="Prompt expansion per stage (default: auto)")
    parser.add_argument("--expand-model", default=None,
                        help="Chat model for --expand llm (default: GPT_IMAGE_EXPANDER_MODEL or gpt-4o-mini)")
    parser.add_argument("--expand-min-words", type=int, default=30,
                        help="auto expands stage prompts shorter than this (default: 30)")
    parser.add_argument("--keep-intermediates", action="store_true", help="Save intermediate stage outputs")
    parser.add_argument("--intermediate-dir", default=None, help="Directory for intermediate files")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    args.quality = QUALITY_ALIASES.get(args.quality.lower(), args.quality.lower())

    # Collect defined stages
    stages = []
    for i in range(1, 6):
        prov = getattr(args, f"stage_{i}_provider")
        model = getattr(args, f"stage_{i}_model")
        prompt = getattr(args, f"stage_{i}_prompt")
        if prov and model and prompt:
            stages.append({"num": i, "provider": prov, "model": model, "prompt": prompt})

    if len(stages) < 2:
        parser.error("At least 2 stages required. Use --stage-1-* and --stage-2-* (and more if needed).")

    if args.verbose:
        print(f"[pipeline] Running {len(stages)} stage(s)")
        print(f"[pipeline] Output: {args.output}")
        print()

    # Intermediate directory
    inter_dir = args.intermediate_dir
    if args.keep_intermediates and not inter_dir:
        inter_dir = os.path.join(tempfile.gettempdir(), "gpt-image-pipeline")
        os.makedirs(inter_dir, exist_ok=True)

    # Run stages
    current_image = None
    for stage in stages:
        if stage["num"] == len(stages):
            # Last stage -> final output
            out_path = args.output
        elif args.keep_intermediates:
            out_path = os.path.join(inter_dir, f"stage-{stage['num']}.png")
        else:
            out_path = os.path.join(tempfile.gettempdir(), f"pipeline-stage-{stage['num']}-{os.getpid()}.png")

        # Expand each stage prompt. Later stages are edits of the previous image, so
        # they use the stricter preservation rules.
        stage_prompt = stage["prompt"]
        if args.expand != "off":
            stage_prompt, expand_report = expand_prompt(
                stage["prompt"],
                mode=args.expand,
                min_words=args.expand_min_words,
                model=args.expand_model,
                is_edit=bool(current_image),
            )
            for line in format_report(expand_report):
                print(f"[expand] Stage {stage['num']}: {line}")
            if args.verbose and stage_prompt != stage["prompt"]:
                print(f"[expand] Stage {stage['num']} prompt: {stage_prompt}")

        try:
            result = run_stage(
                stage_num=stage["num"],
                provider_name=stage["provider"],
                model_id=stage["model"],
                prompt=stage_prompt,
                size=args.size,
                quality=args.quality,
                input_image=current_image,
                output_path=out_path,
                verbose=args.verbose,
            )
        except NotImplementedError as e:
            print(f"[pipeline] ERROR Stage {stage['num']}: {e}")
            print(f"[pipeline] The provider '{stage['provider']}' doesn't support image editing.")
            print(f"[pipeline] For this stage, use a provider that supports editing: openai, stability")
            sys.exit(1)
        except Exception as e:
            print(f"[pipeline] ERROR Stage {stage['num']} failed: {e}")
            sys.exit(1)

        if not result:
            print(f"[pipeline] ERROR Stage {stage['num']} produced no output")
            sys.exit(1)

        current_image = result

        if args.verbose:
            print(f"[pipeline] Stage {stage['num']} complete: {result}")
            print()

    # Final output is already set by the last stage
    if current_image != args.output:
        # If last stage used a temp path, copy to final
        import shutil
        shutil.copy(current_image, args.output)
        if not args.keep_intermediates and current_image.startswith(tempfile.gettempdir()):
            os.remove(current_image)

    print(f"[pipeline] Done. Final output: {args.output}")
    if args.keep_intermediates and inter_dir:
        print(f"[pipeline] Intermediates saved to: {inter_dir}")


if __name__ == "__main__":
    main()

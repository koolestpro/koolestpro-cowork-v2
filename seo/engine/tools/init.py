#!/usr/bin/env python3
"""Set up the SEO engine in a project: creates seo/project/ from the template and an .env.example.

Run from the repo root after copying seo/engine/ in:
  python3 seo/engine/tools/init.py --name "Tap and Rate" --url https://tapandrate.co.uk --platform shopify --location 2826
Safe to re-run: never overwrites existing project files.
"""
import argparse
import json
import shutil

from _common import ENGINE_DIR, REPO_ROOT, SEO_ROOT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--platform", choices=["shopify", "nextjs-resources", "files-only"], default="shopify")
    ap.add_argument("--location", type=int, default=2826, help="2826 UK, 2840 US, 2566 Nigeria, 2124 Canada")
    args = ap.parse_args()

    proj = SEO_ROOT / "project"
    (proj / "runs").mkdir(parents=True, exist_ok=True)
    tpl = ENGINE_DIR / "templates" / "project"
    for f in tpl.iterdir():
        if f.name.startswith(".env"):
            continue
        dest = proj / f.name
        if not dest.exists():
            shutil.copy(f, dest)
            print(f"created {dest.relative_to(REPO_ROOT)}")

    cfg_path = proj / "project.json"
    cfg = json.loads(cfg_path.read_text())
    if cfg.get("name") == "Business Name":
        domain = args.url.split("//")[-1].strip("/").removeprefix("www.")
        cfg.update(name=args.name, site_url=args.url.rstrip("/"), platform=args.platform,
                   location_code=args.location, gsc_property=f"sc-domain:{domain}")
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
        print("filled project.json")

    env_ex = REPO_ROOT / ".env.example"
    if not env_ex.exists():
        shutil.copy(tpl / ".env.example", env_ex)
        print("created .env.example (copy to .env and fill in)")
    gi = REPO_ROOT / ".gitignore"
    lines = gi.read_text().splitlines() if gi.exists() else []
    add = [x for x in (".env", "__pycache__/") if x not in lines]
    if add:
        gi.write_text("\n".join(lines + add) + "\n")
        print(f"added {add} to .gitignore")
    print("\nNext: read seo/engine/SETUP.md, then run stage 0 (seo/engine/prompts/00-business-profile.md).")


if __name__ == "__main__":
    main()

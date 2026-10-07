#!/usr/bin/env python3
"""Copy docs/system/cro-finding-rules.md into both CRO skills as references/finding-rules.md.

Run after every edit to the rules:  python3 .ai-workflow/tools/sync_cro_rules.py
Then re-upload the two skills on claude.ai (Settings > Capabilities > Skills) so the account copies match.
"""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "docs/system/cro-finding-rules.md"
SKILLS = ["koolestpro-store-auditor-skill-a", "koolestpro-client-audit"]

header = "<!-- GENERATED from docs/system/cro-finding-rules.md by .ai-workflow/tools/sync_cro_rules.py. Edit the source, not this copy. -->\n\n"
for name in SKILLS:
    dest = ROOT / ".agents/skills" / name / "references/finding-rules.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(header + SRC.read_text(encoding="utf-8"), encoding="utf-8")
    print("updated", dest.relative_to(ROOT))

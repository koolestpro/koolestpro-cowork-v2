#!/usr/bin/env python3
"""Compose the real iPhone mockups (compose_mobile_flat) for the Fishwife CRO Fix, 2026-10-25."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".ai-workflow/skills/page-presentation-kit/scripts"))
from build_device_still import compose_mobile_flat
A = ROOT / "outputs/cro-fixes/fishwife/_assets"; V = ROOT / "outputs/cro-fixes/fishwife/_variants"
jobs = {A / "before_raw.png": A / "phones/fishwife_before_phone.png", A / "after_raw.png": A / "phones/fishwife_after_phone.png"}
for i in range(1, 5): jobs[V / f"v{i}.png"] = V / f"v{i}_phone.png"
for src, dst in jobs.items():
    im, var = compose_mobile_flat(str(src)); im.save(dst); print(dst.name, im.size, var)

#!/usr/bin/env python3
"""Prep Fishwife CRO assets (2026-10-25): background-removed cutouts of their real packshots
(flood fill from the border on the near-white studio background, soft shadow kept as alpha),
WebP at display size. Source images: eatfishwife.com product feed (/products.json), 2026-10-25."""
import pathlib, numpy as np, cv2
from PIL import Image
A = pathlib.Path(__file__).resolve().parent.parent / "outputs/cro-fixes/fishwife/_assets"
SRC = ["fbj_0.png", "gold_0.png", "starter_0.jpg", "sard_0.png", "tuna_0.png", "belly_0.jpg", "spicy_0.jpg", "zhong_0.png"]

def cutout(p):
    im = np.array(Image.open(p).convert("RGB")).astype(np.int16)
    h, w, _ = im.shape
    bg = np.median(np.concatenate([im[:6].reshape(-1, 3), im[-6:].reshape(-1, 3), im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)]), axis=0)
    dist = np.abs(im - bg).max(axis=2)
    cand = (dist < 46).astype(np.uint8)
    n, lab = cv2.connectedComponents(cand, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    region = np.isin(lab, list(border)) & (cand == 1)
    alpha = np.full((h, w), 255, np.float32)
    a_reg = np.clip((dist.astype(np.float32) - 6) / 40.0, 0, 1) * 150  # shadows -> soft translucent
    alpha[region] = a_reg[region]
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    rgb = im.astype(np.uint8).copy()
    rgb[region] = (np.array([40, 34, 30]) * 1).astype(np.uint8)  # shadow tint
    out = np.dstack([rgb, alpha.clip(0, 255).astype(np.uint8)])
    img = Image.fromarray(out, "RGBA")
    bb = img.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox()
    return img.crop(bb)

def main():
    (A / "cut").mkdir(exist_ok=True)
    for f in SRC:
        c = cutout(A / "img" / f)
        c.thumbnail((300, 300), Image.LANCZOS)
        stem = f.split("_")[0]
        c.save(A / "cut" / f"{stem}.png"); c.save(A / "cut" / f"{stem}.webp", "WEBP", quality=82)
        print(stem, c.size)

if __name__ == "__main__":
    main()

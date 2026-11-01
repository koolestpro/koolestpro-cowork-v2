#!/usr/bin/env python3
"""Prep FleeMoto CRO assets (2026-11-01): background-removed cutouts of their two white-background
wheel photos, WebP versions of the two on-bike photos, Inter (their theme body font) woff2, Iconify icons.
Source images: fleemoto.shop product JSON, 2026-11-01. Pattern: prep_fishwife_assets.py."""
import pathlib, numpy as np, cv2, urllib.request, re
from PIL import Image
A = pathlib.Path(__file__).resolve().parent.parent / "outputs/cro-fixes/fleemoto/_assets"

def cutout(p):
    im = np.array(Image.open(p).convert("RGB")).astype(np.int16)
    h, w, _ = im.shape
    bg = np.median(np.concatenate([im[:6].reshape(-1, 3), im[-6:].reshape(-1, 3), im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)]), axis=0)
    dist = np.abs(im - bg).max(axis=2)
    cand = (dist < 40).astype(np.uint8)
    n, lab = cv2.connectedComponents(cand, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    region = np.isin(lab, list(border)) & (cand == 1)
    alpha = np.full((h, w), 255, np.float32); alpha[region] = 0
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    out = np.dstack([im.astype(np.uint8), alpha.clip(0, 255).astype(np.uint8)])
    img = Image.fromarray(out, "RGBA")
    return img.crop(img.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())

def get(url, dst):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    dst.write_bytes(urllib.request.urlopen(req, timeout=30).read())

# 2026-11-01: photos 3 and 4 have the store app's wishlist/zoom icons baked into the top-right corner;
# those were painted out with the photo background before the cutout (not part of the product).
def main():
    for d in ("cut", "fonts", "icons", "photo"): (A / d).mkdir(exist_ok=True)
    for f, stem in (("w3.jpg", "pair"), ("w2.jpg", "single")):
        c = cutout(A / "img" / f); c.thumbnail((900, 900), Image.LANCZOS)
        c.save(A / "cut" / f"{stem}.png"); c.save(A / "cut" / f"{stem}.webp", "WEBP", quality=84); print(stem, c.size)
    for f, stem in (("w0.jpg", "wall"), ("w1.jpg", "sunset")):
        im = Image.open(A / "img" / f).convert("RGB"); im.thumbnail((900, 1200), Image.LANCZOS)
        im.save(A / "photo" / f"{stem}.webp", "WEBP", quality=80); im.save(A / "photo" / f"{stem}.jpg", quality=84)
    css_req = urllib.request.Request("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
                                     headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    css = urllib.request.urlopen(css_req, timeout=30).read().decode()
    blocks = re.findall(r"/\* latin \*/\s*@font-face\s*{[^}]*}", css)
    url = re.search(r"url\((https://[^)]+\.woff2)\)", blocks[0]).group(1)  # Inter is variable: one latin file
    get(url, A / "fonts" / "inter-latin.woff2"); print("font", (A / "fonts/inter-latin.woff2").stat().st_size)
    for name in ["mdi:motorbike", "mdi:check-circle", "mdi:clock-outline", "mdi:shield-lock-outline", "mdi:tire", "mdi:email-outline",
                 "mdi:chevron-down", "mdi:cart-outline", "mdi:menu", "mdi:magnify", "mdi:account-outline", "mdi:calendar-check",
                 "mdi:package-variant-closed", "mdi:truck-fast-outline", "mdi:help-circle-outline", "mdi:star-four-points"]:
        p, i = name.split(":"); get(f"https://api.iconify.design/{p}/{i}.svg", A / "icons" / f"ic_{i}.svg")
    print("icons ok")

if __name__ == "__main__":
    main()

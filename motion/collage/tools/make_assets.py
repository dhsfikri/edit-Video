#!/usr/bin/env python3
"""Jana aset statik untuk template collage (gaya kertas lama).

Guna:  python3 -I motion/collage/tools/make_assets.py [--photo <frame.png> <x,y,w,h> <nama>]

Output dalam motion/collage/assets/:
  paper.jpg        — latar kertas krim 1080x1920 (bintik, serat, vignette)
  grid.png         — kertas grid telus (untuk tampalan)
  <nama>.png       — foto cut-out hitam-putih halftone (dari frame rakaman)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

OUT = Path(__file__).resolve().parent.parent / "assets"
rng = np.random.default_rng(7)


def blur_noise(h, w, scale, sigma):
    n = rng.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    im = Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(sigma)), np.float32) / 255


def paper(w=1080, h=1920):
    base = np.array([236, 227, 207], np.float32)
    blot = blur_noise(h, w, 60, 40) - 0.5
    mid = blur_noise(h, w, 8, 3) - 0.5
    grain = rng.normal(0, 1, (h, w)).astype(np.float32)
    img = base[None, None, :] + blot[..., None] * 34 + mid[..., None] * 10 + grain[..., None] * 5
    # serat halus
    fib = np.zeros((h, w), np.float32)
    for _ in range(900):
        x, y = rng.integers(0, w), rng.integers(0, h)
        L, a = rng.integers(10, 50), rng.random() * np.pi
        for t in range(L):
            xx, yy = int(x + np.cos(a) * t), int(y + np.sin(a) * t)
            if 0 <= xx < w and 0 <= yy < h:
                fib[yy, xx] = 1
    fib = np.asarray(Image.fromarray((fib * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    img -= fib[..., None] * 18
    # vignette
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - np.clip(d - 0.55, 0, 1) * 0.28)[..., None]
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(OUT / "paper.jpg", quality=92)


def grid(w=1080, h=1100, step=44):
    a = np.zeros((h, w, 4), np.uint8)
    a[..., :3] = (60, 90, 110)
    for x in range(0, w, step):
        a[:, x : x + 2, 3] = 46
    for y in range(0, h, step):
        a[y : y + 2, :, 3] = 46
    Image.fromarray(a).save(OUT / "grid.png")


def halftone_photo(src, box, name, cell=5):
    x, y, w, h = box
    im = Image.open(src).convert("L").crop((x, y, x + w, y + h))
    im = im.resize((w * 2, h * 2), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=2)
    g = np.asarray(im, np.float32) / 255
    H, W = g.shape
    out = np.full((H, W), 255, np.uint8)
    yy, xx = np.mgrid[0:cell, 0:cell]
    c = (cell - 1) / 2
    dist = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    for j in range(0, H - cell + 1, cell):
        for i in range(0, W - cell + 1, cell):
            v = 1 - g[j : j + cell, i : i + cell].mean()
            r = np.sqrt(v) * cell * 0.72
            out[j : j + cell, i : i + cell][dist <= r] = 28
    # campur sedikit foto asal supaya tak terlalu grafik
    mix = (out.astype(np.float32) * 0.7 + np.asarray(im, np.float32) * 0.3)
    rgb = np.stack([mix * 0.98 + 4, mix * 0.95 + 6, mix * 0.88 + 10], -1)
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(OUT / f"{name}.jpg", quality=92)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    args = sys.argv[1:]
    if args and args[0] == "--photo":
        halftone_photo(args[1], tuple(int(v) for v in args[2].split(",")), args[3])
    else:
        paper()
        grid()
    print("OK", sorted(p.name for p in OUT.iterdir()))

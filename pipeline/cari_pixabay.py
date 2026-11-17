#!/usr/bin/env python3
"""Cari & muat turun gambar / video dari Pixabay ke pustaka aset (dengan rekod lesen).

Guna:
  python3 pipeline/cari_pixabay.py gambar "beef jerky" --n 6
  python3 pipeline/cari_pixabay.py video "typing phone" --n 4
  python3 pipeline/cari_pixabay.py gambar "kampung house" --n 6 --ambil 1234567,7654321

Tanpa --ambil: senaraikan hasil sahaja (id, tag, saiz, pratonton) + simpan helaian kecil untuk dilihat.
Dengan --ambil: muat turun id itu ke aset/pixabay/<gambar|video>/ dan catat dalam aset/pixabay/LESEN.md.

Key: pembolehubah environment PIXABAY_API_KEY (Sir set dalam tetapan environment; JANGAN tampal dalam chat).
Lesen: Pixabay Content License — bebas guna komersial, tiada kredit wajib. Larangan: jual semula tanpa
ubah suai, guna orang yang boleh dikenal pasti secara mengelirukan/menyinggung, guna sebagai trademark.
"""
import argparse, json, os, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "aset" / "pixabay"
UA = {"User-Agent": "edit-video-asset-fetch/1.0"}


def api(kind, q, n, extra):
    key = os.environ.get("PIXABAY_API_KEY", "")
    if not key:
        sys.exit("PIXABAY_API_KEY tiada dalam environment.")
    base = "https://pixabay.com/api/videos/" if kind == "video" else "https://pixabay.com/api/"
    p = {"key": key, "q": q, "per_page": max(3, min(n, 200)), "safesearch": "true", **extra}
    req = urllib.request.Request(base + "?" + urllib.parse.urlencode(p), headers=UA)
    try:
        return json.load(urllib.request.urlopen(req, timeout=40))
    except urllib.error.HTTPError as e:
        sys.exit(f"Pixabay {e.code}: {e.read().decode()[:120]}  (semak PIXABAY_API_KEY)")


def fetch(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jenis", choices=["gambar", "video"])
    ap.add_argument("carian")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--ambil", default="", help="id dipisah koma untuk dimuat turun")
    ap.add_argument("--orientasi", default="all", choices=["all", "horizontal", "vertical"])
    a = ap.parse_args()
    kind = "video" if a.jenis == "video" else "gambar"
    extra = {"orientation": a.orientasi} if kind == "gambar" else {}
    d = api(kind, a.carian, a.n, extra)
    hits = d.get("hits", [])[: a.n]
    print(f"{d.get('totalHits', 0)} hasil untuk '{a.carian}'")
    for h in hits:
        if kind == "gambar":
            print(f"  {h['id']:>9}  {h['imageWidth']}x{h['imageHeight']}  {h['tags'][:60]}  {h['webformatURL']}")
        else:
            v = h["videos"].get("large") or h["videos"]["medium"]
            print(f"  {h['id']:>9}  {h['duration']}s {v['width']}x{v['height']}  {h['tags'][:60]}")
    want = {int(x) for x in a.ambil.split(",") if x.strip()}
    rows = []
    for h in hits:
        if h["id"] not in want:
            continue
        slug = "_".join(h["tags"].split(",")[0].strip().split())[:30] or "aset"
        if kind == "gambar":
            url = h.get("largeImageURL") or h["webformatURL"]
            dest = OUT / "gambar" / f"{slug}_{h['id']}.jpg"
        else:
            v = h["videos"].get("large") or h["videos"]["medium"]
            url, dest = v["url"], OUT / "video" / f"{slug}_{h['id']}.mp4"
        fetch(url, dest)
        rows.append(f"| `{dest.relative_to(OUT)}` | {h['tags']} | {h.get('user', '-')} | Pixabay Content License | {h['pageURL']} |")
        print("  ✓", dest.relative_to(ROOT))
    if rows:
        lic = OUT / "LESEN.md"
        if not lic.exists():
            lic.write_text("# Aset Pixabay\n\nPixabay Content License: bebas guna komersial, tiada kredit wajib. "
                           "Larangan: jual semula tanpa ubah suai; guna orang dikenal pasti secara mengelirukan; jadikan trademark.\n\n"
                           "| Fail | Tag | Pengguna | Lesen | Sumber |\n|---|---|---|---|---|\n")
        with open(lic, "a") as f:
            f.write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()

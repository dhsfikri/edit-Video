#!/usr/bin/env python3
"""Pustaka aset (gambar/ikon/video) — cari, ambil, simpan & rekod dalam library/katalog.json.

Setiap aset yang diambil disimpan dalam library/<kategori>/ dan direkod (sumber, lesen, kredit, tag,
video yang guna). Semua video ambil aset dari sini, jadi aset yang sama boleh diguna semula.

Guna:
  python3 -I pipeline/aset.py cari "customer phone" [--video] [--n 10]   # Pexels (perlu key)
  python3 -I pipeline/aset.py ambil <pexels_id> --kategori suasana --tag "phone,customer" [--video]
  python3 -I pipeline/aset.py ikon message-circle phone check x --warna 25D366
  python3 -I pipeline/aset.py frame <raw.mp4> <saat> --nama sir-terkejut --tag "ekspresi,terkejut" [--rotate cw|ccw]
  python3 -I pipeline/aset.py guna <aset_id> <projek_id>                 # tandakan aset diguna dalam video
  python3 -I pipeline/aset.py senarai [--tag phone]

Key Pexels: network secret untuk api.pexels.com (proxy suntik header), ATAU env PEXELS_API_KEY.
"""
import argparse, datetime, json, os, re, subprocess, sys, tarfile, tempfile, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
KAT = LIB / "katalog.json"
TABLER = "3.35.0"
MAX_W = 1080  # gambar disimpan maks 1080px lebar (cukup untuk 1080x1920)


def load():
    return json.loads(KAT.read_text()) if KAT.exists() else {"aset": []}


def save(k):
    k["aset"].sort(key=lambda a: a["id"])
    KAT.write_text(json.dumps(k, ensure_ascii=False, indent=1) + "\n")


def add(k, rec):
    k["aset"] = [a for a in k["aset"] if a["id"] != rec["id"]] + [rec]
    save(k)
    print(f"✓ {rec['id']} → {rec['fail']}")


def today():
    return datetime.date.today().isoformat()


def pexels(path, **q):
    url = f"https://api.pexels.com/{path}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "edit-video-library/1.0"})
    key = os.environ.get("PEXELS_API_KEY")
    if key:
        req.add_header("Authorization", key)
    try:
        return json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("✗ Pexels 401: key belum disetkan (network secret api.pexels.com atau PEXELS_API_KEY).")
        raise


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "edit-video-library/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 16):
            f.write(chunk)


def shrink(p):
    from PIL import Image
    im = Image.open(p)
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.convert("RGB").save(p, "JPEG", quality=85, optimize=True)


def cmd_cari(a):
    if a.video:
        d = pexels("videos/search", query=a.q, per_page=a.n, orientation="portrait")
        for v in d.get("videos", []):
            print(f"{v['id']:>10}  {v['duration']:>3}s  {v['width']}x{v['height']}  {v['user']['name']}  {v['url']}")
    else:
        d = pexels("v1/search", query=a.q, per_page=a.n, orientation=a.orientasi)
        for p in d.get("photos", []):
            print(f"{p['id']:>10}  {p['width']}x{p['height']}  {p['photographer']}  {p.get('alt','')[:60]}  {p['url']}")


def cmd_ambil(a):
    k = load()
    tags = [t.strip() for t in a.tag.split(",") if t.strip()]
    if a.video:
        v = pexels(f"videos/videos/{a.id}")
        files = sorted([f for f in v["video_files"] if f.get("height") and f["height"] <= 1920],
                       key=lambda f: f["height"], reverse=True)
        src = files[0]
        dest = LIB / a.kategori / f"pexels-v{a.id}.mp4"
        download(src["link"], dest)
        rec = dict(id=f"pexels-v{a.id}", jenis="video", fail=str(dest.relative_to(ROOT)), sumber="Pexels",
                   url=v["url"], kredit=v["user"]["name"], lesen="Pexels License (percuma, komersial OK, tiada kredit wajib)",
                   dimensi=f"{src['width']}x{src['height']}", durasi=v["duration"])
    else:
        p = pexels(f"v1/photos/{a.id}")
        dest = LIB / a.kategori / f"pexels-{a.id}.jpg"
        download(p["src"]["large2x"], dest)
        shrink(dest)
        rec = dict(id=f"pexels-{a.id}", jenis="gambar", fail=str(dest.relative_to(ROOT)), sumber="Pexels",
                   url=p["url"], kredit=p["photographer"], lesen="Pexels License (percuma, komersial OK, tiada kredit wajib)",
                   alt=p.get("alt", ""))
    rec.update(kategori=a.kategori, tag=tags, tarikh=today(), digunakan=[])
    add(k, rec)


def cmd_ikon(a):
    k = load()
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["npm", "pack", f"@tabler/icons@{TABLER}", "-q", "--pack-destination", td],
                       check=True, capture_output=True)
        tgz = next(Path(td).glob("*.tgz"))
        with tarfile.open(tgz) as t:
            for name in a.nama:
                gaya = "filled" if a.filled else "outline"
                try:
                    svg = t.extractfile(f"package/icons/{gaya}/{name}.svg").read().decode()
                except KeyError:
                    print(f"✗ ikon '{name}' tiada (lihat https://tabler.io/icons)")
                    continue
                if a.warna:
                    svg = svg.replace("currentColor", f"#{a.warna.lstrip('#')}")
                suf = f"-{a.warna.lstrip('#').lower()}" if a.warna else ""
                dest = LIB / "ikon" / f"{name}{'-filled' if a.filled else ''}{suf}.svg"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(svg)
                add(k, dict(id=f"ikon-{dest.stem}", jenis="ikon", fail=str(dest.relative_to(ROOT)),
                            sumber=f"Tabler Icons {TABLER}", url="https://tabler.io/icons", kredit="Tabler",
                            lesen="MIT (percuma, komersial OK)", kategori="ikon", tag=[name], tarikh=today(), digunakan=[]))


def cmd_frame(a):
    k = load()
    dest = LIB / "sir" / f"{a.nama}.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    vf = {"cw": "transpose=1,", "ccw": "transpose=2,"}.get(a.rotate, "")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.saat), "-i", a.raw, "-frames:v", "1",
                    "-vf", f"{vf}scale='min({MAX_W},iw)':-2", "-q:v", "2", str(dest)], check=True)
    add(k, dict(id=f"sir-{a.nama}", jenis="frame", fail=str(dest.relative_to(ROOT)),
                sumber=f"Rakaman Sir: {Path(a.raw).name} @ {a.saat}s", url="", kredit="Sir Dharma",
                lesen="Milik sendiri", kategori="sir", tag=[t.strip() for t in a.tag.split(",") if t.strip()],
                tarikh=today(), digunakan=[]))


def cmd_guna(a):
    k = load()
    for x in k["aset"]:
        if x["id"] == a.id:
            if a.projek not in x["digunakan"]:
                x["digunakan"].append(a.projek)
            save(k)
            print(f"✓ {a.id} ditanda guna dalam {a.projek}")
            return
    sys.exit(f"✗ aset {a.id} tiada dalam katalog")


def cmd_senarai(a):
    for x in load()["aset"]:
        if a.tag and a.tag not in x["tag"] and a.tag != x["kategori"]:
            continue
        print(f"{x['id']:<28} {x['jenis']:<7} {','.join(x['tag'])[:30]:<30} guna:{','.join(x['digunakan']) or '-'}  {x['fail']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest="cmd", required=True)
    p = s.add_parser("cari"); p.add_argument("q"); p.add_argument("--n", type=int, default=10)
    p.add_argument("--video", action="store_true"); p.add_argument("--orientasi", default="portrait")
    p = s.add_parser("ambil"); p.add_argument("id"); p.add_argument("--kategori", required=True)
    p.add_argument("--tag", default=""); p.add_argument("--video", action="store_true")
    p = s.add_parser("ikon"); p.add_argument("nama", nargs="+"); p.add_argument("--warna")
    p.add_argument("--filled", action="store_true")
    p = s.add_parser("frame"); p.add_argument("raw"); p.add_argument("saat", type=float)
    p.add_argument("--nama", required=True); p.add_argument("--tag", default=""); p.add_argument("--rotate")
    p = s.add_parser("guna"); p.add_argument("id"); p.add_argument("projek")
    p = s.add_parser("senarai"); p.add_argument("--tag")
    a = ap.parse_args()
    globals()[f"cmd_{a.cmd}"](a)


if __name__ == "__main__":
    main()

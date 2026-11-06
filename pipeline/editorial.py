#!/usr/bin/env python3
"""Render satu video dalam pakej gaya editorial (clean | bold | chat | magazine).

Guna:  python3 pipeline/editorial.py projects/<ID>/edit.json projects/<ID>/data.js <gaya> <outdir> [--fps 50]

Langkah: cut.py (grade + zoom ikut gaya) -> overlay motion/editorial (style) -> compose.py (SFX gaya) -> QC safe zone.
- Gaya ditakrif dalam motion/editorial/styles.json.
- data.js: skema overlay-v2 (titles, brackets, callouts, words, cta). Jika tiada `transitions`,
  peralihan diletak automatik pada setiap titik potong (dari cuts.json).
- `words`: kalau data.js letak "words": "auto", guna words.json dari cut.py.
- `broll`: [{src, start, dur}] (cth dari motion/broll-mag) diteruskan ke compose.py.
Output dalam <outdir>/<gaya>/: base.mov, overlay.mov, <ID>_<gaya>.mp4, <ID>_<gaya>_safezone.png
"""
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOTION = ROOT / "motion" / "editorial"

ap = argparse.ArgumentParser()
ap.add_argument("edit"); ap.add_argument("data"); ap.add_argument("style"); ap.add_argument("outdir")
ap.add_argument("--skip-cut", action="store_true", help="guna base.mov sedia ada")
a = ap.parse_args()

styles = json.load(open(MOTION / "styles.json"))
if a.style not in styles or a.style.startswith("_"):
    sys.exit(f"Gaya tak dikenali: {a.style}. Pilih: {', '.join(k for k in styles if not k.startswith('_'))}")
S = styles[a.style]
edit = json.load(open(a.edit))
fps = edit.get("fps", 30)
out = Path(a.outdir) / a.style
out.mkdir(parents=True, exist_ok=True)
vid = Path(a.edit).parent.name

# 1) Potong A-roll dengan grade & corak zoom gaya
edit["workdir"] = str(out)
edit["color"] = S["grade"]
for i, seg in enumerate(edit["segments"]):
    z = S["zoom"][i % len(S["zoom"])]
    seg["zoom"] = seg["zoom_to"] = z
ej = out / "edit.json"
json.dump(edit, open(ej, "w"), ensure_ascii=False, indent=1)
if not a.skip_cut:
    subprocess.run([sys.executable, "-I", str(ROOT / "pipeline" / "cut.py"), str(ej)], check=True)
cuts = json.load(open(out / "cuts.json"))

# 2) Data overlay
src = open(a.data).read()
E = json.loads(src.split("window.EDIT =", 1)[1].strip().rstrip(";"))
E["style"] = a.style
E["duration"] = cuts["duration"]
if E.get("words") == "auto":
    E["words"] = json.load(open(out / "words.json"))
if "transitions" not in E:
    t, trs = 0.0, []
    for seg in cuts["segments"][:-1]:
        t += seg["end"] - seg["start"]
        trs.append({"t": round(t, 3)})
    E["transitions"] = trs
(MOTION / "data.js").write_text(f"// Dijana oleh pipeline/editorial.py ({vid}, gaya {a.style})\nwindow.EDIT = " + json.dumps(E, ensure_ascii=False, indent=1) + ";\n")
ov = out / "overlay.mov"
subprocess.run(["npx", "hyperframes", "render", "--format", "mov", "-f", str(fps), "-w", "4", "-o", str(ov)], cwd=MOTION, check=True)

# 3) Gabung + SFX
sfx = [{"src": str(ROOT / "motion/intro/assets/signature.wav"), "at": 0.03, "vol": 0.4}]
vol = S["sfx"].get("vol", 0.4)
if S["sfx"].get("transition"):
    sfx += [{"src": str(MOTION / "assets" / S["sfx"]["transition"]), "at": max(tr["t"] - 0.2, 0), "vol": vol} for tr in E["transitions"] if tr.get("kind") in (None, S["transition"])]
if S["sfx"].get("title"):
    for g in E.get("titles", [])[1:] if a.style != "chat" else E.get("titles", []):
        for line in g["lines"] if a.style == "chat" else g["lines"][:1]:
            sfx.append({"src": str(MOTION / "assets" / S["sfx"]["title"]), "at": line[0]["t"], "vol": vol})
for x in E.get("sfx_extra", []):  # [{file, at, vol}] bunyi tambahan (cth ding notifikasi), fail dalam motion/editorial/assets
    sfx.append({"src": str(MOTION / "assets" / x["file"]), "at": x["at"], "vol": x.get("vol", 0.5)})
comp = {"base": str(out / "base.mov"), "out": str(out / f"{vid}_{a.style}.mp4"), "fps": fps, "overlay": str(ov), "sfx": sfx}
# Kad kaca (magazine): baca geometri kad dari template untuk blur sebenar
glass = json.loads(subprocess.check_output(["node", str(ROOT / "pipeline" / "probe_glass.js"), str(MOTION), a.style]).decode() or "[]")
if glass:
    comp["blur"] = glass
if E.get("fade_out"):
    comp["fade_out"] = E["fade_out"]
if E.get("broll"):
    comp["broll"] = E["broll"]  # [{src, start, dur}] masa timeline akhir
if E.get("hold_end"):
    comp["insert"] = {"at": round(cuts["duration"] - 0.05, 3), "dur": E["hold_end"]}
cj = out / "compose.json"
json.dump(comp, open(cj, "w"), indent=1)
subprocess.run([sys.executable, "-I", str(ROOT / "pipeline" / "compose.py"), str(cj)], check=True)

# 4) QC
subprocess.run([sys.executable, "-I", str(ROOT / "pipeline" / "safezone_qc.py"), comp["out"], str(out / f"{vid}_{a.style}_safezone.png")], check=True)
print(f"SIAP {comp['out']}")

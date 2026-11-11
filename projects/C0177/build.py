#!/usr/bin/env python3
"""Bina lapisan C0177 (burn out, tanpa siri, tiada iklan) selepas pipeline/cut.py + pipeline/eyeline.py:
   B-roll (tugas, graf, bateri, cas) → data.js overlay → compose.json.
Guna:  python3 -I projects/C0177/build.py <workdir> [broll] [data]
Cue ditulis dalam MASA SUMBER (rakaman asal) dan dipetakan ke timeline melalui cuts.json.
"""
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WD = Path(sys.argv[1]); STEPS = sys.argv[2:] or ["broll", "data"]
cuts = json.load(open(WD / "cuts.json")); words = json.load(open(WD / "words.json"))
BASE = str(WD / "base_eye.mov"); TOTAL = cuts["duration"]; FPS = 30; HOLD = 1.0

offs, o = [], 0.0
for s in cuts["segments"]:
    offs.append(o); o += s["end"] - s["start"]


def m(src):
    """masa sumber → masa timeline"""
    for s, of in zip(cuts["segments"], offs):
        if s["start"] - 0.03 <= src <= s["end"] + 0.03:
            return round(of + src - s["start"], 3)
    raise SystemExit(f"masa sumber {src} tiada dalam mana-mana segmen")


seg_end = lambda i: round(offs[i] + cuts["segments"][i]["end"] - cuts["segments"][i]["start"], 3)
B = {
    "tugas": dict(on=m(12.95), off=seg_end(2), items=[m(13.10), m(15.75), m(18.30)]),
    "graf": dict(on=m(31.80), off=seg_end(5), items=[m(31.95), m(34.05), m(36.89)]),
    "bateri": dict(on=m(43.55), off=seg_end(7), items=[m(44.59), m(45.59)]),
    "cas": dict(on=m(51.83), off=seg_end(10), items=[m(53.61), m(55.25), m(55.77)]),
}
for b in B.values():
    b["a"] = round((b["on"] - 0.4) * FPS) / FPS
    b["b"] = b["off"] if b["off"] >= TOTAL - 0.05 else b["off"] + 0.4
    b["dur"] = round((b["b"] - b["a"]) * FPS) / FPS


def rel(b, t):
    return round(t - b["a"], 3)


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


if "broll" in STEPS:
    adir = REPO / "motion/poin/assets"
    for name, b in B.items():
        ar, fc, tmp = adir / ("aroll_cur.mp4" if b.get("comp", "poin") == "poin" else f"aroll_{name}.mp4"), adir / ("face_cur.mp4" if b.get("comp", "poin") == "poin" else f"face_{name}.mp4"), WD / f"_face_{name}.mp4"  # poin: src statik
        pad = 12 - b["dur"] + 0.5
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['a']:.3f}", "-t", f"{b['dur']:.3f}", "-i", BASE, "-an",
             "-vf", f"fps={FPS},tpad=stop_mode=clone:stop_duration={pad:.2f}", "-t", "12",
             "-c:v", "libx264", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p", str(ar)])
        run([sys.executable, "-I", str(REPO / "pipeline/facecrop.py"), BASE, str(tmp), "--rotate", "none",
             "--seg", f"{b['a']:.3f}:{b['b']:.3f}", "--fps", str(FPS)], stdout=subprocess.DEVNULL)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}", "-t", "12",
             "-c:v", "libx264", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p", str(fc)])
        cue = dict(on=rel(b, b["on"]), off=rel(b, b["off"]) if b["off"] < TOTAL - 0.05 else 99, items=[rel(b, t) for t in b["items"]])
        var = dict(scene=name, face=f"assets/{fc.name}", aroll=f"assets/{ar.name}", cue=json.dumps(cue))
        raw = WD / f"_broll_{name}.mp4"
        run(["npx", "hyperframes", "render", "--variables", json.dumps(var), "-f", str(FPS), "-q", "high", "-w", "4", "-o", str(raw)],
            cwd=REPO / "motion/poin", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-t", f"{b['dur']:.3f}", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
             str(WD / f"broll_{name}.mp4")])
        print("B-roll", name, f"{b['a']:.2f}–{b['b']:.2f}", cue)

if "data" in STEPS:
    ws = []
    for w in words:
        t = w["w"].strip()
        if t.startswith("-") and ws:
            ws[-1]["w"] += t; ws[-1]["e"] = w["e"]; continue
        d = {"w": t, "s": w["s"], "e": w["e"]}
        if t[:1].isupper() and t[1:2].islower():
            d["b"] = 1
        ws.append(d)
    D = round(TOTAL + HOLD, 3)

    def title(start, end, top, lines):
        t, out = start + 0.05, []
        for ln in lines:
            row = []
            for tok in ln:
                row.append({"t": round(tok[2] if len(tok) > 2 else t, 3), "text": tok[0], "k": tok[1]}); t += 0.14
            out.append(row)
        return {"start": round(start, 3), "end": round(end, 3), "top": top, "lines": out}

    TOP = 1060
    E = {
        "duration": D, "series": "", "episode": "", "maxWords": 3, "hideBadge": [],
        "titles": [
            title(0, m(8.05) - 0.03, TOP, [[("3 tanda awak", "script")], [("DAH MULA", "bold")], [("BURN OUT", "box", m(3.57))]]),
            title(m(8.08), B["tugas"]["on"] - 0.25, TOP, [[("tanda 1", "script")], [("SERBA", "bold")], [("TAK KENA", "box")]]),
            title(m(25.95), B["graf"]["on"] - 0.25, TOP, [[("tanda 2", "script")], [("TAK", "bold")], [("SEMANGAT", "box")]]),
            title(m(38.98), B["bateri"]["on"] - 0.25, TOP, [[("tanda 3", "script")], [("TAK", "bold")], [("BEREMOSI", "box")]]),
            title(m(46.80), m(49.30) - 0.03, TOP, [[("hati-hati dengan", "script")], [("3 TANDA NI", "box")]]),
            title(m(57.80), D, TOP - 20, [[("BURN OUT", "bold")], [("IS REAL", "box")]]),
        ],
        "brackets": [], "callouts": [],
        "cta": {"start": round(TOTAL + 0.05, 3), "text": "🔔 follow @sirdharma_", "top": 1235},
        "words": ws,
    }
    js = "// Data overlay Gaya v2 untuk C0177 (burn out) — dijana oleh projects/C0177/build.py\nwindow.EDIT = " + json.dumps(E, ensure_ascii=False, indent=1) + ";\n"
    (REPO / "projects/C0177/data.js").write_text(js); (REPO / "motion/overlay-v2/data.js").write_text(js)

    A = str(REPO / "motion/pakej/assets")
    sfx = [{"src": str(REPO / "motion/intro/assets/signature.wav"), "at": 0.03, "vol": 0.4},
           {"src": A + "/whoosh.wav", "at": round(m(3.57) - 0.2, 3), "vol": 0.18},
           {"src": A + "/whoosh.wav", "at": round(m(57.80) - 0.15, 3), "vol": 0.18}]
    for b in B.values():
        for t in [b["on"]] + ([b["off"]] if b["off"] < TOTAL - 0.05 else []):
            sfx.append({"src": A + "/whoosh.wav", "at": round(t - 0.24, 3), "vol": 0.22})
        for t in b["items"]:
            sfx.append({"src": A + "/pop.wav", "at": t, "vol": 0.14})
    comp = {"base": BASE, "out": str(WD / "C0177_draf_v1.mp4"), "fps": FPS, "hold": HOLD,
            "broll": [{"src": str(WD / f"broll_{n}.mp4"), "start": b["a"], "dur": b["dur"]} for n, b in B.items()],
            "overlay": str(WD / "overlay.mov"), "sfx": sfx}
    json.dump(comp, open(REPO / "projects/C0177/compose.json", "w"), indent=1)
    print("data.js + compose.json OK · durasi akhir", D)
    for t in E["titles"]:
        print(" tajuk", t["start"], "→", t["end"], " ".join(x["text"] for l in t["lines"] for x in l))

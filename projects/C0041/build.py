#!/usr/bin/env python3
"""Bina lapisan C0041 "3 step nak mudah closing" (TIPS JUALAN #03) — sumber C0041 (a) + C0042 (b) + C0043 (c).
Langkah sebelum: pipeline/cut.py + pipeline/eyeline.py untuk edit_a/b/c.json, kemudian gabung (lihat brief) → base_eye.mov, cuts.json, words.json.
Guna:  python3 -I projects/C0041/build.py <workdir> [hook] [broll] [data]
Cue ditulis sebagai m(bahagian, masa sumber) dan dipetakan ke timeline melalui cuts.json.
"""
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WD = Path(sys.argv[1]); STEPS = sys.argv[2:] or ["hook", "broll", "data"]
cuts = json.load(open(WD / "cuts.json")); words = json.load(open(WD / "words.json"))
BASE = str(WD / "base_eye.mov"); TOTAL = cuts["duration"]; FPS = 30; AD = 4.0; HOLD = 1.0
SEG = cuts["segments"]


def m(part, src):
    for s in SEG:
        if s["part"] == part and s["start"] - 0.03 <= src <= s["end"] + 0.03:
            return round(s["t0"] + src - s["start"], 3)
    raise SystemExit(f"{part}:{src} tiada dalam mana-mana segmen")


def seg_end(note_prefix):
    s = next(x for x in SEG if x["note"].startswith(note_prefix))
    return round(s["t0"] + s["end"] - s["start"], 3)


INS = seg_end("b3")                                   # iklan selepas step 2
fin = lambda t: round(t + (AD if t >= INS - 1e-6 else 0), 3)
TW, OUT = m("a", 4.82), m("a", 5.52)                  # twist pada "kan", keluar pada "beli"
ORD = [0.15, 0.55, 0.95, 1.3, 1.6, 1.85, 2.1]

B = {
    "validate": dict(scene="validate", on=m("a", 19.75) + 0.06, off=seg_end("a4") - 0.05, items=[m("a", 24.46), m("a", 25.58), m("a", 27.02)]),
    "step1": dict(scene="step", level=1, on=m("a", 33.26), off=seg_end("a6"), items=[m("a", 33.98)]),
    "step3": dict(scene="step", level=3, on=m("b", 29.59) + 0.12, off=seg_end("b4"), items=[m("b", 33.0)]),
    "mampu": dict(scene="mampu", on=m("c", 17.6), off=seg_end("c3"), items=[m("c", 20.68), m("c", 22.24)]),
}
for b in B.values():
    b["a"] = round(max(b["on"] - 0.4, 0) * FPS) / FPS
    b["b"] = b["off"] + 0.4 if not any(abs(b["off"] - seg_end(s["note"][:2])) < 0.01 for s in SEG) else b["off"] + 0.3
    b["dur"] = round((b["b"] - b["a"]) * FPS) / FPS
B["step3"]["a"] = round(INS * FPS) / FPS; B["step3"]["dur"] = round((B["step3"]["b"] - B["step3"]["a"]) * FPS) / FPS  # mula tepat selepas iklan


def rel(b, t):
    return round(t - b["a"], 3)


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


if "hook" in STEPS:
    run([sys.executable, "-I", str(REPO / "pipeline/facecrop.py"), BASE, str(REPO / "motion/hook/assets/face_hook.mp4"), "--rotate", "none",
         "--seg", f"0:{OUT + 0.6:.2f}", "--fps", str(FPS)], stdout=subprocess.DEVNULL)
    var = dict(twist=TW, out=OUT, face="assets/face_hook.mp4", orders=json.dumps(ORD))
    run(["npx", "hyperframes", "render", "--format", "mov", "--variables", json.dumps(var), "-f", str(FPS), "-w", "4", "-o", str(WD / "hook.mov")],
        cwd=REPO / "motion/hook", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hd = round((OUT + 0.3) * FPS) / FPS
    run(["ffmpeg", "-v", "error", "-y", "-t", f"{hd}", "-i", BASE, "-t", f"{hd}", "-i", str(WD / "hook.mov"), "-filter_complex",
         "[1:v]format=yuva444p[h];[0:v][h]overlay=0:0:eof_action=pass,format=yuv420p[v]", "-map", "[v]", "-an",
         "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(WD / "broll_hook.mp4")])
    print("hook", TW, OUT, hd)

ONLY = next((x.split(":", 1)[1].split(",") for x in STEPS if x.startswith("broll:")), None)  # cth broll:step1,step3
if "broll" in STEPS or ONLY:
    adir = REPO / "motion/poin/assets"
    for name, b in B.items():
        if ONLY and name not in ONLY:
            continue
        ar, fc, tmp = adir / ("aroll_cur.mp4" if b.get("comp", "poin") == "poin" else f"aroll_{name}.mp4"), adir / ("face_cur.mp4" if b.get("comp", "poin") == "poin" else f"face_{name}.mp4"), WD / f"_face_{name}.mp4"  # poin: src statik
        pad = 12 - b["dur"] + 0.5
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['a']:.3f}", "-t", f"{b['dur']:.3f}", "-i", BASE, "-an",
             "-vf", f"fps={FPS},tpad=stop_mode=clone:stop_duration={pad:.2f}", "-t", "12", "-c:v", "libx264", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p", str(ar)])
        run([sys.executable, "-I", str(REPO / "pipeline/facecrop.py"), BASE, str(tmp), "--rotate", "none",
             "--seg", f"{b['a']:.3f}:{b['b']:.3f}", "--fps", str(FPS)], stdout=subprocess.DEVNULL)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}", "-t", "12",
             "-c:v", "libx264", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p", str(fc)])
        cue = dict(on=rel(b, b["on"]), off=rel(b, b["off"]), items=[rel(b, t) for t in b["items"]], level=b.get("level", 1))
        if name == "step3":
            cue["on"] = 0.32  # sapuan masuk terus selepas iklan
        var = dict(scene=b["scene"], face=f"assets/{fc.name}", aroll=f"assets/{ar.name}", cue=json.dumps(cue))
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
    if ws and ws[0]["w"].lower().startswith("siapa"):
        ws[0]["w"] = "Siapa"
    for w in ws:
        sh = AD if (w["s"] + w["e"]) / 2 >= INS else 0
        w["s"], w["e"] = round(w["s"] + sh, 3), round(w["e"] + sh, 3)
    D = round(TOTAL + AD + HOLD, 3)

    def title(start, end, top, lines):
        t, out = start + 0.05, []
        for ln in lines:
            row = []
            for tok in ln:
                row.append({"t": round(tok[2] if len(tok) > 2 else t, 3), "text": tok[0], "k": tok[1]}); t += 0.14
            out.append(row)
        return {"start": round(start, 3), "end": round(end, 3), "top": top, "lines": out}

    TOP = 1060
    st1 = B["validate"]["on"]
    E = {
        "duration": D, "series": "TIPS JUALAN", "episode": "03", "maxWords": 3,
        "hideBadge": [[0, OUT + 0.05]] + [[fin(b["on"]) - 0.1, fin(b["off"]) + 0.1] for b in B.values()] + [[INS - 0.02, INS + AD]],
        "titles": [
            title(OUT - 0.02, m("a", 12.9) - 0.03, TOP, [[("jual barang tapi", "script")], [("ORANG SUSAH", "bold")], [("BELI?", "box")]]),
            title(m("a", 12.9), st1 - 0.25, TOP, [[("step asas", "script")], [("PILIH", "bold")], [("PRODUK", "box", m("a", 14.36))]]),
            title(m("a", 29.44), B["step1"]["on"] - 0.25, TOP, [[("ikut formula ni", "script")], [("1.", "bold"), ("TAHU", "box", m("a", 31.34))]]),
            title(m("b", 7.87), m("b", 10.78) - 0.03, TOP, [[("step kedua", "script")], [("2.", "bold"), ("PERLU", "box", m("b", 8.84))]]),
            title(fin(m("c", 11.6)), fin(B["mampu"]["on"]) - 0.25, TOP, [[("step ketiga", "script")], [("3.", "bold"), ("MAMPU", "box", fin(m("c", 13.14)))]]),
            title(fin(m("c", 38.4)), D, 990, [[("jual pada", "script")], [("ORANG YANG", "bold")], [("BETUL", "box")]]),
        ],
        "brackets": [],
        "callouts": [
            {"t": fin(m("c", 31.26)), "end": fin(m("c", 37.2)), "x": 90, "y": 1060, "text": "anak muda: boleh amal", "kind": "ok"},
            {"t": fin(m("c", 34.46)), "end": fin(m("c", 37.2)), "x": 90, "y": 1150, "text": "dewasa: seminggu sekali", "kind": "tag"},
        ],
        "cta": {"start": round(TOTAL + AD + 0.05, 3), "text": "🔔 follow @sirdharma_", "top": 1250},
        "words": ws,
    }
    js = "// Data overlay Gaya v2 untuk C0041 (TIPS JUALAN #03) — dijana oleh projects/C0041/build.py\nwindow.EDIT = " + json.dumps(E, ensure_ascii=False, indent=1) + ";\n"
    (REPO / "projects/C0041/data.js").write_text(js); (REPO / "motion/overlay-v2/data.js").write_text(js)

    A = str(REPO / "motion/pakej/assets")
    sfx = [{"src": str(REPO / "motion/intro/assets/signature.wav"), "at": 0.03, "vol": 0.35}]
    sfx += [{"src": A + "/kaching.wav", "at": t, "vol": 0.35} for t in ORD]
    sfx += [{"src": A + "/scratch.wav", "at": TW, "vol": 0.7}, {"src": A + "/whoosh.wav", "at": round(OUT - 0.24, 3), "vol": 0.22}]
    for n, b in B.items():
        for t in ([] if n == "step3" else [b["on"]]) + [b["off"]]:
            sfx.append({"src": A + "/whoosh.wav", "at": round(fin(t) - 0.24, 3), "vol": 0.22})
        for t in b["items"]:
            sfx.append({"src": A + "/pop.wav", "at": fin(t), "vol": 0.14})
    hd = round((OUT + 0.3) * FPS) / FPS
    comp = {"base": BASE, "out": str(WD / "C0041_draf_v1.mp4"), "fps": FPS,
            "insert": {"at": INS, "dur": AD, "overlay": str(WD / "iklan.mov"), "sfx": str(REPO / "motion/iklan/assets/ding.wav"), "sfx_vol": 0.6},
            "hold": HOLD,
            "broll": [{"src": str(WD / "broll_hook.mp4"), "start": 0, "dur": hd}] +
                     [{"src": str(WD / f"broll_{n}.mp4"), "start": fin(b["a"]), "dur": b["dur"]} for n, b in B.items()],
            "overlay": str(WD / "overlay.mov"), "sfx": sfx}
    json.dump(comp, open(REPO / "projects/C0041/compose.json", "w"), indent=1)
    print("data.js + compose.json OK · durasi akhir", D, "· iklan @", INS)
    for t in E["titles"]:
        print(" tajuk", t["start"], "→", t["end"], " ".join(x["text"] for l in t["lines"] for x in l))

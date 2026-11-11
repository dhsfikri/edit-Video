#!/usr/bin/env python3
"""Bina semua lapisan C0175 (TIPS JUALAN #02) selepas pipeline/cut.py:
   B-roll (offer, pakej, nama) → data.js overlay → compose.json.
Guna:  python3 -I projects/C0175/build.py <workdir> [broll] [data]
Semua cue ditulis dalam MASA SUMBER (rakaman asal) dan dipetakan ke timeline melalui cuts.json.
"""
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WD = Path(sys.argv[1]); STEPS = sys.argv[2:] or ["broll", "data"]
cuts = json.load(open(WD / "cuts.json")); words = json.load(open(WD / "words.json"))
BASE = str(WD / "base.mov"); TOTAL = cuts["duration"]; FPS = 30
AD = 4.0; HOLD = 1.0

offs, o = [], 0.0
for s in cuts["segments"]:
    offs.append(o); o += s["end"] - s["start"]


def m(src):
    """masa sumber → masa base.mov"""
    for s, of in zip(cuts["segments"], offs):
        if s["start"] - 0.03 <= src <= s["end"] + 0.03:
            return round(of + src - s["start"], 3)
    raise SystemExit(f"masa sumber {src} tiada dalam mana-mana segmen")


INS = round(offs[7], 3)  # iklan disisip di sempadan G→H (selepas poin 2)
fin = lambda t: round(t + (AD if t >= INS - 1e-6 else 0), 3)  # base → timeline akhir

# ---------- B-roll: tetingkap [a,b] (masa base) + cue (masa sumber) ----------
B = {}
on, off = m(30.55), m(39.0)
B["offer"] = dict(comp="poin", a=on - 0.4, b=off + 0.4, on=on, off=off, pad=12,
                  items=[m(30.75), m(32.15), m(36.85), m(38.18)])
on = m(56.90)
B["pakej"] = dict(comp="pakej", a=on - 0.4, b=INS, pad=30,
                  switches=[[on, 1], [m(65.76), 0], [m(68.50), 1], [m(71.24), 0], [m(75.36), 1], [INS - 0.45, 0]],
                  cards=[dict(**{"in": m(57.41)}, labelAt=m(60.51), priceAt=m(64.15), subAt=m(64.75)),
                         dict(**{"in": m(68.58)}, labelAt=m(68.80), priceAt=m(69.32), subAt=m(70.50)),
                         dict(**{"in": m(75.45)}, labelAt=m(75.70), bestAt=m(76.85), priceAt=m(77.55), subAt=m(78.15))],
                  note=m(78.85))
on, off = m(88.30), m(92.45)
B["nama"] = dict(comp="poin", a=on - 0.4, b=off + 0.4, on=on, off=off, pad=12,
                 items=[m(88.42), m(89.75), m(91.25)])
for b in B.values():
    b["a"] = round(b["a"] * FPS) / FPS; b["dur"] = round((b["b"] - b["a"]) * FPS) / FPS


def rel(b, t):
    return round(t - b["a"], 3)


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


if "broll" in STEPS:
    for name, b in B.items():
        adir = REPO / "motion" / b["comp"] / "assets"
        ar, fc, tmp = adir / ("aroll_cur.mp4" if b.get("comp", "poin") == "poin" else f"aroll_{name}.mp4"), adir / ("face_cur.mp4" if b.get("comp", "poin") == "poin" else f"face_{name}.mp4"), WD / f"_face_{name}.mp4"  # poin: src statik
        pad = b["pad"] - b["dur"] + 0.5
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['a']:.3f}", "-t", f"{b['dur']:.3f}", "-i", BASE, "-an",
             "-vf", f"fps={FPS},tpad=stop_mode=clone:stop_duration={pad:.2f}", "-t", str(b["pad"]),
             "-c:v", "libx264", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p", str(ar)])
        run([sys.executable, "-I", str(REPO / "pipeline/facecrop.py"), BASE, str(tmp), "--rotate", "none",
             "--seg", f"{b['a']:.3f}:{b['b']:.3f}", "--fps", str(FPS)])
        run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}", "-t", str(b["pad"]),
             "-c:v", "libx264", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p", str(fc)])
        if b["comp"] == "pakej":
            cue = dict(cards=[{k: rel(b, v) for k, v in c.items()} for c in b["cards"]],
                       switches=[[rel(b, t), on_] for t, on_ in b["switches"]], note=rel(b, b["note"]))
            var = dict(face=f"assets/{fc.name}", aroll=f"assets/{ar.name}", cue=json.dumps(cue))
        else:
            cue = dict(on=rel(b, b["on"]), off=rel(b, b["off"]), items=[rel(b, t) for t in b["items"]])
            var = dict(scene=name, face=f"assets/{fc.name}", aroll=f"assets/{ar.name}", cue=json.dumps(cue))
        raw = WD / f"_broll_{name}.mp4"
        run(["npx", "hyperframes", "render", "--variables", json.dumps(var), "-f", str(FPS), "-q", "high", "-w", "4", "-o", str(raw)],
            cwd=REPO / "motion" / b["comp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-t", f"{b['dur']:.3f}", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
             str(WD / f"broll_{name}.mp4")])
        print("B-roll", name, f"{b['a']:.2f}–{b['b']:.2f}", cue)

if "data" in STEPS:
    # ---------- subtitle: gabung "-siapa", buang "tempat", anjak selepas iklan ----------
    ws = []
    for w in words:
        t = w["w"].strip()
        if t.startswith("-") and ws:
            ws[-1]["w"] += t; ws[-1]["e"] = w["e"]; continue
        if t == "tempat" and ws:
            ws[-1]["e"] = w["e"]; continue
        d = {"w": t, "s": w["s"], "e": w["e"]}
        if t[:1].isupper() and t[1:2].islower():
            d["b"] = 1  # mula ayat (Whisper huruf besar) → kumpulan subtitle baru
        ws.append(d)
    for w in ws:
        mid = (w["s"] + w["e"]) / 2
        sh = AD if mid >= INS else 0
        w["s"], w["e"] = round(w["s"] + sh, 3), round(min(w["e"], INS) + sh if not sh else w["e"] + sh, 3)
    D = round(TOTAL + AD + HOLD, 3)

    def title(start, end, top, lines):
        t, out = start + 0.05, []
        for ln in lines:
            row = []
            for tok in ln:
                tt = tok[2] if len(tok) > 2 else t
                row.append({"t": round(tt, 3), "text": tok[0], "k": tok[1]}); t += 0.14
            out.append(row)
        return {"start": round(start, 3), "end": round(end, 3), "top": top, "lines": out}

    on_ivs = [[B["offer"]["on"], B["offer"]["off"]]]
    sw = B["pakej"]["switches"]
    on_ivs += [[sw[i][0], sw[i + 1][0]] for i in range(0, len(sw), 2)]
    hide = [[round(a - 0.1, 3), round(b + 0.1, 3)] for a, b in on_ivs] + [[INS - 0.02, INS + AD]]
    hide.append([fin(B["nama"]["on"]) - 0.1, fin(B["nama"]["off"]) + 0.1])
    t3 = fin(INS)
    E = {
        "duration": D, "series": "TIPS JUALAN", "episode": "02", "maxWords": 3, "hideBadge": hide,
        "titles": [
            title(0, m(14.74) - 0.03, 1000, [[("bisnes", "script")], [("STRUGGLE?", "bold")], [("CEK", "bold"), ("3 PERKARA", "box")]]),
            title(m(14.76), B["offer"]["on"] - 0.25, 1070, [[("yang pertama", "script")], [("1. OFFER", "box")]]),
            title(m(40.40), B["pakej"]["switches"][0][0] - 0.25, 1070, [[("nombor dua", "script")], [("2. BUDGET", "box")]]),
            title(t3 + 0.1, fin(B["nama"]["on"]) - 0.25, 1070, [[("yang ketiga, paling penting", "script")], [("3. NAMA BAIK", "box", fin(m(85.80)))]]),
            title(fin(B["nama"]["off"]) + 0.3, D, 1010, [[("OFFER · BUDGET", "bold")], [("NAMA BAIK", "box")]]),
        ],
        "brackets": [], "callouts": [],
        "cta": {"start": round(TOTAL + AD + 0.1, 3), "text": "🔔 follow @sirdharma_"},
        "words": ws,
    }
    js = "// Data overlay Gaya v2 untuk C0175 (TIPS JUALAN #02) — dijana oleh projects/C0175/build.py\nwindow.EDIT = " + json.dumps(E, ensure_ascii=False, indent=1) + ";\n"
    (REPO / "projects/C0175/data.js").write_text(js); (REPO / "motion/overlay-v2/data.js").write_text(js)

    # ---------- compose.json ----------
    A = str(REPO / "motion/pakej/assets")
    sfx = [{"src": str(REPO / "motion/intro/assets/signature.wav"), "at": 0.03, "vol": 0.4}]
    for name, b in B.items():
        sws = b["switches"] if "switches" in b else [[b["on"], 1], [b["off"], 0]]
        for t, _ in sws:
            sfx.append({"src": A + "/whoosh.wav", "at": round(fin(t) - 0.24, 3), "vol": 0.22})
        for t in ([c["in"] for c in b["cards"]] if "cards" in b else b["items"]):
            sfx.append({"src": A + "/pop.wav", "at": fin(t), "vol": 0.14})
        for c in b.get("cards", []):
            sfx.append({"src": A + "/tick.wav", "at": round(fin(c["priceAt"]) + 0.32, 3), "vol": 0.12})
    comp = {
        "base": BASE, "out": str(WD / "C0175_draf_v1.mp4"), "fps": FPS,
        "insert": {"at": INS, "dur": AD, "overlay": str(WD / "iklan.mov"), "sfx": str(REPO / "motion/iklan/assets/ding.wav"), "sfx_vol": 0.6},
        "hold": HOLD,
        "broll": [{"src": str(WD / f"broll_{n}.mp4"), "start": fin(b["a"]), "dur": b["dur"]} for n, b in B.items()],
        "overlay": str(WD / "overlay.mov"), "sfx": sfx,
    }
    json.dump(comp, open(REPO / "projects/C0175/compose.json", "w"), indent=1)
    print("data.js + compose.json OK · durasi akhir", D, "· iklan @", INS)
    for t in E["titles"]:
        print(" tajuk", t["start"], "→", t["end"], " ".join(x["text"] for l in t["lines"] for x in l))

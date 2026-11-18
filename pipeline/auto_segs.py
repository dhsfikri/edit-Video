#!/usr/bin/env python3
"""Julat ayat → segmen edit.json dengan jeda dibuang (ikut tenaga audio).

Guna: python3 pipeline/auto_segs.py <audio16k.wav> <transcript.json> <ranges.json> <out_segments.json> [--thr -24] [--gap 0.32]
ranges.json: [["nota", mula, akhir], ...] (saat raw, ikut susunan dalam video)
Ambang (thr, dB) lalai = lantai bising + 9 dB (dikira automatik) jika tidak diberi.
"""
import json, sys, wave, argparse
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("wav"); ap.add_argument("tr"); ap.add_argument("ranges"); ap.add_argument("out")
ap.add_argument("--thr", type=float); ap.add_argument("--gap", type=float, default=0.32)
a = ap.parse_args()
w = wave.open(a.wav); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
hop = 0.02; n = int(len(x) / sr / hop)
db = np.array([20 * np.log10(np.sqrt((x[int(i*hop*sr):int((i+1)*hop*sr)] ** 2).mean()) + 1e-9) for i in range(n)])
thr = a.thr if a.thr is not None else float(np.percentile(db, 10)) + 9
W = [q for s in json.load(open(a.tr))["segments"] for q in s["words"]]
out, tot = [], 0
for name, s0, e0 in json.load(open(a.ranges)):
    i0, i1 = int(s0 / hop), int(e0 / hop)
    loud = np.where(db[i0:i1] >= thr)[0]
    if not len(loud): continue
    st, en = i0 + loud[0], i0 + loud[-1] + 1
    pieces, cur, run = [], st, 0
    for i in range(st, en):
        if db[i] < thr: run += 1
        else:
            if run * hop >= a.gap: pieces.append((cur, i - run)); cur = i
            run = 0
    pieces.append((cur, en))
    for p, q in pieces:
        s, e = round(max(s0, p * hop - 0.08), 2), round(min(e0, q * hop + 0.14), 2); tot += e - s
        txt = " ".join(q2["w"] for q2 in W if s <= (q2["s"] + q2["e"]) / 2 <= e)
        out.append({"note": f"{name}: {txt}", "start": s, "end": e, "zoom": 1.0, "cy": 0.0})
        print(f"{s:6.2f}-{e:6.2f} {e-s:4.2f} {name}: {txt}")
print(f"ambang {thr:.1f} dB · jumlah {tot:.2f}s · {len(out)} segmen")
json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)

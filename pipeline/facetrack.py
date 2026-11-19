#!/usr/bin/env python3
"""Jejak muka Sir sepanjang video (untuk hook crash-zoom & bulatan ikut muka dalam motion/editorial).

Guna:  python3 -I pipeline/facetrack.py <base.mov> <facetrack.json> [--step 0.12] [--maxx 760] [--min 210]
Output: [[t, x, y], ...] dalam ruang 1080x1920 (pusat muka), dilicinkan (purata 7 sampel).
- Frame diskala ke 1080x1920 dulu (rakaman 4K 1440x2560 pun sama).
- Calon dengan x > --maxx dibuang (maskot JERUNG / poster di kanan set lama).
- Pilih calon paling dekat dengan kedudukan sebelumnya (elak lompat ke muka lain).
"""
import argparse, json
import cv2, numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--step", type=float, default=0.12)
ap.add_argument("--maxx", type=int, default=760)
ap.add_argument("--min", type=int, default=210)
a = ap.parse_args()

cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(a.src)
fps = cap.get(cv2.CAP_PROP_FPS) or 25
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
every = max(1, round(a.step * fps))
raw, prev, i = [], None, 0
while True:
    ok = cap.grab()
    if not ok:
        break
    if i % every == 0:
        _, fr = cap.retrieve()
        g = cv2.cvtColor(cv2.resize(fr, (1080, 1920)), cv2.COLOR_BGR2GRAY)
        fs = cas.detectMultiScale(g, 1.1, 5, minSize=(a.min, a.min))
        c = [(x + w / 2, y + h / 2) for x, y, w, h in fs if x + w / 2 <= a.maxx]
        if c:
            p = min(c, key=lambda q: (q[0] - prev[0]) ** 2 + (q[1] - prev[1]) ** 2) if prev else max(c, key=lambda q: q[1])
            prev = p
        raw.append([round(i / fps, 2), prev])
    i += 1
first = next((p for _, p in raw if p), (540, 760))
pts = [[t, p or first] for t, p in raw]
xs = np.array([p[0] for _, p in pts]); ys = np.array([p[1] for _, p in pts])
k = np.ones(7) / 7
sm = lambda v: np.convolve(np.pad(v, 3, mode="edge"), k, mode="valid")
xs, ys = sm(xs), sm(ys)
out = [[t, int(round(x)), int(round(y))] for (t, _), x, y in zip(pts, xs, ys)]
json.dump(out, open(a.out, "w"))
print(f"OK {len(out)} sampel, median muka ({int(np.median(xs))}, {int(np.median(ys))})")

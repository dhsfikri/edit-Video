#!/usr/bin/env python3
"""Kunci PARAS MATA sama di setiap scene (zoom in / zoom out), ikut muka setiap frame.

Guna:  python3 -I pipeline/eyeline.py projects/<ID>/edit.json
Perlu: base.mov dari pipeline/cut.py (zoom 1.0) + cuts.json dalam workdir.

edit.json:
  "eyeline": {"y": 620, "x": 540}          # kedudukan mata dalam frame 1080x1920
  segments[i].zk: [[t_rel, zoom], ...]      # keyframe zoom dalam segmen (saat dari mula segmen);
                                            # dua keyframe rapat (≤0.2s) = punch-in laju
Output: base_eye.mov (ganti base.mov dalam langkah seterusnya), eyeline.json (zoom & mata per frame).

- Muka dikesan (OpenCV Haar) setiap 2 frame, dilicinkan DALAM segmen sahaja (tiada seretan merentas potongan).
- Mata ≈ 42% dari atas kotak muka. Tetingkap crop dikira dalam koordinat sumber → satu resize sahaja.
- Zoom minimum disyorkan 1.12 supaya ada ruang untuk anjak frame (kalau tak cukup ruang, mata diklamp).
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np, cv2

cfg = json.load(open(sys.argv[1]))
wd = Path(cfg["workdir"]); cuts = json.load(open(wd / "cuts.json"))
EY = cfg.get("eyeline", {}).get("y", 620); EX = cfg.get("eyeline", {}).get("x", 540)
fps = cfg.get("fps", 30); W, H = 1080, 1920
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(str(wd / "base.mov"))
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
cap.release()
N = len(frames)

# segmen dalam index frame
bounds, o = [], 0.0
for s in cuts["segments"]:
    d = s["end"] - s["start"]; bounds.append((int(round(o * fps)), int(round((o + d) * fps)))); o += d
bounds[-1] = (bounds[-1][0], N)


def zoom_at(zk, t):
    if len(zk) == 1 or t <= zk[0][0]:
        return zk[0][1]
    for (t0, z0), (t1, z1) in zip(zk, zk[1:]):
        if t <= t1:
            u = (t - t0) / max(t1 - t0, 1e-6)
            u = u * u * (3 - 2 * u)  # ease in-out
            return z0 + (z1 - z0) * u
    return zk[-1][1]


out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                        "-i", str(wd / "base.mov"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "12",
                        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                        "-c:a", "copy", "-shortest", str(wd / "base_eye.mov")], stdin=subprocess.PIPE)
log = []
for (a, b), seg in zip(bounds, cfg["segments"]):
    dets = {}
    for i in range(a, b, 2):
        g = cv2.cvtColor(cv2.resize(frames[i], None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY)
        fs = casc.detectMultiScale(g, 1.1, 5, minSize=(80, 80))
        if len(fs):
            x, y, w, h = max(fs, key=lambda r: r[2] * r[3])
            dets[i] = (2 * (x + w / 2), 2 * (y + 0.42 * h))
    idx = sorted(dets)
    if not idx:
        raise SystemExit(f"Tiada muka dalam segmen {seg['note']}")
    arr = np.array([dets[i] for i in idx])
    rng = np.arange(a, b)
    track = np.stack([np.interp(rng, idx, arr[:, k]) for k in range(2)], 1)
    k = max(1, int(fps * 0.6)); ker = np.ones(k) / k
    track = np.stack([np.convolve(np.pad(track[:, j], (k, k), mode="edge"), ker, "same")[k:-k] for j in range(2)], 1)
    zk = seg.get("zk") or [[0, seg.get("zoom", 1.12)]]
    for n, i in enumerate(rng):
        z = zoom_at(zk, n / fps); cx, ey = track[n]
        cw, ch = W / z, H / z
        x0 = float(np.clip(cx - EX / z, 0, W - cw)); y0 = float(np.clip(ey - EY / z, 0, H - ch))
        M = np.array([[z, 0, -x0 * z], [0, z, -y0 * z]], np.float32)
        out.stdin.write(cv2.warpAffine(frames[i], M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
        log.append({"f": int(i), "z": round(z, 3), "eye_y": round((ey - y0) * z, 1), "eye_x": round((cx - x0) * z, 1)})
out.stdin.close(); out.wait()
json.dump(log, open(wd / "eyeline.json", "w"))
ys = np.array([l["eye_y"] for l in log])
print(f"OK base_eye.mov {len(log)} frame · mata y: median {np.median(ys):.0f}, min {ys.min():.0f}, max {ys.max():.0f} (sasaran {EY})")

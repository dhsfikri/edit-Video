#!/usr/bin/env python3
"""Hasilkan klip muka (kotak segi empat, ikut muka) untuk bulatan PiP dalam babak explainer.

Guna:
  python3 pipeline/facecrop.py SRC OUT.mp4 --rotate ccw --seg 23.42:24.9 --seg 5.95:7.6 [--size 480] [--box 2.6]

- Kesan muka (OpenCV Haar) setiap 3 frame, isi jurang & licinkan, kemudian crop kotak
  bersaiz `box` x lebar muka (kepala + bahu) berpusat sedikit di bawah muka.
- Segmen digabung mengikut susunan --seg.
"""
import argparse, subprocess, json
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--rotate", default="none", choices=["cw", "ccw", "none"])
ap.add_argument("--seg", action="append", required=True)
ap.add_argument("--size", type=int, default=480)
ap.add_argument("--box", type=float, default=2.6)
ap.add_argument("--fps", type=float, default=30)
a = ap.parse_args()

casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
rot = {"cw": cv2.ROTATE_90_CLOCKWISE, "ccw": cv2.ROTATE_90_COUNTERCLOCKWISE}.get(a.rotate)

frames_out = []
for seg in a.seg:
    t0, t1 = map(float, seg.split(":"))
    cap = cv2.VideoCapture(a.src)
    cap.set(cv2.CAP_PROP_POS_MSEC, t0 * 1000)
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(round((t1 - t0) * src_fps))
    imgs, dets = [], []
    for i in range(n):
        ok, f = cap.read()
        if not ok:
            break
        if rot is not None:
            f = cv2.rotate(f, rot)
        imgs.append(f)
        d = None
        if i % 3 == 0:
            g = cv2.cvtColor(cv2.resize(f, None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY)
            fs = casc.detectMultiScale(g, 1.1, 5, minSize=(30, 30))
            if len(fs):
                x, y, w, h = max(fs, key=lambda r: r[2] * r[3])
                d = (2 * (x + w / 2), 2 * (y + h / 2), 2 * w)
        dets.append(d)
    cap.release()
    idx = [i for i, d in enumerate(dets) if d]
    if not idx:
        raise SystemExit(f"Tiada muka dikesan dalam segmen {seg}")
    arr = np.array([dets[i] for i in idx], float)
    full = np.stack([np.interp(range(len(imgs)), idx, arr[:, k]) for k in range(3)], 1)
    # licinkan (purata bergerak ~0.5s) supaya kamera maya tak bergegar
    k = max(1, int(src_fps * 0.5))
    ker = np.ones(k) / k
    sm = np.stack([np.convolve(np.pad(full[:, j], (k, k), mode="edge"), ker, "same")[k:-k] for j in range(3)], 1)
    side = float(np.median(sm[:, 2]) * a.box)
    for f, (cx, cy, _) in zip(imgs, sm):
        H, W = f.shape[:2]
        s = int(min(side, W, H))
        x0 = int(np.clip(cx - s / 2, 0, W - s))
        y0 = int(np.clip(cy - s * 0.38, 0, H - s))
        frames_out.append(cv2.resize(f[y0:y0 + s, x0:x0 + s], (a.size, a.size), interpolation=cv2.INTER_LANCZOS4))

p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{a.size}x{a.size}",
                      "-r", str(a.fps), "-i", "-", "-vf", "eq=saturation=0.9:contrast=1.03", "-c:v", "libx264", "-crf", "14",
                      "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
for f in frames_out:
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
print(json.dumps({"out": a.out, "frames": len(frames_out), "seconds": round(len(frames_out) / a.fps, 2)}))

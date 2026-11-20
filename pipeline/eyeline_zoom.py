#!/usr/bin/env python3
"""Zoom dekat muka dengan EYE LINE tetap (crop ikut muka setiap frame).

Guna (biasanya untuk segmen hook):
  python3 -I pipeline/eyeline_zoom.py SRC OUT.mov --start 5.705 --dur 5.0 --zoom 1.55 --zoom-to 1.7 \
      --eye-y 1060 --fps 25 [--color "eq=..."] [--detect DETECT_SRC]

- SRC: rakaman asal (4K, ffmpeg auto-rotate). DETECT_SRC (pilihan): versi kecil untuk kesan muka (lebih laju).
- zoom relatif kepada frame penuh (1.0 = lebar penuh dimuatkan ke 1080), sama macam cut.py.
- Mata dikunci pada y = --eye-y (piksel output 1920), muka di tengah mendatar; dilicinkan supaya tak bergegar.
- Output: video sahaja 1080x1920 (gabung audio dari segmen cut.py yang sama).
"""
import argparse, json, subprocess
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--start", type=float, required=True); ap.add_argument("--dur", type=float, required=True)
ap.add_argument("--zoom", type=float, default=1.6); ap.add_argument("--zoom-to", type=float, default=None)
ap.add_argument("--eye-y", type=float, default=1060); ap.add_argument("--fps", type=float, default=25)
ap.add_argument("--color", default="null"); ap.add_argument("--detect", default=None)
a = ap.parse_args()
z1 = a.zoom_to or a.zoom
n = int(round(a.dur * a.fps))

def probe(f):
    o = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height:stream_side_data=rotation", "-of", "json", f]))["streams"][0]
    w, h = o["width"], o["height"]
    rot = [s.get("rotation", 0) for s in o.get("side_data_list", [])]
    return (h, w) if rot and abs(rot[0]) == 90 else (w, h)

def frames(f, w, h):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(a.start), "-i", f, "-t", str(a.dur), "-r", str(a.fps),
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE, bufsize=w * h * 3)
    for _ in range(n):
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.stdout.close(); p.wait()

# 1) Kesan muka (pada versi kecil), nilai dinormalkan 0..1
det = a.detect or a.src
dw, dh = probe(det)
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
raw = []
for f in frames(det, dw, dh):
    s = 720 / dw
    g = cv2.cvtColor(cv2.resize(f, None, fx=s, fy=s), cv2.COLOR_BGR2GRAY)
    fs = casc.detectMultiScale(g, 1.1, 6, minSize=(80, 80))
    if len(fs):
        x, y, w, h = max(fs, key=lambda r: r[2])
        raw.append(((x + w / 2) / s / dw, (y + 0.42 * h) / s / dh))  # pusat muka, paras mata
    else:
        raw.append(None)
idx = [i for i, r in enumerate(raw) if r]
if not idx: raise SystemExit("muka tak dijumpai")
cx = np.interp(range(len(raw)), idx, [raw[i][0] for i in idx])
ey = np.interp(range(len(raw)), idx, [raw[i][1] for i in idx])
# licinkan: median (buang lonjakan) + purata bergerak ~0.6s
def smooth(v, k=int(a.fps * 0.6) | 1):
    m = np.array([np.median(v[max(0, i - 3):i + 4]) for i in range(len(v))])
    pad = np.pad(m, k // 2, mode="edge")
    return np.convolve(pad, np.ones(k) / k, mode="valid")
cx, ey = smooth(cx), smooth(ey)

# 2) Crop 4K ikut muka, resize ke 1080x1920
sw, sh = probe(a.src)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920",
    "-r", str(a.fps), "-i", "-", "-vf", f"setsar=1,{a.color}", "-c:v", "libx264", "-preset", "medium", "-crf", "12",
    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", a.out],
    stdin=subprocess.PIPE)
cnt = 0
for i, f in enumerate(frames(a.src, sw, sh)):
    j = min(i, len(cx) - 1)
    z = a.zoom + (z1 - a.zoom) * i / max(n - 1, 1)
    cw, ch = sw / z, sh / z                      # saiz crop dalam piksel sumber (nisbah 9:16)
    left = np.clip(cx[j] * sw - cw / 2, 0, sw - cw)
    top = np.clip(ey[j] * sh - a.eye_y / 1920 * ch, 0, sh - ch)
    crop = f[int(top):int(top + ch), int(left):int(left + cw)]
    enc.stdin.write(cv2.resize(crop, (1080, 1920), interpolation=cv2.INTER_LANCZOS4).tobytes())
    cnt += 1
enc.stdin.close(); enc.wait()
print(json.dumps({"out": a.out, "frames": cnt, "eye_y_src_range": [round(float(ey.min()), 3), round(float(ey.max()), 3)]}))

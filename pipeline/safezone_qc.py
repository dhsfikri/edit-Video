#!/usr/bin/env python3
"""QC safe zone TikTok: ambil beberapa frame dari video, lukis zon larangan (merah) dan zon selamat (cyan).

Guna:  python3 pipeline/safezone_qc.py VIDEO.mp4 [OUT.png] [--times 0.5,2,5 ...]
Tanpa --times: 8 frame sama rata.
Zon (BRANDKIT.md §5): atas y<220, bawah y>1440, kanan x>900 (y 700–1500).
"""
import subprocess, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out", nargs="?", default=None)
ap.add_argument("--times", default=None)
a = ap.parse_args()
out = a.out or a.video.rsplit(".", 1)[0] + "_safezone.png"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video]))
ts = [float(x) for x in a.times.split(",")] if a.times else [round(dur * (i + 0.5) / 8, 2) for i in range(8)]

zones = ("drawbox=x=0:y=0:w=1080:h=220:color=red@0.35:t=fill,"
         "drawbox=x=0:y=1440:w=1080:h=480:color=red@0.35:t=fill,"
         "drawbox=x=900:y=700:w=180:h=800:color=red@0.35:t=fill,"
         "drawbox=x=60:y=220:w=840:h=1220:color=cyan@0.9:t=4")
inputs, labels = [], []
for i, t in enumerate(ts):
    inputs += ["-ss", str(t), "-i", a.video]
    labels.append(f"[{i}:v]trim=end_frame=1,{zones},scale=270:-1,"
                  f"drawtext=text='{t}s':fontcolor=yellow:fontsize=20:x=6:y=6:box=1:boxcolor=black[f{i}]")
fc = ";".join(labels) + ";" + "".join(f"[f{i}]" for i in range(len(ts))) + f"hstack=inputs={len(ts)}"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-frames:v", "1", out], check=True)
print(out)

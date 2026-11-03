#!/usr/bin/env python3
"""Potong A-roll ikut senarai segmen, pusing, zoom, betulkan warna & audio.

Guna:  python3 pipeline/cut.py projects/<nama>/edit.json

edit.json:
{
  "source": "/path/C0029.MP4",
  "transcript": "/path/raw_transcript.json",   # output faster-whisper (word timestamps)
  "workdir": "/path/out",
  "rotate": "cw",                               # cw | ccw | none
  "fps": 50,
  "color": "eq=brightness=0.03:contrast=1.06:saturation=1.08:gamma=1.08",
  "corrections": {"say": "sale"},
  "segments": [{"start": 7.82, "end": 11.15, "zoom": 1.0, "zoom_to": 1.0, "cy": 0.42}, ...]
}

Output (dalam workdir):
  base.mp4    — A-roll siap potong (1080x1920, CRF 12, audio dinormalkan -14 LUFS)
  words.json  — perkataan + masa baru dalam video yang dah dipotong (untuk subtitle)
  cuts.json   — masa sebenar setiap potongan (selepas snap ke titik senyap)
"""
import json, subprocess, sys, wave
from pathlib import Path

import numpy as np

W, H = 1080, 1920


def run(cmd):
    subprocess.run(cmd, check=True)


def load_audio(src, sr=16000):
    tmp = Path(cfg["workdir"]) / "_snap.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", str(sr), str(tmp)])
    w = wave.open(str(tmp))
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a, sr


def snap(t, a, sr, win=0.12, direction=0):
    """Cari titik paling senyap dekat t (tetingkap 20ms), supaya potongan tak makan suku kata."""
    lo = t - win if direction <= 0 else t
    hi = t + win if direction >= 0 else t
    best, best_e = t, 1e9
    step = 0.005
    for x in np.arange(max(lo, 0), hi, step):
        i = int(x * sr)
        seg = a[i : i + int(0.02 * sr)]
        if len(seg) == 0:
            continue
        e = float(np.sqrt(np.mean(seg**2)))
        if e < best_e:
            best, best_e = x, e
    return round(float(best), 3)


cfg = json.load(open(sys.argv[1]))
out = Path(cfg["workdir"])
out.mkdir(parents=True, exist_ok=True)
fps = cfg.get("fps", 30)
audio, sr = load_audio(cfg["source"])

segs = []
for s in cfg["segments"]:
    # mula: cari ke hadapan sahaja (elak tertarik perkataan sebelumnya, cth "So")
    st = snap(s["start"], audio, sr, win=0.05, direction=1)
    en = snap(s["end"], audio, sr)
    segs.append({**s, "start": st, "end": en})

rot = {"cw": "transpose=1,", "ccw": "transpose=2,", "none": ""}[cfg.get("rotate", "none")]
color = cfg.get("color", "null")

parts, labels = [], []
for i, s in enumerate(segs):
    d = s["end"] - s["start"]
    z0, z1 = s.get("zoom", 1.0), s.get("zoom_to", s.get("zoom", 1.0))
    cy = s.get("cy", 0.42)  # pusat zoom menegak (muka)
    # zoom linear z0 -> z1 sepanjang segmen: scale ikut frame, kemudian crop 1080x1920 berpusat pada muka
    z = f"({z0}+({z1}-{z0})*t/{d:.3f})" if z0 != z1 else str(z0)
    zoom = (
        f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:x='(iw-{W})/2':y='(ih-{H})*{cy}'"
    )
    vf = (
        f"[0:v]trim={s['start']}:{s['end']},setpts=PTS-STARTPTS,{rot}fps={fps},"
        f"{zoom},setsar=1,{color}[v{i}]"
    )
    af = (
        f"[0:a]atrim={s['start']}:{s['end']},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d=0.012,afade=t=out:st={max(d-0.015,0):.3f}:d=0.015[a{i}]"
    )
    parts += [vf, af]
    labels.append(f"[v{i}][a{i}]")

fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[vc][ac];"
fc += "[ac]highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.89,aresample=48000[ao]"

run([
    "ffmpeg", "-v", "error", "-stats", "-y", "-i", cfg["source"],
    "-filter_complex", fc, "-map", "[vc]", "-map", "[ao]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "pcm_s16le", str(out / "base.mov"),
])

# Petakan masa perkataan ke timeline baru
tr = json.load(open(cfg["transcript"]))
words = [w for seg in tr["segments"] for w in seg["words"]]
fix = {k.lower(): v for k, v in cfg.get("corrections", {}).items()}
mapped, offset = [], 0.0
for s in segs:
    for w in words:
        mid = (w["s"] + w["e"]) / 2
        if s["start"] - 0.02 <= mid <= s["end"] + 0.02:
            raw = w["w"].strip()
            core = raw.strip(",.?!").lower()
            text = raw.replace(raw.strip(",.?!"), fix[core]) if core in fix else raw
            mapped.append({
                "w": text,
                "s": round(max(w["s"], s["start"]) - s["start"] + offset, 3),
                "e": round(min(w["e"], s["end"]) - s["start"] + offset, 3),
            })
    offset += s["end"] - s["start"]

json.dump(mapped, open(out / "words.json", "w"), ensure_ascii=False, indent=1)
json.dump({"segments": segs, "duration": round(offset, 3)}, open(out / "cuts.json", "w"), indent=1)
print(f"OK base.mov {offset:.2f}s, {len(mapped)} perkataan")

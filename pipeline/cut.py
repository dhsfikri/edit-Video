#!/usr/bin/env python3
"""Potong A-roll ikut senarai segmen, pusing, zoom, betulkan warna & audio.

Guna:  python3 pipeline/cut.py projects/<nama>/edit.json

edit.json:
{
  "source": "/path/C0029.MP4",
  "transcript": "/path/raw_transcript.json",   # output faster-whisper (word timestamps)
  "workdir": "/path/out",
  "rotate": "cw",                               # cw | ccw | none
  "precrop": "crop=1215:2160:1620:0",           # pilihan: crop rakaman landscape 4K ke 9:16 SEBELUM zoom
  "pretranscode": true,                         # pilihan: salinan perantara dulu (elak kehabisan memori, rakaman bitrate tinggi)
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
# "size": [1440, 2560] → output resolusi lebih tinggi (rakaman 4K) supaya punch-in/zoom dalam HyperFrames kekal tajam
W, H = cfg.get("size", [W, H])
out = Path(cfg["workdir"])
out.mkdir(parents=True, exist_ok=True)
fps = cfg.get("fps", 30)
# Rakaman Sony bitrate tinggi (10-bit, 50+ Mbps) → filter_complex dengan banyak trim boleh kehabisan memori.
# "pretranscode": true → buat salinan perantara 1080-lebar CRF 12 sekali lalu (precrop/rotate dipakai di sini), kemudian potong dari salinan itu.
if cfg.get("pretranscode"):
    src_mid = out / "_src.mov"
    if not src_mid.exists():
        vf = ",".join(f for f in [cfg.get("precrop", ""), {"cw": "transpose=1", "ccw": "transpose=2"}.get(cfg.get("rotate", "none"), ""), f"scale={W}:-2:flags=lanczos"] if f)
        run(["ffmpeg", "-v", "error", "-y", "-i", cfg["source"], "-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "12",
             "-pix_fmt", "yuv420p", "-threads", "4", "-c:a", "pcm_s16le", str(src_mid)])
    cfg["source"], cfg["precrop"], cfg["rotate"] = str(src_mid), "", "none"
audio, sr = load_audio(cfg["source"])

segs = []
for s in cfg["segments"]:
    # mula: cari ke hadapan sahaja (elak tertarik perkataan sebelumnya, cth "So")
    st = snap(s["start"], audio, sr, win=0.05, direction=1)
    en = snap(s["end"], audio, sr)
    segs.append({**s, "start": st, "end": en})

rot = {"cw": "transpose=1,", "ccw": "transpose=2,", "none": ""}[cfg.get("rotate", "none")]
color = cfg.get("color", "null")
pre = cfg.get("precrop", "")
pre = pre + "," if pre else ""

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
        f"[0:v]trim={s['start']}:{s['end']},setpts=PTS-STARTPTS,{pre}{rot}fps={fps},"
        f"{zoom},setsar=1,{color}[v{i}]"
    )
    af = (
        f"[0:a]atrim={s['start']}:{s['end']},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d=0.012,afade=t=out:st={max(d-0.015,0):.3f}:d=0.015[a{i}]"
    )
    parts += [vf, af]
    labels.append(f"[v{i}][a{i}]")

fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[vc][ac];"
extra = cfg.get("audio_extra", "")
fc += f"[ac]highpass=f=70,{extra + ',' if extra else ''}loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.89,aresample=48000[ao]"

if cfg.get("chunked") or len(segs) > 14:
    # Mod CHUNKED (elak kehabisan memori): setiap segmen di-encode berasingan (seek pantas), kemudian concat + loudnorm sekali
    tmpd = out / "_chunks"; tmpd.mkdir(exist_ok=True); lst = []
    for i, s in enumerate(segs):
        d = s["end"] - s["start"]
        vfi = parts[2 * i].split("]", 1)[1].rsplit("[", 1)[0].replace(f"trim={s['start']}:{s['end']},setpts=PTS-STARTPTS,", "")
        afi = f"afade=t=in:d=0.012,afade=t=out:st={max(d-0.015,0):.3f}:d=0.015"
        cf = tmpd / f"c{i:03d}.mov"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['start']:.3f}", "-i", cfg["source"], "-t", f"{d:.3f}",
             "-vf", vfi, "-af", afi, "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p",
             "-c:a", "pcm_s16le", "-ar", "48000", str(cf)])
        lst.append(f"file '{cf}'")
    (tmpd / "list.txt").write_text("\n".join(lst))
    af2 = f"highpass=f=70,{extra + ',' if extra else ''}loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.89,aresample=48000"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmpd / "list.txt"), "-af", af2,
         "-c:v", "copy", "-c:a", "pcm_s16le", str(out / "base.mov")])
else:
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

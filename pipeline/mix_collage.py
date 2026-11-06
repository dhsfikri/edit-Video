#!/usr/bin/env python3
"""Gabung render collage (visual penuh, tanpa audio) + audio A-roll + SFX → MP4 akhir.

Guna: python3 -I pipeline/mix_collage.py <visual.mp4> <base.mov> <mix.json> <sfx_dir> <out.mp4>
mix.json: {"hold": 1.5, "sfx": [[nama, saat, vol], ...]}   (hold = saat frame akhir ditahan → audio dipad senyap)
"""
import json, subprocess, sys
vis, base, cfgp, sfxdir, out = sys.argv[1:6]
c = json.load(open(cfgp))
inputs = ["-i", vis, "-i", base]
fc = [f"[1:a]apad=pad_dur={c.get('hold', 0)}[voice]"]
mix = ["[voice]"]
for i, (name, at, vol) in enumerate(c["sfx"]):
    inputs += ["-i", f"{sfxdir}/{name}.wav"]
    ms = int(at * 1000)
    fc.append(f"[{i+2}:a]volume={vol},adelay={ms}|{ms},aresample=48000[s{i}]")
    mix.append(f"[s{i}]")
fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,alimiter=limit=0.79:level=false[aout]")
dur = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vis]).decode().strip()
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]", "-t", dur,
    "-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-crf", "16", "-maxrate", "20M", "-bufsize", "30M", "-g", "60",
    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
print("OK", out, dur)

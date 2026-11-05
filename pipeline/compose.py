#!/usr/bin/env python3
"""Gabung semua lapisan jadi video akhir.

Guna:  python3 pipeline/compose.py projects/<nama>/compose.json

compose.json:
{
  "base": ".../base.mov",                 # A-roll siap potong (dari cut.py)
  "out": ".../C0029_draf_v2.mp4",
  "fps": 50,
  "insert": {"at": 14.42, "dur": 2.0, "overlay": ".../iklan.mov", "sfx": ".../ding.wav"},
        # optional: hentikan video pada 'at' (frame beku), tindih iklan, kemudian sambung
  "broll": [{"src": ".../kupon.mp4", "start": 3.45, "dur": 2.5}],   # masa dalam timeline AKHIR
  "overlay": ".../overlay.mov",            # grafik + subtitle (telus), timeline AKHIR
  "blur": [{"x":60,"y":880,"w":840,"h":380,"start":0.05,"end":5,"radius":30}],
        # optional: kawasan kabur (kesan kad kaca) bawah overlay, sudut bulat, fade 0.2s
  "sfx": [{"src": ".../signature.wav", "at": 0.04, "vol": 0.55}]
}
"""
import json, subprocess, sys

c = json.load(open(sys.argv[1]))
fps = c.get("fps", 50)
ins = c.get("insert")
inputs = ["-i", c["base"]]
idx = 1
fc = []

# 1) A-roll (dengan sisipan frame beku jika ada)
if ins:
    at, d = ins["at"], ins["dur"]
    fc += [
        f"[0:v]split[va][vb]",
        f"[va]trim=0:{at},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d}[v1]",
        f"[vb]trim={at},setpts=PTS-STARTPTS[v2]",
        f"[v1][v2]concat=n=2:v=1:a=0[vbase]",
        f"[0:a]asplit[aa][ab]",
        f"[aa]atrim=0:{at},asetpts=PTS-STARTPTS,afade=t=out:st={at-0.03}:d=0.03,apad=pad_dur={d}[a1]",
        f"[ab]atrim={at},asetpts=PTS-STARTPTS,afade=t=in:d=0.03[a2]",
        f"[a1][a2]concat=n=2:v=0:a=1[abase]",
    ]
else:
    fc += ["[0:v]null[vbase]", "[0:a]anull[abase]"]
cur = "vbase"

# 2) B-roll (penuh skrin, audio A-roll diteruskan)
for i, b in enumerate(c.get("broll", [])):
    inputs += ["-i", b["src"]]
    fc.append(f"[{idx}:v]trim=0:{b['dur']},setpts=PTS-STARTPTS+{b['start']}/TB,fps={fps},format=yuv420p[b{i}]")
    fc.append(f"[{cur}][b{i}]overlay=0:0:eof_action=pass:enable='between(t,{b['start']},{b['start']+b['dur']-0.001})'[vb{i}]")
    cur = f"vb{i}"
    idx += 1

# 2b) Blur kad kaca (sebelum overlay). Masa dalam timeline AKHIR.
for i, g in enumerate(c.get("blur", [])):
    x, y, w, h, r = g["x"], g["y"], g["w"], g["h"], g.get("radius", 30)
    st, en = g["start"], g["end"]
    fd = min(0.2, (en - st) / 3)
    rr = f"if(gte(X,{r})*lt(X,W-{r})+gte(Y,{r})*lt(Y,H-{r})+lte(hypot(min(X,W-1-X)-{r},min(Y,H-1-Y)-{r}),{r}),255,0)"
    fc += [
        f"[{cur}]split[gb{i}a][gb{i}b]",
        f"[gb{i}b]crop={w}:{h}:{x}:{y},boxblur=22:3,eq=brightness=-0.04,format=yuva420p[gb{i}c]",
        # topeng sudut bulat: kira SEKALI (1 frame) kemudian ulang — geq setiap frame terlalu perlahan
        f"color=c=black:s={w}x{h}:r={fps}:d={1/fps:.4f},format=gray,geq=lum='{rr}',loop=loop=-1:size=1,setpts=N/{fps}/TB[gb{i}m]",
        f"[gb{i}c][gb{i}m]alphamerge,fade=t=in:st={st}:d={fd}:alpha=1,fade=t=out:st={en - fd}:d={fd}:alpha=1[gb{i}d]",
        f"[gb{i}a][gb{i}d]overlay={x}:{y}:shortest=1:enable='between(t,{st},{en})'[gb{i}o]",
    ]
    cur = f"gb{i}o"

# 3) Overlay grafik + subtitle
if c.get("overlay"):
    inputs += ["-i", c["overlay"]]
    fc.append(f"[{idx}:v]format=yuva444p[ovl]")
    fc.append(f"[{cur}][ovl]overlay=0:0:format=auto:eof_action=pass[vo]")
    cur = "vo"
    idx += 1

# 4) Iklan di atas segalanya
if ins and ins.get("overlay"):
    inputs += ["-i", ins["overlay"]]
    fc.append(f"[{idx}:v]format=yuva444p,setpts=PTS-STARTPTS+{ins['at']}/TB[adv]")
    fc.append(f"[{cur}][adv]overlay=0:0:format=auto:eof_action=pass:enable='between(t,{ins['at']},{ins['at']+ins['dur']-0.001})'[vad]")
    cur = "vad"
    idx += 1
fc.append(f"[{cur}]format=yuv420p[vout]")

# 5) Bunyi tambahan
amix = ["[abase]"]
sfx = list(c.get("sfx", []))
if ins and ins.get("sfx"):
    sfx.append({"src": ins["sfx"], "at": ins["at"], "vol": ins.get("sfx_vol", 0.6)})
for i, s in enumerate(sfx):
    inputs += ["-i", s["src"]]
    ms = int(s["at"] * 1000)
    fc.append(f"[{idx}:a]volume={s.get('vol', 0.55)},adelay={ms}|{ms}[s{i}]")
    amix.append(f"[s{i}]")
    idx += 1
fc.append(f"{''.join(amix)}amix=inputs={len(amix)}:duration=first:normalize=0,alimiter=limit=0.79:level=false[aout]")

total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", c["base"]]))
total += ins["dur"] if ins else 0

cmd = ["ffmpeg", "-v", "error", "-stats", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}", "-r", str(fps),
       "-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-crf", "16", "-maxrate", "20M", "-bufsize", "30M",
       "-g", str(fps * 2), "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
       "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", c["out"]]
subprocess.run(cmd, check=True)
print(f"OK {c['out']} ({total:.2f}s)")

#!/usr/bin/env python3
"""Transkrip Bahasa Melayu dengan word timestamps (faster-whisper medium int8).

Guna: python3 -I pipeline/transcribe.py <audio16k.wav> <out transcript.json>
Sediakan audio: ffmpeg -i RAKAMAN.MP4 -ac 1 -ar 16000 audio16k.wav
Output: {"segments":[{start,end,text,words:[{w,s,e}]}]} — cetak ayat + masa untuk semakan.
"""
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel

w = wave.open(sys.argv[1])
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768  # hantar array (pyav rosak untuk path)
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(a, language="ms", word_timestamps=True, vad_filter=True, beam_size=5)
out = []
for s in segs:
    out.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                "words": [{"w": x.word.strip(), "s": round(x.start, 2), "e": round(x.end, 2)} for x in s.words]})
    print(f"[{s.start:5.1f}-{s.end:5.1f}] {s.text.strip()}", flush=True)
json.dump({"segments": out}, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)

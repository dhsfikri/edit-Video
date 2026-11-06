#!/usr/bin/env python3
"""Jana SFX sintetik (tiada muzik/alat muzik): chop (kapak kena kayu), thud (tumbang), stamp (cop), paper (kertas masuk)."""
import wave
from pathlib import Path
import numpy as np
SR = 48000; OUT = Path(__file__).resolve().parent.parent / "sfx"; rng = np.random.default_rng(3)

def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    w = wave.open(str(OUT / f"{name}.wav"), "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)

def lp(x, k):  # low-pass purata bergerak
    return np.convolve(x, np.ones(k) / k, "same")

n = int(SR * .5); t = np.arange(n) / SR
chop = lp(rng.normal(size=n), 6) * env(n, .001, .035) * 1.2 + np.sin(2*np.pi*(140 - 60*t)*t) * env(n, .002, .09)
save("chop", chop)
n = int(SR * .9); t = np.arange(n) / SR
thud = np.sin(2*np.pi*(70 - 30*t)*t) * env(n, .004, .18) + lp(rng.normal(size=n), 40) * env(n, .002, .12) * 2
save("thud", thud)
n = int(SR * .35); t = np.arange(n) / SR
stamp = lp(rng.normal(size=n), 3) * env(n, .0005, .02) + np.sin(2*np.pi*220*t) * env(n, .001, .05) * .6
save("stamp", stamp)
n = int(SR * .45); t = np.arange(n) / SR
paper = (rng.normal(size=n) - lp(rng.normal(size=n), 30)) * np.sin(np.pi * t / t[-1]) ** 2 * (1 + .5*np.sin(2*np.pi*23*t))
save("paper", paper * .5)
print("OK", sorted(p.name for p in OUT.iterdir()))

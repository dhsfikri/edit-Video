"""Bina audio intro-kinetic (bed + SFX) secara sintetik — bebas hak cipta.
Guna: python3 make_audio.py <output.wav>
Masa SFX ikut timeline index.html.
"""
import sys, wave
import numpy as np

SR = 48000
DUR = 21.5
N = int(SR * DUR)
out = np.zeros(N)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR


def add(sig, at, gain=1.0):
    i = int(at * SR)
    j = min(N, i + len(sig))
    out[i:j] += sig[: j - i] * gain


def env(n, a=0.01, r=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / r)
    return e


def whoosh(d=0.45):
    n = int(SR * d)
    x = rng.standard_normal(n)
    # low-pass bergerak (sapuan) dengan purata bergerak
    y = np.zeros(n); acc = 0
    for k in range(n):
        c = 0.02 + 0.25 * np.sin(np.pi * k / n)
        acc += c * (x[k] - acc); y[k] = acc
    w = np.sin(np.pi * np.arange(n) / n) ** 2
    return y * w * 2.2


def click():
    n = int(SR * 0.03)
    return rng.standard_normal(n) * env(n, 0.0005, 0.006)


def boom(d=1.2):
    n = int(SR * d); t = np.arange(n) / SR
    f = 38 + 60 * np.exp(-t / 0.08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.35) * 1.4


def hit(d=0.5):
    n = int(SR * d); t = np.arange(n) / SR
    f = 70 + 120 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.12)


def riser(d=1.0):
    n = int(SR * d); t = np.arange(n) / SR
    f = 200 + 1400 * (t / d) ** 2
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15 + rng.standard_normal(n) * 0.05
    return s * (t / d) ** 2


# bed: denyut bass 100 BPM + pad lembut
beat = 0.6
for k in range(int(DUR / beat)):
    tt = k * beat
    if 12.4 < tt < 13.6:  # senyap sekejap sekitar klimaks
        continue
    add(hit(0.4), tt, 0.35 if k % 2 == 0 else 0.2)
pad = (np.sin(2 * np.pi * 110 * t_all) + 0.5 * np.sin(2 * np.pi * 164.8 * t_all) + 0.4 * np.sin(2 * np.pi * 220 * t_all)) * 0.03
pad *= np.minimum(1, t_all / 1.5) * np.minimum(1, (DUR - t_all) / 1.5)
out += pad

# SFX
add(hit(0.6), 0.0, 0.9)
for at in [2.6, 4.85, 6.45, 7.7, 16.65, 18.95]:
    add(whoosh(), at, 0.5)
for k in range(18):
    add(click(), 1.1 + k * 0.039, 0.25)
for k in range(25):
    add(click(), 14.1 + k * 0.036, 0.25)
add(hit(0.5), 2.8, 0.7)
add(hit(0.5), 5.05, 0.8)
add(hit(0.4), 5.75, 0.6)
add(hit(0.5), 7.2, 0.7)
add(hit(0.5), 8.45, 0.7)
add(riser(1.0), 11.5, 1.0)
add(boom(), 12.55, 1.0)
add(whoosh(0.35), 13.45, 0.6)
add(hit(0.4), 15.25, 0.6)
add(hit(0.4), 18.4, 0.6)

# signature
try:
    w = wave.open("assets/signature.wav")
    sr2, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    raw = np.frombuffer(w.readframes(w.getnframes()), {2: np.int16, 4: np.int32}[sw]).astype(float)
    raw /= 2 ** (8 * sw - 1)
    if ch > 1:
        raw = raw.reshape(-1, ch).mean(1)
    if sr2 != SR:
        raw = np.interp(np.arange(0, len(raw), sr2 / SR), np.arange(len(raw)), raw)
    add(raw, 19.2, 0.9)
except FileNotFoundError:
    pass

out /= max(1e-9, np.abs(out).max()) / 0.89
pcm = (out * 32767).astype(np.int16)
st = np.repeat(pcm[:, None], 2, axis=1)
o = wave.open(sys.argv[1], "wb"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
o.writeframes(st.tobytes()); o.close()
print("ok", sys.argv[1])

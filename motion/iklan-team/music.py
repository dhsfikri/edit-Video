#!/usr/bin/env python3
"""Muzik + SFX asal untuk iklan Setup Team Sales (15s, 120 BPM). Dijana sepenuhnya dengan numpy,
jadi bebas hak cipta. Pertukaran babak (5.5, 7.5, 9.5, 11.5s) jatuh tepat pada garis bar.

Guna: python3 music.py <out.wav>   (kemudian render.mjs campur dengan video & normalkan -14 LUFS)
"""
import sys
import wave
import numpy as np

SR = 48000
DUR = 15.0
BPM = 120
BEAT = 60 / BPM
T0 = -0.5  # bar bermula pada -0.5s → bar di 1.5, 3.5, 5.5, 7.5, 9.5, 11.5, 13.5
DROP = 5.5
N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N)
Rr = np.zeros(N)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N:
        return
    j = 0
    if i < 0:
        j, i = -i, 0
    seg = sig[j:j + N - i] * gain
    L[i:i + len(seg)] += seg * (1 - max(0, pan))
    Rr[i:i + len(seg)] += seg * (1 + min(0, pan))


def env(n, a=0.005, d=0.2, s=0.0, sus=0.0, r=0.05):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), 1.0)
    dec = s + (1 - s) * np.exp(-(t - a) / max(d, 1e-6))
    e = np.where(t >= a, dec, e)
    if r > 0:
        rel = np.clip((n / SR - t) / r, 0, 1)
        e *= rel
    return e


def saw(f, n, harm=12, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, harm + 1):
        if f * k > SR / 2.2:
            break
        out += np.sin(2 * np.pi * f * (1 + detune) * k * t) / k
    return out * 0.55


# ---------- instrumen ----------
def kick(gain=1.0):
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5)
    s += 0.25 * rng.standard_normal(n) * np.exp(-t * 180)  # klik
    return s * gain


def clap():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    nz = np.diff(nz, prepend=0)  # cerahkan
    e = np.exp(-t * 18)
    for off in (0.0, 0.011, 0.022):
        e += 0.6 * np.exp(-np.clip(t - off, 0, None) * 120) * (t >= off)
    return nz * e * 0.22 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.15


def hat(open_=False):
    n = int((0.22 if open_ else 0.05) * SR)
    t = np.arange(n) / SR
    nz = np.diff(np.diff(rng.standard_normal(n), prepend=0), prepend=0)
    return nz * np.exp(-t * (14 if open_ else 70)) * 0.06


def pluck(m, gain=0.2, bright=8, dur=0.32):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = mtof(m)
    s = saw(f, n, bright) + 0.5 * saw(f, n, bright, 0.004)
    return s * np.exp(-t * 9) * env(n, 0.002, 1, 1, 1, 0.03) * gain


def bass(m, dur, gain=0.32):
    n = int(dur * SR)
    s = saw(mtof(m), n, 6) + 0.6 * np.sin(2 * np.pi * mtof(m - 12) * np.arange(n) / SR)
    return s * env(n, 0.004, 0.18, 0.55, 0, 0.03) * gain


def pad(notes, dur, gain=0.07):
    n = int(dur * SR)
    s = np.zeros(n)
    for m in notes:
        for dt in (-0.003, 0.003):
            s += saw(mtof(m), n, 5, dt)
    t = np.arange(n) / SR
    e = np.clip(t / 0.5, 0, 1) * np.clip((dur - t) / 0.4, 0, 1)
    return s * e * gain


def riser(dur=1.2, gain=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = t / dur
    nz = rng.standard_normal(n)
    # "buka filter" kasar: campur noise licin → noise cerah
    smooth = np.convolve(nz, np.ones(40) / 40, mode="same")
    s = (smooth * (1 - x) + np.diff(nz, prepend=0) * 0.5 * x) * x ** 2
    s += 0.3 * np.sin(2 * np.pi * np.cumsum(200 + 900 * x ** 2) / SR) * x ** 3
    return s * gain


def whoosh(dur=0.45, gain=0.16):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = t / dur
    nz = rng.standard_normal(n)
    sm = np.convolve(nz, np.ones(24) / 24, mode="same")
    e = np.sin(np.pi * np.clip(x, 0, 1)) ** 2
    return sm * e * gain * 3


def impact(gain=0.5):
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 6)) / SR) * np.exp(-t * 3.2)
    nz = np.convolve(rng.standard_normal(n), np.ones(12) / 12, mode="same") * np.exp(-t * 5) * 0.5
    return (boom + nz) * gain


def pop(m=84, gain=0.12):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = mtof(m) * (1 + 0.5 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40) * gain


def load_wav(path):
    with wave.open(path) as w:
        d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        ch = w.getnchannels()
        d = d.reshape(-1, ch).mean(axis=1)
        if w.getframerate() != SR:
            x = np.linspace(0, len(d) - 1, int(len(d) * SR / w.getframerate()))
            d = np.interp(x, np.arange(len(d)), d)
    return d


# ---------- susunan ----------
CHORDS = [  # (mula, akar bass, nota kord)
    (-0.5, 45, [57, 60, 64]),  # Am
    (1.5, 41, [53, 57, 60]),   # F
    (3.5, 43, [55, 59, 62]),   # G (bina ketegangan)
    (5.5, 48, [60, 64, 67]),   # C  ← DROP (solusi)
    (7.5, 43, [55, 59, 62]),   # G
    (9.5, 45, [57, 60, 64]),   # Am
    (11.5, 41, [53, 57, 60]),  # F  ← CTA
    (13.5, 48, [60, 64, 67]),  # C  (penutup)
]

for idx, (start, root, notes) in enumerate(CHORDS):
    end = CHORDS[idx + 1][0] if idx + 1 < len(CHORDS) else DUR
    drop = start >= DROP
    # pad
    add(pad(notes, end - max(start, 0) + 0.3, 0.05 if not drop else 0.07), max(start, 0))
    # arpeggio pluck 16th
    arp = notes + [notes[0] + 12, notes[1] + 12] if drop else notes + [notes[0] + 12]
    step = BEAT / 4 if drop else BEAT / 2
    k = 0
    t = start
    while t < end - 1e-6:
        if t >= 0:
            m = arp[k % len(arp)]
            add(pluck(m, 0.16 if drop else 0.12, 10 if drop else 5), t, pan=(0.35 if k % 2 else -0.35))
        k += 1
        t += step
    # bass 8th (selepas drop), not panjang sebelum drop
    if drop:
        t = start
        while t < end - 1e-6:
            add(bass(root, BEAT / 2 * 0.9), t)
            t += BEAT / 2
    elif start >= 1.5:
        add(bass(root, end - start, 0.2), start)

# dram
b = 0
t = T0
while t < DUR:
    beat_in_bar = b % 4
    if t >= DROP:
        add(kick(0.55), t)
        if beat_in_bar in (1, 3):
            add(clap(), t)
        add(hat(True), t + BEAT / 2, pan=0.3)
        add(hat(), t + BEAT / 4, pan=-0.3)
        add(hat(), t + 3 * BEAT / 4, pan=-0.3)
    elif t >= 1.5 and t < 5.0:
        if beat_in_bar in (0, 2):
            add(kick(0.45), t)
        if t >= 3.5:
            add(hat(), t + BEAT / 2, pan=0.3)
    b += 1
    t += BEAT

# ---------- SFX selari dengan animasi ----------
ding = load_wav("../iklan/assets/ding.wav")
add(whoosh(0.7, 0.12), 0.0)                              # telefon masuk
for tm in (1.0, 1.55, 2.1):                               # mesej staf
    add(ding * 0.22, tm)
add(whoosh(0.4, 0.1), 2.8)                                # tajuk keluar
for i, tm in enumerate((3.15, 3.6, 4.05, 4.5)):          # notifikasi leads
    add(ding * (0.3 + 0.04 * i), tm, pan=0.2 * (-1) ** i)
add(riser(1.2), 4.3)                                      # bina ke drop
add(impact(0.45), 5.5)                                    # DROP
for tm in (5.8, 7.6, 9.6):                                # tanda ✓
    add(pop(88, 0.14), tm)
for i, tm in enumerate((6.05, 6.2, 6.35, 6.5)):          # tag peranan
    add(pop(79 + i * 2, 0.08), tm)
add(whoosh(0.45, 0.12), 7.9)                              # dokumen SOP
add(whoosh(0.5, 0.12), 9.7)                               # kad laporan
add(whoosh(0.8, 0.14), 11.3)                              # ke CTA
add(impact(0.35), 11.75)                                  # kad CTA
for i in range(5):                                        # titik slot
    add(pop(91, 0.06), 12.45 + i * 0.12)

# ---------- master ----------
# reverb ringkas (konvolusi FFT dengan IR noise menyusut)
ir_n = int(1.8 * SR)
ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 3.2)
ir[0] = 0
ir /= np.sqrt((ir ** 2).sum())


def conv(x):
    n = len(x) + ir_n
    f = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, f) * np.fft.rfft(ir, f), f)[: len(x)]


L = L + 0.18 * conv(L)
Rr = Rr + 0.18 * conv(Rr)
# fade keluar (loop)
fade = np.ones(N)
fs = int(14.4 * SR)
fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
L *= fade
Rr *= fade
peak = max(np.abs(L).max(), np.abs(Rr).max())
L, Rr = L / peak * 0.8, Rr / peak * 0.8
st = (np.stack([L, Rr], axis=1) * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else "music.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(st.tobytes())
print("ok")

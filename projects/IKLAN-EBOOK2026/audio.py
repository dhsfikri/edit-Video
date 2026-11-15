"""Muzik + SFX sintetik (bebas royalti) untuk iklan Ebook 2026, 30s. Output: WAV stereo 48k.
Guna: python3 -I projects/IKLAN-EBOOK2026/audio.py <out.wav> <ding.wav> <signature.wav>"""
import sys, wave, numpy as np
SR = 48000; DUR = 30.0; N = int(SR * DUR)
out, ding_p, sig_p = sys.argv[1:4]
rng = np.random.default_rng(3)
t_all = np.arange(N) / SR
mix = np.zeros((N, 2))

def load(p):
    w = wave.open(p); ch = w.getnchannels(); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    a = a.reshape(-1, ch).mean(1)
    if sr != SR: a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
    return a
def add(sig, at, vol=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    mix[i:i + len(sig), 0] += sig * vol * (1 - pan) ; mix[i:i + len(sig), 1] += sig * vol * (1 + pan)
def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)); return e * np.exp(-t / r)
def tone(f, d, a=0.005, r=0.3, shape="sine"):
    n = int(d * SR); t = np.arange(n) / SR; ph = 2 * np.pi * f * t
    s = np.sin(ph) if shape == "sine" else (2 * (t * f % 1) - 1) if shape == "saw" else np.sign(np.sin(ph))
    return s * env(n, a, r)
def lp(x, k):  # one-pole low-pass, k 0..1
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y
def noise(d): return rng.uniform(-1, 1, int(d * SR))
midi = lambda m: 440 * 2 ** ((m - 69) / 12)

# ── Muzik: 110 bpm, Am–F–C–G
BPM = 110; B = 60 / BPM
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]
bass = [45, 41, 48, 43]
nb = int(DUR / B)
for b in range(nb):
    t0 = b * B; ci = (b // 4) % 4
    full = t0 >= 8.3 and t0 < 29.0
    if b % 4 == 0:  # pad
        for m in chords[ci]:
            pad = tone(midi(m), 4 * B, a=0.4, r=3.0, shape="saw") + tone(midi(m) * 1.003, 4 * B, a=0.4, r=3.0, shape="saw")
            add(lp(pad, 0.04) * (0.05 if full else 0.035), t0, pan=-0.2)
            add(lp(pad, 0.04) * (0.05 if full else 0.035), t0, pan=0.2)
    if full or t0 >= 3.0:  # bass
        add(lp(tone(midi(bass[ci]), B * 0.9, a=0.01, r=0.35, shape="saw"), 0.08), t0, 0.22 if full else 0.12)
    if full:  # kick + clap + hat + pluck arp
        n = int(0.35 * SR); tt = np.arange(n) / SR
        kick = np.sin(2 * np.pi * (50 * tt + 90 * (1 - np.exp(-tt * 30)) / 30)) * np.exp(-tt * 9)
        add(kick, t0, 0.55)
        if b % 2 == 1: add(lp(noise(0.18), 0.5) * env(int(0.18 * SR), 0.001, 0.05), t0, 0.16)
        for h in (0.5,): add((noise(0.05) - lp(noise(0.05), 0.3)) * env(int(0.05 * SR), 0.001, 0.012), t0 + h * B, 0.13, pan=0.3)
        arp = chords[ci] + [chords[ci][0] + 12]
        for k in range(2): add(tone(midi(arp[(b * 2 + k) % 4] + 12), 0.25, 0.003, 0.12, "square") * 0.5, t0 + k * B / 2, 0.035, pan=(-0.4 if k else 0.4))
    elif t0 < 8.3:  # tik-tok jam (tension)
        add(tone(2200, 0.03, 0.001, 0.01), t0, 0.05)
# akord akhir
for m in chords[0] + [69]: add(lp(tone(midi(m), 2.0, 0.01, 1.2, "saw"), 0.06), 29.0, 0.05)

# ── SFX
ding = load(ding_p); sig = load(sig_p)
def pop(): n = int(0.08 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * (900 - 4000 * tt) * tt) * env(n, 0.001, 0.025)
def whoosh(d=0.45, up=False):
    x = noise(d); k = np.linspace(0.02, 0.4, len(x)) if up else np.linspace(0.4, 0.02, len(x))
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k[i] * (v - acc); y[i] = acc
    e = np.sin(np.linspace(0, np.pi, len(x))) ** 2; return y * e * 2.2
def thud(f=70, d=0.4): n = int(d * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt * (1 + np.exp(-tt * 20))) * np.exp(-tt * 7)
def click(): return (noise(0.012) * env(int(0.012 * SR), 0.0005, 0.003))
def sparkle():
    s = np.zeros(int(0.6 * SR))
    for k, m in enumerate([84, 88, 91, 96]): seg = tone(midi(m), 0.35, 0.002, 0.15); i = int(k * 0.06 * SR); s[i:i + len(seg)] += seg
    return s
def riser(d=1.2):
    n = int(d * SR); tt = np.arange(n) / SR; f = 200 + 1400 * (tt / d) ** 2
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + whoosh(d, True)[:n] * 0.6) * (tt / d) ** 1.5

add(pop(), 0.25, 0.5); add(click(), 0.95, 0.5)
for t in (3.4, 4.4, 5.4): add(ding, t, 0.32)
add(thud(55, 0.3), 5.45, 0.35); add(thud(), 6.0, 0.45); add(click(), 6.5, 0.6)
add(whoosh(), 7.55, 0.35)
add(riser(1.0), 8.2, 0.35); add(thud(48, 0.7), 9.2, 0.6); add(sparkle(), 9.2, 0.18)
add(pop(), 10.2, 0.4); add(pop(), 10.38, 0.4)
add(whoosh(), 13.4, 0.35)
for l in (14.2, 15.9, 17.6):
    for k in range(3): add(click(), l + k * 0.32, 0.55)
    add(pop(), l + 0.2, 0.35)
add(whoosh(), 19.55, 0.35)
add(pop(), 20.5, 0.45); add(ding, 21.75, 0.38)
add(thud(60, 0.5), 22.6, 0.7); add(sparkle(), 22.62, 0.25); add(whoosh(0.3), 23.6, 0.3)
add(pop(), 24.1, 0.45); add(thud(65, 0.4), 25.2, 0.55); add(whoosh(0.25), 26.5, 0.3)
add(sparkle(), 26.75, 0.25); add(thud(50, 0.5), 26.95, 0.45)
add(click(), 28.95, 0.9); add(sig, 29.1, 0.4)

mix *= 0.9 / max(1e-9, np.abs(mix).max())
w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print("ok", out)

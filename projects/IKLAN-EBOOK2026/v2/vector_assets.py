"""Bina aset vektor iklan Ebook 2026 v2 guna VectorCraft (headless CLI).
Guna: python3 -I projects/IKLAN-EBOOK2026/v2/vector_assets.py <out_dir> <cover.png>
Setiap aset = satu dokumen VectorCraft -> export .svg + .png (2x). Warna ikut BRANDKIT.
"""
import json, os, subprocess, sys

VC = "/opt/vectorcraft/vectorcraft-0.11.0-linux-x86_64/bin/vectorcraft-cli"
OUT, COVER = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)
GREEN, INK, WHITE, DEEP, YEL, BLUE = "#25d366", "#0b0b0b", "#ffffff", "#0b3d2e", "#ffd60a", "#34b7f1"


class Doc:
    def __init__(self, name, w, h):
        self.name, self.cmds = name, [("file.new", {"width": w, "height": h, "units": "Pixels", "name": name})]

    def c(self, cid, **p):
        self.cmds.append((cid, p)); return self

    def fill(self, color=None, stroke=None, weight=None, cap="round", join="round"):
        self.c("paint.setFill", **({"color": color} if color else {"none": True}))
        self.c("paint.setStroke", **({"color": stroke} if stroke else {"none": True}))
        if stroke and weight: self.c("stroke.set", weight=weight, cap=cap, join=join)
        return self

    def rect(self, x, y, w, h, r=0, **paint):
        self.c("shape.rectangle", x=x, y=y, width=w, height=h, radius=r); return self.fill(**paint)

    def ellipse(self, x, y, w, h, **paint):
        self.c("shape.ellipse", x=x, y=y, width=w, height=h); return self.fill(**paint)

    def path(self, d, **paint):
        self.c("path.create", d=d); return self.fill(**paint)

    def text(self, x, y, s, size, color=INK, style="ExtraBold", justify="left"):
        return self.c("text.create", x=x, y=y, text=s, size=size, font="Montserrat", style=style, color=color, justify=justify)

    def place(self, path, x, y, w, h):
        return self.c("file.place", path=path, rect=[x, y, w, h])

    def run(self, scale=2):
        args = [VC, "run"]
        for cid, p in self.cmds: args += ["--cmd", cid, "--params", json.dumps(p)]
        for ext, extra in (("svg", {}), ("png", {"scale": scale, "background": "transparent"})):
            args += ["--cmd", "document.export", "--params", json.dumps({"path": f"{OUT}/{self.name}.{ext}", **extra})]
        r = subprocess.run(args, capture_output=True, text=True, timeout=300)
        bad = [l for l in r.stdout.splitlines() if '"error"' in l]
        print(self.name, "OK" if r.returncode == 0 and not bad else f"ERR {r.returncode} {bad[:2]} {r.stderr[-300:]}")


# ── Ikon kecil
d = Doc("shield", 460, 520)
d.path("M230 16 L428 92 V256 C428 384 340 468 230 504 C120 468 32 384 32 256 V92 Z", color=GREEN, stroke=INK, weight=14)
d.path("M132 264 L204 336 L336 192", stroke=INK, weight=40); d.run()

d = Doc("sparkle", 200, 200)
d.path("M100 0 C110 72 128 90 200 100 C128 110 110 128 100 200 C90 128 72 110 0 100 C72 90 90 72 100 0 Z", color=GREEN); d.run()

d = Doc("cursor", 120, 150)
d.path("M14 8 L14 112 L40 88 L60 134 L82 124 L62 80 L100 80 Z", color=WHITE, stroke=INK, weight=8); d.run()

d = Doc("check_circle", 320, 320)
d.ellipse(10, 10, 300, 300, color="#e9fbf0", stroke=GREEN, weight=10)
d.path("M98 166 L142 210 L226 122", stroke=GREEN, weight=22); d.run()

# Chip ikon (kad putih, gaya "folder icon" reference)
d = Doc("chip_chat", 240, 240)
d.rect(10, 10, 220, 220, 48, color=WHITE, stroke="#dfe7e2", weight=3)
d.path("M60 70 H180 C192 70 200 78 200 90 V146 C200 158 192 166 180 166 H104 L72 192 V166 H60 C48 166 40 158 40 146 V90 C40 78 48 70 60 70 Z", color=GREEN)
for x in (82, 120, 158): d.ellipse(x - 10, 108, 20, 20, color=WHITE)
d.run()

d = Doc("chip_book", 240, 240)
d.rect(10, 10, 220, 220, 48, color=WHITE, stroke="#dfe7e2", weight=3)
d.rect(62, 46, 116, 148, 10, color="#e2312b")
d.rect(62, 46, 18, 148, 4, color="#9f1814")
d.rect(92, 84, 70, 14, 4, color=YEL); d.rect(92, 108, 54, 14, 4, color=WHITE)
d.run()

d = Doc("chip_team", 240, 240)
d.rect(10, 10, 220, 220, 48, color=WHITE, stroke="#dfe7e2", weight=3)
for cx, col in ((78, DEEP), (162, DEEP), (120, GREEN)):
    d.ellipse(cx - 24, 62 if cx == 120 else 78, 48, 48, color=col)
    d.path(f"M{cx-40} {178 if cx==120 else 190} C{cx-40} {130 if cx==120 else 142} {cx+40} {130 if cx==120 else 142} {cx+40} {178 if cx==120 else 190} Z", color=col)
d.run()


# ── Skrin telefon (600x1240): bingkai + skrin
def phone(name, title, sub):
    d = Doc(name, 600, 1240)
    d.rect(0, 0, 600, 1240, 86, color="#1a1f1c")
    d.rect(18, 18, 564, 1204, 70, color="#f3f5f4")
    d.rect(18, 18, 564, 170, 0, color=DEEP); d.rect(18, 18, 564, 120, 70, color=DEEP)
    d.rect(230, 34, 140, 30, 15, color="#1a1f1c")
    d.ellipse(50, 92, 70, 70, color="#cfe9dc")
    d.text(140, 118, title, 32, WHITE); d.text(140, 156, sub, 22, "#cfe9dc", "SemiBold")
    d.rect(40, 1130, 520, 64, 32, color=WHITE); d.text(70, 1171, "Tulis mesej…", 22, "#9aa5a0", "SemiBold")
    return d

def bubble(d, y, lines, me=False, ticks=False, h=None):
    w = max(len(s) for s in lines) * 17 + 60
    h = h or 40 + 38 * len(lines)
    x = 560 - w if me else 40
    d.rect(x, y, w, h, 28, color="#d7f8e3" if me else WHITE)
    for i, s in enumerate(lines): d.text(x + 26, y + 50 + i * 38, s, 27, "#0b2e1f" if me else "#1d2421", "SemiBold")
    if ticks: d.text(x + w - 70, y + h - 12, "✓✓", 20, BLUE, "ExtraBold")
    return y + h + 22

d = phone("phone_chat", "Customer", "online")
y = 560
y = bubble(d, y, ["Salam boss 😊 Ini info", "produk yang boss tanya."], me=True, ticks=True)
y = bubble(d, y, ["Mahal la…"]); y = bubble(d, y, ["Nanti saya fikir dulu"]); y = bubble(d, y, ["Tunggu gaji dulu ye"])
d.run(scale=1.5)

d = phone("phone_closed", "Customer", "online")
y = 640
y = bubble(d, y, ["Mahal la…"])
y = bubble(d, y, ["Faham boss. Kalau saya bagi", "cara bayar lebih ringan,", "boss okay?"], me=True, ticks=True)
y = bubble(d, y, ["Ok, saya nak 1 😊"])
d.run(scale=1.5)

d = phone("phone_ebook", "Ebook 2026", "105 muka surat")
d.place(COVER, 120, 260, 360, 563)
d.rect(120, 880, 360, 16, 8, color="#dfe7e2"); d.rect(120, 880, 250, 16, 8, color=GREEN)
d.text(300, 960, "Bab 3: Formula 1-4-6-10", 26, INK, "ExtraBold", "center")
d.run(scale=1.5)

d = phone("phone_skrip", "Skrip Closing", "Template 2026")
for i, (t, s) in enumerate([("1. Salam & kenal", "Buka chat tanpa hard-sell"), ("2. Gali keperluan", "Soalan yang buat dia cerita"),
                            ("3. Handle bantahan", "\"Mahal\", \"fikir dulu\", \"gaji\""), ("4. Ajak closing", "Ayat tutup tanpa paksa")]):
    yy = 250 + i * 210
    d.rect(44, yy, 512, 180, 26, color=WHITE)
    d.ellipse(70, yy + 52, 76, 76, color=GREEN if i < 3 else YEL)
    d.text(108, yy + 104, "✓", 34, INK, "ExtraBold", "center")
    d.text(170, yy + 80, t, 28, INK); d.text(170, yy + 124, s, 22, "#4b5550", "SemiBold")
d.run(scale=1.5)

# ── Kad produk (UI kedai generik)
d = Doc("product_card", 860, 360)
d.rect(0, 0, 860, 360, 36, color=WHITE, stroke="#dfe7e2", weight=3)
d.place(COVER, 36, 36, 184, 288)
d.text(250, 92, "Ebook 2026:", 34, INK); d.text(250, 136, "Wassap Masih Relevan?", 34, INK)
d.text(250, 186, "105 m/s · Formula 1-4-6-10", 24, "#4b5550", "SemiBold")
d.text(250, 250, "RM67", 30, "#9aa5a0", "SemiBold"); d.rect(246, 238, 86, 5, 2, color="#ff4d4f")
d.text(350, 254, "RM37", 46, GREEN)
d.rect(530, 222, 290, 92, 46, color=GREEN); d.text(675, 280, "Dapatkan", 34, INK, "ExtraBold", "center")
d.run()
print("siap ->", OUT)

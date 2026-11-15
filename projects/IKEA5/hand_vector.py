"""Ilustrasi tangan gaya IKEA Together — dilukis dalam VectorCraft (headless), export SVG berlapis (id ikut nama objek).
Tapak tangan menghadap atas, jari ke kiri, ibu jari ke atas (menjepit manik antara ibu jari & telunjuk).
Bahagian boleh dianimasi berasingan: #thumb + #thumbNail, #index + #indexJ1/#indexJ2.
Guna: python3 -I projects/IKEA5/hand_vector.py <out_dir>
"""
import json, os, subprocess, sys

VC = "/opt/vectorcraft/vectorcraft-0.11.0-linux-x86_64/bin/vectorcraft-cli"
OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
LIGHT, BASE, SHADE, DEEP, LINE, NAIL = "#e6fcdc", "#d3f5c8", "#b4e2a8", "#9fd293", "#9ccc90", "#bfe6b3"

cmds = [("file.new", {"width": 1400, "height": 520, "units": "Pixels", "name": "hand"})]
def c(cid, **p): cmds.append((cid, p))
def grad(stops, angle=-90):
    return {"kind": "linear", "angle": angle, "stops": [{"offset": o, "color": col} for o, col in stops]}
def shape(name, d=None, rect=None, fill=None, stroke=None, weight=None):
    if d: c("path.create", d=d)
    else: x, y, w, h, r = rect; c("shape.rectangle", x=x, y=y, width=w, height=h, radius=r)
    c("paint.setFill", **({"gradient": fill} if isinstance(fill, dict) else {"color": fill} if fill else {"none": True}))
    c("paint.setStroke", **({"color": stroke} if stroke else {"none": True}))
    if stroke and weight: c("stroke.set", weight=weight, cap="round", join="round")
    c("object.setProps", name=name)

def dgrad(stops, y0=128, y1=408):   # gradient dalam koordinat dokumen: bahagian bertindih bersambung tanpa garis
    return {"kind": "linear", "start": [700, y0], "end": [700, y1], "stops": [{"offset": o, "color": col} for o, col in stops]}
SKIN = dgrad([(0, LIGHT), (0.45, BASE), (0.82, SHADE), (1, DEEP)])
FING = grad([(0, LIGHT), (0.6, BASE), (1, SHADE)])

def finger(name, x, y, x2, h):   # hujung kiri bulat, pangkal kanan rata (masuk ke tapak tangan)
    r = h / 2; k = r * 1.333
    shape(name, d=f"M{x+r},{y} L{x2},{y} L{x2},{y+h} L{x+r},{y+h} C{x+r-k},{y+h} {x+r-k},{y} {x+r},{y} Z", fill=FING)

# tapak tangan + lengan (gradient sama → licin)
shape("palm", d="M300,150 C420,140 530,150 640,160 L640,346 C540,392 420,408 300,400 C292,330 290,214 300,150 Z", fill=SKIN)
shape("arm", d="M560,160 C760,148 980,136 1400,128 L1400,392 C1000,378 780,356 560,346 Z", fill=SKIN)
# jari di atas tapak tangan
finger("pinky", 150, 352, 318, 54)
finger("ring", 64, 290, 322, 62)
finger("middle", 34, 222, 324, 66)
finger("index", 72, 158, 322, 60)
# bayang pendek di celah jari, atas tapak tangan
for k, yy in enumerate((220, 289, 352)):
    shape(f"gap{k+1}", d=f"M318,{yy} C340,{yy+1} 356,{yy+3} 368,{yy+6}", stroke=SHADE, weight=4)
# garis sendi jari
for nm, xs, y0, y1 in (("indexJ", (150, 214), 166, 210), ("middleJ", (122, 198), 230, 280), ("ringJ", (148, 214), 298, 344), ("pinkyJ", (212, 258), 360, 398)):
    for k, x in enumerate(xs):
        shape(f"{nm}{k+1}", d=f"M{x},{y0+6} C{x-5},{(y0+y1)/2} {x-5},{(y0+y1)/2} {x},{y1-6}", stroke=LINE, weight=3)
# ibu jari (naik ke atas) + kuku
shape("thumb", d="M430,190 C420,132 410,100 420,82 C434,60 474,64 490,86 C506,110 524,150 566,182 C520,204 470,204 430,190 Z", fill=dgrad([(0, LIGHT), (0.5, BASE), (1, SHADE)], 60, 230))
shape("thumbNail", d="M428,90 C432,78 452,76 460,86 L466,118 C458,126 440,126 434,118 Z", fill=NAIL)
# garis tapak tangan (thenar)
shape("palmCrease", d="M388,206 C392,250 426,268 474,266", stroke=LINE, weight=3.5)

args = [VC, "run"]
for cid, p in cmds: args += ["--cmd", cid, "--params", json.dumps(p)]
args += ["--cmd", "document.export", "--params", json.dumps({"path": f"{OUT}/hand.svg"}),
         "--cmd", "document.export", "--params", json.dumps({"path": f"{OUT}/hand.png", "background": "transparent", "scale": 1})]
r = subprocess.run(args, capture_output=True, text=True, timeout=300)
bad = [l for l in r.stdout.splitlines() if '"error"' in l]
print("OK" if r.returncode == 0 and not bad else f"ERR {r.returncode} {bad[:3]} {r.stderr[-400:]}", "->", OUT)

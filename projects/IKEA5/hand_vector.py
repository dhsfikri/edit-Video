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

def dgrad(stops, y0=120, y1=440):   # gradient dalam koordinat dokumen: bahagian bertindih bersambung tanpa garis
    return {"kind": "linear", "start": [700, y0], "end": [700, y1], "stops": [{"offset": o, "color": col} for o, col in stops]}
SKIN = dgrad([(0, LIGHT), (0.45, BASE), (0.8, SHADE), (1, DEEP)])
FING = grad([(0, LIGHT), (0.5, BASE), (0.85, SHADE), (1, DEEP)])

def finger(name, x, y, x2, h):   # hujung kiri bulat, pangkal kanan rata (masuk ke tapak tangan); jari lebih gemuk
    r = h / 2; k = r * 1.333
    shape(name, d=f"M{x+r},{y} L{x2},{y} L{x2},{y+h} L{x+r},{y+h} C{x+r-k},{y+h} {x+r-k},{y} {x+r},{y} Z", fill=FING)

# tapak tangan + lengan (lebih berisi)
shape("palm", d="M300,146 C420,134 540,146 660,156 L660,370 C560,420 430,440 300,430 C290,350 288,214 300,146 Z", fill=SKIN)
shape("arm", d="M580,156 C780,142 1000,128 1400,118 L1400,414 C1000,402 800,384 580,370 Z", fill=SKIN)
# jari di atas tapak tangan (tebal, rapat)
finger("pinky", 140, 368, 318, 64)
finger("ring", 52, 296, 324, 76)
finger("middle", 20, 222, 326, 80)
finger("index", 62, 150, 326, 76)
# bayang pendek di celah jari, atas tapak tangan
for k, yy in enumerate((224, 297, 368)):
    shape(f"gap{k+1}", d=f"M320,{yy} C344,{yy+1} 362,{yy+4} 376,{yy+8}", stroke=SHADE, weight=5)
# garis sendi jari
for nm, xs, y0, y1 in (("indexJ", (146, 214), 150, 226), ("middleJ", (110, 192), 222, 302), ("ringJ", (138, 210), 296, 372), ("pinkyJ", (206, 256), 368, 432)):
    for k, x in enumerate(xs):
        shape(f"{nm}{k+1}", d=f"M{x},{y0+12} C{x-6},{(y0+y1)/2} {x-6},{(y0+y1)/2} {x},{y1-12}", stroke=LINE, weight=3.5)
# ibu jari (lebih besar, naik ke atas) + kuku
shape("thumb", d="M424,190 C410,128 398,90 410,66 C428,40 480,44 500,72 C520,104 538,148 580,182 C530,208 470,208 424,190 Z", fill=dgrad([(0, LIGHT), (0.5, BASE), (1, SHADE)], 44, 230))
shape("thumbNail", d="M420,76 C426,60 452,58 464,70 L470,108 C460,118 438,118 430,108 Z", fill=NAIL)
# garis tapak tangan (thenar)
shape("palmCrease", d="M392,214 C396,262 430,282 482,280", stroke=LINE, weight=4)

args = [VC, "run"]
for cid, p in cmds: args += ["--cmd", cid, "--params", json.dumps(p)]
args += ["--cmd", "document.export", "--params", json.dumps({"path": f"{OUT}/hand.svg"}),
         "--cmd", "document.export", "--params", json.dumps({"path": f"{OUT}/hand.png", "background": "transparent", "scale": 1})]
r = subprocess.run(args, capture_output=True, text=True, timeout=300)
bad = [l for l in r.stdout.splitlines() if '"error"' in l]
print("OK" if r.returncode == 0 and not bad else f"ERR {r.returncode} {bad[:3]} {r.stderr[-400:]}", "->", OUT)

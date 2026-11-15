// IKLAN EBOOK 2026 v3 — 3D penuh (EffectCraft). Setiap babak = comp sendiri dengan kamera 3D + motion blur,
// disusun dalam comp IKLAN. Teknik animasi ikut reference; isi & aset milik Sir (VectorCraft + halaman PDF ebook).
// Jalankan dari folder yang ada assets/:
//   effectcraft-cli script iklan_v3.jsx --empty
//   effectcraft-cli render --project iklan_v3.ecproj --comp IKLAN --out video.mp4 --format h264 --fps 30 --audio off
// Safe zone TikTok: teks x 60–900 (pusat 480), y 220–1440.

var W = 1080, H = 1920, DUR = 30, FPS = 30, CX = 480, CY = 960;
var INK = [0.043, 0.043, 0.043], GREEN = [0.145, 0.827, 0.4], WHITE = [1, 1, 1], GREY = [0.55, 0.6, 0.58],
    YEL = [1, 0.84, 0.04], RED = [1, 0.3, 0.31], DEEP = [0.043, 0.239, 0.18], BG = [0.957, 0.98, 0.965];

var MAIN = app.project.items.addComp("IKLAN", W, H, 1, DUR, FPS);
MAIN.bgColor = BG; try { MAIN.motionBlur = true; MAIN.shutterAngle = 180; } catch (e) {}
var C = MAIN, L = MAIN.layers, footCache = {};

function tr(layer, name) { return layer.property("Transform").property(name); }
function ease(prop, inf) {
  for (var i = 1; i <= prop.numKeys; i++) {
    var dims = 1;
    try { var v = prop.keyValue(i); if (v && v.length && !prop.isSpatial) dims = v.length; } catch (e) {}
    var arr = []; for (var d = 0; d < dims; d++) arr.push(new KeyframeEase(0, inf || 75));
    try { prop.setTemporalEaseAtKey(i, arr, arr); } catch (e) { try { prop.setTemporalEaseAtKey(i, [arr[0]], [arr[0]]); } catch (e2) {} }
  }
}
function KP(p, keys, linear, inf) { for (var i = 0; i < keys.length; i++) p.setValueAtTime(keys[i][0], keys[i][1]); if (!linear) ease(p, inf); return p; }
function K(layer, name, keys, linear, inf) { return KP(tr(layer, name), keys, linear, inf); }
function span(layer, t0, t1) { layer.inPoint = t0; layer.outPoint = t1; }
function mb(l) { try { l.motionBlur = true; } catch (e) {} return l; }
function shadow(layer, dist, soft, op) {
  try { var ds = layer.property("Effects").addProperty("ADBE Drop Shadow");
    ds.property("Distance").setValue(dist); ds.property("Softness").setValue(soft); ds.property("Opacity").setValue(op || 40);
    try { ds.property("Direction").setValue(180); } catch (e) {} } catch (e) {}
}
function blurKeys(layer, keys) {
  try { var b = layer.property("Effects").addProperty("ADBE Gaussian Blur 2").property("Blurriness"); KP(b, keys); } catch (e) {}
}
function T(s, o) {
  var t = L.addText(s), src = t.property("Source Text"), td = src.value;
  td.fontSize = o.size || 96; td.fillColor = o.color || INK; td.font = "Montserrat-" + (o.w || "ExtraBold");
  td.justification = ParagraphJustification.CENTER_JUSTIFY; if (o.lead) td.leading = o.lead; src.setValue(td);
  tr(t, "Position").setValue([o.x == null ? CX : o.x, o.y]); span(t, o.t0, o.t1);
  var nw = s.split(/\s+/).length, st = o.stagger == null ? 0.16 : o.stagger;
  if (o.reveal !== false) {
    try {
      var an = t.property("Text").property("Animators").addProperty("ADBE Text Animator"), pr = an.property("Properties");
      pr.addProperty("ADBE Text Opacity").setValue(0);
      pr.addProperty("ADBE Text Position 3D").setValue([0, o.rise || 70, 0]);
      try { pr.addProperty("ADBE Text Blur").setValue([18, 18]); } catch (e) {}
      var sel = an.property("Selectors").addProperty("ADBE Text Selector");
      try { sel.property("Advanced").property("Based On").setValue(3); sel.property("Advanced").property("Ease Low").setValue(60); sel.property("Advanced").property("Ease High").setValue(60); } catch (e) {}
      var sp = sel.property("Start"); sp.setValueAtTime(o.t0, 0); sp.setValueAtTime(o.t0 + Math.max(0.35, nw * st + 0.2), 100);
    } catch (e) {}
  }
  if (o.hl) for (var h = 0; h < o.hl.length; h++) {
    try {
      var a2 = t.property("Text").property("Animators").addProperty("ADBE Text Animator");
      a2.property("Properties").addProperty("ADBE Text Fill Color").setValue(o.hl[h][1]);
      var s2 = a2.property("Selectors").addProperty("ADBE Text Selector");
      s2.property("Advanced").property("Based On").setValue(3); s2.property("Advanced").property("Units").setValue(2);
      s2.property("Start").setValue(o.hl[h][0]); s2.property("End").setValue(o.hl[h][0] + 1);
    } catch (e) {}
  }
  if (o.out !== false) {
    K(t, "Opacity", [[o.t1 - 0.28, 100], [o.t1 - 0.02, 0]]);
    if (o.out == "up") K(t, "Position", [[o.t1 - 0.3, [o.x == null ? CX : o.x, o.y]], [o.t1, [o.x == null ? CX : o.x, o.y - 60]]]);
  }
  if (o.zoom) K(t, "Scale", [[o.t0, [100, 100]], [o.t1, [o.zoom, o.zoom]]], true);
  return t;
}
function FOOT(f) { if (!footCache[f]) footCache[f] = app.project.importFile(new ImportOptions(new File(f))); return footCache[f]; }
function IMG(file, o) {
  var l = L.add(FOOT(file));
  if (o.d3) { l.threeDLayer = true; mb(l); }
  if (o.parent) l.parent = o.parent;   // parent DULU, baru kedudukan (koordinat tempatan)
  tr(l, "Position").setValue(o.d3 ? [o.x, o.y, o.z || 0] : [o.x, o.y]);
  var sc = o.s || 100; tr(l, "Scale").setValue(o.d3 ? [sc, sc, sc] : [sc, sc]);
  if (o.ori) tr(l, "Orientation").setValue(o.ori);
  span(l, o.t0, o.t1); return l;
}
function RECT(w, h, r, color, x, y, t0, t1, d3) {
  var s = L.addShape(), g = s.property("Contents").addProperty("ADBE Vector Group");
  var rr = g.property("Contents").addProperty("ADBE Vector Shape - Rect"); rr.property("Size").setValue([w, h]); rr.property("Roundness").setValue(r);
  g.property("Contents").addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(color);
  if (d3) { s.threeDLayer = true; mb(s); }
  tr(s, "Position").setValue(d3 ? [x, y, 0] : [x, y]); span(s, t0, t1); return s;
}
function ELL(w, h, color, x, y, t0, t1) {
  var s = L.addShape(), g = s.property("Contents").addProperty("ADBE Vector Group");
  g.property("Contents").addProperty("ADBE Vector Shape - Ellipse").property("Size").setValue([w, h]);
  g.property("Contents").addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(color);
  tr(s, "Position").setValue([x, y]); span(s, t0, t1); return s;
}
function NUL(x, y, z, t0, t1) { var n = L.addNull(); n.threeDLayer = true; tr(n, "Position").setValue([x, y, z]); span(n, t0, t1); return n; }
function CAM(posKeys, poiKeys, zoom, inf) {
  var cam = L.addCamera("CAM", [CX, CY]);
  try { cam.property("Camera Options").property("Zoom").setValue(zoom || 1500); } catch (e) {}
  KP(cam.property("Transform").property("Position"), posKeys, false, inf);
  KP(cam.property("Transform").property("Point of Interest"), poiKeys, false, inf);
  return cam;
}
// Babak = comp sendiri, diletak dalam IKLAN pada masa `start`
function SCENE(name, start, dur, build) {
  var c = app.project.items.addComp(name, W, H, 1, dur, FPS);
  try { c.motionBlur = true; c.shutterAngle = 200; c.bgColor = BG; } catch (e) {}
  var pC = C, pL = L; C = c; L = c.layers; build(); C = pC; L = pL;
  var l = MAIN.layers.add(c); l.startTime = start; l.inPoint = start; l.outPoint = start + dur; mb(l);
  return l;
}
var seed = 11; function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }

// ═════ LATAR (IKLAN): putih kehijauan + cahaya hijau lembut bergerak
var glow = ELL(1100, 1100, [0.78, 0.95, 0.85], 480, 900, 0, DUR);
blurKeys(glow, [[0, 220]]);
K(glow, "Position", [[0, [300, 700]], [10, [700, 1100]], [20, [350, 1250]], [30, [600, 800]]]);

// ═════ A 0–2.95  HOOK: perkataan bertukar, sedikit dolly 3D
SCENE("A_hook", 0, 2.95, function () {
  T("Customer", { y: 980, size: 120, w: "SemiBold", t0: 0.0, t1: 1.0, out: "up", zoom: 104 });
  T("SEEN ✓✓", { y: 990, size: 160, color: GREEN, t0: 1.0, t1: 1.85, stagger: 0.1, out: "up", zoom: 106 });
  T("tapi tak reply?", { y: 980, size: 104, w: "SemiBold", t0: 1.85, t1: 2.95, hl: [[2, RED]], out: "up", zoom: 104 });
});

// ═════ B 2.9–5.45  ayat + kad ikon 3D (kaca) → rebah ke belakang jadi satah perspektif
SCENE("B_chip", 2.9, 2.55, function () {
  T("Chat banyak", { y: 720, size: 100, w: "SemiBold", t0: 0.05, t1: 1.75, hl: [[1, GREEN]] });
  T("Closing sikit.", { y: 1260, size: 100, w: "SemiBold", t0: 0.6, t1: 1.75, hl: [[1, RED]] });
  var tray = RECT(980, 1300, 60, WHITE, CX, 1000, 1.5, 2.55, true);
  K(tray, "X Rotation", [[1.5, 0], [2.2, 72]]); K(tray, "Scale", [[1.5, [20, 20, 20]], [2.2, [100, 100, 100]]]);
  K(tray, "Opacity", [[1.5, 0], [1.75, 100], [2.25, 100], [2.55, 0]]); shadow(tray, 30, 80, 25);
  var chip = IMG("assets/chip_chat.png", { x: CX, y: 990, z: 0, s: 70, d3: true, t0: 0.25, t1: 2.55 });
  K(chip, "Scale", [[0.25, [0, 0, 0]], [0.6, [80, 80, 80]], [0.8, [72, 72, 72]], [1.5, [72, 72, 72]], [2.2, [60, 60, 60]]]);
  K(chip, "Y Rotation", [[0.25, -70], [0.8, -18], [1.5, 22]]);
  K(chip, "X Rotation", [[0.25, 25], [0.8, 8], [1.5, 6], [2.2, 72]]);
  K(chip, "Position", [[1.5, [CX, 990, 0]], [2.2, [CX, 1000, -10]]]);
  K(chip, "Opacity", [[2.2, 100], [2.5, 0]]); shadow(chip, 30, 60, 30);
  CAM([[0, [CX, CY, -1500]], [1.5, [CX, CY - 40, -1400]], [2.55, [CX, CY - 700, -900]]], [[0, [CX, CY, 0]], [1.5, [CX, CY, 0]], [2.55, [CX, CY + 80, 0]]], 1500);
});

// ═════ C 5.2–10.35  TEROWONG TELEFON: kamera dalam bulatan telefon, dolly + roll, teks berganti di tengah
SCENE("C_tunnel", 5.2, 5.15, function () {
  T("Cuma buka", { y: 960, size: 100, w: "SemiBold", t0: 0.05, t1: 1.45, hl: [[1, GREEN]], stagger: 0.2 });
  T("dan…", { y: 1090, size: 100, w: "SemiBold", t0: 0.6, t1: 1.45 });
  var ring = NUL(CX, CY, 0, 0, 5.15);
  K(ring, "Z Rotation", [[0, -40], [5.15, 75]], false, 40);
  var imgs = ["assets/phone_chat.png", "assets/phone_ebook.png", "assets/phone_skrip.png", "assets/phone_closed.png"];
  var R = 640;
  for (var rg = 0; rg < 3; rg++) for (var i = 0; i < 6; i++) {
    var th = i * 60 + rg * 30, a = th * Math.PI / 180;
    var l = IMG(imgs[(i + rg) % 4], { x: R * Math.cos(a), y: R * Math.sin(a), z: rg * 1700, s: 78, d3: true, ori: [0, 90, th], parent: ring, t0: 0, t1: 5.15 });
    tr(l, "Z Rotation").setValue(90);   // sisi panjang telefon ikut arah terowong
    K(l, "Opacity", [[1.0 + rg * 0.2, 0], [1.5 + rg * 0.2, 100]]);
  }
  // kamera: dari jauh masuk ke dalam terowong, kemudian meluru keluar (motion blur)
  CAM([[0, [CX, CY, -3600]], [1.4, [CX, CY, -2300]], [4.3, [CX, CY, 600]], [5.15, [CX, CY, 2600]]],
      [[0, [CX, CY, 0]], [1.4, [CX, CY, 1500]], [4.3, [CX, CY, 3800]], [5.15, [CX, CY, 6000]]], 900, 55);
  var tp = RECT(700, 120, 60, WHITE, CX, 958, 1.45, 5.1); K(tp, "Opacity", [[1.45, 0], [1.7, 92], [4.8, 92], [5.1, 0]]); K(tp, "Scale", [[4.05, [100, 100]], [5.1, [150, 150]]], true); shadow(tp, 14, 40, 18);
  T("Skrip.", { y: 975, size: 60, t0: 1.5, t1: 2.35, color: GREEN, out: false, stagger: 0.05 });
  T("Skrip. Formula.", { y: 975, size: 60, t0: 2.35, t1: 3.2, out: false, hl: [[1, GREEN]], stagger: 0.05 });
  T("Skrip. Formula. Team.", { y: 975, size: 60, t0: 3.2, t1: 4.05, out: false, hl: [[1, GREEN], [2, GREEN]], stagger: 0.05 });
  T("Semua dalam 1 ebook", { y: 975, size: 64, t0: 4.05, t1: 5.1, hl: [[3, GREEN]], zoom: 150 });
});

// ═════ D 10.2–12.1  telefon terbang melepasi kamera (motion blur) → bar "Closing…"
SCENE("D_bar", 10.2, 1.9, function () {
  var fly = IMG("assets/phone_skrip.png", { x: 900, y: 1500, z: -600, s: 80, d3: true, t0: 0, t1: 0.6 });
  K(fly, "Position", [[0, [-500, 1600, 400]], [0.55, [1700, 300, -900]]], false, 30);
  K(fly, "Y Rotation", [[0, 60], [0.55, -40]]); K(fly, "Z Rotation", [[0, -30], [0.55, 20]]);
  T("Closing…", { y: 900, size: 64, w: "SemiBold", t0: 0.45, t1: 1.9, color: DEEP, stagger: 0.05 });
  var track = RECT(760, 64, 32, [0.85, 0.92, 0.88], CX, 1010, 0.5, 1.9);
  var bar = RECT(760, 64, 32, GREEN, CX, 1010, 0.5, 1.9);
  tr(bar, "Anchor Point").setValue([-380, 0]); tr(bar, "Position").setValue([CX - 380, 1010]);
  K(bar, "Scale", [[0.6, [2, 100]], [1.65, [100, 100]]]);
  K(track, "Opacity", [[0.5, 0], [0.7, 100], [1.7, 100], [1.9, 0]]); K(bar, "Opacity", [[0.5, 0], [0.7, 100], [1.7, 100], [1.9, 0]]);
  CAM([[0, [CX, CY, -1500]], [1.9, [CX, CY, -1500]]], [[0, [CX, CY, 0]], [1.9, [CX, CY, 0]]], 1500);
});

// ═════ E 12.05–14.05  "Closed ✓" + confetti 3D
SCENE("E_closed", 12.05, 2.0, function () {
  T("Closed", { y: 690, size: 110, color: GREEN, t0: 0.0, t1: 1.95, stagger: 0.1 });
  var cc = IMG("assets/check_circle.png", { x: CX, y: 1030, z: 0, s: 60, d3: true, t0: 0.05, t1: 2.0 });
  K(cc, "Scale", [[0.05, [0, 0, 0]], [0.4, [72, 72, 72]], [0.55, [60, 60, 60]]]);
  K(cc, "Y Rotation", [[0.05, -120], [0.55, 0], [1.9, 18]]);
  K(cc, "Opacity", [[1.7, 100], [2.0, 0]]); shadow(cc, 20, 60, 25);
  var CFC = [GREEN, YEL, [0.2, 0.72, 0.95], [1, 0.45, 0.6], DEEP];
  for (var c = 0; c < 44; c++) {
    var cf = RECT(18 + rnd() * 16, 30 + rnd() * 18, 3, CFC[c % 5], CX, 1030, 0.3, 2.0, true);
    var ex = CX + (rnd() - 0.5) * 1200, ey = 1030 - 300 - rnd() * 800, ez = (rnd() - 0.5) * 1400;
    K(cf, "Position", [[0.3, [CX, 1030, 0]], [0.9, [ex, ey, ez]], [2.0, [ex + (rnd() - 0.5) * 200, ey + 1000, ez]]]);
    K(cf, "X Rotation", [[0.3, 0], [2.0, (rnd() - 0.5) * 1440]], true);
    K(cf, "Y Rotation", [[0.3, 0], [2.0, (rnd() - 0.5) * 1440]], true);
  }
  CAM([[0, [CX, CY, -1600]], [2.0, [CX + 60, CY - 40, -1350]]], [[0, [CX, CY, 0]], [2.0, [CX, CY, 0]]], 1500);
});

// ═════ F 14.0–17.45  panel "pustaka ebook" condong 3D + kamera tolak masuk + halaman flip keluar
SCENE("F_library", 14.0, 3.45, function () {
  T("Isi sebenar ebook", { y: 330, size: 66, w: "SemiBold", t0: 0.1, t1: 1.9, hl: [[1, GREEN]] });
  var P = NUL(CX, 1050, 0, 0, 3.45); tr(P, "Scale").setValue([78, 78, 78]);
  K(P, "X Rotation", [[0, 35], [2.0, 14]]); K(P, "Y Rotation", [[0, -38], [2.0, -14]]); K(P, "Z Rotation", [[0, 6], [2.0, 2]]);
  K(P, "Position", [[0, [CX + 300, 1300, 600]], [1.0, [CX, 1050, 0]]]);
  var panel = RECT(940, 1180, 40, WHITE, 0, 0, 0, 3.45, true); panel.parent = P; tr(panel, "Scale").setValue([100, 100, 100]); tr(panel, "Position").setValue([0, 0, 2]); shadow(panel, 40, 90, 22);
  var hd = RECT(940, 110, 0, DEEP, 0, -535, 0, 3.45, true); hd.parent = P; tr(hd, "Position").setValue([0, -535, 0]);
  var pages = [];
  for (var k = 0; k < 6; k++) {
    var gx = -300 + (k % 3) * 300, gy = -240 + Math.floor(k / 3) * 470;
    var pg = IMG("assets/page" + (k + 1) + ".png", { x: gx, y: gy, z: -160, s: 48, d3: true, parent: P, t0: 0, t1: 3.45 });
    K(pg, "Opacity", [[0.15 + k * 0.08, 0], [0.45 + k * 0.08, 100]]);
    pages.push(pg);
  }
  // kursor klik halaman 2, halaman itu terbang & flip ke kamera
  var cur = IMG("assets/cursor.png", { x: 900, y: 1500, s: 45, t0: 1.0, t1: 2.3 });
  K(cur, "Position", [[1.0, [980, 1500]], [1.75, [520, 860]]]);
  K(cur, "Scale", [[1.85, [45, 45]], [1.93, [36, 36]], [2.0, [45, 45]]], true);
  K(cur, "Opacity", [[1.0, 0], [1.2, 100], [2.1, 100], [2.3, 0]]);
  var pop = IMG("assets/page2.png", { x: 0, y: -240, z: -162, s: 48, d3: true, parent: P, t0: 1.95, t1: 3.45 });
  K(pop, "Position", [[1.95, [0, -240, -162]], [3.0, [0, -60, -1150]]], false, 50);
  K(pop, "Y Rotation", [[1.95, 0], [3.0, 360]], false, 50);
  K(pop, "Opacity", [[3.05, 100], [3.4, 0]]);
  K(pages[1], "Opacity", [[1.95, 100], [1.96, 0]], true);
  CAM([[0, [CX, CY, -2900]], [2.0, [CX, CY + 40, -1750]], [3.45, [CX - 40, CY, -1500]]], [[0, [CX, 1050, 0]], [2.0, [CX, 1000, 0]], [3.45, [CX - 40, 960, 0]]], 1500);
});

// ═════ G 17.35–19.25  halaman bertebaran pada kedalaman berbeza, kamera dolly (parallax)
SCENE("G_scatter", 17.35, 1.9, function () {
  for (var q = 0; q < 14; q++) {
    var ang = q * 2.4, rad = 380 + rnd() * 380, z = (q % 7) * 420 - 600;
    var x = CX + Math.cos(ang) * rad, y = CY + Math.sin(ang) * rad * 1.35;
    var pc = IMG("assets/page" + ((q % 7) + 1) + ".png", { x: x, y: y, z: z, s: 42, d3: true, t0: 0, t1: 1.9 });
    tr(pc, "Orientation").setValue([(rnd() - 0.5) * 50, (rnd() - 0.5) * 70, (rnd() - 0.5) * 50]);
    K(pc, "Y Rotation", [[0, (rnd() - 0.5) * 60], [1.9, (rnd() - 0.5) * 60]], true);
    K(pc, "Opacity", [[0, 0], [0.25, 100]]); shadow(pc, 30, 70, 25);
  }
  T("105 muka surat", { y: 1000, size: 92, t0: 0.25, t1: 1.9, hl: [[0, GREEN]], stagger: 0.14 });
  CAM([[0, [CX - 200, CY + 100, -2600]], [1.9, [CX + 120, CY - 60, -700]]], [[0, [CX, CY, 600]], [1.9, [CX, CY, 900]]], 1500);
});

// ═════ H 19.15–23.35  kad produk condong 3D, kamera tolak masuk ke butang + kursor klik → butang rata
SCENE("H_product", 19.15, 4.2, function () {
  T("Semua dah siap untuk anda", { y: 560, size: 56, w: "SemiBold", t0: 0.1, t1: 2.3, hl: [[2, GREEN]] });
  var card = IMG("assets/product_card.png", { x: CX, y: 1000, z: 0, s: 52, d3: true, t0: 0, t1: 2.75 });
  K(card, "Y Rotation", [[0, -45], [1.4, -16], [2.6, -8]]); K(card, "X Rotation", [[0, 30], [1.4, 12], [2.6, 6]]);
  K(card, "Position", [[0, [CX + 250, 1250, 500]], [1.0, [CX, 1000, 0]]]);
  K(card, "Opacity", [[0, 0], [0.3, 100], [2.45, 100], [2.75, 0]]); shadow(card, 40, 90, 28);
  var cur = IMG("assets/cursor.png", { x: 900, y: 1300, s: 45, t0: 0.6, t1: 4.2 });
  K(cur, "Position", [[0.6, [990, 1450]], [1.75, [690, 1060]], [2.7, [700, 1080]], [3.3, [560, 1080]]]);
  K(cur, "Scale", [[1.85, [45, 45]], [1.93, [36, 36]], [2.0, [45, 45]], [3.4, [45, 45]], [3.48, [36, 36]], [3.55, [45, 45]]], true);
  K(cur, "Opacity", [[0.6, 0], [0.9, 100], [3.9, 100], [4.2, 0]]);
  CAM([[0, [CX, CY, -1800]], [1.3, [CX, CY, -1500]], [2.6, [CX + 230, CY + 80, -700]]], [[0, [CX, CY, 0]], [1.3, [CX, CY, 0]], [2.6, [CX + 230, CY + 80, 0]]], 1500);
  var btn = RECT(640, 140, 70, GREEN, CX, 1060, 2.45, 4.2, true);
  K(btn, "Scale", [[2.45, [40, 40, 40]], [2.75, [100, 100, 100]], [3.42, [100, 100, 100]], [3.5, [92, 92, 92]], [3.6, [100, 100, 100]]]);
  K(btn, "Y Rotation", [[2.45, -40], [2.9, 0]]);
  K(btn, "Opacity", [[2.45, 0], [2.6, 100], [3.95, 100], [4.2, 0]]); shadow(btn, 24, 60, 30);
  var bt = T("Dapatkan · RM37", { y: 1080, size: 58, t0: 2.6, t1: 4.2, stagger: 0.06 });
});

// ═════ I 23.2–26.1  ✦ → perisai berpusing 3D → jaminan refund + harga
SCENE("I_jaminan", 23.2, 2.9, function () {
  var spk = IMG("assets/sparkle.png", { x: CX, y: 980, s: 45, t0: 0, t1: 0.85 });
  K(spk, "Scale", [[0, [0, 0]], [0.35, [55, 55]], [0.75, [10, 10]]]); K(spk, "Rotation", [[0, -90], [0.8, 90]]);
  var shd = IMG("assets/shield.png", { x: CX, y: 520, z: 0, s: 26, d3: true, t0: 0.5, t1: 2.9 });
  K(shd, "Scale", [[0.5, [0, 0, 0]], [0.8, [30, 30, 30]], [0.95, [26, 26, 26]]]);
  K(shd, "Y Rotation", [[0.5, -540], [1.3, 0]], false, 60); K(shd, "Opacity", [[2.6, 100], [2.9, 0]]);
  T("Ebook ni tak membantu?", { y: 760, size: 64, t0: 0.65, t1: 2.9 });
  var ybox = RECT(820, 250, 30, YEL, CX, 935, 1.15, 2.9, true);
  K(ybox, "X Rotation", [[1.15, -80], [1.5, 0]]); K(ybox, "Opacity", [[1.15, 0], [1.3, 100], [2.6, 100], [2.9, 0]]);
  shadow(ybox, 14, 10, 90);
  T("Kita REFUND\rbalik duit.", { y: 905, size: 88, t0: 1.25, t1: 2.9, lead: 98, stagger: 0.08, hl: [[1, [0.75, 0.05, 0.08]]] });
  T("Dalam 7 hari · claim via WhatsApp", { y: 1140, size: 36, w: "SemiBold", color: [0.25, 0.3, 0.28], t0: 1.7, t1: 2.9, stagger: 0.04 });
  T("RM67", { x: 225, y: 1320, size: 74, w: "SemiBold", color: GREY, t0: 1.95, t1: 2.9, reveal: false });
  var strike = RECT(200, 10, 5, RED, 225, 1296, 2.2, 2.9);
  tr(strike, "Anchor Point").setValue([-100, 0]); tr(strike, "Position").setValue([125, 1296]);
  K(strike, "Scale", [[2.2, [0, 100]], [2.4, [100, 100]]]); K(strike, "Opacity", [[2.65, 100], [2.9, 0]]);
  var np = T("RM37", { x: 630, y: 1340, size: 140, color: GREEN, t0: 2.35, t1: 2.9, reveal: false });
  K(np, "Scale", [[2.35, [40, 40]], [2.6, [108, 108]], [2.75, [100, 100]]]);
  CAM([[0, [CX, CY, -1500]], [2.9, [CX, CY, -1380]]], [[0, [CX, CY, 0]], [2.9, [CX, CY, 0]]], 1500);
});

// ═════ J 26.05–28.1  tagline 3 perkataan
SCENE("J_tagline", 26.05, 2.05, function () {
  T("Seen. Reply. Closed.", { y: 1000, size: 76, w: "SemiBold", t0: 0, t1: 2.0, stagger: 0.38, hl: [[0, GREY], [1, GREEN]], zoom: 106 });
  var sp2 = IMG("assets/sparkle.png", { x: 870, y: 930, s: 14, t0: 1.0, t1: 2.0 });
  K(sp2, "Scale", [[1.05, [0, 0]], [1.3, [16, 16]], [1.5, [12, 12]]]); K(sp2, "Rotation", [[1.0, 0], [2.0, 120]]);
});

// ═════ K 28.0–30  penutup: cover 3D + nama
SCENE("K_end", 28.0, 2.0, function () {
  var cv = IMG("assets/cover.png", { x: CX, y: 900, z: 0, s: 40, d3: true, t0: 0, t1: 2.0 });
  K(cv, "Y Rotation", [[0, -70], [0.7, -14], [2.0, 10]]); K(cv, "X Rotation", [[0, 20], [0.7, 4]]);
  K(cv, "Opacity", [[0, 0], [0.3, 100]]); K(cv, "Position", [[0, [CX, 1050, 400]], [0.7, [CX, 900, 0]]]);
  shadow(cv, 40, 80, 40);
  T("Wassap Masih Relevan?", { y: 1250, size: 58, t0: 0.4, t1: 2.0, out: false, hl: [[2, GREEN]] });
  T("@sirdharma_", { y: 1340, size: 40, w: "SemiBold", color: [0.3, 0.35, 0.33], t0: 0.8, t1: 2.0, out: false });
  CAM([[0, [CX - 150, CY, -1500]], [2.0, [CX + 80, CY, -1350]]], [[0, [CX, CY, 0]], [2.0, [CX, CY, 0]]], 1500);
});

app.project.save(new File("iklan_v3.ecproj"));
writeLn("OK main layers=" + MAIN.numLayers);

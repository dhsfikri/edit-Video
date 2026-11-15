// IKLAN EBOOK 2026 v2 — EffectCraft (skrip gaya After Effects). Animasi ikut babak reference, isi & aset milik Sir.
// Jalankan dari folder yang ada assets/ (dijana oleh vector_assets.py + halaman PDF):
//   effectcraft-cli script iklan_v2.jsx --empty      -> iklan_v2.ecproj
//   effectcraft-cli render --project iklan_v2.ecproj --comp IKLAN --out video.mp4 --format h264 --fps 30
// Safe zone TikTok: teks x 60–900 (pusat 480), y 220–1440.

var W = 1080, H = 1920, DUR = 30, FPS = 30, CX = 480;
var INK = [0.043, 0.043, 0.043], GREEN = [0.145, 0.827, 0.4], WHITE = [1, 1, 1], GREY = [0.55, 0.6, 0.58],
    YEL = [1, 0.84, 0.04], RED = [1, 0.3, 0.31], DEEP = [0.043, 0.239, 0.18], BG = [0.957, 0.98, 0.965];

var comp = app.project.items.addComp("IKLAN", W, H, 1, DUR, FPS);
comp.bgColor = BG;
var L = comp.layers;
var footCache = {};

function hex(c) { return c; }
function tr(layer, name) { return layer.property("Transform").property(name); }
function ease(prop) {
  for (var i = 1; i <= prop.numKeys; i++) {
    var dims = 1;
    try { var v = prop.keyValue(i); if (v && v.length && !prop.isSpatial) dims = v.length; } catch (e) {}
    var arr = []; for (var d = 0; d < dims; d++) arr.push(new KeyframeEase(0, 70));
    try { prop.setTemporalEaseAtKey(i, arr, arr); } catch (e) { try { prop.setTemporalEaseAtKey(i, [arr[0]], [arr[0]]); } catch (e2) {} }
  }
}
// K(layer, "Position", [[t, v], ...], noEase)
function K(layer, name, keys, linear) {
  var p = tr(layer, name);
  for (var i = 0; i < keys.length; i++) p.setValueAtTime(keys[i][0], keys[i][1]);
  if (!linear) ease(p);
  return p;
}
function span(layer, t0, t1) { layer.inPoint = t0; layer.outPoint = t1; }
function shadow(layer, dist, soft, op) {
  try { var ds = layer.property("Effects").addProperty("ADBE Drop Shadow");
    ds.property("Distance").setValue(dist); ds.property("Softness").setValue(soft); ds.property("Opacity").setValue(op || 45);
    try { ds.property("Direction").setValue(180); } catch (e) {} } catch (e) { writeLn("shadow err " + e); }
}
function blurKeys(layer, keys) {
  try { var b = layer.property("Effects").addProperty("ADBE Gaussian Blur 2").property("Blurriness");
    for (var i = 0; i < keys.length; i++) b.setValueAtTime(keys[i][0], keys[i][1]); ease(b); } catch (e) { writeLn("blur err " + e); }
}

// ── Teks: perkataan muncul satu-satu (opacity + naik + blur), keluar fade-up
function T(s, o) {
  var t = L.addText(s);
  var src = t.property("Source Text"), td = src.value;
  td.fontSize = o.size || 96; td.fillColor = o.color || INK; td.font = "Montserrat-" + (o.w || "ExtraBold");
  td.justification = o.just == "l" ? ParagraphJustification.LEFT_JUSTIFY : o.just == "r" ? ParagraphJustification.RIGHT_JUSTIFY : ParagraphJustification.CENTER_JUSTIFY;
  if (o.lead) td.leading = o.lead;
  src.setValue(td);
  tr(t, "Position").setValue([o.x == null ? CX : o.x, o.y]);
  span(t, o.t0, o.t1);
  var nw = s.split(/\s+/).length, st = o.stagger == null ? 0.16 : o.stagger;
  if (o.reveal !== false) {
    try {
      var an = t.property("Text").property("Animators").addProperty("ADBE Text Animator");
      var pr = an.property("Properties");
      pr.addProperty("ADBE Text Opacity").setValue(0);
      pr.addProperty("ADBE Text Position 3D").setValue([0, o.rise || 70, 0]);
      try { pr.addProperty("ADBE Text Blur").setValue([18, 18]); } catch (e) {}
      var sel = an.property("Selectors").addProperty("ADBE Text Selector");
      try { sel.property("Advanced").property("Based On").setValue(3); } catch (e) {}
      try { sel.property("Advanced").property("Ease Low").setValue(60); sel.property("Advanced").property("Ease High").setValue(60); } catch (e) {}
      var sp = sel.property("Start");
      sp.setValueAtTime(o.t0, 0); sp.setValueAtTime(o.t0 + Math.max(0.35, nw * st + 0.2), 100);
    } catch (e) { writeLn("anim err " + e); }
  }
  // warna per perkataan: hl = [[indexPerkataan, warna], ...]
  if (o.hl) for (var h = 0; h < o.hl.length; h++) {
    try {
      var a2 = t.property("Text").property("Animators").addProperty("ADBE Text Animator");
      a2.property("Properties").addProperty("ADBE Text Fill Color").setValue(o.hl[h][1]);
      var s2 = a2.property("Selectors").addProperty("ADBE Text Selector");
      s2.property("Advanced").property("Based On").setValue(3);
      s2.property("Advanced").property("Units").setValue(2);
      s2.property("Start").setValue(o.hl[h][0]); s2.property("End").setValue(o.hl[h][0] + 1);
    } catch (e) { writeLn("hl err " + e); }
  }
  if (o.out !== false) {
    K(t, "Opacity", [[o.t1 - 0.28, 100], [o.t1 - 0.02, 0]]);
    if (o.out == "up") K(t, "Position", [[o.t1 - 0.3, [o.x == null ? CX : o.x, o.y]], [o.t1, [o.x == null ? CX : o.x, o.y - 60]]]);
  }
  return t;
}

// ── Gambar / aset vektor
function IMG(file, o) {
  if (!footCache[file]) footCache[file] = app.project.importFile(new ImportOptions(new File(file)));
  var l = L.add(footCache[file]);
  if (o.d3) l.threeDLayer = true;
  tr(l, "Position").setValue(o.d3 ? [o.x, o.y, o.z || 0] : [o.x, o.y]);
  var sc = o.s || 100; tr(l, "Scale").setValue(o.d3 ? [sc, sc, sc] : [sc, sc]);
  span(l, o.t0, o.t1);
  return l;
}
function fadeIO(l, t0, t1, din, dout) {
  K(l, "Opacity", [[t0, 0], [t0 + (din || 0.3), 100], [t1 - (dout || 0.3), 100], [t1, 0]]);
}
// ── Shape bulat-segi (fill)
function RECT(w, h, r, color, x, y, t0, t1) {
  var s = L.addShape(); var g = s.property("Contents").addProperty("ADBE Vector Group");
  var rr = g.property("Contents").addProperty("ADBE Vector Shape - Rect"); rr.property("Size").setValue([w, h]); rr.property("Roundness").setValue(r);
  g.property("Contents").addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(color);
  tr(s, "Position").setValue([x, y]); span(s, t0, t1); return s;
}
function ELL(w, h, color, x, y, t0, t1) {
  var s = L.addShape(); var g = s.property("Contents").addProperty("ADBE Vector Group");
  g.property("Contents").addProperty("ADBE Vector Shape - Ellipse").property("Size").setValue([w, h]);
  g.property("Contents").addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(color);
  tr(s, "Position").setValue([x, y]); span(s, t0, t1); return s;
}

// ═════ LATAR: putih kehijauan + cahaya hijau lembut bergerak
var glow = ELL(1100, 1100, [0.78, 0.95, 0.85], 480, 900, 0, DUR);
blurKeys(glow, [[0, 220]]);
K(glow, "Position", [[0, [300, 700]], [10, [700, 1100]], [20, [350, 1250]], [30, [600, 800]]]);
K(glow, "Opacity", [[0, 70], [30, 70]], true);

// ═════ 0–2.9  HOOK: perkataan bertukar satu-satu (gaya "Turn Books → Audio → Any")
T("Customer", { y: 980, size: 120, w: "SemiBold", t0: 0.0, t1: 1.0, out: "up" });
T("SEEN ✓✓", { y: 990, size: 160, color: GREEN, t0: 1.0, t1: 1.85, stagger: 0.1, out: "up" });
T("tapi tak reply?", { y: 980, size: 104, w: "SemiBold", t0: 1.85, t1: 2.9, hl: [[2, RED]], out: "up" });

// ═════ 2.9–5.2  ayat + ikon kad terapung di tengah (gaya "Any language [ikon] Instantly")
T("Chat banyak", { y: 760, size: 100, w: "SemiBold", t0: 2.95, t1: 5.2, hl: [[1, GREEN]] });
var chip = IMG("assets/chip_chat.png", { x: CX, y: 980, s: 70, t0: 3.2, t1: 5.6 });
K(chip, "Scale", [[3.2, [0, 0]], [3.55, [78, 78]], [3.75, [70, 70]]]);
K(chip, "Rotation", [[3.2, -25], [3.75, -6], [5.0, 6]]);
K(chip, "Position", [[3.75, [CX, 980]], [5.0, [CX, 955]], [5.6, [CX, 640]]]);
K(chip, "Opacity", [[5.3, 100], [5.6, 0]]);
shadow(chip, 26, 50, 30);
T("Closing sikit.", { y: 1230, size: 100, w: "SemiBold", t0: 3.6, t1: 5.2, hl: [[1, RED]] });

// ═════ 5.2–6.6  "Cuma buka dan…" (gaya "Just drop and")
T("Cuma buka", { y: 980, size: 110, w: "SemiBold", t0: 5.25, t1: 6.6, hl: [[1, GREEN]], stagger: 0.2 });
var dan = T("dan…", { y: 1120, size: 110, w: "SemiBold", t0: 5.8, t1: 6.6 });

// ═════ 6.6–10.2  3 telefon 3D berpusing + teks kecil berganti di tengah
var ph = [
  ["assets/phone_chat.png", -330, 640, 120, 38, -8],
  ["assets/phone_skrip.png", 1290, 700, 160, -40, 9],
  ["assets/phone_ebook.png", CX, 1900, 260, 0, 0]
];
for (var i = 0; i < ph.length; i++) {
  var p = ph[i], l = IMG(p[0], { x: p[1], y: p[2], z: p[3], s: 52, d3: true, t0: 6.6, t1: 10.4 });
  K(l, "Y Rotation", [[6.6, p[4] * 1.8], [10.2, p[4] * 0.5]]);
  K(l, "Z Rotation", [[6.6, p[5]], [10.2, -p[5]]]);
  K(l, "X Rotation", [[6.6, i == 2 ? 55 : 8], [10.2, i == 2 ? 35 : -6]]);
  var px = i == 0 ? 20 : i == 1 ? 990 : CX, py = i == 2 ? 1760 : p[2];
  K(l, "Position", [[6.6, [p[1], p[2] + 300, p[3]]], [7.3, [px, py, p[3]]], [9.9, [px + (i == 0 ? -40 : i == 1 ? 40 : 0), py + (i == 2 ? 60 : -40), p[3] - 80]], [10.4, [px + (i == 0 ? -500 : i == 1 ? 500 : 0), py + (i == 2 ? 700 : -200), p[3]]]]);
  shadow(l, 40, 90, 35);
}
var pill = RECT(560, 140, 70, WHITE, CX, 1000, 7.0, 10.2);
K(pill, "Scale", [[7.0, [0, 0]], [7.35, [100, 100]]]); K(pill, "Opacity", [[9.9, 100], [10.2, 0]]);
shadow(pill, 20, 60, 25);
T("Skrip.", { y: 1025, size: 70, t0: 7.2, t1: 8.0, color: GREEN, out: false });
T("Skrip. Formula. Team.", { y: 1022, size: 50, t0: 8.0, t1: 9.0, stagger: 0.12, out: false, hl: [[1, GREEN], [2, GREEN]], reveal: true });
T("Semua dalam 1 ebook", { y: 1022, size: 50, t0: 9.0, t1: 10.2, stagger: 0.12, hl: [[3, GREEN]] });

// ═════ 10.2–12  swoosh hijau + progress bar naik
var sw = ELL(1300, 700, GREEN, -900, 1300, 10.1, 11.1);
blurKeys(sw, [[10.1, 60]]);
K(sw, "Position", [[10.1, [-900, 1500]], [10.65, [500, 900]], [11.1, [1900, 300]]]);
K(sw, "Scale", [[10.1, [50, 30]], [10.65, [110, 70]], [11.1, [60, 30]]]);
K(sw, "Rotation", [[10.1, -30], [11.1, 20]]);
T("Closing…", { y: 900, size: 64, w: "SemiBold", t0: 10.75, t1: 12.0, color: DEEP, stagger: 0.05 });
var track = RECT(760, 64, 32, [0.85, 0.92, 0.88], CX, 1010, 10.8, 12.05);
var bar = RECT(760, 64, 32, GREEN, CX, 1010, 10.8, 12.05);
tr(bar, "Anchor Point").setValue([-380, 0]); tr(bar, "Position").setValue([CX - 380, 1010]);
K(bar, "Scale", [[10.9, [2, 100]], [11.85, [100, 100]]]);
fadeIO(track, 10.8, 12.05, 0.2, 0.2); fadeIO(bar, 10.8, 12.05, 0.2, 0.2);

// ═════ 12–14  "Closed ✓" dalam bulatan + confetti
T("Closed", { y: 690, size: 110, color: GREEN, t0: 12.05, t1: 14.0, stagger: 0.1 });
var cc = IMG("assets/check_circle.png", { x: CX, y: 1030, s: 60, t0: 12.1, t1: 14.0 });
K(cc, "Scale", [[12.1, [0, 0]], [12.45, [72, 72]], [12.6, [60, 60]]]);
K(cc, "Opacity", [[13.7, 100], [14.0, 0]]);
shadow(cc, 20, 60, 25);
var CFC = [GREEN, YEL, [0.2, 0.72, 0.95], [1, 0.45, 0.6], DEEP], seed = 11;
function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
for (var c = 0; c < 36; c++) {
  var cf = RECT(16 + rnd() * 14, 26 + rnd() * 16, 3, CFC[c % 5], CX, 1030, 12.35, 14.0);
  var ex = CX + (rnd() - 0.5) * 1000, ey = 1030 - 300 - rnd() * 700;
  K(cf, "Position", [[12.35, [CX, 1030]], [12.95, [ex, ey]], [14.0, [ex + (rnd() - 0.5) * 160, ey + 900]]]);
  K(cf, "Rotation", [[12.35, 0], [14.0, (rnd() - 0.5) * 900]], true);
}

// ═════ 14–16.8  kad halaman ebook meluncur (gaya baris kad video)
T("Isi sebenar ebook:", { y: 520, size: 64, w: "SemiBold", t0: 14.0, t1: 16.8, hl: [[1, GREEN]] });
for (var k = 0; k < 5; k++) {
  var pg = IMG("assets/page" + (k + 1) + ".png", { x: 1400 + k * 400, y: 1000, s: 62, t0: 14.0, t1: 16.85 });
  K(pg, "Position", [[14.0 + k * 0.08, [1500 + k * 400, 1000]], [14.9 + k * 0.08, [CX - 400 + k * 400, 1000]], [16.5, [CX - 640 + k * 400, 1000]]]);
  K(pg, "Rotation", [[14.0, 8], [15.0, 0]]);
  K(pg, "Opacity", [[16.55, 100], [16.85, 0]]);
  shadow(pg, 26, 60, 35);
}

// ═════ 16.8–19  kad bertebaran 3D + teks tengah (gaya "Multiple Languages")
var sc = [[150, 520, -25, 30], [820, 470, 20, -28], [120, 1430, 18, 25], [840, 1480, -15, -30], [480, 300, 5, 0], [480, 1650, -6, 0]];
for (var q = 0; q < sc.length; q++) {
  var pc = IMG("assets/page" + ((q % 7) + 1) + ".png", { x: sc[q][0], y: sc[q][1], z: 0, s: 48, d3: true, t0: 16.8, t1: 19.1 });
  K(pc, "Z Rotation", [[16.8, sc[q][2] * 1.6], [19.0, sc[q][2]]]);
  K(pc, "Y Rotation", [[16.8, sc[q][3] * 1.5], [19.0, sc[q][3] * 0.6]]);
  K(pc, "Position", [[16.8, [CX + (sc[q][0] - CX) * 0.2, 960 + (sc[q][1] - 960) * 0.2, 600]], [17.4, [sc[q][0], sc[q][1], 0]], [18.8, [sc[q][0] + (sc[q][0] - CX) * 0.08, sc[q][1] + (sc[q][1] - 960) * 0.08, -60]], [19.1, [sc[q][0] + (sc[q][0] - CX) * 0.7, sc[q][1] + (sc[q][1] - 960) * 0.7, -60]]]);
  shadow(pc, 30, 70, 30);
}
T("105 muka surat", { y: 1000, size: 92, t0: 17.2, t1: 19.0, hl: [[0, GREEN]], stagger: 0.14 });

// ═════ 19–23  UI kad produk + kursor klik "Dapatkan"
var card = IMG("assets/product_card.png", { x: CX, y: 1000, s: 48, t0: 19.0, t1: 22.2 });
K(card, "Scale", [[19.0, [36, 36]], [19.5, [48, 48]], [21.3, [50, 50]], [22.0, [130, 130]]]);
K(card, "Position", [[19.0, [CX, 1200]], [19.5, [CX, 1000]], [21.3, [CX, 1000]], [22.0, [CX - 400, 960]]]);
K(card, "Opacity", [[19.0, 0], [19.4, 100], [21.8, 100], [22.2, 0]]);
shadow(card, 34, 80, 30);
T("Semua dah siap untuk anda", { y: 760, size: 56, w: "SemiBold", t0: 19.2, t1: 21.6, hl: [[2, GREEN]] });
var cur = IMG("assets/cursor.png", { x: 900, y: 1300, s: 45, t0: 19.6, t1: 23.0 });
K(cur, "Position", [[19.6, [980, 1400]], [20.6, [770, 1040]], [21.9, [770, 1040]], [22.3, [600, 1080]], [22.6, [575, 1075]]]);
K(cur, "Scale", [[20.75, [45, 45]], [20.85, [36, 36]], [20.95, [45, 45]], [22.65, [45, 45]], [22.75, [36, 36]], [22.85, [45, 45]]], true);
K(cur, "Opacity", [[19.6, 0], [19.9, 100], [22.75, 100], [23.0, 0]]);
// butang sahaja (gaya "Distribute To Youtube")
var btn = RECT(640, 140, 70, GREEN, CX, 1040, 22.0, 23.2);
K(btn, "Scale", [[22.0, [40, 40]], [22.3, [100, 100]], [22.7, [92, 92]], [22.85, [100, 100]]]);
K(btn, "Opacity", [[22.0, 0], [22.2, 100], [23.0, 100], [23.2, 0]]);
shadow(btn, 24, 60, 30);
T("Dapatkan · RM37", { y: 1060, size: 58, t0: 22.15, t1: 23.2, stagger: 0.06 });

// ═════ 23–26  ✦ → jaminan refund + harga
var spk = IMG("assets/sparkle.png", { x: CX, y: 980, s: 45, t0: 23.1, t1: 24.0 });
K(spk, "Scale", [[23.1, [0, 0]], [23.45, [55, 55]], [23.8, [10, 10]]]); K(spk, "Rotation", [[23.1, -90], [23.9, 90]]);
var shd = IMG("assets/shield.png", { x: CX, y: 520, s: 26, t0: 23.7, t1: 26.0 });
K(shd, "Scale", [[23.7, [0, 0]], [24.0, [30, 30]], [24.15, [26, 26]]]); K(shd, "Opacity", [[25.7, 100], [26.0, 0]]);
T("Ebook ni tak membantu?", { y: 760, size: 64, t0: 23.85, t1: 26.0 });
var ybox = RECT(820, 250, 30, YEL, CX, 935, 24.35, 26.0);
K(ybox, "Scale", [[24.35, [60, 60]], [24.6, [104, 104]], [24.75, [100, 100]]]); K(ybox, "Opacity", [[24.35, 0], [24.5, 100], [25.7, 100], [26.0, 0]]);
shadow(ybox, 14, 10, 90);
T("Kita REFUND\rbalik duit.", { y: 905, size: 88, t0: 24.45, t1: 26.0, lead: 98, stagger: 0.08, hl: [[1, [0.75, 0.05, 0.08]]] });
T("Dalam 7 hari · claim via WhatsApp", { y: 1140, size: 36, w: "SemiBold", color: [0.25, 0.3, 0.28], t0: 24.9, t1: 26.0, stagger: 0.04 });
T("RM67", { x: 225, y: 1320, size: 74, w: "SemiBold", color: GREY, t0: 25.15, t1: 26.0, reveal: false });
var strike = RECT(200, 10, 5, RED, 225, 1296, 25.4, 26.0);
tr(strike, "Anchor Point").setValue([-100, 0]); tr(strike, "Position").setValue([125, 1296]);
K(strike, "Scale", [[25.4, [0, 100]], [25.6, [100, 100]]]); K(strike, "Opacity", [[25.75, 100], [26.0, 0]]);
var np = T("RM37", { x: 630, y: 1340, size: 140, color: GREEN, t0: 25.55, t1: 26.0, reveal: false });
K(np, "Scale", [[25.55, [40, 40]], [25.8, [108, 108]], [25.95, [100, 100]]]);

// ═════ 26–28  tagline 3 perkataan (gaya "Translate. Dub. Distribute.")
T("Seen. Reply. Closed.", { y: 1000, size: 76, w: "SemiBold", t0: 26.05, t1: 28.0, stagger: 0.38, hl: [[0, GREY], [1, GREEN]] });
var sp2 = IMG("assets/sparkle.png", { x: 870, y: 930, s: 14, t0: 27.0, t1: 28.0 });
K(sp2, "Scale", [[27.1, [0, 0]], [27.25, [16, 16]], [27.5, [12, 12]]]); K(sp2, "Rotation", [[27.0, 0], [28.0, 120]]);

// ═════ 28–30  penutup: cover + nama (gaya logo akhir)
var cv = IMG("assets/cover.png", { x: CX, y: 900, s: 40, d3: true, t0: 28.0, t1: 30.0 });
K(cv, "Y Rotation", [[28.0, -50], [28.6, -12], [30, 8]]);
K(cv, "Opacity", [[28.0, 0], [28.3, 100]]);
K(cv, "Position", [[28.0, [CX, 1000, 0]], [28.6, [CX, 900, 0]]]);
shadow(cv, 40, 80, 40);
T("Wassap Masih Relevan?", { y: 1250, size: 58, t0: 28.4, t1: 30.0, out: false, hl: [[2, GREEN]] });
T("@sirdharma_", { y: 1340, size: 40, w: "SemiBold", color: [0.3, 0.35, 0.33], t0: 28.8, t1: 30.0, out: false });

app.project.save(new File("iklan_v2.ecproj"));
writeLn("OK layers=" + comp.numLayers);

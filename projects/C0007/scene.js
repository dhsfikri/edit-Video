// C0007 — Gaya Dynamic v1 PREMIUM (rujukan Apple), sampel 0–17.3s. Masa = timeline base (edit_v2_sample).
// Tiada emoji. Ikon garisan + tipografi kinetik + kamera licin.
window.SCENE = function (tl, api) {
  // 1) COLD OPEN 0–2.69: kad video (kiri, condong 3D halus) atas latar gelap + glow hangat;
  //    ikon dilukis ikut perkataan (dendeng → mangkuk, kampung → rumah, raya → bulan); ayat besar muncul ikut suara.
  tl.set("#glow", { opacity: 1 }, 0);
  api.card(0, { s: 0.5, x: -190, y: -150, ry: 10 }, 0);
  tl.fromTo("#cam", { opacity: 0, y: 40 }, { opacity: 1, y: -150, duration: 0.5, ease: "power3.out", immediateRender: false }, 0);
  tl.to("#cam", { rotationY: 6, duration: 2.4, ease: "sine.inOut" }, 0.1);
  api.icon(1.19, 2.6, "mangkuk", 690, 400, 170);
  api.icon(1.8, 2.6, "rumah", 690, 640, 170);
  api.icon(2.2, 2.6, "bulan", 690, 880, 170);
  api.type(2.66, [[["Teringat", "", 0.55], ["dendeng", "g", 1.19]], [["kampung,", "", 1.8], ["time", "", 2.15], ["raya.", "g", 2.29]]], 70, 1290, 62);
  // 2) Expand licin ke skrin penuh (masuk hook)
  api.full(2.45, 0.6);
  tl.to("#glow", { opacity: 0, duration: 0.4 }, 2.5);
  // 3) "nak tahu rahsia" 8.90–10.97: tolak masuk perlahan + vignette + ikon kunci terbuka
  tl.fromTo("#cam", { scale: 1 }, { scale: 1.08, duration: 2.0, ease: "sine.inOut", immediateRender: false }, 8.9);
  tl.to("#vig", { opacity: 1, duration: 0.4 }, 8.9);
  const k = api.icon(9.22, 10.85, "kunci", 730, 330, 150);
  tl.to(k.querySelector(".sh"), { y: -22, duration: 0.4, ease: "power3.out" }, 10.3);
  tl.to("#vig", { opacity: 0, duration: 0.3 }, 10.75);
  // 4) Kad TIP 01 (10.90–12.5): angka besar gradient + ayat; dipanjangkan atas "jangan tunjuk pandai"
  api.tipCard(10.9, 12.5, "01", "TIP PERTAMA", [[["Jangan", ""]], [["tunjuk", "g"], ["pandai.", "g"]]]);
  // 5) "tunjuk pandai" (14.12): ikon topi graduasi dilukis atas kepala
  api.icon(14.12, 16.1, "topi", 455, 300, 170);
  // 6) "banyak bercakap" (16.18): belon kaca muncul keliling kepala
  api.bubbles(16.18, 17.3, [
    ["Bla bla bla…", 70, 560], ["7 lapisan", 650, 520], ["Gred A", 60, 820],
    ["Ada sijil", 690, 780], ["10 tahun", 70, 1080], ["1001 kelebihan", 560, 1040],
  ]);
};

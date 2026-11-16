// C0007 Gaya Vox — babak 1–5 (sampel). Masa = timeline base edit_vox_sampel.
window.VOX = {
  duration: 10.97,
  paper: [[6.21, 8.85]],
  breaks: [2.93, 6.21, 8.9],
  words: [{"w": "Nak", "s": 0.0, "e": 0.485}, {"w": "orang", "s": 0.485, "e": 0.965}, {"w": "senang", "s": 0.965, "e": 1.565}, {"w": "percaya", "s": 1.565, "e": 2.105}, {"w": "kita", "s": 2.105, "e": 2.785}, {"w": "dan", "s": 2.925, "e": 3.32}, {"w": "bila", "s": 3.32, "e": 3.56}, {"w": "percaya", "s": 3.56, "e": 4.24}, {"w": "membeli", "s": 4.24, "e": 4.6}, {"w": "apa", "s": 4.6, "e": 5.08}, {"w": "sahaja", "s": 5.08, "e": 5.32}, {"w": "yang", "s": 5.32, "e": 5.46}, {"w": "kita", "s": 5.46, "e": 5.62}, {"w": "jual", "s": 5.62, "e": 6.08}, {"w": "buat", "s": 6.21, "e": 6.495}, {"w": "dia", "s": 6.495, "e": 6.755}, {"w": "teringat", "s": 6.755, "e": 7.395}, {"w": "dendeng", "s": 7.395, "e": 7.835}, {"w": "kat", "s": 7.835, "e": 8.015}, {"w": "kampung", "s": 8.015, "e": 8.355}, {"w": "time", "s": 8.355, "e": 8.495}, {"w": "raya", "s": 8.495, "e": 8.9}, {"w": "Nak", "s": 8.9, "e": 9.08}, {"w": "tahu", "s": 9.08, "e": 9.22}, {"w": "rahsia", "s": 9.22, "e": 9.46}, {"w": "ni,", "s": 9.46, "e": 9.62}, {"w": "tonton", "s": 9.7, "e": 9.88}, {"w": "video", "s": 9.88, "e": 10.1}, {"w": "ni", "s": 10.1, "e": 10.26}, {"w": "sampai", "s": 10.26, "e": 10.44}, {"w": "habis", "s": 10.44, "e": 10.8}],
  scene(tl, api) {
    // 1) 0–2.9 Hook: badge + jalur "Nak orang PERCAYA?" (highlight pada "percaya" 1.56)
    api.badge(0.1, 10.97, "TIPS JUALAN", "02");
    const s1 = api.strip(0.1, 2.88, '<span class="lt">Nak orang </span><hl>PERCAYA?</hl>', 80, 290, -1);
    api.hl(s1, 1.5);
    // 2) bulatan merah + nota
    api.circle(1.75, 2.88, 455, 262, 470, 150);
    api.note(2.05, 2.88, "kunci jualan", 600, 430);
    // 3) 2.93–6.2 "bila percaya, BELI" (highlight pada "membeli" 4.24) + gambar dendeng koyak
    const s2 = api.strip(2.95, 6.05, '<span class="lt">bila percaya, </span><hl>BELI</hl>', 80, 290, 1);
    api.hl(s2, 4.2);
    api.prop(4.3, 6.05, "dendeng.png", 160, 930, 720, 5, "right");
    // 4) 6.21–8.9 KOLAJ atas kertas (suara Sir): kertas turun, gambar ditampal ikut perkataan
    api.tearIn(6.0, 8.78);
    api.prop(6.6, 8.78, "dendeng.png", 110, 420, 740, -4, "left", "up");
    api.prop(7.8, 8.78, "rumah_kampung.png", 160, 760, 720, 2, "right", "down");
    api.prop(8.2, 8.78, "ketupat.png", 540, 1000, 340, -6, "bottom", "down");
    const s3 = api.strip(6.5, 8.8, '<span class="lt">teringat </span><hl>kampung</hl>', 80, 290, -1);
    api.hl(s3, 8.0);
    // 5) 8.9–10.97 kertas terkoyak → Sir; "nak tahu RAHSIA?" + nota + anak panah
    const s4 = api.strip(9.0, 10.97, '<span class="lt">nak tahu </span><hl>RAHSIA?</hl>', 80, 290, -1);
    api.hl(s4, 9.2);
    api.note(9.7, 10.97, "tonton sampai habis", 300, 1170, -2);
    api.arrow(10.25, 10.97, 760, 1040, 140, 160);
  }
};

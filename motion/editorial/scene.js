// C0225 — DRAF 1 GAYA EDITORIAL (brandkit, font tebal). 0–16.3s timeline base. Untuk banding dengan versi Split Kad.
window.ED = {
  duration: 16.3,
  face: { x: 526, y: 760 },
  words: [{"w": "saya", "s": 0.0, "e": 0.19}, {"w": "ada", "s": 0.19, "e": 0.39}, {"w": "satu", "s": 0.39, "e": 0.73}, {"w": "thread", "s": 0.73, "e": 0.87}, {"w": "yang", "s": 0.87, "e": 1.13}, {"w": "blow", "s": 1.13, "e": 1.39}, {"w": "up", "s": 1.39, "e": 1.89}, {"w": "kat", "s": 1.89, "e": 2.25}, {"w": "thread", "s": 2.25, "e": 3.19}, {"w": "Dan", "s": 3.19, "e": 3.77}, {"w": "kebanyakannya,", "s": 3.77, "e": 5.17}, {"w": "mungkin", "s": 5.4, "e": 5.68}, {"w": "agak", "s": 5.68, "e": 5.94}, {"w": "tak", "s": 5.94, "e": 6.14}, {"w": "setuju", "s": 6.14, "e": 6.44}, {"w": "dengan", "s": 6.44, "e": 6.66}, {"w": "apa", "s": 6.66, "e": 6.82}, {"w": "yang", "s": 6.82, "e": 6.88}, {"w": "saya", "s": 6.88, "e": 7.08}, {"w": "cadangkan", "s": 7.08, "e": 7.48}, {"w": "kalau", "s": 7.54, "e": 7.795}, {"w": "ada", "s": 7.795, "e": 8.015}, {"w": "customer", "s": 8.015, "e": 8.355}, {"w": "survey,", "s": 8.355, "e": 9.195}, {"w": "nak", "s": 9.195, "e": 9.39}, {"w": "buat", "s": 9.39, "e": 9.57}, {"w": "apa?", "s": 9.57, "e": 9.975}, {"w": "Sebab", "s": 9.975, "e": 10.125}, {"w": "kalau", "s": 10.125, "e": 10.465}, {"w": "terlebih", "s": 10.465, "e": 11.985}, {"w": "buat,", "s": 11.985, "e": 12.345}, {"w": "nanti", "s": 12.465, "e": 12.645}, {"w": "orang", "s": 12.645, "e": 12.825}, {"w": "kata", "s": 12.825, "e": 13.065}, {"w": "memaksa", "s": 13.065, "e": 13.625}, {"w": "Tapi", "s": 13.625, "e": 13.885}, {"w": "kalau", "s": 13.885, "e": 14.165}, {"w": "tak", "s": 14.165, "e": 14.365}, {"w": "buat", "s": 14.365, "e": 14.545}, {"w": "apa-apa,", "s": 14.545, "e": 14.965}, {"w": "kita", "s": 15.185, "e": 15.365}, {"w": "melepas", "s": 15.365, "e": 16.145}, {"w": "Kenapa?", "s": 16.245, "e": 16.595}],
  keywords: ["thread", "blow", "up", "setuju", "survey", "memaksa", "melepas"],
  hideCaps: [[0, 1.1]],
  scene(tl, a, put) {
    // 0–1.1 pembuka: panel hitam, label + perkataan besar
    const p0 = a.panel(0, 1.1, `<div style="position:absolute;left:80px;top:700px">
      <div id="l0" class="lbl" style="color:#25D366">thread saya</div>
      <div id="b0" class="big" style="font-size:260px;color:#fff;margin-top:18px">BLOW<br><span class="kw">UP.</span></div></div>`);
    tl.set(p0, { opacity: 1, filter: "blur(0px)" }, 0);
    a.reveal(0.05, p0.querySelector("#l0"), 0.4); a.reveal(0.15, p0.querySelector("#b0"), 0.55);
    // 1.1–5.38 Sir penuh + kad reply sebenar (kecil, sepertiga atas)
    a.cam(1.1, 1.0); a.cam(3.19, 1.06);
    const k1 = put(`<div style="position:absolute;left:80px;top:240px;width:820px">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px"><div class="lbl" style="color:#fff;font-size:28px;text-shadow:0 2px 10px rgba(0,0,0,.6)">reply paling popular</div>
      <div id="lk" style="background:#25D366;color:#0B0B0B;border-radius:40px;padding:8px 24px;font-weight:800;font-size:32px"><span id="n">0</span> setuju</div></div>
      <img src="assets/kad/r13.png" style="width:820px;border-radius:18px;box-shadow:0 18px 40px rgba(0,0,0,.35)"></div>`);
    a.pop(1.35, 5.38, k1);
    const lk = k1.querySelector("#lk"); a.pop(2.6, 5.38, lk, { dy: 10 }); a.counter(lk.querySelector("#n"), [[2.6, 0], [3.3, 22]]);
    // 5.38–7.5 perkataan editorial atas Sir
    a.cam(5.38, 1.0);
    const g = put(`<div style="position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,0))"></div>`);
    a.pop(5.3, 7.5, g, { dy: 0, dur: 0.3 });
    const t2 = put(`<div style="position:absolute;left:80px;top:290px"><div id="l2" class="lbl" style="color:#25D366">tapi ramai yang</div>
      <div id="b2" class="big" style="font-size:150px;color:#fff;margin-top:14px">TAK<br><span class="kw">SETUJU.</span></div></div>`);
    tl.set(t2, { opacity: 1 }, 0); a.reveal(5.45, t2.querySelector("#l2"), 0.4); a.reveal(5.6, t2.querySelector("#b2"));
    tl.to(t2, { opacity: 0, filter: "blur(8px)", duration: 0.25 }, 7.3);
    // 7.5–10.0 bar chat (gaya bar prompt) — customer menaip
    a.cam(7.5, 1.08);
    const bar = put(`<div style="position:absolute;left:80px;top:300px;width:820px">
      <div class="lbl" style="color:#fff;font-size:28px;margin-bottom:14px;text-shadow:0 2px 10px rgba(0,0,0,.6)">customer</div>
      <div class="card" style="position:relative;height:130px;border-radius:65px;display:flex;align-items:center;padding:0 36px;gap:22px">
        <div style="width:64px;height:64px;border-radius:50%;background:#e8e8e8;flex:none"></div>
        <div id="tx" style="font-weight:700;font-size:44px;color:#0B0B0B;white-space:nowrap"></div>
        <div style="margin-left:auto;width:70px;height:70px;border-radius:50%;background:#25D366;flex:none"></div></div></div>`);
    a.pop(7.55, 10.0, bar); a.type(bar.querySelector("#tx"), "Ok, saya survey dulu ye", 7.8, 0.045);
    // 10.0–16.2 kad senarai: memaksa / melepas dipangkah
    a.cam(10.0, 1.0); a.cam(13.6, 1.06);
    const ls = put(`<div class="card" style="left:80px;top:270px;width:820px;padding:34px 40px">
      <div class="lbl" style="color:#0B0B0B;opacity:.6;font-size:28px">pilihan seller</div>
      <div id="r1" style="margin-top:22px;display:flex;align-items:center;gap:22px;font-size:44px;font-weight:700;color:#0B0B0B;white-space:nowrap">
        <span style="flex:none;width:52px;height:52px;border-radius:50%;background:#0B0B0B;color:#fff;font-size:28px;display:flex;align-items:center;justify-content:center">1</span>
        <span style="position:relative">Terlebih buat → <b class="kw2">memaksa</b><i class="strike"></i></span></div>
      <div id="r2" style="margin-top:20px;display:flex;align-items:center;gap:22px;font-size:44px;font-weight:700;color:#0B0B0B;white-space:nowrap">
        <span style="flex:none;width:52px;height:52px;border-radius:50%;background:#0B0B0B;color:#fff;font-size:28px;display:flex;align-items:center;justify-content:center">2</span>
        <span style="position:relative">Tak buat apa-apa → <b>melepas</b><i class="strike"></i></span></div></div>`);
    a.pop(10.05, 16.3, ls);
    a.pop(10.3, 16.3, ls.querySelector("#r1"), { dy: 20 }); a.pop(13.65, 16.3, ls.querySelector("#r2"), { dy: 20 });
    const st = ls.querySelectorAll(".strike"); a.strike(13.05, st[0]); a.strike(15.4, st[1]);
  },
};

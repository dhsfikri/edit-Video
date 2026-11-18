// C0225 — Gaya SPLIT KAD (hijau), Hook 2. SAMPEL 10s (0–10.4 timeline base). Masa = cuts.json.
window.SPLIT = {
  duration: 10.4,
  face: { x: 526, y: 760, top: 545 },
  words: [{"w": "saya", "s": 0.0, "e": 0.19}, {"w": "ada", "s": 0.19, "e": 0.39}, {"w": "satu", "s": 0.39, "e": 0.73}, {"w": "thread", "s": 0.73, "e": 0.87}, {"w": "yang", "s": 0.87, "e": 1.13}, {"w": "blow", "s": 1.13, "e": 1.39}, {"w": "up", "s": 1.39, "e": 1.89}, {"w": "kat", "s": 1.89, "e": 2.25}, {"w": "thread", "s": 2.25, "e": 3.19}, {"w": "Dan", "s": 3.19, "e": 3.77}, {"w": "kebanyakannya,", "s": 3.77, "e": 5.17}, {"w": "mungkin", "s": 5.4, "e": 5.68}, {"w": "agak", "s": 5.68, "e": 5.94}, {"w": "tak", "s": 5.94, "e": 6.14}, {"w": "setuju", "s": 6.14, "e": 6.44}, {"w": "dengan", "s": 6.44, "e": 6.66}, {"w": "apa", "s": 6.66, "e": 6.82}, {"w": "yang", "s": 6.82, "e": 6.88}, {"w": "saya", "s": 6.88, "e": 7.08}, {"w": "cadangkan", "s": 7.08, "e": 7.48}, {"w": "kalau", "s": 7.54, "e": 7.795}, {"w": "ada", "s": 7.795, "e": 8.015}, {"w": "customer", "s": 8.015, "e": 8.355}, {"w": "survey,", "s": 8.355, "e": 9.195}, {"w": "nak", "s": 9.195, "e": 9.39}, {"w": "buat", "s": 9.39, "e": 9.57}, {"w": "apa?", "s": 9.57, "e": 9.975}, {"w": "Sebab", "s": 9.975, "e": 10.125}, {"w": "kalau", "s": 10.125, "e": 10.465}],
  keywords: ["thread", "blow", "up", "setuju", "customer", "survey"],
  modeA: [[0, 5.38], [7.5, 10.4]],
  scene(tl, a, put) {
    const FR = a.R(70, 1230, 940, 760);
    // ---- 0–5.4 MOD A: reply Threads sebenar bertimbun (nama dikabur) ----
    a.frame(0, FR, { s: 1.3, out: 60, cut: "s", dur: 0.01 });
    const lbl = put(`<div class="card" style="left:60px;top:250px;padding:16px 30px;border-radius:40px;font-weight:600;font-size:36px;color:#1A1A1A">Threads · <span class="ser" style="font-size:44px;color:#1fae55">"saya survey dulu ye"</span></div>`, "#back");
    a.pop(0.05, 5.38, lbl, { dy: -30 });
    const cards = [["r01", 340, -2.5], ["r11", 380, 2], ["r04", 420, -1.5], ["r13", 450, 1]];
    cards.forEach(([f, y, rot], i) => {
      const c = put(`<img src="assets/kad/${f}.png" style="position:absolute;left:${40 + (i % 2) * 20}px;top:${y}px;width:980px;border-radius:18px;box-shadow:0 20px 40px rgba(0,0,0,.28)">`, "#back");
      a.pop(0.25 + i * 0.62, 5.38, c, { dy: 220, rot, sc: 0.9 });
    });
    // denyut like "22" pada kad teratas
    const heart = put(`<div class="pill" style="left:600px;top:800px;background:#e5322d;font-size:38px;padding:10px 26px">&#9829; <span id="lk">0</span> setuju</div>`, "#back");
    a.pop(2.6, 5.38, heart, { dy: 30 });
    a.counter(heart.querySelector("#lk"), [[2.6, 0], [3.4, 22]]);
    tl.to(heart, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 3, ease: "sine.inOut" }, 3.4);
    // ---- 5.4–7.5 MOD B: muka penuh, "tak setuju" ----
    a.full(5.38, { z: 1.85, fy: 700, cut: "s" });
    // ---- 7.5–10.4 MOD A: kad chat "saya survey dulu ye" ----
    a.frame(7.5, FR, { s: 1.3, out: 60, cut: "s" });
    const chat = put(`<div class="card" style="left:90px;top:290px;width:820px;height:540px;padding:34px">
      <div style="display:flex;align-items:center;gap:18px"><div style="width:70px;height:70px;border-radius:50%;background:#d9d4cc"></div>
        <div><div style="font-weight:600;font-size:34px">Customer</div><div style="font-size:26px;color:#8a8a8a">dalam talian</div></div></div>
      <div id="b1" style="margin-top:34px;display:inline-block;background:#F1EEE9;border-radius:28px 28px 28px 8px;padding:22px 30px;font-size:40px;color:#1A1A1A">Harga berapa ya?</div>
      <div style="text-align:right;margin-top:18px"><div id="b2" style="display:inline-block;background:#25D366;color:#fff;border-radius:28px 28px 8px 28px;padding:22px 30px;font-size:40px">RM189, free postage</div></div>
      <div id="b3" style="margin-top:18px;display:inline-block;background:#F1EEE9;border-radius:28px 28px 28px 8px;padding:22px 30px;font-size:44px;font-weight:600;color:#1A1A1A">Ok, saya survey dulu ye</div></div>`, "#back");
    a.pop(7.55, 10.4, chat, { dy: 80 });
    ["#b1", "#b2", "#b3"].forEach((s, i) => a.pop(7.75 + i * 0.45, 10.4, chat.querySelector(s), { dy: 30, ease: "power3.out" }));
    tl.fromTo(chat.querySelector("#b3"), { boxShadow: "0 0 0 0 rgba(37,211,102,0)" }, { boxShadow: "0 0 0 8px rgba(37,211,102,.55)", duration: 0.3, yoyo: true, repeat: 1, immediateRender: false }, 8.9);
  },
};

// C0226 — KLON UJIAN gaya PRO (rujukan docs/rujukan/pro-miracle/) + penambahbaikan. 0–11.1s timeline base.
// Penambahbaikan vs rujukan: cold open atas Sir (bukan skrin hitam kosong), framing kiri/kanan ikut ayat, B-roll gambar sebenar CC0.
window.ED = {
  duration: 11.1,
  face: { x: 472, y: 714 },
  shiftY: 300,
  initCam: { x: -448.4, y: -235.8, scale: 1.95, filter: "blur(10px)" },
  capStyle: "pro",
  words: [{"w": "video", "s": 0.09, "e": 0.25}, {"w": "ni", "s": 0.25, "e": 0.39}, {"w": "akan", "s": 0.39, "e": 0.55}, {"w": "di-edit", "s": 0.55, "e": 0.85}, {"w": "oleh", "s": 0.85, "e": 1.07}, {"w": "Claude.", "s": 1.07, "e": 1.37}, {"w": "ini", "s": 1.4, "e": 1.5}, {"w": "adalah", "s": 1.5, "e": 1.9}, {"w": "akaun", "s": 1.9, "e": 2.42}, {"w": "baru", "s": 2.42, "e": 2.98}, {"w": "yang", "s": 2.98, "e": 3.24}, {"w": "saya", "s": 3.24, "e": 3.44}, {"w": "nak", "s": 3.44, "e": 3.66}, {"w": "create", "s": 3.66, "e": 3.86}, {"w": "from", "s": 3.86, "e": 4.14}, {"w": "zero.", "s": 4.14, "e": 4.56}, {"w": "everything", "s": 4.77, "e": 4.91}, {"w": "yang", "s": 4.91, "e": 5.13}, {"w": "saya", "s": 5.13, "e": 5.37}, {"w": "buat,", "s": 5.37, "e": 5.61}, {"w": "kita", "s": 5.71, "e": 5.95}, {"w": "akan", "s": 5.95, "e": 6.15}, {"w": "record.", "s": 6.15, "e": 6.53}, {"w": "kita", "s": 6.66, "e": 6.8}, {"w": "nak", "s": 6.8, "e": 6.96}, {"w": "jimat", "s": 6.96, "e": 7.14}, {"w": "masa,", "s": 7.14, "e": 7.52}, {"w": "nak", "s": 8.0, "e": 8.14}, {"w": "jimat", "s": 8.14, "e": 8.38}, {"w": "tenaga.", "s": 8.38, "e": 9.24}, {"w": "Betul", "s": 9.26, "e": 9.54}, {"w": "lah,", "s": 9.54, "e": 9.62}, {"w": "supaya", "s": 9.64, "e": 9.88}, {"w": "kita", "s": 9.88, "e": 10.04}, {"w": "boleh", "s": 10.04, "e": 10.18}, {"w": "shoot", "s": 10.18, "e": 10.38}, {"w": "dengan", "s": 10.38, "e": 10.54}, {"w": "lebih", "s": 10.54, "e": 10.72}, {"w": "banyak.", "s": 10.72, "e": 11.0}],
  keywords: ["zero", "record", "shoot"],
  redWords: ["record"],
  hideCaps: [[0, 1.35], [6.6, 9.2]],
  scene(tl, a, put) {
    const SYh = 300, Fh = { x: 472, y: 714 };
    const C = (z, side = 0) => { const lo = 1080 - 1080 * z, x0 = Fh.x - Fh.x * z; const x = side < 0 ? lo : side > 0 ? 0 : Math.min(0, Math.max(lo, x0)); return { x, y: SYh + Fh.y - Fh.y * z + (z - 1) * 150, scale: z }; };
    const cut = (t, z, side = 0) => tl.set("#camWrap", { ...C(z, side), filter: "blur(0px)" }, t);
    // ===== 0–1.35 COLD OPEN kinetik ATAS Sir (crash-zoom gelap di belakang) =====
    tl.fromTo("#camWrap", { filter: "blur(10px)" }, { filter: "blur(3px)", duration: 0.2, immediateRender: false }, 0.001);
    tl.fromTo("#camWrap", C(1.95), { ...C(2.1), duration: 1.2, ease: "none", immediateRender: false }, 0.05);
    const dk = put(`<div class="L" style="background:rgba(0,0,0,.72)"></div>`, "#fx"); tl.set(dk, { opacity: 1 }, 0); tl.to(dk, { opacity: 0, duration: 0.15 }, 1.25);
    const co = put(`<div style="position:absolute;left:80px;right:180px;top:560px;text-align:left">
      <div id="c1" style="font-weight:700;font-size:54px;color:#fff">video ni</div>
      <div id="c2" style="font-family:Anton;font-size:250px;line-height:.95;color:#fff;letter-spacing:.01em">DIEDIT</div>
      <div id="c3" style="font-weight:700;font-size:54px;color:#fff;margin-top:6px">oleh</div>
      <div id="c4" style="font-family:Anton;font-size:300px;line-height:.95;color:#FFD60A;transform-origin:left center">CLAUDE.</div></div>`, "#fx");
    tl.set(co, { opacity: 1 }, 0);
    [["#c1", 0.08], ["#c2", 0.55], ["#c3", 0.85], ["#c4", 1.05]].forEach(([s, t]) => { const n = co.querySelector(s); tl.set(n, { opacity: 0 }, 0);
      tl.fromTo(n, { opacity: 0, scale: s === "#c4" ? 1.5 : 1.15, filter: "blur(6px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: s === "#c4" ? 0.12 : 0.16, ease: "expo.out", immediateRender: false }, t); });
    const fl = put(`<div class="L" style="background:#fff;opacity:0"></div>`, "#fx"); tl.set(fl, { opacity: 0.85 }, 1.07); tl.set(fl, { opacity: 0 }, 1.11);
    tl.to(co, { opacity: 0, scale: 1.3, filter: "blur(10px)", duration: 0.16, ease: "power3.in" }, 1.22); tl.set(co, { opacity: 0 }, 1.4);
    // whip keluar → babak B
    tl.fromTo("#camWrap", { ...C(2.1), filter: "blur(3px)" }, { ...C(1.35, -1), filter: "blur(14px)", duration: 0.14, ease: "power3.in", immediateRender: false }, 1.24);
    tl.fromTo("#camWrap", { filter: "blur(14px)" }, { filter: "blur(0px)", duration: 0.12, immediateRender: false }, 1.38);
    // ===== 1.4–4.6 Sir ke KIRI + nombor gergasi "0" di kanan (gaya No.1) =====
    const z0 = put(`<div style="position:absolute;left:680px;top:520px;text-align:left">
      <div class="lbl" style="color:#25D366;font-size:30px">follower</div>
      <div id="zz" style="font-family:Anton;font-size:470px;line-height:.9;color:#FFD60A;opacity:.92">0</div>
      <div class="lbl" style="color:#fff;font-size:28px">hari 1</div></div>`);
    tl.set(z0, { opacity: 0 }, 0);
    tl.fromTo(z0, { opacity: 0, x: 80, filter: "blur(10px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.3, ease: "expo.out", immediateRender: false }, 1.9);
    tl.to(z0, { opacity: 0, x: 60, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, 4.42);
    cut(1.42, 1.35, -1); cut(3.24, 1.45, -1);
    // ===== 4.6–6.6 punch-in TENGAH + UI kamera (viewfinder, REC, timecode) =====
    cut(4.6, 1.35, 0); cut(5.71, 1.45, 0);
    const vf = put(`<div class="L">
      <svg width="1080" height="1920" style="position:absolute;inset:0"><g fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".9">
        <path d="M90 360 v-80 h80"/><path d="M990 360 v-80 h-80"/><path d="M90 1360 v80 h80"/><path d="M990 1360 v80 h-80"/></g></svg>
      <div style="position:absolute;left:120px;top:300px;display:flex;align-items:center;gap:14px;font-weight:800;font-size:36px;color:#fff"><span id="rd" style="width:26px;height:26px;border-radius:50%;background:#FF4D4D"></span>REC <span id="tc" style="font-weight:600;margin-left:10px">00:00:00</span></div></div>`);
    tl.set(vf, { opacity: 0 }, 0); tl.set(vf, { opacity: 1 }, 4.62); tl.set(vf, { opacity: 0 }, 6.6);
    tl.to(vf.querySelector("#rd"), { opacity: 0.15, duration: 0.25, yoyo: true, repeat: 3 }, 4.7);
    const tc = vf.querySelector("#tc"), o = { f: 0 }; tl.to(o, { f: 49, duration: 1.98, ease: "none", onUpdate: () => (tc.textContent = "00:00:" + String(Math.floor(o.f / 25)).padStart(2, "0") + ":" + String(Math.floor(o.f % 25)).padStart(2, "0")) }, 4.62);
    // ===== 6.6–9.2 B-ROLL kolaj PUTIH: jimat [MASA] + jam sebenar → jimat [TENAGA] + bateri =====
    const wb = a.panel(6.6, 9.2, `
      <div style="position:absolute;left:80px;top:330px;font-weight:800;font-size:110px;color:#0B0B0B;line-height:1">jimat</div>
      <div id="m1" style="position:absolute;left:80px;top:450px;font-family:Anton;font-size:230px;color:#FF4D4D;line-height:1">[MASA]</div>
      <div id="m2" style="position:absolute;left:80px;top:450px;font-family:Anton;font-size:230px;color:#FF4D4D;line-height:1;opacity:0">[TENAGA]</div>
      <img id="jm" src="assets/jam_hijau.png" style="position:absolute;left:470px;top:760px;height:640px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.35))">
      <svg id="bt" width="420" height="220" viewBox="0 0 420 220" style="position:absolute;left:420px;top:900px;opacity:0"><rect x="8" y="8" width="360" height="204" rx="30" fill="none" stroke="#0B0B0B" stroke-width="16"/><rect x="376" y="70" width="34" height="80" rx="10" fill="#0B0B0B"/><rect id="lv" x="34" y="34" width="308" height="152" rx="14" fill="#25D366"/></svg>
      <div style="position:absolute;left:80px;top:1290px;font-weight:600;font-size:34px;color:#0B0B0B;opacity:.55">claude edit · bukan saya</div>`, "#fff");
    tl.fromTo(wb.querySelector("#jm"), { y: 300, rotation: 12, opacity: 0 }, { y: 0, rotation: -4, opacity: 1, duration: 0.45, ease: "expo.out", immediateRender: false }, 6.75);
    tl.to(wb.querySelector("#jm"), { rotation: 2, duration: 1.1, ease: "sine.inOut" }, 7.2);
    tl.to(wb.querySelector("#m1"), { opacity: 0, y: -40, duration: 0.15 }, 7.95); tl.fromTo(wb.querySelector("#m2"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.2, ease: "expo.out", immediateRender: false }, 8.0);
    tl.to(wb.querySelector("#jm"), { x: 700, rotation: 25, opacity: 0, duration: 0.25, ease: "power3.in" }, 7.95);
    tl.fromTo(wb.querySelector("#bt"), { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.3, ease: "expo.out", immediateRender: false }, 8.1);
    tl.fromTo(wb.querySelector("#lv"), { attr: { width: 40 } }, { attr: { width: 308 }, duration: 0.7, ease: "power2.out", immediateRender: false }, 8.35);
    // ===== 9.2–11.1 Sir ke KANAN + jalur filem =====
    cut(9.2, 1.3, 1); cut(10.15, 1.4, 1);
    const fs = put(`<div style="position:absolute;left:60px;top:300px;width:300px;height:900px;overflow:hidden"><div id="st" style="display:flex;flex-direction:column;gap:14px"></div></div>`);
    const st = fs.querySelector("#st"); for (let i = 0; i < 9; i++) st.insertAdjacentHTML("beforeend", `<div style="height:170px;border-radius:12px;border:6px solid #fff;background:linear-gradient(135deg,#1d1d1d,#3a3a3a);position:relative"><div style="position:absolute;right:10px;bottom:8px;font-weight:800;font-size:22px;color:#FFD60A">${String(i + 1).padStart(2, "0")}</div></div>`);
    tl.set(fs, { opacity: 0 }, 0); tl.set(fs, { opacity: 1 }, 9.25);
    tl.fromTo(st, { y: 0 }, { y: -900, duration: 1.85, ease: "none", immediateRender: false }, 9.25);
  },
};

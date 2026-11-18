// C0226 — UJIAN INTRO 6s ikut rujukan @andy_feb (docs/rujukan/intro-andy/): light leak → grade teal + gradient + tipografi berselang → picit ke bulatan atas putih → ikon garisan mengorbit.
window.ED = {
  duration: 6.4,
  face: { x: 472, y: 714 },
  shiftY: 0,
  initCam: { x: -212.4, y: -395, scale: 1.45, filter: "blur(0px)" },
  words: [],
  hideCaps: [[0, 6.4]],
  scene(tl, a, put) {
    // ---- 0–0.6 LIGHT LEAK: kilat warna (merah-oren → cyan → oren) ----
    const lk = put(`<div class="L" style="mix-blend-mode:screen">
      <div id="k1" class="L" style="background:radial-gradient(70% 55% at 30% 30%, rgba(255,90,40,.95), rgba(255,140,60,.4) 45%, transparent 75%)"></div>
      <div id="k2" class="L" style="background:radial-gradient(80% 60% at 70% 40%, rgba(120,255,240,.85), rgba(80,200,220,.3) 50%, transparent 80%)"></div>
      <div id="k3" class="L" style="background:radial-gradient(75% 60% at 50% 70%, rgba(255,170,60,.9), rgba(255,120,40,.35) 50%, transparent 80%)"></div></div>`, "#fx");
    ["#k1", "#k2", "#k3"].forEach((s, i) => { const n = lk.querySelector(s); tl.set(n, { opacity: 0 }, 0);
      tl.to(n, { opacity: 1, duration: 0.08 }, i * 0.18); tl.to(n, { opacity: 0, duration: 0.14 }, i * 0.18 + 0.12); });
    const ex = put(`<div class="L" style="background:#fff"></div>`, "#fx"); tl.set(ex, { opacity: 0.55 }, 0); tl.to(ex, { opacity: 0, duration: 0.25 }, 0.02);
    // ---- 0.6–2.2 gradient bawah + TIPOGRAFI berselang ----
    const gb = put(`<div class="L" style="background:linear-gradient(rgba(0,0,0,0) 45%, rgba(0,0,0,.82) 85%)"></div>`, "#top");
    tl.set(gb, { opacity: 1 }, 0); tl.to(gb, { opacity: 0, duration: 0.15 }, 2.15);
    const ty = put(`<div style="position:absolute;left:100px;width:800px;top:980px">
      <div id="t1" style="font-weight:600;font-size:44px;color:#fff">video ni akan</div>
      <div id="t2" style="font-weight:800;font-size:150px;line-height:.95;color:#FFD60A">diedit</div>
      <div id="t3" style="font-weight:600;font-size:44px;color:#fff;text-align:right;margin-top:10px">oleh</div>
      <div id="t4" style="font-weight:800;font-size:150px;line-height:.95;color:#FFD60A;text-align:right">Claude.</div></div>`, "#top");
    const ic = put(`<svg width="130" height="130" viewBox="0 0 100 100" style="position:absolute;left:140px;top:1320px"><path d="M50 8 L58 42 L92 50 L58 58 L50 92 L42 58 L8 50 L42 42 Z" fill="none" stroke="#FFD60A" stroke-width="5" stroke-linejoin="round"/></svg>`, "#top");
    [["#t1", 0.6], ["#t2", 0.62], ["#t3", 0.85], ["#t4", 1.07]].forEach(([s, t]) => { const n = ty.querySelector(s); tl.set(n, { opacity: 0 }, 0);
      tl.fromTo(n, { opacity: 0, y: 30, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power3.out", immediateRender: false }, t); });
    a.draw ? 0 : 0;
    const icp = ic.querySelector("path"); const L = 340; icp.style.strokeDasharray = L; tl.set(icp, { strokeDashoffset: L }, 0);
    tl.to(icp, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, 1.15); tl.fromTo(ic, { rotation: -30, scale: 0.6 }, { rotation: 0, scale: 1, duration: 0.45, ease: "power3.out", immediateRender: false }, 1.15);
    tl.to([ty, ic], { opacity: 0, y: 40, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }, 2.0);
    // gerakan halus kamera (push perlahan) semasa babak gred
    tl.fromTo("#camWrap", { x: -212.4, y: -395, scale: 1.45 }, { x: -240.7, y: -430.7, scale: 1.51, duration: 2.15, ease: "none", immediateRender: false }, 0.05);
    // ---- 2.2–2.6 PICIT: penuh → pil → BULATAN, latar jadi putih ----
    tl.set("#root", { background: "#0B0B0B" }, 0); tl.set("#root", { background: "#F4F4F2" }, 2.2);
    tl.set("#vig", { opacity: 1 }, 0); tl.set("#vig", { opacity: 0 }, 2.2);
    tl.set("#cam", { clipPath: "inset(0px 0px 0px 0px round 0px)" }, 0);
    tl.to("#cam", { clipPath: "inset(430px 90px 600px 90px round 400px)", duration: 0.2, ease: "power3.in" }, 2.2);
    tl.to("#cam", { clipPath: "inset(570px 250px 770px 250px round 290px)", duration: 0.25, ease: "power3.out" }, 2.4);
    // muka di tengah bulatan (540,880), kepala penuh + sedikit bahu (z 1.2) — IKUT JEJAK MUKA (OpenCV, dilicinkan) supaya Sir sentiasa di tengah
    const FT = [[2.3, 605, 723], [2.4, 600, 726], [2.5, 593, 731], [2.6, 580, 740], [2.8, 559, 749], [2.9, 532, 757], [3.0, 504, 762], [3.1, 477, 765], [3.2, 458, 763], [3.4, 451, 758], [3.5, 457, 755], [3.6, 473, 757], [3.7, 498, 752], [3.8, 525, 748], [4.2, 553, 745], [4.3, 566, 746], [4.6, 577, 744], [4.7, 582, 748], [4.8, 586, 751], [4.9, 587, 753], [5.0, 596, 749], [5.2, 604, 746], [5.3, 609, 743], [5.4, 613, 741], [5.5, 614, 741], [5.6, 614, 742], [5.8, 613, 741], [5.9, 611, 742], [6.0, 607, 743], [6.1, 600, 742], [6.2, 594, 742], [6.4, 588, 742]], ZC = 1.0, CX = 540, CY = 935;
    const at = (fx, fy) => ({ x: CX - fx * ZC, y: CY - fy * ZC, scale: ZC });
    const ft0 = FT.find((r) => r[0] >= 2.6) || FT[0];
    tl.to("#camWrap", { ...at(ft0[1], ft0[2]), duration: 0.45, ease: "power3.inOut" }, 2.2);
    FT.filter((r) => r[0] > 2.7).forEach((r, i, arr) => { const prev = i ? arr[i - 1][0] : 2.65; tl.to("#camWrap", { ...at(r[1], r[2]), duration: Math.max(0.05, r[0] - prev), ease: "none" }, prev); });
    const sh = put(`<div style="position:absolute;left:250px;top:570px;width:580px;height:580px;border-radius:50%;box-shadow:0 30px 70px rgba(0,0,0,.28)"></div>`, "#back");
    if (!document.querySelector("#back")) {}
    tl.set(sh, { opacity: 0 }, 0); tl.set(sh, { opacity: 1 }, 2.6);
    // ---- 2.6–4.5 teks atas/bawah bulatan ----
    const up1 = put(`<div style="position:absolute;left:0;right:0;top:470px;text-align:center;font-weight:600;font-size:46px;color:#5b5b5b">ini akaun baru</div>`, "#top");
    const dn1 = put(`<div style="position:absolute;left:0;right:0;top:1185px;text-align:center;font-weight:800;font-size:96px;color:#0B0B0B">dari <span style="color:#1fae55">zero.</span></div>`, "#top");
    [[up1, 2.6], [dn1, 3.86]].forEach(([n, t]) => { tl.set(n, { opacity: 0 }, 0); tl.fromTo(n, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, t); tl.to(n, { opacity: 0, duration: 0.18 }, 4.55); });
    // ---- 4.6–6.4 everything kita REKOD + ikon garisan mengorbit ----
    const up2 = put(`<div style="position:absolute;left:0;right:0;top:470px;text-align:center;font-weight:600;font-size:46px;color:#5b5b5b">everything yang saya buat</div>`, "#top");
    const dn2 = put(`<div style="position:absolute;left:0;right:0;top:1185px;text-align:center;font-weight:800;font-size:96px;color:#0B0B0B">kita <span style="color:#1fae55">rekod.</span></div>`, "#top");
    [[up2, 4.75], [dn2, 5.7]].forEach(([n, t]) => { tl.set(n, { opacity: 0 }, 0); tl.fromTo(n, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, t); });
    const IC = {
      cam: '<rect x="14" y="30" width="58" height="42" rx="8"/><path d="M72 44 L88 34 V68 L72 58"/>',
      cut: '<circle cx="30" cy="70" r="10"/><circle cx="70" cy="70" r="10"/><path d="M36 62 L72 18 M64 62 L28 18"/>',
      chat: '<path d="M18 22 H82 V64 H46 L30 80 V64 H18 Z"/>',
      chart: '<path d="M18 82 H84 M28 70 V52 M46 70 V36 M64 70 V44 M80 70 V22"/>',
      play: '<circle cx="50" cy="50" r="34"/><path d="M42 36 L64 50 L42 64 Z"/>',
      heart: '<path d="M50 80 C 20 58, 14 40, 26 28 C 36 18, 48 24, 50 34 C 52 24, 64 18, 74 28 C 86 40, 80 58, 50 80 Z"/>',
    };
    const pos = [[210, 620], [850, 610], [150, 880], [845, 900], [215, 1130], [830, 1140]];
    Object.values(IC).forEach((d, i) => {
      const [x, y] = pos[i];
      const n = put(`<div style="position:absolute;left:${x - 55}px;top:${y - 55}px;width:110px;height:110px;border-radius:50%;background:#fff;box-shadow:0 14px 30px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center">
        <svg width="62" height="62" viewBox="0 0 100 100"><g fill="none" stroke="${i % 2 ? "#1fae55" : "#0B0B0B"}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">${d}</g></svg></div>`, "#top");
      tl.set(n, { opacity: 0 }, 0);
      tl.fromTo(n, { opacity: 0, scale: 0.3, x: (540 - x) * 0.4, y: (860 - y) * 0.4 }, { opacity: 1, scale: 1, x: 0, y: 0, duration: 0.4, ease: "back.out(1.6)", immediateRender: false }, 4.65 + i * 0.16);
      tl.to(n, { y: -14, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: 1 }, 5.1 + i * 0.05);
    });
  },
};

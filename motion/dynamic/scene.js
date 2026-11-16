// C0007 — koreografi Gaya Dynamic v1 (sampel 0–17.3s). Masa = timeline base (cuts.json edit_v2_sample).
window.SCENE = function (tl, api) {
  // 1) COLD OPEN 0–2.69: video jadi kad condong atas latar kampung malam raya
  tl.set("#kampung", { opacity: 1 }, 0);
  api.card(0, 0.62, -5, -70);
  tl.fromTo("#cam", { y: 500, scale: 0.45 }, { y: -70, scale: 0.62, duration: 0.35, ease: "expo.out" }, 0);
  tl.to("#pelita .fl", { scaleY: 1.25, transformOrigin: "50% 100%", duration: 0.12, yoyo: true, repeat: 21, stagger: 0.05, ease: "sine.inOut" }, 0);
  api.sticker(0.55, 2.62, "🌙", 760, 240, { size: 120, from: { x: 300, rotation: 40, scale: 0.5 }, bob: true });
  api.sticker(1.19, 2.62, "🍚", 600, 930, { size: 170, rot: -8 });
  api.sticker(1.27, 2.62, "🥩", 760, 990, { size: 130, rot: 12 });
  api.pill(1.3, 2.62, "DENDENG MAK 😋", 500, 1150, { y: true, rot: -3 });
  api.pill(1.8, 2.62, "KAMPUNG 🏡", 80, 1040, { rot: 4, from: { x: -400, scale: 1, rotation: 0 } });
  // 2) WHIP ke hook (2.69): kad kembang penuh
  api.leak(2.5);
  api.whip(2.69, (at) => { api.full(at); tl.set("#kampung", { opacity: 0 }, at); });
  // hook: punch "membeli" (5.61) + shake
  api.shake(5.61, 0.3, 16);
  api.leak(5.55);
  // 3) "nak tahu rahsia" 8.90–10.97: tolak masuk perlahan + vignette (rasa rahsia)
  tl.fromTo("#cam", { scale: 1 }, { scale: 1.1, duration: 2.0, ease: "sine.inOut", immediateRender: false }, 8.9);
  tl.to("#vig", { opacity: 1, duration: 0.3 }, 8.9);
  api.sticker(9.22, 10.9, "🤫", 720, 300, { size: 140, bob: true });
  tl.to("#vig", { opacity: 0, duration: 0.15 }, 10.9);
  tl.set("#cam", { scale: 1 }, 10.97);
  // 4) Kad TIP 1 (10.90–11.75) → punch "jangan tunjuk pandai"
  api.flash(10.88);
  api.tipCard(10.9, 11.75);
  api.shake(11.72, 0.32, 18);
  // 5) "tunjuk pandai" (14.12): topi graduasi jatuh atas kepala
  api.sticker(14.12, 16.1, "🎓", 450, 300, { size: 190, from: { y: -500, rotation: -30, scale: 1 }, rot: -8 });
  api.sticker(14.4, 16.1, "🤓", 790, 560, { size: 110 });
  // 6) "banyak bercakap" (16.18): belon cakap meletup keliling kepala
  api.bubbles(16.18, 17.3, [
    ["bla bla bla… 🗣️", 70, 560, "r"], ["7 lapisan!", 640, 520, "l"], ["gred A!", 60, 820, "r"],
    ["ada sijil!", 680, 780, "l"], ["10 tahun!", 70, 1080, "r"], ["1001 kelebihan!", 520, 1040, "l"],
  ]);
  api.shake(16.36, 0.6, 8);
};

# Resipi video harian @adabclosing (KUNCI — Sir, 2026-11-18)

**Gaya dikunci: EDITORIAL brandkit** (contoh lengkap: C0225 → `projects/C0225/scene_ed.js`, final `C0225_final_editorial.mp4`).
**Untuk video seterusnya Sir hanya akan minta: perbaiki / variasi HOOK.** Jangan cadang gaya baru melainkan Sir minta.

## Peraturan gaya (tetap)
- Sir **penuh skrin, tangkapan lebar**, zoom potong 1.0 ↔ 1.06–1.08 sahaja (maks ~1.1). Tiada cutout/pop-out pada A-roll.
- **Framing `shiftY: 300`**: video diturunkan, atas hitam pudar → grafik di sepertiga atas TIDAK tindih kepala.
- Warna BRANDKIT: hitam #0B0B0B, putih, hijau #25D366 (label), kuning #FFD60A (keyword / perkataan kedua), merah #FF4D4D hanya untuk pangkah.
- Font tebal sahaja: Poppins 700–800 (tiada serif / font kurus).
- Komponen (api dalam `motion/editorial/index.html`): `panel` (pembuka hitam + perkataan besar), `word`-style label + perkataan besar 2 baris, kad putih (bar chat menaip, senarai + pangkah, petikan reply), titik/kaunter, outro tetap (logo sticker + "KOMEN DI BAWAH: … ?").
- Caption: kotak gelap kecil paras dada (y 1290), perkataan-demi-perkataan, keyword kuning. Peralihan = blur. Tiada lantunan, tiada emoji dalam video.
- Bukti sebenar dahulu (SS Threads/komen → kad, nama & avatar DIKABURKAN).
- Outro tetap 1.6s beku: logo `aset/logo-adabclosing/adabclosing_telus_2160.png` + CTA komen 2 pilihan (contoh "PUJUK atau BIAR?").

## Tambahan Sir (2026-11-18, C0226)
- **Hook: Sir TERUS nampak dari frame 1** + tajuk di ruang atas + push-in perlahan (`a.push(0, 1.35, 1.0, 1.18)`). JANGAN panel hitam penuh menutup Sir di awal.
- **Variasi zoom antara babak:** selang-seli LEBAR (1.0) ↔ DEKAT (1.2–1.28), dan push-in/pull-out perlahan (`a.push(t0,t1,z0,z1)`). Muka kekal di tempat sama; maks ~1.3 (kepala tak masuk zon grafik).
- **2–3 B-roll skrin penuh motion graphic** (`a.panel`): contoh skrin "Claude sedang edit" (bar arahan + timeline dipotong + render %), telefon profil TikTok, telefon Threads + TikTok guna aset sebenar (SS kad, thumbnail). Caption kekal atas B-roll.

## Langkah (arahan)
1. **Log** rakaman baru dalam `LOG-VIDEO.md` (kunci ID Drive). Download: `curl -sSL -o X.MP4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
2. **Transkrip**: `ffmpeg -i X.MP4 -ac 1 -ar 16000 a16.wav` → `python3 -I pipeline/transcribe.py a16.wav projects/<ID>/transcript.json`.
3. **Plan ringkas kepada Sir**: 3 pilihan HOOK (ayat Sir sebenar + perkataan besar pembuka) → Sir pilih. (Gaya tak perlu dipilih lagi.)
4. **Potong**: `projects/<ID>/ranges.json` (susunan ayat, hook dulu) → `python3 pipeline/auto_segs.py a16.wav transcript.json ranges.json segs.json --gap 0.5 --thr -46` → semak perkataan tak terpotong → `edit.json` dengan `"pretranscode": true`, `"rotate": "none"`, `"fps": <rakaman>` → `python3 pipeline/cut.py projects/<ID>/edit.json` → transkrip semula base untuk sahkan.
5. **Beku outro**: `ffmpeg -i base.mov -vf tpad=stop_mode=clone:stop_duration=1.6 -af apad=pad_dur=1.6 … base_ext.mov` → `motion/editorial/assets/base.mp4`; kemas `data-duration` dalam `index.html`.
6. **Babak**: salin `projects/C0225/scene_ed.js` → `projects/<ID>/scene_ed.js`, tukar `words` (gabung token "-…"), `keywords`, `face` (OpenCV), babak ikut masa perkataan → salin ke `motion/editorial/scene.js` → `npx hyperframes snapshot` semak tindih kepala/teks.
7. **Suara**: `ffmpeg -i base_ext.mov -vn -ac 1 -ar 48000 -af "$(cat pipeline/voice_filter.txt)" voice_clean.wav` (EQ jelas + gate + noise reduction — Sir lulus).
8. **Render & gabung**: `npx hyperframes render . -o r.mp4 -f <fps> -q delivery -w 2` → mux suara → `compose.json` (SFX ringan: whoosh 0.16, pop 0.2, taip 0.2, pen 0.26, ding 0.2–0.25) dengan **`"crf": 13`** (sasaran ~12–15 Mbps; 19 Mbps tak perlu) → `python3 pipeline/compose.py`.
9. **QC**: `python3 pipeline/safezone_qc.py final.mp4 --times …` (semua babak + outro). Hantar **draf** → Sir lulus → final.
10. **Thumbnail + caption**: skill `tiktok-thumbnail` (`thumb.json`, `"freeY": true`, `series: ""`); caption `projects/<ID>/caption.md` (hook baris 1, cerita, ✅/❌, soalan, CTA komen sama dengan video, Follow @adabclosing, 8–10 hashtag).
11. **Post**: Sir upload manual (TikTok Studio, hidupkan Upload HD) ATAU Zernio (`media_generate_upload_link` → `posts_create_post` dengan `tiktok_settings.draft: true` → inbox TikTok). JANGAN post tanpa arahan Sir.
12. **Rekod**: `docs/akaun-adabclosing/JOURNEY.md` (log video + link). Selepas 24 jam tarik statistik Zernio (`analytics_get_analytics` akaun `6afc469e238b5ba47be82d95`).
13. **Ayat share WhatsApp** (personal / group / status): templat `docs/adabclosing/SHARE-WHATSAPP.md`.

## Nota kualiti
- TikTok mungkin tayang 540p dahulu untuk video baru (C0225: 576x1024 @0.44 Mbps pada jam pertama) — semak semula selepas 24 jam.

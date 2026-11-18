# Peraturan Projek (untuk Claude / editor)

## Skill (ikut langkah dalam skill)
- **`tiktok-edit`** (`.claude/skills/tiktok-edit/SKILL.md`) — edit video dari rakaman Raw sampai final.
- **`tiktok-thumbnail`** (`.claude/skills/tiktok-thumbnail/SKILL.md`) — thumbnail cover + caption.
- Skill boleh dikemas kini: naikkan nombor versi + changelog. Perubahan besar (gaya/urutan/peraturan) → brief Sir dulu; pembetulan teknikal kecil → terus kemas kini & maklumkan.

## FLOW KERJA RASMI (Sir, 2026-11-17) — ikut setiap video
1. **Sir upload raw** ke Drive `Raw` → saya log dalam `LOG-VIDEO.md` (kunci ID Drive).
2. **Analisis**: transkrip, spec rakaman, potensi hook, `riset-trend`.
3. **Cadangan** (tunggu Sir pilih): **2 pilihan gaya + 1 ditanda Cadangan**, setiap satu dengan storyboard visual (`director`) + **3 pilihan hook** (`hook-lab`) + plan animasi/edit.
4. **Reference dari Sir didahulukan**: sebelum guna, **klon ujian 5–10s hampir 100% sama** (susun atur, masa, gerakan, warna) guna aset kita → tunjuk sebelah-menyebelah dengan asal → Sir kata "dah sama" → baru adaptasi ke video Sir. Simpan analisis dalam `docs/rujukan/<nama>/`.
5. **Semakan**: plan → **sampel 10s** (hook + gaya; WAJIB untuk gaya/reference baru, boleh langkau untuk gaya yang Sir dah lulus) → draf penuh → final.
6. **Aset**: setiap aset baru (prop, grafik VectorCraft, template EffectCraft/HyperFrames, SFX, LUT) disimpan dalam repo (`aset/`, `motion/`, `motion/effectcraft/`) + rekod lesen. Zip mingguan untuk Sir upload ke Drive `Aset` (sandaran).
7. **Alat**: guna penuh **HyperFrames** (kad UI, caption, blok registry, 3D three.js), **VectorCraft** (grafik vektor, ikon, logo), **EffectCraft** (komposit, pop-out, 3D, tracking, render). Rujuk `docs/alat/UJIAN-EFFECTCRAFT-VECTORCRAFT.md` untuk ciri yang sah jalan.
8. **Rentak lalai: LAJU** — potongan rapat, perubahan visual setiap 1–3s, buang jeda/filler. Akan dilaras ikut report analitik Sir (bila diberi → simpan dalam `docs/analitik/`).

## WAJIB: Log video (`LOG-VIDEO.md`)
- **Awal setiap sesi:** senarai video dalam Drive `Raw` (termasuk subfolder) → banding dengan `LOG-VIDEO.md` → tambah video baru. Jangan edit video yang sudah ✅/⛔.
- **Selepas setiap langkah** (transkrip, brief, draf, final) → kemas kini baris video itu + commit.
- **Kunci = ID fail Drive** (nama kamera berulang, contoh dua `C0060`).

## WAJIB: Skill `director` dulu (reference → aset → storyboard visual), kemudian plan & brief

## WAJIB: Plan & brief dulu sebelum edit
Setiap kali nak mula edit video baru (atau ubah besar pada video sedia ada):
1. **Buat plan** guna `templates/brief-edit.md` (objektif, konsep, gaya editing, hook, timeline, style, aset, kualiti).
2. **Brief Sir Dharma** — bentangkan plan tu dengan jelas dan ringkas.
3. **Tunggu approval.** Jangan mula edit, render atau upload selagi Sir belum setuju.
4. Kalau ada perubahan pada plan masa edit (contoh: tukar hook, tukar gaya, B-roll tak cukup), **brief semula** sebelum teruskan.

## WAJIB: Brand kit & safe zone
- Ikut **`BRANDKIT.md`** untuk warna, font, siri, gaya video dan **thumbnail standard** (`motion/thumbnail-std/`, config `projects/<ID>/thumb.json`).
- **Semua teks & overlay dalam safe zone TikTok:** x 60–900, y 220–1440 (BRANDKIT §5).
- Setiap draf: jalankan `python3 pipeline/safezone_qc.py <video>` dan semak gambar sebelum hantar kepada Sir. Tiada teks dalam zon merah.
- Thumbnail: teks hanya dalam y 290–1450 (grid profil potong 3:4; "▷ views" di bawah kiri).

## Editor & tools
- **Claude yang edit** (bukan CapCut). FFmpeg (`pipeline/`) + HyperFrames (`motion/`) untuk tajuk, subtitle, B-roll, iklan; faster-whisper untuk transcribe.
- Rakaman diterima melalui upload chat atau folder Google Drive Sir.
- Hantar **draf** dulu untuk semakan, final hanya selepas approval.
- Export: 1080x1920, fps ikut rakaman (30/50), H.264 ~15–20 Mbps, AAC, `+faststart` (`pipeline/compose.py`).

## Identiti jenama (tetap)
- Siri: "AYAT CLOSING #NN" (konsep lain: "BEDAH CHAT #NN", "OBJECTION KILLER #NN")
- TikTok: @sirdharma_ (utama) · @adabclosing (akaun kedua, logo `aset/logo-adabclosing/adabclosing_profil.png`)
- Warna: hijau #25D366, hitam #0B0B0B, putih, keyword kuning #FFD60A
- Font: **Poppins** Bold/ExtraBold + Light (video), **Kalam** (tulisan tangan), Anton (headline thumbnail) — dikemas kini 2026-11-17 (BRANDKIT §3)
- Intro: badge siri + tajuk hook + bunyi signature, TANPA intro berasingan (Sir bercakap dari saat 0)
- Siri juga: "TIPS JUALAN #NN" (jualan umum / TikTok Shop)

## Google Drive (pustaka aset)
- `Folder Video` (id 1K3AzhqGOV5IhaRmOGf5TpdDUz4xZzx1g) → `Raw` (rakaman mentah, id 1U4zM7ykx7C97n6ZbkILKLw8fK_x_N3KB)
- `Folder Video/Aset` (id 1BvpjU99Can-NpRC2qbW4_pzIRQbdShGq):
  - `01 Intro` (1LAPSkDfYMTDljeh9k2dsTFtIVBeSuwwD) · `02 B-Roll` (1DI7CBy7abVmU4Kj0brD94chd5jXwTDDI)
  - `03 Outro` (19Zucgqv_279GQ27CzY7muqMQ3-tZElWy) · `04 Iklan 2s` (1ZFuMen20VBMqrRmI5WncmWC9TgFwLM9r)
- Baca/senarai fail: Google Drive connector. **Download** fail besar: `https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t` (folder perlu "Anyone with the link").
- **Upload** video ke Drive melalui connector TIDAK praktikal (kandungan mesti dihantar inline). Hantar fail kepada Sir (zip), Sir upload ke folder yang betul.
- Sumber asal semua aset (template HyperFrames) ada dalam repo `motion/` — boleh render semula bila-bila.

## Rujukan
- Flow penuh: `FLOW-EDIT-VIDEO.md`
- Template skrip: `templates/skrip-30s.md`
- Checklist QC: `templates/checklist-qc.md`

## Gaya komunikasi
- Guna Bahasa Melayu Malaysia yang santai tapi teliti.
- Niche: sales closing melalui WhatsApp.

## Keputusan & Keutamaan Sir (WAJIB ikut — dikemas kini setiap kali Sir bagi komen)
- **2026-11-16 — Gaya Dynamic:** "dynamic" = **transition + motion graphic** (video Sir sendiri bergerak: kad, zoom/expand, kad TIP skrin penuh, grafik ikut perkataan). BUKAN sekadar caption/pop teks + bunyi.
- **2026-11-16 — TIADA EMOJI** dalam video (sticker, tajuk, pop, mockup chat). Guna **grafik motion** (ikon garisan SVG yang dilukis, bentuk, tipografi kinetik).
- **2026-11-16 — Reference gaya: Apple Style Motion** — fail dalam Drive `Reference & Inspo/04 Idea Konten`. Analisis: `docs/rujukan/apple-motion/README.md`. Ringkas: **latar cerah**, **komponen UI yang morph** (pil → kad produk → butang), **gambar sebenar dalam kad**, tipografi bersih campur berat, pil chat, gerakan licin. (Versi gelap + ikon lukisan = SALAH, Sir tolak.)
- **2026-11-16 — Guna gambar/aset sebenar**, jangan lukis semula. Pustaka: `aset/gambar/` (+ `LESEN.md`), Drive `Aset`. Skill `director` WAJIB sebelum edit (reference → aset → storyboard VISUAL → approval).
- **2026-11-16 — Vibe premium, bukan kartun** (tiada emoji, tiada lantunan/gegaran, tiada ilustrasi kartun).
- Template: `motion/dynamic/` (lapisan motion + video) + `motion/overlay-dyn/` (teks/subtitle). Koreografi per video: `projects/<ID>/scene.js`.
- Sumber isi: dengar betul-betul — contoh C0007 "dinding" sebenarnya **dendeng** (lauk). Ayat tak pasti → tanya Sir.
- **2026-11-16 — GAYA VOX (pilot C0007)** — keputusan Sir (grill): spesifikasi penuh dalam `docs/rujukan/vox/README.md` §Keputusan Sir. Ringkas: seluruh video gaya Vox; **paper tear pada gambar + transition** (video Sir kekal bersih penuh skrin, TIADA grain/bingkai pada video Sir); muka Sir ~60% / kolaj ~40%; subtitle **karaoke biasa**; tajuk **jalur kertas + highlighter kuning**; coretan tangan **merah**; chat B-roll = **kad chat UI ala reel Hiiiilo** (`docs/rujukan/broll-hiiiilo/`) atas latar kertas Vox, masuk/keluar dengan koyakan kertas, aksen hijau brand (generik, tiada emoji); gambar dari **stok berlesen + `aset/gambar/`**; intro **soalan dulu** (percaya → beli → dendeng kampung); muzik: Sir tambah masa posting. C0008 tunggu Sir semak C0007.
- **2026-11-16 — GAYA PYNK (gaya edit baru, BUKAN upgrade gaya sedia ada)** — rujukan `docs/rujukan/pynk-vox-director/`. Sir mahu SEMUA elemen: B-roll Vox beranimasi, belah skrin + UI terapung, demo skrin + butang morph, caption monospace + logo penutup glitch + CTA komen. Keputusan: B-roll = **HyperFrames kolaj 2.5D** (bukan AI video); aset vintaj = **domain awam**; demo skrin = **mockup chat generik**; UI terapung = **ikut topik video**; logo = **fail dari Sir** (Drive `Aset/03 Outro`). Langkah sekarang: **bina template `motion/pynk/` + pustaka aset dulu**, belum guna pada video.
- **2026-11-17 — GAYA SPLIT KAD (rujukan @nicksaraevdaily)** — analisis `docs/rujukan/split-kad-nick/`, workflow `docs/split-kad/WORKFLOW.md`. Sir minta guna skill berkaitan + **EffectCraft** (komposit utama: split, bingkai matte, kad 3D, render). Kad UI berteks = HyperFrames → .mov telus → import EffectCraft. EffectCraft hanya baca fail dalam repo → letak media dalam `_kerja/` (diabaikan git). Font: `aset/fonts/` (Instrument Serif + Inter).
- **2026-11-17 — Font baru:** Poppins (tebal + Light untuk teks kurus) + Kalam (tulisan tangan). Montserrat/Caveat = lama. **Colour grading: KEKAL ASAL** — Sir lebih suka rakaman asal tanpa filter (pilihan dicuba: `docs/split-kad/pilihan_grading.png`). Jangan tambah grade/filter kecuali Sir minta.
- **2026-11-17 — B-ROLL VIDEO SIR = POP-OUT:** bila B-roll guna rakaman Sir sendiri (bukan stok), guna kesan pop-out yang sama (kepala/badan terkeluar dari bingkai) — resipi `docs/split-kad/WORKFLOW.md` §Resipi POP-OUT.
- **2026-11-17 — HOOK = STORYTELLING + IDEA KREATIF (+ trend):** setiap video baru jalankan `riset-trend` → `hook-lab` (3 pilihan hook lengkap dengan storyboard) sebelum brief. Nota trend: `docs/trend/`.
- **2026-11-17 — Akaun kedua @adabclosing:** rekod journey grow dari 0 dalam `docs/akaun-adabclosing/JOURNEY.md` (rekod mingguan + log setiap video). Data dari **Zernio** (connector claude.ai, akaun ID `6afc469e238b5ba47be82d95`) — tarik statistik terus; JANGAN post melalui Zernio tanpa arahan Sir.
- **2026-11-18 — POP-OUT HANYA UNTUK B-ROLL** (cutout berat: masa + token). Bingkai/A-roll Sir dalam Split Kad = TANPA cutout. **Jangan zoom dekat** — Sir sengaja rakam lebar supaya tak nampak talking head sangat (zoom maks ~1.1).
- **2026-11-18 — Sir: gaya SPLIT KAD (versi C0225) 'terlalu kartun'** — lulus sebagai final untuk C0225 sahaja; JANGAN guna lagi tanpa tanya. Perlu kenal pasti elemen yang rasa kartun sebelum gaya harian @adabclosing dimuktamadkan.
- **2026-11-18 — GAYA EDITORIAL (asas rujukan @akidahmad, `docs/rujukan/editorial-akid/`)** — Sir: **ikut warna BRANDKIT**, **tak suka font kurus** (guna Poppins 600–800 sahaja, tiada serif Didone). Template `motion/editorial/`. Draf 1 = 16s pertama C0225.

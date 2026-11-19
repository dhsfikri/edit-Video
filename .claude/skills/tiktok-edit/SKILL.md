---
name: tiktok-edit
description: Edit video TikTok Sir Dharma (@adabclosing gaya EDITORIAL harian, juga @sirdharma_) dari rakaman mentah sampai MP4 final — ambil dari Google Drive Raw, transcribe Bahasa Melayu, 3 pilihan hook, potong buang jeda, babak HyperFrames (hook crash-zoom, tajuk poster, B-roll skrin penuh, bulatan ikut muka), suara bersih, SFX, semakan penuh, QC safe zone, draf & final. Guna bila Sir minta edit / buat video / proses rakaman baru, atau ubah video sedia ada dalam repo edit-Video.
---

# Skill: Edit Video TikTok — Sir Dharma

**Versi:** 2.0 (2026-11-19)
**Changelog:**
- 2.0 — Aliran utama = **GAYA EDITORIAL @adabclosing** (dari C0225–C0236): rakaman 4K tegak, `cut.py` chunked + `size`, `pipeline/facetrack.py` (baru), suara set2, babak `motion/editorial/`, semakan snapshot → render `-w 1` → semakan penuh 2fps, perangkap biasa, nama fail ikut ID projek. Gaya v2 lama (@sirdharma_) dipindah ke Lampiran.
- 1.0 — Versi pertama, dari pengalaman C0029 (TIPS JUALAN #01) & C0296 (AYAT CLOSING #01).

> Sebelum mula: baca `CLAUDE.md` (bahagian Keputusan Sir), `BRANDKIT.md` dan **`docs/adabclosing/RESIPI-HARIAN.md`** (resipi dikunci). Komunikasi dengan Sir dalam Bahasa Melayu santai tapi teliti.
> Thumbnail & caption → skill `tiktok-thumbnail`. Hook → skill `hook-lab`.

---

## Peraturan WAJIB (jangan langkau)
1. **Hook dulu, tunggu Sir pilih.** Video @adabclosing: gaya dah dikunci — beri **3 pilihan hook** sahaja (jangan cadang gaya baru). Kalau Sir kata "buat yang the best", pilih sendiri & nyatakan sebabnya.
2. **Brand kit** (`BRANDKIT.md`) + keputusan Sir dalam `CLAUDE.md`: tiada emoji dalam video, tiada colour grading, font tebal sahaja (Poppins 600–800, Anton), headline **3–4 perkataan**, topik tak teknikal.
3. **Safe zone TikTok:** semua teks x 60–900, y 220–1440. Lebar teks ≤ 820px.
4. **Semakan penuh sebelum setiap draf** (lembaran 2fps + setiap transition) — jangan hantar tanpa tengok sendiri.
5. Hantar **draf** → Sir semak → **final** hanya selepas approve.
6. **Nama fail ikut ID projek:** `<ID>_draf_vN.mp4`, `<ID>_final.mp4`, `<ID>_thumbnail.png`, `<ID>_caption.md`.
7. Mockup app **generik**; tiada bukti bayaran/testimoni palsu (notifikasi = ilustrasi cerita Sir sendiri).
8. Kemas kini `LOG-VIDEO.md` + commit & push selepas setiap langkah.

---

## 0. Persediaan environment
```bash
python3 -c "import faster_whisper, cv2; print(cv2.__version__, hasattr(cv2,'CascadeClassifier'))"
ls motion/node_modules/hyperframes >/dev/null || (cd motion && npm install --no-audit --no-fund)
```
- **faster-whisper** `medium` (domain Hugging Face perlu dibenarkan). **OpenCV 4.x** (`opencv-python-headless==4.10.0.84`; v5 tiada `CascadeClassifier`).
- **HyperFrames** dipin dalam `motion/package.json`; GSAP & font dari `node_modules` → `assets/` template.
- Semua fail besar (raw, base, render, draf) → **scratchpad** `<S>/<ID>w/`. Fail `*_final*.mp4` dalam `projects/` diabaikan git.

## 1. Ambil rakaman (Drive `Raw/<tarikh>`)
- Senarai: Drive connector `search_files` (parent = folder Raw / subfolder tarikh). Banding dengan `LOG-VIDEO.md`, tambah baris baru (kunci = ID Drive).
- **JANGAN** `download_file_content` untuk video. Download:
```bash
curl -sSL -o <S>/raw-<ID>/<ID>.MP4 "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"
```
- Spec: `ffprobe … width,height,r_frame_rate`. Set semasa = **4K tegak 2160x3840, 25p** → `rotate: "none"`, `fps: 25`, `size: [1440,2560]`. (Rakaman lama Sony baring → `rotate cw/ccw`, lihat Lampiran.)

## 2. Transcribe + 3 hook
- `pipeline/transcribe.py` (faster-whisper medium int8, `language='ms'`, hantar **numpy array**). Simpan `projects/<ID>/transcript.json`.
- Baca transkrip penuh, kenal pasti cerita/twist. Perkataan pelik → `corrections` dalam edit.json; **yang tak pasti → tanya Sir** (contoh: "Fifi"=fee, "tergulai lebih"→"terlebih-lebih").
- `riset-trend` → `hook-lab`: 3 hook (ayat skrin 3–4 perkataan, visual 0–3s, storyboard). Simpan `projects/<ID>/PLAN.md`.

## 3. Potong buang jeda — `auto_segs.py` + `cut.py`
1. `projects/<ID>/ranges.json`: `[["nota", mula, akhir], …]` (saat raw, ikut susunan dalam video; hook boleh diambil dari tengah rakaman).
2. `python3 pipeline/auto_segs.py audio16k.wav transcript.json ranges.json segs.json` (ambang auto = p10 + 9 dB, buang jeda > 0.32s).
3. `projects/<ID>/edit.json`: `source, transcript, workdir, rotate, fps, color:"null", pretranscode:true, size:[1440,2560], corrections, segments`.
4. `python3 pipeline/cut.py projects/<ID>/edit.json` → `base.mov`, `words.json`, `cuts.json`. >14 segmen = **mod chunked automatik** (elak OOM 4K).
5. Transcribe semula `base.mov` → pastikan tiada suku kata terpotong. Betulkan `words.json` dengan tangan bila `corrections` kena perkataan salah (simpan sebagai `w<ID>.json`).
6. **Beku outro** ~1.6–2s: `ffmpeg -i base.mov -vf tpad=stop_mode=clone:stop_duration=2 -af apad=pad_dur=2 … base_ext.mov`.

## 4. Jejak muka + suara
```bash
python3 -I pipeline/facetrack.py <S>/<ID>w/base_ext.mov <S>/<ID>w/facetrack.json     # [[t,x,y]] ruang 1080x1920, median → ED.face
ffmpeg -i base_ext.mov -vn -ac 1 -ar 48000 -af "$(cat pipeline/voice_filter_set2.txt)" voice_clean.wav
```
- Suara: set 4K baru = `voice_filter_set2.txt` (TIADA gate/compressor — naikkan desir); set bilik lama = `voice_filter.txt`. Ukur SNR (p90−p5) sebelum/selepas.

## 5. Babak — `motion/editorial/` (gaya Editorial, resipi dikunci)
Tulis `projects/<ID>/scene_ed.js` (`window.ED = { duration, face, shiftY:300, initCam, words, keywords, hideCaps, scene(tl, a, put) }`) — salin helper dari video terdahulu (`projects/C0236/scene_ed.js` paling lengkap: `cam`, `slam`, `typeIn`, `flash`, `out`, `word`, `row`, `notif`).
Kemudian:
```bash
cp projects/<ID>/scene_ed.js motion/editorial/scene.js
ffmpeg -i base_ext.mov -an -c:v libx264 -crf 14 -preset fast -pix_fmt yuv420p -g 12 motion/editorial/assets/base.mp4
# kemas data-duration dalam motion/editorial/index.html (DUA tempat: #root dan <video>)
```
**Struktur standard (~60–70s):**
| Masa | Isi |
|---|---|
| 0–2.8s | **Hook crash-zoom**: `initCam` zoom 1.8 + blur, jejak muka (`facetrack` ≤ 2.68s), elemen cerita (cth kad notifikasi), tajuk **POSTER** (label Poppins 600 jarak .3em + Anton gergasi, kata kunci kuning) hentak + flash pada perkataan kunci, kemudian **whip** blur ke lebar |
| badan | Babak 3–6s bergilir: shot lebar dengan `word()` poster / pil / kad ✓ (sepertiga atas) · punch-in 1.2–1.4 pada ayat kuat · **2–3 B-roll skrin penuh** `a.panel` (motion graphic: neraca, langkah 1-2-3, chat generik) · **bulatan ikut muka** (`clipPath: circle()`, latar #F4F4F2, teks atas/bawah, pil terapung) |
| akhir | Penutup kuat (perkataan kunci + punch-in) → **outro** logo `assets/logo.png` + soalan CTA komen ("PERNAH MALU?") |
- `hideCaps` semasa hook, B-roll, bulatan & outro (mula outro **0.1s lebih awal** dari kumpulan perkataan terakhir).
- Variasi zoom: 1.0 lebar ↔ 1.15–1.42 dekat; jangan lebih 1.1 untuk shot biasa yang lama.

## 6. Semakan snapshot (sebelum render)
```bash
cd motion/editorial && npx hyperframes snapshot . -o <S>/snapX --at 0.4,1.3,2.0,4,6.8,… --no-end --timeout 20000
```
Baca `contact-sheet-*.jpg`. Semak: muka/mata tak tertutup (notifikasi, tajuk), teks lebar ≤ 820px (kanan ≤ 900), kad tak kosong lama, kamera betul selepas hook.

## 7. Render + gabung
```bash
npx hyperframes render . -o <S>/<ID>w/ed.mp4 -w 1 -f 25          # 4K: WAJIB -w 1 (2 worker = OOM), ~5 min / 70s
ffmpeg -i ed.mp4 -i voice_clean.wav -map 0:v -map 1:a -c:v copy -af apad -t <D> -c:a pcm_s16le ed_av.mov
python3 pipeline/compose.py projects/<ID>/compose.json             # base=ed_av.mov, out=<ID>_draf_vN.mp4, fps 25, crf 12, sfx[]
```
**SFX standard** (`motion/sfx/`): `whoosh` 0.16–0.3 pada setiap tukar babak/whip · `pop` 0.3–0.5 pada hentakan tajuk/pil · `pop` 0.18–0.2 pada baris kad · `ding` 0.2–0.3 pada notifikasi/✓ · `pen` 0.28 pada coretan · `klik` pada snap hook.

## 8. Semakan penuh (WAJIB) + QC
```bash
ffmpeg -i <draf> -vf "fps=2,scale=216:384,tile=12x6" -frames:v 2 <S>/<ID>w/rv/sheet%d.jpg     # baca kedua-dua lembaran
python3 pipeline/safezone_qc.py <draf> --times <frame penting>                                 # tiada teks dalam merah
```
**Perangkap yang pernah berlaku (semak setiap kali):**
- **Kamera tersangkut zoom selepas hook** — tween jejak muka/`+=` melepasi `tl.set` reset → akhiri jejak sebelum whip (≤ 2.68s).
- Frame 0 lebar walaupun hook zoom → guna `initCam` (bukan `tl.set` pada 0).
- **Kad kosong** > 0.5s sebelum baris pertama → masukkan kad ~0.3s sebelum baris pertama.
- Caption bocor dalam outro/B-roll → laras `hideCaps`.
- Notifikasi/tajuk tutup mata → turunkan muka (target y 760) atau naikkan kad (top 250).
- Pil/tajuk terkeluar kanan (KELUARGA?, SAYA BUAT DULU.) → kecilkan font, bukan alih ke luar safe zone.
- Bulatan: `clipPath circle` + latar root tukar ke #F4F4F2 masa masuk dan kembali hitam masa keluar; semak B-roll dalam bulatan frame demi frame.
- Pembetulan perkataan tersalah sasaran (cth "semua"→"customer" kena "layan semua orang") → betulkan dalam `words` secara manual.

## 9. Hantar → final
- Kemas `LOG-VIDEO.md` (🟡 draf), commit, `SendUserFile` `<ID>_draf_v1.mp4` + ringkasan babak + **perkataan yang Sir perlu sahkan**.
- Revisi → render semula (snapshot dulu untuk babak yang diubah).
- Approve → `cp` draf ke `projects/<ID>/<ID>_final.mp4` → skill `tiktok-thumbnail` (`<ID>_thumbnail.png`, `<ID>_caption.md`) → LOG ✅ → commit → hantar ketiga-tiga fail.
- Selepas Sir post: rekod dalam `docs/akaun-adabclosing/JOURNEY.md`, ayat share `docs/adabclosing/SHARE-WHATSAPP.md`.

---

# LAMPIRAN — Gaya v2 lama (@sirdharma_, versi 1.0)
> Masih sah untuk video akaun utama yang guna overlay Gaya v2. Rakaman Sony baring: kepala di KIRI → `rotate: "cw"`; di KANAN → `"ccw"`. Audio mic kamera bilik → `audio_extra: "afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80"`. Brief guna `templates/brief-edit.md` → `briefs/`.

## L5. Potong A-roll — `pipeline/cut.py`
`projects/<ID>/edit.json`: `source, transcript, workdir, rotate, fps, color, audio_extra, corrections, segments[{note,start,end,zoom,zoom_to,cy}]`.
- Gaya v2: zoom tetap ~1.2 (rakaman lebar) dan **tiada punch-in besar**; `color: "eq=brightness=0.01:contrast=1.04:saturation=0.86:gamma=1.02"`.
- Skrip **snap** masa potong ke titik senyap (mula: cari ke hadapan sahaja). Lepas run, baca `cuts.json` untuk masa SEBENAR — guna masa ini untuk semua langkah seterusnya.
- Semak hasil: transcribe semula `base.mov` untuk pastikan tiada perkataan terpotong.
- Output: `base.mov`, `words.json` (masa timeline baru), `cuts.json`.

## L6. B-roll
**Explainer Gaya v2 (utama)** — `motion/explainer/` (muka dalam bulatan + mockup chat generik + cop ✓/✕):
1. Klip muka ikut muka: `python3 -I pipeline/facecrop.py <SRC> motion/explainer/assets/face_<scene>.mp4 --rotate <cw|ccw> --seg <start>:<end> [--seg …]` — guna masa dari **cuts.json**.
2. Babak baru → tambah dalam `SCENES` (index.html): `script`, `box`, `stamp`, `msgs[[t,"c"|"s"|"sys"|"typing",teks]]`, `stampAt`.
3. Render: `npx hyperframes render --variables '{"scene":"x","dur":D,"face":"assets/face_x.mp4"}' -f <fps> -q high -w 4 -o ex.mp4` → **trim** `ffmpeg -t D` (composition `data-duration` tetap; render lebih panjang).
- Letak B-roll **semasa Sir bercakap** (bukan senyap).
**Animasi kedai/troli** — `motion/broll/` (`scene`: kupon/troli/kosong/selesai/konten).
**Higgsfield (AI)** — hanya B-roll suasana, semak kredit & anggaran dalam brief dulu.

## L7. Overlay Gaya v2 — `motion/overlay-v2/`
`projects/<ID>/data.js` → salin ke `motion/overlay-v2/data.js`. Skema `window.EDIT`:
```
duration, series, episode, maxWords(4), hideBadge[[a,b]] (sembunyi semasa B-roll),
titles[{start,end,lines[[{t,text,k:"script"|"bold"|"box"}]]}],
brackets[{start,end,box:[x,y,w,h]}], callouts[{t,end,x,y,text,kind:"ok"|"no"|"tag"}],
cta{start,text}, words[{w,s,e}]
```
- **Tajuk = headline:** muncul sekali gus (token selang 0.14s), **kekal lama**, TIDAK ikut suara. Hanya 2–3 tajuk sevideo: hook (0 → sebelum B-roll), poin utama, penutup (jawapan kepada hook → kesan loop).
- **Bracket:** kotak muka dari OpenCV pada `base.mov` (median per segmen).
- **Callout:** di bawah/tepi muka (y ±960–1120), template auto-clamp x ≤ 900.
- **CTA:** pendek (`🔔 follow @sirdharma_`).
- Pembetulan subtitle (cth "buat payment") dalam `words`.
- Bila parse `data.js` dengan Python: potong selepas `window.EDIT =` (komen mungkin ada `=`).
- Render: `npx hyperframes render --format mov -f <fps> -w 4 -o overlay.mov`.

## L8. Iklan (optional) — `motion/iklan/`
Iklan 4s "Setup Team Sales A–Z" (telus). Disisip dengan **video dihentikan seketika** di sempadan ayat (tiada perkataan hilang) melalui `insert` dalam compose; anjak semua masa overlay selepas titik sisipan.

## L9. Gabung — `pipeline/compose.py`
`projects/<ID>/compose.json`: `base, out, fps, insert{at,dur,overlay?,sfx?}, broll[{src,start,dur}], overlay, sfx[{src,at,vol}]`.
- **Tahan frame akhir 1s** untuk CTA: `insert: {"at": <durasi-0.05>, "dur": 1.0}`.
- Bunyi signature: `motion/intro/assets/signature.wav` @0.03, vol 0.4.
- Audio akhir: -14 LUFS, peak ≤ -2 dB (alimiter 0.79).

## L10. QC (WAJIB sebelum hantar)
```bash
python3 -I pipeline/safezone_qc.py <draf.mp4> <out.png> --times <frame penting>   # tiada teks dalam merah
ffmpeg -hide_banner -i <draf.mp4> -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"
```
Lihat frame: tajuk muncul? kotak terkeluar? subtitle bertindih? B-roll peralihan hitam? Betulkan dulu, baru hantar.

## L11. Hantar & iterasi
- `SendUserFile` draf (`<ID>_draf_vN.mp4`) + jadual ringkas apa berlaku setiap saat + **apa Sir perlu semak** (rentak, ekspresi, timing, ayat tak pasti).
- Revisi: kemas kini `edit.json`/`data.js`/`compose.json`, render semula, catat dalam bahagian **Revisi** brief.
- Approve → final: `<ID>_final.mp4` (salin draf yang diluluskan, sahkan decode) → hantar → tanda brief **FINAL**.
- Seterusnya: skill `tiktok-thumbnail` (thumbnail cover + caption).

## L12. Fail & simpanan
- Repo: `projects/<ID>/` (edit.json, data.js, compose.json, thumb.json, <ID>_caption.md, <ID>_thumbnail.png, <ID>_final.mp4), `briefs/`.
- Scratchpad: rakaman, base.mov, render, draf (besar — tidak dalam git).
- Aset untuk Drive → zip & hantar kepada Sir (connector tak boleh upload video). Folder Aset ID dalam `CLAUDE.md`.

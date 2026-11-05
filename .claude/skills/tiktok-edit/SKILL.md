---
name: tiktok-edit
description: Edit video TikTok Sir Dharma (@sirdharma_) dari rakaman mentah sampai MP4 final — ambil dari Google Drive Raw, transcribe Bahasa Melayu, brief, potong, B-roll explainer, overlay Gaya v2, iklan, gabung, QC safe zone, draf & final. Guna bila Sir minta edit / buat video / proses rakaman baru, atau ubah video sedia ada dalam repo edit-Video.
---

# Skill: Edit Video TikTok — Sir Dharma

**Versi:** 1.2 (2026-11-05)
**Changelog:**
- 1.2 — Gaya utama Sir: MAGAZINE + tajuk kad kaca (kinetic, keyword kuning). B-roll gaya magazine `motion/broll-mag/` (babak produk, database). `compose.py` sokong `blur` (kad kaca), `editorial.py` sokong `broll`.
- 1.1 — Tambah pakej gaya editorial (`EDITORIAL.md`, `motion/editorial/`, `pipeline/editorial.py`), 4 gaya. Medan `titleY` untuk muka tinggi dalam frame.
- 1.0 — Versi pertama, dari pengalaman C0029 (TIPS JUALAN #01) & C0296 (AYAT CLOSING #01).

> Sebelum mula: baca `CLAUDE.md` dan `BRANDKIT.md`. Komunikasi dengan Sir dalam Bahasa Melayu santai tapi teliti.
> Thumbnail & caption → skill `tiktok-thumbnail`.

---

## Peraturan WAJIB (jangan langkau)
1. **Brief dulu, tunggu approval** sebelum edit/render (`templates/brief-edit.md` → `briefs/`). Plan berubah masa edit → brief semula (soalan ringkas cukup).
2. **Brand kit** (`BRANDKIT.md`): warna, font, siri, Gaya v2.
3. **Safe zone TikTok:** semua teks x 60–900, y 220–1440. QC dengan `pipeline/safezone_qc.py` sebelum hantar draf.
4. Hantar **draf** → Sir semak → **final** hanya selepas approve.
5. Tiada janji hasil tanpa bukti. Mockup app **generik** (tiada logo/rupa WhatsApp/TikTok Shop sebenar). Tiada bukti bayaran/testimoni palsu.
6. Commit & push setiap langkah penting ke branch kerja.

---

## 0. Persediaan environment (semak dulu, pasang jika tiada)
```bash
python3 -c "import faster_whisper, cv2; print(cv2.__version__, hasattr(cv2,'CascadeClassifier'))"
ls motion/node_modules/hyperframes >/dev/null || (cd motion && npm install --no-audit --no-fund)
```
- **faster-whisper**: `pip install faster-whisper`. Model `medium` dari Hugging Face — perlu domain dibenarkan: `huggingface.co`, `cas-server.xethub.hf.co`, `cas-bridge.xethub.hf.co`, `us.aws.cdn.hf.co` (atau `*.hf.co`).
- **OpenCV MESTI 4.x** (`opencv-python-headless==4.10.0.84`). Versi 5 tiada `CascadeClassifier`. Kalau pip lambat: `pip download --only-binary=:all: opencv-python-headless==4.10.0.84 --no-deps -d <scratch>/whl` kemudian `pip install --no-deps <whl>`.
- **HyperFrames** dipin `0.8.179` (`motion/package.json`). GSAP & font dari `node_modules` (CDN disekat) — salin ke `assets/` projek.
- **Playwright/Chromium** sudah ada (untuk thumbnail).
- Fail kerja besar → **scratchpad**, bukan repo.

## 1. Ambil rakaman dari Google Drive
- Senarai: Drive connector `search_files` dengan `parentId = '1U4zM7ykx7C97n6ZbkILKLw8fK_x_N3KB'` (folder Raw).
- **JANGAN** guna `download_file_content` untuk video (base64 masuk konteks — gagal).
- Download (folder perlu "Anyone with the link"; domain `drive.usercontent.google.com` dibenarkan):
```bash
D=<scratch>/raw-<ID> && mkdir -p $D && curl -sSL -o $D/<NAMA>.MP4 \
 "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"
```

## 2. Semak spec
```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate,color_transfer -of compact <f>
ffmpeg -v error -y -i <f> -vf "fps=1/4,scale=360:-1,tile=6x2" -frames:v 1 sheet.png   # lihat gambar
```
- **Rakaman Sony selalu dirakam baring** (1920x1080). Lihat arah kepala: kepala di KIRI → `rotate: "cw"`; kepala di KANAN → `"ccw"`. Sahkan dengan `transpose=1/2` pada satu frame.
- FPS: kekal ikut rakaman (50 atau 30).
- Audio mic kamera dalam bilik → `audio_extra: "afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80"`. Beritahu Sir gema tak boleh dibuang sepenuhnya.

## 3. Transcribe (Bahasa Melayu)
```python
# python3 -I ; HANTAR numpy array (bukan path) — pyav dalam env ni rosak untuk path
w=wave.open('audio16k.wav'); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
m=WhisperModel('medium',device='cpu',compute_type='int8',cpu_threads=4)
segs,_=m.transcribe(a,language='ms',word_timestamps=True,vad_filter=True,beam_size=5)
```
Simpan JSON `{"segments":[{start,end,text,words:[{w,s,e}]}]}`. Cetak word timestamps untuk rancang potongan.
**Salah dengar biasa:** "say"→**sale**, "dedisyen"→**decision**, "bayar bayaran"→**buat payment**, "geng-geng dof"/"bukan kesian" (tak jelas → tanya Sir/buang). Ayat tak jelas → transcribe semula snippet itu sahaja (temperature 0 & 0.4) dan **tanya Sir** dalam brief.

## 4. Brief → tunggu approval
`briefs/<YYYY-MM-DD>_<ID>_<slug>.md`: spec, objektif, siri (`AYAT CLOSING` = closing/WhatsApp, `TIPS JUALAN` = jualan umum/TikTok Shop), struktur timeline (sumber → ayat → grafik), ayat dibuang, B-roll, soalan untuk Sir (privasi peserta, ayat tak jelas, iklan ya/tidak).
**Hook mesti di depan** (soalan/masalah). Buang pembukaan lambat ("Alhamdulillah…", "Faham? Dan satu lagi…", "So…").

## 5. Potong A-roll — `pipeline/cut.py`
`projects/<ID>/edit.json`: `source, transcript, workdir, rotate, fps, color, audio_extra, corrections, segments[{note,start,end,zoom,zoom_to,cy}]`.
- Gaya v2: zoom tetap ~1.2 (rakaman lebar) dan **tiada punch-in besar**; `color: "eq=brightness=0.01:contrast=1.04:saturation=0.86:gamma=1.02"`.
- Skrip **snap** masa potong ke titik senyap (mula: cari ke hadapan sahaja). Lepas run, baca `cuts.json` untuk masa SEBENAR — guna masa ini untuk semua langkah seterusnya.
- Semak hasil: transcribe semula `base.mov` untuk pastikan tiada perkataan terpotong.
- Output: `base.mov`, `words.json` (masa timeline baru), `cuts.json`.

## 6. B-roll
**Explainer Gaya v2 (utama)** — `motion/explainer/` (muka dalam bulatan + mockup chat generik + cop ✓/✕):
1. Klip muka ikut muka: `python3 -I pipeline/facecrop.py <SRC> motion/explainer/assets/face_<scene>.mp4 --rotate <cw|ccw> --seg <start>:<end> [--seg …]` — guna masa dari **cuts.json**.
2. Babak baru → tambah dalam `SCENES` (index.html): `script`, `box`, `stamp`, `msgs[[t,"c"|"s"|"sys"|"typing",teks]]`, `stampAt`.
3. Render: `npx hyperframes render --variables '{"scene":"x","dur":D,"face":"assets/face_x.mp4"}' -f <fps> -q high -w 4 -o ex.mp4` → **trim** `ffmpeg -t D` (composition `data-duration` tetap; render lebih panjang).
- Letak B-roll **semasa Sir bercakap** (bukan senyap).
**Animasi kedai/troli** — `motion/broll/` (`scene`: kupon/troli/kosong/selesai/konten).
**B-roll MAGAZINE (gaya utama)** — `motion/broll-mag/` (lihat `EDITORIAL.md`): muka segi empat + kad kaca + kandungan generik. Masuk `data.js` → `broll`.
**Higgsfield (AI)** — hanya B-roll suasana, semak kredit & anggaran dalam brief dulu.

## 7. Overlay Gaya v2 — `motion/overlay-v2/`
> **Baru (1.1):** kalau brief pilih gaya editorial, guna `motion/editorial/` (skema data sama + `titleY`, `chapter`, `transitions`) dan render terus dengan
> `python3 -I pipeline/editorial.py projects/<ID>/edit.json projects/<ID>/data.js <gaya> <outdir>` (cut → overlay → compose → QC). B-roll/iklan: tambah dalam `<outdir>/<gaya>/compose.json` dan jalankan `compose.py` semula.

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

## 8. Iklan (optional) — `motion/iklan/`
Iklan 4s "Setup Team Sales A–Z" (telus). Disisip dengan **video dihentikan seketika** di sempadan ayat (tiada perkataan hilang) melalui `insert` dalam compose; anjak semua masa overlay selepas titik sisipan.

## 9. Gabung — `pipeline/compose.py`
`projects/<ID>/compose.json`: `base, out, fps, insert{at,dur,overlay?,sfx?}, broll[{src,start,dur}], overlay, sfx[{src,at,vol}]`.
- **Tahan frame akhir 1s** untuk CTA: `insert: {"at": <durasi-0.05>, "dur": 1.0}`.
- Bunyi signature: `motion/intro/assets/signature.wav` @0.03, vol 0.4.
- Audio akhir: -14 LUFS, peak ≤ -2 dB (alimiter 0.79).

## 10. QC (WAJIB sebelum hantar)
```bash
python3 -I pipeline/safezone_qc.py <draf.mp4> <out.png> --times <frame penting>   # tiada teks dalam merah
ffmpeg -hide_banner -i <draf.mp4> -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"
```
Lihat frame: tajuk muncul? kotak terkeluar? subtitle bertindih? B-roll peralihan hitam? Betulkan dulu, baru hantar.

## 11. Hantar & iterasi
- `SendUserFile` draf (`<ID>_draf_vN.mp4`) + jadual ringkas apa berlaku setiap saat + **apa Sir perlu semak** (rentak, ekspresi, timing, ayat tak pasti).
- Revisi: kemas kini `edit.json`/`data.js`/`compose.json`, render semula, catat dalam bahagian **Revisi** brief.
- Approve → final: `<YYYYMMDD>_<slug>.mp4` (salin draf yang diluluskan, sahkan decode) → hantar → tanda brief **FINAL**.
- Seterusnya: skill `tiktok-thumbnail` (thumbnail cover + caption).

## 12. Fail & simpanan
- Repo: `projects/<ID>/` (edit.json, data.js, compose.json, thumb.json, caption.md, thumbnail), `briefs/`.
- Scratchpad: rakaman, base.mov, render, draf (besar — tidak dalam git).
- Aset untuk Drive → zip & hantar kepada Sir (connector tak boleh upload video). Folder Aset ID dalam `CLAUDE.md`.

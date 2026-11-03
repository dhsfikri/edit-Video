# Flow Edit Video TikTok — Talking Head 30 Saat

> Format: **Vertikal 9:16** · **Talking head** · **B-roll** · **Hook title motion graphic** · **Subtitle** · **≤ 30 saat**

---

## 0. Spec Ringkas (set sekali, guna selalu)

| Item | Setting |
|---|---|
| Aspect ratio | 9:16 (1080 x 1920) |
| Frame rate | 30 fps (ikut rakaman asal, jangan campur 25 & 30) |
| Durasi | 25–30 saat (sasaran 28s, bagi ruang loop) |
| Export | 1080p, 30fps, bitrate **Higher** (~15–20 Mbps), H.264 MP4 — lihat Bahagian 5 |
| Safe zone | Elak letak teks kat **bawah 20%** (caption & button TikTok) dan **kanan 15%** (icon like/comment/share). Atas ~10% pun elak (nama akaun / Following-For You) |
| Font subtitle | Bold sans-serif (cth: Montserrat ExtraBold / Poppins Bold), saiz besar, stroke/shadow hitam |

---

## 1. Struktur Video 30 Saat (Timeline)

```
0s ────3s──────────────────────────24s──────28s──30s
│ HOOK │      ISI / VALUE (3 point)    │ CTA   │loop│
```

| Masa | Bahagian | Visual | Teks atas skrin |
|---|---|---|---|
| **0 – 3s** | **HOOK** | Talking head close-up, terus cakap (TAK ADA intro, tak ada "Assalamualaikum semua") | **Hook title motion graphic** + subtitle |
| 3 – 10s | Point 1 / Masalah | Talking head → potong ke **B-roll #1** | Subtitle |
| 10 – 17s | Point 2 / Solusi | B-roll #2 + talking head (punch-in zoom) | Subtitle + keyword highlight |
| 17 – 24s | Point 3 / Bukti | B-roll #3 (testimoni / screenshot WhatsApp / hasil) | Subtitle |
| 24 – 28s | **CTA** | Talking head, pandang kamera | "Komen ___" / "WhatsApp link kat bio" |
| 28 – 30s | Loop | Ayat akhir sambung balik ke ayat hook | — |

**Peraturan emas:** setiap **2–3 saat** mesti ada perubahan visual (cut, zoom, B-roll, teks pop). Tak ada perubahan = orang scroll.

---

## 2. PRA-PRODUKSI (sebelum rakam)

### 2.0 Plan & brief dulu (WAJIB)
Sebelum mula edit, isi **`templates/brief-edit.md`** dan brief Sir Dharma dulu.
**Edit hanya bermula selepas brief di-approve.** Kalau plan berubah masa edit, brief semula.

### 2.1 Tulis skrip (guna `templates/skrip-30s.md`)
- 30 saat ≈ **70–85 patah perkataan** (cakap laju sikit dari biasa).
- Hook mesti salah satu jenis ni:
  - **Masalah**: "Customer tanya harga lepas tu senyap? Ni sebabnya."
  - **Kontra**: "Jangan bagi harga dulu kat WhatsApp."
  - **Nombor**: "3 ayat yang buat customer terus transfer."
  - **Curiosity**: "Ayat ni naikkan closing saya 2x."
- Tulis **2–3 versi hook** — boleh A/B test nanti.

### 2.2 Shot list B-roll
Senaraikan B-roll ikut point dalam skrip. Contoh untuk niche sales WhatsApp:
- Screen record chat WhatsApp (blur nombor/nama customer!)
- Tangan taip kat phone
- Notifikasi "payment received" / screenshot resit (blur info sensitif)
- Produk / packing barang
- Muka customer happy / testimoni

---

## 3. RAKAMAN

| Item | Tips |
|---|---|
| Kamera | Phone kamera belakang, 1080p/4K 30fps, **mode vertikal** |
| Framing | Mata pada 1/3 atas frame, ruang sikit atas kepala. Rakam sedikit longgar — senang buat punch-in zoom |
| Cahaya | Hadap tingkap / ring light depan muka. Elak cahaya dari belakang |
| Audio | Mic clip-on (lavalier). Bilik kecil yang ada langsir/kain kurang echo |
| Delivery | Tenaga 20% lebih dari biasa. Rakam setiap ayat 2–3 kali. **Diam 1 saat** sebelum & lepas setiap take (senang potong) |
| B-roll | Rakam setiap shot 5–8 saat, steady. Lebih baik lebih dari kurang |

---

## 4A. CARA KERJA DENGAN CLAUDE (Claude yang edit)

```
1. Sir bagi topik / skrip  →  2. Claude buat BRIEF  →  3. Sir APPROVE
        ↓
4. Sir rakam & hantar fail  →  5. Claude edit & render DRAF  →  6. Sir semak
        ↓
7. Revisi (kalau ada)  →  8. Claude hantar MP4 FINAL  →  9. Sir upload TikTok
```

### Apa Sir perlu hantar
| Fail | Nota |
|---|---|
| Rakaman talking head (A-roll) | Fail **asal** dari phone (bukan hantar melalui WhatsApp). Boleh hantar semua take — Claude pilih yang terbaik |
| B-roll | Video pendek, screen record, gambar, screenshot (Claude akan blur info sensitif, tapi tolong tandakan apa yang perlu blur) |
| Skrip akhir | Ayat yang Sir cakap — Claude guna untuk subtitle yang tepat |
| Logo (optional) | PNG latar telus |
| Muzik (optional) | Fail lagu yang selamat untuk komersial. Kalau tiada, tambah lagu dari library TikTok masa upload |

**Cara hantar:** upload terus dalam chat ni, ATAU letak dalam satu folder **Google Drive** dan bagi nama folder — Claude ambil dari situ.

### Apa Claude hantar balik
- **Draf** (MP4) untuk Sir semak, bersama nota ringkas apa yang dibuat.
- Lepas Sir approve → **Final MP4** 1080x1920 · 30fps · ~15–20 Mbps, sedia upload.

### Had yang Sir perlu tahu
- Claude tak "nampak" video macam manusia tengok — Claude semak guna frame (gambar) dan data audio. Jadi **semakan Sir pada draf tetap penting**, terutama timing B-roll dan ekspresi muka.
- Subtitle bergantung pada **skrip** yang Sir bagi. Kalau ayat dalam rakaman lain dari skrip, sebut masa hantar fail.
- Motion graphic dibuat dengan teks beranimasi (pop-in, slide, highlight keyword, kotak warna). Effect 3D / animasi kompleks macam After Effects tak termasuk.

## 4. FLOW EDIT (step-by-step)

> **Editor: Claude.** Sir hantar rakaman, Claude edit guna kod (FFmpeg untuk potong/zoom/audio/export, subtitle & hook title beranimasi dirender terus ke video), lepas tu hantar MP4 siap. Lihat **Bahagian 4A** untuk cara kerja dan apa yang Sir perlu hantar.

### STEP 1 — Setup projek & import
1. New project → ratio **9:16**.
2. Import semua clip talking head + B-roll + logo/aset.
3. Susun folder/nama: `A-roll_take1`, `Broll_chat`, `Broll_produk`...

### STEP 2 — Rough cut talking head (A-roll)
1. Letak semua take talking head kat main track.
2. Pilih take terbaik untuk setiap ayat.
3. **Buang semua senyap, "emm", "aaa", tarik nafas, ulang ayat.** (Claude kesan senyap secara automatik, kemudian semak dengan skrip)
4. Jump cut tak apa — memang style TikTok.
5. Semak durasi: **mesti ≤ 30s**. Lebih? Potong ayat, bukan laju-kan suara.

### STEP 3 — Punch-in zoom (gerak tanpa B-roll)
- Kat setiap jump cut, selang-seli scale **100% → 115–120%**.
- Ayat penting / punchline → zoom lebih rapat (130%) atau slow zoom-in.
- Ni yang buat talking head nampak "hidup".

### STEP 4 — Letak B-roll (overlay track)
1. Letak B-roll atas track kedua, **tutup** talking head (audio suara masih jalan bawah).
2. Durasi setiap B-roll: **1.5 – 3 saat** sahaja.
3. B-roll mesti **match apa yang sedang dicakap** (cakap "chat WhatsApp" → tunjuk chat).
4. Jangan tutup muka masa hook (0–3s) dan CTA — orang perlu nampak muka untuk trust.
5. Pilihan style: full screen, atau **split screen** (B-roll atas, muka bawah), atau picture-in-picture.

### STEP 5 — Hook title motion graphic (0–3s)
1. Teks hook: **maks 6–8 patah perkataan**, 2 baris.
2. Posisi: tengah-atas (dalam safe zone), jangan tutup muka.
3. Animasi masuk: **pop / scale-in / typewriter**, 0.2–0.4s. Keluar: fade/cut kat ~3s (atau kekal kecil kat atas sepanjang video sebagai "title bar").
4. Highlight **1 keyword** dengan warna lain (cth: kuning/hijau) atau box belakang teks.
5. Tambah **SFX "whoosh / pop"** sync dengan teks masuk.
6. Optional: emoji / arrow / ikon kecil beranimasi untuk tarik mata.

Contoh:
```
  CUSTOMER "SEEN" JE?
  ➜ Buat [3 BENDA] ni 🔥
```

### STEP 6 — Subtitle
1. Teks subtitle diambil dari **skrip yang Sir approve** dalam brief, kemudian dipadankan dengan masa suara dalam rakaman.
2. **Semak setiap perkataan** — kalau Sir tukar ayat masa rakam (ad-lib), Claude betulkan ikut apa yang betul-betul dicakap.
3. Format:
   - **1–4 patah perkataan** sebaris (bukan ayat panjang)
   - Font bold, putih + stroke hitam
   - Posisi: **tengah skrin, sedikit bawah muka** (atas safe zone bawah)
   - Highlight keyword warna lain / animasi word-by-word (karaoke style)
4. Pastikan subtitle **tak bertindih** dengan hook title.

### STEP 7 — Audio
| Layer | Level |
|---|---|
| Suara (A-roll) | Utama — sekitar **-6 dB hingga -3 dB** peak. Guna *Enhance voice / Noise reduction* |
| Background music | **-25 hingga -20 dB** (perlahan, jangan lawan suara). Sir bekalkan fail muzik yang selamat untuk komersial, ATAU biarkan kosong dan tambah lagu dari library TikTok masa upload (lihat 5.5) |
| SFX | Whoosh kat transition, pop kat teks masuk, "ding" kat point penting. Jangan lebih |

### STEP 8 — Color & polish
1. Filter ringan / adjust: brightness +, contrast sikit, warmth ikut selera — **samakan warna A-roll & B-roll**.
2. Transition: kebanyakan **hard cut**. Guna zoom/whoosh transition hanya 1–2 kali.
3. Tambah logo/watermark kecil (optional), sudut atas kiri.

### STEP 9 — CTA (24–28s)
- Teks CTA atas skrin + cakap serentak.
- Untuk sales WhatsApp, contoh:
  - "Komen **'NAK'**, saya DM skrip penuh"
  - "Klik link WhatsApp kat bio"
  - "Follow untuk part 2"

### STEP 10 — Loop ending
- Ayat terakhir sambung balik ke hook, contoh: hook = "Kenapa customer senyap lepas tanya harga?" → ending = "...dan sebab tu lah customer senyap lepas tanya harga."
- Potong tepat, **tak ada outro / fade to black**. Ini naikkan watch time (orang tengok 2x).

### STEP 11 — QC & export
1. Tengok full video **kat phone**, dengan & tanpa bunyi (`templates/checklist-qc.md`).
2. Export: **1080p · 30fps · bitrate Higher (~15–20 Mbps) · MP4**. Detail kualiti: lihat Bahagian 5.
3. Nama fail: `YYYYMMDD_topik_hookA.mp4`.

### STEP 12 — Upload TikTok
- Caption: ulang hook + 3–5 hashtag relevan (#tipsniaga #closingsales #whatsappmarketing #bisnesonline).
- Cover: frame hook (muka + hook title).
- Post masa audience aktif (semak TikTok Analytics).
- Lepas 24–48 jam semak: **retention 3 saat pertama** & **average watch time**. Hook lemah → test hook versi B.

---

## 5. KUALITI VIDEO — Pastikan Sharp & Tak Pecah Bila Upload

TikTok akan **compress** setiap video yang diupload. Kalau fail asal dah lemah, lepas compress jadi lagi pecah. Jadi kualiti kena jaga dari rakaman sampai upload.

### 5.1 Masa rakam
| Setting | Buat macam ni |
|---|---|
| Resolusi | **4K 30fps** (paling baik) atau minimum 1080p 30fps |
| HDR | **OFF** (iPhone: Settings → Camera → Record Video → HDR Video OFF). HDR selalu jadi pudar/pelik lepas upload |
| Kamera | Kamera **belakang**, lensa utama (1x). Jangan guna digital zoom |
| Lensa | **Lap lensa** sebelum rakam (cap jari = video kabur) |
| Fokus & exposure | Tekan lama kat muka untuk **lock AE/AF** supaya tak berubah-ubah |
| Cahaya | Mesti terang. Bilik gelap = noise/grain = paling cepat pecah lepas compress |
| Stabil | Guna tripod. Video bergoyang = lebih banyak blok pecah |

### 5.2 Pindah fail
- ❌ **JANGAN hantar video melalui WhatsApp/Telegram biasa.** WhatsApp compress teruk.
- ✅ Guna kabel, AirDrop, Google Drive, atau WhatsApp **"Document"** (hantar sebagai fail, bukan video).
- B-roll / screen record pun sama: guna fail asal.

### 5.3 Masa edit
| Perkara | Buat macam ni |
|---|---|
| Project | 9:16, **1080x1920**, frame rate sama dengan rakaman (30fps) |
| Punch-in zoom | Rakaman 1080p → zoom maksimum **~120%**. Rakaman 4K → boleh zoom sampai 200% tanpa kabur |
| Gambar / screenshot | Guna resolusi asal. Jangan besarkan gambar kecil (contoh: screenshot yang di-crop sikit lepas tu besarkan) |
| Screen record chat | Rakam terus kat phone (resolusi penuh), jangan rakam skrin guna phone lain |
| Filter / effect | Jangan tambah grain, noise, atau sharpen berlebihan. Effect "glitch/blur" banyak buat compress jadi pecah |
| Export berulang | Jangan export → import → export lagi. Setiap kali export, kualiti turun. Edit semua dalam satu projek |

### 5.4 Setting export (Claude render guna FFmpeg)
| Setting | Nilai |
|---|---|
| Resolution | **1080p** |
| Frame rate | **30fps** (ikut rakaman) |
| Bitrate | **~15–20 Mbps** (H.264 High profile, CRF rendah) |
| Format | MP4 (H.264 + AAC 320kbps, `+faststart`) |
| Saiz fail | Video 30s biasanya ~40–70 MB. Kalau bawah 15 MB, bitrate terlalu rendah |

> Nota: Export 2K/4K tak semestinya lebih sharp sebab TikTok akan turunkan ke 1080p juga. **1080p + bitrate tinggi** biasanya hasil paling konsisten.

### 5.5 Masa upload TikTok
1. **Matikan Data Saver**: Profile → ☰ → Settings → Data Saver → OFF.
2. Masa post: **More options → "Allow high-quality uploads" / "Upload HD" → ON** (nama menu boleh berubah ikut versi app).
3. Upload guna **WiFi yang laju**, bukan data lemah.
4. Upload dari **app TikTok terus** (atau TikTok Studio desktop). Jangan upload melalui app pihak ketiga yang compress semula.
5. Jangan guna editor dalam TikTok untuk tambah teks/effect lagi, sebab TikTok akan render semula. Semua teks dah siap dalam video yang Claude render. (Tambah lagu dari library TikTok tak apa.)

### 5.6 Semak lepas upload
- Tunggu 5–10 minit (TikTok process versi HD dulu, mula-mula memang nampak kabur sikit).
- Tengok kat phone lain / akaun lain. Kalau masih pecah, semak balik: cahaya rakaman, bitrate export, dan cara pindah fail.

---

## 6. Ringkasan Flow (1 muka)

```
PLAN & BRIEF → tunggu approval Sir Dharma
   ↓
SKRIP (hook + 3 point + CTA, ≤85 patah)
   ↓
RAKAM (A-roll talking head + B-roll ikut shot list)
   ↓
ROUGH CUT (buang senyap & salah, ≤30s)
   ↓
PUNCH-IN ZOOM (setiap jump cut)
   ↓
B-ROLL OVERLAY (1.5–3s setiap satu, match ayat)
   ↓
HOOK TITLE MOTION GRAPHIC (0–3s, pop-in + SFX)
   ↓
SUBTITLE (auto → semak → style bold 1–4 patah)
   ↓
AUDIO (suara jelas, muzik perlahan, SFX)
   ↓
COLOR + CTA + LOOP ENDING
   ↓
QC KAT PHONE → EXPORT 1080p 30fps bitrate tinggi
   ↓
UPLOAD (WiFi, Data Saver OFF, HD upload ON)
```

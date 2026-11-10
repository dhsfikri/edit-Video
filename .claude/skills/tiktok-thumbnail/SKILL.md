---
name: tiktok-thumbnail
description: Buat thumbnail TikTok gaya COVER (standard brand kit Sir Dharma) dan caption panjang untuk video @sirdharma_. Guna selepas video final, atau bila Sir minta thumbnail/cover/caption.
---

# Skill: Thumbnail Cover + Caption — Sir Dharma

**Versi:** 1.0 (2026-11-04)
**Changelog:**
- 1.0 — Gaya cover diluluskan Sir (band hijau gelap, headline Anton penuh lebar, 1 keyword kuning, muka besar, 1 callout).

> Rujukan: `BRANDKIT.md` §6. Brief konsep ringkas kepada Sir dulu (teks headline, frame, callout) — tunggu approval.

## A. Thumbnail
**Template:** `motion/thumbnail-std/` (`index.html` + `render.cjs`). Frame disimpan dalam `motion/thumbnail-std/frames/` (gitignore).

### 1. Pilih frame
```bash
T="0.3 0.9 2.6 4.5 6.1"; for t in $T; do ffmpeg -v error -y -ss $t -i base.mov -frames:v 1 \
  -vf "scale=200:-1,drawtext=text='$t':fontcolor=yellow:fontsize=22:x=6:y=6:box=1:boxcolor=black" c_$t.png; done
ffmpeg -v error -y $(for t in $T; do echo -i c_$t.png; done) -filter_complex hstack=5 cands.png
```
- Pilih **ekspresi kuat** (frust/terkejut/serius), mata terbuka, tangan bergerak bagus. Zoom masuk untuk lihat mata.
- Ambil frame penuh: `ffmpeg -ss <t> -i base.mov -frames:v 1 motion/thumbnail-std/frames/<ID>.png`
- Cari pusat muka (fx, fy) dalam frame (OpenCV atau anggar dari gambar).

### 2. Config `projects/<ID>/thumb.json`
```json
{"photo":"frames/<ID>.png","fx":560,"fy":1080,"scale":1.25,"faceY":1290,
 "series":"AYAT CLOSING","episode":"02","kicker":"kenapa orang",
 "line1":"TAK DENGAR","line2":"CAKAP [AWAK?]",
 "callout":{"kind":"no","text":"tak minta order"}}
```
- `line1`/`line2`: **2–3 perkataan sebaris**, huruf besar. Setiap baris dibesarkan automatik sampai penuh lebar.
- **Satu** `[keyword]` (kotak kuning).
- `kicker`: tulisan tangan pendek (boleh kosong).
- `callout.kind`: `ok` (✓ hijau) atau `no` (✕ hitam).
- **Syot rapat** (muka dah tinggi dalam frame): tambah `"allowDown": true` supaya gambar boleh turun ke `faceY`; anjak muka ke kiri (besarkan `fx`) supaya callout (kanan, y 1320) tak tutup mata. Cari muka dengan OpenCV, jangan anggar.
- `scale`/`faceY`: muka besar, pusat ~y 1290. Rakaman lebar (orang kecil) → `scale` 1.5–1.6 (akan sedikit lembut).

### 3. Render & semak
```bash
cd motion/thumbnail-std && NODE_PATH=$(npm root -g) node render.cjs ../../projects/<ID>/thumb.json <out.png>
# Pratonton grid profil (3:4 + views)
ffmpeg -v error -y -i <out.png> -vf "crop=1080:1440:0:240,scale=300:400,drawtext=text='▷ 294':fontcolor=white:fontsize=22:x=10:y=368:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" grid.png
```
Semak: teks dalam y 290–1450 & x ≤ 1010 · mata tak tertutup tajuk · keyword tak terkeluar · bawah kiri kosong (▷ views).
Perangkap: font mesti dimuat sebelum ukur (`document.fonts.load` — dah dalam template). Jangan `import` ESM dengan NODE_PATH — guna `render.cjs`.

### 4. Hantar
Simpan `projects/<ID>/thumbnail.png`, hantar kepada Sir (`SendUserFile`, render) + pratonton grid.
Cara guna: TikTok → **Edit cover → Upload from gallery**.

## B. Caption panjang
Simpan `projects/<ID>/caption.md`. Struktur:
1. **Baris 1 = hook** (sama dengan video) + emoji — inilah yang nampak sebelum "more".
2. Situasi yang Sir & penonton kenal (2–3 baris pendek).
3. Punca / poin utama — senarai ❌ atau ✅.
4. Nilai tambah yang **tiada dalam video** (satu ayat refleksi/soalan).
5. CTA: `Komen "<KATA>"` (sama dengan CTA video) · Save & share · `Follow @sirdharma_ untuk lagi tips closing 🔔`
6. 8–10 hashtag: campur luas (#bisnesonline #jualanonline) + khusus (#ayatclosing #tipsclosing #closingsales #whatsappmarketing #sellermalaysia #usahawanmalaysia ...).

Bahasa Melayu santai Malaysia. Tiada janji hasil tanpa bukti.

## C. Selesai
Commit `projects/<ID>/thumb.json`, `thumbnail.png`, `caption.md` → push.

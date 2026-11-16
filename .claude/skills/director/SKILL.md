---
name: director
description: Pengarah kreatif video TikTok Sir Dharma. WAJIB dijalankan SEBELUM tiktok-edit memotong/render — baca reference dalam Drive & repo, semak pustaka aset (gambar, B-roll, SFX, muzik), hasilkan STORYBOARD VISUAL (gambar frame), dan dapatkan approval Sir. Guna bila Sir minta edit video, ubah konsep/gaya, buat intro/hook baru, atau bila Sir kata "tak suka" pada visual.
---

# Director — Sir Dharma (@sirdharma_)

**Versi:** 1.0 (2026-11-16). Lahir dari kesilapan sesi 2026-11-16: edit tanpa buka reference, tanpa storyboard visual, tanpa pustaka aset → Sir kena ajar semula.

## Peraturan
1. **Jangan reka gaya sendiri.** Gaya datang dari reference Sir. Jika reference tak cukup → tanya Sir, jangan teka.
2. **Storyboard mesti VISUAL** (gambar frame), bukan jadual teks sahaja. Sir tak boleh bayang dari tulisan.
3. **Guna aset sebenar dulu** (Drive Aset → `aset/` repo → stok berlesen). Jangan lukis semula benda yang boleh dimuat turun.
4. Setiap keputusan/komen Sir → terus catat dalam `CLAUDE.md` "Keputusan & Keutamaan Sir".

## Langkah
### 1. Baca reference (setiap sesi, sebelum apa-apa)
- Repo: `CLAUDE.md` (Keputusan & Keutamaan Sir), `BRANDKIT.md`, `docs/rujukan/*/README.md`.
- Drive `Folder Video/Reference & Inspo` (id `1WkXi5i1Pwe425k4kZp-gjJ7koWva0nhj`): `01 Hook`, `02 Gaya Editing`, `03 Thumbnail & Cover`, `04 Idea Konten`. Fail BARU yang belum ada analisis dalam `docs/rujukan/` → muat turun, ambil frame (`ffmpeg ... fps=2,tile`), tulis `docs/rujukan/<nama>/README.md` + simpan frame kecil.
- Gaya aktif sekarang: **Apple Style Motion** → `docs/rujukan/apple-motion/README.md`.

### 2. Semak pustaka aset
| Jenis | Tempat |
|---|---|
| Gambar | `aset/gambar/` (lesen: `aset/gambar/LESEN.md`) · Drive `Aset` |
| B-roll video | Drive `Aset/02 B-Roll` (id `1DI7CBy7abVmU4Kj0brD94chd5jXwTDDI`) · stok berlesen (skill `cari-aset`) |
| SFX | Drive `Aset/05 SFX` (id `1AhUahjvZgEOKhm1Pf1BC6Faj5ylIasKv`) · `motion/sfx/` |
| Muzik | Drive `Aset/06 Muzik` (id `1dTkEF8cMVYXLo9HkF3Jop94-k951nXwe`) |
| Material (chat, bukti, skrip) | Drive `Folder Video/Material` (id `1ZqG_d_rPEAygS5_N_vtjalDfJdoFHdCX`) |
Aset kurang → cari stok berlesen komersial (Openverse/Wikimedia/Flickr CC, Pexels jika ada key), simpan dalam `aset/` + catat lesen. Folder Drive kosong → beritahu Sir.

### 3. Storyboard visual
- Pecah video ikut ayat (masa dari transkrip). Setiap babak: masa, ayat, komponen/visual, gerakan, aset, SFX.
- **Hasilkan gambar frame** (mock HTML → screenshot Playwright, atau `npx hyperframes snapshot`) menggunakan still sebenar dari rakaman + aset sebenar. Gabung jadi satu helaian `briefs/<tarikh>_<ID>_storyboard.png`.
- Hantar helaian kepada Sir (SendUserFile). Tunggu pilihan/approval.

### 4. Serah kepada `tiktok-edit`
Selepas approve: koreografi dalam `projects/<ID>/scene.js` (template `motion/dynamic/`), teks dalam `motion/overlay-dyn/`. Render **sampel pendek** dulu untuk babak baru/berisiko.

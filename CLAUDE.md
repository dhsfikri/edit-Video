# Peraturan Projek (untuk Claude / editor)

## Skill (ikut langkah dalam skill)
- **`tiktok-edit`** (`.claude/skills/tiktok-edit/SKILL.md`) — edit video dari rakaman Raw sampai final.
- **`tiktok-thumbnail`** (`.claude/skills/tiktok-thumbnail/SKILL.md`) — thumbnail cover + caption.
- Skill boleh dikemas kini: naikkan nombor versi + changelog. Perubahan besar (gaya/urutan/peraturan) → brief Sir dulu; pembetulan teknikal kecil → terus kemas kini & maklumkan.

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
- TikTok: @sirdharma_
- Warna: hijau #25D366, hitam #0B0B0B, putih, keyword kuning #FFD60A
- Font: Montserrat ExtraBold/SemiBold (video), Anton (headline thumbnail), Caveat (tulisan tangan)
- Intro: badge siri + tajuk hook + bunyi signature, TANPA intro berasingan (Sir bercakap dari saat 0)
- Siri juga: "TIPS JUALAN #NN" (jualan umum / TikTok Shop)

## Google Drive (pustaka aset)
- `Folder Video` (id 1K3AzhqGOV5IhaRmOGf5TpdDUz4xZzx1g) → `Raw` (rakaman mentah, id 1U4zM7ykx7C97n6ZbkILKLw8fK_x_N3KB)
- `Folder Video/Aset` (id 1BvpjU99Can-NpRC2qbW4_pzIRQbdShGq):
  - `01 Intro` (1LAPSkDfYMTDljeh9k2dsTFtIVBeSuwwD) · `02 B-Roll` (1DI7CBy7abVmU4Kj0brD94chd5jXwTDDI)
  - `03 Outro` (19Zucgqv_279GQ27CzY7muqMQ3-tZElWy) · `04 Iklan 2s` (1ZFuMen20VBMqrRmI5WncmWC9TgFwLM9r)
  - `05 SFX` (1AhUahjvZgEOKhm1Pf1BC6Faj5ylIasKv) · `06 Muzik` (1dTkEF8cMVYXLo9HkF3Jop94-k951nXwe)
- `Folder Video/Material` (id 1ZqG_d_rPEAygS5_N_vtjalDfJdoFHdCX) — bahan khusus per video dari Sir:
  - `01 Screenshot Chat` (1CDqlCWNpp3c3G_t15nP2Fs4hBOXLF1zF) · `02 Bukti & Testimoni` (1qtLaKQaEuNl5Jp6mB8mG7cap6F6PEYxH)
  - `03 Skrip & Bank Ayat` (125WjwLwMoxc0FEZ2MR_9yc65MnpNqDAK) · `04 Rujukan Video` (1WkXi5i1Pwe425k4kZp-gjJ7koWva0nhj)
- `Folder Video/Edited` (id 1XQvZGEOJpoDoe7yKeQRwAq5hvACET_QN) — DRAF untuk semakan Sir (subfolder `<SIRI-NN>_<Tajuk>`)
- `Folder Video/Final` (id 1dQgYEcrcn6DawR362tiVy714YWMZKLtR) — video LULUS + thumbnail + caption (subfolder per episod)
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

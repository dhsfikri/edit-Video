---
name: hook-lab
description: Reka hook 0–3 saat yang engaging untuk video TikTok Sir Dharma dengan menggabungkan STORYTELLING (kenapa orang nak tahu) + IDEA VISUAL KREATIF (apa yang buat orang berhenti scroll) + TREND semasa. Hasilkan 3 pilihan hook lengkap (ayat, teks skrin, visual/motion, storyboard 3 frame) untuk Sir pilih. Guna setiap kali brief video baru atau bila Sir kata hook lemah / tak engaging.
---

# Hook Lab — Sir Dharma

**Versi 1.0 (2026-11-17).** Peraturan Sir: hook = storytelling + idea kreatif. Bukan salah satu.

## Input
- Transkrip video (`projects/<ID>/transcript.json`) — ayat Sir yang SEBENAR (hook mesti guna suara Sir; boleh susun semula ayat, jangan reka ayat yang Sir tak cakap).
- `docs/trend/<tarikh terkini>.md` (skill `riset-trend`) · `docs/bank-idea-motion.md` (jika ada) · gaya aktif dalam `CLAUDE.md`.

## 1. Lapisan STORYTELLING — pilih 1 jenis ketegangan
| Jenis | Rupa | Contoh untuk niche Sir |
|---|---|---|
| **Soalan sakit** | Sebut masalah yang penonton rasa | "Customer baca je, tak balas?" |
| **Lawan kebiasaan** | Cabar apa orang percaya | "Diskaun bukan sebab orang beli." |
| **Mula di tengah cerita** | Masuk terus ke momen | "Dia dah nak bayar… lepas tu senyap." |
| **Kos / akibat** | Tunjuk kerugian | "Satu ayat ni hilangkan RM3,000 sebulan." *(hanya jika ada bukti — tiada janji hasil)* |
| **Teaser hasil** | Tunjuk penghujung dulu | Flash-forward: chat "✓ Dah bayar" → "macam mana?" |
| **Identiti** | Panggil kumpulan | "Seller TikTok Shop, dengar ni." |
Sumber kerangka: `social-media-skills:hook-writer`, `storytelling-and-narrative`, `viral-reverse-engineering`.

## 2. Lapisan IDEA KREATIF — padankan dengan metafora visual
- Cari **benda boleh nampak** untuk konsep abstrak (percaya → gembok/jambatan; banyak cakap → gelembung melimpah; follow up → kalendar/notifikasi; closing → butang "Hantar" → "✓ Bayar").
- Pilih **1 gerakan utama** sahaja dalam 3 saat (skill `motion-art-direction`: hierarki & kekangan): pop-out muka Sir, kad 3D flip, UI morph, kolaj kertas, kaunter nombor, freeze-frame, pembuka 3D (`title-sequence-3d`).
- Muka Sir kelihatan dalam frame pertama (kecuali konsep teaser yang Sir setuju).

## 3. Lapisan TREND (jika ada yang lulus tapisan)
Sambung kepada kempen/format semasa (contoh 11.11, LIVE selling, #JomLokal) — dalam teks skrin atau contoh, bukan paksa.

## 4. Output: 3 pilihan, setiap satu
| Medan | Isi |
|---|---|
| Jenis cerita + trend | contoh "Soalan sakit + 11.11" |
| Ayat dicakap | dari transkrip (masa raw) |
| Teks skrin | ≤ 6 patah, font brand |
| Visual / motion | metafora + 1 gerakan utama + alat (EffectCraft/HyperFrames/VectorCraft) |
| Storyboard | 3 frame (0s, 1.5s, 3s) — gambar, ikut skill `director` |
| Kenapa engaging | 1 ayat |
Tandakan satu **(Cadangan)**. Sir pilih → masuk brief → `tiktok-edit`.

## QC hook
Faham tanpa bunyi? · Ada sebab nak tengok saat ke-4? · Muka Sir/jenama jelas? · Teks dalam safe zone? · Tiada emoji, tiada janji hasil tanpa bukti?

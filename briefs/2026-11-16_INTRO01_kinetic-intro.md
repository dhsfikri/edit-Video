# Brief Edit: INTRO01, video pengenalan "Kinetic Intro" (gaya rujukan)

**Tarikh:** 2026-11-16 · **Versi brief:** v1
**Status:** ☐ Menunggu approval  ☐ Approved  ☐ Perlu ubah
> Sir minta "plan dan terus bagi 1 draf", jadi draf v1 dibuat terus ikut brief ni.

## 0. Analisis video rujukan (`Turn_Attention_Into_Action_shorts.mp4`)
| Item | Dapatan |
|---|---|
| Spec | 1080x1920, 30fps, 19.7s, tiada orang bercakap (muzik + SFX sahaja) |
| Struktur | 7 babak, setiap satu ±2.5s, 1 idea sebaris. Hook headline terus di saat 0, logo reveal di hujung |
| Tipografi | Gabung 2 font: **condensed tebal huruf besar** (YOU DON'T) + **serif italic** untuk kata emosi (*need*, *attention*). Perkataan masuk satu-satu, ada yang ditaip |
| Highlight | Kotak warna yang "ditaip" di belakang perkataan (EVERYONE TO NOTICE YOU, *doesn't reach everyone*) |
| Visual | Imej simbolik (helmet, otak, mata, patung) + babak abstrak (partikel, bulatan orbit, garisan melengkung ke titik) |
| Klimaks | Bulatan merah membesar jadi skrin merah penuh, **ACTION** gergasi (saat ±12) |
| Warna | Hitam + merah + krim kertas. Satu warna aksen sahaja, jadi nampak premium |
| Penutup | Nama jenama muncul huruf demi huruf + garisan bawah + glow |

**Kenapa berkesan:** ayat dipecah jadi cebisan pendek, mata sentiasa ada benda baru, dan ada "letupan" warna penuh di tengah video.

## 1. Objektif
- Video **pengenalan** @sirdharma_: siapa Sir dan apa yang Sir ajar (closing WhatsApp)
- Sasaran: seller / usahawan / team sales yang ramai lead tapi kurang closing
- CTA: follow @sirdharma_

## 2. Konsep & gaya
- Gaya **F. Cinematic** + kinetic typography (tiru struktur rujukan, tukar ke brand kit kita)
- Merah rujukan → **hijau #25D366**. Keyword → **kuning #FFD60A**. Serif italic → **Caveat** (tulisan tangan brand). Condensed → **Anton**. Teks kecil → **Montserrat**
- Imej simbolik rujukan → **mockup chat generik** (tiada logo/rupa WhatsApp sebenar)

## 3. Hook (headline, tanpa salam)
- Atas skrin: **KAU TAK PERLU** *lebih ramai* **[LEAD UNTUK CLOSING]**
- Animasi: perkataan hentak masuk, Caveat ditulis, kotak hijau "ditaip" + SFX whoosh

## 4. Timeline (±21s)
| Masa | Teks | Visual | SFX |
|---|---|---|---|
| 0–3.0 | KAU TAK PERLU *lebih ramai* [LEAD UNTUK CLOSING] | Gelembung chat "Berapa harga?" banjir dari bawah | whoosh + taip |
| 3.0–5.6 | *Faham* cara customer **berfikir** | Gelembung chat bercahaya + orbit: YAKIN · PERCAYA · SEGERA | hit |
| 5.6–8.2 | KENAPA DIA *seen…* [TERUS SENYAP] | Flash putih → mockup chat: harga dihantar → ✓✓ → "…" | whoosh |
| 8.2–11.5 | Tukar *"seen"* tu → JADI → **CLOSING** | Partikel → bulatan hijau → skrin hijau penuh | riser + boom |
| 11.5–15.0 | " Customer tak beli produk. **[Dia beli rasa yakin.]** | Latar kertas krim, teks ditaip | taip |
| 15.0–17.6 | satu ayat / *boleh ubah satu sale* | Grid titik, garisan hijau melengkung ke titik sasaran | swoosh |
| 17.6–21.0 | **DHARMA** · Sales Guru · @sirdharma_ · pil siri | Logo reveal + garisan + glow | bunyi signature |

## 5. Style & audio
- Latar hitam #0B0B0B / kertas krim (babak 5), skrin hijau penuh (klimaks)
- Audio: bed bass + SFX disintesis sendiri (bebas hak cipta) + `signature.wav`. Sir boleh tukar ke trending sound dalam TikTok

## 6. Aset
- Semua grafik dibina dalam kod: `motion/intro-kinetic/`. Tiada rakaman diperlukan

## 7. Export
- 1080x1920 · 30fps · H.264 ~16 Mbps · AAC · +faststart · QC safe zone

## 8. Soalan untuk Sir
1. Nak guna **"kau"** atau **"awak"**? (draf guna "kau", lebih padu untuk hook)
2. Nak masukkan **muka Sir** (klip pendek) dalam babak 7? Kalau ya, hantar rakaman ±3s
3. Nama di logo: "DHARMA · Sales Guru" ok?

---
## Draf v2 (2026-11-16): tambah potret studio Sir
Sumber: Drive `Website Sales - Testimoni / 05 Potret Sir Dharma (Studio 2024)`
| Babak | Potret | Kenapa |
|---|---|---|
| 1 Hook | IMG_0244 (tunjuk ke kamera) → `p_tunjuk.jpg` | "KAU TAK PERLU…" terus tunjuk penonton |
| 2 Faham | IMG_0247 (isyarat OK di mata) → `p_ok.jpg` | Ganti shot "mata" dalam rujukan; label YAKIN/PERCAYA/SEGERA sekeliling |
| 3 Senyap | IMG_0248 (isyarat diam) → `p_senyap.jpg` | Masuk tepat bila keluar "TERUS SENYAP?" (selepas mockup chat) |
| 7 Logo | IMG_0239 (tangan di dada) → `p_dada.jpg` | Wajah Sir di atas nama DHARMA |
Gelembung chat babak 1 dibuang (diganti potret, lebih bersih macam rujukan).

---
## Draf v3 (2026-11-16): ikut struktur rujukan + collage cut-out
Sir minta ikut rujukan dengan rapat, dan cut terus gaya collage. Gambar Sir dipotong dari latar (rembg `u2net_human_seg`).
| Masa | Rujukan | Versi kita |
|---|---|---|
| 0–2.8 | Helmet + YOU DON'T NEED + kotak ditaip | Cut-out Sir **tunjuk** + KAU TAK PERLU *lebih ramai* [LEAD UNTUK CLOSING] |
| 2.8–5.0 | Otak emas + orbit label + *Rewire* | Orb chat hijau + orbit YAKIN/PERCAYA/SEGERA + *Faham* cara customer **berfikir** |
| 5.0–6.6 | Flash → orang intai di sebalik langsir + UNDERSTAND WHAT CAPTURES | Flash → cut-out Sir **shh** di celah langsir hijau + KENAPA DIA [SENYAP?] |
| 6.6–7.8 | Makro mata + *their* ATTENTION | Makro gelembung chat kabur + ✓✓ Seen + *dia dah baca...* TAPI TAK BALAS |
| 7.8–10.2 | Kertas + bingkai emas patung + bunga | Kertas + **bingkai hijau-kuning potret Sir** + selotep + sticker chat (ganti bunga) + *Cakap terus apa yang dia nak* |
| 10.2–13.5 | Partikel → bulatan merah → ACTION | Partikel → bulatan hijau → **CLOSING** |
| 13.5–16.8 | Kertas, petikan ditaip + highlight hitam | " Customer tak beli produk. [Dia beli rasa yakin.] |
| 16.8–19.1 | Grid titik + garisan ke titik merah | satu ayat *boleh ubah satu sale* |
| 19.1–21.5 | Logo Velkine | **DHARMA** · SALES GURU · @sirdharma_ |
Nota: teks kabur besar di babak makro sengaja keluar tepi (latar grafik, macam shot mata dalam rujukan), bukan teks utama.

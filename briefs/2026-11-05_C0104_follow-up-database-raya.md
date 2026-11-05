# Brief Edit — C0104 "Raya dah dekat, plan naikkan sale?" (TIPS JUALAN #02)

**Fail asal:** `Folder Video/Raw/C0104.MP4` · **Versi brief:** v1 · **Tarikh:** 2026-11-05
**Status:** ☐ Menunggu approval  ☑ Approved (Sir: "finalize dan rendered") · **FINAL**

## 0. Spec
| Item | Nilai | Tindakan |
|---|---|---|
| Resolusi | 1920x1080 baring (kepala kiri) | `rotate: cw` → 1080x1920 |
| FPS | 50 | Kekal 50 |
| Durasi | 32.6s | Jadi 25.0s |
| Muka | Dekat kamera, tinggi dalam frame | Tajuk di atas baju (`titleY` 880) |

## 1. Objektif
- Siri **TIPS JUALAN #02** (jualan umum, musim raya)
- Mesej: tak semua produk laku masa raya → follow up database, tanya dulu apa customer perlukan
- CTA: **komen "PART 2"** (cara simpan database) + follow

## 2. Gaya: EDITORIAL MAGAZINE (pilihan Sir)
Grade warm + vignette · keyword kuning · tajuk **kad kaca + kinetic typography** · B-roll gaya magazine · wipe hijau→hitam pada B-roll, soft flash pada jump cut · fade-out hujung.

## 3. Timeline (final)
| Masa | Sumber | Ayat | Grafik |
|---|---|---|---|
| 0–1.9 | 0.72–2.63 | Raya kan dah nak dekat betul tak? | Kad kaca 01: *raya dah dekat,* PLAN NAIKKAN **SALE?** |
| 1.9–5.0 | 3.10–6.23 | Apa plan awak untuk naikkan sale ketika raya nanti? | (kad 01 kekal) |
| 5.0–8.6 | 6.50–10.03 | Kita tahu bila buat raya ni, tak semua produk laku tau | **B-roll produk**: grid 6 produk → ✕ TAK LAKU / ✓ LAKU |
| 8.6–10.1 | 12.89–14.41 | Macam mana nak tukar produk dengan baik? | Bracket fokus |
| 10.1–11.3 | 14.84–16.06 | Kat sini saya nak share satu tips | Kad kaca 02: *satu tips:* FOLLOW UP **DATABASE** |
| 11.3–14.5 | 17.40–20.58 | Korang, tolong follow up balik database | (kad 02 kekal) |
| 14.5–17.5 | 20.58–23.56 | Tanya mereka apa yang mereka perlukan untuk raya ni | **B-roll database**: senarai customer → chat follow up generik |
| 17.5–19.3 | 23.56–25.34 | Nampak tak? | — |
| 19.3–21.3 | 25.43–27.50 | So, kadang-kadang kan database tu sangat penting | Callout ✓ database sangat penting |
| 21.3–25.0 | 27.72–31.34 | Kalau nak tahu cara simpan database, komen part 2, okey? | Kad kaca 03: *nak tahu cara simpan database?* KOMEN **PART 2** · fade-out |

**Dibuang:** "So," pembuka ayat · "mungkin kita tak paksa tukar produk" (maksud kurang jelas, soalan selepasnya cukup sebagai jambatan ke tips).

## 4. QC
Safe zone ✓ (`pipeline/safezone_qc.py`) · Audio -14.9 LUFS, peak -2.3 dB ✓ · 1080x1920 50fps H.264 ~11 Mbps + AAC 320k, faststart ✓
Mockup produk & chat **generik/rekaan** (nama customer contoh sahaja).

## 5. Output
- Video: `20261105_tips-raya-follow-up-database.mp4`
- Thumbnail: `projects/C0104/thumbnail.png` (frame 1.0s, ruang atas dilanjutkan supaya muka turun bawah tajuk)
- Caption: `projects/C0104/caption.md`

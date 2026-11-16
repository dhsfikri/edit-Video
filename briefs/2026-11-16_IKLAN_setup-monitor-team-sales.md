# Brief Edit Video — Iklan Animasi: Setup & Monitor Team Sales

**Tarikh:** 2026-11-16  **Tajuk/Topik:** Iklan servis Setup Team Sales A–Z + Monitoring 30 hari  **Versi brief:** v4 (final selepas soal jawab dengan Sir)

## 1. Objektif
- Tujuan video: **lead**, iaitu tempahan **sesi konsultasi percuma 30 minit (online)**
- Target penonton: **owner company servis** (cth renovation, cleaning, aircond, agensi, takaful, training, perunding) yang **dah ada 2–5 staf** jaga leads WhatsApp (quotation, temujanji), tapi **tiada sistem**: setiap staf kerja ikut cara sendiri.
- Janji utama (tanpa angka hasil): owner dapat **sistem + laporan**, iaitu peranan jelas, skrip & SOP, dan laporan mingguan untuk tahu siapa perform.
- CTA: **"Konsultasi PERCUMA 30 min · Hanya 5 slot sebulan · WhatsApp link di bio"**

## 2. Skop servis (disahkan Sir)
- Client **rekrut staf sendiri**. Sir **tidak** rekrut.
- Sir: susun struktur & peranan team, skrip & SOP closing WhatsApp, monitoring 30 hari dengan laporan.

## 3. Konsep & gaya
- Iklan servis (masalah → solusi → CTA), **100% animasi**, tanpa rakaman muka.
- Gaya: **F. Cinematic + E. Chat Simulation**: iPhone 3D (three.js) + teks kinetik (GSAP), timing ikut prinsip `motion-design`.
- **Prinsip (arahan Sir): setiap teks di skrin mesti ada visual yang menunjukkan benda yang sama, pada masa yang sama.**
- Benang cerita: skrin iPhone tunjuk **group chat "Team Sales"** (mockup generik) dengan 4 staf. Mula-mula kelam-kabut, kemudian disusun langkah demi langkah sampai ada sistem.

## 4. Hook
- Kicker kecil (Caveat, tulisan tangan): *"Untuk company servis"*
- Headline: **"Staf ada, sistem takde?"** ("sistem takde?" warna kuning)
- Visual: iPhone 3D berpusing masuk; group "Team Sales · 4 ahli" penuh mesej bercelaru.
- SFX: whoosh + ding notifikasi berulang

## 5. Plan timeline (15s, tiada suara: teks + muzik)
| Masa | Isi | Visual | Teks / motion graphic | SFX |
|---|---|---|---|---|
| 0–3s | Hook | Group "Team Sales · 4 ahli": *"Lead ni siapa pegang?"* · *"Saya ingat Hafiz dah reply"* · *"Quotation yang mana satu?"*; leads baru masuk tanpa jawapan | kicker *Untuk company servis* · "Staf ada, **sistem takde?**" | whoosh + ding |
| 3–5.5s | Masalah | Notifikasi leads bertimbun: *"Boleh dapat quotation?"*, *"Bila boleh datang survey?"*, kiraan "belum dibalas" naik | "Leads masuk, **tiada siapa follow up**" | ding laju |
| 5.5–7.5s | Solusi 1 | Badge **SETUP TEAM SALES A–Z**; tag peranan melekat pada setiap staf: Aina · *Follow up leads*, Hafiz · *Closer*, Mira · *Quotation*, Danish · *After sales* | ✓ Susun peranan team | pop setiap tag |
| 7.5–9.5s | Solusi 2 | Mesej 📌 disematkan: dokumen "SOP & Skrip Closing WhatsApp" | ✓ Skrip & SOP closing | swoosh |
| 9.5–11.5s | Solusi 3 | Kad laporan mingguan dalam group: setiap staf dengan **quotation dihantar · temujanji · closing** (angka rekaan), "Minggu 1/4" | ✓ **Monitoring 30 hari** + laporan | ding |
| 11.5–14.5s | CTA | Group tersusun & tenang; kad CTA dengan butang hijau berdenyut | **Konsultasi PERCUMA 30 min** · *Hanya 5 slot sebulan* · "WhatsApp link di bio" · @sirdharma_ | hit akhir |
| 14.5–15s | Loop | Fade ke frame hook | — | — |

## 6. Style
- Font: Montserrat ExtraBold/SemiBold; Caveat untuk kicker.
- Warna: hijau #25D366, hitam #0B0B0B, putih; kuning #FFD60A (satu keyword setiap babak: "sistem takde?", "Monitoring 30 hari", "PERCUMA"); merah #FF5A5A hanya untuk lencana "belum dibalas".
- Latar: hitam dengan cahaya hijau lembut. iPhone gaya titanium (tanpa logo).
- **Muzik:** upbeat korporat, **dijana dalam code** (synth asal, rentak sederhana laju), jadi bebas hak cipta sepenuhnya; dicampur -14 LUFS, SFX di atas rentak.
- **Patuh brand kit:** chat mockup generik (tiada logo WhatsApp), **tiada janji hasil**. Laporan hanya tunjuk apa yang dipantau.

## 7. Aset
- Ada: template iPhone 3D (`motion/threejs-test/`), ding.wav, font, warna.
- Akan dibina: muzik synth, SFX whoosh/pop.
- Info sensitif: tiada (semua nama, mesej & angka laporan rekaan).

## 8. Kualiti & export
- 1080x1920 · 30fps · H.264 ~16 Mbps · AAC · +faststart
- QC safe zone (`pipeline/safezone_qc.py`) + loudness sebelum hantar draf.

## 9. Keputusan Sir (soal jawab 2026-11-16)
| Perkara | Keputusan |
|---|---|
| Rekrut | Client ambil sendiri |
| Hasil akhir | Sistem + laporan |
| Target | Company servis, dah ada 2–5 staf |
| CTA | Konsultasi percuma 30 min online |
| Segera | Slot terhad: **5 slot sebulan** |
| Headline | "Staf ada, sistem takde?" |
| Format | 15s + muzik (upbeat korporat) |

---
**Status:** ☑ Menunggu approval  ☐ Approved  ☐ Perlu ubah (nota: ____)

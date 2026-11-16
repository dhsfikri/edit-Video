# Brief Edit Video — Iklan Animasi: Setup & Monitor Team Sales

**Tarikh:** 2026-11-16  **Tajuk/Topik:** Iklan servis Setup Team Sales A–Z + Monitoring 30 hari  **Versi brief:** v1

## 1. Objektif
- Tujuan video: **lead** (owner bisnes DM / WhatsApp untuk tanya servis)
- Target penonton: owner bisnes / ketua team sales yang ada 2–20 orang sales (closer WhatsApp), leads banyak tapi closing tak konsisten
- CTA: **"WhatsApp link di bio"** + @sirdharma_

## 2. Konsep & gaya
- Konsep isi: Iklan servis (masalah → solusi → CTA). Tanpa rakaman muka, **100% animasi**.
- Gaya editing: **F. Cinematic + E. Chat Simulation**
  - iPhone 3D (three.js, dari sampel BEDAH CHAT) sebagai "hero"
  - Teks kinetik GSAP (huruf/perkataan masuk ikut rentak), timing ikut prinsip `motion-design`
- Kenapa: servis ni tentang **team & WhatsApp**. Telefon dengan chat yang tak berjawab terus kena dengan masalah penonton. Gaya 3D bagi rasa "premium" dan sesuai dengan servis berbayar.

## 3. Hook
- Hook title atas skrin (maks 8 patah): **"Team sales ramai, closing sikit?"**
- Animasi hook: perkataan "slam" masuk satu-satu; "closing sikit?" warna kuning, bergegar sedikit. Di bawahnya iPhone 3D penuh notifikasi chat belum dibalas (badge merah "27").
- SFX: whoosh pendek + "ding" notifikasi (`motion/iklan/assets/ding.wav`)
- Hook versi B (A/B test): **"Leads masuk banyak, sales tak jalan?"**

## 4. Plan timeline (15s, tiada suara: teks + muzik)
| Masa | Isi | Visual | Teks / motion graphic | SFX / muzik |
|---|---|---|---|---|
| 0–2.5s | Hook | iPhone 3D masuk berpusing; senarai chat "27 belum dibalas" | "Team sales ramai, **closing sikit?**" | whoosh + ding berulang |
| 2.5–6s | Masalah | Telefon ke tepi, 3 kad masalah masuk satu-satu (✕ merah) | ✕ Leads lambat dibalas · ✕ Tiada skrip & SOP · ✕ Tak tahu siapa perform | "tick" setiap kad |
| 6–11s | Solusi | Badge **SETUP TEAM SALES A–Z**; skrin telefon bertukar jadi papan pantau team (bar prestasi setiap sales, generik) | ✓ Setup team & struktur · ✓ Skrip & SOP closing WhatsApp · ✓ **Monitoring 30 hari** (kuning) | muzik naik, "ding" setiap ✓ |
| 11–14s | CTA | Butang hijau berdenyut | **"WhatsApp link di bio"** · @sirdharma_ | hit akhir |
| 14–15s | Loop | Fade ke frame hook | — | — |

## 5. Style
- Font: Montserrat ExtraBold/SemiBold. Warna: hijau #25D366, hitam #0B0B0B, putih, kuning #FFD60A (satu keyword sahaja: "Monitoring 30 hari"), merah #FF5A5A untuk ✕ sahaja.
- Latar: hitam dengan cahaya hijau lembut (sama macam sampel iPhone).
- Muzik: upbeat korporat moden, bebas royalti (perlu pilih; atau Sir guna sound TikTok masa upload).
- **Patuh brand kit:** chat mockup generik (tiada logo WhatsApp), **tiada janji hasil** (cth "sales naik 2x").

## 6. Aset
- Ada: template iPhone 3D (`motion/threejs-test/`), ding.wav, font, warna, salinan iklan 4s sedia ada (`motion/iklan/`).
- Masih perlu: muzik latar (atau tanpa muzik, Sir letak sound masa upload).
- Info sensitif: tiada (nama dalam chat & papan pantau rekaan).

## 7. Kualiti & export
- 1080x1920 · 30fps · H.264 ~16 Mbps · AAC · +faststart
- QC safe zone (`pipeline/safezone_qc.py`) sebelum hantar draf.

## 8. Soalan / perkara untuk Sir putuskan
1. **Format:** iklan 15s berasingan (post sendiri / TikTok Ads) **atau** ganti iklan 4s yang disisip dalam video? (Cadangan: buat 15s dulu, kemudian potong versi 4s daripadanya.)
2. **Tawaran / harga:** nak tunjuk harga atau tawaran (cth slot terhad bulan ni)? Atau kekal tanpa harga?
3. **Butiran servis:** checklist 3 perkara di atas betul? Ada yang nak tambah (cth latihan team, KPI mingguan, laporan)?
4. **CTA:** "WhatsApp link di bio" ok, atau nak "DM 'TEAM'"?
5. **Muzik:** saya pilih muzik bebas royalti, atau tanpa muzik (Sir letak sound TikTok sendiri)?

---
**Status:** ☑ Menunggu approval  ☐ Approved  ☐ Perlu ubah (nota: ____)

# Brief Edit Video — Iklan Animasi: Setup & Monitor Team Sales

**Tarikh:** 2026-11-16  **Tajuk/Topik:** Iklan servis Setup Team Sales A–Z + Monitoring 30 hari  **Versi brief:** v2 (headline baru dari Sir; visual ikut teks)

## 1. Objektif
- Tujuan video: **lead** (owner bisnes DM / WhatsApp untuk tanya servis)
- Target penonton: owner bisnes yang **kali pertama nak bina team sales** (closer WhatsApp), belum ada sistem, tak tahu nak mula dari mana
- CTA: **"WhatsApp link di bio"** + @sirdharma_

## 2. Konsep & gaya
- Konsep isi: Iklan servis (masalah → solusi → CTA). Tanpa rakaman muka, **100% animasi**.
- Gaya editing: **F. Cinematic + E. Chat Simulation**
  - iPhone 3D (three.js, dari sampel BEDAH CHAT) sebagai "hero"
  - Teks kinetik GSAP (huruf/perkataan masuk ikut rentak), timing ikut prinsip `motion-design`
- **Prinsip v2 (arahan Sir): setiap teks di skrin mesti ada visual yang menunjukkan benda yang sama, pada masa yang sama.**
- Benang cerita: skrin iPhone tunjuk **group chat "Team Sales"** (mockup generik). Mula-mula kosong (1 ahli, owner seorang), kemudian dibina langkah demi langkah sampai lengkap.

## 3. Hook
- Hook title atas skrin: **"First time setup team sales?"** ("team sales" warna kuning)
- Visual hook: iPhone 3D berpusing masuk; skrin tunjuk group baru **"Team Sales · 1 ahli"** yang kosong, cuma mesej sistem "Anda mencipta group ini".
- SFX: whoosh pendek + "pop" bila group dibuka

## 4. Plan timeline (15s, tiada suara: teks + muzik)
| Masa | Isi | Visual | Teks / motion graphic | SFX / muzik |
|---|---|---|---|---|
| 0–2.5s | Hook | Group "Team Sales · 1 ahli", kosong | "**First time** setup **team sales?**" | whoosh + pop |
| 2.5–6s | Masalah | 3 soalan muncul satu-satu sebagai mesej owner dalam group (tiada siapa jawab, "dibaca" sahaja) | "Tak tahu nak mula dari mana?" · bubble: *Nak ambil berapa orang?* · *Nak bagi skrip apa?* · *Macam mana nak pantau?* | "ding" setiap bubble |
| 6–8s | Solusi 1 | Ahli masuk satu-satu: "Aina menyertai", "Hafiz menyertai", "Mira menyertai"; kiraan ahli naik 1 → 4 | Badge **SETUP TEAM SALES A–Z** · ✓ Bina team & struktur | pop setiap ahli |
| 8–9.5s | Solusi 2 | Mesej disematkan (📌) muncul: dokumen "SOP & Skrip Closing WhatsApp" | ✓ Skrip & SOP closing | swoosh |
| 9.5–11s | Solusi 3 | Kad laporan mingguan dalam group: bar prestasi setiap ahli + "Minggu 1/4" | ✓ **Monitoring 30 hari** (kuning) | ding |
| 11–14s | CTA | Group lengkap & aktif; butang hijau berdenyut di bawah telefon | **"WhatsApp link di bio"** · @sirdharma_ | hit akhir |
| 14–15s | Loop | Fade ke frame hook | — | — |

## 5. Style
- Font: Montserrat ExtraBold/SemiBold. Warna: hijau #25D366, hitam #0B0B0B, putih, kuning #FFD60A (satu keyword setiap babak: "team sales" masa hook, "Monitoring 30 hari" masa solusi), merah #FF5A5A untuk ✕ sahaja.
- Latar: hitam dengan cahaya hijau lembut (sama macam sampel iPhone).
- Muzik: upbeat korporat moden, bebas royalti (perlu pilih; atau Sir guna sound TikTok masa upload).
- **Patuh brand kit:** chat mockup generik (tiada logo WhatsApp), **tiada janji hasil** (cth "sales naik 2x").

## 6. Aset
- Ada: template iPhone 3D (`motion/threejs-test/`), ding.wav, font, warna, salinan iklan 4s sedia ada (`motion/iklan/`).
- Masih perlu: muzik latar (atau tanpa muzik, Sir letak sound masa upload).
- Info sensitif: tiada (nama ahli group & laporan semuanya rekaan).

## 7. Kualiti & export
- 1080x1920 · 30fps · H.264 ~16 Mbps · AAC · +faststart
- QC safe zone (`pipeline/safezone_qc.py`) sebelum hantar draf.

## 8. Soalan / perkara untuk Sir putuskan
1. **Format:** iklan 15s berasingan (post sendiri / TikTok Ads) **atau** ganti iklan 4s yang disisip dalam video? (Cadangan: buat 15s dulu, kemudian potong versi 4s daripadanya.)
2. **Tawaran / harga:** nak tunjuk harga atau tawaran (cth slot terhad bulan ni)? Atau kekal tanpa harga?
3. **Butiran servis:** checklist betul? Khususnya "Bina team & struktur": adakah servis ni termasuk **cari / rekrut** sales, atau hanya susun struktur team yang owner dah ambil? (Visual "ahli menyertai" perlu ikut jawapan ni.)
4. **CTA:** "WhatsApp link di bio" ok, atau nak "DM 'TEAM'"?
5. **Muzik:** saya pilih muzik bebas royalti, atau tanpa muzik (Sir letak sound TikTok sendiri)?

---
**Status:** ☑ Menunggu approval  ☐ Approved  ☐ Perlu ubah (nota: ____)

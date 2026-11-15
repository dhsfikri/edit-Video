# Brief Edit Video: Iklan Ebook 2026 "Wassap Masih Relevan?"

**Tarikh:** 2026-11-15  **Tajuk/Topik:** Iklan animasi penuh Ebook 2026  **Versi brief:** v3

## 1. Objektif
- Tujuan video: **closing / jualan terus** (iklan berbayar + post organik)
- Target penonton: owner bisnes & team sales yang closing melalui WhatsApp, chat banyak tapi closing sikit
- Produk: **Ebook 2026: Wassap Masih Relevan?** (105 muka surat · Formula 1-4-6-10 · susun team · skrip 2026)
- Harga: ~~RM67~~ **RM37** (ikut bcl.my)
- Jaminan: **"Ebook ni tak membantu, kita refund balik duit."** Dalam **7 hari** selepas beli; claim melalui WhatsApp, refund dibuat hari yang sama.
- CTA: "Dapatkan sekarang, RM37" (butang dalam video, TIADA URL di skrin). Link https://sweetcactusenterprise.bcl.my/form/ebook-sirdharma diletak dalam setting iklan (Meta destination / TikTok link).

## 2. Konsep & gaya
- Konsep: **Chat Simulation + Kinetic Typography** (gaya reference "SaaS product launch", diadaptasi ke brand Sir)
- Gaya editing: E. Chat Simulation + B. Bold & Laju
- Kenapa: animasi penuh tanpa A-roll. Chat WhatsApp terus kena dengan niche Sir. Teks perkataan demi perkataan senang dibaca walaupun tanpa bunyi (iklan selalu ditonton dalam mod mute).
- Diambil dari reference: hanya **gaya** (teks muncul perkataan demi perkataan, ikon terapung, kad dengan bayang lembut, rumusan 3 perkataan, penutup logo bersih). Tiada aset atau logo reference digunakan.

## 3. Hook
- Hook title atas skrin: **"Customer SEEN… tapi tak reply?"**
- Animasi hook: bubble chat Sir keluar → ✓✓ bertukar biru → "typing…" muncul lalu hilang → tiada balasan. SFX: bunyi notifikasi WhatsApp, kemudian sunyi.
- Hook versi B (A/B): **"WhatsApp dah tak relevan?"** (taip, kemudian padam "tak")

## 4. Plan timeline (30s, 1080x1920, 30fps)
| Masa | Isi | Visual | Teks / motion graphic | SFX / muzik |
|---|---|---|---|---|
| 0–3s | Hook | Skrin chat WhatsApp, ✓✓ biru, typing… hilang | "Customer **SEEN**… tapi tak reply?" | Ting notifikasi → sunyi |
| 3–8s | Pain | 3 bubble bantahan bertindih: "mahal la…", "nanti saya fikir dulu", "tunggu gaji" | Kaunter **"Closing hari ni: 0"** | Whoosh setiap bubble |
| 8–14s | Reveal produk | Cover ebook (gambar dari bcl.my) terbang masuk dalam 3D, glow hijau, sparkle ✦ | "**Ebook 2026: Wassap Masih Relevan?**" · "105 muka surat" | Riser, kemudian impact |
| 14–20s | Isi / manfaat | Ikon kecil terapung di tengah ayat (gaya reference) | "Formula **1-4-6-10**." → "Susun **team**." → "Skrip **2026**." | Klik setiap perkataan |
| 20–24s | Transformasi (ilustrasi) | Chat sama: customer balas "Ok, nak 1 😊" → resit "Dah transfer" + confetti ✓ | "Dari SEEN → **CLOSED**" | Ding + confetti |
| 24–28s | Jaminan + harga | Ikon perisai hijau | "Ebook ni tak membantu? **Kita REFUND balik duit.**" · kecil: "Dalam 7 hari · claim via WhatsApp" · ~~RM67~~ **RM37** | Stamp / thud |
| 28–30s | CTA + loop | Butang "Dapatkan sekarang" ditekan kursor | "Klik link · RM37" · @sirdharma_ | Bunyi signature |

## 5. Style
- Latar: hitam #0B0B0B (gaya premium), kad putih dengan bayang lembut, aksen hijau #25D366, keyword kuning #FFD60A
- Font: Montserrat ExtraBold (tajuk) / SemiBold (badan)
- Pergerakan: ease-in-out yang smooth, ikut reference; tiada transisi kasar
- Muzik: instrumental corporate-upbeat bebas royalti; SFX WhatsApp versi buatan sendiri (bukan audio asal WhatsApp)
- Semua teks dalam safe zone: x 60–900, y 220–1440

## 6. Aset
- Ada: cover ebook (CDN bcl.my), brand kit, template `motion/iklan/`, `motion/explainer/`, logo/handle
- Masih perlu: syarat refund (lihat §8)
- Info sensitif: nama/nombor dalam chat semuanya rekaan, tiada data customer sebenar

## 7. Kualiti & export
- Animasi penuh (HyperFrames → `pipeline/compose.py`)
- Export: 1080x1920 · 30fps · H.264 ~15–20 Mbps · AAC · +faststart
- QC: `pipeline/safezone_qc.py` sebelum hantar draf

## 8. Keputusan Sir
1. Refund: claim melalui WhatsApp, refund dibuat hari yang sama ✅
2. Link CTA: `ebook-sirdharma` ✅
3. Platform: Meta Ads + TikTok ✅ (satu master 9:16; teks dalam safe zone TikTok supaya selamat untuk kedua-dua)
4. Suara: muzik + SFX sahaja ✅
5. Babak "SEEN → CLOSED": ilustrasi, tanpa angka % ✅
6. Tempoh refund: 7 hari ✅

---
**Status:** ☐ Menunggu approval  ☑ Approved (2026-11-15)  ☐ Perlu ubah (nota: ____)

## Revisi / log
- **Draf v1 (2026-11-15):** sumber `motion/iklan-ebook/index.html`, audio `projects/IKLAN-EBOOK2026/audio.py` (muzik + SFX sintetik, bebas royalti). Cover dari halaman 1 PDF ebook.
  - Ikut peraturan skill (mockup generik, tiada bukti bayaran palsu): babak 20–24s guna **balasan ikut skrip → "Ok, saya nak 1"**, BUKAN resit transfer.
  - QC: safe zone lulus · -14.4 LUFS · peak -2.1 dB · 1080x1920 30fps H.264.

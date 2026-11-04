# Brand Kit — Dharma | Sales Guru (@sirdharma_)

> Rujukan WAJIB setiap kali edit video TikTok, buat thumbnail, atau reka grafik.
> Status: **v1 — menunggu approval Sir** (2026-11-04)

---

## 1. Identiti
| Item | Nilai |
|---|---|
| Nama | Dharma \| Sales Guru |
| TikTok | **@sirdharma_** |
| Niche | Sales closing (WhatsApp), tips jualan, team sales |
| Servis | Setup team sales A–Z + monitoring 30 hari · Personal coaching (link di bio) |

## 2. Warna
| Token | Hex | Guna untuk |
|---|---|---|
| Hijau jenama | `#25D366` | Badge siri, aksen, kotak karaoke subtitle, CTA |
| Hijau gelap | `#0B3D2E` / `#082015` | Latar explainer, band atas thumbnail, teks dalam kotak putih |
| Hitam | `#0B0B0B` | Pil badge, kad |
| Putih | `#FFFFFF` | Teks utama, kotak keyword dalam video |
| Kuning | `#FFD60A` | **Keyword dalam thumbnail** (satu sahaja), harga/amaran |
| Merah | `#FF5A5A` | Ikon ✕ (salah) sahaja |

## 3. Font
| Font | Guna | Fail |
|---|---|---|
| **Anton** | Headline THUMBNAIL (huruf besar, condensed) | `@fontsource/anton` |
| **Montserrat ExtraBold 800 / SemiBold 600** | Semua teks dalam video, badge, subtitle, callout | `@fontsource/montserrat` |
| **Caveat 700** | Tulisan tangan (kicker kecil atas headline) | `@fontsource/caveat` |

## 4. Siri (badge)
`AYAT CLOSING #NN` · `TIPS JUALAN #NN` · `BEDAH CHAT #NN` · `OBJECTION KILLER #NN`
Pil hitam, border hijau, titik hijau, nombor hijau.

---

## 5. ⚠️ SAFE ZONE TIKTOK (video 1080x1920) — WAJIB

```
y=0    ┌──────────────────────────────┐
       │░░░░ ATAS: tab Following/For You ░░│  y < 220   ✗ tiada teks/grafik
y=220  ├──────────────────────────┬───┤
       │                          │░░░│
       │      ZON SELAMAT         │░░░│  x > 900 (y 700–1500): butang
       │   x 60 – 900             │░░░│  profil/like/komen/save/share
       │   y 220 – 1440           │░░░│  ✗ tiada teks
       │                          │░░░│
y=1440 ├──────────────────────────┴───┤
       │░░░ BAWAH: username, caption, ░░░│  y > 1440  ✗ tiada teks
       │░░░ muzik, butang produk      ░░░│
y=1920 └──────────────────────────────┘
```

| Elemen | Kedudukan standard |
|---|---|
| Badge siri | x 60, **y 240** |
| Tajuk kinetik / hook | x 60, y 300–620 |
| Callout / pil | dalam x 60–900 |
| Subtitle | **y 1300–1400** (tengah) |
| Kad CTA | y 1150–1280 |
| Grafik penuh skrin (B-roll/iklan) | Boleh penuh, TAPI semua **teks** kekal dalam zon selamat |

**QC:** setiap draf → `python3 pipeline/safezone_qc.py <video>` → semak gambar dengan garisan zon. Tiada teks dalam zon merah.

---

## 6. THUMBNAIL STANDARD
Template: `motion/thumbnail-std/` · Config per video: `projects/<ID>/thumb.json`

Grid profil potong thumbnail jadi **3:4 (y 240–1680)** dan letak **"▷ views" di bawah kiri**.

```
y=240  ┌───────────────────────┐ ← mula nampak dalam grid
y=300  │ ● SIRI #NN            │  badge
y=385  │ kicker (tulisan tangan)│
       │ HEADLINE BARIS 1      │  Anton, putih, BESAR
       │ BARIS 2 [KEYWORD]     │  1 keyword kotak KUNING
       │      ╭─────╮          │
y~1160 │      │MUKA │          │  muka besar, ekspresi kuat
       │      ╰─────╯ [✕ pil] │  1 callout kanan (y 1260–1400)
y=1450 │░░░░ ▷ views ░░░░░░░░░│  ✗ tiada teks
y=1680 └───────────────────────┘ ← habis nampak dalam grid
```

**Peraturan:**
1. Headline **maks 2 baris, 3–6 patah perkataan**, huruf besar, font Anton.
2. **Satu** keyword dalam kotak kuning — perkataan yang paling "sakit"/menarik.
3. Band hijau gelap di atas (sama untuk semua video) → grid nampak seragam.
4. Muka Sir: close-up, ekspresi kuat (frust/terkejut/serius), pusat ~y 1160.
5. Satu pil callout (✓ hijau atau ✕ hitam) di kanan — tambah rasa ingin tahu.
6. Tiada teks di y < 290, y > 1450, atau x > 1010.

## 7. Gaya video (rujukan)
- **Gaya v2** (standard semasa): tajuk headline kiri-atas, subtitle kecil karaoke hijau, bracket fokus, callout, babak explainer (muka dalam bulatan + mockup chat generik), grade lembut.
- Template: `motion/overlay-v2/`, `motion/explainer/`, `motion/iklan/`, `motion/broll/`.
- Tiada rupa/logo app sebenar (WhatsApp/TikTok Shop) — mockup generik sahaja.
- Tiada janji hasil (cth "sales naik 2x") tanpa bukti sebenar.

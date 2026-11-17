---
name: riset-trend
description: Riset trend pantas untuk video TikTok Sir Dharma (sales closing WhatsApp / seller Malaysia) — apa yang tengah naik (topik, format, hook, bunyi, kempen platform) dan bagaimana kaitkan dengan isi Sir. Guna sebelum brief video baru, sebelum hook-lab, atau bila Sir tanya "apa trend sekarang".
---

# Riset Trend — Sir Dharma

**Versi 1.0 (2026-11-17).** Tujuan: dalam ~5 minit, tahu apa yang relevan MINGGU INI — bukan semua trend, hanya yang boleh disambung dengan jualan/closing WhatsApp. (Panduan seller: kejar semua trend = views kosong, bukan jualan.)

## Sumber (yang SAH jalan dalam environment ini)
| Sumber | Cara | Untuk apa |
|---|---|---|
| **WebSearch** (standard; extended jika nipis) | Kueri BM + EN: "TikTok trend Malaysia <bulan tahun>", "TikTok Shop kempen <bulan>", "seller Malaysia viral <topik>" | Kempen platform (11.11, 12.12, Raya), format yang naik, berita seller |
| **Google Trends RSS** | `curl -s "https://trends.google.com/trending/rss?geo=MY"` → tajuk + trafik | Topik umum yang sedang dicari (cari yang boleh disambung ke jualan) |
| **Video rujukan dari Sir** (TikTok/IG/FB link) | `yt-dlp` → helaian frame → skill `reverse-any-video` / `viral-reverse-engineering` | Struktur hook, rentak, teknik visual |
| Plugin social media | `social-media-skills:trend-jacking`, `content-research-and-sourcing`, `tiktok-growth` | Kerangka menilai & menunggang trend |
**JANGAN** guna API dalaman tidak berdokumen (contoh `creative_radar_api`) — disekat & melanggar terma. TikTok Creative Center: hanya jika boleh dibuka sebagai halaman awam.

## Langkah
1. Jalankan 3–5 carian + Google Trends RSS.
2. Tapis: simpan hanya trend yang lulus **3 soalan**: (a) penonton Sir (seller/peniaga) peduli? (b) boleh sambung kepada satu pelajaran jualan/closing? (c) selamat untuk jenama (tiada isu sensitif, tiada janji hasil)?
3. Untuk setiap trend yang lulus, tulis: **trend → sudut Sir (1 ayat) → idea hook → format/visual**.
4. Simpan `docs/trend/<YYYY-MM-DD>.md` (+ senarai sumber dengan link). Fail minggu lepas dibaca dulu supaya tak ulang.
5. Serahkan kepada `hook-lab`.

## Format output (`docs/trend/<tarikh>.md`)
```
# Trend <tarikh>
| Trend | Kenapa relevan | Sudut Sir | Idea hook | Format |
## Sumber
- [tajuk](url)
```

# Konsep Editorial — Dharma | Sales Guru (@sirdharma_)

> Pakej gaya untuk setiap video. Pilih **satu gaya** dalam brief (`templates/brief-edit.md` §2).
> Semua gaya ikut `BRANDKIT.md` (warna, font, siri) dan **safe zone** (teks x 60–900, y 220–1440).
> Status: **v1 (2026-11-05)**. Sir pilih **MAGAZINE** (warna C: grade warm + keyword kuning) sebagai gaya utama. 3 gaya lain kekal sebagai pilihan.

Template: `motion/editorial/` (satu template, 4 gaya) · Definisi gaya: `motion/editorial/styles.json`
Render satu arahan:
```bash
python3 -I pipeline/editorial.py projects/<ID>/edit.json projects/<ID>/data.js <clean|bold|chat|magazine> <outdir>
```

---

## Ringkasan pilihan

| | 1. CLEAN COACH | 2. BOLD & LAJU | 3. CHAT STORY | 4. EDITORIAL MAGAZINE |
|---|---|---|---|---|
| **Mood** | Tenang, berwibawa | Bertenaga, scroll-stopper | "Intai" chat sebenar | Premium, serius |
| **Grade** | Lembut, kurang saturasi | Kontras tinggi + tajam | Lembut, sedikit sejuk | Sinematik warm + vignette |
| **Zoom A-roll** | Tetap 1.2 | Bertukar 1.2 ↔ 1.42 setiap potong (punch-in) | Tetap 1.2 | Tetap 1.26 |
| **Tajuk** | Caveat + Montserrat, keyword kotak putih ditaip | Huruf besar tengah, slam satu-satu + gegar, keyword kotak kuning | Bubble chat + "typing…", keyword bubble hijau ✓✓ | Anton penuh lebar, mask reveal, garisan + "01 / 03", keyword & kicker **kuning** |
| **Subtitle** | Kecil, kotak karaoke hijau | Besar huruf besar, outline hitam, perkataan aktif kuning | Dalam pil hijau gelap, perkataan aktif hijau | Nipis, garis bawah kuning |
| **Callout** | Pil putih ✓/✕ | Kotak kuning outline hitam | Cop serong ✓ BETUL / ✕ | Label garis tepi hijau |
| **Peralihan** | Soft (kilat putih lembut) | Flash putih + whoosh | Swipe panel hijau gelap ke atas | Wipe blok hijau → hitam |
| **SFX** | Signature sahaja | Pop (tajuk) + whoosh | Tick (bubble) + whoosh | Boom rendah (tajuk) + whoosh |
| **Sesuai siri** | AYAT CLOSING, tips panjang | OBJECTION KILLER, hook kontroversi | BEDAH CHAT | TIPS JUALAN, case study |

> Padanan siri hanya **cadangan**. Sir boleh pilih gaya lain untuk mana-mana video.

---

## Peraturan semua gaya
1. **Hook di depan** (0–3s), tajuk hook muncul dari saat 0.
2. **2–3 tajuk** sahaja sevideo: hook → poin utama → penutup (jawapan kepada hook untuk loop).
3. **Satu keyword** sahaja ditonjolkan dalam setiap tajuk.
4. Peralihan hanya pada **titik potong** (automatik dari `cuts.json`). Jangan tambah peralihan tanpa potongan.
5. Muka tinggi dalam frame (duduk dekat kamera)? Guna `titleY` (cth 880), dan tajuk diletak atas baju. Template tolak tajuk naik secara automatik kalau sampai kena subtitle.
6. Mockup app **generik**. Tiada janji hasil tanpa bukti.

## Medan data tambahan (data.js)
| Medan | Guna |
|---|---|
| `style` | Diisi oleh `editorial.py`, tak perlu tulis manual |
| `transitions` | `[{t, kind?}]`. Kosongkan untuk peralihan automatik di setiap potongan |
| `chapter` | Label kecil gaya magazine (cth "TIPS RAYA") |
| `titleY` / `titles[].y` | Kedudukan y tajuk |
| `magMax` | Saiz maksimum font Anton gaya magazine (default 200) |
| `hold_end` | Tahan frame akhir N saat untuk CTA |
| `words: "auto"` | Guna words.json terus dari cut.py |

## Tambah gaya baru
1. Tambah entri dalam `motion/editorial/styles.json` (grade, zoom, transition, sfx).
2. Tambah CSS `.s-<gaya>` dan builder tajuk dalam `motion/editorial/index.html`.
3. Render preview, brief Sir, kemas kini jadual di atas.

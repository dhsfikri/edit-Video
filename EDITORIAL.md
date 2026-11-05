# Konsep Editorial — Dharma | Sales Guru (@sirdharma_)

> Pakej gaya untuk setiap video. Pilih **satu gaya** dalam brief (`templates/brief-edit.md` §2).
> Semua gaya ikut `BRANDKIT.md` (warna, font, siri) dan **safe zone** (teks x 60–900, y 220–1440).
> Status: **v1.1 (2026-11-05)**. Sir pilih **MAGAZINE** sebagai gaya utama: grade warm, keyword kuning, tajuk **kad kaca + kinetic typography** (konsep no. 6). 3 gaya lain kekal sebagai pilihan.

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
| **Tajuk** | Caveat + Montserrat, keyword kotak putih ditaip | Huruf besar tengah, slam satu-satu + gegar, keyword kotak kuning | Bubble chat + "typing…", keyword bubble hijau ✓✓ | **Kad kaca** (blur sebenar) + kinetic typography: label → kicker → perkataan masuk satu-satu (blur→tajam), keyword **kuning** huruf demi huruf, bar kuning. Pilihan lama: `titleStyle: "cover"` (Anton penuh lebar) |
| **Subtitle** | Kecil, kotak karaoke hijau | Besar huruf besar, outline hitam, perkataan aktif kuning | Dalam pil hijau gelap, perkataan aktif hijau | Nipis, garis bawah kuning |
| **Callout** | Pil putih ✓/✕ | Kotak kuning outline hitam | Cop serong ✓ BETUL / ✕ | Pil kaca, garis tepi kuning |
| **Peralihan** | Soft (kilat putih lembut) | Flash putih + whoosh | Swipe panel hijau gelap ke atas | Wipe blok hijau → hitam |
| **SFX** | Signature sahaja | Pop (tajuk) + whoosh | Tick (bubble) + whoosh | Pop lembut (tajuk) + whoosh |
| **Sesuai siri** | AYAT CLOSING, tips panjang | OBJECTION KILLER, hook kontroversi | BEDAH CHAT | TIPS JUALAN, case study |

> Padanan siri hanya **cadangan**. Sir boleh pilih gaya lain untuk mana-mana video.

---

## B-roll gaya MAGAZINE — `motion/broll-mag/`
Latar gelap warm + cahaya kabur + grain, muka Sir dalam tetingkap segi empat bulat (kiri atas), kad kaca tajuk (sama dengan tajuk video), kandungan y 720–1280.
| Babak | Isi |
|---|---|
| `produk` | Grid 6 kad produk generik → cop ✕ TAK LAKU (kad digelapkan) → cop ✓ LAKU kuning |
| `database` | Senarai kontak "DATABASE CUSTOMER" → highlight pilih customer → chat generik follow up |
```bash
python3 -I pipeline/facecrop.py <SRC> motion/broll-mag/assets/face_<babak>.mp4 --rotate cw --seg <mula>:<tamat> --fps 50
cd motion/broll-mag && npx hyperframes render --variables '{"scene":"produk","dur":3.5,"face":"assets/face_produk.mp4"}' -f 50 -q high -o br.mp4   # kemudian trim -t dur
```
Masukkan dalam `data.js` → `"broll": [{"src", "start", "dur"}]` dan letak `transitions` pada sempadan B-roll (wipe).
Tambah babak baru: entri baru dalam `SCENES` (label, kick, words [[teks, keyword?]], build()).

## Peraturan berasaskan data (`docs/prestasi-tiktok.md`)
> Dikemas kini setiap kali ada data baru. Data 1 (28 Okt–3 Nov): like ×8.7 selepas gaya baru, **komen 0 selama 7 hari**, share rendah.

1. **CTA komen wajib ada "kata kunci + ganjaran"**, keluar di skrin (kad kaca) DAN disebut Sir. Contoh: *Komen "PART 2" → saya buat video seterusnya*. Jangan guna CTA kabur ("komen di bawah").
2. **Seed komen:** satu soalan mudah di tengah video yang boleh dijawab satu perkataan (cth "Raya ni awak jual apa? Komen 👇"). Letak sebagai callout kecil semasa babak santai.
3. **Momen "boleh share":** setiap video ada satu kad ringkas yang orang nak hantar kepada team/kawan seller (senarai 3 langkah, ayat closing yang boleh disalin). Tahan ≥ 2s supaya sempat screenshot.
4. **Kekal yang menjadi:** hook soalan pada 0–1s, B-roll explainer, subtitle karaoke. Gaya baru naikkan like rate 0.44% → 3.81%.
5. **Tolak ke profil:** CTA akhir sebut *sebab* untuk follow/klik profil (cth "Part 2 keluar esok, follow supaya tak terlepas").
6. **Setiap brief tulis 1 hipotesis** yang nak diuji, dan metrik untuk ukur (lihat jadual hipotesis dalam `docs/prestasi-tiktok.md`).

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
| `titleStyle` | Magazine: `glass` (default, kad kaca) atau `cover` |
| `magMax` | Saiz maksimum font Anton gaya `cover` (default 200) |
| `broll` | `[{src, start, dur}]` B-roll penuh skrin (diteruskan ke compose.py) |
| `hold_end` | Tahan frame akhir N saat untuk CTA |
| `words: "auto"` | Guna words.json terus dari cut.py |

## Tambah gaya baru
1. Tambah entri dalam `motion/editorial/styles.json` (grade, zoom, transition, sfx).
2. Tambah CSS `.s-<gaya>` dan builder tajuk dalam `motion/editorial/index.html`.
3. Render preview, brief Sir, kemas kini jadual di atas.

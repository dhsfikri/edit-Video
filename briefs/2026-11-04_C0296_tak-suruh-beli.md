# Brief Edit — C0296 "Kenapa orang tak dengar cakap awak?" (DEMO GAYA v2)

**Fail asal:** `Folder Video/Raw/C0296.MP4` · **Versi brief:** v1
**Status:** ☐ Menunggu approval  ☑ Approved  ☐ Perlu ubah

## 0. Spec fail asal (dah semak)
| Item | Nilai | Tindakan |
|---|---|---|
| Resolusi | 1920x1080 dirakam **sideways** (arah lain dari C0029) | Pusing 90° lawan jam → 1080x1920 |
| FPS | 29.97 | Kekal 30fps |
| Durasi | 25.5s | Potong jadi ±16–18s |
| Lokasi | Kelas / training, Sir berdiri depan whiteboard, ada peserta di depan kamera | — |
| Kamera | Handheld, bergerak di awal (0–9s), lebih stabil 9–25s | Guna 9–25s untuk isi utama |
| Audio | Mic kamera, ada gema bilik (mean -20.7 dB) | Kurangkan noise + kuatkan suara. Gema tak boleh dibuang sepenuhnya |

## 1. Objektif
- Siri: **AYAT CLOSING #01** (topik closing — kena dengan niche asal)
- Mesej: customer tak beli sebab **kita tak suruh** — tak suruh beli, tak suruh bayar, tak buat keputusan untuk dia
- CTA: komen / follow

## 2. Struktur (loop)
| Video | Sumber | Ayat | Grafik gaya v2 |
|---|---|---|---|
| 0–1.6s | 9.95–11.17 | "Kenapa orang tu tak dengar cakap awak?" | **Tajuk kinetik kiri-atas**: *kenapa orang* (tulisan tangan) / TAK DENGAR / CAKAP **[AWAK?]** (kotak putih ditaip) |
| 1.6–2.1s | 13.20–13.62 | "Kenapa?" | Bracket fokus pada muka |
| 2.1–3.0s | 16.52–17.38 | "Sebab awak tak cakap." | Bracket kekal, keyword **TAK CAKAP** |
| 3.0–6.5s | — | (babak explainer) | Latar hijau gelap, muka Sir dalam bulatan, **mockup chat**: customer "Nanti saya fikir dulu ya" → seller menunggu… ❌ |
| 6.5–7.4s | 20.34–21.18 | "Awak tak suruh dia beli." | Tag callout ❌ *tak suruh beli* di sebelah Sir |
| 7.4–8.5s | 21.74–22.80 | "Awak tak suruh dia buat bayaran." | Tag ❌ *tak suruh bayar* |
| 8.5–10.0s | 23.42–24.86 | "Awak tak buat decision untuk dia." | Tag ❌ *tak buat keputusan* |
| 10.0–13.5s | — | (babak explainer) | Mockup chat versi BETUL: seller "Saya hantar link bayaran sekarang ya? 😊" → customer "Ok ✅" |
| 13.5–15.1s | 5.95–7.57 | "Orang boleh dengar cakap awak." | Tajuk kinetik: *ingat* / ORANG BOLEH **[DENGAR]** — sambung loop ke hook |

Dibuang: "Faham? Dan satu lagi…" (pembukaan), "Tapi sekarang ni", "Kenapa geng-geng dof?", "Bukan kesian", "Sebab tak cakap" (ulang), "Percayai cakap saya".

## 3. Gaya v2 (demo pertama)
- Subtitle kecil bawah, kotak karaoke hijau pada perkataan aktif
- Font Montserrat + Caveat (tulisan tangan)
- Grade lembut / sinematik
- Rentak tenang, tiada punch-in besar
- Badge siri kecil

## 4. Perkara untuk Sir putuskan
1. Peserta dalam kelas nampak di depan kamera (kebanyakan belakang kepala). Mereka dah setuju untuk muncul dalam video?
2. Whisper dengar "Bukan **kesian**" dan "Kenapa geng-geng **dof**" — Sir sebenarnya cakap apa? (Saya cadang buang kedua-dua ayat ni.)
3. Durasi ±15s tanpa iklan. Nak sisip iklan 4s juga? (Cadangan: tak, sebab video pendek — iklan akan ambil 25% video.)

---
## Revisi
- B-roll: babak chat SALAH/BETUL diletak **semasa Sir bercakap** (bukan senyap) — muka dalam bulatan ikut muka (pipeline/facecrop.py).
- **Draf v1 (11.5s):** hook → kenapa → sebab tak cakap (callout) → chat SALAH → chat BETUL → percayai cakap saya + CTA follow.
- **Draf v2 (14.7s):** Sir minta ±15s & kekalkan hook di depan → tambah "Saya nak cerita, orang boleh dengar cakap kita" + "Tapi sekarang ni…" SELEPAS hook.
- **Draf v3:** tajuk jadi headline — muncul sekali gus (0.5s), kekal lama, tak ikut suara. 3 tajuk sahaja: hook (0–4.9s), TAK CAKAP (4.9–6.7s), ORANG BOLEH DENGAR (12.8s–akhir).
- Subtitle: "bayar bayaran" → "buat payment" (perlu Sir sahkan).

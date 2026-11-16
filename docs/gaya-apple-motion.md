# Gaya "Apple Motion": nota teknik

> Sumber: *Learn Apple Style Motion Graphics in 20 minutes | After Effects* (Bart_VFX), dikaji 2026-11-16
> (transkrip + frame). Sampel kita: `motion/apple-morph-test/` (tema gelap & cerah, 60fps).

## 5 teknik teras
| # | Teknik | Dalam After Effects (rujukan) | Cara kita (code) |
|---|---|---|---|
| 1 | **Morphing**: satu bentuk berubah jadi bentuk lain, bukan potong babak | Shape layer "frame" + "circle"; ubah `size` & `position` | Satu bekas (`FW/FH`) + satu butang (`BX/BY/BW/BH`); bucu ikut ketinggian (pill → kad) |
| 2 | **Bounce**: terlajak sedikit, mendarat lembut | Ekspresi bounce pada size / position / scale | `spring(dt, D, ζ=0.62)` (lajak ~8%); `soft()` ζ=0.95 untuk opacity / warna |
| 3 | **Offset masa** anak vs induk | `valueAtTime(time - 0.1)` | Anak panah ikut `BW(t - 0.1)`; ikon & teks masuk 0.05–0.1s selepas induk |
| 4 | **Teks**: jatuh ikut perkataan; angka/harga masuk ikut huruf dari kanan | Text animator: Position Y -100 + Opacity 0 + Expression Selector (words / characters) | `dropWords()` stagger 0.04–0.06s; `slideChars()` stagger 0.018–0.03s |
| 5 | **Kemasan**: 60fps, motion blur, putaran halus seluruh komposisi, laluan melengkung, "tekan butang" sebelum morph | 60fps comp, motion blur on, null "all" + rotation, pen tool pada laluan position, scale 100→~88→100 | Render 60fps; purata 8 sub-frame (shutter 180°); `ROT` ±1.5–1.8° bila morph; tempoh x ≠ y untuk lengkung; `BS` tekan |

## Peraturan ringkas
- Kunci sesedikit mungkin; biar spring buat kerja. Laraskan **masa**, bukan bentuk lengkung.
- Setiap morph didahului "sebab" (butang ditekan / ditolak) → rasa fizikal.
- Laluan pergerakan melengkung, bukan garis lurus.
- Latar bersih (rujukan: kelabu cerah; brand kita: hitam + cahaya hijau lembut). Satu warna aksen.
- Semua teks kekal dalam safe zone TikTok (x 60–900, y 220–1440).

## Nota percanggahan
Skill `motion-design` (personaliti *Premium*) sarankan 0% lajak. Rujukan Apple ini **guna bounce kecil (~5–10%)**.
Untuk kerja gaya Apple, ikut rujukan ini.

## Versi CINEMATIC + 3D (`motion/apple-morph-test/cinematic.html`)
Ikut skill `cinetic` (lighting.md §1/§7, camera.md §8/§9/§13) + `threejs-lighting` / `threejs-postprocessing`:

| Elemen | Nilai yang dipakai |
|---|---|
| Cahaya kunci | SpotLight dari atas kiri (azimuth ~315°, elevation ~34°), kolam cahaya bergerak perlahan (cahaya hidup, bukan objek) |
| Bayang | VSM lembut (radius 14) + cahaya "kontak" hampir dari depan untuk bayang pendek & tajam rapat dengan objek; bayang dalam hue dinding (hijau gelap), bukan hitam |
| Ketinggian (lift) | Objek naik bila bergerak (bayang memanjang & lembut), turun bila ditekan (bayang mengecil) |
| Bahan | Slab extrude dengan bevel (tepi menangkap cahaya = rim); butang emissive ringan; teks pada satah tanpa cahaya (sentiasa tajam) |
| Kamera | Kanta panjang (FOV 28°); dolly masuk semasa buka → satu orbit 3D (yaw −13°) masa kad muncul, mendarat menghadap → push ke butang akhir. Tiada terapung antara gerakan |
| Kemasan | NeutralToneMapping (warna brand kekal), bloom hanya > 1.0 (butang sahaja, tiada halo pada teks), vignette, grain, motion blur 2 sub-frame |
| Teks | Tanpa lajak (cinetic: tiada spring pada copy); bentuk & butang guna spring |
| Kos render | ~1.6 s/sub-frame tanpa DOF (Bokeh ~2× lebih lambat; ditinggalkan kerana semua elemen dalam satu satah fokus) |

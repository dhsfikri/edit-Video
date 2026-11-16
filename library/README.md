# Pustaka Aset (library/)

Semua gambar, ikon, frame & klip yang Claude guna dalam video **disimpan di sini dan direkod dalam `katalog.json`**.
Aset yang sama boleh diguna semula, dan setiap satu ada rekod sumber + lesen.

| Folder | Isi | Sumber |
|---|---|---|
| `suasana/` | Gambar stok (orang guna phone, kedai, pejabat, wang, dll.) | Pexels (percuma, komersial OK) |
| `b-roll/` | Klip video stok pendek | Pexels Videos |
| `ikon/` | Ikon SVG (warna brand) | Tabler Icons (MIT) via npm |
| `sir/` | Frame ekspresi Sir dari rakaman sendiri (terkejut, senyum, tunjuk, serius) | Raw Sir |
| `mockup/` | Mockup chat generik, kad ayat, grafik yang Claude bina | Claude (HyperFrames/HTML) |

## Cara guna (`pipeline/aset.py`)
```bash
python3 -I pipeline/aset.py cari "customer phone" --n 10          # cari gambar Pexels (portrait)
python3 -I pipeline/aset.py cari "typing phone" --video            # cari klip video
python3 -I pipeline/aset.py ambil 607812 --kategori suasana --tag "phone,customer"
python3 -I pipeline/aset.py ikon message-circle check x --warna 25D366
python3 -I pipeline/aset.py frame raw.MP4 12.4 --nama sir-terkejut --tag "ekspresi,terkejut" --rotate cw
python3 -I pipeline/aset.py guna pexels-607812 C0301                # rekod video mana guna aset ni
python3 -I pipeline/aset.py senarai --tag phone
```

## Peraturan
- **Lesen mesti jelas** sebelum guna. Hanya: Pexels License, MIT/ISC, CC0, atau milik sendiri. Tiada gambar Google/Pinterest rawak.
- Tiada logo/rupa app sebenar (WhatsApp, TikTok Shop) — BRANDKIT §7.
- Tiada gambar orang yang boleh nampak macam testimoni/customer sebenar Sir.
- Gambar disimpan maks 1080px lebar, JPEG q85 (repo kekal ringan). Klip video besar (>20 MB) → scratchpad + zip kepada Sir untuk Drive `02 B-Roll`.
- Salinan Drive: Claude zip folder `library/` bila ada tambahan, Sir upload ke `Aset` (connector tak praktikal untuk upload fail binari).

## Setup sekali sahaja
Pexels perlukan **API key percuma** (https://www.pexels.com/api/). Simpan dalam tetapan environment → *Network secrets*:
host `api.pexels.com`, header `Authorization`, nilai = key (tanpa "Bearer").

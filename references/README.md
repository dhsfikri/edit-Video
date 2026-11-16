# References (video rujukan)

Sir hantar **link sahaja** (TikTok / IG / FB / YouTube) dalam chat + satu ayat apa yang Sir suka.
Claude jalankan:

```bash
python3 -I pipeline/ref.py "<link>" --nota "suka hook dia" --kerja <scratchpad>/ref
```

Hasil:
- `references/<platform>-<id>.md` — metadata, statistik, rentak (tukar visual), transkrip, analisa Claude
- `references/img/<platform>-<id>.jpg` — contact sheet (1 frame / 2s)
- Video asal **tidak** disimpan dalam repo (folder sementara sahaja).

Peraturan: reference untuk **pinjam struktur/rentak/gaya**, bukan tiru sebiji. Brief mesti nyatakan apa yang dipinjam.

Kalau download gagal dengan 403: host CDN video belum dibenarkan. Skrip cetak nama host → tambah ke
Allowed domains environment (atau Sir tambah wildcard `*.tiktokcdn.com`, `*.tiktok.com`, `*.cdninstagram.com`, `*.fbcdn.net` di Settings).

# Ujian 5s — gaya pembukaan "IKEA Together" (allkustom)
- Sumber animasi: `motion/ikea5/index.html` (HyperFrames + GSAP). Tangan: ilustrasi **VectorCraft** (`hand_vector.py` → `motion/ikea5/assets/hand.svg`, disisip ke index.html). Audio: `audio_ikea5.py` (sintetik).
- Babak: bar jatuh bina "WASSAP" → tali + manik hijau → tangan tarik → huruf runtuh jadi bar → peralihan berlian → lampu menyala, perabot bercantum, telefon menyala + notifikasi.
- Gaya diambil daripada reference; isi, warna (kuning #FFD60A, hitam, hijau #25D366) milik Sir. Tiada aset/logo IKEA.
- QC: teks dalam safe zone · -13.2 LUFS · peak -2.3 dB.

## v3 (animasi tidak kaku)
- Tangan lebih berisi (jari tebal, ibu jari besar) — `hand_vector.py` → `motion/ikea5/assets/hand.svg`.
- Prinsip animasi: lengan meluncur dari kanan dengan lengkungan kecil (pivot bahu), overshoot & settle, tangan "bernafas",
  anticipation sebelum tarik, huruf ditolak & penyek → runtuh jadi blok tebal (elastic), manik = bandul teredam,
  bar mendarat dengan squash, perabot mendarat dengan squash & stretch (titik asal transform dikunci).
- QC: teks dalam safe zone · -14.5 LUFS · peak -3.2 dB.

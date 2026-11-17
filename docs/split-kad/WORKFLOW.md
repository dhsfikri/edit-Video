# Workflow: Gaya "Split Kad" (rujukan @nicksaraevdaily) — EffectCraft + skill

Rujukan analisis: `docs/rujukan/split-kad-nick/README.md` · Prototaip: `motion/effectcraft/proto_split.ecproj`

## Pembahagian kerja alat
| Kerja | Alat | Kenapa |
|---|---|---|
| Potong rakaman, transkrip, masa perkataan | `pipeline/cut.py` + faster-whisper (skill `tiktok-edit` §3–5) | Sudah terbukti |
| Storyboard visual + approval | skill **`director`** | Wajib sebelum render |
| Pelan gerakan (easing, stagger, tujuan setiap gerakan) | skill **`motion`** | Satu "bahasa" gerakan |
| Prinsip kamera / transition antara mod | skill **`cinematic-camera`** | Satu dunia, bukan panel bertaburan |
| **Komposit utama**: susun atur split, bingkai video bersudut bulat (track matte), kad 3D flip, pentas gelap + spotlight, maskot, kamera, render akhir | **EffectCraft** (MCP, setara After Effects) | 3D sebenar, matte, effect, keyframe/expression, render H.264 |
| Kad UI berteks banyak (kad kamus, tweet, how-it-works, mockup chat) | **HyperFrames** (`motion/`) → render `.mov` telus → import ke EffectCraft | Susun atur HTML lebih pantas untuk UI |
| Blok siap (kaunter, kursor, text swap) | skill **`hyperframes-registry`** | Jangan bina semula |
| Caption perkataan-demi-perkataan + kata kunci serif italic | HyperFrames (overlay telus) | Masa perkataan dari `words.json` |
| QC safe zone, kenyaringan | `pipeline/safezone_qc.py`, ebur128 | Wajib setiap draf |

## Langkah setiap video
1. **Transkrip + potong** (`tiktok-edit`): `edit.json` → `base.mov`, `words.json`, `cuts.json`.
2. **Director**: tandakan setiap ayat dengan mod **A (split) / B (penuh muka) / C (pentas gelap)** + komponen yang muncul. Hasilkan storyboard visual → Sir approve.
3. **Kad UI** (HyperFrames): bina setiap kad dalam `motion/split-kad/` → render `_kerja/<ID>/kad_*.mov` (telus).
4. **EffectCraft**: buka templat `motion/effectcraft/split_kad_template.ecproj` (dari prototaip) →
   - import `base.mov` + kad `.mov` ke `_kerja/<ID>/` (EffectCraft hanya baca dalam repo),
   - mod A: video skala ~90% dalam matte bulat + bingkai aksen; mod B: video penuh; mod C: pentas gelap,
   - tukar mod dengan transition licin (bingkai membesar jadi penuh skrin / mengecil semula),
   - kad masuk/flip ikut masa perkataan, maskot berjalan atas bingkai.
5. **Caption** (HyperFrames overlay telus) → import sebagai lapisan atas.
6. **Render** EffectCraft H.264 → `pipeline/compose.py` untuk audio akhir (-14 LUFS) + SFX.
7. **QC** safe zone + semak frame → draf kepada Sir.

## Resipi: kesan POP-OUT (kepala Sir terkeluar dari bingkai) — keputusan Sir 2026-11-17
1. Potong latar video Sir: `npx hyperframes remove-background _kerja/<ID>/base.mp4 -o _kerja/<ID>/sir_cutout.mov` (model `u2net_human_seg`, khas orang; ~0.6s/frame CPU → 30s video ≈ 9 min). Hasil: ProRes 4444 dengan alpha.
   - **Object Matte EffectCraft TIDAK jalan dalam sesi CPU ini** (keluar lapisan kosong) — jangan guna.
2. EffectCraft (dari bawah ke atas): latar → bingkai aksen (bulat) → video asal **track matte** bentuk bulat → `sir_cutout.mov` (transform SAMA dengan video asal) **track matte** segi empat yang lebar = dalam bingkai, tinggi dari ~400px atas bingkai hingga bawah bingkai.
3. Letak video supaya kepala melepasi garis atas bingkai ~120–180px; susun kad/caption di atas ruang kepala.
Prototaip: `motion/effectcraft/proto_split.ecproj` (render contoh `_kerja/proto_popout.mp4`).

## Sumber yang sudah disediakan
| Sumber | Tempat | Status |
|---|---|---|
| Font brand **Poppins** (tajuk/caption + Light) + **Kalam** (tulisan tangan) — ganti serif italic rujukan (keputusan Sir 2026-11-17). Kata kunci = Poppins Bold hijau brand. Instrument Serif/Inter kekal dalam `aset/fonts/` tetapi TIDAK dipakai | `aset/fonts/` + `motion/assets-brand/` (setup script pasang ke `~/.local/share/fonts`) | ✅ |
| Colour grading | **TIADA** — rakaman asal (keputusan Sir) | ✅ |
| EffectCraft 0.10.0 + MCP | setup script environment | ✅ |
| Folder kerja EffectCraft | `_kerja/` (diabaikan git) | ✅ |
| Prototaip split + kad 3D flip + render | `motion/effectcraft/proto_split.ecproj` | ✅ diuji (4s render ~20s CPU) |
| Skill: director, motion, cinematic-camera, hyperframes(+registry), reverse-any-video, tiktok-edit | `.claude/skills/` | ✅ |

## Belum / perlu keputusan Sir
Lihat bahagian "Soalan" dalam mesej sesi 2026-11-17: warna aksen, maskot, logo/ikon kad, video pertama.

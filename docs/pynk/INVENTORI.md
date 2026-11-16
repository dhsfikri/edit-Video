# Inventori Gaya PYNK — skill, plugin, aset (status)

## Skill / alat
| Perkara | Guna | Status |
|---|---|---|
| `director` (projek) | reference → aset → storyboard visual | ✅ ada |
| `hyperframes` + `hyperframes-registry` | render + blok siap (kaunter, kursor, glitch, caption) | ✅ ada |
| `reverse-any-video` | analisis video reference | ✅ ada (ciri "reverse" penuh = HyperFrames Pro) |
| `rembg` (pip) | buang latar gambar → prop | ⚠️ dipasang dalam sesi ini sahaja — perlu masuk setup script environment |
| `yt-dlp`, `opencv`, `faster-whisper` (pip) | download reference, kesan muka, transcribe | ⚠️ sama — perlu setup script |
| Playwright + Chromium | storyboard / mockup | ✅ pra-pasang |

## Blok registry HyperFrames yang dipakai
`number-wheel` (kaunter views), `agent-cursor` (kursor klik), `rgb-glitch-text` (logo glitch), `text-state-swap` (Generate→Generating), `grain-overlay`, `hw-arrow` / `hw-underline` (coretan), `paper-collage-reveal`.

## Aset
| Aset | Sumber | Tempat | Status |
|---|---|---|---|
| Ukiran vintaj domain awam (bangunan, tangan, orang, telefon lama, surat, wang, timbang, pembesar suara, jam, kedai) | Wikimedia Commons (PD) | `aset/vintaj/` (+ `prop/` dipotong) | ⏳ sedang kumpul |
| Tekstur kertas, kertas grid, wang kertas | dijana CSS/SVG + PD | dalam template | ⏳ |
| Mockup chat generik, butang morph, kad post, folder/kad terapung | dibina HTML | `motion/pynk/` | ⏳ |
| Logo Sir (PNG/SVG telus) | **Sir** → Drive `Aset/03 Outro` | `aset/logo/` | ❌ tunggu Sir |
| Font monospace caption | JetBrains Mono / IBM Plex Mono (OFL) | `motion/pynk/assets/` | ⏳ |
| SFX (klik, whoosh, kertas, glitch) | dijana sendiri | `motion/sfx/` | ✅ sebahagian |

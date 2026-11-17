# Ujian EffectCraft 0.10.0 + VectorCraft 0.11.0 (2026-11-17, sesi cloud CPU tanpa GPU)

Projek ujian: `motion/effectcraft/uji_alat.ecproj` (comp `uji_alat`, `uji_fx`, `grade_test`) · prototaip: `motion/effectcraft/proto_split.ecproj`.
Rakaman ujian: C0007 (`_kerja/proto_base.mov`). **EffectCraft hanya baca fail dalam repo → letak media dalam `_kerja/`.**

## EffectCraft
| Ciri | Keputusan | Nota / cara |
|---|---|---|
| Komposisi berlapis, matte bulat, teks font brand | ✅ | `layer.setTrackMatte` |
| Pop-out (kepala keluar bingkai) | ✅ | Latar dibuang dengan `hyperframes remove-background` (bukan Object Matte) |
| Kad 3D flip + perspektif | ✅ | `layer.setSwitch threeD` + `rotationY` keyframe |
| Kamera 3D + spotlight (berbayang) | ✅ | `layer.newCamera`, `layer.newLight` |
| Keyframe + easing, render H.264 + audio | ✅ | 4s ≈ 20–30s render |
| Warp Stabilizer | ✅ | `track.warpStabilizer {wait:true}` (rakaman tripod — beza kecil) |
| Motion tracking + parent | ✅ | `track.new` → `setPoint` → `analyze` → `apply` ke Null → `layer.setParent` label. Label ikut dahi Sir |
| Face tracking — model **MediaPipe** | ✅ | Data licin, kesan kelip mata. **Perlu `face.model.download {id:"mediapipe-face"}` setiap sesi baru** (3.7MB) + `face.model.select` |
| Face tracking — model Classic (bawaan) | ❌ | Data melompat-lompat, tak boleh pakai |
| Chroma key (Key Light) | ✅ | Diuji dengan latar hijau tiruan; tepi rambut green screen sebenar belum diuji |
| Time remap (freeze / slow-mo) | ✅ | `layer.enableTimeRemap` + keyframe `timeRemap` |
| Effect (Gaussian Blur, Glow, Noise) | ✅ | `effect.apply` + `prop.set effects/#n/...` |
| Colour grading Lumetri | ❌ | Hanya Saturation berkesan; Temperature/tint/look hampir tiada kesan → guna FFmpeg (Sir pilih kekal asal) |
| Object Matte (AI potong objek) | ❌ | Lapisan kosong |

## VectorCraft
| Ciri | Keputusan |
|---|---|
| Bentuk + teks Poppins → SVG/PNG | ✅ |
| Path bebas (gelembung chat), gradient, bayang lembut (`stylize.dropShadow`) | ✅ |
| Teks atas laluan melengkung dengan **Kalam** | ✅ |
| Bintang/poligon, garis coretan | ✅ |
| Eksport PNG telus → import EffectCraft (alpha + bayang kekal) | ✅ |
| Bersihkan logo Sir | ⏳ tunggu fail logo |

## Belum diuji
Green screen sebenar · kualiti stabilizer pada rakaman goyang · camera tracker 3D · Lottie import.

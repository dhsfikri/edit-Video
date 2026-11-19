---
name: mula
description: Mula session baru untuk video @adabclosing dengan satu arahan — semak branch, banding Drive Raw dengan LOG-VIDEO, pilih video seterusnya (atau ID yang Sir beri), download, transcribe dan bagi 3 pilihan hook. Guna bila Sir taip "/mula", "/mula C0237", "mula video baru" atau "sambung video seterusnya".
---

# Skill: Mula Session Video (jimat token)

**Versi:** 1.0 (2026-11-19)
**Changelog:**
- 1.0 — Arahan ringkas permulaan session (permintaan Sir: session baru setiap video supaya jimat token).

Argumen: ID video (cth `C0237`). Tiada argumen → ambil video ⏳/🔵 pertama dalam `LOG-VIDEO.md` yang belum ✅/⛔.

## Langkah
1. **Branch:** `git fetch -q origin claude/bold-bardeen-qxp9ue && git checkout claude/bold-bardeen-qxp9ue && git pull -q` (jika branch kerja session lain, gabung dari branch ni dulu). Pastikan `.claude/skills/tiktok-edit/SKILL.md` versi ≥ 2.0 wujud.
2. **Baca SAHAJA:** `CLAUDE.md` (auto dimuat), jadual dalam `LOG-VIDEO.md`, `docs/adabclosing/RESIPI-HARIAN.md`. Skill `tiktok-edit` dibaca bila sampai langkah potong/edit. Jangan baca dokumen rujukan lain kecuali perlu.
3. **Drive:** senarai folder `Raw` (+ subfolder tarikh terbaru) → video baru yang tiada dalam LOG → tambah baris (kunci = ID Drive). Commit.
4. **Video sasaran:** download (skill `tiktok-edit` §1), transcribe (§2). Simpan `projects/<ID>/transcript.json`.
5. **3 pilihan hook** (ikut `hook-lab`, ringkas): setiap satu = ayat pembuka Sir dari transkrip + tajuk poster 3–4 perkataan + idea visual 0–3s. Tandakan 1 sebagai **Cadangan**. Senaraikan perkataan yang tak pasti untuk Sir sahkan. Simpan `projects/<ID>/PLAN.md`, kemas LOG (🔵), commit & push.
6. Tunggu Sir pilih → teruskan skill `tiktok-edit` §3–§9 sampai draf.

## Jimat token (ikut sepanjang session)
- **Satu video = satu session.** Lepas final + thumbnail + caption dihantar, ingatkan Sir: "Video ni siap. Untuk video seterusnya, buka session baru dan taip `/mula`."
- Semakan imej: lembaran kecil (`scale=216:384`, tile 12x6) dan snapshot pada masa penting sahaja; jangan baca frame satu-satu kecuali ada masalah.
- Gabungkan arahan shell dalam satu panggilan; potong output panjang (`tail`, `grep`).
- Jangan baca semula fail besar (scene.js, transcript) bila isinya dah diketahui.
- Render panjang → jalankan di latar belakang, tunggu notifikasi (jangan poll).

#!/usr/bin/env python3
"""Reference dari link: download → contact sheet + potongan scene + transkrip → nota references/.

  python3 -I pipeline/ref.py "<link TikTok/IG/FB/YouTube>" [--nota "apa Sir suka"] [--model small] [--lang en]

- Video disimpan di folder sementara (--kerja, default /tmp/ref) — TIDAK masuk repo.
- Repo hanya simpan: references/<platform>-<id>.md (nota) + references/img/<platform>-<id>.jpg (contact sheet).
- Bahagian "Analisa" dalam nota diisi oleh Claude selepas tengok contact sheet.
- Kalau download gagal "Tunnel connection failed: 403": host CDN belum dibenarkan dalam
  network environment. Skrip cetak nama host → tambah ke Allowed domains.
Perlu: yt-dlp, faster-whisper, ffmpeg (pip install yt-dlp faster-whisper).
"""
import argparse, json, re, subprocess, sys, urllib.parse
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--nota", default="", help="apa Sir suka tentang video ni")
    p.add_argument("--kerja", default="/tmp/ref", help="folder sementara untuk video")
    p.add_argument("--model", default="small", help="model faster-whisper (small/medium)")
    p.add_argument("--lang", default=None, help="bahasa transkrip (ms/en); kosong = auto")
    a = p.parse_args()

    url = re.sub(r"\?.*$", "", a.url) if "tiktok.com" in a.url else a.url
    kerja = Path(a.kerja); kerja.mkdir(parents=True, exist_ok=True)
    ytdlp = [sys.executable, "-m", "yt_dlp", "--no-playlist", "--retries", "2", "-f", "b[ext=mp4]/b"]

    # 1. Metadata (tanpa download) — untuk tahu id + host CDN
    r = run(ytdlp + ["-J", url])
    if r.returncode:
        sys.exit("✗ Gagal baca link:\n" + r.stderr[-600:])
    info = json.loads(r.stdout)
    plat = info.get("extractor_key", "web").lower()
    vid = f"{plat}-{info['id']}"
    hosts = sorted({urllib.parse.urlparse(f["url"]).hostname for f in info.get("formats", []) if f.get("url")})

    # 2. Download video
    mp4 = kerja / f"{vid}.mp4"
    if not mp4.exists():
        r = run(ytdlp + ["-o", str(mp4), url])
        if r.returncode or not mp4.exists():
            msg = "✗ Download gagal."
            if "403" in r.stderr:
                msg += "\n  Host CDN disekat network environment. Tambah ke Allowed domains:\n  " + "\n  ".join(hosts)
            sys.exit(msg + "\n" + r.stderr[-400:])
    print(f"✓ Video: {mp4}")

    # 3. Contact sheet ±36 frame dengan cap masa (video pendek → frame lebih rapat, min 0.5s)
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)]).stdout or 0)
    step = max(0.5, round(dur / 36 * 2) / 2)
    n = max(1, int(dur / step))
    rows = -(-n // 9)
    (REF / "img").mkdir(parents=True, exist_ok=True)
    sheet = REF / "img" / f"{vid}.jpg"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf",
         f"fps=1/{step},scale=200:-1,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=14:fontcolor=red,"
         f"tile=9x{rows}:padding=3", "-frames:v", "1", "-q:v", "4", str(sheet)])
    print(f"✓ Contact sheet: {sheet.relative_to(ROOT)}")

    # 4. Potongan scene (tukar visual) → rentak
    r = run(["ffmpeg", "-hide_banner", "-i", str(mp4), "-vf", "select='gt(scene,0.12)',showinfo", "-f", "null", "-"])
    cuts = []
    for t in re.findall(r"pts_time:([0-9.]+)", r.stderr):
        t = float(t)
        if not cuts or t - cuts[-1] > 0.3:  # gabung pengesanan berturut-turut
            cuts.append(t)
    purata = dur / (len(cuts) + 1) if dur else 0

    # 5. Transkrip
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    m = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=4)
    segs, tinfo = m.transcribe(audio, language=a.lang)
    trans = [f"| {s.start:.1f}–{s.end:.1f}s | {s.text.strip()} |" for s in segs]
    print(f"✓ Transkrip ({tinfo.language}): {len(trans)} segmen")

    # 6. Nota (kalau run semula: kekalkan Analisa + "Sir suka" yang sedia ada)
    nota = REF / f"{vid}.md"
    analisa = "_(isi: struktur hook, layout, gaya teks, B-roll/motion, bunyi, CTA, apa nak pinjam, apa tak sesuai untuk Sir)_"
    if nota.exists():
        lama = nota.read_text()
        if "## Analisa (Claude)\n" in lama:
            analisa = lama.split("## Analisa (Claude)\n", 1)[1].strip()
        m_suka = re.search(r"\*\*Sir suka:\*\* (.*)", lama)
        if not a.nota and m_suka:
            a.nota = m_suka.group(1).strip()
    desc = (info.get("description") or "").replace("\n", " ")
    stat = " · ".join(f"{k} {info[k]:,}" for k in ("view_count", "like_count", "comment_count", "repost_count", "save_count") if info.get(k))
    nota.write_text(f"""# Reference: {info.get('uploader') or info.get('channel') or ''} — {info.get('title','')[:70]}

- **Link:** {a.url}
- **Tarikh simpan:** {date.today()} · **Durasi:** {dur:.1f}s · **Resolusi:** {info.get('width')}x{info.get('height')}
- **Statistik (masa simpan):** {stat or '-'}
- **Caption asal:** {desc[:400]}
- **Sir suka:** {a.nota if a.nota and a.nota != '_(isi)_' else '_(isi)_'}

![contact sheet](img/{vid}.jpg)

## Rentak
- Tukar visual (potongan keras) dikesan: **{len(cuts)} kali** → purata **{purata:.1f}s** setiap visual
- Titik: {', '.join(f'{c:.1f}' for c in cuts) or '-'}\n- Contact sheet: 1 frame setiap {step}s. Nota: animasi berterusan (motion graphic) jarang dikesan sebagai potongan — rujuk contact sheet.

## Transkrip
| Masa | Ayat |
|---|---|
""" + "\n".join(trans) + """

## Analisa (Claude)
""" + analisa + "\n")
    print(f"✓ Nota: {nota.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

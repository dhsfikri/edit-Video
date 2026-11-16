#!/usr/bin/env bash
# Gabung video + audio, normalkan 2-pass ke -14 LUFS, puncak ≤ -2 dBTP.
# Guna: bash mux.sh <video.mp4> <audio.wav> <out.mp4>
set -euo pipefail
V="$1"; A="$2"; OUT="$3"
M=$(ffmpeg -hide_banner -i "$A" -af loudnorm=I=-14:TP=-2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
AF="loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true"
ffmpeg -v error -y -i "$V" -i "$A" -map 0:v -map 1:a -c:v copy \
  -af "$AF,alimiter=limit=0.63:level=false" -c:a aac -b:a 192k -ar 48000 \
  -shortest -movflags +faststart "$OUT"

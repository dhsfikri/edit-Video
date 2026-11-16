#!/usr/bin/env bash
# Build iklan Setup Team Sales: muzik → video (frame demi frame) → gabung + normal -14 LUFS
# Guna: bash build.sh <out.mp4>
set -euo pipefail
cd "$(dirname "$0")"
OUT="${1:?beri laluan output .mp4}"
TMP="$(mktemp -d)"
[ -d node_modules ] || npm install --silent
python3 music.py "$TMP/music.wav"
node render.mjs "$TMP/video.mp4" 30 15
bash mux.sh "$TMP/video.mp4" "$TMP/music.wav" "$OUT"
rm -rf "$TMP"
echo "siap: $OUT"

#!/usr/bin/env bash
# Pregătește vocea și cadrele Ellei dintr-un clip video local.
# Utilizare: bash ella-decoflair/scripts/pregatire_media.sh <video> [dir-iesire]
set -euo pipefail
IN="${1:?da calea catre video}"
OUT="${2:-$(dirname "$0")/../media}"
mkdir -p "$OUT/voce" "$OUT/cadre" "$OUT/sursa"
cp -n "$IN" "$OUT/sursa/" 2>/dev/null || true

ffmpeg -hide_banner -loglevel error -y -i "$IN" -vn -ac 1 -ar 44100 "$OUT/voce/ella-voce-44k-mono.wav"
ffmpeg -hide_banner -loglevel error -y -i "$OUT/voce/ella-voce-44k-mono.wav" \
  -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 44100 -ac 1 "$OUT/voce/ella-voce-curata.wav"
ffmpeg -hide_banner -loglevel error -y -i "$IN" -vf "fps=1" -q:v 2 "$OUT/cadre/cadru-%02d.jpg"

{
  echo "Sursa: $(basename "$IN")"
  ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,sample_rate -of default=nw=1 "$IN"
  echo "--- nivel audio curatat"
  ffmpeg -hide_banner -i "$OUT/voce/ella-voce-curata.wav" -af ebur128 -f null - 2>&1 | grep -E "I:|LRA:" | tail -2
} > "$OUT/info.txt"
echo "Gata -> $OUT"; cat "$OUT/info.txt"

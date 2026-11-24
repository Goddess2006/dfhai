#!/usr/bin/env bash
# Generează un MP3 de test cu vocea clonată a Ellei (ElevenLabs).
# Necesită în .env (local, necomis): ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID_ELLA
set -euo pipefail
cd "$(dirname "$0")/../.."
set -a; [ -f .env ] && . ./.env; set +a
TEXT="${1:?textul de citit}"
OUT="${2:-ella-decoflair/media/voce/test-$(date +%Y%m%d-%H%M%S).mp3}"
mkdir -p "$(dirname "$OUT")"
python3 - "$TEXT" > /tmp/ella_req.json <<'PY'
import json,sys
print(json.dumps({"text":sys.argv[1],"model_id":"eleven_multilingual_v2",
 "voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.15,"use_speaker_boost":True}}))
PY
curl -sS -f -X POST "https://api.elevenlabs.io/v1/text-to-speech/${ELEVENLABS_VOICE_ID_ELLA}" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" -H "Content-Type: application/json" \
  --data @/tmp/ella_req.json -o "$OUT"
echo "Salvat: $OUT"

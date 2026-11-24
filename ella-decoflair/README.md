# Ella — personajul-expert decoflair.ro

- `PERSONA.md` — cine e Ella, expertiza, tonul, reguli de folosire (acord, aprobare, etichetare AI).
- `VOCE-SI-IMAGINE.md` — cum se salvează vocea și imaginea, clonare voce (ElevenLabs), avatar, glosar de pronunție.
- `scripts/pregatire_media.sh <video>` — extrage voce curată (WAV) + cadre de referință în `media/`.
- `scripts/voce_test.sh "text"` — generează voce off cu clona Ellei.
- `media/` — **ignorat de git** (date biometrice: voce, față). Copia permanentă: `BAZE/ELLA/`.

Stare (24.11.2026): profil creat; clipul TikTok nu a putut fi descărcat din sesiunea cloud → de pus fișierul video în `media/sursa/` sau `BAZE/ELLA/sursa/` și rulat scriptul.

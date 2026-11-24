# Vocea și imaginea Ellei — cum le salvăm și cum le folosim

## 1. Materialul sursă
Pune clipul original (cel mai bine fișierul de pe telefon, nu cel descărcat de pe TikTok — e la calitate mai mare și fără muzică) în:
- local: `/home/dfh/workspace/BAZE/ELLA/sursa/` **sau** `ella-decoflair/media/sursa/` (ambele ignorate de git).

Pentru o clonă de voce bună mai sunt utile (opțional, dar recomandat):
- **1–3 minute** de vorbire curată (fără muzică, fără ecou), ideal 2–3 înregistrări în care Ella explică un produs, natural.
- Pentru o clonă „profesională” (ElevenLabs PVC): **30 min+** de audio curat.
- Pentru imagine: 10–20 fotografii clare ale feței (față, ¾, profil, lumină naturală), 2–3 ținute de brand.

## 2. Pregătire automată
```bash
bash ella-decoflair/scripts/pregatire_media.sh <cale-video>
```
Rezultă în `ella-decoflair/media/`:
- `voce/ella-voce-44k-mono.wav` — audio întreg, mono 44,1 kHz
- `voce/ella-voce-curata.wav` — filtrat (high-pass 80 Hz, reducere zgomot, normalizare −16 LUFS) → **acesta se urcă pentru clonare**
- `cadre/cadru-XX.jpg` — 1 cadru pe secundă la rezoluție maximă, pentru alegerea pozelor de referință
- `info.txt` — durată, rezoluție, nivel audio

## 3. Clonarea vocii (o singură dată)
Recomandat: **ElevenLabs** (suportă bine româna, model `eleven_multilingual_v2`).
1. Cont decoflair.ro → *Voices → Add voice → Instant Voice Clone* (sau *Professional* cu 30 min+).
2. Urcă `ella-voce-curata.wav` (+ celelalte înregistrări curate).
3. Nume: `Ella – decoflair.ro`; bifează declarația că ai drepturile (Ella e chiar titulara vocii).
4. Notează **voice_id** în `.env` local (NU în git): `ELEVENLABS_VOICE_ID_ELLA=...`, `ELEVENLABS_API_KEY=...`.
5. Setări pornire: stability 0,45 · similarity 0,80 · style 0,15 · speaker boost ON.
6. Test: `bash ella-decoflair/scripts/voce_test.sh "Bună, eu sunt Ella de la Deco and Flair. Hai să-ți arăt cum alegi cornișa potrivită."`

Alternative: Resemble.ai, PlayHT; local/open-source: XTTS-v2 (calitate mai slabă pe română).

## 4. Imaginea
- **Filmare reală** rămâne varianta cea mai credibilă (fără aspect AI — cerința constantă a clientului).
- Pentru avatar video (HeyGen „Instant Avatar” / Synthesia „Personal Avatar”): 2–5 min de filmare cu Ella privind în cameră, fundal liniștit, lumină frontală; platforma cere și o **înregistrare video de consimțământ** a Ellei.
- Cadrele din `media/cadre/` servesc ca referință vizuală (ținută, păr, stil) pentru brieful Codex / generări de imagine — **doar** în materiale aprobate de Ella.

## 5. Pronunție (glosar pentru TTS)
| Scris | Se citește |
|---|---|
| Deco & Flair | „Deco end Fler” |
| decoflair.ro | „deco-fler punct ro” |
| NMC | „en-em-ce” |
| LED | „led” |
| ADRo | „a-de-ro” |
| PU | „poliuretan” (scrie cuvântul întreg în text) |

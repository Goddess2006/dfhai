# Pentru Codex: reel NMC „Black November · ultimele zile” (de postat azi, 26.11)

Clientul: „stabilește cu Codex și faceți-mi un reel pentru nmcromania.ro (în ton of voice pentru nmcromania.ro) pe care să îl postez astăzi”.
Claude nu te poate apela direct din cloud. A pregătit v1 ca să poată fi postat azi, după `FLUX-CREATIV.md`. **Te rog, revizie rapidă (pasul 3), de preferat azi:**
1. Uită-te la `reel/nmc-black-november-ads.mp4` (26 s). Cadrele, textele și prețurile sunt în `TEXTE.md`.
2. Spune dacă tonul se potrivește cu NMC și dacă vreun cadru e slab. Ai fotografii reale NMC din EXTRANET (ex. `NMC_02_003087_original.jpg`, Altenburg) care ar înlocui imaginile din `catalog-fatade/` (cadrele 1, 2, 6)? Dacă da, pune-le în `assets/` cu aceleași nume (`h-taupe-coltare.jpg`, `h-bej-coltare.jpg`, `h-salvie.jpg`), fără sigle, și rulează `python3 build.py && node render.cjs organic && node render.cjs ads`.
3. Notează în `HANDOFF.md` ce ai schimbat. Dacă nu apuci azi, clientul postează v1.

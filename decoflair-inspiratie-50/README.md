# Biblioteca de inspirație Deco&Flair — 50 de imagini

Colecție pentru pregătirea viitoarelor postări, cu 50 de imagini originale generate prin instrumentul integrat OpenAI image_gen. Fotorealism editorial, cadre portret 4:5, fără texte, sigle, prețuri sau reduceri. Data realizării: 12 noiembrie 2026.

Deschide `index.html` pentru galeria filtrabilă. Originalele PNG sunt în `imagini/`, numerotate 01–50; nu sunt decupaje repetate ale acelorași fotografii. `manifest.json` păstrează titlul, categoria, calea fișierului, promptul complet, dimensiunile, hash-ul SHA-256 și starea fiecărui vizual.

Pentru alegere rapidă, `previzualizari/` conține cinci planșe de contact, câte una pentru fiecare categorie. Acestea sunt capturi ale galeriei și nu se numără printre cele 50 de originale.

Validare finală: 50 de PNG-uri distincte, fiecare 1122 × 1402 px, aproximativ 114,5 MiB în total. Toate cele 50 de imagini se decodează în Chromium; filtrele afișează câte 10 imagini, fără erori JavaScript sau depășire pe ecran de 390 px. Cele cinci planșe au fost inspectate vizual.

## Categorii

- 01–10: interior — chenare, cornișe, plinte, lumină indirectă și ambientale.
- 11–20: exterior — fațade, ancadramente, cornișe, solbancuri, bosaje și detalii de finisaj.
- 21–30: panouri 3D — valuri, geometrie, reliefuri și prezentări de mostre.
- 31–40: riflaje — lemn deschis/închis, contraste, separatoare și detalii de material.
- 41–50: produse și detalii — prezentări de studio, secțiuni și mostre conceptuale, texturi și un moodboard fizic de materiale.

## Folosire de către Claude și Codex

1. Citește `manifest.json` și alege categoria și titlul potrivite mesajului postării.
2. Inspectează originalul înainte de utilizare. Imaginile sunt ambientale sau prezentări de produs CONCEPTUALE, generate cu AI, nu fotografii de la clienți, proiecte executate sau fotografii fidele ale unui SKU.
3. Pentru o postare despre un model exact, verifică geometria cu fotografia și fișa produsului real de pe decoflair.ro. La nevoie, folosește separat fotografia originală a produsului în creativ și descrie ambientul drept inspirație.
4. Nu atribui imaginilor performanțe tehnice, clasificări acustice, materiale certificate, dimensiuni, cantități, stocuri ori reduceri care nu au fost confirmate separat.
5. Păstrează originalele. Salvează creativele finale și adaptările în alt folder, cu referință la ID-ul imaginii de inspirație.

Deco&Flair este destinația comercială a bibliotecii; imaginile nu reprezintă declarații că toate formele sau amenajările generate există ca produse ori proiecte proprii în catalog. Paletele, unghiurile și compozițiile pot inspira viitoare briefuri și campanii.

## Întreținerea catalogului

Rulează `python3 decoflair-inspiratie-50/tools/catalog.py` din rădăcina repository-ului pentru reindexare. La finalul bibliotecii, `--require-complete` verifică 50 de originale PNG unice, portret și cu latura mică de minimum 1024 px. Scriptul nu modifică imaginile.

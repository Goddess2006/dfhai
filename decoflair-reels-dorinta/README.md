# Seria „Dorință” — Deco&Flair (noiembrie 2026)

Cererea clientului: reels noi, cu alte produse de pe decoflair.ro, care **să nu pară făcute cu AI**, cu ambient cald, care să trezească dorința de a cumpăra, construite pe modelul celor mai bune reclame din lume și realizate împreună cu Codex.

**Principiu:** doar fotografii reale: cataloagele producătorilor (Dolce & Gabbana, Roberto Cavalli, Emiliana), portofoliul decoflair.ro și fotografiile NMC. Ritm lent, tranziții prin ceață, **paleta și sigla originală Deco&Flair** (auriu `#C2A15E` / `#E2CB94` pe cărbune `#141210`). Afirmațiile sunt adevărate: prețuri și stocuri citite pe site la 24.11.2026, fără urgență falsă.

| Reel | Produse | Reper | Fișiere |
|---|---|---|---|
| **„Haute couture pentru pereți”** (32,8 s) | Tapet Dolce & Gabbana (panou 3×3 m, 6.534 lei), Roberto Cavalli (panou 3.630 lei; rolă de la 1.064 lei), Emiliana (484 lei/rolă) | Filmele de modă Chanel/Dior + ritmul Guinness „Surfer” | `reel/decoflair-lux-{organic,ads}.mp4` |
| **„Casa în care se întorc toți”** (32,8 s) | Cornișă LED IL18 (217 lei, 92 buc.), rozetă R15 (413 lei, 5 buc.), brâu WO2 (59 lei, 126 buc.) | John Lewis (Crăciun), Edeka „#heimkommen”, Apple „The Surprise” | `reel/decoflair-craciun-{organic,ads}.mp4` |

Rulare: `python3 engine.py configs/<reel>.py && node render.cjs <reel> organic && node render.cjs <reel> ads`. Previzualizare: `node preview.cjs <reel> ads 2,8,15`.
Reel nou = fișier nou în `configs/` (scene: imagine, încadrare, replici cu `*cuvinte evidențiate*`, etichetă produs, durată).

## Cele 10 repere și ce am luat din fiecare
| # | Reclama (an) | De ce a funcționat | Ce am preluat |
|---|---|---|---|
| 1 | **Apple „1984”** (1984) | Un singur gest care schimbă tot, cu un dușman clar | „Casa banală” e dușmanul; un singur detaliu o schimbă |
| 2 | **Volkswagen „Think Small”** (1959) | Onestitate, autoironie, adevăr spus simplu | Prețuri reale, inclusiv „de la 484 lei”: fără exagerări |
| 3 | **IKEA „Lamp”**, Spike Jonze (2002) | Obiectele „simt”; umor care întoarce emoția | Casa/camera care vorbește (reel-urile v3) |
| 4 | **Guinness „Surfer”** (1999) | „Good things come to those who wait”: ritm lent, ritual | Ritmul lent, tranzițiile prin ceață |
| 5 | **Chanel N°5 / filmele de modă Dior** | Dorința se construiește prin atmosferă, nu prin argumente | „Haute couture pentru pereți”: lux pe negru și auriu |
| 6 | **John Lewis, reclamele de Crăciun** (2011–) | Emoția dăruirii și a așteptării | „Anul ăsta, toată familia vine la tine.” |
| 7 | **Edeka „#heimkommen”** (2015) | Dorul de casă, momentul întoarcerii | Finalul: „Fă-ți casa în care vor să se întoarcă.” |
| 8 | **Old Spice „The Man Your Man Could Smell Like”** (2010) | Aspirație + umor, adresare directă către privitor | „Psst… tu.”, adresarea directă |
| 9 | **Dove „Real Beauty Sketches”** (2013) | Cum ne vedem vs. cum ne văd alții | „Ce văd când intră pe ușă?”, „Cine v-a amenajat?” |
| 10 | **Nike „Dream Crazy”** (2018) | Aspirație, a te vedea mai mare | „Și visul începe de la 484 lei.”: accesul la lux |

## Lucrul cu Codex (conform `FLUX-CREATIV.md`)
Codex nu este accesibil din sesiunea cloud a lui Claude. Colaborarea trece prin repo și `HANDOFF.md`. Cererea concretă: `CODEX-BRIEF.md`.

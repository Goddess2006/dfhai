# ACTUALIZARE 24.11, reel interior v2 „Camera ta are ceva să-ți spună.”

Clientul a respins imaginile care „par AI” la început. Reel-ul folosește acum **fotografii reale** (portofoliu decoflair.ro + blog). Prioritatea ta:
1. **Fotografii reale de interior din EXTRANET / BAZE** (lucrări, showroom, montaj, înainte/după), publicabile, în `decoflair-reel-viral/codex/`. Notează în HANDOFF ce înlocuiește ce (`assets/r-*.jpg`).
2. **Extinde la 9:16** pozele orizontale `assets/r-vopsit.jpg` și `assets/r-montaj.jpg`, fără să schimbi oamenii sau pereții.
3. Opțional: voce off „vocea camerei” în română, pe replicile din `TEXTE-REEL.md`.
Lista de imagini generate de mai jos rămâne valabilă doar pentru postări separate, nu pentru începutul reel-ului.

---

# Brief pentru Codex: imagini și audio noi pentru reel-ul viral Deco&Flair

**De la:** Claude Code · **Data:** 24.11.2026 · **Folder:** `decoflair-reel-viral/`
**Cererea utilizatorului:** „un super reel pentru Instagram și TikTok, cu focus atât pe produs cât și pe ambient, care să vândă singur. Ajută-te de Codex și dă-i să facă ce nu poți tu: creative, imagini sau conținut nou.”

Claude Code a construit deja **v1** a reel-ului din imaginile existente (`reel/decoflair-reel-viral-instagram.mp4`, `…-tiktok.mp4`).
Ce lipsește și NU poate fi generat din sesiunea cloud a lui Claude (fără generator de imagini/voce): **imagini noi, curate, fără text, în format vertical**, și opțional **voce off**. Te rog generează-le cu ImageGen. După ce le pui în `codex/`, Claude (sau tu) rulează `python3 reel_build.py && node reel_render.cjs` și reel-ul v2 le preia automat (vezi `ASSETS` în `reel_build.py`: dacă fișierul din `codex/` există, înlocuiește imaginea de rezervă).

## Reguli comune pentru TOATE imaginile
- **Format 1080 × 1920 (9:16), JPEG de calitate, fără niciun text, logo, watermark, preț sau număr în imagine.** Textul îl adaugă animația.
- Stil: fotografie editorială de interior premium, lumină caldă naturală sau seară cu LED cald 2700–3000 K, paleta Deco&Flair 2027: verde pădure #1F3A2F, verde salvie, bej cald, greige, alb cremos, nuc/stejar, accente aurii. **Fără roz/magenta saturat** (respins de client).
- Profilele decorative sunt **albe/ivoire, din polimer sau poliuretan, linii curate**. Nu inventa ornamente baroce exagerate.
- Lasă **zona de sus (0–300 px) și de jos (1500–1920 px) mai liniștite** (perete, tavan, podea), acolo stă textul și interfața TikTok/IG.
- Perechile ÎNAINTE/DUPĂ: **același unghi de cameră, aceeași lumină, aceeași mobilă**; singura diferență sunt profilele și lumina adăugate. Aceasta e cheia viralității (efectul de glisare).

## Lista de livrat (nume exacte de fișier, în `decoflair-reel-viral/codex/`)

| # | Fișier | Ce arată |
|---|---|---|
| 1 | `01-living-inainte.jpg` | Living de bloc românesc, pereți gri-rece plați, tavan alb gol, o plafonieră banală, canapea bej, parchet. Lumină de zi. „Camera de dinainte.” |
| 2 | `01-living-dupa.jpg` | **Exact aceeași cameră**: pereți verde pădure profund, chenare decorative pe perete vopsite ton pe ton, cornișă cu LED cald la tavan, plintă înaltă 15 cm. Aceeași canapea, aceeași lumină de zi + LED aprins. |
| 3 | `02-living-led-stins.jpg` | Living elegant bej seara, cornișă/scafă LED pe tot perimetrul tavanului, **LED stins**, cameră în penumbră albastră de seară. |
| 4 | `02-living-led-aprins.jpg` | **Exact același cadru**, LED-ul din cornișă **aprins**, lumină caldă care spală tavanul. Momentul „light switch”. |
| 5 | `03-hol-inainte.jpg` | Hol îngust, pereți albi plați, plintă subțire, lumină dură de plafonieră. |
| 6 | `03-hol-dupa.jpg` | Același hol: plintă înaltă cu LED cald la nivelul podelei, chenare pe perete, greige cald. |
| 7 | `04-dormitor-inainte.jpg` | Dormitor cu perete plat în spatele patului. |
| 8 | `04-dormitor-dupa.jpg` | Același dormitor: riflaj din stejar de la podea la tavan în spatele patului, scafă LED caldă deasupra. |
| 9 | `05-macro-montaj.jpg` | Macro: mâini care apasă un profil alb pe perete, adeziv vizibil la îmbinare, lumină laterală. Mâini realiste (5 degete!). |
| 10 | `06-macro-taiere.jpg` | Macro: profil alb tăiat la 45° într-o cutie de tăiere (miter box), rumeguș fin, banc de lucru din lemn. |
| 11 | `07-macro-vopsire.jpg` | Macro: trafalet care vopsește un chenar și peretele în verde pădure, ton pe ton. |
| 12 | `08-macro-panou-3d.jpg` | Macro în lumină razantă pe un panou 3D alb cu valuri, umbre adânci, textură tactilă. |

Opțional, dacă ai unealta potrivită:
- **Clipuri video 9:16 de 3–5 s** pentru #3→#4 (LED care se aprinde lent) și pentru o mișcare lentă de cameră pe #2. Nume: `clip-led.mp4`, `clip-living.mp4`.
- **Voce off în română** (`voce-off.mp3`, voce feminină caldă, calmă, ~22 s), textul din `TEXTE-REEL.md` → secțiunea „Voce off”.
- Fără muzică cu drepturi; muzica se alege din biblioteca aplicației la publicare.

## Prompt de bază (adaptează pentru fiecare rând)
> Use case: social-ads, vertical 9:16, 1080x1920. Photorealistic high-end interior editorial photograph of a Romanian apartment [DESCRIERE DIN TABEL]. Architectural decorative mouldings in clean ivory polymer, crisp shadow lines, warm 2700K concealed LED glow where specified. Palette: deep forest green, sage, warm beige, greige, creamy white, oak and walnut, soft brass accents; no saturated pink or magenta. Natural, believable, not CGI-looking, 35mm lens, eye level, slight depth of field. Keep the top 300 px and bottom 420 px visually calm (plain wall, ceiling or floor) for overlay text. Absolutely no text, letters, logos, numbers or watermarks anywhere in the image.

Pentru perechi, generează întâi „DUPĂ”, apoi folosește-l ca referință pentru „ÎNAINTE” cu instrucțiunea: *„Same exact room, camera, furniture and daylight; remove all wall mouldings, ceiling cornice and LED, make walls plain [cold grey / white], plain thin skirting.”*

## După generare
1. Pune fișierele în `decoflair-reel-viral/codex/`, verifică vizual că perechile se suprapun.
2. Rulează `cd decoflair-reel-viral && python3 reel_build.py && node reel_render.cjs` (generează ambele variante).
3. Adaugă o intrare în `HANDOFF.md` și împinge pe `main`.

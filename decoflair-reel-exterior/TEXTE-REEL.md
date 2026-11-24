# Reel exterior Deco&Flair v2: „Schița devine casă”

**v2 (24.11.2026, la cererea clientului):** fără zăpadă, concept complet nou, final cu site-ul centrat în stil reclamă „din 2030”. Varianta cu zăpada (v1) rămâne în istoricul git (`reel_build_v1_zapada.py`).

Fișiere (1080×1920, 23 s, 30 fps, fără sunet):
- `reel/decoflair-reel-exterior-organic.mp4`: postare organică (finalul are „Link în bio”).
- `reel/decoflair-reel-exterior-ads.mp4`: pentru reclame. Finalul e curat, fără text în zona butonului „Cumpără acum”.
- `reel/coperta.jpg` (schița cu profilele) și `reel/final-2030.jpg` (cadrul final).

## Povestea, secundă cu secundă
| Timp | Ce se vede |
|---|---|
| 0–2,4 s | Tipografie cinetică pe verde închis: „Casa ta e frumoasă.” → „Lipsesc doar **5** detalii.” (cifra 5 pulsează) |
| 2,4–11,6 s | **Plan tehnic animat**: fațada P+1 se desenează linie cu linie pe grilă, apoi cele 5 profile se „montează” pe rând, cu strălucire aurie: cornișă NC104 (194 lei) → colțar NCL107 (248 lei) → ancadrament NA102 (71 lei) → solbanc NS110 (118 lei) → cheie de boltă NCB104 (87 lei). Fiecare are numele mare și un card cu poza reală și prețul. |
| 11,6–14,4 s | O linie de lumină scanează ecranul și schița devine **casa reală**, în lumină aurie: „Din schiță. Pe casa ta.” |
| 14,4–18,2 s | Panou de comandă cu contoare care se numără: **2.135 colțare · 1.733 ancadramente · 519 chei de boltă** în stoc → „Livrare în 3–5 zile” · „Gata de sărbători” |
| 18,2–23 s | **Final 2030**: negru profund, particule care converg într-o orbită, inel de lumină care se extinde, fascicul care traversează, **decoflair.ro** centrat, metalic, cu reflex de lumină care trece peste litere → „Detaliile care fac casa.” · „Profile de exterior · din stoc” |

## Ce am preluat din video-ul NMC și ce am schimbat
| NMC (short „Colțar decorativ fațade”, 21 s) | Deco&Flair |
|---|---|
| Prezentator în cadru, vorbește lângă colțar | **Fără actor**: produsul e eroul (studio → casă) |
| Pastile portocalii „FĂRĂ ÎMBINĂRI”, „ELEGANT”… | Nume de produs mari, numerotate 01–05, cu card de preț și poza reală |
| Problemă → soluție → rezistență ADRo Quartz → „comandă de la producător” | Lipsă („5 detalii”) → **profilele se montează pe schiță, cu prețuri reale** → casa reală → **stoc real** → final de brand |
| Un singur produs | NCL107 + ancadrament NA102, solbanc NS110, cheie de boltă NCB104, cornișă NC104 |

## Cifrele din video (verificate pe decoflair.ro la 24.11.2026)
| Produs | Preț cu TVA | În stoc |
|---|---|---|
| Colțar NCL107 300/300×30×1000 | 248,09 lei/buc | 2.135 buc. |
| Ancadrament NA102 95×30×2000 | 71,06 lei | 1.733 buc. |
| Solbanc NS110 120×90×2000 | 118,83 lei | 265 buc. |
| Cheie de boltă NCB104 | 87,28 lei | 519 buc. |
| Cornișă NC104 220×80×2000 | 194,74 lei | 185 buc. |

Livrare: „Livrare în 3–5 zile”. Acesta e termenul de pe pagina Plată și livrare pentru profile de exterior în stoc (flota proprie). **Nu am scris „livrare imediată”**, pentru că pe site apare 3–5 zile. Dacă aveți livrare în 24 h pentru anumite zone, schimbă textul pastilei `g1` în `reel_build.py` și randează din nou.
**Înainte de a promova, verifică stocurile și prețurile:** se schimbă, iar reclama poate rula săptămâni.

## Descriere organică (Instagram / Facebook)
> Casa ta e frumoasă. Lipsesc doar 5 detalii. ✨
> 01 Cornișă · 02 Colțar cu bosaje · 03 Ancadrament · 04 Solbanc · 05 Cheie de boltă
> Toate din stoc: 2.135 colțare, 1.733 ancadramente, 519 chei de boltă.
> 📦 Livrare în 3–5 zile sau ridicare din Domnești, Ilfov · Gata înainte de sărbători
> 💬 Consultanță gratuită: 0765 740 280 · 🔗 decoflair.ro
>
> #fatada #fatadacasa #profiledecorative #renovarecasa #casaromaneasca #ancadramente #coltare #cornisa #amenajareexterioara #decoflair

**TikTok:** „De la schiță la casă în 20 de secunde 📐✨ Care detaliu îi lipsește casei tale? 1–5 👇 #fatada #casa #renovare #profiledecorative #romania #fyp”
**Comentariu fixat:** „Trimite-ne o poză cu fațada în DM: îți spunem ce profile i se potrivesc și câte bucăți îți trebuie 📐”

## Reclame (Meta Ads Manager / TikTok Ads)
- **Video:** `…-ads.mp4`. Plasamente: Reels, Stories, TikTok In-Feed. Pentru Feed 4:5, Meta decupează automat; textul important e centrat.
- **Obiectiv:** *Vânzări* (dacă pixelul Meta e pe decoflair.ro) sau *Trafic*. **Buton:** „Cumpără acum”.
- **Link:** `https://decoflair.ro/profile-decorative-exterior?utm_source=meta&utm_medium=paid&utm_campaign=exterior-sarbatori-2026&utm_content=reel-schita-casa` (TikTok: `utm_source=tiktok`).
- **Text principal (125 caractere):** „Casa ta e frumoasă. Lipsesc doar 5 detalii. Cornișe, colțare, ancadramente și solbancuri din stoc, livrate în 3–5 zile.”
- **Titlu:** „Profile de exterior din stoc” · **Descriere:** „Consultanță gratuită · decoflair.ro”
- **Public:** România, 30–60 ani, interese: construcții, renovare, case, grădină, materiale de construcții. Dacă flota livrează doar în anumite zone, restrânge publicul la acele județe. **Buget de test:** 50–80 lei/zi, 5–7 zile, apoi crește setul cu cel mai mic cost pe click.
- **După sărbători:** schimbă pastila „Gata de sărbători” (de ex. cu „Pregătește fațada pentru primăvară”) și randează din nou.

## Notă despre imagini și drepturi
- Casa reală din final e din biblioteca de inspirație generată digital pentru Deco&Flair, deci e sigur pentru reclame. Imaginile de produs sunt cele de pe decoflair.ro.
- **Nu am folosit** fotografiile din `catalog-fatade/` (case românești): proveniența lor nu e declarată și trebuie confirmate drepturile înainte de reclame plătite.
- O fotografie nouă, mai credibilă (casă românească P+1 în lumină aurie, cu exact cele 5 profile din schiță), sunt comandate lui Codex în `CODEX-BRIEF.md`. Reel-ul le preia automat la următoarea randare.

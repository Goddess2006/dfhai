# Reel exterior Deco&Flair: „Ultimul final touch înainte de prima zăpadă”

Fișiere (1080×1920, 25 s, 30 fps, fără sunet):
- `reel/decoflair-reel-exterior-organic.mp4`: postare organică Instagram/TikTok/Facebook (final cu „link în bio”).
- `reel/decoflair-reel-exterior-ads.mp4`: pentru reclame (Meta Reels/Stories, TikTok In-Feed). Ultimele 4 s lasă liberă partea de jos pentru butonul „Cumpără acum”.
- `reel/coperta.jpg`: coperta (eroul de produs NCL107).

## Ce am preluat din video-ul NMC și ce am schimbat
| NMC (short „Colțar decorativ fațade”, 21 s) | Deco&Flair |
|---|---|
| Prezentator în cadru, vorbește lângă colțar | **Fără actor**: produsul e eroul (studio → casă) |
| Pastile portocalii „FĂRĂ ÎMBINĂRI”, „ELEGANT”… | Pastile verzi Deco&Flair: *Debitat în L · Ascunde muchiile imperfecte · Rășină + nisip cuarțos · Rezistă la îngheț și UV* (din fișa produsului) |
| Problemă → soluție → rezistență ADRo Quartz → „comandă de la producător” | Problemă → soluție → **stoc real + preț** → alte 4 „final touch”-uri → **urgență sezonieră** (prima zăpadă, sărbători) → comandă |
| Un singur produs | NCL107 + ancadrament NA102, solbanc NS110, cheie de boltă NCB104, cornișă NC104 |

## Cifrele din video (verificate pe decoflair.ro la 24.11.2026)
| Produs | Preț cu TVA | În stoc |
|---|---|---|
| Colțar NCL107 300/300×30×1000 | 248,09 lei/buc | 2.135 buc. |
| Ancadrament NA102 95×30×2000 | 71,06 lei | 1.733 buc. |
| Solbanc NS110 120×90×2000 | 118,83 lei | 265 buc. |
| Cheie de boltă NCB104 | 87,28 lei | 519 buc. |
| Cornișă NC104 220×80×2000 | 194,74 lei | 185 buc. |

Livrare: „Din stoc · livrare în 3–5 zile”. Acesta e termenul de pe pagina Plată și livrare pentru profile de exterior în stoc (flota proprie). **Nu am scris „livrare imediată”**, pentru că pe site apare 3–5 zile. Dacă aveți livrare în 24 h pentru anumite zone, schimbă `DELIVERY` în `reel_build.py` și randează din nou.
**Înainte de a promova, verifică stocurile și prețurile:** se schimbă, iar reclama poate rula săptămâni.

## Descriere organică (Instagram / Facebook)
> Prima zăpadă vine. Fațada ta e gata? ❄️
> Ultimul final touch al anului, din stoc:
> ▫️ Colțar NCL107: ascunde muchiile imperfecte, rezistă la îngheț și UV (2.135 buc. în stoc)
> ▫️ Ancadramente · solbancuri · chei de boltă · cornișe
> 📦 Livrare în 3–5 zile sau ridicare din Domnești, Ilfov
> 💬 Consultanță gratuită: 0765 740 280
> 🔗 decoflair.ro/profile-decorative-exterior
>
> #fatada #fatadacasa #profiledecorative #renovarecasa #casaromaneasca #ancadramente #coltare #cornisa #amenajareexterioara #decoflair

**TikTok:** „Fațada gata înainte de prima zăpadă ❄️ Ce detaliu îi lipsește casei tale? #fatada #casa #renovare #profiledecorative #romania #fyp”
**Comentariu fixat:** „Trimite-ne o poză cu fațada în DM și îți spunem ce profile i se potrivesc și câte bucăți îți trebuie 📐”

## Reclame (Meta Ads Manager / TikTok Ads)
- **Video:** `…-ads.mp4`. Plasamente: Reels, Stories, TikTok In-Feed. Pentru Feed 4:5, Meta decupează automat; textul important e centrat.
- **Obiectiv:** *Vânzări* (dacă pixelul Meta e pe decoflair.ro) sau *Trafic*. **Buton:** „Cumpără acum”.
- **Link:** `https://decoflair.ro/profile-decorative-exterior?utm_source=meta&utm_medium=paid&utm_campaign=exterior-iarna-2026&utm_content=reel-final-touch` (TikTok: `utm_source=tiktok`).
- **Text principal (125 caractere):** „Prima zăpadă vine. Colțare, ancadramente și cornișe din stoc, livrate în 3–5 zile. Fațada gata de sărbători.”
- **Titlu:** „Profile de exterior din stoc” · **Descriere:** „Consultanță gratuită · decoflair.ro”
- **Public:** România, 30–60 ani, interese: construcții, renovare, case, grădină, materiale de construcții. Dacă flota livrează doar în anumite zone, restrânge publicul la acele județe. **Buget de test:** 50–80 lei/zi, 5–7 zile, apoi crește setul cu cel mai mic cost pe click.
- **Urgență reală:** oprește sau schimbă reclama în ianuarie. Mesajul „înainte de prima zăpadă / de sărbători” expiră.

## Notă despre imagini și drepturi
- Ambientul (vile, colț cu bosaje, intrare, cornișă) e din biblioteca de inspirație generată digital pentru Deco&Flair, deci e sigur pentru reclame. Imaginile de produs sunt cele de pe decoflair.ro.
- **Nu am folosit** fotografiile din `catalog-fatade/` (case românești): proveniența lor nu e declarată și trebuie confirmate drepturile înainte de reclame plătite.
- Imagini noi, mai credibile (case românești iarna, perechea „colț înainte/după”, produsul în studio, depozitul plin), sunt comandate lui Codex în `CODEX-BRIEF.md`. Reel-ul le preia automat la următoarea randare.

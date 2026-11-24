# NCL107 · Fațada la amurg

[Spot Ads de 15 secunde](reel/decoflair-ncl107-amurg-ads-15s.mp4) · [Copertă](reel/coperta-ncl107-amurg.jpg)

**Text principal**

Când ajungi acasă seara, lumina îți arată fiecare detaliu. Dă muchiilor fațadei relief cu modelul NCL107. Comandă direct pe decoflair.ro.

**Titlu**

Colțar de fațadă NCL107 · În stoc

**Descriere**

Livrare estimată în 3–5 zile lucrătoare de la confirmarea comenzii.

**Buton**

Cumpără acum

[Destinația butonului · fișa exactă NCL107, cu UTM](https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300?utm_source=meta&utm_medium=paid_social&utm_campaign=exterior-sarbatori-2026&utm_content=ncl107-amurg-15s)

## Montaj

| Timp | Cadru |
|---|---|
| 0–2,7 s | Colțar montat, la distanță medie, cu ferestrele vizibile. Identificare NCL107. |
| 2,7–10,3 s | Retragere continuă, cu parallax, până la fațada întreagă la amurg. |
| 10,3–15 s | Casa rămâne în mișcare în fundal, cu „Comandă NCL107”, stoc și livrare în stânga jos. |

Cadru continuu generat cu HeyGen Video 1 pe baza [imaginii oficiale NCL107](https://decoflair.ro/image/cache/catalog/produse/Coltare/NCL107/coltar-NCL107-web-800x800.jpg) și a [referinței de lumină NMC](https://www.nmcromania.ro/black-november/assets/hero-vila.jpg). Clădirea ilustrează un posibil ambient. Sursa generată are 768 × 1344 și watermark HeyGen. Exportul păstrează watermarkul și folosește 1080 × 1920, cu scalare Lanczos și claritate discretă.

Claude Code a recomandat retragerea fizică de la colț și finalul concis. Am aplicat și gradientul local, ca fațada să rămână vizibilă în final.

Stoc verificat pe [fișa NCL107](https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300) la 24.11.2026. Termenul estimat este cel publicat pentru profile exterioare din stoc. [Plată și livrare Deco & Flair](https://decoflair.ro/plata-si-livrare)

Indicator principal: comenzi atribuite variantei `ncl107-amurg-15s`. Indicator secundar: clickuri către fișa NCL107.

## Randare

Cu Pillow și FFmpeg, din rădăcina repository-ului:

```sh
python3 decoflair-reel-exterior/reel_ncl107_amurg.py decoflair-reel-exterior/assets/ncl107-amurg-footage.mp4
```

### Export dintr-o sursă nativă

Versiunea fără watermark necesită un clip-sursă curat, generat sau filmat nativ la 1080 × 1920. După verificarea sursei, opțiunea `--native` păstrează dimensiunile și folosește nume de fișiere separate. Sursa HeyGen existentă este respinsă de acest mod.

```sh
python3 decoflair-reel-exterior/reel_ncl107_amurg.py --native /cale/catre/clipul-sursa-curat.mp4
```

<details>
<summary>Promptul pentru clipul-sursă</summary>

> Generate background footage for an original Romanian exterior-trim advertisement, exactly 15 seconds, vertical 9:16, crisp 1080p. Reference 1 is the exact NCL107 quoin geometry only: tall right-angle stacked plain rectangular exterior blocks, clean horizontal seams, modest projection. Reference 2 guides a lived-in Romanian façade and warm evening atmosphere only; use more modest two-story house geometry in a tasteful warm ivory plaster. One continuous physically filmed shot. At time zero camera is 3 to 4 metres from the home's outside corner at shoulder height, a medium view with several installed NCL107 blocks and one full adjacent window, no extreme macro. The corner fills about one third of the width and is immediately legible. Starting at time zero, smooth backwards dolly with a gentle rightward arc around a restrained foreground bush, steady horizon and physically accurate parallax among the foliage, corner, windows and roof. Ease out by second 10, then hold a stable wider view of the same house until 15. The house occupies the centre and upper frame with room below for editorial typography. Character comes from warm 2700K interior window lamps and soft real evening light against blue dusk. Real subtle branch/leaf movement and natural small-scale surface texture. NCL107 geometry must stay unchanged throughout; no building morph, no changing time of day, no virtual zoom, no lens flares or excessive blur. The shot should feel like high-quality architectural footage, sharp detail, restrained cinematic exposure, realistic dusk. No persons, no text, no captions, no graphics, no logos, no voice. This is footage to be edited separately.

</details>

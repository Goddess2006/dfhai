# NCL107 la amurg · reconstrucție 3D

[Spot vertical, 15 secunde](../reel/decoflair-ncl107-amurg-ads-15s-3d.mp4) · [Copertă](../reel/coperta-ncl107-amurg-3d.jpg)

Cadru continuu cu retragere fizică a camerei de la colțarul montat până la casa întreagă. Casa și grădina sunt o vizualizare 3D de inspirație. Geometria colțarului urmează cei 300 × 300 × 30 × 1000 mm ai produsului și cele cinci benzi din imaginea de catalog. [Fișa NCL107](https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300)

MP4 H.264/AAC, 1080 × 1920 nativ, 24 fps, 360 cadre, 15,00 s, fără watermark. Camera, luminile, materialele și profunzimea de câmp se randează în WebGL la rezoluția finală. Titlurile sunt compuse la aceeași rezoluție.

## Setări Meta Ads

**Text principal**

Când se aprind luminile, fațada își arată detaliile. Dă relief colțurilor casei cu NCL107.

**Titlu**

Colțar de fațadă NCL107

**Buton**

Cumpără acum

Introdu URL-ul de mai jos în câmpul „Site web” al reclamei. Textul „Comandă NCL107” din clip indică acțiunea, iar butonul platformei deschide fișa produsului. [Destinație directă Meta Ads](https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300?utm_source=meta&utm_medium=paid_social&utm_campaign=exterior-sarbatori-2026&utm_content=ncl107-amurg-15s-3d)

Indicator principal pentru primele șapte zile de la publicare: comenzi atribuite variantei `ncl107-amurg-15s-3d`. Indicator secundar: clickuri către fișa NCL107.

## Reproducere

Node.js cu Playwright și Chromium, Python cu Pillow și FFmpeg cu libx264. Rulează din rădăcina repo-ului. Randarea folosește biblioteca [Three.js 0.160.1](https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.min.js), verificată după SHA-256 în script. Chromium trebuie să aibă suport WebGL 2. Procesarea se face local.

```sh
node decoflair-reel-exterior/amurg-3d/render.cjs --three /cale/three.min.js --output /tmp/ncl107-amurg-3d.mp4
python3 decoflair-reel-exterior/reel_ncl107_amurg.py --recreation /tmp/ncl107-amurg-3d.mp4
```

Folosește `--preview --output /cale/previzualizari` cu primul script pentru șapte cadre de lucru la rezoluție redusă.

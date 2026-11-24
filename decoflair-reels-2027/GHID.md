# Deco & Flair · Reel-uri de cumpărături

| Serie | Clip · 30 s | Copertă | Imagine hero |
|---|---|---|---|
| Interior | [MP4](decoflair-interior-reel.mp4) | [JPG](interior-coperta.jpg) | [JPG](interior-hero.jpg) |
| Exterior | [MP4](decoflair-exterior-reel.mp4) | [JPG](exterior-coperta.jpg) | [JPG](exterior-hero.jpg) |

Clipuri verticale de 1080 × 1920 px, 30 fps, H.264 și AAC stereo. Atmosferele provin din colecția Deco & Flair 2027, cu recadrare verticală din cadrele de ambient. Paginile oficiale de produs furnizează fotografiile, prețurile și disponibilitatea. Coloana `banner` din `catalog.json` indică bannerul corespondent din colecție.

Deschide [versiunea interactivă](index.html) din folderul extras. Alege seria și un capitol, folosește „Vezi în reel” pentru salt la cadrul cu prețul sau deschide fișa produsului. Cantitatea modifică subtotalul orientativ. Clipurile MP4 includ animația de preț și datele de contact. Capitolele, calculatorul și linkurile funcționează în pagina interactivă.

## Produse și prețuri

Prețurile sunt cele afișate pe site la **24.11.2026**, cu TVA, pe bucată. Verifică fișa de produs pentru prețul curent înainte de publicare.

| Serie | Produs | Preț |
|---|---|---:|
| Interior | [Baghetă decorativă NOMASTYL® N](https://decoflair.ro/brau-decorativn-nomastyl) | 30,90 lei |
| Interior | [Cornișă LED WALLSTYL® IL18](https://decoflair.ro/cornisa-led-il18-121x90x2000) | 217,56 lei |
| Interior | [Rozetă ARSTYL® R15](https://decoflair.ro/rozeta-decorativar15-arstyl) | 413,94 lei |
| Interior | [Plintă WALLSTYL® FD2](https://decoflair.ro/plintafd2-wallstyl) | 114,28 lei |
| Interior | [Panou 3D ARSTYL® WAVE](https://decoflair.ro/panou-decorativ-3d-wave) | 433,85 lei |
| Exterior | [Ancadrament ADRo® NA107](https://decoflair.ro/ancadrament-decorativna107) | 81,30 lei |
| Exterior | [Colțar ADRo® NCL107](https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300) | 248,09 lei |
| Exterior | [Pilastru ADRo® NP28](https://decoflair.ro/pilastru-coloana-decorativa-adro-decor-np28) · la comandă, 14 zile | 222,45 lei |
| Exterior | [Cornișă ADRo® NC104](https://decoflair.ro/cornisa-decorativa-exterior-nc104-220x80x2000) | 194,74 lei |
| Exterior | [Capac de stâlp ADRo® ST105](https://decoflair.ro/capac-gard-st105) | 200,58 lei |

## Refacerea exporturilor

Din rădăcina repository-ului, cu Python 3, Pillow și FFmpeg cu encoderul `libx264`:

```sh
python3 decoflair-reels-2027/render.py
```

Actualizează în `catalog.json` data, prețul în bani și disponibilitatea. Comanda regenerează videoclipurile, cover-urile, cadrele hero și datele JavaScript. Opțiunea `--series interior` sau `--series exterior` limitează exportul media la o singură serie. Pentru a reface doar cadrele fixe și datele vizualizatorului, folosește `--stills`. Muzica instrumentală originală este sintetizată în `render.py`, la 100 BPM.

| Segment | Interval |
|---|---|
| Hero | 0,00–2,40 s |
| Ambient și produs 1 | 2,40–7,20 s |
| Ambient și produs 2 | 7,20–12,00 s |
| Ambient și produs 3 | 12,00–16,80 s |
| Ambient și produs 4 | 16,80–21,60 s |
| Ambient și produs 5 | 21,60–26,40 s |
| Site, consultanță și data prețurilor | 26,40–30,00 s |

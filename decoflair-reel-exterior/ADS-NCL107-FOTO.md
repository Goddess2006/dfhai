# NCL107 · Fațade fotografiate

[Spot Meta Ads (MP4)](reel/decoflair-ncl107-foto-ads-15s.mp4) · [Copertă](reel/coperta-ncl107-foto.jpg)

Spot 9:16. Montajul trece prin tăieturi fotografice de la muchia unei fațade reale la produs și la două perspective ale altei case fotografiate la amurg.

| Interval aproximativ | Imagine și proveniență |
| --- | --- |
| 0–2,04 s | Rosturi pe fațada proiectului Altenburg. Fotografie NMC EXTRANET `NMC_02_003087_original.jpg`, 2362 × 2944 px. Metadatele proiectului indică profile DOMOSTYL, prezentate ca inspirație de fațadă. |
| 2,04–5,21 s | NCL107 și „Relief pentru muchiile casei tale”, imagine de catalog `assets/p-ncl107-hero.jpg` verificată față de [fișa NMC](https://www.nmcromania.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300). |
| 5,21–8,17 s | Detaliu la amurg, Curtis Adams, [fotografia intrării](https://www.pexels.com/photo/charming-stone-facade-house-at-dusk-36777965/). |
| 8,17–10,79 s | Cadru intermediar pe muchia de piatră și fereastra luminată. |
| 10,79–15 s | Fațada întreagă și „Comandă NCL107”. Curtis Adams, [fotografia de ansamblu din aceeași ședință](https://www.pexels.com/photo/modern-stone-house-in-tranquil-forest-setting-36777966/). |

Fotografiile Curtis Adams se folosesc în montaj sub [licența Pexels](https://www.pexels.com/license/). Imaginea de produs este distinctă de proiectele de inspirație. Format final 1080 × 1920, 24 fps, 15,00 s. Fotografiile de fațadă au rezoluție suficientă pentru decupajele folosite, iar imaginea de catalog este plasată într-o casetă adaptată sursei.

## Reclamă Meta

**Text principal**

Colțurile schimbă felul în care se vede întreaga fațadă. Dă-le relief cu profilul exterior NCL107.

**Titlu**

Colțar de fațadă NCL107

**Buton**

Cumpără acum

[Destinația butonului, fișa NCL107](https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300?utm_source=meta&utm_medium=paid_social&utm_campaign=exterior-sarbatori-2026&utm_content=ncl107-foto-15s)

Indicator principal: comenzi atribuite variantei `ncl107-foto-15s` în primele șapte zile de la publicare. Indicator secundar: clickuri către fișa produsului.

## Randare

Din rădăcina repo-ului, cu Pillow și FFmpeg. Descarcă în afara repo-ului fotografiile de amurg de pe paginile Pexels de mai sus. Scriptul detectează originalul de exterior din `EXTRANET/source/`. Folosește `--extranet /cale/fotografie.jpg` ca să-l indici explicit.

```sh
python3 decoflair-reel-exterior/reel_ncl107_foto.py --porch /cale/36777965.jpg --wide /cale/36777966.jpg
```

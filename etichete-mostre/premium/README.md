# Etichete de colecție Deco&Flair

- `etichete-mono-A4.pdf`: alb-negru, inclusiv sigla și ilustrația.
- `etichete-color-A4.pdf`: verde închis, ivoire și accente aurii.
- `comparatie.png`: cele două variante alăturate.
- `apercu-*.png`: câte o etichetă la aproximativ 288 dpi.
- `coala-*.png`: previzualizări ale colilor complete.

Tipăriți PDF-ul la **100% / Actual size**, A4, fără „Fit to page”. Patru etichete de 105 × 148,5 mm; tăiere pe liniile punctate. Elementele utile au margine de siguranță de 6 mm. Fundalul deschis poate fi limitat de marginile imprimantei. Fișierele nu includ bleed sau conversie CMYK; sunt potrivite pentru imprimare uzuală. Auriul este o culoare imprimată, nu finisaj metalizat.

Sunt etichete pentru întreaga colecție, fără preț sau cod. Compoziția combină un ambient de inspirație cu un singur detaliu de secțiune, ilustrativ, fără cote sau grilă de modele. Avantajele sunt scrise discret, fără pictograme.

## Surse și conținut

Sigla oficială și QR-ul provin din eticheta lui Claude, în directorul părinte. Originalele au fost păstrate. QR-ul indică https://decoflair.ro/bagheta-polistiren și are zonă albă de protecție de patru module.

`assets/ambient-interior.png` este un ambient conceptual generat cu OpenAI imagegen pentru această machetă, nu o fotografie a unui anumit model din catalog. Este marcat pe etichetă „Ambient de inspirație”. Detaliul tehnic este un SVG ilustrativ simplificat, inclus direct în generator.

Conform cerinței utilizatorului, blocul de contact include exclusiv site-ul decoflair.ro, telefonul 0723 300 603 și mențiunea mai mică „Depozit: Chiajna-Ilfov”, alături de QR. Numele societății, sediul social, CUI și ONRC au fost eliminate de pe etichetele premium. Localizarea depozitului este furnizată explicit de utilizator.

Fonturile Cormorant Garamond și Montserrat sunt salvate local de la Google Fonts. Licențele OFL sunt în `assets/`. Nu sunt necesare conexiuni externe pentru deschiderea etichetelor HTML.

## Regenerare

Necesită Python 3 și Node.js cu npm:

```sh
npm ci
npx playwright install --with-deps chromium
npm run build
npm run render
```

`build.py` generează ambele HTML-uri din aceeași machetă și folosește QR-ul original din directorul părinte. `render.cjs` produce PDF-urile și PNG-urile; verifică fonturile, imaginile, depășirile, numărul de etichete/pagini, decodarea QR și absența culorii în varianta mono. Păstrați structura de directoare: sigla este în directorul părinte.

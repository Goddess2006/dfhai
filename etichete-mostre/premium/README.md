# Etichete de colecție Deco&Flair

- `etichete-mono-A4.pdf`: alb-negru, inclusiv sigla și ilustrația.
- `etichete-color-A4.pdf`: verde închis, ivoire și accente aurii.
- `comparatie.png`: cele două variante alăturate.
- `apercu-*.png`: câte o etichetă la aproximativ 288 dpi.
- `coala-*.png`: previzualizări ale colilor complete.

Tipăriți PDF-ul la **100% / Actual size**, A4, fără „Fit to page”. Patru etichete de 105 × 148,5 mm; tăiere pe liniile punctate. Elementele utile au margine de siguranță de 6 mm. Fundalul deschis poate fi limitat de marginile imprimantei. Fișierele nu includ bleed sau conversie CMYK; sunt potrivite pentru imprimare uzuală. Auriul este o culoare imprimată, nu finisaj metalizat.

Sunt etichete pentru întreaga colecție, fără preț sau cod. Cele cinci secțiuni sunt forme ilustrative, nu desene tehnice ale unor modele comerciale. Mențiunea „Bară 2 m” a fost omisă până la confirmarea ei pentru toată colecția.

## Surse

Sigla oficială și ilustrația SVG provin din eticheta lui Claude, în directorul părinte. Originalele au fost păstrate. QR-ul indică https://decoflair.ro/bagheta-polistiren și are zonă albă de protecție de patru module.

Datele vânzătorului au fost consultate la 5 noiembrie 2026 la https://decoflair.ro/contact: Deco & Flair Hub SRL; telefon 0723 300 603; Str. Făurei nr. 1, sector 1, București; CUI RO 54681700; ONRC J2026031505008. Sediul social este folosit pentru a evita adresele neuniforme ale depozitului din aceeași pagină.

Fonturile Cormorant Garamond și Montserrat sunt salvate local de la Google Fonts. Licențele OFL sunt în `assets/`. Nu sunt necesare conexiuni externe pentru deschiderea etichetelor HTML.

## Regenerare

Necesită Python 3 și Node.js cu npm:

```sh
npm ci
npx playwright install --with-deps chromium
npm run build
npm run render
```

`build.py` generează ambele HTML-uri din aceeași machetă și folosește QR-ul original din directorul părinte. `assets/artwork.js` păstrează ilustrația lui Claude, cu ID-uri SVG unice pentru fiecare etichetă. `render.cjs` produce PDF-urile și PNG-urile; verifică fonturile, imaginile, depășirile, numărul de etichete/pagini, decodarea QR și absența culorii în varianta mono. Păstrați structura de directoare: sigla este în directorul părinte.

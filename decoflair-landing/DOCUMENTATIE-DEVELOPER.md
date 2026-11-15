# Selecția Premium · Deco&Flair — documentație pentru developer

Landing page static și **atemporal** (fără date, countdown sau campanii) pentru **decoflair.ro** (OpenCart 3 + tema Journal 3). Poate fi folosit în două feluri:
- ca pagină de sine stătătoare: `https://decoflair.ro/selectia-premium/`;
- afișat peste homepage, înainte ca vizitatorul să intre în magazin.

Nu are nevoie de bază de date, OCMOD, extensii, API sau build pe server.

---

## 1. Conținutul arhivei `decoflair-selectia-premium.zip`

| Cale | Ce este | Se urcă pe server? |
|---|---|---|
| `selectia-premium/index.html` | Landing-ul (HTML static, generat) | **da** |
| `selectia-premium/df.css` | Stilurile (izolate, nu ating tema) | **da** |
| `selectia-premium/df.js` | Interacțiuni: căutare, animații, stoc live, coș, punte cu overlay-ul | **da** |
| `selectia-premium/homepage-overlay.js` | Scriptul care afișează landing-ul peste homepage | **da** |
| `selectia-premium/assets/` | 58 de imagini optimizate (≈4 MB): ambient, produse, logo | **da** |
| `cod-homepage.html` | Linia de pus pe homepage (varianta HTML) | nu, se copiază în temă |
| `cod-homepage.js` | Aceeași linie, varianta doar JavaScript | nu, se copiază în temă |
| `DOCUMENTATIE-DEVELOPER.md` | Acest document | nu |
| `sursa/tools/build.py` | Generatorul `index.html` (texte, produse, capitole) | nu |
| `sursa/tools/package.py` | Generatorul arhivei | nu |
| `sursa/surse-imagini.json` | Proveniența imaginilor ambientale (URL-urile de pe decoflair.ro) | nu |

---

## 2. Instalare — pagina `/selectia-premium/`

1. Dezarhivează și urcă folderul `selectia-premium/` în rădăcina publică a magazinului, lângă `index.php`. De exemplu: `public_html/selectia-premium/`.
2. Deschide `https://decoflair.ro/selectia-premium/` pe desktop și pe mobil.
3. Nu se suprascrie niciun fișier al magazinului. Folderul nu intră în conflict cu rutele SEO OpenCart: serverul servește fișierul static înaintea `index.php`.
4. Dacă `.htaccess` redirecționează tot traficul spre `index.php`, verifică să existe condițiile standard OpenCart:
   ```apache
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   ```
5. Golește cache-ul CDN/Cloudflare, dacă există.

**Link în meniu sau banner:** Journal › Menus / Banners → URL `https://decoflair.ro/selectia-premium/`.

---

## 3. Instalare — afișare peste homepage

Adaugă **o singură dată** pe homepage, înainte de `</body>`:

```html
<script defer src="/selectia-premium/homepage-overlay.js"></script>
```

**Unde se pune:**
- **Journal 3:** Journal › Skins › skinul activ › Custom Code › *Footer* (câmpul pentru HTML).
  Dacă există doar câmpul *Custom JS*, folosește varianta din `cod-homepage.js`:
  ```js
  (function(){var s=document.createElement('script');s.src='/selectia-premium/homepage-overlay.js';s.defer=true;document.body.appendChild(s);})();
  ```
- **Fără Journal:** `catalog/view/theme/<tema>/template/common/footer.twig`, înainte de `</body>`. Apoi Extensii › Modificări › Refresh și golește cache-ul temei (Dashboard › rotița albastră).

**Test:** `https://decoflair.ro/?df=1` forțează afișarea, indiferent de frecvență.

### Opțiuni (atribute pe tagul `<script>`)

| Atribut | Valori | Implicit |
|---|---|---|
| `data-enabled` | `false` = oprit complet | activ |
| `data-frequency` | `session` (o dată pe sesiune), `day` (o dată la 24 h), `always` (test) | `session` |
| `data-ends` | opțional, data după care nu mai apare, ex. `2027-03-01T00:00:00+02:00` | fără dată de final |
| `data-delay` | întârzierea afișării, în ms | `400` |

Exemplu: `<script defer src="/selectia-premium/homepage-overlay.js" data-frequency="day"></script>`

### Comportament (verificat cu Playwright pe un homepage simulat pe domeniul decoflair.ro, desktop + mobil)

- **Unde apare:** doar pe `/`, `/index.php` și `index.php?route=common/home`, inclusiv variantele cu prefix de limbă `/xx/`. Nu apare pe pagini de produs, categorie sau coș.
- **Închidere:** butonul „Intră în magazin ×” sau tasta Escape închid landing-ul, chiar și când focusul e în interiorul lui. Se restabilesc scroll-ul și focusul paginii.
- **Memorare:** după închidere, landing-ul nu reapare la reîncărcare în aceeași sesiune. Memorarea folosește `sessionStorage`, respectiv `localStorage` la `day`.
- **Linkuri:** un link spre produs, categorie sau blog deschide pagina în fereastra principală. Ancorele `#lumina`, `#tavan` etc. rămân în landing.
- **Coș:** „Adaugă în coș” funcționează din landing; produsul apare în coș după închidere.
- **Redeschidere** din alt buton sau banner: `window.DecoFlairPremium.open()`.

### Cerințe de securitate pentru server

- **Același domeniu:** landing-ul se încarcă într-un `iframe` de pe același domeniu. Dacă serverul trimite `X-Frame-Options: DENY` sau CSP `frame-ancestors 'none'`, iframe-ul nu se afișează. Trebuie setate `SAMEORIGIN`, respectiv `frame-ancestors 'self'`.
- **CSP:** dacă site-ul folosește Content-Security-Policy, permite `fonts.googleapis.com` (stiluri) și `fonts.gstatic.com` (fonturi), sau găzduiește fonturile local.
- **Mixed content:** scriptul refuză să funcționeze dacă landing-ul ar fi pe alt domeniu, ca protecție.

---

## 4. Ce face `df.js` pe decoflair.ro

Când pagina rulează pe `decoflair.ro`, scriptul citește pagina fiecărui produs (aceeași origine, fără API):
- **Stoc live:** produsele fără stoc apar „Disponibil la comandă”, cu punct gri.
- **„Adaugă în coș”:** apare doar la produsele în stoc și fără opțiuni obligatorii. Folosește endpoint-ul standard OpenCart `index.php?route=checkout/cart/add` (POST `product_id`, `quantity=1`). Pentru produsele cu opțiuni sau cu cantitate minimă, butonul duce la pagina produsului.
- **Încărcare:** maximum 4 cereri în paralel; rezultatele se păstrează în memorie.
- **Căutare fără diacritice:** „cornisa”, „wave”, „led”, „z11”.

Testat cu paginile reale ale produselor. Coșul a fost testat cu răspuns simulat, nu pe un coș real.

**Landing atemporal:** fără date, countdown sau mesaje de campanie, și fără prețuri sau procente pe produse. Clientul vede prețul actual pe pagina produsului din magazin. Pagina poate rămâne publicată oricât. `build.py` refuză să genereze pagina dacă apare „lei” în HTML.

---

## 5. Structura paginii

1. Header: logo, cele 7 capitole, căutare, coș
2. Hero: „Lux liniștit. Pentru fiecare casă.”, imagine în arcadă, carduri de sticlă, CTA
3. Banda de branduri: Arstyl®, Wallstyl®, Nomastyl®, ADRo®, NMC®, Carrara Best, Roberto Cavalli, Noël & Marquet
4. Manifest („curatori de tendințe”) + 3 piloni: Premium · Inovație · Know-how + cuprins
5. **7 capitole**, fiecare cu imagine ambientală în arcadă, text, sfat „Know-how Deco&Flair” și produse:
   - 01 Lumină: L5, L2, IL18, IL11
   - 02 Texturi 3D: WAVE, CANELE L, LIQUID, ICON
   - 03 Tavan: Z11, Z21, WT25, R12
   - 04 Pereți & plinte: WO2, Z1360, WL6, FD3, FD21
   - 05 Riflaje: stejar deschis, stejar închis
   - 06 Tapet: Carrara Best 82603, 82671, Roberto Cavalli 19070
   - 07 Fațadă: NA105, NCL106, A113
6. Servicii: Consultanță premium · Randare 3D · Produse personalizate + contact (0723 300 603, office@decoflair.ro, @decoflairhub)
7. Jurnal: 4 articole din blogul decoflair.ro
8. Întrebări frecvente
9. Final „Elevate your space. Define your style.” + footer

Toate cele 25 de produse erau în stoc la publicare; stocul se actualizează live pe pagină. Toate linkurile (produse, servicii, blog) răspund HTTP 200.

---

## 6. Sistemul vizual

**Direcție:** „quiet luxury”, cu aer Tokyo / Singapore contemporan: aerisit, mult spațiu alb, linii fine, arcade (formă semnătură), carduri de sticlă (glassmorphism), aure difuze de culoare, text vertical, numere de capitol în contur.

**Fonturi:**
- **Jost** pentru texte și etichete: fontul folosit pe decoflair.ro.
- **Instrument Serif** pentru titluri: un serif editorial condensat, cu italic.
- Ambele de la Google Fonts.

**Culori** (tokeni CSS în `:root` din `df.css`):

| Token | Valoare | Rol |
|---|---|---|
| `--cream` | `#F4EEE6` | fundal |
| `--paper` | `#FBF8F3` | carduri |
| `--nude` / `--sand` | `#E6D7C8` / `#D8C3AF` | fundaluri imagini, accente |
| `--ink` | `#141214` | negru elegant: text, butoane, footer |
| `--mauve` / `--mauve-soft` | `#A6919F` / `#E8DEE4` | mov șters |
| `--forest` → `--sage` | `#2F4A3C` → `#A9BBAA` | degradeu verde forest |
| `--powder` | `#EBCFCB` | roz pudră |
| `--g-text` | forest → mov → roz | italicul din titluri |

**Animații:** discrete, dezactivate automat la `prefers-reduced-motion`.
- aurele de fundal se mișcă lent;
- imaginile se măresc ușor la hover;
- conținutul apare la derulare;
- banda de branduri rulează continuu.

**Responsive:** desktop, tabletă, mobil (verificat la 1440 px și 390 px, fără derulare orizontală). Pe mobil:
- produsele fiecărui capitol devin un carusel orizontal cu snap;
- apare o bară fixă jos, cu „Explorează selecția” și telefon.

**Accesibilitate:**
- link „Sari la produse”;
- `aria-label` pe butoane și pe căutare;
- focus vizibil;
- contrast AA pe texte;
- pagina funcționează complet fără JavaScript.

---

## 7. Modificări ulterioare

Toate textele, produsele și imaginile sunt în `sursa/tools/build.py`:
- **`CAMPANIE`:** telefonul, emailul, programul, Instagram;
- **`CAPITOLE`:** titlurile, textele, sfaturile know-how, imaginea ambientală și produsele fiecărui capitol;
- **`SERVICII`, `BLOG`, `BRANDURI`.**

Pentru un produs nou adaugi o intrare `P(id=..., brand=..., name=..., spec=..., url="slug-din-decoflair", img="nume-imagine")` și pui imaginea în `assets/nume-imagine.jpg` (recomandat 720×720 px, JPG). Opțional:
- `hover="imagine-ambient"` arată un ambient la trecerea mouse-ului;
- `tag="Nou"` adaugă o etichetă pe card.

Apoi rulezi, din folderul proiectului:
```bash
python3 tools/build.py
```
```bash
python3 tools/package.py
```
și urci din nou fișierele din `selectia-premium/`.

**Fără dată de expirare:** pagina și overlay-ul rămân active până le dezactivezi. Dacă vrei totuși ca overlay-ul să se oprească singur la o dată, pune `data-ends` pe tag.

---

## 8. Checklist înainte de lansare

- [ ] `https://decoflair.ro/selectia-premium/` se deschide; imaginile și fonturile se încarcă.
- [ ] Pe mobil: caruselul produselor, bara de jos, căutarea.
- [ ] Butoanele „Descoperă” deschid produsele corecte.
- [ ] „Adaugă în coș” apare la produsele în stoc și adaugă corect în coș.
- [ ] Linia de cod e pe homepage; `https://decoflair.ro/?df=1` afișează landing-ul.
- [ ] Butonul „Intră în magazin ×” și Escape închid; nu reapare la reîncărcare.
- [ ] Antetele `X-Frame-Options` / CSP permit `SAMEORIGIN`.
- [ ] Prețurile speciale sunt configurate în OpenCart (Specials / Discounts). Landing-ul nu le afișează și nu le modifică.
- [ ] Golit cache-ul Journal 3 / OpenCart / CDN.

**Dezactivare:** ștergi linia de pe homepage sau adaugi `data-enabled="false"`. Folderul `selectia-premium/` se poate păstra ca pagină de prezentare.

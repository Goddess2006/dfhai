# Instalare Black Friday pe NMC România

Pachetul este pregătit pentru integrare statică pe domeniul magazinului. Nu a fost instalat sau validat pe un mediu NMC de test: nu avem acces la administrarea ori sursele magazinului. Site-ul public folosește tema Journal 3; versiunea exactă OpenCart nu este cunoscută. Nu sunt necesare modificări de bază de date sau acces la API.

## Publicare

1. Rulează `python3 black-friday/tools/package.py` din rădăcina repository-ului. Arhiva rezultată este `black-friday/release/nmc-black-friday.zip`.
2. Extrage folderul `black-friday` în rădăcina publică a magazinului, pe același domeniu/protocol cu homepage-ul. Fișierele existente ale magazinului nu se înlocuiesc. Verifică accesul la `/black-friday/index.html` și la fotografii.
3. Pentru suprapunere, politica `frame-src` a homepage-ului și `frame-ancestors`/`X-Frame-Options` ale landingului trebuie să permită încadrarea de pe același domeniu (nu `DENY`). Deschide landingul direct și verifică fotografiile, reducerile și navigarea. Dacă există CSP, permite scripturile/stilurile existente ale landingului, resursele proprii (`script-src`, `style-src`, `img-src`, `connect-src 'self'`) și fonturile Google ori găzduiește fonturile local. Nu dezactiva global CSP. Pagina conține CSS și JavaScript inline; mută-le în fișiere sau autorizează hash-urile lor dacă politica site-ului o cere.
4. Adaugă o singură dată în homepage, înainte de `</body>`, prin template sau facilitatea de inserare HTML/script a magazinului:

```html
<script defer src="/black-friday/homepage-overlay.js"
        data-campaign="black-friday-2026"></script>
```

Dacă editorul acceptă exclusiv JavaScript, folosește varianta de mai jos, fără taguri HTML:

```js
if (!document.querySelector('script[src="/black-friday/homepage-overlay.js"]')) {
  const script = document.createElement('script');
  script.src = '/black-friday/homepage-overlay.js';
  script.dataset.campaign = 'black-friday-2026';
  document.head.append(script);
}
```

5. Golește cache-ul paginii și al CDN-ului după instalare. Scriptul este activ numai pe `/` și `/index.php` cu ruta absentă sau `common/home`. Dacă homepage-ul real are o rută de limbă diferită, ajustează explicit verificarea `home` înainte de instalare.

## Comportament

Landingul apare într-un dialog pe tot ecranul, într-un iframe de pe același domeniu. Homepage-ul rămâne dedesubt. Butonul „Continuă în magazin” și Escape închid suprapunerea, restabilesc scroll-ul și focusul și salvează închiderea în `sessionStorage`. Nu reapare la revenirea pe homepage în aceeași sesiune de filă. O campanie nouă poate folosi alt `data-campaign`. Dacă browserul nu suportă dialogul nativ, homepage-ul rămâne accesibil.

Linkurile către produse deschid magazinul în fereastra principală. Navigarea între categorii rămâne în landing. Pentru a redeschide intenționat suprapunerea pe homepage, un buton poate apela `window.NMCBlackFriday.open()`.

Nu există calendar de activare presupus: campania începe când este inserat scriptul. Confirmă ofertele și perioada cu echipa comercială înainte de lansare.

## Campania fără prețuri

Singura reducere comunicată este **−30% la adezivul pentru lipire exterior ADRO-FIX de 1,5 kg** (`adeziv12`). Toate celelalte produse sunt la preț întreg, inclusiv ADRO-FIX de 4 kg, exteriorul, interiorul și Carrara Best. Reducerile anterioare de 20%, 30% la tapet și până la 40% la interior sunt retrase. Nu există prețuri numerice sau cereri de preț în landing.

`catalog.json` declară reducerea pe fiecare produs. `tools/render.py` generează HTML-ul și expune eticheta de reducere exclusiv pe produsul eligibil. `campaign.js` gestionează căutarea, navigarea pe categorii și galeriile orizontale, cu săgeți și glisare pe mobil. `polish.css` definește tema bleumarin/alb cald/roz, contururile duble și umbrele.

## Verificarea înainte de activare

- Verifică pe desktop/mobil hero-ul cu ADRO-FIX 1,5 kg și unica reducere de 30%. Celelalte carduri trebuie să rămână fără badge de reducere.
- Verifică navigarea cu săgeți, glisarea pe mobil și căutarea produselor.
- Închiderea și Escape trebuie să readucă homepage-ul cu scroll-ul/focusul restabilite. Overlay-ul nu apare pe pagini de produs/categorie/coș.
- Confirmă oferta efectivă de 30% pentru ambalajul de 1,5 kg în magazin, disponibilitatea și perioada campaniei. Landingul comunică oferta; nu modifică prețurile magazinului.
- Verifică CSP și încadrarea pe același domeniu înainte de activarea scriptului.

## Dezactivare

Elimină scriptul inserat sau setează `data-enabled="false"`, apoi golește cache-ul homepage-ului. Landingul direct rămâne la `/black-friday/`; îl poți elimina separat. Nu se schimbă template-ul original al homepage-ului.

## Test local

Rulează `python3 black-friday/tools/preview.py --port 8765` și deschide `http://127.0.0.1:8765/`. Homepage-ul este demonstrativ. Serverul servește numai fișiere locale și nu se publică în magazin. Un server static simplu poate afișa de asemenea landingul.

Testele automate necesită Node.js și dependențele de dezvoltare: din `black-friday`, rulează `npm ci` și `npm test`. Nu sunt necesare pe serverul magazinului.

## Selecția actuală și stocul

Cele 32 de produse și fotografiile reale din selecția verificată la 4 noiembrie 2026 sunt păstrate ca prezentare de catalog. Numai ADRO-FIX 1,5 kg are reducere. Nu există sincronizare automată de stoc; disponibilitatea curentă se confirmă în pagina produsului.

După actualizarea catalogului rulează `python3 black-friday/tools/render.py`, apoi `python3 black-friday/tools/package.py`. Nu atribui reduceri după categorie: acestea sunt declarate individual prin `discountPercent`.

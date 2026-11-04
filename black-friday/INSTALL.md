# Instalare Black Friday pe NMC România

Pachetul este pregătit pentru integrare statică pe domeniul magazinului. Nu a fost instalat sau validat pe un mediu NMC de test: nu avem acces la administrarea ori sursele magazinului. Site-ul public folosește tema Journal 3; versiunea exactă OpenCart nu este cunoscută. Nu sunt necesare modificări de bază de date sau acces la API.

## Publicare

1. Rulează `python3 black-friday/tools/package.py` din rădăcina repository-ului. Arhiva rezultată este `black-friday/release/nmc-black-friday.zip`.
2. Extrage folderul `black-friday` în rădăcina publică a magazinului, pe același domeniu/protocol cu homepage-ul. Fișierele existente ale magazinului nu se înlocuiesc. Verifică accesul la `/black-friday/index.html` și la fotografii.
3. Pentru suprapunere, politica `frame-src` a homepage-ului și `frame-ancestors`/`X-Frame-Options` ale landingului trebuie să permită încadrarea de pe același domeniu (nu `DENY`). Deschide landingul direct și verifică dacă prețurile se încarcă. Dacă există CSP, permite scripturile/stilurile existente ale landingului, resursele proprii (`script-src`, `style-src`, `img-src`, `connect-src 'self'`) și fonturile Google ori găzduiește fonturile local. Nu dezactiva global CSP. Pagina conține CSS și JavaScript inline; mută-le în fișiere sau autorizează hash-urile lor dacă politica site-ului o cere.
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

## Prețuri sincronizate

`live-prices.js` citește HTML-ul paginilor celor 14 produse, pe același domeniu și cu sesiunea vizitatorului. Citește doar grupul principal `.product-price-group` din `#product-product .product-info`, inclusiv prețul anterior dacă magazinul îl afișează. Nu citește prețuri din produsele recomandate.

Citirea se face la deschidere, revenire în filă și la fiecare 120 de secunde cât timp pagina este vizibilă, cu maximum trei cereri simultane și timeout de 10 secunde. Nu este o conexiune push: modificările apar la următoarea citire, în funcție și de cache-ul magazinului/CDN-ului. Estimarea minimă pe categorie apare doar dacă toate produsele categoriei au preț valid. Nu sunt presupuse reduceri procentuale sau stocuri.

Dacă o pagină nu răspunde, structura ei se schimbă ori prețul nu este în lei, apare „Vezi prețul în magazin”. Valorile precedente sunt eliminate după o eroare; în orice caz expiră după maximum trei minute. Nu există fallback numeric din `catalog.json`. În browsere fără JavaScript rămân imaginile, produsele și linkurile, fără prețuri vechi.

Acest mecanism nu necesită backend nou, însă implică până la 14 cereri de pagini la o reîmprospătare completă. Pentru trafic mare de Black Friday, soluția preferată este un endpoint de catalog în backend care returnează toate prețurile într-o singură cerere, respectând sesiunea și regulile comerciale. Acesta necesită acces la sursele magazinului. Verifică încărcarea pe staging înaintea activării; un timeout nu va afișa un preț vechi.

## Verificarea înainte de activare

- Desktop și mobil: landingul se deschide; închiderea și Escape readuc homepage-ul fără scroll blocat; focusul revine la elementul anterior.
- Pagini de produs/categorie/coș: suprapunerea nu se deschide.
- Modifică un preț pe staging: acesta se schimbă în toate cardurile landingului la următoarea actualizare; prețul anterior dispare dacă oferta a fost retrasă.
- Verifică prețul pentru vizitator și client autentificat; eventualele variante, cantități și discounturi din coș se confirmă la comandă.
- Simulează o eroare de rețea: cardul invită la verificarea în magazin. Nu afișează valoarea veche.
- Verifică CSP, protecția anti-bot, cache-ul și încărcarea cu utilizatori concurenți. Dacă magazinul modifică prețul prin alt script după încărcare, adaptează integrarea la sursa acelui preț înainte de lansare.

## Dezactivare

Elimină scriptul inserat sau setează `data-enabled="false"`, apoi golește cache-ul homepage-ului. Landingul direct rămâne la `/black-friday/`; îl poți elimina separat. Nu se schimbă template-ul original al homepage-ului.

## Test local

Rulează `python3 black-friday/tools/preview.py --port 8765` și deschide `http://127.0.0.1:8765/`. Homepage-ul este demonstrativ. Serverul de test citește numai paginile publice ale produselor din lista permisă; nu se publică pe site și nu accesează contul vizitatorului. Un server static simplu poate afișa designul, dar nu poate simula paginile magazinului pentru prețuri.

Testele automate necesită Node.js și dependențele de dezvoltare: din `black-friday`, rulează `npm ci` și `npm test`. Nu sunt necesare pe serverul magazinului.

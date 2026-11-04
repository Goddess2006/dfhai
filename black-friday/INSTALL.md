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

Landingul afișează numai reducerile indicate de utilizator: întreaga gamă de exterior 20% (inclusiv adezivii exterior afișați), tapet 30% exclusiv pentru Carrara Best în stoc și interior până la 40% exclusiv pentru Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5, în limita stocului disponibil pe site. Nu există prețuri, valori de rezervă, cereri de preț către magazin sau actualizări automate.

`campaign.js` gestionează numai căutarea produselor și navigarea pe categorii. Fotografiile sunt locale. `catalog.json` păstrează denumirile, linkurile și proveniența imaginilor, fără valori numerice ale prețurilor; nu este necesar în pachetul de producție.

## Verificarea înainte de activare

- Desktop și mobil: verifică prezentarea reducerilor și fotografiilor.
- Închiderea și Escape readuc homepage-ul fără scroll blocat; focusul revine la elementul anterior.
- Suprapunerea nu apare pe paginile de produs/categorie/coș și rămâne închisă în sesiunea curentă după închidere.
- Linkurile deschid produsele în magazin, în fereastra principală.
- Confirmă configurarea efectivă a reducerilor și regulilor de eligibilitate în magazin și perioada campaniei. Landingul comunică ofertele; nu modifică prețurile sau reducerile din magazin.
- Verifică politica CSP și permisiunea de încadrare pe același domeniu.

## Dezactivare

Elimină scriptul inserat sau setează `data-enabled="false"`, apoi golește cache-ul homepage-ului. Landingul direct rămâne la `/black-friday/`; îl poți elimina separat. Nu se schimbă template-ul original al homepage-ului.

## Test local

Rulează `python3 black-friday/tools/preview.py --port 8765` și deschide `http://127.0.0.1:8765/`. Homepage-ul este demonstrativ. Serverul servește numai fișiere locale și nu se publică în magazin. Un server static simplu poate afișa de asemenea landingul.

Testele automate necesită Node.js și dependențele de dezvoltare: din `black-friday`, rulează `npm ci` și `npm test`. Nu sunt necesare pe serverul magazinului.

## Selecția actuală și stocul

Selecția a fost verificată la 4 noiembrie 2026: toate cele opt modele de interior și 18 variante Carrara Best aveau stoc indicat pe paginile produselor. Au fost excluse variantele Carrara Best 85602, 85613 și 85615, marcate `PreOrder` (la comandă). Pentru 82663 și 82653, stocul pozitiv a fost confirmat în grupul principal `product-stock in-stock`, deoarece datele structurate nu declarau disponibilitatea.

Nu există sincronizare automată a stocului. Înaintea lansării, verifică din nou stocurile în magazin; nu include produse la comandă. `catalog.json` păstrează eligibilitatea, proveniența și rezultatele verificării, fără prețuri. Reface HTML-ul după actualizarea selecției cu `python3 black-friday/tools/render.py`, apoi regenerează arhiva. Reaprovizionarea nu extinde automat campania.

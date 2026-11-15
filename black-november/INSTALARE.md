# Black November · NMC România — instalare (OpenCart 3 / Journal 3)

Landing page static: `index.html` + `bn.css` + `bn.js` + `assets/` (59 imagini, ~3,3 MB). Nu are nevoie de bază de date, OCMOD sau modificări în temă.

## Publicare
1. Dezarhivează `nmc-black-november.zip` în rădăcina publică a magazinului (lângă `index.php`), ca să obții `https://www.nmcromania.ro/black-november/`.
2. Deschide pagina pe desktop și pe mobil. Pune un link din meniu, din slider-ul de pe homepage sau din bannere către `/black-november/`.
3. Golește cache-ul Journal 3 sau al CDN-ului, dacă există.

## Afișare peste homepage (înainte ca vizitatorul să intre în magazin)
După ce `/black-november/` funcționează, adaugă O SINGURĂ DATĂ pe homepage, înainte de `</body>`:

```html
<script defer src="/black-november/homepage-overlay.js"></script>
```

Unde se pune în OpenCart 3:
- **Journal 3:** Journal › Skins › (skinul activ) › Custom Code › „Footer” (sau „Custom JS” fără tagul `<script>`, folosind varianta JS de mai jos).
- **Fără Journal:** `catalog/view/theme/<tema>/template/common/footer.twig`, înainte de `</body>`. Apoi Extensii › Modificări › Refresh și golește cache-ul temei.

Dacă editorul acceptă doar JavaScript, fără taguri HTML:

```js
(function(){var s=document.createElement('script');s.src='/black-november/homepage-overlay.js';s.defer=true;document.body.appendChild(s);})();
```

Ce face:
- **Unde apare:** doar pe homepage (`/`, `/index.php`, `index.php?route=common/home`), pe tot ecranul, deasupra site-ului.
- **Butonul de închidere:** „Intră în magazin ×” (sus-dreapta) sau tasta Escape închid landing-ul și lasă clientul pe homepage.
- **Linkurile:** orice link spre un produs sau o categorie deschide pagina în fereastra principală. Navigarea pe secțiuni (#exterior, #interior…) rămâne în landing.
- **Coșul:** „Adaugă în coș” funcționează și din landing; coșul se vede după închidere.
- **Frecvența:** apare o dată pe sesiune de navigare (implicit). Opțiuni: `data-frequency="day"` (o dată la 24 de ore) sau `data-frequency="always"` (pentru test).
- **Data de final:** după 1 decembrie 2026, 00:00, nu mai apare automat (`data-ends="..."` pentru altă dată).
- **Test:** `https://www.nmcromania.ro/?bn=1` forțează afișarea.
- **Dezactivare rapidă:** `data-enabled="false"` pe tag sau ștergerea liniei. Un buton/banner poate redeschide landing-ul cu `window.NMCBlackNovember.open()`.
- **Antetul de securitate:** dacă serverul trimite `X-Frame-Options: DENY` sau CSP `frame-ancestors 'none'`, iframe-ul nu se încarcă. Trebuie `SAMEORIGIN` / `frame-ancestors 'self'`.

## Regula campaniei: fără prețuri pe produse
„Prețuri speciale” apare doar în mesajele generale (hero, benzi, secțiuni). Pe produse nu se afișează prețuri, procente sau alte cifre. Clientul vede prețul special pe pagina produsului din magazin. `build.py` refuză să genereze pagina dacă apare „lei” în HTML.

## Ce face scriptul `bn.js` pe domeniul magazinului
Când pagina rulează pe `nmcromania.ro`, scriptul citește pagina fiecărui produs (aceeași origine, fără API):
- **Stocul.** Produsele fără stoc apar cu „Disponibil la comandă”.
- **Butonul „Adaugă în coș”.** Folosește `index.php?route=checkout/cart/add` și apare doar la produsele în stoc, fără opțiuni.

Testat cu paginile reale ale produselor, cu răspunsul coșului simulat. Butonul de coș nu a fost testat cu un coș real.

Fără JavaScript, sau deschisă pe alt domeniu, pagina rămâne complet funcțională: butoanele duc la pagina produsului.

## Modificări
Textele, produsele, linkurile și imaginile sunt în `tools/build.py` (CAMPANIE, PRODUSE, BLOG, CERCURI).
Rulează `python3 tools/build.py`, apoi `python3 tools/package.py`.

## De verificat înainte de lansare
- **Afirmațiile din pagină.** Textele folosite au sursă pe site, la `/despre-noi`: „peste 20 de ani”, „lider de piață”, „linie de producție proprie”, „stocuri mari”, „prezenți în lanțurile DIY”. Formulările „cel mai bun preț din România” și „cele mai mari stocuri din România” NU sunt folosite, pentru că superlativele absolute cer dovezi (publicitate comparativă). Pagina folosește „cel mai bun raport calitate–preț”.
- **Produse fără stoc la 15.11.2026:** NP27, NFC112 (preț la cerere), A114 și kitul Linea. Pagina le marchează „Disponibil la comandă”.
- **Data de final.** Campania se încheie pe 30.11.2026, 23:59 (countdown-ul se ia din `CAMPANIE["sfarsit"]`).

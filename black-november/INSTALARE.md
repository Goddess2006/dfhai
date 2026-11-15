# Black November · NMC România — instalare (OpenCart 3 / Journal 3)

Landing page static: `index.html` + `bn.css` + `bn.js` + `assets/` (59 imagini, ~3,3 MB). Nu are nevoie de bază de date, OCMOD sau modificări în temă.

## Publicare
1. Dezarhivează `nmc-black-november.zip` în rădăcina publică a magazinului (lângă `index.php`), ca să obții `https://www.nmcromania.ro/black-november/`.
2. Deschide pagina pe desktop și pe mobil. Pune un link din meniu, din slider-ul de pe homepage sau din bannere către `/black-november/`.
3. Golește cache-ul Journal 3 sau al CDN-ului, dacă există.

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

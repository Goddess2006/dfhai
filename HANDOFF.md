# Handoff

Ultima actualizare: 2026-11-05
Agent: Codex

## Adaptare grafică premium — Codex, 2026-11-05
Livrare: `etichete-mostre/premium/`. Două variante finale independente: `etichete-mono-A4.pdf` și `etichete-color-A4.pdf`, fiecare cu 4 etichete de 105 × 148,5 mm pe o coală A4. Previzualizare alăturată: `comparatie.png`; surse HTML/CSS, fonturi locale și generator comun incluse. Originalele lui Claude sunt păstrate.
Design: tipografie editorială aliniată la stânga, sigla oficială păstrată, ilustrația SVG și cele cinci secțiuni generice preluate din original. Color: verde închis/ivoire/auriu; mono: exclusiv tonuri de gri, inclusiv sigla și ilustrația. Bloc vânzător distinct cu site, telefon, nume firmă, sediu, CUI și ONRC. Date preluate din https://decoflair.ro/contact la 05.11.2026. QR original păstrat, cu zonă albă de protecție adăugată. Fără preț sau cod produs; secțiunile sunt marcate „Forme ilustrative”. Mențiunea „Bară 2 m” omisă deoarece rămăsese neconfirmată pentru întreaga colecție.
Verificare: Chromium/Playwright; ambele PDF-uri au exact o pagină A4; patru etichete fără overflow, fonturi locale încărcate, imagini încărcate. Ambele QR-uri decodate din PNG-ul etichetei spre https://decoflair.ro/bagheta-polistiren; scanare pixel cu pixel: zero pixeli colorați în varianta mono. Comparația vizuală inspectată. Reproducere în README.md din folderul premium; dependențe Node fixate în package-lock.json. PDF RGB pentru imprimare uzuală, fără bleed; accentele aurii sunt culoare imprimată, nu folie metalică. Tipar 100% / Actual size, fără ajustare la pagină.

## Nou: etichete paletar mostre — baghete de tavan din polistiren (Deco&Flair)
Folder: `etichete-mostre/`
- `etichete-baghete-A4.pdf` — coala de tipar: 4 etichete A6 (105×148,5 mm) pe A4, linii punctate de tăiere. Tipar la 100% / „Actual size”.
- `etichete-baghete-A4.html` — sursa (CSS + JS/SVG inline). Ilustrația camerei și secțiunile profilelor sunt generate în JS; fonturi Google (Cormorant Garamond, Montserrat).
- `eticheta-preview.png` — previzualizare o etichetă; `logo-decoflair.png` — sigla oficială de pe decoflair.ro (450×173 px, sursa: https://decoflair.ro/image/cache/catalog/logo-deco-wide-450x173.png; rezoluție mică — de înlocuit cu vectorial dacă îl furnizează utilizatorul).
Conținut: sigla, titlul „Baghete de tavan” + „din polistiren”, ilustrație desenată (cornișă de jur împrejur pe tavan, rozetă, lustră), 4 avantaje (Ultraușoare, Montaj rapid, Se vopsesc, Bară 2 m), „Secțiuni profile” cu 5 secțiuni generice (Concav, Clasic, Modern, Minimalist, Elegant), QR spre https://decoflair.ro/bagheta-polistiren și decoflair.ro.
Cerințe utilizator: eticheta e pentru TOATĂ colecția — fără cod produs, fără preț. Secțiunile sunt forme tipice, nu copii ale modelelor din catalog. De confirmat cu utilizatorul: „Bară 2 m” (toate modelele văzute pe site au 2000 mm).
Re-generare PDF: Playwright/Chromium → `page.pdf({format:'A4', printBackground:true, margin 0})`.

## Context anterior (Codex — Black Friday NMC)

Ultima actualizare: 2026-11-04
Agent: Codex
Stare: Reguli finale: −20% la toate PROFILELE de exterior, EXCLUSIV adezivi; −30% doar Carrara Best în stoc; interior până la −40% exclusiv Z21, Z11, WO2, WT25, FD3, FO1, L2, L5; ADRO-FIX exterior 1,5 kg −30%; ADRO-FIX 4 kg la preț întreg. Toate ofertele sunt în limita stocului disponibil pe site. Fără prețuri numerice.
Design: există acum DOUĂ variante. Varianta 1 `/black-friday/` este păstrată identic, byte cu byte. Varianta 2 `/black-friday/varianta-2/` folosește aceleași produse, oferte și ordine a secțiunilor, cu sigla reală NMC în alb-negru, inscripții Black Friday laterale mai pronunțate, o bandă animată lent, reflexie discretă în titlu și interacțiuni mai vii. Mișcarea este dezactivată la prefers-reduced-motion. CSS-ul suplimentar este varianta-2/variant.css.
Logo: sursa oficială este https://www.nmcromania.ro/image/cache/catalog/logo4-307x189.png, descărcată ca assets/nmc-logo-original.png și inspectată. Varianta 2 folosește filtrare CSS grayscale/brightness/contrast pentru fundal negru și litere albe, fără portocaliu. Nu se redesenează sigla. Proveniența este în catalog.json/brandLogo.
Imagini: fotografii ambientale reale din galeria Z11, galeria Carrara Best 82671 și bannerul exterior al homepage-ului, inspectate înainte de integrare. CSS folosește treimea dreaptă arhitecturală din bannerul exterior, pentru a omite textul din original. Sursele sunt în catalog.json/ambientImages; fotografiile sunt salvate local și incluse în pachet.
Date: 32 produse plus 3 vedete duplicate în prezentare. Stocurile celor 4 exemple exterior și 2 adezivi au fost reverificate la 04.11.2026: toate în stoc. Cele 8 modele interior și 18 variante Carrara Best păstrează verificarea din aceeași zi; variantele PreOrder 85602, 85613, 85615 sunt excluse. Stocurile nu sunt sincronizate automat. Calificativul „până la” este păstrat la interior.
Implementare: tools/render.py generează ambele variante din aceeași sursă și aceleași reguli. Pachetul release/nmc-black-friday.zip include ambele variante și resursele comune. homepage-overlay.js acceptă data-variant="2" pentru suprapunerea noii variante; implicit rămâne varianta 1. INSTALL.md documentează alegerea. Fără acces NMC/staging și fără publicare externă.
Verificare: 11 teste Node/linkedom au trecut, inclusiv identitatea ofertelor între variante, sigla oficială în varianta 2 și alegerea variantei pentru overlay. Confirmat că HTML-ul variantei 1 este identic cu versiunea anterioară. Structura HTML, ID/ancore, resursele relative ale ambelor variante și integritatea arhivei verificate. Ambele URL-uri de preview răspund HTTP 200 la localhost:8765. Fără verificare vizuală automată în browser.
Context anterior: utilizatorul vizat pe server este `dfh`; restricția SSH root (`PermitRootLogin prohibit-password`) e efectivă. `test.txt` conține `123`.
Următorul pas: utilizatorul compară variantele 1 și 2. Înaintea activării pe NMC, persoana cu acces confirmă stocurile și ofertele/perioada în magazin și instalează varianta aleasă.

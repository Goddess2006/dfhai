# Handoff

Ultima actualizare: 2026-11-04
Agent: Codex
Stare: Campania a fost restrânsă conform noilor reguli. Utilizatorul a clarificat explicit că reducerea de tapet vizează numai Carrara Best, nu Carrara 3.
Oferte: −20% la întreaga gamă de exterior, inclusiv adezivii exterior afișați. Interior: până la −40% exclusiv pentru Z21, Z11, WO2, WT25, FD3, FO1, L2, L5, în limita stocului disponibil. Tapet: −30% exclusiv Carrara Best în stoc. Condițiile sunt explicite în panouri, carduri, secțiuni și FAQ; nu se afișează prețuri.
Selecție: 32 produse: 4 exemple exterior, 2 adezivi exterior, cele 8 modele de interior și 18 variante Carrara Best. Toate cele 8 modele de interior aveau stoc indicat pe paginile reale la verificarea din 04.11.2026. Din Carrara Best au fost excluse 85602, 85613, 85615 (PreOrder). La 82663 și 82653 stocul pozitiv a fost confirmat în product-stock in-stock, deoarece availability lipsea din datele structurate. Nu există sincronizare automată de stoc; pagina precizează data selecției și confirmarea stocului actual în magazin.
Implementare: catalogul fără prețuri include proveniența imaginilor, modelele, verificarea disponibilității și excluderile. `tools/render.py` generează HTML-ul din catalog și regulile de prezentare. După modificarea selecției rulează rendererul și `tools/package.py`. Imaginile vechi din selecțiile neeligibile au fost eliminate. `INSTALL.md` și pachetul ignorat `release/nmc-black-friday.zip` sunt actualizate.
Suprapunere: mecanismul existent de homepage cu închidere/Escape și memorare în sesiune rămâne funcțional. Nu există acces la magazin/staging și nu s-a publicat extern.
Verificare: selecția exactă a celor 8 modele, cele 18 variante Carrara Best în stoc, excluderea variantelor PreOrder din HTML, lipsa produselor vechi neeligibile și a prețurilor, structura HTML/ancore/resurse, răspuns HTTP preview și `git diff --check`. Cele 5 teste existente pentru overlay/navigare au trecut. Fără verificare vizuală automată în browser.
Context anterior: utilizatorul vizat pe server este `dfh`; restricția SSH root (`PermitRootLogin prohibit-password`) e efectivă. `test.txt` conține `123`.
Următorul pas: feedback pe vizual; înaintea lansării trebuie reverificate stocurile în magazin, confirmate procentele individuale la interior/perioada campaniei și instalat pachetul de persoana cu acces la NMC.

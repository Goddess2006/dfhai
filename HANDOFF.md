# Handoff

Ultima actualizare: 2026-11-04
Agent: Codex
Stare: Landingul Black Friday a fost refăcut vizual la cererea utilizatorului, fără prețuri. Temă neagră, galbenă și roșie, hero editorial cu fotografii reale, trei panouri comerciale și secțiuni de produse.
Oferte comunicate conform instrucțiunii utilizatorului: exterior −20%, tapet −30%, interior până la −40%. Calificativul „până la” este păstrat la interior în hero, panouri, navigare și carduri. Adezivii sunt produse complementare, fără reducere atribuită.
Implementare: `index.html`, `polish.css` și `campaign.js`; 14 produse cu fotografii locale. Au fost eliminate `live-prices.js`, testele lui, toate sloturile/mesajele de preț și valorile istorice de preț din `catalog.json`. Landingul nu mai face cereri pentru prețuri. Scriptul campaniei gestionează numai filtrarea și categoria activă.
Suprapunere: mecanismul existent `homepage-overlay.js` + `overlay-bridge.js` rămâne funcțional, cu închidere prin buton/Escape, păstrarea homepage-ului dedesubt și memorare în sesiunea filei. Nu există acces la magazin/staging și nu s-a publicat extern.
Livrare: `INSTALL.md` a fost actualizat pentru varianta fără prețuri; `tools/package.py` generează `black-friday/release/nmc-black-friday.zip`, ignorat în Git. Serverul local `tools/preview.py` este acum complet static, fără proxy către produse. Previziualizarea noii pagini a fost solicitată în panoul browser la `http://localhost:8765/black-friday/`.
Verificare: 5 teste existente pentru overlay/navigare au trecut. Verificate structura HTML, unicitatea ID-urilor, ancorele, imaginile și scripturile locale, procentele, absența prețurilor, răspunsul HTTP de preview și `git diff --check`. Nu a fost disponibilă verificarea vizuală automată în browser.
Context anterior: utilizatorul vizat pe server este `dfh`; restricția SSH root (`PermitRootLogin prohibit-password`) e efectivă. `test.txt` conține `123`.
Următorul pas: feedback pe noul vizual; persoana cu acces la NMC confirmă reducerile efective și perioada campaniei și instalează pachetul dacă se aprobă vizualul.

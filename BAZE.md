# BAZE și EXTRANET — documentație și date sursă

Două foldere locale în rădăcina workspace-ului comun Claude Code + Codex:

| Folder | Cale | Rol |
|---|---|---|
| **BAZE** | `/home/dfh/workspace/BAZE` | baze de date (DistribNet), imagini catalog produse, date suplimentare |
| **EXTRANET** | `/home/dfh/workspace/EXTRANET` | documentație / materiale extranet (conținut de inventariat la prima sesiune locală) |

**Locație BAZE:** `/home/dfh/workspace/BAZE`.

De aici se iau datele suplimentare pentru toate proiectele: baze de date, imagini catalog produse, liste de prețuri, documentație.

## Reguli
- Ambele foldere (`BAZE/`, `EXTRANET/`) sunt în `.gitignore`: **nu se comite pe GitHub** (conține baza de clienți, prețuri interne, fișiere mari). Se citește local de ambii agenți.
- Sesiunile Claude Code din cloud (claude.ai/code) **nu** au acces la el — acolo fișierele trebuie trimise în chat sau copiate punctual în repo (doar ce nu e confidențial, ex. imagini de produs).
- Când un proiect folosește ceva din BAZE, notează în `HANDOFF.md` ce fișier, ce câmpuri și cum se reface (script / comandă), cu cale relativă `BAZE/...`.
- Nu modifica fișierele din BAZE / EXTRANET (sunt surse); scrie rezultatele în folderul proiectului.
- La prima sesiune locală care deschide EXTRANET: inventariază pe scurt conținutul (subfoldere, tipuri de fișiere, la ce folosesc) în secțiunea de mai jos.

## EXTRANET — conținut
_De completat la prima sesiune locală (cloud-ul nu are acces)._

## Ce știm până acum despre date (2026-11-24)
- **Gestiune: DistribNet 3.2** (NMC STIL DISTRIBUTION SRL), tabele Visual FoxPro (.dbf) grupate în containere `marfa.dbc`, `fin.dbc`, `dl.dbc`, `altele.dbc`. Copie pe rețea: `\\rds.nmc.local\Backup\baze`.
- `preturi.dbf` (marfa.dbc): CODPR, CATPRET (nr. listă), PRETVANZ (lei cu TVA), PRETVAL + CODVAL (1 = EUR). Lista NMC05.10.26 = CATPRET 90 (prețuri = nmcromania.ro cu TVA).
- `client.dbf` (dl.dbc): CODCLI, NUMECLI, ADRESA, INVECHIT; clienții cu prefix „XXX” sunt dezactivați.
- Avize Metro (meniul „Vânzare Metro”, raport `aviztrmetro_nou_netipizat.frx`): câmpuri NRAVIZ, CODPR, CODPRMETRO, CODMARE, DENPROD, CANTIT, PVANZFTVA, CODLOCM, DENLOCM, LOCALITATE, NRDL, FACTOUT, DATA, NUMECLI, GREUTATE. Tabelul DBF exact încă neconfirmat.
- DL-uri cursă (raport „facturi_nmc”): NRDL, FIRMA, NRFACTURA, SUMDEINCAS (cu TVA), GR_DL, INCASAT, NRCHITANTA.
- Liste de prețuri EUR fără TVA pentru parteneri: `nmc-calculator-oferta/data/liste-eur/` (Interior Premium 05.10.2026, Selit, Izolații țeavă).

## Folosit de
- `nmc-calculator-oferta/` — foaia NMC Parteneri (prețuri lista 90, clienți) și foaia Borderou livrări (avize / facturi, DL-uri). În browser se conectează la folderul bazei prin „Conectează folderul bazei” (poate fi `BAZE/...` local sau `\\rds.nmc.local\Backup\baze`).
- `nmc-analiza-online/` — analiza vânzărilor agentului MAGAZIN ONLINE la preț de listă vs. discount (facturi + linii, client.dbf, agenți, preturi.dbf, denumiri liste); sincronizare automată cu folderul bazei.

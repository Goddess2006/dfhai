# Calculator ofertă NMC · Deco&Flair

Trei foi (taburi sus): **NMC România** (catalog nmcromania.ro, 561 produse, nr. NMC-AAAA-0001) **NMC Parteneri** (prețuri din lista de parteneri a gestiunii, ex. NMC05.10.26, nr. NMCP-AAAA-0001) și **Deco&Flair** (catalog decoflair.ro, 989 produse, nr. DF-AAAA-0001, sigla și datele firmei Deco & Flair Hub SRL). Fiecare foaie are oferta, numerotarea și ciorna ei. Link direct: `Calculator-Oferta.html#decoflair` sau `#nmc`.

**Pe desktop:** copiază `Calculator-Oferta.html` pe Desktop și deschide-l cu dublu-clic (Chrome / Edge). Fișier unic, funcționează și fără internet. (`index.html` e același fișier.)

- Căutare produse după cod sau denumire (561 produse, coduri „Model” și prețuri cu TVA de pe nmcromania.ro); filtru pe categorii; Enter adaugă primul rezultat.
- Cantitate, preț unitar **fără TVA** și **cu TVA** editabile pe fiecare rând (în RON sau EUR, în toate foile; celălalt preț se recalculează) (se vede „preț site” + „revino” dacă prețul a fost schimbat); rând liber pentru produse/servicii în afara catalogului.
- Discount în % sau valoare (RON/EUR), aplicat doar la produse.
- Transport: flotă NMC 242 lei cu TVA, curier 150 lei cu TVA, sau fără transport.
- RON ⇄ EUR, curs euro editabil; totaluri cu TVA 21%, fără TVA și echivalent în cealaltă monedă.
- Nr. comandă automat (NMC-AAAA-0001, crește la „Ofertă nouă”, editabil), data automată, date client, informații suplimentare.
- **Descarcă PDF** (A4, generat direct în pagină, cu diacritice) și **Descarcă Word** (.docx real, editabil), denumite `Oferta-<nr>-<client>`.
- **Trimite pe e-mail:** destinatar (din e-mailul clientului) + subiect; „Outlook / Mail” sau „Gmail” descarcă PDF-ul și deschid un e-mail completat cu rezumatul ofertei (PDF-ul se atașează din Descărcări); „Partajează PDF-ul” apare unde Windows permite trimiterea directă a fișierului.
- „Printează”, „Copiază text”. Oferta curentă se păstrează automat în browser.

Biblioteci incluse local (data/lib): jsPDF 2.5.1, jspdf-autotable 3.8.2, Roboto (subset cu diacritice). Word-ul e generat de `export.js` (zip propriu, fără bibliotecă).

## Oferte salvate
Fiecare ofertă se salvează automat (IndexedDB, în browser) cât lucrezi la ea. Butonul „Oferte salvate” le listează (pe foaie sau toate), cu căutare după nr. comandă, client, CUI sau dată: **Deschide** (o reîncarci și o editezi; modificările se salvează în aceeași ofertă), **Duplică** (copie cu număr nou și data de azi), **Șterge** (cu confirmare). „Descarcă backup” salvează toate ofertele într-un .json; „Restaurează din backup” le aduce înapoi (și pe alt calculator).

## Gestiune NMC — schema cunoscută
`preturi.dbf` (marfa.dbc): CODPR, CATPRET (nr. listă), PRETVANZ (lei, cu TVA). Lista NMC05.10.26 = **CATPRET 90** (754 articole; prețurile coincid cu prețurile cu TVA de pe nmcromania.ro, ex. cod 2875 = NA102 = 71,06 lei). `client.dbf` (dl.dbc): CODCLI, NUMECLI, ADRESA, INVECHIT; clienții cu prefix „XXX” sau învechiți sunt ignorați. Denumirile/UM ale articolelor vin din tabelul de articole din același folder (detectat automat după CODPR + DENUMIRE); fără el, rândurile apar ca „Articol cod …”.

Actualizare prețuri: `python3 tools/scrape.py nmc && python3 tools/scrape.py decoflair && python3 build.py`.

## Foaia NMC Parteneri
**Automat, din baza gestiunii (Chrome/Edge):** „Conectează folderul bazei” → alegi o dată `\\rds.nmc.local\Backup\baze`. Calculatorul citește direct tabelele Visual FoxPro (.dbf), găsește singur tabelul cu lista NMC05.10.26 (caută valoarea în tabelele mici, ia codul listei și tabelul de prețuri care îl folosește), tabelul de articole (cod, denumire, UM) și tabelul de clienți (denumire + cod fiscal; furnizorii sunt ocoliți). La fiecare deschidere a foii se resincronizează singur dacă browserul a păstrat permisiunea (în Chrome/Edge alege „Permite la fiecare vizită”), altfel un clic pe „Sincronizează acum”. „Setări bază” arată ce tabele/câmpuri au fost alese și permite corectarea; „Copiază structura bazei” copiază doar numele tabelelor și câmpurilor.

**Manual (orice browser):**
- Datele vin din programul de gestiune prin **import de fișier** (Excel .xlsx/.xls, CSV, .dbf sau .ods): butoanele „Importă lista de prețuri” și „Importă clienții” de deasupra foii.
- La import, calculatorul ghicește coloanele (cod, denumire, UM, preț; pentru clienți: denumire, CUI, Reg. Com., adresă, localitate, județ, telefon, e-mail) și arată o previzualizare; le poți corecta din liste. Dacă tabelul are mai multe liste de preț, alegi coloana listei și lista (se preselectează NMC05.10.26). Bifezi dacă prețurile din fișier includ TVA (implicit: fără TVA, se adaugă 21%).
- Datele importate rămân doar în browserul de pe calculatorul tău (nu se urcă nicăieri, nu sunt în repo). Re-importă când se schimbă lista.
- Client: câmpul de căutare din „Date client” (nume, CUI, localitate) completează automat datele clientului.
- Discount pe fiecare produs (coloana „Disc. %”) + discount general (pe produse, după discountul pe linie). Rândurile bifate „Serv.” sunt servicii: nu primesc niciodată discount; transportul nu primește niciodată discount. Articolele cu „montaj/manoperă/serviciu/transport…” în denumire sunt bifate automat ca servicii.

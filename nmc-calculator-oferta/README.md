# Calculator ofertă NMC

Deschide `index.html` în browser (fișier unic, funcționează și offline, fără server).

- Căutare produse după cod sau denumire (561 produse, coduri „Model” și prețuri cu TVA de pe nmcromania.ro); filtru pe categorii; Enter adaugă primul rezultat.
- Cantitate și preț unitar editabile (se vede „preț site” + „revino” dacă prețul a fost schimbat); rând liber pentru produse/servicii în afara catalogului.
- Discount în % sau valoare (RON/EUR), aplicat doar la produse.
- Transport: flotă NMC 242 lei cu TVA, curier 150 lei cu TVA, sau fără transport.
- RON ⇄ EUR, curs euro editabil; totaluri cu TVA 21%, fără TVA și echivalent în cealaltă monedă.
- Nr. comandă automat (NMC-AAAA-0001, crește la „Ofertă nouă”, editabil), data automată, date client, informații suplimentare.
- „Printează / PDF” (A4, fără butoane și câmpuri goale), „Copiază oferta (text)”. Oferta curentă se păstrează automat în browser.

Actualizare prețuri: `python3 tools/scrape.py && python3 build.py`.

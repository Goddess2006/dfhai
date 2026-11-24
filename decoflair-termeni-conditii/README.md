# Termeni și condiții — decoflair.ro (actualizare 24.11.2026)

Fișier de publicat: `termeni-si-conditii.html` (fragment HTML cu stil propriu, prefixat `.df-tc`, nu afectează restul temei).

## Cum se publică (OpenCart + Journal3)
1. Admin → Catalog → Informații → „Termeni și condiții” (information_id=3) → tab-ul limbii române.
2. În editor apăsați butonul **Cod sursă** (`</>`), ștergeți tot conținutul vechi și lipiți integral conținutul fișierului.
3. Tab SEO:
   - Meta Title: `Termeni și condiții | Deco & Flair`
   - Meta Description: `Termenii și condițiile de vânzare decoflair.ro: comenzi, plată, livrare, dreptul de retragere în 14 zile, garanția legală de conformitate și date de contact.`
4. Salvați și goliți cache-ul temei (Journal → System → Clear cache).

## De corectat în altă parte pe site (adresa veche Făurei nr. 1, Sector 1)
- Pagina Contact (`/contact`) și subsolul site-ului.
- Politica de retur (`/politica-retur`) — secțiunile 1 și 3.
- Politica de confidențialitate, setările magazinului (System → Settings → Store → Address), antetul facturilor/proformelor și e-mailurile automate.

## Recomandări legale suplimentare
- Butonul „Retrageți-vă din contract aici” trebuie să fie vizibil permanent (de ex. în subsol și în contul de client) — OUG 18/2026, aplicabilă din 19.06.2026. Formularul `/formular-retur` nu ar trebui să ceară obligatoriu motivul pentru retragere și trebuie să trimită automat confirmare pe e-mail cu data și ora.
- Eliminați pictograma/linkul SOL (platforma ODR a UE a fost închisă la 20.07.2025); păstrați pictograma ANPC – SAL.
- Politica de retur trebuie să indice costul estimat de retur pentru produsele agabaritice (textul T&C trimite acolo).
- Transpunerea Directivei (UE) 2024/1799 (dreptul la reparare) este încă în proiect la ANPC; la adoptare, secțiunea 11 se actualizează.

# Despre noi — decoflair.ro

Fișier de publicat: `despre-noi.html` (stil scopat `.df-dn`). Admin → Catalog → Informații → „Despre noi” → Cod sursă (`</>`) → înlocuiți tot conținutul → Salvare → Clear cache.
Textul păstrează mesajul original, mai aerisit: Cine suntem, Ce găsiți la noi (4 game, cu linkuri), Cum vă ajutăm (consultanță, randare 3D, produse personalizate, livrare), citatul final și **Date de identificare** (sediu Str. Renului nr. 3, Sector 2; tel. 0765 740 280).
Blocul FAQ de sub pagină este un modul Journal separat și nu se modifică prin acest fișier. De corectat în el: „garanție conform standardelor europene” → „garanția legală de conformitate de 2 ani (OUG 140/2021)”; verificați și afirmația despre tutorialele video „pentru fiecare gamă”.

# Politica de retur — decoflair.ro

Fișier de publicat: `politica-retur.html` (stil scopat `.df-pr`). Admin → Catalog → Informații → „Politica de retur” → Cod sursă (`</>`) → înlocuiți tot conținutul → Salvare → Clear cache.
Conținutul juridic existent a fost păstrat și reorganizat; schimbări: sediu Str. Renului nr. 3, Sector 2; tel. 0765 740 280; e-mail vanzari@decoflair.ro (păstrat); buton „Retrageți-vă din contract aici” sus; cuprins; cost estimat retur pentru produse agabaritice (150 lei curier / 242 lei flotă, ca tarifele de livrare; gratuit dacă e adus la depozit); excepție produse sigilate/igienă; formular de retragere cu linii de completat; trimitere ANPC/SAL.

# Politica de confidențialitate — decoflair.ro

Fișier de publicat: `politica-de-confidentialitate.html` (stil scopat `.df-cf`). Admin → Catalog → Informații → „Politica de confidențialitate” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Rescrisă complet, GDPR: operator cu sediul nou, date colectate, tabel scopuri ↔ temei legal (art. 6), destinatari reali detectați pe site (FAN Courier, NETOPIA, Google Analytics/Tag Manager/reCAPTCHA, Meta Pixel, TikTok Pixel, Microsoft Clarity), transferuri SUA (DPF/SCC), termene de păstrare, cookie-uri, drepturi + termen de răspuns 1 lună, ANSPDCP, securitate, minori.
De verificat: furnizorul de newsletter (nenominalizat) și termenele de păstrare propuse (cont inactiv 3 ani, mesaje fără comandă 2 ani, log-uri 12 luni).

# Notă titluri (H1)
Tema Journal3 afișează deja titlul paginii ca H1 („Termeni și condiții Deco&Flair”, „Politica de retur – Deco&Flair” etc.). Fișierele nu mai conțin H1 propriu, ca să nu apară titlul de două ori. Termenii și Politica de retur, deja publicate cu H1, trebuie relipite din versiunea actuală.

# Politica de utilizare a cookie-urilor — decoflair.ro

Fișier de publicat: `politica-cookie.html` (stil scopat `.df-ck`). Admin → Catalog → Informații → „Politica de utilizare a cookie-urilor” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Rescrisă după inventarul real al cookie-urilor (scanare Playwright, 24.11.2026): necesare (OCSESSID, language, currency, _GRECAPTCHA, NETOPIA), statistică (Google Analytics G-58RZ7V8D9P / G-264NWLB9C0 prin GTM-N6S3P2XC; Microsoft Clarity), marketing (Meta _fbp, TikTok _ttp/ttcsid, Microsoft Advertising/Bing UET _uetsid/_uetvid). Eliminate serviciile inexistente din textul vechi (Yahoo, Pinterest, LinkedIn, WhatsApp, geolocalizare).

## PROBLEMĂ DE CONFORMITATE (de reparat tehnic)
Toate cookie-urile de statistică și marketing (GA, Clarity, Meta, TikTok, Bing UET) se setează **la prima încărcare, înainte de „Accepta toate”**. Încalcă art. 4 alin. (5) din Legea 506/2004 și GDPR. De făcut: în GTM-N6S3P2XC activat Consent Mode v2 (default denied pentru analytics_storage, ad_storage, ad_user_data, ad_personalization), toate tag-urile (GA4, Meta, TikTok, Clarity, UET) declanșate doar după consimțământ; scoase eventualele coduri puse direct în tema Journal3 / modulele OpenCart, în afara GTM; bannerul să trimită update de consimțământ către GTM. Apoi retestat cu browser curat.

# Plata și livrare — decoflair.ro

Fișier de publicat: `plata-si-livrare.html` (stil scopat `.df-pl`). Admin → Catalog → Informații → „Plata și livrare” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Păstrate datele existente (metode de plată, termene 1–2 / 3–5 / 14 / 7–10 zile, tarife 150 lei FAN Courier și 242 lei flotă, km suplimentari, validare telefonică). Adăugate: NETOPIA, IBAN pentru OP, facturare + RO e-Factura, termen legal max. 30 de zile, ridicare gratuită din depozit (adresă, program), verificarea coletului, transferul riscului, anularea la întârziere cu restituire în 14 zile, contact cu datele noi.
De confirmat: tarifele includ TVA; „Visa sau Mastercard”; termenul de recontactare „o zi lucrătoare”; termenele de interior se aplică și pentru tapet/adezivi/accesorii.

# Sugestii și reclamații — decoflair.ro

Fișier de publicat: `sugestii-si-reclamatii.html` (stil scopat `.df-sr`). Admin → Catalog → Informații → „Sugestii și reclamații” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Păstrat: mesajul de deschidere, informațiile necesare pentru reclamație, răspuns în max. 3 zile lucrătoare. Adăugat: telefon 0765 740 280, formularul de retur, adresa poștală (sediul nou), soluționare în max. 30 de zile (aliniat cu T&C) și 15 zile pentru neconformitate (OUG 140/2021), ANPC / SAL / ECC România, protecția datelor. Ton „dumneavoastră”, ca pe celelalte pagini.

# Produse personalizate — decoflair.ro

Fișier de publicat: `produse-personalizate.html` (stil scopat `.df-pp`). Admin → Catalog → Informații → „Produse personalizate” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Textul vechi (repetitiv, două introduceri) a fost condensat: intro + butoane „Cereți o ofertă” / telefon, Ce putem realiza (3 carduri), Materiale și execuție (Chiajna, EPS 120/150/200), Cum lucrăm (5 pași, execuție 7–10 zile lucrătoare ca pe Plata și livrare), ce trebuie trimis pentru ofertă, notă legală (fără drept de retragere, cu garanție de conformitate), caseta finală de ofertă. Telefon 0765 740 280.
Imagini (adăugate ulterior): 11 fotografii deja existente pe server, din `image/catalog/category/` și `image/catalog/categorii produse/exterior/` (fronton, termosistem 2, cheie de boltă, brâuri, solbanc2, butaforie, capiteluri, ancadramente, arcade, cornișă5, coloane). Nu trebuie urcat nimic; dacă imaginile sunt redenumite sau șterse din catalog, pagina trebuie actualizată. Galeria „Inspirație” trimite către categoriile de exterior corespunzătoare.

# Consultanță premium — decoflair.ro

Fișier de publicat: `consultanta-premium.html` (stil scopat `.df-cs`). Admin → Catalog → Informații → „Consultanță” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Mesajul original păstrat, condensat: intro + butoane (telefon 0765 740 280 / e-mail), colaj 3 imagini, Ce înseamnă consultanța (cu imagine), Cum vă ghidăm (5 pași), Unde are loc (showroom / la locație, carduri cu imagini; serviciu premium, cost și durată comunicate la programare), De ce Deco & Flair (6 carduri), casetă de programare cu linkuri spre Randare 3D și Produse personalizate.
Imagini: 7 fotografii din portofoliu, deja pe server (`image/catalog/galerie/` 26, 27, 16, 13, 32, 31), 900×1200, < 160 KB.
De confirmat: existența showroom-ului (pe Contact apare doar depozitul/punctul de ridicare) și faptul că sesiunea este cu plată.

# Randare 3D — decoflair.ro

Fișier de publicat: `randare-3d.html` (stil scopat `.df-rd`). Admin → Catalog → Informații → „Randare” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Păstrat: mesajul, procesul, publicul țintă, video-ul YouTube „Randare Profile decorative – Fatade de exceptie” (oLWAl1k8Fvs), acum responsive și prin youtube-nocookie.com (nu setează cookie-uri YouTube până la redare). Adăugat: butoane telefon / e-mail, colaj din portofoliu (galerie 25, 29, 30), imagine detaliu LED (24), pasul 5 (ofertă pe baza randării), ce trebuie pregătit, casetă finală cu linkuri spre Consultanță și Produse personalizate. Telefon 0765 740 280.
De confirmat: randarea se plătește? (textul spune „termenul și costul în funcție de complexitate”).

# Parteneriate — decoflair.ro

Fișier de publicat: `parteneriate.html` (stil scopat `.df-pt`). Admin → Catalog → Informații → „Parteneriate” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Păstrate: mesajul, beneficiile, cele două imagini existente din `image/catalog/Arhitecti/`. Adăugat: butoane „Deveniți partener” (e-mail cu subiect) / telefon 0765 740 280, 4 tipuri de parteneri (+ constructori/echipe de montaj), 6 beneficii (+ suport tehnic, randări și produse personalizate), linkuri către game, 4 pași de colaborare, casetă finală. Fără promisiuni de discount concrete („condiții comerciale în funcție de volum”).

# Catalogul nostru — decoflair.ro/catalog-produse-decoflair

Fișier de publicat: `catalog-produse.html` (stil scopat `.df-ct`). Admin → Catalog → Informații → „Catalogul nostru” → Cod sursă → înlocuiți tot → Salvare → Clear cache.
Catalog vizual: intro, butoane rapide pe categorii, 5 carduri mari cu imagine (Interior, Exterior, Riflaje 3D, Tapet, Adezivi și accesorii), fiecare cu toate subcategoriile ca linkuri și „Vedeți toate…”, casetă finală (Consultanță, Produse personalizate, Oferte speciale). Toate cele 40+ linkuri și 5 imagini verificate (fără 404); imaginile sunt deja pe server.
Modulul Journal „Catalogul nostru” (Catalog Blocks, ID 682, lista pliabilă de deasupra textului) afișează „Riflaje Acustice 3D” de două ori și dublează conținutul nou: recomandat să fie scos din layoutul paginii (Journal → Layouts → layoutul paginii de informații / Catalogul nostru) sau măcar să se șteargă duplicatul.

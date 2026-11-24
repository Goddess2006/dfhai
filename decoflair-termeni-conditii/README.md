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

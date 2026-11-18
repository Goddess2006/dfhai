# Newsletter Deco&Flair „Ediția 2027”: ghid de trimitere

## 1. Ce ai în folder

| Fișier | La ce folosește |
|---|---|
| `out/newsletter-brevo.html` | **Fișierul de lipit în Brevo** („Paste your code / Lipește codul”). Dezabonarea și „Vezi online” sunt deja legate. |
| `out/newsletter-mailerlite.html` | Același e-mail, cu tag-urile MailerLite. |
| `out/newsletter-themarketer.html` | **Varianta pentru theMarketer**: dezabonare `{{unsubscribe_link}}`, iar sus, în loc de „Vezi online”, un link spre decoflair.ro. |
| `out/newsletter-preview.html` | Doar pentru previzualizare locală (imagini din `img/`). |
| `out/newsletter.txt` | Versiunea text simplu. Lipește-o la „Plain text”: ajută la livrabilitate. |
| `img/` | 27 de imagini optimizate (~1 MB în total), **de urcat înainte de trimitere**. |
| `expert/expert-hq.jpg` | Fotografia expertei la claritate HQ (2228×2824, mărită 2× cu Real-ESRGAN + textură naturală). |
| `PALETA.md` | Paleta 2027 și verificarea de contrast (toate perechile de text trec WCAG AA). |

### Urcarea imaginilor (obligatoriu)
E-mailul caută imaginile la `https://decoflair.ro/image/catalog/newsletter/2026-11/`.
1. Intră în OpenCart, deschide **Image Manager**, creează folderul `catalog/newsletter/2026-11/` și urcă tot conținutul folderului `img/`.
2. Verifică în browser: `https://decoflair.ro/image/catalog/newsletter/2026-11/hero.jpg` trebuie să se deschidă.
3. Dacă vrei alt folder, schimbă `IMG_BASE` în `build.py` și rulează `python3 build.py`.

## 2. Pe ce platformă trimiți ~1000 de e-mailuri

**Recomandare: Brevo** (brevo.com). Are firmă și servere în UE, interfață în română și importă cod HTML propriu chiar și pe planul gratuit.
- **Gratuit:** 300 de e-mailuri pe zi, deci cele 1000 pleacă în 4 zile (vezi tranșele de mai jos). Apare sigla Brevo în subsol.
- **Starter (plătit, lunar):** trimiți tot dintr-o dată, fără siglă. Pentru 1000 de contacte e cel mai mic pachet (în jur de 9 €/lună, verifică prețul actual pe brevo.com/pricing). Îl poți opri după campanie.
- Alternativa este MailerLite, dar acolo editorul de HTML propriu e doar pe planurile plătite.

**Nu trimite din Outlook sau Gmail-ul firmei** (office@…): 1000 de destinatari dintr-o căsuță obișnuită înseamnă limite de trimitere, spam și risc de blocare a domeniului.

### Setări în Brevo
1. **Autentifică domeniul** din care trimiți (Senders, Domains & IPs → Domains): adaugi în DNS înregistrările SPF, DKIM și DMARC pe care ți le dă Brevo. Fără ele, e-mailul ajunge în Spam la Gmail și Yahoo.
2. Importă lista din CSV cu coloanele `EMAIL, PRENUME, NUME, DATA_ULTIMEI_COMENZI`. Scoate duplicatele și adresele invalide.
3. Campaign → Create → „Paste your code” → lipește `newsletter-brevo.html`; la „Plain text” lipește `newsletter.txt`.
4. Activează **click tracking** și **Google Analytics tracking**. Linkurile au deja UTM-uri (`utm_source=newsletter`, `utm_campaign=decoflair-2027`, câte un `utm_content` pentru fiecare bloc).

## 2b. Dacă trimiți din theMarketer

theMarketer e o platformă românească, făcută pentru magazine online. **Planul Basic e gratuit până la 1000 de contacte**; Standard costă ~20 €/lună, iar Ecommerce ~25 €/lună (cu integrare cu magazinul și tracking de vânzări). Prețurile sunt fără TVA; verifică-le pe themarketer.com/pricing.

1. **Validează domeniul:** Settings → Email settings → „Domain validation”. Copiezi înregistrările DNS la furnizorul de domeniu decoflair.ro, apoi apeși „Validate”.
2. **Importă contactele** din CSV (email, prenume, nume).
3. **Creează campania** și caută în editor opțiunea de cod HTML (bloc „HTML” / „Custom code” / import HTML). Lipește tot conținutul din `out/newsletter-themarketer.html`.
   - Documentația publică descrie doar editorul drag-and-drop, deci nu am putut confirma unde e opțiunea de HTML. Dacă n-o găsești, cere-o la suport: iam@themarketer.com („vreau să import un newsletter HTML propriu”).
4. **Dezabonarea:** linkul folosește `{{unsubscribe_link}}`, tag-ul din documentația theMarketer. theMarketer adaugă oricum un subsol cu dezabonare. Dacă îl vezi de două ori la test, poți șterge rândul nostru de dezabonare.
5. **Personalizare (opțional):** `{{client_first_name}}`, de exemplu în subiect: „{{client_first_name}}, casa ta la nivelul următor”. Setează și o valoare implicită pentru cei fără prenume.
6. **Imaginile** se încarcă tot de pe decoflair.ro (pasul cu Image Manager de mai sus), deci în theMarketer nu urci nimic.
7. **Trimite-ți întâi un test** și verifică trei lucruri: imaginile apar, linkul de dezabonare merge, prenumele se completează.

## 3. Expeditor și partea legală

- Expeditor: `Deco&Flair`, adresă de pe domeniul decoflair.ro (ex. `noutati@decoflair.ro`), reply-to `office@decoflair.ro`.
- Textul e-mailului nu spune de unde vine adresa destinatarului. NMC apare doar ca „Deco&Flair, dealer autorizat NMC®”.
- Obligatoriu și deja în subsol: identitatea firmei (Deco & Flair Hub SRL, CUI) și linkul de dezabonare. Cererile de dezabonare se respectă imediat.
- Trimite doar adreselor pe care aveți dreptul să le folosiți pentru marketing. Dacă un destinatar întreabă de unde aveți adresa, GDPR (art. 14–15) vă obligă să-i spuneți sursa.

## 4. Subiect și preheader

Preheader (deja în cod): *Kit complet de cameră cu 15% inclus, −10% la profile LED și plinte, tendințele 2027 și sfatul expertului.*

Fă test A/B pe primele 2 tranșe:
- **A:** `Casa ta, la nivelul următor: idei 2027 + −10%`
- **B:** `Sfatul expertului: 3 detalii care schimbă o cameră (+ −10%)`
- Rezervă: `Lux real, la prețul corect: noutățile 2027 pentru casa ta`

Expeditor: `Deco&Flair`.

## 5. Planul de trimitere pentru ~1000 de adrese

| Pas | Cine | Când |
|---|---|---|
| 0. Test | 3–5 adrese proprii (Gmail, Yahoo, Outlook, telefon) | cu o zi înainte |
| 1. Tranșa 1: 300 | clienții cu comenzi în ultimele 12 luni (cei mai „calzi”) | marți sau miercuri, 10:00 |
| 2. Tranșa 2: 300 | comenzi de acum 1–2 ani, cu subiectul câștigător | a doua zi, 10:00 |
| 3. Tranșa 3: rest | restul listei | joi, 19:30 (seara se citește din pat, de pe telefon) |
| 4. Retrimitere | celor care NU au deschis, cu subiect nou | după 4–5 zile |

Trimiterea în tranșe protejează reputația domeniului și se potrivește cu limita de 300 pe zi a planului gratuit Brevo.

## 6. Ce faci cu click-urile: blocul „Ce cameră transformi în 2027?”

Fiecare cameră (Living, Dormitor, Hol, Fațadă) are un link diferit (`utm_content=camera-…`). În Brevo, segmentează după linkul apăsat și trimite după 7–10 zile un **e-mail scurt, doar pentru camera aleasă**: 3 produse, un sfat și „Sună-ne pentru o randare 3D”. Asta e partea care vinde cel mai bine.

## 7. Cum poziționăm Deco&Flair

Mesajul central: **„Casa ta, la nivelul următor. Expert premium, la prețul corect.”**
- **Garanția de calitate:** „Dealer autorizat NMC®”. Profilele ARSTYL®, WALLSTYL® și NOMASTYL®, fabricate în Belgia, plus tapet italian de designer, panouri 3D și riflaje.
- **Expertul are un chip:** fotografia expertei și sfatul personal transformă magazinul într-un consultant.
- **Lux accesibil:** „Luxul nu e un preț. E o alegere bine făcută.” Prețuri reale, reduceri reale.
- **Seria de 3 e-mailuri:** (1) acesta, statement + oferte; (2) după 10 zile, e-mailul pe camera aleasă; (3) în ianuarie, „Planul casei tale pentru 2027” cu Trend 2027 · Tokyo × Singapore și o ofertă de început de an.
- **Pe rețele, în aceeași săptămână:** reel-urile Trend 2027, Idei 2027 și Blog (deja în repo) cresc recunoașterea, așa că e-mailul nu vine „din senin”.

KPI-uri realiste pentru o listă de clienți: deschideri 30–45%, click 3–6%, dezabonări sub 0,5%. Urmărește în GA4 traficul cu `utm_source=newsletter`, `utm_campaign=decoflair-2027`.

## 8. Checklist înainte de „Trimite”

- [ ] Imaginile urcate și verificate (hero.jpg se deschide).
- [ ] Prețurile încă valabile pe decoflair.ro/oferte-speciale (au fost citite la **18.11.2026**: −10% la L5, L2, WO2, FD3, FO1, FL13; Kit LINEA 2.838,30 lei). Dacă se schimbă, modifică `PRODUCTS` în `build.py` și rulează `python3 build.py`.
- [ ] Domeniul autentificat (SPF, DKIM, DMARC).
- [ ] Testul arată bine în Gmail (telefon + desktop) și în Outlook.
- [ ] Lista curățată (fără duplicate, adrese invalide sau dezabonați).
- [ ] Opțional: numele expertei (`EXPERT_NAME`) și un cod de bun venit (`COUPON`; creează întâi codul în OpenCart!) în `build.py`.

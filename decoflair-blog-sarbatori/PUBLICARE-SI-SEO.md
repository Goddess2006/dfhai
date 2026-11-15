# Articol blog Deco&Flair — „Casa de sărbători”: publicare și SEO

## Câmpurile articolului (Journal › Blog › Posts › Add)

| Câmp | Valoare |
|---|---|
| **Titlu (Name)** | Casa de sărbători: ghidul de design pentru o renovare elegantă înainte de Crăciun |
| **Slug / SEO URL** | `casa-de-sarbatori-ghid-design-renovare-inainte-de-craciun` |
| **Meta Title** (≤ 60 caractere) | Ghid de design: renovare elegantă înainte de Crăciun |
| **Meta Description** (≤ 155) | Cum transformi peretele din spatele mesei de Crăciun cu profile decorative, lumină caldă și paleta 2027. Plan în 4 săptămâni, pentru orice buget. |
| **Meta Keywords** | renovare inainte de craciun, design masa de craciun, perete cu chenare, profile decorative, cornisa led, panouri 3d, culori 2027, decor sarbatori |
| **Imagine principală (Image)** | `catalog/blog/casa-de-sarbatori/01-coperta-masa-sub-rozeta.jpg` |
| **Categorie** | Amenajări interioare / Idei (categoria existentă de pe blog) |
| **Tag-uri** | sărbători, Crăciun, renovare, ghid de design, culori 2027, profile decorative |
| **Descriere scurtă (excerpt)** | Peretele din spatele mesei este scena sărbătorilor. Paleta 2027, șase rețete de perete, planul în patru săptămâni și produsele potrivite, pentru orice buget. |
| **Autor** | Echipa Deco&Flair |

Cuvântul-cheie principal este „renovare înainte de Crăciun”; cele secundare sunt „perete masă de Crăciun”, „culori 2027” și „profile decorative”.

## Pași de publicare

1. **Imaginile:** urcă cele 26 de fișiere din `img/` în `image/catalog/blog/casa-de-sarbatori/`. Poți folosi Image Manager (folder nou `blog` › `casa-de-sarbatori`) sau FTP.
2. **Articolul nou:** deschide Journal › Blog › Posts › Add și completează câmpurile din tabelul de mai sus.
3. **Conținutul:** la **Description**, apasă butonul **Cod sursă `</>`**, lipește TOT conținutul din `articol.html`, apasă din nou `</>`, apoi salvează. Nu edita textul în modul vizual.
4. **Cache:** golește cache-ul Journal 3 (Dashboard › rotița albastră) și pe cel al CDN-ului, dacă există.
5. **Verificarea:** deschide articolul pe desktop și pe mobil, apoi verifică linkurile spre produse.

**Dacă editorul elimină `<style>` sau `<link>`** (unele configurații Summernote fac asta):
- **Varianta 1:** pune conținutul blocului `<style>…</style>` din `articol.html` în Journal › Skins › Custom Code › Custom CSS, iar linia `<link …fonts.googleapis…>` în Custom Code › Header. Toate stilurile sunt izolate sub clasa `.dfb`, deci nu afectează restul site-ului.
- **Varianta 2:** introduci conținutul direct în baza de date, în tabela cu descrierile articolelor Journal 3 (de regulă `oc_journal3_blog_post_description`, câmpul `description`; verifică numele în baza ta).

## Ce conține articolul

- **Lungime:** aproximativ 2.400 de cuvinte, cu timp de citire de circa 14 minute.
- **Structură:** 9 capitole, cu cuprins ancorat.
- **Paleta:** 6 culori cu coduri hex, plus 3 combinații de culori.
- **Plan:** un calendar de lucru pe 4 săptămâni.
- **6 rețete de perete:** fiecare are imagine, stil, nivel de buget, 4 pași și produsele recomandate cu link.
- **Bugete:** 3 niveluri (Esențial · Rafinat · Signature).
- **Restul:** styling pentru masa de Crăciun, greșeli de evitat, un checklist, o selecție completă de 17 produse, întrebări frecvente și un îndemn spre consultanță, randare 3D și telefon.

**Fără prețuri și fără date:** articolul nu are prețuri și nu are date calendaristice, deci rămâne valabil și în anii următori. Paleta este prezentată explicit ca recomandare editorială Deco&Flair, nu ca „culoarea oficială a anului”.

Toate produsele au fost verificate în stoc pe decoflair.ro la 15.11.2026, iar toate linkurile răspund HTTP 200.

## Imaginile

Imaginile ambientale sunt din biblioteca de inspirație Deco&Flair (`decoflair-inspiratie-50`). Sunt imagini AI de stil, nu proiecte executate. Ilustrează dining-uri și pereți cu chenare, cornișe, rozete, relief 3D și riflaj, dar **nu au decor de Crăciun**.

Pentru a pune fotografii cu mese de Crăciun, generează imaginile din `PROMPTURI-IMAGINI.md` și înlocuiește fișierele cu **aceleași nume**. Articolul nu trebuie modificat.

# Ghid de listare și optimizare — Kituri Deco&Flair pe Trendyol

## Cum se folosește
Fiecare kit are un fișier `content/<cod>.md` cu: denumire, titlu Trendyol, descriere (text + HTML), puncte-cheie, atribute,
SEO (cuvinte cheie cu volume Semrush RO, title, meta, slug), GEO (rezumat factual), AEO (FAQ), alt-text imagini și JSON-LD.
`content/trendyol-upload.csv` are toate câmpurile pe un rând per kit (Excel, separator `;`).

## Strategia de titlu (Trendyol + Google)
Formula: **Set [cantitate] [termenul cel mai căutat] [model] [termen secundar] [dimensiune] [+ accesoriu] [total ml]**.
Termenul cu cel mai mare volum stă la începutul titlului (Trendyol taie titlul în listă după ~60 caractere).
Volume lunare Google România (Semrush, noiembrie 2026) folosite la alegere:

| Kit | Termen principal în titlu | Volum/lună |
|---|---|---:|
| Cornișă Z11 | cornisa tavan / baghete tavan | 1.300 / 720 |
| Plintă FD3 | plinta parchet / plinta alba / plinta polimer | 5.400 / 1.300 / 1.000 |
| Baghete WL1 | baghete decorative perete / bagheta decorativa / chenare decorative | 480 / 590 / 210 |
| Cornișă LED IL13 | banda led tavan / profil led tavan / cornisa led | 590 / 480 / 210 |
| Colțar NCL107 | coltare polistiren / profile decorative exterior | 590 / 1.300 |
| Ancadrament NA105 | ancadramente ferestre / ancadrament fereastra | 1.300 / 390 |
| Cornișă NC104 | cornise exterior / profile decorative exterior | 110 / 1.300 |
| Brâu REMA1 | profile decorative exterior / brau decorativ | 1.300 / 210 |

„adeziv polistiren exterior” (880/lună) apare în descrierile kiturilor cu ADRO-FIX. „chenare perete”, „caroiaje perete”,
„brau fatada”, „cornisa fatada” au volum zero în Google RO — folosește-le doar în text, nu în titlu.

## GEO (Generative Engine Optimization) — să fii citat de AI
- Folosește aceeași denumire peste tot (Trendyol, decoflair.ro, social): „Kit Chenare & Tablouri WL1 — 8 baghete, 16 ml”.
- Paragraful GEO din fiecare fișier este autonom: are produsul, cantitatea, dimensiunile, materialul, acoperirea, prețul și data. Pune-l primul pe pagina kitului de pe decoflair.ro.
- Lista „Fapte cheie” e făcută pentru extragere automată (atribut: valoare). Păstrează cifrele exacte.
- Publică pe decoflair.ro câte o pagină per kit (slug-urile sunt propuse) cu JSON-LD Product + FAQPage, apoi leagă din articolele de blog relevante (chenare decorative, cornișă LED, fațade).

## AEO (Answer Engine Optimization) — răspunsuri directe
- Întrebările din FAQ sunt formulate cum caută oamenii („Câte cornișe îmi trebuie pentru o cameră?”); răspunsul începe direct cu informația, în 1–3 propoziții.
- Pe Trendyol, FAQ-ul intră la finalul descrierii; pe decoflair.ro, marchează-l cu JSON-LD FAQPage (inclus).
- Răspunde la întrebările clienților din Trendyol (secțiunea Întrebări) folosind aceleași formulări.

## Reguli Trendyol de reținut
- Imagini: 1200×1800, fără preț, fără date de contact sau link-uri; prima imagine = coperta kitului. Max. 8 imagini.
- Barcode: kitul are nevoie de un cod de bare propriu (nu folosi EAN-ul unui singur profil). Codul kitului (`P01-Z11x5` etc.) poate fi folosit ca cod vânzător.
- Marca: listează sub marca pentru care contul are aprobare (de ex. Deco&Flair). Mărcile producătorilor (NMC, WALLSTYL®, ARSTYL®, ADRo®) apar doar în descriere, ca informație.
- Categoria: alege în panou categoria de profile/decorațiuni pentru perete și tavan (interior) sau materiale de fațadă (exterior); atributele din fișiere se potrivesc cu câmpurile cerute.
- Garanție: 24 de luni, garanția legală de conformitate.
- Prețul final nu include comisionul Trendyol.

## De verificat înainte de publicare
- Codul „WL12” cerut nu există pe decoflair.ro; s-a folosit WL1.
- Z11: textul de pe site spune „poliuretan ARSTYL®”, iar tabelul de atribute de pe aceeași pagină spune „polimer dur”. S-a folosit poliuretan (gama ARSTYL®).
- Țara de origine nu e menționată pe site; completeaz-o din documentele de la furnizor.

# Pachete Deco&Flair pentru Trendyol

8 pachete, fiecare listat ca **un singur produs**. Preț = preț de listă NEREDUS de pe decoflair.ro (TVA inclus; dacă produsul e azi la ofertă se ia prețul vechi, cel tăiat) × cantitate + **200 lei transport**.

| Cod | Pachet | Produse | Transport | **Preț final** |
|---|---|---:|---:|---:|
| P01-Z11x5 | 5 × cornișă tavan Z11 (10 ml) | 1.462,35 | 200 | **1.662,35** |
| P02-FD3x5 | 5 × plintă FD3 (10 ml) | 605,65 | 200 | **805,65** |
| P03-WL1x8 | 8 × brâu WL1 pentru chenare/caroiaje (16 ml) | 490,96 | 200 | **690,96** |
| P04-IL13x5 | 5 × cornișă LED IL13 (10 ml) | 982,40 | 200 | **1.182,40** |
| P05-NCL107x5-QUARTZ | 5 × colțar NCL107 + 1 rășină ADRO-QUARTZ 1,5 kg | 1.313,29 | 200 | **1.513,29** |
| P06-NA105x5-FIX | 5 × ancadrament NA105 + 1 adeziv ADRO-FIX 4 kg | 924,21 | 200 | **1.124,21** |
| P07-NC104x5-FIX | 5 × cornișă exterior NC104 + 1 adeziv ADRO-FIX 4 kg | 1.079,41 | 200 | **1.279,41** |
| P08-REMA1x5-QUARTZ | 5 × brâu fațadă REMA1 + 1 rășină ADRO-QUARTZ 1,5 kg | 659,29 | 200 | **859,29** |

Prețuri citite live la 24.11.2026 (`data/produse.json`). FD3 e azi la ofertă (109,02), în pachet s-a folosit prețul neredus 121,13.
Prețurile finale NU includ comisionul Trendyol.

## Fișiere
- `out/trendyol-pachete.csv` — fișa de listare (titlu, SKU, preț final, conținut, descriere, ordinea imaginilor); se deschide în Excel (separator `;`).
- `out/<cod>/01…05-*.jpg` — imaginile pachetului, 1200×1800 (2:3, cât cere Trendyol): copertă, ambient, idee/montaj, detalii tehnice, conținut.
- `out/<cod>/produs-*.jpg` — fotografiile produselor de pe decoflair.ro pe fundal alb 1200×1800.
- `out/index.html` — galerie + calcul.
- La P03 (WL1): imaginea `03-caroiaje-tablouri.jpg` arată caroiajele ca rame pentru tablouri, plus două ambienturi cu chenare.

## Reguli respectate pe imagini
Fără preț, fără site, fără telefon (reguli Trendyol). Ambienturile din `catalog-fatade/` și `decoflair-inspiratie-50/` sunt imagini de prezentare (marcate discret „Imagine de prezentare”), nu fotografii ale SKU-ului exact.

## Reproducere
```
python3 tools/fetch_prices.py && python3 tools/fetch_images.py && python3 build.py && node render.cjs
```
Pachetele se editează în `data/pachete.json`; transportul în `TRANSPORT` din `build.py`.

## Conținut (SEO / GEO / AEO) — `content/`
- `content/<cod>.md` — per kit: nume kit, titlu Trendyol, descriere (text + HTML), puncte-cheie, atribute, cuvinte cheie cu volume Google RO (Semrush, nov. 2026), SEO title/meta/slug/H1, rezumat GEO + fapte cheie, FAQ (AEO), alt-text imagini, JSON-LD Product + FAQPage.
- `content/TOATE-KITURILE.md` — toate într-un fișier; `content/trendyol-upload.csv` — toate câmpurile, un rând per kit.
- `content/GHID-LISTARE-SEO-GEO-AEO.md` — strategia de titlu, reguli Trendyol, ce e de verificat.
- Surse: `data/keywords-semrush-ro.csv`, fișele oficiale `src/<cod>/descriere.txt`, `data/meta-site.json` (EAN, producător).
- Reproducere: `python3 tools/fetch_desc.py && python3 build.py && node render.cjs && python3 content.py`.

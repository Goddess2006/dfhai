---
name: decoflair-catalog
description: Citește catalogul public decoflair.ro (≈1.000 de produse din sitemap) — nume, cod model, categorie, preț, disponibilitate, descriere și pozele de produs la 1500 px — și descarcă pozele ca referință pentru generare de imagini/video. Folosește-l înainte de orice postare, reclamă, newsletter sau imagine AI despre un produs Deco&Flair, ca să nu inventezi produse, prețuri sau forme; și pentru alegerea produselor săptămânii.
---

# Catalog Deco&Flair

Script: `scripts/catalog.py` (doar biblioteca standard Python, fără login).

```bash
python3 .claude/skills/decoflair-catalog/scripts/catalog.py list --grep cornisa --limit 30
python3 .claude/skills/decoflair-catalog/scripts/catalog.py product <url-produs>
python3 .claude/skills/decoflair-catalog/scripts/catalog.py images <url-produs> --dest <proiect>/refs/<cod>
python3 .claude/skills/decoflair-catalog/scripts/catalog.py pick --n 7 --seed 2026-W48
```

- `list` → url, titlu, toate pozele din sitemap. `product` → JSON-LD (name, model, category, price RON cu TVA, availability, brand) + galeria deduplicată la cea mai mare rezoluție.
- `pick` alege reproductibil (aceeași sămânță = aceeași listă) produse cu poze, pentru calendarul săptămânii.
- Prețul și stocul se citesc **în ziua publicării**; nu le copia din materiale vechi.
- Date interne (liste de parteneri, clienți, DistribNet) NU sunt aici: sunt în `BAZE/` local și nu se publică.
- Pozele descărcate sunt referințe de lucru; pune-le în folderul proiectului, nu le comite dacă nu e nevoie.

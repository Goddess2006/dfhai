# Catalog imagini de referință — fațade și interioare (NMC / Deco&Flair)

Bibliotecă permanentă de imagini de fațade, pentru creative, landing-uri, bannere și reel-uri.
Imaginile au fost furnizate de client pe 17–18.11.2026: 15 imagini, 01–10 fațade și 11–15 interioare.

- `imagini/`: originalele (WebP, 1536 × 1024). **Nu se modifică.**
- `jpg/`: aceleași imagini în JPG (calitate 93), pentru unelte care nu citesc WebP.
- `manifest.json`: pentru fiecare imagine: titlu, culori, elemente decorative vizibile, stil, unghi, idei de folosire, zona liberă pentru text și SHA-256.
- `index.html`: galeria de vizualizare.
- `planse-contact.jpg`: toate imaginile pe o singură planșă.

| ID | Imagine | Elemente vizibile |
|---|---|---|
| 01 | Casă terracota pe două niveluri | ancadramente crem, brâu între etaje, solbancuri |
| 02 | Casă crem cu portic | ancadramente gri, cornișă portic, pilaștri |
| 03 | Casă bej cu mansardă | **colțare albe tip bosaje**, ancadramente |
| 04 | Casă galbenă pe parter | ancadramente cu cheie de boltă, cornișă |
| 05 | Casă albastru-gri pe parter | ancadramente albe cu pilaștri, cornișă |
| 06 | Casă taupe pe parter | **colțare tip bosaje**, ancadramente, cornișă, gard cu capace |
| 07 | Casă albă cu portic | ancadramente cu cornișă, portic |
| 08 | Casă gri deschis | ancadramente, cornișă profilată |
| 09 | Casă verde salvie, două niveluri | ancadramente, brâu între etaje |
| 10 | Casă piersică pe parter | ancadramente, cornișă de fronton, pilaștri |
| 11 | Living salvie — **ÎNAINTE** (pereche cu 13) | cornișă LED, perete simplu |
| 12 | Hol albastru-petrol | chenare pe pereți, cornișă, plinte |
| 13 | Living salvie — **DUPĂ** (pereche cu 11) | chenare din brâu + cornișă LED |
| 14 | Dormitor mov-prună | chenare în spatele patului |
| 15 | Bucătărie terracota | chenare + brâu la jumătatea peretelui |

**Perechea 11 / 13** este aceeași cameră, fără și cu chenare. E ideală pentru postări de tip ÎNAINTE/DUPĂ cu brâuri decorative.

## Reguli de folosire (Claude Code și Codex)

1. Alege imaginea după elementele din `manifest.json`. De exemplu, pentru colțare (NCL107, NCL113) folosește 03; pentru chei de boltă, 04.
2. Nu afirma că în imagine apare un anumit cod de produs fără verificare cu fișa de pe site. Dacă nu e sigur, prezintă imaginea ca „exemplu de fațadă” sau „inspirație”.
3. Proveniența exactă (fotografie proprie, randare sau AI) nu a fost declarată. Confirmă drepturile de folosire înainte de reclame plătite.
4. Adaptările (decupaje, tentă de culoare) se salvează în folderul proiectului care le folosește, nu aici.

## Adăugare imagini noi

Pune fișierul în `imagini/` (nume: `NN-descriere-scurta.webp`), adaugă descrierea în `meta.json`, apoi rulează:

```bash
python3 catalog-fatade/build_catalog.py
```

Scriptul regenerează manifestul, galeria și planșa de contact, plus JPG-urile pentru imaginile noi.

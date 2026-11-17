# Catalog fațade — imagini de referință (NMC / Deco&Flair)

Bibliotecă permanentă de imagini de fațade, pentru creative, landing-uri, bannere și reel-uri.
Imaginile au fost furnizate de client pe 17.11.2026.

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

## Reguli de folosire (Claude Code și Codex)

1. Alege imaginea după elementele din `manifest.json`. De exemplu, pentru colțare (NCL107, NCL113) folosește 03; pentru chei de boltă, 04.
2. Nu afirma că în imagine apare un anumit cod de produs fără verificare cu fișa de pe site. Dacă nu e sigur, prezintă imaginea ca „exemplu de fațadă” sau „inspirație”.
3. Proveniența exactă (fotografie proprie, randare sau AI) nu a fost declarată. Confirmă drepturile de folosire înainte de reclame plătite.
4. Adaptările (decupaje, tentă de culoare) se salvează în folderul proiectului care le folosește, nu aici.

## Adăugare imagini noi

Pune fișierul în `imagini/` (nume: `NN-descriere-scurta.webp`), adaugă descrierea în `META` din `build_catalog.py`, apoi rulează:

```bash
python3 catalog-fatade/build_catalog.py
```

Scriptul regenerează manifestul, galeria și planșa de contact, plus JPG-urile pentru imaginile noi.

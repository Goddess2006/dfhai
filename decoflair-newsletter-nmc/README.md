# Newsletter Deco&Flair „Ediția 2027”

E-mail HTML compatibil cu clienții de e-mail: tabele, stiluri inline, 600 px, se stivuiește pe mobil, ~62 KB (sub limita Gmail de 102 KB).
Secțiuni: bara „dealer autorizat NMC®”, hero „statement”, manifest, sfatul expertului (cu fotografie), reduceri −10% (6 produse în stoc), LINEA Room Kit, 3 kituri recomandate, sondaj interactiv „Ce cameră transformi?” (click = segmentare), Trend 2027 · Tokyo × Singapore, Întrebări & răspunsuri, blog, avantaje, CTA final, subsol cu dezabonare.

- Generare: `python3 build.py` → `img/` + `out/`
- Paletă: `python3 tools/palette_check.py` → `PALETA.md`
- Fotografia expertei HQ: `python3 tools/upscale.py MODEL.onnx expert/expert-original.jpg expert/expert` (model realesr-general-x4v3, ONNX, de pe Hugging Face; nu e în repo)
- Sursele mari (`src/`) nu sunt în git: ele vin de pe decoflair.ro (bannere, poze de produs, imagini de blog) și din `decoflair-idei-2027/assets`, `decoflair-trend-2027/assets`.
- Trimitere, GDPR, platformă, plan: **GHID-TRIMITERE.md**

"""Arhiva completă pentru developer: black-november/release/nmc-black-november.zip

Conținut:
  black-november/            -> se urcă în rădăcina magazinului (landing + script homepage + imagini)
  CITESTE-MA.md              -> instrucțiunile de instalare
  cod-homepage.html          -> linia de pus pe homepage (varianta HTML)
  cod-homepage.js            -> aceeași, varianta doar JavaScript
  sursa/                     -> generatorul paginii (pentru modificări ulterioare)
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
out = root / "release/nmc-black-november.zip"; out.parent.mkdir(exist_ok=True)
site = [root / n for n in ("index.html", "bn.css", "bn.js", "homepage-overlay.js")] + sorted((root / "assets").glob("*.*"))
html = '<script defer src="/black-november/homepage-overlay.js"></script>\n'
js = "(function(){var s=document.createElement('script');s.src='/black-november/homepage-overlay.js';s.defer=true;document.body.appendChild(s);})();\n"
with ZipFile(out, "w", ZIP_DEFLATED) as z:
    for f in site:
        z.write(f, "black-november/" + str(f.relative_to(root)))
    z.write(root / "INSTALARE.md", "CITESTE-MA.md")
    z.writestr("cod-homepage.html", "<!-- Se pune O SINGURĂ DATĂ pe homepage, înainte de </body> -->\n" + html)
    z.writestr("cod-homepage.js", "// Varianta pentru câmpurile care acceptă doar JavaScript (ex. Journal 3 › Custom JS)\n" + js)
    for f in ("tools/build.py", "tools/package.py"):
        z.write(root / f, "sursa/" + f)
print(out)

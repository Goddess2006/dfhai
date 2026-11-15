"""Arhiva completă pentru developer: decoflair-landing/release/decoflair-selectia-premium.zip"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
out = root / "release/decoflair-selectia-premium.zip"; out.parent.mkdir(exist_ok=True)
site = [root / n for n in ("index.html", "df.css", "df.js", "homepage-overlay.js")] + sorted((root / "assets").glob("*.*"))
html = '<script defer src="/selectia-premium/homepage-overlay.js"></script>\n'
js = "(function(){var s=document.createElement('script');s.src='/selectia-premium/homepage-overlay.js';s.defer=true;document.body.appendChild(s);})();\n"
with ZipFile(out, "w", ZIP_DEFLATED) as z:
    for f in site:
        z.write(f, "selectia-premium/" + str(f.relative_to(root)))
    z.write(root / "DOCUMENTATIE-DEVELOPER.md", "DOCUMENTATIE-DEVELOPER.md")
    z.writestr("cod-homepage.html", "<!-- Se pune O SINGURĂ DATĂ pe homepage, înainte de </body> -->\n" + html)
    z.writestr("cod-homepage.js", "// Varianta pentru câmpurile care acceptă doar JavaScript (ex. Journal 3 › Custom JS)\n" + js)
    for f in ("tools/build.py", "tools/package.py", "surse-imagini.json"):
        z.write(root / f, "sursa/" + f)
print(out)

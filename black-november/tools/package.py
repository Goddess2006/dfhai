"""Arhiva de urcat pe server: black-november/release/nmc-black-november.zip"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parents[1]
out = root / "release/nmc-black-november.zip"; out.parent.mkdir(exist_ok=True)
files = [root / n for n in ("index.html", "bn.css", "bn.js", "INSTALARE.md")] + sorted((root / "assets").glob("*.*"))
with ZipFile(out, "w", ZIP_DEFLATED) as z:
    for f in files:
        z.write(f, "black-november/" + str(f.relative_to(root)))
print(out, len(files), "fișiere")

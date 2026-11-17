"""Catalog de imagini de fațade (furnizate de client) — regenerează manifest.json + index.html + planșa de contact.
Adaugă imagini noi în `imagini/` (webp/jpg/png), completează descrierea în META, apoi rulează:
  python3 catalog-fatade/build_catalog.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib, json, html

ROOT = Path(__file__).resolve().parent

META = {
    "01-casa-terracota-ancadramente-brau": dict(
        titlu="Casă pe două niveluri, terracota, cu ancadramente crem și brâu",
        culori=["terracota", "crem", "maro ciocolatiu (tâmplărie)"],
        elemente=["ancadramente ferestre", "ancadrament ușă", "brâu decorativ între etaje", "solbancuri", "soclu placat"],
        stil="clasic-modern, casă familială", unghi="frontal-ușor oblic", sezon="vară",
        potrivit=["campanii ancadramente", "brâuri exterior", "Înainte/După (după)", "landing fațade"],
        cadru_util="tot cadrul; spațiu liber minim pentru text (cer în dreapta-sus)"),
    "02-casa-crem-ancadramente-gri-portic": dict(
        titlu="Casă crem cu ancadramente gri și portic cu pilaștri",
        culori=["crem / alb cald", "gri cald", "negru (acoperiș, tâmplărie)"],
        elemente=["ancadramente ferestre gri", "cornișă portic", "pilaștri / coloane pătrate", "solbancuri", "soclu gri"],
        stil="modern-clasic, minimalist premium", unghi="frontal-oblic", sezon="vară, cer înnorat",
        potrivit=["creative premium (paletă 2027 crem/negru)", "pilaștri și cornișe", "landing hero"],
        cadru_util="cerul din stânga-sus permite text; casa ocupă dreapta"),
    "03-casa-bej-coltare-bosaje-ancadramente": dict(
        titlu="Casă bej cu colțare albe tip bosaje și ancadramente",
        culori=["bej / nisip", "alb", "maro (acoperiș, tâmplărie)"],
        elemente=["colțare decorative (bosaje) la colțuri", "ancadramente ferestre", "solbancuri", "soclu maro"],
        stil="clasic, casă cu mansardă", unghi="oblic, pe colț", sezon="vară",
        potrivit=["colțare NCL (ex. NCL107, NCL113)", "ancadramente", "Problema/Soluția colțuri plate"],
        cadru_util="colțarele sunt clar vizibile la stânga și la dreapta; cer liber sus-dreapta"),
    "04-casa-galbena-ancadramente-cheie-bolta-cornisa": dict(
        titlu="Casă galbenă pe parter cu ancadramente cu cheie de boltă și cornișă",
        culori=["galben pastel", "alb", "maro (acoperiș, poartă, gard)"],
        elemente=["ancadramente cu cheie de boltă", "cornișă sub streașină", "solbancuri", "soclu maro"],
        stil="tradițional românesc renovat", unghi="frontal-oblic", sezon="vară",
        potrivit=["chei de boltă", "ancadramente clasice", "renovare casă bătrânească", "cornișe exterior"],
        cadru_util="tot cadrul; poarta din stânga poate fi decupată"),
    "05-casa-albastra-ancadramente-cornisa": dict(
        titlu="Casă albastru-gri pe parter cu ancadramente albe și cornișă",
        culori=["albastru-gri", "alb", "teracotă (acoperiș)", "maro (tâmplărie)"],
        elemente=["ancadramente cu pilaștri decorativi", "cornișă sub streașină", "solbancuri", "soclu gri"],
        stil="tradițional românesc renovat, rural", unghi="frontal", sezon="vară",
        potrivit=["renovare casă la țară", "ancadramente decorative", "campanii cu prețuri accesibile"],
        cadru_util="frontal simetric; bun pentru format pătrat/4:5 cu decupaj central"),
}

(ROOT / "jpg").mkdir(exist_ok=True)
items = []
for f in sorted((ROOT / "imagini").iterdir()):
    if f.suffix.lower() not in (".webp", ".jpg", ".jpeg", ".png"):
        continue
    im = Image.open(f)
    jp = ROOT / "jpg" / f"{f.stem}.jpg"
    if not jp.exists():
        im.convert("RGB").save(jp, quality=93)
    m = META.get(f.stem, {})
    items.append(dict(id=f.stem[:2], fisier=f"imagini/{f.name}", jpg=f"jpg/{f.stem}.jpg", latime=im.width, inaltime=im.height,
                      sha256=hashlib.sha256(f.read_bytes()).hexdigest(), **m))

manifest = dict(
    nume="Catalog fațade — imagini de referință",
    sursa="Imagini furnizate de client (proprietarul NMC / Deco&Flair) în conversație, 17.11.2026. Proveniența exactă (fotografii proprii, randări, AI sau stoc) nu a fost declarată — confirmați drepturile înainte de folosire în reclame plătite.",
    branduri=["nmcromania.ro", "decoflair.ro"],
    reguli=[
        "Folosește imaginile ca ambient de fațadă pentru creative, landing-uri, bannere, reel-uri.",
        "Nu afirma că un anumit SKU (cod de produs) apare în imagine fără verificare cu fișa produsului; descrie ca „inspirație”/„exemplu de fațadă” dacă nu e sigur.",
        "Nu modifica originalele din `imagini/`; salvează adaptările în folderul proiectului care le folosește.",
        "Pentru 4:5 / 9:16 decupează din centru; cerul liber e indicat în câmpul `cadru_util`.",
    ],
    imagini=items,
)
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))

# galerie HTML
cards = ""
for it in items:
    tags = "".join(f"<span>{html.escape(t)}</span>" for t in it.get("elemente", []))
    cards += (f'<figure><img src="{it["jpg"]}" alt="{html.escape(it.get("titlu", ""))}" loading="lazy">'
              f'<figcaption><b>{it["id"]} · {html.escape(it.get("titlu", ""))}</b>'
              f'<small>{html.escape(it.get("stil", ""))} · {it["latime"]}×{it["inaltime"]}</small><div class="t">{tags}</div>'
              f'<small>Potrivit pentru: {html.escape(", ".join(it.get("potrivit", [])))}</small></figcaption></figure>')
(ROOT / "index.html").write_text(f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Catalog fațade</title><style>
body{{margin:0;font-family:system-ui,sans-serif;background:#F3ECDF;color:#1d1f1c;padding:24px}}
h1{{font-weight:600;margin:0 0 6px}}p{{margin:0 0 20px;color:#555}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px}}
figure{{margin:0;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,.08)}}
img{{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}}
figcaption{{padding:12px 14px;display:flex;flex-direction:column;gap:6px}}small{{color:#666}}
.t{{display:flex;flex-wrap:wrap;gap:6px}}.t span{{font-size:12px;background:#1E3A2E;color:#F3ECDF;border-radius:20px;padding:3px 9px}}
</style></head><body><h1>Catalog fațade</h1><p>{len(items)} imagini de referință · sursa: furnizate de client · vezi manifest.json</p>
<div class="g">{cards}</div></body></html>""")

# planșă de contact
W, H = 480, 320
sheet = Image.new("RGB", (W * 3, (H + 40) * ((len(items) + 2) // 3)), "#F3ECDF")
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except OSError:
    font = ImageFont.load_default()
for i, it in enumerate(items):
    x, y = (i % 3) * W, (i // 3) * (H + 40)
    sheet.paste(Image.open(ROOT / it["jpg"]).resize((W - 8, H - 8)), (x + 4, y + 4))
    d.text((x + 8, y + H + 8), f'{it["id"]} · {it.get("titlu", "")[:44] + ("…" if len(it.get("titlu", "")) > 44 else "")}', fill="#1d1f1c", font=font)
sheet.save(ROOT / "planse-contact.jpg", quality=88)
print("catalog:", len(items), "imagini")

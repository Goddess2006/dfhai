"""Generează 5 creative Facebook (1080x1350) Black Friday NMC: ambient + produs + preț redus.
Prețuri preluate de pe nmcromania.ro la 12.11.2026 (cu TVA). Rulare: python3 build.py && node render.cjs
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

PRODUCTS = [
    dict(slug="01-coltar-ncl113", kicker="Colțar exterior decorativ", name="NCL113",
         dims="250/250 × 30 × 1000 mm", headline="Colțuri care dau<br>caracter fațadei",
         ambient="ambient-vila.jpg", amb_pos="50% 35%", product="ncl113.png", cutout=True,
         old="223,29", new="178,63", unit="lei / buc", pct=20,
         url="https://www.nmcromania.ro/coltar-exterior-decorativ-polistiren-ncl113-250-250x30x1000"),
    dict(slug="02-termosistem-fuga-panel-1", kicker="Termosistem decorativ", name="FUGA PANEL 1",
         dims="500 × 40 × 2000 mm", headline="Fațadă nouă,<br>montaj rapid",
         ambient="fuga1fer.jpg", amb_pos="50% 50%", product="fuga1.jpg", cutout=False,
         old="219,57", new="175,65", unit="lei / buc", pct=20,
         url="https://www.nmcromania.ro/termosistem-decorativ-fuga-panel-1-de-4-cm-500x40x2000"),
    dict(slug="03-cornisa-exterior-nc104", kicker="Cornișă decorativă exterior", name="NC104",
         dims="220 × 80 × 2000 mm", headline="Linia care<br>încheie casa",
         ambient="nc104fr.jpg", amb_pos="50% 0%", product="nc104.jpg", cutout=False,
         old="194,74", new="155,79", unit="lei / bară 2 m", pct=20,
         url="https://www.nmcromania.ro/cornisa-decorativa-exterior-nc104-220x80x2000"),
    dict(slug="04-cornisa-interior-z11", kicker="Cornișă decorativă tavan", name="Z11",
         dims="148 × 69 × 2000 mm", headline="Eleganță clasică<br>pe tavan",
         ambient="z11a.jpg", amb_pos="50% 30%", product="z11b.jpg", cutout=False,
         old="292,47", new="175,48", unit="lei / bară 2 m", pct=40,
         url="https://www.nmcromania.ro/plinta-decorativa-tavan-arstyl-z11"),
    dict(slug="05-tapet-carrara-best-82671", kicker="Tapet Carrara Best", name="82671",
         dims="rolă 1,06 × 10,05 m (10,65 mp)", headline="Efect de marmură<br>pe pereți",
         ambient="t82671b.jpg", amb_pos="50% 45%", product="t82671.jpg", cutout=False,
         old="665,50", new="465,85", unit="lei / rolă", pct=30,
         url="https://www.nmcromania.ro/tapet-carrara-82671"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;background:#161618;font-family:Roboto,sans-serif;color:#fff;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:#161618}
.amb{position:absolute;left:0;top:0;width:1080px;height:860px;object-fit:cover}
.shade{position:absolute;left:0;top:0;width:1080px;height:870px;
 background:linear-gradient(180deg,rgba(22,22,24,.55) 0%,rgba(22,22,24,0) 22%,rgba(22,22,24,0) 55%,rgba(22,22,24,.92) 92%,#161618 100%)}
.top{position:absolute;left:56px;right:56px;top:48px;display:flex;justify-content:space-between;align-items:center}
.logo{width:150px;height:auto;display:block;border-radius:10px;box-shadow:0 6px 24px rgba(0,0,0,.35)}
.bf{font-weight:900;font-size:40px;letter-spacing:4px;text-transform:uppercase;background:#000;padding:16px 26px 14px;border-radius:8px;line-height:1}
.bf i{font-style:normal;color:#FF671F}
.head{position:absolute;left:56px;top:560px;font-weight:900;font-size:66px;line-height:1.02;letter-spacing:-1px;text-shadow:0 4px 24px rgba(0,0,0,.45);max-width:600px}
.badge{position:absolute;right:48px;top:470px;width:270px;height:270px;border-radius:50%;background:#FF671F;
 display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 14px 40px rgba(0,0,0,.45);transform:rotate(-8deg)}
.badge b{font-weight:900;font-size:112px;line-height:.9;letter-spacing:-4px}
.badge span{font-weight:700;font-size:26px;letter-spacing:3px;text-transform:uppercase;margin-top:6px}
.card{position:absolute;left:56px;top:790px;width:400px;height:400px;background:#fff;border-radius:22px;overflow:hidden;
 box-shadow:0 18px 50px rgba(0,0,0,.5);border:6px solid #fff}
.card img{width:100%;height:100%;object-fit:cover}
.cut{position:absolute;left:10px;top:690px;width:470px;height:600px;
 background:radial-gradient(ellipse at 50% 92%,rgba(0,0,0,.55),rgba(0,0,0,0) 60%)}
.cut img{width:100%;height:100%;object-fit:contain;object-position:50% 100%;filter:drop-shadow(0 24px 30px rgba(0,0,0,.6))}
.info{position:absolute;left:500px;right:56px;top:828px}
.kick{color:#FF671F;font-weight:700;font-size:27px;letter-spacing:2.5px;text-transform:uppercase}
.name{font-weight:900;font-size:76px;line-height:1;margin-top:10px;letter-spacing:-1px}
.dims{color:#b9bcc6;font-size:26px;margin-top:10px}
.old{margin-top:22px;font-size:36px;color:#9a9ca6;font-weight:500}
.old s{text-decoration-thickness:3px;text-decoration-color:#FF671F}
.new{display:flex;align-items:flex-start;color:#FF671F;font-weight:900;line-height:.86;margin-top:4px}
.new .i{font-size:140px;letter-spacing:-5px}
.new .d{font-size:62px;margin-top:8px;margin-left:4px}
.unit{color:#fff;font-size:28px;font-weight:500;margin-top:10px}
.foot{position:absolute;left:0;right:0;bottom:0;height:86px;background:#FF671F;display:flex;align-items:center;justify-content:space-between;padding:0 56px}
.foot b{font-weight:900;font-size:36px;letter-spacing:.5px}
.foot span{font-size:21px;font-weight:500;text-align:right;line-height:1.25}

/* ---- Story / Reel 1080x1920: zone sigure sus ~200px si jos ~250px ---- */
body.story,.story .c{height:1920px}
.story .amb{height:1130px}.story .shade{height:1140px;background:linear-gradient(180deg,rgba(22,22,24,.6) 0%,rgba(22,22,24,0) 20%,rgba(22,22,24,0) 58%,rgba(22,22,24,.92) 92%,#161618 100%)}
.story .top{top:200px}
.story .head{top:770px;font-size:78px;max-width:660px}
.story .badge{top:630px;width:300px;height:300px}.story .badge b{font-size:124px}
.story .card{top:1060px;width:410px;height:410px}
.story .cut{top:910px;height:620px}
.story .info{top:1090px}
.story .foot{bottom:250px;height:100px}.story .foot b{font-size:40px}
.story .tail{position:absolute;left:0;right:0;bottom:0;height:250px;background:#161618}
"""

def scene(p):
    i, d = p["new"].split(",")
    if p["cutout"]:
        prod = f'<div class="cut"><img src="assets/{p["product"]}" alt=""></div>'
    else:
        prod = f'<div class="card"><img src="assets/{p["product"]}" alt=""></div>'
    return f"""
<img class="amb" src="assets/{p['ambient']}" style="object-position:{p['amb_pos']}" alt="">
<div class="shade"></div>
<div class="top"><img class="logo" src="assets/nmc-logo.png" alt="nmc"><div class="bf">Black <i>Friday</i></div></div>
<div class="head">{p['headline']}</div>
<div class="badge"><b>−{p['pct']}%</b><span>reducere</span></div>
{prod}
<div class="info">
 <div class="kick">{p['kicker']}</div>
 <div class="name">{p['name']}</div>
 <div class="dims">{p['dims']}</div>
 <div class="old">Preț vechi <s>{p['old']} lei</s></div>
 <div class="new"><span class="i">{i}</span><span class="d">,{d}</span></div>
 <div class="unit">{p['unit']} · TVA inclus</div>
</div>
<div class="foot"><b>nmcromania.ro</b><span>Ofertă valabilă în limita<br>stocului disponibil</span></div>"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
 '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">'
 '<style>' + CSS + '</style></head>')

def page(p, story=False):
    t = f"NMC Black Friday — {p['kicker']} {p['name']}" + (" — Story" if story else "")
    cls = ' class="story"' if story else ''
    tail = '<div class="tail"></div>' if story else ''
    return HEAD.replace('{t}', t) + f'<body{cls}><div class="c">' + scene(p) + tail + '</div></body></html>'

for p in PRODUCTS:
    (ROOT / f"{p['slug']}.html").write_text(page(p))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, True).replace('src="assets/', 'src="../assets/'))
(ROOT / "products.json").write_text(json.dumps(
    {"pricesCheckedAt": "2026-11-12", "source": "https://www.nmcromania.ro/", "products": PRODUCTS},
    ensure_ascii=False, indent=1))
print("ok", len(PRODUCTS))

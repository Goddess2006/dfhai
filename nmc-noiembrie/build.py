"""Postere generice NMC — noiembrie (fără preț/reducere), focus pe produs.
Feed 1080x1350 (./NN-*.html) + Story 1080x1920 (./story/*-story.html). Rulare: python3 build.py && node render.cjs
Date de produs verificate pe nmcromania.ro la 12.11.2026 (toate InStock).
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

TAG = "Inspirație de sezon"

PRODUCTS = [
    dict(slug="01-plinta-fl12", kicker="Plintă decorativă · Wallstyl", name="FL12",
         dims="80 × 13 × 2000 mm · polimer dur", headline="Finisajul curat<br>pe care îl vezi zilnic",
         ambient="fl12amb.jpg", amb_pos="50% 50%", product="sec-fl12.png", badge=("Gata de", "vopsit"),
         points=["Rezistentă la șocuri și umezeală", "Montaj curat, fără praf sau șuruburi", "Linii simple, moderne, atemporale"],
         url="https://www.nmcromania.ro/plinta-polimer-dur-fl12"),
    dict(slug="02-plinta-led-il11", kicker="Plintă cu iluminat LED", name="IL11 negru",
         dims="80 × 20 × 2000 mm · RAL 7021", headline="Lumină caldă<br>la nivelul podelei",
         ambient="il11amb.jpg", amb_pos="60% 50%", product="sec-il11.png", badge=("Iluminat", "indirect"),
         points=["Lumină ambientală discretă, la podea", "Design modern, în negru mat", "Rezistentă la șocuri și umezeală"],
         url="https://www.nmcromania.ro/plinta-decorativa-il11-neagra-80x20x2000"),
    dict(slug="03-scafa-led-arstyl-l2", kicker="Scafă / cornișă LED · Arstyl", name="L2",
         dims="200 × 250 × 2000 mm · poliuretan", headline="Tavanul devine<br>sursă de lumină",
         ambient="l2a.jpg", amb_pos="50% 50%", product="sec-l2b.png", badge=("Pentru", "LED & spoturi"),
         points=["Integrează bandă LED sau spoturi", "Ascunde cabluri și tubulaturi", "Preamorsată, gata de vopsit"],
         url="https://www.nmcromania.ro/l2-arstyl"),
    dict(slug="04-brau-chenare-wo2", kicker="Brâu decorativ · Wallstyl", name="WO2",
         dims="38 × 18 × 2000 mm · polimer dur", headline="Chenare elegante<br>pe orice perete",
         ambient="wo2a.jpg", amb_pos="50% 50%", product="sec-wo2b.png", badge=("Ideal pentru", "chenare"),
         points=["Rame decorative pe pereți și uși", "Ușor de tăiat și îmbinat la 45°", "Preamorsat, gata de vopsit"],
         url="https://www.nmcromania.ro/brau-decorativwo2-wallstyl"),
    dict(slug="05-accent-3d-exterior-a106", kicker="Accent 3D exterior", name="A106",
         dims="600 × 450 × 55 mm · polistiren cu rășină", headline="Ultimul strop<br>de eleganță<br>înainte de sărbători",
         ambient="ambient-vila.jpg", amb_pos="50% 20%", product="a106.jpg", badge=("Detaliu", "de fațadă"),
         points=["Punctul de atracție al fațadei", "Polistiren acoperit cu rășină", "Se vopsește în orice culoare"],
         url="https://www.nmcromania.ro/accent-3d-a106-600x450x55"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;background:#161618;font-family:Roboto,sans-serif;color:#fff;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:#161618}
.amb{position:absolute;left:0;top:0;width:1080px;height:860px;object-fit:cover}
.shade{position:absolute;left:0;top:0;width:1080px;height:870px;
 background:linear-gradient(180deg,rgba(22,22,24,.55) 0%,rgba(22,22,24,0) 22%,rgba(22,22,24,0) 50%,rgba(22,22,24,.92) 90%,#161618 100%)}
.top{position:absolute;left:56px;right:56px;top:48px;display:flex;justify-content:space-between;align-items:center}
.logo{width:150px;height:auto;display:block;border-radius:10px;box-shadow:0 6px 24px rgba(0,0,0,.35)}
.tag{font-weight:700;font-size:28px;letter-spacing:3px;text-transform:uppercase;background:rgba(0,0,0,.78);padding:16px 24px 14px;border-radius:8px;line-height:1;border-left:6px solid #FF671F}
.head{position:absolute;left:56px;bottom:auto;top:auto;font-weight:900;font-size:64px;line-height:1.03;letter-spacing:-1px;text-shadow:0 4px 24px rgba(0,0,0,.5);max-width:640px}
.badge{position:absolute;right:48px;top:500px;width:240px;height:240px;border-radius:50%;background:#FF671F;
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.45);transform:rotate(-8deg);padding:20px}
.badge span{font-weight:500;font-size:28px;line-height:1.1}
.badge b{font-weight:900;font-size:40px;line-height:1.02;text-transform:uppercase;margin-top:4px}
.card{position:absolute;left:56px;top:800px;width:400px;height:400px;background:#fff;border-radius:22px;overflow:hidden;
 box-shadow:0 18px 50px rgba(0,0,0,.5);border:6px solid #fff}
.card img{width:100%;height:100%;object-fit:contain}
.info{position:absolute;left:500px;right:56px;top:828px}
.kick{color:#FF671F;font-weight:700;font-size:25px;letter-spacing:2.2px;text-transform:uppercase}
.name{font-weight:900;font-size:76px;line-height:1;margin-top:10px;letter-spacing:-1px}
.dims{color:#b9bcc6;font-size:25px;margin-top:10px}
ul{list-style:none;margin-top:26px}
li{position:relative;padding-left:40px;font-size:28px;line-height:1.25;margin-top:14px;font-weight:500}
li::before{content:"";position:absolute;left:0;top:7px;width:22px;height:22px;border-radius:50%;background:#FF671F}
li::after{content:"";position:absolute;left:6px;top:11px;width:9px;height:5px;border-left:3px solid #fff;border-bottom:3px solid #fff;transform:rotate(-45deg)}
.foot{position:absolute;left:0;right:0;bottom:0;height:86px;background:#FF671F;display:flex;align-items:center;justify-content:space-between;padding:0 56px}
.foot b{font-weight:900;font-size:36px;letter-spacing:.5px}
.foot span{font-size:24px;font-weight:700;text-align:right;text-transform:uppercase;letter-spacing:1.5px}
/* ---- Story 1080x1920: zone sigure sus ~200px si jos ~250px ---- */
body.story,.story .c{height:1920px}
.story .amb{height:1130px}.story .shade{height:1140px;background:linear-gradient(180deg,rgba(22,22,24,.6) 0%,rgba(22,22,24,0) 20%,rgba(22,22,24,0) 52%,rgba(22,22,24,.92) 90%,#161618 100%)}
.story .top{top:200px}
.story .badge{top:640px;width:270px;height:270px}
.story .card{top:1060px;width:410px;height:410px}
.story .info{top:1090px}
.story .foot{bottom:250px;height:100px}.story .foot b{font-size:40px}
.story .tail{position:absolute;left:0;right:0;bottom:0;height:250px;background:#161618}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')


def scene(p, story):
    lines = p["headline"].count("<br>") + 1
    # titlul se așază deasupra cardului, indiferent de numărul de rânduri
    bottom_edge = 1020 if story else 760
    top = bottom_edge - lines * 66
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    return f"""<img class="amb" src="assets/{p['ambient']}" style="object-position:{p['amb_pos']}" alt="">
<div class="shade"></div>
<div class="top"><img class="logo" src="assets/nmc-logo.png" alt="nmc"><div class="tag">{TAG}</div></div>
<div class="head" style="top:{top}px">{p['headline']}</div>
<div class="badge"><span>{p['badge'][0]}</span><b>{p['badge'][1]}</b></div>
<div class="card"><img src="assets/{p['product']}" alt=""></div>
<div class="info">
 <div class="kick">{p['kicker']}</div>
 <div class="name">{p['name']}</div>
 <div class="dims">{p['dims']}</div>
 <ul>{pts}</ul>
</div>
<div class="foot"><b>nmcromania.ro</b><span>Descoperă colecția</span></div>"""


def page(p, story=False):
    t = f"NMC — {p['kicker']} {p['name']}" + (" — Story" if story else "")
    cls = ' class="story"' if story else ''
    tail = '<div class="tail"></div>' if story else ''
    return HEAD.replace('{t}', t) + f'<body{cls}><div class="c">' + scene(p, story) + tail + '</div></body></html>'


for p in PRODUCTS:
    (ROOT / f"{p['slug']}.html").write_text(page(p))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, True).replace('src="assets/', 'src="../assets/'))
(ROOT / "products.json").write_text(json.dumps(
    {"checkedAt": "2026-11-12", "source": "https://www.nmcromania.ro/", "products": PRODUCTS}, ensure_ascii=False, indent=1))
print("ok", len(PRODUCTS))

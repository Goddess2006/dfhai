"""NMC — 4 creative de vânzare pentru produse de exterior ADRo (producție proprie în România).
Fără preț numeric (reducerea nu e stabilită): insigna „Prețuri speciale”. Feed 1080x1350 + Story 1080x1920.
Rulare: python3 build.py && node render.cjs
Afirmații preluate de pe nmcromania.ro (Despre noi + fișe produs, 15.11.2026): peste 20 de ani, lider de piață,
linie de producție proprie, strat de rășină + nisip cuarțos, rezistent la UV / umiditate / îngheț-dezgheț, vopsibil.
„Rășină brevetată” = afirmație a clientului, nu apare pe site — de confirmat înainte de publicare.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

TRUST = [
    ("flag", "Producție proprie<br>în România"),
    ("shield", "Rășină brevetată<br>ADRo® + cuarț"),
    ("weather", "Rezistent la UV,<br>ger și umezeală"),
]

PRODUCTS = [
    dict(slug="01-termosistem-fuga-panel-1", kicker="Termosistem decorativ ADRo", name="FUGA PANEL 1",
         dims="500 × 40 × 2000 mm", h1="Fațadă nouă,", h2="făcută să reziste.",
         ambient="fuga1fer.jpg", amb_pos="50% 45%", cards=[("fuga1.jpg", "")],
         chips=["Finisaj decorativ + izolație", "Se vopsește în orice culoare RAL"],
         url="https://www.nmcromania.ro/termosistem-decorativ-fuga-panel-1-de-4-cm-500x40x2000"),
    dict(slug="02-termosistem-sidding-panel-3", kicker="Termosistem decorativ ADRo", name="SIDDING PANEL 3",
         dims="500 × 40 × 2000 mm", h1="Durabilitate", h2="fără compromis.",
         ambient="sid3fer.jpg", amb_pos="50% 45%", cards=[("sid3.jpg", "")],
         chips=["Aspect de lambriu orizontal", "Montaj rapid, prin lipire"],
         url="https://www.nmcromania.ro/termosistem-decorativ-sidding-panel-3-500x40x2000"),
    dict(slug="03-coltar-ncl107", kicker="Colțar exterior decorativ ADRo", name="NCL107",
         dims="300/300 × 30 × 1000 mm", h1="Colțuri puternice,", h2="case care durează.",
         ambient="ambient-casa.jpg", amb_pos="62% 45%", cards=[("ncl107.jpg", "")],
         chips=["Strat de rășină + nisip cuarțos", "Vopsibil cu vopsea acrilică"],
         url="https://www.nmcromania.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300"),
    dict(slug="04-gama-exterior-adro", kicker="Gama de exterior ADRo", name="Fațada completă",
         dims="Ancadramente · Cornișe · Solbancuri · Colțare", h1="Fațada completă,", h2="produsă în România.",
         ambient="ambient-vila.jpg", amb_pos="50% 30%",
         cards=[("na105f.jpg", "Ancadrament NA105"), ("nc104.jpg", "Cornișă NC104"), ("ns111.jpg", "Solbanc NS111")],
         chips=[], url="https://www.nmcromania.ro/profile-decorative-exterior"),
]

ICONS = {
    "flag": '<svg viewBox="0 0 36 24"><rect width="12" height="24" fill="#002B7F"/><rect x="12" width="12" height="24" fill="#FCD116"/><rect x="24" width="12" height="24" fill="#CE1126"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="#FF671F" stroke-width="2" stroke-linejoin="round"><path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8 12l3 3 5-6" stroke-linecap="round"/></svg>',
    "weather": '<svg viewBox="0 0 24 24" fill="none" stroke="#FF671F" stroke-width="2" stroke-linecap="round"><circle cx="8" cy="8" r="3.2"/><path d="M8 1.5v1.6M8 12.9v1.6M1.5 8h1.6M12.9 8h1.6M3.4 3.4l1.1 1.1M11.5 11.5l1.1 1.1M3.4 12.6l1.1-1.1M11.5 4.5l1.1-1.1"/><path d="M17 13v9M13.1 15.2l7.8 4.6M13.1 19.8l7.8-4.6"/></svg>',
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;background:#161618;font-family:Roboto,sans-serif;color:#fff;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:#161618}
.amb{position:absolute;left:0;top:0;width:1080px;height:800px;object-fit:cover}
.shade{position:absolute;left:0;top:0;width:1080px;height:810px;
 background:linear-gradient(180deg,rgba(22,22,24,.65) 0%,rgba(22,22,24,.05) 24%,rgba(22,22,24,0) 45%,rgba(22,22,24,.85) 85%,#161618 100%)}
.top{position:absolute;left:56px;right:56px;top:48px;display:flex;justify-content:space-between;align-items:center}
.logo{width:150px;height:auto;display:block;border-radius:10px;box-shadow:0 6px 24px rgba(0,0,0,.35)}
.tag{text-align:right;background:rgba(0,0,0,.8);padding:14px 22px;border-radius:8px;border-right:6px solid #FF671F}
.tag b{display:block;font-weight:900;font-size:30px;letter-spacing:2px;text-transform:uppercase;line-height:1}
.tag span{display:block;font-size:19px;letter-spacing:2px;text-transform:uppercase;color:#FF671F;font-weight:700;margin-top:6px}
.head{position:absolute;left:56px;right:330px;top:520px;font-weight:900;font-size:62px;line-height:1.04;letter-spacing:-1px;text-shadow:0 4px 24px rgba(0,0,0,.55)}
.head .l2{color:#FF671F;display:block}
.badge{position:absolute;right:48px;top:470px;width:250px;height:250px;border-radius:50%;background:#FF671F;
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.45);transform:rotate(-8deg)}
.badge span{font-weight:700;font-size:26px;letter-spacing:3px;text-transform:uppercase}
.badge b{font-weight:900;font-size:50px;line-height:.95;text-transform:uppercase;margin:6px 0}
.badge small{font-size:19px;font-weight:500;line-height:1.2}
.card{position:absolute;left:56px;top:770px;width:360px;height:360px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.5);border:6px solid #fff}
.card img{width:100%;height:100%;object-fit:cover}
.made{position:absolute;left:0;bottom:0;right:0;background:rgba(22,22,24,.86);display:flex;align-items:center;gap:10px;padding:10px 14px;font-size:18px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase}
.made svg{width:30px;height:20px;flex:none}
.info{position:absolute;left:452px;right:56px;top:790px}
.kick{color:#FF671F;font-weight:700;font-size:24px;letter-spacing:2.2px;text-transform:uppercase}
.name{font-weight:900;font-size:66px;line-height:1;margin-top:10px;letter-spacing:-1px}
.dims{color:#b9bcc6;font-size:25px;margin-top:10px}
.chips{display:flex;flex-direction:column;gap:12px;margin-top:24px}
.chips span{align-self:flex-start;border:2px solid #FF671F;border-radius:40px;padding:9px 20px;font-size:23px;font-weight:500}
.cards3{position:absolute;left:56px;right:56px;top:780px;display:flex;gap:26px}
.cards3 figure{flex:1;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.5)}
.cards3 img{width:100%;height:240px;object-fit:cover;display:block}
.cards3 figcaption{color:#161618;font-weight:700;font-size:22px;padding:12px 14px;text-align:center}
.trust{position:absolute;left:56px;right:56px;bottom:112px;display:flex;justify-content:space-between;border-top:1px solid #3a3a3e;padding-top:20px}
.trust div{display:flex;align-items:center;gap:12px;font-size:20px;font-weight:700;line-height:1.2;text-transform:uppercase;letter-spacing:.5px}
.trust svg{width:40px;height:30px;flex:none}
.trust div:first-child svg{width:36px;height:24px}
.foot{position:absolute;left:0;right:0;bottom:0;height:86px;background:#FF671F;display:flex;align-items:center;justify-content:space-between;padding:0 56px}
.foot b{font-weight:900;font-size:36px;letter-spacing:.5px}
.foot span{font-size:22px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px}
.gama .info{display:none}
/* ---- Story 1080x1920 ---- */
body.story,.story .c{height:1920px}
.story .amb{height:1150px}.story .shade{height:1160px;background:linear-gradient(180deg,rgba(22,22,24,.75) 0%,rgba(22,22,24,.15) 22%,rgba(22,22,24,0) 45%,rgba(22,22,24,.85) 85%,#161618 100%)}
.story .top{top:210px}
.story .head{top:860px;font-size:68px}
.story .badge{top:800px}
.story .card{top:1110px;width:380px;height:380px}
.story .info{top:1130px;left:470px}
.story .cards3{top:1110px}.story .cards3 img{height:280px}
.story .trust{bottom:370px}
.story .foot{bottom:250px;height:100px}
.story .tail{position:absolute;left:0;right:0;bottom:0;height:250px;background:#161618}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')


def scene(p):
    flag = ICONS["flag"]
    trust = "".join(f'<div>{ICONS[k]}<span>{t}</span></div>' for k, t in TRUST)
    if len(p["cards"]) == 1:
        prod = (f'<div class="card"><img src="assets/{p["cards"][0][0]}" alt="">'
                f'<div class="made">{flag}Made in Romania</div></div>'
                '<div class="info">'
                f'<div class="kick">{p["kicker"]}</div><div class="name">{p["name"]}</div><div class="dims">{p["dims"]}</div>'
                '<div class="chips">' + "".join(f"<span>{c}</span>" for c in p["chips"]) + '</div></div>')
    else:
        prod = '<div class="cards3">' + "".join(
            f'<figure><img src="assets/{f}" alt=""><figcaption>{cap}</figcaption></figure>' for f, cap in p["cards"]) + '</div>'
    return f"""<img class="amb" src="assets/{p['ambient']}" style="object-position:{p['amb_pos']}" alt="">
<div class="shade"></div>
<div class="top"><img class="logo" src="assets/nmc-logo.png" alt="nmc"><div class="tag"><b>Lider de piață</b><span>peste 20 de ani de experiență</span></div></div>
<div class="head">{p['h1']}<span class="l2">{p['h2']}</span></div>
<div class="badge"><span>Prețuri</span><b>speciale</b><small>calitate fără<br>compromis</small></div>
{prod}
<div class="trust">{trust}</div>
<div class="foot"><b>nmcromania.ro</b><span>Descoperă prețurile speciale</span></div>"""


def page(p, story=False):
    t = f"NMC — {p['kicker']} {p['name']}" + (" — Story" if story else "")
    cls = ["gama"] if len(p["cards"]) > 1 else []
    if story:
        cls.append("story")
    tail = '<div class="tail"></div>' if story else ''
    return (HEAD.replace('{t}', t) + f'<body class="{" ".join(cls)}"><div class="c">' + scene(p) + tail + '</div></body></html>')


for p in PRODUCTS:
    (ROOT / f"{p['slug']}.html").write_text(page(p))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, True).replace('src="assets/', 'src="../assets/'))
(ROOT / "products.json").write_text(json.dumps(
    {"checkedAt": "2026-11-15", "source": "https://www.nmcromania.ro/", "products": PRODUCTS}, ensure_ascii=False, indent=1))
print("ok", len(PRODUCTS))

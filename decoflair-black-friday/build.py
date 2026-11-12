"""Creative Black Friday Deco&Flair — feed 1080x1350 (Facebook + Instagram) și story 1080x1920.
Prețuri și reduceri reale de pe decoflair.ro (12.11.2026, cu TVA, toate InStock).
Rulare: python3 build.py && node render.cjs
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

PRODUCTS = [
    dict(slug="01-scafa-led-l5", kicker="Scafă LED pentru tavan · Arstyl", name="L5",
         dims="200 × 200 × 2000 mm · poliuretan", h1="Lumina", h2="devine arhitectură.",
         ambient="amb-led.jpg", amb_pos="55% 30%", product="l5a.jpg",
         old="585,36", new="409,75", unit="lei / bară 2 m", pct=30,
         url="https://decoflair.ro/l5-arstyl"),
    dict(slug="02-cornisa-z11", kicker="Cornișă decorativă de tavan · Arstyl", name="Z11",
         dims="148 × 69 × 2000 mm · poliuretan", h1="Tavanul care", h2="spune o poveste.",
         ambient="amb-interior.jpg", amb_pos="50% 25%", product="z11a.jpg",
         old="292,47", new="204,73", unit="lei / bară 2 m", pct=30,
         url="https://decoflair.ro/plinta-decorativa-tavan-arstyl-z11"),
    dict(slug="03-brau-chenare-wo2", kicker="Brâu decorativ pentru chenare · Wallstyl", name="WO2",
         dims="38 × 18 × 2000 mm · polimer dur", h1="Pereți cu ritm,", h2="proporție și eleganță.",
         ambient="amb-chenare.jpg", amb_pos="40% 40%", product="wo2a.jpg",
         old="66,03", new="46,22", unit="lei / bară 2 m", pct=30,
         url="https://decoflair.ro/brau-decorativwo2-wallstyl"),
    dict(slug="04-tapet-carrara-82603", kicker="Tapet premium Carrara Best", name="82603",
         dims="rolă 1,06 × 10,05 m (10,65 mp)", h1="Eleganța marmurei,", h2="acasă la tine.",
         ambient="t03b.jpg", amb_pos="50% 40%", product="t03.jpg",
         old="665,50", new="465,85", unit="lei / rolă", pct=30,
         url="https://decoflair.ro/tapet-carrara-82603"),
    dict(slug="05-ancadrament-na105", kicker="Ancadrament decorativ fereastră", name="NA105",
         dims="175 × 40 × 2000 mm · polistiren cu rășină", h1="Fațada pe care", h2="ți-ai dorit-o.",
         ambient="amb-exterior.jpg", amb_pos="40% 50%", product="na105f.jpg",
         old="163,70", new="130,96", unit="lei / bară 2 m", pct=20,
         url="https://decoflair.ro/ancadrament-decorativ-na105"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--gold:#D6BC84;--gold2:#b89a5e;--red:#B42127;--ink:#141213;--cream:#f5efe4;--mut:#b8afa3}
html,body{font-variant-numeric:lining-nums;width:1080px;height:1350px;background:var(--ink);font-family:Jost,sans-serif;color:#fff;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:var(--ink)}
.amb{position:absolute;left:0;top:0;width:1080px;height:880px;object-fit:cover}
.shade{position:absolute;left:0;top:0;width:1080px;height:890px;
 background:linear-gradient(180deg,rgba(20,18,19,.78) 0%,rgba(20,18,19,.25) 20%,rgba(20,18,19,0) 40%,rgba(20,18,19,.55) 70%,rgba(20,18,19,.96) 94%,var(--ink) 100%)}
.frame{position:absolute;inset:26px;border:1.5px solid rgba(214,188,132,.55);pointer-events:none}
.top{position:absolute;left:62px;right:62px;top:58px;display:flex;justify-content:space-between;align-items:center}
.logo{width:230px;height:auto;display:block;filter:drop-shadow(0 2px 10px rgba(0,0,0,.5))}
.bf{text-align:right;line-height:1}
.bf b{display:block;font-family:'Playfair Display',serif;font-weight:700;font-size:44px;letter-spacing:2px;color:var(--gold);text-shadow:0 2px 14px rgba(0,0,0,.5)}
.bf span{display:inline-block;margin-top:10px;font-size:17px;letter-spacing:5px;text-transform:uppercase;font-weight:500;padding-left:14px;border-left:4px solid var(--red)}
.head{position:absolute;left:62px;right:62px;top:600px;font-family:'Playfair Display',serif;font-weight:700;text-transform:uppercase;line-height:1.02;letter-spacing:.5px;text-shadow:0 4px 28px rgba(0,0,0,.6)}
.head .l1{font-size:60px;color:#fff;display:block}
.head .l2{font-size:60px;color:var(--gold);display:block}
.rule{width:90px;height:3px;background:var(--gold);margin-bottom:22px}
.card{position:absolute;left:62px;top:842px;width:360px;height:360px;background:var(--cream);overflow:hidden;
 box-shadow:0 22px 60px rgba(0,0,0,.6);outline:1.5px solid var(--gold);outline-offset:8px}
.card img{width:100%;height:100%;object-fit:cover}
.medal{position:absolute;left:22px;top:790px;width:170px;height:170px;border-radius:50%;background:var(--red);
 display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 12px 34px rgba(0,0,0,.55);
 border:3px solid var(--gold);outline:1.5px solid rgba(214,188,132,.6);outline-offset:6px}
.medal b{font-family:'Playfair Display',serif;font-weight:700;font-size:62px;line-height:.9;letter-spacing:-1px}
.medal span{font-size:15px;letter-spacing:3.5px;text-transform:uppercase;margin-top:6px;font-weight:500;color:var(--cream)}
.info{position:absolute;left:466px;right:62px;top:850px}
.kick{color:var(--gold);font-weight:500;font-size:21px;letter-spacing:3px;text-transform:uppercase;line-height:1.3}
.name{font-variant-numeric:lining-nums;font-family:'Playfair Display',serif;font-weight:700;font-size:66px;line-height:1;margin-top:12px}
.dims{color:var(--mut);font-size:23px;margin-top:10px;font-weight:300}
.old{margin-top:18px;font-size:28px;color:var(--mut);font-weight:300;letter-spacing:.5px}
.old s{text-decoration-thickness:2px;text-decoration-color:var(--red)}
.new{display:flex;align-items:flex-start;color:var(--gold);font-family:'Playfair Display',serif;font-weight:700;line-height:.9;margin-top:6px}
.new .i{font-size:104px;letter-spacing:-1px}
.new .d{font-size:46px;margin-top:8px;margin-left:4px}
.unit{color:#fff;font-size:23px;font-weight:400;margin-top:6px;letter-spacing:.5px}
.foot{position:absolute;left:62px;right:62px;bottom:56px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(214,188,132,.45);padding-top:20px}
.foot b{font-family:'Playfair Display',serif;font-weight:700;font-size:32px;letter-spacing:1px;color:var(--cream)}
.foot span{font-size:16px;letter-spacing:3px;text-transform:uppercase;color:var(--mut)}
/* ---- Story 1080x1920: zone sigure sus ~200px si jos ~250px ---- */
body.story,.story .c{height:1920px}
.story .amb{height:1180px}.story .shade{height:1190px;background:linear-gradient(180deg,rgba(20,18,19,.85) 0%,rgba(20,18,19,.55) 22%,rgba(20,18,19,0) 38%,rgba(20,18,19,.55) 70%,rgba(20,18,19,.96) 94%,var(--ink) 100%)}
.story .top{top:210px}
.story .head{top:860px}.story .head .l1,.story .head .l2{font-size:66px}
.story .card{top:1150px}
.story .medal{top:1095px}
.story .info{top:1158px}
.story .foot{bottom:270px}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')


def scene(p):
    i, d = p["new"].split(",")
    return f"""<img class="amb" src="assets/{p['ambient']}" style="object-position:{p['amb_pos']}" alt="">
<div class="shade"></div><div class="frame"></div>
<div class="top"><img class="logo" src="assets/logo-decoflair.png" alt="Deco&amp;Flair"><div class="bf"><b>BLACK FRIDAY</b><span>Deco &amp; Flair</span></div></div>
<div class="head"><div class="rule"></div><span class="l1">{p['h1']}</span><span class="l2">{p['h2']}</span></div>
<div class="card"><img src="assets/{p['product']}" alt=""></div>
<div class="medal"><b>−{p['pct']}%</b><span>reducere</span></div>
<div class="info">
 <div class="kick">{p['kicker']}</div>
 <div class="name">{p['name']}</div>
 <div class="dims">{p['dims']}</div>
 <div class="old">Preț întreg <s>{p['old']} lei</s></div>
 <div class="new"><span class="i">{i}</span><span class="d">,{d}</span></div>
 <div class="unit">{p['unit']} · TVA inclus</div>
</div>
<div class="foot"><b>decoflair.ro</b><span>În limita stocului disponibil</span></div>"""


def page(p, story=False):
    t = f"Deco&Flair Black Friday — {p['kicker']} {p['name']}" + (" — Story" if story else "")
    cls = ' class="story"' if story else ''
    return HEAD.replace('{t}', t) + f'<body{cls}><div class="c">' + scene(p) + '</div></body></html>'


for p in PRODUCTS:
    (ROOT / f"{p['slug']}.html").write_text(page(p))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, True).replace('src="assets/', 'src="../assets/'))
(ROOT / "products.json").write_text(json.dumps(
    {"pricesCheckedAt": "2026-11-12", "source": "https://decoflair.ro/oferte-speciale", "products": PRODUCTS},
    ensure_ascii=False, indent=1))
print("ok", len(PRODUCTS))

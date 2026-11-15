"""Deco&Flair — 10 creative „Lux 2027”: know-how + produse premium + mesaj de cumpărare (fără butoane).
Ton decoflair.ro (întunecat, auriu, vișiniu) într-un aspect modern-futurist: linii HUD fine, etichete monospace,
panou de sticlă pentru produs, aură caldă. Feed 1080x1350 + Story 1080x1920.
Prețuri live de pe decoflair.ro la 15.11.2026 (cu TVA, toate InStock).
Rulare: python3 build.py && node render.cjs
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

P = [
    dict(slug="01-tapet-carrara-82603", cat="Tapet premium", name="Carrara Best 82603", spec="rolă 1,06 × 10,05 m · 10,65 mp",
         l1="Pereți care arată", l2="a marmură italiană.",
         tip="Un singur perete accent cu tapet texturat schimbă complet camera — fără renovare.",
         amb="t03b.jpg", pos="50% 45%", img="t03.jpg", price="465,85", unit="lei / rolă",
         buy="Comandă tapetul pe", url="https://decoflair.ro/tapet-carrara-82603"),
    dict(slug="02-tapet-carrara-82671", cat="Tapet premium", name="Carrara Best 82671", spec="rolă 1,06 × 10,05 m · 10,65 mp",
         l1="Dormitor de hotel 5 stele,", l2="acasă la tine.",
         tip="Tapetul din spatele patului devine punctul focal al camerei, ca o tăblie generoasă.",
         amb="t71b.jpg", pos="50% 45%", img="t71.jpg", price="465,85", unit="lei / rolă",
         buy="Comandă tapetul pe", url="https://decoflair.ro/tapet-carrara-82671"),
    dict(slug="03-scafa-led-l5", cat="Scafă LED · Arstyl", name="L5", spec="200 × 200 × 2000 mm · poliuretan",
         l1="Lumina care face", l2="camera să pară mai înaltă.",
         tip="Lumina indirectă spre tavan ridică optic plafonul și elimină umbrele dure.",
         amb="amb-led.jpg", pos="60% 30%", img="l5a.jpg", price="409,75", unit="lei / bară 2 m",
         buy="Comandă scafa pe", url="https://decoflair.ro/l5-arstyl"),
    dict(slug="04-cornisa-z11", cat="Cornișă ornamentală · Arstyl", name="Z11", spec="148 × 69 × 2000 mm · poliuretan",
         l1="„Vai, ce casă", l2="frumoasă aveți!”",
         tip="Cornișa ornamentată e primul detaliu pe care îl observă musafirii. Se montează lipit, fără praf.",
         amb="amb-interior.jpg", pos="45% 20%", img="z11a.jpg", price="204,73", unit="lei / bară 2 m",
         buy="Comandă cornișa pe", url="https://decoflair.ro/plinta-decorativa-tavan-arstyl-z11"),
    dict(slug="05-cornisa-z21", cat="Cornișă de tavan · Arstyl", name="Z21", spec="101 × 112 × 2000 mm · poliuretan",
         l1="Tavane ca în filmele", l2="de Crăciun.",
         tip="La tavane înalte, alege o cornișă mai generoasă: proporția face diferența dintre simplu și spectaculos.",
         amb="amb-led-window.jpg", pos="50% 30%", img="z21a.jpg", price="205,02", unit="lei / bară 2 m",
         buy="Comandă cornișa pe", url="https://decoflair.ro/plinta-decorativa-tavan-arstyl-z21"),
    dict(slug="06-brau-chenare-wo2", cat="Brâu pentru chenare · Wallstyl", name="WO2", spec="38 × 18 × 2000 mm · polimer dur",
         l1="Lux de 5 stele,", l2="cu bani puțini.",
         tip="Chenarele din brâu dau pereților aspect de boiserie clasică, la o fracțiune din cost.",
         amb="amb-chenare.jpg", pos="40% 40%", img="wo2a.jpg", price="46,22", unit="lei / bară 2 m",
         buy="Comandă brâul pe", url="https://decoflair.ro/brau-decorativwo2-wallstyl"),
    dict(slug="07-plinta-fd3", cat="Plintă decorativă · Wallstyl", name="FD3", spec="100 × 20 × 2000 mm · polimer dur",
         l1="Detaliul de jos", l2="care ridică tot interiorul.",
         tip="O plintă înaltă și albă face pardoseala să pară mai scumpă și ascunde cablurile.",
         amb="amb-led-floor.jpg", pos="40% 70%", img="fd3a.jpg", price="84,79", unit="lei / bară 2 m",
         buy="Comandă plinta pe", url="https://decoflair.ro/plintafd3-wallstyl"),
    dict(slug="08-cornisa-wt25", cat="Cornișă modernă · Wallstyl", name="WT25", spec="78 × 78 × 2000 mm · polimer dur",
         l1="Linii curate,", l2="eleganță contemporană.",
         tip="În interioarele minimaliste, profilul simplu al cornișei păstrează liniile curate și arată modern.",
         amb="amb-tapet.jpg", pos="50% 30%", img="wt25a.jpg", price="150,93", unit="lei / bară 2 m",
         buy="Comandă cornișa pe", url="https://decoflair.ro/cornisa-decorativa-wt25-wallstyl"),
    dict(slug="09-ancadrament-na105", cat="Ancadrament fereastră · exterior", name="NA105", spec="175 × 40 × 2000 mm · polistiren cu rășină",
         l1="Fațade care", l2="întorc toate privirile.",
         tip="Ancadramentele pun ferestrele în valoare și dau casei proporții de vilă clasică.",
         amb="amb-exterior.jpg", pos="45% 45%", img="na105f.jpg", price="130,96", unit="lei / bară 2 m",
         buy="Comandă ancadramentele pe", url="https://decoflair.ro/ancadrament-decorativ-na105"),
    dict(slug="10-coltar-ncl106", cat="Colțar exterior", name="NCL106", spec="250/250 × 30 × 1000 mm · rășină + cuarț",
         l1="Exterior de excepție,", l2="colț cu colț.",
         tip="Colțarii dau relief fațadei: seara, umbrele lor desenează arhitectura casei.",
         amb="amb-exterior.jpg", pos="92% 40%", img="ncl106.jpg", price="178,63", unit="lei / buc",
         buy="Comandă colțarii pe", url="https://decoflair.ro/coltar-exterior-decorativ-polistiren-ncl106-250-250x30x1000"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--gold:#D6BC84;--red:#B42127;--ink:#0b0a0c;--cream:#f5efe4;--mut:#b9b0a4}
html,body{width:1080px;height:1350px;background:var(--ink);font-family:Jost,sans-serif;color:#fff;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--ink)}
.amb{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.9) brightness(.85) contrast(1.06)}
.grade{position:absolute;inset:0;background:
 linear-gradient(180deg,rgba(11,10,12,.80) 0%,rgba(11,10,12,.10) 16%,rgba(11,10,12,0) 36%,rgba(11,10,12,.70) 56%,rgba(11,10,12,.97) 78%,var(--ink) 100%)}
.aura{position:absolute;left:-200px;right:-200px;bottom:-260px;height:760px;
 background:radial-gradient(ellipse at 30% 60%,rgba(180,33,39,.38),transparent 55%),radial-gradient(ellipse at 80% 70%,rgba(214,188,132,.22),transparent 55%);filter:blur(10px)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(214,188,132,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(214,188,132,.06) 1px,transparent 1px);background-size:90px 90px;
 -webkit-mask:linear-gradient(180deg,transparent 45%,#000 75%)}
.hud{position:absolute;inset:34px;pointer-events:none}
.hud i{position:absolute;width:42px;height:42px;border:0 solid var(--gold)}
.hud i:nth-child(1){left:0;top:0;border-left-width:2px;border-top-width:2px}
.hud i:nth-child(2){right:0;top:0;border-right-width:2px;border-top-width:2px}
.hud i:nth-child(3){left:0;bottom:0;border-left-width:2px;border-bottom-width:2px}
.hud i:nth-child(4){right:0;bottom:0;border-right-width:2px;border-bottom-width:2px}
.top{position:absolute;left:70px;right:70px;top:66px;display:flex;justify-content:space-between;align-items:center}
.logo{width:200px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.6))}
.mono{font-family:'Space Mono',monospace;font-size:17px;letter-spacing:3px;text-transform:uppercase;color:var(--gold)}
.top .mono{text-align:right;line-height:1.6}
.top .mono span{color:rgba(255,255,255,.7)}
.head{position:absolute;left:70px;right:70px;top:560px}
.l1{display:block;font-weight:300;font-size:50px;letter-spacing:4px;text-transform:uppercase;line-height:1.1;text-shadow:0 4px 24px rgba(0,0,0,.6)}
.l2{display:block;font-family:'Playfair Display',serif;font-style:italic;font-weight:600;font-size:76px;line-height:1.05;color:var(--gold);margin-top:6px;text-shadow:0 4px 30px rgba(0,0,0,.6)}
.tip{position:absolute;left:70px;right:70px;top:790px;display:flex;gap:18px;align-items:flex-start}
.tip b{flex:none;font-family:'Space Mono',monospace;font-weight:700;font-size:15px;letter-spacing:3px;background:var(--red);padding:9px 12px 7px;border-radius:3px;margin-top:4px}
.tip span{font-weight:300;font-size:27px;line-height:1.4;color:rgba(255,255,255,.92)}
.glass{position:absolute;left:70px;right:70px;top:940px;height:300px;display:flex;gap:30px;align-items:center;padding:26px;
 background:linear-gradient(135deg,rgba(255,255,255,.10),rgba(255,255,255,.03));border:1px solid rgba(214,188,132,.45);border-radius:22px;
 backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);box-shadow:0 30px 80px rgba(0,0,0,.55)}
.glass .ph{flex:none;width:248px;height:248px;border-radius:14px;overflow:hidden;background:var(--cream);box-shadow:0 0 0 1px rgba(214,188,132,.6)}
.glass .ph img{width:100%;height:100%;object-fit:cover}
.glass .tx{flex:1;min-width:0}
.name{font-weight:600;font-size:46px;line-height:1.05;margin-top:8px}
.spec{font-size:21px;color:var(--mut);margin-top:8px;font-weight:300}
.price{display:flex;align-items:baseline;gap:12px;margin-top:16px}
.price b{font-weight:600;font-size:64px;color:var(--gold);letter-spacing:-1px;line-height:1}
.price span{font-size:21px;color:#fff;font-weight:300}
.buy{position:absolute;left:70px;right:70px;bottom:58px;display:flex;align-items:center;justify-content:space-between}
.buy .t{font-weight:300;font-size:26px;letter-spacing:1px}
.buy .t b{font-family:'Playfair Display',serif;font-weight:600;font-size:40px;color:var(--cream);margin-left:10px;letter-spacing:.5px}
.buy .line{flex:1;height:1px;margin-left:28px;background:linear-gradient(90deg,var(--gold),transparent);position:relative}
/* ---- Story 1080x1920 ---- */
body.story,.story .c{height:1920px}
.story .top{top:220px}
.story .grade{background:linear-gradient(180deg,rgba(11,10,12,.85) 0%,rgba(11,10,12,.55) 14%,rgba(11,10,12,0) 30%,rgba(11,10,12,.65) 48%,rgba(11,10,12,.97) 68%,var(--ink) 100%)}
.story .head{top:880px}
.story .tip{top:1120px}
.story .glass{top:1270px}
.story .buy{bottom:290px}
.story .hud{top:180px;bottom:220px}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;600&family=Playfair+Display:ital,wght@1,600'
        '&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')


def scene(p, i):
    return f"""<img class="amb" src="assets/{p['amb']}" style="object-position:{p['pos']}" alt="">
<div class="grade"></div><div class="aura"></div><div class="grid"></div><div class="hud"><i></i><i></i><i></i><i></i></div>
<div class="top"><img class="logo" src="assets/logo-decoflair.png" alt="Deco&amp;Flair"><div class="mono">Know-how {i:02d}/10<br><span>Holiday Edition</span></div></div>
<div class="head"><span class="l1">{p['l1']}</span><span class="l2">{p['l2']}</span></div>
<div class="tip"><b>KNOW-HOW</b><span>{p['tip']}</span></div>
<div class="glass"><div class="ph"><img src="assets/{p['img']}" alt=""></div><div class="tx">
 <div class="mono">{p['cat']}</div><div class="name">{p['name']}</div><div class="spec">{p['spec']}</div>
 <div class="price"><b>{p['price']}</b><span>{p['unit']}</span></div></div></div>
<div class="buy"><div class="t">{p['buy']}<b>decoflair.ro</b></div><div class="line"></div></div>"""


def page(p, i, story=False):
    t = f"Deco&Flair — {p['cat']} {p['name']}" + (" — Story" if story else "")
    cls = ' class="story"' if story else ''
    return HEAD.replace('{t}', t) + f'<body{cls}><div class="c">' + scene(p, i) + '</div></body></html>'


for i, p in enumerate(P, 1):
    (ROOT / f"{p['slug']}.html").write_text(page(p, i))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, i, True).replace('src="assets/', 'src="../assets/'))
(ROOT / "products.json").write_text(json.dumps({"pricesCheckedAt": "2026-11-15", "source": "https://decoflair.ro/", "products": P},
                                               ensure_ascii=False, indent=1))
print("ok", len(P))

"""Deco&Flair — „Idei 2027”: 1 manifest + 10 idei de amenajare cu produse premium, FĂRĂ prețuri.
Mesaj: pe decoflair.ro nu cumperi doar un produs — cumperi selecție atentă, know-how, frumos, imaginea casei tale.
Aspect 2027: alternanță lumină (crem) / întuneric (onix), ambient în arcadă arhitecturală, produs în medalion,
etichete monospace, text vertical, aură vișinie. Feed 1080x1350 + Story 1080x1920.
Rulare: python3 build.py && node render.cjs
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

P = [
    dict(slug="01-tapet-carrara-82603", theme="light", room="Living", cat="Tapet premium", name="Carrara Best 82603",
         h="Pereți pe care<br><i>îi fotografiază musafirii.</i>",
         idea="Un singur perete accent cu tapet efect marmură — și camera arată ca un lounge de hotel de lux.",
         amb="t03b.jpg", pos="50% 45%", img="t03.jpg"),
    dict(slug="02-tapet-carrara-82671", theme="dark", room="Dormitor", cat="Tapet premium", name="Carrara Best 82671",
         h="Dormitorul care arată<br><i>ca în reviste.</i>",
         idea="Tapetul din spatele patului devine tăblie, artă și punct focal. Fără renovare, fără praf.",
         amb="t71b.jpg", pos="50% 45%", img="t71.jpg"),
    dict(slug="03-scafa-led-l5", theme="light", room="Tavan", cat="Scafă LED · Arstyl", name="L5",
         h="Lumina care face<br><i>tavanul să plutească.</i>",
         idea="Scafa ascunde banda LED: camera pare mai înaltă, iar seara devine o scenă.",
         amb="amb-led.jpg", pos="60% 30%", img="l5a.jpg"),
    dict(slug="04-cornisa-z11", theme="dark", room="Salon", cat="Cornișă ornamentală · Arstyl", name="Z11",
         h="„Vai, ce casă<br><i>frumoasă aveți!”</i>",
         idea="Cornișa ornamentată e primul detaliu pe care îl observă musafirii. Se montează lipit, fără praf.",
         amb="amb-interior.jpg", pos="45% 20%", img="z11a.jpg"),
    dict(slug="05-cornisa-z21", theme="light", room="Sufragerie", cat="Cornișă de tavan · Arstyl", name="Z21",
         h="Tavane de film,<br><i>înainte de sărbători.</i>",
         idea="La tavanele înalte alege o cornișă generoasă: proporția face diferența dintre simplu și spectaculos.",
         amb="amb-led-window.jpg", pos="50% 30%", img="z21a.jpg"),
    dict(slug="06-brau-chenare-wo2", theme="dark", room="Pereți", cat="Brâu pentru chenare · Wallstyl", name="WO2",
         h="Boiserie de palat,<br><i>la buget de apartament.</i>",
         idea="Chenarele din brâu transformă orice perete plat într-unul de lux. Arată scump, costă puțin.",
         amb="amb-chenare.jpg", pos="40% 40%", img="wo2a.jpg"),
    dict(slug="07-plinta-fd3", theme="light", room="Pardoseală", cat="Plintă decorativă · Wallstyl", name="FD3",
         h="Luxul<br><i>începe de jos.</i>",
         idea="O plintă înaltă și albă face pardoseala să pară mai scumpă și ascunde elegant cablurile.",
         amb="amb-led-floor.jpg", pos="40% 70%", img="fd3a.jpg"),
    dict(slug="08-cornisa-wt25", theme="dark", room="Interior modern", cat="Cornișă modernă · Wallstyl", name="WT25",
         h="Minimalism care<br><i>nu trece neobservat.</i>",
         idea="Profilul simplu al cornișei păstrează liniile curate ale unui interior contemporan.",
         amb="amb-tapet.jpg", pos="50% 30%", img="wt25a.jpg"),
    dict(slug="09-ancadrament-na105", theme="light", room="Fațadă", cat="Ancadrament fereastră · exterior", name="NA105",
         h="Prima impresie<br><i>începe din stradă.</i>",
         idea="Ancadramentele dau ferestrelor proporții de vilă clasică. Fațada devine carte de vizită.",
         amb="amb-exterior.jpg", pos="45% 45%", img="na105f.jpg"),
    dict(slug="10-coltar-ncl106", theme="dark", room="Fațadă", cat="Colțar exterior", name="NCL106",
         h="Înăuntru premium.<br><i>Pe afară, la fel.</i>",
         idea="Colțarii dau relief fațadei: seara, umbrele lor desenează arhitectura casei.",
         amb="amb-exterior.jpg", pos="92% 40%", img="ncl106.jpg"),
]

PROOF = "Selecție atentă din mulți furnizori · Idei + produse · Soluții pentru orice buget"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--gold:#C9A869;--gold2:#D6BC84;--red:#9E1F2A;--onyx:#121115;--cream:#F3EDE3;--ink:#1d1a1a}
html,body{width:1080px;height:1350px;font-family:Jost,sans-serif;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;overflow:hidden}
.light .c{background:var(--cream);color:var(--ink)}
.dark .c{background:var(--onyx);color:var(--cream)}
.aura{position:absolute;width:900px;height:900px;right:-380px;top:-380px;border-radius:50%;
 background:radial-gradient(circle,rgba(158,31,42,.35),transparent 65%)}
.light .aura{background:radial-gradient(circle,rgba(201,168,105,.45),transparent 65%)}
.grain{position:absolute;inset:0;opacity:.06;background-image:radial-gradient(#000 1px,transparent 1px);background-size:4px 4px}
.top{position:absolute;left:70px;right:70px;top:54px;display:flex;justify-content:space-between;align-items:center;z-index:3}
.logo{width:190px}
.light .logo{filter:brightness(.82) contrast(1.15)}
.mono{font-family:'Space Mono',monospace;font-size:17px;letter-spacing:3px;text-transform:uppercase}
.top .mono{text-align:right;line-height:1.6}
.top .mono b{color:var(--red)}
.dark .top .mono b{color:var(--gold2)}
.arch{position:absolute;left:150px;right:70px;top:150px;height:690px;border-radius:430px 430px 26px 26px;overflow:hidden;
 box-shadow:0 30px 80px rgba(0,0,0,.25)}
.dark .arch{box-shadow:0 0 0 1px rgba(214,188,132,.4),0 30px 90px rgba(0,0,0,.6)}
.arch img{width:100%;height:100%;object-fit:cover}
.arch::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 60%,rgba(0,0,0,.25))}
.side{position:absolute;left:84px;top:160px;height:680px;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:space-between}
.side .mono{font-size:15px;letter-spacing:5px;opacity:.75}
.side i{display:block;width:1px;flex:1;margin:18px 0;background:currentColor;opacity:.3}
.room{position:absolute;left:190px;top:770px;z-index:2;background:rgba(255,255,255,.88);color:var(--ink);padding:10px 18px 8px;border-radius:30px}
.dark .room{background:rgba(18,17,21,.82);color:var(--gold2)}
.medal{position:absolute;right:96px;top:700px;width:250px;height:250px;border-radius:50%;overflow:hidden;z-index:2;background:#fff;
 box-shadow:0 0 0 3px var(--gold),0 0 0 14px rgba(201,168,105,.18),0 24px 60px rgba(0,0,0,.35)}
.medal img{width:100%;height:100%;object-fit:cover}
.h{position:absolute;left:70px;right:340px;top:872px;font-family:'Playfair Display',serif;font-weight:500;font-size:54px;line-height:1.06}
.h i{color:var(--red);font-weight:600}
.dark .h i{color:var(--gold2)}
.prod{position:absolute;right:70px;top:970px;width:270px;text-align:center}
.prod .mono{font-size:14px;letter-spacing:2px;opacity:.75}
.prod b{display:block;font-weight:600;font-size:30px;margin-top:6px;line-height:1.1}
.idea{position:absolute;left:70px;right:70px;top:1090px;display:flex;gap:18px;align-items:flex-start}
.idea .mono{flex:none;font-size:14px;font-weight:700;letter-spacing:2.5px;padding:8px 12px 6px;border:1.5px solid currentColor;border-radius:4px;margin-top:5px}
.idea span{font-weight:300;font-size:27px;line-height:1.4}
.foot{position:absolute;left:70px;right:70px;bottom:44px;border-top:1px solid rgba(128,110,80,.45);padding-top:18px;display:flex;justify-content:space-between;align-items:center}
.foot .go{font-weight:300;font-size:24px}
.foot .go b{font-family:'Playfair Display',serif;font-weight:600;font-size:36px;margin-left:8px}
.foot .go em{font-style:normal;color:var(--red);margin-left:10px;font-size:30px}
.dark .foot .go em{color:var(--gold2)}
.foot .sale{font-family:'Space Mono',monospace;font-size:15px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;background:var(--red);color:#fff;padding:10px 16px 8px;border-radius:30px}
.proof{position:absolute;left:70px;right:70px;bottom:118px;font-family:'Space Mono',monospace;font-size:14px;letter-spacing:1.6px;text-transform:uppercase;opacity:.7}
/* manifest */
.man .arches{position:absolute;left:70px;right:70px;top:150px;height:560px;display:flex;gap:28px}
.man .arches div{flex:1;border-radius:300px 300px 22px 22px;overflow:hidden;position:relative}
.man .arches img{width:100%;height:100%;object-fit:cover}
.man .arches span{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);white-space:nowrap}
.man .q{position:absolute;left:70px;right:70px;top:760px;font-family:'Playfair Display',serif;font-size:40px;font-style:italic;opacity:.6;text-decoration:line-through;text-decoration-color:var(--red);text-decoration-thickness:3px}
.man .h{top:815px;right:70px;font-size:56px}
.man .idea{top:1060px}
/* ---- Story 1080x1920 ---- */
body.story,.story .c{height:1920px}
.story .top{top:210px}
.story .arch{top:320px;height:860px}
.story .side{top:330px;height:850px}
.story .room{top:1110px}
.story .medal{top:1040px}
.story .h{top:1230px}
.story .prod{top:1310px}
.story .idea{top:1420px}
.story .proof{bottom:360px}
.story .foot{bottom:290px}
.story.man .arches{top:320px;height:760px}
.story.man .q{top:1110px}.story.man .h{top:1180px}.story.man .idea{top:1420px}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;600&family=Playfair+Display:ital,wght@0,500;1,500;1,600'
        '&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')

FOOT = ('<div class="proof">' + PROOF + '</div>'
        '<div class="foot"><div class="go">Vezi ideea completă pe<b>decoflair.ro</b><em>→</em></div><div class="sale">Reduceri de sezon</div></div>')


def scene(p, i):
    return f"""<div class="aura"></div><div class="grain"></div>
<div class="top"><img class="logo" src="assets/logo-decoflair.png" alt="Deco&amp;Flair"><div class="mono">Ideea <b>{i:02d}</b>/10<br>Holiday 2026</div></div>
<div class="side"><span class="mono">Ales cu grijă</span><i></i><span class="mono">Know-how</span><i></i><span class="mono">decoflair.ro</span></div>
<div class="arch"><img src="assets/{p['amb']}" style="object-position:{p['pos']}" alt=""></div>
<div class="room mono">{p['room']}</div>
<div class="medal"><img src="assets/{p['img']}" alt=""></div>
<div class="h">{p['h']}</div>
<div class="prod"><div class="mono">{p['cat']}</div><b>{p['name']}</b></div>
<div class="idea"><span class="mono">Ideea noastră</span><span>{p['idea']}</span></div>
""" + FOOT


def manifest():
    return """<div class="aura"></div><div class="grain"></div>
<div class="top"><img class="logo" src="assets/logo-decoflair.png" alt="Deco&amp;Flair"><div class="mono">Manifest<br>Holiday 2026</div></div>
<div class="arches"><div><img src="assets/amb-exterior.jpg" style="object-position:45% 45%" alt=""><span class="room mono" style="position:absolute;left:50%;top:auto">Pe afară</span></div>
<div><img src="assets/amb-interior.jpg" style="object-position:45% 30%" alt=""><span class="room mono" style="position:absolute;left:50%;top:auto">Înăuntru</span></div></div>
<div class="q">„Pe afară vopsit gardul, înăuntru leopardul.”</div>
<div class="h">La noi e invers:<br><i>fațade impecabile, interioare premium.</i></div>
<div class="idea"><span class="mono">Promisiunea</span><span>Nu ai idei de amenajare? Avem noi — și idei, și produsele potrivite. Pentru orice buget.</span></div>
""" + FOOT


def page(body, t, theme, story=False, extra=""):
    cls = f"{theme}{' story' if story else ''}{extra}"
    return HEAD.replace('{t}', t) + f'<body class="{cls}"><div class="c">' + body + '</div></body></html>'


def story_fix(html):
    return html.replace('src="assets/', 'src="../assets/')


(ROOT / "00-manifest.html").write_text(page(manifest(), "Deco&Flair — Manifest", "light", extra=" man"))
(ROOT / "story" / "00-manifest-story.html").write_text(story_fix(page(manifest(), "Deco&Flair — Manifest — Story", "light", True, " man")))
for i, p in enumerate(P, 1):
    t = f"Deco&Flair — Ideea {i:02d}: {p['cat']} {p['name']}"
    (ROOT / f"{p['slug']}.html").write_text(page(scene(p, i), t, p['theme']))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(story_fix(page(scene(p, i), t + " — Story", p['theme'], True)))
(ROOT / "products.json").write_text(json.dumps({"createdAt": "2026-11-15", "prices": "fără prețuri (la cererea clientului)", "products": P},
                                               ensure_ascii=False, indent=1))
print("ok", len(P) + 1)

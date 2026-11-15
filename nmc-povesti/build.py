"""NMC — 5 creative separate „Povești de casă”: nevoia clientului → produsul ca răspuns → nmcromania.ro.
Ambient pe tot ecranul cu tentă misterioasă (albastru-noapte / violet), produsul într-o „lupă” rotundă, fără preț.
Feed 1080x1350 + Story 1080x1920. Rulare: python3 build.py && node render.cjs
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

PRODUCTS = [
    dict(slug="01-atmosfera-plinta-led-il11", chapter="Atmosferă", n="01",
         need="Vrei ca serile acasă<br>să fie mai liniștite?",
         answer="Plinta <b>IL11</b> ascunde o bandă LED și desenează o linie de lumină caldă la nivelul podelei. Fără lustre, fără umbre dure.",
         ambient="il11amb.jpg", amb_pos="12% 60%", lens="sec-il11.png", lens_fit="contain", lens_bg="#fff",
         label="IL11 · Plintă cu iluminat LED", tone="teal", bright=1.35),
    dict(slug="02-ordine-scafa-led-l2", chapter="Ordine", n="02",
         need="Cabluri, țevi, tubulaturi?<br>Tavanul le poate ascunde.",
         answer="Scafa <b>L2</b> acoperă ce nu vrei să vezi și găzduiește spoturi sau bandă LED. În cameră rămâne doar lumina.",
         ambient="l2a.jpg", amb_pos="50% 50%", lens="sec-l2b.png", lens_fit="contain", lens_bg="#fff",
         label="L2 · Scafă LED pentru tavan", tone="violet", bright=1.05),
    dict(slug="03-eleganta-cornisa-z11", chapter="Eleganță", n="03",
         need="Un tavan simplu<br>poate spune o poveste.",
         answer="Cornișa <b>Z11</b>, cu motiv floral clasic, transformă îmbinarea dintre perete și tavan într-un detaliu care se privește.",
         ambient="ambient-interior.jpg", amb_pos="55% 30%", lens="z11a.jpg", lens_fit="cover", lens_bg="#ddd",
         label="Z11 · Cornișă decorativă", tone="plum"),
    dict(slug="04-prima-impresie-ancadrament-na105", chapter="Prima impresie", n="04",
         need="Casa ta e prima poveste<br>pe care o vede strada.",
         answer="Ancadramentele <b>NA105</b> conturează ferestrele cu linii clasice și dau fațadei proporție. Rezistente la UV, ger și umezeală.",
         ambient="ambient-vila.jpg", amb_pos="50% 25%", lens="na105f.jpg", lens_fit="cover", lens_bg="#fff",
         label="NA105 · Ancadrament fereastră", tone="night"),
    dict(slug="05-caracter-coltar-ncl113", chapter="Caracter", n="05",
         need="Când se aprind luminile,<br>fiecare colț contează.",
         answer="Colțarul <b>NCL113</b> dă fațadei relief și umbre adânci. Strat de rășină și nisip cuarțos, gata de vopsit în orice culoare.",
         ambient="ambient-casa.jpg", amb_pos="62% 50%", lens="ncl113.png", lens_fit="contain", lens_bg="radial-gradient(circle at 50% 40%,#3a3550,#11131c)",
         label="NCL113 · Colțar exterior", tone="violet"),
]

TONES = {  # tentă misterioasă peste ambient
    "teal":   "linear-gradient(160deg,rgba(10,40,52,.55),rgba(16,14,40,.35))",
    "violet": "linear-gradient(160deg,rgba(43,26,78,.55),rgba(10,22,40,.35))",
    "plum":   "linear-gradient(160deg,rgba(60,18,48,.45),rgba(14,16,36,.40))",
    "night":  "linear-gradient(160deg,rgba(12,22,58,.60),rgba(36,20,60,.35))",
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;background:#0c0f18;font-family:Roboto,sans-serif;color:#fff;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:#0c0f18;overflow:hidden}
.amb{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.8) brightness(.78) contrast(1.05)}
.tone{position:absolute;inset:0;mix-blend-mode:multiply}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse at 78% 18%,rgba(255,140,60,.18),transparent 45%)}
.vig{position:absolute;inset:0;background:
 linear-gradient(180deg,rgba(8,10,18,.75) 0%,rgba(8,10,18,0) 18%,rgba(8,10,18,0) 40%,rgba(8,10,18,.82) 70%,rgba(8,10,18,.96) 100%),
 radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(5,6,12,.55) 100%)}
.top{position:absolute;left:64px;right:64px;top:56px;display:flex;justify-content:space-between;align-items:center}
.logo{width:112px;border-radius:8px}
.chap{display:flex;align-items:center;gap:16px;font-weight:300;font-size:22px;letter-spacing:6px;text-transform:uppercase;color:rgba(255,255,255,.85)}
.chap b{font-weight:700;color:#FF671F;letter-spacing:2px}
.chap i{display:block;width:60px;height:1px;background:rgba(255,255,255,.5)}
.story-txt{position:absolute;left:64px;right:64px;top:760px}
.need{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:74px;line-height:1.02;letter-spacing:-.5px;text-shadow:0 4px 30px rgba(0,0,0,.6)}
.answer{margin-top:28px;max-width:560px;font-weight:300;font-size:29px;line-height:1.42;color:rgba(255,255,255,.9)}
.answer b{font-weight:700;color:#fff}
.lens{position:absolute;right:64px;top:930px;width:300px;height:300px;border-radius:50%;overflow:hidden;
 box-shadow:0 0 0 2px rgba(255,103,31,.95),0 0 0 14px rgba(255,255,255,.08),0 30px 80px rgba(0,0,0,.7)}
.lens img{width:100%;height:100%;display:block}
.lab{position:absolute;right:34px;top:1250px;width:360px;text-align:center;font-size:18px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,.75);font-weight:500}
.cta{position:absolute;left:64px;bottom:62px;display:flex;align-items:center;gap:22px}
.cta span{font-weight:300;font-size:22px;letter-spacing:4px;text-transform:uppercase;color:rgba(255,255,255,.8)}
.cta b{font-weight:700;font-size:38px;letter-spacing:.5px}
.cta i{display:block;width:90px;height:2px;background:#FF671F;position:relative}
.cta i::after{content:"";position:absolute;right:-2px;top:-6px;width:12px;height:12px;border-top:2px solid #FF671F;border-right:2px solid #FF671F;transform:rotate(45deg)}
/* ---- Story 1080x1920 ---- */
body.story,.story .c{height:1920px}
.story .top{top:210px}
.story .story-txt{top:1150px}
.story .need{font-size:80px}
.story .lens{top:760px;right:64px;width:330px;height:330px}
.story .lab{top:1110px;width:330px}
.story .cta{bottom:290px}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900'
        '&family=Cormorant+Garamond:ital,wght@1,500;1,600&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')


def scene(p):
    return f"""<img class="amb" src="assets/{p['ambient']}" style="object-position:{p['amb_pos']};filter:saturate(.85) brightness({p.get('bright',.8)}) contrast(1.05)" alt="">
<div class="tone" style="background:{TONES[p['tone']]}"></div><div class="glow"></div><div class="vig"></div>
<div class="top"><img class="logo" src="assets/nmc-logo.png" alt="nmc"><div class="chap"><b>{p['n']}</b><i></i>{p['chapter']}</div></div>
<div class="lens" style="background:{p['lens_bg']}"><img src="assets/{p['lens']}" style="object-fit:{p['lens_fit']}" alt=""></div>
<div class="lab">{p['label']}</div>
<div class="story-txt"><div class="need">{p['need']}</div><div class="answer">{p['answer']}</div></div>
<div class="cta"><span>Descoperă pe</span><b>nmcromania.ro</b><i></i></div>"""


def page(p, story=False):
    t = f"NMC — {p['chapter']}: {p['label']}" + (" — Story" if story else "")
    cls = ' class="story"' if story else ''
    return HEAD.replace('{t}', t) + f'<body{cls}><div class="c">' + scene(p) + '</div></body></html>'


for p in PRODUCTS:
    (ROOT / f"{p['slug']}.html").write_text(page(p))
    (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, True).replace('src="assets/', 'src="../assets/'))
(ROOT / "products.json").write_text(json.dumps({"createdAt": "2026-11-15", "products": PRODUCTS}, ensure_ascii=False, indent=1))
print("ok", len(PRODUCTS))

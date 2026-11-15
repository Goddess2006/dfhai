"""Deco&Flair „Trend 2027 · Tokyo × Singapore” — 8 creative cu produse de nișă, cu forme spectaculoase.
Structură: PROBLEMA → SOLUȚIA (produsul) → REZULTATUL. Fără prețuri. Imagini vii (ambient pe produs),
estetică japoneză/singaporeză: hârtie washi, cerneală, jad, sigiliu hanko, text vertical, cerc ensō, kanji.
Feed 1080x1350 + Story 1080x1920. Rulare: python3 build.py && node render.cjs
Afirmații tehnice luate din fișele de pe decoflair.ro (15.11.2026); toate produsele InStock.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

P = [
    dict(slug="01-riflaj-acustic-stejar", kanji="静", jp="liniște", accent="#8a6a3f", name="Riflaj acustic 3D", var="stejar deschis",
         q="Livingul tău sună<br>a sală goală?", a="Liniștea are o formă nouă.",
         prob="Ecou, voci care răsună, pereți reci.",
         sol="Panouri riflaj acustic de doar 3,1 kg, montaj fără scule speciale.",
         res="Acustică mai bună cu până la 25% și un perete cald, japandi.",
         amb="riflaj-amb.jpg", pos="50% 50%", img="riflaj.jpg", url="https://decoflair.ro/riflaj-acustic-panou-3d-stejar-deschis"),
    dict(slug="02-panou-3d-canele-l", kanji="線", jp="linie", accent="#3f6b55", name="Panou 3D CANELÉ L", var="design Bertrand Lejoly",
         q="Un perete plat,<br>fără personalitate?", a="Dă-i ritm.",
         prob="Pereți goi care nu spun nimic despre tine.",
         sol="Caneluri sculptate, semnate de designerul belgian Bertrand Lejoly. 30 cm × 2 m.",
         res="Linii verticale care înalță camera. Se vopsește în orice culoare.",
         amb="canele-amb.jpg", pos="55% 50%", img="canele.jpg", url="https://decoflair.ro/panou-decorativ-canelel"),
    dict(slug="03-panou-3d-wave", kanji="波", jp="val", accent="#5d7c8c", name="Panou 3D WAVE", var="Wallstyl · alb mat",
         q="Dormitorul tău arată<br>ca toate celelalte?", a="Fă-l să curgă.",
         prob="Un perete de pat banal, uitat după montaj.",
         sol="Valuri sculptate în relief, preamorsate, gata de vopsit.",
         res="Lumina laterală desenează umbre vii, de dimineața până seara.",
         amb="wave-amb.jpg", pos="50% 50%", img="wave.jpg", url="https://decoflair.ro/panou-decorativ-3d-wave"),
    dict(slug="04-panou-3d-wing", kanji="翼", jp="aripă", accent="#1f6b4a", name="Panou 3D WING", var="Arstyl · 175 × 250 mm",
         q="Vrei culoare,<br>dar fără tapet?", a="Dă-i aripi peretelui.",
         prob="Vopseaua singură arată plat și previzibil.",
         sol="Module mici WING, din poliuretan, combinate liber pe perete.",
         res="Un perete-sculptură, în culoarea ta preferată.",
         amb="wing-amb.jpg", pos="50% 50%", img="wing.jpg", url="https://decoflair.ro/panou-decorativ3d-wing-arstyl"),
    dict(slug="05-panou-3d-ray", kanji="光", jp="lumină", accent="#1f4f7a", name="Panou 3D RAY", var="Arstyl · 320 × 550 mm",
         q="Un dining care<br>nu impresionează?", a="Lasă lumina să lucreze.",
         prob="Masa e frumoasă. Peretele din spate, nu.",
         sol="Romburi cu raze în relief, care prind lumina din fiecare unghi.",
         res="Un fundal de restaurant de lux, la tine acasă.",
         amb="ray-amb.jpg", pos="50% 50%", img="ray.jpg", url="https://decoflair.ro/panou-decorativ-3d-ray-arstyl"),
    dict(slug="06-panou-3d-icon", kanji="形", jp="formă", accent="#b8862a", name="Panou 3D ICON", var="Wallstyl · forme rotunjite",
         q="Biroul de acasă<br>arată a birou?", a="Fă-l iconic.",
         prob="Un colț de lucru fără inspirație, care se vede în fiecare call.",
         sol="Forme rotunjite, retro-futuriste, preamorsate pentru orice culoare.",
         res="Un fundal la care toți te vor întreba: „Unde l-ai găsit?”",
         amb="icon-amb.jpg", pos="50% 30%", img="icon.jpg", url="https://decoflair.ro/panou-decorativ-3d-icon"),
    dict(slug="07-panou-puzzle-3d", kanji="遊", jp="joc", accent="#b5603a", name="Panou PUZZLE 3D", var="380 × 380 mm · poliuretan",
         q="Același perete,<br>de ani de zile?", a="Joacă-te cu umbrele.",
         prob="Pereți monotoni, pe care nu-i mai vezi.",
         sol="Piese 3D pe care le rotești ca să compui modele diferite.",
         res="Un perete unic, care nu seamănă cu al nimănui.",
         amb="puzzle-amb.jpg", pos="60% 45%", img="puzzle.jpg", url="https://decoflair.ro/panou-decorativ-3d-interior-poliuretan-puzzle-3d"),
    dict(slug="08-cornisa-led-il18", kanji="灯", jp="lumină caldă", accent="#9c7a45", name="Cornișă LED IL18", var="Wallstyl · 121 × 90 mm",
         q="Șina de perdea<br>se vede urât?", a="Ascunde-o în lumină.",
         prob="Șine la vedere și lumină rece de plafon.",
         sol="IL18 maschează șina de perdea și are spațiu pentru banda LED.",
         res="Draperii scăldate în lumină caldă, ca într-un hotel boutique.",
         amb="il18-amb.jpg", pos="50% 40%", img="il18.jpg", url="https://decoflair.ro/cornisa-led-il18-121x90x2000"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--washi:#F4F1EA;--ink:#1B1B1F;--mut:#6d675f;--hanko:#C8392B;--gold:#C9A869}
html,body{width:1080px;height:1350px;font-family:Jost,sans-serif;overflow:hidden;background:var(--washi);color:var(--ink)}
.c{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--washi)}
.fiber{position:absolute;inset:0;opacity:.35;background:
 repeating-linear-gradient(17deg,rgba(120,100,70,.05) 0 2px,transparent 2px 9px),repeating-linear-gradient(-23deg,rgba(120,100,70,.04) 0 1px,transparent 1px 13px)}
.photo{position:absolute;left:0;right:0;top:0;height:790px;overflow:hidden}
.photo img{width:100%;height:100%;object-fit:cover;filter:saturate(1.12) contrast(1.04)}
.photo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.28) 0%,transparent 22%,transparent 80%,rgba(244,241,234,.25) 100%)}
.grid{position:absolute;inset:0;pointer-events:none;background:
 linear-gradient(90deg,transparent 64px,rgba(27,27,31,.10) 64px 65px,transparent 65px calc(100% - 65px),rgba(27,27,31,.10) calc(100% - 65px) calc(100% - 64px),transparent calc(100% - 64px))}
.top{position:absolute;left:64px;right:64px;top:48px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.chip{background:rgba(244,241,234,.92);border-radius:40px;padding:12px 22px;display:flex;align-items:center;gap:14px;box-shadow:0 8px 24px rgba(0,0,0,.18)}
.chip img{width:150px;filter:brightness(.8) contrast(1.2)}
.mono{font-family:'Space Mono',monospace;font-size:16px;letter-spacing:3px;text-transform:uppercase}
.tag{background:var(--ink);color:var(--washi);border-radius:40px;padding:12px 20px 10px}
.tag b{color:var(--gold)}
.tate{position:absolute;right:64px;top:150px;z-index:4;display:flex;flex-direction:column;align-items:center;gap:16px;
 background:rgba(244,241,234,.9);padding:22px 14px;border-radius:40px;box-shadow:0 8px 24px rgba(0,0,0,.18)}
.tate .kj{font-family:'Noto Serif JP',serif;font-size:64px;line-height:1;color:var(--acc)}
.tate .v{writing-mode:vertical-rl;font-family:'Space Mono',monospace;font-size:15px;letter-spacing:6px;text-transform:uppercase}
.enso{position:absolute;right:70px;top:610px;width:300px;height:300px;z-index:6}
.enso .ring{position:absolute;inset:-18px}
.enso .pic{position:absolute;inset:18px;border-radius:50%;overflow:hidden;background:#fff;box-shadow:0 18px 50px rgba(0,0,0,.30)}
.enso .pic img{width:100%;height:100%;object-fit:cover}
.panel{position:absolute;left:64px;right:64px;top:820px}
.q{font-weight:300;font-size:56px;line-height:1.06;letter-spacing:-.5px;max-width:640px}
.a{font-family:'Playfair Display',serif;font-style:italic;font-weight:600;font-size:52px;color:var(--acc);margin-top:6px}
.steps{position:absolute;left:64px;right:64px;top:1060px;display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:18px}
.st{border-top:2px solid var(--ink);padding-top:12px}
.st.s2{border-top:4px solid var(--acc)}
.st .mono{font-size:13px;letter-spacing:2.5px;font-weight:700}
.st.s2 .mono{color:var(--acc)}
.st p{font-size:21px;line-height:1.35;margin-top:8px;font-weight:400}
.st.s2 p b{display:block;font-size:24px;font-weight:600;margin-bottom:2px}
.foot{position:absolute;left:64px;right:64px;bottom:40px;display:flex;align-items:center;gap:20px}
.hanko{width:62px;height:62px;flex:none;background:var(--hanko);color:#fff;border-radius:8px;display:flex;align-items:center;justify-content:center;
 font-family:'Playfair Display',serif;font-weight:600;font-size:22px;line-height:.9;text-align:center;transform:rotate(-4deg);box-shadow:inset 0 0 0 3px rgba(255,255,255,.35)}
.foot .go{font-size:24px;font-weight:300}
.foot .go b{font-family:'Playfair Display',serif;font-weight:600;font-size:34px;margin-left:6px}
.foot .sp{flex:1}
.foot .mono{font-size:13px;letter-spacing:2px;color:var(--mut);text-align:right;line-height:1.5}
/* story */
body.story,.story .c{height:1920px}
.story .photo{height:1080px}
.story .top{top:200px}
.story .tate{top:310px}
.story .enso{top:900px}
.story .panel{top:1110px}
.story .steps{top:1360px}
.story .foot{bottom:280px}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;600&family=Playfair+Display:ital,wght@0,600;1,600'
        '&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">'
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@600&text=%E9%9D%99%E7%B7%9A%E6%B3%A2%E7%BF%BC%E5%85%89%E5%BD%A2%E9%81%8A%E7%81%AF&display=swap" rel="stylesheet">'
        '<style>' + CSS + '</style></head>')

ENSO = ('<svg class="ring" viewBox="0 0 336 336"><circle cx="168" cy="168" r="158" fill="none" stroke="var(--ink)" stroke-width="7" '
        'stroke-linecap="round" stroke-dasharray="880 120" transform="rotate(-70 168 168)" opacity=".85"/>'
        '<circle cx="168" cy="168" r="150" fill="none" stroke="var(--acc)" stroke-width="2.5" stroke-dasharray="6 10" opacity=".9"/></svg>')


def scene(p, i):
    return f"""<div class="fiber"></div>
<div class="photo"><img src="assets/{p['amb']}" style="object-position:{p['pos']}" alt=""></div>
<div class="grid"></div>
<div class="top"><div class="chip"><img src="assets/logo-decoflair.png" alt="Deco&amp;Flair"></div><div class="tag mono">No.<b>{i:02d}</b> · Trend 2027</div></div>
<div class="tate"><span class="kj">{p['kanji']}</span><span class="v">{p['jp']}</span></div>
<div class="enso">{ENSO}<div class="pic"><img src="assets/{p['img']}" alt=""></div></div>
<div class="panel"><div class="q">{p['q']}</div><div class="a">{p['a']}</div></div>
<div class="steps">
 <div class="st"><div class="mono">01 · Problema</div><p>{p['prob']}</p></div>
 <div class="st s2"><div class="mono">02 · Soluția</div><p><b>{p['name']}</b>{p['sol']}</p></div>
 <div class="st"><div class="mono">03 · Rezultatul</div><p>{p['res']}</p></div>
</div>
<div class="foot"><div class="hanko">D<br>&amp;F</div><div class="go">Descoperă-l pe<b>decoflair.ro</b></div><div class="sp"></div>
<div class="mono">Ales cu grijă · Pentru orice buget<br>Reduceri de sezon</div></div>"""


def page(p, i, story=False):
    t = f"Deco&Flair Trend 2027 — {p['name']}" + (" — Story" if story else "")
    cls = ' class="story"' if story else ''
    return HEAD.replace('{t}', t) + f'<body{cls} style="--acc:{p["accent"]}"><div class="c">' + scene(p, i) + '</div></body></html>'


if __name__ == "__main__":
    for i, p in enumerate(P, 1):
        (ROOT / f"{p['slug']}.html").write_text(page(p, i))
        (ROOT / "story" / f"{p['slug']}-story.html").write_text(page(p, i, True).replace('src="assets/', 'src="../assets/'))
    (ROOT / "products.json").write_text(json.dumps({"createdAt": "2026-11-15", "prices": "fără", "products": P}, ensure_ascii=False, indent=1))
    print("ok", len(P))

"""Coperta „Ghidul de idei Deco&Flair” — feed 1080x1350 (00-coperta.html) + Story 1080x1920.
Folosită și ca deschidere animată în reel. Rulare: python3 cover.py && node render.cjs
"""
from pathlib import Path
import build

ROOT = Path(__file__).resolve().parent

COVER_CSS = """
.cv .c{background:radial-gradient(ellipse at 50% 42%,#fff8ea 0%,var(--cream) 45%,#e6dccb 100%);color:var(--ink)}
.cv .dust{position:absolute;inset:0;background-image:
 radial-gradient(circle at 18% 22%,rgba(201,168,105,.9) 0 2px,transparent 3px),radial-gradient(circle at 82% 30%,rgba(201,168,105,.8) 0 2px,transparent 3px),
 radial-gradient(circle at 12% 62%,rgba(201,168,105,.7) 0 1.5px,transparent 3px),radial-gradient(circle at 90% 70%,rgba(201,168,105,.8) 0 2px,transparent 3px),
 radial-gradient(circle at 70% 12%,rgba(201,168,105,.6) 0 1.5px,transparent 3px),radial-gradient(circle at 28% 84%,rgba(201,168,105,.6) 0 1.5px,transparent 3px)}
.cv .halo{position:absolute;left:50%;top:640px;width:1100px;height:1100px;transform:translate(-50%,-50%);border-radius:50%;
 background:radial-gradient(circle,rgba(214,188,132,.55),rgba(214,188,132,0) 60%)}
.cv .ring{position:absolute;left:50%;transform:translateX(-50%);border:1.5px solid rgba(201,168,105,.55);border-bottom:none}
.cv .r1{top:150px;width:700px;height:760px;border-radius:350px 350px 0 0}
.cv .r2{top:110px;width:800px;height:800px;border-radius:400px 400px 0 0;opacity:.6}
.cv .r3{top:70px;width:900px;height:840px;border-radius:450px 450px 0 0;opacity:.3}
.cv .door{position:absolute;left:50%;top:190px;width:620px;height:720px;transform:translateX(-50%);border-radius:310px 310px 18px 18px;overflow:hidden;
 box-shadow:0 0 0 3px var(--gold),0 40px 100px rgba(60,30,10,.35)}
.cv .door img{width:100%;height:100%;object-fit:cover;object-position:45% 30%}
.cv .door::after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 35%,rgba(255,220,160,.25),transparent 60%),linear-gradient(180deg,transparent 65%,rgba(0,0,0,.35))}
.cv .leaf{position:absolute;top:0;bottom:0;width:50%;background:linear-gradient(90deg,#1a1416,#2a1d1f);border:1px solid rgba(214,188,132,.5)}
.cv .leaf.l{left:0;transform-origin:left center}.cv .leaf.r{right:0;transform-origin:right center}
.cv .leaf i{position:absolute;top:50%;width:10px;height:70px;border-radius:5px;background:var(--gold)}
.cv .leaf.l i{right:24px}.cv .leaf.r i{left:24px}
.cv .pre{position:absolute;left:0;right:0;top:66px;text-align:center}
.cv .pre .logo{width:210px;filter:brightness(.82) contrast(1.15)}
.cv .ttl{position:absolute;left:0;right:0;top:935px;text-align:center}
.cv .ttl .mono{color:var(--red);font-weight:700}
.cv .ttl h1{font-family:'Playfair Display',serif;font-weight:500;font-size:112px;line-height:1;margin-top:12px;letter-spacing:-1px}
.cv .ttl h1 i{color:var(--red);font-weight:600}
.cv .ttl p{font-family:'Playfair Display',serif;font-style:italic;font-size:38px;margin-top:16px;color:#4a3c33}
.cv .chap{position:absolute;left:70px;right:70px;top:1185px;display:flex;justify-content:center;flex-wrap:wrap;gap:10px 14px}
.cv .chap span{font-family:'Space Mono',monospace;font-size:15px;letter-spacing:2px;text-transform:uppercase;border:1px solid rgba(29,26,26,.35);border-radius:30px;padding:8px 14px 6px}
.cv .bot{position:absolute;left:70px;right:70px;bottom:44px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(128,110,80,.45);padding-top:16px}
.cv .bot .mono{font-size:15px}
.cv .bot b{font-family:'Playfair Display',serif;font-weight:600;font-size:34px}
.cv .bot em{font-style:normal;color:var(--red)}
/* story */
.cv.story .pre{top:190px}
.cv.story .r1{top:370px;height:840px}.cv.story .r2{top:330px;height:880px}.cv.story .r3{top:290px;height:920px}
.cv.story .door{top:400px;height:800px}
.cv.story .halo{top:800px}
.cv.story .ttl{top:1235px}
.cv.story .chap{top:1530px}
.cv.story .bot{bottom:290px}
"""

CHAPTERS = ["Tapet", "Lumină", "Cornișe", "Chenare", "Plinte", "Fațade"]


def cover(doors_open=True):
    leaves = '' if doors_open else '<div class="leaf l"><i></i></div><div class="leaf r"><i></i></div>'
    chap = "".join(f"<span>{c}</span>" for c in CHAPTERS)
    return f"""<div class="halo"></div><div class="dust"></div>
<div class="ring r3"></div><div class="ring r2"></div><div class="ring r1"></div>
<div class="door"><img src="assets/amb-interior.jpg" alt="">{leaves}</div>
<div class="pre"><img class="logo" src="assets/logo-decoflair.png" alt="Deco&amp;Flair"><div class="mono" style="margin-top:6px">prezintă</div></div>
<div class="ttl"><div class="mono">Ediția de sărbători · 2026</div><h1>Ghidul <i>de idei</i></h1>
<p>10 idei pentru o casă care întoarce privirile</p></div>
<div class="chap">{chap}</div>
<div class="bot"><span class="mono">Ales cu grijă · Know-how · Pentru orice buget</span><span>Deschide ghidul pe <b>decoflair.ro</b> <em>→</em></span></div>"""


def page(story=False):
    css = build.CSS + COVER_CSS
    head = build.HEAD.replace(build.CSS, css).replace('{t}', 'Deco&Flair — Ghidul de idei — Coperta' + (' — Story' if story else ''))
    return head + f'<body class="cv{" story" if story else ""}"><div class="c">' + cover() + '</div></body></html>'


if __name__ == "__main__":
    (ROOT / "00-coperta.html").write_text(page())
    (ROOT / "story" / "00-coperta-story.html").write_text(page(True).replace('src="assets/', 'src="../assets/'))
    print("coperta ok")

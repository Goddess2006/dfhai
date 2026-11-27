"""Bannere „1 Decembrie” — program sărbători (30.11–1.12.2026) pentru decoflair.ro și nmcromania.ro.
Mesaj: nu procesăm comenzi pe 30 noiembrie și 1 decembrie; comenzile plasate atunci se procesează începând cu 3 decembrie 2026.
Urare de Ziua Națională. Două stiluri diferite, în tonul fiecărui site:
  Deco&Flair: cald, elegant (auriu pe cărbune, sigla aripii, Cormorant italic, interior cald)
  NMC: direct, clar (noapte / ivoire / verde pădure din landing-ul NMC, Inter + Cormorant, fațadă)
Rulare: python3 build.py && node render.cjs  → out/*.jpg
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)
R = "../../"  # din out/ către rădăcina repo-ului

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700&display=block" rel="stylesheet">'

# ---------------------------------------------------------------- Deco&Flair
DF_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--gold:#C2A15E;--gold2:#E2CB94;--ink:#141210;--ivory:#F6F0E4}
body{width:%(w)spx;height:%(h)spx;overflow:hidden;background:#0c0a08;color:var(--ivory);font-family:Manrope,sans-serif;position:relative}
.ph{position:absolute;background:url(%(img)s) center/cover no-repeat}
.fade{position:absolute;inset:0}
.logo{display:block}
.k{font-size:%(k)spx;letter-spacing:.32em;text-transform:uppercase;color:var(--gold2);font-weight:600;display:flex;align-items:center;gap:14px}
.h{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;line-height:1.02;color:#fff}
.h em{font-style:italic;color:var(--gold2)}
.p{line-height:1.5;color:#E9E1D2;font-weight:500}
.p b{color:#fff;font-weight:700}
.line{height:1px;background:linear-gradient(90deg,var(--gold),transparent)}
.wish{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;color:var(--gold2)}
.tri{display:inline-flex;gap:0;border-radius:2px;overflow:hidden}
.tri i{display:block}
.frame{position:absolute;border:1px solid rgba(194,161,94,.45);pointer-events:none}
"""

DF_DESK = """<div class="ph" style="right:0;top:0;bottom:0;width:62%%"></div>
<div class="fade" style="background:linear-gradient(90deg,#0c0a08 38%%,rgba(12,10,8,.86) 50%%,rgba(12,10,8,.25) 72%%,rgba(12,10,8,.05) 100%%)"></div>
<div class="frame" style="inset:28px"></div>
<div style="position:absolute;left:96px;top:86px;width:720px">
  <img class="logo" src="%(r)sdecoflair-reels-dorinta/assets/logo-wide.png" style="width:250px">
  <div class="k" style="margin-top:56px">%(tri)s Program de sărbători</div>
  <div class="h" style="font-size:78px;margin-top:22px">Ne luăm o scurtă<br><em>pauză de sărbătoare.</em></div>
  <div class="p" style="font-size:23px;margin-top:28px;width:640px">Pe <b>30 noiembrie</b> și <b>1 decembrie</b> nu procesăm comenzi.<br>Comenzile plasate în aceste zile vor fi procesate<br>începând cu <b>3 decembrie 2026</b>.</div>
  <div class="line" style="width:420px;margin:34px 0 26px"></div>
  <div class="wish" style="font-size:40px">La mulți ani, România!</div>
  <div style="font-size:16px;letter-spacing:.3em;text-transform:uppercase;color:#BFB4A0;margin-top:10px">1 Decembrie · Ziua Națională</div>
</div>"""

DF_MOB = """<div class="ph" style="left:0;right:0;top:0;height:560px"></div>
<div class="fade" style="background:linear-gradient(180deg,rgba(12,10,8,.15) 0%%,rgba(12,10,8,.2) 30%%,#0c0a08 50%%)"></div>
<div class="frame" style="inset:22px"></div>
<img class="logo" src="%(r)sdecoflair-reels-dorinta/assets/logo-wide.png" style="position:absolute;left:60px;top:60px;width:230px;filter:drop-shadow(0 2px 14px rgba(0,0,0,.6))">
<div style="position:absolute;left:64px;right:64px;top:540px">
  <div class="k" style="">%(tri)s Program de sărbători</div>
  <div class="h" style="font-size:76px;margin-top:20px">Ne luăm o scurtă<br><em>pauză de sărbătoare.</em></div>
  <div class="p" style="font-size:29px;margin-top:26px">Pe <b>30 noiembrie</b> și <b>1 decembrie</b> nu procesăm comenzi. Comenzile plasate în aceste zile vor fi procesate începând cu <b>3 decembrie 2026</b>.</div>
  <div class="line" style="width:380px;margin:34px 0 24px"></div>
  <div class="wish" style="font-size:52px">La mulți ani, România!</div>
  <div style="font-size:20px;letter-spacing:.3em;text-transform:uppercase;color:#BFB4A0;margin-top:10px">1 Decembrie · Ziua Națională</div>
</div>"""

# ---------------------------------------------------------------- NMC
NMC_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--night:#070A09;--ivory:#F2ECE3;--forest:#123A2A;--forest2:#1C5A40;--sage:#9CC3AC;--muted:#A39E95}
body{width:%(w)spx;height:%(h)spx;overflow:hidden;background:var(--night);color:var(--ivory);font-family:Inter,sans-serif;position:relative}
.ph{position:absolute;background:url(%(img)s) center/cover no-repeat}
.fade{position:absolute;inset:0}
.tag{display:inline-flex;align-items:center;gap:14px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--sage);background:rgba(18,58,42,.7);border:1px solid rgba(156,195,172,.45);border-radius:40px}
.h{font-weight:700;line-height:1.04;letter-spacing:-.02em;color:#fff}
.box{background:var(--ivory);color:#0B100E;border-radius:18px}
.box .t{font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--forest2)}
.box .v{font-weight:700;letter-spacing:-.01em}
.box .d{color:#4b4943}
.wish{font-family:'Cormorant Garamond',serif;font-weight:600;color:#fff}
.tri{display:inline-flex;border-radius:2px;overflow:hidden}
.tri i{display:block}
.c{color:#E9E3DA}
.c b{color:#fff}
"""

NMC_DESK = """<div class="ph" style="right:0;top:0;bottom:0;width:50%%;background-position:50%% 40%%"></div>
<div class="fade" style="background:linear-gradient(90deg,var(--night) 48%%,rgba(7,10,9,.55) 58%%,rgba(7,10,9,0) 75%%)"></div>
<div style="position:absolute;left:120px;top:110px;width:980px">
  <img src="%(r)snmc-reel-bn-final/assets/nmc-logo-alb.png" style="height:56px;display:block">
  <div class="tag" style="font-size:18px;padding:12px 22px;margin-top:54px">%(tri)s Program 30 noiembrie – 1 decembrie</div>
  <div class="h" style="font-size:74px;margin-top:28px">Pe 30&nbsp;noiembrie și 1&nbsp;decembrie<br>nu procesăm comenzi.</div>
  <div class="box" style="display:flex;gap:36px;align-items:center;padding:26px 34px;margin-top:40px;width:920px">
    <div><div class="t" style="font-size:16px">Comenzile plasate în aceste zile</div><div class="v" style="font-size:38px;margin-top:6px">se procesează începând cu 3&nbsp;decembrie&nbsp;2026</div></div>
  </div>
  <div class="c" style="font-size:24px;margin-top:30px">Consultanță gratuită <b>021&nbsp;319&nbsp;35&nbsp;35</b></div>
  <div class="wish" style="font-size:52px;margin-top:40px">La mulți ani, România! <span style="font-family:Inter;font-size:20px;letter-spacing:.2em;color:var(--sage);vertical-align:middle;margin-left:14px">1 DECEMBRIE · ZIUA NAȚIONALĂ</span></div>
</div>"""

NMC_MOB = """<div class="ph" style="left:0;right:0;top:0;height:560px;background-position:50%% 35%%"></div>
<div class="fade" style="background:linear-gradient(180deg,rgba(7,10,9,.35) 0%%,rgba(7,10,9,.1) 22%%,rgba(7,10,9,.85) 40%%,var(--night) 48%%)"></div>
<img src="%(r)snmc-reel-bn-final/assets/nmc-logo-alb.png" style="position:absolute;left:64px;top:64px;height:52px">
<div style="position:absolute;left:64px;right:64px;top:520px">
  <div class="tag" style="font-size:20px;padding:12px 22px">%(tri)s 30 noiembrie – 1 decembrie</div>
  <div class="h" style="font-size:76px;margin-top:24px">Pe 30&nbsp;noiembrie<br>și 1&nbsp;decembrie<br>nu procesăm comenzi.</div>
  <div class="box" style="padding:26px 30px;margin-top:34px">
    <div class="t" style="font-size:18px">Comenzile plasate în aceste zile</div>
    <div class="v" style="font-size:40px;margin-top:8px">se procesează începând cu 3 decembrie 2026</div>
  </div>
  <div class="c" style="font-size:25px;margin-top:26px">Consultanță gratuită <b>021&nbsp;319&nbsp;35&nbsp;35</b></div>
  <div class="wish" style="font-size:60px;margin-top:30px">La mulți ani, România!</div>
  <div style="font-size:20px;letter-spacing:.2em;color:var(--sage);margin-top:6px;font-weight:600">1 DECEMBRIE · ZIUA NAȚIONALĂ</div>
</div>"""

JOBS = [
    ("decoflair-1-decembrie-desktop-1480x800", 1480, 800, DF_CSS, DF_DESK, "decoflair-film-brand/assets/f10-living-nmc.jpg", 15, 12),
    ("decoflair-1-decembrie-mobil-900x1200", 900, 1200, DF_CSS, DF_MOB, "decoflair-film-brand/assets/f10-living-nmc.jpg", 18, 14),
    ("nmc-1-decembrie-desktop-1920x970", 1920, 970, NMC_CSS, NMC_DESK, "nmc-black-november-homepage/assets/exterior.jpg", 0, 14),
    ("nmc-1-decembrie-mobil-1080x1350", 1080, 1350, NMC_CSS, NMC_MOB, "nmc-black-november-homepage/assets/exterior.jpg", 0, 16),
]
for name, w, h, css, body, img, k, tw in JOBS:
    tri = f'<span class="tri">' + ''.join(f'<i style="width:{tw}px;height:{int(tw*1.7)}px;background:{c}"></i>' for c in ('#002B7F', '#FCD116', '#CE1126')) + '</span>'
    html = (f'<!doctype html><html lang="ro"><head><meta charset="utf-8">{FONTS}<style>'
            + css % dict(w=w, h=h, img=R + img, k=k) + '</style></head><body>' + body % dict(r=R, tri=tri) + '</body></html>')
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
print("OK", [j[0] for j in JOBS])

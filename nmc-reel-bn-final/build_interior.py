"""Reel NMC România INTERIOR — „Black November · Colecția Interior” (Instagram/Facebook/TikTok, 1080x1920, ~26 s).

Ton de voce nmcromania.ro (din landing-ul Black November): direct, sigur, factual — „Lider de piață de peste 20 de ani”,
„producție proprie în România”, „livrare imediată pentru produsele din stoc”, „stocuri mari”, „cel mai bun raport calitate–preț”,
„rezistente la UV, ploaie și îngheț, gata de vopsit în orice culoare”, „Consultanță gratuită 021 319 35 35”.
Paleta landing-ului: noapte #070A09, ivoire #F2ECE3, verde pădure #123A2A/#1C5A40/#2E7A57, salvie #9CC3AC (fără roz/magenta).
Prețuri verificate pe nmcromania.ro la 26.11.2026 (−30%: SIDDING PANEL 3 223,31→156,31; NCL107 248,09→173,66).
Rulare: python3 build.py && node render.cjs organic|ads
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
A = "../assets/"

SCENES = [  # interior — prețuri verificate pe nmcromania.ro la 26.11.2026 (blocul principal de preț): Carrara 82671 665,50→465,85; riflaj 382,54 FĂRĂ reducere
    ("i-living-led.jpg", "50% 50%", "BLACK NOVEMBER · COLECȚIA INTERIOR", "Detaliile care<br>schimbă camera.", "Prețuri speciale doar<br>până pe 30 noiembrie.", None, 3.6),
    ("i-riflaj.jpg", "50% 50%", "RIFLAJ ACUSTIC 3D", "Mai cald.<br>Mai liniștit.", "", ("Riflaj acustic 3D", "", "382,54", "p-riflaj.jpg", "stejar deschis · 51 buc. în stoc"), 3.8),
    ("i-tapet-camera.jpg", "45% 50%", "TAPET CARRARA BEST", "Efect de marmură.<br>Fără marmură.", "", ("Tapet Carrara Best 82671", "665,50", "465,85", "p-tapet-82671.jpg", "tapet de perete · rolă"), 3.8),
    ("i-chenare.jpg", "50% 50%", "ALEGEREA LUNII · KIT LINEA", "O cameră întreagă,<br>într-un singur gest.", "Plintă FD2 + cornișă GT + brâu WD5.<br>Profile Noël &amp; Marquet, fabricate în Belgia.", None, 3.6),
    ("i-led.jpg", "50% 50%", "PLINTE · CORNIȘE · ROZETE", "Montaj curat,<br>prin lipire.", "Gata de vopsit.", None, 3.3),
    ("i-tv.jpg", "50% 50%", "ÎN STOC", "Stocuri mari.<br>Livrare imediată.", "Pentru produsele din stoc.", None, 3.3),
]
FINAL = 4.6
T_FINAL = round(sum(s[6] for s in SCENES), 2)
TOTAL = round(T_FINAL + FINAL, 2)
VARIANTS = {"organic": "Link în bio", "ads": ""}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--night:#070A09;--ivory:#F2ECE3;--forest:#123A2A;--forest2:#1C5A40;--forest3:#2E7A57;--sage:#9CC3AC;--muted:#A39E95}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--night);color:var(--ivory);font-family:Inter,sans-serif}
.sc{position:absolute;inset:0;overflow:hidden;display:none}
.bg{position:absolute;inset:-40px;background-size:cover;background-repeat:no-repeat}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,10,9,.82) 0%,rgba(7,10,9,.35) 26%,rgba(7,10,9,0) 42%,rgba(7,10,9,0) 55%,rgba(7,10,9,.78) 78%,rgba(7,10,9,.92) 100%)}
.top{position:absolute;top:150px;left:64px;right:64px;display:flex;align-items:center;justify-content:space-between;z-index:8}
.top img{height:46px}
.pill{font-size:21px;letter-spacing:4px;font-weight:700;padding:12px 20px;border-radius:40px;background:rgba(18,58,42,.85);border:1px solid rgba(156,195,172,.55);color:var(--ivory)}
.pill b{color:var(--sage)}
.k{position:absolute;left:64px;right:120px;top:1150px;font-size:22px;letter-spacing:6px;font-weight:700;color:var(--sage)}
.t{position:absolute;left:64px;right:110px;top:1195px;font-family:'Cormorant Garamond',serif;font-weight:600;font-size:96px;line-height:1.0;text-shadow:0 6px 30px rgba(0,0,0,.6)}
.s{position:absolute;left:64px;right:120px;top:1420px;font-size:34px;line-height:1.35;font-weight:500;color:#E9E3DA}
.card{position:absolute;left:64px;right:120px;top:1410px;display:flex;align-items:center;gap:24px;background:rgba(242,236,227,.97);color:#0B100E;border-radius:22px;padding:16px 26px 16px 16px;box-shadow:0 24px 60px rgba(0,0,0,.45)}
.card .im{width:150px;height:150px;border-radius:14px;background:#fff center/contain no-repeat;flex:0 0 150px}
.card .n{font-size:30px;font-weight:700}
.card .d{font-size:19px;color:#6F6B65;margin-top:2px}
.card .p{display:flex;align-items:baseline;gap:16px;margin-top:6px}
.card .old{font-size:28px;color:#6F6B65;text-decoration:line-through}
.card .new{font-size:56px;font-weight:700;color:var(--forest2);letter-spacing:-1px}
.card .new small{font-size:26px}
.badge{position:absolute;right:120px;top:1370px;width:132px;height:132px;border-radius:50%;background:var(--forest2);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:40px;color:#fff;box-shadow:0 0 0 6px rgba(156,195,172,.35),0 18px 40px rgba(0,0,0,.4);z-index:6}
#grain{position:absolute;inset:-200px;background:url(../assets/grain.png);background-size:540px 960px;opacity:.07;mix-blend-mode:overlay;z-index:50;pointer-events:none}
#fin{position:absolute;inset:0;display:none;z-index:20;background:radial-gradient(ellipse at 50% 42%,#1C5A40 0%,#123A2A 40%,#070A09 85%)}
#fin .lg{position:absolute;left:50%;top:430px;width:300px;margin-left:-150px}
#fin .h{position:absolute;left:0;right:0;top:620px;text-align:center;font-family:'Cormorant Garamond',serif;font-weight:600;font-size:118px;line-height:1}
#fin .d{position:absolute;left:0;right:0;top:770px;text-align:center;font-size:30px;letter-spacing:8px;font-weight:600;color:var(--sage)}
#fin .u{position:absolute;left:90px;right:90px;top:900px;text-align:center;font-size:44px;font-weight:700;padding:26px 0;border-radius:70px;background:var(--ivory);color:#0B100E}
#fin .c{position:absolute;left:0;right:0;top:1060px;text-align:center;font-size:32px;line-height:1.5;font-weight:500;color:#E9E3DA}
#fin .c b{color:#fff}
#fin .f{position:absolute;left:0;right:0;top:1230px;text-align:center;font-size:26px;letter-spacing:4px;color:var(--muted)}
#sweep{position:absolute;top:-300px;bottom:-300px;width:420px;background:linear-gradient(90deg,transparent,rgba(242,236,227,.16),transparent);z-index:21;pointer-events:none}
"""

JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const out=x=>1-Math.pow(1-cl(x),3);
const back=x=>{x=cl(x);const c1=1.6,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
const ST=[];{let a=0;SC.forEach(d=>{ST.push(a);a+=d});}
window.TOTAL=TOTAL;
function up(el,t,a,d=.5,dist=40){if(!el)return 0;const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.transform=`translateY(${(1-k)*dist}px)`;el.style.filter=`blur(${(1-k)*6}px)`;return k}
window.setT=function(t){
  $('#grain').style.transform=`translate(${(Math.floor(t*24)*37)%200-100}px,${(Math.floor(t*24)*53)%200-100}px)`;
  SC.forEach((d,i)=>{const a=ST[i], e=a+d, el=$('#s'+i);
    const on=t>=(i?a-.45:0)&&t<e+.45; el.style.display=on?'block':'none'; if(!on) return; el.style.zIndex=i+1;
    const k=i?ease(seg(t,a-.45,a+.35)):1; el.style.clipPath=i?`inset(${(1-k)*100}% 0 0 0)`:'none';
    el.querySelector('.bg').style.transform=`scale(${1.12-.07*seg(t,a-.45,e+.45)}) translateY(${(1-k)*-60}px)`;
    const f=1-seg(t,e-.35,e);
    [['.k',.15],['.t',.3],['.s',.75],['.card',.7]].forEach(([s,o])=>{const x=el.querySelector(s); if(x){up(x,t,a+o,.55); x.style.opacity=+x.style.opacity*f;}});
    const b=el.querySelector('.badge'); if(b){const kk=seg(t,a+1.0,a+1.45); b.style.opacity=cl(kk*2)*f; b.style.transform=`scale(${.4+.6*back(kk)}) rotate(${(1-kk)*-30}deg)`;}
  });
  const T=t-T_FINAL, F=$('#fin'); F.style.display=T>=-.4?'block':'none'; F.style.opacity=out(seg(T,-.4,.3));
  up($('#fin .lg'),t,T_FINAL+.15,.5,20); up($('#fin .h'),t,T_FINAL+.35,.6,30); up($('#fin .d'),t,T_FINAL+.8,.5,20);
  const u=$('#fin .u'); const ku=seg(t,T_FINAL+1.2,T_FINAL+1.7); u.style.opacity=cl(ku*2); u.style.transform=`scale(${.8+.2*back(ku)})`;
  up($('#fin .c'),t,T_FINAL+1.8,.5,20); up($('#fin .f'),t,T_FINAL+2.3,.5,10);
  $('#sweep').style.transform=`translateX(${-500+2200*seg(T,1.6,3.0)}px) rotate(14deg)`; $('#sweep').style.opacity=T>0?1:0;
};
"""


def scene(i, s):
    img, pos, k, t, sub, card, d = s
    html = f'<div class="sc" id="s{i}"><div class="bg" style="background-image:url({A}{img});background-position:{pos}"></div><div class="shade"></div>'
    html += f'<div class="top"><img src="{A}nmc-logo-alb.png" alt="NMC"><div class="pill">BLACK NOVEMBER · <b>PÂNĂ PE 30.11</b></div></div>'
    html += f'<div class="k">{k}</div><div class="t">{t}</div>'
    if card:
        n, old, new, im, dim = card
        badge = '<div class="badge">−30%</div>' if old else ''
        oldp = f'<span class="old">{old} lei</span>' if old else ''
        html += (f'{badge}<div class="card"><div class="im" style="background-image:url({A}{im})"></div><div>'
                 f'<div class="n">{n}</div><div class="d">{dim}</div><div class="p">{oldp}<span class="new">{new} <small>lei</small></span></div></div></div>')
    elif sub:
        html += f'<div class="s">{sub}</div>'
    return html + '</div>'


for v, foot in VARIANTS.items():
    page = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Inter:wght@400;500;600;700&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>
{''.join(scene(i, s) for i, s in enumerate(SCENES))}
<div id="fin"><img class="lg" src="{A}nmc-logo-alb.png" alt="NMC"><div class="h">Black November</div><div class="d">COLECȚIA INTERIOR · PÂNĂ PE 30.11</div>
<div class="u">nmcromania.ro/black-november</div>
<div class="c">Consultanță gratuită <b>021 319 35 35</b><br>Livrare imediată pentru produsele din stoc</div><div class="f">{foot}</div></div>
<div id="sweep"></div><div id="grain"></div>
<script>const SC={json.dumps([s[6] for s in SCENES])};const T_FINAL={T_FINAL};const TOTAL={TOTAL};{JS}
setT(0);</script></body></html>"""
    (ROOT / "reel" / f"nmc-bn-interior-{v}.html").write_text(page, encoding="utf-8")
print("OK", TOTAL, "s")

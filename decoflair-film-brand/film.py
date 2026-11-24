"""Film de prezentare Deco&Flair — „Detaliile care fac casa.” (16:9, 1920x1080, ~56 s, muzică ambientală originală).

Manifest de brand: de la peretele gol la casa care spune cine ești. Doar fotografii reale (portofoliu decoflair.ro,
foto NMC/Arstyl de pe site, cataloage Dolce & Gabbana / Roberto Cavalli), paleta și sigla originale Deco&Flair.
Format cinematografic (benzi 2,39:1), capitole, tranziții prin ceață, granulație de film.
Rulare: python3 film.py && python3 music.py && node render.cjs   → out/decoflair-film-prezentare.mp4
"""
from pathlib import Path
import json, random, math

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)
A = "../assets/"

# (imagini, capitol, replică, subtitlu, durată). Două imagini = diptic (fotografii verticale)
SCENES = [
    (["f01-perete-gol.jpg"], "", "Fiecare casă începe cu un perete gol.", "", 4.8),
    (["f02-montaj.jpg"], "", "Noi vedem ce poate deveni.", "", 4.4),
    (["f03a-chenare-albastru.jpg", "f03b-chenare-gri.jpg"], "Proporție", "Linii care dau ordine unei încăperi.", "chenare · brâuri · plinte", 4.6),
    (["f04-cornisa-led.jpg"], "Lumină", "Lumina care nu se vede. Se simte.", "cornișe și scafe cu LED", 4.6),
    (["f05-riflaj-macro.jpg"], "Textură", "Materie caldă, pe care o atingi cu privirea.", "riflaje acustice · panouri 3D", 4.6),
    (["f06a-flower.jpg", "f06b-wave.jpg"], "", "Pereți care prind viață în lumină.", "", 4.2),
    (["f07a-dg-leopard.jpg", "f07b-cavalli.jpg"], "Caracter", "Un perete care spune cine ești.", "tapet de colecție · Dolce & Gabbana · Roberto Cavalli", 4.8),
    (["f08-coloane.jpg"], "Prezență", "Afară, o fațadă care rămâne.", "profile de exterior · coloane · ancadramente", 4.6),
    (["f09a-conac.jpg", "f09b-ancadramente.jpg"], "", "Case care se recunosc din stradă.", "", 4.2),
    (["f10-living-nmc.jpg"], "", "Pentru cei care nu se mulțumesc cu „destul de bine”.", "", 4.8),
    (["f11a-rozeta.jpg", "f11b-tv.jpg"], "", "Consultanță. Randări 3D. Livrare în toată țara.", "", 4.4),
]
FINAL = 7.6
T_FINAL = round(sum(s[4] for s in SCENES), 2)
TOTAL = round(T_FINAL + FINAL, 2)

random.seed(5)
MOTES = [[round(random.random() * 1920, 1), round(random.random() * 1080, 1), round(random.uniform(1.5, 4.5), 1), round(random.uniform(8, 26), 1), round(random.random() * 6.28, 2), round(random.uniform(.15, .5), 2)] for _ in range(80)]
PARTS = []
for _ in range(180):
    ang = random.random() * math.tau
    PARTS.append([round(960 + math.cos(ang) * random.uniform(700, 1500), 1), round(540 + math.sin(ang) * random.uniform(500, 1000), 1),
                  round(random.uniform(380, 470), 1), round(ang, 3), round(random.uniform(1.5, 4), 1), round(random.uniform(.25, .7), 2)])

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--gold:#C2A15E;--gold2:#E2CB94;--ink:#0c0a08}
html,body{width:1920px;height:1080px;overflow:hidden;background:#000;color:#fff;font-family:Manrope,sans-serif}
.sc{position:absolute;inset:0;overflow:hidden;display:none}
.im{position:absolute;top:0;bottom:0;overflow:hidden}
.im i{position:absolute;inset:-30px;background-size:cover;background-position:center;display:block}
.single{left:0;right:0}
.dl{left:0;width:956px}.dr{right:0;width:956px}
.shade{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 40%,rgba(0,0,0,.55) 100%),linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.72) 100%)}
.txt{position:absolute;left:0;right:0;bottom:190px;text-align:center;z-index:5}
.ch{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:30px;letter-spacing:18px;text-transform:uppercase;color:var(--gold2);margin-bottom:14px;text-shadow:0 2px 18px rgba(0,0,0,.6)}
.ln{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;font-size:66px;line-height:1.1;text-shadow:0 4px 30px rgba(0,0,0,.75)}
.sub{margin-top:16px;font-size:20px;letter-spacing:7px;text-transform:uppercase;font-weight:600;color:rgba(255,255,255,.78)}
.bars:before,.bars:after{content:'';position:absolute;left:0;right:0;height:138px;background:#000;z-index:40}
.bars:before{top:0}.bars:after{bottom:0}
#mist{position:absolute;inset:-300px;z-index:30;pointer-events:none;opacity:0;background:radial-gradient(ellipse 45% 40% at 30% 45%,rgba(255,236,205,.7),rgba(255,236,205,0) 70%),radial-gradient(ellipse 40% 35% at 72% 58%,rgba(255,214,160,.5),rgba(255,214,160,0) 70%);filter:blur(40px)}
#leak{position:absolute;top:-200px;bottom:-200px;width:900px;z-index:31;pointer-events:none;opacity:0;background:linear-gradient(90deg,transparent,rgba(255,190,110,.28),rgba(255,235,200,.35),transparent);filter:blur(30px);mix-blend-mode:screen}
#motes{position:absolute;inset:0;z-index:32;pointer-events:none}
#motes i{position:absolute;left:0;top:0;border-radius:50%;background:#FFF3D6;box-shadow:0 0 10px rgba(230,190,110,.9)}
#grain{position:absolute;inset:-200px;background:url(../assets/grain.png);background-size:540px 960px;opacity:.08;mix-blend-mode:overlay;z-index:45;pointer-events:none}
/* final */
#fin{position:absolute;inset:0;background:#0c0a08;display:none;z-index:20}
#glow{position:absolute;left:50%;top:50%;width:1800px;height:1800px;margin:-900px 0 0 -900px;border-radius:50%;background:radial-gradient(circle,rgba(194,161,94,.38) 0%,rgba(140,105,50,.14) 30%,rgba(0,0,0,0) 60%)}
#beam{position:absolute;left:-800px;top:-300px;width:600px;height:1700px;background:linear-gradient(90deg,transparent,rgba(255,232,190,.18),transparent);mix-blend-mode:screen}
#ring{position:absolute;left:50%;top:50%;border-radius:50%;border:2px solid rgba(226,203,148,.9);box-shadow:0 0 44px rgba(194,161,94,.7),inset 0 0 40px rgba(194,161,94,.4)}
#parts i{position:absolute;left:0;top:0;border-radius:50%;background:#FFF1D0;box-shadow:0 0 10px rgba(226,190,120,.95)}
#logo{position:absolute;left:50%;top:250px;width:560px;margin-left:-280px;filter:drop-shadow(0 0 30px rgba(194,161,94,.45))}
#site{position:absolute;left:0;right:0;top:545px;text-align:center;font-family:Unbounded,sans-serif;font-weight:800;font-size:96px;line-height:1.1;
 background:linear-gradient(100deg,#8a6d35 0%,#fff3d6 18%,#C2A15E 32%,#fffaf0 46%,#a8843f 60%,#fff3d6 74%,#E2CB94 100%);background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent}
#tag{position:absolute;left:0;right:0;top:690px;text-align:center;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;font-size:54px}
#contact{position:absolute;left:0;right:0;top:790px;text-align:center;font-size:22px;letter-spacing:6px;font-weight:700;color:var(--gold2);text-transform:uppercase}
#flare{position:absolute;left:50%;top:50%;width:1200px;height:6px;margin-left:-600px;background:radial-gradient(ellipse,rgba(255,255,255,.95),rgba(255,210,140,0) 70%);filter:blur(2px)}
"""

JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const out=x=>1-Math.pow(1-cl(x),3);
const expo=x=>{x=cl(x);return x==1?1:1-Math.pow(2,-10*x)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
const ST=[];{let a=0;SC.forEach(d=>{ST.push(a);a+=d});}
window.TOTAL=TOTAL;
function tx(el,t,a,d=1.0,dist=16){const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.filter=`blur(${(1-k)*10}px)`;el.style.transform=`translateY(${(1-k)*dist}px)`;return k}
window.setT=function(t){
  $('#grain').style.transform=`translate(${(Math.floor(t*24)*37)%200-100}px,${(Math.floor(t*24)*53)%200-100}px)`;
  let mist=0;
  SC.forEach((d,i)=>{const a=ST[i], e=a+d, el=$('#s'+i);
    const start=i==0?0:a-.7, end=e+.9; const on=t>=start&&t<end; el.style.display=on?'block':'none'; if(!on) return;
    el.style.zIndex=i+1;
    const k=i==0?out(seg(t,0,1.4)):ease(seg(t,a-.7,a+.9)); el.style.opacity=k;
    if(i>0) mist=Math.max(mist,Math.sin(Math.PI*seg(t,a-.8,a+1.0)));
    const ex=seg(t,e-.4,e+.9);
    el.querySelectorAll('.im i').forEach((im,j)=>{const dir=(i+j)%2?1:-1;
      im.style.transform=`scale(${1.06+.07*seg(t,a-.7,e+.9)}) translateX(${dir*22*seg(t,a-.7,e+.9)}px)`;
      im.style.filter=`blur(${ex*7}px) brightness(${1+.15*ex}) saturate(${1-.2*ex})`;});
    const fade=1-seg(t,e-.6,e);
    const ch=el.querySelector('.ch'); if(ch){const kk=tx(ch,t,a+.35,1.1,0); ch.style.opacity=kk*fade; ch.style.letterSpacing=`${18+14*(1-kk)}px`;}
    const ln=el.querySelector('.ln'); const k2=tx(ln,t,a+.75,1.2,18); ln.style.opacity=k2*fade;
    const sb=el.querySelector('.sub'); if(sb){const k3=tx(sb,t,a+1.5,1.0,10); sb.style.opacity=k3*fade*.95;}
  });
  vis('#mist', .05+.5*Math.max(mist,Math.sin(Math.PI*seg(t,T_FINAL-.8,T_FINAL+1.2))));
  $('#mist').style.transform=`translate(${Math.sin(t*.3)*90}px,${Math.cos(t*.23)*60}px)`;
  // reflex cald peste unele tranziții
  const LK=[ST[2],ST[4],ST[6],ST[9]]; let lk=0,lx=-900; LK.forEach(a=>{const k=seg(t,a-.6,a+1.4); if(k>0&&k<1){lk=Math.sin(Math.PI*k);lx=-900+3000*k}});
  vis('#leak',lk*.9); $('#leak').style.transform=`translateX(${lx}px) rotate(12deg)`;
  $$('#motes i').forEach((m,i)=>{const d=MOTES[i];const y=((d[1]-t*d[3])%1120+1120)%1120-20, x=d[0]+Math.sin(t*.45+d[4])*26;
    m.style.transform=`translate(${x}px,${y}px)`; m.style.opacity=d[5]*(.55+.45*Math.sin(t*1.2+d[4]))*(t<T_FINAL?1:1-seg(t,T_FINAL,T_FINAL+1.5));});
  // final
  const F=$('#fin'); const T=t-T_FINAL; F.style.display=T>=-.6?'block':'none'; F.style.opacity=out(seg(T,-.6,.6));
  vis('#glow', out(seg(T,0,1.6))*(.85+.15*Math.sin(t*1.8)));
  $('#beam').style.transform=`translateX(${-200+3200*seg(T,.6,3.2)}px) rotate(18deg)`;
  $$('#parts i').forEach((p,i)=>{const d=PARTS[i]; const k=ease(seg(T,0,2.0)); const ang=d[3]+T*.3;
    const rx=960+Math.cos(ang)*d[2]*1.25, ry=540+Math.sin(ang)*d[2]*.45;
    p.style.transform=`translate(${d[0]+(rx-d[0])*k}px,${d[1]+(ry-d[1])*k}px)`; p.style.opacity=d[5]*out(seg(T,0,.5))*(1-.5*seg(T,4,6.5));});
  const rk=expo(seg(T,.8,2.4)); const R=100+900*rk; const ring=$('#ring'); ring.style.width=ring.style.height=R+'px'; ring.style.margin=`${-R/2}px 0 0 ${-R/2}px`; ring.style.opacity=(1-rk)*.9+.06;
  tx($('#logo'),t,T_FINAL+.9,1.4,20);
  const sk=out(seg(T,1.6,2.6)); const site=$('#site'); site.style.opacity=sk; site.style.letterSpacing=`${(1-sk)*30}px`;
  site.style.filter=`blur(${(1-sk)*10}px) drop-shadow(0 0 26px rgba(194,161,94,.5))`; site.style.backgroundPosition=`${100-100*seg(T,2,5.5)}% 0`;
  const fl=seg(T,2.8,3.8); vis('#flare',Math.sin(Math.PI*fl)); $('#flare').style.transform=`scaleX(${.3+fl})`;
  tx($('#tag'),t,T_FINAL+3.0,1.2,16); tx($('#contact'),t,T_FINAL+3.9,1.0,10);
  vis('#black', seg(t,TOTAL-.9,TOTAL));
};
function vis(s,o){$(s).style.opacity=o}
"""


def scene(i, s):
    imgs, ch, ln, sub, d = s
    if len(imgs) == 1:
        im = f'<div class="im single"><i style="background-image:url({A}{imgs[0]})"></i></div>'
    else:
        im = f'<div class="im dl"><i style="background-image:url({A}{imgs[0]})"></i></div><div class="im dr"><i style="background-image:url({A}{imgs[1]})"></i></div>'
    return (f'<div class="sc" id="s{i}">{im}<div class="shade"></div><div class="txt">'
            + (f'<div class="ch">{ch}</div>' if ch else '')
            + f'<div class="ln">{ln}</div>' + (f'<div class="sub">{sub}</div>' if sub else '') + '</div></div>')


html = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Unbounded:wght@800&family=Cormorant+Garamond:ital,wght@0,600;1,600&display=block" rel="stylesheet">
<style>{CSS}</style></head><body class="bars">
{''.join(scene(i, s) for i, s in enumerate(SCENES))}
<div id="fin"><div id="glow"></div><div id="beam"></div><div id="ring"></div><div id="parts">{''.join(f'<i style="width:{p[4]}px;height:{p[4]}px"></i>' for p in PARTS)}</div>
<img id="logo" src="{A}logo-wide.png" alt="Deco &amp; Flair" style="opacity:0"><div id="site" style="opacity:0">decoflair.ro</div><div id="flare"></div>
<div id="tag" style="opacity:0">Detaliile care fac casa.</div>
<div id="contact" style="opacity:0">Consultanță gratuită · 0765 740 280</div></div>
<div id="mist"></div><div id="leak"></div><div id="motes">{''.join(f'<i style="width:{m[2]}px;height:{m[2]}px"></i>' for m in MOTES)}</div>
<div id="grain"></div><div id="black" style="position:absolute;inset:0;background:#000;opacity:0;z-index:60"></div>
<script>const SC={json.dumps([s[4] for s in SCENES])};const T_FINAL={T_FINAL};const TOTAL={TOTAL};const MOTES={json.dumps(MOTES)};const PARTS={json.dumps(PARTS)};{JS}
setT(0);</script></body></html>"""
(OUT / "film.html").write_text(html, encoding="utf-8")
(OUT / "timing.json").write_text(json.dumps({"total": TOTAL, "final": T_FINAL, "starts": [round(sum(s[4] for s in SCENES[:i]), 2) for i in range(len(SCENES))]}), encoding="utf-8")
print("OK durată", TOTAL, "s; final la", T_FINAL)

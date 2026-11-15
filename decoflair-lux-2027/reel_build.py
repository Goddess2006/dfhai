"""Reel Deco&Flair „Lux 2027” — reel/reel.html (1080x1920): intro + 10 creative + final, ritm alert-elegant.
Rulare: python3 reel_build.py && node reel_render.cjs
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

(ROOT / "reel").mkdir(exist_ok=True)

EXTRA = """
.sc{position:absolute;inset:0;opacity:0;overflow:hidden}
.sc .c{position:absolute;inset:0;height:1920px}
.amb{transform-origin:50% 40%}
.io{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,#3a1418 0%,#140d10 50%,#0b0a0c 85%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}
.io::after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(214,188,132,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(214,188,132,.06) 1px,transparent 1px);background-size:90px 90px}
.io .lg{width:380px;position:relative;z-index:1}
.io .mono{margin-top:60px;position:relative;z-index:1}
.io .t1{font-weight:300;font-size:58px;letter-spacing:8px;text-transform:uppercase;margin-top:40px;position:relative;z-index:1}
.io .t2{font-family:'Playfair Display',serif;font-style:italic;font-weight:600;font-size:96px;color:var(--gold);line-height:1.05;margin-top:10px;position:relative;z-index:1}
.io .ln{width:140px;height:2px;background:var(--red);margin:50px 0 40px;position:relative;z-index:1}
.io p{font-weight:300;font-size:36px;line-height:1.45;color:rgba(255,255,255,.88);position:relative;z-index:1}
.io b.site{font-family:'Playfair Display',serif;font-weight:600;font-size:76px;color:var(--cream);margin-top:18px;display:block;position:relative;z-index:1}
"""

scenes = ["""<div class="sc" data-k="io"><div class="io">
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="mono">Holiday Edition · 10 detalii</div>
<div class="t1">Case ca în filme</div>
<div class="t2">înainte de sărbători.</div>
<div class="ln"></div>
<p>Lux real, la prețuri reale.</p></div></div>"""]
for i, p in enumerate(build.P, 1):
    inner = build.scene(p, i).replace('src="assets/', 'src="../assets/')
    scenes.append(f'<div class="sc" data-k="p"><div class="c">{inner}</div></div>')
scenes.append("""<div class="sc" data-k="io"><div class="io">
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="t1">Fă-i să spună</div>
<div class="t2">„Vai, ce casă frumoasă!”</div>
<div class="ln"></div>
<p>Comandă detaliile pe</p>
<b class="site">decoflair.ro</b></div></div>""")

JS = r"""
const D={io:2.8,p:3.5}, X=0.45;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const seg=(u,a,b)=>cl((u-a)/(b-a));
const q=(s,sel)=>s.querySelector(sel);
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  let o=0; if(u>=0&&u<=s.d){o=1; if(i>0&&u<X)o=u/X;}
  s.style.opacity=o; s.style.display=o>0?'block':'none'; if(!o)return;
  if(s.dataset.k==='p'){
   q(s,'.amb').style.transform=`scale(${1.13-0.09*cl(u/s.d)})`;
   const h=ease(seg(u,.1,.7)); q(s,'.hud').style.opacity=h; q(s,'.hud').style.transform=`scale(${1.06-.06*h})`;
   fade(q(s,'.l1'),ease(seg(u,.2,.75)),-40,0);
   fade(q(s,'.l2'),ease(seg(u,.4,1.0)),40,0);
   fade(q(s,'.tip'),ease(seg(u,.9,1.4)),0,24);
   fade(q(s,'.glass'),ease(seg(u,.6,1.2)),0,120);
   const pr=seg(u,1.3,1.8); q(s,'.price b').style.cssText=`display:inline-block;transform:scale(${1+.12*Math.sin(Math.PI*pr)});transform-origin:0 70%`;
   fade(q(s,'.buy'),ease(seg(u,1.5,2.0)),0,16);
  } else {
   [...s.querySelectorAll('.lg,.mono,.t1,.t2,.ln,p,.site')].forEach((e,j)=>fade(e,ease(seg(u,.15+j*.22,.8+j*.22)),0,30));
  }
 });
};
setT(0);
"""

html = (build.HEAD.replace('{t}', 'Deco&Flair Lux 2027 — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative">' + "".join(scenes)
        + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

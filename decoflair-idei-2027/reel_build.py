"""Reel Deco&Flair „Idei 2027” — reel/reel.html (1080x1920): intro + manifest + 10 idei + final, alternanță lumină/întuneric.
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
.arch img{transform-origin:50% 60%}
.io{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}
.io.l{background:radial-gradient(circle at 70% 20%,rgba(201,168,105,.45),transparent 50%),var(--cream);color:var(--ink)}
.io.d{background:radial-gradient(circle at 30% 80%,rgba(158,31,42,.45),transparent 55%),var(--onyx);color:var(--cream)}
.io .lg{width:340px}
.io .l.lg{filter:brightness(.82) contrast(1.15)}
.io .t1{font-family:'Playfair Display',serif;font-weight:500;font-size:74px;line-height:1.1;margin-top:70px}
.io .t2{font-family:'Playfair Display',serif;font-style:italic;font-weight:600;font-size:74px;line-height:1.1;margin-top:10px}
.io.l .t2{color:var(--red)}.io.d .t2{color:var(--gold2)}
.io .ln{width:120px;height:2px;background:var(--gold);margin:50px 0 40px}
.io p{font-weight:300;font-size:36px;line-height:1.5}
.io .site{font-family:'Playfair Display',serif;font-weight:600;font-size:80px;margin-top:20px}
.io .mono{margin-top:40px;opacity:.75}
"""

scenes = ["""<div class="sc" data-k="io"><div class="io l">
<img class="lg" src="../assets/logo-decoflair.png" style="filter:brightness(.82) contrast(1.15)" alt="Deco&amp;Flair">
<div class="t1">Pe decoflair.ro nu cumperi</div>
<div class="t2">doar un produs.</div>
<div class="ln"></div>
<p>Cumperi selecție, know-how<br>și casa pe care o visezi.</p></div></div>"""]
scenes.append('<div class="sc light man story" data-k="p"><div class="c">'
              + build.manifest().replace('src="assets/', 'src="../assets/') + '</div></div>')
for i, p in enumerate(build.P, 1):
    inner = build.scene(p, i).replace('src="assets/', 'src="../assets/')
    scenes.append(f'<div class="sc {p["theme"]}" data-k="p"><div class="c">{inner}</div></div>')
scenes.append("""<div class="sc" data-k="io"><div class="io d">
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="t1">Cumpără privirea</div>
<div class="t2">musafirului din prag.</div>
<div class="ln"></div>
<p>Idei și produse pentru orice buget, pe</p>
<div class="site">decoflair.ro</div>
<div class="mono">Reduceri de sezon</div></div></div>""")

JS = r"""
const D={io:3.0,p:3.4}, X=0.45;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const back=v=>{const c=1.6;return 1+(c+1)*Math.pow(v-1,3)+c*Math.pow(v-1,2)};
const seg=(u,a,b)=>cl((u-a)/(b-a));
const qa=(s,sel)=>[...s.querySelectorAll(sel)];
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  let o=0; if(u>=0&&u<=s.d){o=1; if(i>0&&u<X)o=u/X;}
  s.style.opacity=o; s.style.display=o>0?'block':'none'; if(!o)return;
  if(s.dataset.k==='p'){
   const a=ease(seg(u,0,.9));
   qa(s,'.arch,.arches div').forEach((e,j)=>{const v=ease(seg(u,j*.12,.9+j*.12)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*70}px)`;});
   qa(s,'.arch img,.arches img').forEach(e=>e.style.transform=`scale(${1.12-.1*cl(u/s.d)})`);
   const m=seg(u,.7,1.2); const me=s.querySelector('.medal'); if(me){me.style.transform=`scale(${m?back(m):0})`;}
   fade(s.querySelector('.room'),ease(seg(u,.6,1.0)),-30,0);
   fade(s.querySelector('.q'),ease(seg(u,.5,1.0)),0,20);
   fade(s.querySelector('.h'),ease(seg(u,.8,1.4)),0,40);
   fade(s.querySelector('.prod'),ease(seg(u,1.1,1.5)),0,20);
   fade(s.querySelector('.idea'),ease(seg(u,1.3,1.9)),0,24);
   fade(s.querySelector('.proof'),ease(seg(u,1.7,2.2)),0,10);
   fade(s.querySelector('.foot'),ease(seg(u,1.8,2.3)),0,16);
   fade(s.querySelector('.side'),a,0,0);
  } else {
   qa(s,'.lg,.t1,.t2,.ln,p,.site,.mono').forEach((e,j)=>fade(e,ease(seg(u,.15+j*.25,.85+j*.25)),0,30));
  }
 });
};
setT(0);
"""

html = (build.HEAD.replace('{t}', 'Deco&Flair Idei 2027 — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative">' + "".join(scenes)
        + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

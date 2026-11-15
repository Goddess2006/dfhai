"""Reel NMC „Povești de casă” — reel/reel.html (1080x1920), ritm lent și elegant: intro + 5 povești + final.
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
.amb{transform-origin:50% 50%}
.io{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,#2a2348 0%,#121526 45%,#0a0c14 80%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}
.io .lg{width:150px;border-radius:10px}
.io .k{margin-top:70px;font-weight:300;font-size:26px;letter-spacing:10px;text-transform:uppercase;color:rgba(255,255,255,.75)}
.io h1,.io h2{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:132px;line-height:1;margin-top:26px}
.io h2{font-size:98px}
.io .ln{width:120px;height:2px;background:#FF671F;margin:56px 0 46px}
.io p{font-weight:300;font-size:36px;line-height:1.45;color:rgba(255,255,255,.88)}
.io b.site{font-weight:700;font-size:64px;margin-top:20px;display:block;color:#fff}
"""

scenes = ["""<div class="sc" data-k="io"><div class="io">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<div class="k">NMC prezintă</div>
<h1>Povești<br>de casă</h1>
<div class="ln"></div>
<p>Cinci detalii care schimbă felul<br>în care îți trăiești casa.</p></div></div>"""]
for p in build.PRODUCTS:
    inner = build.scene(p).replace('src="assets/', 'src="../assets/')
    scenes.append(f'<div class="sc" data-k="p"><div class="c">{inner}</div></div>')
scenes.append("""<div class="sc" data-k="io"><div class="io">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<h2>Care e povestea<br>casei tale?</h2>
<div class="ln"></div>
<p>Găsește detaliul potrivit pe</p>
<b class="site">nmcromania.ro</b></div></div>""")

JS = r"""
const D={io:3.0,p:4.6}, X=0.7;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const seg=(u,a,b)=>cl((u-a)/(b-a));
const q=(s,sel)=>s.querySelector(sel);
function fade(e,v,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translateY(${(1-v)*dy}px)`;}
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  let o=0; if(u>=0&&u<=s.d){o=1; if(i>0&&u<X)o=u/X;}
  s.style.opacity=o; s.style.display=o>0?'block':'none'; if(!o)return;
  if(s.dataset.k==='p'){
   q(s,'.amb').style.transform=`scale(${1.12-0.08*cl(u/s.d)}) translateX(${-14*cl(u/s.d)}px)`;
   fade(q(s,'.top'),ease(seg(u,.2,.9)),-20);
   fade(q(s,'.need'),ease(seg(u,.5,1.4)),40);
   fade(q(s,'.answer'),ease(seg(u,1.4,2.2)),30);
   const l=ease(seg(u,1.0,1.9)); const le=q(s,'.lens'); le.style.opacity=l; le.style.transform=`scale(${.75+.25*l})`;
   fade(q(s,'.lab'),ease(seg(u,1.7,2.3)),16);
   fade(q(s,'.cta'),ease(seg(u,2.3,3.0)),20);
  } else {
   [...s.querySelectorAll('.lg,.k,h1,h2,.ln,p,.site')].forEach((e,j)=>fade(e,ease(seg(u,.2+j*.3,1.0+j*.3)),30));
  }
 });
};
setT(0);
"""

html = (build.HEAD.replace('{t}', 'NMC Povești de casă — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative">' + "".join(scenes)
        + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

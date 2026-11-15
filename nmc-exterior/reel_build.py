"""Reel NMC exterior — reel/reel.html (1080x1920): intro + 4 creative + final, cu timeline determinist window.setT(t).
Rulare: python3 reel_build.py && node reel_render.cjs  (necesită ffmpeg)
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (regenerează și feed/story)

(ROOT / "reel").mkdir(exist_ok=True)

EXTRA = """
.sc{position:absolute;inset:0;opacity:0;overflow:hidden}
.sc .c{position:absolute;inset:0;height:1920px}
.amb{transform-origin:50% 100%}
.intro,.outro{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 42%,#3a2014 0%,#161618 62%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.intro .lg,.outro .lg{width:260px;border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.5)}
.intro h1{font-weight:900;font-size:140px;line-height:1.05;letter-spacing:-2px;margin-top:70px;text-transform:uppercase}
.intro h1 i{font-style:normal;color:#FF671F;display:block}
.intro p{font-size:54px;font-weight:700;margin-top:56px}
.intro p b{color:#FF671F;font-weight:900}
.intro .fl svg{width:54px;height:36px;vertical-align:-4px;margin-right:6px}
.intro small{font-size:34px;color:#b9bcc6;margin-top:22px;letter-spacing:6px;text-transform:uppercase;font-weight:500}
.outro p{font-size:46px;font-weight:500;margin-top:80px;color:#d8d9de}
.outro h2{font-weight:900;font-size:104px;color:#FF671F;margin-top:14px;letter-spacing:-1px}
.outro small{font-size:30px;color:#9a9ca6;margin-top:40px}
"""

scenes = []
scenes.append(f"""<div class="sc" data-k="intro"><div class="intro">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<h1>Fațade care<i>rezistă</i></h1>
<p><span class="fl">{build.ICONS['flag']}</span> Producție proprie <b>în România</b></p>
<small>Profile de exterior ADRo®</small></div></div>""")
for p in build.PRODUCTS:
    inner = build.scene(p).replace('src="assets/', 'src="../assets/')
    g = ' gama' if len(p["cards"]) > 1 else ''
    scenes.append(f'<div class="sc{g}" data-k="p"><div class="c">{inner}</div></div>')
scenes.append("""<div class="sc" data-k="outro"><div class="outro">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<p>Prețuri speciale pe</p>
<h2>nmcromania.ro</h2>
<small>Lider de piață · peste 20 de ani de experiență</small></div></div>""")

JS = r"""
const D={intro:2.6,p:4.2,outro:3.0}, X=0.4;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const back=v=>{const c=1.7;return 1+(c+1)*Math.pow(v-1,3)+c*Math.pow(v-1,2)};
const seg=(u,a,b)=>cl((u-a)/(b-a));
function q(s,sel){return s.querySelector(sel)}
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  let o=0; if(u>=0&&u<=s.d){o=1; if(i>0&&u<X)o=u/X; if(i<S.length-1&&u>s.d-X)o=Math.min(o,1);}
  if(i<S.length-1&&u>s.d){o=0}
  s.style.opacity=o; s.style.display=o>0?'block':'none'; if(!o)return;
  const k=s.dataset.k;
  if(k==='p'){
   q(s,'.amb').style.transform=`scale(${1.14-0.10*cl(u/s.d)})`;
   const h=ease(seg(u,.15,.65)); {const e=q(s,'.head');e.style.opacity=h;e.style.transform=`translateY(${(1-h)*50}px)`;}
   const b=seg(u,.45,.95); q(s,'.badge').style.transform=`rotate(-8deg) scale(${b?back(b):0})`;
   const c=ease(seg(u,.3,.85)); const pr=q(s,'.card'); if(pr)pr.style.transform=`translateX(${(1-c)*-560}px)`; [...s.querySelectorAll('.cards3 figure')].forEach((e,j)=>{const v=ease(seg(u,.3+j*.15,.8+j*.15)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*80}px)`;});
   const f=ease(seg(u,.65,1.15)); {const e=q(s,'.info'); if(e){e.style.opacity=f;e.style.transform=`translateY(${(1-f)*60}px)`;}}
   [...s.querySelectorAll('.chips span,.trust div')].forEach((e,j)=>{const v=ease(seg(u,1.1+j*.18,1.5+j*.18)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*24}px)`;});
  } else {
   const a=ease(seg(u,0,.6)); const lg=q(s,'.lg'); lg.style.cssText=`opacity:${a};transform:translateY(${(1-a)*-40}px)`;
   const h=q(s,'h1')||q(s,'h2'); const hb=seg(u,.2,.75); h.style.transform=`scale(${hb?back(hb):0})`;
   [...s.querySelectorAll('p,small')].forEach((e,j)=>{const v=ease(seg(u,.6+j*.25,1.1+j*.25)); e.style.cssText=`opacity:${v};transform:translateY(${(1-v)*30}px)`;});
  }
 });
};
setT(0);
"""

html = (build.HEAD.replace('{t}', 'NMC Exterior — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative">' + "".join(scenes)
        + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

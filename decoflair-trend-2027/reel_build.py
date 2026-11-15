"""Reel Deco&Flair „Trend 2027 · Tokyo × Singapore” — reel/reel.html (1080x1920).
Intro (cerc desenat + 2027, sigiliu D&F care „ștampilează”) → 8 produse: teaser (cuvântul-cheie + întrebarea pe fotografie vie), mesaje scurte între produse, ritm lent →
dezvăluire (cerc ensō desenat, pașii Problemă → Soluție → Rezultat pe rând), tranziție tip pagină, bară de progres →
final cu logo, site, QR și contact. Rulare: python3 build.py && python3 reel_build.py && node reel_render.cjs
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

(ROOT / "reel").mkdir(exist_ok=True)
vb, qd = (ROOT / "assets" / "qr-decoflair.txt").read_text().split("\n", 1)

HEAD = build.HEAD

EXTRA = """
.sc{position:absolute;inset:0;overflow:hidden;box-shadow:-40px 0 80px rgba(0,0,0,.3)}
.sc .c{position:absolute;inset:0;height:1920px}
.photo img{transform-origin:50% 50%}
.tz{position:absolute;inset:0;z-index:30;overflow:hidden;background:#111}
.tz img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(1.15) brightness(.62)}
.tz .in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff;padding:0 80px}
.tz .jp{font-family:'Space Mono',monospace;font-size:30px;letter-spacing:16px;text-transform:uppercase;opacity:.95;padding:14px 26px;border:1.5px solid rgba(255,255,255,.7);border-radius:40px}
.tz .ln{width:0;height:2px;background:#fff;margin-top:50px}
.tz .qq{font-weight:400;font-size:82px;line-height:1.08;margin-top:56px;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.tz .no{position:absolute;top:240px;left:0;right:0;text-align:center}
.prog{position:absolute;left:60px;right:60px;top:120px;display:flex;gap:8px;z-index:80}
.prog i{flex:1;height:5px;border-radius:3px;background:rgba(255,255,255,.4);overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.1)}
.prog i b{display:block;height:100%;width:0;background:#C8392B}
.io{position:absolute;inset:0;background:var(--washi);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--ink)}
.io .big{position:relative;width:400px;height:400px;margin-top:40px}.io .big svg{position:absolute;inset:0}.io .big span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-weight:600;font-size:118px}
.io .stamp{position:absolute;width:190px;height:190px;background:var(--hanko);color:#fff;border-radius:18px;display:flex;align-items:center;justify-content:center;
 font-family:'Playfair Display',serif;font-weight:600;font-size:64px;line-height:.9;text-align:center;box-shadow:inset 0 0 0 8px rgba(255,255,255,.35)}
.io .t1{font-weight:300;font-size:64px;letter-spacing:10px;text-transform:uppercase;margin-top:60px}
.io .t2{font-family:'Playfair Display',serif;font-style:italic;font-weight:600;font-size:76px;color:var(--hanko);margin-top:6px}
.io .mono{margin-top:44px;color:var(--mut)}
.io .lg{width:340px;filter:brightness(.8) contrast(1.2)}
.io .site{font-family:'Playfair Display',serif;font-weight:600;font-size:104px;margin-top:10px}
.io .k{font-weight:300;font-size:44px;margin-top:60px}
.io .qr{margin-top:40px;width:240px;height:240px;background:#fff;padding:16px;border-radius:14px;box-shadow:0 0 0 3px var(--ink)}
.io .qr svg{width:100%;height:100%;display:block}
.io .ct{margin-top:40px;display:flex;flex-direction:column;gap:12px;font-size:31px;font-weight:300}
.io .ct span{font-family:'Space Mono',monospace;font-size:19px;letter-spacing:3px;text-transform:uppercase;color:var(--hanko);margin-right:12px}
.io .ct b{font-weight:600}
.msg .mt{font-family:'Playfair Display',serif;font-weight:500;font-size:84px;line-height:1.12;margin-top:40px;padding:0 80px}
.msg .mt i{color:var(--hanko);font-weight:600}
.msg .ml{width:0;height:2px;background:var(--ink);margin-top:56px}
"""

scenes = ["""<div class="sc" data-k="intro"><div class="io"><div class="fiber" style="position:absolute;inset:0"></div>
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="big"><svg viewBox="0 0 400 400" width="400" height="400"><circle cx="200" cy="200" r="180" fill="none" stroke="#1B1B1F" stroke-width="9" stroke-linecap="round"/></svg><span>2027</span></div>
<div class="stamp" style="right:190px;top:900px">D<br>&amp;F</div>
<div class="t1">Trend 2027</div>
<div class="t2">Tokyo × Singapore</div>
<div class="mono">8 forme care schimbă o casă</div></div></div>"""]
MSG = ['Liniștea, rezolvată.<br><i>Acum, ritmul.</i>', 'Un singur detaliu<br><i>schimbă o cameră întreagă.</i>', 'Culoarea are nevoie<br><i>de formă.</i>', 'Restul îl face<br><i>lumina.</i>', 'Acasă poate arăta<br><i>ca un hotel boutique.</i>', 'Unic înseamnă<br><i>al tău.</i>', 'Ultimul detaliu:<br><i>lumina caldă.</i>']
for i, p in enumerate(build.P, 1):
    if i > 1:
        scenes.append(f'<div class="sc" data-k="msg"><div class="io msg"><div class="fiber" style="position:absolute;inset:0"></div><div class="mono">Deco&amp;Flair · Trend 2027</div><div class="mt">{MSG[i-2]}</div><div class="ml"></div></div></div>')
    inner = build.scene(p, i).replace('src="assets/', 'src="../assets/')
    tz = (f'<div class="tz"><img src="../assets/{p["amb"]}" style="object-position:{p["pos"]}" alt="">'
          f'<div class="no mono" style="color:#fff">No.{i:02d}</div>'
          f'<div class="in"><div class="jp">{p["jp"]}</div><div class="qq">{p["q"]}</div><div class="ln"></div></div></div>')
    scenes.append(f'<div class="sc" data-k="p" style="--acc:{p["accent"]}">{tz}<div class="c">{inner}</div></div>')
scenes.append(f"""<div class="sc" data-k="out"><div class="io"><div class="fiber" style="position:absolute;inset:0"></div>
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="k">Fii primul care le are acasă.</div>
<div class="site">decoflair.ro</div>
<div class="qr"><svg viewBox="{vb}"><path d="{qd}" fill="#1B1B1F"/></svg></div>
<div class="ct"><div><span>Consultanță</span><b>0723 300 603</b></div>
<div><span>E-mail</span>office@decoflair.ro</div>
<div><span>Program</span>Luni – Vineri · 07:30 – 16:00</div>
<div><span>Instagram</span>@decoflairhub</div></div></div></div>""")

JS = r"""
const D={intro:4.6,p:7.8,msg:3.0,out:6.5}, X=0.9, R=2.2;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const P=S.filter(s=>s.dataset.k==='p');
const prog=document.querySelector('.prog'); P.forEach(()=>{const i=document.createElement('i');i.appendChild(document.createElement('b'));prog.appendChild(i);});
const bars=[...prog.querySelectorAll('b')];
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const eio=v=>v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;
const back=v=>{const c=1.7;return 1+(c+1)*Math.pow(v-1,3)+c*Math.pow(v-1,2)};
const seg=(u,a,b)=>cl((u-a)/(b-a));
const qa=(s,sel)=>[...s.querySelectorAll(sel)];
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
// pregătire cerc ensō: lungimea traseului
document.querySelectorAll('.enso circle').forEach(c=>{const L=2*Math.PI*c.r.baseVal.value;c.dataset.L=L;c.style.strokeDasharray=c.getAttribute('stroke-dasharray')==='6 10'?'6 10':`${L*.88} ${L}`;});
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  if(!(u>=0&&u<=s.d+X)){s.style.display='none';return;}
  s.style.display='block'; s.style.zIndex=i;
  const sl=i>0?eio(seg(u,0,X)):1; s.style.transform=`translateX(${(1-sl)*100}%)`;
  const k=s.dataset.k;
  if(k==='intro'){
   fade(s.querySelector('.lg'),ease(seg(u,.1,.6)),0,-30);
   const b=s.querySelector('.big'); const c=b.querySelector('circle'); const L=2*Math.PI*180; c.style.strokeDasharray=`${L*.9} ${L}`; c.style.strokeDashoffset=`${L*.9*(1-ease(seg(u,.3,1.8)))}`; c.style.transform='rotate(-80deg)'; c.style.transformOrigin='200px 200px'; const yv=ease(seg(u,1.2,2.0)); b.querySelector('span').style.opacity=yv; b.querySelector('span').style.transform=`scale(${1.2-.2*yv})`;
   const st=s.querySelector('.stamp'); const sv=seg(u,2.0,2.3); st.style.opacity=sv?1:0; st.style.transform=`rotate(-8deg) scale(${sv?2.2-1.2*ease(sv):0})`;
   fade(s.querySelector('.t1'),ease(seg(u,2.4,3.0)),0,30);
   fade(s.querySelector('.t2'),ease(seg(u,2.8,3.4)),0,30);
   fade(s.querySelector('.mono'),ease(seg(u,3.2,3.8)),0,20);
  } else if(k==='p'){
   const tz=s.querySelector('.tz'); const tv=eio(seg(u,R,R+.9));
   tz.style.clipPath=`inset(0 0 ${tv*100}% 0)`;  // cortina urcă
   tz.querySelector('img').style.transform=`scale(${1.05+.08*seg(u,0,R)})`;
      fade(tz.querySelector('.jp'),ease(seg(u,.5,1.1)),0,16);
   fade(tz.querySelector('.qq'),ease(seg(u,.8,1.5)),0,40);
   tz.querySelector('.ln').style.width=`${140*ease(seg(u,1.2,1.9))}px`;
   fade(tz.querySelector('.no'),ease(seg(u,.3,.7)),0,-16);
   const w=u-R;
   s.querySelector('.photo img').style.transform=`scale(${1.12-.1*cl(w/(s.d-R))})`;
   fade(s.querySelector('.top'),ease(seg(w,0,.8)),0,-20);
   const ta=s.querySelector('.tate'); const tav=ease(seg(w,.3,1.0)); ta.style.opacity=tav; ta.style.transform=`translateY(${(1-tav)*-60}px)`;
   // ensō desenat
   const e=s.querySelector('.enso'); const ev=seg(w,.4,1.6); e.style.opacity=ev?1:0;
   e.querySelectorAll('circle').forEach((c,j)=>{const L=+c.dataset.L; if(j===0){c.style.strokeDashoffset=`${L*(1-ease(ev))}`;} else c.style.opacity=.9*ease(ev);});
   const pic=e.querySelector('.pic'); const pv=seg(w,.6,1.2); pic.style.transform=`scale(${pv?back(pv):0})`;
   fade(s.querySelector('.q'),ease(seg(w,.6,1.3)),-40,0);
   fade(s.querySelector('.a'),ease(seg(w,1.0,1.7)),40,0);
   qa(s,'.st').forEach((el,j)=>{const v=ease(seg(w,1.6+j*.6,2.3+j*.6)); el.style.opacity=v; el.style.transform=`translateY(${(1-v)*40}px)`;});
   const h=s.querySelector('.hanko'); const hv=seg(w,3.4,3.7); h.style.transform=`rotate(-4deg) scale(${hv?2-ease(hv):0})`;
   fade(s.querySelector('.foot .go'),ease(seg(w,3.5,4.0)),20,0);
   fade(s.querySelector('.foot .mono'),ease(seg(w,3.6,4.1)),0,0);
  } else if(k==='msg'){
   fade(s.querySelector('.mono'),ease(seg(u,.3,.9)),0,-20);
   fade(s.querySelector('.mt'),ease(seg(u,.5,1.4)),0,40);
   s.querySelector('.ml').style.width=`${160*ease(seg(u,1.0,1.8))}px`;
  } else {
   qa(s,'.lg,.k,.site,.qr,.ct div').forEach((e,j)=>{const v=ease(seg(u,.3+j*.35,1.1+j*.35)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*30}px)`;});
  }
 });
 const first=P[0].t0,last=P[P.length-1];
 prog.style.opacity=(t>=first&&t<=last.t0+last.d)?1:0;
 P.forEach((s,j)=>{bars[j].style.width=`${100*cl((t-s.t0)/(s.d-X))}%`;});
};
setT(0);
"""

html = (HEAD.replace('{t}', 'Deco&Flair Trend 2027 — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative;overflow:hidden">' + "".join(scenes)
        + '<div class="prog"></div>' + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

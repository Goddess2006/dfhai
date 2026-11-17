"""Reel NMC −30% (SIDDING PANEL 3 + NCL107) — reel/reel.html 1080x1920, paleta premium 2027.
Intro → chat Sidding (mesajele se scriu în timp real, indicator „scrie…”, cardul ofertei urcă) → mega Sidding
(„−30%” umplut cu imaginea) → chat NCL107 → mega NCL107 → final (logo, −30% până pe 30 noiembrie, QR spre landing, contact).
Rulare: python3 build.py && python3 reel_build.py && node reel_render.cjs
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

(ROOT / "reel").mkdir(exist_ok=True)
vb, qd = (ROOT / "assets" / "qr-bn.txt").read_text().split("\n", 1)

EXTRA = """
.sc{position:absolute;inset:0;overflow:hidden}
.sc .c{position:absolute;inset:0;height:1920px}
.typing{opacity:0}
.typing i{animation:none}
.io{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 80px;z-index:5}
.io .lg{width:180px;border-radius:14px}
.io .k{font-family:'Unbounded',sans-serif;font-weight:600;font-size:22px;letter-spacing:5px;text-transform:uppercase;margin-top:60px;color:var(--cream2)}
.io h1{font-family:'Unbounded',sans-serif;font-weight:800;font-size:86px;line-height:1.05;margin-top:30px;letter-spacing:-2px}
.io h2{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-size:86px;line-height:1.05;margin-top:6px}
.io p{font-size:34px;line-height:1.45;margin-top:40px;color:rgba(243,236,223,.85)}
.io .big{font-family:'Unbounded',sans-serif;font-weight:900;font-size:230px;line-height:1;letter-spacing:-10px;margin-top:30px}
.io .site{font-family:'Unbounded',sans-serif;font-weight:700;font-size:58px;margin-top:20px}
.io .qr{margin-top:40px;width:240px;height:240px;background:var(--cream);padding:16px;border-radius:18px;box-shadow:0 0 0 4px var(--forest2),0 0 60px rgba(185,163,189,.35)}
.io .qr svg{width:100%;height:100%;display:block}
.io .ct{margin-top:36px;font-size:30px;line-height:1.6;color:rgba(243,236,223,.9)}
.io .ct b{font-weight:800}
.io .mono{font-size:18px;letter-spacing:3px;text-transform:uppercase;color:var(--mauve);margin-top:14px}
"""


def sc(k, inner, extra_cls=""):
    return f'<div class="sc" data-k="{k}"><div class="c {extra_cls}">{inner.replace("src=\"assets/", "src=\"../assets/").replace("url(assets/", "url(../assets/")}</div></div>'


def chat_inner(k):
    html = build.chat(k)
    # indicator „scrie…” înaintea fiecărui răspuns NMC
    return html.replace('<div class="b bn">', '<div class="typing"><i></i><i></i><i></i></div><div class="b bn">')


scenes = [f"""<div class="sc" data-k="intro"><div class="c"><div class="mesh"></div><div class="grain"></div><div class="io">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<div class="k">Black November</div>
<h1>Fațada ta are<br>întrebări?</h1>
<h2 class="grad">Noi avem răspunsuri.</h2>
<p>Și o reducere de <b>−30%</b>.</p></div></div></div>""",
          sc("chat", chat_inner("sid"), "chat story"),
          sc("mega", build.mega("sid"), "mega story"),
          sc("chat", chat_inner("ncl"), "chat story"),
          sc("mega", build.mega("ncl"), "mega story"),
          f"""<div class="sc" data-k="out"><div class="c"><div class="mesh"></div><div class="grain"></div><div class="io">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<div class="big grad">−30%</div>
<div class="k" style="margin-top:10px">Până pe 30 noiembrie</div>
<div class="site">nmcromania.ro</div>
<div class="qr"><svg viewBox="{vb}"><path d="{qd}" fill="#0F1110"/></svg></div>
<div class="mono">Scanează · Black November</div>
<div class="ct">Consultanță gratuită: <b>021 319 35 35</b><br>În limita stocului disponibil</div></div></div></div>"""]

JS = r"""
const D={intro:3.6,chat:13.4,mega:6.0,out:6.0}, X=0.7;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const eio=v=>v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;
const back=v=>{const c=1.6;return 1+(c+1)*Math.pow(v-1,3)+c*Math.pow(v-1,2)};
const seg=(u,a,b)=>cl((u-a)/(b-a));
const qa=(s,sel)=>[...s.querySelectorAll(sel)];
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
// pregătește textul pentru scriere progresivă (doar bulele clientului, text simplu)
document.querySelectorAll('.b.bc').forEach(b=>{const w=b.querySelector('.who');const txt=b.textContent.replace(w.textContent,'').trim();b.dataset.full=txt;
  const span=document.createElement('span');span.className='tt';b.appendChild(span);[...b.childNodes].forEach(n=>{if(n.nodeType===3)n.remove();});});
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  if(!(u>=0&&u<=s.d+X)){s.style.display='none';return;}
  s.style.display='block'; s.style.zIndex=i;
  const o=i>0?ease(seg(u,0,X)):1; s.style.opacity=o; s.style.transform=`scale(${1.04-.04*o})`;
  const k=s.dataset.k;
  const mesh=s.querySelector('.mesh'); if(mesh) mesh.style.transform=`rotate(${u*2}deg) scale(1.1)`;
  if(k==='intro'||k==='out'){
   qa(s,'.io > *').forEach((e,j)=>{const v=ease(seg(u,.2+j*.3,.9+j*.3)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*30}px)`+(e.classList.contains('big')?` scale(${.7+.3*v})`:'');});
  } else if(k==='chat'){
   const amb=s.querySelector('.amb'); amb.style.transform=`scale(${1.12-.08*cl(u/s.d)})`;
   fade(s.querySelector('.top'),ease(seg(u,.2,.7)),0,-20); fade(s.querySelector('.note'),ease(seg(u,.4,.9)),0,0);
   // timeline mesaje
   let tt=0.9; const items=[...s.querySelector('.thread').children];
   items.forEach(e=>{
     if(e.classList.contains('typing')){const a=tt,b=tt+.9; const v=(u>=a&&u<b)?1:0; e.style.display=v?'flex':'none'; e.style.opacity=v;
       qa(e,'i').forEach((d,j)=>d.style.transform=`translateY(${-6*Math.max(0,Math.sin((u*7)-j*.8))}px)`); tt=b;}
     else if(e.classList.contains('bc')){const full=e.dataset.full; const dur=Math.min(2.0,full.length*.028); const v=seg(u,tt,tt+.25);
       e.style.display=u>=tt?'block':'none'; e.style.opacity=ease(v); e.style.transform=`translateY(${(1-ease(v))*20}px)`;
       const n=Math.round(full.length*seg(u,tt+.15,tt+.15+dur)); e.querySelector('.tt').textContent=full.slice(0,n)+(n<full.length&&u>=tt?'▍':''); tt+=dur+.6;}
     else {const v=seg(u,tt,tt+.35); e.style.display=u>=tt?'block':'none'; e.style.opacity=ease(v); e.style.transform=`translateY(${(1-ease(v))*24}px) scale(${.96+.04*ease(v)})`; tt+=1.5;}
   });
   const of=s.querySelector('.offer'); const ov=eio(seg(u,tt,tt+.7)); of.style.opacity=ov; of.style.transform=`translateY(${(1-ov)*200}px)`;
   const pc=s.querySelector('.pct'); const pv=seg(u,tt+.5,tt+.9); pc.style.transform=`scale(${pv?back(pv):0}) rotate(${(1-cl(pv))*-90}deg)`;
   fade(s.querySelector('.foot'),ease(seg(u,tt+.6,tt+1.1)),0,16);
  } else if(k==='mega'){
   fade(s.querySelector('.top'),ease(seg(u,.1,.6)),0,-20);
   const kk=s.querySelector('.kick'); fade(kk,ease(seg(u,.3,.9)),-40,0);
   const h=s.querySelector('.huge'), h2=s.querySelector('.huge2'); const hv=eio(seg(u,.5,1.4));
   h.style.opacity=hv; h.style.transform=`scale(${1.35-.35*hv})`; h.style.transformOrigin='30% 50%'; h.style.backgroundPosition=`${50-20*cl(u/s.d)}% 50%`;
   h2.style.opacity=ease(seg(u,1.1,1.6))*.9;
   const orb=s.querySelector('.orb'); const ob=seg(u,1.3,1.8); orb.style.transform=`scale(${ob?back(ob):0})`;
   qa(s,'.ps > div').forEach((e,j)=>fade(e,ease(seg(u,1.7+j*.5,2.3+j*.5)),-40,0));
   const pr=s.querySelector('.price'); fade(pr,ease(seg(u,2.7,3.3)),0,40);
   const pb=pr.querySelector('.pv b'); const pp=seg(u,3.3,3.8); pb.style.transform=`scale(${1+.1*Math.sin(Math.PI*pp)})`; pb.style.transformOrigin='100% 80%';
   fade(s.querySelector('.foot'),ease(seg(u,3.2,3.7)),0,16);
  }
 });
};
setT(0);
"""

html = (build.HEAD.replace('{t}', 'NMC −30% — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative;overflow:hidden">' + "".join(scenes)
        + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

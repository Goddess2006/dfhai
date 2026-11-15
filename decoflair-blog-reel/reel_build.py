"""Reel pentru promovarea blogului Deco&Flair (decoflair.ro/blog) — „Jurnalul Deco&Flair”.
Stil revistă: intro → 7 articole reale (imaginea principală a articolului + titlu + ce afli) → final cu QR spre blog și contact.
Ritm lent, lizibil. Rulare: python3 reel_build.py && node reel_render.cjs  → reel/decoflair-blog-reel.mp4
Titluri și imagini preluate de pe decoflair.ro/blog (15.11.2026).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
vb, qd = (ROOT / "assets" / "qr-blog.txt").read_text().split("\n", 1)

A = [
    dict(cat="Interior · Exterior", img="a1-detalii.jpg", pos="50% 50%",
         t="10 detalii arhitecturale care cresc valoarea percepută a unei locuințe",
         d="Detaliile pe care le observă orice musafir — și cum le aduci în casa ta.",
         url="decoflair.ro/blog/10-detalii-arhitecturale-care-cresc-valoarea-perceputa-a-unei-locuinte"),
    dict(cat="Apartament", img="a2-apartament.jpg", pos="50% 50%",
         t="Cum faci un apartament nou să nu arate ca toate celelalte",
         d="Idei concrete pentru personalitate într-un apartament standard."),
    dict(cat="Pereți", img="a3-chenare.jpg", pos="50% 50%",
         t="Chenare decorative pe perete: model, dimensiuni și proporții corecte",
         d="Regulile de proporție pe care le folosesc designerii, explicate simplu."),
    dict(cat="Lumină", img="a4-cornisa-led.jpg", pos="45% 50%",
         t="Cornișă LED pentru iluminare indirectă într-un interior elegant",
         d="Cum obții lumina caldă de hotel boutique, acasă."),
    dict(cat="Uși", img="a5-usa.jpg", pos="55% 50%",
         t="Cum transformi o ușă simplă într-un element arhitectural",
         d="Fără să o înlocuiești. Doar cu profile decorative."),
    dict(cat="Fațade", img="a6-fatade.jpg", pos="50% 50%",
         t="Cele mai frumoase fațade de case: 10 idei care dau personalitate",
         d="Combinații de profile care fac o casă să fie recunoscută din stradă."),
    dict(cat="Exterior", img="a7-gard.jpg", pos="45% 50%",
         t="Idei de gard pentru casă: 9 modele, construcție și amenajare",
         d="Prima impresie începe de la poartă."),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--washi:#F4F1EA;--ink:#1B1B1F;--mut:#6d675f;--red:#9E1F2A;--gold:#C9A869}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:Jost,sans-serif;background:var(--washi);color:var(--ink)}
.stage{position:relative;width:1080px;height:1920px;overflow:hidden}
.sc{position:absolute;inset:0;overflow:hidden;background:var(--washi);box-shadow:-40px 0 80px rgba(0,0,0,.25)}
.mono{font-family:'Space Mono',monospace;font-size:20px;letter-spacing:4px;text-transform:uppercase}
.fiber{position:absolute;inset:0;opacity:.35;background:repeating-linear-gradient(17deg,rgba(120,100,70,.05) 0 2px,transparent 2px 9px),repeating-linear-gradient(-23deg,rgba(120,100,70,.04) 0 1px,transparent 1px 13px)}
/* intro / outro */
.io{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}
.io .lg{width:330px;filter:brightness(.8) contrast(1.2)}
.io .kick{margin-top:70px;color:var(--red)}
.io h1{font-family:'Playfair Display',serif;font-weight:500;font-size:96px;line-height:1.05;margin-top:26px}
.io h1 i{color:var(--red);font-weight:600}
.io p{font-weight:300;font-size:40px;line-height:1.4;margin-top:40px;color:#3a352f}
.io .ln{width:0;height:2px;background:var(--ink);margin-top:50px}
.io .q{font-family:'Playfair Display',serif;font-style:italic;font-weight:500;font-size:78px;line-height:1.1}
.io .site{font-family:'Playfair Display',serif;font-weight:600;font-size:92px;margin-top:16px}
.io .qr{margin-top:40px;width:250px;height:250px;background:#fff;padding:16px;border-radius:14px;box-shadow:0 0 0 3px var(--ink)}
.io .qr svg{width:100%;height:100%;display:block}
.io .ct{margin-top:40px;display:flex;flex-direction:column;gap:12px;font-size:31px;font-weight:300}
.io .ct span{font-family:'Space Mono',monospace;font-size:19px;letter-spacing:3px;text-transform:uppercase;color:var(--red);margin-right:12px}
.io .ct b{font-weight:600}
/* pagină articol */
.ph{position:absolute;left:0;right:0;top:0;height:1180px;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover;transform-origin:50% 50%}
.ph::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,transparent 22%,transparent 85%,rgba(244,241,234,.3) 100%)}
.hdr{position:absolute;left:60px;right:60px;top:180px;display:flex;justify-content:space-between;align-items:center;color:#fff;z-index:3}
.hdr .chip{background:rgba(244,241,234,.92);border-radius:40px;padding:12px 22px}
.hdr .chip img{width:160px;display:block;filter:brightness(.8) contrast(1.2)}
.hdr .no{background:var(--ink);color:var(--washi);border-radius:40px;padding:12px 20px 10px}
.hdr .no b{color:var(--gold)}
.card{position:absolute;left:0;right:0;top:1100px;bottom:0;background:var(--washi);border-radius:40px 40px 0 0;padding:56px 70px 0;box-shadow:0 -20px 60px rgba(0,0,0,.18)}
.card .cat{display:inline-block;color:var(--red);border:1.5px solid var(--red);border-radius:30px;padding:9px 18px 7px}
.card h2{font-family:'Playfair Display',serif;font-weight:500;font-size:62px;line-height:1.1;margin-top:28px}
.card .d{font-weight:300;font-size:33px;line-height:1.4;margin-top:24px;color:#3a352f}
.card .go{position:absolute;left:70px;right:70px;bottom:300px;display:flex;align-items:center;gap:18px;border-top:1px solid rgba(27,27,31,.25);padding-top:22px}
.card .go span{font-size:28px;font-weight:300}
.card .go b{font-family:'Playfair Display',serif;font-weight:600;font-size:40px}
.card .go i{flex:1;height:2px;background:linear-gradient(90deg,var(--red),transparent)}
.prog{position:absolute;left:60px;right:60px;top:120px;display:flex;gap:8px;z-index:50}
.prog i{flex:1;height:5px;border-radius:3px;background:rgba(255,255,255,.45);overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.1)}
.prog i b{display:block;height:100%;width:0;background:var(--red)}
"""

scenes = ["""<div class="sc" data-k="intro"><div class="fiber"></div><div class="io">
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="q">Ai idei pentru casă,<br>dar nu știi de unde<br>să începi?</div>
<div class="ln"></div>
<div class="kick mono">Jurnalul Deco&amp;Flair</div>
<h1>Blogul care îți<br><i>face casa frumoasă.</i></h1>
<p>Ghiduri, proporții și idei,<br>explicate de oameni care fac asta zilnic.</p></div></div>"""]
for i, a in enumerate(A, 1):
    scenes.append(f"""<div class="sc" data-k="a">
<div class="ph"><img src="../assets/{a['img']}" style="object-position:{a['pos']}" alt=""></div>
<div class="hdr"><div class="chip"><img src="../assets/logo-decoflair.png" alt="Deco&amp;Flair"></div><div class="no mono">Articol <b>{i:02d}</b>/{len(A):02d}</div></div>
<div class="card"><div class="cat mono">{a['cat']}</div><h2>{a['t']}</h2><div class="d">{a['d']}</div>
<div class="go"><span>Citește pe</span><b>decoflair.ro/blog</b><i></i></div></div></div>""")
scenes.append(f"""<div class="sc" data-k="out"><div class="fiber"></div><div class="io">
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="q" style="margin-top:60px">Citește. Alege.<br>Transformă.</div>
<div class="site">decoflair.ro/blog</div>
<div class="qr"><svg viewBox="{vb}"><path d="{qd}" fill="#1B1B1F"/></svg></div>
<div class="mono" style="margin-top:18px;color:var(--red)">Scanează și citește</div>
<div class="ct"><div><span>Consultanță</span><b>0723 300 603</b></div>
<div><span>E-mail</span>office@decoflair.ro</div>
<div><span>Instagram</span>@decoflairhub</div></div></div></div>""")

JS = r"""
const D={intro:6.0,a:6.4,out:6.8}, X=0.9;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const Ar=S.filter(s=>s.dataset.k==='a');
const prog=document.querySelector('.prog'); Ar.forEach(()=>{const i=document.createElement('i');i.appendChild(document.createElement('b'));prog.appendChild(i);});
const bars=[...prog.querySelectorAll('b')];
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const eio=v=>v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;
const seg=(u,a,b)=>cl((u-a)/(b-a));
const qa=(s,sel)=>[...s.querySelectorAll(sel)];
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  if(!(u>=0&&u<=s.d+X)){s.style.display='none';return;}
  s.style.display='block'; s.style.zIndex=i;
  const sl=i>0?eio(seg(u,0,X)):1; s.style.transform=`translateX(${(1-sl)*100}%)`;
  const k=s.dataset.k;
  if(k==='intro'){
   fade(s.querySelector('.lg'),ease(seg(u,.2,.8)),0,-30);
   const q=s.querySelector('.q'); const qv=ease(seg(u,.5,1.3)); const qo=1-ease(seg(u,2.6,3.1));
   q.style.opacity=qv*qo; q.style.transform=`translateY(${(1-qv)*30}px)`; q.style.height=`${(1-ease(seg(u,2.9,3.4)))*260}px`; q.style.overflow='hidden';
   s.querySelector('.ln').style.width=`${160*ease(seg(u,1.2,2.0))}px`;
   fade(s.querySelector('.kick'),ease(seg(u,3.1,3.6)),0,20);
   fade(s.querySelector('h1'),ease(seg(u,3.3,4.1)),0,40);
   fade(s.querySelector('p'),ease(seg(u,3.9,4.6)),0,20);
  } else if(k==='a'){
   const im=s.querySelector('.ph img'); im.style.transform=`scale(${1.14-.12*cl(u/s.d)}) translateX(${-12*cl(u/s.d)}px)`;
   fade(s.querySelector('.hdr'),ease(seg(u,.5,1.1)),0,-20);
   const c=s.querySelector('.card'); const cv=eio(seg(u,.6,1.4)); c.style.transform=`translateY(${(1-cv)*420}px)`;
   fade(s.querySelector('.cat'),ease(seg(u,1.2,1.7)),-30,0);
   fade(s.querySelector('h2'),ease(seg(u,1.4,2.2)),0,30);
   fade(s.querySelector('.d'),ease(seg(u,2.3,3.0)),0,20);
   const g=s.querySelector('.go'); fade(g,ease(seg(u,3.0,3.6)),0,16);
   g.querySelector('i').style.transform=`scaleX(${ease(seg(u,3.3,4.2))})`; g.querySelector('i').style.transformOrigin='0 50%';
  } else {
   qa(s,'.lg,.q,.site,.qr,.mono,.ct div').forEach((e,j)=>{const v=ease(seg(u,.3+j*.35,1.1+j*.35)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*30}px)`;});
  }
 });
 const f=Ar[0].t0,l=Ar[Ar.length-1];
 prog.style.opacity=(t>=f&&t<=l.t0+l.d)?1:0;
 Ar.forEach((s,j)=>{bars[j].style.width=`${100*cl((t-s.t0)/(s.d-X))}%`;});
};
setT(0);
"""

html = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Deco&amp;Flair — Blog — Reel</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500;1,600'
        '&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"><style>' + CSS + '</style></head>'
        '<body><div class="stage">' + "".join(scenes) + '<div class="prog"></div></div>'
        f'<script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

"""Reel Deco&Flair „Ghidul de idei” v2 — reel/reel.html (1080x1920).
Coperta animată (arcade + uși care se deschid) → manifest + 10 idei (teaser-întrebare → dezvăluire, tranziție
tip pagină, bară de progres ca la Story, „Salvează ghidul”) → final cu logo, site, QR și date de contact.
Rulare: python3 cover.py && python3 reel_build.py && node reel_render.cjs
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402
import cover  # noqa: E402

(ROOT / "reel").mkdir(exist_ok=True)
vb, qd = (ROOT / "assets" / "qr-decoflair.txt").read_text().split("\n", 1)

TEASE = {
    "manifest": ("Manifest", "„Pe afară vopsit gardul,<br>înăuntru leopardul”?"),
    "01-tapet-carrara-82603": ("Ideea 01", "Pereți fără<br>personalitate?"),
    "02-tapet-carrara-82671": ("Ideea 02", "Un dormitor<br>prea obișnuit?"),
    "03-scafa-led-l5": ("Ideea 03", "Tavanul pare<br>prea jos?"),
    "04-cornisa-z11": ("Ideea 04", "Vrei să-i lași<br>fără cuvinte?"),
    "05-cornisa-z21": ("Ideea 05", "Sărbători într-o<br>casă banală?"),
    "06-brau-chenare-wo2": ("Ideea 06", "Lux pe pereți,<br>cu buget mic?"),
    "07-plinta-fd3": ("Ideea 07", "Ce lipsește<br>jos de tot?"),
    "08-cornisa-wt25": ("Ideea 08", "Minimalist,<br>dar nu rece?"),
    "09-ancadrament-na105": ("Ideea 09", "Cum arată casa ta<br>din stradă?"),
    "10-coltar-ncl106": ("Ideea 10", "Și seara,<br>la lumina felinarelor?"),
}

EXTRA = cover.COVER_CSS + """
.sc{position:absolute;inset:0;opacity:0;overflow:hidden;box-shadow:-40px 0 80px rgba(0,0,0,.35)}
.sc .c{position:absolute;inset:0;height:1920px}
.arch img{transform-origin:50% 60%}
.tz{position:absolute;inset:0;z-index:20;overflow:hidden}
.tz img{position:absolute;inset:-40px;width:calc(100% + 80px);height:calc(100% + 80px);object-fit:cover;filter:blur(18px) brightness(.45) saturate(.9)}
.tz .in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--cream);padding:0 80px}
.tz .mono{color:var(--gold2);font-weight:700;font-size:22px;letter-spacing:6px}
.tz .qq{font-family:'Playfair Display',serif;font-style:italic;font-weight:500;font-size:96px;line-height:1.08;margin-top:26px}
.tz .ln{width:120px;height:2px;background:var(--gold2);margin-top:40px}
.prog{position:absolute;left:60px;right:60px;top:120px;display:flex;gap:8px;z-index:50}
.prog i{flex:1;height:5px;border-radius:3px;background:rgba(255,255,255,.35);overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.08)}
.prog i b{display:block;height:100%;width:0;background:var(--gold2)}
.save{position:absolute;right:60px;top:360px;z-index:60;background:var(--red);color:#fff;border-radius:40px;padding:18px 28px 16px;
 font-family:'Space Mono',monospace;font-weight:700;font-size:22px;letter-spacing:2px;text-transform:uppercase;box-shadow:0 14px 40px rgba(0,0,0,.4);opacity:0}
.out{position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,rgba(158,31,42,.5),transparent 55%),radial-gradient(circle at 50% 100%,rgba(201,168,105,.25),transparent 50%),var(--onyx);
 color:var(--cream);display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:300px}
.out .lg{width:420px}
.out .k{font-family:'Playfair Display',serif;font-style:italic;font-size:58px;margin-top:60px;line-height:1.1}
.out .site{font-family:'Playfair Display',serif;font-weight:600;font-size:110px;margin-top:20px;color:#fff}
.out .qr{margin-top:46px;width:250px;height:250px;background:var(--cream);padding:18px;border-radius:16px;box-shadow:0 0 0 3px var(--gold2),0 0 60px rgba(214,188,132,.35)}
.out .qr svg{width:100%;height:100%;display:block}
.out .scan{margin-top:20px;color:var(--gold2)}
.out .ct{margin-top:46px;display:flex;flex-direction:column;gap:14px;font-size:32px;font-weight:300}
.out .ct b{font-weight:600}
.out .ct span{color:var(--gold2);font-family:'Space Mono',monospace;font-size:20px;letter-spacing:3px;text-transform:uppercase;margin-right:14px}
"""

scenes = ['<div class="sc cv" data-k="cover"><div class="c">'
          + cover.cover(doors_open=False).replace('src="assets/', 'src="../assets/') + '</div></div>']


def teaser(key, img, pos):
    lab, q = TEASE[key]
    return (f'<div class="tz"><img src="../assets/{img}" style="object-position:{pos}" alt="">'
            f'<div class="in"><div class="mono">{lab}</div><div class="qq">{q}</div><div class="ln"></div></div></div>')


scenes.append('<div class="sc light man story" data-k="p">' + teaser("manifest", "amb-interior.jpg", "45% 30%")
              + '<div class="c">' + build.manifest().replace('src="assets/', 'src="../assets/') + '</div></div>')
for i, p in enumerate(build.P, 1):
    inner = build.scene(p, i).replace('src="assets/', 'src="../assets/')
    scenes.append(f'<div class="sc {p["theme"]}" data-k="p">' + teaser(p["slug"], p["amb"], p["pos"])
                  + f'<div class="c">{inner}</div></div>')
scenes.append(f"""<div class="sc" data-k="out"><div class="out">
<img class="lg" src="../assets/logo-decoflair.png" alt="Deco&amp;Flair">
<div class="k">Ideile complete te așteaptă pe</div>
<div class="site">decoflair.ro</div>
<div class="qr"><svg viewBox="{vb}"><path d="{qd}" fill="#121115"/></svg></div>
<div class="scan mono">Scanează și intră în ghid</div>
<div class="ct"><div><span>Consultanță</span><b>0723 300 603</b></div>
<div><span>E-mail</span>office@decoflair.ro</div>
<div><span>Program</span>Luni – Vineri · 07:30 – 16:00</div>
<div><span>Instagram</span>@decoflairhub</div></div></div></div>""")

JS = r"""
const D={cover:4.4,p:3.9,out:5.2}, X=0.55;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const P=S.filter(s=>s.dataset.k==='p');
const prog=document.querySelector('.prog'); P.forEach(()=>{const i=document.createElement('i');i.appendChild(document.createElement('b'));prog.appendChild(i);});
const bars=[...prog.querySelectorAll('b')]; const save=document.querySelector('.save');
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const eio=v=>v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;
const back=v=>{const c=1.6;return 1+(c+1)*Math.pow(v-1,3)+c*Math.pow(v-1,2)};
const seg=(u,a,b)=>cl((u-a)/(b-a));
const qa=(s,sel)=>[...s.querySelectorAll(sel)];
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
const R=1.25; // momentul dezvăluirii în fiecare idee
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  let vis=u>=0&&u<=s.d+X; if(!vis){s.style.display='none';return;}
  s.style.display='block'; s.style.opacity=1;
  // tranziție tip pagină: intră din dreapta
  const sl=i>0?eio(seg(u,0,X)):1; s.style.transform=`translateX(${(1-sl)*100}%)`; s.style.zIndex=i;
  const k=s.dataset.k;
  if(k==='cover'){
   qa(s,'.ring').forEach((e,j)=>{const v=ease(seg(u,.1+j*.15,.9+j*.15)); e.style.opacity=v; e.style.transform=`translateX(-50%) scale(${.85+.15*v})`;});
   const h=ease(seg(u,0,1.2)); s.querySelector('.halo').style.opacity=h;
   fade(s.querySelector('.pre'),ease(seg(u,.2,.9)),0,-30);
   const op=eio(seg(u,1.0,2.2));
   s.querySelector('.leaf.l').style.transform=`perspective(1400px) rotateY(${-100*op}deg)`;
   s.querySelector('.leaf.r').style.transform=`perspective(1400px) rotateY(${100*op}deg)`;
   s.querySelector('.door img').style.transform=`scale(${1.25-.25*op})`;
   const tt=s.querySelector('.ttl'); fade(tt.querySelector('.mono'),ease(seg(u,1.6,2.1)),0,20);
   const h1=tt.querySelector('h1'); const hv=ease(seg(u,1.8,2.5)); h1.style.opacity=hv; h1.style.letterSpacing=`${(1-hv)*30-1}px`;
   fade(tt.querySelector('p'),ease(seg(u,2.3,2.9)),0,20);
   qa(s,'.chap span').forEach((e,j)=>{const v=seg(u,2.6+j*.08,3.0+j*.08); e.style.opacity=v; e.style.transform=`scale(${v?back(v):0})`;});
   fade(s.querySelector('.bot'),ease(seg(u,3.0,3.5)),0,20);
  } else if(k==='p'){
   // teaser
   const tz=s.querySelector('.tz'); const tv=ease(seg(u,R,R+.45));
   tz.style.opacity=1-tv; tz.querySelector('.in').style.transform=`scale(${1+.25*tv})`;
   tz.querySelector('img').style.transform=`scale(${1+.08*seg(u,0,R)})`;
   fade(tz.querySelector('.mono'),ease(seg(u,.35,.75)),0,20);
   const qq=tz.querySelector('.qq'); const qv=ease(seg(u,.45,1.0)); qq.style.opacity=qv; qq.style.transform=`translateY(${(1-qv)*40}px)`;
   tz.querySelector('.ln').style.width=`${120*ease(seg(u,.6,1.1))}px`;
   // creativul
   const w=u-R+.2;
   qa(s,'.arch,.arches div').forEach((e,j)=>{const v=ease(seg(w,j*.1,.6+j*.1)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*60}px)`;});
   qa(s,'.arch img,.arches img').forEach(e=>e.style.transform=`scale(${1.15-.13*cl(w/(s.d-R))})`);
   const m=seg(w,.35,.8); const me=s.querySelector('.medal'); if(me){me.style.transform=`scale(${m?back(m):0}) rotate(${(1-cl(m))*-40}deg)`;}
   fade(s.querySelector('.room'),ease(seg(w,.3,.7)),-30,0);
   fade(s.querySelector('.q'),ease(seg(w,.3,.7)),0,20);
   fade(s.querySelector('.h'),ease(seg(w,.45,1.0)),0,40);
   fade(s.querySelector('.prod'),ease(seg(w,.7,1.1)),0,20);
   fade(s.querySelector('.idea'),ease(seg(w,.85,1.35)),0,24);
   fade(s.querySelector('.proof'),ease(seg(w,1.1,1.5)),0,10);
   const ft=s.querySelector('.foot'); fade(ft,ease(seg(w,1.2,1.6)),0,16);
   const sale=ft.querySelector('.sale'); const sv=seg(w,1.6,2.0); sale.style.transform=`scale(${1+.12*Math.sin(Math.PI*sv)})`;
   fade(s.querySelector('.side'),ease(seg(w,0,.6)),0,0);
   fade(s.querySelector('.top'),ease(seg(w,0,.5)),0,-16);
  } else {
   qa(s,'.lg,.k,.site,.qr,.scan,.ct div').forEach((e,j)=>{const v=ease(seg(u,.2+j*.22,.8+j*.22)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*30}px)${e.classList.contains('qr')?` scale(${.8+.2*v})`:''}`;});
  }
 });
 // bară de progres
 const first=P[0].t0, last=P[P.length-1];
 prog.style.opacity=(t>=first&&t<=last.t0+last.d)?1:0;
 P.forEach((s,j)=>{bars[j].style.width=`${100*cl((t-s.t0)/(s.d-X))}%`;});
 // „Salvează ghidul” — apare la ideea 05
 const sv=P[5]; const su=t-sv.t0-R-.6; const so=seg(su,0,.4)*(1-seg(su,2.6,3.0));
 save.style.opacity=so; save.style.transform=`scale(${so?back(seg(su,0,.4)):0})`;
};
setT(0);
"""

html = (build.HEAD.replace('{t}', 'Deco&Flair — Ghidul de idei — Reel').replace('</style>', EXTRA + '</style>')
        + '<body class="story"><div class="c" style="position:relative;overflow:hidden">' + "".join(scenes)
        + '<div class="prog"></div><div class="save">🔖 Salvează ghidul</div>'
        + f'</div><script>{JS}</script></body></html>')
(ROOT / "reel" / "reel.html").write_text(html)
print("reel.html ok")

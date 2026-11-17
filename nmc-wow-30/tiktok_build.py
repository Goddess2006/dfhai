"""TikTok NMC −30% (SIDDING PANEL 3 + NCL107) — 1080x1920, ~25 s, două variante:
  ads     → final „Apasă «Cumpără acum» ↓” (butonul nativ TikTok Ads, link setat în Ads Manager)
  organic → final „Link în bio” + QR spre landing
Zone sigure TikTok: sus ~160 px, dreapta ~140 px (iconițe), jos ~420 px (descriere + buton reclamă).
Etichete de produs animate pe imagine (pin + card preț). Paletă premium 2027 (verde forest, crem, mov, roz pal).
Rulare: python3 tiktok_build.py && node tiktok_render.cjs
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

OUT = ROOT / "tiktok"
OUT.mkdir(exist_ok=True)
vb, qd = (ROOT / "assets" / "qr-bn.txt").read_text().split("\n", 1)
S, N = build.PROD["sid"], build.PROD["ncl"]

CSS = build.CSS + """
html,body{height:1920px}
.stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--ink)}
.sc{position:absolute;inset:0;overflow:hidden}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,17,16,.65) 0%,rgba(15,17,16,0) 22%,rgba(15,17,16,0) 50%,rgba(15,17,16,.85) 78%,var(--ink) 100%)}
.tint{position:absolute;inset:0;background:linear-gradient(160deg,rgba(30,58,46,.45),rgba(74,42,71,.30) 60%,rgba(15,17,16,.35));mix-blend-mode:multiply}
.brand{position:absolute;left:60px;top:170px;display:flex;align-items:center;gap:16px;z-index:20}
.brand img{width:110px;border-radius:10px}
.brand .pill{font-size:15px}
.hook{position:absolute;left:60px;right:160px;top:620px;font-family:'Unbounded',sans-serif;font-weight:800;font-size:92px;line-height:1.02;letter-spacing:-2px;z-index:10;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.hook i{display:block;font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-size:84px;letter-spacing:0}
.stamp{position:absolute;right:170px;top:400px;width:230px;height:230px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:11;
 font-family:'Unbounded',sans-serif;font-weight:900;font-size:56px;color:var(--ink);letter-spacing:-2px;
 background:conic-gradient(from 200deg,#F3ECDF,#E8D3CD,#B9A3BD,#CDBB9A,#F3ECDF);box-shadow:0 0 0 8px rgba(30,58,46,.85),0 0 70px rgba(185,163,189,.5)}
.q{position:absolute;left:60px;right:160px;top:300px;z-index:10;padding:24px 28px;border-radius:30px;border-bottom-left-radius:8px;background:rgba(243,236,223,.95);color:#1d1f1c;font-size:34px;line-height:1.3;box-shadow:0 14px 40px rgba(0,0,0,.35)}
.q small{display:block;font-size:15px;letter-spacing:2px;text-transform:uppercase;opacity:.6;margin-bottom:6px;font-weight:600}
.a{position:absolute;left:180px;right:160px;top:500px;z-index:10;padding:24px 28px;border-radius:30px;border-bottom-right-radius:8px;color:var(--cream);font-size:32px;line-height:1.3;
 background:linear-gradient(125deg,#2F5242,#1E3A2E 45%,#4A2A47);border:1px solid rgba(232,211,205,.35);box-shadow:0 14px 40px rgba(0,0,0,.35)}
.a b{color:#E8D3CD}
.a small{display:block;font-size:15px;letter-spacing:2px;text-transform:uppercase;opacity:.7;margin-bottom:6px;font-weight:600}
/* eticheta de produs */
.pin{position:absolute;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:var(--cream);z-index:12;box-shadow:0 0 0 6px rgba(243,236,223,.35)}
.pin::after{content:"";position:absolute;inset:-26px;border-radius:50%;border:3px solid rgba(243,236,223,.8)}
.tag{position:absolute;z-index:13;display:flex;align-items:center;gap:18px;padding:16px 22px 16px 16px;border-radius:26px;
 background:rgba(15,17,16,.72);border:1px solid rgba(243,236,223,.45);backdrop-filter:blur(14px);box-shadow:0 18px 50px rgba(0,0,0,.5)}
.tag .th{width:110px;height:110px;border-radius:16px;overflow:hidden;background:#fff;flex:none}
.tag .th img{width:100%;height:100%;object-fit:cover}
.tag .nm{font-family:'Unbounded',sans-serif;font-weight:700;font-size:28px;line-height:1.05}
.tag .pr{display:flex;align-items:baseline;gap:12px;margin-top:8px}
.tag .pr s{font-size:20px;color:rgba(243,236,223,.6);text-decoration-color:#B9A3BD;text-decoration-thickness:2px}
.tag .pr b{font-family:'Unbounded',sans-serif;font-weight:800;font-size:40px}
.tag .pr span{font-size:16px;color:rgba(243,236,223,.8)}
.tag .go{width:56px;height:56px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;background:var(--cream);color:var(--ink);font-size:30px;font-weight:800}
.tag .off{position:absolute;top:-18px;right:-14px;font-family:'Unbounded',sans-serif;font-weight:800;font-size:18px;color:var(--ink);padding:8px 12px;border-radius:20px;
 background:linear-gradient(90deg,#F3ECDF,#E8D3CD,#B9A3BD)}
/* final */
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;padding:200px 160px 0 60px;text-align:center;z-index:5}
.end .lg{width:150px;border-radius:12px}
.end h3{font-family:'Unbounded',sans-serif;font-weight:800;font-size:64px;line-height:1.05;margin-top:40px;letter-spacing:-1px}
.end h3 i{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;display:block;font-size:64px;letter-spacing:0}
.cards{display:flex;gap:22px;margin-top:44px;width:100%}
.cards .cd{flex:1;border-radius:26px;overflow:hidden;background:rgba(243,236,223,.08);border:1px solid rgba(243,236,223,.35);text-align:left}
.cards .cd img{width:100%;height:230px;object-fit:cover;background:#fff;display:block}
.cards .cd div{padding:16px 18px}
.cards .cd b{display:block;font-family:'Unbounded',sans-serif;font-weight:700;font-size:24px}
.cards .cd s{font-size:18px;color:rgba(243,236,223,.6);text-decoration-color:#B9A3BD}
.cards .cd em{font-style:normal;font-family:'Unbounded',sans-serif;font-weight:800;font-size:38px;display:block;margin-top:4px}
.cta{margin-top:40px;font-family:'Unbounded',sans-serif;font-weight:700;font-size:40px;line-height:1.15}
.cta small{display:block;font-family:Inter,sans-serif;font-weight:400;font-size:24px;letter-spacing:2px;text-transform:uppercase;color:var(--mauve);margin-top:12px}
.arrow{position:absolute;left:50%;bottom:330px;width:90px;height:150px;margin-left:-45px;z-index:6}
.qrbox{display:flex;align-items:center;gap:24px;margin-top:30px;text-align:left}
.qrbox .qr{width:190px;height:190px;background:var(--cream);padding:12px;border-radius:16px;flex:none}
.qrbox .qr svg{width:100%;height:100%;display:block}
.qrbox span{font-size:26px;line-height:1.4;color:rgba(243,236,223,.9)}
.bnote{position:absolute;left:60px;top:250px;z-index:20}
"""


def tag(p, x, y, tx, ty):
    return (f'<div class="pin" style="left:{x}px;top:{y}px"></div>'
            f'<div class="tag" style="left:{tx}px;top:{ty}px"><span class="off">−30%</span>'
            f'<div class="th"><img src="../assets/{p["img"]}" alt=""></div>'
            f'<div><div class="nm">{p["name"]}</div><div class="pr"><s>{p["old"]}</s><b class="grad">{p["new"]}</b><span>lei</span></div></div>'
            f'<div class="go">→</div></div>')


BRAND = '<div class="brand"><img src="../assets/nmc-logo.png" alt="nmc"><div class="pill">Black November · <b>−30%</b></div></div>'


def page(variant):
    hook = f"""<div class="sc" data-k="hook"><img class="bg" src="../assets/{S['amb']}" style="object-position:40% 50%" alt="">
<div class="tint"></div><div class="shade"></div>{BRAND}
<div class="stamp">−30%</div>
<div class="hook">Fațada ta<br>arată obosită?<i class="grad">Avem răspunsul.</i></div></div>"""
    sid = f"""<div class="sc" data-k="p"><img class="bg" src="../assets/{S['amb']}" style="object-position:40% 50%" alt="">
<div class="tint"></div><div class="shade"></div>{BRAND}
<span class="note bnote">{S['amb_note']}</span>
<div class="q"><small>Tu</small>Fațada arată obosită și iarna simt frigul.</div>
<div class="a"><small>NMC</small><b>SIDDING PANEL 3</b>: finisaj decorativ + termoizolație. Se lipește direct pe fațadă.</div>
{tag(S, 300, 1060, 60, 1180)}</div>"""
    ncl = f"""<div class="sc" data-k="p"><img class="bg" src="../assets/{N['amb']}" style="object-position:50% 50%" alt="">
<div class="tint"></div><div class="shade"></div>{BRAND}
<span class="note bnote">{N['amb_note']}</span>
<div class="q"><small>Tu</small>Colțurile casei arată plate.</div>
<div class="a"><small>NMC</small><b>Colțarul NCL107</b>: relief și umbre. Rezistent la UV, ger și umezeală.</div>
{tag(N, 690, 920, 60, 1180)}</div>"""
    if variant == "ads":
        cta = ('<div class="cta">Apasă <span class="grad">„Cumpără acum”</span><small>Prețuri speciale până pe 30 noiembrie</small></div>'
               '<svg class="arrow" viewBox="0 0 90 150" fill="none" stroke="#F3ECDF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
               '<path d="M45 10v120M15 100l30 32 30-32"/></svg>')
    else:
        cta = ('<div class="cta">Link în bio <span class="grad">↗</span><small>sau scanează codul</small></div>'
               f'<div class="qrbox"><div class="qr"><svg viewBox="{vb}"><path d="{qd}" fill="#0F1110"/></svg></div>'
               '<span>nmcromania.ro/<br>black-november<br><b>Până pe 30 noiembrie</b></span></div>')
    end = f"""<div class="sc" data-k="end"><div class="mesh"></div><div class="grain"></div><div class="end">
<img class="lg" src="../assets/nmc-logo.png" alt="nmc">
<h3>Două probleme.<i class="grad">Două soluții −30%.</i></h3>
<div class="cards"><div class="cd"><img src="../assets/{S['img']}" alt=""><div><b>{S['name']}</b><s>{S['old']} lei</s><em class="grad">{S['new']} lei</em></div></div>
<div class="cd"><img src="../assets/{N['img']}" alt=""><div><b>{N['name']}</b><s>{N['old']} lei</s><em class="grad">{N['new']} lei</em></div></div></div>
{cta}</div></div>"""
    JS = r"""
const D={hook:2.8,p:7.6,end:%END%}, X=0.45;
const S=[...document.querySelectorAll('.sc')];
let t0=0; S.forEach(s=>{s.t0=t0; s.d=D[s.dataset.k]; t0+=s.d-X;});
window.TOTAL=t0+X;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=v=>1-Math.pow(1-v,3);
const eio=v=>v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;
const back=v=>{const c=1.7;return 1+(c+1)*Math.pow(v-1,3)+c*Math.pow(v-1,2)};
const seg=(u,a,b)=>cl((u-a)/(b-a));
const qa=(s,sel)=>[...s.querySelectorAll(sel)];
function fade(e,v,dx,dy){if(!e)return;e.style.opacity=v;e.style.transform=`translate(${(1-v)*dx}px,${(1-v)*dy}px)`;}
window.setT=function(t){
 S.forEach((s,i)=>{const u=t-s.t0;
  if(!(u>=0&&u<=s.d+X)){s.style.display='none';return;}
  s.style.display='block'; s.style.zIndex=i;
  const sl=i>0?eio(seg(u,0,X)):1; s.style.transform=`translateY(${(1-sl)*100}%)`;  // swipe în sus, ca pe TikTok
  const k=s.dataset.k; const bg=s.querySelector('.bg'); if(bg) bg.style.transform=`scale(${1.15-.1*cl(u/s.d)})`;
  const m=s.querySelector('.mesh'); if(m) m.style.transform=`rotate(${u*3}deg) scale(1.15)`;
  if(k==='hook'){
   fade(s.querySelector('.brand'),ease(seg(u,0,.4)),0,-20);
   qa(s,'.hook').forEach(h=>{const v=ease(seg(u,.05,.55)); h.style.opacity=v; h.style.transform=`scale(${1.2-.2*v})`; h.style.transformOrigin='0 50%';});
   const st=s.querySelector('.stamp'); const sv=seg(u,.7,1.05); st.style.opacity=sv?1:0; st.style.transform=`rotate(-12deg) scale(${sv?2.4-1.4*ease(sv):0})`;
  } else if(k==='p'){
   fade(s.querySelector('.brand'),1,0,0); fade(s.querySelector('.note'),ease(seg(u,.4,.8)),0,0);
   const q=s.querySelector('.q'); const qv=ease(seg(u,.3,.7)); q.style.opacity=qv; q.style.transform=`translateY(${(1-qv)*30}px) scale(${.94+.06*qv})`;
   const a=s.querySelector('.a'); const av=ease(seg(u,1.6,2.0)); a.style.opacity=av; a.style.transform=`translateY(${(1-av)*30}px) scale(${.94+.06*av})`;
   const pin=s.querySelector('.pin'); const pv=seg(u,3.0,3.3); pin.style.transform=`scale(${pv?back(pv):0})`;
   pin.style.setProperty('--r',0); const ring=(u*1.4)%1; pin.style.boxShadow=`0 0 0 ${6+28*ring}px rgba(243,236,223,${.45*(1-ring)})`;
   const tg=s.querySelector('.tag'); const tv=eio(seg(u,3.3,3.9)); tg.style.opacity=tv; tg.style.transform=`translateY(${(1-tv)*120}px) scale(${.9+.1*tv})`;
   const go=tg.querySelector('.go'); const gp=seg(u,4.6,5.4); go.style.transform=`translateX(${10*Math.sin(Math.PI*2*gp)}px)`;
  } else {
   qa(s,'.end > *').forEach((e,j)=>fade(e,ease(seg(u,.15+j*.3,.75+j*.3)),0,30));
   qa(s,'.cd').forEach((e,j)=>{const v=ease(seg(u,.75+j*.25,1.3+j*.25)); e.style.opacity=v; e.style.transform=`translateY(${(1-v)*60}px)`;});
   const ar=s.querySelector('.arrow'); if(ar){const v=ease(seg(u,1.9,2.4)); ar.style.opacity=v; ar.style.transform=`translateY(${16*Math.sin(u*5)}px)`;}
  }
 });
};
setT(0);
""".replace('%END%', '5.6' if variant == 'ads' else '6.2')
    return ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>NMC −30% TikTok — ' + variant + '</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800;900&family=Instrument+Serif:ital@1'
            '&family=Inter:wght@400;600;800&display=swap" rel="stylesheet"><style>' + CSS + '</style></head>'
            '<body class="story"><div class="stage">' + hook + sid + ncl + end + f'</div><script>{JS}</script></body></html>')


for v in ("ads", "organic"):
    (OUT / f"tiktok-{v}.html").write_text(page(v))
print("ok")

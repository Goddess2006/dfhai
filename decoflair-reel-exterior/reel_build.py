"""Reel exterior Deco&Flair v3 — „Casa ta are ceva să-ți spună.” (IG/TikTok/Meta Ads, 1080x1920, ~24 s).

Cererea clientului: imagini REALE la început (grafica plictisește și pare AI), culori noi, ceva care surprinde, creativ care „vorbește”.
Concept: fațada e personajul. Pe fotografii reale de case, casa vorbește cu privitorul prin subtitrări cuvânt-cu-cuvânt
(formatul de „subtitrare cinetică” din reclamele japoneze, coreene și americane), cu umor românesc, apoi cu produsul real,
prețul și stocul. Paletă nouă: albastru cobalt electric, alb osos, negru. Finalul „2030” păstrat, recolorat în cobalt.

Scene: hook „Psst. Da, tu.” → schele „acum o lună” → ancadramente → colțare → materialul → brâu/cornișă → „vecinii mă întreabă…”
→ „Le-am zis: decoflair.ro” → final 2030.
Rulare: python3 reel_build.py && node reel_render.cjs organic|ads
"""
from pathlib import Path
import json, random, math

ROOT = Path(__file__).resolve().parent
(ROOT / "reel").mkdir(exist_ok=True)


def asset(fallback, codex=None):
    if codex and (ROOT / "codex" / codex).exists():
        return f"../codex/{codex}"
    return f"../assets/{fallback}"


# fiecare scenă: imagine reală, poziție, replici (cuvinte; *cuvânt* = evidențiat), etichetă produs (opțional)
# date produs verificate pe decoflair.ro la 24.11.2026
SCENES = [
    dict(img=asset("r-conac.jpg", "r01-conac-9x16.jpg"), pos="50% 50%", lines=["Psst… *tu.*", "Sunt *casa* ta. Ascultă-mă puțin."], tag=None, d=4.4, src="foto reală · portofoliu decoflair.ro"),
    dict(img=asset("r-schele.jpg", "r02-schele-9x16.jpg"), pos="62% 50%", lines=["Acum o lună eram doar", "*schele* și polistiren."], tag=("ÎNAINTE", "", ""), d=4.2, src="foto reală"),
    dict(img=asset("r-ancadramente.jpg", "r03-ancadramente-9x16.jpg"), pos="45% 50%", lines=["Mi-au pus *ancadramente.*", "Acum arăt *îngrijită.*"], tag=("Ancadrament NA102", "de la 71 lei", "1.733 în stoc"), d=4.2, src="foto reală"),
    dict(img=asset("cx-ncl107.jpg"), pos="50% 50%", lines=["Colțurile mele erau *ciupite.*", "Acum par din *piatră.*"], tag=("Colțar NCL107", "248 lei/buc", "2.135 în stoc"), d=4.2, src=""),
    dict(img=asset("cx-nc104.jpg"), pos="50% 30%", lines=["O *cornișă* sub acoperiș…", "și parcă am *întinerit.*"], tag=("Cornișă NC104", "194 lei", "185 în stoc"), d=4.2, src=""),
    dict(img=asset("cx-st105.jpg"), pos="50% 50%", lines=["Până și *gardul*", "arată ca nou."], tag=("Capac gard ST105", "200 lei", "18 în stoc"), d=4.0, src=""),
    dict(img=asset("cx-seara.jpg", "r07-vecini-9x16.jpg"), pos="50% 50%", lines=["Vecinii mă întreabă", "de unde m-am *aranjat.*", "Le-am zis:"], tag=("Din stoc", "livrare în 3–5 zile", ""), d=5.0, src=""),
]
T_FINAL = sum(s["d"] for s in SCENES)
TOTAL = round(T_FINAL + 5.8, 2)

VARIANTS = {"organic": dict(foot="Link în bio"), "ads": dict(foot="")}

random.seed(21)
MOTES = [[round(random.random()*1080,1), round(random.random()*1920,1), round(random.uniform(2,6),1), round(random.uniform(12,40),1), round(random.random()*6.28,2), round(random.uniform(.15,.55),2)] for _ in range(70)]
PARTS = []
for i in range(170):
    ang = random.random() * math.tau
    PARTS.append([round(540 + math.cos(ang) * random.uniform(500, 1100), 1), round(930 + math.sin(ang) * random.uniform(600, 1300), 1),
                  round(random.uniform(330, 430), 1), round(ang, 3), round(random.uniform(2, 5), 1), round(random.uniform(.25, .7), 2)])

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--co:#2340FF;--co2:#6E86FF;--bone:#F5F1E8;--ink:#0A0A0B}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Manrope,sans-serif;color:#fff}
.sc{position:absolute;inset:0;overflow:hidden;opacity:0}
.bg{position:absolute;inset:-40px;background-size:cover;background-repeat:no-repeat;filter:contrast(1.06) saturate(1.05)}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 45%,rgba(0,0,0,.55) 100%),linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,0) 22%,rgba(0,0,0,0) 48%,rgba(0,0,0,.55) 72%,rgba(0,0,0,.7))}
#grain{position:absolute;inset:-200px;background:url(../assets/grain.png);background-size:540px 960px;opacity:.10;mix-blend-mode:overlay;z-index:60;pointer-events:none}
#mist{position:absolute;inset:-300px;z-index:52;pointer-events:none;opacity:0;background:radial-gradient(ellipse 55% 35% at 30% 40%,rgba(235,240,255,.75),rgba(235,240,255,0) 70%),radial-gradient(ellipse 50% 30% at 75% 62%,rgba(200,210,255,.6),rgba(200,210,255,0) 70%),radial-gradient(ellipse 70% 45% at 50% 50%,rgba(255,255,255,.35),rgba(255,255,255,0) 70%);filter:blur(30px)}
#motes{position:absolute;inset:0;z-index:53;pointer-events:none}
#motes i{position:absolute;left:0;top:0;border-radius:50%;background:#F4F1FF;box-shadow:0 0 12px rgba(160,175,255,.9)}
#flash{position:absolute;inset:0;background:#fff;opacity:0;z-index:55;pointer-events:none}
/* subtitrare cinetică */
.cap{position:absolute;left:60px;right:60px;top:1060px;text-align:center;z-index:5}
.ln{display:block;margin:0 auto 18px;font-size:72px;line-height:1.14;font-weight:800;letter-spacing:-1px;text-shadow:0 4px 30px rgba(0,0,0,.75);opacity:0}
.w{display:inline-block;margin:0 .13em;white-space:nowrap}
.w.hl{background:var(--co);color:#fff;padding:0 .18em;border-radius:10px;text-shadow:none;box-shadow:0 10px 40px rgba(35,64,255,.55)}
.who{position:absolute;left:0;right:0;top:985px;text-align:center;font-size:24px;letter-spacing:8px;font-weight:800;color:var(--bone);opacity:.85;z-index:5}
.src{position:absolute;right:60px;top:330px;font-size:18px;letter-spacing:3px;font-weight:700;color:rgba(255,255,255,.7);text-transform:uppercase;z-index:6}
.who b{display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--co);margin-right:12px;box-shadow:0 0 16px var(--co)}
/* etichetă produs (sticker) */
.tag{position:absolute;left:60px;top:250px;display:flex;flex-direction:column;gap:6px;background:var(--bone);color:var(--ink);border-radius:22px;padding:18px 26px;z-index:6;box-shadow:0 18px 50px rgba(0,0,0,.4);transform-origin:left top}
.tag .n{font-size:34px;font-weight:800;letter-spacing:-.5px}
.tag .p{font-size:30px;font-weight:800;color:var(--co)}
.tag .s{font-size:24px;font-weight:800;color:#0a7a3e}
.tag.solo{background:var(--co);color:#fff}
.tag.solo .n{font-size:36px;letter-spacing:5px}
.wm{position:absolute;top:255px;right:60px;font-size:20px;letter-spacing:7px;font-weight:800;z-index:6;opacity:.9;display:flex;align-items:center;gap:12px}
.wm i{width:3px;height:24px;background:var(--co);display:block}
.bar{position:absolute;top:215px;left:60px;right:60px;height:5px;display:flex;gap:6px;z-index:6}
.bar span{flex:1;background:rgba(255,255,255,.28);border-radius:3px;overflow:hidden}
.bar span i{display:block;height:100%;width:0;background:#fff}
/* zbor decoflair.ro din subtitrare spre final */
#fly{position:absolute;left:0;right:0;top:1345px;text-align:center;font-family:Unbounded,sans-serif;font-weight:800;font-size:76px;color:#fff;z-index:58;opacity:0;text-shadow:0 0 30px rgba(110,134,255,.9)}
/* final 2030 (cobalt) */
#s9{background:#020309}
#glow{position:absolute;left:50%;top:930px;width:1500px;height:1500px;margin:-750px 0 0 -750px;border-radius:50%;background:radial-gradient(circle,rgba(35,64,255,.42) 0%,rgba(35,64,255,.16) 30%,rgba(0,0,0,0) 62%)}
#beam{position:absolute;left:-600px;top:-200px;width:520px;height:2400px;background:linear-gradient(90deg,transparent,rgba(190,205,255,.20),transparent);mix-blend-mode:screen}
#ring{position:absolute;left:50%;top:930px;border-radius:50%;border:2px solid rgba(150,170,255,.95);box-shadow:0 0 44px rgba(35,64,255,.8),inset 0 0 40px rgba(35,64,255,.45)}
#ring2{position:absolute;left:50%;top:930px;border-radius:50%;border:1px solid rgba(255,255,255,.45)}
#parts i{position:absolute;left:0;top:0;border-radius:50%;background:#EEF2FF;box-shadow:0 0 10px rgba(130,150,255,.95)}
#site{position:absolute;left:0;right:0;top:860px;text-align:center;font-family:Unbounded,sans-serif;font-weight:800;font-size:122px;line-height:1.1;
  background:linear-gradient(100deg,#7d8bd6 0%,#fff 18%,#9fb0ff 32%,#ffffff 46%,#5f74ff 60%,#ffffff 74%,#b9c4ff 100%);background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent}
#wm5{position:absolute;left:0;right:0;top:790px;display:flex;justify-content:center}
#wm5 .wm{position:static}
#tag1{position:absolute;left:0;right:0;top:1025px;text-align:center;font-size:52px;font-weight:700;color:#fff;letter-spacing:-.5px}
#tag2{position:absolute;left:0;right:0;top:1100px;text-align:center;font-size:26px;font-weight:800;letter-spacing:6px;color:var(--co2);text-transform:uppercase}
#foot{position:absolute;left:0;right:0;top:1340px;text-align:center;font-size:28px;font-weight:700;color:rgba(255,255,255,.7);letter-spacing:3px}
#flare{position:absolute;left:50%;top:930px;width:900px;height:6px;margin-left:-450px;background:radial-gradient(ellipse,rgba(255,255,255,.95),rgba(140,160,255,0) 70%);filter:blur(2px)}
"""

JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const out=x=>1-Math.pow(1-cl(x),3);
const expo=x=>{x=cl(x);return x==1?1:1-Math.pow(2,-10*x)};
const back=x=>{x=cl(x);const c1=1.8,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
const vis=(el,o)=>el.style.opacity=o;
function rise(el,t,a,d=.45,dist=30){const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.transform=`translateY(${(1-k)*dist}px)`}
window.TOTAL=TOTAL;
// starturi scene
const ST=[];{let a=0;SC.forEach(s=>{ST.push(a);a+=s.d});}
window.setT=function(t){
  // granulație de film animată
  $('#grain').style.transform=`translate(${(Math.floor(t*24)*37)%200-100}px,${(Math.floor(t*24)*53)%200-100}px)`;
  let mist=0;
  SC.forEach((s,i)=>{const a=ST[i], e=a+s.d, el=$('#sc'+i);
    const start=i==0?0:a-.6, end=(i==SC.length-1)? e+1.0 : e+.8;
    const on=t>=start&&t<end; el.style.display=on?'block':'none'; el.style.opacity=1; el.style.zIndex=i+1;
    if(!on) return;
    const lt=t-a;
    if(i>0){const k=ease(seg(t,a-.6,a+.8)); const R=-35+175*k;
      el.style.webkitMaskImage=el.style.maskImage=k>=1?'none':`radial-gradient(circle at 50% 44%, #000 ${R}%, rgba(0,0,0,0) ${R+32}%)`;
      mist=Math.max(mist, Math.sin(Math.PI*seg(t,a-.7,a+1.0)));}
    const ex=seg(t,e-.6,e+.8);
    const bg=el.querySelector('.bg');
    bg.style.transform=`scale(${1.06+.08*seg(lt,-0.6,s.d+.8)}) translate(${Math.sin((t+i)*.25)*12}px,${Math.cos((t+i)*.2)*10}px)`;
    bg.style.filter=`contrast(1.05) saturate(${1.02-.25*ex}) brightness(${1+.18*ex}) blur(${ex*8}px)`;
    const L=el.querySelectorAll('.ln'); const gap=Math.min(1.1,(s.d-2.2)/Math.max(1,L.length-1));
    L.forEach((ln,j)=>{const la=a+.55+j*gap; const k=out(seg(t,la,la+.9));
      const fade=(i==SC.length-1)?1:1-seg(t,e-.7,e-.05);
      ln.style.opacity=k*fade; ln.style.filter=`blur(${(1-k)*12}px)`; ln.style.letterSpacing=`${(1-k)*6-1}px`; ln.style.transform=`translateY(${(1-k)*18}px)`;});
    const who=el.querySelector('.who'); who.style.opacity=.85*out(seg(t,a+.3,a+1))*(1-seg(t,e-.7,e-.05));
    const tg=el.querySelector('.tag'); if(tg){const k=out(seg(t,a+1.4,a+2.3)); tg.style.opacity=k*(1-seg(t,e-.6,e)); tg.style.transform=`translateY(${(1-k)*-14}px) scale(${.96+.04*k})`; tg.style.filter=`blur(${(1-k)*6}px)`;}
    const src=el.querySelector('.src'); if(src) src.style.opacity=out(seg(t,a+.8,a+1.6))*(1-seg(t,e-.6,e));
    el.querySelectorAll('.bar i').forEach((x,j)=>{x.style.width=(j<i?100:j==i?seg(t,a,e)*100:0)+'%'});
  });
  const tfm=Math.sin(Math.PI*seg(t,T_FINAL-.6,T_FINAL+1.2));
  vis($('#mist'), .06+.55*Math.max(mist,tfm));
  $('#mist').style.transform=`translate(${Math.sin(t*.35)*80}px,${Math.cos(t*.27)*60}px) scale(${1.05+.05*Math.sin(t*.4)})`;
  $$('#motes i').forEach((m,i)=>{const d=MOTES[i]; const y=((d[1]-t*d[3])%1980+1980)%1980-30, x=d[0]+Math.sin(t*.5+d[4])*30;
    m.style.transform=`translate(${x}px,${y}px)`; m.style.opacity=d[5]*(.55+.45*Math.sin(t*1.3+d[4]))*(t<T_FINAL?1:1-seg(t,T_FINAL,T_FINAL+1));});
  vis($('#flash'), 0);
  // „decoflair.ro” sare din subtitrare în final
  const tf=T_FINAL, fk=seg(t,tf-.5,tf+.9); const fly=$('#fly');
  fly.style.opacity = out(seg(t,tf-1.3,tf-.6))*(t<tf+.9?1:1-seg(t,tf+.9,tf+1.2));
  fly.style.transform=`translateY(${-485*ease(fk)}px) scale(${1+ .6*ease(fk)})`; fly.style.letterSpacing=`${ease(seg(t,tf+.2,tf+.9))*8}px`; fly.style.filter=`blur(${ease(seg(t,tf+.4,tf+1.1))*8}px)`;
  // final 2030
  const S=$('#s9'); vis(S, t>=tf?1:0);
  const T=t-tf;
  vis($('#glow'), out(seg(T,0,1.2))*(.85+.15*Math.sin(t*2.2)));
  $('#beam').style.transform=`translateX(${-200+2200*seg(T,.3,2.4)}px) rotate(18deg)`;
  $$('#parts i').forEach((p,i)=>{const d=PARTS[i]; const k=ease(seg(T,0,1.6)); const ang=d[3]+T*.35;
    const rx=540+Math.cos(ang)*d[2], ry=930+Math.sin(ang)*d[2]*.42;
    const x=d[0]+(rx-d[0])*k, y=d[1]+(ry-d[1])*k; p.style.transform=`translate(${x}px,${y}px)`; p.style.opacity=d[5]*out(seg(T,0,.4))*(1-.6*seg(T,3.2,4.8));});
  const rk=expo(seg(T,.6,1.9)); const R=80+720*rk; const ring=$('#ring');
  ring.style.width=ring.style.height=R+'px'; ring.style.margin=`${-R/2}px 0 0 ${-R/2}px`; ring.style.opacity=(1-rk)*.9+.08;
  const R2=60+560*expo(seg(T,.8,2.3)); const r2=$('#ring2'); r2.style.width=r2.style.height=R2+'px'; r2.style.margin=`${-R2/2}px 0 0 ${-R2/2}px`; r2.style.opacity=.6*(1-seg(T,1.3,2.7));
  const sk2=out(seg(T,.3,1.1)); const site=$('#site');
  site.style.opacity=sk2; site.style.letterSpacing=`${(1-sk2)*30}px`; site.style.filter=`blur(${(1-sk2)*10}px) drop-shadow(0 0 26px rgba(35,64,255,.55))`;
  site.style.backgroundPosition=`${100-100*seg(T,.8,3.2)}% 0`;
  const fl=seg(T,1.6,2.4); vis($('#flare'), Math.sin(Math.PI*fl)); $('#flare').style.transform=`scaleX(${.3+fl})`;
  rise($('#wm5'),t,tf+1.2,.5,20); rise($('#tag1'),t,tf+1.8,.5,30); rise($('#tag2'),t,tf+2.3,.5,20); rise($('#foot'),t,tf+2.8,.5,20);
};
"""


def words(line):
    out = []
    for w in line.split(" "):
        hl = w.startswith("*")
        w = w.replace("*", "")
        out.append(f'<span class="w{" hl" if hl else ""}">{w}</span>')
    return f'<span class="ln">{"".join(out)}</span>'


def scene_html(i, s):
    bars = "".join("<span><i></i></span>" for _ in SCENES)
    tag = ""
    if s["tag"]:
        n, p, st = s["tag"]
        if p:
            tag = f'<div class="tag"><div class="n">{n}</div><div class="p">{p}</div>{f"<div class=s>✓ {st}</div>" if st else ""}</div>'
        else:
            tag = f'<div class="tag solo"><div class="n">{n}</div></div>'
    return f"""<div class="sc" id="sc{i}"><div class="bg" style="background-image:url('{s['img']}');background-position:{s['pos']}"></div><div class="vig"></div>
  <div class="bar">{bars}</div><div class="wm"><i></i>DECO &amp; FLAIR</div>{tag}
  <div class="who"><b></b>CASA</div>{f'<div class="src">{s["src"]}</div>' if s.get("src") else ""}<div class="cap">{"".join(words(l) for l in s['lines'])}</div></div>"""


def page(v):
    V = VARIANTS[v]
    parts = "".join(f'<i style="width:{p[4]}px;height:{p[4]}px"></i>' for p in PARTS)
    motes = "".join(f'<i style="width:{m[2]}px;height:{m[2]}px"></i>' for m in MOTES)
    sc = "\n".join(scene_html(i, s) for i, s in enumerate(SCENES))
    return f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Unbounded:wght@800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>
{sc}
<div class="sc" id="s9" style="z-index:40"><div id="glow"></div><div id="beam"></div><div id="ring2"></div><div id="ring"></div><div id="parts">{parts}</div>
  <div id="wm5" style="opacity:0"><div class="wm"><i></i>DECO &amp; FLAIR</div></div>
  <div id="site">decoflair.ro</div><div id="flare"></div>
  <div id="tag1" style="opacity:0">Fațada care vorbește pentru tine.</div>
  <div id="tag2" style="opacity:0">Profile de exterior · din stoc</div>
  <div id="foot" style="opacity:0">{V['foot']}</div>
</div>
<div id="fly">decoflair.ro</div><div id="mist"></div><div id="motes">{motes}</div><div id="flash"></div><div id="grain"></div>
<script>const SC={json.dumps([dict(d=s['d']) for s in SCENES])};const T_FINAL={T_FINAL};const TOTAL={TOTAL};const PARTS={json.dumps(PARTS)};const MOTES={json.dumps(MOTES)};{JS}
setT(0);</script></body></html>"""


for v in VARIANTS:
    (ROOT / "reel" / f"reel-{v}.html").write_text(page(v), encoding="utf-8")
print("OK", list(VARIANTS), "durată", TOTAL, "s; final la", T_FINAL)

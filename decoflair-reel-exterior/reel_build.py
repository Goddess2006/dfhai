"""Reel exterior Deco&Flair v2 — „Schița devine casă” (IG/TikTok/Meta Ads, 1080x1920, 23 s). Fără zăpadă.

  0,0–2,4  CÂRLIG     tipografie cinetică: „Casa ta e frumoasă.” → „Dar îi lipsesc 5 detalii.”
  2,4–11,6 SCHIȚA     plan tehnic animat: fațada se desenează, apoi cele 5 profile „se montează” pe rând (nume, preț real, foto produs)
 11,6–14,4 REALITATE  linie de scanare: schița devine casa reală, în lumină aurie
 14,4–18,2 STOC       contoare HUD: 2.135 colțare · 1.733 ancadramente · 519 chei de boltă → din stoc, 3–5 zile, gata de sărbători
 18,2–23,0 FINAL 2030 decoflair.ro centrat: particule care converg, inel de lumină, fascicul, text metalic cu reflex
Variante: organic (cu „link în bio”) și ads (fără nimic în zona butonului). Rulare: python3 reel_build.py && node reel_render.cjs organic|ads
"""
from pathlib import Path
import json, random, math

ROOT = Path(__file__).resolve().parent
(ROOT / "reel").mkdir(exist_ok=True)


def asset(fallback, codex=None):
    if codex and (ROOT / "codex" / codex).exists():
        return f"../codex/{codex}"
    return f"../assets/{fallback}"


REAL = asset("a-vila.jpg", "03-fatada-aurie.jpg")

# date verificate pe decoflair.ro la 24.11.2026
STEPS = [  # (id element svg, nume, cod, preț, imagine)
    ("el-cornisa", "Cornișă", "NC104", "194", "../assets/p-nc104-main.jpg"),
    ("el-coltar", "Colțar cu bosaje", "NCL107", "248", "../assets/p-ncl107-hero-crop.jpg"),
    ("el-ancadr", "Ancadrament", "NA102", "71", "../assets/p-na102-main.jpg"),
    ("el-solbanc", "Solbanc", "NS110", "118", "../assets/p-ns110-closeup.jpg"),
    ("el-cheie", "Cheie de boltă", "NCB104", "87", "../assets/p-ncb104-main.jpg"),
]
STOCK = [("2135", "colțare NCL107"), ("1733", "ancadramente NA102"), ("519", "chei de boltă NCB104")]

VARIANTS = {"organic": dict(foot="Link în bio"), "ads": dict(foot="")}

# ---------------------------------------------------------------- fațada SVG (coordonate în cadrul 1080x1920)
X0, X1, Y_ROOF, Y_TOP, Y_BOT = 150, 930, 560, 720, 1360
WIN = [(270, 800, 140, 170), (670, 800, 140, 170), (270, 1090, 140, 170), (670, 1090, 140, 170)]
DOOR = (480, 1110, 120, 250)


def facade_svg():
    L = []
    line = 'fill="none" stroke="#CFE3DA" stroke-width="3" pathLength="1" class="draw"'
    # grilă
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1920" />' for x in range(0, 1081, 60)) + \
           "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" />' for y in range(0, 1921, 60))
    L.append(f'<g id="grid" stroke="rgba(207,227,218,.08)" stroke-width="1">{grid}</g>')
    # contur casă
    L.append(f'<path {line} d="M{X0} {Y_BOT} L{X0} {Y_TOP} L{X1} {Y_TOP} L{X1} {Y_BOT} Z"/>')
    L.append(f'<path {line} d="M{X0 - 50} {Y_TOP} L540 {Y_ROOF} L{X1 + 50} {Y_TOP}"/>')
    L.append(f'<path {line} d="M{X0 - 80} {Y_BOT} L{X1 + 80} {Y_BOT}"/>')
    for x, y, w, h in WIN:
        L.append(f'<path {line} d="M{x} {y} h{w} v{h} h{-w} Z M{x + w / 2} {y} v{h} M{x} {y + h * .45} h{w}"/>')
    x, y, w, h = DOOR
    L.append(f'<path {line} d="M{x} {Y_BOT} V{y} h{w} V{Y_BOT} M{x + w / 2} {y} V{Y_BOT}"/>')
    # cote
    L.append(f'<path {line} stroke="rgba(214,188,132,.7)" stroke-width="2" d="M{X0} {Y_BOT + 50} H{X1} M{X0} {Y_BOT + 38} v24 M{X1} {Y_BOT + 38} v24"/>')
    iv = 'fill="#F1E7D3" stroke="#B9A67F" stroke-width="1.5"'
    # 1 cornișă
    L.append(f'<g id="el-cornisa" class="el"><path {iv} d="M{X0 - 30} {Y_TOP - 6} H{X1 + 30} V{Y_TOP + 26} H{X1 + 8} V{Y_TOP + 42} H{X0 - 8} V{Y_TOP + 26} H{X0 - 30} Z"/>'
             f'<path stroke="#B9A67F" stroke-width="2" d="M{X0 - 8} {Y_TOP + 34} H{X1 + 8}"/></g>')
    # 2 colțare (bosaje alternante)
    q = []
    y, i = Y_TOP + 42, 0
    while y < Y_BOT - 10:
        hb = 62
        for xc, side in ((X0, 1), (X1, -1)):
            w = 70 if i % 2 == 0 else 48
            xx = xc if side == 1 else xc - w
            q.append(f'<rect {iv} x="{xx}" y="{y + 3}" width="{w}" height="{hb - 6}" rx="2"/>')
        y += hb
        i += 1
    L.append(f'<g id="el-coltar" class="el">{"".join(q)}</g>')
    # 3 ancadramente
    a = "".join(f'<path {iv} fill-rule="evenodd" d="M{x - 22} {y - 22} h{w + 44} v{h + 22} h{-(w + 44)} Z M{x} {y} h{w} v{h} h{-w} Z"/>' for x, y, w, h in WIN)
    L.append(f'<g id="el-ancadr" class="el">{a}</g>')
    # 4 solbancuri
    s = "".join(f'<rect {iv} x="{x - 36}" y="{y + h}" width="{w + 72}" height="20" rx="2"/><rect {iv} x="{x - 28}" y="{y + h + 20}" width="{w + 56}" height="10"/>' for x, y, w, h in WIN)
    L.append(f'<g id="el-solbanc" class="el">{s}</g>')
    # 5 chei de boltă
    k = "".join(f'<path {iv} d="M{x + w / 2 - 22} {y - 46} h44 l-8 50 h-28 Z"/>' for x, y, w, h in WIN)
    L.append(f'<g id="el-cheie" class="el">{k}</g>')
    return f'<svg id="plan" viewBox="0 0 1080 1920" width="1080" height="1920">{"".join(L)}</svg>'


random.seed(11)
PARTS = []
for i in range(160):
    ang = random.random() * math.tau
    PARTS.append([round(540 + math.cos(ang) * random.uniform(500, 1100), 1), round(930 + math.sin(ang) * random.uniform(600, 1300), 1),
                  round(random.uniform(330, 420), 1), round(ang, 3), round(random.uniform(2, 5), 1), round(random.uniform(.2, .6), 2)])

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--g:#1F3A2F;--g0:#0E1C16;--gold:#D6BC84;--ink:#141412;--mint:#CFE3DA}
html,body{width:1080px;height:1920px;overflow:hidden;background:#050607;font-family:Manrope,sans-serif;color:#fff}
.sc{position:absolute;inset:0;overflow:hidden;opacity:0}
.serif{font-family:'Cormorant Garamond',serif;font-weight:600}
.wm{font-size:22px;letter-spacing:7px;font-weight:700;display:flex;align-items:center;gap:14px}
.wm i{display:block;width:3px;height:26px;background:#9E1F2A}
/* cârlig */
#s1{background:radial-gradient(ellipse at 50% 40%,#22423a,#0E1C16 70%)}
.kin{position:absolute;left:72px;right:72px;font-size:120px;line-height:1.0}
.five{color:var(--gold);font-family:Unbounded,sans-serif;font-weight:800}
/* plan */
#s2{background:radial-gradient(ellipse at 50% 50%,#1b3a30 0%,#0E1C16 75%)}
#plan{position:absolute;inset:0}
.cota{fill:rgba(214,188,132,.85);font:700 22px Manrope;letter-spacing:5px}
.el{opacity:0;transform-box:fill-box;transform-origin:center}
.step-n{position:absolute;top:250px;left:72px;font-size:26px;letter-spacing:6px;font-weight:800;color:var(--gold)}
.step-t{position:absolute;top:292px;left:72px;right:72px;font-size:104px;line-height:1}
.chip{position:absolute;left:72px;top:1440px;display:flex;align-items:center;gap:20px;background:rgba(244,238,228,.97);color:var(--ink);border-radius:24px;padding:12px 28px 12px 12px;box-shadow:0 0 0 1px rgba(214,188,132,.6),0 20px 60px rgba(0,0,0,.45)}
.chip .im{width:120px;height:120px;border-radius:14px;background:#fff center/cover no-repeat}
.chip .k{font-size:19px;letter-spacing:3px;text-transform:uppercase;color:#7A5B22;font-weight:800}
.chip .v{font-size:52px;font-weight:800;line-height:1.05}
.chip .v small{font-size:24px}
.dots{position:absolute;top:262px;right:72px;display:flex;gap:10px}
.dots i{width:14px;height:14px;border-radius:50%;border:2px solid var(--gold)}
/* realitate */
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.scan{position:absolute;left:0;right:0;height:6px;background:linear-gradient(90deg,transparent,#fff,transparent);box-shadow:0 0 40px 10px rgba(214,188,132,.8)}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.45) 24%,rgba(0,0,0,0) 40%,rgba(0,0,0,0) 62%,rgba(0,0,0,.7))}
/* stoc */
#s4{background:#07110d}
.hud{position:absolute;left:72px;right:72px}
.cnt{font-family:Unbounded,sans-serif;font-weight:800;font-size:150px;line-height:1;color:#fff;letter-spacing:-4px}
.cnt-l{font-size:34px;font-weight:700;color:var(--mint);letter-spacing:2px;margin-top:6px}
.hline{height:2px;background:linear-gradient(90deg,var(--gold),transparent);margin:26px 0 30px;transform-origin:left}
.pillg{display:inline-block;margin:10px 12px 0 0;padding:14px 26px;border-radius:40px;border:2px solid rgba(214,188,132,.7);font-size:34px;font-weight:800}
/* final 2030 */
#s5{background:#030405}
#glow{position:absolute;left:50%;top:930px;width:1400px;height:1400px;margin:-700px 0 0 -700px;border-radius:50%;background:radial-gradient(circle,rgba(214,188,132,.28) 0%,rgba(46,82,68,.25) 30%,rgba(0,0,0,0) 62%)}
#beam{position:absolute;left:-600px;top:-200px;width:500px;height:2400px;background:linear-gradient(90deg,transparent,rgba(255,240,210,.18),transparent);transform-origin:center;mix-blend-mode:screen}
#ring{position:absolute;left:50%;top:930px;border-radius:50%;border:2px solid rgba(214,188,132,.9);box-shadow:0 0 40px rgba(214,188,132,.6),inset 0 0 40px rgba(214,188,132,.35)}
#ring2{position:absolute;left:50%;top:930px;border-radius:50%;border:1px solid rgba(207,227,218,.5)}
#parts i{position:absolute;left:0;top:0;border-radius:50%;background:#FFF4DC;box-shadow:0 0 10px rgba(255,220,160,.9)}
#site{position:absolute;left:0;right:0;top:860px;text-align:center;font-family:Unbounded,sans-serif;font-weight:800;font-size:122px;line-height:1.1;
  background:linear-gradient(100deg,#9a8a68 0%,#fff 18%,#D6BC84 32%,#fff6e2 46%,#b79a62 60%,#ffffff 74%,#D6BC84 100%);background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 24px rgba(214,188,132,.35))}
#wm5{position:absolute;left:0;right:0;top:790px;display:flex;justify-content:center}
#tag{position:absolute;left:0;right:0;top:1025px;text-align:center;font-size:44px;font-weight:600;color:#fff}
#tag2{position:absolute;left:0;right:0;top:1100px;text-align:center;font-size:26px;font-weight:700;letter-spacing:6px;color:var(--gold);text-transform:uppercase}
#foot{position:absolute;left:0;right:0;top:1340px;text-align:center;font-size:28px;font-weight:700;color:rgba(255,255,255,.7);letter-spacing:3px}
#flare{position:absolute;left:50%;top:930px;width:900px;height:6px;margin-left:-450px;background:radial-gradient(ellipse,rgba(255,255,255,.95),rgba(255,220,160,0) 70%);filter:blur(2px)}
"""

JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const out=x=>1-Math.pow(1-cl(x),3);
const expo=x=>{x=cl(x);return x==1?1:1-Math.pow(2,-10*x)};
const back=x=>{x=cl(x);const c1=1.7,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
const vis=(el,o)=>el.style.opacity=o;
function rise(el,t,a,d=.4,dist=60){const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.transform=`translateY(${(1-k)*dist}px)`}
function pop(el,t,a,d=.4){const k=seg(t,a,a+d);el.style.opacity=cl(k*2);el.style.transform=`scale(${.7+.3*back(k)})`}
function blurIn(el,t,a,d=.5){const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.filter=`blur(${(1-k)*18}px)`;el.style.transform=`scale(${1.12-.12*k})`}
window.TOTAL=23.0;
const S0=3.9, SD=1.5;  // primul profil la 3,9 s, câte 1,5 s
window.setT=function(t){
  // 1 cârlig
  vis($('#s1'), t<2.55?1:0);
  blurIn($('#k1'),t,.05,.45); $('#k1').style.opacity=Math.min(+$('#k1').style.opacity,1-seg(t,1.05,1.2));
  blurIn($('#k2'),t,1.15,.4);
  const f=$('#five'); const fk=seg(t,1.45,1.9); f.style.display='inline-block'; f.style.transform=`scale(${1+.6*Math.sin(Math.PI*fk)})`;
  $('#s1').style.clipPath=`inset(0 0 ${ease(seg(t,2.2,2.55))*100}% 0)`;
  // 2 plan
  const S2=$('#s2'); vis(S2, t>=2.2&&t<14.4?1:0);
  $('#grid').style.opacity=seg(t,2.3,2.8);
  $$('.draw').forEach((p,i)=>{const k=ease(seg(t,2.45+i*.07,3.35+i*.07)); p.style.strokeDasharray='1'; p.style.strokeDashoffset=1-k;});
  $$('.cota').forEach(c=>c.style.opacity=seg(t,3.2,3.6));
  STEPS.forEach((s,i)=>{const a=S0+i*SD, el=$('#'+s[0]);
    const k=seg(t,a,a+.45); el.style.opacity=cl(k*2);
    el.style.transform=`translateY(${(1-out(k))*-40}px) scale(${1+.08*(1-out(k))})`;
    const active=t>=a&&t<a+SD; el.style.filter= active? `drop-shadow(0 0 ${10+8*Math.sin(t*8)}px rgba(214,188,132,.95))` : 'drop-shadow(0 6px 8px rgba(0,0,0,.35))';
    const lab=$('#lab'+i); const on=t>=a-.02&&t<a+SD-.02 || (i==STEPS.length-1&&t>=a&&t<11.4);
    lab.style.display=on?'block':'none'; if(on){rise(lab.querySelector('.step-t'),t,a,.35,40); vis(lab.querySelector('.step-n'),out(seg(t,a,a+.25))); pop(lab.querySelector('.chip'),t,a+.25,.35)}
    $$('.dots i')[i].style.background = t>=a? 'var(--gold)':'transparent';
  });
  // zoom lent pe plan
  $('#plan').style.transform=`scale(${1+.05*seg(t,2.4,11.6)})`;
  $('.dots').style.opacity=seg(t,3.7,4)*(1-seg(t,11.3,11.6));
  // 3 realitate (scanare de jos în sus)
  const S3=$('#s3'); vis(S3, t>=11.5&&t<14.55?1:0); S3.style.zIndex=20;
  const sk=ease(seg(t,11.6,12.6)); S3.style.clipPath=`inset(${(1-sk)*100}% 0 0 0)`;
  $('#scan').style.top=((1-sk)*1920-3)+'px'; vis($('#scan'), sk>0&&sk<1?1:0);
  $('#s3 .bg').style.transform=`scale(${1.12-.08*seg(t,11.6,14.4)})`;
  rise($('#r1'),t,12.3,.45); rise($('#r2'),t,12.75,.45);
  // 4 stoc
  const S4=$('#s4'); vis(S4, t>=14.3&&t<18.4?out(seg(t,14.3,14.55)):0); S4.style.zIndex=21;
  STOCK.forEach((s,i)=>{const a=14.55+i*.45; const box=$('#st'+i); rise(box,t,a,.4,50);
    const n=Math.round(+s[0]*expo(seg(t,a,a+1.1))); box.querySelector('.cnt').textContent=n.toLocaleString('ro-RO');
    box.querySelector('.hline').style.transform=`scaleX(${out(seg(t,a+.2,a+.9))})`;});
  rise($('#g1'),t,16.4,.4,30); rise($('#g2'),t,16.8,.4,30); rise($('#hudt'),t,14.45,.4,30);
  // 5 final 2030
  const S5=$('#s5'); vis(S5, t>=18.2?1:0); S5.style.zIndex=22;
  const T=t-18.2;
  vis($('#glow'), out(seg(T,0,1.2))*(.85+.15*Math.sin(t*2.2)));
  $('#beam').style.transform=`translateX(${-200+2200*seg(T,.3,2.4)}px) rotate(18deg)`;
  $$('#parts i').forEach((p,i)=>{const d=PARTS[i]; const k=ease(seg(T,0,1.6)); const ang=d[3]+T*.35;
    const rx=540+Math.cos(ang)*d[2], ry=930+Math.sin(ang)*d[2]*.42;
    const x=d[0]+(rx-d[0])*k, y=d[1]+(ry-d[1])*k; p.style.transform=`translate(${x}px,${y}px)`; p.style.opacity=d[5]*out(seg(T,0,.4))*(1-.6*seg(T,3.2,4.8)) + (k>.98?.15*Math.sin(t*6+i):0);});
  const rk=expo(seg(T,.9,2.2)); const R=80+720*rk; const ring=$('#ring');
  ring.style.width=ring.style.height=R+'px'; ring.style.margin=`${-R/2}px 0 0 ${-R/2}px`; ring.style.opacity=(1-rk)*.9+.08;
  const R2=60+560*expo(seg(T,1.1,2.6)); const r2=$('#ring2'); r2.style.width=r2.style.height=R2+'px'; r2.style.margin=`${-R2/2}px 0 0 ${-R2/2}px`; r2.style.opacity=.6*(1-seg(T,1.6,3));
  const sk2=out(seg(T,1.0,1.9)); const site=$('#site');
  site.style.opacity=sk2; site.style.letterSpacing=`${(1-sk2)*60}px`; site.style.filter=`blur(${(1-sk2)*14}px) drop-shadow(0 0 24px rgba(214,188,132,.35))`;
  site.style.backgroundPosition=`${100-100*seg(T,1.4,3.6)}% 0`;
  const fl=seg(T,2.1,2.9); vis($('#flare'), Math.sin(Math.PI*fl)); $('#flare').style.transform=`scaleX(${.3+fl})`;
  rise($('#wm5'),t,18.2+1.6,.5,20); rise($('#tag'),t,18.2+2.2,.5,30); rise($('#tag2'),t,18.2+2.6,.5,20); rise($('#foot'),t,18.2+3.1,.5,20);
};
"""


def page(v):
    V = VARIANTS[v]
    labs = "".join(f"""<div id="lab{i}" style="display:none"><div class="step-n">PROFIL {i + 1:02d} / 05</div><div class="step-t serif">{n}</div>
  <div class="chip"><div class="im" style="background-image:url('{img}')"></div><div><div class="k">{c} · de la</div><div class="v">{p} <small>lei</small></div></div></div></div>"""
                   for i, (_, n, c, p, img) in enumerate(STEPS))
    stock = "".join(f'<div class="hud" id="st{i}" style="top:{560 + i * 270}px;opacity:0"><div class="cnt">0</div><div class="cnt-l">{l}</div><div class="hline"></div></div>' for i, (_, l) in enumerate(STOCK))
    parts = "".join(f'<i style="width:{p[4]}px;height:{p[4]}px"></i>' for p in PARTS)
    return f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Manrope:wght@500;600;700;800&family=Unbounded:wght@800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="sc" id="s2">{facade_svg()}
  <div class="dots">{''.join('<i></i>' for _ in STEPS)}</div>{labs}</div>
<div class="sc" id="s1" style="z-index:10">
  <div class="kin serif" id="k1" style="top:760px">Casa ta e<br>frumoasă.</div>
  <div class="kin serif" id="k2" style="top:700px;opacity:0">Lipsesc doar<br><span class="five" id="five">5</span> detalii.</div>
</div>
<div class="sc" id="s3"><div class="bg" style="background-image:url('{REAL}');background-position:50% 35%"></div><div class="shade"></div>
  <div class="kin serif" id="r1" style="top:280px;font-size:108px">Din schiță.</div>
  <div class="kin serif" id="r2" style="top:395px;font-size:108px;color:var(--gold)">Pe casa ta.</div>
</div>
<div class="scan" id="scan" style="z-index:25;opacity:0"></div>
<div class="sc" id="s4">
  <div class="hud" id="hudt" style="top:300px;font-size:28px;letter-spacing:7px;font-weight:800;color:var(--gold)">ÎN STOC ACUM · DECOFLAIR.RO</div>
  {stock}
  <div class="hud" style="top:1380px"><span class="pillg" id="g1">Livrare în 3–5 zile</span><span class="pillg" id="g2">Gata de sărbători</span></div>
</div>
<div class="sc" id="s5"><div id="glow"></div><div id="beam"></div><div id="ring2"></div><div id="ring"></div><div id="parts">{parts}</div>
  <div id="wm5" style="opacity:0"><div class="wm"><i></i>DECO &amp; FLAIR</div></div>
  <div id="site">decoflair.ro</div><div id="flare"></div>
  <div id="tag" class="serif" style="opacity:0;font-size:56px">Detaliile care fac casa.</div>
  <div id="tag2" style="opacity:0">Profile de exterior · din stoc</div>
  <div id="foot" style="opacity:0">{V['foot']}</div>
</div>
<script>const STEPS={json.dumps(STEPS)};const STOCK={json.dumps(STOCK)};const PARTS={json.dumps(PARTS)};{JS}
setT(0);</script></body></html>"""


for v in VARIANTS:
    (ROOT / "reel" / f"reel-{v}.html").write_text(page(v), encoding="utf-8")
print("OK", list(VARIANTS))

"""Reel exterior Deco&Flair — „Ultimul final touch înainte de prima zăpadă” (IG/TikTok/Meta Ads, 1080x1920, ~25 s).

Inspirat din short-ul NMC „Colțar decorativ fațade” (NCL107: problemă → soluție debitată în L → rezistență ADRO Quartz → comandă),
adaptat pentru decoflair.ro, cu produsul în prim-plan (fără prezentator):
  0,0–2,3  CÂRLIG    colț de fațadă + ninsoare: „Prima zăpadă vine. Fațada ta e gata?”
  2,3–4,6  PROBLEMA  ton rece: „Muchii ciupite. Colțuri strâmbe.” → „Le ascunde un singur profil.”
  4,6–10,0 EROU      NCL107 pe fundal de studio, secțiune în L, pastile cu beneficii, stoc + preț → „Așa arată pe casă.”
 10,0–17,2 FINAL TOUCH  4 produse × 1,8 s: ancadrament, solbanc, cheie de boltă, cornișă (ambient + produs + stoc + preț)
 17,2–20,6 URGENȚĂ   amurg rece, ninsoare, ferestre calde: „Din stoc. Livrare în 3–5 zile.” „Gata de sărbători.”
 20,6–25,0 CTA       organic: link în bio; ads: zona de jos liberă pentru butonul „Cumpără acum”.
Imaginile din codex/ (CODEX-BRIEF.md) înlocuiesc automat rezervele. Rulare: python3 reel_build.py && node reel_render.cjs organic|ads
"""
from pathlib import Path
import json, random

ROOT = Path(__file__).resolve().parent
(ROOT / "reel").mkdir(exist_ok=True)


def asset(fallback, codex=None):
    if codex and (ROOT / "codex" / codex).exists():
        return f"../codex/{codex}"
    return f"../assets/{fallback}"


# Date verificate pe decoflair.ro la 24.11.2026 (preț cu TVA, „Disponibilitate” = bucăți în stoc)
HERO = dict(code="NCL107", name="Colțar decorativ NCL107", dim="300/300 × 30 × 1000 mm", price="248", stock="2.135",
            img=asset("p-ncl107-hero-crop.jpg", "10-ncl107-studio.jpg"), sec="../assets/p-ncl107-sectiune.jpg",
            amb=asset("a-colt.jpg", "02-colt-dupa.jpg"))
HOOK = asset("a-colt.jpg", "01-colt-zapada.jpg")
PROBLEM = asset("a-colt.jpg", "02-colt-inainte.jpg")
DUSK = asset("a-vila.jpg", "03-fatada-amurg-sarbatori.jpg")
REAL_DUSK = (ROOT / "codex" / "03-fatada-amurg-sarbatori.jpg").exists()

ITEMS = [
    dict(t="Ancadramente", s="Ferestre cu prezență", code="NA102", price="71", stock="1.733", amb=asset("a-vila.jpg"), p="../assets/p-na102-main.jpg", pos="50% 40%"),
    dict(t="Solbanc", s="Pervaz care închide perfect", code="NS110", price="118", stock="265", amb=asset("a-solbanc.jpg"), p="../assets/p-ns110-closeup.jpg", pos="50% 60%"),
    dict(t="Cheie de boltă", s="Accentul de deasupra", code="NCB104", price="87", stock="519", amb=asset("a-intrare.jpg"), p="../assets/p-ncb104-main.jpg", pos="50% 30%"),
    dict(t="Cornișă", s="Linia clară sub acoperiș", code="NC104", price="194", stock="185", amb=asset("a-cornisa.jpg"), p="../assets/p-nc104-main.jpg", pos="50% 30%"),
]

DELIVERY = "Din stoc · livrare în 3–5 zile"  # termen din /plata-si-livrare pentru profile de exterior în stoc
PILLS = ["Debitat în L", "Ascunde muchiile imperfecte", "Rășină + nisip cuarțos", "Rezistă la îngheț și UV"]

VARIANTS = {
    "organic": dict(cta="Comandă de pe<br>decoflair.ro", sub="Link în bio · Consultanță gratuită<br>0765 740 280", free_bottom=False),
    "ads": dict(cta="Comandă acum.<br>Din stoc.", sub="decoflair.ro · Consultanță gratuită<br>0765 740 280", free_bottom=True),
}

random.seed(7)
SNOW = [(random.random() * 1080, random.random() * 1920, random.uniform(3, 9), random.uniform(60, 160), random.uniform(0, 6.28), random.uniform(.35, .95)) for _ in range(140)]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--g:#1F3A2F;--cr:#F4EEE4;--gold:#D6BC84;--ink:#141412;--ice:#DCE8F2}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0c0f12;font-family:Manrope,sans-serif;color:#fff}
.sc{position:absolute;inset:0;overflow:hidden;opacity:0}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,0) 28%,rgba(0,0,0,0) 45%,rgba(0,0,0,.66) 70%,rgba(0,0,0,.8) 100%)}
.serif{font-family:'Cormorant Garamond',serif;font-weight:600}
.wm{position:absolute;top:210px;left:72px;font-size:22px;letter-spacing:6px;font-weight:700;display:flex;align-items:center;gap:14px}
.wm i{display:block;width:3px;height:26px;background:#9E1F2A}
.big{position:absolute;left:72px;right:150px;font-size:116px;line-height:.98;text-shadow:0 6px 40px rgba(0,0,0,.5)}
.sub{position:absolute;left:72px;right:150px;font-size:46px;line-height:1.2;font-weight:700;text-shadow:0 4px 30px rgba(0,0,0,.6)}
#snow{position:absolute;inset:0;pointer-events:none;z-index:50}
#snow i{position:absolute;border-radius:50%;background:#fff;filter:blur(1px)}
/* erou */
.studio{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 42%,#f6f3ee 0%,#e7e1d8 55%,#cfc6b9 100%)}
.hero{position:absolute;left:440px;top:600px;width:600px;height:880px;background-size:contain;background-repeat:no-repeat;background-position:center;mix-blend-mode:multiply}
.sec{position:absolute;right:150px;top:1080px;width:250px;height:250px;background:#fff center/contain no-repeat;border-radius:20px;box-shadow:0 14px 40px rgba(0,0,0,.18)}
.dark{color:var(--ink);text-shadow:none}
.pill{position:absolute;left:72px;padding:14px 26px;border-radius:40px;background:var(--g);color:#fff;font-size:34px;font-weight:800;box-shadow:0 10px 30px rgba(0,0,0,.25);white-space:nowrap}
.chip{position:absolute;left:72px;display:flex;gap:16px;align-items:stretch}
.chip div{background:#fff;color:var(--ink);border-radius:22px;padding:14px 24px;box-shadow:0 12px 34px rgba(0,0,0,.2)}
.chip .k{font-size:20px;letter-spacing:3px;text-transform:uppercase;color:#7A5B22;font-weight:800}
.chip .v{font-size:54px;font-weight:800;line-height:1.05}
.chip .v small{font-size:26px}
.chip .stk{background:var(--g);color:#fff}
.chip .stk .k{color:var(--gold)}
/* final touch */
.ft-n{position:absolute;top:282px;text-shadow:0 2px 14px rgba(0,0,0,.6);left:72px;font-size:28px;letter-spacing:5px;font-weight:800;color:var(--gold);text-transform:uppercase}
.ft-t{position:absolute;top:355px;left:72px;right:150px;font-size:112px;line-height:1;text-shadow:0 6px 40px rgba(0,0,0,.5)}
.ft-s{position:absolute;top:485px;left:72px;right:150px;font-size:44px;font-weight:700;text-shadow:0 4px 26px rgba(0,0,0,.6)}
.pcard{position:absolute;left:72px;top:1120px;display:flex;align-items:center;gap:22px;background:rgba(244,238,228,.97);color:var(--ink);border-radius:26px;padding:14px 30px 14px 14px;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.pcard .im{width:170px;height:170px;border-radius:16px;background:#fff center/cover no-repeat}
.pcard .k{font-size:20px;letter-spacing:3px;text-transform:uppercase;color:#7A5B22;font-weight:800}
.pcard .v{font-size:56px;font-weight:800;line-height:1.05}
.pcard .v small{font-size:26px}
.pcard .c{font-size:22px;color:#3d5c4d;font-weight:800}
/* urgență + cta */
.cold{filter:saturate(.55) brightness(.7) hue-rotate(-8deg)}
.solid{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,#2E5244 0%,#1F3A2F 55%,#122219 100%)}
.btn{display:inline-block;margin-top:34px;padding:22px 40px;border:3px solid var(--gold);border-radius:60px;font-size:42px;font-weight:800}
.badge{display:inline-flex;align-items:center;gap:14px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.35);border-radius:50px;padding:14px 26px;font-size:34px;font-weight:800;margin-top:22px}
"""

JS = r"""
const $=s=>document.querySelector(s);
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const out=x=>1-Math.pow(1-cl(x),3);
const back=x=>{x=cl(x);const c1=1.6,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
const vis=(el,o)=>el.style.opacity=o;
function rise(el,t,a,d=.42,dist=60){const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.transform=`translateY(${(1-k)*dist}px)`}
function pop(el,t,a,d=.42){const k=seg(t,a,a+d);el.style.opacity=cl(k*2);el.style.transform=`scale(${.6+.4*back(k)})`}
function slide(el,t,a,d=.4){const k=out(seg(t,a,a+d));el.style.opacity=cl(k*1.5);el.style.transform=`translateX(${(1-k)*-120}px)`}
window.TOTAL=25.0;
const FT0=10.0, FTD=1.8;
window.setT=function(t){
  // ninsoare: intensitate pe scene
  const snowI = t<4.6? .9 : t<10? 0 : t<17.2? .25 : t<20.6? 1 : .55;
  document.querySelectorAll('#snow i').forEach((f,i)=>{const d=SNOW[i];
    const y=(d[1]+t*d[3])%2000-40, x=d[0]+Math.sin(t*1.3+d[4])*24;
    f.style.transform=`translate(${x}px,${y}px)`; f.style.opacity=d[5]*snowI;});
  // 1 cârlig
  const S1=$('#s1'); vis(S1,t<4.75?1:0);
  $('#s1 .bg').style.transform=`scale(${1.18-.1*seg(t,0,4.6)})`;
  $('#s1 .bg').style.filter=`saturate(${1-.45*seg(t,2.2,2.6)}) brightness(${1-.3*seg(t,2.2,2.6)})`;
  rise($('#h1'),t,.1,.45); rise($('#h1b'),t,.6,.45);
  const o1=1-seg(t,2.1,2.35); $('#hk').style.opacity=o1;
  // 2 problema
  rise($('#p1'),t,2.4,.4); rise($('#p2'),t,3.3,.45);
  $('#pb').style.opacity = t<4.5?1:1-seg(t,4.5,4.7);
  $('#s1').style.clipPath = `circle(${(1-ease(seg(t,4.45,4.8)))*150}% at 50% 45%)`;
  // 3 erou
  const S3=$('#s3'); vis(S3,t>=4.4&&t<10.15?1:0);
  const hk=seg(t,4.6,5.3);
  $('#hero').style.transform=`translateY(${(1-out(hk))*500}px) rotate(${(1-out(hk))*-14+Math.sin(t*1.1)*1.5}deg) scale(${.9+.1*out(hk)+.03*seg(t,5.3,8.2)})`;
  $('#hero').style.opacity=cl(hk*2)*(1-seg(t,8.3,8.7));
  rise($('#hn'),t,4.8,.4,30); rise($('#ht'),t,4.9,.45);
  $$pills.forEach((p,i)=>slide(p,t,5.5+i*.45,.38));
  pop($('#hchip'),t,7.2,.45);
  ['#hn','#ht'].forEach(s=>{$(s).style.opacity=Math.min(+$(s).style.opacity,1-seg(t,8.3,8.6))});
  $$pills.forEach(p=>p.style.opacity=Math.min(+p.style.opacity,1-seg(t,8.3,8.6)));
  // tranziție: studioul se „deschide” spre casă
  const am=$('#hamb'); const ak=ease(seg(t,8.4,9.0)); am.style.clipPath=`inset(${(1-ak)*50}% 0 ${(1-ak)*50}% 0)`; am.style.transform=`scale(${1.15-.08*seg(t,8.4,10)})`;
  rise($('#hon'),t,8.9,.4); $('#hchip').style.top=(1130+(ak*80))+'px';
  // 4 final touch
  ITEMS.forEach((it,i)=>{const a=FT0+i*FTD, el=$('#f'+i);
    vis(el,t>=a-.12&&t<a+FTD+.12?1:0); el.style.zIndex=10+i;
    const k=ease(seg(t,a-.12,a+.22)); el.style.clipPath = `inset(0 0 0 ${(1-k)*100}%)`;
    el.querySelector('.bg').style.transform=`scale(${1.16-.1*seg(t,a,a+FTD)}) translateX(${-20+40*seg(t,a,a+FTD)}px)`;
    rise(el.querySelector('.ft-n'),t,a+.05,.3,24); rise(el.querySelector('.ft-t'),t,a+.08,.35); rise(el.querySelector('.ft-s'),t,a+.3,.35,30);
    pop(el.querySelector('.pcard'),t,a+.45,.4);
  });
  // 5 urgență
  const S5=$('#s5'); vis(S5,t>=17.1&&t<20.75?out(seg(t,17.1,17.4)):0); S5.style.zIndex=30;
  const bg5=$('#s5 .bg'); bg5.style.transform=`scale(${1.12-.07*seg(t,17.2,20.6)})`;
  if(!REAL_DUSK){bg5.style.filter=`saturate(.6) brightness(${.5-.08*seg(t,17.2,20.6)}) hue-rotate(-12deg) contrast(1.05)`}
  vis($('#glow'), .55+.25*Math.sin(t*3));
  rise($('#u1'),t,17.35,.4); rise($('#u2'),t,18.1,.4,40); rise($('#u3'),t,18.7,.4,40); rise($('#u4'),t,19.3,.45);
  // 6 cta
  const S6=$('#s6'); vis(S6,t>=20.6?out(seg(t,20.6,20.9)):0); S6.style.zIndex=31;
  rise($('#c0'),t,20.7,.35,30); rise($('#c1'),t,20.85,.45); rise($('#c2'),t,21.5,.45); pop($('#c3'),t,22.1,.45); rise($('#c5'),t,22.4,.45,40); rise($('#c4'),t,22.6,.45,30);
};
"""


def page(v):
    V = VARIANTS[v]
    pills = "".join(f'<div class="pill" style="top:{1180 + i * 0}px"></div>' for i in [])
    pill_html = "".join(f'<div class="pill p" style="top:{690 + i * 100}px;left:72px">{p}</div>' for i, p in enumerate(PILLS))
    items = "".join(f"""<div class="sc" id="f{i}"><div class="bg" style="background-image:url('{it['amb']}');background-position:{it['pos']}"></div><div class="shade"></div>
  <div class="ft-n">Final touch {i + 1}/4</div><div class="ft-t serif">{it['t']}</div><div class="ft-s">{it['s']}</div>
  <div class="pcard"><div class="im" style="background-image:url('{it['p']}')"></div><div><div class="k">de la · {it['code']}</div><div class="v">{it['price']} <small>lei</small></div><div class="c">✓ {it['stock']} buc. în stoc</div></div></div></div>"""
                    for i, it in enumerate(ITEMS))
    snow = "".join(f'<i style="width:{s[2]:.1f}px;height:{s[2]:.1f}px"></i>' for s in SNOW)
    cta_top = 300 if V["free_bottom"] else 330
    return f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=Manrope:wght@500;600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="sc" id="s1" style="z-index:5"><div class="bg" style="background-image:url('{HOOK}');background-position:50% 40%"></div><div class="shade"></div>
  <div class="wm"><i></i>DECO &amp; FLAIR</div>
  <div id="hk"><div class="big serif" id="h1" style="top:320px">Prima zăpadă<br>vine.</div>
  <div class="sub" id="h1b" style="top:620px">Fațada ta e gata? ❄️</div></div>
  <div id="pb"><div class="big serif" id="p1" style="top:320px;opacity:0">Muchii ciupite.<br>Colțuri strâmbe.</div>
  <div class="sub" id="p2" style="top:630px;opacity:0;color:var(--gold)">Le ascunde un singur profil.</div></div>
</div>
<div class="sc" id="s3" style="z-index:4"><div class="studio"></div>
  <div class="hero" id="hero" style="background-image:url('{HERO['img']}')"></div>
  <div class="dark" style="position:absolute;left:72px;top:300px;font-size:28px;letter-spacing:5px;font-weight:800;color:#7A5B22;text-transform:uppercase" id="hn">{HERO['code']} · {HERO['dim']}</div>
  <div class="big serif dark" id="ht" style="top:345px;font-size:100px">Colțarul care<br>termină casa.</div>
  {pill_html}
  <div class="bg" id="hamb" style="background-image:url('{HERO['amb']}');background-position:50% 40%;clip-path:inset(50% 0 50% 0)"><div class="shade"></div>
    <div class="big serif" id="hon" style="top:320px;opacity:0">Așa arată<br>pe casă.</div></div>
  <div class="chip" id="hchip" style="top:1130px;opacity:0"><div><div class="k">de la</div><div class="v">{HERO['price']} <small>lei/buc</small></div></div><div class="stk"><div class="k">în stoc acum</div><div class="v">{HERO['stock']} <small>buc.</small></div></div></div>
</div>
{items}
<div class="sc" id="s5"><div class="bg" style="background-image:url('{DUSK}');background-position:50% 45%"></div>
  <div id="glow" style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 62%,rgba(255,180,90,.35),rgba(255,180,90,0) 55%);mix-blend-mode:screen"></div><div class="shade"></div>
  <div class="big serif" id="u1" style="top:320px">Ultimul final<br>touch al anului.</div>
  <div class="sub" id="u2" style="top:590px"><span class="badge">📦 {DELIVERY}</span></div>
  <div class="sub" id="u3" style="top:700px"><span class="badge">🏠 Ridicare din Domnești, Ilfov</span></div>
  <div class="sub" id="u4" style="top:830px;color:var(--gold);font-size:56px">Casa gata de sărbători.</div>
</div>
<div class="sc" id="s6"><div class="solid"></div>
  <div style="position:absolute;left:72px;right:150px;top:{cta_top}px">
   <div class="wm" id="c0" style="position:static;margin-bottom:56px"><i></i>DECO &amp; FLAIR</div>
   <div class="serif" id="c1" style="font-size:108px;line-height:1">Profile de exterior<br>din stoc.</div>
   <div id="c2" style="margin-top:30px;font-size:50px;line-height:1.2;font-weight:700">{V['cta']}</div>
   <div class="btn" id="c3">decoflair.ro</div>
   <div id="c5" style="display:flex;gap:14px;margin-top:44px">{''.join(f'<div style="width:130px;height:130px;border-radius:18px;background:#fff url({x}) center/cover no-repeat"></div>' for x in ['../assets/p-ncl107-hero.jpg'] + [it['p'] for it in ITEMS])}</div>
   <div id="c4" style="margin-top:36px;font-size:34px;line-height:1.4;font-weight:600;color:rgba(255,255,255,.88)">{V['sub']}</div>
  </div>
</div>
<div id="snow">{snow}</div>
<script>const SNOW={json.dumps([[round(x, 2) for x in s] for s in SNOW])};const ITEMS={json.dumps([it['code'] for it in ITEMS])};const REAL_DUSK={str(REAL_DUSK).lower()};
{JS.replace('$$pills', '__P')}
const __P=[...document.querySelectorAll('.pill.p')];
setT(0);</script>
</body></html>"""


for v in VARIANTS:
    (ROOT / "reel" / f"reel-{v}.html").write_text(page(v), encoding="utf-8")
print("OK", list(VARIANTS), "codex:", sorted(p.name for p in (ROOT / "codex").glob("*.jpg")) or "niciunul")

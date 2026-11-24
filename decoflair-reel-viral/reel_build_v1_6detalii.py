"""Reel viral Deco&Flair — „Aceeași cameră. Doar 6 detalii.” (Instagram Reels + TikTok, 1080x1920).

Structură (~30 s), gândită pentru retenție:
  0,0–2,4  CÂRLIG     cameră „înainte” + „Aceeași cameră.” (întrebare implicită: ce s-a schimbat?)
  2,4–5,6  GLISARE    linie care dezvăluie „după” + „Doar 6 detalii.”
  5,6–20,0 6 DETALII  macro produs → ambient (zoom-through), nr. 01–06, beneficiu, preț real cu foto produs
 20,0–23,2 LUMINA     hol în penumbră → „click” → LED cald aprins
 23,2–26,0 BUGET      „Living 4×5 m · ~3.570 lei în profile”
 26,0–30,0 CTA        salvează / trimite / decoflair.ro (diferit pe IG vs TikTok)

Imaginile din codex/ (generate de Codex, vezi CODEX-BRIEF.md) înlocuiesc automat imaginile de rezervă din assets/.
Rulare: python3 reel_build.py && node reel_render.cjs
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
(ROOT / "reel").mkdir(exist_ok=True)


def asset(fallback, codex=None):
    """Preferă imaginea Codex dacă există."""
    if codex and (ROOT / "codex" / codex).exists():
        return f"../codex/{codex}"
    return f"../assets/{fallback}"


BEFORE = asset("inainte.jpg", "01-living-inainte.jpg")
AFTER = asset("dupa.jpg", "01-living-dupa.jpg")
HOL_OFF = asset("hol.jpg", "02-living-led-stins.jpg")
HOL_ON = asset("hol.jpg", "02-living-led-aprins.jpg")
REAL_SWITCH = (ROOT / "codex" / "02-living-led-aprins.jpg").exists()

# preț = cel mai mic preț cu TVA din familie, citit pe decoflair.ro la 24.11.2026
BEATS = [
    dict(n="01", t="Cornișă LED", b="Lumină de hotel.<br>Fără tavan fals.", p="196", m=asset("m-led.jpg", "05-macro-montaj.jpg"), a=asset("a-led.jpg"), pr="../assets/p-led.jpg", code="IL13", pos="50% 30%"),
    dict(n="02", t="Chenare pe perete", b="Peretele plat<br>devine boiserie.", p="59", m=asset("m-chenare.jpg", "07-macro-vopsire.jpg"), a=asset("a-chenare.jpg"), pr="../assets/p-chenare.jpg", code="WO2", pos="50% 50%"),
    dict(n="03", t="Plintă înaltă", b="Tavanul pare<br>mai sus.", p="65", m=asset("m-plinta.jpg", "06-macro-taiere.jpg"), a=asset("a-plinta.jpg"), pr="../assets/p-plinta.jpg", code="FL13", pos="50% 70%"),
    dict(n="04", t="Panouri 3D", b="Peretele prinde<br>viață în lumină.", p="166", m=asset("m-panou.jpg", "08-macro-panou-3d.jpg"), a=asset("a-panou.jpg"), pr="../assets/p-panou.jpg", code="RAY", pos="50% 50%"),
    dict(n="05", t="Riflaj din lemn", b="Căldură. Și mai<br>puțin ecou.", p="382", m=asset("m-riflaj.jpg"), a=asset("a-riflaj.jpg"), pr="../assets/p-riflaj.jpg", code="Riflaj acustic 3D", pos="50% 50%"),
    dict(n="06", t="Rozetă de tavan", b="Privirea urcă.<br>Camera crește.", p="199", m=asset("m-rozeta.jpg"), a=asset("a-rozeta.jpg"), pr="../assets/p-rozeta.jpg", code="R13", pos="50% 10%"),
]

VARIANTS = {
    "instagram": dict(
        l1="Salvează reel-ul.", l2="Trimite-l cuiva<br>care renovează.",
        site="decoflair.ro", sub="Ghidul complet „Tendințe 2027”<br>e pe blog · link în bio"),
    "tiktok": dict(
        l1="Salvează-l acum.", l2="O să ai nevoie<br>de el la renovare.",
        site="decoflair.ro", sub="Ghidul complet + prețuri<br>link în bio"),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--g:#1F3A2F;--g2:#2E5244;--cr:#F4EEE4;--gold:#D6BC84;--ink:#141412}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0d0f0e;font-family:Manrope,sans-serif;color:#fff}
.sc{position:absolute;inset:0;overflow:hidden;opacity:0}
.bg{position:absolute;inset:0;background-size:cover;background-position:center;will-change:transform}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 26%,rgba(0,0,0,0) 40%,rgba(0,0,0,.62) 62%,rgba(0,0,0,.78) 100%)}
.serif{font-family:'Cormorant Garamond',serif;font-weight:600}
.kick{font-size:26px;letter-spacing:7px;text-transform:uppercase;font-weight:700;color:var(--gold)}
.wm{position:absolute;top:210px;left:72px;font-size:22px;letter-spacing:6px;font-weight:700;display:flex;align-items:center;gap:14px;opacity:.92}
.wm i{display:block;width:3px;height:26px;background:#9E1F2A}
.big{position:absolute;left:72px;right:150px;font-size:118px;line-height:.98;text-shadow:0 6px 40px rgba(0,0,0,.45)}
.tag{position:absolute;padding:10px 22px;border-radius:40px;font-size:26px;font-weight:800;letter-spacing:4px;text-transform:uppercase}
/* glisare */
#after{clip-path:inset(0 0 0 0)}
.line{position:absolute;top:0;bottom:0;width:6px;background:#fff;box-shadow:0 0 30px rgba(255,255,255,.9)}
.knob{position:absolute;top:50%;left:50%;width:96px;height:96px;margin:-48px 0 0 -48px;border-radius:50%;background:#fff;color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:800}
/* beat */
.num{position:absolute;top:300px;left:72px;font-size:30px;font-weight:800;letter-spacing:4px;color:var(--gold)}
.num b{color:#fff}
.bt{position:absolute;top:350px;left:72px;right:150px;font-size:112px;line-height:1;text-shadow:0 4px 34px rgba(0,0,0,.55)}
.bb{position:absolute;left:72px;right:150px;top:1060px;font-size:56px;line-height:1.12;font-weight:700;text-shadow:0 4px 30px rgba(0,0,0,.6)}
.card{position:absolute;left:72px;top:1260px;display:flex;align-items:center;gap:22px;background:rgba(244,238,228,.96);color:var(--ink);border-radius:26px;padding:16px 30px 16px 16px;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.card img{width:132px;height:132px;border-radius:16px;object-fit:cover;background:#fff}
.card .k{font-size:22px;letter-spacing:3px;text-transform:uppercase;color:#7A5B22;font-weight:800}
.card .v{font-size:58px;font-weight:800;line-height:1.05}
.card .v small{font-size:28px;font-weight:700}
.card .c{font-size:22px;color:#5b5650;font-weight:600}
.macro{position:absolute;overflow:hidden;background-position:center;background-size:cover;background-repeat:no-repeat;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.macro::after{content:'';position:absolute;inset:0;opacity:var(--sh,1);background:linear-gradient(180deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.25) 30%,rgba(0,0,0,0) 45%,rgba(0,0,0,0) 70%,rgba(0,0,0,.45) 100%)}
.bar{position:absolute;top:262px;left:72px;right:150px;height:6px;display:flex;gap:8px}
.bar span{flex:1;background:rgba(255,255,255,.28);border-radius:3px;overflow:hidden}
.bar span i{display:block;height:100%;width:0;background:#fff}
/* lumina */
.flash{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 85%,rgba(255,196,120,.55),rgba(255,170,90,0) 60%);opacity:0;mix-blend-mode:screen}
.click{position:absolute;left:50%;top:880px;width:150px;height:150px;margin-left:-75px;border-radius:50%;border:5px solid #fff;opacity:0}
/* buget + cta */
.solid{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,#2E5244 0%,#1F3A2F 55%,#122219 100%)}
.ctr{position:absolute;left:72px;right:150px;text-align:left}
.price{font-size:190px;line-height:.95;color:var(--gold);font-family:Manrope,sans-serif;font-weight:800;letter-spacing:-6px}
.small{font-size:36px;line-height:1.35;font-weight:600;color:rgba(255,255,255,.88)}
.btn{display:inline-block;margin-top:34px;padding:22px 40px;border:3px solid var(--gold);border-radius:60px;font-size:42px;font-weight:800;color:#fff}
"""

JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const out=x=>1-Math.pow(1-cl(x),3);
const back=x=>{x=cl(x);const c1=1.6,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
function vis(el,o){el.style.opacity=o}
function rise(el,t,a,d=.45,dist=60){const k=out(seg(t,a,a+d));el.style.opacity=k;el.style.transform=`translateY(${(1-k)*dist}px)`}
function pop(el,t,a,d=.45){const k=seg(t,a,a+d);el.style.opacity=cl(k*2);el.style.transform=`scale(${.6+.4*back(k)})`}
const B=BEATS, T0=5.6, BD=2.4;
window.TOTAL=30.0;
window.setT=function(t){
  // 1 cârlig + 2 glisare
  const s1=$('#s1'); vis(s1, t<5.75?1:0);
  $('#before').style.transform=`scale(${1.08+0.06*seg(t,0,5.6)}) translateX(${-40+60*seg(t,0,5.6)}px)`;
  $('#after').style.transform=$('#before').style.transform;
  const w=ease(seg(t,2.4,3.9)); // procent dezvăluit
  $('#after').style.clipPath=`inset(0 ${(1-w)*100}% 0 0)`;
  const ln=$('#ln'); ln.style.left=`calc(${w*100}% - 3px)`; vis(ln, t>2.35&&t<4.3?1:0);
  rise($('#h1'),t,.15,.5); rise($('#h1b'),t,.75,.5);
  vis($('#tagB'), t<2.6?out(seg(t,.1,.5)):0); vis($('#tagA'), out(seg(t,3.4,3.8)));
  const hookOut=seg(t,2.2,2.5); $('#hk').style.opacity=1-hookOut;
  rise($('#h2'),t,3.9,.5); rise($('#h2b'),t,4.4,.5,40);
  $('#s1').style.filter=`brightness(${1-0.5*seg(t,5.35,5.75)})`;
  // 3 detalii
  B.forEach((b,i)=>{
    const a=T0+i*BD, e=a+BD, el=$('#b'+i), lt=t-a;
    vis(el, t>=a-0.15 && t<e+0.15 ? (i==0?out(seg(t,a-.15,a+.15)):1) : 0);
    el.style.zIndex=10+i;
    // intrare: tranziție rapidă (cortină diagonală) peste beat-ul anterior
    const inK=ease(seg(t,a-.15,a+.2));
    el.style.clipPath= i==0? 'none' : `polygon(0 0, ${inK*140}% 0, ${inK*140-40}% 100%, 0 100%)`;
    // macro: plin ecran la început, apoi se micșorează în card
    const m=el.querySelector('.macro'), k=ease(seg(lt,.75,1.25));
    m.style.width=(1080-(1080-300)*k)+'px'; m.style.height=(1920-(1920-380)*k)+'px';
    m.style.left=(640*k)+'px'; m.style.top=(560*k)+'px';
    m.style.borderRadius=(k*28)+'px'; m.style.setProperty('--sh',1-k);
    m.style.opacity= 1-seg(lt,1.9,2.2);
    el.querySelector('.bg').style.transform=`scale(${1.18-.12*seg(lt,.75,2.4)})`;
    rise(el.querySelector('.num'),t,a+.05,.35,30); rise(el.querySelector('.bt'),t,a+.1,.4,50);
    rise(el.querySelector('.bb'),t,a+1.0,.4,40); pop(el.querySelector('.card'),t,a+1.15,.45);
    el.querySelectorAll('.bar i').forEach((x,j)=>{x.style.width=(j<i?100:j==i?seg(t,a,e)*100:0)+'%'});
  });
  // 4 lumina
  const L=$('#s4'), la=T0+6*BD; vis(L, t>=la-.1&&t<23.35?1:0); L.style.zIndex=30;
  const on=seg(t,la+1.15,la+1.55);
  L.querySelector('.bg').style.filter = REAL_SWITCH ? 'none' : `brightness(${.28+.72*on}) saturate(${.5+.5*on}) hue-rotate(${(1-on)*-25}deg)`;
  L.querySelector('.bg').style.transform=`scale(${1.12-.08*seg(t,la,23.2)})`;
  if(REAL_SWITCH){$('#s4on').style.opacity=on}
  vis(L.querySelector('.flash'), on*(1-seg(t,la+1.6,la+2.6))*0.9+on*.25);
  const ck=seg(t,la+1.0,la+1.5); const c=L.querySelector('.click'); c.style.opacity=ck>0&&ck<1?1-ck:0; c.style.transform=`scale(${.5+1.6*ck})`;
  rise($('#l1'),t,la+.15,.45); rise($('#l2'),t,la+1.6,.45);
  // 5 buget
  const S5=$('#s5'); vis(S5, t>=23.2&&t<26.15?out(seg(t,23.2,23.5)):0); S5.style.zIndex=31;
  rise($('#p1'),t,23.35,.4,40);
  const n=Math.round(3570*out(seg(t,23.55,24.7))); $('#pn').textContent='~'+n.toLocaleString('ro-RO');
  rise($('#p2'),t,23.55,.4,60); rise($('#p3'),t,24.6,.4,40);
  // 6 cta
  const S6=$('#s6'); vis(S6, t>=26.0?out(seg(t,26.0,26.3)):0); S6.style.zIndex=32;
  rise($('#c0'),t,26.1,.4,30); rise($('#c1'),t,26.25,.45); rise($('#c2'),t,26.8,.45); pop($('#c3'),t,27.5,.5); rise($('#c4'),t,28.0,.45,30);
};
"""


def beat_html(i, b):
    bars = "".join("<span><i></i></span>" for _ in BEATS)
    return f"""<div class="sc" id="b{i}">
  <div class="bg" style="background-image:url('{b['a']}');background-position:{b['pos']}"></div>
  <div class="shade"></div>
  <div class="macro" style="background-image:url('{b['m']}')"></div>
  <div class="bar">{bars}</div>
  <div class="num"><b>{b['n']}</b> / 06</div>
  <div class="bt serif">{b['t']}</div>
  <div class="bb">{b['b']}</div>
  <div class="card"><img src="{b['pr']}" alt=""><div><div class="k">de la</div><div class="v">{b['p']} <small>lei</small></div><div class="c">{b['code']} · decoflair.ro</div></div></div>
</div>"""


def page(v):
    V = VARIANTS[v]
    beats = "\n".join(beat_html(i, b) for i, b in enumerate(BEATS))
    s4on = f'<div class="bg" id="s4on" style="background-image:url(\'{HOL_ON}\');opacity:0"></div>' if REAL_SWITCH else ""
    return f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=Manrope:wght@500;600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="sc" id="s1">
  <div class="bg" id="before" style="background-image:url('{BEFORE}');background-position:30% 50%"></div>
  <div class="bg" id="after" style="background-image:url('{AFTER}');background-position:30% 50%"></div>
  <div class="shade"></div>
  <div class="line" id="ln"><div class="knob">⇆</div></div>
  <div class="wm"><i></i>DECO &amp; FLAIR</div>
  <div id="hk"><div class="big serif" id="h1" style="top:330px">Aceeași<br>cameră.</div>
  <div class="small" id="h1b" style="position:absolute;left:72px;top:600px;font-size:44px;font-weight:700">Fără renovare. Fără praf.</div></div>
  <div class="big serif" id="h2" style="top:330px;opacity:0">Doar 6<br>detalii.</div>
  <div class="small" id="h2b" style="position:absolute;left:72px;top:600px;font-size:44px;font-weight:700;opacity:0">Uite care 👇</div>
  <div class="tag" id="tagB" style="left:72px;top:1330px;background:rgba(0,0,0,.55);color:#fff">Înainte</div>
  <div class="tag" id="tagA" style="right:150px;top:1330px;background:var(--gold);color:#141412;opacity:0">După</div>
</div>
{beats}
<div class="sc" id="s4"><div class="bg" style="background-image:url('{HOL_OFF}')"></div>{s4on}<div class="flash"></div><div class="shade"></div>
  <div class="click"></div>
  <div class="big serif" id="l1" style="top:330px;font-size:104px">Și la final…</div>
  <div class="big serif" id="l2" style="top:470px;font-size:104px;color:var(--gold)">aprinzi lumina.</div>
</div>
<div class="sc" id="s5"><div class="solid"></div>
  <div class="ctr" style="top:420px"><div class="kick" id="p1">Living 4 × 5 m · exemplu real</div>
  <div class="price" id="p2" style="margin-top:40px"><span id="pn">~0</span><br><span style="font-size:90px;letter-spacing:0">lei</span></div>
  <div class="small" id="p3" style="margin-top:50px">cornișă LED + plinte + 3 chenare<br>prețuri decoflair.ro · noiembrie 2026<br><span style="color:var(--gold)">fără bandă LED, adeziv și manoperă</span></div></div>
</div>
<div class="sc" id="s6"><div class="solid"></div>
  <div class="ctr" style="top:330px">
   <div class="wm" id="c0" style="position:static;margin-bottom:60px"><i></i>DECO &amp; FLAIR</div>
   <div class="serif" id="c1" style="font-size:112px;line-height:1">{V['l1']}</div>
   <div class="small" id="c2" style="margin-top:30px;font-size:52px;line-height:1.2;color:#fff;font-weight:700">{V['l2']}</div>
   <div class="btn" id="c3">{V['site']}</div>
   <div class="small" id="c4" style="margin-top:40px">{V['sub']}<br><span style="color:var(--gold)">Livrare 1–2 zile · consultanță gratuită</span></div>
  </div>
</div>
<script>const BEATS={json.dumps([{k: b[k] for k in ('n','t')} for b in BEATS])};const REAL_SWITCH={str(REAL_SWITCH).lower()};{JS}
setT(0);</script>
</body></html>"""


for v in VARIANTS:
    (ROOT / "reel" / f"reel-{v}.html").write_text(page(v), encoding="utf-8")
print("OK", list(VARIANTS), "codex assets:", sorted(p.name for p in (ROOT / "codex").glob("*.jpg")) or "niciunul (folosesc rezervele)")

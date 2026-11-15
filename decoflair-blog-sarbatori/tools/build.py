#!/usr/bin/env python3
"""Generează articolul de blog „Casa de sărbători” pentru decoflair.ro (Journal 3 Blog).

Rezultate:
  articol.html          → fragmentul care se lipește în editorul de articol (mod Cod sursă)
  previzualizare.html   → același articol într-o pagină de test (imagini locale)
Rulare: python3 decoflair-blog-sarbatori/tools/build.py
"""
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://decoflair.ro/"
IMG_SITE = "/image/catalog/blog/casa-de-sarbatori/"   # unde se urcă imaginile pe server

def prod(id_, name, brand, why, url):
    return dict(id=id_, name=name, brand=brand, why=why, url=SITE + url)

PR = {
    "wo2": prod("wo2", "Brâu WO2 pentru chenare", "Wallstyl®", "Cel mai accesibil mod de a desena chenare clasice.", "brau-decorativwo2-wallstyl"),
    "z1360": prod("z1360", "Brâu Z1360", "Arstyl®", "Profil subțire, pentru chenare fine și moderne.", "brau-z1360"),
    "wl6": prod("wl6", "Brâu WL6", "Wallstyl®", "Linie orizontală la înălțimea scaunelor (chair rail).", "brau-decorativwl6-wallstyl"),
    "z11": prod("z11", "Cornișă Z11", "Arstyl®", "Cornișă ornamentală, pentru tavanul unui dining festiv.", "plinta-decorativa-tavan-arstyl-z11"),
    "z21": prod("z21", "Cornișă Z21", "Arstyl®", "Profil generos, cu umbre adânci.", "plinta-decorativa-tavan-arstyl-z21"),
    "r12": prod("r12", "Rozetă R12", "Arstyl®", "Rozetă Ø 825 mm deasupra mesei, sub candelabru.", "rozeta-decorativar12-arstyl"),
    "wave": prod("wave", "Panou 3D WAVE", "Arstyl®", "Relief în valuri pentru un perete-sculptură.", "panou-decorativ-3d-wave"),
    "canele": prod("canele", "Panou 3D CANELE L", "Arstyl®", "Canelură verticală, eleganță arhitecturală.", "panou-decorativ-canelel"),
    "l5": prod("l5", "Scafă LED L5", "Arstyl®", "Lumină indirectă caldă pe tot perimetrul tavanului.", "l5-arstyl"),
    "il18": prod("il18", "Cornișă LED IL18", "Wallstyl®", "Lumină care „spală” draperiile sau peretele.", "cornisa-led-il18-121x90x2000"),
    "il11": prod("il11", "Plintă LED IL11", "Wallstyl®", "Linie de lumină la nivelul pardoselii.", "plinta-decorativa-parchet-alba-polimer-dur-wallstyl-il11-80x20x2m"),
    "rif-deschis": prod("rif-deschis", "Riflaj acustic · stejar deschis", "NMC®", "Căldura lemnului și mai puțin ecou la masă.", "riflaj-acustic-panou-3d-stejar-deschis"),
    "rif-inchis": prod("rif-inchis", "Riflaj acustic · stejar închis", "NMC®", "Varianta profundă, pentru un dining dramatic.", "riflaj-acustic-panou-3d-stejar-inchis"),
    "c82603": prod("c82603", "Tapet Carrara Best 82603", "Carrara Best", "Marmură caldă, pentru peretele principal.", "tapet-carrara-82603"),
    "c82671": prod("c82671", "Tapet Carrara Best 82671", "Carrara Best", "Marmură crem cu nervuri aurii.", "tapet-carrara-82671"),
    "fd21": prod("fd21", "Plintă FD21", "Wallstyl®", "Plintă înaltă, care „ancorează” peretele.", "plintafd21-wallstyl"),
    "adefix": prod("adefix", "Adeziv ADEFIX 310 ml", "Adefix", "Adezivul pentru lipirea profilelor de interior.", "adeziv-lipire-adefix-310-ml"),
}

PALETA = [
    ("Verde forest", "#2F4A3C", "Profunzime, natură, liniște. Superb pe chenare, cu alb cald pe profile."),
    ("Salvie prăfuit", "#A9BBAA", "Varianta luminoasă a verdelui: proaspăt, calm, foarte fotogenic."),
    ("Roz pudră", "#EBCFCB", "Căldură discretă. Arată „scump” lângă alamă și lemn natural."),
    ("Mov șters", "#A6919F", "Tonul surpriză: elegant, misterios, perfect pentru seara de Crăciun."),
    ("Crem cald", "#F1E8DC", "Baza care face totul să respire. Ideal pentru profile și tavan."),
    ("Onix", "#1A1719", "Accentul de lux: rame, metal, sticlă fumurie, detalii fine."),
]

RETETE = [
    dict(id="chenare-verde", n="01", titlu="Chenare clasice în verde forest", stil="Clasic-contemporan · cald · intim",
         img="02-chenare-verde-forest", buget="Esențial → Rafinat",
         text="Cea mai sigură alegere pentru un dining de sărbători: peretele din spatele mesei primește chenare din brâu WO2 sau Z1360, iar totul (perete și profile) se vopsește în același verde forest. Efectul ton-pe-ton e modern, iar umbrele profilelor dau relief fără să încarce.",
         pasi=["Împarte peretele în 2 sau 3 chenare verticale, aliniate cu axul mesei.", "Lasă 8–12 cm între chenare și față de colțuri: aerul dintre ele face eleganța.", "Pune un brâu WL6 la înălțimea spătarului scaunelor ca linie de separare, dacă tavanul trece de 2,70 m.", "Vopsește peretele și profilele în aceeași culoare, mat sau satinat."],
         produse=["wo2", "z1360", "wl6", "adefix"]),
    dict(id="tavan-rozeta", n="02", titlu="Tavan festiv: cornișă și rozetă deasupra mesei", stil="Clasic · luminos · ceremonial",
         img="03-chenare-si-cornisa-ivoriu", buget="Rafinat",
         text="Masa de Crăciun are un punct firesc de centru: corpul de iluminat de deasupra ei. O rozetă R12 sub candelabru și o cornișă Z11 sau Z21 pe perimetru transformă tavanul într-un „baldachin” care încadrează masa și face camera să pară mai înaltă.",
         pasi=["Centrează rozeta exact pe axul mesei, nu al camerei, dacă masa nu e centrată.", "Alege cornișa după înălțime: Z21 pentru tavane înalte, Z11 pentru dramatism ornamental.", "Vopsește tavanul și cornișa în crem cald, iar pereții un ton mai închis.", "Folosește becuri calde (2700K) și un variator pentru seara de Ajun."],
         produse=["r12", "z11", "z21", "adefix"]),
    dict(id="relief-3d", n="03", titlu="Peretele-sculptură: relief 3D în spatele mesei", stil="Contemporan · artistic · spectaculos",
         img="04-dining-relief-3d", buget="Rafinat → Signature",
         text="Un singur perete cu panouri 3D WAVE sau CANELE L în spatele mesei e cel mai „instagramabil” fundal pentru fotografiile de sărbători. Relieful prinde lumina lumânărilor și se schimbă de la o oră la alta.",
         pasi=["Acoperă tot peretele, de la plintă la tavan: fragmentele mici arată neterminat.", "Începe montajul din centru, ca modelul să fie simetric față de masă.", "Vopsește panourile într-un ton cald (crem, roz pudră, salvie), nu alb rece.", "Adaugă o lumină laterală (aplică sau LED) ca să dubleze adâncimea reliefului."],
         produse=["wave", "canele", "adefix"]),
    dict(id="lumina", n="04", titlu="Lumina care face totul să strălucească", stil="Minimal · cald · atmosferic",
         img="05-lumina-indirecta", buget="Rafinat",
         text="Lumina indirectă este secretul fotografiilor de sărbători care arată „ca în reviste”. Scafa LED L5 pe perimetru sau cornișa IL18 deasupra draperiilor creează o aură caldă, iar plinta IL11 adaugă o linie fină de lumină la podea.",
         pasi=["Alege bandă LED caldă (2700–3000K) și un dimmer: seara de Crăciun cere lumină joasă.", "Pune banda la 5–10 cm de perete, ca lumina să „spele” suprafața uniform.", "Combină trei niveluri: tavan (L5), perete (IL18) și podea (IL11).", "Stinge spoturile directe în timpul cinei: rămân doar LED-ul și lumânările."],
         produse=["l5", "il18", "il11"]),
    dict(id="lemn", n="05", titlu="Lemn și liniște: riflaj acustic în dining", stil="Japandi · natural · primitor",
         img="06-dining-lamele-lemn", buget="Rafinat",
         text="La o masă cu familia mare, ecoul obosește. Riflajul acustic cu aspect de stejar aduce căldura lemnului și reduce reverberația. Pus pe peretele din spatele mesei sau la jumătate de perete, schimbă complet senzația camerei.",
         pasi=["Stejar deschis pentru spații mici și luminoase; stejar închis pentru un dining dramatic.", "Montează lamelele vertical, ca să înalțe vizual camera.", "Lasă un fir de lumină LED deasupra sau în spatele panourilor.", "Combină cu textile naturale: in, lână, catifea în verde sau mov șters."],
         produse=["rif-deschis", "rif-inchis"]),
    dict(id="marmura", n="06", titlu="Marmură fără marmură: tapetul Carrara Best", stil="Lux · luminos · atemporal",
         img="07-marmura-tapet", buget="Signature",
         text="Pentru cine vrea lux fără șantier: tapetul Carrara Best cu efect de marmură, pe peretele principal din spatele mesei, se aplică rapid și transformă camera într-o singură zi. Arată spectaculos lângă alamă, sticlă și lumânări albe.",
         pasi=["Folosește tapetul pe un singur perete, cel principal: mai mult devine apăsător.", "Încadrează-l cu o plintă înaltă FD21 și o cornișă simplă, vopsite în crem.", "Alege accente metalice calde (alamă, bronz) pentru masă.", "Verifică numărul de role cu un consultant înainte de comandă."],
         produse=["c82603", "c82671", "fd21"]),
]

NIVELURI = [
    ("Esențial", "Un weekend · buget mic", "Chenare din brâu WO2 pe peretele din spatele mesei + o culoare nouă. Diferența se vede din prima seară.", ["wo2", "adefix"]),
    ("Rafinat", "1–2 săptămâni · buget mediu", "Chenare + cornișă pe perimetru + scafă LED. Camera capătă arhitectură și atmosferă.", ["z1360", "z11", "l5"]),
    ("Signature", "2–3 săptămâni · investiție", "Perete-sculptură 3D sau tapet Carrara + rozetă deasupra mesei + lumină pe trei niveluri.", ["wave", "c82671", "r12"]),
]

PLAN = [
    ("Săptămâna 1", "Decizia", "Alege peretele-scenă (cel din spatele mesei), stilul și paleta. Măsoară, fotografiază camera și cere o consultanță sau o randare 3D. Comandă profilele, adezivul și vopseaua."),
    ("Săptămâna 2", "Montajul", "Lipește profilele cu adeziv, începând cu cornișa, apoi chenarele și plintele. Respectă timpii de uscare din fișa tehnică a adezivului."),
    ("Săptămâna 3", "Finisajul", "Chituiește îmbinările, șlefuiește fin, aplică amorsa unde e nevoie și două straturi de vopsea. Montează banda LED în scafe."),
    ("Săptămâna 4", "Povestea", "Masa, textilele, lumânările, verdeața. Fă o „repetiție” de lumină seara și fotografiază camera înainte de musafiri."),
]

GRESELI = [
    ("Profile prea mici pe un perete mare", "Proporția contează: pe pereți înalți alege profile cu secțiune generoasă sau dublează linia."),
    ("Chenare care nu țin cont de masă", "Peretele din spatele mesei se compune în funcție de masă și scaune, nu invers."),
    ("Alb rece peste tot", "Albul optic face camera clinică. Pentru sărbători alege crem, ivoriu sau un alb cald."),
    ("Lumină puternică, de sus", "Spoturile directe aplatizează relieful. Lumina indirectă și lumânările îl pun în valoare."),
    ("Prea multe idei într-o singură cameră", "Alege o vedetă (relief, marmură sau lemn) și lasă restul să o susțină."),
    ("Montaj pe ultima sută de metri", "Adezivul și vopseaua au nevoie de timp. Începe cu 3–4 săptămâni înainte de Crăciun."),
]

FAQ = [
    ("Pot face asta singur, fără meșter?", "Da, pentru variantele Esențial și Rafinat. Profilele din poliuretan și polimer dur sunt ușoare, se taie cu un fierăstrău fin și o cutie de îmbinări la 45°, și se lipesc cu adeziv. Pentru panouri 3D pe un perete întreg sau pentru LED recomandăm un montator."),
    ("În cât timp e gata un perete cu chenare?", "Montajul propriu-zis durează de obicei o zi, iar chituirea și vopsirea încă 1–2 zile, în funcție de timpii de uscare ai adezivului și vopselei."),
    ("Ce vopsea folosesc pe profile?", "Vopsea acrilică pe bază de apă, mată sau satinată, aceeași ca pe perete pentru efectul ton-pe-ton. Profilele preamorsate pot fi vopsite direct."),
    ("Cum calculez câte bare îmi trebuie?", "Măsoară perimetrul fiecărui chenar, adună-le și adaugă 10–15% pentru tăieri. Barele au 2 m. Consultanții Deco&Flair te ajută gratuit cu necesarul."),
    ("Se potrivesc profilele într-un apartament de bloc?", "Absolut. Tocmai în spațiile standard, un perete cu chenare sau o scafă LED face cea mai mare diferență, fără lucrări de construcție."),
]


def ico_arrow():
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def pcard(k, IMG):
    p = PR[k]
    return f'''<a class="dfb-p" href="{p["url"]}"><span class="dfb-p__img"><img src="{IMG}p-{p["id"]}.jpg" alt="{e(p["name"])}" loading="lazy"></span><span class="dfb-p__b"><small>{e(p["brand"])}</small><b>{e(p["name"])}</b><span>{e(p["why"])}</span><em>Vezi produsul {ico_arrow()}</em></span></a>'''


def fig(img, cap, IMG, cls=""):
    return f'<figure class="dfb-fig {cls}"><img src="{IMG}{img}.jpg" alt="{e(cap)}" loading="lazy"><figcaption>{e(cap)}</figcaption></figure>'


CSS = r"""
.dfb{--cream:#F4EEE6;--paper:#FBF8F3;--nude:#E6D7C8;--ink:#141214;--ink2:#2A2629;--muted:#7B7176;--line:#14121418;--mauve:#A6919F;--forest:#2F4A3C;--forest2:#5E7F6B;--powder:#EBCFCB;
 --g-text:linear-gradient(100deg,#2F4A3C 0%,#5E7F6B 35%,#A6919F 70%,#C79C98 100%);--serif:"Instrument Serif","Times New Roman",serif;--sans:"Jost",system-ui,sans-serif;
 font:300 18px/1.8 var(--sans);color:var(--ink2);background:var(--cream);max-width:100%;overflow:hidden;border-radius:28px}
.dfb *{box-sizing:border-box}
.dfb img{display:block;max-width:100%;height:auto}
.dfb a{color:inherit;text-decoration:none}
.dfb p{margin:0 0 1.1em}
.dfb strong{font-weight:500;color:var(--ink)}
.dfb h2,.dfb h3{font-family:var(--serif);font-weight:400;color:var(--ink);letter-spacing:-.01em;margin:0}
.dfb h2{font-size:clamp(34px,4vw,56px);line-height:1.05;margin:0 0 22px}
.dfb h3{font-size:clamp(28px,3vw,40px);line-height:1.1;margin:0 0 14px}
.dfb h2 em,.dfb h3 em,.dfb .dfb-hero h2 em{font-style:italic;background:var(--g-text);-webkit-background-clip:text;background-clip:text;color:transparent;padding-right:.05em}
.dfb-in{max-width:880px;margin:0 auto;padding:0 clamp(18px,4vw,40px)}
.dfb-wide{max-width:1200px;margin:0 auto;padding:0 clamp(18px,4vw,40px)}
.dfb-label{display:inline-flex;align-items:center;gap:10px;font:400 12px/1 var(--sans);letter-spacing:.26em;text-transform:uppercase;color:var(--muted);margin-bottom:16px}
.dfb-label::before{content:"";width:26px;height:1px;background:currentColor}
.dfb-label b{font-weight:500;color:var(--ink)}
.dfb-sec{padding:clamp(48px,6vw,90px) 0 0}
/* hero */
.dfb-hero{position:relative;padding:clamp(40px,6vw,80px) 0 0;background:radial-gradient(50% 60% at 0% 0%,#EBCFCB,transparent 70%),radial-gradient(45% 60% at 100% 30%,#C9D4C6,transparent 70%),var(--cream)}
.dfb-hero__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,60px);align-items:center}
.dfb-hero h2{font-size:clamp(42px,5.4vw,78px);line-height:1}
.dfb-lead{font-size:20px;color:var(--ink2)}
.dfb-meta{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:22px;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.dfb-arch{overflow:hidden;border-radius:999px 999px 26px 26px;background:var(--nude);box-shadow:0 50px 90px -60px #2F4A3C99}
.dfb-arch img{width:100%;aspect-ratio:4/5;object-fit:cover}
@media (max-width:820px){.dfb-hero__grid{grid-template-columns:1fr}}
/* cuprins */
.dfb-toc{margin-top:clamp(36px,5vw,64px);padding:26px 28px;border-radius:24px;background:var(--paper);border:1px solid var(--line)}
.dfb-toc ol{margin:8px 0 0;padding:0;list-style:none;columns:2;column-gap:32px}
.dfb-toc li{break-inside:avoid;padding:8px 0;border-bottom:1px solid var(--line);font-size:16px}
.dfb-toc li a{display:flex;gap:12px}
.dfb-toc li a b{font:italic 400 18px/1.4 var(--serif);color:var(--forest2);min-width:24px}
.dfb-toc li a:hover{color:var(--forest)}
@media (max-width:640px){.dfb-toc ol{columns:1}}
/* citat */
.dfb-quote{margin:clamp(40px,5vw,70px) 0;padding:0 0 0 26px;border-left:2px solid var(--powder);font:italic 400 clamp(26px,3vw,38px)/1.25 var(--serif);color:var(--ink)}
/* know-how */
.dfb-know{display:flex;gap:14px;margin:26px 0;padding:20px 22px;border-radius:20px;background:linear-gradient(135deg,#FBF8F3,#F3DFDB90);border:1px solid #EBCFCB;font-size:16.5px;line-height:1.65}
.dfb-know small{display:block;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--forest2);margin-bottom:4px}
.dfb-know i{flex:none;font:italic 400 26px/1 var(--serif);color:var(--forest)}
/* paletă */
.dfb-pal{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
.dfb-sw{border-radius:22px;overflow:hidden;background:var(--paper);border:1px solid var(--line)}
.dfb-sw span{display:block;height:110px}
.dfb-sw div{padding:14px 16px 18px;font-size:15px;line-height:1.55}
.dfb-sw b{display:block;font:400 24px/1.1 var(--serif);color:var(--ink)}
.dfb-sw code{font:400 12px/1 var(--sans);letter-spacing:.14em;color:var(--muted)}
@media (max-width:720px){.dfb-pal{grid-template-columns:1fr 1fr}}
.dfb-combo{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:18px}
.dfb-combo div{padding:16px;border-radius:18px;border:1px solid var(--line);background:#FBF8F3b0;font-size:15px}
.dfb-combo i{display:flex;gap:4px;margin-bottom:10px}.dfb-combo i span{flex:1;height:26px;border-radius:8px}
.dfb-combo b{font-weight:500;color:var(--ink)}
@media (max-width:720px){.dfb-combo{grid-template-columns:1fr}}
/* figuri */
.dfb-fig{margin:30px 0}
.dfb-fig img{width:100%;border-radius:26px;aspect-ratio:4/3;object-fit:cover}
.dfb-fig.arch img{border-radius:999px 999px 26px 26px;aspect-ratio:4/5}
.dfb-fig figcaption{margin-top:10px;font-size:13px;letter-spacing:.06em;color:var(--muted)}
/* plan */
.dfb-plan{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}
.dfb-plan div{padding:22px 20px;border-radius:22px;background:var(--paper);border:1px solid var(--line);font-size:15.5px;line-height:1.6}
.dfb-plan small{display:block;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--forest2)}
.dfb-plan b{display:block;margin:6px 0 8px;font:400 28px/1 var(--serif);color:var(--ink)}
@media (max-width:900px){.dfb-plan{grid-template-columns:1fr 1fr}}@media (max-width:520px){.dfb-plan{grid-template-columns:1fr}}
/* rețete */
.dfb-r{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(24px,4vw,56px);align-items:start;padding:clamp(36px,5vw,64px) 0;border-top:1px solid var(--line)}
.dfb-r:nth-of-type(even) .dfb-r__img{order:2}
.dfb-r__img img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:999px 999px 26px 26px;position:sticky;top:110px}
.dfb-r__n{font:italic 400 64px/1 var(--serif);color:transparent;-webkit-text-stroke:1px #2F4A3C66}
.dfb-r__tags{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}
.dfb-r__tags span{padding:6px 12px;border-radius:999px;border:1px solid var(--line);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.dfb-r__tags span:last-child{background:var(--ink);color:var(--cream);border-color:var(--ink)}
.dfb-steps{margin:18px 0;padding:0;list-style:none;counter-reset:s}
.dfb-steps li{counter-increment:s;position:relative;padding:10px 0 10px 44px;border-bottom:1px solid var(--line);font-size:16.5px;line-height:1.6}
.dfb-steps li::before{content:counter(s,decimal-leading-zero);position:absolute;left:0;top:9px;font:italic 400 22px/1 var(--serif);color:var(--forest2)}
@media (max-width:820px){.dfb-r{grid-template-columns:1fr}.dfb-r:nth-of-type(even) .dfb-r__img{order:0}.dfb-r__img img{position:static;aspect-ratio:5/4}}
/* carduri produs */
.dfb-ps{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:18px}
.dfb-p{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:center;padding:10px;border-radius:20px;background:var(--paper);border:1px solid var(--line);transition:border-color .3s,transform .3s}
.dfb-p:hover{border-color:#2F4A3C44;transform:translateY(-2px)}
.dfb-p__img{display:block;border-radius:14px;overflow:hidden;background:#fff}
.dfb-p__img img{width:96px;height:96px;object-fit:contain;padding:4px}
.dfb-p__b{display:flex;flex-direction:column;gap:2px;font-size:14px;line-height:1.4}
.dfb-p__b small{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mauve)}
.dfb-p__b b{font:400 21px/1.1 var(--serif);color:var(--ink)}
.dfb-p__b em{white-space:nowrap;font-style:normal;display:inline-flex;align-items:center;gap:6px;margin-top:4px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--forest)}
.dfb-r .dfb-ps{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
@media (max-width:560px){.dfb-ps,.dfb-r .dfb-ps{grid-template-columns:1fr}}
/* niveluri */
.dfb-lv{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
.dfb-lv>div{display:flex;flex-direction:column;padding:26px 22px;border-radius:24px;border:1px solid var(--line);background:var(--paper)}
.dfb-lv>div:nth-child(2){background:linear-gradient(160deg,#FBF8F3,#F3DFDB)}
.dfb-lv>div:nth-child(3){background:linear-gradient(160deg,#2F4A3C,#5E7F6B);color:#EEF2EC;border-color:transparent}
.dfb-lv>div:nth-child(3) b,.dfb-lv>div:nth-child(3) .dfb-p__b b{color:#fff}
.dfb-lv b{font:400 34px/1 var(--serif);color:var(--ink)}
.dfb-lv small{display:block;margin:8px 0 12px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;opacity:.75}
.dfb-lv p{font-size:15.5px;line-height:1.6}
.dfb-lv ul{list-style:none;margin:auto 0 0;padding:12px 0 0;border-top:1px solid #14121420;font-size:14px}
.dfb-lv li a{display:flex;justify-content:space-between;padding:6px 0;text-decoration:underline;text-underline-offset:3px}
@media (max-width:820px){.dfb-lv{grid-template-columns:1fr}}
/* masă */
.dfb-table{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:22px}
.dfb-table div{padding:20px;border-radius:20px;border:1px solid var(--line);background:#FBF8F3b0;font-size:15.5px;line-height:1.6}
.dfb-table b{display:block;font:400 24px/1.1 var(--serif);color:var(--ink);margin-bottom:6px}
@media (max-width:640px){.dfb-table{grid-template-columns:1fr}}
/* greșeli */
.dfb-err{display:grid;grid-template-columns:repeat(2,1fr);gap:0;margin-top:20px;border-top:1px solid var(--line)}
.dfb-err div{padding:18px 18px 18px 0;border-bottom:1px solid var(--line);font-size:15.5px;line-height:1.6}
.dfb-err b{display:block;font-weight:500;color:var(--ink);margin-bottom:4px}
.dfb-err b::before{content:"×";margin-right:10px;color:#C79C98}
@media (max-width:640px){.dfb-err{grid-template-columns:1fr}}
/* checklist */
.dfb-check{margin:20px 0 0;padding:24px 28px;border-radius:24px;background:var(--paper);border:1px solid var(--line);list-style:none}
.dfb-check li{padding:8px 0 8px 34px;position:relative;border-bottom:1px solid var(--line);font-size:16px}
.dfb-check li:last-child{border-bottom:0}
.dfb-check li::before{content:"";position:absolute;left:0;top:13px;width:18px;height:18px;border-radius:6px;border:1.5px solid var(--forest2)}
/* faq */
.dfb details{border-bottom:1px solid #1412142b}.dfb details:first-of-type{border-top:1px solid #1412142b}
.dfb summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;padding:20px 0;font:400 23px/1.25 var(--serif);color:var(--ink)}
.dfb summary::-webkit-details-marker{display:none}
.dfb summary::after{content:"+";font:300 24px/1 var(--sans);color:var(--forest2)}
.dfb details[open] summary::after{content:"–"}
.dfb details p{font-size:16.5px}
/* cta */
.dfb-cta{margin:clamp(56px,7vw,100px) 0 0;padding:clamp(40px,6vw,80px) clamp(20px,4vw,60px);text-align:center;background:radial-gradient(50% 80% at 10% 100%,#5E7F6B66,transparent 70%),radial-gradient(45% 70% at 95% 0%,#EBCFCB,transparent 70%),#EFE7DC}
.dfb-cta h2{font-size:clamp(40px,5vw,72px)}
.dfb-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:26px}
.dfb-btn{display:inline-flex;align-items:center;gap:10px;height:54px;padding:0 28px;border-radius:999px;font:500 13px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;background:var(--ink);color:var(--cream)!important}
.dfb-btn--ghost{background:transparent;color:var(--ink)!important;border:1px solid #1412142b}
.dfb-note{margin-top:30px;font-size:13px;color:var(--muted)}
"""


def article(IMG):
    t = []
    a = t.append
    a(f'<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">')
    a(f'<style>{CSS}</style>')
    a('<div class="dfb">')
    # hero
    a(f'''<header class="dfb-hero"><div class="dfb-wide dfb-hero__grid">
  <div><span class="dfb-label"><b>Ghid de design</b> · Deco&amp;Flair</span>
  <h2>Casa de sărbători:<br><em>renovare elegantă înainte de Crăciun.</em></h2>
  <p class="dfb-lead">Cum transformi peretele din spatele mesei de Crăciun într-o scenă de revistă, în patru săptămâni și pentru orice buget. Paleta de culori pentru 2027, șase rețete de perete, planul de lucru și produsele potrivite.</p>
  <div class="dfb-meta"><span>Timp de citire · 14 min</span><span>Nivel · de la începător</span><span>Buget · orice buzunar</span></div></div>
  <div class="dfb-arch"><img src="{IMG}01-coperta-masa-sub-rozeta.jpg" alt="Dining elegant cu masă rotundă, rozetă și cornișă decorativă" loading="eager"></div>
</div></header>''')
    toc = [("perete", "Peretele din spatele mesei e scena sărbătorilor"), ("paleta", "Paleta 2027: tonurile care vin"), ("plan", "Planul în 4 săptămâni"),
           ("retete", "Șase rețete de perete pentru masa de Crăciun"), ("buget", "Lux pentru orice buzunar: 3 niveluri"), ("masa", "Masa de Crăciun pe paleta 2027"),
           ("greseli", "Greșeli de evitat"), ("checklist", "Checklist înainte de musafiri"), ("intrebari", "Întrebări frecvente")]
    a('<div class="dfb-in"><nav class="dfb-toc"><span class="dfb-label"><b>Cuprins</b></span><ol>' + "".join(f'<li><a href="#{i}"><b>{k+1:02d}</b>{e(s)}</a></li>' for k, (i, s) in enumerate(toc)) + '</ol></nav></div>')
    # 1
    a(f'''<section class="dfb-sec" id="perete"><div class="dfb-in"><span class="dfb-label"><b>01</b> · De unde începem</span>
<h2>Peretele din spatele mesei<br><em>e scena sărbătorilor.</em></h2>
<p>În decembrie, aproape toată viața casei se mută în jurul mesei. Acolo se strâng familia și prietenii, acolo se fac fotografiile pe care le vei revedea ani de zile. Și aproape în toate acele fotografii apare un singur fundal: <strong>peretele din spatele mesei</strong>.</p>
<p>De aceea, dacă ai timp și buget pentru un singur proiect înainte de sărbători, acesta e proiectul. Nu ai nevoie de o renovare completă: un perete gândit corect, cu profile decorative, lumină caldă și culoarea potrivită, schimbă percepția întregii camere.</p>
<blockquote class="dfb-quote">Luxul adevărat nu e mai mult. E mai bine gândit: proporție, lumină și un singur detaliu memorabil.</blockquote>
<p>La Deco&amp;Flair lucrăm zilnic cu arhitecți, designeri și clienți care vor un rezultat de revistă cu bugete foarte diferite. În ghidul de mai jos am adunat ce funcționează cu adevărat: paleta pe care o vedem crescând pentru 2027, șase „rețete” de perete testate și un plan realist de patru săptămâni, ca totul să fie gata înainte de Ajun.</p>
<div class="dfb-know"><i>✦</i><div><small>Know-how Deco&amp;Flair</small>Fotografiază peretele de acum din locul în care vei sta la masă. Ce vezi în poză e exact ce vor vedea musafirii: de acolo pornește designul.</div></div>
</div></section>''')
    # 2 paleta
    sw = "".join(f'<div class="dfb-sw"><span style="background:{c}"></span><div><b>{e(n)}</b><code>{c}</code><br>{e(d)}</div></div>' for n, c, d in PALETA)
    combos = [(["#2F4A3C", "#F1E8DC", "#B08D57"], "Forest + crem + alamă", "Clasicul elegant: chenare verzi, tavan crem, accente aurii pe masă."),
              (["#EBCFCB", "#A6919F", "#F1E8DC"], "Roz pudră + mov șters", "Romantic și sofisticat: perfect pentru relief 3D și lumânări albe."),
              (["#1A1719", "#A9BBAA", "#E6D7C8"], "Onix + salvie + nude", "Modern-dramatic: riflaj închis, textile salvie, ceramică nude.")]
    cb = "".join(f'<div><i>{"".join(f"<span style=\'background:{c}\'></span>" for c in cs)}</i><b>{e(n)}</b><br>{e(d)}</div>' for cs, n, d in combos)
    a(f'''<section class="dfb-sec" id="paleta"><div class="dfb-in"><span class="dfb-label"><b>02</b> · Culoare</span>
<h2>Paleta 2027:<br><em>tonurile care vin.</em></h2>
<p>După ani de alb rece și gri, interioarele se încălzesc. Vedem tot mai des, în proiectele partenerilor noștri și în colecțiile producătorilor, nuanțe <strong>naturale, prăfuite, catifelate</strong>: verdele de pădure, rozul pudrat, movul șters, cremul cald, cu accente fine de negru onix. Este paleta pe care o recomandăm pentru casa de sărbători din 2027. Arată festiv în decembrie și rămâne elegantă tot anul.</p>
<div class="dfb-pal">{sw}</div>
<h3 style="margin-top:40px">Trei combinații care nu greșesc</h3>
<div class="dfb-combo">{cb}</div>
{fig("08-moodboard-paleta", "Moodboard: profile, riflaj și marmură în tonuri calde. Imagine de inspirație.", IMG)}
<div class="dfb-know"><i>✦</i><div><small>Know-how Deco&amp;Flair</small>Vopsește profilele în aceeași culoare cu peretele (ton-pe-ton). Relieful se vede doar prin umbră: e cea mai elegantă și cea mai iertătoare variantă.</div></div>
<p class="dfb-note">Paleta reprezintă recomandarea editorială Deco&amp;Flair pentru 2027, nu o listă oficială de culori ale anului.</p>
</div></section>''')
    # 3 plan
    pl = "".join(f'<div><small>{e(s)}</small><b>{e(ti)}</b>{e(d)}</div>' for s, ti, d in PLAN)
    a(f'''<section class="dfb-sec" id="plan"><div class="dfb-wide"><div class="dfb-in" style="padding:0"><span class="dfb-label"><b>03</b> · Calendar</span>
<h2>Planul în 4 săptămâni,<br><em>fără stres de ultim moment.</em></h2>
<p>Profilele decorative se montează repede, dar adezivul, chitul și vopseaua au nevoie de timp. Cel mai sigur e să începi cu 3–4 săptămâni înainte de Crăciun:</p></div>
<div class="dfb-plan">{pl}</div></div></section>''')
    # 4 rețete
    rs = []
    for r in RETETE:
        rs.append(f'''<article class="dfb-r" id="{r["id"]}"><div class="dfb-r__img"><img src="{IMG}{r["img"]}.jpg" alt="{e(r["titlu"])}" loading="lazy"></div>
<div><span class="dfb-r__n">{r["n"]}</span><h3>{e(r["titlu"])}</h3>
<div class="dfb-r__tags"><span>{e(r["stil"])}</span><span>{e(r["buget"])}</span></div>
<p>{e(r["text"])}</p>
<ol class="dfb-steps">{"".join(f"<li>{e(s)}</li>" for s in r["pasi"])}</ol>
<span class="dfb-label" style="margin-top:10px"><b>Produsele rețetei</b></span>
<div class="dfb-ps">{"".join(pcard(k, IMG) for k in r["produse"])}</div></div></article>''')
    a(f'''<section class="dfb-sec" id="retete"><div class="dfb-wide"><div class="dfb-in" style="padding:0"><span class="dfb-label"><b>04</b> · Inspirație</span>
<h2>Șase rețete de perete<br><em>pentru masa de Crăciun.</em></h2>
<p>Fiecare rețetă pornește de la același principiu: un singur perete-vedetă, în spatele mesei, și restul camerei care îl susține. Alege-o pe cea care se potrivește casei tale, nu pe cea mai spectaculoasă.</p></div>
{"".join(rs)}</div></section>''')
    # 5 niveluri
    lv = "".join(f'<div><b>{e(n)}</b><small>{e(s)}</small><p>{e(d)}</p><ul>{"".join(f"<li><a href=\'{PR[k]['url']}\'>{e(PR[k]['name'])} <span>→</span></a></li>" for k in ks)}</ul></div>' for n, s, d, ks in NIVELURI)
    a(f'''<section class="dfb-sec" id="buget"><div class="dfb-wide"><div class="dfb-in" style="padding:0"><span class="dfb-label"><b>05</b> · Buget</span>
<h2>Lux pentru<br><em>orice buzunar.</em></h2>
<p>Eleganța nu ține de preț, ține de alegeri. Am împărțit proiectul în trei niveluri, ca să poți începe cu ce ai acum și să adaugi detalii în timp, fără să refaci nimic.</p></div>
<div class="dfb-lv">{lv}</div>
<div class="dfb-in" style="padding:0">{fig("09-valuri-relief", "Relieful 3D în ton cald: varianta Signature. Imagine de inspirație.", IMG)}</div></div></section>''')
    # 6 masa
    a(f'''<section class="dfb-sec" id="masa"><div class="dfb-in"><span class="dfb-label"><b>06</b> · Styling</span>
<h2>Masa de Crăciun<br><em>pe paleta 2027.</em></h2>
<p>Peretele e scena; masa e povestea. Iată cum le legi într-un singur tablou, fără să pară decor de vitrină:</p>
<div class="dfb-table">
<div><b>Textile</b>Față de masă din in natural sau catifea în salvie ori mov șters. Șervete în roz pudră legate cu panglică de mătase.</div>
<div><b>Lumină</b>Lumânări albe sau crem, la înălțimi diferite, în sfeșnice de alamă. Stinge spoturile: rămân LED-ul indirect și flăcările.</div>
<div><b>Verdeață</b>Ramuri de eucalipt, brad și măslin, puse liber pe centrul mesei. Verdele face legătura cu peretele forest.</div>
<div><b>Veselă</b>Porțelan alb sau nude, pahare din sticlă fumurie, tacâmuri aurii sau negre mat. Mai puține piese, dar mai bune.</div>
</div>
{fig("06-dining-lamele-lemn", "Dining cald, cu lemn și lumină naturală: baza perfectă pentru o masă de sărbători. Imagine de inspirație.", IMG)}
<div class="dfb-know"><i>✦</i><div><small>Know-how Deco&amp;Flair</small>Fotografiază masa în „ora albastră” (imediat după apus), cu lumina indirectă aprinsă. Relieful peretelui și flăcările lumânărilor ies spectaculos, fără blitz.</div></div>
</div></section>''')
    # 7 greșeli
    gr = "".join(f'<div><b>{e(x)}</b>{e(y)}</div>' for x, y in GRESELI)
    a(f'''<section class="dfb-sec" id="greseli"><div class="dfb-in"><span class="dfb-label"><b>07</b> · Atenție</span>
<h2>Greșeli de evitat.</h2><div class="dfb-err">{gr}</div></div></section>''')
    # 8 checklist
    ck = ["Am ales peretele-scenă și l-am fotografiat de la masă.", "Am ales paleta (2–3 tonuri + un metal).", "Am măsurat peretele și am calculat necesarul de bare (+10–15%).",
          "Am comandat profilele, adezivul și vopseaua cu 3–4 săptămâni înainte.", "Am montat, chituit și vopsit; am respectat timpii de uscare.", "Am instalat LED-ul cald (2700–3000K) și un dimmer.",
          "Am făcut o repetiție de lumină seara.", "Am pregătit masa: textile, lumânări, verdeață."]
    a(f'''<section class="dfb-sec" id="checklist"><div class="dfb-in"><span class="dfb-label"><b>08</b> · De bifat</span>
<h2>Checklist<br><em>înainte de musafiri.</em></h2><ul class="dfb-check">{"".join(f"<li>{e(x)}</li>" for x in ck)}</ul></div></section>''')
    # selecție completă
    allp = ["wo2", "z1360", "wl6", "z11", "z21", "r12", "wave", "canele", "l5", "il18", "il11", "rif-deschis", "rif-inchis", "c82603", "c82671", "fd21", "adefix"]
    a(f'''<section class="dfb-sec" id="selectie"><div class="dfb-wide"><div class="dfb-in" style="padding:0"><span class="dfb-label"><b>Selecția Deco&amp;Flair</b></span>
<h2>Toate produsele<br><em>din acest ghid.</em></h2></div>
<div class="dfb-ps" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr))">{"".join(pcard(k, IMG) for k in allp)}</div></div></section>''')
    # faq
    fq = "".join(f'<details><summary>{e(q)}</summary><p>{e(r)}</p></details>' for q, r in FAQ)
    a(f'''<section class="dfb-sec" id="intrebari"><div class="dfb-in"><span class="dfb-label"><b>09</b> · FAQ</span><h2>Întrebări<br><em>frecvente.</em></h2>{fq}</div></section>''')
    # cta
    a(f'''<section class="dfb-cta"><span class="dfb-label"><b>Consultanță premium</b></span>
<h2>Vrei ca peretele tău<br><em>să fie gata de Crăciun?</em></h2>
<p>Trimite-ne o fotografie a camerei. Îți recomandăm profilele, culoarea și calculăm necesarul, gratuit.</p>
<div class="dfb-btns"><a class="dfb-btn" href="tel:+40723300603">Sună: 0723 300 603</a><a class="dfb-btn dfb-btn--ghost" href="{SITE}consultanta-premium">Consultanță premium</a><a class="dfb-btn dfb-btn--ghost" href="{SITE}randare-3d">Randare 3D</a></div>
<p class="dfb-note">Luni–Vineri, 07:30–16:00 · office@decoflair.ro · Imaginile ambientale din articol sunt orientative, cu rol de inspirație.</p></section>''')
    a('</div>')
    return "\n".join(t)


if __name__ == "__main__":
    frag = article(IMG_SITE)
    assert " lei" not in frag
    (ROOT / "articol.html").write_text("<!-- Articol blog Deco&Flair · se lipește în editorul articolului (mod Cod sursă). Imaginile: " + IMG_SITE + " -->\n" + frag, encoding="utf-8")
    prev = f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Previzualizare · Casa de sărbători · Deco&amp;Flair</title><style>body{{margin:0;background:#fff;font-family:Jost,sans-serif}} .pg{{max-width:1240px;margin:24px auto;padding:0 12px}} .pg>h1{{font:500 28px Jost,sans-serif;margin:0 0 16px}}</style></head>
<body><div class="pg"><h1>Casa de sărbători: ghidul de design pentru o renovare elegantă înainte de Crăciun</h1>{article("img/")}</div></body></html>'''
    (ROOT / "previzualizare.html").write_text(prev, encoding="utf-8")
    print("OK")

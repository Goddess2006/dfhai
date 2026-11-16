#!/usr/bin/env python3
"""Articol de blog NMC România: „Galeria NMC” — ghid de amenajare interioară și exterioară.

Rezultate:
  articol.html          → fragmentul de lipit în editorul articolului (mod Cod sursă), CSS izolat sub .nmg
  previzualizare.html   → același articol într-o pagină de test (imagini locale)
Rulare: python3 nmc-blog-galerie/tools/build.py
"""
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.nmcromania.ro/"
IMG_SITE = "/image/catalog/blog/galeria-nmc/"

def P(id, name, mat, dim, url, colectie):
    return dict(id=id, name=name, mat=mat, dim=dim, url=SITE + quote(url, safe="/-"), col=colectie)

PR = {p["id"]: p for p in [
    P("na105", "Ancadrament NA105", "Polistiren cu strat mineral ADRo®", "175 × 40 × 2000 mm", "ancadrament-decorativ-na105", "Fațadă"),
    P("rema3", "Ancadrament REMA3", "Polistiren cu strat mineral ADRo®", "135 × 25 × 2000 mm", "ancadrament-decorativ-rema3", "Fațadă"),
    P("ns108", "Solbanc NS108", "Polistiren cu strat mineral ADRo®", "125 × 100 × 2000 mm", "pervazsolbanc-ns108", "Fațadă"),
    P("ncl107", "Colțar NCL107", "Polistiren cu strat mineral ADRo®", "300/300 × 30 × 1000 mm", "coltar-exterior-decorativ-polistiren-ncl107-1000x30x300", "Fațadă"),
    P("nc158", "Cornișă NC158", "Polistiren cu strat mineral ADRo®", "200 × 127 × 2000 mm", "cornisa-decorativa-nc158", "Fațadă"),
    P("nc104", "Cornișă NC104", "Polistiren cu strat mineral ADRo®", "220 × 80 × 2000 mm", "cornisa-decorativa-exterior-nc104-220x80x2000", "Fațadă"),
    P("fuga1", "Termosistem FUGA PANEL 1", "Termosistem decorativ ADRo®", "500 × 40 × 2000 mm", "termosistem-decorativ-fuga-panel-1-de-4-cm-500x40x2000", "Fațadă"),
    P("sid3", "Termosistem SIDDING PANEL 3", "Termosistem decorativ ADRo®", "500 × 40 × 2000 mm", "termosistem-decorativ-sidding-panel-3-500x40x2000", "Fațadă"),
    P("npp1", "Pilastru NPP1", "Polistiren cu strat mineral ADRo®", "250 × 30 × 2000 mm", "pilastru-coloana-decorativanpp1", "Fațadă"),
    P("a106", "Ornament 3D A106", "Polistiren cu strat mineral ADRo®", "600 × 450 × 55 mm", "accent-3d-a106-600x450x55", "Fațadă"),
    P("il11", "Plintă LED IL11 neagră", "Polimer dur · Noël & Marquet", "80 × 20 × 2000 mm", "plinta-decorativa-il11-neagra-80x20x2000", "Lumină"),
    P("z19", "Cornișă Z19", "Poliuretan · Arstyl", "79 × 79 × 2000 mm", "plinta-decorativa-tavan-arstyl-z19", "Tavan"),
    P("wt10", "Cornișă WT10", "Polimer dur · Wallstyl", "84 × 84 × 2000 mm", "cornisa-decorativawt10-wallstyl", "Tavan"),
    P("wt17", "Cornișă WT17", "Polimer dur · Noël & Marquet", "95 × 95 × 2000 mm", "cornisa-decorativa-wt17", "Tavan"),
    P("r8", "Rozetă R8", "Poliuretan · Arstyl", "Ø 495 mm", "rozeta-decorativar8-arstyl", "Tavan"),
    P("wl11", "Profil WL11", "Polimer dur · Wallstyl", "49 × 15 × 2000 mm", "profil-decorativ-wl11", "Pereți"),
    P("z1360", "Brâu Z1360", "Polimer dur · Noël & Marquet", "60 × 15 × 2000 mm", "brau-z1360", "Pereți"),
    P("fl2", "Plintă FL2", "Polimer dur · Wallstyl", "120 × 15 × 2000 mm", "plintafl2-wallstyl", "Pereți"),
    P("ft2", "Plintă FT2 neagră", "Polimer dur · Noël & Marquet", "58 × 13 × 2000 mm", "plinta-decorativa-ft2-neagra-58x13x2000", "Pereți"),
    P("riflaj-deschis", "Riflaj acustic · stejar deschis", "Panou acustic 3D · NMC", "565 × 2600 × 19 mm", "riflaj-acustic-panou-3d-stejar-deschis", "Textură"),
    P("riflaj-inchis", "Riflaj acustic · stejar închis", "Panou acustic 3D · NMC", "565 × 2600 × 19 mm", "riflaj-acustic-panou-3d-stejar-inchis", "Textură"),
    P("c82671", "Tapet Carrara Best 82671", "Tapet de designer", "rolă", "tapet-carrara-82671", "Textură"),
    P("rc19070", "Tapet Roberto Cavalli 19070", "Tapet de designer", "rolă", "tapet-roberto-cavalli-8-19070", "Textură"),
]}

# Fiecare „sală” are opere (exponate): imagine + problema ascunsă + soluția + produsele
GRAD = {
    "fatada": "linear-gradient(135deg,#FF9A6B 0%,#F27BAE 50%,#9C8CF2 100%)",
    "lumina": "linear-gradient(135deg,#FFB547 0%,#FF7A59 55%,#E8507E 100%)",
    "tavan": "linear-gradient(135deg,#6C7CF7 0%,#9A6DF0 50%,#D27BEA 100%)",
    "pereti": "linear-gradient(135deg,#2BB5A0 0%,#57C5D8 50%,#7E9CF4 100%)",
    "textura": "linear-gradient(135deg,#C98A63 0%,#D9798F 50%,#8F7BD6 100%)",
}

SALI = [
    dict(id="fatada", nr="I", nume="Fațada", sub="Prima impresie, de la poartă", intro=
         "Musafirii îți „citesc” casa în primele secunde, de la poartă. Nu analizează materialele: simt proporția, umbra și finisajul. O fațadă fără detalii arhitecturale pare neterminată, oricât de scump a fost construită.",
         opere=[
            dict(img="ext-ferestre", titlu="Fereastra care nu are ramă", prob="Ferestrele par „lipite” pe perete, iar fațada arată plată, fără umbră. În plus, la baza ferestrei, apa de ploaie se scurge direct pe tencuială și lasă dâre.",
                 sol="Un ancadrament încadrează fereastra exact cum o ramă încadrează un tablou: creează umbră, adâncime și proporție. Solbancul de dedesubt îndepărtează apa de perete și protejează tencuiala.",
                 prod=["na105", "rema3", "ns108"]),
            dict(img="nc158-amb", titlu="Colțul care se uzează primul", prob="Colțurile clădirii sunt cele mai expuse: se lovesc, se fisurează și sunt primele care trădează vârsta fațadei.",
                 sol="Colțarul decorativ transformă un punct slab într-un detaliu de arhitectură clasică. Profilul este rezistent la șocuri, UV, îngheț și umezeală și se vopsește în orice culoare.",
                 prod=["ncl107"]),
            dict(img="hero-vila", titlu="Linia acoperișului", prob="Fără cornișă, peretele se oprește brusc sub streașină, iar îmbinarea dintre fațadă și acoperiș rămâne vizibilă și expusă.",
                 sol="Cornișa desenează o linie de umbră care „încununează” casa și maschează elegant îmbinarea. Este detaliul care face diferența între o clădire oarecare și o vilă.",
                 prod=["nc158", "nc104"]),
            dict(img="fuga1-amb", titlu="Pielea casei", prob="Fațadele mai vechi au adesea izolație subțire și un aspect demodat. Renovarea clasică înseamnă două șantiere: unul pentru izolație, altul pentru finisaj.",
                 sol="Termosistemele decorative combină finisajul cu izolația într-un singur sistem: rosturi tip piatră (FUGA) sau lambriu orizontal (SIDDING), fără întreținerea lemnului sau a pietrei naturale.",
                 prod=["fuga1", "sid3"]),
         ]),
    dict(id="lumina", nr="II", nume="Lumina", sub="Arta luminii indirecte", intro=
         "Într-o galerie nu vezi niciodată becul, vezi doar opera. Lumina indirectă face același lucru acasă: pune în valoare pereții și ascunde sursa.",
         opere=[
            dict(img="int-led", titlu="Lumina care obosește", prob="Spoturile din tavan luminează puternic, de sus, și aplatizează camera. Seara, lumina dură obosește ochii și face spațiul să pară mai mic.",
                 sol="O plintă cu LED trasează o linie fină de lumină la nivelul podelei. Ghidează pașii noaptea, alungește vizual camera și creează atmosfera unui hotel boutique.",
                 prod=["il11"]),
         ]),
    dict(id="tavan", nr="III", nume="Tavanul", sub="A cincea fațadă a camerei", intro=
         "Tavanul este suprafața pe care o vedem cel mai puțin și cea care schimbă cel mai mult proporțiile. Galeriile clasice știu asta de secole.",
         opere=[
            dict(img="z19-amb", titlu="Fisura pe care o tot vopsești", prob="La îmbinarea dintre tavan și perete apar des fisuri fine, care revin după fiecare zugrăveală.",
                 sol="Cornișa acoperă elegant îmbinarea și transformă o problemă de finisaj într-un detaliu de arhitectură. Bonus: o cornișă bine aleasă face camera să pară mai înaltă.",
                 prod=["z19", "wt10", "wt17"]),
            dict(img="r8-amb", titlu="Lustra fără „scenă”", prob="Corpul de iluminat pare suspendat la întâmplare, iar în jurul lui se văd adesea urme de la găurile vechi.",
                 sol="Rozeta din poliuretan creează un punct focal deasupra mesei sau a canapelei și ascunde imperfecțiunile din jurul prinderii.",
                 prod=["r8"]),
         ]),
    dict(id="pereti", nr="IV", nume="Pereții", sub="Simezele casei tale", intro=
         "Un perete gol nu este minimalist, este neterminat. În stil scandinav, pereții au structură discretă: chenare fine, plinte curate, totul în tonuri calde și luminoase.",
         opere=[
            dict(img="sala-perete-chenare", titlu="Peretele care nu „ține” mobila", prob="Canapeaua, patul sau masa par puse la întâmplare, pentru că peretele din spate nu are nicio structură care să le ancoreze.",
                 sol="Chenarele din profile subțiri desenează „simeze” pe perete: zone clare în care mobila și tablourile își găsesc locul. Vopsite ton-pe-ton, arată sculptate.",
                 prod=["wl11", "z1360"]),
            dict(img="int-elegant", titlu="Plinta care pare ieftină", prob="Plintele joase din PVC fac orice interior să pară provizoriu, iar dâre de la mătură și aspirator apar pe pereți.",
                 sol="O plintă înaltă din polimer dur protejează baza pereților și dă camerei o fundație vizuală solidă. Varianta neagră creează contrastul grafic preferat de designul scandinav contemporan.",
                 prod=["fl2", "ft2"]),
         ]),
    dict(id="textura", nr="V", nume="Textura", sub="Liniște, lemn și marmură", intro=
         "Ultima sală este despre simțuri: cum sună camera și ce simți când atingi peretele. Aici stă diferența dintre o casă frumoasă și una în care te simți bine.",
         opere=[
            dict(img="int-living", titlu="Ecoul din open-space", prob="Pardoselile dure, pereții goi și ferestrele mari fac ca vocile să răsune. La o masă cu musafiri, conversația devine obositoare.",
                 sol="Riflajul acustic cu aspect de stejar absoarbe o parte din ecou și aduce căldura lemnului, exact elementul cheie al stilului scandinav.",
                 prod=["riflaj-deschis", "riflaj-inchis"]),
            dict(img="c82671-amb", titlu="Peretele fără personalitate", prob="Un dormitor sau un living poate fi perfect funcțional și totuși impersonal.",
                 sol="Un singur perete cu tapet de designer, cu efect de marmură sau model grafic, devine opera centrală a camerei.",
                 prod=["c82671", "rc19070"]),
         ]),
]

REGULI = [
    ("Lumina naturală e prima operă", "Nu o bloca. Alege tonuri deschise, calde, care o reflectă: alb cald, gresie, nisip, gri perlat."),
    ("Rama face opera", "Ferestre, uși, tavane și pereți arată „scump” doar când sunt încadrați: ancadramente, cornișe, chenare."),
    ("Spațiul gol e un lux", "Mai puține obiecte, mai bine alese. Lasă aer între chenare, între mobile, între decorațiuni."),
    ("Lemnul și albul cald", "Combinația scandinavă care nu se demodează: profile albe, riflaj din stejar, textile naturale."),
    ("Detaliul se vede de aproape", "Îmbinări curate, chit fin, vopsea uniformă. Galeriile sunt perfecte la un pas distanță."),
]

TENDINTE = [
    ("Rămân", ["Profile albe vopsite ton-pe-ton", "Lumină indirectă, caldă", "Lemn natural și riflaj", "Chenare fine, proporționate", "Fațade albe/nisip cu ancadramente"]),
    ("Trec", ["Tavane false cu multe spoturi", "Gri rece pe toate suprafețele", "Plinte joase din PVC", "Pereți de accent în culori stridente", "Fațade fără nicio umbră"]),
]

STILURI = [
    ("Scandinav cald", "Alb cald, stejar, in și lână.", ["wl11", "fl2", "riflaj-deschis", "z19"]),
    ("Clasic parizian", "Chenare mari, cornișă, rozetă, parchet în spic.", ["z1360", "wt17", "r8", "fl2"]),
    ("Minimal contemporan", "Linii negre, lumină ascunsă, contrast grafic.", ["ft2", "il11", "wt10", "riflaj-inchis"]),
]

FAQ = [
    ("Profilele de exterior rezistă în timp?", "Profilele ADRo® sunt realizate din polistiren de înaltă densitate, protejat cu un strat mineral, și sunt rezistente la șocuri, radiații UV, îngheț și umezeală. Se vopsesc cu vopsea acrilică de exterior, în orice culoare."),
    ("Pot monta singur profilele de interior?", "Da. Profilele de interior se lipesc cu adeziv, se taie cu un fierăstrău fin și o cutie de îmbinări, apoi se chituiesc îmbinările și se vopsesc. Pentru fațade și termosisteme recomandăm o echipă de montaj."),
    ("Cum aleg dimensiunea potrivită?", "Regula de bază: profilul trebuie să fie proporțional cu suprafața. Pe tavane înalte și fațade mari alege secțiuni generoase; în camere mici, profile fine. Echipa NMC te ajută gratuit cu alegerea și cu necesarul."),
    ("Cât de repede primesc produsele?", "NMC menține stocuri mari, iar produsele aflate în stoc se pregătesc imediat pentru livrare. Disponibilitatea apare pe pagina fiecărui produs."),
    ("Se potrivesc profilele într-un apartament?", "Absolut. Tocmai în spațiile standard, o cornișă, o plintă înaltă sau câteva chenare fac cea mai mare diferență, fără lucrări de construcție."),
]

CSS = r"""
.nmg{--ink:#16151C;--ink2:#3C3A46;--muted:#77737F;--line:#16151C14;--orange:#FF671F;--orange2:#FF9A5C;
 --g-hero:linear-gradient(125deg,#FFE3D3 0%,#F6D3E6 28%,#D9D4F7 58%,#CDE9F2 100%);
 --g-brand:linear-gradient(100deg,#FF671F 0%,#F2459B 45%,#7B5CF5 100%);
 --display:"Space Grotesk",system-ui,sans-serif;--sans:"Roboto",system-ui,sans-serif;
 font:300 17.5px/1.8 var(--sans);color:var(--ink2);background:#FBFAFD;border-radius:28px;overflow:hidden;position:relative}
.nmg *{box-sizing:border-box}.nmg img{display:block;max-width:100%;height:auto}.nmg a{color:inherit;text-decoration:none}
.nmg p{margin:0 0 1em}.nmg strong{font-weight:500;color:var(--ink)}
.nmg h2,.nmg h3{font-family:var(--display);font-weight:500;color:var(--ink);letter-spacing:-.035em;margin:0}
.nmg h2{font-size:clamp(36px,4.6vw,64px);line-height:1.02;margin-bottom:20px}
.nmg h3{font-size:clamp(26px,2.6vw,36px);line-height:1.1;margin-bottom:12px}
.nmg h2 em,.nmg h3 em{font-style:normal;background:var(--g-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
.nmg-in{max-width:860px;margin:0 auto;padding:0 clamp(18px,4vw,40px)}
.nmg-wide{max-width:1200px;margin:0 auto;padding:0 clamp(18px,4vw,40px)}
.nmg-kick{display:inline-flex;align-items:center;gap:10px;margin-bottom:16px;padding:7px 14px;border-radius:999px;background:#ffffffb3;border:1px solid #ffffff;backdrop-filter:blur(10px);font:500 11px/1 var(--sans);letter-spacing:.24em;text-transform:uppercase;color:var(--ink)}
.nmg-kick::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--g-brand)}
.nmg-sec{padding:clamp(56px,7vw,110px) 0 0}
/* „rama” = ecran de expoziție digitală */
.nmg-frame{position:relative;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 40px 80px -40px #3B2A6E66,0 0 0 1px #ffffff}
.nmg-frame::after{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px #ffffff66;pointer-events:none}
.nmg-frame img{width:100%;object-fit:cover}
/* hero */
.nmg-hero{position:relative;padding:clamp(56px,8vw,120px) 0 clamp(40px,5vw,70px);text-align:center;background:var(--g-hero);overflow:hidden}
.nmg-hero::before,.nmg-hero::after{content:"";position:absolute;border-radius:50%;filter:blur(70px);opacity:.8;pointer-events:none}
.nmg-hero::before{width:520px;height:520px;left:-140px;top:-120px;background:#FFB48A}
.nmg-hero::after{width:560px;height:560px;right:-160px;bottom:-200px;background:#9DB8FF}
.nmg-hero>*{position:relative;z-index:1}
.nmg-hero h2{font-size:clamp(46px,7vw,104px);line-height:.95;margin:18px 0 24px}
.nmg .nmg-lead{max-width:680px;margin:0 auto;font-size:19.5px;color:var(--ink2)}
.nmg-meta{display:flex;justify-content:center;flex-wrap:wrap;gap:8px 10px;margin-top:24px}
.nmg-meta span{padding:7px 14px;border-radius:999px;background:#ffffff80;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}
.nmg-hero .nmg-frame{max-width:1000px;margin:clamp(36px,5vw,64px) auto 0}
.nmg-hero .nmg-frame img{aspect-ratio:16/9}
.nmg-label{display:inline-flex;flex-direction:column;margin-top:12px;padding:10px 16px;border-radius:14px;background:#ffffffcc;border:1px solid #fff;backdrop-filter:blur(10px);text-align:left;font-size:12.5px;line-height:1.5;color:var(--muted)}
.nmg-label b{font:500 15px/1.3 var(--display);color:var(--ink);letter-spacing:-.01em}
/* harta expoziției */
.nmg-plan{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:clamp(36px,4vw,56px)}
.nmg-plan a{padding:20px 14px;border-radius:18px;background:var(--g);color:#fff;text-align:left;transition:transform .3s}
.nmg-plan a:hover{transform:translateY(-4px)}
.nmg-plan b{display:block;font:500 32px/1 var(--display);letter-spacing:-.03em}
.nmg-plan span{display:block;margin-top:10px;font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.9}
@media (max-width:760px){.nmg-plan{grid-template-columns:1fr 1fr}}
/* reguli */
.nmg-rules{counter-reset:r;margin:22px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.nmg-rules li{counter-increment:r;display:grid;grid-template-columns:56px 1fr;gap:16px;padding:18px 20px;border-radius:18px;background:#fff;border:1px solid var(--line)}
.nmg-rules li::before{content:"0" counter(r);font:500 22px/1 var(--display);background:var(--g-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
.nmg-rules b{display:block;font:500 20px/1.25 var(--display);color:var(--ink);margin-bottom:4px;letter-spacing:-.01em}
/* sală = încăpere a expoziției, cu degradeul ei */
.nmg-room{margin-top:clamp(56px,7vw,100px);padding:clamp(56px,7vw,100px) 0;background:var(--g);position:relative}
.nmg-room::before{content:"";position:absolute;inset:0;background:radial-gradient(60% 50% at 80% 0%,#ffffff55,transparent 70%),linear-gradient(180deg,transparent 60%,#FBFAFD 100%);pointer-events:none}
.nmg-room>*{position:relative}
.nmg-room__head{text-align:left;max-width:760px}
.nmg-room__nr{display:block;margin-bottom:12px;font:500 clamp(64px,8vw,120px)/.9 var(--display);letter-spacing:-.05em;color:#ffffffd9}
.nmg-room__head h2{margin-top:4px;color:#fff}
.nmg-room__head .sub{display:inline-block;padding:6px 12px;border-radius:999px;background:#ffffff33;font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:#fff}
.nmg .nmg-room__head p{margin-top:18px;color:#ffffffe6;font-size:18.5px}
.nmg-work{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(24px,4vw,56px);align-items:start;margin-top:clamp(36px,4vw,60px);padding:clamp(18px,2.4vw,30px);border-radius:28px;background:#ffffffd9;backdrop-filter:blur(16px);border:1px solid #ffffff;box-shadow:0 40px 80px -50px #1d123d55}
.nmg-work:nth-child(even) .nmg-work__art{order:2}
.nmg-work__art .nmg-frame img{aspect-ratio:4/3}
.nmg-work__nr{display:inline-block;padding:5px 11px;border-radius:999px;background:var(--g);color:#fff;font-size:11px;letter-spacing:.2em;text-transform:uppercase}
.nmg-work h3{margin-top:12px}
.nmg-pb{margin:16px 0;padding:16px 18px;border-radius:16px;background:#FFF2EA;border:1px solid #FFD9C4}
.nmg-sol{padding:16px 18px;border-radius:16px;background:#F2F0FF;border:1px solid #DCD6FF}
.nmg-pb small,.nmg-sol small{display:block;font-size:10.5px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--orange);margin-bottom:6px}
.nmg-sol small{color:#6A4FE0}
@media (max-width:860px){.nmg-work{grid-template-columns:1fr}.nmg-work:nth-child(even) .nmg-work__art{order:0}}
/* exponate */
.nmg-pieces{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-top:18px}
.nmg-piece{display:flex;flex-direction:column;border-radius:18px;background:#fff;border:1px solid var(--line);overflow:hidden;transition:transform .35s,box-shadow .35s}
.nmg-piece:hover{transform:translateY(-4px);box-shadow:0 24px 40px -26px #3B2A6E88}
.nmg-piece .nmg-frame{border-radius:0;box-shadow:none;padding:8px}
.nmg-piece .nmg-frame::after{display:none}
.nmg-piece .nmg-frame img{aspect-ratio:1;object-fit:contain;border-radius:12px}
.nmg-piece .nmg-label{display:block;margin:0;border:0;border-radius:0;background:transparent;padding:4px 12px 14px;font-size:11.5px;backdrop-filter:none}
.nmg-piece .nmg-label b{display:block;font-size:15px}
.nmg-piece .nmg-label i{display:inline-block;margin-top:6px;font-style:normal;font-size:10.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;background:var(--g-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
@media (max-width:560px){.nmg-pieces{grid-template-columns:1fr 1fr;gap:8px}}
/* tabel */
.nmg-table{width:100%;border-collapse:separate;border-spacing:0;margin-top:24px;font-size:15.5px;background:#fff;border-radius:22px;overflow:hidden;border:1px solid var(--line)}
.nmg-table th,.nmg-table td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.nmg-table th{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#fff;font-weight:500;background:var(--g-brand)}
.nmg-table td:first-child{font:500 16.5px/1.3 var(--display);color:var(--ink);width:30%}
.nmg-table a{color:#6A4FE0;text-decoration:underline;text-underline-offset:3px}
@media (max-width:640px){.nmg-table,.nmg-table tbody,.nmg-table tr,.nmg-table td{display:block;width:100%!important}.nmg-table thead{display:none}.nmg-table tr{border-bottom:1px solid var(--line)}.nmg-table td{border:0;padding:6px 14px}}
/* tendințe + stiluri */
.nmg-trend{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:22px}
.nmg-trend div{padding:26px;border-radius:24px;color:#fff}
.nmg-trend div:first-child{background:linear-gradient(135deg,#1FA38A,#5BC6E8)}
.nmg-trend div:last-child{background:linear-gradient(135deg,#8A8796,#C9C6D3)}
.nmg-trend b{display:block;font:500 30px/1 var(--display);margin-bottom:12px;letter-spacing:-.03em}
.nmg-trend ul{margin:0;padding:0;list-style:none}.nmg-trend li{padding:8px 0;border-top:1px solid #ffffff40}
.nmg-trend div:first-child li::before{content:"✓";margin-right:10px}
.nmg-trend div:last-child li::before{content:"×";margin-right:10px}
@media (max-width:640px){.nmg-trend{grid-template-columns:1fr}}
.nmg-styles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px}
.nmg-styles>div{padding:24px;border-radius:24px;background:#fff;border:1px solid var(--line);position:relative;overflow:hidden}
.nmg-styles>div::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:var(--g)}
.nmg-styles b{display:block;font:500 24px/1.1 var(--display);color:var(--ink);letter-spacing:-.02em}
.nmg-styles p{margin:8px 0 12px;font-size:15px}
.nmg-styles ul{margin:0;padding:0;list-style:none;font-size:14.5px}
.nmg-styles li a{display:flex;justify-content:space-between;padding:7px 0;border-top:1px solid var(--line)}
.nmg-styles li a:hover{color:var(--orange)}
@media (max-width:820px){.nmg-styles{grid-template-columns:1fr}}
.nmg .nmg-quote{margin:clamp(50px,6vw,90px) auto 0;max-width:900px;padding:clamp(30px,4vw,56px);border-radius:28px;background:var(--g-hero);text-align:center;font:500 clamp(24px,3vw,38px)/1.25 var(--display);letter-spacing:-.025em;color:var(--ink)}
.nmg-quote span{display:block;margin-top:14px;font:500 11px/1 var(--sans);letter-spacing:.26em;text-transform:uppercase;color:var(--muted)}
.nmg details{margin-bottom:10px;padding:0 20px;border-radius:18px;background:#fff;border:1px solid var(--line)}
.nmg summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;padding:18px 0;font:500 19px/1.3 var(--display);color:var(--ink);letter-spacing:-.01em}
.nmg summary::-webkit-details-marker{display:none}.nmg summary::after{content:"+";font:400 22px/1 var(--sans);color:var(--orange)}
.nmg details[open] summary::after{content:"–"}
.nmg-cta{margin-top:clamp(70px,9vw,130px);padding:clamp(56px,8vw,110px) clamp(20px,4vw,60px);text-align:center;background:linear-gradient(125deg,#FF671F 0%,#F2459B 50%,#7B5CF5 100%);color:#fff}
.nmg-cta h2,.nmg-cta h2 em{color:#fff;-webkit-text-fill-color:#fff;background:none}
.nmg-cta .nmg-kick{color:var(--ink)}
.nmg-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:24px}
.nmg-btn{display:inline-flex;align-items:center;height:54px;padding:0 28px;border-radius:999px;font:500 13px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;background:#fff;color:var(--ink)!important;transition:transform .2s}
.nmg-btn:hover{transform:translateY(-2px)}
.nmg-btn--ghost{background:#ffffff26;color:#fff!important;border:1px solid #ffffff80}
.nmg-note{margin-top:28px;font-size:13px;opacity:.85}
.nmg h2,.nmg h3,.nmg-label b,.nmg-plan b,.nmg summary,.nmg-table td{font-variant-numeric:lining-nums}
"""


def piece(k, IMG):
    p = PR[k]
    return f'''<a class="nmg-piece" href="{p["url"]}"><div class="nmg-frame"><img src="{IMG}{p["id"]}.jpg" alt="{e(p["name"])}" loading="lazy"></div>
<span class="nmg-label"><b>{e(p["name"])}</b>{e(p["mat"])}<br>{e(p["dim"])}<br><i>Vezi exponatul →</i></span></a>'''


def article(IMG):
    t = []
    a = t.append
    a('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">')
    a(f"<style>{CSS}</style>")
    a('<div class="nmg">')
    plan = "".join(f'<a href="#{s["id"]}" style="--g:{GRAD[s["id"]]}"><b>{s["nr"]}</b><span>{e(s["nume"])}</span></a>' for s in SALI)
    a(f'''<header class="nmg-hero"><div class="nmg-wide">
<span class="nmg-kick">NMC prezintă · Expoziția virtuală a casei</span>
<h2>Galeria NMC:<br><em>casa ta, expusă ca o operă de artă.</em></h2>
<p class="nmg-lead">Un tur ghidat prin cinci săli: fațada, lumina, tavanul, pereții și textura. Pentru fiecare, problema pe care probabil nu știi că o ai și soluția care o transformă în detaliu de arhitectură.</p>
<div class="nmg-meta"><span>Timp de citire · 12 min</span><span>5 săli · 11 opere</span><span>Interior + exterior</span></div>
<div class="nmg-frame"><img src="{IMG}vila-alba.jpg" alt="Vilă albă cu ancadramente și cornișe decorative" loading="eager"></div>
<span class="nmg-label"><b>„Casa albă”</b>Fațadă cu ancadramente, cornișă și solbancuri · Profile decorative NMC</span>
<nav class="nmg-plan" aria-label="Planul galeriei">{plan}</nav></div></header>''')
    # intro + reguli
    rl = "".join(f'<li><div><b>{e(x)}</b>{e(y)}</div></li>' for x, y in REGULI)
    a(f'''<section class="nmg-sec"><div class="nmg-in"><span class="nmg-kick">Înainte de tur</span>
<h2>De ce privim altfel<br><em>o galerie de artă?</em></h2>
<p>Când intri într-un muzeu precum Luvrul, nu te întrebi din ce sunt făcute ramele sau cum e montată lumina. Simți doar că totul este <strong>la locul lui</strong>: proporții calme, lumină care pune în valoare, spațiu care te lasă să respiri.</p>
<p>Exact asta simt musafirii când intră într-o casă bine gândită. Nu numără metrii pătrați și nu știu ce mobilier ai cumpărat. Observă <strong>ramele</strong>: ferestre încadrate, colțuri finisate, tavane cu cornișă, pereți cu structură. Sunt detaliile care fac diferența între „frumos” și „wow, cine v-a făcut proiectul?”.</p>
<p>În acest ghid te luăm într-un tur prin cinci săli ale casei. Fiecare operă are o <strong>problemă ascunsă</strong>, una pe care majoritatea oamenilor o observă abia după ce au rezolvat-o, și o <strong>soluție NMC</strong>, prezentată ca un exponat, cu plăcuța lui de muzeu.</p>
<h3 style="margin-top:44px">Cele cinci reguli ale galeriei</h3>
<ol class="nmg-rules">{rl}</ol></div></section>''')
    # săli
    for s in SALI:
        works = []
        for i, o in enumerate(s["opere"]):
            works.append(f'''<article class="nmg-work"><div class="nmg-work__art"><div class="nmg-frame"><img src="{IMG}{o["img"]}.jpg" alt="{e(o["titlu"])}" loading="lazy"></div>
<span class="nmg-label"><b>„{e(o["titlu"])}”</b>Sala {s["nr"]} · {e(s["nume"])} · imagine de inspirație</span></div>
<div><span class="nmg-work__nr">Opera {s["nr"]}.{i+1}</span><h3>{e(o["titlu"])}</h3>
<div class="nmg-pb"><small>Problema pe care nu știi că o ai</small>{e(o["prob"])}</div>
<div class="nmg-sol"><small>Soluția NMC</small>{e(o["sol"])}</div>
<div class="nmg-pieces">{"".join(piece(k, IMG) for k in o["prod"])}</div></div></article>''')
        a(f'''<section class="nmg-room" id="{s["id"]}" style="--g:{GRAD[s["id"]]}"><div class="nmg-wide"><div class="nmg-room__head"><span class="nmg-room__nr">{s["nr"]}</span><span class="sub">Sala {s["nr"]} · {e(s["sub"])}</span><h2>{e(s["nume"])}</h2><p>{e(s["intro"])}</p></div>
{"".join(works)}</div></section>''')
    a('<p class="nmg-quote">„Într-o galerie nu vezi rama. Simți doar că opera e la locul ei.”<span>Ghidul NMC</span></p>')
    # tabel
    rows = []
    for s in SALI:
        for o in s["opere"]:
            links = ", ".join(f'<a href="{PR[k]["url"]}">{e(PR[k]["name"])}</a>' for k in o["prod"])
            rows.append(f'<tr><td>{e(o["titlu"])}</td><td>{e(o["prob"].split(".")[0])}.</td><td>{links}</td></tr>')
    a(f'''<section class="nmg-sec" id="probleme"><div class="nmg-wide"><span class="nmg-kick">Pe scurt</span>
<h2>Problemele pe care<br><em>nu știai că le ai.</em></h2>
<table class="nmg-table"><thead><tr><th>Problema</th><th>Cum o recunoști</th><th>Soluția NMC</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>''')
    # tendințe + stiluri
    tr = "".join(f'<div><b>{e(n)}</b><ul>{"".join(f"<li>{e(x)}</li>" for x in L)}</ul></div>' for n, L in TENDINTE)
    SG = ["linear-gradient(90deg,#57C5D8,#7E9CF4)","linear-gradient(90deg,#FF9A6B,#F27BAE)","linear-gradient(90deg,#6C7CF7,#D27BEA)"]
    st = "".join(f'<div style="--g:{SG[i]}"><b>{e(n)}</b><p>{e(d)}</p><ul>{"".join(f"<li><a href=\'{PR[k]['url']}\'>{e(PR[k]['name'])}<span>→</span></a></li>" for k in ks)}</ul></div>' for i, (n, d, ks) in enumerate(STILURI))
    a(f'''<section class="nmg-sec" id="tendinte"><div class="nmg-wide"><span class="nmg-kick">Tendințe care țin</span>
<h2>Ce rămâne în galerie<br><em>și ce iese din expoziție.</em></h2>
<p>Modele vin și pleacă. Proporția, lumina și materialele naturale rămân. Iată ce recomandăm pentru o casă care arată la fel de bine și peste zece ani:</p>
<div class="nmg-trend">{tr}</div>
<h3 style="margin-top:56px">Ghidul curatorului: trei stiluri, patru exponate</h3>
<div class="nmg-styles">{st}</div></div></section>''')
    fq = "".join(f'<details><summary>{e(q)}</summary><p>{e(r)}</p></details>' for q, r in FAQ)
    a(f'''<section class="nmg-sec" id="intrebari"><div class="nmg-in"><span class="nmg-kick">Întrebări frecvente</span><h2>Bine de<br><em>știut.</em></h2>{fq}</div></section>''')
    a(f'''<section class="nmg-cta"><span class="nmg-kick">Consultanță gratuită</span>
<h2>Vrei ca și casa ta<br><em>să arate ca o galerie?</em></h2>
<p>Spune-ne ce proiect ai. Te ajutăm să alegi profilele potrivite și să calculezi necesarul, înainte de comandă.</p>
<div class="nmg-btns"><a class="nmg-btn" href="tel:+40213193535">Sună: 021 319 35 35</a><a class="nmg-btn nmg-btn--ghost" href="{SITE}profile-decorative-exterior">Profile exterior</a><a class="nmg-btn nmg-btn--ghost" href="{SITE}profile-decorative-interior">Profile interior</a></div>
<p class="nmg-note">Luni–Vineri, 07:30–16:00 · NMC România, lider de piață de peste 20 de ani · Imaginile ambientale sunt orientative, cu rol de inspirație.</p></section>''')
    a('</div>')
    return "\n".join(t)


if __name__ == "__main__":
    frag = article(IMG_SITE)
    assert " lei" not in frag
    (ROOT / "articol.html").write_text("<!-- Articol blog NMC România · se lipește în editorul articolului (mod Cod sursă). Imaginile: " + IMG_SITE + " -->\n" + frag, encoding="utf-8")
    prev = f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Previzualizare · Galeria NMC</title><style>body{{margin:0;background:#fff;font-family:Roboto,sans-serif}} .pg{{max-width:1240px;margin:24px auto;padding:0 12px}} .pg>h1{{font:500 28px Roboto,sans-serif;margin:0 0 16px;color:#29292B}}</style></head>
<body><div class="pg"><h1>Galeria NMC: ghid de amenajare interioară și exterioară, ca într-o galerie de artă</h1>{article("img/")}</div></body></html>'''
    (ROOT / "previzualizare.html").write_text(prev, encoding="utf-8")
    print("OK")

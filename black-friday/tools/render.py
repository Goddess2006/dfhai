from pathlib import Path
from html import escape
import json
root=Path(__file__).resolve().parents[1]; catalog=json.loads((root/'catalog.json').read_text());products=catalog['products']
for p in products:
 p.pop('price',None);p.pop('old',None)
(root/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
cats=[('ext','exterior','Profile exterior','−20%','Reducere la produsele de exterior.','Fațada face prima impresie.','Cornișe, ancadramente și solbancuri pentru o casă care iese în evidență.','profile-decorative-exterior','ext0'),('int','interior','Profile interior','−40%','Reduceri de până la','Detaliile schimbă totul.','Doar modelele Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5, în limita stocului disponibil pe site.','profile-decorative-interior','int-z11'),('tapet','tapet','Carrara Best','−30%','Reducere la tapet.','Pereți cu personalitate.','Reducere de 30% exclusiv la produsele Carrara Best aflate în stoc. Nu se aplică altor colecții de tapet.','tapet-carrara-best','tapet-82671'),('adeziv','adeziv','Adezivi exterior','−20%','Tot exteriorul −20%','Un proiect bun, până la capăt.','Completează amenajarea cu adezivul potrivit pentru profilele de exterior.','consumabile-profiluri-decorative','adeziv12')]
def promo(c,mini=False):
 id,slug,name,percent,label,title,desc,url,img=c
 return f'''<a class="offer offer--{id}" href="#{slug}"><span class="offer__index">0{['ext','int','tapet','adeziv'].index(id)+1} / BLACK FRIDAY</span><h2>{name}</h2><div class="offer__amount">{('<span>până la</span>' if id=='int' else '')}<strong>{percent}</strong></div><img src="assets/{img}.jpg" alt="" width="400" height="400"><span class="offer__scope">{('Întreaga gamă exterior' if id=='ext' else 'Doar modelele selectate · în limita stocului' if id=='int' else 'Doar Carrara Best în stoc')}</span><span class="offer__link">Descoperă colecția <b>↗</b></span></a>'''
def card(p):
 c=next(c for c in cats if c[0]==p['cat']);id,slug,name,percent,*_=c
 tag=('până la '+percent) if id=='int' else percent
 return f'''<article class="product" data-search="{escape((p['name']+' '+name).lower())}"><a class="product__image" href="{p['url']}" aria-label="{escape(p['name'])}">{f'<span class="product__discount">{tag}</span>' if tag else ''}<img src="{p['img']}" alt="{escape(p['name'])}" width="400" height="400" loading="lazy"></a><div class="product__body"><span class="kicker">{name}</span>{('<span class="stock-note">În limita stocului disponibil</span>' if id in ['int','tapet'] else '')}<h3><a href="{p['url']}">{escape(p['name'])}</a></h3><a class="product__cta" href="{p['url']}">Descoperă produsul <span>↗</span></a></div></article>'''
sections=''
for c in cats:
 id,slug,name,percent,label,title,desc,url,img=c
 sections+=f'''<section class="collection" id="{slug}"><div class="wrap"><div class="collection__head"><div><span class="kicker">NMC România / {name}</span><h2>{title}</h2><p>{desc}</p></div><div class="collection__offer">{('<span>până la</span>' if id=='int' else '')}<strong>{percent}</strong><a href="https://www.nmcromania.ro/{url}">Vezi colecția ↗</a></div></div><div class="products">{''.join(card(p) for p in products if p['cat']==id)}</div><p class="empty" hidden>Niciun produs găsit. Încearcă un alt termen.</p></div></section>'''
h=f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Black Friday NMC România — Reduceri de până la 40%</title>
<meta name="description" content="Black Friday NMC România: 20% la tot exteriorul. 30% doar la Carrara Best în stoc. Până la 40% doar la modelele de interior selectate, în limita stocului disponibil.">
<meta name="theme-color" content="#101010"><meta property="og:title" content="Black Friday NMC România — Dă un nou stil casei tale">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="polish.css">
</head>
<body>
<div class="ticker"><span>BLACK FRIDAY · NMC ROMÂNIA</span><span>EXTERIOR −20%</span><span>CARRARA BEST ÎN STOC −30%</span><span>INTERIOR SELECTAT PÂNĂ LA −40%</span></div>
<header class="header"><div class="wrap header__inner"><a class="logo" href="https://www.nmcromania.ro/"><span class="logo__mark">N</span><span>NMC<span class="logo__country">ROMÂNIA</span></span></a><nav class="header__nav" aria-label="Colecții"><a href="#exterior">Exterior</a><a href="#interior">Interior</a><a href="#tapet">Tapet</a></nav><a class="store-link" href="https://www.nmcromania.ro/">Intră în magazin ↗</a></div></header>
<main>
<section class="hero"><div class="wrap hero__grid"><div class="hero__copy"><span class="eyebrow"><i></i> E timpul pentru o schimbare.</span><h1>BLACK<br><span>FRIDAY</span><span class="hero__dot">.</span></h1><p class="hero__tagline">Dă un nou stil<br>casei tale.</p><p class="hero__lead">La exterior, întreaga gamă are −20%. La interior și tapet, alege produsele eligibile din selecția noastră, în limita stocului disponibil pe site.</p><a class="button" href="#oferte">Descoperă reducerile <span>↓</span></a></div>
<div class="hero__visual" aria-label="Produse reale din colecțiile NMC România"><div class="visual__grid"></div><div class="hero__stamp"><span>REDUCERI DE</span><span>PÂNĂ LA · INTERIOR SELECTAT</span><strong>−40<small>%</small></strong></div><figure class="visual__product visual__product--main"><img src="assets/ext0.jpg" alt="Cornișă decorativă exterior NC104" width="400" height="400"><figcaption>EXTERIOR / NC104</figcaption></figure><figure class="visual__product visual__product--paper"><img src="assets/tapet-82671.jpg" alt="Tapet Carrara Best — 82671" width="400" height="400"><figcaption>TAPET / CARRARA BEST</figcaption></figure><div class="visual__note">DETALII MICI.<br><b>SCHIMBĂRI MARI.</b><span>✳</span></div><span class="visual__caption">COLECȚII PENTRU CASA TA / NMC ROMÂNIA</span></div></div></section>
<section class="offers-section" id="oferte"><div class="wrap"><div class="section-label"><span>Alege de unde începe schimbarea</span><span>03 COLECȚII. UN NOU ÎNCEPUT.</span></div><div class="offers">{''.join(promo(c) for c in cats[:3])}</div></div></section>
<nav class="category-nav" aria-label="Navigare produse"><div class="wrap category-nav__inner">{''.join(f'<a class="chip" href="#{c[1]}">{c[2]} <span>{("până la " if c[0]=="int" else "")+c[3]}</span></a>' for c in cats)}<label class="search"><span class="sr-only">Caută în selecția de produse</span><input type="search" id="q" placeholder="Caută un produs…"><span aria-hidden="true">⌕</span></label></div></nav>
<div class="wrap"><p id="searchStatus" role="status" aria-live="polite"></p></div>
{sections}
<section class="project wrap"><div><span class="kicker">ALEGE. COMBINĂ. TRANSFORMĂ.</span><h2>Ideea e a ta.<br>Detaliile sunt la noi.</h2><p>Nu știi de unde să începi? Echipa NMC te ajută să alegi profilele și materialele potrivite pentru proiectul tău.</p><a class="button button--light" href="tel:+40213193535">Hai să vorbim <span>↗</span></a><span class="project__phone">021 319 35 35 · L–V, 07:30–16:00</span></div><div class="project__art"><img src="assets/int-z11.jpg" alt="Cornișă decorativă Z11" width="400" height="400" loading="lazy"><span>CASA TA.<br>STILUL TĂU.</span></div></section>
<section class="faq wrap"><h2>Bine de știut.</h2><details><summary>Cum comand produsele?</summary><p>Alege un produs pentru a deschide pagina lui pe nmcromania.ro. Acolo verifici detaliile, disponibilitatea și finalizezi comanda.</p></details><details><summary>Care sunt reducerile?</summary><p>20% la întreaga gamă de exterior. La tapet: 30% doar la Carrara Best aflat în stoc. La interior: reduceri de până la 40% doar pentru Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5, în limita stocului disponibil pe site. Reducerile nu se extind la alte colecții de tapet sau alte modele de interior.</p></details><details><summary>Ce se întâmplă când se epuizează stocul?</summary><p>La tapet și interior, oferta este valabilă doar pentru produsele eligibile și cantitățile disponibile în magazin. Selecția de aici a fost verificată la 4 noiembrie 2026; stocul actual se confirmă în pagina produsului, înainte de comandă. Nu sunt incluse variantele marcate la comandă sau cu stoc neconfirmat.</p></details><details><summary>Cum aleg materialele pentru montaj?</summary><p>Consultă instrucțiunile produselor și cere recomandarea echipei NMC pentru suprafața și materialele folosite. Adezivii de exterior prezentați fac parte din oferta de −20% la exterior.</p></details></section>
</main>
<footer><div class="wrap"><a class="logo" href="https://www.nmcromania.ro/">NMC ROMÂNIA</a><span>Tapet și interior: doar produsele eligibile, în limita stocului disponibil.</span><a href="https://www.nmcromania.ro/">nmcromania.ro ↗</a></div></footer>
<script src="campaign.js" defer></script><script src="overlay-bridge.js" defer></script>
</body>
</html>
'''
h=h.replace('href="https://www.nmcromania.ro/profile-decorative-interior">Vezi colecția', 'href="#interior">Modelele eligibile')
h=h.replace('href="https://www.nmcromania.ro/tapet-carrara-best">Vezi colecția', 'href="#tapet">Variantele eligibile')
(root/'index.html').write_text(h)

"""Render the campaign from the catalog; only explicit per-product discounts are shown."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text())
products = catalog['products']
featured = next(p for p in products if p['id'] == 'adeziv12')
categories = [
    ('ext', 'exterior', 'Exterior', 'Prima impresie. Un caracter aparte.', 'Cornișe, ancadramente și solbancuri care pun în valoare arhitectura casei.', 'ext0'),
    ('int', 'interior', 'Interior', 'Armonia începe cu detaliile.', 'De la linia unei cornișe la conturul unei plinte. Descoperă selecția Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5.', 'int-z11'),
    ('tapet', 'tapet', 'Carrara Best', 'Pereți cu o poveste a lor.', 'Texturi și motive care dau profunzime spațiului. Variante Carrara Best din selecția verificată în stoc.', 'tapet-82671'),
    ('adeziv', 'adeziv', 'Montaj', 'Frumusețea merită un montaj bun.', 'Completează proiectul cu materialele potrivite. Oferta de −30% se aplică exclusiv ADRO-FIX de exterior, 1,5 kg.', 'adeziv12'),
]


def discount(product):
    return product.get('discountPercent', 0)


def card(product):
    category = next(c for c in categories if c[0] == product['cat'])
    sale = discount(product)
    label = f'<span class="product__discount">−{sale}% · Black Friday</span>' if sale else ''
    scope = 'Oferta specială · 1,5 kg' if sale else 'Din selecția NMC România'
    return f'''<article class="product" data-product-id="{product['id']}" data-search="{escape((product['name'] + ' ' + category[2]).lower())}">
  <a class="product__image" href="{product['url']}" aria-label="{escape(product['name'])}">{label}<img src="{product['img']}" alt="{escape(product['name'])}" width="400" height="400" loading="lazy"></a>
  <div class="product__body"><span class="kicker">{category[2]}</span><h3><a href="{product['url']}">{escape(product['name'])}</a></h3><span class="product__note">{scope}</span><a class="product__cta" href="{product['url']}">Vezi detaliile <span aria-hidden="true">↗</span></a></div>
</article>'''


sections = ''
for index, (identifier, slug, name, title, description, image) in enumerate(categories, 1):
    sections += f'''<section class="collection wrap framed" id="{slug}">
  <div class="collection__head"><div><span class="kicker">0{index} / {name}</span><h2>{title}</h2><p>{description}</p></div><span class="collection__annotation">{'O singură ofertă.<br>−30% la ADRO-FIX 1,5 kg.' if identifier == 'adeziv' else 'Colecția NMC.<br>Detalii care inspiră.'}</span></div>
  <div class="collection__controls"><span>{sum(p['cat'] == identifier for p in products)} produse selectate</span><div><button type="button" data-carousel="-1" aria-label="Produsele anterioare din {name}" aria-controls="products-{slug}">←</button><button type="button" data-carousel="1" aria-label="Următoarele produse din {name}" aria-controls="products-{slug}">→</button></div></div>
  <div class="products" id="products-{slug}" tabindex="0" role="region" aria-label="Produse {name}">{''.join(card(p) for p in products if p['cat'] == identifier)}</div><p class="empty" hidden>Niciun produs găsit. Încearcă un alt termen.</p>
</section>'''

teasers = ''
for index, (_, slug, name, _, _, image) in enumerate(categories[:3], 1):
    teasers += f'''<a class="editorial-card framed" href="#{slug}"><span class="editorial-card__top">0{index} / COLECȚIA NMC</span><div class="editorial-card__image"><img src="assets/{image}.jpg" alt="" width="400" height="400" loading="lazy"></div><div class="editorial-card__bottom"><h3>{name}</h3><span aria-hidden="true">↗</span></div></a>'''

html = f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Black Friday NMC România — ADRO-FIX exterior 1,5 kg, −30%</title>
<meta name="description" content="O ofertă specială de Black Friday: −30% exclusiv la adezivul exterior ADRO-FIX 1,5 kg. Descoperă colecțiile NMC România. Celelalte produse sunt la preț întreg.">
<meta name="theme-color" content="#151b2b">
<meta property="og:title" content="Black Friday NMC România — Detaliile fac întregul">
<meta property="og:description" content="−30% doar la ADRO-FIX exterior 1,5 kg. Colecții pentru exterior, interior și tapet, prezentate la preț întreg.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="polish.css">
</head>
<body>
<div class="announcement"><span>BLACK FRIDAY / NMC ROMÂNIA</span><a href="#oferta">ADRO-FIX exterior 1,5 kg <strong>−30%</strong><span aria-hidden="true">↗</span></a><span>Detaliile fac diferența.</span></div>
<header class="header"><div class="wrap header__inner"><a class="logo" href="https://www.nmcromania.ro/" aria-label="NMC România"><span class="logo__mark">N</span><span>NMC<span class="logo__country">ROMÂNIA</span></span></a><nav class="header__nav" aria-label="Colecții"><a href="#exterior">Exterior</a><a href="#interior">Interior</a><a href="#tapet">Tapet</a><a href="#oferta">Oferta Black Friday</a></nav><a class="store-link" href="https://www.nmcromania.ro/">Magazin online <span aria-hidden="true">↗</span></a></div></header>
<main>
<section class="hero" id="oferta"><div class="hero__halo"></div><div class="wrap hero__grid"><div class="hero__copy"><span class="eyebrow"><i></i> BLACK FRIDAY. ALES CU GRIJĂ.</span><h1>Detaliile<br>fac <em>întregul.</em></h1><p class="hero__lead">Linii care conturează. Texturi care inspiră.<br>O casă în care fiecare alegere îți poartă semnătura.</p><div class="hero__offer"><span class="offer-label">O singură ofertă. Un început bun.</span><p><strong>−30%</strong><span>ADRO-FIX exterior<br><b>1,5 kg</b></span></p></div><div class="hero__actions"><a class="button" href="{featured['url']}">Descoperă oferta <span aria-hidden="true">↗</span></a><a class="text-link" href="#colectii">Explorează colecțiile <span aria-hidden="true">↓</span></a></div><p class="hero__terms">Reducerea se aplică exclusiv produsului de 1,5 kg.<br>Toate celelalte produse sunt prezentate la preț întreg.</p></div>
<div class="hero__visual"><div class="feature-label"><span>THE NMC EDIT</span><span>BLACK FRIDAY / 2026</span></div><div class="featured-product framed"><span class="featured-product__badge">OFERTA SPECIALĂ <b>−30%</b></span><div class="featured-product__image"><img src="{featured['img']}" alt="Adeziv pentru lipire exterior ADRO-FIX, ambalaj de 1,5 kg" width="400" height="400" fetchpriority="high"></div><div class="featured-product__caption"><span>ADRO-FIX</span><span>EXTERIOR / 1,5 KG</span></div></div><div class="visual__footnote"><span>Finisajul se vede.<br><b>Montajul contează.</b></span><span class="visual__seal" aria-hidden="true">NMC<br><small>ROMÂNIA</small></span></div></div></div></section>
<section class="curation wrap" id="colectii"><div class="section-heading"><div><span class="kicker">O casă. O perspectivă nouă.</span><h2>Stilul tău, în fiecare detaliu.</h2></div><p>O selecție de forme și texturi.<br>Produse la preț întreg, alese să te inspire.</p></div><div class="editorial-grid">{teasers}</div></section>
<nav class="category-nav" aria-label="Navigare produse"><div class="wrap category-nav__inner">{''.join(f'<a class="chip" href="#{c[1]}">{c[2]}</a>' for c in categories)}<label class="search"><span class="sr-only">Caută în selecția de produse</span><input type="search" id="q" placeholder="Caută un produs…"><span aria-hidden="true">⌕</span></label></div></nav>
<div class="wrap"><p id="searchStatus" role="status" aria-live="polite"></p></div>
{sections}
<section class="project wrap framed"><div><span class="kicker">ALEGERI FRUMOASE. PROIECTE ÎMPLINITE.</span><h2>Ai viziunea.<br><em>Găsim detaliile.</em></h2><p>De la primul profil până la ultimul finisaj, echipa NMC te ajută să alegi materialele potrivite pentru proiectul tău.</p><a class="button" href="tel:+40213193535">Vorbește cu un consultant <span aria-hidden="true">↗</span></a><span class="project__phone">021 319 35 35 · L–V, 07:30–16:00</span></div><div class="project__art"><img src="assets/int-z11.jpg" alt="Cornișă decorativă Z11 din colecția NMC" width="400" height="400" loading="lazy"><span>Forma urmează<br><em>inspirația.</em></span></div></section>
<section class="faq wrap"><div class="faq__intro"><span class="kicker">Înainte de ultimul detaliu.</span><h2>Bine de știut.</h2></div><div class="faq__items"><details><summary>Ce produs are reducere?</summary><p>Doar adezivul de lipire pentru exterior ADRO-FIX în ambalaj de 1,5 kg are reducere de 30%. ADRO-FIX de 4 kg, profilele de exterior, profilele de interior și tapetul sunt la preț întreg.</p></details><details><summary>Cum comand și verific disponibilitatea?</summary><p>Deschide pagina produsului pe nmcromania.ro pentru a verifica oferta, stocul actual și condițiile de comandă. Produsele se comandă în limita stocului disponibil în magazin.</p></details><details><summary>Cum aleg materialele pentru montaj?</summary><p>Verifică instrucțiunile produselor și solicită recomandarea echipei NMC pentru suprafața și materialele folosite în proiect.</p></details></div></section>
</main>
<footer><div class="wrap"><a class="logo" href="https://www.nmcromania.ro/">NMC ROMÂNIA</a><span>O singură ofertă: ADRO-FIX exterior 1,5 kg, −30%.<br>Celelalte produse sunt la preț întreg.</span><a href="https://www.nmcromania.ro/">Descoperă magazinul ↗</a></div></footer>
<script src="campaign.js" defer></script><script src="overlay-bridge.js" defer></script>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html)

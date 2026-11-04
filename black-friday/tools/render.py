"""Render the campaign from the catalog; only explicit per-product discounts are shown."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text())
products = catalog['products']
featured = next(p for p in products if p['id'] == 'adeziv12')
categories = [
    ('ext', 'exterior', 'Exterior', 'Prima impresie. Un caracter aparte.', 'Întreaga gamă de profile pentru exterior are reducere de 20%. Descoperă cornișele, ancadramentele și solbancurile NMC.', 'ext0'),
    ('int', 'interior', 'Interior', 'Armonia începe cu detaliile.', 'Până la 40% reducere doar pentru Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5, în limita stocului disponibil pe site.', 'int-z11'),
    ('tapet', 'tapet', 'Carrara Best', 'Pereți cu o poveste a lor.', '30% reducere exclusiv la variantele Carrara Best aflate în stoc. Oferta nu se aplică altor colecții de tapet.', 'tapet-82671'),
    ('adeziv', 'adeziv', 'Montaj', 'Frumusețea merită un montaj bun.', 'Completează proiectul cu materialele potrivite. Oferta de −30% se aplică exclusiv ADRO-FIX de exterior, 1,5 kg.', 'adeziv12'),
]


def discount(product):
    return product.get('discountPercent', 0)


def card(product):
    category = next(c for c in categories if c[0] == product['cat'])
    sale = discount(product)
    up_to = product.get('discountUpToPercent', 0)
    offer = f'până la −{up_to}%' if up_to else f'−{sale}%' if sale else ''
    label = f'<span class="product__discount">{offer} · Black Friday</span>' if offer else ''
    scope = ('În limita stocului disponibil' if product['cat'] in ['int', 'tapet']
             else 'Oferta specială · 1,5 kg' if product['id'] == 'adeziv12'
             else 'Întreaga gamă exterior · −20%' if product['cat'] == 'ext'
             else 'La preț întreg · fără reducere')
    return f'''<article class="product" data-product-id="{product['id']}" data-search="{escape((product['name'] + ' ' + category[2]).lower())}">
  <a class="product__image" href="{product['url']}" aria-label="{escape(product['name'])}">{label}<img src="{product['img']}" alt="{escape(product['name'])}" width="400" height="400" loading="lazy"></a>
  <div class="product__body"><span class="kicker">{category[2]}</span><h3><a href="{product['url']}">{escape(product['name'])}</a></h3><span class="product__note">{scope}</span><a class="product__cta" href="{product['url']}">Vezi detaliile <span aria-hidden="true">↗</span></a></div>
</article>'''


category_offers = {
    'ext': '−20%<small>Întreaga gamă exterior</small>',
    'int': '<small>până la</small>−40%<small>Doar modelele selectate · în limita stocului</small>',
    'tapet': '−30%<small>Doar Carrara Best în stoc</small>',
    'adeziv': '−30%<small>Doar ADRO-FIX exterior 1,5 kg</small>',
}

sections = ''
for index, (identifier, slug, name, title, description, image) in enumerate(categories, 1):
    sections += f'''<section class="collection wrap framed" id="{slug}">
  <div class="collection__head"><div><span class="kicker">0{index} / {name}</span><h2>{title}</h2><p>{description}</p></div><span class="collection__annotation">{category_offers[identifier]}</span></div>
  <div class="collection__controls"><span>{sum(p['cat'] == identifier for p in products)} produse selectate</span><div><button type="button" data-carousel="-1" aria-label="Produsele anterioare din {name}" aria-controls="products-{slug}">←</button><button type="button" data-carousel="1" aria-label="Următoarele produse din {name}" aria-controls="products-{slug}">→</button></div></div>
  <div class="products" id="products-{slug}" tabindex="0" role="region" aria-label="Produse {name}">{''.join(card(p) for p in products if p['cat'] == identifier)}</div><p class="empty" hidden>Niciun produs găsit. Încearcă un alt termen.</p>
</section>'''

teasers = ''
for index, (identifier, slug, name, _, _, image) in enumerate(categories[:3], 1):
    teasers += f'''<a class="editorial-card framed" href="#{slug}"><span class="editorial-card__top">0{index} / COLECȚIA NMC</span><span class="editorial-card__offer">{category_offers[identifier]}</span><div class="editorial-card__image"><img src="assets/{image}.jpg" alt="" width="400" height="400" loading="lazy"></div><div class="editorial-card__bottom"><h3>{name}</h3><span aria-hidden="true">↗</span></div></a>'''

html = f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Black Friday NMC România — Reduceri de până la 40%</title>
<meta name="description" content="Exterior −20%, Carrara Best în stoc −30%, interior selectat până la −40% și ADRO-FIX exterior 1,5 kg −30%. Descoperă ofertele NMC România.">
<meta name="theme-color" content="#151b2b">
<meta property="og:title" content="Black Friday NMC România — Detaliile fac întregul">
<meta property="og:description" content="Exterior −20%, Carrara Best în stoc −30%, interior selectat până la −40%, ADRO-FIX exterior 1,5 kg −30%.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="polish.css">
</head>
<body>
<div class="announcement"><span>BLACK FRIDAY / NMC ROMÂNIA</span><a href="#oferta">ADRO-FIX exterior 1,5 kg <strong>−30%</strong><span aria-hidden="true">↗</span></a><span>Detaliile fac diferența.</span></div>
<header class="header"><div class="wrap header__inner"><a class="logo" href="https://www.nmcromania.ro/" aria-label="NMC România"><span class="logo__mark">N</span><span>NMC<span class="logo__country">ROMÂNIA</span></span></a><nav class="header__nav" aria-label="Colecții"><a href="#exterior">Exterior</a><a href="#interior">Interior</a><a href="#tapet">Tapet</a><a href="#oferta">Oferta Black Friday</a></nav><a class="store-link" href="https://www.nmcromania.ro/">Magazin online <span aria-hidden="true">↗</span></a></div></header>
<main>
<section class="hero" id="oferta"><div class="hero__halo"></div><div class="wrap hero__grid"><div class="hero__copy"><span class="eyebrow"><i></i> BLACK FRIDAY. ALES CU GRIJĂ.</span><h1>Detaliile<br>fac <em>întregul.</em></h1><p class="hero__lead">Linii care conturează. Texturi care inspiră.<br>O casă în care fiecare alegere îți poartă semnătura.</p><div class="hero__offer"><span class="offer-label">Un montaj bun. O ofertă specială.</span><p><strong>−30%</strong><span>ADRO-FIX exterior<br><b>1,5 kg</b></span></p></div><div class="hero__actions"><a class="button" href="{featured['url']}">Descoperă oferta <span aria-hidden="true">↗</span></a><a class="text-link" href="#colectii">Explorează colecțiile <span aria-hidden="true">↓</span></a></div><p class="hero__terms">La adezivi, −30% doar pentru ambalajul de 1,5 kg; cel de 4 kg rămâne la preț întreg.<br>Descoperă mai jos reducerile pentru exterior, interior și Carrara Best.</p></div>
<div class="hero__visual"><div class="feature-label"><span>THE NMC EDIT</span><span>BLACK FRIDAY / 2026</span></div><div class="featured-product framed"><span class="featured-product__badge">OFERTA SPECIALĂ <b>−30%</b></span><div class="featured-product__image"><img src="{featured['img']}" alt="Adeziv pentru lipire exterior ADRO-FIX, ambalaj de 1,5 kg" width="400" height="400" fetchpriority="high"></div><div class="featured-product__caption"><span>ADRO-FIX</span><span>EXTERIOR / 1,5 KG</span></div></div><div class="visual__footnote"><span>Finisajul se vede.<br><b>Montajul contează.</b></span><span class="visual__seal" aria-hidden="true">NMC<br><small>ROMÂNIA</small></span></div></div></div></section>
<section class="curation wrap" id="colectii"><div class="section-heading"><div><span class="kicker">O casă. O perspectivă nouă.</span><h2>Stilul tău, în fiecare detaliu.</h2></div><p>Forme, texturi și oferte alese.<br>Interiorul și tapetul: în limita stocului disponibil.</p></div><div class="editorial-grid">{teasers}</div></section>
<nav class="category-nav" aria-label="Navigare produse"><div class="wrap category-nav__inner">{''.join(f'<a class="chip" href="#{c[1]}">{c[2]}</a>' for c in categories)}<label class="search"><span class="sr-only">Caută în selecția de produse</span><input type="search" id="q" placeholder="Caută un produs…"><span aria-hidden="true">⌕</span></label></div></nav>
<div class="wrap"><p id="searchStatus" role="status" aria-live="polite"></p></div>
{sections}
<section class="project wrap framed"><div><span class="kicker">ALEGERI FRUMOASE. PROIECTE ÎMPLINITE.</span><h2>Ai viziunea.<br><em>Găsim detaliile.</em></h2><p>De la primul profil până la ultimul finisaj, echipa NMC te ajută să alegi materialele potrivite pentru proiectul tău.</p><a class="button" href="tel:+40213193535">Vorbește cu un consultant <span aria-hidden="true">↗</span></a><span class="project__phone">021 319 35 35 · L–V, 07:30–16:00</span></div><div class="project__art"><img src="assets/int-z11.jpg" alt="Cornișă decorativă Z11 din colecția NMC" width="400" height="400" loading="lazy"><span>Forma urmează<br><em>inspirația.</em></span></div></section>
<section class="faq wrap"><div class="faq__intro"><span class="kicker">Înainte de ultimul detaliu.</span><h2>Bine de știut.</h2></div><div class="faq__items"><details><summary>Care sunt reducerile campaniei?</summary><p>Întreaga gamă de profile exterior are reducere de 20%. Carrara Best: 30% doar la variantele în stoc. Interior: până la 40% doar pentru Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5, în limita stocului disponibil. La adezivi: ADRO-FIX exterior de 1,5 kg are reducere de 30%; cel de 4 kg rămâne la preț întreg.</p></details><details><summary>Cum comand și verific disponibilitatea?</summary><p>Deschide pagina produsului pe nmcromania.ro pentru a verifica oferta, stocul actual și condițiile de comandă. Produsele se comandă în limita stocului disponibil în magazin.</p></details><details><summary>Cum aleg materialele pentru montaj?</summary><p>Verifică instrucțiunile produselor și solicită recomandarea echipei NMC pentru suprafața și materialele folosite în proiect.</p></details></div></section>
</main>
<footer><div class="wrap"><a class="logo" href="https://www.nmcromania.ro/">NMC ROMÂNIA</a><span>Exterior −20% · Carrara Best în stoc −30% · Interior selectat până la −40%.<br>ADRO-FIX exterior 1,5 kg −30% · ADRO-FIX 4 kg la preț întreg.</span><a href="https://www.nmcromania.ro/">Descoperă magazinul ↗</a></div></footer>
<script src="campaign.js" defer></script><script src="overlay-bridge.js" defer></script>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html)

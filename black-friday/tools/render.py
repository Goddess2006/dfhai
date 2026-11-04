"""Render the stock-limited Black Friday campaign without numeric prices."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text())
products = catalog['products']
categories = [
    ('ext', 'exterior', 'Profile exterior', 'O fațadă cu personalitate.', '−20% la toate profilele de exterior. Adezivii sunt excluși din această reducere. Oferta este valabilă în limita stocului disponibil pe site.', 'ambient-exterior.jpg'),
    ('int', 'interior', 'Profile interior', 'Detaliile care schimbă camera.', 'Până la −40% exclusiv pentru Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5. Doar în limita stocului disponibil pe site.', 'scene-interior.jpg'),
    ('tapet', 'tapet', 'Carrara Best', 'Texturi pe care le simți acasă.', '−30% doar pentru tapetul Carrara Best aflat în stoc. Nu se aplică altor colecții sau variantelor la comandă.', 'scene-tapet.jpg'),
    ('adeziv', 'adeziv', 'Montaj exterior', 'Ultimul pas. Montajul potrivit.', 'ADRO-FIX exterior 1,5 kg: −30%, în limita stocului disponibil pe site. ADRO-FIX 4 kg rămâne la preț întreg. Adezivii nu intră în reducerea de −20% pentru profile.', None),
]

def offer(product):
    up_to = product.get('discountUpToPercent', 0)
    sale = product.get('discountPercent', 0)
    return f'până la −{up_to}%' if up_to else f'−{sale}%' if sale else ''


def card(product, featured=False):
    category = next(c for c in categories if c[0] == product['cat'])
    badge = offer(product)
    label = f'<span class="product__discount">{badge}</span>' if badge else ''
    scope = 'În limita stocului disponibil' if badge else 'La preț întreg · fără reducere'
    return f'''<article class="product{' product--featured' if featured else ''}" data-product-id="{product['id']}" data-search="{escape((product['name'] + ' ' + category[2]).lower())}">
  <a class="product__image" href="{product['url']}" aria-label="{escape(product['name'])}">{label}<img src="{product['img']}" alt="{escape(product['name'])}" width="400" height="400" loading="lazy"></a>
  <div class="product__body"><span class="kicker">{category[2]}{' / Vedetă Black Friday' if featured else ''}</span><h3><a href="{product['url']}">{escape(product['name'])}</a></h3><span class="product__note">{scope}</span><a class="product__cta" href="{product['url']}">Vezi produsul <span aria-hidden="true">↗</span></a></div>
</article>'''

category_offers = {
    'ext': '<strong>−20%</strong><small>Toate profilele exterior · fără adezivi</small>',
    'int': '<small>până la</small><strong>−40%</strong><small>Doar cele 8 modele selectate</small>',
    'tapet': '<strong>−30%</strong><small>Doar Carrara Best în stoc</small>',
    'adeziv': '<strong>−30%</strong><small>Doar ADRO-FIX exterior 1,5 kg</small>',
}

def collection(category, index):
    identifier, slug, name, title, description, image = category
    items = [p for p in products if p['cat'] == identifier]
    return f'''<section class="collection wrap framed{' collection--adhesive' if identifier == 'adeziv' else ''}" id="{slug}">
  <div class="collection__head"><div><span class="kicker">0{index} / {name}</span><h2>{title}</h2><p>{description}</p></div><div class="collection__annotation">{category_offers[identifier]}</div></div>
  <div class="collection__controls"><span>{len(items)} produse selectate · verifică stocul în magazin</span><div><button type="button" data-carousel="-1" aria-label="Produsele anterioare din {name}" aria-controls="products-{slug}">←</button><button type="button" data-carousel="1" aria-label="Următoarele produse din {name}" aria-controls="products-{slug}">→</button></div></div>
  <div class="products" id="products-{slug}" tabindex="0" role="region" aria-label="Produse {name}">{''.join(card(p) for p in items)}</div><p class="empty" hidden>Niciun produs găsit. Încearcă un alt termen.</p>
</section>'''

teasers = ''
for index, (identifier, slug, name, title, _, image) in enumerate(categories[:3], 1):
    teasers += f'''<a class="ambience-card ambience-card--{identifier} framed" href="#{slug}"><img src="assets/{image}" alt="Ambient {name} de pe nmcromania.ro" width="800" height="800" loading="lazy"><div class="ambience-card__shade"></div><span class="ambience-card__number">0{index} / NMC ROMÂNIA</span><div class="ambience-card__copy"><h3>{name}</h3><div class="ambience-card__offer">{category_offers[identifier]}</div><span class="ambience-card__link">Descoperă selecția <b>↗</b></span></div></a>'''

featured_ids = ['ext0', 'int-z11', 'tapet-82671']
stars = ''.join(card(next(p for p in products if p['id'] == identifier), True) for identifier in featured_ids)

html = f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Black Friday NMC România — Reduceri de până la 40%</title>
<meta name="description" content="Profile exterior −20%, fără adezivi. Carrara Best în stoc −30%. Doar 8 modele de interior: până la −40%. ADRO-FIX exterior 1,5 kg −30%. Totul în limita stocului disponibil.">
<meta name="theme-color" content="#0e0b13"><meta property="og:title" content="Black Friday NMC România — Casa ta, în altă lumină">
<meta property="og:description" content="Profile exterior, interior selectat și Carrara Best. Reduceri în limita stocului disponibil pe nmcromania.ro.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="polish.css">
</head>
<body>
<div class="edge-word edge-word--left" aria-hidden="true">BLACK FRIDAY</div><div class="edge-word edge-word--right" aria-hidden="true">BLACK FRIDAY</div>
<div class="announcement"><span>BLACK FRIDAY / NMC ROMÂNIA</span><span>Detaliile fac diferența.</span><span>În limita stocului disponibil pe site</span></div>
<header class="header"><div class="wrap header__inner"><a class="logo" href="https://www.nmcromania.ro/" aria-label="NMC România"><span class="logo__mark">N</span><span>NMC<span class="logo__country">ROMÂNIA</span></span></a><nav class="header__nav" aria-label="Colecții"><a href="#exterior">Exterior</a><a href="#interior">Interior</a><a href="#tapet">Carrara Best</a><a href="#vedete">Produse vedetă</a></nav><a class="store-link" href="https://www.nmcromania.ro/">Magazin online <span aria-hidden="true">↗</span></a></div></header>
<main>
<section class="hero wrap" id="oferta"><div class="hero-shell framed"><img class="hero-scene" src="assets/scene-tapet.jpg" alt="Dormitor amenajat cu tapet Carrara Best, fotografie ambientală din magazinul NMC" width="800" height="800" fetchpriority="high"><div class="hero-shade"></div><div class="hero__copy"><span class="eyebrow"><i></i> NMC ROMÂNIA / COLECȚIA DE OFERTE</span><h1>BLACK<br><span>FRIDAY</span><b>.</b></h1><p class="hero__tagline">Casa ta, în altă lumină.</p><p class="hero__lead">Profile care conturează. Texturi care inspiră.<br>Descoperă detaliile care transformă un spațiu în acasă.</p><a class="button" href="#vedete">Descoperă produsele vedetă <span aria-hidden="true">↗</span></a><p class="hero__terms">Toate ofertele sunt în limita stocului disponibil pe site.</p></div><div class="hero__ambient-label"><span>INSPIRAȚIE REALĂ</span><b>Carrara Best / NMC România</b></div></div>
<div class="campaign-deals"><a href="#exterior"><span>Profile exterior</span><strong>−20%</strong><small>Toate profilele · fără adezivi</small></a><a href="#interior"><span>Interior selectat</span><strong><em>până la</em>−40%</strong><small>Doar Z21, Z11, WO2, WT25, FD3, FO1, L2, L5</small></a><a href="#tapet"><span>Tapet Carrara Best</span><strong>−30%</strong><small>Doar variantele aflate în stoc</small></a></div></section>
<section class="curation wrap" id="colectii"><div class="section-heading"><div><span class="kicker">FRUMOS ÎN IMAGINI. ȘI MAI FRUMOS ACASĂ.</span><h2>Alege de unde începe schimbarea.</h2></div><p>Imagini ambientale reale din magazin.<br>Oferte pentru proiectul tău.</p></div><div class="ambience-grid">{teasers}</div></section>
<section class="featured wrap" id="vedete"><div class="section-heading"><div><span class="kicker">ÎN PRIM-PLAN</span><h2>Vedetele Black Friday.</h2></div><p>Exterior. Interior. Carrara Best.<br>Produse cu reducere, în limita stocului.</p></div><div class="featured-grid">{stars}</div></section>
<nav class="category-nav" aria-label="Navigare produse"><div class="wrap category-nav__inner">{''.join(f'<a class="chip" href="#{c[1]}">{c[2]}</a>' for c in categories)}<label class="search"><span class="sr-only">Caută în selecția de produse</span><input type="search" id="q" placeholder="Caută un produs…"><span aria-hidden="true">⌕</span></label></div></nav>
<div class="wrap"><p id="searchStatus" role="status" aria-live="polite"></p></div>
{''.join(collection(c, i) for i, c in enumerate(categories[:3], 1))}
<section class="project wrap framed"><div><span class="kicker">PROIECTUL TĂU MERITĂ ATENȚIE.</span><h2>Ai o idee.<br><span>Îi dăm contur.</span></h2><p>Echipa NMC te ajută să alegi profilele și materialele potrivite, de la prima schiță până la ultimul detaliu.</p><a class="button" href="tel:+40213193535">Vorbește cu un consultant <span aria-hidden="true">↗</span></a><span class="project__phone">021 319 35 35 · L–V, 07:30–16:00</span></div><img src="assets/scene-interior.jpg" alt="Detaliu decorativ într-un ambient de interior din galeria NMC" width="800" height="800" loading="lazy"></section>
{collection(categories[3], 4)}
<section class="faq wrap"><div class="faq__intro"><span class="kicker">CLAR, ÎNAINTE DE COMANDĂ.</span><h2>Bine de știut.</h2></div><div class="faq__items"><details><summary>Ce reduceri se aplică?</summary><p>−20% la toate profilele de exterior, cu excepția adezivilor. −30% doar la tapetul Carrara Best aflat în stoc. Până la −40% exclusiv la modelele de interior Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5. La adezivi, doar ADRO-FIX exterior 1,5 kg are −30%; ambalajul de 4 kg este la preț întreg.</p></details><details><summary>Ofertele sunt limitate de stoc?</summary><p>Da. Toate ofertele sunt în limita stocului disponibil pe nmcromania.ro. Deschide pagina produsului pentru a verifica stocul actual, oferta și condițiile de comandă. Variantele Carrara Best la comandă nu sunt incluse în reducere.</p></details><details><summary>Reducerile de interior se aplică întregii game?</summary><p>Nu. Campania de interior include doar Z21, Z11, WO2, WT25, FD3, FO1, L2 și L5, cu reduceri de până la 40%, în limita stocului disponibil. Alte modele de interior nu fac parte din această ofertă.</p></details></div></section>
</main>
<footer><div class="wrap"><a class="logo" href="https://www.nmcromania.ro/">NMC ROMÂNIA</a><span>Black Friday · Toate ofertele, în limita stocului disponibil pe site.<br>Stocul actual și condițiile de comandă se confirmă în magazin.</span><a href="https://www.nmcromania.ro/">Descoperă magazinul ↗</a></div></footer>
<script src="campaign.js" defer></script><script src="overlay-bridge.js" defer></script>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html)

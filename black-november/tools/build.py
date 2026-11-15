#!/usr/bin/env python3
"""Generează black-november/index.html din datele de mai jos.

Rulare:  python3 black-november/tools/build.py

Tot ce se schimbă des (texte de campanie, produse, linkuri) este în
CAMPANIE, PRODUSE, BANNERE și BLOG. HTML-ul rezultat e static: pagina se vede
complet și fără JavaScript. bn.js adaugă countdown, filtre, căutare și, când
pagina rulează pe nmcromania.ro, prețul și stocul live + „Adaugă în coș”.
"""
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.nmcromania.ro/"

# ---------------------------------------------------------------- campanie
CAMPANIE = {
    "titlu1": "BLACK",
    "titlu2": "NOVEMBER",
    "subtitlu": "O lună întreagă de prețuri speciale la profile decorative",
    "promisiune": "Calitate premium la cel mai bun raport calitate–preț",
    "sfarsit": "2026-11-30T23:59:59+02:00",
    "sfarsit_text": "30 noiembrie",
    "telefon": "021 319 35 35",
    "telefon_link": "tel:+40213193535",
    "program": "Luni–Vineri, 07:30–16:00",
    # Afirmațiile de încredere. Cele marcate (site) apar pe nmcromania.ro/despre-noi.
    "usp": [
        ("tag", "Prețuri speciale", "toată luna noiembrie, pe produsele din campanie"),
        ("truck", "Livrare imediată", "pentru produsele aflate în stoc"),
        ("box", "Stocuri mari", "pregătite pentru proiecte mici și mari"),          # (site) „menținem stocuri mari”
        ("ro", "Producție proprie", "în România · lider de piață de peste 20 de ani"),  # (site)
    ],
    "ticker": [
        "Black November la NMC România",
        "Prețuri speciale până pe 30 noiembrie",
        "Livrare imediată din stoc",
        "Stocuri mari pentru orice proiect",
        "Lider de piață de peste 20 de ani",
        "Cel mai bun raport calitate–preț",
    ],
}

# ---------------------------------------------------------------- produse
# cat: ext | int | riflaj | tapet ; sub: filtrul din secțiune ; star: apare la vedete
P = lambda **k: k
PRODUSE = [
    # ---- EXTERIOR (ADRo®) ----
    P(id="fuga1", cat="ext", sub="Termosisteme", brand="ADRo®", name="Termosistem decorativ FUGA PANEL 1", spec="500 × 40 × 2000 mm · finisaj + izolație",
      url="termosistem-decorativ-fuga-panel-1-de-4-cm-500x40x2000", img="fuga1", amb="fuga1-amb", star="Fațadă nouă, cu izolație inclusă", tag="Recomandat"),
    P(id="sid3", cat="ext", sub="Termosisteme", brand="ADRo®", name="Termosistem decorativ SIDDING PANEL 3", spec="500 × 40 × 2000 mm · aspect de lambriu",
      url="termosistem-decorativ-sidding-panel-3-500x40x2000", img="sid3", amb="sid3-amb", star="Aspect de lemn, fără întreținerea lemnului"),
    P(id="ncl107", cat="ext", sub="Colțare", brand="ADRo®", name="Colțar exterior NCL107", spec="300/300 × 30 × 1000 mm",
      url="coltar-exterior-decorativ-polistiren-ncl107-1000x30x300", img="ncl107", amb="ext-vila-patrat", star="Colțuri puternice, fațadă cu caracter", tag="Recomandat"),
    P(id="nc158", cat="ext", sub="Cornișe", brand="ADRo®", name="Cornișă decorativă exterior NC158", spec="200 × 127 × 2000 mm",
      url="cornisa-decorativa-nc158", img="nc158", amb="nc158-amb", star="Linia de acoperiș care se vede de departe"),
    P(id="np27", stoc=False, cat="ext", sub="Termosisteme", brand="ADRo®", name="Termosistem decorativ NP27", spec="540 × 45 × 2000 mm",
      url="termosistem-decorativ-polistiren-adro-decor-np27-540x45x2000", img="np27"),
    P(id="nc104", cat="ext", sub="Cornișe", brand="ADRo®", name="Cornișă decorativă exterior NC104", spec="220 × 80 × 2000 mm",
      url="cornisa-decorativa-exterior-nc104-220x80x2000", img="nc104"),
    P(id="rema3", cat="ext", sub="Ancadramente", brand="ADRo®", name="Ancadrament fereastră REMA3", spec="135 × 25 × 2000 mm",
      url="ancadrament-decorativ-rema3", img="rema3", hover="rema3-amb"),
    P(id="rema16", cat="ext", sub="Ancadramente", brand="ADRo®", name="Ancadrament fereastră REMA16", spec="100 × 30 × 2000 mm",
      url="ancadrament-decorativrema16", img="rema16"),
    P(id="na105", cat="ext", sub="Ancadramente", brand="ADRo®", name="Ancadrament fereastră NA105", spec="175 × 40 × 2000 mm",
      url="ancadrament-decorativ-na105", img="na105", hover="na105-amb"),
    P(id="ns108", cat="ext", sub="Solbancuri", brand="ADRo®", name="Solbanc fereastră NS108", spec="125 × 100 × 2000 mm",
      url="pervazsolbanc-ns108", img="ns108", hover="ns108-amb"),
    P(id="ns112", cat="ext", sub="Solbancuri", brand="ADRo®", name="Solbanc fereastră NS112", spec="135 × 75 × 2000 mm",
      url="pervazsolbanc-ns112", img="ns112"),
    P(id="refa15", cat="ext", sub="Solbancuri", brand="ADRo®", name="Solbanc fereastră REFA15", spec="75 × 65 × 2000 mm",
      url="pervazsolbanc-refa15", img="refa15"),
    P(id="nfc112", stoc=False, cat="ext", sub="Coloane", brand="ADRo®", name="Coloană decorativă NFC112", spec="Ø 200–350 × 2500 mm · la alegere", pret="Preț la cerere",
      url="coloana-decorativa-nfc112", img="nfc112"),
    P(id="npp1", cat="ext", sub="Coloane", brand="ADRo®", name="Pilastru decorativ NPP1", spec="250 × 30 × 2000 mm",
      url="pilastru-coloana-decorativanpp1", img="npp1"),
    P(id="a106", cat="ext", sub="Ornamente 3D", brand="ADRo®", name="Ornament 3D A106", spec="600 × 450 × 55 mm",
      url="accent-3d-a106-600x450x55", img="a106"),
    P(id="a114", stoc=False, cat="ext", sub="Ornamente 3D", brand="ADRo®", name="Ornament 3D A114", spec="500 × 630 × 65 mm",
      url="accent-3d-a114-500x630x65", img="a114"),
    # ---- INTERIOR ----
    P(id="linea", stoc=False, cat="int", sub="Kituri", brand="Noël & Marquet", name="Linea — kit complet pentru o cameră", spec="Plintă FD2 + cornișă GT + brâu WD5",
      url="linea-room-kit-complet-amenajare-fd2-gt-wd5-set-pentru-o-cameră", img="linea", tag="Kit complet"),
    P(id="fl2", cat="int", sub="Plinte", brand="Wallstyl", name="Plintă polimer dur FL2", spec="120 × 15 × 2000 mm",
      url="plintafl2-wallstyl", img="fl2"),
    P(id="ft2", cat="int", sub="Plinte", brand="Noël & Marquet", name="Plintă decorativă FT2 neagră", spec="58 × 13 × 2000 mm",
      url="plinta-decorativa-ft2-neagra-58x13x2000", img="ft2", tag="Negru mat"),
    P(id="il11", cat="int", sub="Plinte", brand="Noël & Marquet", name="Plintă LED IL11 neagră", spec="80 × 20 × 2000 mm · pentru bandă LED",
      url="plinta-decorativa-il11-neagra-80x20x2000", img="il11", tag="Iluminat LED"),
    P(id="wl11", cat="int", sub="Profile perete", brand="Wallstyl", name="Profil decorativ WL11", spec="49 × 15 × 2000 mm",
      url="profil-decorativ-wl11", img="wl11", hover="wl11-amb"),
    P(id="z1360", cat="int", sub="Profile perete", brand="Noël & Marquet", name="Brâu decorativ Z1360", spec="60 × 15 × 2000 mm",
      url="brau-z1360", img="z1360"),
    P(id="wt10", cat="int", sub="Cornișe", brand="Wallstyl", name="Cornișă polimer dur WT10", spec="84 × 84 × 2000 mm",
      url="cornisa-decorativawt10-wallstyl", img="wt10"),
    P(id="wt17", cat="int", sub="Cornișe", brand="Noël & Marquet", name="Cornișă decorativă WT17", spec="95 × 95 × 2000 mm",
      url="cornisa-decorativa-wt17", img="wt17"),
    P(id="z19", cat="int", sub="Cornișe", brand="Arstyl", name="Cornișă poliuretan Z19", spec="79 × 79 × 2000 mm",
      url="plinta-decorativa-tavan-arstyl-z19", img="z19", hover="z19-amb"),
    P(id="r8", cat="int", sub="Rozete", brand="Arstyl", name="Rozetă decorativă R8", spec="Ø 495 mm · poliuretan",
      url="rozeta-decorativar8-arstyl", img="r8", hover="r8-amb"),
    # ---- RIFLAJ (fără Alb cenușă — nu este pe stoc) ----
    P(id="rif-deschis", cat="riflaj", sub="Riflaje", brand="NMC", name="Riflaj acustic 3D — stejar deschis", spec="565 × 2600 × 19 mm · 1,47 m²/panou",
      url="riflaj-acustic-panou-3d-stejar-deschis", img="riflaj-deschis", tag="Acustic"),
    P(id="rif-inchis", cat="riflaj", sub="Riflaje", brand="NMC", name="Riflaj acustic 3D — stejar închis", spec="565 × 2600 × 19 mm · 1,47 m²/panou",
      url="riflaj-acustic-panou-3d-stejar-inchis", img="riflaj-inchis", tag="Acustic"),
    # ---- TAPET (modele în stoc) ----
    P(id="c82671", cat="tapet", sub="Tapet", brand="Carrara Best", name="Tapet Carrara Best — 82671", spec="Efect de marmură · rolă",
      url="tapet-carrara-82671", img="c82671", amb="c82671-amb"),
    P(id="rc19070", cat="tapet", sub="Tapet", brand="Roberto Cavalli", name="Tapet Roberto Cavalli 8 — 19070", spec="Colecție de designer · rolă",
      url="tapet-roberto-cavalli-8-19070", img="rc19070", amb="rc19070-amb"),
]

BLOG = [
    ("ext-casa", "Ce profile rezistă cel mai bine la ploaie, soare și îngheț", "blog/ce-profile-decorative-rezista-cel-mai-bine-la-ploaie-soare-si-inghet"),
    ("ext-ferestre", "Profile pentru ferestre: modele, proporții, greșeli de evitat", "blog/profile-decorative-ferestre-modele-proportii-greseli"),
    ("int-led", "Cum faci camera să pară mai înaltă și mai spațioasă", "blog/cum-faci-camera-sa-para-mai-inalta-spatioasa-profile-decorative"),
    ("riflaj-fatada", "Riflaje acustice 3D: perete premium și confort acustic", "blog/riflaje-acustice-3d-perete-premium-confort-acustic"),
]

CERCURI = [  # „stories” de categorie, în stil Trendyol
    ("Termosisteme", "fuga1-amb", "#exterior", "Termosisteme"),
    ("Cornișe ext.", "nc158", "#exterior", "Cornișe"),
    ("Colțare", "ncl107", "#exterior", "Colțare"),
    ("Ancadramente", "rema3-amb", "#exterior", "Ancadramente"),
    ("Solbancuri", "ns108-amb", "#exterior", "Solbancuri"),
    ("Coloane", "ext-colonade", "#exterior", "Coloane"),
    ("Ornamente 3D", "a106", "#exterior", "Ornamente 3D"),
    ("Kit cameră", "linea", "#interior", "Kituri"),
    ("Plinte", "il11", "#interior", "Plinte"),
    ("Cornișe int.", "z19-amb", "#interior", "Cornișe"),
    ("Rozete", "r8-amb", "#interior", "Rozete"),
    ("Riflaje", "riflaj-deschis", "#riflaj", ""),
    ("Tapet", "c82671-amb", "#tapet", ""),
]

ICONS = {
    "tag": '<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="8" cy="8" r="1.6"/>',
    "truck": '<path d="M2 6h12v10H2zM14 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "ro": '<path d="M12 2l2.6 6.2L21 9l-5 4.4L17.5 20 12 16.6 6.5 20 8 13.4 3 9l6.4-.8z"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "cart": '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6.2"/><circle cx="10" cy="20.5" r="1.3"/><circle cx="18" cy="20.5" r="1.3"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
}
ico = lambda k, s=22: f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'
href = lambda slug: SITE + quote(slug, safe="/-")
A = lambda name: f"assets/{name}.jpg"
CATN = {"ext": "Exterior", "int": "Interior", "riflaj": "Riflaje", "tapet": "Tapet"}


def price_ph(p):
    if p.get("pret"):
        return f'<span class="price__ph">{e(p["pret"])}</span>'
    return '<span class="price__ph">Preț special<span class="hide-m"> Black November</span></span>'


def stock_html(p, light=False):
    cls = "stock" + (" stock--light" if light else "")
    if p.get("stoc", True):
        return f'<p class="{cls}" data-stock><i></i>În stoc · livrare imediată</p>'
    return f'<p class="{cls} is-out" data-stock><i></i>Disponibil la comandă</p>'


def card(p, extra=""):
    u = href(p["url"])
    hover = f'<img class="card__hover" src="{A(p["hover"])}" alt="" loading="lazy">' if p.get("hover") else ""
    tag = f'<span class="tag">{e(p["tag"])}</span>' if p.get("tag") else ""
    search = " ".join([p["name"], p["spec"], p["brand"], p["sub"], CATN[p["cat"]], p["id"]]).lower()
    return f'''<article class="card{extra}" data-cat="{p["cat"]}" data-sub="{e(p["sub"])}" data-url="{u}" data-search="{e(search)}">
  <a class="card__img" href="{u}" aria-label="{e(p["name"])}"><img src="{A(p["img"])}" alt="{e(p["name"])}" loading="lazy" width="700" height="700">{hover}</a>
  <span class="badge">Preț special</span>{tag}
  <div class="card__body">
    <span class="card__brand">{e(p["brand"])} · {CATN[p["cat"]]}</span>
    <h3 class="card__name"><a href="{u}">{e(p["name"])}</a></h3>
    <p class="card__spec">{e(p["spec"])}</p>
    <div class="price" data-price>{price_ph(p)}</div>
    {stock_html(p)}
    <div class="card__actions"><a class="btn btn--buy" href="{u}" data-cta>Vezi prețul special {ico("arrow", 16)}</a></div>
  </div>
</article>'''


def star(p, i):
    u = href(p["url"])
    return f'''<article class="star" data-url="{u}" data-search="{e((p["name"]+" "+p["spec"]).lower())}">
  <div class="star__amb"><a href="{u}" tabindex="-1" aria-hidden="true"><img src="{A(p["amb"])}" alt="" loading="{"eager" if i < 2 else "lazy"}"></a>
    <img class="star__thumb" src="{A(p["img"])}" alt="" loading="lazy"></div>
  <span class="star__n">#{i+1} Vedetă</span>
  <div class="star__body">
    <span class="badge badge--static">Preț special</span>
    <h3><a href="{u}">{e(p["name"])}</a></h3>
    <p class="star__pitch">{e(p["star"])}</p>
    <p class="card__spec">{e(p["spec"])}</p>
    <div class="price price--light" data-price><span class="price__ph">Preț special<span class="hide-m"> Black November</span></span></div>
    {stock_html(p, True)}
    <a class="btn btn--hot" href="{u}" data-cta>Vezi prețul special {ico("arrow", 16)}</a>
  </div>
</article>'''


def chips(cat, items):
    subs = []
    for p in items:
        if p["sub"] not in subs:
            subs.append(p["sub"])
    if len(subs) < 2:
        return ""
    b = [f'<button class="fchip is-on" data-filter="*" aria-pressed="true">Toate <small>{len(items)}</small></button>']
    for s in subs:
        n = sum(1 for p in items if p["sub"] == s)
        b.append(f'<button class="fchip" data-filter="{e(s)}" aria-pressed="false">{e(s)} <small>{n}</small></button>')
    return f'<div class="filters" role="toolbar" aria-label="Filtrează {CATN[cat]}" data-for="{cat}">{"".join(b)}</div>'


def section(cat, kicker, title, lead, banner, accent, extra_top=""):
    items = [p for p in PRODUSE if p["cat"] == cat]
    return f'''<section class="sec" id="{ {"ext":"exterior","int":"interior","riflaj":"riflaj","tapet":"tapet"}[cat] }" style="--acc:{accent}">
  <div class="wrap">
    <div class="banner">
      <img src="{A(banner)}" alt="" loading="lazy">
      <div class="banner__txt">
        <span class="kicker">{e(kicker)}</span>
        <h2>{title}</h2>
        <p>{e(lead)}</p>
        <div class="banner__chips"><span>Preț special</span><span>În stoc</span><span>Livrare imediată</span></div>
      </div>
      <div class="banner__count"><b>{len(items)}</b><span>produse<br>în campanie</span></div>
    </div>
    {extra_top}
    {chips(cat, items)}
    <div class="grid" data-grid="{cat}">{"".join(card(p) for p in items)}</div>
    <p class="noresults" hidden>Niciun produs nu corespunde căutării în această secțiune.</p>
  </div>
</section>'''


def linea_spot():
    p = next(p for p in PRODUSE if p["id"] == "linea")
    u = href(p["url"])
    return f'''<div class="spot" data-url="{u}" data-search="linea kit cameră plintă cornișă brâu">
  <a class="spot__img" href="{u}"><img src="{A("linea")}" alt="Dormitor amenajat cu kitul Linea" loading="lazy"></a>
  <div class="spot__body">
    <span class="kicker">Recomandarea lunii · Interior</span>
    <h3>O cameră întreagă,<br>într-un singur pachet.</h3>
    <p>Kitul <b>Linea</b> reunește plinta FD2, cornișa GT și brâul WD5, profile Noël &amp; Marquet fabricate în Belgia. Alegi o singură dată și ai tot ce îți trebuie pentru o cameră.</p>
    <ul class="ticks"><li>Plintă FD2</li><li>Cornișă GT</li><li>Brâu WD5</li></ul>
    <div class="price price--light" data-price><span class="price__ph">Preț special<span class="hide-m"> Black November</span></span></div>
    <a class="btn btn--hot" href="{u}" data-cta>Vezi kitul Linea {ico("arrow", 16)}</a>
  </div>
</div>'''


def tapet_section():
    items = [p for p in PRODUSE if p["cat"] == "tapet"]
    cards = "".join(f'''<article class="wp" data-url="{href(p["url"])}" data-search="{e((p["name"]+" tapet").lower())}">
  <a class="wp__amb" href="{href(p["url"])}"><img src="{A(p["amb"])}" alt="Ambient cu {e(p["name"])}" loading="lazy"></a>
  <div class="wp__body">
    <img class="wp__swatch" src="{A(p["img"])}" alt="" loading="lazy">
    <div>
      <span class="card__brand">{e(p["brand"])} · în stoc</span>
      <h3><a href="{href(p["url"])}">{e(p["name"])}</a></h3>
      <p class="card__spec">{e(p["spec"])}</p>
      <div class="price" data-price><span class="price__ph">Preț special<span class="hide-m"> Black November</span></span></div>
    </div>
    <a class="btn btn--buy" href="{href(p["url"])}" data-cta>Vezi tapetul {ico("arrow", 16)}</a>
  </div>
</article>''' for p in items)
    return f'''<section class="sec" id="tapet" style="--acc:var(--purple)">
  <div class="wrap">
    <div class="sec-head"><div><span class="kicker">Tapet de designer · modele în stoc</span><h2>Pereți care spun o poveste</h2></div>
    <a class="link" href="{SITE}tapet">Toate modelele de tapet {ico("arrow", 16)}</a></div>
    <div class="wps">{cards}</div>
  </div>
</section>'''


def riflaj_section():
    items = [p for p in PRODUSE if p["cat"] == "riflaj"]
    feat = '''<div class="feat">
      <span class="kicker kicker--green">De ce riflaj acustic</span>
      <ul>
        <li><b>Acustic</b><span>panou cu pâslă care reduce ecoul din cameră</span></li>
        <li><b>Ușor</b><span>aprox. 3,4 kg/panou, pentru perete și tavan</span></li>
        <li><b>1,47 m²</b><span>acoperă un singur panou de 565 × 2600 mm</span></li>
        <li><b>Eco</b><span>realizat din PET reciclat</span></li>
      </ul>
      <p>Modele în stoc: stejar deschis și stejar închis.</p>
    </div>'''
    return f'''<section class="sec" id="riflaj" style="--acc:var(--green)">
  <div class="wrap">
    <div class="banner banner--green">
      <img src="{A("riflaj-fatada")}" alt="" loading="lazy">
      <div class="banner__txt">
        <span class="kicker">Riflaje acustice 3D</span>
        <h2>Textura lemnului.<br>Liniștea unui studio.</h2>
        <p>Panouri 3D cu aspect de lemn natural, ușor de montat prin lipire și prindere mecanică.</p>
        <div class="banner__chips"><span>Preț special</span><span>În stoc</span><span>Livrare imediată</span></div>
      </div>
    </div>
    <div class="grid grid--rif">{feat}{"".join(card(p) for p in items)}</div>
  </div>
</section>'''


def page():
    C = CAMPANIE
    stars = [p for p in PRODUSE if p.get("star")]
    usp = "".join(f'<div class="usp__i"><span class="usp__ico">{ico(k)}</span><div><b>{e(t)}</b><span>{e(s)}</span></div></div>' for k, t, s in C["usp"])
    ticker = "".join(f"<span>{e(t)}</span>" for t in C["ticker"] * 3)
    circles = "".join(f'<a class="circ" href="{h}" data-jump="{e(f)}"><span class="circ__img"><img src="{A(img)}" alt="" loading="lazy"></span><span class="circ__t">{e(t)}</span></a>' for t, img, h, f in CERCURI)
    blog = "".join(f'<a class="post" href="{SITE}{u}"><img src="{A(img)}" alt="" loading="lazy"><span class="post__t">{e(t)}</span><span class="post__more">Citește pe blog {ico("arrow", 14)}</span></a>' for img, t, u in BLOG)
    n_ext = sum(1 for p in PRODUSE if p["cat"] == "ext")
    n_int = sum(1 for p in PRODUSE if p["cat"] == "int")
    hero_cards = "".join(f'''<a class="hcard" href="{href(p["url"])}"><img src="{A(p["img"])}" alt=""><span><small>Preț special</small><b>{e(p["name"].replace("Termosistem decorativ ", ""))}</b><em>Vezi oferta →</em></span></a>''' for p in stars[:3])
    sections = (
        section("ext", "Exterior · ADRo®", "Fațade care cresc<br>valoarea casei",
                "Termosisteme, cornișe, colțare, ancadramente, solbancuri, coloane și ornamente 3D. Rezistente la UV, ploaie și îngheț, gata de vopsit în orice culoare.",
                "ext-vila-seara", "var(--red)")
        + f'''<section class="trust" aria-label="De ce NMC">
  <div class="trust__bg"><img src="{A("ext-fatada")}" alt="" loading="lazy"></div>
  <div class="wrap trust__in">
    <div><span class="kicker kicker--green">De ce să cumperi acum</span>
    <h2>Stocuri mari.<br><em>Livrare imediată.</em></h2>
    <p>Produsele din campanie sunt pe stoc și pleacă imediat spre tine. Fără liste de așteptare, fără „revenim cu un termen”.</p></div>
    <ul class="trust__list">
      <li><b>20+</b><span>ani de experiență · lider de piață</span></li>
      <li><b>RO</b><span>linie de producție proprie în România</span></li>
      <li><b>DIY</b><span>prezenți în marile lanțuri de bricolaj</span></li>
    </ul>
  </div>
</section>'''
        + section("int", "Interior · Noël &amp; Marquet · Wallstyl · Arstyl".replace("&amp;", "&"), "Detaliile care<br>schimbă camera",
                  "Plinte (inclusiv negre și cu LED), profile de perete, cornișe și rozete. Montaj curat, prin lipire, gata de vopsit.",
                  "int-led", "var(--purple)", linea_spot())
        + riflaj_section()
        + tapet_section()
    )
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Black November NMC România — prețuri speciale la profile decorative</title>
<meta name="description" content="Black November la NMC România: prețuri speciale toată luna la profile decorative de exterior și interior, riflaje și tapet. Stocuri mari, livrare imediată pentru produsele din stoc.">
<meta name="theme-color" content="#0B0A10">
<meta property="og:title" content="Black November la NMC România — prețuri speciale toată luna">
<meta property="og:description" content="Profile de exterior și interior, riflaje și tapet. Stocuri mari, livrare imediată.">
<meta property="og:image" content="assets/hero-vila.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="bn.css">
</head>
<body>
<a class="skip" href="#exterior">Sari la produse</a>

<div class="topbar"><div class="topbar__track">{ticker}</div></div>

<header class="hdr">
  <div class="wrap hdr__row">
    <a class="logo" href="{SITE}" aria-label="NMC România"><img src="assets/nmc-logo-alb.png" alt="NMC" width="120" height="34"><span>Black<br>November</span></a>
    <label class="search"><span class="sr-only">Caută în ofertele Black November</span>{ico("search", 18)}
      <input id="bn-q" type="search" placeholder="Caută: NCL107, cornișă, plintă neagră, riflaj…" autocomplete="off"></label>
    <a class="hdr__phone" href="{C["telefon_link"]}">{ico("phone", 18)}<span><small>Consultanță gratuită</small>{C["telefon"]}</span></a>
    <a class="hdr__shop" href="{SITE}cos-cumparaturi" aria-label="Coșul din magazin">{ico("cart", 20)}<b id="bn-cart" hidden>0</b></a>
  </div>
  <nav class="wrap nav" aria-label="Secțiuni">
    <a href="#vedete" class="nav__hot">🔥 Vedete</a><a href="#exterior">Exterior <small>{n_ext}</small></a><a href="#interior">Interior <small>{n_int}</small></a><a href="#riflaj">Riflaje</a><a href="#tapet">Tapet</a><a href="#inspiratie">Inspirație</a><a href="#intrebari">Întrebări</a>
  </nav>
</header>

<main>
<section class="hero">
  <img class="hero__bg" src="{A("hero-vila")}" alt="Vilă cu fațadă decorată cu profile NMC" fetchpriority="high">
  <div class="hero__shade"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <span class="pill"><i></i> Doar până pe {C["sfarsit_text"]}</span>
      <h1><span class="h1a">{C["titlu1"]}</span><span class="h1b">{C["titlu2"]}</span></h1>
      <p class="hero__sub">{e(C["subtitlu"])}</p>
      <p class="hero__promise">{ico("tag", 18)} {e(C["promisiune"])}</p>
      <div class="hero__cta">
        <a class="btn btn--hot btn--lg" href="#exterior">Vezi ofertele de exterior {ico("arrow", 18)}</a>
        <a class="btn btn--ghost btn--lg" href="#interior">Interior &amp; tapet</a>
      </div>
      <div class="cd" role="timer" aria-label="Timp rămas din campanie">
        <span class="cd__l">Prețurile speciale expiră în</span>
        <div class="cd__b" data-cd="{C["sfarsit"]}"><span><b data-d>--</b>zile</span><span><b data-h>--</b>ore</span><span><b data-m>--</b>min</span><span><b data-s>--</b>sec</span></div>
      </div>
    </div>
    <div class="hero__deals" aria-label="Produse vedetă">{hero_cards}</div>
  </div>
</section>

<section class="usp"><div class="wrap usp__row">{usp}</div></section>

<section class="circles" aria-label="Categorii"><div class="wrap circles__row">{circles}</div></section>

<section class="sec sec--dark" id="vedete">
  <div class="wrap">
    <div class="sec-head"><div><span class="kicker kicker--hot">Vedetele Black November</span><h2>Vedetele lunii<br>pentru fațada ta</h2></div>
      <span class="timer-mini">Expiră în <b data-cd-mini>--</b></span></div>
    <div class="stars">{"".join(star(p, i) for i, p in enumerate(stars))}</div>
  </div>
</section>

<p class="wrap searchinfo" id="bn-status" role="status" aria-live="polite"></p>
{sections}

<section class="sec" id="inspiratie">
  <div class="wrap">
    <div class="sec-head"><div><span class="kicker">Inspirație din blogul NMC</span><h2>Idei înainte de comandă</h2></div>
    <a class="link" href="{SITE}blog">Toate articolele {ico("arrow", 16)}</a></div>
    <div class="posts">{blog}</div>
  </div>
</section>

<section class="sec" id="consultanta">
  <div class="wrap">
    <div class="help">
      <img src="{A("ext-intrare")}" alt="" loading="lazy">
      <div class="help__body">
        <span class="kicker kicker--green">Consultanță gratuită</span>
        <h2>Nu știi ce profil să alegi?</h2>
        <p>Spune-ne ce proiect ai: te ajutăm să alegi modelul și să calculezi necesarul, înainte de comandă.</p>
        <div class="hero__cta"><a class="btn btn--green btn--lg" href="{C["telefon_link"]}">{ico("phone", 18)} Sună: {C["telefon"]}</a>
        <a class="btn btn--ghost btn--lg" href="{SITE}contact">Scrie-ne</a></div>
        <small>{e(C["program"])}</small>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="intrebari">
  <div class="wrap faq">
    <div><span class="kicker">Bine de știut</span><h2>Întrebări frecvente</h2></div>
    <div>
      <details><summary>Cât timp sunt valabile prețurile speciale?</summary><p>Campania Black November ține până pe {C["sfarsit_text"]}, în limita stocului disponibil. Prețul final este cel afișat pe pagina produsului din magazin în momentul comenzii.</p></details>
      <details><summary>Cât de repede primesc comanda?</summary><p>Produsele aflate în stoc se pregătesc imediat pentru livrare. Disponibilitatea apare pe fiecare pagină de produs; costul și condițiile de livrare sunt afișate în coș.</p></details>
      <details><summary>Profilele de exterior se pot vopsi?</summary><p>Da. Profilele ADRo® pentru exterior se vopsesc cu vopsea acrilică de exterior, în orice culoare. Pentru lipire și finisare găsești adezivii și amorsele potrivite în magazin.</p></details>
      <details><summary>Mă puteți ajuta cu necesarul pentru casa mea?</summary><p>Da, gratuit. Sună la <a href="{C["telefon_link"]}">{C["telefon"]}</a> ({e(C["program"])}) sau trimite-ne planurile prin pagina de contact.</p></details>
    </div>
  </div>
</section>
</main>

<footer class="ftr">
  <div class="wrap ftr__row">
    <img src="assets/nmc-logo-alb.png" alt="NMC România" width="96" height="27">
    <p>Black November · prețuri speciale până pe {C["sfarsit_text"]}, în limita stocului disponibil. Prețul, stocul și condițiile de livrare se confirmă pe pagina fiecărui produs.</p>
    <a href="{SITE}">nmcromania.ro {ico("arrow", 14)}</a>
  </div>
</footer>

<div class="mbar"><a class="btn btn--hot" href="#vedete">Vezi ofertele</a><a class="btn btn--green" href="{C["telefon_link"]}" aria-label="Sună">{ico("phone", 18)}</a></div>
<div class="toast" id="bn-toast" role="status" aria-live="polite"></div>
<script src="bn.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    for p in PRODUSE:
        for k in ("img", "amb", "hover"):
            if p.get(k):
                assert (ROOT / A(p[k])).exists(), A(p[k])
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    print("OK", ROOT / "index.html", len(PRODUSE), "produse")

#!/usr/bin/env python3
"""Generează black-november/index.html (Black November · NMC România).

Rulare:  python3 black-november/tools/build.py

Regulă de campanie: „prețuri speciale” se comunică DOAR general (hero, benzi,
secțiuni). Pe produse nu apar prețuri, procente sau alte cifre de preț.
Tot ce se schimbă des este în CAMPANIE, PRODUSE, BLOG și CERCURI.
"""
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.nmcromania.ro/"

CAMPANIE = {
    "sfarsit": "2026-11-30T23:59:59+02:00",
    "sfarsit_text": "30 noiembrie",
    "telefon": "021 319 35 35",
    "telefon_link": "tel:+40213193535",
    "program": "Luni–Vineri, 07:30–16:00",
    "ticker": [
        "Black November · prețuri speciale doar până pe 30 noiembrie",
        "Livrare imediată pentru produsele din stoc",
        "Stocuri mari, pregătite pentru proiectul tău",
        "Lider de piață de peste 20 de ani",
        "Cel mai bun raport calitate–preț",
    ],
}

P = lambda **k: k
PRODUSE = [
    # ---- EXTERIOR (ADRo®) ----
    P(id="fuga1", cat="ext", sub="Termosisteme", brand="ADRo®", name="Termosistem decorativ FUGA PANEL 1", spec="500 × 40 × 2000 mm · finisaj + izolație",
      url="termosistem-decorativ-fuga-panel-1-de-4-cm-500x40x2000", img="fuga1", amb="fuga1-amb", star="Fațadă nouă, cu izolație inclusă", tag="Alegerea lunii"),
    P(id="sid3", cat="ext", sub="Termosisteme", brand="ADRo®", name="Termosistem decorativ SIDDING PANEL 3", spec="500 × 40 × 2000 mm · aspect de lambriu",
      url="termosistem-decorativ-sidding-panel-3-500x40x2000", img="sid3", amb="sid3-amb", star="Aspect de lemn, fără întreținerea lemnului"),
    P(id="ncl107", cat="ext", sub="Colțare", brand="ADRo®", name="Colțar exterior NCL107", spec="300/300 × 30 × 1000 mm",
      url="coltar-exterior-decorativ-polistiren-ncl107-1000x30x300", img="ncl107", amb="ext-vila-patrat", star="Colțuri puternice, fațadă cu caracter", tag="Alegerea lunii"),
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
    P(id="nfc112", stoc=False, cat="ext", sub="Coloane", brand="ADRo®", name="Coloană decorativă NFC112", spec="Ø 200–350 × 2500 mm · la alegere",
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
    "crown": '<path d="M3 8l4.5 4L12 5l4.5 7L21 8l-2 11H5z"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "cart": '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6.2"/><circle cx="10" cy="20.5" r="1.3"/><circle cx="18" cy="20.5" r="1.3"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
}
ico = lambda k, s=22: f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'
href = lambda slug: SITE + quote(slug, safe="/-")
A = lambda name: f"assets/{name}.jpg"
CATN = {"ext": "Exterior", "int": "Interior", "riflaj": "Riflaje", "tapet": "Tapet"}
SECID = {"ext": "exterior", "int": "interior", "riflaj": "riflaj", "tapet": "tapet"}


def stock_html(p):
    if p.get("stoc", True):
        return '<p class="stock" data-stock><i></i>În stoc · livrare imediată</p>'
    return '<p class="stock is-out" data-stock><i></i>Disponibil la comandă</p>'


def card(p):
    u = href(p["url"])
    hover = f'<img class="card__hover" src="{A(p["hover"])}" alt="" loading="lazy">' if p.get("hover") else ""
    tag = f'<span class="tag">{e(p["tag"])}</span>' if p.get("tag") else ""
    search = " ".join([p["name"], p["spec"], p["brand"], p["sub"], CATN[p["cat"]], p["id"]]).lower()
    return f'''<article class="card" data-cat="{p["cat"]}" data-sub="{e(p["sub"])}" data-url="{u}" data-search="{e(search)}">
  <a class="card__img" href="{u}" aria-label="{e(p["name"])}"><img src="{A(p["img"])}" alt="{e(p["name"])}" loading="lazy" width="700" height="700">{hover}</a>{tag}
  <div class="card__body">
    <span class="card__brand">{e(p["brand"])}</span>
    <h3 class="card__name"><a href="{u}">{e(p["name"])}</a></h3>
    <p class="card__spec">{e(p["spec"])}</p>
    {stock_html(p)}
    <div class="card__actions"><a class="btn btn--line" href="{u}" data-cta>Descoperă produsul {ico("arrow", 15)}</a></div>
  </div>
</article>'''


def star(p, i):
    u = href(p["url"])
    return f'''<article class="star" data-url="{u}" data-search="{e((p["name"]+" "+p["spec"]).lower())}">
  <div class="star__amb"><a href="{u}" tabindex="-1" aria-hidden="true"><img src="{A(p["amb"])}" alt="" loading="{"eager" if i < 2 else "lazy"}"></a>
    <img class="star__thumb" src="{A(p["img"])}" alt="" loading="lazy"></div>
  <div class="star__body">
    <span class="star__n">N° {i+1:02d} · Vedeta lunii</span>
    <h3><a href="{u}">{e(p["name"])}</a></h3>
    <p class="star__pitch">{e(p["star"])}</p>
    <p class="card__spec">{e(p["spec"])}</p>
    {stock_html(p)}
    <a class="btn btn--rose" href="{u}" data-cta>Descoperă produsul {ico("arrow", 16)}</a>
  </div>
</article>'''


def chips(cat, items):
    subs = []
    for p in items:
        if p["sub"] not in subs:
            subs.append(p["sub"])
    if len(subs) < 2:
        return ""
    b = ['<button class="fchip is-on" data-filter="*" aria-pressed="true">Toate</button>']
    b += [f'<button class="fchip" data-filter="{e(s)}" aria-pressed="false">{e(s)}</button>' for s in subs]
    return f'<div class="filters" role="toolbar" aria-label="Filtrează {CATN[cat]}" data-for="{cat}">{"".join(b)}</div>'


def banner(img, kicker, title, lead, tone="forest", promise="Prețuri speciale în noiembrie"):
    return f'''<div class="banner banner--{tone}">
      <img src="{A(img)}" alt="" loading="lazy">
      <div class="banner__txt">
        <span class="kicker">{e(kicker)}</span>
        <h2>{title}</h2>
        <p>{e(lead)}</p>
        <div class="banner__promise"><span>{e(promise)}</span><span>În stoc</span><span>Livrare imediată</span></div>
      </div>
    </div>'''


def section(cat, kicker, title, lead, img, tone, extra_top=""):
    items = [p for p in PRODUSE if p["cat"] == cat]
    return f'''<section class="sec sec--{tone}" id="{SECID[cat]}">
  <div class="wrap">
    {banner(img, kicker, title, lead, tone)}
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
    <span class="kicker">Alegerea lunii · Interior</span>
    <h3>O cameră întreagă,<br><em>într-un singur gest.</em></h3>
    <p>Kitul <b>Linea</b> reunește plinta FD2, cornișa GT și brâul WD5, profile Noël &amp; Marquet fabricate în Belgia. Tot ce îi trebuie unei camere ca să arate finisată, în același pachet.</p>
    <ul class="ticks"><li>Plintă FD2</li><li>Cornișă GT</li><li>Brâu WD5</li></ul>
    {stock_html(p)}
    <a class="btn btn--rose" href="{u}" data-cta>Descoperă kitul Linea {ico("arrow", 16)}</a>
  </div>
</div>'''


def riflaj_section():
    items = [p for p in PRODUSE if p["cat"] == "riflaj"]
    feat = f'''<div class="feat">
      <span class="kicker">De ce riflaj acustic</span>
      <ul>
        <li><b>Acustic</b><span>pâslă care reduce ecoul din cameră</span></li>
        <li><b>Ușor</b><span>pentru perete și tavan, montaj simplu</span></li>
        <li><b>Natural</b><span>aspect de stejar, deschis sau închis</span></li>
        <li><b>Eco</b><span>realizat din PET reciclat</span></li>
      </ul>
      <p class="feat__note">Două nuanțe în stoc: stejar deschis și stejar închis. Prețuri speciale în noiembrie.</p>
      <a class="btn btn--forest" href="{SITE}riflaje-acustice-3d">Toate riflajele</a>
    </div>'''
    return f'''<section class="sec sec--forest" id="riflaj">
  <div class="wrap">
    {banner("riflaj-fatada", "Riflaje acustice 3D", "Textura lemnului.<br><em>Liniștea unui studio.</em>", "Panouri 3D cu aspect de lemn natural, pentru pereți și tavane care se aud la fel de bine cum arată.", "forest")}
    <div class="grid grid--rif">{feat}{"".join(card(p) for p in items)}</div>
  </div>
</section>'''


def tapet_section():
    items = [p for p in PRODUSE if p["cat"] == "tapet"]
    cards = "".join(f'''<article class="wp" data-url="{href(p["url"])}" data-search="{e((p["name"]+" tapet").lower())}">
  <a class="wp__amb" href="{href(p["url"])}"><img src="{A(p["amb"])}" alt="Ambient cu {e(p["name"])}" loading="lazy"></a>
  <div class="wp__body">
    <img class="wp__swatch" src="{A(p["img"])}" alt="" loading="lazy">
    <div>
      <span class="card__brand">{e(p["brand"])}</span>
      <h3><a href="{href(p["url"])}">{e(p["name"])}</a></h3>
      <p class="card__spec">{e(p["spec"])}</p>
      {stock_html(p)}
    </div>
    <a class="btn btn--line" href="{href(p["url"])}" data-cta>Descoperă tapetul {ico("arrow", 15)}</a>
  </div>
</article>''' for p in items)
    return f'''<section class="sec sec--plum" id="tapet">
  <div class="wrap">
    <div class="sec-head"><div><span class="kicker">Tapet de designer · modele în stoc</span><h2>Pereți care<br><em>spun o poveste.</em></h2></div>
    <a class="link" href="{SITE}tapet">Toate modelele de tapet {ico("arrow", 16)}</a></div>
    <div class="wps">{cards}</div>
  </div>
</section>'''


def page():
    C = CAMPANIE
    stars = [p for p in PRODUSE if p.get("star")]
    ticker = "".join(f"<span>{e(t)}</span>" for t in C["ticker"] * 3)
    circles = "".join(f'<a class="circ" href="{h}" data-jump="{e(f)}"><span class="circ__img"><img src="{A(img)}" alt="" loading="lazy"></span><span class="circ__t">{e(t)}</span></a>' for t, img, h, f in CERCURI)
    blog = "".join(f'<a class="post" href="{SITE}{u}"><img src="{A(img)}" alt="" loading="lazy"><span class="post__t">{e(t)}</span><span class="post__more">Citește pe blog {ico("arrow", 14)}</span></a>' for img, t, u in BLOG)
    usp = [("tag", "Prețuri speciale", "pe toată selecția, doar în noiembrie"),
           ("truck", "Livrare imediată", "pentru produsele aflate în stoc"),
           ("box", "Stocuri mari", "pregătite pentru proiecte mici și mari"),
           ("crown", "Lider de piață", "peste 20 de ani · producție proprie în România")]
    usp_html = "".join(f'<div class="usp__i"><span class="usp__ico">{ico(k)}</span><div><b>{e(t)}</b><span>{e(s)}</span></div></div>' for k, t, s in usp)
    sections = (
        section("ext", "Colecția Exterior · ADRo®", "Fațade care<br><em>cresc valoarea casei.</em>",
                "Termosisteme, cornișe, colțare, ancadramente, solbancuri, coloane și ornamente 3D. Rezistente la UV, ploaie și îngheț, gata de vopsit în orice culoare.",
                "ext-vila-seara", "forest")
        + f'''<section class="manifest" aria-label="De ce acum">
  <div class="manifest__bg"><img src="{A("ext-fatada")}" alt="" loading="lazy"></div>
  <div class="wrap manifest__in">
    <span class="kicker">Black November</span>
    <p class="manifest__quote">O singură lună în care<br><em>calitatea premium</em> are<br>prețuri speciale.</p>
    <div class="manifest__row">
      <div><b>Stocuri mari</b><span>Produsele din campanie sunt pregătite pentru livrare imediată.</span></div>
      <div><b>Producție proprie</b><span>Profile de exterior realizate pe propria linie de producție din România.</span></div>
      <div><b>Peste 20 de ani</b><span>Lider de piață în profile și finisaje decorative.</span></div>
    </div>
    <a class="btn btn--rose btn--lg" href="#interior">Continuă cu interiorul {ico("arrow", 18)}</a>
  </div>
</section>'''
        + section("int", "Colecția Interior", "Detaliile care<br><em>schimbă camera.</em>",
                  "Plinte negre și cu LED, profile de perete, cornișe și rozete. Montaj curat, prin lipire, gata de vopsit.",
                  "int-led", "plum", linea_spot())
        + riflaj_section()
        + tapet_section()
    )
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Black November · NMC România — prețuri speciale la profile decorative</title>
<meta name="description" content="Black November la NMC România: prețuri speciale toată luna noiembrie la profile decorative de exterior și interior, riflaje și tapet. Stocuri mari, livrare imediată pentru produsele din stoc.">
<meta name="theme-color" content="#070A09">
<meta property="og:title" content="Black November · NMC România — prețuri speciale până pe 30 noiembrie">
<meta property="og:description" content="Profile de exterior și interior, riflaje și tapet de designer. Stocuri mari, livrare imediată.">
<meta property="og:image" content="assets/hero-vila.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="bn.css">
</head>
<body>
<a class="skip" href="#exterior">Sari la produse</a>
<div class="grain" aria-hidden="true"></div>

<div class="topbar"><div class="topbar__track">{ticker}</div></div>

<header class="hdr">
  <div class="wrap hdr__row">
    <a class="logo" href="{SITE}" aria-label="NMC România"><img src="assets/nmc-logo-alb.png" alt="NMC" width="110" height="31"><span>Black November</span></a>
    <label class="search"><span class="sr-only">Caută în colecția Black November</span>{ico("search", 17)}
      <input id="bn-q" type="search" placeholder="Caută: NCL107, cornișă, plintă neagră, riflaj…" autocomplete="off"></label>
    <a class="hdr__phone" href="{C["telefon_link"]}">{ico("phone", 17)}<span><small>Consultanță gratuită</small>{C["telefon"]}</span></a>
    <a class="hdr__shop" href="{SITE}cos-cumparaturi" aria-label="Coșul din magazin">{ico("cart", 19)}<b id="bn-cart" hidden>0</b></a>
  </div>
  <nav class="wrap nav" aria-label="Secțiuni">
    <a href="#vedete">Vedete</a><a href="#exterior">Exterior</a><a href="#interior">Interior</a><a href="#riflaj">Riflaje</a><a href="#tapet">Tapet</a><a href="#inspiratie">Inspirație</a><a href="#intrebari">Întrebări</a>
  </nav>
</header>

<main>
<section class="hero">
  <img class="hero__bg" src="{A("hero-vila")}" alt="Vilă cu fațadă decorată cu profile NMC" fetchpriority="high">
  <div class="hero__shade"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <span class="eyebrow"><i></i>Ediție limitată · până pe {C["sfarsit_text"]}</span>
      <h1><span class="h1a">Black</span><span class="h1b">November</span></h1>
      <p class="hero__sub">Prețuri speciale pe întreaga selecție de profile decorative.<br><strong>O singură lună. Doar la NMC.</strong></p>
      <p class="hero__promise">Calitate premium · cel mai bun raport calitate–preț</p>
      <div class="hero__cta">
        <a class="btn btn--rose btn--lg" href="#vedete">Descoperă ofertele {ico("arrow", 18)}</a>
        <a class="btn btn--ghost btn--lg" href="#exterior">Colecția Exterior</a>
      </div>
      <div class="cd" role="timer" aria-label="Timp rămas din campanie">
        <span class="cd__l">Prețurile speciale se încheie în</span>
        <div class="cd__b" data-cd="{C["sfarsit"]}"><span><b data-d>--</b>zile</span><span><b data-h>--</b>ore</span><span><b data-m>--</b>min</span><span><b data-s>--</b>sec</span></div>
      </div>
    </div>
  </div>
  <a class="hero__scroll" href="#vedete" aria-label="Derulează la oferte"><span></span></a>
</section>

<section class="usp"><div class="wrap usp__row">{usp_html}</div></section>

<section class="circles" aria-label="Categorii"><div class="wrap circles__row">{circles}</div></section>

<section class="sec sec--plum" id="vedete">
  <div class="wrap">
    <div class="sec-head"><div><span class="kicker">Vedetele Black November</span><h2>Alese pentru<br><em>fațada ta.</em></h2></div>
      <span class="timer-mini">Prețuri speciale încă <b data-cd-mini>--</b></span></div>
    <div class="stars">{"".join(star(p, i) for i, p in enumerate(stars))}</div>
  </div>
</section>

<p class="wrap searchinfo" id="bn-status" role="status" aria-live="polite"></p>
{sections}

<section class="sec" id="inspiratie">
  <div class="wrap">
    <div class="sec-head"><div><span class="kicker">Din jurnalul NMC</span><h2>Inspirație<br><em>înainte de comandă.</em></h2></div>
    <a class="link" href="{SITE}blog">Toate articolele {ico("arrow", 16)}</a></div>
    <div class="posts">{blog}</div>
  </div>
</section>

<section class="sec" id="consultanta">
  <div class="wrap">
    <div class="help">
      <img src="{A("ext-intrare")}" alt="" loading="lazy">
      <div class="help__body">
        <span class="kicker">Consultanță gratuită</span>
        <h2>Nu știi ce profil<br><em>să alegi?</em></h2>
        <p>Spune-ne ce proiect ai. Te ajutăm să alegi modelul potrivit și să calculezi necesarul, cât timp prețurile speciale sunt încă active.</p>
        <div class="hero__cta"><a class="btn btn--forest btn--lg" href="{C["telefon_link"]}">{ico("phone", 18)} {C["telefon"]}</a>
        <a class="btn btn--ghost btn--lg" href="{SITE}contact">Scrie-ne</a></div>
        <small>{e(C["program"])}</small>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="intrebari">
  <div class="wrap faq">
    <div><span class="kicker">Bine de știut</span><h2>Întrebări<br><em>frecvente.</em></h2></div>
    <div>
      <details><summary>Cât timp sunt valabile prețurile speciale?</summary><p>Campania Black November ține până pe {C["sfarsit_text"]}, în limita stocului disponibil. Prețul final este cel afișat în magazin la momentul comenzii.</p></details>
      <details><summary>Cât de repede primesc comanda?</summary><p>Produsele aflate în stoc se pregătesc imediat pentru livrare. Disponibilitatea apare pe pagina fiecărui produs, iar costul și condițiile de livrare sunt afișate în coș.</p></details>
      <details><summary>Profilele de exterior se pot vopsi?</summary><p>Da. Profilele ADRo® pentru exterior se vopsesc cu vopsea acrilică de exterior, în orice culoare. Adezivii și amorsele potrivite le găsești tot în magazin.</p></details>
      <details><summary>Mă puteți ajuta cu necesarul pentru casa mea?</summary><p>Da, gratuit. Sună la <a href="{C["telefon_link"]}">{C["telefon"]}</a> ({e(C["program"])}) sau trimite-ne planurile prin pagina de contact.</p></details>
    </div>
  </div>
</section>

<section class="closing">
  <div class="wrap closing__in">
    <span class="kicker">Ultimele zile</span>
    <h2>Black <em>November</em></h2>
    <p>Prețurile speciale se încheie pe {C["sfarsit_text"]}. După aceea, colecția revine la prețurile obișnuite.</p>
    <a class="btn btn--rose btn--lg" href="#vedete">Alege acum {ico("arrow", 18)}</a>
  </div>
</section>
</main>

<footer class="ftr">
  <div class="wrap ftr__row">
    <img src="assets/nmc-logo-alb.png" alt="NMC România" width="92" height="26">
    <p>Black November · prețuri speciale până pe {C["sfarsit_text"]}, în limita stocului disponibil. Prețul, stocul și condițiile de livrare se confirmă pe pagina fiecărui produs.</p>
    <a href="{SITE}">nmcromania.ro {ico("arrow", 14)}</a>
  </div>
</footer>

<div class="mbar"><a class="btn btn--rose" href="#vedete">Descoperă ofertele</a><a class="btn btn--forest" href="{C["telefon_link"]}" aria-label="Sună">{ico("phone", 18)}</a></div>
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
    html = page()
    assert "lei" not in html.lower().replace("lumea", ""), "Nu punem prețuri pe pagină"
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("OK", ROOT / "index.html", len(PRODUSE), "produse")

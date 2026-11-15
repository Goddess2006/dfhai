#!/usr/bin/env python3
"""Generează decoflair-landing/index.html — „Selecția Premium 2027” · Deco&Flair.

Rulare:  python3 decoflair-landing/tools/build.py

Regula campaniei: pe produse nu apar prețuri, procente sau alte cifre de preț.
„Prețuri speciale” se comunică doar general (hero, benzi, final).
Tot ce se schimbă des e în CAMPANIE, CAPITOLE (produse), SERVICII și BLOG.
"""
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://decoflair.ro/"

CAMPANIE = {
    "eticheta": "Black November · Ediția 2027",
    "sfarsit": "2026-11-30T23:59:59+02:00",   # countdown; după dată banda de campanie dispare (vezi df.js)
    "sfarsit_text": "30 noiembrie",
    "telefon": "0723 300 603",
    "telefon_link": "tel:+40723300603",
    "email": "office@decoflair.ro",
    "program": "Luni–Vineri, 07:30–16:00",
    "instagram": "https://www.instagram.com/decoflairhub/",
}

BRANDURI = ["Arstyl®", "Wallstyl®", "Nomastyl®", "ADRo®", "NMC®", "Carrara Best", "Roberto Cavalli", "Noël & Marquet"]

P = lambda **k: k
# Fiecare capitol: ambient + produse (toate verificate „în stoc” pe decoflair.ro la 15.11.2026)
CAPITOLE = [
    dict(id="lumina", n="01", nume="Lumină", titlu="Lumina devine<br><em>arhitectură.</em>",
         text="Scafe și cornișe pentru bandă LED: lumină indirectă, caldă, fără corpuri de iluminat la vedere. Detaliul care schimbă complet atmosfera unei camere.",
         amb="living-led", know="Pune banda LED la 5–10 cm de perete: lumina „spală” suprafața uniform, fără puncte vizibile.",
         produse=[
            P(id="l5", brand="Arstyl®", name="Scafă LED L5", spec="200 × 200 × 2000 mm · poliuretan", url="l5-arstyl", img="l5", tag="Inovație"),
            P(id="l2", brand="Arstyl®", name="Scafă LED L2", spec="Lumină indirectă tavan / perete", url="l2-arstyl", img="l2"),
            P(id="il18", brand="Wallstyl®", name="Cornișă LED IL18", spec="121 × 90 × 2000 mm", url="cornisa-led-il18-121x90x2000", img="il18", hover="il18-amb"),
            P(id="il11", brand="Wallstyl®", name="Plintă LED IL11", spec="80 × 20 × 2000 mm", url="plinta-decorativa-parchet-alba-polimer-dur-wallstyl-il11-80x20x2m", img="il11", hover="il11-amb"),
         ]),
    dict(id="texturi", n="02", nume="Texturi 3D", titlu="Pereți care<br><em>se simt.</em>",
         text="Panouri decorative 3D din poliuretan: valuri, canelură, forme organice. Se vopsesc în orice culoare și transformă un perete simplu într-o piesă de design.",
         amb="wave-amb", know="Pe un perete texturat, lumina laterală (aplică sau LED) dublează adâncimea reliefului.",
         produse=[
            P(id="wave", brand="Arstyl®", name="Panou 3D WAVE", spec="Relief în valuri · poliuretan", url="panou-decorativ-3d-wave", img="wave", hover="wave-amb", tag="Tendință 2027"),
            P(id="canele", brand="Arstyl®", name="Panou 3D CANELE L", spec="Canelură verticală fină", url="panou-decorativ-canelel", img="canele", hover="canele-amb"),
            P(id="liquid", brand="Arstyl®", name="Panou 3D LIQUID", spec="Forme fluide, organice", url="panou-decorativ-3d-liquid", img="liquid", hover="liquid-amb"),
            P(id="icon", brand="Arstyl®", name="Panou 3D ICON", spec="Module rotunjite, ritm grafic", url="panou-decorativ-3d-icon", img="icon", hover="icon-amb"),
         ]),
    dict(id="tavan", n="03", nume="Tavan", titlu="Tavanul care<br><em>spune o poveste.</em>",
         text="Cornișe și rozete din poliuretan de înaltă densitate: de la linii minimaliste la clasic rafinat. Montaj curat, prin lipire, gata de vopsit.",
         amb="living-nude", know="Regula proporției: cu cât tavanul e mai înalt, cu atât cornișa poate fi mai generoasă.",
         produse=[
            P(id="z11", brand="Arstyl®", name="Cornișă Z11", spec="148 × 69 × 2000 mm", url="plinta-decorativa-tavan-arstyl-z11", img="z11", hover="z11-amb"),
            P(id="z21", brand="Arstyl®", name="Cornișă Z21", spec="101 × 112 × 2000 mm", url="plinta-decorativa-tavan-arstyl-z21", img="z21"),
            P(id="wt25", brand="Wallstyl®", name="Cornișă WT25", spec="78 × 78 × 2000 mm · polimer dur", url="cornisa-decorativa-wt25-wallstyl", img="wt25", hover="wt25-amb"),
            P(id="r12", brand="Arstyl®", name="Rozetă R12", spec="Ø 825 mm · poliuretan", url="rozeta-decorativar12-arstyl", img="r12", hover="r12-amb"),
         ]),
    dict(id="pereti", n="04", nume="Pereți & plinte", titlu="Proporție,<br><em>ritm, liniște.</em>",
         text="Brâuri pentru chenare, profile de perete și plinte înalte. Arhitectura discretă care face o cameră să pară gândită de un designer.",
         amb="hol-arc", know="Chenarele arată cel mai bine când distanța dintre ele e egală cu distanța până la colțul peretelui.",
         produse=[
            P(id="wo2", brand="Wallstyl®", name="Brâu WO2 pentru chenare", spec="38 × 18 × 2000 mm", url="brau-decorativwo2-wallstyl", img="wo2", hover="wo2-amb", tag="Accesibil"),
            P(id="z1360", brand="Arstyl®", name="Brâu Z1360", spec="60 × 15 × 2000 mm", url="brau-z1360", img="z1360", hover="z1360-amb"),
            P(id="wl6", brand="Wallstyl®", name="Brâu WL6", spec="75 × 22 × 2000 mm", url="brau-decorativwl6-wallstyl", img="wl6", hover="wl6-amb"),
            P(id="fd3", brand="Wallstyl®", name="Plintă FD3", spec="100 × 20 × 2000 mm", url="plintafd3-wallstyl", img="fd3"),
            P(id="fd21", brand="Wallstyl®", name="Plintă FD21", spec="130 × 20 × 2000 mm", url="plintafd21-wallstyl", img="fd21", hover="fd21-amb"),
         ]),
    dict(id="riflaje", n="05", nume="Riflaje", titlu="Textura lemnului,<br><em>liniștea unui studio.</em>",
         text="Panouri acustice 3D cu aspect de stejar: absorb ecoul și încălzesc vizual spațiul. Ușoare, pentru perete și tavan.",
         amb="hol-riflaj", know="Un singur perete cu riflaj, pus în spatele televizorului sau al patului, e suficient ca să schimbe acustica și caracterul camerei.",
         produse=[
            P(id="rif-deschis", brand="NMC®", name="Riflaj acustic · stejar deschis", spec="565 × 2600 × 19 mm", url="riflaj-acustic-panou-3d-stejar-deschis", img="rif-deschis"),
            P(id="rif-inchis", brand="NMC®", name="Riflaj acustic · stejar închis", spec="565 × 2600 × 19 mm", url="riflaj-acustic-panou-3d-stejar-inchis", img="rif-inchis"),
         ]),
    dict(id="tapet", n="06", nume="Tapet", titlu="Marmură, mătase,<br><em>semnătură de designer.</em>",
         text="Tapet premium Carrara Best cu efect de marmură și colecția Roberto Cavalli. Modele aflate în stoc, pentru pereți care nu mai sunt doar fundal.",
         amb="living-dark", know="Tapetul cu efect de marmură arată cel mai natural pe peretele principal, nu pe toți pereții camerei.",
         produse=[
            P(id="c82603", brand="Carrara Best", name="Tapet Carrara Best 82603", spec="Efect de marmură · rolă", url="tapet-carrara-82603", img="c82603", hover="c82603-amb"),
            P(id="c82671", brand="Carrara Best", name="Tapet Carrara Best 82671", spec="Efect de marmură · rolă", url="tapet-carrara-82671", img="c82671", hover="c82671-amb"),
            P(id="rc19070", brand="Roberto Cavalli", name="Tapet Roberto Cavalli 19070", spec="Colecția 8 · rolă", url="tapet-roberto-cavalli-8-19070", img="rc19070", hover="rc19070-amb"),
         ]),
    dict(id="fatada", n="07", nume="Fațadă", titlu="Prima impresie,<br><em>pentru ani buni.</em>",
         text="Ancadramente, colțare și ornamente 3D ADRo® pentru exterior: rezistente la UV, ploaie și îngheț, gata de vopsit în orice culoare.",
         amb="ext-arcade", know="Ancadramentele pun în valoare ferestrele doar dacă au aceeași lățime pe toată fațada.",
         produse=[
            P(id="na105", brand="ADRo®", name="Ancadrament NA105", spec="175 × 40 × 2000 mm", url="ancadrament-decorativ-na105", img="na105", hover="na105-amb"),
            P(id="ncl106", brand="ADRo®", name="Colțar NCL106", spec="250/250 × 30 × 1000 mm", url="coltar-exterior-decorativ-polistiren-ncl106-250-250x30x1000", img="ncl106"),
            P(id="a113", brand="ADRo®", name="Ornament 3D A113", spec="1850 × 891 × 65 mm", url="accent-3d-a113-1850x891x65", img="a113"),
         ]),
]

SERVICII = [
    ("Consultanță premium", "Îți spunem ce profil, ce finisaj și ce culoare se potrivesc spațiului tău.", "consultanta-premium"),
    ("Randare 3D", "Vezi camera sau fațada înainte de montaj, cu produsele alese.", "randare-3d"),
    ("Produse personalizate", "Profile și decoruri realizate pe măsura proiectului.", "produse-personalizate"),
]

BLOG = [
    ("led-olive", "Cornișa LED: iluminat indirect și eleganță", "blog/cornisa-led-iluminat-indirect-eleganta-interior"),
    ("perete-alb", "Chenare decorative: modele, dimensiuni, proporții", "blog/chenare-decorative-perete-modele-dimensiuni-proportii"),
    ("living-nude", "Profile decorative pentru pereți și tavan", "blog/profile-decorative-pereti-tavan-2026"),
    ("ext-vila", "Cele mai frumoase fațade de case", "blog/cele-mai-frumoase-fatade-de-case"),
]

ICO = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "cart": '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6.2"/><circle cx="10" cy="20.5" r="1.3"/><circle cx="18" cy="20.5" r="1.3"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19 13 11"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
}
ico = lambda k, s=20: f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICO[k]}</svg>'
href = lambda slug: SITE + quote(slug.strip(), safe="/-")
A = lambda n: f"assets/{n}.jpg"


def card(p, cap):
    u = href(p["url"])
    hover = f'<img class="pc__hover" src="{A(p["hover"])}" alt="" loading="lazy">' if p.get("hover") else ""
    tag = f'<span class="pc__tag">{e(p["tag"])}</span>' if p.get("tag") else ""
    s = " ".join([p["name"], p["spec"], p["brand"], cap["nume"], p["id"]]).lower()
    return f'''<article class="pc" data-url="{u}" data-search="{e(s)}">
  <a class="pc__img" href="{u}" aria-label="{e(p["name"])}"><img src="{A(p["img"])}" alt="{e(p["name"])}" loading="lazy" width="720" height="720">{hover}</a>{tag}
  <div class="pc__body">
    <span class="pc__brand">{e(p["brand"])}</span>
    <h3 class="pc__name"><a href="{u}">{e(p["name"])}</a></h3>
    <p class="pc__spec">{e(p["spec"])}</p>
    <p class="stock" data-stock><i></i>În stoc · livrare rapidă</p>
    <div class="pc__actions"><a class="btn btn--line" href="{u}">Descoperă {ico("arrow", 14)}</a></div>
  </div>
</article>'''


def chapter(c, i):
    flip = " chapter--flip" if i % 2 else ""
    return f'''<section class="chapter{flip}" id="{c["id"]}">
  <div class="wrap">
    <div class="chapter__head">
      <div class="chapter__media">
        <div class="arch"><img src="{A(c["amb"])}" alt="" loading="lazy"></div>
        <span class="chapter__num" aria-hidden="true">{c["n"]}</span>
      </div>
      <div class="chapter__copy">
        <span class="label"><b>{c["n"]}</b> / 07 · {e(c["nume"])}</span>
        <h2>{c["titlu"]}</h2>
        <p>{e(c["text"])}</p>
        <div class="knowhow">{ico("spark", 18)}<div><small>Know-how Deco&amp;Flair</small>{e(c["know"])}</div></div>
      </div>
    </div>
    <div class="rail" data-rail>
      <div class="rail__track">{"".join(card(p, c) for p in c["produse"])}</div>
    </div>
  </div>
</section>'''


def page():
    C = CAMPANIE
    n = sum(len(c["produse"]) for c in CAPITOLE)
    marquee = "".join(f"<span>{e(b)}</span>" for b in BRANDURI * 3)
    toc = "".join(f'<a href="#{c["id"]}"><b>{c["n"]}</b>{e(c["nume"])}</a>' for c in CAPITOLE)
    nav = "".join(f'<a href="#{c["id"]}">{e(c["nume"])}</a>' for c in CAPITOLE)
    serv = "".join(f'<a class="svc" href="{SITE}{u}"><span class="svc__n">0{i+1}</span><b>{e(t)}</b><span>{e(d)}</span><em>Află mai mult {ico("arrow", 14)}</em></a>' for i, (t, d, u) in enumerate(SERVICII))
    blog = "".join(f'<a class="post" href="{href(u)}"><span class="post__img"><img src="{A(img)}" alt="" loading="lazy"></span><b>{e(t)}</b><em>Citește în jurnal {ico("arrow", 14)}</em></a>' for img, t, u in BLOG)
    chapters = "".join(chapter(c, i) for i, c in enumerate(CAPITOLE))
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Selecția Premium 2027 · Deco&amp;Flair — design premium, accesibil</title>
<meta name="description" content="Selecția Premium Deco&amp;Flair: profile decorative cu LED, panouri 3D, cornișe, rozete, riflaje acustice, tapet de designer și elemente de fațadă. Know-how, inovație și prețuri speciale în noiembrie.">
<meta name="theme-color" content="#F4EEE6">
<meta property="og:title" content="Selecția Premium 2027 · Deco&amp;Flair">
<meta property="og:description" content="Lux liniștit, accesibil. Produse premium alese cu know-how.">
<meta property="og:image" content="assets/hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="df.css">
</head>
<body>
<a class="skip" href="#lumina">Sari la produse</a>
<div class="aura" aria-hidden="true"><i class="a1"></i><i class="a2"></i><i class="a3"></i></div>

<div class="topline" data-campaign><span>{e(C["eticheta"])}</span><span class="dot"></span><span>Prețuri speciale până pe {C["sfarsit_text"]}</span><span class="dot"></span><span class="topline__cd">Încă <b data-cd-mini>--</b></span></div>

<header class="hdr">
  <div class="wrap hdr__row">
    <a class="logo" href="{SITE}" aria-label="Deco&amp;Flair"><img src="assets/logo-ink.png" alt="Deco&amp;Flair" width="120" height="46"></a>
    <nav class="nav" aria-label="Capitole">{nav}</nav>
    <label class="search"><span class="sr-only">Caută în selecție</span>{ico("search", 16)}<input id="df-q" type="search" placeholder="Caută: LED, wave, cornișă…" autocomplete="off"></label>
    <a class="hdr__cart" href="{SITE}cos-cumparaturi" aria-label="Coș">{ico("cart", 18)}<b id="df-cart" hidden>0</b></a>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <span class="label"><b>Deco&amp;Flair</b> · Selecția Premium 2027</span>
      <h1>Lux liniștit.<br><em>Pentru fiecare casă.</em></h1>
      <p class="hero__lead">Profile decorative, panouri 3D, lumină indirectă și tapet de designer, alese cu know-how de la producători de renume. Design premium, la prețuri accesibile.</p>
      <div class="hero__cta">
        <a class="btn btn--ink" href="#lumina">Explorează selecția {ico("arrow", 16)}</a>
        <a class="btn btn--ghost" href="#servicii">Consultanță premium</a>
      </div>
      <div class="hero__meta" data-campaign>
        <span class="pill"><i></i>{e(C["eticheta"])}</span>
        <span class="hero__cd" role="timer" data-cd="{C["sfarsit"]}"><span><b data-d>--</b>zile</span><span><b data-h>--</b>ore</span><span><b data-m>--</b>min</span></span>
      </div>
    </div>
    <div class="hero__visual">
      <div class="arch arch--hero"><img src="{A("hero")}" alt="Perete cu panouri 3D WAVE într-un dining luminos" fetchpriority="high"></div>
      <div class="ring" aria-hidden="true"></div>
      <div class="glass glass--a"><small>Inovație</small><b>Panouri 3D &amp; LED</b></div>
      <div class="glass glass--b"><small>{n} produse</small><b>în stoc acum</b></div>
      <span class="vert" aria-hidden="true">Elevate your space · Define your style</span>
    </div>
  </div>
</section>

<div class="brands" aria-label="Branduri"><div class="brands__track">{marquee}</div></div>

<section class="pillars">
  <div class="wrap">
    <p class="manifesto">Nu suntem doar un magazin. Suntem <em>curatori de tendințe</em>: alegem fiecare produs pentru calitate, durabilitate și acel <em>„wow”</em> pe care îl simți când intri în cameră.</p>
    <div class="pillars__row">
      <div class="pillar"><span>{ico("spark", 22)}</span><b>Premium</b><p>Producători de renume internațional: Arstyl®, Wallstyl®, Nomastyl®, ADRo®, Carrara Best, Roberto Cavalli.</p></div>
      <div class="pillar"><span>{ico("leaf", 22)}</span><b>Inovație</b><p>Lumină integrată, texturi 3D, riflaje acustice. Materiale ușoare, rezistente, gata de vopsit.</p></div>
      <div class="pillar"><span>{ico("eye", 22)}</span><b>Know-how</b><p>Îți recomandăm produsul, finisajul, culoarea și montajul potrivit, nu doar un cod din catalog.</p></div>
    </div>
    <nav class="toc" aria-label="Cuprins">{toc}</nav>
  </div>
</section>

<p class="wrap searchinfo" id="df-status" role="status" aria-live="polite"></p>
{chapters}

<section class="services" id="servicii">
  <div class="wrap">
    <div class="sec-head"><span class="label"><b>Servicii</b> · incluse în experiența Deco&amp;Flair</span><h2>Nu știi de unde să începi?<br><em>Începe cu noi.</em></h2></div>
    <div class="svc__row">{serv}</div>
    <div class="contact">
      <div class="arch arch--small"><img src="{A("consultanta")}" alt="" loading="lazy"></div>
      <div>
        <span class="label"><b>Consultanță</b> · {e(C["program"])}</span>
        <p class="contact__big"><a href="{C["telefon_link"]}">{C["telefon"]}</a></p>
        <p><a href="mailto:{C["email"]}">{C["email"]}</a> · <a href="{C["instagram"]}">@decoflairhub</a></p>
      </div>
    </div>
  </div>
</section>

<section class="journal" id="jurnal">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><span class="label"><b>Jurnal</b> · idei din blog</span><h2>Inspirație,<br><em>înainte de comandă.</em></h2></div><a class="link" href="{SITE}blog">Toate articolele {ico("arrow", 14)}</a></div>
    <div class="posts">{blog}</div>
  </div>
</section>

<section class="faq" id="intrebari">
  <div class="wrap faq__grid">
    <div><span class="label"><b>FAQ</b></span><h2>Bine de<br><em>știut.</em></h2></div>
    <div>
      <details><summary>Sunt produsele cu adevărat accesibile?</summary><p>Da. Selecția acoperă de la brâuri și plinte pentru orice buget până la piese statement. În noiembrie, produsele din campanie au prețuri speciale, afișate pe pagina fiecărui produs.</p></details>
      <details><summary>Cât de repede primesc comanda?</summary><p>Produsele din această selecție sunt în stoc. Disponibilitatea apare pe pagina fiecărui produs; costul și termenul de livrare se văd în coș.</p></details>
      <details><summary>Se pot vopsi profilele și panourile 3D?</summary><p>Da. Profilele din poliuretan și polimer dur sunt preamorsate sau gata de vopsit, iar elementele de exterior ADRo® se vopsesc cu vopsea acrilică de exterior.</p></details>
      <details><summary>Mă ajutați să aleg și să calculez necesarul?</summary><p>Da. Sună la <a href="{C["telefon_link"]}">{C["telefon"]}</a> ({e(C["program"])}) sau scrie la <a href="mailto:{C["email"]}">{C["email"]}</a>. Pentru proiecte mari oferim și randare 3D.</p></details>
    </div>
  </div>
</section>

<section class="closing">
  <div class="wrap closing__in">
    <span class="label"><b>Deco&amp;Flair</b></span>
    <h2>Elevate your space.<br><em>Define your style.</em></h2>
    <p data-campaign>Prețuri speciale până pe {C["sfarsit_text"]}, în limita stocului disponibil.</p>
    <a class="btn btn--ink" href="#lumina">Începe cu lumina {ico("arrow", 16)}</a>
  </div>
</section>
</main>

<footer class="ftr"><div class="wrap ftr__row"><img src="assets/logo-ink.png" alt="Deco&amp;Flair" width="96" height="37"><p>Prețul, stocul și condițiile de livrare se confirmă pe pagina fiecărui produs. Imaginile ambientale sunt orientative.</p><a href="{SITE}">decoflair.ro {ico("arrow", 14)}</a></div></footer>

<div class="mbar"><a class="btn btn--ink" href="#lumina">Explorează selecția</a><a class="btn btn--ghost" href="{C["telefon_link"]}" aria-label="Sună">{ico("phone", 18)}</a></div>
<div class="toast" id="df-toast" role="status" aria-live="polite"></div>
<script src="df.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    for c in CAPITOLE:
        assert (ROOT / A(c["amb"])).exists(), c["amb"]
        for p in c["produse"]:
            for k in ("img", "hover"):
                if p.get(k):
                    assert (ROOT / A(p[k])).exists(), A(p[k])
    for img, *_ in BLOG:
        assert (ROOT / A(img)).exists(), img
    html = page()
    assert " lei" not in html.lower(), "Fără prețuri pe pagină"
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("OK", ROOT / "index.html", sum(len(c["produse"]) for c in CAPITOLE), "produse")

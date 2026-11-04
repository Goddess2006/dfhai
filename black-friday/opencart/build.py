#!/usr/bin/env python3
"""Generează varianta pentru OpenCart 3 a landing page-ului Black Friday.

Sursa: black-friday/index.html (pagina completă, independentă).
Rezultat: black-friday/opencart/descriere-pagina-informatii.html — codul care
se lipește în Catalog > Informații > Descriere (modul Cod sursă).

Ce schimbă față de pagina independentă:
  * scoate <html>, <head>, <body>, <title>, meta (le dă OpenCart);
  * izolează tot CSS-ul sub #nmc-bf, ca să nu afecteze tema și ca tema
    (Bootstrap 3) să nu strice landing-ul;
  * elimină antetul propriu al landing-ului (site-ul are deja antet) și mută
    căutarea în bara de categorii;
  * redenumește ID-urile care se bat cu OpenCart (ex. #top) și pune JS-ul
    într-o funcție izolată;
  * schimbă căile imaginilor din assets/ în /image/catalog/black-friday/.

Rulare:  python3 black-friday/opencart/build.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "index.html"
OUT = HERE / "descriere-pagina-informatii.html"
IMG_PREFIX = "/image/catalog/black-friday/"
ROOT = "#nmc-bf#nmc-bf"  # id dublat = specificitate mare, câștigă în fața temei

html = SRC.read_text(encoding="utf-8")

# ---------------------------------------------------------------- CSS
css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
css = re.sub(r"(?<![\w-])footer(?![\w-])", ".bf-foot", css)


def split_top(s):
    """Împarte un selector după virgule, ignorând virgulele din paranteze."""
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def scope_selector(sel):
    if sel in (":root", "html", "body"):
        return ROOT
    if sel.startswith("*"):
        return f"{ROOT} {sel}"
    return f"{ROOT} {sel}"


def scope(block):
    res, i, n = [], 0, len(block)
    while i < n:
        j = block.find("{", i)
        if j == -1:
            break
        head = block[i:j].strip()
        # găsește acolada de închidere potrivită
        depth, k = 1, j + 1
        while depth and k < n:
            if block[k] == "{":
                depth += 1
            elif block[k] == "}":
                depth -= 1
            k += 1
        body = block[j + 1:k - 1]
        if head.startswith("@keyframes") or head.startswith("@font-face"):
            res.append(f"{head}{{{body}}}")
        elif head.startswith("@"):
            res.append(f"{head}{{{scope(body)}}}")
        else:
            sels = ",".join(scope_selector(s) for s in split_top(head))
            res.append(f"{sels}{{{body.strip()}}}")
        i = k
    return "\n".join(res)


scoped = scope(css)
# overflow-x:hidden pe wrapper ar opri bara sticky; clip nu o oprește
scoped = scoped.replace("overflow-x:hidden", "overflow-x:clip")

R = ROOT
compat = f"""
/* ---- integrare OpenCart 3 / Bootstrap 3 ---- */
body{{overflow-x:hidden}}
#information-information #content > h1:first-of-type{{display:none}}
{R} h1,{R} h2,{R} h3{{font-family:inherit; color:inherit; font-weight:inherit; letter-spacing:inherit}}
{R} p{{margin:1em 0}}
{R} a,{R} a:hover,{R} a:focus{{text-decoration:none}}
{R} label{{display:block; margin:0; font-weight:inherit; max-width:none}}
{R} .badge{{padding:0; min-width:0; white-space:normal; vertical-align:baseline}}
{R} .btn{{border:0; white-space:nowrap; line-height:1; margin:0; text-shadow:none}}
{R} [hidden]{{display:none!important}}
{R} img{{vertical-align:middle; height:auto}}
"""
after = f"""
/* ---- landing pe toată lățimea ecranului, chiar dacă e în .container ---- */
{R}{{display:block; position:relative; width:100vw; max-width:100vw; margin:0 calc(50% - 50vw)}}
body:has(#nmc-bf) footer{{margin-top:0}}
body:has(#nmc-bf) #content{{padding-bottom:0; min-height:0}}
/* ---- ajustări după mutarea căutării în bara de categorii ---- */
{R} .catnav{{top:0}}
{R} .catnav__row{{align-items:center}}
{R} .catnav .search{{flex:0 1 240px; min-width:180px; margin-left:auto; max-width:none}}
{R} .catnav .search input{{height:38px}}

"""
css_out = compat + "\n" + scoped + "\n" + after

# ---------------------------------------------------------------- HTML
body = re.search(r"<body>(.*?)<script>", html, re.S).group(1)
script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
fonts = re.findall(r'<link[^>]+fonts\.googleapis[^>]+css2[^>]*>', html)[0]

# 1) antetul propriu iese, căutarea trece în bara de categorii
search = re.search(r'<label class="search">.*?</label>', body, re.S).group(0)
body = re.sub(r"<!-- =+ HEADER =+ -->\s*<header.*?</header>", "", body, flags=re.S)
body = body.replace('<div class="wrap catnav__row" id="catnav">',
                    '<div class="wrap catnav__row" id="nmc-bf-catnav">')
body = re.sub(r'(<div class="wrap catnav__row" id="nmc-bf-catnav">.*?)(</div>\s*</nav>)',
              lambda m: m.group(1) + search + m.group(2), body, count=1, flags=re.S)

# 2) ID-uri care se bat cu OpenCart / tema
body = body.replace('<main id="top">', '<div class="bf-main">').replace("</main>", "</div>")
for old in ["q", "ticker", "searchStatus", "domains", "stats", "starsGrid", "bundle", "categories", "heroMax"]:
    body = body.replace(f'id="{old}"', f'id="nmc-bf-{old}"')
    script = script.replace(f"getElementById('{old}')", f"getElementById('nmc-bf-{old}')")
body = body.replace('<label class="search">', '<label class="search" for="nmc-bf-q">')

# 3) footer -> div (tema OpenCart stilizează <footer>)
body = re.sub(r"<footer>(.*?)</footer>", r'<div class="bf-foot">\1</div>', body, flags=re.S)

# 4) ticker static (merge și dacă editorul elimină scriptul)
items = ["Black Friday · NMC România", "Profile exterior", "Profile interior", "Tapet de designer", "Adeziv exterior"]
ticker = "".join(f"<span>{t}</span>" for t in items * 4)
body = body.replace('<div class="ticker__track" id="nmc-bf-ticker"></div>',
                    f'<div class="ticker__track" id="nmc-bf-ticker">{ticker}</div>')
script = re.sub(r"const ticker = .*?join\(''\);\s*", "", script, flags=re.S)

# 5) imagini
body = body.replace('src="assets/', f'src="{IMG_PREFIX}')

# 6) JS izolat, limitat la landing
script = script.replace("document.querySelectorAll(", "root.querySelectorAll(")
script = script.replace("'#categories ", "'#nmc-bf-categories ")
script = "(function(){\nvar root = document.getElementById('nmc-bf'); if (!root) return;\n" + script.strip() + "\n})();"

body = re.sub(r"\n{3,}", "\n\n", body.strip())

out = f"""<!-- ===== NMC România · Black Friday · landing pentru OpenCart 3 =====
     Generat automat din black-friday/index.html de black-friday/opencart/build.py.
     Se lipește în Catalog > Informații > Descriere, în modul Cod sursă (</>).
     Imaginile se încarcă în image/catalog/black-friday/ (Image Manager > folder „black-friday”). -->
{fonts}
<style>
{css_out}
</style>
<div id="nmc-bf" class="nmc-bf">
{body}
</div>
<script>
{script}
</script>
"""
OUT.write_text(out, encoding="utf-8")
print(f"OK -> {OUT.relative_to(HERE.parent.parent)} ({len(out):,} caractere)")

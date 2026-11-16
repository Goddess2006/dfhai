"""Actualizeaza catalogul (cod, pret, UM) de pe nmcromania.ro -> data/catalog.json.
Rulare: python3 tools/scrape.py   (descarca ~560 pagini de produs, 8 in paralel)"""
import re, html, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
UA = {'User-Agent': 'Mozilla/5.0'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf8', 'ignore')
def clean(x): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).strip()
def num(x): return float(x.replace(',', '').strip()) if x else None
def parse(url, s):
    i = s.find('<h1 class="title page-title">')
    if i < 0: return None
    b = s[i:]
    name = clean(re.search(r'<h1[^>]*>(.*?)</h1>', b, re.S).group(1))
    m = re.search(r'product-model"><b>Model:</b>\s*<span>(.*?)</span>', b, re.S)
    pn = re.search(r'class="product-price-new">([\d.,]+)', b)
    po = re.search(r'class="product-price-old">([\d.,]+)', b)
    p = re.search(r'class="product-price">([\d.,]+)', b)
    tax = re.search(r'class="product-tax">Fără TVA:\s*([\d.,]+)', b)
    price = num(pn.group(1)) if pn else (num(p.group(1)) if p else None)
    if not m or price is None: return None
    st = re.search(r'product-stock ([\w-]+)"><b>.*?</b>\s*<span>(.*?)</span>', b, re.S)
    um = re.search(r'Unitate de masura\s*</td>\s*<td>(.*?)</td>', b, re.S)
    j = s.find('class="breadcrumb"')
    bc = [clean(x) for x in re.findall(r'<a[^>]*>(.*?)</a>', s[j:j + 3000], re.S)]
    bc = [x for x in bc if x and x != name]
    cat = bc[1] if len(bc) > 1 and bc[0] in ('Profile decorative exterior', 'Profile decorative interior') else (bc[0] if bc else '')
    cat = re.split(r' – | \| ', cat)[0].strip()
    if cat == 'Noutati': cat = 'Noutăți'
    if cat in ('', 'Profile decorative interior', 'Profile decorative exterior'):
        cat = 'Cornisa decorativa interior' if 'ornis' in name else 'Altele'
    u = (um.group(1) if um else '').strip()
    u = clean(u).lower().replace('bucată', 'buc').replace('bucata', 'buc').replace('x/ ', '')
    u = re.sub(r'\s*/\s*', ' / ', u) or 'buc'
    return dict(c=clean(m.group(1)), n=name, p=price, o=num(po.group(1)) if po else None,
                f=num(tax.group(1)) if tax else round(price / 1.21, 2), u=u, k=cat,
                s=(st.group(1) == 'in-stock') if st else None, l=url.replace('https://www.nmcromania.ro/', ''))
def one(url):
    try: return parse(url, get(url))
    except Exception as e: print('ERR', url, e, file=sys.stderr)
if __name__ == '__main__':
    urls = []
    for n in (1, 2):
        urls += re.findall(r'<url>\s*<loc><!\[CDATA\[(https://www.nmcromania.ro/[^\]]+)\]\]>', get(f'https://www.nmcromania.ro/sitemap-product-{n}.xml'))
    with ThreadPoolExecutor(8) as ex: items = [x for x in ex.map(one, sorted(set(urls))) if x]
    seen, out = set(), []
    for x in sorted(items, key=lambda x: (x['k'], x['c'])):
        key = (x['c'], x['n'])
        if key not in seen: seen.add(key); out.append(x)
    json.dump(out, open(os.path.join(ROOT, 'data', 'catalog.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'produse')

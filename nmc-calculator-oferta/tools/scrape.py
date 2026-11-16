"""Actualizeaza catalogul (cod, pret, UM) de pe nmcromania.ro sau decoflair.ro.
Rulare: python3 tools/scrape.py nmc      -> data/catalog.json
        python3 tools/scrape.py decoflair -> data/catalog-decoflair.json
Optional: --pages DIR  (parseaza pagini HTML deja descarcate, fara retea)"""
import re, html, json, os, sys, glob, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
UA = {'User-Agent': 'Mozilla/5.0'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = {
    'nmc': dict(base='https://www.nmcromania.ro/', out='catalog.json', ro_num=False),
    'decoflair': dict(base='https://decoflair.ro/', out='catalog-decoflair.json', ro_num=True),
}
TOP = ('Profile decorative exterior', 'Profile decorative interior')
def get(u):
    for a in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf8', 'ignore')
        except Exception:
            if a == 3: raise
            time.sleep(2 + 3 * a)
def clean(x): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).strip()
def num(x, ro):
    if not x: return None
    x = x.strip()
    x = x.replace('.', '').replace(',', '.') if ro else x.replace(',', '')
    return float(x)
def parse(url, s, cfg):
    ro = cfg['ro_num']
    i = s.find('<h1 class="title page-title')
    if i < 0: return None
    b = s[i:]
    name = clean(re.search(r'<h1[^>]*>(.*?)</h1>', b, re.S).group(1))
    m = re.search(r'product-model"><b>(?:Model|Cod produs):</b>\s*<span>(.*?)</span>', s, re.S)
    N = r'([\d.,]+)'
    pn = re.search(r'class="product-price-new">' + N, b)
    po = re.search(r'class="product-price-old">' + N, b)
    p = re.search(r'class="product-price">' + N, b)
    tax = re.search(r'class="product-tax">F(?:ă|a)r(?:ă|a) TVA:\s*' + N, b)
    price = num(pn.group(1), ro) if pn else (num(p.group(1), ro) if p else None)
    if not m or not price: return None
    st = re.search(r'product-stock ([\w-]+)"><b>.*?</b>\s*<span>(.*?)</span>', s, re.S)
    um = re.search(r'Unitate de masura\s*</td>\s*<td>(.*?)</td>', b, re.S)
    j = s.find('class="breadcrumb"')
    bc = [clean(x) for x in re.findall(r'<a[^>]*>(.*?)</a>', s[j:j + 3000], re.S)]
    bc = [x for x in bc if x and x != name and x.lower() != 'home']
    cat = bc[1] if len(bc) > 1 and bc[0] in TOP else (bc[0] if bc else '')
    cat = re.split(r' – | \| ', cat)[0].strip()
    if cat == 'Noutati': cat = 'Noutăți'
    if cat in ('',) + TOP:
        cat = 'Cornisa decorativa interior' if 'ornis' in name else 'Altele'
    ln = name.lower()
    if ln.startswith('mostra tapet'): cat = 'Mostre tapet'
    elif ln.startswith('tapet') and cat != 'Tapet': cat = 'Tapet'
    elif cat == 'Altele' and 'coloan' in ln: cat = 'Coloane decorative'
    elif cat.startswith('Linea'): cat = 'Kituri amenajare'
    u = clean(um.group(1) if um else '').lower().replace('bucată', 'buc').replace('bucata', 'buc').replace('x/ ', '')
    u = re.sub(r'\s*/\s*', ' / ', u) or 'buc'
    return dict(c=clean(m.group(1)), n=name, p=price, o=num(po.group(1), ro) if po else None,
                f=num(tax.group(1), ro) if tax else round(price / 1.21, 2), u=u, k=cat,
                s=(st.group(1) == 'in-stock') if st else None, l=url.replace(cfg['base'], ''))
def finish(items, cfg):
    seen, out = set(), []
    for x in sorted(items, key=lambda x: (x['k'], x['c'])):
        key = (x['c'], x['n'])
        if key not in seen: seen.add(key); out.append(x)
    json.dump(out, open(os.path.join(ROOT, 'data', cfg['out']), 'w'), ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'produse ->', cfg['out'])
if __name__ == '__main__':
    site = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else 'nmc'
    cfg = SITES[site]
    if '--pages' in sys.argv:
        d = sys.argv[sys.argv.index('--pages') + 1]; items = []
        for f in glob.glob(os.path.join(d, '*.html')):
            s = open(f, encoding='utf8', errors='ignore').read()
            c = re.search(r'rel="canonical" href="([^"]+)"', s) or re.search(r'<link href="([^"]+)" rel="canonical"', s)
            x = parse(c.group(1) if c else cfg['base'] + os.path.basename(f)[:-5], s, cfg)
            if x: items.append(x)
        finish(items, cfg); sys.exit()
    urls = []
    for n in (1, 2, 3):
        try: urls += re.findall(r'<url>\s*<loc><!\[CDATA\[(' + re.escape(cfg['base']) + r'[^\]]+)\]\]>', get(f"{cfg['base']}sitemap-product-{n}.xml"))
        except Exception: pass
    def one(u):
        try: return parse(u, get(u), cfg)
        except Exception as e: print('ERR', u, e, file=sys.stderr)
    with ThreadPoolExecutor(4) as ex: finish([x for x in ex.map(one, sorted(set(urls))) if x], cfg)

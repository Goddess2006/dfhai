"""Extrage descrierea + meta (producator, EAN) de pe pagina fiecarui produs -> src/<COD>/descriere.txt (pentru verificarea continutului)."""
import re, json, os, html, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, 'data', 'produse.json')))
def txt(x):
    x = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', x, flags=re.S)
    x = re.sub(r'</(p|h\d|li|tr|div)>|<br\s*/?>', '\n', x)
    x = html.unescape(re.sub(r'<[^>]+>', ' ', x))
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t]+', ' ', x)).strip()
meta = {}
for c, p in P.items():
    s = urllib.request.urlopen(urllib.request.Request('https://decoflair.ro/' + p['l'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read().decode('utf8', 'ignore')
    md = re.search(r'name="description" content="([^"]*)"', s)
    ean = re.search(r'EAN:</b>\s*<span>([^<]*)', s) or re.search(r'"gtin13":"(\d+)"', s)
    man = re.search(r'Producator:</b>\s*<span>.*?>([^<]+)</a>', s, re.S) or re.search(r'"manufacturer":"([^"]+)"', s)
    lines = [m.start() for m in re.finditer(r'data-start="\d+"', s)]
    body = txt(s[max(0, lines[0] - 400): lines[-1] + 2000]) if lines else ''
    if not body:
        i = s.find('id="tab-description"'); body = txt(s[i:i + 15000]) if i > 0 else ''
    meta[c] = dict(ean=(ean.group(1).strip() if ean else ''), producator=(man.group(1).strip() if man else ''), meta=html.unescape(md.group(1)) if md else '')
    open(os.path.join(ROOT, 'src', c, 'descriere.txt'), 'w').write(f"META: {meta[c]}\n\n{body[:8000]}")
    print(c, meta[c]['ean'], meta[c]['producator'], len(body))
json.dump(meta, open(os.path.join(ROOT, 'data', 'meta-site.json'), 'w'), ensure_ascii=False, indent=1)

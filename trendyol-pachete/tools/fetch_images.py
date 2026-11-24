"""Descarca galeria (imaginile 1600x1600) de pe pagina fiecarui produs decoflair.ro.
Rulare: python3 tools/fetch_images.py  -> src/<COD>/NN.jpg + src/<COD>/page.json"""
import re, json, os, sys, urllib.request, html
UA = {'User-Agent': 'Mozilla/5.0'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get(u, binary=False):
    d = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return d if binary else d.decode('utf8', 'ignore')
def main():
    prods = json.load(open(os.path.join(ROOT, 'data', 'produse.json')))
    for code, p in prods.items():
        out = os.path.join(ROOT, 'src', code.replace(' ', '_'))
        os.makedirs(out, exist_ok=True)
        s = get('https://decoflair.ro/' + p['l'])
        imgs = []
        for u in re.findall(r'https://decoflair.ro/image/cache/catalog/[^" ]+?-1600x1600h?w?\.(?:jpg|png|webp)', s):
            if u not in imgs: imgs.append(u)
        if not imgs:
            m = re.search(r'og:image" content="([^"]+)"', s)
            if m: imgs = [m.group(1)]
        desc = ''
        m = re.search(r'<div[^>]+(?:id|class)="[^"]*(?:tab-description|product_tabs-description|block-description)[^"]*"[^>]*>(.*?)</div>\s*</div>', s, re.S)
        if m: desc = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1)))).strip()
        files = []
        for i, u in enumerate(imgs[:6]):
            ext = u.rsplit('.', 1)[1]
            f = os.path.join(out, f'{i+1:02d}.{ext}')
            open(f, 'wb').write(get(u.replace(' ', '%20'), True)); files.append(os.path.basename(f))
        json.dump({'url': 'https://decoflair.ro/' + p['l'], 'images': imgs[:6], 'files': files, 'desc': desc[:4000]},
                  open(os.path.join(out, 'page.json'), 'w'), ensure_ascii=False, indent=1)
        print(code, len(files), len(desc))
if __name__ == '__main__': main()

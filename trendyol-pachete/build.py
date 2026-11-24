"""Pachete Deco&Flair pentru Trendyol: calcul pret + HTML pentru imagini (1200x1800) + fisa de listare.
Rulare: python3 tools/fetch_prices.py && python3 tools/fetch_images.py && python3 build.py && node render.cjs"""
import json, os, csv, math, html, shutil
from PIL import Image
import ambient as amb

ROOT = os.path.dirname(os.path.abspath(__file__))
TRANSPORT = 200.00
W, H = 1200, 1800
P = json.load(open(os.path.join(ROOT, 'data', 'produse.json')))
PK = json.load(open(os.path.join(ROOT, 'data', 'pachete.json')))

INFO = {  # dimensiuni / material, din denumirile de pe decoflair.ro
 'Z11': dict(dim='148 × 69 mm', L='2 m', mat='Poliuretan', sec='src/Z11/02.jpg', hero='src/Z11/01.jpg', short='Cornișă Z11'),
 'FD3': dict(dim='100 × 20 mm', L='2 m', mat='Polimer dur', sec='src/FD3/02.jpg', hero='src/FD3/01.jpg', short='Plintă FD3'),
 'WL1': dict(dim='38 × 18 mm', L='2 m', mat='Polimer dur', sec='src/WL1/02.jpg', hero='src/WL1/01.jpg', short='Brâu WL1'),
 'IL13': dict(dim='80 × 52 mm', L='2 m', mat='Polimer dur', sec=None, hero='src/IL13/01.jpg', short='Cornișă LED IL13'),
 'NCL107': dict(dim='300/300 × 30 mm', L='1 m', mat='Polistiren acoperit cu rășină și cuarț', sec='src/NCL107/02.jpg', hero='src/NCL107/01.jpg', short='Colțar NCL107'),
 'NA105': dict(dim='175 × 40 mm', L='2 m', mat='Polistiren acoperit cu rășină și cuarț', sec='src/NA105/02.jpg', hero='src/NA105/03.jpg', short='Ancadrament NA105'),
 'NC104': dict(dim='220 × 80 mm', L='2 m', mat='Polistiren acoperit cu rășină și cuarț', sec='src/NC104/02.jpg', hero='src/NC104/01.jpg', short='Cornișă NC104'),
 'REMA1': dict(dim='140 × 30 mm', L='2 m', mat='Polistiren acoperit cu rășină și cuarț', sec='src/REMA1/02.jpg', hero='src/REMA1/01.jpg', short='Brâu REMA1'),
 'Adro-Quartz1.5': dict(dim='1,5 kg', L='', mat='Rășină de chituire', sec=None, hero='src/Adro-Quartz1.5/01.jpg', short='Rășină ADRO-QUARTZ 1,5 kg'),
 'Adro-Fix4': dict(dim='4 kg', L='', mat='Adeziv de montaj', sec=None, hero='src/Adro-Fix4/01.jpg', short='Adeziv ADRO-FIX 4 kg'),
}

def ro(x):  # 1234.5 -> 1.234,50
    return f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def price(pk):
    lines = []
    for it in pk['items']:
        p = P[it['c']]
        lines.append(dict(c=it['c'], n=p['n'], q=it['q'], pu=p['regular'], tot=round(p['regular'] * it['q'], 2),
                          url='https://decoflair.ro/' + p['l'], stoc=p['s'], oferta=p['p'] if p['o'] else None))
    prod = round(sum(l['tot'] for l in lines), 2)
    final = round(prod + TRANSPORT, 2)
    return lines, prod, final

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">')
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:1800px;overflow:hidden}
body{font-family:Jost,sans-serif;color:#1F3A2F;background:#FAF7F2;position:relative}
.serif,h1,.qq,.badge b{font-variant-numeric:lining-nums}
.serif{font-family:'Playfair Display',serif}
.eyebrow{font-size:26px;letter-spacing:.32em;text-transform:uppercase;font-weight:500;color:#7A5B22}
.gold{color:#7A5B22}
.full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,20,17,.0) 40%,rgba(15,20,17,.78) 100%)}
.shadeT{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,20,17,.62) 0%,rgba(15,20,17,0) 38%)}
.cap{position:absolute;left:70px;right:70px;bottom:90px;color:#fff}
.cap h1{font-family:'Playfair Display',serif;font-weight:500;font-size:84px;line-height:1.06;margin:18px 0 22px}
.cap p{font-size:36px;font-weight:300;line-height:1.35;max-width:960px}
.note{position:absolute;right:28px;bottom:22px;font-size:18px;color:rgba(255,255,255,.75);letter-spacing:.04em}
.chip{display:inline-block;border:1.5px solid currentColor;border-radius:99px;padding:10px 26px;font-size:24px;letter-spacing:.18em;text-transform:uppercase}
"""

def page(body, extra=''):
    return f'<!doctype html><html lang="ro"><head><meta charset="utf-8">{FONTS}<style>{CSS}{extra}</style></head><body>{body}</body></html>'

def rel(path):  # cale relativa de la build/<id>/ la fisierul sursa
    return os.path.relpath(os.path.join(ROOT, path), os.path.join(ROOT, 'build', 'x'))

def main_code(pk): return pk['items'][0]['c']

def qty_label(pk):
    it = pk['items'][0]; inf = INFO[it['c']]
    lab = pk.get('mlLabel') or f"{pk['ml']} ml"
    return f"{it['q']} bare × {inf['L']} = {lab}"

def cover(pk):
    it = pk['items'][0]; inf = INFO[it['c']]
    extra = pk['items'][1:]
    acc = ''
    if extra:
        e = INFO[extra[0]['c']]
        acc = f'''<div class="acc"><div class="plus">+</div><img src="{rel(e['hero'])}"><div class="accl">{extra[0]['q']} × {html.escape(e['short'])}</div></div>'''
    bars = ''.join('<i></i>' for _ in range(it['q']))
    body = f'''
<div class="top"><div class="eyebrow">{html.escape(pk['kit'])} · {'Interior' if pk['zona']=='interior' else 'Exterior'}</div></div>
<div class="hero"><img src="{rel(inf['hero'])}"></div>
<div class="badge"><b>{it['q']}</b><span>bucăți</span></div>
{acc}
<div class="foot">
  <div class="brand">{html.escape(pk['brand'])}</div>
  <h1 class="serif">{html.escape(pk['scurt'])}</h1>
  <div class="bars">{bars}</div>
  <div class="q">{html.escape(qty_label(pk))} · {html.escape(inf['dim'])}</div>
</div>'''
    css = """
.top{position:absolute;top:70px;left:0;right:0;text-align:center}
.hero{position:absolute;top:150px;left:70px;width:1060px;height:1060px;border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 30px 60px rgba(31,58,47,.14)}
.hero img{width:100%;height:100%;object-fit:cover}
.badge{position:absolute;top:110px;right:40px;width:230px;height:230px;border-radius:50%;background:#1F3A2F;color:#F4EEE4;display:flex;flex-direction:column;align-items:center;justify-content:center;border:6px solid #D6BC84;box-shadow:0 14px 30px rgba(0,0,0,.2)}
.badge b{font-family:'Playfair Display',serif;font-size:118px;line-height:.9;font-weight:600;color:#D6BC84}
.badge span{font-size:28px;letter-spacing:.2em;text-transform:uppercase;margin-top:6px}
.acc{position:absolute;top:900px;left:40px;display:flex;align-items:center;gap:0;background:#fff;border-radius:200px;padding:14px 34px 14px 14px;box-shadow:0 16px 36px rgba(0,0,0,.18);border:3px solid #D6BC84}
.acc img{width:230px;height:230px;object-fit:contain;border-radius:50%;background:#fff}
.acc .plus{position:absolute;left:-10px;top:-10px;width:70px;height:70px;border-radius:50%;background:#D6BC84;color:#1F3A2F;font-size:56px;font-weight:600;display:flex;align-items:center;justify-content:center;line-height:1}
.accl{font-size:34px;font-weight:500;max-width:330px;line-height:1.2;margin-left:12px}
.foot{position:absolute;left:70px;right:70px;top:1260px;text-align:center}
.brand{font-size:24px;letter-spacing:.3em;color:#7A5B22;text-transform:uppercase;font-weight:500}
.foot h1{font-size:86px;font-weight:500;line-height:1.08;margin:18px 0 28px}
.bars{display:flex;justify-content:center;gap:16px;margin-bottom:28px}
.bars i{display:block;width:70px;height:16px;border-radius:8px;background:linear-gradient(90deg,#D6BC84,#B8975A)}
.q{font-size:38px;font-weight:400;color:#2E5244}
"""
    return page(body, css)

def ambient(pk, img, title, sub, eyebrow, note=True):
    nt = '<div class="note">Imagine de prezentare</div>' if note and '/src/' not in '/' + img else ''
    body = f'''<img class="full" src="{rel(img)}"><div class="shade"></div>
<div class="cap"><div class="chip">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1><p>{html.escape(sub)}</p></div>{nt}'''
    css = '.full{object-position:center}'
    return page(body, css)

def caroiaj(pk):
    """Ilustratie: perete cu caroiaje din brau WL1 si tablouri in interiorul chenarelor."""
    def frame(x, y, w, h):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#F6F2EA" stroke-width="16"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#9FB2A5" stroke-width="2" transform="translate(5 5)"/>'
                f'<rect x="{x-8}" y="{y-8}" width="{w+16}" height="{h+16}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>')
    def art(x, y, w, h, c1, c2, c3):
        return (f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="{h+28}" fill="#C9A86A"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c1}"/>'
                f'<path d="M{x} {y+h*.68} Q{x+w*.3} {y+h*.5} {x+w*.55} {y+h*.64} T{x+w} {y+h*.58} V{y+h} H{x}Z" fill="{c2}"/>'
                f'<circle cx="{x+w*.7}" cy="{y+h*.3}" r="{w*.11}" fill="{c3}"/>'
                f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="{h+28}" fill="none" stroke="rgba(0,0,0,.18)" stroke-width="3"/>')
    svg = f'''<svg viewBox="0 0 1200 1300" width="1200" height="1300" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B6C4B5"/><stop offset="1" stop-color="#A3B3A3"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9A57A"/><stop offset="1" stop-color="#A9825A"/></linearGradient>
<radialGradient id="glow" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="1120" fill="url(#wall)"/><rect width="1200" height="1120" fill="url(#glow)"/>
<rect y="0" width="1200" height="34" fill="#EFEAE0"/>
{frame(70, 120, 300, 560)}{frame(450, 120, 300, 560)}{frame(830, 120, 300, 560)}
{frame(70, 790, 300, 230)}{frame(450, 790, 300, 230)}{frame(830, 790, 300, 230)}
<rect x="0" y="736" width="1200" height="16" fill="#F6F2EA"/><rect x="0" y="752" width="1200" height="3" fill="#8FA294"/>
{art(140, 230, 160, 210, '#E9D5CC', '#7C8F7E', '#D6BC84')}{art(500, 200, 200, 270, '#F4EEE4', '#4B6B5C', '#B42127')}{art(900, 230, 160, 210, '#DCCFBF', '#8C6F5A', '#F4EEE4')}
<rect x="0" y="1120" width="1200" height="180" fill="url(#floor)"/><rect x="0" y="1106" width="1200" height="20" fill="#F6F2EA"/>
<rect x="380" y="960" width="440" height="150" rx="6" fill="#6B4E37"/><rect x="380" y="955" width="440" height="14" rx="4" fill="#7E5D43"/>
<rect x="420" y="1110" width="14" height="22" fill="#4A3527"/><rect x="766" y="1110" width="14" height="22" fill="#4A3527"/>
<path d="M560 955 q-6 -60 18 -110 q8 50 -2 110z" fill="#5D7A5E"/><path d="M585 955 q16 -70 52 -96 q-14 54 -36 96z" fill="#6E8C6E"/><rect x="556" y="905" width="60" height="52" rx="10" fill="#EFE7DA"/>
<circle cx="700" cy="930" r="26" fill="#D6BC84"/>
</svg>'''
    body = f'''<div class="head"><div class="chip">Idee de amenajare</div>
<h1 class="serif">{html.escape(pk['headline'])}</h1></div>
<div class="ill">{svg}
<div class="call c1"><b>Brâu WL1</b> · 38 × 18 mm</div>
<div class="call c2">Chenar în jurul tabloului</div>
<div class="call c3">Caroiaje sub brâul orizontal</div></div>'''
    css = """
.head{position:absolute;top:60px;left:70px;right:70px;text-align:center;color:#1F3A2F}
.head .chip{color:#7A5B22}
.head h1{font-size:68px;font-weight:500;line-height:1.1;margin-top:26px}
.ill{position:absolute;top:400px;left:0;width:1200px;height:1300px}
.ill svg{display:block}
.call{position:absolute;background:#1F3A2F;color:#F4EEE4;font-size:30px;padding:14px 26px;border-radius:12px;box-shadow:0 10px 24px rgba(0,0,0,.2)}
.call b{color:#D6BC84;font-weight:600}
.call:before{content:'';position:absolute;width:18px;height:18px;border-radius:50%;background:#D6BC84;border:4px solid #fff}
.c1{left:470px;top:56px}.c1:before{left:-34px;top:16px}
.c2{left:60px;top:520px}.c2:before{right:-30px;top:16px}
.c3{right:50px;top:860px}.c3:before{left:-34px;top:16px}
"""
    return page(body, css)

def detalii(pk):
    it = pk['items'][0]; inf = INFO[it['c']]
    img = inf['sec'] or inf['hero']
    rows = [('Model', it['c']), ('Secțiune', inf['dim']), ('Lungime bară', inf['L']), ('Material', inf['mat']), ('În pachet', qty_label(pk))]
    tr = ''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td></tr>' for a, b in rows)
    li = ''.join(f'<li>{html.escape(b)}</li>' for b in pk['beneficii'])
    body = f'''<div class="eyebrow" style="position:absolute;top:70px;left:0;right:0;text-align:center">Detalii tehnice</div>
<div class="sec"><img src="{rel(img)}"></div>
<table>{tr}</table><ul>{li}</ul>'''
    css = """
.sec{position:absolute;top:150px;left:150px;width:900px;height:760px;background:#fff;border-radius:24px;overflow:hidden;border:1px solid #E6DCCB}
.sec img{width:100%;height:100%;object-fit:contain}
table{position:absolute;top:960px;left:110px;width:980px;border-collapse:collapse;font-size:36px}
td{padding:16px 6px;border-bottom:1px solid #E1D6C3}
td:first-child{color:#7A5B22;width:330px;font-weight:500}
ul{position:absolute;top:1430px;left:110px;width:980px;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:18px 30px}
li{font-size:31px;line-height:1.25;padding-left:44px;position:relative}
li:before{content:'';position:absolute;left:0;top:9px;width:24px;height:24px;border-radius:50%;background:#D6BC84;box-shadow:inset 0 0 0 6px #FAF7F2;border:2px solid #D6BC84}
"""
    return page(body, css)

def continut(pk):
    cards = ''
    for it in pk['items']:
        inf = INFO[it['c']]
        sub = f"{inf['dim']}" + (f" · bară {inf['L']}" if inf['L'] else '')
        cards += f'''<div class="card"><img src="{rel(inf['hero'])}"><div><div class="qq">{it['q']} ×</div><div class="nm">{html.escape(inf['short'])}</div><div class="sb">{html.escape(sub)}</div></div></div>'''
    body = f'''<div class="wrap"><div class="eyebrow">Ce primești</div><h1 class="serif">Conținutul pachetului</h1>
{cards}
<div class="cov"><span>Acoperire</span>{html.escape(pk['acoperire'])}</div>
<div class="ship"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#D6BC84" stroke-width="1.6"><path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>
<div><b>Livrare inclusă în preț</b><br>Ambalare atentă, pentru bare lungi și fragile</div></div></div>'''
    css = """
.wrap{position:absolute;inset:70px 80px}
.wrap h1{font-size:76px;font-weight:500;margin:18px 0 50px}
.card{display:flex;align-items:center;gap:40px;background:#fff;border-radius:24px;padding:26px;margin-bottom:30px;border:1px solid #E6DCCB}
.card img{width:330px;height:330px;object-fit:cover;border-radius:16px;flex:none}
.qq{font-family:'Playfair Display',serif;font-size:90px;color:#7A5B22;line-height:1}
.nm{font-size:46px;font-weight:500;margin:8px 0}
.sb{font-size:32px;color:#2E5244}
.cov{font-size:36px;line-height:1.35;border-left:6px solid #D6BC84;padding:6px 0 6px 30px;margin:20px 0 40px}
.cov span{display:block;font-size:24px;letter-spacing:.28em;text-transform:uppercase;color:#7A5B22;font-weight:500;margin-bottom:6px}
.ship{position:absolute;left:0;right:0;bottom:0;display:flex;gap:30px;align-items:center;background:#1F3A2F;color:#F4EEE4;border-radius:24px;padding:36px 44px;font-size:32px;line-height:1.35}
.ship b{color:#D6BC84;font-weight:500;font-size:40px}
"""
    return page(body, css)

def produs_jpg(src, dst):
    """Fotografia de produs de pe site pe canvas alb 1200x1800 (raport Trendyol 2:3)."""
    im = Image.open(os.path.join(ROOT, src)).convert('RGB')
    im.thumbnail((W, W), Image.LANCZOS)
    c = Image.new('RGB', (W, H), 'white')
    c.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    c.save(dst, quality=92)

def desc(pk, lines, final):
    it = pk['items'][0]; inf = INFO[it['c']]
    cont = '\n'.join(f"- {l['q']} × {P[l['c']]['n']}" for l in lines)
    ben = '\n'.join(f'- {b}' for b in pk['beneficii'])
    return (f"{pk['headline']} {pk['sub']}\n\nConținutul pachetului:\n{cont}\n\n"
            f"Specificații: model {it['c']}, secțiune {inf['dim']}, lungime bară {inf['L']}, material {inf['mat'].lower()}.\n"
            f"Acoperire: {pk['acoperire']}.\n\nAvantaje:\n{ben}\n\n"
            f"Livrarea este inclusă în preț. Produsele se livrează ambalate pentru transport. " +
            ("Culoarea din imaginile de prezentare este orientativă; profilele se livrează " + ("albe, preamorsate" if pk['zona']=='interior' else "în culoare naturală gri-nisipiu") + " și se pot vopsi."))

def main():
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    out = os.path.join(ROOT, 'out'); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    rows, summary = [], []
    for pk in PK:
        lines, prod, final = price(pk)
        bd = os.path.join(ROOT, 'build', pk['id']); shutil.rmtree(bd, ignore_errors=True); os.makedirs(bd)
        od = os.path.join(out, pk['id']); os.makedirs(od)
        # imagini 100% de ambient (fotografii reale), fara desene tehnice — vezi ambient.py
        it0 = pk['items'][0]
        qty = f"{it0['q']} bucăți · {pk.get('mlLabel') or str(pk['ml']) + ' metri'}"
        pages = amb.pages(pk, bd, INFO, qty)
        for name, h in pages:
            open(os.path.join(bd, name + '.html'), 'w').write(h)
        # o singura fotografie de produs (cea „pe perete”), fara sectiuni / cote
        prod_imgs = []
        for it in pk['items']:
            src = INFO[it['c']]['hero'] if it['c'] != 'NA105' else 'src/NA105/04.jpg'
            dst = f"produs-{it['c']}.jpg"
            produs_jpg(src, os.path.join(od, dst)); prod_imgs.append(dst)
        imgs = [n + '.jpg' for n, _ in pages] + prod_imgs
        trendyol = imgs[:8]
        rows.append({'Cod pachet (SKU / barcode vânzător)': pk['id'], 'Titlu Trendyol': pk['titlu'],
                     'Zonă': pk['zona'], 'Preț produse (lei, TVA incl.)': ro(prod), 'Transport (lei)': ro(TRANSPORT),
                     'PREȚ FINAL (lei, TVA incl.)': ro(final),
                     'Conținut': '; '.join(f"{l['q']} × {l['c']} @ {ro(l['pu'])} = {ro(l['tot'])}" for l in lines),
                     'Imagini (ordine Trendyol, max. 8)': ' | '.join(f"{pk['id']}/{x}" for x in trendyol),
                     'Descriere': desc(pk, lines, final)})
        summary.append(dict(pk=pk, lines=lines, prod=prod, final=final, imgs=imgs, trendyol=trendyol))
        print(f"{pk['id']:22} produse {ro(prod):>10} + transport {ro(TRANSPORT)} = FINAL {ro(final):>10} lei · {len(imgs)} imagini")
    with open(os.path.join(out, 'trendyol-pachete.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';'); w.writeheader(); w.writerows(rows)
    json.dump([dict(id=s['pk']['id'], titlu=s['pk']['titlu'], final=s['final'], produse=s['prod'], transport=TRANSPORT,
                    linii=s['lines'], imagini=s['imgs'], trendyol=s['trendyol']) for s in summary],
              open(os.path.join(out, 'pachete-calcul.json'), 'w'), ensure_ascii=False, indent=1)
    gallery(summary)

def gallery(summary):
    cards = ''
    for s in summary:
        pk = s['pk']
        tbl = ''.join(f"<tr><td>{l['q']} ×</td><td><a href='{l['url']}'>{html.escape(l['n'])}</a>{' <em>(azi la ofertă: ' + ro(l['oferta']) + ')</em>' if l['oferta'] else ''}</td><td class=r>{ro(l['pu'])}</td><td class=r>{ro(l['tot'])}</td></tr>" for l in s['lines'])
        thumbs = ''.join(f"<a href='{pk['id']}/{x}'><img loading=lazy src='{pk['id']}/{x}' alt=''></a>" for x in s['imgs'])
        cards += f"""<section><h2>{html.escape(pk['titlu'])}</h2><div class=sku>{pk['id']}</div>
<table>{tbl}<tr class=s><td></td><td>Transport</td><td></td><td class=r>{ro(TRANSPORT)}</td></tr>
<tr class=f><td></td><td>PREȚ FINAL Trendyol (TVA inclus)</td><td></td><td class=r>{ro(s['final'])} lei</td></tr></table>
<div class=th>{thumbs}</div></section>"""
    h = f"""<!doctype html><html lang=ro><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Pachete Trendyol</title>
<style>:root{{--bg:#FAF7F2;--fg:#1F3A2F;--mut:#7A5B22;--card:#fff;--line:#E6DCCB}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#141815;--fg:#EDE6D8;--mut:#D6BC84;--card:#1E2420;--line:#333B35}}}}
body{{background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,sans-serif;margin:0;padding:24px 16px}}main{{max-width:1100px;margin:auto}}
h1{{font-family:Georgia,serif;font-weight:500}}section{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0}}
h2{{margin:0;font-size:19px}}.sku{{color:var(--mut);font:13px monospace;margin:4px 0 10px}}table{{width:100%;border-collapse:collapse;font-size:14px}}td{{padding:5px 4px;border-bottom:1px solid var(--line)}}
.r{{text-align:right;white-space:nowrap}}tr.f td{{font-weight:700;font-size:16px;color:var(--mut)}}a{{color:inherit}}em{{color:var(--mut);font-size:12px}}
.th{{display:flex;gap:8px;overflow-x:auto;margin-top:12px}}.th img{{height:180px;border-radius:6px;border:1px solid var(--line)}}</style></head>
<body><main><h1>Pachete Deco&amp;Flair pentru Trendyol</h1>
<p>Prețuri de listă nereduse de pe decoflair.ro (TVA inclus), citite la {P['Z11']['citit']}, + {ro(TRANSPORT)} lei transport pe pachet.</p>{cards}</main></body></html>"""
    open(os.path.join(ROOT, 'out', 'index.html'), 'w').write(h)

if __name__ == '__main__':
    main()

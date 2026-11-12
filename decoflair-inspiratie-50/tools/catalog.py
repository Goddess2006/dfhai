"""Index generated originals without modifying the image files."""
from pathlib import Path
from html import escape
import hashlib,json,struct,argparse

root=Path(__file__).resolve().parents[1]
def build(require_complete=False):
    manifest=json.loads((root/'manifest.json').read_text())
    complete=[]
    for item in manifest['images']:
        path=root/item['file']
        if not path.is_file():
            item['status']='pending'
            continue
        raw=path.read_bytes()
        if raw[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError(f'Invalid PNG: {path}')
        width,height=struct.unpack('>II',raw[16:24])
        item.update(status='generated',width=width,height=height,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        complete.append(item)
    if require_complete:
        assert len(complete)==50, f'{len(complete)}/50 images available'
        assert len({i['sha256'] for i in complete})==50, 'Duplicate images'
        assert all(i['width']>=1024 and i['height']>=1024 for i in complete)
        assert all(i['width']<i['height'] for i in complete), 'Portrait assets required'
    manifest['countGenerated']=len(complete)
    (root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    names={'interior':'Interior','exterior':'Exterior','panouri-3d':'Panouri 3D','riflaje':'Riflaje','produse-detalii':'Produse și detalii'}
    nav='<button class="active" data-filter="all">Toate</button>'+''.join(f'<button data-filter="{key}">{name}</button>' for key,name in names.items())
    cards=''
    for item in manifest['images']:
        if item['status']!='generated':continue
        cards+=f'''<article data-category="{item['category']}"><a href="{escape(item['file'])}" target="_blank" rel="noopener"><img src="{escape(item['file'])}" alt="{escape(item['title'])}" width="{item['width']}" height="{item['height']}" loading="lazy"></a><div><small>{item['id']:02d} / {names[item['category']]}</small><h2>{escape(item['title'])}</h2><p>Imagine conceptuală de inspirație</p><a href="{escape(item['file'])}" download>Descarcă originalul ↗</a><details><summary>Brief de generare</summary><p>{escape(item['prompt'])}</p></details></div></article>'''
    page='''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Biblioteca vizuală Deco&Flair</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#151310;color:#f4eee4;font:15px/1.6 system-ui,sans-serif}header,main{max-width:1450px;margin:auto;padding:32px}header{padding-top:48px}header small{letter-spacing:.2em;color:#cfb887}h1{font:500 clamp(32px,5vw,64px)/1.1 Georgia,serif;margin:16px 0}header p{max-width:850px;color:#bdb7ae}.toolbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin-top:25px}button{font:inherit;font-size:13px;border:1px solid #4f4432;border-radius:30px;padding:9px 16px;background:#211d17;color:#d9c8a6;cursor:pointer}button.active{background:#d6bc84;color:#211d17}.count{font-size:13px;color:#aaa;margin-left:auto}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}article{background:#211d18;border:1px solid #393126;border-radius:16px;overflow:hidden}article>a{display:block}img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover}article>div{padding:20px}article small{font-size:10px;letter-spacing:.1em;color:#bfa77b}h2{font:500 22px/1.3 Georgia,serif;margin:10px 0}article p{font-size:12px;color:#b4aa9a}a{color:#e2c78e;text-decoration:none;font-size:12px}details{font-size:12px;color:#c3b69e;margin-top:14px}summary{cursor:pointer}details p{overflow-wrap:anywhere}footer{max-width:1450px;margin:auto;padding:32px;color:#a49985;font-size:12px}[hidden]{display:none!important}:focus-visible{outline:2px solid #e2c78e;outline-offset:3px}@media(max-width:1050px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:750px){header,main{padding:22px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}article>div{padding:14px}h2{font-size:19px}}@media(max-width:430px){.grid{grid-template-columns:1fr}}
</style></head><body><header><small>DECO&FLAIR / BIBLIOTECA DE INSPIRAȚIE</small><h1>Idei care dau formă casei.</h1><p>50 de direcții vizuale pentru postări viitoare: ambientale, materiale și prezentări de produs. Imagini generate cu AI pentru inspirație; nu documentează lucrări reale sau modele exacte de catalog.</p><div class="toolbar">NAV<span class="count" id="count">COUNT imagini salvate</span></div></header><main><div class="grid">CARDS</div></main><footer>Fără prețuri, reduceri sau sigle în imagini. Înaintea unei postări despre un produs concret, verifică asocierea vizualului cu fotografia și specificațiile produsului real. Prompturile și proveniența sunt păstrate în manifest.json.</footer><script>const buttons=[...document.querySelectorAll('[data-filter]')];buttons.forEach(button=>button.addEventListener('click',()=>{buttons.forEach(b=>b.classList.toggle('active',b===button));let shown=0;document.querySelectorAll('article').forEach(card=>{card.hidden=button.dataset.filter!=='all'&&card.dataset.category!==button.dataset.filter;if(!card.hidden)shown++;});document.getElementById('count').textContent=shown+' imagini';}));</script></body></html>'''.replace('NAV',nav).replace('COUNT',str(len(complete))).replace('CARDS',cards)
    (root/'index.html').write_text(page)
    print(f"{len(complete)}/50 images indexed; {sum(i['bytes'] for i in complete)/1024/1024:.1f} MiB")
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--require-complete',action='store_true');args=p.parse_args();build(args.require_complete)

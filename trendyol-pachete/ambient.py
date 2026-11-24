"""Imagini Trendyol 100% de ambient (1200x1800): fotografii reale de pe decoflair.ro / din repository,
produsul evidentiat cu o eticheta-reper (ca in cataloagele de mobila) si un medalion cu produsul. Fara desene tehnice.
Folosit de build.py: pages(pk, build_dir) -> [(nume, html)]"""
import os, html
from PIL import Image, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
W, H = 1200, 1800
CF = '../catalog-fatade/jpg/'
IN = '../decoflair-inspiratie-50/imagini/'
A = 'src/amb/'

# kind: hero (foto + panou jos + medalion), split (foto + text), full (foto pe toata imaginea), ba (inainte/dupa), kit (continut)
# tag: (x, y, eticheta) in fractiuni din imaginea sursa; f: punct de focalizare pentru decupare
SCENES = {
 'P01-Z11x5': [
  dict(kind='hero', img=A + 'site-living-alb-cornisa-led.png', f=(.42, .3), tag=(.56, .1, 'Cornișă de tavan'),
       title='Tavanul care face camera să pară mai înaltă.', sub='O linie elegantă de jur împrejur — și livingul arată ca proaspăt renovat.'),
  dict(kind='split', img=CF + '12-hol-albastru-chenare-cornisa.jpg', f=(.5, .5), tag=(.5, .07, 'Cornișă'), title='Detaliul pe care îl observă toți musafirii.', sub='O cornișă albă face orice hol să pară mai elegant.'),
  dict(kind='split', img=A + 'site-montaj-cornisa.png', f=(.5, .45), title='Se montează într-o după-amiază.', sub='Se lipește, se îmbină, se vopsește. Fără praf, fără șuruburi.', top=True),
  dict(kind='full', img='../decoflair-blog-reel/assets/a3-chenare.jpg', f=(.62, .5), title='Clasic, luminos. La tine acasă.', sub='Holul de la intrare spune primul povestea casei.'),
 ],
 'P02-FD3x5': [
  dict(kind='hero', img=IN + 'interior/05-hol-plinta.png', f=(.45, .55), tag=(.3, .62, 'Plintă albă'),
       title='Finisajul care schimbă tot.', sub='Plinta albă, înaltă, leagă parchetul de perete — curat și luminos.'),
  dict(kind='split', img=A + 'site-hol-lemn.png', f=(.45, .55), title='Un hol care te întâmpină frumos.', sub='Linii simple, culori calde, plinte care completează imaginea.'),
  dict(kind='full', img=A + 'site-dormitor-plinta.jpg', f=(.5, .5), title='Liniște. Lumină. Ordine.', sub='Plinta albă face dormitorul să pară mai mare și mai aerisit.'),
  dict(kind='split', img=A + 'site-vopsire-perete.png', f=(.42, .5), title='Schimbi culoarea? Plinta o urmează.', sub='O vopsești în culoarea peretelui sau o lași albă, ca accent.', top=True),
 ],
 'P03-WL1x8': [
  dict(kind='hero', img=A + 'wl1-living-tablouri.jpg', f=(.5, .5), tag=(.47, .57, 'Chenare din brâu'),
       title='Rame elegante pentru tablouri. Direct pe perete.', sub='Câteva baghete, puțină vopsea — și peretele gol devine piesa centrală a camerei.'),
  dict(kind='ba', before=CF + '11-living-salvie-cornisa-led-inainte.jpg', after=CF + '13-living-salvie-cornisa-led-chenare-dupa.jpg', f=(.5, .45),
       title='Același living. Alt nivel.'),
  dict(kind='split', img=A + 'wl1-bucatarie-tablouri.jpg', f=(.55, .4), tag=(.39, .3, 'Chenar pentru tablou'),
       title='Și în bucătărie, de ce nu?', sub='Chenare vopsite în culoarea peretelui, cu tablourile tale preferate.'),
  dict(kind='split', img=CF + '12-hol-albastru-chenare-cornisa.jpg', f=(.62, .5), tag=(.82, .45, 'Caroiaje'),
       title='Holul care arată ca într-o revistă.', sub='Chenare pe pereții colorați, un covor de iută și lumină caldă.', top=True),
  dict(kind='full', img=CF + '14-dormitor-mov-chenare.jpg', f=(.5, .5), title='Peretele din spatele patului, transformat.', sub='Chenarele încadrează patul și aplicele — fără tăblie scumpă.'),
 ],
 'P04-IL13x5': [
  dict(kind='hero', img=IN + 'interior/07-living-scafa-led.png', f=(.55, .35), tag=(.6, .2, 'Lumină indirectă'),
       title='Lumina devine atmosferă.', sub='Banda LED ascunsă în cornișă luminează tavanul, cald și fără să orbească.'),
  dict(kind='split', img=A + 'site-living-modern-led.png', f=(.35, .45), tag=(.4, .07, 'Cornișă LED'),
       title='Seara, livingul arată ca la hotel.', sub='Lumina caldă de sus face camera primitoare și mai înaltă.'),
  dict(kind='split', img=CF + '13-living-salvie-cornisa-led-chenare-dupa.jpg', f=(.5, .4), tag=(.5, .05, 'Cornișă cu LED'),
       title='Cea mai frumoasă lumină din casă.', sub='Perfectă pentru serile de film, cu o lampă și o pătură moale.', top=True),
  dict(kind='full', img='../decoflair-blog-reel/assets/a4-cornisa-led.jpg', f=(.5, .5), title='Un detaliu. Toată diferența.', sub='Lumina pleacă într-o singură direcție, spre tavan.'),
 ],
 'P05-NCL107x5-QUARTZ': [
  dict(kind='hero', img=CF + '06-casa-taupe-coltare-bosaje-ancadramente-cornisa.jpg', f=(.45, .55), tag=(.27, .5, 'Colțare de fațadă'),
       title='Colțuri de casă cu aer de piatră.', sub='Bosajele dau fațadei aspect solid, elegant — vizibil de pe stradă.'),
  dict(kind='full', img=IN + 'exterior/17-colt-fatada.png', f=(.5, .5), tag=(.62, .45, 'Colțar'), title='Detaliul care dă caracter.', sub='Lumina serii pune în valoare fiecare bosaj.'),
  dict(kind='split', img=CF + '03-casa-bej-coltare-bosaje-ancadramente.jpg', f=(.5, .5), title='Casa ta, cu altă personalitate.', sub='Colțarele se vopsesc în culoarea fațadei sau în contrast.'),
  dict(kind='split', img=A + 'site-fatada-colt.jpg', f=(.5, .5), title='Arată ca piatra. E ușor ca polistirenul.', sub='Se lipește direct pe fațadă și rezistă la soare, ploaie și ger.', top=True),
 ],
 'P06-NA105x5-FIX': [
  dict(kind='hero', img=CF + '08-casa-gri-ancadramente-cornisa.jpg', f=(.5, .5), tag=(.33, .42, 'Ancadrament'),
       title='Ferestre încadrate ca la o vilă.', sub='Ancadramentele albe transformă o casă simplă într-una cu stil.'),
  dict(kind='split', img=A + 'site-fatada-renovare.png', f=(.5, .45), title='Renovezi fațada? Începe cu ferestrele.', sub='Ancadramentele se montează înainte de vopsirea finală.', top=True),
  dict(kind='full', img=A + 'site-ancadrament-fereastra.jpg', f=(.5, .5), title='Umbre fine. Linii curate.', sub='Profilul lat, cu trepte, se vede frumos în lumina zilei.'),
  dict(kind='split', img=CF + '02-casa-crem-ancadramente-gri-portic.jpg', f=(.5, .5), title='Casa pe care o recunoști de pe stradă.', sub='Ancadramente vopsite în contrast pentru un efect elegant.'),
 ],
 'P07-NC104x5-FIX': [
  dict(kind='hero', img=CF + '05-casa-albastra-ancadramente-cornisa.jpg', f=(.5, .45), tag=(.62, .3, 'Cornișă de fațadă'),
       title='Linia care încununează casa.', sub='Cornișa de sub streașină dă fațadei un aspect finisat, îngrijit.'),
  dict(kind='full', img=IN + 'exterior/15-cornisa-acoperis.png', f=(.5, .5), title='Frumoasă de aproape. Și de departe.', sub='Lumina soarelui desenează profilul cornișei.'),
  dict(kind='split', img=A + 'site-casa-fatada.webp', f=(.5, .5), title='Detaliile care fac casa să pară nouă.', sub='Cornișă, ancadramente și o culoare caldă de fațadă.'),
  dict(kind='split', img=CF + '04-casa-galbena-ancadramente-cheie-bolta-cornisa.jpg', f=(.5, .5), title='O fațadă veselă, cu personalitate.', sub='Cornișa albă pe fațada colorată — combinația care nu dă greș.', top=True),
 ],
 'P08-REMA1x5-QUARTZ': [
  dict(kind='hero', img=CF + '09-casa-verde-salvie-ancadramente-brau.jpg', f=(.5, .5), tag=(.22, .48, 'Brâu de fațadă'),
       title='Fațada cu ritm și proporție.', sub='Brâul dintre etaje face casa să pară mai bine proporționată.'),
  dict(kind='split', img=CF + '01-casa-terracota-ancadramente-brau.jpg', f=(.5, .5), title='Culoare caldă, linii albe.', sub='Brâul subliniază fațada și leagă ferestrele între ele.'),
  dict(kind='full', img='../decoflair-blog-reel/assets/a6-fatade.jpg', f=(.5, .5), title='Casa visată, pe strada ta.', sub='Profilele decorative fac diferența dintre „o casă” și „casa ta”.'),
  dict(kind='split', img=CF + '10-casa-piersica-ancadramente-cornisa-pilastri.jpg', f=(.5, .5), title='Mic detaliu, efect mare.', sub='Se vopsește în culoarea fațadei sau în alb, pentru contrast.', top=True),
 ],
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">')
CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{width:1200px;height:1800px;overflow:hidden}
body{font-family:Jost,sans-serif;color:#2A2622;background:#F6F1E9;position:relative}
h1,h2{font-family:'Playfair Display',serif;font-weight:500;font-variant-numeric:lining-nums}
img.ph{position:absolute;left:0;display:block}
.tag{position:absolute;transform:translate(-22px,-22px);display:flex;align-items:center;gap:14px}
.tag i{width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.95);box-shadow:0 0 0 8px rgba(255,255,255,.35),0 6px 18px rgba(0,0,0,.25);position:relative;flex:none}
.tag i:after{content:'';position:absolute;inset:13px;border-radius:50%;background:#B8894A}
.tag b{background:rgba(255,255,255,.96);color:#2A2622;font-weight:500;font-size:30px;padding:12px 24px;border-radius:40px;box-shadow:0 8px 22px rgba(0,0,0,.18);white-space:nowrap}
.tag.l{flex-direction:row-reverse;transform:translate(calc(-100% + 22px),-22px)}
.pill{display:inline-block;font-size:24px;letter-spacing:.22em;text-transform:uppercase;color:#8A6A3A;font-weight:500}
.note{position:absolute;right:22px;font-size:17px;color:rgba(255,255,255,.8)}
"""

def page(body, extra=''):
    return f'<!doctype html><html lang="ro"><head><meta charset="utf-8">{FONTS}<style>{CSS}{extra}</style></head><body>{body}</body></html>'

def crop(src, w, h, f, dst):
    """Decupeaza sursa la w x h in jurul punctului f; intoarce functia de mapare a reperelor."""
    im = Image.open(os.path.join(ROOT, src)).convert('RGB')
    sw, sh = im.size; s = max(w / sw, h / sh); cw, ch = w / s, h / s
    x0 = min(max(f[0] * sw - cw / 2, 0), sw - cw); y0 = min(max(f[1] * sh - ch / 2, 0), sh - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)
    if s > 1.05: im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60 if s > 1.4 else 40, threshold=2))
    im = ImageEnhance.Color(im).enhance(1.04)
    im.save(dst, quality=93)
    return lambda tx, ty: ((tx * sw - x0) * s, (ty * sh - y0) * s)

def tag_html(m, t, top_off=0):
    x, y = m(t[0], t[1]); y += top_off
    if not (40 < x < W - 40 and 40 < y < H - 40): return ''
    cls = 'tag l' if x > W * 0.6 else 'tag'
    return f'<div class="{cls}" style="left:{x:.0f}px;top:{y:.0f}px"><i></i><b>{html.escape(t[2])}</b></div>'

def is_ai(src): return 'inspiratie' in src or 'catalog-fatade' in src or 'blog-reel' in src or 'wl1-' in src

def note(src, bottom):
    return f'<div class="note" style="bottom:{bottom}px">Imagine de prezentare</div>' if is_ai(src) else ''

def zoom(src, t, bd, frac=.2):
    """Lupa: detaliu marit din aceeasi fotografie, centrat pe produs."""
    im = Image.open(os.path.join(ROOT, src)).convert('RGB'); w, h = im.size; s = min(w, h) * frac
    x0 = min(max(t[0] * w - s / 2, 0), w - s); y0 = min(max(t[1] * h - s / 2, 0), h - s)
    im = im.crop((int(x0), int(y0), int(x0 + s), int(y0 + s))).resize((600, 600), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    im.save(os.path.join(bd, 'm-zoom.jpg'), quality=93); return 'm-zoom.jpg'

def hero(pk, sc, bd, qty, prod_img):
    ph = 1240; m = crop(sc['img'], W, ph, sc['f'], os.path.join(bd, 'p-hero.jpg'))
    if sc.get('zoom', sc.get('tag')): prod_img = zoom(sc['img'], sc.get('zoom', sc.get('tag')), bd, sc.get('zf', .2))
    tg = tag_html(m, sc['tag']) if sc.get('tag') else ''
    extra = f"<div class='acc'>+ {html.escape(pk['acc_label'])}</div>" if pk.get('acc_label') else ''
    body = f"""<img class="ph" src="p-hero.jpg" style="top:0;width:{W}px;height:{ph}px">{tg}{note(sc['img'], 1800-ph+18)}
<div class="medal"><img src="{prod_img}"></div>
<div class="panel"><div class="pill">{html.escape(pk['kit'])}</div><h1>{html.escape(sc['title'])}</h1><p>{html.escape(sc['sub'])}</p>
<div class="chips"><span>{html.escape(qty)}</span>{extra}<span class="g">Livrare inclusă</span></div></div>"""
    css = f""".panel{{position:absolute;z-index:1;top:{ph}px;left:0;right:0;bottom:0;padding:44px 70px 0;background:#F6F1E9}}
.panel h1{{font-size:62px;line-height:1.08;margin:14px 330px 18px 0}}.panel p{{font-size:30px;line-height:1.35;color:#5A5048;margin-right:300px;font-weight:300}}
.chips{{position:absolute;left:70px;bottom:44px;display:flex;gap:14px}}.chips span,.acc{{font-size:27px;padding:12px 26px;border-radius:40px;background:#fff;border:1.5px solid #E2D6C3;font-weight:500}}
.chips span.g{{background:#2F4A3A;color:#F6F1E9;border-color:#2F4A3A}}.acc{{display:inline-block}}
.medal{{position:absolute;z-index:5;right:60px;top:{ph-170}px;width:320px;height:320px;border-radius:50%;overflow:hidden;border:10px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.25)}}
.medal img{{width:100%;height:100%;object-fit:cover}}"""
    return page(body, css)

def split(pk, sc, bd, name):
    ph = 1400; top = sc.get('top'); y = 400 if top else 0
    m = crop(sc['img'], W, ph, sc['f'], os.path.join(bd, f'p-{name}.jpg'))
    tg = tag_html(m, sc['tag'], y) if sc.get('tag') else ''
    ty = 0 if top else ph
    body = f"""<img class="ph" src="p-{name}.jpg" style="top:{y}px;width:{W}px;height:{ph}px">{tg}{note(sc['img'], (1800 - y - ph) + 18)}
<div class="cap" style="top:{ty}px"><h2>{html.escape(sc['title'])}</h2><p>{html.escape(sc['sub'])}</p></div>"""
    css = """.cap{position:absolute;left:0;right:0;height:400px;padding:0 80px;display:flex;flex-direction:column;justify-content:center;background:#F6F1E9}
.cap h2{font-size:64px;line-height:1.08;margin-bottom:18px}.cap p{font-size:31px;line-height:1.35;color:#5A5048;font-weight:300}"""
    return page(body, css)

def full(pk, sc, bd, name):
    m = crop(sc['img'], W, H, sc['f'], os.path.join(bd, f'p-{name}.jpg'))
    tg = tag_html(m, sc['tag']) if sc.get('tag') else ''
    body = f"""<img class="ph" src="p-{name}.jpg" style="top:0;width:{W}px;height:{H}px"><div class="sh"></div>{tg}
<div class="cap"><h2>{html.escape(sc['title'])}</h2><p>{html.escape(sc['sub'])}</p></div>{note(sc['img'], 18)}"""
    css = """.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(20,16,12,.72) 100%)}
.cap{position:absolute;left:80px;right:80px;bottom:110px;color:#fff}.cap h2{font-size:76px;line-height:1.06;margin-bottom:20px}.cap p{font-size:34px;line-height:1.35;font-weight:300}"""
    return page(body, css)

def ba(pk, sc, bd, name):
    hh = 800
    crop(sc['before'], W, hh, sc['f'], os.path.join(bd, 'p-inainte.jpg'))
    crop(sc['after'], W, hh, sc['f'], os.path.join(bd, 'p-dupa.jpg'))
    body = f"""<div class="t"><h2>{html.escape(sc['title'])}</h2></div>
<img class="ph" src="p-inainte.jpg" style="top:200px;width:{W}px;height:{hh}px"><div class="lb" style="top:230px">Înainte</div>
<img class="ph" src="p-dupa.jpg" style="top:{200+hh}px;width:{W}px;height:{hh}px"><div class="lb d" style="top:{230+hh}px">După · cu chenare</div>
<div class="line" style="top:{200+hh-3}px"></div>{note(sc['after'], 18)}"""
    css = """.t{position:absolute;top:0;left:0;right:0;height:200px;display:flex;align-items:center;justify-content:center}.t h2{font-size:66px}
.lb{position:absolute;left:40px;background:rgba(255,255,255,.95);font-size:30px;font-weight:500;padding:12px 28px;border-radius:40px}.lb.d{background:#2F4A3A;color:#F6F1E9}
.line{position:absolute;left:0;right:0;height:6px;background:#F6F1E9}"""
    return page(body, css)

def kit(pk, sc0, bd, items):
    crop(sc0['img'], W, H, sc0['f'], os.path.join(bd, 'p-bg.jpg'))
    cards = ''.join(f"""<div class="c"><img src="{img}"><div><div class="q">{q} ×</div><div class="n">{html.escape(n)}</div></div></div>""" for img, q, n in items)
    body = f"""<img class="ph bg" src="p-bg.jpg" style="top:0;width:{W}px;height:{H}px"><div class="veil"></div>
<div class="card"><div class="pill">Ce primești</div><h2>{html.escape(pk['kit'])}</h2>{cards}
<div class="tot">{html.escape(pk['acoperire_scurt'])}</div><div class="ship">Livrare inclusă în preț · totul într-o singură comandă</div></div>"""
    css = """.bg{filter:blur(14px) brightness(.9);transform:scale(1.08)}.veil{position:absolute;inset:0;background:rgba(246,241,233,.35)}
.card{position:absolute;left:80px;right:80px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.93);border-radius:34px;padding:56px 56px 48px;box-shadow:0 30px 70px rgba(0,0,0,.25)}
.card h2{font-size:70px;margin:12px 0 36px}.c{display:flex;align-items:center;gap:34px;margin-bottom:28px}
.c img{width:300px;height:300px;object-fit:cover;border-radius:22px;flex:none}.q{font-family:'Playfair Display',serif;font-size:88px;color:#8A6A3A;line-height:1}
.n{font-size:42px;font-weight:500;margin-top:8px;line-height:1.2}.tot{font-size:32px;color:#5A5048;margin:6px 0 26px;font-weight:300}.ship{margin-top:18px;background:#2F4A3A;color:#F6F1E9;border-radius:22px;padding:28px 34px;font-size:32px;text-align:center}"""
    return page(body, css)

def rel(bd, p): return os.path.relpath(os.path.join(ROOT, p), bd)

MEDAL = {  # (sursa, centru x, centru y, zoom) — decupaj pe produs pentru medalion / cardul „Ce primești”
 'Z11': ('src/Z11/01.jpg', .55, .3, 1.9), 'FD3': ('src/FD3/01.jpg', .55, .62, 2.0), 'WL1': ('src/WL1/01.jpg', .5, .55, 2.6),
 'IL13': ('src/IL13/01.jpg', .62, .38, 1.9), 'NCL107': ('src/NCL107/01.jpg', .55, .5, 1.6), 'NA105': ('src/NA105/04.jpg', .55, .5, 1.3),
 'NC104': ('src/NC104/01.jpg', .55, .45, 1.5), 'REMA1': ('src/REMA1/01.jpg', .55, .5, 1.6),
 'Adro-Quartz1.5': ('src/Adro-Quartz1.5/01.jpg', .5, .5, 1.1), 'Adro-Fix4': ('src/Adro-Fix4/01.jpg', .5, .5, 1.1)}

def medal(code, bd):
    src, cx, cy, z = MEDAL[code]
    im = Image.open(os.path.join(ROOT, src)).convert('RGB'); w, h = im.size; s = min(w, h) / z
    x0 = min(max(cx * w - s / 2, 0), w - s); y0 = min(max(cy * h - s / 2, 0), h - s)
    im = im.crop((int(x0), int(y0), int(x0 + s), int(y0 + s))).resize((600, 600), Image.LANCZOS)
    dst = os.path.join(bd, f'm-{code}.jpg'); im.save(dst, quality=93); return os.path.basename(dst)

def pages(pk, bd, info, qty):
    scenes = SCENES[pk['id']]; out = []
    main = pk['items'][0]['c']
    prod = medal(main, bd)
    pk = dict(pk, acoperire_scurt=pk['acoperire'].split(' + ')[0].replace('metri liniari', 'metri'))
    if len(pk['items']) > 1: pk = dict(pk, acc_label=info[pk['items'][1]['c']]['short'])
    n = 1
    for sc in scenes:
        if sc['kind'] == 'hero': h = hero(pk, sc, bd, qty, prod); nm = 'pachet'
        elif sc['kind'] == 'split': h = split(pk, sc, bd, f'{n}'); nm = 'ambient'
        elif sc['kind'] == 'full': h = full(pk, sc, bd, f'{n}'); nm = 'ambient'
        else: h = ba(pk, sc, bd, f'{n}'); nm = 'inainte-dupa'
        out.append((f'{n:02d}-{nm}', h)); n += 1
    items = []
    for it in pk['items']:
        f = info[it['c']]
        items.append((medal(it['c'], bd), it['q'], f['short']))
    out.append((f'{n:02d}-ce-primesti', kit(pk, scenes[0] if scenes[0]['kind'] != 'ba' else scenes[1], bd, items)))
    return out

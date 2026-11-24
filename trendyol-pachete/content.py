"""Genereaza continutul complet pe kit: Trendyol (titlu, descriere HTML/text, atribute, cuvinte cheie),
SEO (title, meta, slug, H1), GEO (rezumat factual + fapte), AEO (FAQ), alt-text imagini, JSON-LD.
Rulare (dupa build.py): python3 content.py -> content/"""
import json, os, csv, html, shutil
from content_data import KITS, MONTAJ_INT, MONTAJ_EXT, volumes
import build

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'content')
VOL = volumes(os.path.join(ROOT, 'data', 'keywords-semrush-ro.csv'))
META = json.load(open(os.path.join(ROOT, 'data', 'meta-site.json')))
CALC = {x['id']: x for x in json.load(open(os.path.join(ROOT, 'out', 'pachete-calcul.json')))}
ro = build.ro
e = html.escape

ALT = {  # descrieri alternative pe tip de imagine
 'pachet': 'Copertă {kit}: {scurt}, {qty}',
 'ambient': '{scurt} — {head} (imagine de prezentare)',
 'caroiaje-tablouri': 'Ilustrație perete cu caroiaje din bagheta WL1 și tablouri încadrate în chenare',
 'detalii': 'Detalii tehnice {main}: secțiune {dim}, lungime bară {L}, material {mat}',
 'continut': 'Conținutul {kit}: {cont}, livrare inclusă',
 'produs': 'Fotografie produs {name} de pe decoflair.ro',
}

def kw_line(ks): return ', '.join(f"{k} ({VOL.get(k, 0)}/lună)" if VOL.get(k) else k for k in ks)

def kit_content(pk):
    k = KITS[pk['id']]; c = CALC[pk['id']]
    it = pk['items'][0]; inf = build.INFO[it['c']]
    final = c['final']; main = build.P[it['c']]
    def nice(l):
        f = build.INFO[l['c']]
        return f"{l['q']} × {f['short']}" + (f" ({f['dim']}, bară de {f['L']})" if f['L'] else '')
    cont = [nice(l) for l in c['linii']]
    zona = pk['zona']
    montaj = MONTAJ_INT if zona == 'interior' else MONTAJ_EXT
    culoare = 'Alb' if zona == 'interior' else 'Gri nisipiu (natur), vopsibil'
    brand_prod = META[it['c']]['producator'].replace('\\u00ae', '®')
    seo_title = k['seo_title']
    meta = k['meta']
    # ------------- GEO: rezumat factual, autonom, citabil
    geo = (f"{pk['kit']} de la Deco&Flair este un set de {pk['zona']} care conține "
           + '; '.join(cont) + f". Profilele au secțiunea {inf['dim']}, lungimea barei {inf['L']} și sunt din "
           f"{inf['mat'].lower()} ({brand_prod}). Setul acoperă {pk['acoperire']}. Prețul kitului este {ro(final)} lei cu TVA, "
           f"livrare inclusă (prețuri de listă decoflair.ro la {build.P[it['c']]['citit']}).")
    fapte = [('Tip produs', f"Kit profile decorative {zona}"), ('Conținut', '; '.join(cont)),
             ('Model', it['c']), ('Producător', brand_prod), ('Secțiune', inf['dim']), ('Lungime bară', inf['L']),
             ('Total', pk.get('mlLabel') or f"{pk['ml']} metri liniari"), ('Material', inf['mat']), ('Culoare', culoare),
             ('Aplicare', 'Interior' if zona == 'interior' else 'Exterior (fațadă)'), ('Montaj', 'Lipire cu adeziv pentru profile'),
             ('Vopsibil', 'Da'), ('Preț kit', f"{ro(final)} lei (TVA inclus), livrare inclusă"),
             ('Cod kit', pk['id'])]
    # ------------- descriere Trendyol HTML
    li = ''.join(f'<li>{e(b)}</li>' for b in k['bullets'])
    lic = ''.join(f'<li>{e(x)}</li>' for x in cont)
    lif = ''.join(f'<li>{e(x)}</li>' for x in k['pentru'])
    faq_h = ''.join(f'<p><strong>{e(q)}</strong><br>{e(a)}</p>' for q, a in k['faq'])
    spec = ''.join(f'<li><strong>{e(a)}:</strong> {e(b)}</li>' for a, b in fapte[2:12])
    extra = f"<h3>Idee: chenare pentru tablouri</h3><p>{e(k['extra'])}</p>" if k.get('extra') else ''
    desc_html = (f"<h2>{e(pk['kit'])} — {e(pk['headline'])}</h2><p>{e(k['intro'])}</p>"
                 f"<h3>De ce să alegi acest kit</h3><ul>{li}</ul>"
                 f"<h3>Ce conține kitul</h3><ul>{lic}</ul><p>Acoperire: {e(pk['acoperire'])}.</p>"
                 f"<h3>Unde se folosește</h3><ul>{lif}</ul>{extra}"
                 f"<h3>Specificații</h3><ul>{spec}</ul>"
                 f"<h3>Montaj</h3><p>{e(montaj)}</p>"
                 f"<h3>Întrebări frecvente</h3>{faq_h}"
                 f"<p><em>Livrarea este inclusă în preț. Imaginile de ambient au rol de prezentare; culoarea finală depinde de vopseaua aleasă.</em></p>")
    desc_txt = (f"{pk['kit']} — {pk['headline']}\n\n{k['intro']}\n\nDE CE SĂ ALEGI ACEST KIT\n" + '\n'.join('• ' + b for b in k['bullets'])
                + "\n\nCE CONȚINE KITUL\n" + '\n'.join('• ' + x for x in cont) + f"\nAcoperire: {pk['acoperire']}."
                + "\n\nUNDE SE FOLOSEȘTE\n" + '\n'.join('• ' + x for x in k['pentru'])
                + (f"\n\nIDEE: CHENARE PENTRU TABLOURI\n{k['extra']}" if k.get('extra') else '')
                + "\n\nSPECIFICAȚII\n" + '\n'.join(f'• {a}: {b}' for a, b in fapte[2:12])
                + f"\n\nMONTAJ\n{montaj}\n\nÎNTREBĂRI FRECVENTE\n" + '\n\n'.join(f'{q}\n{a}' for q, a in k['faq'])
                + "\n\nLivrarea este inclusă în preț. Imaginile de ambient au rol de prezentare; culoarea finală depinde de vopseaua aleasă.")
    # ------------- atribute Trendyol (de potrivit cu lista categoriei din panou)
    atr = {'Culoare': culoare.split(',')[0], 'Material': inf['mat'], 'Model / cod': it['c'],
           'Număr de bucăți în set': str(it['q']) + (f" + {pk['items'][1]['q']}" if len(pk['items']) > 1 else ''),
           'Lungime bară (cm)': inf['L'].replace(' m', '00').replace('1 00', '100').replace('2 00', '200'),
           'Dimensiuni secțiune (mm)': inf['dim'].replace(' mm', ''), 'Total metri liniari': str(pk['ml']),
           'Zonă de utilizare': 'Interior' if zona == 'interior' else 'Exterior', 'Stil': 'Clasic / Modern / Elegant',
           'Vopsibil': 'Da', 'Garanție': '24 luni (conform legii)'}
    # ------------- alt text imagini
    alts = []
    import ambient as amb
    scs = amb.SCENES[pk['id']]
    for f in c['trendyol']:
        if f.startswith('produs-'):
            code = f[7:-4]; a = f"{build.P[code]['n']} — fotografie produs"
        elif 'ce-primesti' in f:
            a = f"{pk['kit']}: " + '; '.join(cont) + ', livrare inclusă'
        else:
            sc = scs[int(f[:2]) - 1]
            if sc['kind'] == 'ba': a = f"Același living înainte și după montarea chenarelor din {inf['short']}"
            else:
                lab = f" — {sc['tag'][2].lower()} {it['c']} în amenajare" if sc.get('tag') else f" — {pk['scurt']} în amenajare"
                a = sc['title'].rstrip('.') + lab
        alts.append((f, a))
    tags = sorted(set(k['kw_primar'] + k['kw_secundar'][:3] + [it['c'].lower(), 'deco flair', 'kit ' + pk['scurt'].split(' ')[0].lower()]))
    # ------------- JSON-LD (pentru pagina kitului pe decoflair.ro)
    url = f"https://decoflair.ro/{k['slug']}"
    ld = [{'@context': 'https://schema.org', '@type': 'Product', 'name': pk['titlu'], 'sku': pk['id'], 'brand': {'@type': 'Brand', 'name': 'Deco&Flair'},
           'description': k['intro'], 'category': f"Profile decorative {zona}", 'material': inf['mat'], 'color': culoare.split(',')[0],
           'isRelatedTo': [{'@type': 'Product', 'name': build.P[l['c']]['n'], 'sku': l['c'], 'gtin13': META[l['c']]['ean'], 'url': l['url']} for l in c['linii']],
           'additionalProperty': [{'@type': 'PropertyValue', 'name': a, 'value': b} for a, b in fapte[2:12]],
           'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'RON', 'price': f"{final:.2f}", 'availability': 'https://schema.org/InStock',
                      'itemCondition': 'https://schema.org/NewCondition',
                      'shippingDetails': {'@type': 'OfferShippingDetails', 'shippingRate': {'@type': 'MonetaryAmount', 'value': '0', 'currency': 'RON'},
                                          'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'RO'}}}},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in k['faq']]}]
    return dict(pk=pk, k=k, c=c, final=final, cont=cont, seo_title=seo_title, meta=meta, geo=geo, fapte=fapte, desc_html=desc_html,
                desc_txt=desc_txt, atr=atr, alts=alts, tags=tags, ld=ld, url=url)

def md(x):
    pk, k = x['pk'], x['k']
    s = [f"# {pk['kit']} — `{pk['id']}`", '',
         f"**Preț final Trendyol:** {ro(x['final'])} lei (TVA inclus; produse {ro(x['c']['produse'])} + transport {ro(x['c']['transport'])})", '',
         '## 1. Denumire', f"- **Nume kit:** {pk['kit']}", f"- **Titlu Trendyol ({len(pk['titlu'])} caractere):** {pk['titlu']}",
         f"- **Nume scurt:** {pk['scurt']}", f"- **Cod kit (SKU):** {pk['id']}", '',
         '## 2. Descriere Trendyol (text — pentru câmpul „Descriere”)', '```', x['desc_txt'], '```', '',
         '## 3. Descriere HTML (dacă editorul acceptă HTML)', '```html', x['desc_html'], '```', '',
         '## 4. Puncte-cheie (bullet points)'] + [f'- {b}' for b in k['bullets']] + ['',
         '## 5. Atribute (de completat în panoul Trendyol)', '| Atribut | Valoare |', '|---|---|'] + [f'| {a} | {b} |' for a, b in x['atr'].items()] + ['',
         '## 6. SEO', f"- **Cuvinte cheie principale:** {kw_line(k['kw_primar'])}", f"- **Secundare:** {kw_line(k['kw_secundar'])}",
         f"- **Long-tail:** {', '.join(k['kw_longtail'])}", f"- **Etichete / tag-uri:** {', '.join(x['tags'])}",
         f"- **SEO title ({len(x['seo_title'])} car.):** {x['seo_title']}", f"- **Meta description ({len(x['meta'])} car.):** {x['meta']}",
         f"- **Slug (pagină decoflair.ro):** `{k['slug']}`", f"- **H1:** {pk['titlu']}", '',
         '## 7. GEO — rezumat pentru motoare AI (ChatGPT, Gemini, Perplexity, AI Overviews)', x['geo'], '', '**Fapte cheie (format citabil):**'] + \
        [f'- **{a}:** {b}' for a, b in x['fapte']] + ['', '## 8. AEO — întrebări și răspunsuri directe'] + \
        [f"**{q}**  \n{a}\n" for q, a in k['faq']] + ['## 9. Text alternativ imagini (ordinea Trendyol)'] + \
        [f'{i+1}. `{f}` — {a}' for i, (f, a) in enumerate(x['alts'])] + ['',
         '## 10. JSON-LD (pentru pagina kitului pe decoflair.ro)', '```json', json.dumps(x['ld'], ensure_ascii=False, indent=1), '```', '']
    return '\n'.join(s)

GHID = """# Ghid de listare și optimizare — Kituri Deco&Flair pe Trendyol

## Cum se folosește
Fiecare kit are un fișier `content/<cod>.md` cu: denumire, titlu Trendyol, descriere (text + HTML), puncte-cheie, atribute,
SEO (cuvinte cheie cu volume Semrush RO, title, meta, slug), GEO (rezumat factual), AEO (FAQ), alt-text imagini și JSON-LD.
`content/trendyol-upload.csv` are toate câmpurile pe un rând per kit (Excel, separator `;`).

## Strategia de titlu (Trendyol + Google)
Formula: **Set [cantitate] [termenul cel mai căutat] [model] [termen secundar] [dimensiune] [+ accesoriu] [total ml]**.
Termenul cu cel mai mare volum stă la începutul titlului (Trendyol taie titlul în listă după ~60 caractere).
Volume lunare Google România (Semrush, noiembrie 2026) folosite la alegere:

| Kit | Termen principal în titlu | Volum/lună |
|---|---|---:|
| Cornișă Z11 | cornisa tavan / baghete tavan | 1.300 / 720 |
| Plintă FD3 | plinta parchet / plinta alba / plinta polimer | 5.400 / 1.300 / 1.000 |
| Baghete WL1 | baghete decorative perete / bagheta decorativa / chenare decorative | 480 / 590 / 210 |
| Cornișă LED IL13 | banda led tavan / profil led tavan / cornisa led | 590 / 480 / 210 |
| Colțar NCL107 | coltare polistiren / profile decorative exterior | 590 / 1.300 |
| Ancadrament NA105 | ancadramente ferestre / ancadrament fereastra | 1.300 / 390 |
| Cornișă NC104 | cornise exterior / profile decorative exterior | 110 / 1.300 |
| Brâu REMA1 | profile decorative exterior / brau decorativ | 1.300 / 210 |

„adeziv polistiren exterior” (880/lună) apare în descrierile kiturilor cu ADRO-FIX. „chenare perete”, „caroiaje perete”,
„brau fatada”, „cornisa fatada” au volum zero în Google RO — folosește-le doar în text, nu în titlu.

## GEO (Generative Engine Optimization) — să fii citat de AI
- Folosește aceeași denumire peste tot (Trendyol, decoflair.ro, social): „Kit Chenare & Tablouri WL1 — 8 baghete, 16 ml”.
- Paragraful GEO din fiecare fișier este autonom: are produsul, cantitatea, dimensiunile, materialul, acoperirea, prețul și data. Pune-l primul pe pagina kitului de pe decoflair.ro.
- Lista „Fapte cheie” e făcută pentru extragere automată (atribut: valoare). Păstrează cifrele exacte.
- Publică pe decoflair.ro câte o pagină per kit (slug-urile sunt propuse) cu JSON-LD Product + FAQPage, apoi leagă din articolele de blog relevante (chenare decorative, cornișă LED, fațade).

## AEO (Answer Engine Optimization) — răspunsuri directe
- Întrebările din FAQ sunt formulate cum caută oamenii („Câte cornișe îmi trebuie pentru o cameră?”); răspunsul începe direct cu informația, în 1–3 propoziții.
- Pe Trendyol, FAQ-ul intră la finalul descrierii; pe decoflair.ro, marchează-l cu JSON-LD FAQPage (inclus).
- Răspunde la întrebările clienților din Trendyol (secțiunea Întrebări) folosind aceleași formulări.

## Reguli Trendyol de reținut
- Imagini: 1200×1800, fără preț, fără date de contact sau link-uri; prima imagine = coperta kitului. Max. 8 imagini.
- Barcode: kitul are nevoie de un cod de bare propriu (nu folosi EAN-ul unui singur profil). Codul kitului (`P01-Z11x5` etc.) poate fi folosit ca cod vânzător.
- Marca: listează sub marca pentru care contul are aprobare (de ex. Deco&Flair). Mărcile producătorilor (NMC, WALLSTYL®, ARSTYL®, ADRo®) apar doar în descriere, ca informație.
- Categoria: alege în panou categoria de profile/decorațiuni pentru perete și tavan (interior) sau materiale de fațadă (exterior); atributele din fișiere se potrivesc cu câmpurile cerute.
- Garanție: 24 de luni, garanția legală de conformitate.
- Prețul final nu include comisionul Trendyol.

## De verificat înainte de publicare
- Codul „WL12” cerut nu există pe decoflair.ro; s-a folosit WL1.
- Z11: textul de pe site spune „poliuretan ARSTYL®”, iar tabelul de atribute de pe aceeași pagină spune „polimer dur”. S-a folosit poliuretan (gama ARSTYL®).
- Ț ara de origine nu e menționată pe site; completeaz-o din documentele de la furnizor.
"""

def main():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(os.path.join(OUT, 'jsonld'))
    xs = [kit_content(pk) for pk in build.PK]
    rows = []
    for x in xs:
        pk = x['pk']
        open(os.path.join(OUT, pk['id'] + '.md'), 'w').write(md(x))
        json.dump(x['ld'], open(os.path.join(OUT, 'jsonld', pk['id'] + '.json'), 'w'), ensure_ascii=False, indent=1)
        rows.append({'Cod kit (SKU)': pk['id'], 'Nume kit': pk['kit'], 'Titlu Trendyol': pk['titlu'], 'Preț final (lei)': ro(x['final']),
                     'Descriere (text)': x['desc_txt'], 'Descriere (HTML)': x['desc_html'],
                     'Puncte-cheie': ' | '.join(x['k']['bullets']), **{'Atribut: ' + a: b for a, b in x['atr'].items()},
                     'Cuvinte cheie principale': ', '.join(x['k']['kw_primar']), 'Cuvinte cheie secundare': ', '.join(x['k']['kw_secundar']),
                     'Long-tail': ', '.join(x['k']['kw_longtail']), 'Etichete': ', '.join(x['tags']),
                     'SEO title': x['seo_title'], 'Meta description': x['meta'], 'Slug': x['k']['slug'], 'Rezumat GEO': x['geo'],
                     'FAQ': ' || '.join(f'{q} — {a}' for q, a in x['k']['faq']),
                     'Imagini + alt text': ' | '.join(f"{pk['id']}/{f} = {a}" for f, a in x['alts'])})
    with open(os.path.join(OUT, 'trendyol-upload.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';'); w.writeheader(); w.writerows(rows)
    open(os.path.join(OUT, 'GHID-LISTARE-SEO-GEO-AEO.md'), 'w').write(GHID.replace('Ț ara', 'Țara'))
    open(os.path.join(OUT, 'TOATE-KITURILE.md'), 'w').write('\n\n---\n\n'.join(md(x) for x in xs))
    for x in xs: print(x['pk']['id'], len(x['desc_txt']), 'car. descriere ·', len(x['meta']), 'car. meta ·', len(x['seo_title']), 'car. title')

if __name__ == '__main__':
    main()

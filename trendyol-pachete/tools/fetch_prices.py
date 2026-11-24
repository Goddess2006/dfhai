"""Citeste live pretul de pe pagina fiecarui produs decoflair.ro (refoloseste parserul din calculator).
Pret neredus = pretul vechi (taiat) daca produsul e la oferta, altfel pretul curent.
Rulare: python3 tools/fetch_prices.py -> data/produse.json"""
import json, os, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '..', 'nmc-calculator-oferta', 'tools'))
import scrape
CFG = scrape.SITES['decoflair']
SLUGS = {
 'Z11': 'plinta-decorativa-tavan-arstyl-z11',
 'FD3': 'plintafd3-wallstyl',
 'WL1': 'brau-decorativwl1-wallstyl',
 'IL13': 'cornisa-led-il13-80x52x2000',
 'NCL107': 'coltar-exterior-decorativ-polistiren-ncl107-1000x30x300',
 'NA105': 'ancadrament-decorativ-na105',
 'NC104': 'cornisa-decorativa-exterior-nc104-220x80x2000',
 'REMA1': 'brau-decorativ-polistiren-adro-decor-rema1-140x30x2000',
 'Adro-Quartz1.5': 'rasina-adro-quartz',
 'Adro-Fix4': 'adeziv-lipire-adro-fix-4-kg',
}
out = {}
for code, slug in SLUGS.items():
    url = CFG['base'] + slug
    r = scrape.parse(url, scrape.get(url), CFG)
    r['regular'] = r['o'] or r['p']
    r['citit'] = datetime.date.today().isoformat()
    out[code] = r
    print(f"{code:15} curent {r['p']:>8} vechi {r['o']} -> neredus {r['regular']} stoc {r['s']} | {r['n']}")
json.dump(out, open(os.path.join(ROOT, 'data', 'produse.json'), 'w'), ensure_ascii=False, indent=1)

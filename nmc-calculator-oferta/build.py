"""Genereaza index.html (fisier unic, se deschide direct in browser) din template.html + data/catalog.json + logo."""
import base64, json, os, datetime
D = os.path.dirname(os.path.abspath(__file__))
cat = json.load(open(os.path.join(D, 'data', 'catalog.json')))
logo = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(D, 'data', 'nmc-logo.png'), 'rb').read()).decode()
date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(D, 'data', 'catalog.json'))).strftime('%d.%m.%Y')
html = open(os.path.join(D, 'template.html'), encoding='utf8').read()
html = html.replace('__CATALOG__', json.dumps(cat, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
html = html.replace('__LOGO__', logo).replace('__DATA_PRETURI__', date)
open(os.path.join(D, 'index.html'), 'w', encoding='utf8').write(html)
print('index.html', len(cat), 'produse,', len(html) // 1024, 'KB')

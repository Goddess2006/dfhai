"""Genereaza calculatorul (fisier unic, offline) cu doua foi: NMC Romania si Deco&Flair.
Iesire: index.html si Calculator-Oferta.html (identice)."""
import base64, json, os, datetime
D = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(D, *a)
def cat(f): return json.dumps(json.load(open(P('data', f))), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
def date(f): return datetime.datetime.fromtimestamp(os.path.getmtime(P('data', f))).strftime('%d.%m.%Y')
def png(f): return 'data:image/png;base64,' + base64.b64encode(open(P('data', f), 'rb').read()).decode()
lib = lambda f: open(P('data', 'lib', f), encoding='utf8').read()
font = lambda f: base64.b64encode(open(P('data', 'lib', f), 'rb').read()).decode()
libs = '<script>' + lib('jspdf.umd.min.js') + '</script>\n<script>' + lib('jspdf.plugin.autotable.min.js') + '</script>\n'
libs += '<script>const FONT_R="%s",FONT_B="%s";</script>' % (font('Roboto-Regular.ttf'), font('Roboto-Bold.ttf'))
html = open(P('template.html'), encoding='utf8').read()
for k, v in {'__LIBS__': libs, '/*__EXPORT__*/': open(P('export.js'), encoding='utf8').read(),
             '__CATALOG_NMC__': cat('catalog.json'), '__CATALOG_DF__': cat('catalog-decoflair.json'),
             '__LOGO_NMC__': png('nmc-logo.png'), '__LOGO_DF__': png('logo-decoflair.png'),
             '__DATE_NMC__': date('catalog.json'), '__DATE_DF__': date('catalog-decoflair.json')}.items():
    assert k in html, k
    html = html.replace(k, v)
for name in ('index.html', 'Calculator-Oferta.html'):
    open(P(name), 'w', encoding='utf8').write(html)
print('OK', len(html) // 1024, 'KB')

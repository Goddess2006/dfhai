"""Generează Analiza-Magazin-Online.html (fișier unic, offline): template.html + app.js + biblioteca xlsx (export Excel)."""
import os
D = os.path.dirname(os.path.abspath(__file__))
lib = open(os.path.join(D, '..', 'nmc-calculator-oferta', 'data', 'lib', 'xlsx.full.min.js'), encoding='utf8').read().replace('�', '\\ufffd')
html = open(os.path.join(D, 'template.html'), encoding='utf8').read()
app = open(os.path.join(D, 'app.js'), encoding='utf8').read()
html = html.replace('__LIBS__', '<script>' + lib + '</script>').replace('/*__APP__*/', app.replace('</script', '<\\/script'))
open(os.path.join(D, 'Analiza-Magazin-Online.html'), 'w', encoding='utf8').write(html)
print('OK', len(html) // 1024, 'KB')

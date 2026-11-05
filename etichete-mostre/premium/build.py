"""Generate both A4 sheets from a common source, preserving Claude's artwork."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
original=(ROOT.parent/'etichete-baghete-A4.html').read_text()
# Keep the original vector QR, add the required 4-module white quiet zone.
qr=re.search(r'<svg class="qr".*?</svg>',original,re.S).group(0)
qr=qr.replace('viewBox="0 0 29 29"','viewBox="-4 -4 37 37" role="img" aria-label="Colecția de baghete pe decoflair.ro"')
qr=qr.replace('<path ', '<rect x="-4" y="-4" width="37" height="37" fill="white"/><path fill="black" ')
icons=[('Ultraușoare','M20 4C12 2 5 6 5 13c0 4 4 6 7 3 3-2 4-6 8-12zM4 21l10-11'),('Montaj rapid','M4 20l6-6M14 4l6 6-8 8-6-6z'),('Se vopsesc','M4 6h13v5H4zM17 8.5h3v5h-9v3M11 16.5v4')]
perks=''.join(f'<div class="perk"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg>{t}</div>' for t,d in icons)
profiles=''.join(f'<figure><svg class="sec" data-p="{i}" viewBox="0 0 40 40" aria-hidden="true"></svg><figcaption>{t}</figcaption></figure>' for i,t in enumerate(['Concav','Clasic','Modern','Minimalist','Elegant']))
label=f'''<article class="label"><div class="frame">
<header class="brand"><img class="logo" src="../logo-decoflair.png" alt="Deco&amp;Flair"><div class="collection"><b>Colecție interior</b><br>Paletar de mostre</div></header>
<h1>Baghete de tavan</h1><p class="sub">din polistiren</p>
<div class="art"><svg class="room" viewBox="0 0 300 170" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ilustrație de montaj: baghete la îmbinarea dintre perete și tavan"></svg><span class="art-caption">Eleganță în fiecare detaliu.</span></div>
<div class="perks">{perks}</div>
<section class="secs"><div class="sech">Secțiuni de profil<span>Forme ilustrative</span></div><div class="secrow">{profiles}</div></section>
<footer class="foot"><a href="https://decoflair.ro/bagheta-polistiren" aria-label="Descoperă întreaga colecție">{qr}</a><div class="contact"><a class="website" href="https://decoflair.ro">decoflair.ro</a><div class="phone"><a href="tel:+40723300603">0723 300 603</a></div><div class="seller"><strong>Vânzător: Deco &amp; Flair Hub SRL</strong><br>Str. Făurei nr. 1, sector 1, București</div><div class="legal">CUI RO 54681700 · J2026031505008</div></div></footer>
</div></article>'''
for theme,title in [('mono','Alb-negru'),('color','Color premium')]:
 html=f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Baghete de tavan — {title} — Deco&amp;Flair</title><link rel="stylesheet" href="design.css"></head><body class="{theme}"><main class="sheet">{label*4}</main><script src="assets/artwork.js"></script></body></html>'''
 (ROOT/f'etichete-{theme}-A4.html').write_text(html)
print('Generated two A4 sheets, four labels each.')

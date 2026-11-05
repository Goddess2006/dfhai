"""Generate both A4 sheets from a common source, using one ambient visual and one illustrative profile."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
original=(ROOT.parent/'etichete-baghete-A4.html').read_text()
# Keep the original vector QR, add the required 4-module white quiet zone.
qr=re.search(r'<svg class="qr".*?</svg>',original,re.S).group(0)
qr=qr.replace('viewBox="0 0 29 29"','viewBox="-4 -4 37 37" role="img" aria-label="Colecția de baghete pe decoflair.ro"')
qr=qr.replace('<path ', '<rect x="-4" y="-4" width="37" height="37" fill="white"/><path fill="black" ')
label=f'''<article class="label"><div class="frame">
<header class="brand"><img class="logo" src="../logo-decoflair.png" alt="Deco&amp;Flair"><div class="collection"><b>Design interior</b></div></header>
<h1>Baghete de tavan</h1><p class="sub">din polistiren</p>
<div class="art"><img class="ambient" src="assets/ambient-interior.png" alt="Ambient de inspirație: living luminos cu baghetă albă la îmbinarea dintre perete și tavan"><span class="art-caption">Ambient de inspirație</span></div>
<section class="detail"><svg class="profile-detail" viewBox="0 0 48 48" role="img" aria-label="Detaliu ilustrativ de secțiune"><path d="M7 7H41V41" class="guide"/><path d="M9 7H41V39H37V35C21 32 16 24 14 14H9Z" class="profile-shape"/></svg><div><h2>Un detaliu. Un interior complet.</h2><p>O trecere elegantă între perete și tavan.</p><small>Secțiune ilustrativă</small></div></section>
<p class="benefits">Ultraușoare <span>·</span> Montaj rapid <span>·</span> Se vopsesc</p>
<footer class="foot"><a href="https://decoflair.ro/bagheta-polistiren" aria-label="Descoperă întreaga colecție">{qr}</a><div class="contact"><a class="website" href="https://decoflair.ro">decoflair.ro</a><div class="phone"><a href="tel:+40723300603">0723 300 603</a></div><div class="depot">Depozit: Chiajna-Ilfov</div></div></footer>
</div></article>'''
for theme,title in [('mono','Alb-negru'),('color','Color premium')]:
 html=f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Baghete de tavan — {title} — Deco&amp;Flair</title><link rel="stylesheet" href="design.css"></head><body class="{theme}"><main class="sheet">{label*4}</main></body></html>'''
 (ROOT/f'etichete-{theme}-A4.html').write_text(html)
print('Generated two A4 sheets, four labels each.')

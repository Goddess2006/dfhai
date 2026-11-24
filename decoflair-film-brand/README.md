# Film de prezentare Deco&Flair: „Detaliile care fac casa.”

**Fișier:** `out/decoflair-film-prezentare.mp4`: 1920×1080 (16:9), 57,6 s, 30 fps, H.264 + AAC 256 kbps, cu muzică ambientală originală.
**Utilizare:** YouTube (canal + trailer de canal), pagina principală / „Despre noi” de pe decoflair.ro, prezentări pentru parteneri, semnătură de e-mail (link), „carte de vizită” video.

## Povestea (manifest de brand)
De la peretele gol la casa care spune cine ești. Cinci capitole, cinci familii de produse, un singur fir: **detaliul**.

| Timp | Imagine (fotografii reale) | Text |
|---|---|---|
| 0:00 | Zugrav la un perete gol | *Fiecare casă începe cu un perete gol.* |
| 0:05 | Montaj real de cornișă | *Noi vedem ce poate deveni.* |
| 0:09 | Diptic: cameră albastră cu chenare / perete gri cu chenar | **PROPORȚIE**: *Linii care dau ordine unei încăperi.* (chenare · brâuri · plinte) |
| 0:14 | Cornișă cu LED (foto NMC) | **LUMINĂ**: *Lumina care nu se vede. Se simte.* (cornișe și scafe cu LED) |
| 0:18 | Macro riflaj stejar | **TEXTURĂ**: *Materie caldă, pe care o atingi cu privirea.* (riflaje · panouri 3D) |
| 0:23 | Diptic: panou FLOWER / WAVE | *Pereți care prind viață în lumină.* |
| 0:27 | Diptic: Dolce & Gabbana leopard / Roberto Cavalli | **CARACTER**: *Un perete care spune cine ești.* (tapet de colecție) |
| 0:32 | Coloane reale pe fațadă (foto NMC) | **PREZENȚĂ**: *Afară, o fațadă care rămâne.* (profile de exterior) |
| 0:36 | Diptic: conac / clădire cu ancadramente | *Case care se recunosc din stradă.* |
| 0:41 | Living cu cornișă LED (foto NMC) | *Pentru cei care nu se mulțumesc cu „destul de bine”.* |
| 0:45 | Diptic: rozetă / perete TV cu chenare | *Consultanță. Randări 3D. Livrare în toată țara.* |
| 0:50 | Sigla Deco&Flair, particule, inel de lumină | **decoflair.ro**: *Detaliile care fac casa.* · Consultanță gratuită · 0765 740 280 |

**Semnătura Deco&Flair:** sigla originală (aripa aurie), auriu `#C2A15E` / `#E2CB94` pe cărbune, serif italic Cormorant, format cinematografic 2,39:1, tranziții prin ceață caldă și reflexe de lumină, particule aurii, granulație de film.

## Muzica
Compoziție ambientală **originală**, generată pentru acest film (`music.py`): pad-uri calde în Re major (Dmaj9 → Bm11 → Gmaj9 → Asus2), note rare de pian, bas profund, reverb lung, acord larg și „clopoțel” la apariția siglei. Nu folosește materiale ale terților, deci nu primește reclamații Content ID pe YouTube.
Dacă vreți o piesă de studio: YouTube Audio Library (filtru „Ambient / Calm”) sau Artlist / Epidemic Sound (licență comercială). Înlocuiți `out/muzica.wav` și rulați din nou `node render.cjs`.

## YouTube
- **Titlu:** Deco&Flair: Detaliile care fac casa | Profile decorative, tapet de colecție, panouri 3D
- **Descriere:**
  > Fiecare casă începe cu un perete gol. Noi vedem ce poate deveni.
  > Deco&Flair aduce în casa ta detaliile care fac diferența: profile decorative pentru interior și exterior, cornișe și scafe cu LED, riflaje acustice, panouri 3D și tapet de colecție Dolce & Gabbana și Roberto Cavalli.
  > Consultanță gratuită · Randări 3D · Livrare în toată țara
  > 🔗 https://decoflair.ro · 📞 0765 740 280
  >
  > 0:00 Peretele gol
  > 0:09 Proporție: chenare, brâuri, plinte
  > 0:14 Lumină: cornișe și scafe cu LED
  > 0:18 Textură: riflaje și panouri 3D
  > 0:27 Caracter: tapet de colecție
  > 0:32 Prezență: profile de exterior
  > 0:50 decoflair.ro
- **Etichete:** decoflair, deco flair, profile decorative, cornisa led, scafa led, riflaje, panouri 3d, tapet premium, tapet dolce gabbana, tapet roberto cavalli, profile exterior, fatade, design interior, amenajari interioare
- **Miniatură:** cadrul de la 0:28 (dipticul leopard / Cavalli) sau finalul cu sigla (`out/miniatura.jpg`).
- Setați-l ca **trailer de canal** pentru vizitatorii noi.

## Pe site (decoflair.ro)
După încărcarea pe YouTube, în OpenCart → Journal → modul HTML (pagina principală sau „Despre noi”):
```html
<div style="position:relative;padding-top:56.25%;border-radius:12px;overflow:hidden">
  <iframe src="https://www.youtube-nocookie.com/embed/ID_VIDEO?rel=0&modestbranding=1&playsinline=1"
          title="Deco&Flair: Detaliile care fac casa" loading="lazy"
          style="position:absolute;inset:0;width:100%;height:100%;border:0"
          allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
```
Înlocuiți `ID_VIDEO` cu ID-ul de pe YouTube.

## Surse foto
Portofoliul decoflair.ro (`/portofoliu`), fotografiile NMC din blog și din categoriile decoflair.ro, fotografiile de ambient Arstyl de pe paginile de produs, cataloagele Dolce & Gabbana și Roberto Cavalli de pe paginile de produs. Imaginile mai mici de 1600 px sunt mărite 2× (Lanczos + claritate fină). **EXTRANET nu a fost accesibil din cloud.** Originalele HQ de acolo pot înlocui orice fișier din `assets/` cu același nume.

Rulare: `python3 film.py && python3 music.py && node render.cjs` · previzualizare: `node preview.cjs 2,10,30`

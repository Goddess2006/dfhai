# Black Friday pe OpenCart 3 — instalare

Fișiere:

- `descriere-pagina-informatii.html` — codul landing-ului (CSS + HTML + JS), gata de lipit.
- `imagini-black-friday.zip` — cele 14 fotografii folosite de landing.
- `build.py` — regenerează codul din `../index.html` după orice modificare (`python3 black-friday/opencart/build.py`).

## 1. Încarcă imaginile

Imaginile trebuie să ajungă în `image/catalog/black-friday/` pe server. Codul le caută la `/image/catalog/black-friday/ext0.jpg` etc.

- Din admin: deschide orice editor (ex. Catalog > Informații > Adaugă) > butonul de imagine > Image Manager > creează folderul `black-friday` > intră în el > Upload > selectează toate cele 14 fișiere din arhivă.
- Sau prin FTP / File Manager din hosting: dezarhivează în `public_html/image/catalog/black-friday/`.

## 2. Creează pagina

Catalog > Informații > **Adaugă**:

- **Titlu informație:** `Black Friday` (titlul nu se afișează pe pagină; e ascuns de cod, landing-ul are titlul lui).
- **Descriere:** apasă butonul **Cod sursă `</>`** din bara editorului, șterge tot ce e acolo, lipește tot conținutul fișierului `descriere-pagina-informatii.html`, apoi apasă din nou `</>` și salvează. Nu edita textul în modul vizual, pentru că editorul poate modifica structura.
- **Meta Tag Title:** `Black Friday NMC România — profile, tapet și adeziv`
- **Meta Tag Description:** `Profile decorative de exterior și interior, tapet de designer și adeziv ADRO-FIX. Selecția NMC România pentru Black Friday.`
- Tab **SEO:** cuvânt cheie `black-friday` → pagina va fi la `https://www.nmcromania.ro/black-friday`.
- Tab **Date:** Stare = Activat. Bifează „Bottom” doar dacă vrei link în footer.

## 3. Verifică

Deschide pagina. Dacă:

- **pagina apare albă/neformatată sau ca text** — editorul a eliminat blocul `<style>`. Vezi „Dacă editorul elimină codul” mai jos.
- **imaginile lipsesc** — verifică că fișierele sunt exact în `image/catalog/black-friday/` (litere mici, extensia `.jpg`).
- **după salvare nu se vede schimbarea** — Extensii > Modificări > Refresh și golește cache-ul temei (Dashboard > rotița albastră > Theme și SASS).

Căutarea din bara de categorii și evidențierea categoriei active folosesc JavaScript. Dacă editorul elimină `<script>`, pagina funcționează în continuare; doar căutarea nu mai filtrează.

## Dacă editorul elimină codul

Unele versiuni ale editorului Summernote din OpenCart 3 curăță `<style>` sau `<script>` la salvare. Variante:

1. **Dezactivează temporar editorul:** unele teme/extensii au opțiune pentru asta; sau folosește o extensie gratuită de tip „Disable Summernote / CKEditor for OpenCart 3”.
2. **Introdu codul direct în baza de date** (phpMyAdmin): tabela `oc_information_description`, rândul paginii, câmpul `description`. OpenCart salvează textul cu entități HTML, deci lipește codul trecut prin `htmlspecialchars` (sau cere-mi un fișier SQL gata făcut, cu `information_id`-ul paginii).
3. **Modulul „HTML Content”** (Extensii > Module > HTML Content) are același editor, deci aceeași problemă; nu e o soluție.

## Actualizarea prețurilor

Prețurile sunt scrise static în HTML (preluate din magazin la 04.11.2026). Când se schimbă, editează `black-friday/index.html` (și `catalog.json`), rulează `build.py` și relipește codul în pagină.

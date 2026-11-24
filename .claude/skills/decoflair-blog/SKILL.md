---
name: decoflair-blog
description: Scrie, ilustrează, încarcă și programează articole pe blogul decoflair.ro (OpenCart + Journal3 Blog) — cercetare de cuvinte cheie, articol SEO în română cu linkuri spre produse, imagini (catalog + AI), urcare imagini în Image Manager, creare articol nepublicat în admin, previzualizare, publicare la ora programată, apoi derivate (reel, carusel, newsletter). Folosește-l pentru „articol de blog”, „programează blogul”, „urcă articolul pe site”, „calendar editorial”, „SEO blog”.
---

# Blog Deco&Flair: de la idee la publicat

Skill-uri folosite: `content-strategy` (calendar, clustere), `seo-audit` / `ai-seo` / `schema`, `copywriting` + `copy-editing`, `decoflair-catalog`, `decoflair-media-gen`, `decoflair-social-pipeline`, `decoflair-newsletter`. Cercetarea de cuvinte cheie: conectorul Semrush (baza `ro`), dacă e conectat; altfel Google autocomplete + „People also ask”.

## Acces la admin
Script: `scripts/opencart_blog.cjs` (Node + Playwright, deja instalate în container). Citește din mediu `DECOFLAIR_ADMIN_URL`, `DECOFLAIR_ADMIN_USER`, `DECOFLAIR_ADMIN_PASS`. Nu le cere niciodată în chat și nu le scrie în fișiere.
Utilizator recomandat: unul dedicat („claude-blog”), într-un grup OpenCart cu drept de acces/modificare doar pe Journal3 și Image Manager.

**Prima rulare (o singură dată):** `login-test`, apoi `capture`: înregistrează cererile reale ale editorului Journal3, fără să modifice ceva. Compară cu rutele implicite din script; dacă diferă, scrie `scripts/endpoints.json` (`list/get/add/edit/bodyMode`). Apoi `get --id 31 --out sablon.json` (un articol existent) = șablonul de câmpuri pentru articolele noi. Până nu e făcut acest pas, `create`/`set-status` nu sunt confirmate.

## Flux pe articol (folder `blog/<slug>/`)
1. **Subiect + cuvânt cheie** — întrebări reale ale clienților, sezon (primăvară = fațade, toamnă = interior), clusterele existente (cornișe, chenare, fațade, montaj, LED). Verifică să nu dubleze un articol existent (`https://decoflair.ro/blog`).
2. **Plan** — titlu (≤60 caractere), slug fără diacritice, meta descriere (≤155), H2/H3, 3–6 produse reale din `decoflair-catalog`, linkuri interne spre 2–3 articole vechi.
3. **Articol** — 1.200–2.000 de cuvinte, română cu diacritice, ton din `.agents/product-marketing.md`; răspuns direct în primul paragraf (bun pentru AI Overviews), tabel cu dimensiuni/proporții unde ajută, secțiune „Întrebări frecvente”, CTA spre produse. HTML curat: `<h2>`, `<p>`, `<ul>`, `<table>`, `<img>` cu `alt` descriptiv.
4. **Imagini** — 1 principală 1200×675 (și pentru social), 3–6 în text, WebP/JPEG < 200 KB; poze reale de catalog + ambient AI (`decoflair-media-gen`). Nume de fișier descriptive (`cornisa-led-living-tavan.webp`).
5. **Aprobare** — proprietarul primește articolul (Artifact/pagină de previzualizare) și data propusă.
6. **Încărcare** (după „da”):
   ```bash
   B=.claude/skills/decoflair-blog/scripts/opencart_blog.cjs
   node $B upload --dir blog/<slug> blog/<slug>/img/*.webp
   node $B create --json blog/<slug>/post.json      # status 0 = nepublicat
   ```
   `post.json` = `sablon.json` cu titlu, conținut, meta, slug (keyword), imagine, categorie, produse legate și `status: 0` completate.
7. **Programare** — la ora aleasă, o sesiune programată (scheduled task Claude Code) rulează `node $B set-status --id <id> --status 1`, apoi `screenshot` pe URL-ul public ca verificare și notează în `HANDOFF.md`.
8. **Derivate** — din articol: reel/carusel (`decoflair-social-pipeline`), bloc în newsletter, pin Pinterest.

## Reguli
- Nimic publicat fără aprobarea proprietarului; creează întâi nepublicat.
- Nu șterge și nu edita articole existente fără cerere explicită.
- Fără afirmații tehnice inventate (rezistențe, garanții): doar ce e pe pagina produsului sau confirmat de proprietar.

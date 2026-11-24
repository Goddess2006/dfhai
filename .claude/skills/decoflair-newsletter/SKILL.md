---
name: decoflair-newsletter
description: Creează și trimite newsletterul Deco&Flair — alege tema și produsele, scrie textele, construiește e-mailul HTML responsive (600 px, stiluri inline, UTM), urcă imaginile, creează campania în Brevo ca draft, trimite test, programează; plus fluxuri automate (bun venit, coș abandonat, revenire). Folosește-l pentru „newsletter”, „campanie e-mail”, „trimite e-mail clienților”, „secvență de e-mailuri”, „Brevo”.
---

# Newsletter Deco&Flair

Model de pornire: `decoflair-newsletter-nmc/` (build.py → HTML pentru Brevo/MailerLite/theMarketer, text simplu, imagini optimizate, `GHID-TRIMITERE.md`). Skill-uri: `emails` (secvențe, subiecte), `copywriting`, `copy-editing`, `decoflair-catalog`, `decoflair-media-gen`.

## Ritm recomandat (solopreneur)
- **1 newsletter la 2 săptămâni**: 1 idee principală (ghid/tendință) + 3–4 produse + 1 CTA. Marți sau joi, 9:30–10:30.
- **Fluxuri automate** (se configurează o dată în Brevo → Automations): bun venit (3 e-mailuri: cine suntem / ghid gratuit de alegere a profilelor / cele mai vândute), coș abandonat (1 h + 24 h; necesită integrarea magazinului), revenire după comandă (montaj, apoi „ce mai poți face” la 30 de zile), reactivare la 6 luni. `emails` scrie textele.

## Flux campanie (folder `newsletter/<AAAA-MM-DD>/`)
1. Temă + produse (`catalog.py`), prețuri citite în ziua trimiterii.
2. Texte: 3 subiecte (≤45 caractere) + preheader; A/B pe subiect în Brevo.
3. HTML: copiază și adaptează `decoflair-newsletter-nmc/build.py` (tabele, stiluri inline, imagini absolute pe `https://decoflair.ro/image/catalog/newsletter/<luna>/`, UTM `utm_source=newsletter&utm_campaign=<data>&utm_content=<bloc>`). Sub ~100 KB HTML.
4. Imagini: urcate în OpenCart Image Manager (sau CDN-ul Brevo) — fără ele e-mailul e gol.
5. Brevo (cheie `BREVO_API_KEY` în mediu, niciodată în repo):
   ```bash
   S=.claude/skills/decoflair-newsletter/scripts/brevo.py
   python3 $S lists
   python3 $S create --name "NL <data>" --subject "..." --preview "..." --html out/newsletter-brevo.html --list <id> --sender-email <adresa verificată>
   python3 $S test --id <id> --to <adresa proprietarului>
   python3 $S schedule --id <id> --at 2026-12-03T09:30:00+02:00   # doar după „da”
   ```
   `send-now` cere `--yes` și se folosește numai la cererea explicită a proprietarului.
   Alternativ: conectorul oficial Brevo MCP (mcp.brevo.com) sau theMarketer (românesc, integrare OpenCart).
6. După 48 h: `brevo.py stats --id <id>` → deschideri, click-uri; vânzările din GA4 pe `utm_campaign`.

## Reguli
- Doar contacte cu consimțământ (GDPR): abonați din site + clienți cu acord. Link de dezabonare obligatoriu.
- Domeniul expeditorului autentificat (SPF, DKIM, DMARC) înainte de prima trimitere.
- Nu trimite din căsuța office@ pentru liste.

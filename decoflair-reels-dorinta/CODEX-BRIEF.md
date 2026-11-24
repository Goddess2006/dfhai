# Brief pentru Codex: seria „Dorință” (consultare + producție)

**De la:** Claude Code · 24.11.2026 · Folder `decoflair-reels-dorinta/` · Context complet: `README.md`

Clientul vrea reclame care „să-i dea pe spate”, fără aspect AI, cu ambient cald, care să trezească dorința de a cumpăra. Claude a făcut primele două reel-uri (lux / Crăciun) din fotografii reale. **Te rog, în ordine:**

1. **Revizie creativă** (pasul 3 din `FLUX-CREATIV.md`): uită-te la `reel/decoflair-lux-ads.mp4` și `reel/decoflair-craciun-ads.mp4`. Spune unde se pierde atenția și ce replică ai schimba. Notează feedback-ul în `HANDOFF.md`; Claude îl aplică.
2. **Fotografii reale din EXTRANET / BAZE** (Claude nu are acces): cataloage de producători (Arstyl, Wallstyl, ADRo, NMC, Decori&Decori, Emiliana, Roberto Cavalli, Dolce & Gabbana) cu **ambient cald, rezoluție mare, format vertical** dacă există. Copiază doar imagini publicabile în `codex/`, cu un `codex/SURSE.md` (fișier, produs, sursă, drept de folosire).
3. **Mărire 2×, fără să modifici conținutul** (Real-ESRGAN, ca la newsletter): `assets/lux-dg-leopard.jpg`, `assets/lux-dg-majolica.jpg` (957 px), `assets/lux-emiliana.jpg` (831 px), `assets/cr-*.jpg` din portofoliu (900 px). Salvează în `codex/` cu același nume. Apoi în `configs/*.py` schimbă calea `../assets/X` în `../codex/X`.
4. **Sunet:** propune 2–3 piese din bibliotecile Instagram/TikTok (pian lent, cinematic, cald) pentru fiecare reel. Opțional, o voce off caldă în română pe replici (`codex/voce-lux.mp3`, `codex/voce-craciun.mp3`).
5. **Următorul reel din serie** (dacă ai materiale reale): `configs/riflaje.py` sau `configs/linea.py` (LINEA Room Kit, 2.838,30 lei), cu aceeași structură.

**Reguli:** fără imagini generate care par AI în primele 3 secunde; prețuri și stocuri verificate pe site în ziua livrării; fără urgență falsă (de ex. „ultimele bucăți” doar dacă e adevărat).

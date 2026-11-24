# Claude Code

Lucrezi în `/home/dfh/workspace`, același codebase cu Codex. Branch-ul de lucru este `main`.

1. `git checkout main`
2. `git pull --rebase origin main`
3. Citește `HANDOFF.md`.
4. Fă modificările în acest director.
5. Actualizează `HANDOFF.md`.
6. Commit pe `main` cu autorul `Claude Code <claude@dfh-ai-hub>`.
7. `git push origin main`

Dacă push-ul este respins, `git pull --rebase origin main` și push din nou. Rămâi pe `main`. Nu comite secrete.

Documentație și date sursă: `/home/dfh/workspace/BAZE` (baze DistribNet, imagini catalog produse, date suplimentare) și `/home/dfh/workspace/EXTRANET` — vezi `BAZE.md`. Ambele foldere sunt în `.gitignore`: se citesc local, nu se comit.

Când Codex îți cere o consultare creativă, folosește [fluxul creativ comun](FLUX-CREATIV.md). Oferă feedback editorial concret pe brief sau pe versiunea de lucru și lasă implementarea în seama agentului care a cerut revizia.

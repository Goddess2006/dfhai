# Flux creativ comun · Codex și Claude Code

Aplică acest flux fiecărui reel, postări, reclame, banner sau alt material creativ. Construiește o execuție care poate servi drept exemplu pentru alți creatori și care leagă ideea de o acțiune măsurabilă.

## Concepție și revizie

1. **Înainte de producție, consultă Claude Code pe brief.** Include publicul, canalul, produsul sau categoria, obiectivul principal, destinația și restricțiile de brand. Propune ideea, primul cadru sau primul rând, dovada pe care o vei arăta și îndemnul la acțiune. Cere observații concrete despre ce problemă recunoaște publicul din deschidere, ce ar convinge și unde s-ar pierde interesul.
2. **Producție.** Alege o idee clară. Fă produsul recognoscibil și arată schimbarea pe care o aduce printr-un detaliu vizual, o demonstrație sau o comparație înainte și după. Distinge cadrele de inspirație de fotografiile produsului. Folosește expresiile pe care le caută publicul în titlu și în descriere, acolo unde sună firesc. Verifică afirmațiile, prețul, disponibilitatea și destinația când apar în material. Potrivește îndemnul cu obiectivul și locul în care publicul poate acționa.
3. **Înainte de livrare, consultă din nou Claude Code pe versiunea de lucru.** Dă-i textul, ordinea cadrelor și momentele-cheie din montaj sau o previzualizare pe care o poate inspecta. Cere o modificare precisă, cu locul și motivul ei. Verifică sugestiile pe material, aplică ce ajută și controlează formatul final, lizibilitatea pe mobil și traseul până la pagina de destinație. La o serie, revizia poate acoperi mai multe piese dacă fiecare primește feedback identificabil.
4. **La livrare, consemnează în `HANDOFF.md`** obiectivul, modificarea aplicată în urma consultării, destinația și indicatorul principal. Dacă Claude Code nu este disponibil, continuă verificarea, menționează la livrare că etapa de consultare a rămas neconfirmată și păstrează brief-ul concis pentru următoarea revizie.

## Măsurare

Alege **un indicator principal** în funcție de scopul piesei și notează înainte de publicare ipoteza și intervalul de măsurare. Când există rezultate comparabile, notează valoarea de referință și ținta. Urmărește restul ca semnale secundare, când datele sunt disponibile.

| Scop | Ce urmărim |
|---|---|
| Vizibilitate în căutare și recomandări | Trafic din căutare sau recomandări, când canalul îl separă, plus retenție ori vizibilitate pentru tema urmărită |
| Urmăritori | Urmăriri atribuite materialului sau rata lor raportată la audiența unică, când atribuirea este disponibilă |
| Clickuri pe site | Clickuri outbound și sesiuni ale campaniei. Pentru linkuri de campanie, folosește UTM și un `utm_content` distinct pentru fiecare variantă |
| Vânzări | Comenzi finalizate și venit atribuit, când măsurarea permite. Pentru reclame, urmărește și costul per comandă raportat la obiectiv |

Compară materiale cu același obiectiv, pe același canal și într-un interval comparabil. Raportează separat distribuția organică și cea plătită, cu valori distincte pentru `utm_medium` unde avem link de campanie. Pentru un test A/B, schimbă o singură variabilă relevantă, de exemplu primul cadru. În raportare, distinge vizionările și salvările, clickurile și cererile de consultanță, respectiv comenzile finalizate. Marchează limitele de atribuire și incertitudinea când volumul este prea mic pentru o concluzie.

## Consultarea din workspace

Scrie un brief cu informațiile pe care le poți partaja și apelează Claude Code printr-o consultare fără unelte de proiect:

```bash
(cd /tmp && claude --safe-mode --tools "" --no-session-persistence --print < /tmp/decoflair-brief-creativ.txt)
```

Include numai informațiile și materialele pe care le poți partaja. Păstrează datele interne din `BAZE/` și `EXTRANET/` în fluxul local.

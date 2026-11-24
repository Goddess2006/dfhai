# Analiză vânzări „Magazin online” — preț de listă vs. discount 40%

**Deschide `Analiza-Magazin-Online.html` în Chrome sau Edge** (dublu-clic; fișier unic, merge și fără internet) → „Conectează folderul bazei” → alegi o dată folderul DistribNet (`\\rds.nmc.local\Backup\baze` sau `BAZE/…`) → „Permite la fiecare vizită”.

Ce face:
- Ia facturile agentului **MAGAZIN ONLINE** din **septembrie, octombrie, noiembrie** (anul ales), fără clientul **Deco & Flair Hub** (filtrul „Exclude clienții care conțin”, potrivire fără diacritice/semne).
- Pentru fiecare linie caută prețul articolului în **lista de preț la care s-a facturat** (CATPRET de pe linie → de pe factură → al clientului → lista implicită 90), din `preturi.dbf` (PRETVANZ cu TVA → fără TVA; articolele doar în EUR: PRETVAL × curs).
- Afișează pe factură, pe lună și total: facturat (fără TVA), valoarea la listă, discountul real acordat, valoarea dacă se dădea −40% din listă, **diferența = facturat − listă × 60%** (pozitiv = s-a încasat mai mult decât cu −40%).
- Liniile fără preț în listă (transport, servicii) rămân în afara comparației (sau, la alegere, incluse la valoarea facturată) și apar separat.
- **Sincronizare în timp real:** la fiecare 20 s (configurabil) verifică dacă tabelele folosite s-au modificat (mărime + dată) și recalculează singur; și la revenirea în fereastră.
- Agent, perioadă, discount, TVA, curs EUR sunt editabile — devine calculator pentru orice agent/discount. Export Excel (Sumar, Facturi, Linii).
- Datele se citesc doar local, în browser; nu se urcă nicăieri.

Tabelele și câmpurile se detectează automat după numele DistribNet (antet facturi: nr./dată/client/agent/CATPRET; linii: CODPR/CANTIT/PVANZFTVA; client.dbf, agenți, preturi.dbf, denumiri liste, articole). Dacă detecția greșește: „Setări bază” → alegi tabelul/câmpul corect sau „Copiază structura bazei” (doar nume de tabele/câmpuri) și o trimiți pentru configurare exactă.

Limită: `preturi.dbf` are doar prețurile actuale — dacă o listă s-a schimbat după emiterea facturii, comparația se face cu prețul de acum.

Reconstruire după modificări în `app.js` / `template.html`: `python3 build.py`.

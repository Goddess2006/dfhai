---
name: decoflair-social-pipeline
description: Motorul săptămânal de conținut Deco&Flair pentru un solopreneur — planifică săptămâna, alege produsele, produce creativele (imagini, carusele, reels, TikTok), scrie textele pe platformă, pregătește programarea în Postiz sau Meta Business Suite și raportează ce a mers. Folosește-l pentru „conținutul săptămânii”, „calendar de postări”, „programează postările”, „ce postăm”, „batch de conținut”, „raport social media”.
---

# Pipeline social media Deco&Flair

Obiectiv: o singură sesiune pe săptămână (~1 oră din timpul proprietarului: aprobare) → 7–10 postări programate pe Facebook, Instagram, TikTok (+ Pinterest), cu link UTM spre produs.

Skill-uri folosite: `content-strategy` (piloni, calendar), `social` (formate, hook-uri), `ad-creative` (variante pentru reclame), `decoflair-catalog`, `decoflair-media-gen`, `copy-editing`, `postiz:postiz` (programare), `.agents/product-marketing.md` (voce).

## Pilonii de conținut (rotație săptămânală)
1. **Produs în ambient** (2×) — imagine/carusel: problemă → soluție → rezultat.
2. **Know-how** (2×) — „3 greșeli la montajul cornișei”, proporții chenare, ce adeziv; din articolele de blog.
3. **Înainte/după sau transformare** (1×) — reel 9:16.
4. **Fațade** (1×) — ancadramente, brâuri, colțare.
5. **Dovadă socială / proiect client** (1×, când există poze reale) sau ofertă/ campanie (doar la nevoie).
TikTok: aceleași idei ca reels native (hook în prima secundă, text pe ecran, 7–20 s).

## Fluxul săptămânii (folder `social/<AAAA-Www>/`)
1. **Plan** — calendarul în `plan.md`: zi, oră, platformă, pilon, produs, unghi. Ține cont de sezon/campanii (Black Friday, Crăciun, primăvara = fațade).
2. **Produse** — `catalog.py pick --n 7 --seed <AAAA-Www>` sau alese de proprietar; `catalog.py product` pentru date actuale.
3. **Creative** — `decoflair-media-gen` pentru ambient/video; text și logo prin șabloane HTML/Playwright ca în `decoflair-lux-2027/`. Formate: 1080×1350, 1080×1920, 1000×1500.
4. **Texte** — în `posts.csv` (UTF-8): `data,ora,platforma,pilon,fisier_media,text,link`. Pe platformă:
   - Facebook: 2–4 rânduri + link cu UTM.
   - Instagram: hook în primul rând, 5–8 rânduri, CTA „link în bio / scrie-ne în DM”, 3–6 hashtaguri românești de nișă (#amenajariinterioare #designinterior #fatadecase #cornisedecorative).
   - TikTok: 1–2 rânduri + 3 hashtaguri; textul principal e pe video.
   - Link: `https://decoflair.ro/<produs>?utm_source=<platforma>&utm_medium=social&utm_campaign=<AAAA-Www>&utm_content=<cod>`.
5. **Aprobare** — trimite proprietarului galeria (Artifact sau fișiere) + `posts.csv`. Nimic nu pleacă fără „da”.
6. **Programare** (după aprobare):
   - **Postiz** (recomandat; skill `postiz:postiz`, MCP/CLI/API; cloud sau self-host): FB, IG, TikTok, Pinterest, YouTube Shorts dintr-un singur loc.
   - Alternativ gratuit: Meta Business Suite (FB+IG, programare nativă) + TikTok Studio (programare până la 10 zile).
7. **Raport** (luni) — reach, salvări, click-uri, vânzări din GA4 pe `utm_campaign`; ce pilon a mers → ajustează planul. Notează concluziile în `.agents/product-marketing.md` (Changelog).

## Reclame (opțional, buget mic)
- Postarea organică cu cele mai multe salvări/click-uri devine reclamă (Advantage+ pe Meta, Spark Ads pe TikTok) — `ad-creative` scrie 3–5 variante de text.
- Catalog dinamic: feed de produse din OpenCart către Meta Commerce Manager + Pixel deja instalat → reclame de retargeting automate. Necesită un modul de feed în OpenCart (de verificat ce are instalat).

## Reguli
- Fără prețuri pe creative dacă nu se cere; prețul din text se verifică în ziua publicării.
- Diacritice corecte; fără roz/magenta saturat.
- Notează livrabilele în `HANDOFF.md`.

# Brief pentru Codex: imagini pentru reel-ul de exterior „Ultimul final touch înainte de prima zăpadă”

**De la:** Claude Code · **Data:** 24.11.2026 · **Folder:** `decoflair-reel-exterior/`
**Cererea utilizatorului:** reel despre profilele de exterior: livrare rapidă, stocuri mari, ultimul „final touch” la fațadă înainte de prima zăpadă și de sărbători. Trebuie să vândă și să poată fi promovat (reclame Meta/TikTok). Inspirat din short-ul NMC „Colțar decorativ fațade” (NCL107), dar **cu focus pe produs, nu pe actor**.

v1 e randat din imaginile existente (`reel/decoflair-reel-exterior-organic.mp4`, `…-ads.mp4`). Imaginile de produs de pe site sunt randări 3D vechi, bej, pe fundal alb; iar ambientul e din `decoflair-inspiratie-50` (vile mediteraneene, vară). **Lipsesc: iarnă/amurg, case românești reale ca tipologie, produsul fotografiat premium și un „înainte” real.** Te rog generează-le cu ImageGen și pune-le în `decoflair-reel-exterior/codex/` cu numele exacte de mai jos. `reel_build.py` le preia automat (funcția `asset`).

## Reguli
- 1080 × 1920 (9:16), JPEG, **fără text, logo, cifre sau watermark**.
- Tipologie: **casă românească P sau P+1, tencuială decorativă** (crem, bej, gri cald, verde salvie). Fără vile de lux mediteraneene: clientul trebuie să-și recunoască propria casă.
- Profile de exterior din polistiren cu strat de rășină și nisip cuarțos: textură fină, minerală, mată, culoare ivoire/alb cald. Colțarul NCL107 are bosaje: blocuri alternante 300/300 mm, îmbinare în L pe muchie.
- Iarnă timpurie: cer rece de noiembrie/decembrie, primii fulgi sau zăpadă subțire pe pervaz și acoperiș, lumină caldă în ferestre. **Fără Moș Crăciun și fără decor kitsch**; cel mult o ghirlandă discretă sau o coroniță pe ușă.
- Zonele de sus (0–300 px) și de jos (1500–1920 px) să fie liniștite (cer, perete, zăpadă), pentru text și interfața aplicațiilor.

## Lista
| Fișier | Ce arată | Unde intră în reel |
|---|---|---|
| `01-colt-zapada.jpg` | Colțul unei case românești cu **colțare tip bosaje NCL107** ivoire pe tencuială bej-gri, primii fulgi, cer rece, o fereastră caldă alături. Cadru vertical, colțul pe treimea stângă. | Cârligul (0–2 s) |
| `02-colt-inainte.jpg` | **Același colț, același cadru**, FĂRĂ colțare: muchie de tencuială ciupită, ușor strâmbă, colț lovit, aspect neterminat. Fără zăpadă. | Problema (2–4,5 s) |
| `02-colt-dupa.jpg` | Același colț, același cadru, CU colțarele NCL107 montate și vopsite, lumină de după-amiază de noiembrie. | „Așa arată pe casă” (8,5–10 s) |
| `03-fatada-amurg-sarbatori.jpg` | Fațada întreagă a unei case P+1 la amurg albastru, ninsoare ușoară: ancadramente, solbancuri, cornișă și colțare ivoire, ferestre calde, ghirlandă discretă de lumini calde pe streașină. | Urgență / „Casa gata de sărbători” (17–20,5 s) |
| `10-ncl107-studio.jpg` | **Fotografie de produs premium**: un colțar NCL107 (formă de L, 5 bosaje, 1 m înălțime, ivoire, textură minerală) în picioare, pe fundal de studio crem-gri cald, lumină laterală moale, umbră scurtă. Produsul să ocupe ~70% din înălțime, centrat pe orizontală în jumătatea dreaptă. | Eroul de produs (4,6–8,5 s) |
| `11-montaj-coltar.jpg` | Macro: mâini cu mănuși de lucru care apasă un colțar pe muchia unei clădiri, adeziv vizibil, schelă în fundal neclar. | Opțional, pentru versiunea v2 |
| `12-stoc-depozit.jpg` | Rafturi de depozit cu profile decorative albe/ivoire ambalate, multe, ordonate; lumină de depozit curată. Dovada vizuală pentru „stocuri mari”. | Opțional, pentru varianta v2 cu „din stoc” |

## Prompt de bază
> Use case: social-ads, vertical 9:16 1080x1920. Photorealistic photograph of a typical Romanian suburban house (single storey or one upper floor), smooth decorative render facade in [culoare], with ivory architectural exterior mouldings made of EPS coated with a fine mineral quartz-sand resin layer, matte, crisp edges: [DESCRIERE]. Early winter in Romania, cold November–December sky, first light snowflakes, warm 2700K light from windows. Believable, documentary-quality, not CGI, 35mm, eye level. Calm plain areas at top 300 px and bottom 420 px. Absolutely no text, letters, numbers, logos or watermarks.

Pentru perechea 02: generează întâi `02-colt-dupa.jpg`, apoi editează-l pentru `02-colt-inainte.jpg`: *„Same exact corner, camera and light; remove all quoin mouldings; show a slightly chipped, uneven bare render corner edge.”*

## După generare
`cd decoflair-reel-exterior && python3 reel_build.py && node reel_render.cjs organic && node reel_render.cjs ads`, apoi intrare în `HANDOFF.md` și push pe `main`.

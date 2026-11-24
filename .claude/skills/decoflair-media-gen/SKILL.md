---
name: decoflair-media-gen
description: Generează imagini și videoclipuri de produs Deco&Flair cu modele AI prin fal.ai (Nano Banana Pro / Seedream pentru imagini, Kling / Veo / Seedance pentru video image-to-video), pornind de la poza reală de catalog ca referință, apoi exportă în formatele pentru Facebook, Instagram, TikTok, Pinterest și site. Folosește-l pentru „fă poze de produs în ambient”, „imagine pentru reclamă”, „video de produs”, „reel”, „UGC”, „înainte/după”, „banner”.
---

# Generare imagini și video de produs

Lucrează împreună cu: `decoflair-catalog` (date + poze reale), `ai-ad-prompt-guide` (prompturi SLCT, camere, anti-halucinații), `ad-creative` / `social` (unghiuri, hook-uri, texte), `.agents/product-marketing.md` (voce, paletă).

## Reguli de neîncălcat
1. **Produsul real e referința.** Descarcă poza de catalog (`catalog.py images`) și trimite-o ca imagine de referință. Profilul (secțiune, ornament, proporții) nu se reinventează. Verifică vizual rezultatul față de referință; respinge variantele cu altă formă.
2. **Costul înainte de generare.** Spune modelul, numărul de imagini/secunde și costul estimativ (de pe pagina modelului pe fal.ai) și cere acordul pentru loturi mai mari de ~10 imagini sau orice video.
3. **Textul se pune în postprocesare**, nu în prompt (diacriticele ies greșit). Titluri, logo, CTA: HTML + Playwright sau PIL, ca în proiectele existente din repo (`decoflair-lux-2027/`, `decoflair-trend-2027/`).
4. Imaginile realiste generate cu AI: bifează eticheta „AI” unde platforma o cere (Meta „AI info”, TikTok „AI-generated”).
5. Cheile (`FAL_KEY`) stau doar în mediul sesiunii / setările environment-ului, niciodată în repo.

## Flux
1. Brief: produs, cameră/fațadă, stil (Lux întunecat-auriu, crem luminos, paleta 2027), platforme.
2. `catalog.py product` + `images` → `proiect/refs/<cod>/`.
3. Prompt (SLCT din `ai-ad-prompt-guide`): subiect = profilul exact „as in the reference image”, unde e montat (tavan, perete, ancadrament fereastră), lumină caldă laterală care scoate umbra profilului, cameră fotografică editorială, fără text, fără oameni dacă nu se cere.
4. Generare (încearcă întâi `--dry-run`):
   ```bash
   python3 .claude/skills/decoflair-media-gen/scripts/fal_run.py <model-id> \
     --prompt-file proiect/prompt.txt --image image_urls=proiect/refs/<cod>/ref-01.jpg \
     --arg aspect_ratio=4:5 --arg num_images=2 --out proiect/gen/<cod>
   ```
   Modele uzuale (verifică ID-ul și parametrii actuali pe fal.ai/models înainte):
   - imagine cu referință: `fal-ai/nano-banana-pro/edit` (păstrează cel mai bine obiectul), alternativ Seedream/Flux Kontext edit;
   - video din imaginea aprobată: Kling image-to-video (mișcări de cameră lente, 5–10 s), Veo (calitate maximă, cu sunet), Seedance (ieftin, bun pentru loturi).
5. Postprocesare: crop/resize, text, logo, subtitrări, muzică (ffmpeg). Video lung = clipuri AI de 5 s cusute cu ffmpeg + cadre de produs reale + text animat (vezi `decoflair-blog-reel/reel_build.py` și `reel_render.cjs`).
6. Export:

| Destinație | Format |
|---|---|
| Feed FB/IG | 1080×1350 (4:5) JPG |
| Story / Reel / TikTok | 1080×1920 (9:16), MP4 H.264, 30 fps, zonă sigură: 250 px sus, 340 px jos fără text |
| Pinterest | 1000×1500 (2:3) |
| Pătrat (catalog, Ads) | 1080×1080 |
| Slider site | 1480×800 desktop, 900×1200 mobil (JPEG progresiv) |

7. Salvează în `proiect/` fișierele finale + `PROMPTURI.md` (prompt, model, sămânță, cost), și notează în `HANDOFF.md`.

## Idei care vând pentru profile decorative
- Înainte/după din aceeași cameră (perete gol → chenare + cornișă LED).
- Macro pe ornament cu lumină razantă; secțiunea cu cote lângă ambient.
- Fațadă la apus cu ancadramente și brâu; „casă de 1 milion” cu buget mic.
- Video: dolly-in lent spre cornișa cu LED care se aprinde; time-lapse de montaj (adeziv → bară → chit → vopsea).
- UGC: mâini care montează bara, „am terminat holul într-o zi”.

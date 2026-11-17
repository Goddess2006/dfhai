# TikTok — NMC −30% (SIDDING PANEL 3 + colțar NCL107)

## Fișiere

- `nmc-wow-30-tiktok-ads.mp4` (22 s): pentru **reclamă plătită** (TikTok Ads Manager, In-Feed sau Spark Ads). La final scrie „Apasă «Cumpără acum»” și o săgeată arată spre butonul nativ al reclamei.
- `nmc-wow-30-tiktok-organic.mp4` (23 s): pentru **postare normală**. La final scrie „Link în bio” și apare un cod QR spre nmcromania.ro/black-november.

Ambele sunt 1080 × 1920. Conținutul stă în zonele sigure TikTok: sus ~160 px, dreapta ~140 px (iconițe), jos ~420 px (descriere și buton). Video-urile nu au sunet; muzica se adaugă în TikTok.

Etichetele de produs din video (pin + card cu preț și „→”) sunt grafică, nu se poate apăsa pe ele. Pe TikTok, în România, linkul spre produs se poate pune doar:

1. prin **butonul nativ al reclamei** (Ads Manager);
2. prin **link în bio** (cont de business).

TikTok Shop, singura variantă cu etichete pe care se apasă în video, nu e disponibil încă în România (noiembrie 2026).

## Varianta 1 — reclamă (Ads Manager)

- **Obiectiv:** Trafic sau Vânzări pe site.
- **Video:** `nmc-wow-30-tiktok-ads.mp4`.
- **Buton (CTA):** „Cumpără acum” (*Shop now*). Textul de pe video spune exact „Cumpără acum”, deci trebuie să aleagă același buton.
- **URL de destinație** (recomandat, cu UTM pentru măsurare):
  `https://www.nmcromania.ro/black-november/?utm_source=tiktok&utm_medium=paid&utm_campaign=black_november_30`
  - Alternativ, două reclame separate, fiecare spre pagina produsului:
    - Sidding: `https://www.nmcromania.ro/termosistem-decorativ-sidding-panel-3-500x40x2000`
    - NCL107: `https://www.nmcromania.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300`
- **Text reclamă (max ~100 caractere):** Fațadă obosită? Colțuri plate? −30% la SIDDING PANEL 3 și NCL107, până pe 30 noiembrie.
- **Nume afișat:** NMC România.
- **Perioadă:** până pe 30 noiembrie (atunci se încheie prețurile speciale).

## Varianta 2 — postare normală

1. Pune linkul în bio (cont de business): `nmcromania.ro/black-november`.
2. Postează `nmc-wow-30-tiktok-organic.mp4` cu descrierea de mai jos.
3. Fixează un comentariu cu linkul și întrebarea pentru public.

**Descriere:**
Fațada ta are întrebări? 🏡 Noi avem răspunsuri −30%.
SIDDING PANEL 3 → 156,31 lei (în loc de 223,31)
Colțar NCL107 → 173,66 lei (în loc de 248,09)
Până pe 30 noiembrie, în limita stocului. Link în bio 🔗
#nmcromania #fatada #renovare #casanoua #blacknovember #diy #constructii #amenajari

**Comentariu fixat:** Ce problemă are fațada ta? Scrie-ne și îți spunem soluția. Link: nmcromania.ro/black-november

## Prețuri

Verificate pe nmcromania.ro la 17.11.2026, cu TVA. Verificați-le din nou înainte de publicare.

Refacere video: `python3 tiktok_build.py && node tiktok_render.cjs`.

# Automatizare content Deco&Flair: skill-uri instalate și plan de lucru

Creat 2026-11-24 (Claude Code). Skill-urile stau în `.claude/skills/` din repo, deci se încarcă automat în orice sesiune Claude Code deschisă pe acest repo (cloud sau local). Codex le poate citi ca documentație.

## 1. Skill-uri instalate

### Scrise pentru Deco&Flair
| Skill | Ce face |
|---|---|
| `decoflair-catalog` | citește cele ~1.000 de produse din sitemap-ul public: nume, cod, preț, stoc, poze 1500 px; descarcă pozele ca referință |
| `decoflair-media-gen` | imagini și video de produs prin fal.ai (o singură cheie pentru toate modelele), cu poza reală de catalog ca referință; formatele pentru fiecare platformă |
| `decoflair-social-pipeline` | săptămâna de conținut: plan → produse → creative → texte → aprobare → programare (Postiz / Meta Business Suite / TikTok Studio) → raport |
| `decoflair-newsletter` | newsletter cu build HTML + Brevo API (draft, test, programare), plus fluxurile automate |
| `.agents/product-marketing.md` | contextul de brand (produse, public, voce, paletă, reguli), citit de toate skill-urile de marketing |

### Preluate de pe GitHub (licență MIT, copiate fără modificări)
| Skill | Sursă | Pentru ce |
|---|---|---|
| `social`, `ad-creative`, `content-strategy`, `copywriting`, `copy-editing`, `emails`, `image`, `video`, `seo-audit`, `ai-seo`, `schema`, `marketing-psychology`, `offers`, `popups`, `sms`, `product-marketing` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ `8fd2fca` | postări pe platformă, reclame, calendar, texte de pagină, secvențe e-mail, SEO + apariție în ChatGPT/AI Overviews, schema produs, oferte |
| `ai-ad-prompt-guide` | [Creatify-AI/ai-ad-prompt-guide](https://github.com/Creatify-AI/ai-ad-prompt-guide) @ `115b398` | prompturi pentru Nano Banana, Veo, Kling, Sora, Seedance: anti-halucinații, mișcări de cameră, UGC |

Actualizare: clonează din nou sursa și copiază folderul skill-ului peste cel vechi.

### Deja disponibile în cont (nu trebuie instalate)
`postiz:postiz` (programare pe 20+ rețele), `small-business:social-content-engine`, `small-business:content-strategy`, `small-business:canva-creator`, `small-business:marketing-monday`, `marketing:email-sequence`, `marketing:seo-audit`, `anthropic-skills:docx/pdf/xlsx`.

### Evaluate și lăsate deoparte
- `krusemediallc/arcads-claude-code`: bun, dar cere abonament Arcads; fal.ai acoperă aceleași modele (Nano Banana, Kling, Veo) cu plată la consum.
- UGC Factory / Higgsfield: cere conturi separate; de reluat doar dacă vrem reclame cu avatar uman.

## 2. Ce trebuie să faci tu o singură dată (conturi și chei)
| Ce | De ce | Cost orientativ |
|---|---|---|
| Cont **fal.ai** + cheie `FAL_KEY` | imagini și video AI | la consum: cenți/imagine, ~0,3–1,5 $/clip video de 5 s, după model (verifică pe fal.ai) |
| Cont **Brevo** + cheie `BREVO_API_KEY`, domeniu autentificat (SPF/DKIM/DMARC) | newsletter și fluxuri automate | gratuit 300/zi; Starter de la ~9 €/lună |
| **Postiz** (cloud sau instalat pe serverul tău) + conectare FB, IG, TikTok, Pinterest | programare din Claude | cloud de la ~29 $/lună; self-host gratuit |
| Cheile în setările environment-ului Claude Code (variabile de mediu) | ca sesiunile să le vadă | — |
| Opțional: conectorul Brevo MCP în claude.ai | trimitere direct din chat | — |

## 3. Procesul automat (solopreneur)
| Când | Ce face Claude | Ce faci tu |
|---|---|---|
| Luni (sesiune programată) | raportul săptămânii trecute + planul noii săptămâni + creativele și textele (`decoflair-social-pipeline`) | aprobi galeria (~30 min) |
| După aprobare | programează în Postiz | — |
| La 2 săptămâni | newsletter: draft în Brevo + test pe adresa ta | aprobi testul, Claude programează |
| O dată, apoi automat | fluxuri Brevo: bun venit, coș abandonat, după comandă, reactivare | aprobi textele |
| Lunar | 2 articole de blog SEO (din întrebările clienților) → reel + carusel + newsletter din fiecare | aprobi articolul, îl urci în OpenCart |
| Lunar | audit SEO / produse fără descriere / schema | — |

O sesiune Claude Code programată (scheduled task, de exemplu luni la 07:40) poate porni singură pasul de luni; spune-mi dacă o vrei.

"""Articol blog Deco&Flair — Tendințe design interior 2027 (noiembrie 2026).

Generează:
  out/articol-opencart.html   -> se lipește în câmpul Content (vizualizare cod </>)
  out/previzualizare.html     -> pagină completă pentru verificare în browser
Rulare: python3 build.py
"""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

SITE = "https://decoflair.ro"
IMG = f"{SITE}/image/catalog/Blog/tendinte-2027"
DATA_PRET = "24.11.2026"
PHONE = "0765 740 280"
WA = "https://wa.me/40765740280"

C_GREEN = "#1F3A2F"
C_GREEN2 = "#2E5244"
C_CREAM = "#F4EEE4"
C_SAND = "#E9D5CC"
C_GOLD = "#7A5B22"
C_INK = "#1d1d1b"
C_MUTED = "#5b5650"

# ---------------------------------------------------------------- produse
# (cod, denumire, url, imagine 450, preț cu TVA la DATA_PRET)
P = {
    "L5": ("Scafă LED Arstyl L5", "/l5-arstyl", "/image/cache/catalog/product/4023-Scafa-ARSTYL-L5-450x450.jpg", "526,83"),
    "L2": ("Scafă LED Arstyl L2", "/l2-arstyl", "/image/cache/catalog/product/4017-Scafa-ARSTYL-L2-450x450.jpg", "668,54"),
    "IL18": ("Cornișă LED IL18 121×90 mm", "/cornisa-led-il18-121x90x2000", "/image/cache/catalog/produse/Cornise/IL18/il18-450x450h.jpg", "217,56"),
    "IL13": ("Cornișă LED IL13 80×52 mm", "/cornisa-led-il13-80x52x2000", "/image/cache/catalog/produse/Cornise/IL13/il13-450x450h.jpg", "196,48"),
    "IL12": ("Profil LED Wallstyl IL12 20×25 mm", "/profil-decorativ-led-il12-20x25x2000", "/image/cache/catalog/Cornișa-IL12_new2-450x450w.jpg", "105,81"),
    "IL10": ("Plintă LED Wallstyl IL10 80×23 mm", "/plinta-decorativa-parchet-alba-polimer-dur-wallstyl-il10-80x23x2m", "/image/cache/catalog/produse/Plinte/il10/il10_product-450x450.jpg", "210,36"),
    "IL11": ("Plintă LED Wallstyl IL11 80×20 mm", "/plinta-decorativa-parchet-alba-polimer-dur-wallstyl-il11-80x20x2m", "/image/cache/catalog/product/plinta-parchet-alba-polimer-dur-wallstyl-IL11-450x450.jpg", "210,36"),
    "Z21": ("Cornișă poliuretan Z21 101×112 mm", "/plinta-decorativa-tavan-arstyl-z21", "/image/cache/catalog/product/3981-Plinta-alba-pentru-tavan-din-poliuretan-ARSTYL-Z21-450x450.jpg", "292,89"),
    "Z11": ("Cornișă poliuretan Z11 148×69 mm", "/plinta-decorativa-tavan-arstyl-z11", "/image/cache/catalog/product/3970-Plinta-alba-pentru-tavan-din-poliuretan-ARSTYL-Z11-450x450.jpg", "292,47"),
    "WT15": ("Cornișă decorativă Wallstyl WT15", "/cornisa-decorativa-wt15", "/image/cache/catalog/produse/Plinte/nmc-02-wallstyl-wt15-cornices-a-tbs-450x450.png", "129,52"),
    "Z1220FLEX": ("Cornișă flexibilă Arstyl Z1220FLEX", "/cornisa-decorativa-arstyl-z1220flex-75x50x2000", "/image/cache/catalog/CORNISA-DECORATIVA_Z1220FLEX_new-450x450w.jpg", "300,09"),
    "FD3": ("Plintă polimer dur FD3 100×20 mm", "/plintafd3-wallstyl", "/image/cache/catalog/product/4233-Plinta-parchet-alba-din-polistiren-WALLSTYL-FD3-450x450.jpg", "109,02"),
    "FL13": ("Plintă polimer dur FL13 58×13 mm", "/plinta-polimer-dur-fl13-58-13-2000", "/image/cache/catalog/produse/DecoPro/Plinta/FL13/NMC_02_wallstyl_fl13_skirtings_a-450x450.jpg", "65,91"),
    "FL17": ("Plintă înaltă FL17 170×18 mm", "/plinta-decorativa-parchet-alba-polimer-dur-wallstyl-fl17-170x18x2m", "/image/cache/catalog/product/plinta-parchet-alba-polimer-dur-wallstyl-fl17-450x450.jpg", "217,56"),
    "FD20": ("Plintă înaltă FD20 200×18 mm", "/plintafd20-wallstyl", "/image/cache/catalog/product/4511-Plinta-alba-parchet-WALLSTYL-FD20-450x450.jpg", "311,94"),
    "WO2": ("Brâu pentru chenare Wallstyl WO2 38×18 mm", "/brau-decorativwo2-wallstyl", "/image/cache/catalog/product/4263-Bagheta-polistiren-pentru-decorare-perete-WALLSTYL-WO2-450x450.jpg", "59,43"),
    "WD5": ("Brâu decorativ Wallstyl WD5 38×10 mm", "/cornisa-brau-polimer-dur-wallstyl-wd5-38x10x2m", "/image/cache/catalog/product/brau-polimer-dur-Wallstyl-WD5-450x450.jpg", "55,44"),
    "WE1": ("Colțar decorativ Wallstyl WE1 30×30 mm", "/brau-decorativwe1-wallstyl", "/image/cache/catalog/product/4277-Bagheta-polistiren-pentru-decorare-perete-WALLSTYL-WE1-450x450.jpg", "38,09"),
    "CANELE": ("Panou 3D CANELÉ L", "/panou-decorativ-canelel", "/image/cache/catalog/produse/panouri%203D/Canele%20L/canele-l%20(2)-450x450.jpg", "696,03"),
    "WAVE": ("Panou 3D Arstyl WAVE", "/panou-decorativ-3d-wave", "/image/cache/catalog/product/4029-Panouri-decorative-de-interior-gama-ARSTYL-3D-model-Wave-380x1135x185-450x450.jpg", "433,85"),
    "ICON": ("Panou 3D Arstyl ICON", "/panou-decorativ-3d-icon", "/image/cache/catalog/product/5226-Panou-decorativ-3d-interior-poliuretan-Arstyl-3D-Icon-380x1135x45-450x450h.jpg", "766,40"),
    "RAY": ("Panou 3D Arstyl RAY", "/panou-decorativ-3d-ray-arstyl", "/image/cache/catalog/produse/panouri%203D/ray/ray_3dp-450x450.jpg", "166,27"),
    "RIF_D": ("Riflaj acustic 3D — stejar deschis", "/riflaj-acustic-panou-3d-stejar-deschis", "/image/cache/catalog/produse/panouri%203D/riflaje%203d/IMG-20250225-WA0013-450x450h.jpg", "382,54"),
    "RIF_I": ("Riflaj acustic 3D — stejar închis", "/riflaj-acustic-panou-3d-stejar-inchis", "/image/cache/catalog/produse/panouri%203D/riflaje%203d/IMG-20250225-WA0014-450x450h.jpg", "382,54"),
    "R15": ("Rozetă tavan Arstyl R15 Ø560 mm", "/rozeta-decorativar15-arstyl", "/image/cache/catalog/category/3951-Rozeta-decorativa-ARSTYL-R15-450x450.jpg", "413,94"),
    "R13": ("Set rozete Arstyl R13 (2 buc.)", "/rozeta-decorativar13-arstyl", "/image/cache/catalog/product/nmc-02-arstyl-r13-ceiling-roses-a-tbs-450x450h.png", "199,36"),
    "T82603": ("Tapet Carrara Best 82603", "/tapet-carrara-82603", "/image/cache/catalog/produse/Tapet/82603-450x450.jpg", "665,50"),
    "T82671": ("Tapet Carrara Best 82671", "/tapet-carrara-82671", "/image/cache/catalog/produse/Tapet/82671-450x450.jpg", "665,50"),
}

CAT = {
    "interior": "/profile-decorative-interior",
    "chenare": "/profile-decorative-interior/chenare-decorative-perete",
    "cornise": "/profile-decorative-interior/cornisa-decorativa-interior",
    "led": "/profile-decorative-interior/profil-banda-led",
    "scafe": "/profile-decorative-interior/scafa-tavan",
    "plinte": "/profile-decorative-interior/plinta-polimer-decorativa",
    "brau": "/profile-decorative-interior/brau-decorativ-interior",
    "panouri": "/profile-decorative-interior/panouri-decorative-3d-interior-poliuretan",
    "rozete": "/profile-decorative-interior/rozete-decorative-tavan",
    "flex": "/profile-decorative-interior/profil-decorativ-flexibil",
    "adezivi": "/profile-decorative-interior/adezivi-profiluri-decorative",
    "riflaje": "/riflaje-acustice-3d",
    "tapet": "/tapet-premium-design-interior",
    "carrara": "/tapet-premium-design-interior/tapet-decori-decori/tapet-carrara-best",
    "cavalli": "/tapet-premium-design-interior/tapet-roberto-cavalli",
    "oferte": "/oferte-speciale",
    "consultanta": "/consultanta-premium",
    "randare": "/randare-3d",
    "linea": "/linea-room-kit-complet-pentru-o-camer%C4%83",
    "livrare": "/plata-si-livrare",
    "contact": "/contact",
}

BLOG = {
    "cornisa_led": "/blog/cornisa-led-iluminat-indirect-eleganta-interior",
    "chenare": "/blog/chenare-decorative-perete-modele-dimensiuni-proportii",
    "riflaje": "/blog/riflaje-acustice-design-functional",
    "montaj": "/blog/montaj-baghete-polistiren-tavan-perete",
    "detalii": "/blog/10-detalii-arhitecturale-care-cresc-valoarea-perceputa-a-unei-locuinte",
    "lux": "/blog/design-interior-lux",
    "apartament": "/blog/cum-faci-un-apartament-nou-sa-nu-arate-ca-toate-celelalte",
}


def a(href, text, title=None):
    t = f' title="{html.escape(title)}"' if title else ""
    return f'<a href="{SITE}{href}"{t}>{text}</a>'


def pa(code, text=None):
    n, u, _, _ = P[code]
    return a(u, text or n, n)


def ca(key, text):
    return a(CAT[key], text)


def ba(key, text):
    return a(BLOG[key], text)


def fig(file, alt, caption, w=1200, h=900, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<figure style="margin:28px 0;">'
        f'<img src="{IMG}/{file}" alt="{html.escape(alt)}" width="{w}" height="{h}" {load} '
        f'style="width:100%;height:auto;border-radius:10px;display:block;">'
        f'<figcaption style="font-size:13px;color:{C_MUTED};margin-top:8px;line-height:1.5;">{caption}</figcaption>'
        f'</figure>'
    )


def cards(codes, title="Produse recomandate"):
    items = []
    for c in codes:
        n, u, i, pr = P[c]
        items.append(
            f'<div style="flex:1 1 180px;max-width:240px;background:#fff;border:1px solid #e6dfd3;border-radius:10px;padding:12px;text-align:center;">'
            f'<a href="{SITE}{u}" title="{html.escape(n)}"><img src="{SITE}{i}" alt="{html.escape(n)}" width="450" height="450" loading="lazy" decoding="async" style="width:100%;height:auto;border-radius:6px;display:block;"></a>'
            f'<p style="margin:10px 0 4px;font-size:14px;line-height:1.35;font-weight:600;color:{C_INK};">{html.escape(n)}</p>'
            f'<p style="margin:0 0 10px;font-size:14px;color:{C_GOLD};font-weight:700;">{pr} lei</p>'
            f'<a href="{SITE}{u}" style="display:inline-block;background:{C_GREEN};color:#fff;text-decoration:none;font-size:13px;font-weight:600;padding:8px 14px;border-radius:6px;">Vezi produsul</a>'
            f'</div>'
        )
    return (
        f'<div style="background:{C_CREAM};border-radius:12px;padding:18px;margin:24px 0;">'
        f'<p style="margin:0 0 12px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:{C_GOLD};font-weight:700;">{title}</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:flex-start;">{"".join(items)}</div>'
        f'</div>'
    )


def box(inner, bg=C_CREAM, border=C_GOLD):
    return f'<div style="background:{bg};border-left:4px solid {border};border-radius:8px;padding:18px 20px;margin:24px 0;">{inner}</div>'


def h2(id_, text):
    return f'<h2 id="{id_}">{text}</h2>'


def lei(x):
    s = f"{x:,.2f}".replace(",", " ").replace(".", ",").replace(" ", ".")
    return s


def price(code):
    return float(P[code][3].replace(".", "").replace(",", "."))


# ---------------------------------------------------------------- buget exemplu
import math

perim = 18.0  # living 4 x 5 m
calc = [
    ("Cornișă LED IL18 (perimetru tavan)", "IL18", perim),
    ("Plintă FD3 (perimetru minus ușă ~2 m)", "FD3", perim - 2),
    ("Brâu WO2 pentru 3 chenare de 80×120 cm", "WO2", 3 * 2 * (0.8 + 1.2)),
]
rows, total = [], 0.0
for label, code, m in calc:
    bars = math.ceil(m * 1.10 / 2)  # +10% pierderi la tăiere, bare de 2 m
    cost = bars * price(code)
    total += cost
    rows.append((label, code, m, bars, cost))

budget_rows = "".join(
    f'<tr><td style="padding:8px;border-bottom:1px solid #e6dfd3;">{lab} — {pa(code, code)}</td>'
    f'<td style="padding:8px;border-bottom:1px solid #e6dfd3;text-align:center;">{lei(m).rstrip("0").rstrip(",")} m</td>'
    f'<td style="padding:8px;border-bottom:1px solid #e6dfd3;text-align:center;">{bars}</td>'
    f'<td style="padding:8px;border-bottom:1px solid #e6dfd3;text-align:right;white-space:nowrap;">{lei(cost)} lei</td></tr>'
    for lab, code, m, bars, cost in rows
)

# ---------------------------------------------------------------- conținut
TOC = [
    ("pe-scurt", "Pe scurt: tendințele 2027 într-un minut"),
    ("culoarea-anului-2027", "Care este culoarea anului 2027?"),
    ("trend-1-verde", "1. Verdele, culoarea-semnătură a lui 2027"),
    ("trend-2-neutri-calzi", "2. Neutri calzi: bej, greige și argilă"),
    ("trend-3-lumina-indirecta", "3. Lumina devine material: scafe și cornișe LED"),
    ("trend-4-lumina-joasa", "4. Lumina joasă: holuri cu plinte LED"),
    ("trend-5-panouri-3d", "5. Pereți cu relief: panouri decorative 3D"),
    ("trend-6-riflaje", "6. Riflaje calde și liniște acustică"),
    ("trend-7-plinte-inalte", "7. Plinte înalte, proporții de vilă"),
    ("trend-8-tavan", "8. Tavanul, al cincilea perete"),
    ("trend-9-curbe", "9. Curbe și forme moi"),
    ("trend-10-tapet", "10. Lux tăcut: tapet cu efect de marmură"),
    ("ce-iese-din-moda", "Ce iese din modă în 2027"),
    ("tabel-tendinte", "Tabel: tendință, cameră, produse"),
    ("buget", "Cât costă: exemplu de buget pentru un living"),
    ("pasi", "Cum aplici tendințele în 5 pași"),
    ("sarbatori", "Ce poți face până de sărbători"),
    ("intrebari-frecvente", "Întrebări frecvente"),
]

toc_html = (
    f'<nav aria-label="Cuprins" style="border:1px solid #e6dfd3;border-radius:10px;padding:16px 20px;margin:24px 0;">'
    f'<p style="margin:0 0 8px;font-weight:700;">Cuprins</p><ol style="margin:0;padding-left:20px;line-height:1.8;">'
    + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in TOC)
    + "</ol></nav>"
)

FAQ = [
    ("Care este culoarea anului 2027?",
     "Nu există o singură culoare oficială. Benjamin Moore a ales <strong>Webster Green HC-130</strong> (anunțată pe 14 octombrie 2026), "
     "WGSN și Coloro au desemnat <strong>Luminous Blue</strong>, Behr a ales <strong>Grounded</strong>, iar Valspar <strong>Cottage Door</strong>. "
     "Pantone își anunță de obicei alegerea la începutul lui decembrie; la 24 noiembrie 2026 culoarea Pantone pentru 2027 nu era publicată. "
     "Direcția comună: verde, albastru-gri liniștit și neutri calzi."),
    ("Care sunt cele mai importante tendințe în design interior pentru 2027?",
     "Zece direcții domină: verdele ca bază, neutrii calzi (bej, greige, argilă), iluminatul indirect integrat în scafe și cornișe LED, "
     "lumina joasă la nivelul plintei, pereții cu relief (panouri 3D), riflajele din lemn cu rol acustic, plintele înalte, tavanul decorat cu rozete și cornișe, "
     "formele curbe și tapetul cu efect de marmură. Toate pun accent pe arhitectura camerei, nu pe obiecte decorative în plus."),
    ("Care este diferența dintre o scafă LED și o cornișă LED?",
     "Cornișa LED se montează la îmbinarea perete–tavan și ascunde banda LED în spatele profilului, proiectând lumina în sus, pe tavan. "
     "Scafa LED este un profil mai adânc, care poate fi montat pe tavan sau pe perete și creează o linie de lumină mai lată, cu efect de tavan „plutitor”. "
     "Ambele oferă iluminat indirect, fără ca sursa de lumină să fie vizibilă."),
    ("Ce temperatură de culoare aleg pentru banda LED din cornișă?",
     "Pentru living și dormitor se recomandă alb cald, 2700–3000 K, care pune în valoare tonurile de bej, verde și lemn. "
     "Pentru birou sau bucătărie poți urca la 3500–4000 K. Alege o bandă LED cu indice de redare a culorilor (CRI) de minimum 90 și un variator (dimmer)."),
    ("Mai sunt la modă riflajele în 2027?",
     "Da, dar evoluează: în 2027 se poartă riflajele din lemn cald (stejar, nuc), montate pe jumătate de perete, la tăblia patului sau în spatele televizorului, "
     "alese și pentru rolul lor acustic. Lamelele subțiri, reci, folosite peste tot, ies din tendințe."),
    ("Ce înălțime trebuie să aibă plinta?",
     "Regula designerilor: la tavane de 2,50–2,70 m, o plintă de 8–10 cm; la 2,80–3,00 m, 10–15 cm; peste 3 m, 15–20 cm. "
     "O plintă înaltă, vopsită în culoarea peretelui, face camera să pară mai înaltă și mai elegantă."),
    ("Pot vopsi profilele decorative din polimer sau poliuretan?",
     "Da. Profilele din polimer dur și poliuretan se vopsesc după montaj cu vopsea acrilică pe bază de apă, de obicei în două straturi. "
     "Vopsirea profilelor în aceeași culoare cu peretele (tehnica „color drenching”) este una dintre cele mai puternice tendințe ale anului 2027."),
    ("Cât costă să transformi un living după tendințele 2027?",
     f"Pentru un living de 4×5 m, cornișa LED, plintele și trei chenare decorative costă aproximativ {lei(total)} lei (prețuri cu TVA la {DATA_PRET}, "
     "cu 10% rezervă la tăiere, fără bandă LED, adeziv și manoperă). Calculul complet este în secțiunea de buget a acestui ghid."),
    ("Pot monta singur profilele decorative?",
     "Da, majoritatea profilelor de interior se lipesc cu adeziv special și se taie cu un fierăstrău și o cutie de tăiere la 45°. "
     "Pentru scafe cu LED și panouri 3D pe suprafețe mari recomandăm un montator, pentru îmbinări perfecte."),
    ("În cât timp primesc produsele comandate de pe decoflair.ro?",
     "Profilele de interior aflate în stoc se livrează prin curier rapid în 1–2 zile lucrătoare. Produsele la comandă au un termen de aproximativ 14 zile lucrătoare. "
     "Poți ridica produsele și din depozitul Deco&Flair din Domnești, Ilfov."),
]

faq_html = (
    '<div itemscope itemtype="https://schema.org/FAQPage">'
    + "".join(
        f'<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question" style="border-bottom:1px solid #e6dfd3;padding:14px 0;">'
        f'<h3 itemprop="name" style="margin:0 0 8px;">{q}</h3>'
        f'<div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text" style="margin:0;">{ans}</p></div>'
        f'</div>'
        for q, ans in FAQ
    )
    + "</div>"
)

table_rows = [
    ("Verde (Webster Green, salvie)", "Living, bibliotecă, dormitor", f'{ca("chenare", "chenare decorative")}, {ca("brau", "brâu")}'),
    ("Neutri calzi: bej, greige, argilă", "Dormitor, living", f'{ca("cornise", "cornișe decorative")}'),
    ("Iluminat indirect LED", "Living, dormitor, dining", f'{ca("scafe", "scafe tavan")}, {ca("led", "profile LED")}'),
    ("Lumină joasă", "Hol, scară, baie", f'{pa("IL10", "plinte LED")}, {pa("IL12", "profil IL12")}'),
    ("Pereți cu relief 3D", "Living, hol, dormitor", f'{ca("panouri", "panouri decorative 3D")}'),
    ("Riflaje calde, acustice", "Living (TV), dormitor, birou", f'{ca("riflaje", "riflaje acustice 3D")}'),
    ("Plinte înalte", "Toată casa", f'{ca("plinte", "plinte decorative")}'),
    ("Tavanul decorat", "Dining, living, dormitor", f'{ca("rozete", "rozete tavan")}, {ca("cornise", "cornișe")}'),
    ("Curbe și forme moi", "Living, nișe, arcade", f'{ca("flex", "profile flexibile")}'),
    ("Lux tăcut: marmură", "Living, baie, hol", f'{ca("carrara", "tapet Carrara")}'),
]
table_html = (
    '<div style="overflow-x:auto;margin:20px 0;"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:520px;">'
    f'<thead><tr style="background:{C_GREEN};color:#fff;"><th style="padding:10px;text-align:left;">Tendința 2027</th>'
    '<th style="padding:10px;text-align:left;">Unde se potrivește</th><th style="padding:10px;text-align:left;">Ce folosești</th></tr></thead><tbody>'
    + "".join(
        f'<tr style="background:{"#fff" if i % 2 == 0 else C_CREAM};"><td style="padding:10px;border-bottom:1px solid #e6dfd3;"><strong>{t}</strong></td>'
        f'<td style="padding:10px;border-bottom:1px solid #e6dfd3;">{r}</td><td style="padding:10px;border-bottom:1px solid #e6dfd3;">{p}</td></tr>'
        for i, (t, r, p) in enumerate(table_rows)
    )
    + "</tbody></table></div>"
)

palette = [
    ("#4F6B4F", "Verde pădure", "inspirat de Webster Green"),
    ("#9CAF88", "Verde salvie", "pereți de dormitor"),
    ("#5E7C8A", "Albastru-gri", "Luminous Blue, în varianta de interior"),
    ("#D9C7B0", "Bej cald", "baza pentru toată casa"),
    ("#A47864", "Argilă", "accente, textile"),
    ("#F2EDE4", "Alb cremos", "profile, tavane"),
]
palette_html = (
    '<div style="display:flex;flex-wrap:wrap;gap:10px;margin:18px 0;">'
    + "".join(
        f'<div style="flex:1 1 120px;border:1px solid #e6dfd3;border-radius:8px;overflow:hidden;background:#fff;">'
        f'<div style="height:64px;background:{hx};"></div>'
        f'<div style="padding:8px 10px;font-size:13px;line-height:1.4;"><strong>{n}</strong><br><span style="color:{C_MUTED};">{d}</span></div></div>'
        for hx, n, d in palette
    )
    + "</div>"
)

cta_btn = (
    f'<a href="{SITE}{CAT["consultanta"]}" style="display:inline-block;background:{C_GREEN};color:#fff;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:8px;margin:6px 8px 6px 0;">Cere consultanță gratuită</a>'
    f'<a href="{WA}" style="display:inline-block;background:#25D366;color:#0b2e17;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:8px;margin:6px 8px 6px 0;">Scrie-ne pe WhatsApp</a>'
    f'<a href="{SITE}{CAT["randare"]}" style="display:inline-block;background:#fff;color:{C_GREEN};border:2px solid {C_GREEN};text-decoration:none;font-weight:700;padding:10px 18px;border-radius:8px;margin:6px 0;">Vezi camera în randare 3D</a>'
)

body = f"""
<p style="font-size:13px;color:{C_MUTED};margin:0 0 16px;">Ghid actualizat la <time datetime="2026-11-24">24 noiembrie 2026</time> · Timp de citire: 14 minute · Echipa de consultanță Deco&amp;Flair</p>

<p style="font-size:19px;line-height:1.6;"><strong>Tendințele în design interior pentru 2027 mută atenția de pe obiecte pe arhitectura casei.</strong> Culoarea anului 2027 vine în nuanțe de verde și albastru liniștit, neutrii devin calzi, iar lumina se ascunde în cornișe și scafe LED. Pereții capătă relief, plintele cresc în înălțime, iar tavanul redevine decorat. În acest ghid găsești cele 10 direcții care vor defini casele frumoase în 2027, cum le aplici în fiecare cameră, ce produse folosești și cât costă.</p>

{fig("tendinte-design-interior-2027-living-scafa-led.jpg", "Living modern în tonuri de bej cu scafă LED pe tavan și chenare decorative pe perete, tendință design interior 2027", "Living în tonuri calde, cu iluminat indirect în scafă LED și chenare decorative pe perete: rezumatul vizual al tendințelor din 2027.", eager=True)}

{box(f'''<p style="margin:0 0 8px;font-weight:700;font-size:17px;" id="pe-scurt">Pe scurt: tendințele 2027 într-un minut</p>
<ul style="margin:0;padding-left:20px;line-height:1.7;">
<li><strong>Culoare:</strong> verdele (Webster Green, Benjamin Moore) și albastrul liniștit (Luminous Blue, WGSN × Coloro) înlocuiesc griul rece.</li>
<li><strong>Lumină:</strong> iluminatul indirect, ascuns în {ca("scafe", "scafe")} și {ca("led", "cornișe LED")}, devine standard, nu lux.</li>
<li><strong>Textură:</strong> {ca("panouri", "panourile decorative 3D")} și {ca("riflaje", "riflajele")} din lemn cald dau pereților relief și liniște acustică.</li>
<li><strong>Proporție:</strong> {ca("plinte", "plintele înalte")}, {ca("chenare", "chenarele decorative")} și {ca("rozete", "rozetele de tavan")} aduc aerul unei case de arhitect.</li>
<li><strong>Atmosferă:</strong> „lux tăcut”: materiale naturale, marmură, curbe moi, fără excese decorative.</li>
</ul>''')}

{toc_html}

{h2("culoarea-anului-2027", "Care este culoarea anului 2027?")}

<p><strong>Pentru 2027 nu există o singură culoare a anului, ci o familie de nuanțe: verdele și albastrul liniștit, susținute de neutri calzi.</strong> Iată ce au anunțat până acum cele mai urmărite branduri și agenții de tendințe:</p>

<ul style="line-height:1.8;">
<li><strong>Benjamin Moore: Webster Green HC-130</strong>, un verde adânc, echilibrat, anunțat pe 14 octombrie 2026, în paleta Color Trends 2027 alături de maro „tawny”, pasteluri prăfuite și ocru.</li>
<li><strong>WGSN × Coloro: Luminous Blue</strong>, un albastru luminos, optimist, ales drept Culoarea Anului 2027.</li>
<li><strong>Behr: Grounded</strong>, un neutru cald, mai profund decât bejul clasic.</li>
<li><strong>Valspar: Cottage Door</strong> și <strong>Glidden: Artifact</strong>, nuanțe de albastru-gri calm, ușor de purtat pe suprafețe mari.</li>
<li><strong>Pantone</strong> își anunță de regulă culoarea anului la începutul lui decembrie. <em>Vom actualiza acest ghid imediat după anunț.</em> Pentru context, culoarea Pantone a anului 2026 a fost Cloud Dancer, un alb cremos.</li>
</ul>

<p>Ce înseamnă asta pentru casa ta? Că în 2027 culorile nu mai „strigă”. Sunt culori care liniștesc, care arată bine la lumina zilei și și mai bine la lumină caldă, indirectă. Și, foarte important, sunt culori care pun în valoare <strong>profilele decorative albe sau vopsite ton pe ton</strong>.</p>

{fig("moodboard-paleta-2027-profile-tapet-riflaj.jpg", "Moodboard design interior 2027 cu tapet efect marmură, riflaj din lemn, cornișă și chenar decorativ", "Moodboard 2027: marmură caldă, lemn de nuc, profile albe sculptate. Paleta se construiește din materiale, nu doar din vopsea.")}

<p style="font-weight:700;margin-bottom:4px;">Paleta Deco&amp;Flair 2027, gata de aplicat</p>
{palette_html}
<p style="font-size:13px;color:{C_MUTED};">Codurile de culoare sunt orientative, pentru ecran. Cere întotdeauna mostra fizică de vopsea înainte să alegi.</p>

{h2("trend-1-verde", "1. Verdele, culoarea-semnătură a lui 2027")}

<p><strong>Verdele este culoarea care leagă aproape toate prognozele pentru 2027:</strong> de la Webster Green (Benjamin Moore) la Celery (Sherwin-Williams) și Soulful Sage (Dulux). Căutările pentru „verde salvie” au crescut constant în România pe parcursul lui 2026, iar trendul se mută acum spre verdele mai adânc, de bibliotecă.</p>

<p>Secretul unui perete verde care arată scump nu este doar nuanța, ci <strong>relieful</strong>. Un perete verde plat poate părea greu. Același perete, cu {ca("chenare", "chenare decorative perete")} vopsite în aceeași culoare, devine o boiserie modernă, cu umbre fine care se schimbă pe parcursul zilei.</p>

{fig("culoarea-anului-2027-perete-verde-chenare-decorative.jpg", "Bibliotecă cu perete verde închis și chenare decorative vopsite ton pe ton, culoarea anului 2027", "Verde de bibliotecă cu chenare vopsite ton pe ton (color drenching): relief fără contrast agresiv.")}

<h3>Cum aplici trendul</h3>
<ul style="line-height:1.8;">
<li><strong>Color drenching:</strong> pereți, chenare și plintă în aceeași nuanță de verde. Efectul este de cameră „îmbrăcată”, foarte actual.</li>
<li><strong>Proporții:</strong> chenarele arată cel mai bine când respectă axele mobilierului. Află regulile în ghidul nostru despre {ba("chenare", "chenare decorative: modele, dimensiuni și proporții")}.</li>
<li><strong>Profile subțiri pentru pereți moderni:</strong> {pa("WO2")} sau {pa("WD5")}; pentru colțuri curate, {pa("WE1", "colțarul WE1")}.</li>
</ul>

{cards(["WO2", "WD5", "WE1"], "Pentru chenare pe pereți verzi")}

{h2("trend-2-neutri-calzi", "2. Neutri calzi: bej, greige și argilă")}

<p><strong>Griul rece iese, iar „neutrii vii” intră:</strong> bej cald, greige (gri cu bază bej), argilă, maro cafea. Behr a numit chiar culoarea anului 2027 „Grounded”, un neutru mai profund decât bejul. Bejul rămâne unul dintre cele mai căutate cuvinte de culoare în România, iar în 2027 devine fundalul pe care se construiește tot restul casei.</p>

<p>Un interior bej poate fi însă plictisitor dacă e plat. Aici intervine arhitectura: o {ca("cornise", "cornișă decorativă")} generoasă la tavan creează o linie de umbră care dă profunzime, iar camera pare imediat mai înaltă.</p>

{fig("dormitor-bej-greige-cornisa-decorativa-2027.jpg", "Dormitor modern bej greige cu cornișă decorativă la tavan și chenare pe peretele din spatele patului", "Dormitor greige: cornișa și chenarul din spatele patului înlocuiesc tăblia supradimensionată și decorul încărcat.")}

<h3>Cum alegi cornișa potrivită</h3>
<ul style="line-height:1.8;">
<li><strong>Tavan 2,50–2,70 m:</strong> cornișe de 5–8 cm, cu profil simplu, de exemplu {pa("WT15")}.</li>
<li><strong>Tavan 2,80 m sau mai înalt:</strong> profile mai ample, ca {pa("Z21")} (101×112 mm) sau {pa("Z11")} (148×69 mm).</li>
<li><strong>Stil:</strong> pentru „lux tăcut” alege linii drepte și profile curate; ornamentele bogate rămân pentru interioarele clasice.</li>
</ul>

{cards(["Z21", "Z11", "WT15"], "Cornișe pentru tavane elegante")}

{h2("trend-3-lumina-indirecta", "3. Lumina devine material: scafe și cornișe LED")}

<p><strong>Iluminatul indirect este cea mai puternică tendință tehnică a anului 2027.</strong> Lustra rămâne un accent, dar lumina de bază vine din arhitectură: bandă LED ascunsă în profile, care proiectează lumina pe tavan sau pe perete. Căutările pentru „bandă LED tavan”, „scafă LED” și „cornișă LED” sunt constante tot anul în România, cu vârfuri toamna și iarna, când zilele scurte ne fac să ne gândim la atmosfera de acasă.</p>

<p><strong>Ce este o scafă LED?</strong> Scafa LED este un profil decorativ, de obicei din poliuretan sau polimer, care ascunde o bandă LED și creează o linie continuă de lumină indirectă pe tavan sau pe perete. Spre deosebire de un tavan fals din gips-carton, se montează direct pe perete, fără structură metalică și fără să reducă înălțimea camerei.</p>

{fig("scafa-led-iluminat-indirect-tavan-detaliu.jpg", "Detaliu scafă LED pentru iluminat indirect pe tavan, lumină caldă difuză", "Lumina nu se vede ca sursă, ci ca efect: linie caldă, difuză, fără reflexii.")}

<h3>Scafă sau cornișă LED?</h3>
<ul style="line-height:1.8;">
<li><strong>Cornișă LED</strong> ({pa("IL18")}, {pa("IL13")}): se montează la îmbinarea perete–tavan și „spală” tavanul cu lumină. Ideală pentru living și dormitor.</li>
<li><strong>Scafă LED</strong> ({pa("L5")}, {pa("L2")}): creează o linie de lumină mai lată, cu efect de tavan plutitor. Ideală pentru camere mari, dining și zone de recepție.</li>
<li><strong>Profil LED discret</strong> ({pa("IL12")}): pentru nișe, rafturi, oglinzi și detalii minimaliste.</li>
</ul>

{box(f'<p style="margin:0;"><strong>Sfatul expertului:</strong> alege bandă LED de 2700–3000 K (alb cald), cu CRI ≥ 90, și montează un variator. Verdele, bejul și lemnul arată de două ori mai scump la lumină caldă, reglabilă. Mai multe idei găsești în articolul {ba("cornisa_led", "Cornișa LED pentru iluminare indirectă într-un interior elegant")}.</p>', bg="#EEF3EF", border=C_GREEN2)}

{cards(["IL18", "IL13", "L5", "L2"], "Profile pentru iluminat indirect")}

{h2("trend-4-lumina-joasa", "4. Lumina joasă: holuri cu plinte LED")}

<p><strong>În 2027, lumina coboară.</strong> După tavane, designerii aduc linia de lumină la nivelul podelei: plinte cu LED integrat, care transformă un hol banal într-un culoar de hotel boutique și servesc, în același timp, drept lumină de veghe pe timp de noapte.</p>

{fig("amenajare-hol-lumina-indirecta-plinta-led.jpg", "Amenajare hol modern cu lumină indirectă la nivelul plintei și pereți în tonuri calde", "Hol cu lumină joasă: plinta LED ghidează pașii noaptea și scoate în evidență textura pardoselii.")}

<p>Pentru o <strong>amenajare de hol</strong> reușită, combină {pa("IL10", "plinta LED IL10")} sau {pa("IL11", "IL11")} cu pereți într-un neutru cald și o singură piesă de mobilier sculpturală. Lumina joasă funcționează excelent și pe scări, în băi sau în dressing.</p>

{cards(["IL10", "IL11", "IL12"], "Pentru lumină la nivelul podelei")}

{h2("trend-5-panouri-3d", "5. Pereți cu relief: panouri decorative 3D")}

<p><strong>Peretele de accent din 2027 nu mai este colorat, ci sculptat.</strong> {ca("panouri", "Panourile decorative 3D pentru perete")} cu valuri, canelură sau geometrie fină creează un joc de umbre care se schimbă de la dimineață la seară. Vopsite în alb cremos sau în culoarea peretelui, aduc un efect de galerie, fără să încarce încăperea.</p>

{fig("panouri-decorative-perete-3d-valuri-living.jpg", "Living cu perete cu panouri decorative 3D cu model de valuri, vopsit alb cremos", "Panouri 3D cu valuri: relieful devine decor, iar lumina naturală desenează perete după perete.")}

<h3>Unde se potrivesc panourile 3D</h3>
<ul style="line-height:1.8;">
<li><strong>În living, în spatele canapelei sau al televizorului:</strong> {pa("WAVE")} pentru un efect organic, {pa("CANELE", "CANELÉ L")} pentru linii verticale care înalță camera.</li>
<li><strong>În dormitor, în locul tăbliei patului:</strong> canelura verticală e caldă și calmă.</li>
<li><strong>În hol sau pe casa scării:</strong> {pa("ICON")} sau {pa("RAY")}, cu iluminare laterală, pentru umbre spectaculoase.</li>
</ul>

{cards(["CANELE", "WAVE", "ICON", "RAY"], "Panouri decorative 3D")}

{h2("trend-6-riflaje", "6. Riflaje calde și liniște acustică")}

<p><strong>Riflajele rămân unul dintre cele mai căutate elemente de amenajare din România, dar în 2027 se schimbă felul în care le folosim.</strong> Nu mai acoperim pereți întregi cu lamele reci. Alegem lemn cald (stejar, nuc), îl montăm strategic și îl alegem și pentru rolul acustic: casele cu suprafețe dure, open space și pardoseli lucioase au nevoie de liniște.</p>

{fig("riflaje-lemn-perete-living-modern.jpg", "Living modern cu perete de riflaje din lemn de nuc și canapea bej", "Riflaj din lemn cald pe peretele principal: textură, căldură și mai puțin ecou.")}

<ul style="line-height:1.8;">
<li><strong>Riflaj pe jumătate de perete</strong>, cu un brâu deasupra: soluție nouă pentru dormitoare și birouri.</li>
<li><strong>Riflaj în spatele televizorului</strong>, cu LED ascuns în partea de sus.</li>
<li><strong>Riflaj la tăblia patului</strong>, din tavan până la podea, pentru un dormitor de hotel.</li>
</ul>

<p>Detalii tehnice și exemple găsești în ghidul {ba("riflaje", "Riflaje acustice: design și funcționalitate")}.</p>

{cards(["RIF_D", "RIF_I"], "Riflaje acustice 3D")}

{h2("trend-7-plinte-inalte", "7. Plinte înalte, proporții de vilă")}

<p><strong>Plinta înaltă este detaliul pe care îl observă oricine intră într-o casă de arhitect, chiar dacă nu știe să-l numească.</strong> În 2027, plintele de 4–6 cm lasă locul profilelor de 10, 15 sau chiar 20 cm, vopsite în culoarea peretelui sau în alb cremos. Rezultatul: tavanul pare mai sus, iar pereții, mai bine finisați.</p>

{fig("plinta-decorativa-inalta-hol-minimalist.jpg", "Hol minimalist cu plintă decorativă înaltă albă și parchet în model herringbone", "Plintă înaltă, albă, pe parchet herringbone: un detaliu simplu care schimbă proporțiile întregului spațiu.")}

<h3>Ce înălțime alegi</h3>
<ul style="line-height:1.8;">
<li><strong>Tavan 2,50–2,70 m:</strong> 8–10 cm, de exemplu {pa("FD3")} (100 mm).</li>
<li><strong>Tavan 2,80–3,00 m:</strong> 15–17 cm, de exemplu {pa("FL17")} (170 mm).</li>
<li><strong>Tavan peste 3 m:</strong> 20 cm, de exemplu {pa("FD20")} (200 mm).</li>
<li><strong>Buget mic, efect mare:</strong> {pa("FL13")} pentru camerele secundare.</li>
</ul>

<p>Profilele din polimer dur sunt rezistente la lovituri și umiditate, se vopsesc ușor și nu se deformează, o alternativă premium la plinta din MDF. Vezi toată gama de {ca("plinte", "plinte decorative")}.</p>

{cards(["FD3", "FL17", "FD20", "FL13"], "Plinte decorative")}

{h2("trend-8-tavan", "8. Tavanul, al cincilea perete")}

<p><strong>După ani de tavane albe și goale, 2027 readuce privirea în sus.</strong> Rozetele de tavan, cornișele bogate și tavanele casetate revin, dar într-o variantă mai curată: un singur element puternic, nu ornamente peste tot. O {ca("rozete", "rozetă decorativă de tavan")} deasupra mesei din dining sau a patului devine centrul compoziției.</p>

{fig("rozeta-tavan-cornisa-dining-clasic-modern.jpg", "Dining clasic modern cu rozetă decorativă de tavan, cornișă sculptată și masă din lemn", "Rozetă de tavan și cornișă sculptată: dining-ul capătă aerul unui apartament parizian.")}

<ul style="line-height:1.8;">
<li><strong>Dining sau living mare:</strong> {pa("R15")}, cu diametru de 560 mm, sub o lustră statement.</li>
<li><strong>Spații mici sau spoturi:</strong> {pa("R13")}, rozete compacte pentru corpuri de iluminat discrete.</li>
<li><strong>Tavan casetat fără gips-carton:</strong> cornișe sau brâuri lipite direct pe tavan, în grilă. Află cum se montează în ghidul {ba("montaj", "montajul baghetelor pe tavan și perete")}.</li>
</ul>

{cards(["R15", "R13"], "Rozete decorative de tavan")}

{h2("trend-9-curbe", "9. Curbe și forme moi")}

<p><strong>Canapelele rotunjite au deschis drumul; în 2027, curbele ajung în arhitectură.</strong> Arcade, nișe rotunjite, colțuri moi și pereți cu relief organic creează spații care par „îmbrățișate”, foarte potrivite pentru dormitoare, băi și zone de relaxare.</p>

{fig("pereti-curbati-relief-organic-design-2027.jpg", "Interior cu perete cu relief organic curbat și oglindă cu ramă aurie, tendință forme curbe 2027", "Relief organic și forme curbe: liniile moi aduc căldură chiar și într-o paletă aproape monocromă.")}

<p>Pentru a urmări o arcadă, un perete curb sau un tavan boltit ai nevoie de {ca("flex", "profile decorative flexibile")}. Acestea se curbează fără să crape, iar după vopsire nu se deosebesc de profilele rigide, de exemplu {pa("Z1220FLEX")}.</p>

{cards(["Z1220FLEX"], "Profile flexibile pentru curbe")}

{h2("trend-10-tapet", "10. Lux tăcut: tapet cu efect de marmură")}

<p><strong>„Quiet luxury” rămâne direcția dominantă și în 2027:</strong> materiale care par naturale, nuanțe calde, fără logo-uri și fără excese. Marmura caldă (crem, nisip, cu vene aurii) este materialul-simbol, iar un {ca("tapet", "tapet premium")} cu efect de marmură îl aduce pe perete la o fracțiune din costul și greutatea pietrei.</p>

{fig("tapet-marmura-premium-living.jpg", "Perete cu tapet premium cu efect de marmură crem cu vene aurii și vază cu flori", "Tapet cu efect de marmură caldă: luxul se simte, nu se afișează.")}

<p>Colecția italiană {ca("carrara", "Carrara Best")} are texturi de piatră pentru living, dormitor sau hol, de exemplu {pa("T82603")} sau {pa("T82671")}. Pentru un perete de accent mai îndrăzneț, vezi colecția {ca("cavalli", "Roberto Cavalli")}. Combinația câștigătoare: tapet marmură pe un perete, chenare albe pe ceilalți și lumină caldă indirectă.</p>

{cards(["T82603", "T82671"], "Tapet premium cu efect de marmură")}

{h2("ce-iese-din-moda", "Ce iese din modă în 2027")}

<ul style="line-height:1.8;">
<li><strong>Griul rece și albul „de spital”</strong>, înlocuite de neutri calzi și alb cremos.</li>
<li><strong>Plafonierele unice, puternice, în mijlocul camerei</strong>, ca singura sursă de lumină.</li>
<li><strong>Pereții 100% plați</strong> și plintele subțiri, care fac orice cameră să pară neterminată.</li>
<li><strong>Riflajele din MDF ieftin pe toate pereții</strong>: în 2027 riflajul e un accent, nu un tapet.</li>
<li><strong>Decorul încărcat, „de catalog”</strong>: mai puține obiecte, mai multă arhitectură.</li>
</ul>

{h2("tabel-tendinte", "Tabel: tendință, cameră, produse")}

<p>Folosește tabelul de mai jos ca listă de verificare atunci când planifici renovarea:</p>
{table_html}

{h2("buget", "Cât costă: exemplu de buget pentru un living")}

<p><strong>Exemplu real, calculat cu prețurile de pe decoflair.ro la {DATA_PRET}:</strong> un living de 4×5 m (perimetru 18 m), cu înălțimea de 2,70 m, în care montăm cornișă LED la tavan, plintă de 10 cm și trei chenare decorative de 80×120 cm pe peretele canapelei. Am adăugat 10% rezervă pentru tăieri, iar profilele se vând în bare de 2 m.</p>

<div style="overflow-x:auto;margin:16px 0;"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:520px;">
<thead><tr style="background:{C_GREEN};color:#fff;"><th style="padding:8px;text-align:left;">Element</th><th style="padding:8px;">Necesar</th><th style="padding:8px;">Bare de 2 m</th><th style="padding:8px;text-align:right;">Cost cu TVA</th></tr></thead>
<tbody>{budget_rows}
<tr style="background:{C_CREAM};"><td colspan="3" style="padding:10px;"><strong>Total profile</strong></td><td style="padding:10px;text-align:right;white-space:nowrap;"><strong>{lei(total)} lei</strong></td></tr>
</tbody></table></div>

<p style="font-size:14px;color:{C_MUTED};">Nu sunt incluse banda LED, alimentatorul, {ca("adezivi", "adezivul pentru profile")}, vopseaua și manopera. Prețurile pot varia; verifică pagina fiecărui produs și secțiunea {ca("oferte", "oferte speciale")}. Pentru o cameră completă la preț de pachet, vezi {ca("linea", "LINEA Room Kit")}.</p>

{h2("pasi", "Cum aplici tendințele 2027 în 5 pași")}

<ol style="line-height:1.8;">
<li><strong>Alege o singură idee forte pe cameră.</strong> Lumină indirectă în living, relief 3D în hol, verde și chenare în dormitor. Nu toate tendințele în aceeași încăpere.</li>
<li><strong>Stabilește paleta: o bază caldă și un accent.</strong> Bej sau greige pe 70% din suprafețe, verde sau albastru-gri pe 20%, lemn și metal cald pe 10%.</li>
<li><strong>Măsoară și desenează.</strong> Perimetrul pentru cornișă și plintă, axele pentru chenare. Dacă vrei să vezi rezultatul înainte, cere o {ca("randare", "randare 3D")} a camerei.</li>
<li><strong>Montează de sus în jos.</strong> Tavan (rozete, cornișe, scafe), apoi pereți (chenare, panouri, riflaje), la final plintele. Vezi {ba("montaj", "ghidul de montaj")}.</li>
<li><strong>Vopsește și aprinde lumina.</strong> Profilele se vopsesc ton pe ton sau în alb cremos; banda LED caldă, pe variator, finalizează atmosfera.</li>
</ol>

{h2("sarbatori", "Ce poți face până de sărbători")}

<p>Decembrie este luna în care casa e cea mai privită: musafiri, mese lungi, poze. Decorațiunile de Crăciun arată spectaculos pe un fundal bine finisat, iar câteva proiecte se pot face într-un singur weekend:</p>
<ul style="line-height:1.8;">
<li><strong>O cornișă LED în living</strong>: lumina caldă indirectă e cel mai bun „decor” de sărbători, și rămâne tot anul.</li>
<li><strong>Chenare pe peretele din spatele mesei</strong>: fundal elegant pentru fotografiile de familie.</li>
<li><strong>O rozetă deasupra mesei din dining</strong>, sub lustra de sărbători.</li>
</ul>
<p>Profilele de interior aflate în stoc se livrează prin curier în 1–2 zile lucrătoare. Detalii pe pagina {ca("livrare", "plată și livrare")}.</p>

{box(f'''<p style="margin:0 0 6px;font-size:20px;font-weight:700;color:{C_GREEN};">Vrei casa ta în tendințele 2027?</p>
<p style="margin:0 0 12px;">Trimite-ne o poză și dimensiunile camerei. Echipa Deco&amp;Flair îți propune profilele potrivite, cantitățile exacte și, la cerere, o randare 3D. Ne găsești la {PHONE} sau pe WhatsApp.</p>
{cta_btn}''', bg=C_SAND, border=C_GREEN)}

{h2("intrebari-frecvente", "Întrebări frecvente despre tendințele în design interior 2027")}

{faq_html}

<h2>Surse și metodologie</h2>
<p style="font-size:14px;color:{C_MUTED};line-height:1.7;">Ghidul combină anunțurile oficiale de culori pentru 2027 (<a href="https://www.benjaminmoore.com/en-us/paint-colors/color-of-the-year-2027" rel="noopener" target="_blank">Benjamin Moore, Color of the Year 2027</a>; <a href="https://www.wgsn.com/en/blog/colour-year-2027-luminous-blue" rel="noopener" target="_blank">WGSN × Coloro, Luminous Blue</a>), datele de căutare din România (Semrush, noiembrie 2026) și experiența echipei Deco&amp;Flair în proiecte de interior. Prețurile sunt cele afișate pe decoflair.ro la {DATA_PRET}, cu TVA. Imaginile de ambient sunt randări de inspirație Deco&amp;Flair; produsele exacte sunt prezentate în fișele de produs.</p>

<p>Citește și: {ba("detalii", "10 detalii arhitecturale care cresc valoarea percepută a unei locuințe")} · {ba("apartament", "Cum faci un apartament nou să nu arate ca toate celelalte")} · {ba("lux", "Design interior de lux")}</p>

<div style="display:flex;gap:14px;align-items:center;border-top:1px solid #e6dfd3;padding-top:18px;margin-top:28px;">
<div style="flex:0 0 56px;height:56px;border-radius:50%;background:{C_GREEN};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;">D&amp;F</div>
<p style="margin:0;font-size:14px;line-height:1.6;"><strong>Echipa de consultanță Deco&amp;Flair</strong>: specialiști în profile decorative de interior și exterior, tapet premium și panouri 3D, dealer autorizat NMC®. Ajutăm clienți din toată România să transforme case și apartamente cu detalii arhitecturale. {ca("consultanta", "Despre consultanța Deco&amp;Flair")}.</p>
</div>
"""

body = "\n".join(line.rstrip() for line in body.strip().splitlines() if line.strip())
(OUT / "articol-opencart.html").write_text(body + "\n", encoding="utf-8")

TITLE = "Tendințe design interior 2027: culoarea anului și 10 idei pentru o casă premium"
preview = f"""<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Previzualizare — {TITLE}</title>
<style>
body{{margin:0;background:#faf8f4;color:{C_INK};font:17px/1.7 Georgia,'Times New Roman',serif;}}
main{{max-width:860px;margin:0 auto;padding:24px 16px 80px;}}
h1{{font:700 34px/1.2 Arial,sans-serif;margin:16px 0;}}
h2{{font:700 26px/1.3 Arial,sans-serif;margin:40px 0 12px;color:{C_GREEN};}}
h3{{font:700 19px/1.4 Arial,sans-serif;margin:24px 0 8px;}}
a{{color:{C_GREEN2};}}
.cover{{width:100%;height:auto;border-radius:12px;}}
</style></head><body><main>
<img class="cover" src="../imagini/tendinte-design-interior-2027-cover.jpg" alt="">
<h1>{TITLE}</h1>
{body.replace(IMG + "/", "../imagini/")}
</main></body></html>"""
(OUT / "previzualizare.html").write_text(preview, encoding="utf-8")

words = len(__import__("re").sub(r"<[^>]+>", " ", body).split())
print(f"OK: {len(body)//1024} KB HTML, ~{words} cuvinte, total buget {lei(total)} lei")
for lab, code, m, bars, cost in rows:
    print(f"  {code}: {m} m -> {bars} bare -> {lei(cost)} lei")

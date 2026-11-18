"""Newsletter „Deco&Flair × clienții NMC” — generator.

python3 build.py            → img/ (imagini optimizate pentru e-mail) + out/*.html + out/newsletter.txt

Ieșiri:
  out/newsletter-preview.html     imagini relative (img/…) — pentru previzualizare locală
  out/newsletter-brevo.html       URL-uri absolute + tag-uri Brevo ({{ unsubscribe }}, {{ mirror }})
  out/newsletter-mailerlite.html  URL-uri absolute + tag-uri MailerLite ({$unsubscribe}, {$url})
  out/newsletter.txt              versiunea text simplu (obligatorie pentru livrabilitate)

IMG_BASE = unde urci folderul img/ (ex. Image Manager OpenCart → catalog/newsletter/2026-11/).
"""
import json, pathlib, html, re
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SRC, IMG, OUT = ROOT / "src", ROOT / "img", ROOT / "out"
IMG.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)

IMG_BASE = "https://decoflair.ro/image/catalog/newsletter/2026-11/"
SITE = "https://decoflair.ro"
CAMPAIGN = "nmc-decoflair-2027"
EXPERT_NAME = ""            # ex. „Ana Popescu” — gol = „Expertul Deco&Flair”
COUPON = None               # ex. {"code": "NMCDECO", "text": "−5% la prima comandă pe decoflair.ro"} — creează întâi codul în OpenCart!
PRICES_DATE = "18.11.2026"

# ---------- paleta (verificată în tools/palette_check.py) ----------
C = dict(forest="#1F3A2F", forest_mid="#2E5244", teal="#256F69", teal_light="#8CCBC2", aubergine="#4B2748",
         mauve="#B9A3BD", mauve_mid="#8E6E93", nude="#E9D5CC", cream="#F4EEE4", ivory="#FBF8F2", ink="#161A17",
         muted="#5B5F5A", gold="#D6BC84", gold_dark="#7A5B22", white="#FFFFFF")
SERIF = "'Playfair Display',Georgia,'Times New Roman',serif"
SANS = "Jost,'Helvetica Neue',Helvetica,Arial,sans-serif"

# ---------- imagini ----------
def fit(src, out, w, h, fx=0.5, fy=0.5, box=None, q=80):
    im = Image.open(SRC / src if not str(src).startswith("/") else src).convert("RGB")
    if box: im = im.crop(box)
    W, H = im.size; ta = w / h
    if W / H > ta:
        nw = int(H * ta); x = int((W - nw) * fx); im = im.crop((x, 0, x + nw, H))
    else:
        nh = int(W / ta); y = int((H - nh) * fy); im = im.crop((0, y, W, y + nh))
    im = im.resize((w, h), Image.LANCZOS)
    im.save(IMG / out, "JPEG", quality=q, optimize=True, progressive=True)

IMAGES = [
    ("hero.jpg", "led.jpg", 1200, 760, 0.62, 0.5),
    ("kit-linea.jpg", "kit.png", 1200, 860, 0.5, 0.55),
    ("p-l5.jpg", "l5a.jpg", 480, 480), ("p-l2.jpg", "l2.jpg", 480, 480), ("p-fd3.jpg", "fd3a.jpg", 480, 480),
    ("p-fo1.jpg", "fo1.jpg", 480, 480), ("p-wo2.jpg", "wo2a.jpg", 480, 480), ("p-fl13.jpg", "fl13.jpg", 480, 480),
    ("room-living.jpg", "amb-interior.jpg", 560, 400, 0.55, 0.6), ("room-dormitor.jpg", "wave-amb.jpg", 560, 400, 0.5, 0.6),
    ("room-hol.jpg", "blog-usi.webp", 560, 400, 0.5, 0.45), ("room-fatada.jpg", "amb-exterior.jpg", 560, 400, 0.5, 0.45),
    ("trend-canele.jpg", "canele-amb.jpg", 560, 640), ("trend-ray.jpg", "ray-amb.jpg", 560, 640),
    ("trend-icon.jpg", "icon-amb.jpg", 560, 640, 0.5, 0.0), ("trend-il18.jpg", "il18-amb.jpg", 560, 640),
    ("kit-lumina.jpg", "amb-led-floor.jpg", 400, 400, 0.45, 0.5), ("kit-galerie.jpg", "amb-chenare.jpg", 400, 400, 0.3, 0.5),
    ("kit-japandi.jpg", "riflaj-amb.jpg", 400, 400),
    ("blog-led.jpg", "blog-led.png", 560, 360, 0.5, 0.4), ("blog-chenare.jpg", "blog-chenare.jpg", 560, 360, 0.5, 0.5),
    ("blog-fatade.jpg", "blog-fatade.webp", 560, 360, 0.5, 0.5),
    ("final.jpg", "amb-tapet.jpg", 1200, 560, 0.5, 0.55),
]

def build_images():
    for spec in IMAGES:
        out, src, w, h, *f = spec
        box = (0, 0, 640, 600) if src == "icon-amb.jpg" else None  # fără colțul alb cu watermark
        fit(src, out, w, h, *(f or []), box=box)
    # expertul: cap + umeri + mâinile încrucișate, din versiunea HQ
    hq = ROOT / "expert" / "expert-hq.jpg"
    fit(str(hq), "expert.jpg", 504, 1000, 0.5, 0.0, box=(250, 0, 1978, 2824), q=84)
    Image.open(SRC / "logo-decoflair.png").save(IMG / "logo-decoflair.png", optimize=True)

# ---------- date ----------
def u(path, content):
    sep = "&" if "?" in path else "?"
    return f"{SITE}{path}{sep}utm_source=nmcromania&utm_medium=email&utm_campaign={CAMPAIGN}&utm_content={content}"

PRODUCTS = [  # prețuri cu TVA citite pe decoflair.ro/oferte-speciale la PRICES_DATE, toate „În stoc”
    dict(img="p-l5.jpg", name="Scafă LED ARSTYL® L5", note="Lumină indirectă, 2 m", old="585,36", new="526,83", unit="lei / bară", url="/l5-arstyl"),
    dict(img="p-l2.jpg", name="Scafă LED ARSTYL® L2", note="Tavan suspendat vizual", old="742,82", new="668,54", unit="lei / bară", url="/l2-arstyl"),
    dict(img="p-wo2.jpg", name="Brâu WALLSTYL® WO2", note="Pentru chenare clasice", old="66,03", new="59,43", unit="lei / bară", url="/brau-decorativwo2-wallstyl"),
    dict(img="p-fd3.jpg", name="Plintă WALLSTYL® FD3", note="10 cm, polimer dur", old="121,13", new="109,02", unit="lei / bară", url="/plintafd3-wallstyl"),
    dict(img="p-fo1.jpg", name="Plintă WALLSTYL® FO1", note="12 cm, profil elegant", old="154,73", new="139,26", unit="lei / bară", url="/plintafo1-wallstyl"),
    dict(img="p-fl13.jpg", name="Plintă polimer dur FL13", note="Linie modernă, 5,8 cm", old="73,23", new="65,91", unit="lei / bară", url="/plinta-polimer-dur-fl13-58-13-2000"),
]

ROOMS = [
    ("room-living.jpg", "Livingul", "Lumină, ritm, primire", "/cornisa-decorativa-interior", "camera-living"),
    ("room-dormitor.jpg", "Dormitorul", "Liniște și textură", "/panouri-decorative-3d-interior-poliuretan", "camera-dormitor"),
    ("room-hol.jpg", "Holul & ușile", "Prima impresie", "/chenare-decorative-perete", "camera-hol"),
    ("room-fatada.jpg", "Fațada", "Casa văzută din stradă", "/profile-decorative-exterior", "camera-fatada"),
]

TREND = [
    ("trend-canele.jpg", "CANELÉ L", "Linii verticale care înalță camera", "/panou-decorativ-canelel", "trend-canele"),
    ("trend-ray.jpg", "RAY", "Romburi care prind lumina", "/panou-decorativ-3d-ray-arstyl", "trend-ray"),
    ("trend-icon.jpg", "ICON", "Forme rotunjite, retro-futuriste", "/panou-decorativ-3d-icon", "trend-icon"),
    ("trend-il18.jpg", "Cornișă LED IL18", "Draperii scăldate în lumină", "/cornisa-led-il18-121x90x2000", "trend-il18"),
]

KITS = [
    ("kit-lumina.jpg", "Kitul „Lumină de hotel”", "Scafă LED L5 + plintă FD3", "Seara, camera pare mai înaltă și mai caldă — fără nicio lustră nouă.", "/l5-arstyl", "kit-lumina"),
    ("kit-galerie.jpg", "Kitul „Perete-galerie”", "Brâu WO2 în chenare + plintă FO1", "Chenarele transformă un perete gol într-un fundal de revistă.", "/brau-decorativwo2-wallstyl", "kit-galerie"),
    ("kit-japandi.jpg", "Kitul „Japandi 2027”", "Riflaj acustic stejar + cornișă LED IL18", "Mai puțin ecou, mai multă căldură. Ritm calm, lumină caldă.", "/riflaj-acustic-panou-3d-stejar-deschis", "kit-japandi"),
]

FAQ = [
    ("Se pot vopsi profilele?", "Da. Profilele WALLSTYL® și ARSTYL® vin preamorsate din fabrică — le vopsești direct, cu vopsea pe bază de apă, în culoarea peretelui (efect ton-pe-ton) sau în contrast."),
    ("Montajul e complicat?", "Nu. Se lipesc cu adezivii dedicați ADEFIX (lipire) și ADEFIX Plus (îmbinări). Fără praf, fără șuruburi. Pe blog găsești ghidul pas cu pas."),
    ("Rezistă în baie sau bucătărie?", "Profilele din polimer dur (HDPS) sunt rezistente la umezeală și la șocuri — potrivite și pentru spațiile „grele” ale casei."),
    ("Nu știu ce să aleg. Mă ajutați?", "Pentru asta suntem aici: consultanță de specialitate la 0723 300 603 și, pentru proiecte mai mari, randare 3D — vezi rezultatul înainte să cumperi."),
]

BLOG = [
    ("blog-led.jpg", "Lumină", "Cornișa LED: eleganță prin iluminare indirectă", "/blog/cornisa-led-iluminat-indirect-eleganta-interior", "blog-led"),
    ("blog-chenare.jpg", "Pereți", "Chenare decorative: modele, dimensiuni, proporții", "/blog/chenare-decorative-perete-modele-dimensiuni-proportii", "blog-chenare"),
    ("blog-fatade.jpg", "Exterior", "Cele mai frumoase fațade: 10 idei și combinații", "/blog/cele-mai-frumoase-fatade-de-case", "blog-fatade"),
]

ADV = [
    ("Fabricat în Belgia", "Profile de interior NMC® — ARSTYL®, WALLSTYL®, NOMASTYL® — calitate europeană, la prețul corect."),
    ("Selecție, nu stoc", "Alegem cu grijă din mulți producători: profile, tapet italian de designer, panouri 3D, riflaje."),
    ("Know-how inclus", "Îți spunem ce merge, ce e în trend și ce rămâne frumos peste ani: produs, finisaj, culoare."),
    ("Randare 3D", "Vezi camera transformată înainte de prima comandă."),
    ("Exterior la comandă", "Tu ai ideea, noi o proiectăm și o executăm din materiale premium."),
    ("Pentru orice buget", "Un singur detaliu bine ales poate schimba o cameră. Îți arătăm care."),
]

# ---------- HTML helpers ----------
def esc(s): return html.escape(s, quote=True)

def img(src, w, alt, h=None, style=""):
    hh = f' height="{h}"' if h else ""
    return (f'<img src="{{IMG}}{src}" width="{w}"{hh} alt="{esc(alt)}" '
            f'style="display:block;width:100%;max-width:{w}px;height:auto;border:0;outline:none;text-decoration:none;{style}">')

def button(text, href, bg=C["teal"], fg=C["white"], border=None):
    b = border or bg
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" class="btn" style="border-collapse:separate;"><tr>'
            f'<td align="center" bgcolor="{bg}" style="border-radius:999px;border:1px solid {b};">'
            f'<a href="{href}" target="_blank" style="display:inline-block;padding:14px 30px;font-family:{SANS};font-size:15px;'
            f'font-weight:600;letter-spacing:.04em;color:{fg};text-decoration:none;border-radius:999px;">{text}</a></td></tr></table>')

def eyebrow(text, color):
    return (f'<div style="font-family:{SANS};font-size:12px;letter-spacing:.24em;text-transform:uppercase;'
            f'color:{color};font-weight:600;margin:0 0 10px;">{text}</div>')

def h2(text, color, size=30):
    return f'<h2 style="margin:0 0 14px;font-family:{SERIF};font-weight:400;font-size:{size}px;line-height:1.18;color:{color};">{text}</h2>'

def p(text, color, size=16, extra=""):
    return f'<p style="margin:0 0 14px;font-family:{SANS};font-size:{size}px;line-height:1.6;color:{color};{extra}">{text}</p>'

def section(inner, bg, pad="44px 40px", grad=None, cls="pad"):
    g = f"background-image:{grad};" if grad else ""
    return (f'<tr><td class="{cls}" bgcolor="{bg}" style="background-color:{bg};{g}padding:{pad};">{inner}</td></tr>')

def two_col(cells, gap=16, valign="top"):
    """cells: listă de HTML; 2 pe rând, se stivuiesc pe mobil."""
    rows = []
    for i in range(0, len(cells), 2):
        a, b = cells[i], cells[i + 1] if i + 1 < len(cells) else ""
        rows.append(f'<tr><td class="col" width="50%" valign="{valign}" style="padding:0 {gap//2}px {gap}px 0;">{a}</td>'
                    f'<td class="col" width="50%" valign="{valign}" style="padding:0 0 {gap}px {gap//2}px;">{b}</td></tr>')
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{"".join(rows)}</table>'

def divider(color=C["mauve"]):
    return f'<tr><td style="padding:0 40px;" bgcolor="{C["cream"]}"><div style="height:1px;line-height:1px;background:{color};font-size:0;">&nbsp;</div></td></tr>'

# ---------- secțiuni ----------
def build_html(variant):
    E = EXPERT_NAME or "Expertul Deco&amp;Flair"
    unsub = {"preview": "#", "brevo": "{{ unsubscribe }}", "mailerlite": "{$unsubscribe}"}[variant]
    mirror = {"preview": "#", "brevo": "{{ mirror }}", "mailerlite": "{$url}"}[variant]
    pre = "Kit complet de cameră cu 15% inclus, −10% la profile LED și plinte, tendințele 2027 și sfatul expertului."

    S = []
    # bara de sus — puntea NMC → Deco&Flair
    S.append(f'''<tr><td bgcolor="{C['ink']}" style="background-color:{C['ink']};padding:10px 24px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="font-family:{SANS};font-size:12px;line-height:1.5;color:{C['nude']};">Pentru clienții NMC România · selecție Deco&amp;Flair</td>
<td align="right" style="font-family:{SANS};font-size:12px;"><a href="{mirror}" style="color:{C['gold']};text-decoration:underline;">Vezi online</a></td>
</tr></table></td></tr>''')

    # header + meniu
    nav = " ".join(f'<a href="{u(h, "meniu-" + k)}" style="color:{C["cream"]};text-decoration:none;font-family:{SANS};font-size:13px;letter-spacing:.08em;padding:0 8px;white-space:nowrap;">{t}</a>'
                   for t, h, k in [("Interior", "/profile-decorative-interior", "interior"), ("Exterior", "/profile-decorative-exterior", "exterior"),
                                   ("Tapet", "/tapet-premium-design-interior", "tapet"), ("Oferte", "/oferte-speciale", "oferte"), ("Blog", "/blog", "blog")])
    S.append(f'''<tr><td align="center" bgcolor="{C['forest']}" style="background-color:{C['forest']};padding:28px 24px 18px;">
<a href="{u('/', 'logo')}" target="_blank"><img src="{{IMG}}logo-decoflair.png" width="190" alt="Deco&amp;Flair" style="display:block;width:190px;max-width:190px;height:auto;border:0;"></a>
<div style="padding-top:16px;line-height:2;">{nav}</div></td></tr>''')

    # HERO
    S.append(f'<tr><td bgcolor="{C["forest"]}" style="background-color:{C["forest"]};"><a href="{u("/", "hero-img")}" target="_blank">{img("hero.jpg", 600, "Living elegant cu scafă LED și profile decorative Deco&Flair")}</a></td></tr>')
    S.append(section(
        eyebrow("Ediția 2027 · Statement", C["gold"]) +
        f'<h1 style="margin:0 0 16px;font-family:{SERIF};font-weight:400;font-size:40px;line-height:1.1;color:{C["cream"]};">Ai ales NMC pentru casa ta.<br><i style="color:{C["gold"]};">Acum alege cum o trăiești.</i></h1>' +
        p("Calitatea o cunoști deja. Pe <b>decoflair.ro</b> găsești restul poveștii: profile fabricate în Belgia, tapet italian de designer, panouri 3D, kituri complete de cameră — și know-how-ul nostru, pus în slujba casei tale.", C["cream"], 17) +
        p("Eleganță și lux, la prețul corect. Pentru orice buget.", C["teal_light"], 15, "font-weight:600;letter-spacing:.02em;") +
        f'<div style="height:10px;"></div>{button("Intră pe decoflair.ro", u("/", "hero-cta"), C["gold"], C["ink"])}',
        C["forest"], "36px 40px 44px", f"linear-gradient(160deg,{C['forest']} 0%,{C['forest_mid']} 55%,{C['teal']} 130%)"))

    # manifest — 3 piloni
    pill = lambda n, t, d: (f'<td class="col3" width="33%" valign="top" style="padding:0 8px;">'
                            f'<div style="font-family:{SERIF};font-size:30px;color:{C["mauve_mid"]};line-height:1;">{n}</div>'
                            f'<div style="font-family:{SANS};font-size:14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{C["ink"]};padding:8px 0 6px;">{t}</div>'
                            f'<div style="font-family:{SANS};font-size:14px;line-height:1.55;color:{C["muted"]};">{d}</div></td>')
    S.append(section(
        f'<div style="text-align:center;">{eyebrow("Manifestul nostru", C["gold_dark"])}{h2("Luxul nu e un preț.<br><i>E o alegere bine făcută.</i>", C["forest"], 32)}</div>'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px;"><tr>'
        + pill("01", "Calitate premium", "Profile de interior fabricate în Belgia, rezistente la umezeală și șocuri.")
        + pill("02", "Prețul corect", "Plătești calitatea, nu eticheta. Reduceri reale, în stoc.")
        + pill("03", "Know-how", "Îți spunem ce să alegi, cum să combini și cum se montează.")
        + '</tr></table>', C["cream"], "44px 32px"))

    # SFATUL EXPERTULUI
    tips = "".join(
        f'<tr><td valign="top" style="padding:0 12px 14px 0;font-family:{SERIF};font-size:20px;color:{C["gold"]};">{n}</td>'
        f'<td valign="top" style="padding:0 0 14px;font-family:{SANS};font-size:15px;line-height:1.55;color:{C["cream"]};"><b style="color:{C["white"]};">{t}</b> {d}</td></tr>'
        for n, t, d in [("1", "Începe cu liniile, nu cu mobila.", "Plinta, brâul și cornișa sunt rama camerei. Când sunt toate trei, camera arată „terminată”."),
                        ("2", "Lumina face jumătate din lux.", "O scafă LED pe peretele lung înalță vizual tavanul și încălzește camera seara."),
                        ("3", "2027 se poartă ton-pe-ton.", "Vopsește profilele în culoarea peretelui — verde pădure, mov prăfuit sau nude. Rezultat: eleganță discretă, de galerie.")])
    expert_txt = (eyebrow("Sfatul expertului", C["gold"]) + h2("„Un detaliu bine ales schimbă toată camera.”", C["cream"], 28) +
                  f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 10px;">{tips}</table>' +
                  f'<div style="font-family:{SANS};font-size:14px;color:{C["nude"]};padding-bottom:16px;">— {E}, consultanță design interior &amp; exterior</div>' +
                  button("Cere o consultanță", u("/consultanta-premium", "expert-cta"), C["gold"], C["ink"]))
    S.append(f'''<tr><td bgcolor="{C['aubergine']}" style="background-color:{C['aubergine']};background-image:linear-gradient(135deg,{C['aubergine']} 0%,#5E3A5B 60%,{C['mauve_mid']} 140%);padding:0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td class="col" width="42%" valign="top" style="padding:0;"><a href="{u('/consultanta-premium', 'expert-foto')}" target="_blank">{img("expert.jpg", 252, "Expertul Deco&Flair")}</a></td>
<td class="col pad" width="58%" valign="middle" style="padding:34px 32px 34px 28px;">{expert_txt}</td>
</tr></table></td></tr>''')

    # OFERTE
    def pcard(x):
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{C["white"]}" style="background:{C["white"]};border-radius:14px;overflow:hidden;">'
                f'<tr><td style="position:relative;"><a href="{u(x["url"], "oferta-" + x["img"][2:-4])}" target="_blank">{img(x["img"], 252, x["name"])}</a></td></tr>'
                f'<tr><td style="padding:14px 16px 18px;">'
                f'<div style="display:inline-block;background:{C["aubergine"]};color:{C["white"]};font-family:{SANS};font-size:11px;font-weight:700;letter-spacing:.08em;padding:4px 10px;border-radius:999px;">−10% · ÎN STOC</div>'
                f'<div style="font-family:{SERIF};font-size:18px;line-height:1.25;color:{C["ink"]};padding:10px 0 2px;">{x["name"]}</div>'
                f'<div style="font-family:{SANS};font-size:13px;color:{C["muted"]};padding-bottom:10px;">{x["note"]}</div>'
                f'<div style="font-family:{SANS};font-size:13px;color:{C["muted"]};"><s>{x["old"]} lei</s></div>'
                f'<div style="font-family:{SANS};font-size:22px;font-weight:700;color:{C["aubergine"]};">{x["new"]} <span style="font-size:13px;font-weight:400;color:{C["muted"]};">{x["unit"]}</span></div>'
                f'<div style="padding-top:10px;"><a href="{u(x["url"], "oferta-" + x["img"][2:-4])}" target="_blank" style="font-family:{SANS};font-size:14px;font-weight:600;color:{C["teal"]};text-decoration:underline;">Vezi produsul →</a></div>'
                f'</td></tr></table>')
    S.append(section(
        f'<div style="text-align:center;">{eyebrow("Reduceri active acum", C["aubergine"])}{h2("Lumină și linii perfecte,<br><i>cu 10% mai puțin.</i>", C["forest"])}'
        + p("Cele mai iubite profile de interior, în stoc, gata de livrare. Alege-le acum, montează-le înainte de sărbători.", C["ink"], 15) + '</div>'
        + '<div style="height:10px;"></div>' + two_col([pcard(x) for x in PRODUCTS])
        + f'<div style="text-align:center;padding-top:6px;">{button("Vezi toate ofertele", u("/oferte-speciale", "oferte-cta"), C["aubergine"])}</div>'
        + p(f"Prețuri cu TVA afișate pe decoflair.ro la {PRICES_DATE}, în limita stocului disponibil. Prețul valabil este cel din coș la momentul comenzii.", C["muted"], 12, "text-align:center;padding-top:14px;"),
        C["nude"], "44px 28px", f"linear-gradient(180deg,{C['nude']} 0%,{C['cream']} 100%)"))

    # KIT LINEA
    S.append(f'<tr><td bgcolor="{C["forest"]}"><a href="{u("/linea-room-kit-complet-pentru-o-cameră", "kit-linea-img")}" target="_blank">{img("kit-linea.jpg", 600, "LINEA Room Kit — set complet de profile pentru o cameră")}</a></td></tr>')
    S.append(section(
        eyebrow("Kit complet de cameră · 15% reducere inclusă", C["gold"]) + h2("LINEA Room Kit.<br><i>O cameră întreagă, o singură comandă.</i>", C["cream"], 30)
        + p("Plintă FD2 + cornișă GT + brâu WD5 — liniile care fac o cameră să arate gândită de arhitect. Fabricate în Belgia, preamorsate, gata de vopsit, montaj curat fără praf sau șuruburi.", C["cream"], 16)
        + f'<div style="font-family:{SANS};font-size:15px;color:{C["teal_light"]};padding-bottom:18px;">Preț kit: <b style="font-size:24px;color:{C["white"]};">2.838,30 lei</b> cu TVA · în stoc</div>'
        + button("Comandă kitul LINEA", u("/linea-room-kit-complet-pentru-o-cameră", "kit-linea-cta"), C["gold"], C["ink"]),
        C["forest"], "34px 40px 42px", f"linear-gradient(160deg,{C['forest']} 0%,{C['teal']} 140%)"))

    # KITURI recomandate de expert
    def krow(x):
        im_, t, items, d, h, k = x
        return (f'<tr><td class="col" width="120" valign="top" style="padding:0 18px 22px 0;"><a href="{u(h, k)}" target="_blank">{img(im_, 120, t, style="border-radius:10px;")}</a></td>'
                f'<td class="col" valign="top" style="padding:0 0 22px;"><div style="font-family:{SERIF};font-size:20px;color:{C["forest"]};">{t}</div>'
                f'<div style="font-family:{SANS};font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:{C["gold_dark"]};padding:6px 0;">{items}</div>'
                f'<div style="font-family:{SANS};font-size:15px;line-height:1.55;color:{C["ink"]};">{d} <a href="{u(h, k)}" target="_blank" style="color:{C["teal"]};font-weight:600;">Vezi →</a></div></td></tr>')
    S.append(section(
        eyebrow("Kituri recomandate de expert", C["gold_dark"]) + h2("Trei combinații care <i>nu dau greș.</i>", C["forest"])
        + p("Le-am testat în sute de proiecte. Alege kitul după starea pe care o vrei în cameră.", C["muted"], 15)
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:12px;">{"".join(krow(k) for k in KITS)}</table>',
        C["ivory"], "44px 40px 26px"))

    # SONDAJ INTERACTIV — ce cameră transformi
    def room(x):
        im_, t, d, h, k = x
        return (f'<a href="{u(h, k)}" target="_blank" style="text-decoration:none;display:block;">{img(im_, 262, t, style="border-radius:12px;")}'
                f'<div style="font-family:{SERIF};font-size:20px;color:{C["cream"]};padding:10px 0 2px;">{t} →</div>'
                f'<div style="font-family:{SANS};font-size:13px;color:{C["teal_light"]};">{d}</div></a>')
    S.append(section(
        f'<div style="text-align:center;">{eyebrow("Alege tu · un click", C["gold"])}{h2("Ce cameră transformi<br><i>în 2027?</i>", C["cream"])}'
        + p("Apasă pe camera ta și îți arătăm soluțiile potrivite — idei, produse și combinații gata făcute.", C["nude"], 15) + '</div>'
        + '<div style="height:8px;"></div>' + two_col([room(r) for r in ROOMS], 16),
        C["aubergine"], "44px 30px 28px", f"linear-gradient(160deg,{C['aubergine']} 0%,#3A1F38 100%)"))

    # TREND 2027 · TOKYO × SINGAPORE
    def tcard(x):
        im_, t, d, h, k = x
        return (f'<a href="{u(h, k)}" target="_blank" style="text-decoration:none;display:block;">{img(im_, 262, "Panou " + t, style="border-radius:12px;")}'
                f'<div style="font-family:{SANS};font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:{C["gold_dark"]};font-weight:700;padding:10px 0 2px;">ARSTYL® · NMC Belgia</div>'
                f'<div style="font-family:{SERIF};font-size:20px;color:{C["forest"]};">{t}</div>'
                f'<div style="font-family:{SANS};font-size:14px;color:{C["muted"]};">{d}</div></a>')
    TREND[3] = TREND[3]  # IL18 e WALLSTYL — eticheta se corectează mai jos
    tc = [tcard(x) for x in TREND]; tc[3] = tc[3].replace("ARSTYL® · NMC Belgia", "WALLSTYL® · NMC Belgia")
    S.append(section(
        f'<div style="text-align:center;">{eyebrow("Trend 2027 · Tokyo × Singapore", C["teal"])}{h2("Liniște, linie, lumină.<br><i>Interiorul calm al anului 2027.</i>", C["forest"])}'
        + p("Minimalism cald, texturi sculptate și lumină ascunsă — estetica marilor orașe asiatice, cu profile fabricate în Belgia. Se vopsesc în orice culoare a anului.", C["ink"], 15) + '</div>'
        + '<div style="height:8px;"></div>' + two_col(tc, 16)
        + f'<div style="text-align:center;padding-top:8px;">{button("Descoperă panourile 3D", u("/panouri-decorative-3d-interior-poliuretan", "trend-cta"), C["teal"])}</div>',
        C["cream"], "44px 30px", f"linear-gradient(180deg,{C['ivory']} 0%,{C['cream']} 100%)"))

    # Q&A
    qa = "".join(f'<tr><td style="padding:0 0 12px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{C["white"]}" style="background:{C["white"]};border-left:3px solid {C["teal"]};border-radius:10px;">'
                 f'<tr><td style="padding:16px 20px;"><div style="font-family:{SERIF};font-size:18px;color:{C["forest"]};padding-bottom:6px;">{q}</div>'
                 f'<div style="font-family:{SANS};font-size:15px;line-height:1.55;color:{C["ink"]};">{a}</div></td></tr></table></td></tr>' for q, a in FAQ)
    S.append(section(
        eyebrow("Întrebări &amp; răspunsuri", C["gold_dark"]) + h2("Ce ne întreabă <i>clienții NMC.</i>", C["forest"])
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:8px;">{qa}</table>'
        + p("Ai altă întrebare? <b>Răspunde direct la acest e-mail</b> — îți scrie un specialist, nu un robot.", C["ink"], 15, "padding-top:6px;"),
        C["nude"], "44px 40px 30px"))

    # BLOG
    brow = "".join(
        f'<tr><td class="col" width="200" valign="top" style="padding:0 18px 20px 0;"><a href="{u(h, k)}" target="_blank">{img(im_, 200, t, style="border-radius:10px;")}</a></td>'
        f'<td class="col" valign="middle" style="padding:0 0 20px;"><div style="font-family:{SANS};font-size:11px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:{C["teal"]};">{cat}</div>'
        f'<a href="{u(h, k)}" target="_blank" style="text-decoration:none;"><div style="font-family:{SERIF};font-size:20px;line-height:1.3;color:{C["forest"]};padding:6px 0;">{t}</div></a>'
        f'<a href="{u(h, k)}" target="_blank" style="font-family:{SANS};font-size:14px;font-weight:600;color:{C["teal"]};">Citește articolul →</a></td></tr>'
        for im_, cat, t, h, k in BLOG)
    S.append(section(
        eyebrow("Din jurnalul Deco&amp;Flair", C["gold_dark"]) + h2("Citește 5 minute.<br><i>Amenajează fără greșeli.</i>", C["forest"])
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:12px;">{brow}</table>'
        + button("Toate articolele", u("/blog", "blog-cta"), C["forest"]),
        C["ivory"], "44px 40px"))

    # AVANTAJE
    adv = [f'<div style="border-top:1px solid {C["gold"]};padding-top:12px;"><div style="font-family:{SERIF};font-size:19px;color:{C["gold"]};padding-bottom:4px;">{t}</div>'
           f'<div style="font-family:{SANS};font-size:14px;line-height:1.55;color:{C["cream"]};">{d}</div></div>' for t, d in ADV]
    S.append(section(
        f'<div style="text-align:center;">{eyebrow("De ce Deco&amp;Flair", C["teal_light"])}{h2("Expert premium,<br><i>la prețul corect.</i>", C["cream"])}</div>'
        + '<div style="height:12px;"></div>' + two_col(adv, 24),
        C["forest"], "44px 36px 24px", f"linear-gradient(200deg,{C['forest']} 0%,{C['forest_mid']} 70%,{C['teal']} 160%)"))

    # COD opțional
    if COUPON:
        S.append(section(
            f'<div style="text-align:center;">{eyebrow("Bun venit, client NMC", C["aubergine"])}'
            f'<div style="display:inline-block;border:2px dashed {C["aubergine"]};border-radius:12px;padding:14px 28px;font-family:{SANS};font-size:26px;font-weight:700;letter-spacing:.18em;color:{C["aubergine"]};">{COUPON["code"]}</div>'
            + p(COUPON["text"], C["ink"], 15, "padding-top:12px;") + '</div>', C["nude"], "34px 40px"))

    # FINAL
    S.append(f'<tr><td bgcolor="{C["ink"]}"><a href="{u("/tapet-premium-design-interior", "final-img")}" target="_blank">{img("final.jpg", 600, "Tapet premium de designer, ambient Deco&Flair")}</a></td></tr>')
    S.append(section(
        f'<div style="text-align:center;">{h2("Casa ta poate arăta<br><i>ca în revistă.</i>", C["cream"], 32)}'
        + p("Intră pe decoflair.ro, alege-ți ideea și lasă-ne pe noi să te ajutăm cu restul.", C["nude"], 16)
        + f'<div style="height:6px;"></div><table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td>{button("Descoperă decoflair.ro", u("/", "final-cta"), C["gold"], C["ink"])}</td></tr></table>'
        + f'<div style="font-family:{SANS};font-size:15px;color:{C["cream"]};padding-top:22px;line-height:1.8;">Consultanță: <a href="tel:+40723300603" style="color:{C["gold"]};text-decoration:none;font-weight:600;">0723 300 603</a> · '
        + f'<a href="mailto:office@decoflair.ro" style="color:{C["gold"]};text-decoration:none;">office@decoflair.ro</a><br>Luni–Vineri 07:30–16:00</div></div>',
        C["ink"], "36px 40px 40px", f"linear-gradient(180deg,{C['ink']} 0%,{C['forest']} 100%)"))

    # footer
    soc = " · ".join(f'<a href="{h}" style="color:{C["muted"]};text-decoration:underline;">{t}</a>' for t, h in
                     [("Instagram", "https://www.instagram.com/decoflairhub"), ("TikTok", "https://www.tiktok.com/@decoflairhub"), ("Facebook", "https://www.facebook.com/HubDecoFlair"), ("YouTube", "https://www.youtube.com/@Decoflairhub")])
    S.append(f'''<tr><td bgcolor="{C['cream']}" style="background-color:{C['cream']};padding:28px 40px 36px;font-family:{SANS};font-size:12px;line-height:1.7;color:{C['muted']};text-align:center;">
{soc}<br><br>
Primești acest mesaj pentru că ești client NMC România (nmcromania.ro). Deco&amp;Flair este partenerul NMC pentru design interior și exterior premium.<br>
Deco &amp; Flair Hub SRL · CUI RO 54681700 · Str. Faurei nr. 1, Sector 1, București · Depozit: Str. Comerțului nr. 3, Domnești, Ilfov<br><br>
Nu mai vrei să primești astfel de mesaje? <a href="{unsub}" style="color:{C['ink']};text-decoration:underline;">Dezabonează-te aici</a>.
</td></tr>''')

    body = "\n".join(S)
    doc = f'''<!DOCTYPE html>
<html lang="ro" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting"><meta name="format-detection" content="telephone=no,address=no,email=no,date=no">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">
<title>Deco&amp;Flair — pentru clienții NMC</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><style>h1,h2,p,div,td,a{{font-family:Georgia,serif!important}}</style><![endif]-->
<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet"><!--<![endif]-->
<style>
body{{margin:0;padding:0;width:100%!important;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background:{C['cream']};}}
table{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}} img{{-ms-interpolation-mode:bicubic;}}
a[x-apple-data-detectors]{{color:inherit!important;text-decoration:none!important;}}
.btn a:hover{{filter:brightness(1.08);}} a img:hover{{opacity:.92;}}
@media only screen and (max-width:620px){{
 .wrap{{width:100%!important;}}
 .pad{{padding-left:20px!important;padding-right:20px!important;}}
 .col{{display:block!important;width:100%!important;padding-left:0!important;padding-right:0!important;}}
 .col.pad{{padding:30px 22px!important;box-sizing:border-box;}}
 .col img{{max-width:100%!important;width:100%!important;}}
 .col3{{display:block!important;width:100%!important;padding:0 0 22px!important;text-align:center;}}
 h1{{font-size:32px!important;}} h2{{font-size:26px!important;}}
}}
</style>
</head>
<body style="margin:0;padding:0;background:{C['cream']};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{C['cream']};">{pre}{"&#847;&zwnj;&nbsp;" * 60}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{C['cream']}" style="background:{C['cream']};">
<tr><td align="center" style="padding:0;">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;margin:0 auto;">
{body}
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table>
</body></html>'''
    base = "../img/" if variant == "preview" else IMG_BASE
    return doc.replace("{IMG}", base)

def build_text():
    L = ["DECO&FLAIR — pentru clienții NMC România", "", "Ai ales NMC pentru casa ta. Acum alege cum o trăiești.",
         "Profile fabricate în Belgia, tapet italian de designer, panouri 3D, kituri complete de cameră — și know-how-ul nostru.",
         f"Intră pe decoflair.ro: {u('/', 'txt-hero')}", "", "SFATUL EXPERTULUI",
         "1. Începe cu liniile, nu cu mobila: plinta, brâul și cornișa sunt rama camerei.",
         "2. Lumina face jumătate din lux: o scafă LED pe peretele lung înalță vizual tavanul.",
         "3. 2027 se poartă ton-pe-ton: vopsește profilele în culoarea peretelui.", "",
         f"REDUCERI ACTIVE (−10%, în stoc, prețuri cu TVA la {PRICES_DATE})"]
    L += [f"- {x['name']}: {x['old']} → {x['new']} {x['unit']} — {u(x['url'], 'txt-oferta')}" for x in PRODUCTS]
    L += ["", "LINEA ROOM KIT — o cameră întreagă, o singură comandă (plintă FD2 + cornișă GT + brâu WD5, 15% inclus): 2.838,30 lei",
          u("/linea-room-kit-complet-pentru-o-cameră", "txt-kit"), "", "TREND 2027 · TOKYO × SINGAPORE"]
    L += [f"- {t}: {d} — {u(h, k)}" for _, t, d, h, k in TREND]
    L += ["", "ÎNTREBĂRI & RĂSPUNSURI"] + [f"- {q} {a}" for q, a in FAQ]
    L += ["", "DIN BLOG"] + [f"- {t} — {u(h, k)}" for _, _, t, h, k in BLOG]
    L += ["", "Consultanță: 0723 300 603 · office@decoflair.ro · Luni–Vineri 07:30–16:00",
          "Deco & Flair Hub SRL · CUI RO 54681700", "Primești acest mesaj pentru că ești client NMC România. Dezabonare: folosește linkul din e-mail."]
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    build_images()
    for v in ("preview", "brevo", "mailerlite"):
        h = build_html(v)
        (OUT / f"newsletter-{v}.html").write_text(h, encoding="utf-8")
        print(v, f"{len(h.encode('utf-8'))/1024:.1f} KB")
    (OUT / "newsletter.txt").write_text(build_text(), encoding="utf-8")
    tot = sum(f.stat().st_size for f in IMG.iterdir())
    print("imagini:", len(list(IMG.iterdir())), f"{tot/1024:.0f} KB")

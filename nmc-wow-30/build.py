"""NMC — creative „wow” −30% pentru SIDDING PANEL 3 și colțarul NCL107 (prețuri verificate pe nmcromania.ro, 17.11.2026).
Două concepte noi: A) CHAT — clientul își spune problema, NMC răspunde cu produsul și prețul;
B) MEGA-TYPE — „−30%” uriaș umplut cu textura produsului, paletă premium 2027: verde forest, negru subtil, crem, mov, roz pal.
Feed 1080x1350 + Story 1080x1920. Rulare: python3 build.py && node render.cjs
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
(ROOT / "story").mkdir(exist_ok=True)

PROD = {
    "sid": dict(name="SIDDING PANEL 3", kind="Termosistem decorativ ADRo", dims="500 × 40 × 2000 mm",
                old="223,31", new="156,31", unit="lei / buc", amb="sid3fer.jpg", amb_pos="50% 50%", img="sid3.jpg",
                tex="sid3fer.jpg", amb_note="Randare de pe nmcromania.ro",
                url="https://www.nmcromania.ro/termosistem-decorativ-sidding-panel-3-500x40x2000"),
    "ncl": dict(name="Colțar NCL107", kind="Colțar exterior decorativ ADRo", dims="300/300 × 30 × 1000 mm",
                old="248,09", new="173,66", unit="lei / buc", amb="amb-colt.jpg", amb_pos="50% 50%", img="ncl107.jpg",
                tex="amb-colt.jpg", amb_note="Ambient de inspirație",
                url="https://www.nmcromania.ro/coltar-exterior-decorativ-polistiren-ncl107-1000x30x300"),
}

CHAT = {
    "sid": [("c", "Fațada mea arată obosită, iar iarna simt frigul. Se poate face ceva fără să refac tot?"),
            ("n", "Da. <b>SIDDING PANEL 3</b> e finisaj decorativ și termoizolație într-un singur panou. Se lipește direct pe fațadă."),
            ("c", "Și îl pot avea în culoarea casei?"),
            ("n", "Sigur, se vopsește în orice culoare RAL. Iar acum are <b>−30%</b>.")],
    "ncl": [("c", "Casa e gata, dar colțurile arată… plate. Simt că lipsește ceva."),
            ("n", "Lipsește relieful. <b>Colțarul NCL107</b> dă fațadei umbre adânci și caracter."),
            ("c", "Rezistă la ger și la soare?"),
            ("n", "Rășină + nisip cuarțos, rezistent la UV, ger și umezeală. Iar acum are <b>−30%</b>.")],
}

MEGA = {
    "sid": dict(h1="Linii orizontale.", h2="Impact total.", prob="Fațadă plată, fără personalitate",
                sol="Finisaj decorativ + termoizolație, montaj prin lipire"),
    "ncl": dict(h1="Colțurile", h2="fac casa.", prob="Colțuri fără relief, fațadă fără caracter",
                sol="Relief și umbre, rezistent la UV, ger și umezeală"),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--forest:#1E3A2E;--forest2:#2F5242;--ink:#0F1110;--cream:#F3ECDF;--cream2:#E6D9C3;--sand:#CDBB9A;--mauve:#9C86A0;--aub:#4A2A47;--blush:#E8D3CD}
html,body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:var(--cream);background:var(--ink)}
.c{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--ink)}
.mesh{position:absolute;inset:-20%;background:
 radial-gradient(circle at 12% 12%,rgba(47,82,66,.95),transparent 42%),
 radial-gradient(circle at 88% 28%,rgba(74,42,71,.9),transparent 42%),
 radial-gradient(circle at 35% 92%,rgba(30,58,46,.95),transparent 48%),
 radial-gradient(circle at 92% 92%,rgba(156,134,160,.45),transparent 38%),
 radial-gradient(circle at 60% 55%,rgba(230,217,195,.10),transparent 40%),var(--ink)}
.grain{position:absolute;inset:0;opacity:.12;mix-blend-mode:overlay;background-image:radial-gradient(#fff 1px,transparent 1px);background-size:3px 3px}
.top{position:absolute;left:56px;right:56px;top:48px;display:flex;justify-content:space-between;align-items:center;z-index:10}
.logo{width:130px;border-radius:10px}
.pill{font-family:'Unbounded',sans-serif;font-weight:600;font-size:16px;letter-spacing:2px;text-transform:uppercase;padding:12px 20px;border-radius:40px;
 background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(10px)}
.pill b{background:linear-gradient(90deg,#F3ECDF,#E8D3CD 50%,#B9A3BD);-webkit-background-clip:text;background-clip:text;color:transparent}
.grad{background:linear-gradient(100deg,#F3ECDF 0%,#E8D3CD 40%,#B9A3BD 75%,#9C86A0 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.note{position:absolute;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;background:rgba(15,17,16,.65);padding:6px 12px;border-radius:20px;color:rgba(255,255,255,.85)}
.foot{position:absolute;left:56px;right:56px;bottom:40px;display:flex;justify-content:space-between;align-items:center;z-index:10}
.foot b{font-family:'Unbounded',sans-serif;font-weight:700;font-size:30px}
.foot span{font-size:15px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.8);text-align:right;line-height:1.4}

/* ===== CHAT ===== */
.chat .amb{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(1.05)}
.chat .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,17,16,.75) 0%,rgba(15,17,16,.15) 18%,rgba(15,17,16,.2) 40%,rgba(15,17,16,.88) 70%,var(--ink) 100%)}
.chat .tint{position:absolute;inset:0;background:linear-gradient(160deg,rgba(30,58,46,.45),rgba(74,42,71,.35) 60%,rgba(15,17,16,.4));mix-blend-mode:multiply}
.chat .thread{position:absolute;left:56px;right:56px;top:300px;display:flex;flex-direction:column;gap:18px}
.b{max-width:76%;padding:22px 26px;font-size:28px;line-height:1.35;border-radius:30px;box-shadow:0 14px 40px rgba(0,0,0,.35)}
.b.bc{align-self:flex-start;background:rgba(243,236,223,.95);color:#1d1f1c;border-bottom-left-radius:8px}
.b.bn{align-self:flex-end;color:var(--cream);background:linear-gradient(125deg,#2F5242 0%,#1E3A2E 45%,#4A2A47 100%);border:1px solid rgba(232,211,205,.35);border-bottom-right-radius:8px}
.b.bn b{font-weight:800;color:#E8D3CD}
.who{font-size:14px;letter-spacing:2px;text-transform:uppercase;opacity:.75;margin-bottom:6px;display:block;font-weight:600}
.typing{align-self:flex-end;display:flex;gap:8px;padding:18px 24px;border-radius:24px;background:rgba(255,255,255,.18)}
.typing i{width:12px;height:12px;border-radius:50%;background:#fff;opacity:.8}
.offer{position:absolute;left:56px;right:56px;top:auto;bottom:130px;display:flex;align-items:center;gap:26px;padding:22px;border-radius:30px;
 background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(16px);box-shadow:0 24px 70px rgba(0,0,0,.5)}
.offer .ph{flex:none;width:190px;height:190px;border-radius:22px;overflow:hidden;background:#fff}
.offer .ph img{width:100%;height:100%;object-fit:cover}
.offer .tx{flex:1}
.offer .k{font-size:15px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.75);font-weight:600}
.offer .nm{font-family:'Unbounded',sans-serif;font-weight:700;font-size:34px;margin-top:6px;line-height:1.05}
.offer .dm{font-size:19px;color:rgba(255,255,255,.75);margin-top:6px}
.offer .pr{display:flex;align-items:baseline;gap:16px;margin-top:10px}
.offer .pr s{font-size:24px;color:rgba(243,236,223,.6);text-decoration-color:#B9A3BD;text-decoration-thickness:3px}
.offer .pr b{font-family:'Unbounded',sans-serif;font-weight:800;font-size:56px}
.offer .pr span{font-size:18px;color:rgba(255,255,255,.8)}
.offer .pct{flex:none;width:150px;height:150px;border-radius:50%;display:flex;align-items:center;justify-content:center;
 font-family:'Unbounded',sans-serif;font-weight:800;font-size:34px;letter-spacing:-1px;color:var(--ink);background:conic-gradient(from 200deg,#F3ECDF,#E8D3CD,#B9A3BD,#CDBB9A,#F3ECDF);box-shadow:0 0 0 6px rgba(30,58,46,.8),0 0 50px rgba(185,163,189,.45)}

/* ===== MEGA ===== */
.mega .mesh{opacity:1}
.mega .kick{position:absolute;left:56px;top:150px;font-family:'Instrument Serif',serif;font-style:italic;font-size:46px;line-height:1.05;z-index:4}
.mega .kick b{font-family:'Unbounded',sans-serif;font-style:normal;font-weight:700;font-size:58px;display:block;letter-spacing:-1px}
.mega .huge{position:absolute;left:44px;top:300px;font-family:'Unbounded',sans-serif;font-weight:900;font-size:262px;line-height:.9;letter-spacing:-14px;
 background-size:cover;background-position:center;-webkit-background-clip:text;background-clip:text;color:transparent;
 -webkit-text-stroke:3px rgba(243,236,223,.95);filter:drop-shadow(0 20px 40px rgba(0,0,0,.45));z-index:3}
.mega .huge2{position:absolute;left:44px;top:300px;font-family:'Unbounded',sans-serif;font-weight:900;font-size:262px;line-height:.9;letter-spacing:-14px;
 color:transparent;-webkit-text-stroke:2px rgba(255,255,255,.25);transform:translate(16px,16px);z-index:2}
.mega .orb{position:absolute;right:56px;top:640px;width:400px;height:400px;border-radius:50%;overflow:hidden;z-index:5;background:#fff;
 box-shadow:0 0 0 10px rgba(255,255,255,.15),0 0 0 22px rgba(255,255,255,.06),0 40px 90px rgba(0,0,0,.55)}
.mega .orb img{width:100%;height:100%;object-fit:cover}
.mega .ps{position:absolute;left:56px;top:720px;width:540px;z-index:5;display:flex;flex-direction:column;gap:18px}
.mega .ps div{padding:20px 22px;border-radius:22px;background:rgba(15,17,16,.5);border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(12px)}
.mega .ps small{display:block;font-family:'Unbounded',sans-serif;font-weight:600;font-size:13px;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px}
.mega .ps .p small{color:#E8D3CD}.mega .ps .s small{color:#B8D0B9}
.mega .ps span{font-size:25px;line-height:1.3}
.mega .price{position:absolute;left:56px;right:56px;bottom:120px;display:flex;align-items:flex-end;justify-content:space-between;z-index:5}
.mega .price .nm{font-family:'Unbounded',sans-serif;font-weight:700;font-size:38px;line-height:1.05}
.mega .price .dm{font-size:19px;color:rgba(255,255,255,.8);margin-top:6px}
.mega .price .pv{text-align:right}
.mega .price s{font-size:26px;color:rgba(243,236,223,.65);text-decoration-color:#B9A3BD;text-decoration-thickness:3px}
.mega .price b{display:block;font-family:'Unbounded',sans-serif;font-weight:800;font-size:76px;line-height:1}
.mega .price em{font-style:normal;font-size:18px;color:rgba(255,255,255,.85)}

/* ===== STORY ===== */
body.story,.story .c{height:1920px}
.story .top{top:200px}
.story.chat .thread{top:420px;gap:24px}
.story .b{font-size:31px}
.story .offer{bottom:300px}
.story .foot{bottom:250px}
.story.mega .kick{top:310px}
.story.mega .huge,.story.mega .huge2{top:480px;font-size:262px}
.story.mega .orb{top:930px}
.story.mega .ps{top:1010px}
.story.mega .price{bottom:340px}
"""

HEAD = ('<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{t}</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800;900&family=Instrument+Serif:ital@1'
        '&family=Inter:wght@400;600;800&display=swap" rel="stylesheet"><style>' + CSS + '</style></head>')

TOP = ('<div class="top"><img class="logo" src="assets/nmc-logo.png" alt="nmc">'
       '<div class="pill">Black November · <b>−30%</b></div></div>')
FOOT = ('<div class="foot"><b>nmcromania.ro</b><span>Până pe 30 noiembrie<br>în limita stocului disponibil</span></div>')


def chat(k):
    p = PROD[k]
    th = ""
    for who, msg in CHAT[k]:
        th += f'<div class="b b{who}"><span class="who">{"Tu" if who == "c" else "NMC"}</span>{msg}</div>'
    return f"""<img class="amb" src="assets/{p['amb']}" style="object-position:{p['amb_pos']}" alt="">
<div class="tint"></div><div class="shade"></div><div class="grain"></div>
{TOP}
<span class="note" style="left:56px;top:140px">{p['amb_note']}</span>
<div class="thread">{th}</div>
<div class="offer"><div class="ph"><img src="assets/{p['img']}" alt=""></div><div class="tx">
<div class="k">{p['kind']}</div><div class="nm">{p['name']}</div><div class="dm">{p['dims']}</div>
<div class="pr"><s>{p['old']} lei</s><b class="grad">{p['new']}</b><span>{p['unit']}</span></div></div>
<div class="pct">−30%</div></div>
{FOOT}"""


def mega(k):
    p, m = PROD[k], MEGA[k]
    return f"""<div class="mesh"></div><div class="grain"></div>
{TOP}
<div class="kick"><b>{m['h1']}</b><span class="grad">{m['h2']}</span></div>
<div class="huge2">−30%</div>
<div class="huge" style="background-image:url(assets/{p['tex']})">−30%</div>
<div class="orb"><img src="assets/{p['img']}" alt=""></div>
<div class="ps"><div class="p"><small>Problema</small><span>{m['prob']}</span></div>
<div class="s"><small>Soluția · {p['name']}</small><span>{m['sol']}</span></div></div>
<div class="price"><div><div class="nm">{p['name']}</div><div class="dm">{p['kind']} · {p['dims']}</div></div>
<div class="pv"><s>{p['old']} lei</s><b class="grad">{p['new']}</b><em>{p['unit']} · TVA inclus</em></div></div>
{FOOT}"""


def page(fn, k, style, story=False):
    t = f"NMC −30% — {PROD[k]['name']} ({style})" + (" — Story" if story else "")
    cls = style + (" story" if story else "")
    return HEAD.replace('{t}', t) + f'<body class="{cls}"><div class="c {style}">' + fn(k) + '</div></body></html>'


ITEMS = [("01-sidding-panel-3-chat", chat, "sid", "chat"), ("02-sidding-panel-3-mega", mega, "sid", "mega"),
         ("03-coltar-ncl107-chat", chat, "ncl", "chat"), ("04-coltar-ncl107-mega", mega, "ncl", "mega")]
for slug, fn, k, st in ITEMS:
    (ROOT / f"{slug}.html").write_text(page(fn, k, st))
    (ROOT / "story" / f"{slug}-story.html").write_text(page(fn, k, st, True).replace('src="assets/', 'src="../assets/').replace('url(assets/', 'url(../assets/'))
print("ok", len(ITEMS))

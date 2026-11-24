"""Generează imaginile articolului din biblioteca decoflair-inspiratie-50 (JPG progresiv, nume SEO)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "decoflair-inspiratie-50" / "imagini"
OUT = ROOT / "imagini"
OUT.mkdir(exist_ok=True)

# (sursă, nume fișier, offset vertical 0=sus 1=jos, raport)
JOBS = [
    ("interior/07-living-scafa-led.png", "tendinte-design-interior-2027-living-scafa-led", 0.32, (4, 3)),
    ("interior/02-biblioteca-verde.png", "culoarea-anului-2027-perete-verde-chenare-decorative", 0.5, (4, 3)),
    ("interior/03-dormitor-greige.png", "dormitor-bej-greige-cornisa-decorativa-2027", 0.35, (4, 3)),
    ("produse-detalii/45-scafa-lumina-detaliu.png", "scafa-led-iluminat-indirect-tavan-detaliu", 0.3, (4, 3)),
    ("interior/06-hol-led-podea.png", "amenajare-hol-lumina-indirecta-plinta-led", 0.5, (4, 3)),
    ("panouri-3d/21-valuri-living.png", "panouri-decorative-perete-3d-valuri-living", 0.45, (4, 3)),
    ("riflaje/31-nuc-living.png", "riflaje-lemn-perete-living-modern", 0.5, (4, 3)),
    ("interior/05-hol-plinta.png", "plinta-decorativa-inalta-hol-minimalist", 0.65, (4, 3)),
    ("interior/04-dining-rozeta.png", "rozeta-tavan-cornisa-dining-clasic-modern", 0.0, (4, 3)),
    ("panouri-3d/25-boutique-organic.png", "pereti-curbati-relief-organic-design-2027", 0.45, (4, 3)),
    ("produse-detalii/49-tapet-marmura.png", "tapet-marmura-premium-living", 0.5, (4, 3)),
    ("produse-detalii/50-moodboard-casa.png", "moodboard-paleta-2027-profile-tapet-riflaj", 0.5, (4, 3)),
    # imagine principală (Image în OpenCart) + imagine de distribuire socială
    ("interior/07-living-scafa-led.png", "tendinte-design-interior-2027-cover", 0.36, (3, 2)),
    ("interior/07-living-scafa-led.png", "tendinte-design-interior-2027-og", 0.4, (40, 21)),
]

def crop(img, offset, ratio):
    w, h = img.size
    rw, rh = ratio
    th = round(w * rh / rw)
    if th <= h:
        y = round((h - th) * offset)
        return img.crop((0, y, w, y + th))
    tw = round(h * rw / rh)
    x = (w - tw) // 2
    return img.crop((x, 0, x + tw, h))

for src, name, off, ratio in JOBS:
    matches = list(SRC.glob(src.split("/")[0] + "/" + src.split("/")[1].split("-")[0] + "-*.png"))
    path = SRC / src if (SRC / src).exists() else matches[0]
    im = crop(Image.open(path).convert("RGB"), off, ratio)
    W = 1200
    im = im.resize((W, round(W * ratio[1] / ratio[0])), Image.LANCZOS)
    dst = OUT / f"{name}.jpg"
    im.save(dst, "JPEG", quality=80, optimize=True, progressive=True)
    print(f"{dst.name:60s} {im.size} {dst.stat().st_size//1024} KB  <- {path.name}")

"""Pune tablouri (printuri abstracte desenate aici) in chenarele din doua fotografii reale de ambient,
ca sa arate ce inseamna caroiaje „gen rame de tablouri”. -> src/amb/wl1-*.jpg
Rulare: python3 tools/tablouri.py CALE_261.png (imaginea Linea Room Kit de pe decoflair.ro)"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)

def art(kind, w, h, seed):
    r = random.Random(seed); S = 4; W, H = w * S, h * S
    paper = {'leaf': (241, 236, 226), 'arch': (238, 228, 214), 'sun': (236, 230, 218), 'line': (244, 240, 233)}[kind]
    im = Image.new('RGB', (W, H), paper); d = ImageDraw.Draw(im)
    if kind == 'arch':
        cols = [(196, 120, 86), (222, 180, 140), (122, 132, 104), (170, 96, 70)]
        for i, c in enumerate(cols):
            x0 = W * (0.12 + 0.18 * i); y0 = H * (0.3 + 0.08 * (i % 2)); ww = W * 0.36
            d.rounded_rectangle([x0, y0, x0 + ww, H * 0.9], radius=ww / 2, fill=c)
    elif kind == 'sun':
        d.ellipse([W * .55, H * .14, W * .85, H * .14 + W * .3], fill=(214, 150, 96))
        for k, c in enumerate([(160, 170, 140), (110, 128, 104), (82, 98, 80)]):
            pts = [(0, H)] + [(x, H * (0.55 + 0.1 * k) + math.sin(x / W * 6 + k * 2) * H * 0.05) for x in range(0, W + 1, W // 40)] + [(W, H)]
            d.polygon(pts, fill=c)
    elif kind == 'leaf':
        stem = [(W * .5 + math.sin(t / 10) * W * .08, H * (0.88 - t / 100 * 0.75)) for t in range(0, 101, 5)]
        d.line(stem, fill=(92, 110, 82), width=S * 2)
        for i, (x, y) in enumerate(stem[2:-1]):
            s = 1 if i % 2 else -1; L = W * (0.22 - i * 0.006)
            box = [x, y - L * .18, x + s * L, y + L * .18] if s > 0 else [x - L, y - L * .18, x, y + L * .18]
            leaf = Image.new('L', (W, H), 0); ImageDraw.Draw(leaf).ellipse(box, fill=255)
            leaf = leaf.rotate(s * 28, center=(x, y)); im.paste((112 + i * 3, 130, 96), (0, 0), leaf)
    else:
        d.line([(W * .2, H * .7), (W * .45, H * .3), (W * .6, H * .55), (W * .8, H * .25)], fill=(40, 40, 40), width=S * 2)
        d.ellipse([W * .62, H * .62, W * .78, H * .62 + W * .16], fill=(196, 120, 86))
    return im.resize((w, h), Image.LANCZOS)

def framed(kind, w, h, seed, frame=(34, 30, 28), mat=0.14):
    m = int(w * mat); f = max(3, w // 40)
    a = art(kind, w - 2 * (m + f), h - 2 * (m + f), seed)
    im = Image.new('RGB', (w, h), frame); ImageDraw.Draw(im).rectangle([f, f, w - f - 1, h - f - 1], fill=(248, 246, 241))
    im.paste(a, (f + m, f + m)); return im

def put(bg, piece, x, y, shadow=(10, 14), light=0.97):
    sh = Image.new('L', bg.size, 0); ImageDraw.Draw(sh).rectangle([x + shadow[0], y + shadow[1], x + piece.width + shadow[0], y + piece.height + shadow[1]], fill=80)
    sh = sh.filter(ImageFilter.GaussianBlur(9)); dark = Image.new('RGB', bg.size, (40, 30, 25))
    bg = Image.composite(dark, bg, sh)
    p = piece.point(lambda v: int(v * light)); bg.paste(p, (x, y)); return bg

def main(p261):
    out = os.path.join(ROOT, 'src', 'amb'); os.makedirs(out, exist_ok=True)
    a = Image.open(p261).convert('RGB')   # 900x900, chenare: stanga 72-272, centru 313-588, dreapta 628-828 (sus 0-472)
    a = put(a, framed('leaf', 120, 165, 1), 112, 160, light=0.95)
    a = put(a, framed('arch', 160, 215, 2), 370, 130, light=0.97)
    a = put(a, framed('sun', 120, 150, 3), 668, 120, light=0.95)
    a.save(os.path.join(out, 'wl1-living-tablouri.jpg'), quality=95)
    k = Image.open(os.path.join(REPO, 'catalog-fatade', 'jpg', '15-bucatarie-terracota-chenare-brau.jpg')).convert('RGB')
    # chenare: A x 600-860 y 95-495; B x 915-1192 y 80-497 (lumina din stanga)
    k = put(k, framed('leaf', 140, 190, 4, frame=(150, 112, 70)), 660, 190, shadow=(12, 12), light=0.93)
    k = put(k, framed('arch', 160, 215, 5, frame=(150, 112, 70)), 973, 180, shadow=(12, 12), light=0.9)
    k.save(os.path.join(out, 'wl1-bucatarie-tablouri.jpg'), quality=95)
    print('ok')
if __name__ == '__main__': main(sys.argv[1])

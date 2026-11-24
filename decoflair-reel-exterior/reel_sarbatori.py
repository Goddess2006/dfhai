"""Product-led Deco & Flair exterior advertisement with original music."""
import argparse
from functools import lru_cache
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent
SHARED = ROOT.parent / "decoflair-reels-2027"
sys.path.insert(0, str(SHARED))
from render import (BEAT, BURGUNDY, FPS, GOLD, HEIGHT, IVORY, WIDTH, brand,
                    font, lines, reveal, wash, write_music)

INK = "#172119"
DARK = "#101710"
PAPER = "#f2e8d8"
BROWN = "#38291b"
RULE = "#bd9b69"
FADE = "#695942"
MARKS = tuple(n * BEAT for n in (0, 4, 12, 19, 26, 31, 37))
TOTAL = MARKS[-1]
AFTER = ROOT / "codex" / "03-fatada-aurie.jpg"
BEFORE = ROOT / "codex" / "03-fatada-fara-coltare.jpg"
ASSETS = ROOT / "assets"
SIZE = WIDTH, HEIGHT


@lru_cache(maxsize=12)
def fitted(path, size, crop=None):
    with Image.open(path) as source:
        source = source.convert("RGB")
        if crop:
            source = source.crop(crop)
        return ImageOps.fit(source, size, Image.Resampling.LANCZOS)


@lru_cache(maxsize=8)
def portrait(path, size):
    with Image.open(path) as source:
        return ImageOps.contain(source.convert("RGB"), size, Image.Resampling.LANCZOS)


def centered(draw, text, y, size, fill, kind="serif"):
    draw.text((WIDTH // 2, y), text, anchor="mt", font=font(kind, size), fill=fill)


def rule(draw, y, x=91, end=735, color=RULE):
    draw.line((x, y, end, y), fill=color, width=1)


@lru_cache(maxsize=8)
def facade_mask(height):
    return wash((WIDTH, height), [(0,101),(218,255),(566,255),(height-1,0)])


def facade(path, height, progress=0):
    source = fitted(path, (WIDTH + 64, height + 90))
    offset = round(28 - 16 * progress)
    overscan = round(35 * (1-progress))
    box = (offset, 25, offset + WIDTH + overscan, 25 + height + overscan)
    return source.resize((WIDTH,height), Image.Resampling.BILINEAR, box=box)


def house_base(path, height, progress):
    canvas = Image.new("RGB", SIZE, INK)
    canvas.paste(facade(path, height, progress), (0,0), facade_mask(height))
    return canvas


def hook(local, cover=False):
    completed = cover or local < 33
    path = AFTER if completed else BEFORE
    canvas = house_base(path, 1335, local / MARKS[1])
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    hero = portrait(ASSETS/"p-ncl107-hero-crop.jpg", (145,287))
    panel_x, panel_y = 548, 848
    draw.rectangle((panel_x, panel_y, 731, 1173), fill=PAPER, outline=RULE)
    canvas.paste(hero, (panel_x + (184-hero.width)//2, panel_y+14))
    draw.text((panel_x+92, 1139), "NCL107", font=font("bold", 22), anchor="mt", fill=BROWN)

    if completed:
        lines(draw, ("Ultimul detaliu", "al fațadei"), (91, 947), 72, IVORY, 69)
    else:
        lines(draw, ("Ce-i lipsește", "colțului?"), (91, 929), 83, IVORY, 75)
    caption = "Vizualizare de inspirație" if completed and not cover else "Profile decorative de exterior"
    draw.text((91,1138),caption,font=font("sans",22),fill=GOLD,anchor="lt")
    rule(draw, 1252)
    return canvas


@lru_cache(maxsize=1)
def product_stage():
    canvas = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    draw.text((91, 256), "Colțar cu bosaje", font=font("serif", 82), fill=IVORY, anchor="lt")
    draw.text((91, 353), "NCL107", font=font("bold", 27), fill=GOLD, anchor="lt")
    draw.rectangle((91, 432, 737, 1125), fill=PAPER, outline=RULE)
    hero = portrait(ASSETS/"p-ncl107-hero-crop.jpg", (268,617))
    canvas.paste(hero, (110 + (268-hero.width)//2, 467))
    draw.line((407,472,407,1086),fill="#b39977",width=1)
    technical = fitted(ASSETS/"p-ncl107-sectiune.jpg", (235,235), (155,155,645,645))
    canvas.paste(technical, (459,539))
    lines(draw, ("Profil în L", "pentru muchie"), (452, 827), 45, BROWN, 44)
    draw.text((452,959),"300 × 300 × 30",font=font("sans",22),fill=BROWN,anchor="lt")
    draw.text((452,990),"× 1.000 mm",font=font("sans",22),fill=BROWN,anchor="lt")
    rule(draw, 1235)
    return canvas


def companion_card(canvas, y, path, title, code):
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((91,y,736,y+253),fill=PAPER,outline=RULE)
    item = fitted(path, (221,207), (0,110,800,690))
    canvas.paste(item,(112,y+23))
    draw.text((364,y+66),title,font=font("serif",53),fill=BROWN,anchor="lt")
    draw.text((364,y+145),code,font=font("bold",25),fill=BROWN,anchor="lt")


def companions(local):
    canvas = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    lines(draw, ("Completează", "fațada"), (91, 246), 82, IVORY, 78)
    offset = round(37 * (1 - reveal(local,0,12)))
    companion_card(canvas, 490 + offset, SHARED/"assets"/"na107-produs.jpg", "Ancadrament", "NA107")
    offset = round(48 * (1 - reveal(local,4,12)))
    companion_card(canvas, 792 + offset, ASSETS/"p-nc104-main.jpg", "Cornișă", "NC104")
    rule(draw, 1235)
    return canvas


def comparison(local):
    duration = MARKS[3] - MARKS[2]
    progress = local / duration
    height = 1370
    before = house_base(BEFORE, height, progress * .45)
    after = house_base(AFTER, height, progress * .45)
    reveal_x = round(WIDTH * reveal(local,15,50))
    if reveal_x > 0:
        before.paste(after.crop((0,0,reveal_x,HEIGHT)), (0,0))
    draw = ImageDraw.Draw(before)
    brand(draw)
    if 0 < reveal_x < WIDTH:
        draw.line((reveal_x,218,reveal_x,1045),fill=GOLD,width=3)
    if reveal_x < 390:
        draw.text((91,1077),"Înainte",font=font("serif",78),fill=IVORY,anchor="lt")
    else:
        draw.text((91,1077),"După",font=font("serif",78),fill=IVORY,anchor="lt")
    draw.text((91,1171),"Vizualizare de inspirație",font=font("sans",23),fill=GOLD,anchor="lt")
    return before


def ready_stock(local):
    canvas = house_base(AFTER, 1365, local / (MARKS[5]-MARKS[4]) * .32)
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    draw.rectangle((91, 808, 737, 1195), fill=INK, outline=RULE)
    draw.text((121,844),"Pregătește fațada pentru sărbători",font=font("sans",23),fill=GOLD,anchor="lt")
    draw.text((121,905),"Stocuri mari",font=font("serif",77),fill=IVORY,anchor="lt")
    draw.text((121,999),"la modelele din clip",font=font("sans",25),fill=IVORY,anchor="lt")
    rule(draw,1060,x=121,end=709)
    draw.text((121,1086),"Livrare în 3–5 zile lucrătoare",font=font("bold",27),fill=GOLD,anchor="lt")
    draw.text((121,1137),"Estimativ, de la confirmarea comenzii",font=font("sans",19),fill=IVORY,anchor="lt")
    return canvas


@lru_cache(maxsize=1)
def brand_plate():
    mask = Image.new("L", SIZE)
    centered(ImageDraw.Draw(mask), "decoflair.ro", 690, 129, 255)
    return mask


def closing(local):
    canvas = Image.new("RGB",SIZE,DARK)
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    draw.rectangle((58,330,WIDTH-58,1110), outline=FADE)
    rule(draw,630,x=WIDTH//2-43,end=WIDTH//2+43,color=GOLD)
    canvas.paste(GOLD,(0,0,WIDTH,HEIGHT),brand_plate())
    shift = round(900 * reveal(local,6,51))
    left, right = max(0,shift-105), min(WIDTH,shift+80)
    if left < right:
        mask = brand_plate().crop((left,685,right,835))
        shimmer = Image.new("L", (right-left,1))
        shimmer.putdata([round(98*max(0,1-abs(x-shift)/96)) for x in range(left,right)])
        gradient = shimmer.resize(mask.size)
        alpha = ImageChops.multiply(mask,gradient)
        canvas.paste(IVORY,(left,685,right,835),alpha)
    centered(draw,"NCL107  ·  NA107  ·  NC104", 551, 23, GOLD, "bold")
    centered(draw,"Comandă profilele de exterior", 881, 33, IVORY, "bold")
    return canvas


def frame_at(frame):
    if frame < MARKS[1]:
        return hook(frame)
    if frame < MARKS[2]:
        return product_stage()
    if frame < MARKS[3]:
        return comparison(frame-MARKS[2])
    if frame < MARKS[4]:
        return companions(frame-MARKS[3])
    if frame < MARKS[5]:
        return ready_stock(frame-MARKS[4])
    local = frame-MARKS[5]
    if local < 9:
        return Image.blend(ready_stock(MARKS[5]-MARKS[4]-1),closing(local),reveal(local,0,9))
    return closing(local)


def export(output, ffmpeg, stills=False):
    output.mkdir(parents=True,exist_ok=True)
    hook(32,cover=True).resize((1080,1920),Image.Resampling.LANCZOS).save(
        output/"coperta-sarbatori.jpg", quality=92, optimize=True, progressive=True)
    if stills:
        return
    with tempfile.TemporaryDirectory() as folder:
        wav = Path(folder)/"sound.wav"
        write_music(wav,"exterior",TOTAL,accents=(MARKS[1],MARKS[2]+32,MARKS[5]))
        args = [ffmpeg,"-y","-hide_banner","-loglevel","error","-filter_threads","2",
                "-f","rawvideo","-pixel_format","rgb24","-video_size",f"{WIDTH}x{HEIGHT}",
                "-framerate",str(FPS),"-i","pipe:0","-i",str(wav),"-map","0:v","-map","1:a",
                "-vf","scale=1080:1920:flags=lanczos:out_color_matrix=bt709,format=yuv420p,setsar=1",
                "-c:v","libx264","-preset","fast","-crf","19","-threads","2",
                "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                "-af","volume=2.7,alimiter=limit=0.8:level=false","-c:a","aac","-b:a","160k",
                "-movflags","+faststart",str(output/"decoflair-exterior-sarbatori-ads.mp4")]
        with subprocess.Popen(args,stdin=subprocess.PIPE) as process:
            assert process.stdin is not None
            for frame in range(TOTAL):
                process.stdin.write(frame_at(frame).tobytes())
            process.stdin.close()
            if process.wait():
                raise RuntimeError("Exportul FFmpeg a eșuat")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--output", type=Path, default=ROOT/"reel")
    parser.add_argument("--stills", action="store_true")
    options = parser.parse_args()
    export(options.output,options.ffmpeg,options.stills)

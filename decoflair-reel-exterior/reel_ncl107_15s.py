"""Render the product-led 15-second NCL107 advertisement."""
import argparse
from functools import lru_cache
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "decoflair-reels-2027"))
from render import FPS, HEIGHT, WIDTH, brand, font, reveal, write_music

SIZE = (WIDTH, HEIGHT)
ASSETS = ROOT / "assets"
INK = "#141b2f"
COBALT = "#2847db"
PALE = "#b6c6ff"
PAPER = "#f6f0e6"
DARK = "#24212a"
CUTS = (72, 150, 246, 342)
TOTAL = 15 * FPS


@lru_cache(maxsize=5)
def source(name):
    with Image.open(ASSETS / name) as image:
        return image.convert("RGB")


def text(draw, xy, value, size, color=PAPER, kind="sans", anchor="lt"):
    draw.text(xy, value, font=font(kind, size), fill=color, anchor=anchor)


def studio():
    frame = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(frame)
    brand(draw)
    draw.line((91, 1250, 735, 1250), fill="#52618b")
    return frame, draw


def hero(local):
    frame, draw = studio()
    text(draw, (91, 202), "COLȚAR EXTERIOR", 29, PALE, "bold")
    text(draw, (91, 255), "NCL107", 113, PAPER, "bold")
    draw.rounded_rectangle((91, 404, 735, 1051), radius=8, fill=PAPER)
    progress = reveal(local, 0, CUTS[0])
    height = 580 + round(38 * progress)
    photo = source("p-ncl107-hero-crop.jpg")
    tile = ImageOps.contain(photo, (369, height), Image.Resampling.LANCZOS)
    frame.paste(tile, (414-tile.width//2, 727-tile.height//2))
    draw.line((113, 1014, 113+round(598*progress), 1014), fill=COBALT, width=4)
    text(draw, (91, 1111), "Colțar cu bosaje", 60, PAPER, "serif")
    return frame


def detail(local):
    frame, draw = studio()
    text(draw, (91, 232), "Profil în L", 111, PAPER, "serif")
    text(draw, (91, 349), "Pentru muchia fațadei", 32, PALE)
    draw.rounded_rectangle((91, 438, 735, 1048), radius=8, fill=PAPER)
    product = ImageOps.contain(source("p-ncl107-hero-crop.jpg"), (247, 535), Image.Resampling.LANCZOS)
    frame.paste(product, (115, 480))
    section = source("p-ncl107-sectiune.jpg").crop((154, 153, 647, 645))
    section.thumbnail((296,296),Image.Resampling.LANCZOS)
    timing = reveal(local, 2, 11)
    placeholder = Image.new("RGB",section.size,PAPER)
    frame.paste(Image.blend(placeholder,section,timing),(406,546))
    draw.line((365, 480, 365, 1005), fill="#c2b5a5")
    text(draw, (411, 880), "Secțiune NCL107", 26, DARK, "bold")
    return frame


@lru_cache(maxsize=1)
def facade():
    finish = ImageOps.fit(source("r-coltare.jpg"), (720,762), Image.Resampling.LANCZOS,
                          centering=(.28,.54))
    return finish


def application(local):
    frame, draw = studio()
    text(draw, (91, 211), "Muchia în prim-plan", 66, PAPER, "serif")
    draw.rectangle((91,330,735,1102),fill=COBALT)
    shot = facade()
    progress = reveal(local,0,CUTS[2]-CUTS[1])
    margin = round(30*(1-progress))
    window = (0, margin, 644+margin, 762)
    frame.paste(shot.resize((638,766),Image.Resampling.BILINEAR,box=window),(94,333))
    text(draw, (91, 1150), "Exemplu de fațadă cu bosaje", 26, PALE)
    return frame


@lru_cache(maxsize=1)
def availability():
    frame, draw = studio()
    text(draw,(91,263),"NCL107",33,PALE,"bold")
    draw.rounded_rectangle((91, 336, 735, 644), radius=10, fill=COBALT)
    text(draw,(129,413),"În stoc",128,PAPER,"serif")
    text(draw,(91,743),"Livrare estimată",35,PALE)
    text(draw,(91,803),"3–5 zile lucrătoare",76,PAPER,"serif")
    text(draw,(91,928),"De la confirmarea comenzii",31,PALE)
    return frame


def closing(local):
    frame, draw = studio()
    draw.rounded_rectangle((70, 361, WIDTH-70, 1112), radius=8, outline="#5367af", width=2)
    position = round(606*reveal(local,0,20))
    draw.line((129, 542, 129+position, 542), fill=PALE, width=4)
    text(draw,(WIDTH//2,642),"Comandă NCL107",62,PAPER,"bold","mt")
    text(draw,(WIDTH//2,784),"decoflair.ro",83,PALE,"serif","mt")
    return frame


def frame_at(frame):
    if frame < CUTS[0]:
        return hero(frame)
    if frame < CUTS[1]:
        return detail(frame-CUTS[0])
    if frame < CUTS[2]:
        return availability()
    if frame < CUTS[3]:
        return application(frame-CUTS[2])
    return closing(frame-CUTS[3])


def export(ffmpeg, output):
    output.mkdir(parents=True, exist_ok=True)
    hero(22).resize((1080,1920), Image.Resampling.LANCZOS).save(
        output/"coperta-ncl107-15s.jpg", quality=92, optimize=True, progressive=True)
    with tempfile.TemporaryDirectory() as temp:
        wav = Path(temp)/"sound.wav"
        write_music(wav, "exterior", TOTAL, accents=CUTS)
        command = [ffmpeg,"-y","-hide_banner","-loglevel","error","-filter_threads","2",
                   "-f","rawvideo","-pixel_format","rgb24","-video_size",f"{WIDTH}x{HEIGHT}",
                   "-framerate",str(FPS),"-i","pipe:0","-i",str(wav),"-map","0:v","-map","1:a",
                   "-vf","scale=1080:1920:flags=lanczos:out_color_matrix=bt709,format=yuv420p,setsar=1",
                   "-c:v","libx264","-preset","fast","-crf","19","-threads","2",
                   "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                   "-af","volume=2.7,alimiter=limit=0.8:level=false","-c:a","aac","-b:a","160k",
                   "-movflags","+faststart",str(output/"decoflair-ncl107-ads-15s.mp4")]
        with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
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
    options = parser.parse_args()
    export(options.ffmpeg, options.output)

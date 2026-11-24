"""Finish the 15-second NCL107 dusk ad from continuous generated footage."""

import argparse
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image, ImageChops, ImageDraw

from reel_ncl107_lumina import font, soundtrack

ROOT = Path(__file__).resolve().parent
SIZE = (1080, 1920)
DURATION = 15
CTA_START = 10.3
EMPTY = (0, 0, 0, 0)
IVORY = "#f9f0e3"
GOLD = "#efca9f"


def overlay(path, final):
    image = Image.new("RGBA", SIZE, EMPTY)
    vertical = Image.new("L", (1, SIZE[1]))
    opacity = 177 if final else 136
    vertical.putdata([
        round(opacity * min(1, max(0,(y-795)/580))**1.6)
        for y in range(SIZE[1])
    ])
    horizontal = Image.new("L", (SIZE[0], 1))
    horizontal.putdata([round(255 * min(1, max(0, (878-x)/180))) for x in range(SIZE[0])])
    shade = Image.new("RGBA", SIZE, (23, 15, 11, 0))
    shade.putalpha(ImageChops.multiply(vertical.resize(SIZE), horizontal.resize(SIZE)))
    image.alpha_composite(shade)
    draw = ImageDraw.Draw(image)
    if final:
        draw.line((103,1110,219,1110), fill=GOLD, width=2)
        draw.text((103,1156), "Comandă NCL107", font=font("bold", 77), fill=IVORY, anchor="lt")
        draw.text((105,1280), "decoflair.ro", font=font("bold", 39), fill=GOLD, anchor="lt")
        draw.text((105,1367), "În stoc · Livrare estimată", font=font("sans", 35), fill=IVORY, anchor="lt")
        draw.text((105,1415), "3–5 zile lucrătoare de la confirmare", font=font("sans", 31),
                  fill=IVORY, anchor="lt")
    else:
        draw.text((103,1184), "Colțar de fațadă", font=font("sans", 39), fill=IVORY, anchor="lt")
        draw.text((101,1249), "NCL107", font=font("bold", 105), fill=IVORY, anchor="lt")
    image.save(path)


def require_native_dimensions(ffmpeg, footage):
    probe = subprocess.run([
        ffmpeg, "-hide_banner", "-i", str(footage),
        "-map", "0:v:0", "-frames:v", "1", "-f", "null", "-"
    ], capture_output=True, text=True, check=True)
    stream = re.search(r"Video:[^\n]*?\b(\d{2,5})x(\d{2,5})\b", probe.stderr)
    if not stream:
        raise ValueError("Dimensiunile fluxului video nu au putut fi citite.")
    width, height = map(int, stream.groups())
    if (width, height) != SIZE:
        raise ValueError(
            f"Sursa are {width} × {height}. Modul nativ cere o sursă de 1080 × 1920."
        )


def export(ffmpeg, footage, output, native=False):
    if native:
        require_native_dimensions(ffmpeg, footage)
    base = "setpts=PTS-STARTPTS,fps=30,"
    if not native:
        base += ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
                 "crop=1080:1920,unsharp=5:5:0.28:5:5:0,")
    output.mkdir(parents=True, exist_ok=True)
    suffix = "-nativ" if native else ""
    target = output/f"decoflair-ncl107-amurg-ads-15s{suffix}.mp4"
    with tempfile.TemporaryDirectory() as workspace:
        work = Path(workspace)
        opening, closing, music = (work/name for name in ("open.png", "close.png", "music.wav"))
        overlay(opening, False)
        overlay(closing, True)
        soundtrack(music)
        # The base is moving footage throughout, including behind the call to action.
        graph = (
            f"[0:v]{base}setsar=1[film];"
            "[1:v]format=rgba,fade=t=out:st=2.4:d=0.32:alpha=1[hook];"
            f"[2:v]format=rgba,fade=t=in:st={CTA_START}:d=0.38:alpha=1[cta];"
            "[film][hook]overlay=enable='lt(t,2.73)'[intro];"
            f"[intro][cta]overlay=enable='gte(t,{CTA_START})'[out]"
        )
        subprocess.run([
            ffmpeg,"-hide_banner","-loglevel","error","-y","-filter_complex_threads","2",
            "-i",str(footage),"-loop","1","-framerate","30","-i",str(opening),
            "-loop","1","-framerate","30","-i",str(closing),"-i",str(music),
            "-filter_complex",graph,"-map","[out]","-map","3:a","-t",str(DURATION),
            "-c:v","libx264","-preset","fast","-crf","18","-threads","2","-pix_fmt","yuv420p",
            "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
            "-c:a","aac","-b:a","160k","-af","volume=1.3,alimiter=limit=0.8:level=false",
            "-movflags","+faststart",str(target)
        ],check=True)
    subprocess.run([
        ffmpeg,"-hide_banner","-loglevel","error","-y","-ss","8.8","-i",str(target),
        "-frames:v","1","-q:v","2",str(output/f"coperta-ncl107-amurg{suffix}.jpg")
    ],check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("footage", type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--output", type=Path, default=ROOT/"reel")
    parser.add_argument("--native", action="store_true", help="Cere o sursă de 1080 × 1920 și păstrează dimensiunile.")
    args = parser.parse_args()
    export(args.ffmpeg,args.footage,args.output,native=args.native)

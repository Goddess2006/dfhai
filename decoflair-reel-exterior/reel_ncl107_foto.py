"""Compose the NCL107 spot from catalog imagery and two real exterior projects."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

from reel_ncl107_lumina import ASSETS, ROOT, font, soundtrack

WIDTH, HEIGHT = 1080, 1920
SIZE = WIDTH, HEIGHT
FPS = 24
INK = "#1c1916"
LIGHT = "#f5eddf"
GOLD = "#d3ad7a"
PAPER = "#f1ede4"
BROWN = "#514438"
EXTRANET_ID = "NMC_02_003087_original.jpg"
STEM = "decoflair-ncl107-foto-ads-15s"


def load(path):
    with Image.open(path) as original:
        return ImageOps.exif_transpose(original).convert("RGB")


def crop(im, box, size):
    width, height = im.size
    region = tuple(c * (width if i % 2 == 0 else height) for i, c in enumerate(box))
    return ImageOps.fit(im.crop(region), size, Image.Resampling.LANCZOS)


def label(draw, x, y, wording, color=LIGHT):
    draw.text((x, y), wording, font=font("bold", 28), fill=color, anchor="lt")


def title(draw, x, y, wording, size, color=LIGHT):
    draw.text((x, y), wording, font=font("serif", size), fill=color, anchor="lt")


def marked_background(photo, box, tag):
    img = crop(photo, box, SIZE).convert("RGBA")
    gradient = Image.new("L", (1, HEIGHT))
    gradient.putdata([
        round(179 * max(0, 1 - y / 400) + 171 * max(0, (y - 1190) / 730))
        for y in range(HEIGHT)
    ])
    shade = Image.new("RGBA", SIZE, INK)
    shade.putalpha(gradient.resize(SIZE))
    img.alpha_composite(shade)
    label(ImageDraw.Draw(img), 102, 275, tag)
    return img.convert("RGB")


def product_frame():
    frame = Image.new("RGB", SIZE, PAPER)
    item = load(ASSETS / "p-ncl107-hero.jpg")
    # This crop preserves the ends of the L-profile and its original shadow.
    item = item.crop((365, 94, 796, 1082))
    item.thumbnail((399, 812), Image.Resampling.LANCZOS)
    white = item.getpixel((5, 5))
    # Match the catalog backdrop to the paper using a uniform color correction.
    channel_luts = [
        [max(0, min(255, value + target - origin)) for value in range(256)]
        for origin, target in zip(white, (241, 237, 228))
    ]
    item = Image.merge("RGB", tuple(channel.point(lut) for channel, lut in zip(item.split(), channel_luts)))
    frame.paste(item, (535, 495))
    draw = ImageDraw.Draw(frame)
    label(draw, 103, 513, "COLȚAR DE FAȚADĂ", BROWN)
    draw.text((97, 572), "NCL107", font=font("bold", 105), fill=INK, anchor="lt")
    draw.line((103, 720, 218, 720), fill="#9e724a", width=3)
    for offset, line in enumerate(("Relief pentru muchiile", "casei tale.")):
        draw.text((103, 765 + offset * 53), line, font=font("sans", 35), fill=BROWN, anchor="lt")
    return frame


def final_frame(photo):
    frame = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(frame)
    label(draw, 100, 295, "DECO & FLAIR")
    horizon = crop(photo, (.120, .027, .955, .868), (1080, 724))
    frame.paste(horizon, (0, 402))
    draw.line((100, 1166, 980, 1166), fill="#514339", width=1)
    title(draw, 94, 1218, "Comandă", 91)
    draw.text((458, 1230), "NCL107", font=font("bold", 72), fill=LIGHT, anchor="lt")
    draw.text((103, 1355), "decoflair.ro", font=font("bold", 40), fill=GOLD, anchor="lt")
    return frame


def build(args):
    if not args.extranet.is_file():
        args.extranet = next((ROOT.parent / "EXTRANET" / "source").glob(f"*/*-{EXTRANET_ID}"), args.extranet)
    detail = ImageEnhance.Color(load(args.extranet)).enhance(.91)
    porch = load(args.porch)
    wide = load(args.wide)
    frames = [
        (marked_background(detail, (.03, .105, .61, .938), "INSPIRAȚIE DE FAȚADĂ"), 49),
        (product_frame(), 76),
        (marked_background(porch, (.35, .015, .72, .990), "INSPIRAȚIE DE FAȚADĂ"), 71),
        (marked_background(wide, (.17, .12, .48, .94), "INSPIRAȚIE DE FAȚADĂ"), 63),
        (final_frame(wide), 101),
    ]
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        inputs, graph = [], []
        for index, (image, count) in enumerate(frames):
            path = work / f"{index}.png"
            image.save(path)
            inputs.extend(["-loop", "1", "-framerate", str(FPS), "-i", str(path)])
            graph.append(f"[{index}:v]trim=end_frame={count},setpts=PTS-STARTPTS[s{index}]")
        sequence = ''.join(f"[s{i}]" for i in range(len(frames)))
        graph.append(
            f"{sequence}concat=n={len(frames)}:v=1:a=0,"
            "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]"
        )
        music = work / "soundtrack.wav"
        soundtrack(music)
        subprocess.run([
            args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-filter_complex_threads", "2", *inputs, "-i", str(music),
            "-filter_complex", ";".join(graph), "-map", "[v]", "-map", f"{len(frames)}:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "2",
            "-colorspace", "bt709", "-color_trc", "bt709", "-color_primaries", "bt709",
            "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
            str(args.output / (STEM + ".mp4")),
        ], check=True)
    frames[-1][0].save(args.output / "coperta-ncl107-foto.jpg", quality=93, optimize=True)
    if args.contact_sheet:
        contact = Image.new("RGB", (1080, 384), INK)
        for index, (image, _) in enumerate(frames):
            contact.paste(image.resize((216, 384), Image.Resampling.LANCZOS), (index * 216, 0))
        contact.save(args.contact_sheet, quality=92)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--extranet", type=Path, default=Path(EXTRANET_ID))
    parser.add_argument("--porch", type=Path, required=True)
    parser.add_argument("--wide", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "reel")
    parser.add_argument("--contact-sheet", type=Path)
    build(parser.parse_args())

"""Render the two 30-second Deco & Flair reels and their cover/hero stills."""

import argparse
from array import array
from functools import lru_cache
import json
import math
from pathlib import Path
import subprocess
import tempfile
import wave

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
FONTS = ROOT.parent / "etichete-mostre" / "premium" / "assets"
WIDTH, HEIGHT = 864, 1536
FPS = 30
BEAT = 18
HERO, SCENE, OUTRO = 4 * BEAT, 8 * BEAT, 6 * BEAT
TOTAL = HERO + 5 * SCENE + OUTRO
IVORY, GOLD, BURGUNDY = "#f8f1e5", "#ddc391", "#ad3e54"
INK, MOSS, PAPER, TEXT = "#1c1715", "#171c17", "#f1e8da", "#211a16"
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
SERIES = {
    "interior": {"title": ("Interioare", "în detaliu"), "hero": "IL18", "ink": INK, "intro": "Profile decorative pentru interior"},
    "exterior": {"title": ("Fațade", "cu caracter"), "hero": "NA107", "ink": MOSS, "intro": "Profile decorative pentru exterior"},
}


def write_web_catalog():
    timeline = {"start": HERO / FPS, "chapter": SCENE / FPS, "reveal": 72 / FPS}
    data = json.dumps(dict(CATALOG, timeline=timeline), ensure_ascii=False, indent=2)
    (ROOT / "catalog.js").write_text("window.DECOFLAIR_CATALOG = " + data + ";\n", encoding="utf-8")


def smooth(value):
    value = min(1, max(0, value))
    return value * value * (3 - 2 * value)


def reveal(frame, start, length):
    return smooth((frame - start) / length)


@lru_cache(maxsize=64)
def font(kind, size):
    files = {"serif": "font-0.ttf", "sans": "font-2.ttf", "bold": "font-3.ttf"}
    return ImageFont.truetype(str(FONTS / files[kind]), size)


def words_in_lines(draw, label, size, width, kind="serif"):
    rows = [""]
    for word in label.split():
        candidate = (rows[-1] + " " + word).strip()
        if rows[-1] and draw.textlength(candidate, font=font(kind, size)) > width:
            rows.append(word)
        else:
            rows[-1] = candidate
    return rows


def lines(draw, strings, xy, size, color, spacing, kind="serif"):
    x, y = xy
    for i, text in enumerate(strings):
        draw.text((x, y + i * spacing), text, font=font(kind, size), fill=color, anchor="lt")


def brand(draw, y=119):
    draw.rectangle((91, y, 96, y + 25), fill=BURGUNDY)
    x = 108
    for char in "DECO & FLAIR":
        draw.text((x, y + 3), char, font=font("bold", 21), fill=IVORY, anchor="lt")
        x += draw.textlength(char, font=font("bold", 21)) + 3.1


def frame_mark(draw, current=None):
    draw.line((91, 1284, 700, 1284), fill="#a08062", width=1)
    if current is None:
        return
    for i in range(5):
        x = 91 + i * 28
        draw.line((x, 1310, x + 20, 1310), fill=GOLD if i == current else "#846b54", width=3)
    draw.text((700, 1302), "decoflair.ro", font=font("sans", 19), fill=IVORY, anchor="rt")


def wash(size, anchors):
    width, height = size
    band = Image.new("L", (1, height))
    values = []
    for (start, left), (end, right) in zip(anchors, anchors[1:]):
        values.extend(round(left + (right - left) * smooth((y - start) / (end - start))) for y in range(start, end))
    values.append(anchors[-1][1])
    band.putdata(values)
    return band.resize((width, height))


@lru_cache(maxsize=18)
def photo_source(name):
    with Image.open(ROOT / name) as source:
        return source.convert("RGB")


@lru_cache(maxsize=24)
def prepare_photo(name, height, focal):
    return ImageOps.fit(photo_source(name), (WIDTH + 70, height + 80), Image.Resampling.LANCZOS, centering=(focal, .42))


def photo(item, height, progress):
    source = prepare_photo(item["ambient"], height, item["focal"])
    dx = round(30 - 20 * progress)
    dy = round(32 - 22 * progress)
    margin = round(36 * (1 - progress))
    return source.resize((WIDTH, height), Image.Resampling.BILINEAR, box=(dx, dy, dx + WIDTH + margin, dy + height + margin))


@lru_cache(maxsize=2)
def scene_wash():
    return wash((WIDTH, 1110), [(0, 74), (143, 178), (315, 255), (704, 255), (1109, 0)])


def money(cents):
    lei, bani = divmod(cents, 100)
    return f"{lei:,}".replace(",", ".") + f",{bani:02d} lei"


@lru_cache(maxsize=12)
def product_panel(code):
    item = next(x for x in CATALOG["products"] if x["code"] == code)
    panel = Image.new("RGB", (645, 516), PAPER)
    draw = ImageDraw.Draw(panel)
    draw.rectangle((11, 11, 633, 504), outline="#9c8060", width=1)
    draw.text((38, 41), item["category"].upper(), font=font("bold", 19), fill="#5d4532")
    draw.line((38, 82, 607, 82), fill="#b49b79", width=1)
    square = ImageOps.contain(photo_source(item["image"]), (271, 271), Image.Resampling.LANCZOS)
    panel.paste(square, (38 + (271-square.width)//2, 121 + (271-square.height)//2))
    draw.rectangle((37,120,309,392), outline="#c0a98c", width=1)
    rows = words_in_lines(draw, item["name"], 41, 262)
    lines(draw, rows, (333, 125), 41, TEXT, 39)
    draw.text((333, 327), "/ buc. · TVA inclus", font=font("sans", 19), fill="#5d4532", anchor="lt")
    draw.line((38, 421, 607, 421), fill="#b49b79", width=1)
    draw.text((38, 454), item["availability"], font=font("sans", 20), fill="#5d4532", anchor="lt")
    draw.text((607, 454), item["code"], font=font("bold", 20), fill=TEXT, anchor="rt")
    return panel


@lru_cache(maxsize=12)
def price_plate(code):
    item = next(x for x in CATALOG["products"] if x["code"] == code)
    plate = Image.new("RGB", (269, 75), PAPER)
    draw = ImageDraw.Draw(plate)
    value = money(item["price"])
    size = 60
    while draw.textlength(value, font=font("serif", size)) > 260:
        size -= 1
    draw.text((0, 10), value, font=font("serif", size), fill=TEXT, anchor="lt")
    return plate


def scene(group, item, index, beat):
    style = SERIES[group]
    canvas = Image.new("RGB", (WIDTH, HEIGHT), style["ink"])
    canvas.paste(photo(item, 1110, beat / SCENE), (0, 0), scene_wash())
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    draw.text((91, 182), "INSPIRAȚIE DE AMENAJARE", font=font("sans", 18), fill=IVORY, anchor="lt")

    main_progress = reveal(beat, 2, 11)
    if beat < 66:
        label = words_in_lines(draw, item["headline"], 75, 625)
        title = Image.new("RGBA", (660, 234))
        td = ImageDraw.Draw(title)
        opacity = round((1 - reveal(beat, 43, 18)) * main_progress * 255)
        color = (248, 241, 229, opacity)
        lines(td, label, (0, 0), 75, color, 69)
        canvas.paste(title, (91, 864 + round(22 * (1-main_progress))), title)

    transition = reveal(beat, 39, 16)
    if transition > 0:
        x, y = 91, 727 + round(573 * (1-transition))
        panel = product_panel(item["code"])
        clipped_height = min(panel.height, 1264 - y)
        if clipped_height > 0:
            canvas.paste(panel.crop((0,0,panel.width,clipped_height)), (x,y))
        price_progress = reveal(beat, 57, 11)
        if price_progress > 0:
            plate = price_plate(item["code"])
            hidden = round(plate.height * (1-price_progress))
            canvas.paste(plate.crop((0, 0, plate.width, plate.height-hidden)), (x + 333, y + 238 + hidden))

    frame_mark(ImageDraw.Draw(canvas), index)
    return canvas


def opening(group, item, frame, cover=False):
    cfg = SERIES[group]
    canvas = Image.new("RGB", (WIDTH, HEIGHT), cfg["ink"])
    if cover:
        with Image.open(ROOT / item["ambient"]) as source:
            image = ImageOps.fit(source.convert("RGB"), (645, 804), Image.Resampling.LANCZOS, centering=(item["focal"], .4))
        canvas.paste(image, (91, 202), wash(image.size, [(0,255),(600,255),(803,0)]))
    else:
        canvas.paste(photo(item, 1200, frame/HERO), (0, 0),
                     wash((WIDTH,1200), [(0,110),(270,255),(637,255),(1199,0)]))
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    if cover:
        draw.rectangle((91,202,735,1209), outline=GOLD, width=1)
    rise = 0 if cover else round(31 * (1-reveal(frame, 4, 13)))
    text_x = 115 if cover else 91
    lines(draw, (cfg["title"][0],), (text_x, 882+rise), 110, IVORY, 100)
    lines(draw, (cfg["title"][1],), (text_x, 979+rise), 110, GOLD, 100)
    draw.text((text_x, 1145), cfg["intro"], font=font("sans", 25), fill=IVORY, anchor="lt")
    frame_mark(draw)
    return canvas


@lru_cache(maxsize=2)
def endcard(group):
    cfg = SERIES[group]
    canvas = Image.new("RGB", (WIDTH,HEIGHT), cfg["ink"])
    draw = ImageDraw.Draw(canvas)
    brand(draw)
    draw.rectangle((91, 298, 735, 1195), outline=GOLD, width=1)
    draw.line((132, 465, 215, 465), fill=GOLD, width=3)
    lines(draw, ("Detaliile fac", "diferența."), (130, 505), 90, IVORY, 85)
    draw.text((130, 757), "decoflair.ro", font=font("serif", 95), fill=GOLD, anchor="lt")
    draw.text((130, 918), "Consultanță", font=font("sans", 25), fill=IVORY, anchor="lt")
    draw.text((130, 962), CATALOG["phone"], font=font("bold", 39), fill=IVORY, anchor="lt")
    frame_mark(draw)
    return canvas


def frame_at(group, products, hero, frame):
    if frame < HERO:
        return opening(group, hero, frame)
    if frame >= TOTAL - OUTRO:
        local = frame - (TOTAL-OUTRO)
        if local < 12:
            last = scene(group, products[-1], 4, SCENE-1)
            return Image.blend(last, endcard(group), reveal(local, 0, 12))
        return endcard(group)
    index, local = divmod(frame - HERO, SCENE)
    return scene(group, products[index], index, local)


def write_music(path, group):
    """A soft original instrumental with 100 BPM scene changes and tuned detail accents."""
    rate = 48_000
    duration = TOTAL / FPS
    stereo = [array("f", [0]) * round(duration*rate) for _ in range(2)]
    progression = [(50,57,60,64), (46,53,57,60), (53,60,64,67), (48,55,57,62)]
    if group == "exterior":
        progression = [(45,52,55,59), (41,48,52,55), (48,55,59,62), (43,50,55,57)]

    def tone(note, start, length, gain, pan, decay, bass=False):
        frequency = 440 * 2 ** ((note-69)/12)
        first = round(start * rate)
        samples = min(len(stereo[0])-first, round(length*rate))
        pan_l, pan_r = math.sqrt(1-pan), math.sqrt(pan)
        for i in range(max(0,samples)):
            t = i/rate
            phase = math.tau*frequency*t
            envelope = min(1,t/.022) * min(1,(samples-i)/(rate*.085)) * math.exp(-t*decay)
            sample = (math.sin(phase) + (.08 if bass else .21)*math.sin(2*phase) +
                      (0 if bass else .07)*math.sin(3*phase)) * envelope * gain
            stereo[0][first+i] += sample*pan_l
            stereo[1][first+i] += sample*pan_r

    for beat in range(TOTAL//BEAT):
        chord = progression[(beat//4) % len(progression)]
        moment = beat * (BEAT/FPS)
        if beat % 4 == 0:
            tone(chord[0]-12, moment, 2.15, .145, .5, .90, True)
            for i, note in enumerate(chord[1:]):
                tone(note, moment+i*.035, 2.10, .073, .22+i*.27, 1.4)
        tone(chord[1+(beat%3)]+12, moment + .03, 0.56, .069 if beat%2 else .045, .3 if beat%2 else .7, 5)
    for index in range(5):
        moment = (HERO + index*SCENE + 56)/FPS
        tone(79 if group == "interior" else 76, moment, .50, .044, .63, 5.6)
    pcm = array("h")
    for i,(left,right) in enumerate(zip(*stereo)):
        t = i / rate
        envelope = min(1, t/.18, (duration-t)/1.1)
        pcm.extend((round(left*envelope*32767), round(right*envelope*32767)))
    with wave.open(str(path),"wb") as handle:
        handle.setparams((2,2,rate,0,"NONE","not compressed"))
        handle.writeframes(pcm.tobytes())


def export(group, output, ffmpeg, only_stills=False):
    products = [p for p in CATALOG["products"] if p["group"] == group]
    hero = next(p for p in products if p["code"] == SERIES[group]["hero"])
    output.mkdir(parents=True, exist_ok=True)
    for label,image in (("coperta",opening(group,hero,42,True)),("hero",opening(group,hero,42))):
        image.resize((1080,1920),Image.Resampling.LANCZOS).save(
            output/f"{group}-{label}.jpg", quality=90, optimize=True, progressive=True)
    if only_stills:
        return

    with tempfile.TemporaryDirectory() as temp:
        soundtrack = Path(temp)/"soundtrack.wav"
        write_music(soundtrack,group)
        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-filter_threads", "2",
               "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
               "-framerate", str(FPS), "-i", "pipe:0", "-i", str(soundtrack),
               "-map", "0:v:0", "-map", "1:a:0",
               "-vf", "scale=1080:1920:flags=lanczos:out_color_matrix=bt709,format=yuv420p,setsar=1",
               "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-threads", "2",
               "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
               "-af", "volume=2.7,alimiter=limit=0.8:level=false", "-c:a", "aac", "-b:a", "160k",
               "-movflags", "+faststart", str(output/f"decoflair-{group}-reel.mp4")]
        with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
            assert process.stdin is not None
            for frame in range(TOTAL):
                process.stdin.write(frame_at(group,products,hero,frame).tobytes())
            process.stdin.close()
            if process.wait():
                raise RuntimeError(f"FFmpeg a eșuat pentru {group}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--output", type=Path, default=ROOT)
    parser.add_argument("--series", choices=["interior","exterior","ambele"], default="ambele")
    parser.add_argument("--stills", action="store_true")
    args = parser.parse_args()
    write_web_catalog()
    for group in (SERIES if args.series=="ambele" else [args.series]):
        export(group,args.output,args.ffmpeg,args.stills)

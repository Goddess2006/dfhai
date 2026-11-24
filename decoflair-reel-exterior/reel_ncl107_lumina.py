"""Edit an original 15-second NCL107 spot from existing brand imagery."""
import argparse
from array import array
from functools import lru_cache
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import wave

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "decoflair-reels-2027"))
from render import FPS, HEIGHT, WIDTH, brand, font, reveal, wash

SIZE = (WIDTH, HEIGHT)
ASSETS = ROOT / "assets"
CREAM = "#fcf3e3"
GOLD = "#e8c497"
SHADE = "#251a13"
TOTAL = 15 * FPS
CUTS = (39, 142, 312)


def letter(draw, xy, value, size, color=CREAM, kind="serif", anchor="lt"):
    draw.text(xy, value, font=font(kind, size), fill=color, anchor=anchor,
              stroke_width=0)


@lru_cache(maxsize=3)
def source(name):
    with Image.open(ASSETS/name) as im:
        photo = im.convert("RGB")
    if name == "p-ncl107-hero-crop.jpg":
        return photo
    # Preserve the architecture and grade the existing daylight photograph.
    channels = photo.split()
    return Image.merge("RGB", tuple(c.point([min(255, round(i*s+v)) for i in range(256)])
                                   for c,s,v in zip(channels,(1.00,.93,.82),(6,1,1))))


def shot(name, box, size):
    return source(name).resize(size, Image.Resampling.BICUBIC, box=box)


def interpolate(a, b, f):
    return tuple(x+(y-x)*f for x,y in zip(a,b))


@lru_cache(maxsize=4)
def shade_mask(height, dark_at_bottom=0):
    return wash((WIDTH,height), [(0,162),(height//4,255),(height//2,255),(height-1,dark_at_bottom)])


def product_photo(local):
    progress = reveal(local,0,CUTS[0])
    crop = interpolate((45,101,305,563),(51,117,299,558),progress)
    frame = Image.new("RGB",SIZE,SHADE)
    frame.paste(shot("p-ncl107-hero-crop.jpg",crop,SIZE),(0,0),shade_mask(HEIGHT,48))
    return frame


def product(local):
    frame = product_photo(local)
    draw = ImageDraw.Draw(frame)
    brand(draw)
    letter(draw,(91,945),"COLȚAR DE FAȚADĂ",27,GOLD,"bold")
    letter(draw,(91,1005),"NCL107",124,CREAM,"bold")
    return frame


def detail(local):
    progress = reveal(local,0,CUTS[1]-CUTS[0])
    crop = interpolate((573,240,986,974),(540,224,1007,1054),progress)
    frame = Image.new("RGB",SIZE,SHADE)
    frame.paste(shot("ncl107-ambient-nmc.jpg",crop,SIZE),(0,0),shade_mask(HEIGHT,0))
    draw = ImageDraw.Draw(frame)
    letter(draw,(91,1002),"Lumina se",94)
    letter(draw,(91,1100),"oprește aici.",94)
    return frame


@lru_cache(maxsize=1)
def wide_mask():
    return wash((WIDTH,1020),[(0,0),(120,255),(748,255),(1019,0)])


def wide_photo(local):
    progress = reveal(local,0,CUTS[2]-CUTS[1])
    crop = interpolate((170,47,1058,1096),(129,15,1082,1140),progress)
    frame = Image.new("RGB",SIZE,SHADE)
    frame.paste(shot("ncl107-ambient-nmc.jpg",crop,(WIDTH,1020)),(0,98),wide_mask())
    return frame


def home(local):
    frame = wide_photo(local)
    draw = ImageDraw.Draw(frame)
    brand(draw)
    letter(draw,(WIDTH//2,1041),"Mai privește o dată.",82,CREAM,"serif","mt")
    return frame


@lru_cache(maxsize=1)
def end_photo():
    return product_photo(CUTS[0]-1)


def final(local):
    progress = reveal(local,0,25)
    frame = Image.blend(end_photo(),Image.new("RGB",SIZE,SHADE),.67+.07*progress)
    draw = ImageDraw.Draw(frame)
    brand(draw)
    draw.line((385,628,479,628),fill=GOLD,width=2)
    letter(draw,(WIDTH//2,672),"Comandă NCL107",66,CREAM,"bold","mt")
    letter(draw,(WIDTH//2,778),"decoflair.ro",91,GOLD,"serif","mt")
    letter(draw,(WIDTH//2,932),"În stoc · Livrare estimată",29,CREAM,"sans","mt")
    letter(draw,(WIDTH//2,983),"3–5 zile lucrătoare",46,CREAM,"bold","mt")
    letter(draw,(WIDTH//2,1044),"De la confirmarea comenzii",24,CREAM,"sans","mt")
    return frame


def frame_at(frame):
    if frame < CUTS[0]:
        return product(frame)
    if frame < CUTS[1]:
        return detail(frame-CUTS[0])
    if frame < CUTS[2]:
        return home(frame-CUTS[1])
    return final(frame-CUTS[2])


def soundtrack(path):
    """A new felt-key motif with a restrained opening sparkle and exterior ambience."""
    hz = 48000
    signal = [array("f", [0])*(15*hz) for _ in range(2)]

    def note(pitch, start, length, level, pan, decay, bright=.18):
        phase = math.tau * 440 * 2**((pitch-69)/12) / hz
        offset = round(start*hz)
        count = min(round(length*hz),len(signal[0])-offset)
        left,right = math.sqrt(1-pan),math.sqrt(pan)
        for i in range(count):
            t = i/hz
            env = min(1,t/.022) * min(1,(count-i)/(hz*.13)) * math.exp(-t*decay)
            value = level*env*(math.sin(phase*i)+bright*math.sin(phase*i*2.002))
            signal[0][offset+i] += value*left
            signal[1][offset+i] += value*right

    for start, chord in [(0,(45,57,60,64)),(2.9,(41,53,57,60)),(5.7,(48,55,60,64)),
                         (8.4,(43,55,59,62)),(10.5,(45,57,60,64))]:
        note(chord[0], start,2.8,.24,.49,.82,.05)
        for i,pitch in enumerate(chord[1:]):
            note(pitch,start+.052*i,2.7,.11,.23+i*.27,1.23)
    for start, pitch in [(0,83),(1.3,76),(2.08,79),(4.74,81),(5.78,84),(7.4,79),(8.95,74),(10.51,81),(12.1,76)]:
        note(pitch,start,1.28,.105,.66 if pitch%2 else .35,3.9,.28)

    rng = random.Random(107)
    noise = 0
    pcm = array("h")
    for i,(l,r) in enumerate(zip(*signal)):
        t=i/hz
        noise=.994*noise+.006*rng.uniform(-1,1)
        ambience=noise*.037
        env=min(1,t/.04,(15-t)/1.5)
        pcm.extend([round((l+ambience)*env*32767),round((r+ambience*.87)*env*32767)])
    with wave.open(str(path),"wb") as w:
        w.setparams((2,2,hz,0,"NONE","not compressed"))
        w.writeframes(pcm.tobytes())


def export(output, ffmpeg):
    output.mkdir(parents=True,exist_ok=True)
    home(118).resize((1080,1920),Image.Resampling.LANCZOS).save(
        output/"coperta-ncl107-lumina.jpg",quality=92,optimize=True,progressive=True)
    with tempfile.TemporaryDirectory() as folder:
        wav = Path(folder)/"ncl107.wav"
        soundtrack(wav)
        command=[ffmpeg,"-y","-hide_banner","-loglevel","error","-filter_threads","2",
                 "-f","rawvideo","-pixel_format","rgb24","-video_size",f"{WIDTH}x{HEIGHT}",
                 "-framerate",str(FPS),"-i","pipe:0","-i",str(wav),"-map","0:v","-map","1:a",
                 "-vf","scale=1080:1920:flags=lanczos:out_color_matrix=bt709,format=yuv420p,setsar=1",
                 "-c:v","libx264","-preset","fast","-crf","18","-threads","2",
                 "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                 "-af","volume=1.15,alimiter=limit=0.8:level=false","-c:a","aac","-b:a","160k",
                 "-movflags","+faststart",str(output/"decoflair-ncl107-lumina-ads-15s.mp4")]
        with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
            assert process.stdin is not None
            for frame in range(TOTAL):
                process.stdin.write(frame_at(frame).tobytes())
            process.stdin.close()
            if process.wait():
                raise RuntimeError("Exportul FFmpeg a eșuat")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg",default="ffmpeg")
    parser.add_argument("--output",type=Path,default=ROOT/"reel")
    options=parser.parse_args()
    export(options.output,options.ffmpeg)

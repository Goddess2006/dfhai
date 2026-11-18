"""Mărire 4x Real-ESRGAN (realesr-general-x4v3, ONNX) pe plăci cu suprapunere + retușuri fine.
Utilizare: python3 tools/upscale.py MODEL.onnx INPUT.jpg OUTPUT_PREFIX"""
import sys, numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter, ImageEnhance
model, src, out = sys.argv[1:4]
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
H, W, _ = im.shape; S = 4; T = 256; P = 16
res = np.zeros((H*S, W*S, 3), np.float32)
for y in range(0, H, T):
    for x in range(0, W, T):
        y0, x0 = max(y-P, 0), max(x-P, 0); y1, x1 = min(y+T+P, H), min(x+T+P, W)
        tile = im[y0:y1, x0:x1].transpose(2, 0, 1)[None]
        o = sess.run(None, {"input": tile})[0][0].transpose(1, 2, 0)
        oy, ox = (y-y0)*S, (x-x0)*S; h, w = min(T, H-y)*S, min(T, W-x)*S
        res[y*S:y*S+h, x*S:x*S+w] = o[oy:oy+h, ox:ox+w]
up = Image.fromarray((np.clip(res, 0, 1)*255+0.5).astype(np.uint8))
# amestec cu originalul mărit Lanczos (păstrează textura naturală a pielii, evită aspectul „plastic”)
lz = Image.open(src).convert("RGB").resize(up.size, Image.LANCZOS)
mix = Image.blend(lz, up, 0.42)
# 2x final (2228x2824) - suficient pentru retina în e-mail și pentru print mic
final = mix.resize((W*2, H*2), Image.LANCZOS)
final = final.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=3))
final = ImageEnhance.Contrast(final).enhance(1.03)
# granulație fină (luminanță) ca să nu pară pictat
rng = np.random.default_rng(7); a = np.asarray(final).astype(np.float32)
g = rng.normal(0, 2.2, a.shape[:2])[..., None]; final = Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8))
final.save(out + "-hq.jpg", quality=95, subsampling=0, optimize=True)
print("ok", final.size)

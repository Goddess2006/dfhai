"""Muzică ambientală originală pentru filmul Deco&Flair (fără drepturi de autor ale terților).
Pad-uri calde (Re major: Dmaj9 – Bm11 – Gmaj9 – Asus2), note rare de pian, bas profund, reverb lung,
creștere și rezolvare pe finalul de brand, clopoțel discret la apariția siglei. Scrie out/muzica.wav (48 kHz, stereo).
"""
import json, wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
T = json.loads((ROOT / "out" / "timing.json").read_text())
DUR = T["total"]; TF = T["final"]
SR = 48000
N = int(DUR * SR) + SR
t = np.arange(N) / SR
rng = np.random.default_rng(7)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 2
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e


def pad_voice(f, n):
    tt = np.arange(n) / SR
    s = np.zeros(n)
    for det in (-0.12, 0.0, 0.11):
        ff = f * 2 ** (det / 12)
        ph = rng.random() * 6.28
        s += np.sin(2 * np.pi * ff * tt + ph) + 0.35 * np.sin(2 * np.pi * 2 * ff * tt + ph) + 0.12 * np.sin(2 * np.pi * 3 * ff * tt + ph)
    s *= 1 + 0.12 * np.sin(2 * np.pi * 0.18 * tt + rng.random() * 6)
    return s / 3


def piano(f, n):
    tt = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (1.6 + k * 0.9)) for k, a in ((1, 1), (2, .45), (3, .22), (4, .1), (5, .05)))
    att = np.minimum(1, tt / 0.006)
    return s * att


L = np.zeros(N); R = np.zeros(N)
CH = [[50, 57, 61, 64, 66], [47, 54, 57, 62, 64], [43, 50, 54, 57, 62], [45, 52, 57, 59, 64]]  # Dmaj9, Bm11, Gmaj9, Asus2
step = 6.6
k = 0; start = 0.0
while start < TF - 0.5:
    ch = CH[k % 4]
    d = min(step + 2.5, TF + 1.0 - start)
    n = int(d * SR); i0 = int(start * SR)
    e = env_adsr(n, 2.2, 2.4)
    for j, m in enumerate(ch):
        v = pad_voice(hz(m), n) * e * (0.11 if j else 0.15)
        pan = 0.5 + 0.35 * ((j % 2) * 2 - 1) * (j / 4)
        L[i0:i0 + n] += v * (1 - pan) * 1.4; R[i0:i0 + n] += v * pan * 1.4
    # bas
    b = np.sin(2 * np.pi * hz(ch[0] - 12) * np.arange(n) / SR) * e * 0.16
    L[i0:i0 + n] += b; R[i0:i0 + n] += b
    # note de pian rare (arpegiu lent)
    for q, m in enumerate([ch[2] + 12, ch[4] + 12, ch[3] + 12, ch[1] + 24]):
        ts = start + 0.9 + q * 1.55 + rng.random() * 0.2
        if ts > TF - 0.3:
            break
        nn = int(3.5 * SR); ii = int(ts * SR)
        p = piano(hz(m), nn) * 0.13
        pan = 0.3 + 0.4 * rng.random()
        L[ii:ii + nn] += p * (1 - pan); R[ii:ii + nn] += p * pan
    start += step; k += 1

# finalul: acord larg Dmaj9 cu creștere, clopoțel la siglă și sclipire la site
n = N - int(TF * SR); i0 = int(TF * SR)
e = env_adsr(n, 1.8, 3.5)
for j, m in enumerate([38, 50, 57, 62, 66, 69, 73, 76]):
    v = pad_voice(hz(m), n) * e * (0.09 if j > 1 else 0.13)
    pan = 0.5 + 0.3 * np.sin(j * 1.7)
    L[i0:i0 + n] += v * (1 - pan) * 1.5; R[i0:i0 + n] += v * pan * 1.5
for ts, m, a in ((TF + 0.9, 86, .10), (TF + 0.95, 81, .08), (TF + 2.0, 93, .06), (TF + 2.05, 88, .05), (TF + 3.0, 90, .05)):
    nn = int(4 * SR); ii = int(ts * SR)
    p = piano(hz(m), nn) * a
    L[ii:ii + nn] += p[: N - ii] * .6; R[ii:ii + nn] += p[: N - ii] * .4

# reverb: răspuns la impuls exponențial (zgomot) — convoluție FFT
irn = int(3.2 * SR)
ir_t = np.arange(irn) / SR
def ir():
    x = rng.standard_normal(irn) * np.exp(-ir_t * 2.1)
    x[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    return x / np.sqrt((x ** 2).sum())
def conv(x, h):
    m = len(x) + len(h) - 1; nf = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(h, nf), nf)[: len(x)]
Lw = conv(L, ir()); Rw = conv(R, ir())
L = 0.55 * L + 0.9 * Lw; R = 0.55 * R + 0.9 * Rw
# filtru trece-jos blând (căldură)
def lp(x, fc=6500):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    out = np.empty_like(x)
    # IIR de ordin 1, vectorizat aproximativ prin scipy-free loop pe blocuri
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; out[i] = acc
    return out
try:
    from scipy.signal import lfilter
    a = np.exp(-2 * np.pi * 6500 / SR); L = lfilter([1 - a], [1, -a], L); R = lfilter([1 - a], [1, -a], R)
except Exception:
    pass
# fade in / out și normalizare
fi = int(1.5 * SR); L[:fi] *= np.linspace(0, 1, fi); R[:fi] *= np.linspace(0, 1, fi)
end = int(DUR * SR); fo = int(2.2 * SR)
for x in (L, R):
    x[end - fo:end] *= np.linspace(1, 0, fo) ** 1.3; x[end:] = 0
L, R = L[:end], R[:end]
peak = max(np.abs(L).max(), np.abs(R).max()); g = 0.89 / peak
st = (np.stack([L, R], 1) * g * 32767).astype(np.int16)
with wave.open(str(ROOT / "out" / "muzica.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print("muzica.wav", round(end / SR, 2), "s")

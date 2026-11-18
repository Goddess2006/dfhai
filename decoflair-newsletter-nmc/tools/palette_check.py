"""Verificare paletă Deco&Flair 2027: contrast WCAG 2.1 pentru fiecare pereche text/fundal folosită în newsletter.
AA text normal >= 4.5 ; AA text mare (>= 24 px sau 18,66 px bold) >= 3.0
Rulează: python3 tools/palette_check.py  → scrie și PALETA.md"""
import json, pathlib

P = {
    "forest":      "#1F3A2F",  # verde pădure (fundal principal închis)
    "forest_mid":  "#2E5244",
    "teal":        "#256F69",  # turcoaz 2027 (accent / butoane)
    "teal_light":  "#8CCBC2",
    "aubergine":   "#4B2748",  # mov puternic
    "mauve":       "#B9A3BD",  # mov pal (decor)
    "nude":        "#E9D5CC",  # roz nude (fundal secțiuni)
    "cream":       "#F4EEE4",  # crem (fundal corp)
    "ivory":       "#FBF8F2",
    "ink":         "#161A17",  # text
    "muted":       "#5B5F5A",  # text secundar
    "gold":        "#D6BC84",  # auriul Deco&Flair (pe închis)
    "gold_dark":   "#7A5B22",  # auriu pentru text pe deschis
    "white":       "#FFFFFF",
}

# (text, fundal, utilizare, mărime: "normal" | "mare")
PAIRS = [
    ("cream", "forest", "titluri și text pe banda verde", "normal"),
    ("gold", "forest", "etichete aurii pe verde", "normal"),
    ("teal_light", "forest", "etichete turcoaz pe verde", "normal"),
    ("white", "teal", "text buton turcoaz", "normal"),
    ("ink", "cream", "text corp", "normal"),
    ("muted", "cream", "text secundar", "normal"),
    ("gold_dark", "cream", "etichete aurii pe crem", "normal"),
    ("teal", "cream", "linkuri pe crem", "normal"),
    ("forest", "nude", "titluri pe roz nude", "normal"),
    ("ink", "nude", "text pe roz nude", "normal"),
    ("aubergine", "nude", "prețuri / accente mov pe nude", "normal"),
    ("aubergine", "cream", "prețuri pe crem", "normal"),
    ("cream", "aubergine", "text pe banda mov", "normal"),
    ("nude", "aubergine", "text secundar pe mov", "normal"),
    ("gold", "aubergine", "etichete aurii pe mov", "normal"),
    ("white", "aubergine", "buton mov", "normal"),
    ("ink", "mauve", "text pe mov pal", "normal"),
    ("forest", "ivory", "titluri pe ivoriu", "normal"),
]

def lum(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

rows, bad = [], 0
for t, b, use, size in PAIRS:
    r = ratio(P[t], P[b]); need = 4.5 if size == "normal" else 3.0
    ok = r >= need; bad += (not ok)
    rows.append((t, b, use, round(r, 2), need, "OK" if ok else "NU"))

if __name__ == "__main__":
    md = ["# Paleta newsletter Deco&Flair × NMC — 2027", "",
          "Direcție: verde pădure + turcoaz (WGSN/Coloro 2027 „Luminous Blue” spre verde-albăstrui), mov puternic (vânăt) + mov pal, roz nude, crem cald. Auriul Deco&Flair rămâne semnătura brandului. Fără roz/magenta saturat (respins anterior).", "",
          "| Nume | Hex |", "|---|---|"] + [f"| {k} | `{v}` |" for k, v in P.items()] + [
          "", "Degradeuri folosite: `forest → teal` (135°, #1F3A2F → #256F69), `aubergine → mauve` (#4B2748 → #8E6E93), `nude → cream`.", "",
          "## Contrast WCAG 2.1", "", "| Text | Fundal | Utilizare | Raport | Minim | Rezultat |", "|---|---|---|---|---|---|"] + [
          f"| {t} | {b} | {u} | {r}:1 | {n}:1 | {o} |" for t, b, u, r, n, o in rows] + ["", f"Perechi care nu trec: {bad}", "", "Mov pal (#B9A3BD) se folosește doar decorativ (linii, chenare, fundal sub text închis), niciodată ca text pe crem (contrast 2:1)."]
    pathlib.Path(__file__).resolve().parent.parent.joinpath("PALETA.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    for r in rows: print(*r, sep=" | ")
    print("perechi care nu trec:", bad)

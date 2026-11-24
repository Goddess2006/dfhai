#!/usr/bin/env python3
"""Catalog decoflair.ro din sitemap-ul public (fără login, fără date interne).

Exemple:
  python3 catalog.py list --out catalog.json            # toate produsele: url, titlu, imagini
  python3 catalog.py list --grep na21 --limit 20        # filtrează după URL/titlu
  python3 catalog.py product https://decoflair.ro/ancadrament-decorativ-fereastra-na214
  python3 catalog.py images https://decoflair.ro/... --dest refs/na214   # descarcă pozele produsului
  python3 catalog.py pick --n 7 --seed 2026-48         # alegere reproductibilă pentru calendarul săptămânii

Doar biblioteca standard Python.
"""
import argparse, json, os, random, re, sys, urllib.request, html

BASE = "https://decoflair.ro"
UA = {"User-Agent": "Mozilla/5.0 (decoflair-content-bot)"}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def sitemap_products():
    idx = get(BASE + "/sitemap.xml")
    maps = [m for m in re.findall(r"<loc><!\[CDATA\[(.*?)\]\]></loc>", idx) if "sitemap-product" in m]
    out = []
    for sm in maps:
        x = get(sm)
        for block in re.findall(r"<url>(.*?)</url>", x, re.S):
            loc = re.search(r"<loc><!\[CDATA\[(.*?)\]\]></loc>", block)
            if not loc:
                continue
            imgs = re.findall(r"<image:loc>(.*?)</image:loc>", block)
            title = re.search(r"<image:title>(.*?)</image:title>", block)
            out.append({
                "url": loc.group(1).strip(),
                "title": html.unescape(title.group(1)).strip() if title else "",
                "images": imgs,
            })
    return out


def product_details(url):
    h = get(url)
    d = {"url": url}
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            j = json.loads(m)
        except Exception:
            continue
        if j.get("@type") == "Product":
            d["name"] = (j.get("name") or "").strip()
            d["model"] = j.get("model")
            d["category"] = html.unescape(j.get("category") or "")
            d["image"] = j.get("image")
            d["description"] = html.unescape(j.get("description") or "")
            off = j.get("offers") or {}
            if isinstance(off, list):
                off = off[0] if off else {}
            d["price"] = off.get("price")
            d["currency"] = off.get("priceCurrency")
            d["availability"] = off.get("availability")
            b = j.get("brand")
            d["brand"] = b.get("name") if isinstance(b, dict) else b
    m = re.search(r'<meta property="og:description" content="([^"]*)"', h)
    if m:
        d["og_description"] = html.unescape(m.group(1))
    found = re.findall(r'https://decoflair\.ro/image/cache/catalog/[^"\' ]+?-(?:1500x1500|1000x1000|800x800)[^"\' ]*?\.(?:jpe?g|png|webp)', h)
    rank = lambda u: 0 if "1500x1500" in u else 1 if "1000x1000" in u else 2
    best = {}
    for u in found:  # o singură variantă per poză, cea mai mare
        k = re.sub(r"-(1500x1500|1000x1000|800x800)", "", u)
        if k not in best or rank(u) < rank(best[k]):
            best[k] = u
    d["gallery"] = sorted(best.values())
    return d


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("list"); a.add_argument("--grep"); a.add_argument("--limit", type=int); a.add_argument("--out")
    b = sub.add_parser("product"); b.add_argument("url")
    c = sub.add_parser("images"); c.add_argument("url"); c.add_argument("--dest", required=True); c.add_argument("--max", type=int, default=6)
    p = sub.add_parser("pick"); p.add_argument("--n", type=int, default=7); p.add_argument("--seed", default="0"); p.add_argument("--grep")
    args = ap.parse_args()

    if args.cmd in ("list", "pick"):
        items = sitemap_products()
        if args.grep:
            g = args.grep.lower()
            items = [i for i in items if g in i["url"].lower() or g in i["title"].lower()]
        if args.cmd == "pick":
            items = [i for i in items if i["images"]]
            random.Random(args.seed).shuffle(items)
            items = items[: args.n]
        elif args.limit:
            items = items[: args.limit]
        s = json.dumps(items, ensure_ascii=False, indent=1)
        if getattr(args, "out", None):
            open(args.out, "w", encoding="utf-8").write(s)
            print(f"{len(items)} produse -> {args.out}", file=sys.stderr)
        else:
            print(s)
    elif args.cmd == "product":
        print(json.dumps(product_details(args.url), ensure_ascii=False, indent=1))
    elif args.cmd == "images":
        d = product_details(args.url)
        urls = d.get("gallery") or ([d["image"]] if d.get("image") else [])
        if not urls:  # cădere pe sitemap
            urls = next((i["images"] for i in sitemap_products() if i["url"] == args.url), [])
        os.makedirs(args.dest, exist_ok=True)
        for n, u in enumerate(urls[: args.max], 1):
            ext = os.path.splitext(u)[1] or ".jpg"
            path = os.path.join(args.dest, f"ref-{n:02d}{ext}")
            req = urllib.request.Request(u, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                f.write(r.read())
            print(path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Rulează orice model fal.ai (imagine sau video) prin Queue API și descarcă rezultatele.

Cheia: variabila de mediu FAL_KEY (nu o scrie niciodată în repo).

Exemple:
  # Imagine de produs în ambient, cu poza de catalog ca referință (Nano Banana Pro edit)
  python3 fal_run.py fal-ai/nano-banana-pro/edit \
      --prompt-file prompt.txt --image image_urls=refs/na214/ref-01.jpg \
      --arg aspect_ratio=4:5 --arg num_images=2 --out out/na214

  # Video image-to-video (ex. Kling) din imaginea aprobată
  python3 fal_run.py fal-ai/kling-video/v2.5-turbo/pro/image-to-video \
      --prompt "slow dolly-in ..." --image image_url=out/na214/01.png --arg duration=5 --out out/na214-video

  --image cheie=cale  -> fișier local trimis ca data URI (sau URL http lăsat ca atare).
                         Dacă cheia se termină în "_urls", se adună într-o listă.
  --arg cheie=valoare -> valoare JSON dacă se poate (numere, true/false, liste), altfel text.
  --dry-run           -> afișează doar payload-ul (fără cost).

ID-urile de modele și parametrii se schimbă des: verifică pagina modelului pe fal.ai/models
înainte de o generare plătită. Doar biblioteca standard Python.
"""
import argparse, base64, json, mimetypes, os, sys, time, urllib.request, urllib.error

QUEUE = "https://queue.fal.run/"


def req(method, url, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Key {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {url}\n{e.read().decode(errors='replace')[:2000]}")


def as_input(v):
    if v.startswith(("http://", "https://", "data:")):
        return v
    mime = mimetypes.guess_type(v)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(open(v, "rb").read()).decode()


def collect_urls(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "url" and isinstance(v, str) and v.startswith("http"):
                acc.append(v)
            else:
                collect_urls(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            collect_urls(v, acc)
    return acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--image", action="append", default=[])
    ap.add_argument("--arg", action="append", default=[])
    ap.add_argument("--out", default="fal-out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()

    body = {}
    if a.prompt_file:
        body["prompt"] = open(a.prompt_file, encoding="utf-8").read().strip()
    elif a.prompt:
        body["prompt"] = a.prompt
    for kv in a.arg:
        k, v = kv.split("=", 1)
        try:
            body[k] = json.loads(v)
        except ValueError:
            body[k] = v
    for kv in a.image:
        k, v = kv.split("=", 1)
        val = as_input(v)
        if k.endswith("_urls"):
            body.setdefault(k, []).append(val)
        else:
            body[k] = val

    if a.dry_run:
        show = json.loads(json.dumps(body))
        for k, v in show.items():
            if isinstance(v, str) and v.startswith("data:"):
                show[k] = v[:40] + "…"
            if isinstance(v, list):
                show[k] = [x[:40] + "…" if isinstance(x, str) and x.startswith("data:") else x for x in v]
        print(json.dumps({"model": a.model, "input": show}, ensure_ascii=False, indent=1))
        return

    key = os.environ.get("FAL_KEY")
    if not key:
        sys.exit("Lipsește FAL_KEY (fal.ai → Dashboard → Keys). Setează-l în mediul sesiunii, nu în repo.")

    sub = req("POST", QUEUE + a.model, key, body)
    status_url, response_url = sub["status_url"], sub["response_url"]
    print("request_id:", sub.get("request_id"), file=sys.stderr)
    t0 = time.time()
    while True:
        st = req("GET", status_url, key)
        s = st.get("status")
        if s == "COMPLETED":
            if st.get("error"):
                sys.exit(f"Eșuat: {st.get('error_type')} {st.get('error')}")
            break
        if time.time() - t0 > a.timeout:
            sys.exit(f"Timeout; reia mai târziu cu GET {response_url}")
        print(f"  {s} {st.get('queue_position', '')}", file=sys.stderr)
        time.sleep(4)

    res = req("GET", response_url, key)
    os.makedirs(a.out, exist_ok=True)
    json.dump(res, open(os.path.join(a.out, "result.json"), "w"), indent=1)
    for n, u in enumerate(collect_urls(res, []), 1):
        ext = os.path.splitext(u.split("?")[0])[1] or ".bin"
        path = os.path.join(a.out, f"{n:02d}{ext}")
        with urllib.request.urlopen(u, timeout=300) as r, open(path, "wb") as f:
            f.write(r.read())
        print(path)


if __name__ == "__main__":
    main()

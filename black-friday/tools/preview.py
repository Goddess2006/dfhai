"""Local-only preview: static landing plus an allowlisted, public product-page proxy."""
import argparse
import json
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
CATALOG = json.loads((ROOT / 'black-friday/catalog.json').read_text())
PRODUCTS = {urlsplit(p['url']).path: p['url'] for p in CATALOG['products']}

class Preview(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = posixpath.normpath(unquote(urlsplit(self.path).path))
        if path == '/black-friday':
            path = '/black-friday/'
        if path in PRODUCTS:
            try:
                req = Request(PRODUCTS[path], headers={'User-Agent': 'NMC-Landing-Preview/1.0', 'Accept': 'text/html'})
                with urlopen(req, timeout=15) as upstream:
                    body = upstream.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
            except Exception:
                self.send_error(502, 'Public product page unavailable')
            return
        if path == '/':
            body = b'''<!doctype html><html lang="ro"><meta charset="utf-8"><title>NMC overlay preview</title>
<body style="font:20px system-ui;padding:48px;background:#f5f1eb"><h1>Homepage demonstrativ</h1>
<p>Acesta este un mediu local de test. Inchide landingul pentru a verifica revenirea.</p>
<button onclick="window.NMCBlackFriday.open()">Redeschide Black Friday</button>
<script src="/black-friday/homepage-overlay.js"></script></body></html>'''
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)
            return
        if not path.startswith('/black-friday/'):
            self.send_error(404)
            return
        super().do_GET()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    print(f'Preview: http://127.0.0.1:{args.port}/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Preview).serve_forever()

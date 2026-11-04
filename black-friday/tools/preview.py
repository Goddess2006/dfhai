"""Local-only preview of the campaign and homepage overlay; no remote requests."""
import argparse
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]

class Preview(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = posixpath.normpath(unquote(urlsplit(self.path).path))
        if path == '/black-friday':
            path = '/black-friday/'
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

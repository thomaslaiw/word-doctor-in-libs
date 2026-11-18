#!/usr/bin/env python3
"""
Word Doctor — shared word bank (optional).

The app works with no server at all: it keeps the word bank in localStorage.
Run this only if you want several devices to share one bank, so that the
"Hardest words" and "Easiest words" modes draw on everybody's results.

It stores counts only. No names, no device ids, no timestamps, no scores per
learner. Two numbers per word: how many times it was answered, how many were
right.

    python3 stats_server.py --port 8099 --file wordbank.json

Then in index.html set:
    const STATS_URL = "https://your-host.example.com";     // no trailing slash

Notes
-----
* Plain HTTP and no authentication. Put it behind HTTPS (a tunnel or a reverse
  proxy) before exposing it to the internet; the page is served over HTTPS so
  a plain http:// endpoint will be blocked as mixed content by the browser.
* Writes are whole-file and atomic enough for a classroom. Do not treat this as
  a database.
* If two people answer at the same instant, both increments are kept: the lock
  serialises them.
"""

import argparse
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

LOCK = threading.Lock()
BANK_FILE = "wordbank.json"
BANK = {}          # word -> {"a": attempts, "c": correct}

ALLOWED_ORIGINS = [
    "https://thomaslaiw.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


def load():
    global BANK
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, encoding="utf-8") as f:
                BANK = json.load(f)
        except Exception:
            BANK = {}


def save():
    tmp = BANK_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(BANK, f, ensure_ascii=False, indent=1)
    os.replace(tmp, BANK_FILE)


class Handler(BaseHTTPRequestHandler):
    server_version = "WordBank/1.0"

    def log_message(self, fmt, *args):
        pass  # keep the console quiet in a classroom

    def _cors(self):
        origin = self.headers.get("Origin", "")
        if origin in ALLOWED_ORIGINS or origin == "":
            self.send_header("Access-Control-Allow-Origin", origin or "*")
        else:
            self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGINS[0])
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        u = urlparse(self.path)

        if u.path == "/health":
            return self._json(200, {"ok": True, "words": len(BANK)})

        if u.path == "/top":
            q = parse_qs(u.query)
            order = (q.get("order", ["hard"])[0] or "hard").lower()
            try:
                n = max(1, min(50, int(q.get("n", ["10"])[0])))
            except ValueError:
                n = 10

            with LOCK:
                rows = [
                    (w, e["c"] / e["a"], e["a"])
                    for w, e in BANK.items()
                    if e.get("a", 0) > 0
                ]
            # easiest = highest accuracy first; hardest = lowest first
            rows.sort(key=lambda r: r[1], reverse=(order != "hard"))
            return self._json(200, {
                "order": order,
                "words": [w for w, _, _ in rows[:n]],
                "detail": [{"word": w, "acc": round(a, 3), "n": n_} for w, a, n_ in rows[:n]],
            })

        if u.path == "/":
            return self._json(200, {"service": "word-doctor word bank", "endpoints": ["/health", "/top", "/record"]})

        return self._json(404, {"error": "no such path"})

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/record":
            return self._json(404, {"error": "no such path"})

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            return self._json(400, {"error": "bad json"})

        word = str(data.get("word", "")).strip().lower()
        if not word or len(word) > 40 or not word.replace("-", "").replace(" ", "").replace("'", "").isalpha():
            return self._json(400, {"error": "bad word"})

        correct = bool(data.get("correct"))

        with LOCK:
            e = BANK.get(word, {"a": 0, "c": 0})
            e["a"] = int(e.get("a", 0)) + 1
            if correct:
                e["c"] = int(e.get("c", 0)) + 1
            BANK[word] = e
            save()

        return self._json(200, {"ok": True, "word": word, "a": e["a"], "c": e["c"]})


def main():
    global BANK_FILE
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8099)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--file", default="wordbank.json")
    ap.add_argument("--allow-origin", action="append", default=None,
                    help="add an origin allowed to call this server")
    a = ap.parse_args()

    BANK_FILE = a.file
    if a.allow_origin:
        ALLOWED_ORIGINS.extend(a.allow_origin)

    load()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"word bank on http://{a.host}:{a.port}  ({len(BANK)} words, file={BANK_FILE})")
    print("endpoints: POST /record   GET /top?order=hard|easy&n=10   GET /health")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()

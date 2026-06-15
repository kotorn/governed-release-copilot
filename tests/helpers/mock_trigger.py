#!/usr/bin/env python3
"""Single-request loopback HTTP trigger used by Pester integration tests."""

from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", required=True, type=Path)
    parser.add_argument("--port-file", required=True, type=Path)
    parser.add_argument("--status", type=int, default=202)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length).decode("utf-8")
            captured = {
                "path": self.path,
                "contentType": self.headers.get("Content-Type"),
                "demoHeader": self.headers.get("X-Demo-Key"),
                "body": json.loads(raw_body),
            }
            args.capture.write_text(json.dumps(captured), encoding="utf-8")
            response = b'{"accepted":true}'
            self.send_response(args.status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            threading.Thread(target=server.shutdown, daemon=True).start()

        def log_message(self, format: str, *values: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    args.port_file.write_text(str(server.server_port), encoding="utf-8")
    server.serve_forever()
    server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

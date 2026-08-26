#!/usr/bin/env python3
"""Persistent HTTP server for PromptKiller web UI."""
import http.server
import socketserver
import os
import sys
import signal

PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIRECTORY)
print(f"🛡️ PromptKiller Web UI serving on http://localhost:{PORT}")
print(f"📁 Serving from: {DIRECTORY}")
print(f"Press Ctrl+C to stop")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress request logs

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)

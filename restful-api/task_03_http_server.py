#!/usr/bin/python3
"""Provide a simple HTTP API on port 8000."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Handle GET requests for the API."""

    def do_GET(self):
        """Return a response based on the requested path."""
        content_type = "text/plain; charset=utf-8"
        status = 200

        if self.path == "/":
            body = "Hello, this is a simple API!"
        elif self.path == "/data":
            content_type = "application/json"
            body = json.dumps({
                "name": "John",
                "age": 30,
                "city": "New York"
            })
        elif self.path == "/status":
            body = "OK"
        elif self.path == "/info":
            content_type = "application/json"
            body = json.dumps({
                "version": "1.0",
                "description": "A simple API built with http.server"
            })
        else:
            status = 404
            body = "Endpoint not found"

        encoded_body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded_body)))
        self.end_headers()
        self.wfile.write(encoded_body)


if __name__ == "__main__":
    server = HTTPServer(("", 8000), SimpleAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

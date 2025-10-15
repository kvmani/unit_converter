"""Flask application factory."""
from __future__ import annotations

from flask import Flask, send_from_directory

from ..config import config
from .routes import bp as units_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(units_blueprint, url_prefix=config.api_prefix)

    @app.after_request
    def apply_security_headers(response):  # type: ignore[override]
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        return response

    @app.get("/")
    def root():
        return send_from_directory(config.static_dir, "index.html")

    @app.get("/ui_dev/<path:filename>")
    def serve_ui(filename: str):
        return send_from_directory(config.static_dir, filename)

    return app


__all__ = ["create_app"]

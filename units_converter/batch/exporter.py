"""Utilities to build downloadable responses."""
from __future__ import annotations

import io

from flask import send_file


def csv_response(content: str, filename: str = "converted.csv"):
    buffer = io.BytesIO(content.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename,
    )

"""Error helpers for the Flask API."""
from __future__ import annotations

from typing import Tuple

from flask import jsonify


def error_response(error_code: str, message: str, status: int) -> Tuple[object, int]:
    payload = {"ok": False, "error_code": error_code, "message": message}
    return jsonify(payload), status

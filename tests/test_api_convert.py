from __future__ import annotations

import json

import pytest

from units_converter.config import config


def test_get_families(client):
    response = client.get(f"{config.api_prefix}/families")
    assert response.status_code == 200
    payload = response.get_json()
    assert "pressure" in payload["families"]


def test_get_units(client):
    response = client.get(f"{config.api_prefix}/units?family=pressure")
    assert response.status_code == 200
    payload = response.get_json()
    symbols = [unit["symbol"] for unit in payload["units"]]
    assert "MPa" in symbols


def test_convert_success(client):
    body = {"value": 200, "from": "MPa", "to": "ksi", "mode": "absolute"}
    response = client.post(
        f"{config.api_prefix}/convert",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert pytest.approx(payload["result"], rel=1e-9) == 29.007547546041838
    assert "ksi" in payload["text"]


def test_convert_invalid_unit(client):
    body = {"value": 1, "from": "unknown", "to": "m"}
    response = client.post(
        f"{config.api_prefix}/convert",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["ok"] is False
    assert payload["error_code"] == "INVALID_UNIT"


def test_convert_bad_mime(client):
    response = client.post(f"{config.api_prefix}/convert", data="{}")
    assert response.status_code == 415

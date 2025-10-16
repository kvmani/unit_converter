from __future__ import annotations

import json

import pytest

from units_converter.config import config


def test_expression_convert(client):
    body = {"expression": "200 MPa * 10 mm^2 to N"}
    response = client.post(
        f"{config.api_prefix}/convert/expression",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert pytest.approx(payload["result"], rel=1e-9) == 2000.0


def test_expression_error(client):
    body = {"expression": "invalid"}
    response = client.post(
        f"{config.api_prefix}/convert/expression",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["ok"] is False

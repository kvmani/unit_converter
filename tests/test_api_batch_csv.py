from __future__ import annotations

import io

import pytest

from units_converter.config import config


CSV_CONTENT = "stress[MPa],thickness[mm]\n200,10\n"


def test_batch_convert_success(client):
    data = {
        "file": (io.BytesIO(CSV_CONTENT.encode("utf-8")), "data.csv"),
        "options": '{"targets":{"stress":"ksi"}}',
    }
    response = client.post(f"{config.api_prefix}/batch/convert", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment")
    body = response.data.decode("utf-8").strip()
    assert "stress[ksi]" in body


def test_batch_invalid_header(client):
    bad_csv = "stress,10\n"
    data = {
        "file": (io.BytesIO(bad_csv.encode("utf-8")), "data.csv"),
    }
    response = client.post(f"{config.api_prefix}/batch/convert", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error_code"] == "BAD_INPUT"

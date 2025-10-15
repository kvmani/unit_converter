"""Flask blueprint exposing the units API."""
from __future__ import annotations

import json
from typing import Any, Dict

from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from ..config import config
from ..engine.converter import (
    BadInputError,
    Converter,
    DimensionMismatchError,
    InvalidUnitError,
    format_value,
)
from ..batch import parser, exporter
from .errors import error_response
from .schemas import BatchOptionsModel, ConvertRequest, ExpressionRequest

bp = Blueprint("units", __name__)
_converter = Converter()


@bp.get("/families")
def get_families() -> Response:
    families = _converter.list_families()
    return jsonify({"families": families})


@bp.get("/units")
def get_units() -> Response:
    family = request.args.get("family")
    if not family:
        return error_response("BAD_INPUT", "family query parameter is required", 400)
    try:
        units = _converter.list_units(family)
    except BadInputError as exc:
        return error_response("BAD_INPUT", str(exc), 400)
    return jsonify({"units": units})


@bp.post("/convert")
def post_convert() -> Response:
    if not request.is_json:
        return error_response("BAD_INPUT", "Request body must be application/json", 415)
    try:
        payload = ConvertRequest.parse_obj(request.get_json())
    except ValidationError as exc:
        return error_response("BAD_INPUT", exc.errors()[0]["msg"], 400)
    if payload.sig_figs is not None and payload.decimals is not None:
        return error_response("BAD_INPUT", "sig_figs and decimals are mutually exclusive", 400)
    try:
        result = _converter.convert(
            payload.value,
            payload.from_unit,
            payload.to_unit,
            mode=payload.mode,
        )
    except InvalidUnitError as exc:
        return error_response("INVALID_UNIT", str(exc), 400)
    except DimensionMismatchError as exc:
        return error_response("DIMENSION_MISMATCH", str(exc), 400)
    except BadInputError as exc:
        return error_response("BAD_INPUT", str(exc), 400)
    formatted_value = format_value(
        result["result"],
        sig_figs=payload.sig_figs,
        decimals=payload.decimals,
        notation=payload.notation,
    )
    body: Dict[str, Any] = {
        "ok": True,
        "result": result["result"],
        "unit": result["unit"],
        "text": f"{formatted_value} {result['unit']}",
        "base": result["base"],
    }
    return jsonify(body)


@bp.post("/convert/expression")
def post_convert_expression() -> Response:
    if not request.is_json:
        return error_response("BAD_INPUT", "Request body must be application/json", 415)
    try:
        payload = ExpressionRequest.parse_obj(request.get_json())
    except ValidationError as exc:
        return error_response("BAD_INPUT", exc.errors()[0]["msg"], 400)
    try:
        result = _converter.convert_expression(payload.expression)
    except InvalidUnitError as exc:
        return error_response("INVALID_UNIT", str(exc), 400)
    except DimensionMismatchError as exc:
        return error_response("DIMENSION_MISMATCH", str(exc), 400)
    except BadInputError as exc:
        return error_response("BAD_INPUT", str(exc), 400)
    body = {"ok": True, "result": result["result"], "unit": result["unit"]}
    return jsonify(body)


@bp.post("/batch/convert")
def post_batch_convert():
    uploaded = request.files.get("file")
    if uploaded is None or uploaded.filename == "":
        return error_response("BAD_INPUT", "file upload is required", 400)
    if not uploaded.filename.lower().endswith(".csv"):
        return error_response("BAD_INPUT", "Only CSV files are supported in v1", 415)
    if request.content_length and request.content_length > config.max_upload_bytes:
        return error_response("LIMIT_EXCEEDED", "Upload is larger than allowed limit", 413)
    raw = uploaded.read()
    if len(raw) > config.max_upload_bytes:
        return error_response("LIMIT_EXCEEDED", "Upload is larger than allowed limit", 413)
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return error_response("BAD_INPUT", "CSV must be UTF-8 encoded", 400)
    options = parser.parse_options(request.form.get("options"))
    try:
        options_model = BatchOptionsModel.parse_obj(options)
    except ValidationError as exc:
        return error_response("BAD_INPUT", exc.errors()[0]["msg"], 400)
    try:
        converted = parser.convert_csv(text, _converter, options_model.dict())
    except parser.BatchConversionError as exc:
        return error_response("BAD_INPUT", str(exc), 400)
    return exporter.csv_response(converted)

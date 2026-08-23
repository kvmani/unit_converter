"""Standalone, dimension-aware local unit conversion service backed by Pint."""
from __future__ import annotations

import argparse

from flask import Flask, Response, jsonify, render_template, request
import pint

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
VERSION = "0.2.0"

FAMILIES = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "inch", "foot", "mile"],
    "Mass": ["gram", "kilogram", "milligram", "pound", "ounce"],
    "Time": ["second", "millisecond", "minute", "hour", "day"],
    "Temperature": ["degC", "degF", "kelvin"],
    "Area": ["meter ** 2", "centimeter ** 2", "foot ** 2", "acre"],
    "Volume": ["liter", "milliliter", "meter ** 3", "gallon"],
    "Speed": ["meter / second", "kilometer / hour", "mile / hour"],
    "Pressure": ["pascal", "kilopascal", "bar", "atmosphere", "psi"],
    "Energy": ["joule", "kilojoule", "calorie", "kilowatt_hour"],
    "Force": ["newton", "kilonewton", "pound_force"],
}

INTERVAL_UNITS = {
    "degC": "delta_degC",
    "degree_Celsius": "delta_degC",
    "degF": "delta_degF",
    "degree_Fahrenheit": "delta_degF",
    "kelvin": "kelvin",
    "K": "kelvin",
}


def _error(code: str, message: str, status: int = 400):
    return jsonify({"ok": False, "error_code": code, "message": message, "error": message}), status


def _interval_unit(unit: str, mode: str) -> str:
    if mode == "absolute":
        return unit
    if mode != "interval":
        raise ValueError("mode must be 'absolute' or 'interval'")
    return INTERVAL_UNITS.get(unit, unit)


def _convert_payload(payload: dict, *, legacy: bool = False):
    try:
        value = float(payload["value"])
        source = str(payload.get("from_unit") if legacy else payload.get("from"))
        target = str(payload.get("to_unit") if legacy else payload.get("to"))
        if source in {"None", ""} or target in {"None", ""}:
            raise KeyError("from/to")
        mode = str(payload.get("mode", "absolute"))
        result = (value * ureg.parse_units(_interval_unit(source, mode))).to(
            _interval_unit(target, mode)
        )
        magnitude = float(result.magnitude)
        return jsonify({
            "ok": True,
            "value": value,
            "from_unit": source,
            "to_unit": target,
            "result": magnitude,
            "unit": target,
            "mode": mode,
            "text": f"{magnitude:g} {target}",
            "formatted": f"{magnitude:g} {target}",
        })
    except KeyError:
        return _error("BAD_INPUT", "value, from, and to are required")
    except pint.DimensionalityError as error:
        return _error("DIMENSION_MISMATCH", str(error))
    except (TypeError, ValueError, pint.PintError) as error:
        return _error("INVALID_UNIT", str(error))


@app.after_request
def security_headers(response: Response) -> Response:
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'")
    if request.path.startswith("/api/"):
        response.headers.setdefault("Cache-Control", "no-store")
    return response


@app.get("/")
def home():
    return render_template("index.html", families=FAMILIES)


@app.get("/help")
def help_page():
    return render_template("help.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "tool_id": "unit-converter", "version": VERSION})


@app.get("/api/families")
def families():
    return jsonify({"ok": True, "families": FAMILIES})


@app.get("/api/units/<family>")
def units(family):
    if family not in FAMILIES:
        return jsonify({"ok": False, "error": "Unknown unit family"}), 404
    return jsonify({"ok": True, "family": family, "units": FAMILIES[family]})


@app.post("/api/convert")
def convert():
    return _convert_payload(request.get_json(silent=True) or {}, legacy=True)


@app.post("/api/expressions")
def expressions():
    payload = request.get_json(silent=True) or {}
    try:
        expression = str(payload["expression"])
        if " to " in expression.lower():
            left, target = expression.rsplit(" to ", 1)
        else:
            left, target = expression, str(payload.get("target", ""))
        quantity = ureg.parse_expression(left.strip())
        result = quantity.to(target.strip()) if target.strip() else quantity
        return jsonify({"ok": True, "expression": expression, "result": float(result.magnitude),
                        "units": str(result.units), "formatted": f"{result.magnitude:g} {result.units}"})
    except (KeyError, TypeError, ValueError, pint.PintError) as error:
        return _error("BAD_INPUT", str(error))


@app.get("/api/v1/units/families")
def v1_families():
    return jsonify({"families": list(FAMILIES)})


@app.get("/api/v1/units/units")
def v1_units():
    family = request.args.get("family", "")
    matched = next((name for name in FAMILIES if name.lower() == family.lower()), None)
    if matched is None:
        return _error("BAD_INPUT", "Unknown unit family", 404)
    units = [{"symbol": unit, "aliases": [], "dimension": matched.lower()} for unit in FAMILIES[matched]]
    return jsonify({"units": units})


@app.post("/api/v1/units/convert")
def v1_convert():
    return _convert_payload(request.get_json(silent=True) or {})


@app.post("/api/v1/units/convert/expression")
def v1_expression():
    return expressions()


def main() -> None:  # pragma: no cover
    from waitress import serve
    parser = argparse.ArgumentParser(description="Unit Converter service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5065)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    serve(app, host=args.host, port=args.port, threads=args.threads)


if __name__ == "__main__":  # pragma: no cover
    main()

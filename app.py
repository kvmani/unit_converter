"""Standalone local unit conversion service backed by Pint."""
from __future__ import annotations

from flask import Flask, jsonify, render_template, request
import pint

app = Flask(__name__)
ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

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


@app.get("/")
def home():
    return render_template("index.html", families=FAMILIES)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "tool_id": "unit-converter", "version": "0.1.0"})


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
    payload = request.get_json(silent=True) or {}
    try:
        value = float(payload["value"])
        source = str(payload["from_unit"])
        target = str(payload["to_unit"])
        result = (value * ureg.parse_units(source)).to(target)
        return jsonify({"ok": True, "value": value, "from_unit": source, "to_unit": target,
                        "result": float(result.magnitude), "formatted": f"{result.magnitude:g} {result.units}"})
    except (KeyError, TypeError, ValueError, pint.PintError) as error:
        return jsonify({"ok": False, "error": str(error)}), 400


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
        return jsonify({"ok": False, "error": str(error)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5065, debug=False)

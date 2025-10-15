"""CSV batch conversion helpers."""
from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from ..engine.converter import Converter

_HEADER_PATTERN = re.compile(r"^(?P<name>[^\[]+)\[(?P<unit>[^\]]+)\]$")


@dataclass
class ColumnInstruction:
    name: str
    source_unit: str
    target_unit: Optional[str]
    mode: str = "absolute"


class BatchConversionError(Exception):
    """Raised for malformed batch files."""


def parse_options(raw: str | None) -> Dict[str, object]:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BatchConversionError("Options payload must be valid JSON.") from exc


def build_instructions(
    headers: Iterable[str], options: Dict[str, object]
) -> List[ColumnInstruction]:
    instructions: List[ColumnInstruction] = []
    targets = options.get("targets", {}) if isinstance(options, dict) else {}
    modes = options.get("mode", {}) if isinstance(options, dict) else {}
    for header in headers:
        match = _HEADER_PATTERN.match(header.strip())
        if not match:
            raise BatchConversionError(
                f"Header '{header}' must include a unit declaration like name[unit]."
            )
        name = match.group("name").strip()
        unit = match.group("unit").strip()
        target_unit = None
        if isinstance(targets, dict):
            target_unit = targets.get(name)
        mode = "absolute"
        if isinstance(modes, dict) and name in modes:
            mode = modes[name]
        instructions.append(ColumnInstruction(name=name, source_unit=unit, target_unit=target_unit, mode=mode))
    return instructions


def convert_csv(content: str, converter: Converter, options: Dict[str, object]) -> str:
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None:
        raise BatchConversionError("CSV must include headers.")
    instructions = build_instructions(reader.fieldnames, options)
    output = io.StringIO()
    fieldnames = [f"{instr.name}[{instr.target_unit or instr.source_unit}]" for instr in instructions]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    row_count = 0
    for row in reader:
        row_count += 1
        converted_row: Dict[str, str] = {}
        for instr in instructions:
            raw_value = row.get(f"{instr.name}[{instr.source_unit}]")
            if raw_value is None or raw_value.strip() == "":
                converted_row[f"{instr.name}[{instr.target_unit or instr.source_unit}]"] = ""
                continue
            result = converter.convert(
                raw_value,
                instr.source_unit,
                instr.target_unit or instr.source_unit,
                mode=instr.mode,
            )
            converted_row[f"{instr.name}[{instr.target_unit or instr.source_unit}]"] = str(result["result"])
        writer.writerow(converted_row)
    return output.getvalue()


__all__ = [
    "BatchConversionError",
    "convert_csv",
    "parse_options",
    "build_instructions",
]

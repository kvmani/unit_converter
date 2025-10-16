"""Custom unit registry definitions and helpers."""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, Iterable, List

from pint import UnitRegistry


_CUSTOM_DEFINITIONS: List[str] = [
    "angstrom = 1e-10 * meter = Å = angstrom = angstroem",
    "micron = 1e-6 * meter = micrometer = µm",
    "ksi = 1000 * psi",
    "MPa = megapascal",
    "GPa = gigapascal",
    "N_per_mm2 = newton / millimeter ** 2 = N/mm^2",
    "millimeter_of_meter = 1e-3 * meter = mm",
    "microohm = 1e-6 * ohm",
    "microohm_centimeter = microohm * centimeter = μΩ·cm",
    "kilojoule_per_mole = kilojoule / mole = kJ/mol",
    "watt_per_meter_kelvin = watt / meter / kelvin = W/m·K = W/m/K = W/m*K",
    "poiseuille = pascal * second = Pa·s",
    "centipoise = poise / 100 = cP",
]


_INTERVAL_UNIT_MAP: Dict[str, str] = {
    "degC": "delta_degC",
    "°C": "delta_degC",
    "celsius": "delta_degC",
    "degF": "delta_degF",
    "°F": "delta_degF",
    "fahrenheit": "delta_degF",
    "kelvin": "kelvin",  # Kelvin works the same for absolute and interval
    "K": "kelvin",
}


def _build_registry() -> UnitRegistry:
    ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
    ureg.default_format = "P"  # Compact pretty printer
    for definition in _CUSTOM_DEFINITIONS:
        ureg.define(definition)
    try:
        ureg.enable_contexts("chemistry")
    except Exception:  # pragma: no cover - context may be unavailable in old Pint
        pass
    return ureg


@lru_cache(maxsize=1)
def get_registry() -> UnitRegistry:
    """Return a shared :class:`~pint.UnitRegistry` instance."""

    return _build_registry()


def get_interval_unit(unit_symbol: str) -> str:
    """Map a temperature unit to its interval counterpart when needed."""

    return _INTERVAL_UNIT_MAP.get(unit_symbol, unit_symbol)


def iter_custom_units() -> Iterable[str]:
    """Yield the string definitions injected into the registry."""

    return tuple(_CUSTOM_DEFINITIONS)

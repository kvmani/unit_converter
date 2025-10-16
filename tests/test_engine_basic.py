from __future__ import annotations

import math

import pytest

from units_converter.engine import Converter, InvalidUnitError


@pytest.fixture(scope="module")
def converter() -> Converter:
    return Converter()


def test_pressure_aliases(converter: Converter) -> None:
    result = converter.convert(1, "MPa", "N/mm^2")
    assert pytest.approx(result["result"], rel=1e-12) == 1.0


def test_pressure_to_ksi(converter: Converter) -> None:
    result = converter.convert(200, "MPa", "ksi")
    assert pytest.approx(result["result"], rel=1e-9) == 29.007547546041838


def test_length_angstrom_to_meter(converter: Converter) -> None:
    result = converter.convert(1, "Å", "m")
    assert pytest.approx(result["result"], rel=1e-12) == 1e-10


def test_energy_kj_per_mol_to_ev(converter: Converter) -> None:
    result = converter.convert(1, "kJ/mol", "eV")
    assert pytest.approx(result["result"], rel=1e-9) == pytest.approx(0.010364269656262174, rel=1e-9)


def test_resistivity_microohm_cm(converter: Converter) -> None:
    result = converter.convert(1, "μΩ·cm", "ohm * meter")
    assert pytest.approx(result["result"], rel=1e-9) == 1e-8


def test_diffusivity_identity(converter: Converter) -> None:
    result = converter.convert(1.0, "m^2/s", "m^2/s")
    assert result["result"] == pytest.approx(1.0)


def test_invalid_unit(converter: Converter) -> None:
    with pytest.raises(InvalidUnitError):
        converter.convert(1, "not_a_unit", "m")

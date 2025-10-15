from __future__ import annotations

import pytest

from units_converter.engine import Converter, DimensionMismatchError


@pytest.fixture(scope="module")
def converter() -> Converter:
    return Converter()


def test_absolute_temperature(converter: Converter) -> None:
    result = converter.convert(25, "degC", "K", mode="absolute")
    assert pytest.approx(result["result"], rel=1e-6) == 298.15


def test_interval_temperature(converter: Converter) -> None:
    result = converter.convert(25, "degC", "K", mode="interval")
    assert pytest.approx(result["result"], rel=1e-9) == 25.0


def test_temperature_mismatch(converter: Converter) -> None:
    with pytest.raises(DimensionMismatchError):
        converter.convert(10, "degC", "m")

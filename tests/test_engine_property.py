from __future__ import annotations

import pytest
from hypothesis import given, strategies as st

from units_converter.engine import Converter


@pytest.fixture(scope="module")
def converter() -> Converter:
    return Converter()


@given(st.floats(min_value=1e-9, max_value=1e6, allow_nan=False, allow_infinity=False))
def test_length_round_trip(converter: Converter, value: float) -> None:
    forward = converter.convert(value, "m", "mm")
    backward = converter.convert(forward["result"], "mm", "m")
    assert pytest.approx(backward["result"], rel=1e-9) == value


@given(st.floats(min_value=1e-6, max_value=1e3, allow_nan=False, allow_infinity=False))
def test_pressure_monotonic(converter: Converter, value: float) -> None:
    result1 = converter.convert(value, "MPa", "ksi")
    result2 = converter.convert(value + 1e-6, "MPa", "ksi")
    assert result2["result"] > result1["result"]

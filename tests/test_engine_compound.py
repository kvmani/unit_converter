from __future__ import annotations

import pytest

from units_converter.engine import Converter, BadInputError


@pytest.fixture(scope="module")
def converter() -> Converter:
    return Converter()


def test_compound_expression(converter: Converter) -> None:
    result = converter.convert_expression("200 MPa * 10 mm^2 to N")
    assert pytest.approx(result["result"], rel=1e-9) == 2000.0


def test_formatting_helper(converter: Converter) -> None:
    basic = converter.convert(1234.5, "Pa", "kPa")
    assert pytest.approx(basic["result"], rel=1e-9) == 1.2345


def test_expression_without_to(converter: Converter) -> None:
    with pytest.raises(BadInputError):
        converter.convert_expression("200 MPa * 10 mm^2")

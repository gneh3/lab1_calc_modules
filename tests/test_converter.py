from decimal import Decimal

import pytest

from toolkit.converter import Converter
from toolkit.errors import ConverterError


@pytest.fixture
def convrt():
    return Converter()

def test_convert_length_and_mass(convrt):
    assert convrt.convert(Decimal(1000), "mm", "m") == Decimal(1)
    assert convrt.convert(Decimal("1.5"), "kg", "g") == Decimal(1500)

def test_convert_temperature(convrt):
    assert convrt.convert(Decimal(0), "C", "F") == Decimal(32)
    assert convrt.convert(Decimal("-273.15"), "C", "K") == Decimal(0)

def test_convert_absolute_zero_error(convrt):
    with pytest.raises(ConverterError):
        convrt.convert(Decimal(-300), "C", "K")
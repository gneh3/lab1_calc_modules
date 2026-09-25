from decimal import Decimal
from typing import ClassVar

from toolkit.additional_functions import round_decimal
from toolkit.errors import ConverterError, ConverterErrorType


class Converter:
    _UNITS: ClassVar[dict[str, dict[str, Decimal]]] = { 
        "length": {
            "m": Decimal(1),
            "km": Decimal(1000),
            "cm": Decimal("0.01"),
            "mm": Decimal("0.001"),
        },
        "mass": {
            "g": Decimal(1),
            "kg": Decimal(1000),
            "mg": Decimal("0.001"),
        },
    }

    _TEMP_UNITS: ClassVar[set[str]] = {"c", "f", "k"} 

    def convert(self, value: Decimal, from_unit: str, to_unit: str) -> Decimal:
        from_u = from_unit.lower().strip()
        to_u = to_unit.lower().strip()

        if (from_u in self._TEMP_UNITS) and (to_u in self._TEMP_UNITS):
            return self._convert_temperature(value, from_u, to_u)

        category = self._find_category(from_u, to_u)
        
        base_value = value*self._UNITS[category][from_u]
        result = base_value/self._UNITS[category][to_u]
        
        return round_decimal(result, False)

    def _find_category(self, from_unit: str, to_unit: str) -> str:
        all_known_units = {u for cat in self._UNITS.values() for u in cat}
        if from_unit not in all_known_units or to_unit not in all_known_units:
            raise ConverterError(ConverterErrorType.UNKNOWN_UNIT.value)

        for category, units in self._UNITS.items():
            if from_unit in units and to_unit in units:
                return category

        raise ConverterError(ConverterErrorType.INCOMPATIBLE_UNITS.value)

    @staticmethod
    def _convert_temperature(value: Decimal, from_u: str, to_u: str) -> Decimal:

        if from_u == "k":
            kelvin = value
        elif from_u == "c":
            kelvin = value + Decimal("273.15")
        elif from_u == "f":
            kelvin = (value - Decimal(32)) * Decimal(5) /Decimal(9) + Decimal("273.15")

        if kelvin < Decimal(0):
            raise ConverterError(ConverterErrorType.BELOW_ABSOLUTE_ZERO.value)

        if to_u == "k":
            return round_decimal(kelvin, False)
        elif to_u == "c":
            return round_decimal(kelvin - Decimal("273.15"), False)
        elif to_u == "f":
            return round_decimal((kelvin - Decimal("273.15")) * Decimal(9) / Decimal(5) + Decimal(32), False)
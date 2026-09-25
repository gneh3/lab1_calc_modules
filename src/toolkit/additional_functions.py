from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from toolkit.constants import ROUNDING_PRECISION
from toolkit.errors import (
        CalculatorError,
        CalculatorErrorType,
        ConverterError,
        ConverterErrorType,
)


def round_decimal(value: Decimal, fromCalc: bool) -> Decimal:
        if ROUNDING_PRECISION == 0:
            mask = Decimal(1)
        else:
            mask = Decimal('0.' + '0' * (ROUNDING_PRECISION - 1) + '1')
    
        try:
            rounded = value.quantize(mask, rounding=ROUND_HALF_UP)
        except InvalidOperation:
            raise CalculatorError(CalculatorErrorType.INVALID_DECIMAL_PARSE.value)\
                if fromCalc else ConverterError(ConverterErrorType.INVALID_DECIMAL_PARSE.value)
    
        if rounded == rounded.to_integral():
            return rounded.quantize(Decimal(1))
        return rounded.normalize()
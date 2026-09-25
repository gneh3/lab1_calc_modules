from decimal import Decimal

import pytest
from toolkit.calculator import ParserToRPN, RPNCalculator, Tokenizer
from toolkit.errors import CalculatorError


def solve(expr: str) -> Decimal:
    tokens = Tokenizer(expr).tokenize_sequence()
    rpn = ParserToRPN(tokens).parse_to_rpn()
    return RPNCalculator(rpn).CalculateRPN()

def test_calc_basic():
    assert solve("  2+3*4") == Decimal(14)
    assert solve("10 / 4 ") == Decimal("2.5")
    assert solve("-2 * -3") == Decimal(6)
    assert solve("10 // 3 + 10 % 3") == Decimal(4)
    assert solve("-(5 * 3) + 3") == Decimal(-12)
    assert solve("2.5 * (4 - 2)") == Decimal(5)

def test_calc_errors():
    with pytest.raises(CalculatorError):
        solve("1/0")
    with pytest.raises(CalculatorError):
        solve("2+a")
    with pytest.raises(CalculatorError):
        solve("2*/3")
    with pytest.raises(CalculatorError):
        solve("")
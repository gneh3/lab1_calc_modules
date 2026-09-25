from enum import Enum


class ToolkitBaseError(Exception):
    """toolkit base error"""

class CalculatorError(ToolkitBaseError):
    """calculator running error"""

class ConverterError(ToolkitBaseError):
    """converter running error"""

class CalculatorErrorType(Enum):
    EMPTY_SEQUENCE = "Empty sequence exception"
    UNDEFINED_CHARACTER = "Undefined character exception"
    WRONG_NUMBER_SYNTAXIS = "Wrong number syntaxis exception"
    PARENTHESIS_MISMATCH = "Parenthesis mismatch exception"
    TWO_BINARY_OPERATIORS_IN_ROW = "Two bianry operators in a row exception"
    BINARY_OPERATOR_AFTER_OPEN_PAREN = "Binary operator after open parenthesis exception"
    BINARY_OPERATOR_AT_START = "Binary operator at the beginning of an expression exception"
    OPERATOR_BEFORE_CLOSE_PAREN = "Operator before close parenthesis exception"
    OPERATOR_IN_THE_END_OF_EXPRESSION = "Operator in the end of expression exception"
    INCORRECT_EXPRESSION = "Incorrect expression exception"
    UNDEFINED_UNARY_OPERATION = "Undefined unary operation exception"
    UNDEFINED_BINARY_OPERATION = "Undefined binary operation exception"
    DIVISION_BY_ZERO = "Division by zero exception"
    INVALID_DECIMAL_PARSE = "Invalid decimal parse exception(ROUNDING_PRECISION is to big?)"

class ConverterErrorType(Enum):
    INCOMPATIBLE_UNITS = "Incompatible units exception"
    UNKNOWN_UNIT = "Unknown unit exception"
    BELOW_ABSOLUTE_ZERO = "Value below absolute zero exception"
    INVALID_DECIMAL_PARSE = "Invalid decimal parse exception(ROUNDING_PRECISION is to big?)"
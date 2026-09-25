from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum, auto

from toolkit import additional_functions
from toolkit.constants import SIGNS_ALPHABET
from toolkit.errors import CalculatorError, CalculatorErrorType


class Token(ABC):
    """base abstract class of token"""

class OperationType(Enum):
    # value = (symbol, priority, arguments_count)
    UNARY_PLUS = ("+", 3, 1)
    UNARY_MINUS = ("-", 3, 1)
    BINARY_PLUS = ("+", 1, 2)
    BINARY_MINUS = ("-", 1, 2)
    MULTIPLICATION = ("*", 2, 2)
    DIVISION = ("/", 2, 2)
    EXACT_DIVISION = ("//", 2, 2)
    REMAINDER = ("%", 2, 2)

    @property
    def symbol(self) -> str:
        return self.value[0]

    @property
    def priority(self) -> int:
        return self.value[1]

    @property
    def arguments_count(self) -> int:
        return self.value[2]

    @staticmethod
    def get_type_by_symbol(symbol: str) -> OperationType:
        for operation in OperationType:
            if operation.symbol == symbol:
                return operation

@dataclass(frozen = True)
class OperationToken(Token):
    operation: OperationType
   
class ParenType(Enum):
    RIGHT = auto()
    LEFT = auto()

@dataclass(frozen = True)
class ParenToken(Token):
    paren_type: ParenType

@dataclass(frozen = True)
class NumberToken(Token):
    value: Decimal

class Tokenizer:
    def __init__(self, raw_sequence: str) -> None:
        if not raw_sequence:
            raise CalculatorError(CalculatorErrorType.EMPTY_SEQUENCE.value)
        self._text = raw_sequence
        self._text_i = 0

    def tokenize_sequence(self) -> list[Token]:
        tokens: list[Token] = []
        last_token: Token = None

        while self._text_i < len(self._text):
            if self._text[self._text_i].isspace():
                self._text_i += 1
            elif self._text[self._text_i].isdigit():
                num_as_string = self._take_while(self._is_decimal_char)
                num_as_string = num_as_string.replace(",", ".")
                try:
                    last_token = NumberToken(value=Decimal(num_as_string))
                except InvalidOperation:
                    raise CalculatorError(CalculatorErrorType.WRONG_NUMBER_SYNTAXIS.value)

                tokens.append(last_token)
            elif self._is_operation_char(self._text[self._text_i]):
                if self._text.startswith("//", self._text_i):
                    last_token = OperationToken(operation=OperationType.EXACT_DIVISION)
                    tokens.append(last_token)
                    self._text_i += 2

                elif self._is_operation_char(self._text[self._text_i]):
                    char = self._text[self._text_i]
                    if char == "+":
                        op = OperationType.UNARY_PLUS if self._is_unary(last_token) else OperationType.BINARY_PLUS
                    elif char == "-":
                        op = OperationType.UNARY_MINUS if self._is_unary(last_token) else OperationType.BINARY_MINUS
                    else:
                        op = OperationType.get_type_by_symbol(char)
        
                    last_token = OperationToken(operation=op)
                    tokens.append(last_token)
                    self._text_i += 1
            elif self._text[self._text_i] in "()":
                paren = ParenType.LEFT if self._text[self._text_i] == "(" else ParenType.RIGHT
                last_token = ParenToken(paren_type=paren)
                tokens.append(last_token)
                self._text_i += 1
            else:
                raise CalculatorError(CalculatorErrorType.UNDEFINED_CHARACTER.value)

        if not tokens:
            raise CalculatorError(CalculatorErrorType.EMPTY_SEQUENCE.value)

        return tokens

    def _take_while(self, predicate: Callable[[str], bool]) -> str:
        start = self._text_i
        while self._text_i < len(self._text) and predicate(self._text[self._text_i]):
            self._text_i += 1
        return self._text[start : self._text_i]

    @staticmethod
    def _is_decimal_char(char: str) -> bool:
        return char.isdigit() or char in ".,"

    @staticmethod
    def _is_operation_char(char: str) -> bool:
        return char in SIGNS_ALPHABET

    @staticmethod
    def _is_unary(last_token: Token) -> bool:
        return last_token is None or (isinstance(last_token, ParenToken) and last_token.paren_type == ParenType.LEFT) or isinstance(last_token, OperationToken) 

class ParserToRPN:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens

    def parse_to_rpn(self) -> list[Token]:
        output_tokens: list[Token] = []
        stack: list[Token] = []
        last_token = None

        for token in self._tokens:
            match token:
                case NumberToken():
                    output_tokens.append(token)
                case ParenToken(paren_type=ParenType.LEFT):
                    stack.append(token)
                case ParenToken(paren_type=ParenType.RIGHT):
                    if isinstance(last_token, OperationToken):
                        raise CalculatorError(CalculatorErrorType.OPERATOR_BEFORE_CLOSE_PAREN.value)
                    while stack:
                        current_token = stack.pop()
                        if isinstance(current_token, ParenToken) and current_token.paren_type == ParenType.LEFT:
                            break
                        else:
                            output_tokens.append(current_token)
                    else:
                        raise CalculatorError(CalculatorErrorType.PARENTHESIS_MISMATCH.value)
                case OperationToken():
                    if token.operation.arguments_count == 2:
                       match last_token:
                           case None:
                               raise CalculatorError(CalculatorErrorType.BINARY_OPERATOR_AT_START.value)
                           case OperationToken() if last_token.operation.arguments_count != 1:
                               raise CalculatorError(CalculatorErrorType.TWO_BINARY_OPERATIORS_IN_ROW.value)
                           case ParenToken() if last_token.paren_type == ParenType.LEFT:
                               raise CalculatorError(CalculatorErrorType.BINARY_OPERATOR_AFTER_OPEN_PAREN.value)
                    while len(stack) != 0 and (not (isinstance(stack[-1], ParenToken) and stack[-1].paren_type == ParenType.LEFT)):
                        if isinstance(stack[-1], OperationToken):
                            if stack[-1].operation.priority >= token.operation.priority:
                                output_tokens.append(stack.pop())
                            else:
                                break
                    stack.append(token)
                        
            last_token = token

        if isinstance(last_token, OperationToken):
            raise CalculatorError(CalculatorErrorType.OPERATOR_IN_THE_END_OF_EXPRESSION.value)

        if len([i for i in stack if isinstance(i, ParenToken)]) != 0:
            raise CalculatorError(CalculatorErrorType.PARENTHESIS_MISMATCH.value)

        while stack:
            output_tokens.append(stack.pop())
             
        return output_tokens

class RPNCalculator:
    def __init__(self, rpn_tokens: list[Token]):
        self._rpn_tokens = rpn_tokens

    def CalculateRPN(self) -> Decimal:
        stack: list[Decimal] = []
        while self._rpn_tokens:
            token: Token = self._rpn_tokens.pop(0)
            if isinstance(token, NumberToken):
                stack.append(token.value) 
            elif isinstance(token, OperationToken):
                result: Decimal = None
                match token.operation.arguments_count:
                    case 1:
                        num1 = stack.pop()
                        match token.operation:
                            case OperationType.UNARY_PLUS:
                                result = num1
                            case OperationType.UNARY_MINUS:
                                result = -num1
                            case _:
                                raise CalculatorError(CalculatorErrorType.UNDEFINED_UNARY_OPERATION.value)
                    case 2:
                        num2 = stack.pop()
                        num1 = stack.pop()
                        if token.operation in (OperationType.DIVISION,\
                            OperationType.EXACT_DIVISION, OperationType.REMAINDER) and num2 == 0:
                            raise CalculatorError(CalculatorErrorType.DIVISION_BY_ZERO.value)
                        match token.operation:
                            case OperationType.BINARY_PLUS:
                                result = num1+num2
                            case OperationType.BINARY_MINUS:
                                result = num1-num2
                            case OperationType.MULTIPLICATION:
                                result = num1*num2
                            case OperationType.DIVISION:
                                result = num1/num2
                            case OperationType.EXACT_DIVISION:
                                result = num1//num2
                            case OperationType.REMAINDER:
                                result = num1%num2
                            case _:
                                raise CalculatorError(CalculatorErrorType.UNDEFINED_BINARY_OPERATION.value)
               
                stack.append(result)

        if len(stack) != 1:
            raise CalculatorError(CalculatorErrorType.INCORRECT_EXPRESSION.value)

        return additional_functions.round_decimal(stack[0], True)
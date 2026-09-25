import argparse
import sys
from decimal import Decimal

from toolkit.calculator import ParserToRPN, RPNCalculator, Tokenizer
from toolkit.converter import Converter
from toolkit.errors import CalculatorError, ConverterError


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI Calculator&Converer" )

    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc", help="Calculate expression")
    calc_parser.add_argument("expression", type=str, help="Math expression")

    convert_parser = subparsers.add_parser("convert", help="Convert values")
    convert_parser.add_argument("value", type=str, help="Value")
    convert_parser.add_argument("--from", dest="from_unit", required=True, help="From")
    convert_parser.add_argument("--to", dest="to_unit", required=True, help="To")

    args = parser.parse_args()

    try:
        if args.command == "calc":
            tokens = Tokenizer(args.expression).tokenize_sequence()
            rpn_tokens = ParserToRPN(tokens).parse_to_rpn()
            result = RPNCalculator(rpn_tokens).CalculateRPN()
            print(f"Result: {result}")
        elif args.command == "convert":
            val = Decimal(args.value.replace(",", "."))
            converter = Converter()
            result = converter.convert(val, args.from_unit, args.to_unit)
            print(f"Result: {result} {args.to_unit}")

    except CalculatorError as err:
        print(f"Calculator Error: {err}", file=sys.stderr)
        sys.exit(2)
    except ConverterError as err:
        print(f"Converter Error: {err}", file=sys.stderr)
        sys.exit(2)
    except Exception as err: # noqa: BLE001
        print(f"Undefined Error: {err}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
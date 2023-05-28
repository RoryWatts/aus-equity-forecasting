import argparse
from . import runtime
import json
DESCRIPTION = f"""
Home Finances Model
Built by Rory Watts, 2023

---------------------------------------------------

Analyse different scenarios for your home finances.
e.g. renting vs. buying.

===================================================
"""

EPILOG = """
For further assistance, please refer to the documentation in the README.md
Examples:
    home_finances individual --input <FILE> --output <FILE>
    home_finances compare --baseline <FILE> --comparison <FILE> --output <FILE>
"""
def individual_handler(input, output=None):
    with open(input, 'r') as f:
        configuration = json.load(f)
    ledger = runtime.simulate(configuration)
    if output is None:
        print(ledger)


def comparison_handler(baseline, comparison, output=None):
    ...


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    # Create the parser for the "individual" command
    parser_individual = subparsers.add_parser('individual', help='Process an individual file')
    parser_individual.add_argument('--input', required=True, help='Input filepath')
    parser_individual.add_argument('--output', help='Output filepath')

    # Create the parser for the "compare" command
    parser_comparison = subparsers.add_parser('compare', help='Perform a comparison between two files.')
    parser_comparison.add_argument('--baseline', required=True, help='Baseline file for the comparison.')
    parser_comparison.add_argument('--comparison', required=True, help='Comparison file.')
    parser_comparison.add_argument('--output', help='Output file for the comparison.')

    # Parse arguments
    args = parser.parse_args()

    # If no arguments were provided, print the help message
    if args.command is None:
        parser.print_help()
        return

    # Call the appropriate handler
    if args.command == 'individual':
        individual_handler(args.input, args.output)
    elif args.command == 'compare':
        comparison_handler(args.baseline, args.comparison, args.output)


if __name__ == '__main__':
    main()
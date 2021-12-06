import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [INPUT-FILE] [OUTPUT-FILE]",
        description="Converts Beaconchain validator CSV rewards exports to Blockpit import Excel file."
    )
    parser.add_argument('inputfile', type=str, nargs=1,
                    help='CSV export file name from beaconcha.in')
    parser.add_argument('outputfile', type=str, nargs=1,
                    help='Output file name (Excel)')
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0.1"
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    print(args.inputfile)
    print(args.outputfile)
main()
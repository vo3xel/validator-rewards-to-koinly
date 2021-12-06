import argparse
import os
import csv
import sys
from decimal import Decimal

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s INPUT-FILE [OUTPUT-FILE]",
        description="Converts Beaconchain validator CSV rewards exports to Blockpit.io Excel file."
    )
    parser.add_argument('input_file', type=str, nargs=1,
                    help='CSV export file name from beaconcha.in')
    parser.add_argument("-o", "--output-file", type=str, nargs=1,
        help='Output file name (Excel) for Blockpit.io')                   
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0.1"
    )
    return parser

def parse_input_file_name(filename: str) -> str:
    if os.path.isfile(filename):
            if len(str(filename).rsplit('.', 1)) != 2 or filename.rsplit('.', 1)[1] != 'csv':
                sys.exit("INPUT-FILE exists but file name is invalid. File name must end with \".csv\"")
            else:
                return filename
    else:
        sys.exit("Error: INPUT-FILE is not a valid file.")

def parse_output_file_name(filename: str) -> str:
    if len(str(filename).rsplit('.', 1)) != 2 or filename.rsplit('.', 1)[1] != 'xlsx':
        sys.exit("OUTPUT-FILE name is invalid. File name must end with \".xlsx\"")
    else:
        return filename

def CSV2XLSX(input_file: str,output_file: str) -> None:
    with open(input_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(csvreader, None)
        print(f"CSV header: {', '.join(headers)}")
        number_of_entries = 0
        total_ETH_rewards = 0
        total_EUR_rewards = 0
        dates = []
        incomes_ETH = []
        incomes_EUR = []
        ETH_prices = []
        for row in csvreader:
            dates.append(row[0])
            current_ETH_reward = Decimal("".join(d for d in row[2] if d.isdigit() or d == '.'))
            current_EUR_reward = Decimal("".join(d for d in row[4] if d.isdigit() or d == '.'))
            incomes_ETH.append(current_ETH_reward)
            incomes_EUR.append(current_EUR_reward)
            ETH_prices.append(Decimal("".join(d for d in row[3] if d.isdigit() or d == '.')))
            number_of_entries = number_of_entries + 1
            total_ETH_rewards = total_ETH_rewards + current_ETH_reward
            total_EUR_rewards = total_EUR_rewards + current_EUR_reward
        average_ETH_price =  sum(ETH_prices)/len(ETH_prices)
        print("---   CSV information   ---")
        print(f"\tTime range: from {dates[-1]} to {dates[0]}")
        print(f"\tNumber of entries: {number_of_entries}")          
        print(f"\tTotal ETH rewards: {total_ETH_rewards}")
        print(f"\tTotal rewards in EUR: {total_EUR_rewards}")
        print(f"\tAverage ETH price: {average_ETH_price}")
        print("--- END CSV information ---")
    return

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    input_file_name = parse_input_file_name(args.input_file[0])
    if args.output_file is None:
        output_file_name = input_file_name.rsplit('.',1)[0] + ".xlsx"
    else:
        output_file_name = parse_output_file_name(args.output_file[0])
    print(f"Input file: {input_file_name}")
    print(f"Output file: {output_file_name}")
    CSV2XLSX(input_file_name,output_file_name)

main()
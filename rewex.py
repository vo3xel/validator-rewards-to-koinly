import argparse
import os
import csv
import sys
from decimal import Decimal
from datetime import datetime

VERSION = "0.0.2"

BLOCKPIT_FIELD_NAMES =  [   'id', \
                            'exchange_name', \
                            'depot_name', \
                            'transaction_date', \
                            'buy_asset', \
                            'buy_amount', \
                            'sell_asset', \
                            'sell_amount', \
                            'fee_asset', \
                            'fee_amount', \
                            'transaction_type', \
                            'note', \
                            'linked_transaction' ]


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s INPUT_FILE [OUTPUT-FILE]",
        description="Converts Beaconchain validator CSV rewards exports to Blockpit.io CSV file."
    )
    parser.add_argument('INPUT_FILE', type=str, nargs=1,
                    help='CSV export file name from beaconcha.in')
    parser.add_argument("-o", "--output-file",type=str, nargs=1,
        help='Output file name (CSV) for Blockpit.io')
    parser.add_argument("-d", "--depot-name", type=str, nargs=1,
        help='Blockpit.io depot name')
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version {VERSION}"
    )
    return parser

def parse_input_file_name(filename: str) -> str:
    if os.path.isfile(filename):
            if len(str(filename).rsplit('.', 1)) != 2 or filename.rsplit('.', 1)[1] != 'csv':
                sys.exit("INPUT_FILE exists but file name is invalid. File name must end with \".csv\"")
            else:
                return filename
    else:
        sys.exit("Error: INPUT_FILE is not a valid file.")

def parse_output_file_name(filename: str) -> str:
    if len(str(filename).rsplit('.', 1)) != 2 or filename.rsplit('.', 1)[1] != 'csv':
        sys.exit("OUTPUT_FILE name is invalid. File name must end with \".csv\"")
    else:
        return filename

# Blockpit CSV format: Date & Time: DD.MM.YYYY HH:MM:SS, Decimal Separator: dot "." and Column Separator: comma ","
# More info: https://help.blockpit.io/hc/de-at/articles/360011877920
def CSV2Blockpit(input_file: str,output_file: str, depot_name: str) -> None:
    with open(input_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(csvreader, None)
        with open(output_file, 'w', newline='') as csvwriterfile:
            csvwriter = csv.writer(csvwriterfile, delimiter=',')
            csvwriter.writerow(BLOCKPIT_FIELD_NAMES)
            total_ETH_rewards = 0
            total_EUR_rewards = 0
            blockpit_transaction_id = 1
            average_ETH_price = 0
            for row in csvreader:
                if blockpit_transaction_id == 1:
                    end_date = row[0]
                start_date = row[0]
                current_ETH_reward = Decimal("".join(d for d in row[2] if d.isdigit() or d == '.'))
                current_EUR_reward = Decimal("".join(d for d in row[4] if d.isdigit() or d == '.'))
                average_ETH_price = average_ETH_price + Decimal("".join(d for d in row[3] if d.isdigit() or d == '.'))
                total_ETH_rewards = total_ETH_rewards + current_ETH_reward
                total_EUR_rewards = total_EUR_rewards + current_EUR_reward
                date_CSV = datetime.strptime(row[0], '%Y-%m-%d')
                date_CSV = date_CSV.replace(hour=22,minute=59,second=59)
                date_Blockpit_CSV = date_CSV.strftime("%d.%m.%Y %H:%M:%S")
                writerow = [blockpit_transaction_id,"exchange",depot_name,date_Blockpit_CSV,"ETH",current_ETH_reward,"","","ETH",0.0,"staking"]
                csvwriter.writerow(writerow)
                blockpit_transaction_id = blockpit_transaction_id + 1
            average_ETH_price =  average_ETH_price/(blockpit_transaction_id-1)
            print("---   CSV information   ---")
            print(f"\tHeader: {', '.join(headers)}")
            print(f"\tTime range: from {start_date} to {end_date}")
            print(f"\tNumber of entries: {blockpit_transaction_id-1}")          
            print(f"\tTotal ETH rewards: {total_ETH_rewards}")
            print(f"\tTotal rewards in EUR: {total_EUR_rewards}")
            print(f"\tAverage ETH price in EUR: {round(average_ETH_price, 2)}")
            print(f"\tDepot-name: {depot_name}")
            print("--- END CSV information ---")
            print("")
            print(f"Blockpit CSV written: {output_file}")
    return

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    input_file_name = parse_input_file_name(args.INPUT_FILE[0])
    if args.output_file is None or args.INPUT_FILE[0] == args.output_file[0]:
        output_file_name = input_file_name.rsplit('.',1)[0] + "_blockpit.csv"
    else:
        output_file_name = parse_output_file_name(args.output_file[0])
    print(f"Input file: {input_file_name}")
    print(f"Output file: {output_file_name}")
    if args.depot_name is None:
        depot_name = 'Validator'
    else:
        depot_name = args.depot_name[0]
    print(depot_name)
    CSV2Blockpit(input_file_name,output_file_name,depot_name)

main()

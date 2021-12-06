import argparse
import os
import csv
from re import I
import sys
from decimal import Decimal
import pylightxl as xl
import shutil
import datetime

from pylightxl.pylightxl import Database

XLSX_TABLE_NAME = "Tabelle1"

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s INPUT-FILE [OUTPUT-FILE]",
        description="Converts Beaconchain validator CSV rewards exports to Blockpit.io Excel file."
    )
    parser.add_argument('input_file', type=str, nargs=1,
                    help='CSV export file name from beaconcha.in')
    parser.add_argument("-o", "--output-file", type=str, nargs=1,
        help='Output file name (Excel) for Blockpit.io')
    parser.add_argument("-d", "--depot-name", type=str, nargs=1,
        help='Blockpit.io depot name', default='Validator')
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

def clearXLSX(db: Database) -> Database:
    for i in range(2, 18):
        for j in range(2,14):
            db.ws(ws='Tabelle1').update_index(row=i, col=j, val="")
    return db

def CSV2XLSX(input_file: str,output_file: str, depot_name: str) -> None:
    with open(input_file, newline='') as csvfile:
        shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)),'tpl','blockpit_xlsx_template.xlsx'),output_file)
        db = xl.readxl(output_file)
        db = clearXLSX(db)
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(csvreader, None)
        total_ETH_rewards = 0
        total_EUR_rewards = 0
        xlsx_transaction_id = 1
        average_ETH_price = 0
        for row in csvreader:
            if xlsx_transaction_id == 1:
                start_date = row[0]
            end_date = row[0]
            current_ETH_reward = Decimal("".join(d for d in row[2] if d.isdigit() or d == '.'))
            current_EUR_reward = Decimal("".join(d for d in row[4] if d.isdigit() or d == '.'))
            average_ETH_price = average_ETH_price + Decimal("".join(d for d in row[3] if d.isdigit() or d == '.'))
            total_ETH_rewards = total_ETH_rewards + current_ETH_reward
            total_EUR_rewards = total_EUR_rewards + current_EUR_reward
            date_CSV = datetime.datetime.strptime(row[0], '%Y-%m-%d')
            date_CSV = date_CSV.replace(hour=23,minute=59,second=59)
            date_XLSX = date_CSV.strftime("%d/%m/%Y %H:%M:%S")
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=1, val=xlsx_transaction_id)
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=3, val=depot_name)
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=4, val=date_XLSX)
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=5, val="ETH")
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=6, val=current_ETH_reward)
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=9, val="ETH")
            db.ws(ws=XLSX_TABLE_NAME).update_index(row=xlsx_transaction_id+1, col=11, val="masternode")
            xlsx_transaction_id = xlsx_transaction_id + 1
        xl.writexl(db=db, fn=output_file)
        average_ETH_price =  average_ETH_price/(xlsx_transaction_id-1)
        print("---   CSV information   ---")
        print(f"\tHeader: {', '.join(headers)}")
        print(f"\tTime range: from {start_date[-1]} to {end_date}")
        print(f"\tNumber of entries: {xlsx_transaction_id-1}")          
        print(f"\tTotal ETH rewards: {total_ETH_rewards}")
        print(f"\tTotal rewards in EUR: {total_EUR_rewards}")
        print(f"\tAverage ETH price: {average_ETH_price}")
        print(f"\tDepot-name: {depot_name}")
        print("--- END CSV information ---")
        print("")
        print("---   EXCEL information   ---")
        print(f"\tHeader: {', '.join(db.ws(ws='Tabelle1').row(row=1))}")
        print("--- END EXCEL information ---")
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
    CSV2XLSX(input_file_name,output_file_name,depot_name=args.depot_name)
main()
# validator-rewards-to-blockpit
This python script converts ETH validator rewards exported from beachoncha.in to a CSV file which can then be imported to blockpit.io

# Usage

## Export validator rewards from Beaconcha.in
Go to https://beaconcha.in/rewards. Select Validator and export CSV.

## Convert CSV files
Use the python script to convert the Beaconcha.in CSV to a Blockpit CSV.

Example: ```python rewex.py -d validator validator_2020.csv```

Takes a Beaconcha.in CSV named ```validator_2020.csv``` and converts it to a Blockpit CSV ```validator_2020_blockpit.csv```. The deposit name is defined by the argument ```-d <deposit name>```.

## Import Blockpit CSV in Blockpit
Go to https://app.blockpit.io/dashboard. Import Blockpit CSV.

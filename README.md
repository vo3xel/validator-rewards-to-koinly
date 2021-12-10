# rewex.py
This python script converts ETH validator rewards exported from beaconcha.in to a CSV file which can then be imported to blockpit.io

# Usage

## Export validator rewards from Beaconcha.in
Go to https://beaconcha.in/rewards. Select Validator and export CSV.

https://user-images.githubusercontent.com/19472607/144933555-8f4fd91d-b96f-4517-ad37-d4f1ebe8b94a.mp4

## Convert CSV files
Use the python script to convert the Beaconcha.in CSV to a Blockpit CSV.

Example: ```python rewex.py -d Validator validator_dez_2021.csv```

Takes a Beaconcha.in CSV named ```validator_dez_2021.csv``` and converts it to a Blockpit CSV ```validator_dez_2021_blockpit.csv```. The deposit name is defined by the argument ```-d <deposit name>```.

## Import Blockpit CSV in Blockpit
Go to https://app.blockpit.io/dashboard. Import Blockpit CSV.

https://user-images.githubusercontent.com/19472607/144933580-8c98031c-cac6-41f5-a83b-7027c1aa510d.mp4

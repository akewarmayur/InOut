import argparse
from Investing.processInDB import ProcessIn
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    my_parser.add_argument('--first', action='store', type=str, required=True)
    args = my_parser.parse_args()
    # machine_name = 'Index'
    machine_name = args.machine_name
    first = args.first
    obj = ProcessIn()
    obj.start(machine_name, first)
    # python mainInvestDB.py --machine_name Index --first TRUE


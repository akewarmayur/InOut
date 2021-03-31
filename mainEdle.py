import argparse
from Edelweiss.processEd import ProcessEd

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    args = my_parser.parse_args()
    obj = ProcessEd()
    print('Machine Name:', args.machine_name)
    obj.start(args.machine_name)
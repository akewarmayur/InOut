import argparse
from Investing.processIn import ProcessIn
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    args = my_parser.parse_args()
    obj = ProcessIn()
    obj.start(args)


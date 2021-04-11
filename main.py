import argparse
from Edelweiss.processEd import ProcessEd

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    args = my_parser.parse_args()
    obj = ProcessEd()
    print('Machine Name:', args.machine_name)
    obj.start(args.machine_name)


    def start(self, q, result, isMarketON, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
        while not q.empty():
            work = q.get()
            print(work)  # fetch new work from the Queue
            try:
                # time.sleep(5)
                iterations = 0
                while True:
                    process(work[1], expiry_date_stocks)
                    if iterations == 5:
                        break
                # result[work[0]] = data          #Store data back at correct index
            except:
                result[work[0]] = {}
            # signal to the queue that task has been processed
            q.task_done()
        return True
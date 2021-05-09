import argparse
from Investing.processInDB import ProcessIn
import logging
from threading import Thread
from queue import Queue
import time
import warnings
import config
import pandas as pd
warnings.filterwarnings("ignore")
import os


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    args = my_parser.parse_args()
    #machine_name = 'A'
    machine_name = args.machine_name
    objPIn = ProcessIn()
    print("Machine Name : ", machine_name)
    URL = objPIn.get_url()
    if URL == 'None':
        URL = objPIn.get_url()
    content = objPIn.objSheet.readSheet('CIEconfig', 'InvestingConfig')
    no_of_days = content['Days']
    resolutions_list = content['Configuration']
    isMarketON = content['MarketON']
    isMarketON = isMarketON[0]
    # print('To be Scrapped: ', str(resolutions_list))
    # print('No of days: ', str(no_of_days))

    content = objPIn.objSheet.readSheet('CIEconfig', 'InvestingStocks', machine_name)
    content = content['Pid']
    content = content.values.tolist()
    pid = [row for row in content if row != '']
    print(pid)


    # machine_name = args.machine_name
    # config.env = args.env
    # config.sessionRestart = args.sesRestart
    q = Queue(maxsize=0)
    # Use many threads (50 max, or one for each url)

    num_theads = len(pid)
    # Populating Queue with tasks
    results = [{} for x in pid]
    # load up the queue with the urls to fetch and the index for each job (as a tuple):
    for i in range(len(pid)):
        # need the index and the url in each queue item.
        q.put((i, pid[i]))


    for i in range(num_theads):
        logging.debug('Starting thread ', i)
        worker = Thread(target=objPIn.start, args=(q, results, URL, resolutions_list, no_of_days, isMarketON))
        worker.setDaemon(True)  # setting threads as "daemon" allows main program to
        # exit eventually even if these dont finish
        # correctly.
        worker.start()
        time.sleep(7)
    # now we wait until the queue has been processed
    q.join()
    logging.info('All tasks completed.')


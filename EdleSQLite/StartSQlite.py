from Edel.HelpersSQLite import HelpEdDB
import argparse
from Edel.ScrapDataSQLite import ScrapData
from Edel.ProcessSQLite import ProcessEd
from Help.DBOperationsSQLite import DatabaseOp
import warnings
import config
import pandas as pd
from Edel.gAPISQLite import GoogleAPI
import logging
from threading import Thread
from queue import Queue
warnings.filterwarnings("ignore")
import os

class MainEdle:

    def __init__(self):
        self.objHelpDB = HelpEdDB()
        self.objScrap = ScrapData()
        self.objDBOP = DatabaseOp()

    def get_expiry_dates(self):
        try:
            expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = self.objScrap.get_expiry_dates()
            return expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly
        except Exception as e:
            print('Exception in getting expiry dates:', e)

    def get_symbol_list(self):
        try:
            EDStocks, EDIndicesM, EDIndicesW = self.get_expiry_dates()
            print(EDStocks, EDIndicesM, EDIndicesW)
            return EDStocks, EDIndicesM, EDIndicesW
        except Exception as e:
            print('Exception in getting Symbol list:', e)




if __name__ == '__main__':
    # my_parser = argparse.ArgumentParser()
    # # jiten,
    # my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    # my_parser.add_argument('--env', action='store', type=str, required=True)
    # my_parser.add_argument('--sesRestart', action='store', type=str, required=True)
    # args = my_parser.parse_args()
    q = Queue(maxsize=0)
    sy_list = ['stocks', 'UPLOAD_THREAD']
    num_theads = len(sy_list)
    # Populating Queue with tasks
    results = [{} for x in sy_list]
    # load up the queue with the urls to fetch and the index for each job (as a tuple):
    for i in range(len(sy_list)):
        # need the index and the url in each queue item.
        q.put((i, sy_list[i]))

    objGAPI = GoogleAPI()
    objpEd = ProcessEd()
    objMain = MainEdle()
    config.DB_Name = 'sqliteDB.db'
    EDStocks, EDIndicesM, EDIndicesW = objMain.get_symbol_list()
    # status = objMain.objHelpDB.create_tables(EDStocks, EDIndicesM, EDIndicesW)
    service = objGAPI.intiate_gdAPI()
    status = objMain.objDBOP.downloadDB(service, EDStocks, EDIndicesM, EDIndicesW)
    df = pd.read_csv('stocks.csv')
    symbol_list = df['Symbol'].unique().tolist()
    print(symbol_list)
    conn = objMain.objDBOP.create_connection()
    print("Connection started====")
    import time
    # for i in range(num_theads):
    #     worker = Thread(target=objpEd.start, args=(q, results, symbol_list, EDStocks, EDIndicesW, conn))
    #     worker.setDaemon(True)  # setting threads as "daemon" allows main program to
    #     # exit eventually even if these dont finish
    #     # correctly.
    #     worker.start()
    #     time.sleep(1)
    #     # now we wait until the queue has been processed
    # q.join()
    objpEd.start(symbol_list, EDStocks, EDIndicesW, conn)







    # status = objpEd.start(symbol_list, EDStocks, EDIndicesW, conn)
    # conn.close()


# obj = MainEdle()
# obj.get_symbol_list()
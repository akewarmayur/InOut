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
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--MarketON', action='store', type=str, required=True)
    args = my_parser.parse_args()

    MarketFlag = args.MarketON


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

    objpEd.start(symbol_list, EDStocks, EDIndicesW, conn, MarketFlag)







    # status = objpEd.start(symbol_list, EDStocks, EDIndicesW, conn)
    # conn.close()


# obj = MainEdle()
# obj.get_symbol_list()
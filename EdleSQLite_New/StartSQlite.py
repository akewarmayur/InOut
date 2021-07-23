from Edel.HelpersSQLite import HelpEdDB
import argparse
from Edel.ScrapDataSQLite import ScrapData
from Edel.ProcessSQLite import ProcessEd
from Help.DBOperationsSQLite import DatabaseOp
from common.sheetOperations import SheetOps
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
        self.objSheet = SheetOps()

    def get_expiry_dates(self):
        try:
            expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = self.objScrap.get_expiry_dates()
            return expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly
        except Exception as e:
            print('Exception in getting expiry dates:', e)



    def get_symbol_list_from_drive(self, machine_name):
        try:
            content = self.objSheet.readSheet('CIEconfig', 'EdelStocks', machine_name)
            df = content[(content.MachineName == machine_name) & (content.Stocks == 'TRUE')]
            ## check Market status
            checkMarketStatus = self.objSheet.readSheet('CIEconfig', 'EdelConfig')
            isMarketON = self.objSheet.readSheetColumns(checkMarketStatus, 'MarketON')
            isMarketON = isMarketON[0]
            return isMarketON, df

        except Exception as e:
            print('Exception in getting Symbol list:', e)

    # def get_symbol_list(self):
    #     try:
    #         EDStocks, EDIndicesM, EDIndicesW = self.get_expiry_dates()
    #         print(EDStocks, EDIndicesM, EDIndicesW)
    #         return EDStocks, EDIndicesM, EDIndicesW
    #     except Exception as e:
    #         print('Exception in getting Symbol list:', e)




if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--MarketON', action='store', type=str, required=True)
    my_parser.add_argument('--MachineName', action='store', type=str, required=True)
    # python StartSQlite.py --MarketON True --MachineName U001
    args = my_parser.parse_args()
    MarketFlag = args.MarketON
    McName = args.MachineName

    objGAPI = GoogleAPI()
    objpEd = ProcessEd()
    objMain = MainEdle()
    config.DB_Name = 'sqliteDB.db'
    #EDStocks, EDIndicesM, EDIndicesW = objMain.get_symbol_list()
    # status = objMain.objHelpDB.create_tables(EDStocks, EDIndicesM, EDIndicesW)
    # service = objGAPI.intiate_gdAPI()
    # status = objMain.objDBOP.downloadDB(service, EDStocks, EDIndicesM, EDIndicesW)
    ####### Reading data from drive
    isMarketON, df = objMain.get_symbol_list_from_drive(McName)
    #status = self.process(symbol, EDStocks, EDIndicesW, conn)
    #conn = objMain.objDBOP.create_connection()
    print("Execution started====")
    objpEd.start(df,MarketFlag)







    # status = objpEd.start(symbol_list, EDStocks, EDIndicesW, conn)
    # conn.close()


# obj = MainEdle()
# obj.get_symbol_list()
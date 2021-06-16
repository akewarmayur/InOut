from Edelweiss.helpEdDB import HelpEdDB
import argparse
from Edelweiss.scrapEdDB import ScrapData
from common.gAPI import GoogleAPI
from common.common import CommonFunctions
from Edelweiss.pEDDB import ProcessEd
import logging
from threading import Thread
from queue import Queue
from common.sheetOperations import SheetOps
from common.DBOperations import DatabaseOp
import time
import warnings
import config
import pandas as pd
from sqlalchemy import create_engine
warnings.filterwarnings("ignore")
import os

class MainEdle:

    def __init__(self):
        self.objHelpDB = HelpEdDB()
        self.objSheet = SheetOps()
        self.objScrap = ScrapData()
        self.objGAPI = GoogleAPI()
        self.objDBOP = DatabaseOp()
        self.objCommon = CommonFunctions()

    def get_expiry_dates(self):
        try:
            expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = self.objScrap.get_expiry_dates()
            return expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly
        except Exception as e:
            print('Exception in getting expiry dates:', e)

    def get_symbol_list(self, machine_name):
        try:
            diction = {}
            Ndiction = {}
            content = self.objSheet.readSheet('CIEconfig', 'EdelStocks', machine_name)
            symbol = self.objSheet.readSheetColumns(content, 'Symbol')
            indices_or_stocks = self.objSheet.readSheetColumns(content, 'Stocks')

            content = self.objSheet.readSheet('CIEconfig', 'EdelConfig')
            isMarketON = self.objSheet.readSheetColumns(content, 'MarketON')
            isMarketON = isMarketON[0]

            EDStocks, EDIndicesM, EDIndicesW = self.get_expiry_dates()

            for i, s in enumerate(symbol):
                if indices_or_stocks[i] == 'TRUE':
                    Ndiction[s] = indices_or_stocks[i]
                    if len(EDStocks) != 0:
                        for j in EDStocks:
                            name = j + '_' + s
                            diction[name] = indices_or_stocks[i]
                if indices_or_stocks[i] == 'FALSE':
                    Ndiction[s] = indices_or_stocks[i]
                    if len(EDIndicesM) != 0:
                        count = 0
                        for a in EDIndicesM:
                            name = str(count) + '_' + a + '_' + s
                            diction[name] = indices_or_stocks[i]
                            count += 1
                    if len(EDIndicesW) != 0:
                        for b in EDIndicesW:
                            name = str(count) + '_' + b + '_' + s
                            diction[name] = indices_or_stocks[i]
                            count += 1

            symbol_list = []
            for key, value in diction.items():
                symbol_list.append(key)

            return isMarketON, symbol_list, diction, EDStocks, EDIndicesM, EDIndicesW, Ndiction
        except Exception as e:
            print('Exception in getting Symbol list:', e)

    def create_folders(self, service, EDStocks, EDIndicesM, EDIndicesW):
        FolderIDs = {}
        print('Creating Folders .....')
        if config.env == 'QA':
            fo_id = '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA'
        else:
            fo_id = '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA'
        try:
            for dt in EDStocks:
                folderID = self.objGAPI.search_file(service, str(dt), '', fo_id, True)
                if folderID == 0:
                    folderID = self.objGAPI.createFolder(service, str(dt), fo_id)
                    FolderIDs[dt] = folderID
                else:
                    FolderIDs[dt] = folderID
            for dt in EDIndicesM:
                folderID = self.objGAPI.search_file(service, str(dt), '', fo_id, True)
                if folderID == 0:
                    folderID = self.objGAPI.createFolder(service, str(dt), fo_id)
                    FolderIDs[dt] = folderID
                else:
                    FolderIDs[dt] = folderID
            for dt in EDIndicesW:
                folderID = self.objGAPI.search_file(service, str(dt), '', fo_id, True)
                if folderID == 0:
                    folderID = self.objGAPI.createFolder(service, str(dt), fo_id)
                    FolderIDs[dt] = folderID
                else:
                    FolderIDs[dt] = folderID
            return FolderIDs
        except Exception as e:
            print('Exception in creating folder:', e)
            return FolderIDs



if __name__ == '__main__':
    # my_parser = argparse.ArgumentParser()
    # # jiten,
    # my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    # my_parser.add_argument('--env', action='store', type=str, required=True)
    # my_parser.add_argument('--sesRestart', action='store', type=str, required=True)
    # args = my_parser.parse_args()
    objpEd = ProcessEd()
    objMain = MainEdle()

    ### manual run
    # config.env = 'QA'
    machine_name = 'Index'
    config.sessionRestart = 'no'
    config.machine_name = machine_name
    config.DB_Name = machine_name + '.db'
    # config.DB_Name = config.DB_Name.replace('.', '')
    #############
    ## COmmand line
    config.env = 'QA'
    config.sessionRestart = 'no'
    #machine_name = 'Index'
    #machine_name = args.machine_name
    config.machine_name = 'Index'
    config.DB_Name = 'index.db'
    config.DB_Name = config.DB_Name.replace('.', '')
    # x = list(config.DB_Name)
    # alllst=[]
    # for row in x:
    #     if "'" in row or "." in row:
    #         continue
    #     else:
    #         alllst.append(row)
    # config.DB_Name = ''.join(alllst)

    ##########################
    ###
    #service = objMain.objGAPI.intiate_gdAPI()
    q = Queue(maxsize=0)
    # Use many threads (50 max, or one for each url)
    isMarketON, symbol_list, diction, EDStocks, EDIndicesM, EDIndicesW, Ndiction = objMain.get_symbol_list(machine_name)
    # symbol_list = ['24 Jun 2021_ACC']
    # Ndiction = {'ACC': 'TRUE'}
    #
    # diction = {'24 Jun 2021_ACC': 'TRUE'}
    # print(symbol_list)
    # print(diction)

    #FolderIDs = objMain.create_folders(service, EDStocks, EDIndicesM, EDIndicesW)
    status = objMain.objHelpDB.create_tables(EDStocks, EDIndicesM, EDIndicesW)
    #objMain.objHelpDB.downLoadAllCSV(service, Ndiction, EDStocks, EDIndicesM, EDIndicesW, config.sessionRestart)
    #status = True
    #symbol_list = symbol_list[:1]
    # symbol_list.append('UPLOAD_THREAD')
    # b['UPLOAD_THREAD'] = 'UPLOAD_DB'
    #symbol_list = symbol_list[0:3]
    print(symbol_list)

    # Insert Thresholds from CSV
    dfThreshold = pd.read_csv(os.getcwd() + '/thresholds.csv')
    conn = objMain.objDBOP.connect2Mysql() # MYSQL
    #objMain.objDBOP.create_mysql_database(config.DB_Name)  # SQLIte

    objMain.objDBOP.create_tableThreshold(conn)
    time.sleep(1)
    for i, row in dfThreshold.iterrows():
        Threshold = row['Threshold']
        ScripName = row['ScripName']
        EXD = row['ExpiryDate']
        objMain.objHelpDB.InsertThreshold(conn, ScripName, EXD, Threshold)
    conn.close()
    print("Closing connection 2")
    #print(symbol_list)
    #print("sytaus true===")
    conn = objMain.objDBOP.connect2Mysql()
    print("Connection started====")
    objpEd.start(symbol_list, isMarketON, diction, conn)  # FolderIDs,
    conn.close()


    #if status == True:
    #     num_theads = len(symbol_list)
    #     # Populating Queue with tasks
    #     results = [{} for x in symbol_list]
    #     # load up the queue with the urls to fetch and the index for each job (as a tuple):
    #     for i in range(len(symbol_list)):
    #         # need the index and the url in each queue item.
    #         q.put((i, symbol_list[i]))

        # que = "select * from stockdetails_24_jun_2021 where ScripName='AARTIIND' order by TradeDateTime DESC LIMIT 5"
        # cur = conn.cursor()
        # cur.execute(que)
        # ows = cur.fetchall()
        # print(ows)
        # engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
        #                        .format(user="root",
        #                                pw="InOut@909",
        #                                db="indexdb"))
        #conn.close()
        # for i in range(num_theads):
            #logging.debug('Starting thread ', i)
            # time.sleep(2)
            # if conn.is_connected()==False:
            #     conn.close()
            #     print("closing connection ===========")
            #     conn = objMain.objDBOP.connect2Mysql()
            #     print("connection Started ===========")
            # c = "conn"+str(i)
            # c = objMain.objDBOP.connect2Mysql()  # MYSQL
            # conn = c
            # print("=====================================",conn)
            # worker = Thread(target=objpEd.start, args=(q, results, isMarketON, diction, conn))#  FolderIDs,
            # worker.setDaemon(True)  # setting threads as "daemon" allows main program to
            # exit eventually even if these dont finish
            # correctly.
            # worker.start()
            # time.sleep(1)

        # now we wait until the queue has been processed

        # q.join()
        # conn.close()
    #     logging.info('All tasks completed.')
    # else:
    #     print('Check Program for errors')

    #Upload DB file at the end of the day
    # file_id = objMain.objGAPI.search_file(service, config.DB_Name, 'mime_type', '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', True)
    # if file_id != 0:
    #     objMain.objGAPI.delete_file(service, file_id)
    # objMain.objGAPI.upload_file(service, config.DB_Name, os.getcwd() + '/DB/' + config.DB_Name, '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', 'application/vnd.sqlite3')


# obj = MainEdle()

# obj.objHelpDB.get_sd_from_prev_day('ZEEL', 'stockDetails')
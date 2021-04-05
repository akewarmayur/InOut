import argparse
from common.gAPI import GoogleAPI
from Edelweiss.pEd import ProcessEd
import logging
from threading import Thread
from queue import Queue
from common.sheetOperations import SheetOps
from Edelweiss.scrapEd import ScrapData
import time
import warnings
warnings.filterwarnings("ignore")

class EdleMain:
    def __init__(self):
        self.objSheet = SheetOps()
        self.objScrap = ScrapData()
        self.objGAPI = GoogleAPI()

    def get_expiry_dates(self):
        try:
            expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = self.objScrap.get_expiry_dates()
            return expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly
        except Exception as e:
            print('Exception in getting expiry dates:', e)

    def get_symbol_list(self, machine_name):
        try:
            diction = {}
            content = self.objSheet.readSheet('CIEconfig', 'EdelStocks', machine_name)
            symbol = self.objSheet.readSheetColumns(content, 'Symbol')
            indices_or_stocks = self.objSheet.readSheetColumns(content, 'Stocks')

            content = self.objSheet.readSheet('CIEconfig', 'EdelConfig')
            isMarketON = self.objSheet.readSheetColumns(content, 'MarketON')
            isMarketON = isMarketON[0]

            for i, s in enumerate(symbol):
                diction[s] = indices_or_stocks[i]

            return isMarketON, symbol, diction
        except Exception as e:
            print('Exception in getting Symbol list:', e)

    def create_folders(self, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
        print('Creating Folders .....')
        try:
            for dt in expiry_date_stocks:
                service = self.objGAPI.intiate_gdAPI()
                folderID = self.objGAPI.search_file(service, str(dt), '', '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA', True)
                if folderID == 0:
                    folderID = self.objGAPI.createFolder(service, str(dt), '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
            for dt in expiry_date_indices_monthly:
                service = self.objGAPI.intiate_gdAPI()
                folderID = self.objGAPI.search_file(service, str(dt), '', '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA', True)
                if folderID == 0:
                    folderID = self.objGAPI.createFolder(service, str(dt), '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
            for dt in expiry_date_indices_weekly:
                service = self.objGAPI.intiate_gdAPI()
                folderID = self.objGAPI.search_file(service, str(dt), '', '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA', True)
                if folderID == 0:
                    folderID = self.objGAPI.createFolder(service, str(dt), '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
        except Exception as e:
            print('Exception in creating folder:', e)

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--machine_name', action='store', type=str, required=True)
    args = my_parser.parse_args()
    objpEd = ProcessEd()
    objMain = EdleMain()
    machine_name = args.machine_name
    #machine_name = 'Mayur'

    q = Queue(maxsize=0)
    # Use many threads (50 max, or one for each url)
    isMarketON, symbol, diction = objMain.get_symbol_list(machine_name)
    expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = objMain.get_expiry_dates()
    objMain.create_folders(expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly)

    # symbol = symbol[:1]
    print(symbol)

    num_theads = len(symbol)

    # Populating Queue with tasks
    results = [{} for x in symbol]
    # load up the queue with the urls to fetch and the index for each job (as a tuple):
    for i in range(len(symbol)):
        # need the index and the url in each queue item.
        q.put((i, symbol[i]))


    for i in range(num_theads):
        logging.debug('Starting thread ', i)
        worker = Thread(target=objpEd.start, args=(q, results, isMarketON, diction, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly))
        worker.setDaemon(True)  # setting threads as "daemon" allows main program to
        # exit eventually even if these dont finish
        # correctly.
        worker.start()
        time.sleep(1.2)
    # now we wait until the queue has been processed
    q.join()
    logging.info('All tasks completed.')
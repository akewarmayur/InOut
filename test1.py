from common.gAPI import GoogleAPI
import pandas as pd
from Edelweiss.scrapEd import ScrapData
from common.common import CommonFunctions
from common.sheetOperations import SheetOps
import time
import Edelweiss.edleConfig as edleConfig
import os
from pytz import timezone
import datetime
import logging
from threading import Thread
from queue import Queue



objGAPI = GoogleAPI()
objScrap = ScrapData()
objCommon = CommonFunctions()
objSheet = SheetOps()
fixed_columns = ['ScripName', 'StrikePrice', 'OptionType',
                      'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                      'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL']
first = True
iterations = 0


strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
diction = {}
content = objSheet.readSheet('CIEconfig', 'EdelStocks', 'Mayur')
symbol = objSheet.readSheetColumns(content, 'Symbol')
indices_or_stocks = objSheet.readSheetColumns(content, 'Stocks')



symbol = symbol[:3]
print(symbol)
q = Queue(maxsize=0)
# Use many threads (50 max, or one for each url)
num_theads = len(symbol)

#Populating Queue with tasks
results = [{} for x in symbol]
#load up the queue with the urls to fetch and the index for each job (as a tuple):
for i in range(len(symbol)):
    #need the index and the url in each queue item.
    q.put((i,symbol[i]))

expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = objScrap.get_expiry_dates()


def save_to_drive(folder_id, name_of_file, destination):
    try:
        # name_of_file = destination.split('/')[1]
        service = objGAPI.intiate_gdAPI()
        # Search file id to check it is exists or not
        # def search_file(service, file_name, mime_type, folder_id, search_in_folder=False):
        file_id = objGAPI.search_file(service, str(name_of_file), 'text/csv', folder_id, True)
        if type(file_id) is int:
            objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
        if type(file_id) is str:
            objGAPI.delete_file(service, file_id)
            time.sleep(1)
            objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
        return True
    except Exception as e:
        print('Exception while saving files on drive', e)
        return False

def concate(previous_df, df_now):
    try:
        previous_df = objCommon.drop_extra_columns(previous_df, fixed_columns)
        df_now = objCommon.drop_extra_columns(df_now, fixed_columns)
        final = df_now.append(previous_df, ignore_index=True)
        final.reset_index(inplace=True)
    except Exception as e:
        print('concat exception: ', e)

    return final

def process(symbol, expiry_date):
    for dt in expiry_date:
        print('Scrapping for : ', dt)
        service = objGAPI.intiate_gdAPI()
        folderID = objGAPI.search_file(service, str(dt), '', '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA', True)
        if folderID == 0:
            folderID = objGAPI.createFolder(service, str(dt), '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
        # Scrap Data
        file = objScrap.start_scraping(str(symbol), dt)
        name_of_file = file.split('csv/')[1]
        # Upload to drive
        # Check if data historical data is available on the drive
        isDataAvailable, file_id = objCommon.check_previous_data_exist(file, folderID)
        if isDataAvailable == False:
            save_to_drive(folderID, name_of_file, file)
        else:
            df_now = pd.read_csv(os.getcwd() + '/Edelweiss/csv/' + name_of_file, index_col=0)
            if first == True:
                # Download file
                file_to_save = os.getcwd() + '/Edelweiss/d_csv/' + name_of_file
                objGAPI.download_files(service, file_to_save, file_id, False)
            previous_df = pd.read_csv(os.getcwd() + '/Edelweiss/d_csv/' + name_of_file, index_col=0)

            # Go for outliers or not
            # if len(previous_df['StrTradeDateTime'].unique().tolist()) >= edleConfig.no_of_past_instruments:
                # Notify Outliers if any
                # get_outliers(symbol, df_now, previous_df, dt)

            result = concate(previous_df, df_now)
            result.to_csv(os.getcwd() + '/Edelweiss/sample_data/' + name_of_file, index=False)
            if iterations == 10:
                save_to_drive(folderID, name_of_file, os.getcwd() + '/Edelweiss/sample_data/' + name_of_file)

def start(q, result):
    while not q.empty():
        work = q.get()
        print(work)#fetch new work from the Queue
        try:
            # time.sleep(5)
            iterations = 0
            while True:
                process(work[1], expiry_date_stocks)
                logging.info("Requested..." + work[1])
                if iterations == 5:
                    break
            # result[work[0]] = data          #Store data back at correct index
        except:
            logging.error('Error with URL check!')
            result[work[0]] = {}
        #signal to the queue that task has been processed
        q.task_done()
    return True


for i in range(num_theads):
    logging.debug('Starting thread ', i)
    worker = Thread(target=start, args=(q,results))
    worker.setDaemon(True)    #setting threads as "daemon" allows main program to
                              #exit eventually even if these dont finish
                              #correctly.
    worker.start()
    time.sleep(1)
#now we wait until the queue has been processed
print(datetime.datetime.now())
q.join()
print(datetime.datetime.now())
logging.info('All tasks completed.')



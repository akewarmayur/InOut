from common.gAPI import GoogleAPI
import pandas as pd
from Edelweiss.scrapEdDB import ScrapData
from common.common import CommonFunctions
from Edelweiss.helpEd import HelpEd
from Edelweiss.helpEdDB import HelpEdDB
import time
import os
from pytz import timezone
import datetime
import threading
import Edelweiss.edleConfig as edleConfig
import config
import warnings
warnings.filterwarnings("ignore")


class ProcessEd(threading.Thread):

    def concate(self, df_now, previous_df):
        objCommon = CommonFunctions()
        fixed_columns = ['ID', 'scripName', 'IndexORStocks', 'strikePrice', 'optionType', 'strcurrentDateTime',
                       'currentDateTime', 'ExpiryDate', 'OI', 'COI', 'IV', 'VOL', 'ChangeCOI', 'Flag', 'CreatedAT']
        try:
            previous_df = objCommon.drop_extra_columns(previous_df, fixed_columns)
            df_now = objCommon.drop_extra_columns(df_now, fixed_columns)
            final = df_now.append(previous_df)
            #final.reset_index(inplace=True)
        except Exception as e:
            print('concat exception: ', e)

        return final

    def save_to_drive(self, folder_id, name_of_file, destination):
        objGAPI = GoogleAPI()
        try:
            service = objGAPI.intiate_gdAPI()
            # Search file id to check it is exists or not
            # def search_file(service, file_name, mime_type, folder_id, search_in_folder=False):
            file_id = objGAPI.search_file(service, str(name_of_file), 'text/csv', folder_id, True)
            if type(file_id) is int:
                objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
            if type(file_id) is str:
                objGAPI.delete_file(service, file_id)
                # time.sleep(1)
                objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
            return True
        except Exception as e:
            print('Exception while saving files on drive', e)
            return False


    def process(self, symbol, table_name, expiry_date, iterations, folder_id):
        objGAPI = GoogleAPI()
        objScrap = ScrapData()
        objCommon = CommonFunctions()
        try:
            exd = expiry_date.replace(' ', '_')
            file_name = symbol + '_' + exd + '.csv'
            status = objScrap.start_scraping(str(symbol), expiry_date)
            if iterations == 30:
                objHDB = HelpEdDB()
                if status == True:
                    current_df, st = objHDB.DB2CSV(symbol, table_name)
                    if os.path.exists(os.getcwd() + '/Edelweiss/d_csv/' + file_name):
                        previous_df = pd.read_csv(os.getcwd() + '/Edelweiss/d_csv/' + file_name, index_col=0)
                        result_df = self.concate(current_df, previous_df)
                    else:
                        result_df = current_df

                    destination = os.getcwd() + '/Edelweiss/sample_data/' + file_name

                    result_df.to_csv(os.getcwd() + '/Edelweiss/sample_data/' + file_name, index=False)
                    service = objGAPI.intiate_gdAPI()
                    isDataAvailable, file_id = objCommon.check_pdata_exist(file_name, folder_id)
                    if isDataAvailable == True:
                        objGAPI.delete_file(service, file_id)
                    objGAPI.upload_file(service, str(file_name), destination, folder_id, 'text/csv')
                else:
                    print(f"Scrapping df empty for : {symbol}")
                    return False
            return True
        except Exception as e:
            print('Exception in Edle Scrapping Process:', e)
            return False

    def start(self, q, result, isMarketON, FolderIDs, diction):
        while not q.empty():
            work = q.get()
            try:
                if isMarketON == 'TRUE':
                    ns = threading.local()
                    ns.iterations = 0
                    while True:
                        print('******************* Iterations : ', ns.iterations)
                        strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                        strcurrentTime = strcurrentTime.replace(':', '.')
                        if float(strcurrentTime) > float(19.30):
                            print('Market is not ON. Try tomorrow or change isMarketON flag')
                            break
                        ScrapedFor = work[1]
                        if diction[ScrapedFor] == 'FALSE':
                            ScrapedFor = ScrapedFor.split('_')
                            expDate = ScrapedFor[1]
                            symbol = ScrapedFor[2]
                            folder_ID = FolderIDs[expDate]
                            exd = expDate.replace(' ', '_')
                            table_name = config.TableName + exd
                            status = self.process(symbol, table_name, expDate, ns.iterations, folder_ID)
                        else:
                            ScrapedFor = ScrapedFor.split('_')
                            expDate = ScrapedFor[0]
                            symbol = ScrapedFor[1]
                            folder_ID = FolderIDs[expDate]
                            exd = expDate.replace(' ', '_')
                            table_name = config.TableName + exd
                            status = self.process(symbol, table_name, expDate, ns.iterations, folder_ID)
                        if status == True:
                            ns.iterations += 1
                        if ns.iterations == 31:
                            ns.iterations = 0

                else:
                    it = 0
                    strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strcurrentTime = strcurrentTime.replace(':', '.')
                    if float(strcurrentTime) > float(15.30):
                        print('Market is not ON. Try tomorrow or change isMarketON flag')
                        break
                    ScrapedFor = work[1]
                    if diction[ScrapedFor] == 'FALSE':
                        ScrapedFor = ScrapedFor.split('_')
                        expDate = ScrapedFor[1]
                        symbol = ScrapedFor[2]
                        folder_ID = FolderIDs[expDate]
                        exd = expDate.replace(' ', '_')
                        table_name = config.TableName + exd
                        status = self.process(symbol, table_name, expDate, it, folder_ID)
                    else:
                        ScrapedFor = ScrapedFor.split('_')
                        expDate = ScrapedFor[0]
                        symbol = ScrapedFor[1]
                        folder_ID = FolderIDs[expDate]
                        exd = expDate.replace(' ', '_')
                        table_name = config.TableName + exd
                        status = self.process(symbol, table_name, expDate, it, folder_ID)

            except:
                result[work[0]] = {}
            # signal to the queue that task has been processed
            q.task_done()
        return True


#
# obj = ProcessEd()
# name_of_file = 'NIFTY_29_Apr_2021.csv'
# previous_df = pd.read_csv(os.getcwd() + '/d_csv/' + name_of_file, index_col=0)
# print(previous_df.head(1))
# df_now = pd.read_csv(os.getcwd() + '/csv/' + name_of_file, index_col=0)
# print(df_now.head(1))
# d = obj.concate(previous_df, df_now)
# print(d.head())
# print(d.tail())
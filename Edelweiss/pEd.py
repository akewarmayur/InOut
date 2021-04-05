from common.gAPI import GoogleAPI
import pandas as pd
from Edelweiss.scrapEd import ScrapData
from common.common import CommonFunctions
from Edelweiss.helpEd import HelpEd
import time
import os
from pytz import timezone
import datetime
import threading
import Edelweiss.edleConfig as edleConfig
import warnings
warnings.filterwarnings("ignore")


class ProcessEd(threading.Thread):
    # def __init__(self):
    #     self.objGAPI = GoogleAPI()
    #     self.objScrap = ScrapData()
    #     self.objCommon = CommonFunctions()
    #     self.objSheet = SheetOps()
    #     self.fixed_columns = ['ScripName', 'StrikePrice', 'OptionType',
    #                           'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
    #                           'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL']
    #     self.it = 0
    #     self.objHelpEd = HelpEd()


    def concate(self, previous_df, df_now):
        objCommon = CommonFunctions()
        fixed_columns = ['ScripName', 'StrikePrice', 'OptionType',
                                  'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                                  'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL']
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

    def process(self, symbol, expiry_date, iterations):
        objGAPI = GoogleAPI()
        objScrap = ScrapData()
        objCommon = CommonFunctions()
        objHelpEd = HelpEd()
        try:
            for dt in expiry_date:
                # print('Scrapping for : ', dt)
                service = objGAPI.intiate_gdAPI()
                folderID = objGAPI.search_file(service, str(dt), '', '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA', True)

                file = objScrap.start_scraping(str(symbol), dt)
                name_of_file = file.split('csv/')[1]
                # Upload to drive
                # Check if data historical data is available on the drive
                isDataAvailable, file_id = objCommon.check_previous_data_exist(file, folderID)
                if isDataAvailable == False:
                    self.save_to_drive(folderID, name_of_file, file)
                else:
                    df_now = pd.read_csv(os.getcwd() + '/Edelweiss/csv/' + name_of_file)
                    current_time = list(df_now['StrTradeDateTime'].unique())[0]
                    if iterations < 2:
                        # Download file
                        file_to_save = os.getcwd() + '/Edelweiss/d_csv/' + name_of_file
                        objGAPI.download_files(service, file_to_save, file_id, False)
                        previous_df = pd.read_csv(os.getcwd() + '/Edelweiss/d_csv/' + name_of_file)
                    else:
                        previous_df = pd.read_csv(os.getcwd() + '/Edelweiss/sample_data/' + name_of_file)

                    # Notify Outliers if any
                    past_time = list(previous_df['StrTradeDateTime'].unique())

                    if len(past_time) < edleConfig.no_of_past_instruments:
                        result_df = self.concate(previous_df, df_now)
                    else:
                        # objHelpEd.outliers_notify(result_df, symbol, dt)
                        result_df = objHelpEd.outliers_notify(df_now, previous_df, current_time, symbol, dt)
                    result_df.to_csv(os.getcwd() + '/Edelweiss/sample_data/' + name_of_file, index=False)
                    if iterations < 2 or iterations == 5:
                        self.save_to_drive(folderID, name_of_file, os.getcwd() + '/Edelweiss/sample_data/' + name_of_file)
        except Exception as e:
            print('Exception in Edle Scrapping Process:', e)

    def start(self, q, result, isMarketON, diction, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
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
                        if float(strcurrentTime) > float(15.35):
                            print('Market is not ON. Try tomorrow or change isMarketON flag')
                            break
                        if diction[work[1]] == 'FALSE':
                            self.process(work[1], expiry_date_indices_monthly, ns.iterations)
                            self.process(work[1], expiry_date_indices_weekly, ns.iterations)
                        else:
                            self.process(work[1], expiry_date_stocks, ns.iterations)
                        ns.iterations += 1
                        if ns.iterations == 5:
                            ns.iterations = 0
                            # self.first = True
                        # if self.iterations > 1 and self.iterations < 10:
                        # self.first = False
                else:
                    it = 0
                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strcurrentDateTime = strcurrentDateTime.replace(':', '.')
                    if float(strcurrentDateTime) >= float(09.15) and float(strcurrentDateTime) <= float(17.00):
                        if diction[work[1]] == 'FALSE':
                            self.process(work[1], expiry_date_indices_monthly, it)
                            self.process(work[1], expiry_date_indices_weekly, it)
                        else:
                            self.process(work[1], expiry_date_stocks, it)
                    else:
                        print('Market is not ON, So no new data is Available')



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
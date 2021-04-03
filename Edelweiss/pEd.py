from common.gAPI import GoogleAPI
import pandas as pd
from Edelweiss.scrapEd import ScrapData
from common.common import CommonFunctions
from common.sheetOperations import SheetOps
from Edelweiss.helpEd import HelpEd
import time
import os
from pytz import timezone
import datetime


class ProcessEd:
    def __init__(self):
        self.objGAPI = GoogleAPI()
        self.objScrap = ScrapData()
        self.objCommon = CommonFunctions()
        self.objSheet = SheetOps()
        self.fixed_columns = ['ScripName', 'StrikePrice', 'OptionType',
                              'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                              'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL']
        self.first = True
        self.iterations = 0
        self.objHelpEd = HelpEd()

    def concate(self, previous_df, df_now):
        try:
            previous_df = self.objCommon.drop_extra_columns(previous_df, self.fixed_columns)
            df_now = self.objCommon.drop_extra_columns(df_now, self.fixed_columns)
            final = df_now.append(previous_df, ignore_index=True)
            final.reset_index(inplace=True)
        except Exception as e:
            print('concat exception: ', e)

        return final

    def save_to_drive(self, folder_id, name_of_file, destination):
        try:
            # name_of_file = destination.split('/')[1]
            service = self.objGAPI.intiate_gdAPI()
            # Search file id to check it is exists or not
            # def search_file(service, file_name, mime_type, folder_id, search_in_folder=False):
            file_id = self.objGAPI.search_file(service, str(name_of_file), 'text/csv', folder_id, True)
            if type(file_id) is int:
                self.objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
            if type(file_id) is str:
                self.objGAPI.delete_file(service, file_id)
                time.sleep(1)
                self.objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
            return True
        except Exception as e:
            print('Exception while saving files on drive', e)
            return False

    def process(self, symbol, expiry_date):
        for dt in expiry_date:
            print('Scrapping for : ', dt)
            service = self.objGAPI.intiate_gdAPI()
            folderID = self.objGAPI.search_file(service, str(dt), '', '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA', True)

            file = self.objScrap.start_scraping(str(symbol), dt)
            name_of_file = file.split('csv/')[1]
            # Upload to drive
            # Check if data historical data is available on the drive
            isDataAvailable, file_id = self.objCommon.check_previous_data_exist(file, folderID)
            if isDataAvailable == False:
                self.save_to_drive(folderID, name_of_file, file)
            else:
                df_now = pd.read_csv(os.getcwd() + '/Edelweiss/csv/' + name_of_file, index_col=0)
                if self.first == True:
                    # Download file
                    file_to_save = os.getcwd() + '/Edelweiss/d_csv/' + name_of_file
                    self.objGAPI.download_files(service, file_to_save, file_id, False)
                previous_df = pd.read_csv(os.getcwd() + '/Edelweiss/d_csv/' + name_of_file, index_col=0)

                result = self.concate(previous_df, df_now)
                # Notify Outliers if any
                self.objHelpEd.outliers_notify(result, symbol, expiry_date)

                result.to_csv(os.getcwd() + '/Edelweiss/sample_data/' + name_of_file, index=False)
                if self.iterations == 10:
                    self.save_to_drive(folderID, name_of_file, os.getcwd() + '/Edelweiss/sample_data/' + name_of_file)

    def start(self, q, result, isMarketON, diction, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
        while not q.empty():
            work = q.get()
            try:
                if isMarketON == 'TRUE':
                    while True:
                        strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                        strcurrentTime = strcurrentTime.replace(':', '.')
                        if float(strcurrentTime) > float(15.35):
                            print('Market is not ON. Try tomorrow or change isMarketON flag')
                            break
                        if diction[work[1]] == 'FALSE':
                            self.process(work[1], expiry_date_indices_monthly)
                            self.process(work[1], expiry_date_indices_weekly)
                        else:
                            self.process(work[1], expiry_date_stocks)
                        self.iterations += 1
                        if self.iterations == 10:
                            self.iterations = 0
                            self.first = True
                        if self.iterations < 10:
                            self.first = False
                else:
                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strcurrentDateTime = strcurrentDateTime.replace(':', '.')
                    if float(strcurrentDateTime) >= float(09.15) and float(strcurrentDateTime) <= float(17.00):
                        if diction[work[1]] == 'FALSE':
                            self.process(work[1], expiry_date_indices_monthly)
                            self.process(work[1], expiry_date_indices_weekly)
                        else:
                            self.process(work[1], expiry_date_stocks)
                    else:
                        print('Market is not ON, So no new data is Available')



            except:
                result[work[0]] = {}
            # signal to the queue that task has been processed
            q.task_done()
        return True







# obj = ProcessEd()
# obj.start('Mayur')
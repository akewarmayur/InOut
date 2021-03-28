from common.gAPI import GoogleAPI
import pandas as pd
from scrapEd import ScrapData
from common.common import CommonFunctions
from common.sheetOperations import SheetOps
import time

class ProcessEd:
    def __init__(self):
        self.objGAPI = GoogleAPI()
        self.objScrap = ScrapData()
        self.objCommon = CommonFunctions()
        self.objSheet = SheetOps()
        self.fixed_columns = ['ScripName', 'StrikePrice', 'OptionType',
                              'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                              'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL']

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
            if folderID == 0:
                folderID = self.objGAPI.createFolder(service, str(dt), '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
            # Scrap Data
            file = self.objScrap.start_scraping(str(symbol), dt)
            name_of_file = file.split('/')[1]
            # Upload to drive
            # Check if data historical data is available on the drive
            isDataAvailable, file_id = self.objCommon.check_previous_data_exist(file, folderID)
            if isDataAvailable == False:
                self.save_to_drive(folderID, name_of_file, file)
            else:
                df_now = pd.read_csv('csv/' + name_of_file, index_col=0)
                # Download file
                file_to_save = 'd_csv/' + name_of_file
                self.objGAPI.download_files(service, file_to_save, file_id, False)
                previous_df = pd.read_csv('d_csv/' + name_of_file, index_col=0)
                result = self.concate(previous_df, df_now)
                result.to_csv('sample_data/' + name_of_file, index=False)
                self.save_to_drive(folderID, name_of_file, 'sample_data/' + name_of_file)

        # machine_name = input('Enter machine name as Mayur/Uddesh/Jiten ')
    def start(self, machine_name):
        diction = {}
        content = self.objSheet.readSheet('CIEconfig', 'EdelStocks', machine_name)
        symbol = self.objSheet.readSheetColumns(content, 'Symbol')
        indices_or_stocks = self.objSheet.readSheetColumns(content, 'Stocks')

        content = self.objSheet.readSheet('CIEconfig', 'EdelConfig')
        isMarketON = self.objSheet.readSheetColumns(content, 'MarketON')
        isMarketON = isMarketON[0]

        for i, s in enumerate(symbol):
            diction[s] = indices_or_stocks[i]

        expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly = self.objScrap.get_expiry_dates()
        print("Stocks Expiry Date => ", expiry_date_stocks)
        print("Indices Monthly Expiry Date => ", expiry_date_indices_monthly)
        print("Indices Weekly Expiry Date => ", expiry_date_indices_weekly)
        folderAvailable = False

        if len(diction) == 0:
            print('No stocks or Indices are available in the list to scrap data')
        else:
            if isMarketON == 'TRUE':
                while True:
                    for symbol, indices_or_stocks in diction.items():
                        print('For =>', symbol)
                        if indices_or_stocks == 'FALSE':
                            self.process(symbol, expiry_date_indices_monthly)
                            self.process(symbol, expiry_date_indices_weekly)
                        else:
                            self.process(symbol, expiry_date_stocks)

            else:
                for symbol, indices_or_stocks in diction.items():
                    print('For =>', symbol)
                    if indices_or_stocks == 'FALSE':
                        self.process(symbol, expiry_date_indices_monthly)
                        self.process(symbol, expiry_date_indices_weekly)
                    else:
                        self.process(symbol, expiry_date_stocks)


obj = ProcessEd()
obj.start('Mayur')
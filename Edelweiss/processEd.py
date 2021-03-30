from common.gAPI import GoogleAPI
import pandas as pd
from Edelweiss.scrapEd import ScrapData
from common.common import CommonFunctions
from common.sheetOperations import SheetOps
import time
import Edelweiss.edleConfig as edleConfig
import os

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

    def get_outliers(self, df_current, df_past, expiry_date):
        timings = df_past['StrTradeDateTime'].unique().tolist()
        timings_to_take = timings[:edleConfig.no_of_past_instruments]
        strik_price_list = df_current['StrikePrice'].unique().tolist()
        newdf = df_past[df_past.StrTradeDateTime.isin(timings_to_take)]

        for a, s in enumerate(strik_price_list):
            tt = []

            current_coi_ce = None
            current_coi_pe = None
            old_coi_ce = None
            old_coi_pe = None

            tempCE = df_current[(df_current.OptionType == 'CE') & (df_current.StrikePrice == s)]['COI']
            current_coi_ce = tempCE.tolist()[0]
            tempPE = df_current[(df_current.OptionType == 'PE') & (df_current.StrikePrice == s)]['COI']
            current_coi_pe = tempPE.tolist()[0]
            tt.append(current_coi_ce)
            tt.append(current_coi_pe)

            for i, j in enumerate(newdf['StrikePrice']):
                if s == j:
                    tt.append(newdf['COI'].iloc[i])

            tt_ce = [tt[x] for x in range(len(tt)) if x % 2 == 0]
            tt_pe = [tt[x] for x in range(len(tt)) if x % 2 != 0]
            old_coi_ce = tt_ce[1]
            old_coi_pe = tt_pe[1]

            # Check Outliers
            list_of_outliers_ce = self.objCommon.get_outliers_from_list(tt_ce)
            list_of_outliers_pe = self.objCommon.get_outliers_from_list(tt_pe)

            d = df_current[(df_current.StrikePrice == s)]
            d_ce = d.iloc[0].to_list()
            d_pe = d.iloc[1].to_list()

            if current_coi_ce in list_of_outliers_ce:
                #writeSheet(self, filenameToRead, list_to_write, sheet_name)
                #datetime, instrument code, option type, strike price, old COI, new COI
                list_to_write = [d_ce[4], d_ce[0], expiry_date, 'CE', s, old_coi_ce, current_coi_ce]
                self.objSheet.writeSheet('CIEnotifications',list_to_write, 'EdelweissNotify')
                print('Notify CE COI')
            if current_coi_pe in list_of_outliers_pe:
                list_to_write = [d_pe[4], d_pe[0], expiry_date, 'PE', s, old_coi_pe, current_coi_pe]
                self.objSheet.writeSheet('CIEnotifications', list_to_write, 'EdelweissNotify')
                print('Notify PE COI')


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
            name_of_file = file.split('csv/')[1]
            # Upload to drive
            # Check if data historical data is available on the drive
            isDataAvailable, file_id = self.objCommon.check_previous_data_exist(file, folderID)
            if isDataAvailable == False:
                self.save_to_drive(folderID, name_of_file, file)
            else:
                df_now = pd.read_csv(os.getcwd() + '/Edelweiss/csv/' + name_of_file, index_col=0)
                # Download file
                file_to_save = os.getcwd() + '/Edelweiss/d_csv/' + name_of_file
                self.objGAPI.download_files(service, file_to_save, file_id, False)
                previous_df = pd.read_csv(os.getcwd() + '/Edelweiss/d_csv/' + name_of_file, index_col=0)

                # Go for outliers or not
                if len(previous_df['StrTradeDateTime'].unique().tolist()) >= edleConfig.no_of_past_instruments:
                    # Notify Outliers if any
                    self.get_outliers(df_now, previous_df, dt)

                result = self.concate(previous_df, df_now)
                result.to_csv(os.getcwd() + '/Edelweiss/sample_data/' + name_of_file, index=False)
                self.save_to_drive(folderID, name_of_file, os.getcwd() + '/Edelweiss/sample_data/' + name_of_file)

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


# obj = ProcessEd()
# obj.start('Mayur')
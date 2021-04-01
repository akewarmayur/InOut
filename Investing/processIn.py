from common.sheetOperations import SheetOps
from Investing.scrapIn import ScrapData
from common.common import CommonFunctions
from common.gAPI import GoogleAPI
from Investing.helpers import Help
import pandas as pd
import Investing.investConfig as investConfig
from Investing.helpIn import HelpIn
import os
import datetime
from pytz import timezone

class ProcessIn:

    def __init__(self):
        self.resolution_dict = {'CONFIG_5MIN': 5, 'CONFIG_15MIN': 15, 'CONFIG_30MIN': 30,
                       'CONFIG_2H': 120, 'CONFIG_1D': 'D', 'CONFIG_1W': 'W', 'CONFIG_1M': 'M'}
        self.objSheet = SheetOps()
        self.objScrap = ScrapData()
        self.objCommon = CommonFunctions()
        self.objGAPI = GoogleAPI()
        self.objHelp = Help()
        self.objHelpIn = HelpIn()
        self.col2wrt = ['datetime', 'symbol', 'pid', 'resolution', 'close',
                        'volume', 'per_change', 'volume_high_count',
                        'close_count', 'per_change_count']
        self.fixed_columns = ['datetime', 'symbol', 'pid', 'resolution', 'open', 'close', 'high',
                              'low', 'volume', 'EMA_50', 'EMA_100', 'EMA_200', 'BBL_14_2.0',
                              'BBM_14_2.0', 'BBU_14_2.0', 'BBB_14_2.0', 'RSI_14', 'PSARl_0.02_0.2',
                              'PSARs_0.02_0.2', 'PSARaf_0.02_0.2', 'PSARr_0.02_0.2', 'ISA_9',
                              'ISB_26', 'ITS_9', 'IKS_26', 'ICS_26', 'per_change',
                              'volume_high_count', 'close_count', 'per_change_count', 'ha_close',
                              'ha_open', 'ha_high', 'ha_low']
        self.first = True
        self.iterations = 0

    def get_url(self):
        for _ in range(5):
          token = str(self.objScrap.get_token())
          if token != 'None':
            break
        URL= 'https://tvc4.forexpros.com/'+str(token)+'/1615191589/56/56/23/history?'
        # print(URL)
        return URL

    def readSymbol(self, pidValue):
        try:
            content = self.objSheet.readSheet('CIEconfig', 'InvestingStocks')
            content = content.loc[content['Pid'] == pidValue]
            return content['Symbol'].values.tolist()
        except Exception as exReadSheet:
            print(exReadSheet)

    def concate(self, previous_df, df_now):
        previous_df = self.objCommon.drop_extra_columns(previous_df, self.objHelp.fixed_columns)

        df_new = previous_df.loc[:, :'volume']

        if len(df_new.index) >= 200:
            slice = df_new.iloc[:200]
        else:
            slice = df_new.iloc[:len(previous_df.index)]

        result = df_now.append(slice)
        result.reset_index(inplace=True)

        # calculate indicators
        result = self.objScrap.cal_indicators(result, ha=True, all=True)

        del_200 = previous_df.iloc[200:]
        final = result.append(del_200)
        final.reset_index(inplace=True)

        return final

    def get_slice(self, current_df, ran):
        df_new = current_df[self.col2wrt]
        df_new = df_new[:ran]
        return df_new

    def process(self, service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file):
        # Download File in Local directory
        if self.first == True:
            self.objGAPI.download_files(service, file_to_save, file_id, False)
            self.first = False
        previous_data = pd.read_csv(file_to_save, parse_dates=['datetime'])
        end_date = self.objHelp.get_end_date(previous_data)
        status = self.objScrap.scrap(URL, PID, symbl, item, end_date, no_of_days[i])
        if status == True:
            current_data = pd.read_csv(file, parse_dates=['datetime'])
            current_data.head()
            data = self.concate(previous_data, current_data)
            # data.reset_index(drop=True, inplace=True)
            if len(current_data) <= 20:
                candles_to_notify_from = len(current_data)
            else:
                candles_to_notify_from = 20
            notify_df = self.get_slice(data, 200 + candles_to_notify_from)
            self.objHelpIn.notifications(notify_df, candles_to_notify_from)
            data = self.objCommon.drop_extra_columns(data, self.fixed_columns)
            name_of_file = file.split('csv/')[1]
            data.to_csv(os.getcwd() + '/Investing/sample_data/' + name_of_file, index=False)
            if self.iterations == 10:
                self.objHelp.save_to_drive(data, file)


    def start(self, machine_name):
        print("Machine Name : ", machine_name)
        service = self.objGAPI.intiate_gdAPI()
        URL = self.get_url()
        if URL == 'None':
            URL = self.get_url()
        content = self.objSheet.readSheet('CIEconfig', 'InvestingConfig')
        no_of_days = content['Days']
        resolutions_list = content['Configuration']
        isMarketON = content['MarketON']
        isMarketON = isMarketON[0]
        # print('To be Scrapped: ', str(resolutions_list))
        # print('No of days: ', str(no_of_days))

        content = self.objSheet.readSheet('CIEconfig', 'InvestingStocks', machine_name)
        content = content['Pid']
        content = content.values.tolist()
        pid = [row for row in content if row != '']
        if len(pid) == 0:
            print('No stocks are available in the list to scrap data')
        else:
            try:
                if isMarketON == 'TRUE':
                    while True:
                        strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                        strcurrentTime = strcurrentTime.replace(':', '.')
                        if float(strcurrentTime) > float(03.30) or float(strcurrentTime) > float(3.30):
                            break
                        for PID in pid:
                            symbl = self.readSymbol(PID)
                            symbl = symbl[0]
                            name_of_stock = symbl
                            for i, item in enumerate(resolutions_list):
                                resolution = self.resolution_dict[item]

                                file = os.getcwd() + '/Investing/csv/' + str(name_of_stock) + '_' + str(resolution) + '.csv'
                                file_to_save = os.getcwd() + '/Investing/d_csv/' + str(name_of_stock) + '_' + str(resolution) + '.csv'
                                # check the historic data is available for the stock
                                isDataAvailable, file_id = self.objHelp.check_previous_data_exist(file)
                                # print('Is Data Available:', isDataAvailable)

                                if isDataAvailable == False:
                                    # URL, PID, symbl, row, end_date, no_of_days)
                                    status = self.objScrap.scrap(URL, PID, symbl, item, 0, no_of_days[i])
                                    # calculate indicators and upload to drive
                                    data = pd.read_csv(file, parse_dates=['datetime'])

                                    # data.reset_index(drop=True, inplace=True)

                                    data = self.objScrap.cal_indicators(data, ha=True, all=True)
                                    # data = objIndicators.cal_heiken_ashi(data)
                                    candles_to_notify_from = 20
                                    notify_df = self.get_slice(data, 200 + candles_to_notify_from)
                                    self.objHelpIn.notifications(notify_df, candles_to_notify_from)
                                    self.objHelp.save_to_drive(data, file)

                                elif isDataAvailable == True:
                                    if resolution == 'W':
                                        if datetime.date.today().isoweekday() == 1:
                                            self.process(service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file)
                                    if resolution == 'D':
                                        strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                                        strcurrentDateTime = strcurrentDateTime.replace(':', '.')
                                        if (float(strcurrentDateTime) < float('12.00')) or (float(strcurrentDateTime) < float('12.30')):
                                            self.process(service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file)
                                    if resolution == 5 or resolution == 15 or resolution == 30:
                                        self.process(service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file)

                                    else:
                                        print('No Data available in the given range of date')

                                else:
                                    print('Something is Wrong, Try Again')
                        self.iterations += 1
                        if self.iterations == 10:
                            self.iterations = 0

                else:
                    for PID in pid:
                        symbl = self.readSymbol(PID)
                        symbl = symbl[0]
                        name_of_stock = symbl
                        for i, item in enumerate(resolutions_list):
                            resolution = self.resolution_dict[item]

                            file = os.getcwd() + '/Investing/csv/' + str(name_of_stock) + '_' + str(resolution) + '.csv'
                            file_to_save = os.getcwd() + '/Investing/d_csv/' + str(name_of_stock) + '_' + str(
                                resolution) + '.csv'
                            # check the historic data is available for the stock
                            isDataAvailable, file_id = self.objHelp.check_previous_data_exist(file)
                            # print('Is Data Available:', isDataAvailable)

                            if isDataAvailable == False:
                                # URL, PID, symbl, row, end_date, no_of_days)
                                status = self.objScrap.scrap(URL, PID, symbl, item, 0, no_of_days[i])
                                # calculate indicators and upload to drive
                                data = pd.read_csv(file, parse_dates=['datetime'])

                                # data.reset_index(drop=True, inplace=True)

                                data = self.objScrap.cal_indicators(data, ha=True, all=True)
                                # data = objIndicators.cal_heiken_ashi(data)
                                candles_to_notify_from = 20
                                notify_df = self.get_slice(data, 200 + candles_to_notify_from)
                                self.objHelpIn.notifications(notify_df, candles_to_notify_from)
                                self.objHelp.save_to_drive(data, file)

                            elif isDataAvailable == True:
                                if resolution == 'W':
                                    if datetime.date.today().isoweekday() == 1:
                                        self.process(service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file)
                                if resolution == 'D':
                                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                                    strcurrentDateTime = strcurrentDateTime.replace(':', '.')
                                    if (float(strcurrentDateTime) < float('9.30')) or (float(strcurrentDateTime) < float('09.30')):
                                        self.process(service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file)
                                if resolution == 5 or resolution == 15 or resolution == 30:
                                    self.process(service, file_to_save, file_id, URL, PID, symbl, item, no_of_days, i, file)
                                else:
                                    print('No Data available in the given range of date')

                            else:
                                print('Something is Wrong, Try Again')

            except Exception as e:
                print(e)


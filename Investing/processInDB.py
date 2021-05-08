from common.sheetOperations import SheetOps
from Investing.scrapInDB import ScrapData
from common.common import CommonFunctions
from Investing.helpers import Help
import pandas as pd
from DBSQL.dbOperations import DBOperations
from Investing.helpIn import HelpIn
import os
import datetime
from pytz import timezone
import time

class ProcessIn:
    def __init__(self):
        self.resolution_dict = {'CONFIG_1MIN': 1, 'CONFIG_5MIN': 5, 'CONFIG_15MIN': 15, 'CONFIG_30MIN': 30,
                       'CONFIG_2H': 120, 'CONFIG_1D': 'D', 'CONFIG_1W': 'W', 'CONFIG_1M': 'M'}
        self.resolution_tables = {'CONFIG_1MIN': '1_MIN', 'CONFIG_5MIN': '5_MIN', 'CONFIG_15MIN': '15_MIN', 'CONFIG_30MIN': '30_MIN',
                               'CONFIG_2H': '2_H', 'CONFIG_1D': 'day', 'CONFIG_1W': 'week'}
        self.objSheet = SheetOps()
        self.objScrap = ScrapData()
        self.objCommon = CommonFunctions()
        self.objHelp = Help()
        self.objHelpIn = HelpIn()
        self.objDB = DBOperations()
        self.col2wrt = ['datetime', 'symbol', 'pid', 'resolution', 'close',
                        'volume', 'per_change', 'volume_high_count',
                        'close_count', 'per_change_count']
        self.fixed_columns = ['datetime', 'symbol', 'pid', 'resolution', 'open', 'close', 'high', 'low', 'volume']



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
        result = self.objScrap.cal_indicators_notify(result)
        previous_df = previous_df.loc[:, :'volume']
        del_200 = previous_df.iloc[200:]
        final = result.append(del_200)
        final.reset_index(inplace=True)

        return final

    def get_slice(self, current_df, ran):
        df_new = current_df[self.col2wrt]
        df_new = df_new[:ran]
        return df_new

    def get_end_date(self, end_d):
        # end_d = df['datetime'].iloc[0]
        print('Last Date of scrapped data=> ', end_d)
        #end_d = datetime.datetime.strptime(end_d, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.timestamp(end_d)
        # print('End date timestamp=> ', end_date)
        return int(end_date)

    def process(self, URL, PID, symbl, item, no_of_days, i, end_datetime, table_name, isMarketON=True):
        try:
            if isMarketON == True:
                # Download File in Local directory
                #query previous data from database
                previous_data = self.objDB.get_previous_data(table_name, symbl)
                end_date = self.get_end_date(end_datetime)
                status, current_data = self.objScrap.scrap(URL, PID, symbl, item, end_date, no_of_days[i])
                if status == True:
                    data = self.concate(previous_data, current_data)
                    # data.reset_index(drop=True, inplace=True)
                    if len(current_data) <= 20:
                        candles_to_notify_from = len(current_data)
                    else:
                        candles_to_notify_from = 20
                    notify_df = self.get_slice(data, 200 + candles_to_notify_from)
                    self.objHelpIn.notifications(notify_df, candles_to_notify_from)
                    # data = self.objCommon.drop_extra_columns(data, self.fixed_columns)
                    # Insert into DB
                    return True, current_data
                else:
                    return False, 0
        except Exception as e:
            print('Exception in Scrapping & Saving data:', e)
            return False


    def start(self, machine_name, first):
        if first == 'TRUE':
            try:
                self.objDB.createDB()
                self.objDB.createTables()
                df = pd.read_csv('investing_stocks.csv', index_col=False)
                for index, row in df.iterrows():
                    symbol = row['Symbol']
                    pid = row['Pid']
                    self.objDB.inertStocks(symbol, int(pid))
            except Exception as e:
                print('Exception in Initialization:', e)
                return False

        print("Machine Name : ", machine_name)
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
                        t1 = time.time()
                        strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                        strcurrentTime = strcurrentTime.replace(':', '.')
                        if float(strcurrentTime) < float(15.30):
                            print('Market is not ON. Try tomorrow or change isMarketON flag')
                            break
                        for PID in pid:
                            symbl = self.readSymbol(PID)
                            symbl = symbl[0]
                            name_of_stock = symbl
                            for i, item in enumerate(resolutions_list):
                                resolution = self.resolution_dict[item]
                                table_name = self.resolution_tables[item]
                                # check the historic data is available in DB
                                query = "SELECT datetime FROM {} WHERE symbol=%s ORDER BY datetime DESC LIMIT 1".format(table_name)
                                res = self.objDB.executeQuery(query, table_name, (symbl,))
                                end_datetime = res[0][0]
                                if resolution == 'W':
                                    if datetime.date.today().isoweekday() == 1:
                                        status, data = self.process(URL, PID, symbl, item, no_of_days, i, end_datetime, table_name
                                                                    )
                                        data = self.objScrap.cal_indicators(data, ha=True, all=True)
                                        self.objDB.DFintoSQL(data, table_name)
                                        if status == False:
                                            print('No Data available in the given range of date')
                                if resolution == 'D':
                                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                                    strcurrentDateTime = strcurrentDateTime.replace(':', '.')
                                    if (float(strcurrentDateTime) < float('15.00')) or (float(strcurrentDateTime) < float('15.30')):
                                        status, data = self.process(URL, PID, symbl, item, no_of_days, i, end_datetime, table_name)
                                        data = self.objScrap.cal_indicators(data, ha=True, all=True)
                                        self.objDB.DFintoSQL(data, table_name)
                                        if status == False:
                                            print('No Data available in the given range of date')
                                if resolution == 1 or resolution == 5 or resolution == 15 or resolution == 30 or resolution == 120:
                                    status, data = self.process(URL, PID, symbl, item, no_of_days, i, end_datetime, table_name)
                                    data = self.objScrap.cal_indicators(data, ha=True, all=True)
                                    self.objDB.DFintoSQL(data, table_name)
                                    if status == False:
                                        print('No Data available in the given range of date')

                                else:
                                    print('Something is Wrong, Try Again')
                        t2 = time.time()
                        time_elapsed = round(t2 - t1)
                        sleep_time = 3600 - time_elapsed
                        time.sleep(sleep_time)

                else:
                    for PID in pid:
                        symbl = self.readSymbol(PID)
                        symbl = symbl[0]
                        for i, item in enumerate(resolutions_list):
                            resolution = self.resolution_dict[item]
                            table_name = self.resolution_tables[item]
                            # URL, PID, symbl, row, end_date, no_of_days)
                            status, data = self.objScrap.scrap(URL, PID, symbl, item, 0, no_of_days[i])
                            # calculate indicators and upload to drive
                            if status == True:
                                # data.reset_index(drop=True, inplace=True)
                                data = self.objScrap.cal_indicators(data, ha=True, all=True)
                                # self.objDB.DFintoSQL(data, table_name)
                                self.objDB.DF2SQL(data, table_name)
                            else:
                                print('No data available in the given range')
            except Exception as e:
                print('Exception in Investing Scrapping process:', e)


import requests
import ast
import datetime
import pandas as pd
import time
import warnings
from pytz import timezone
from Investing.helpers import Help
from Investing.Indicators import Indicators
import pandas_ta as ta
warnings.filterwarnings("ignore")


class ScrapData:

    def __init__(self):
        self.url = 'https://in.investing.com/'
        self.USER_AGENT={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.objHelp = Help()
        self.objIndicators = Indicators()

    def get_token(self):
        response = requests.get(self.url, headers=self.USER_AGENT)
        res =response.text[5168:5209].split('"')
        for row in res:
            if len(row)> 20:
                token=row.isalnum()
                if token ==True:
                    return row
                    break
                else:
                    time.sleep(5)
                    self.get_token()

    def scrap(self, URL, PID, symbl, row, end_date, no_of_days):
        status = False
        no_of_days = int(no_of_days)
        if 'CONFIG_5MIN' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 5, self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 5, end_date, self.objHelp.cnvNumber(), symbl)
        elif 'CONFIG_15MIN' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 15, self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 15, end_date, self.objHelp.cnvNumber(), symbl)
        elif 'CONFIG_30MIN' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 30, self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 30, end_date, self.objHelp.cnvNumber(), symbl)
        elif 'CONFIG_2H' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 120, self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 120, end_date, self.objHelp.cnvNumber(), symbl)
        elif 'CONFIG_1D' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 'D', self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 'D', end_date, self.objHelp.cnvNumber(), symbl)
        elif 'CONFIG_1W' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 'W', self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 'W', end_date, self.objHelp.cnvNumber(), symbl)
        elif 'CONFIG_1M' == row:
            if end_date == 0:
                status = self.read_url(URL, PID, 'M', self.objHelp.cnvNumberWithDate(no_of_days), self.objHelp.cnvNumber(), symbl)
            else:
                status = self.read_url(URL, PID, 'M', end_date, self.objHelp.cnvNumber(), symbl)

        return status



    def read_url(self, URL, symbol, resolution, fromValue, toValue, symbl):
        try:
            # print('fromValue:', fromValue)
            # print('toValue:', toValue)
            url = URL+'symbol='+str(symbol)+'&resolution='+str(resolution)+'&from='+str(fromValue)+'&to='+str(toValue)
            print(url)
            response = requests.get(url, headers=self.USER_AGENT)
            res = ast.literal_eval(response.text)
            #print('********', res)
            try:
              del res['vo']
            except:
              pass
            try:
              del res['s']
            except:
              pass
            res['pid'] = symbol
            res['resolution'] = resolution
            res['symbol'] = symbl
            df = pd.DataFrame()
            df = pd.DataFrame(res)
            df.rename(columns = {"t": "datetime", "o":"open", "c":"close", "h":"high", "l":"low", "v":"volume"}, inplace = True)
            new_columns = ['symbol', 'pid', 'resolution', 'datetime', 'open', 'close', 'high', 'low', 'volume']
            df['datetime'] = df['datetime'].apply(self.objHelp.cvtNumberToDateTime)
            df.sort_values(by=['datetime'], inplace=True, ascending=False)
            #df.reset_index(drop=True, inplace=True)
            df = df.reindex(columns=new_columns)
            #df.set_index('datetime', inplace=True)
            df.set_index('datetime', inplace=True)
            df.to_csv('csv/'+str(symbl)+'_'+str(resolution)+ '.csv')
            return True
        except Exception as e:
            print('Getting Response Exception:', e)
            return False

    def cal_indicators(self, temp, ha=False, all=True):
        if all == True:
            # print(temp.head(2))
            temp.ta.strategy(self.objIndicators.CustomStrategy)

        # calculate custom indicators
        temp = self.objIndicators.custom_indicators(temp, 'per_change')

        temp = self.objIndicators.custom_indicators(temp, 'volume_high_count')

        temp = self.objIndicators.custom_indicators(temp, 'close_count')

        temp = self.objIndicators.custom_indicators(temp, 'per_change_count')

        if ha == True:
            temp = self.objIndicators.cal_heiken_ashi(temp)

        return temp





# objScrapData = ScrapData()
#

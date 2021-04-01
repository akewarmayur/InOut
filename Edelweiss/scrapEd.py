from datetime import datetime
import datetime
import pandas as pd
import warnings
from pytz import timezone
import requests
from dateutil.parser import parse
import io
import os
warnings.filterwarnings("ignore")

class ScrapData:
    def __init__(self):
        self.url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
        self.headers = {'Content-Length': '52', 'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                        'Content-Type': 'application/json', 'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9'}

    def start_scraping(self, scripName, expDate):
        #time_now = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
        exd = expDate.replace(' ', '_')
        file_saved_as = os.getcwd() + "/Edelweiss/csv/" + str(scripName) + "_" + str(exd) + ".csv"
        if scripName == 'FINNIFTY' or scripName == 'BANKNIFTY' or scripName == 'NIFTY':
            data = '{ ' + "'exp':'{0}','aTyp':'OPTIDX','uSym':'{1}'".format(expDate, scripName) + '}'
        else:
            data = '{ ' + "'exp':'{0}','aTyp':'OPTSTK','uSym':'{1}'".format(expDate, scripName) + '}'
        # print(data)
        runCtr = 0
        try:
            r = requests.post(url=self.url, timeout=20, headers=self.headers, data=data)
            jsons = r.json()['opChn']
            #print(jsons)
            # Init Dataframe to store Edelweiss values
            df = pd.DataFrame(
                columns=['ScripName', 'StrikePrice', 'OptionType', 'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                         'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL'])

            runCtr = runCtr + 1
            ctr = 0
            for j in jsons:
                ctr = ctr + 1
                if (j['ceQt']['trdSym'][-2:] == 'CE'):
                    tradeSymbol = j['ceQt']['trdSym']
                    optionType = tradeSymbol[-2:]
                    strExpiryDate = tradeSymbol[len(scripName):(len(scripName) + 7)]
                    ExpiryDate = datetime.datetime.strptime(strExpiryDate, '%d%b%y')
                    currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))
                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strikePrice = float(tradeSymbol[len(scripName) + 7:-2])
                    OI = j['ceQt']['opInt']
                    COI = j['ceQt']['opIntChg']
                    IV = j['ceQt']['ltpivfut']
                    VOL = j['ceQt']['vol']
                    df.loc[
                        ctr] = scripName, strikePrice, optionType, strcurrentDateTime, currentDateTime, ExpiryDate, strExpiryDate, float(
                        OI), float(COI), float(IV), int(VOL)
                    ctr = ctr + 1

                if (j['peQt']['trdSym'][-2:] == 'PE'):
                    tradeSymbol = j['peQt']['trdSym']
                    optionType = tradeSymbol[-2:]
                    strExpiryDate = tradeSymbol[len(scripName):(len(scripName) + 7)]
                    ExpiryDate = datetime.datetime.strptime(strExpiryDate, '%d%b%y')
                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strikePrice = float(tradeSymbol[len(scripName) + 7:-2])
                    OI = j['peQt']['opInt']
                    COI = j['peQt']['opIntChg']
                    IV = j['peQt']['ltpivfut']
                    VOL = j['peQt']['vol']
                    df.loc[
                        ctr] = scripName, strikePrice, optionType, strcurrentDateTime, currentDateTime, ExpiryDate, strExpiryDate, float(
                        OI), float(COI), float(IV), int(VOL)
            df.to_csv(file_saved_as, index=False)
            # print(df.head(2))
            print(strcurrentDateTime)
            return file_saved_as
        except Exception as e:
            print("In Exception ", e)
            return file_saved_as

    def get_expiry_dates(self):
        try:

            url = 'https://api.kite.trade/instruments'
            urlData = requests.get(url).content
            instrument_data = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
            exp_dt_stks = instrument_data[instrument_data['name'] == 'ACC']['expiry'].unique().tolist()[:2]
            expiry_date_indices = instrument_data[instrument_data['name'] == 'BANKNIFTY']['expiry'].unique().tolist()
            expiry_date_indices.remove(exp_dt_stks[0])

            def change_format(dt):
                dt = parse(dt)
                return dt.strftime('%d %b %Y')

            expiry_date_stocks = list(map(change_format, exp_dt_stks))
            expiry_date_indices = list(map(change_format, expiry_date_indices))

            expiry_date_indices_monthly = expiry_date_stocks
            expiry_date_indices_weekly = expiry_date_indices[:2]

            return expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly
        except Exception as e:
            print("Exception while getting Expiry dates", e)
            return [], [], []

# obj = ScrapData()
# obj.start_scraping('ACC', '29 Apr 2021')
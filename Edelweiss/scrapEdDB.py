from datetime import datetime
import datetime
import pandas as pd
import warnings
from pytz import timezone
import requests
from dateutil.parser import parse
import io
import os
import numpy as np
import config
from common.DBOperations import DatabaseOp
from common.sheetOperations import SheetOps

warnings.filterwarnings("ignore")

class ScrapData:
    def __init__(self):
        self.url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
        self.headers = {'Content-Length': '52', 'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                        'Content-Type': 'application/json', 'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9'}
        self.objDB = DatabaseOp()
        self.objSheet = SheetOps()


    def notifications(self, dt, strikePrice, symbol, expiry_date, option_type, old_OI, current_OI):
        if config.env == 'QA':
            sheet_to_notify = 'EdelNotifyQA'
        else:
            sheet_to_notify = 'EdelweissNotify'
        try:
            list_to_write = [dt, symbol, expiry_date, option_type, strikePrice, old_OI, current_OI]
            self.objSheet.writeSheet('CIEnotifications', list_to_write, sheet_to_notify)
        except Exception as e:
            print('Exception in outliers Notification Process:', e)


    def start_scraping(self, scripName, expDate):
        exd = expDate.replace(' ', '_')
        table_name = config.TableName + exd
        conn = self.objDB.create_connection()
        query = 'SELECT StrTradeDateTime FROM {} WHERE ScripName=? ORDER BY StrTradeDateTime DESC LIMIT 1'.format(table_name)
        cur = conn.cursor()
        cur.execute(query, [scripName])
        rows = cur.fetchall()
        if len(rows) != 0:
            pvTime = rows[0][0]
            print(pvTime)
        else:
            pvTime = ''
        que = 'SELECT Threshold FROM Threshold WHERE ScripName=? AND ExpiryDate=?'
        cur = conn.cursor()
        ed = expDate.replace(' ', '-')
        ed = ed.replace('20', '')
        cur.execute(que, [scripName, str(ed)])
        rr = cur.fetchone()
        threshold = rr[0]

        currentDate = str(datetime.datetime.now(timezone('Asia/Calcutta'))).split(' ')[0]
        currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))

        if scripName == 'FINNIFTY' or scripName == 'BANKNIFTY' or scripName == 'NIFTY':
            data = '{ ' + "'exp':'{0}','aTyp':'OPTIDX','uSym':'{1}'".format(expDate, scripName) + '}'
            IndexORStocks = 1
        else:
            data = '{ ' + "'exp':'{0}','aTyp':'OPTSTK','uSym':'{1}'".format(expDate, scripName) + '}'
            IndexORStocks = 0
        # print(data)
        runCtr = 0
        try:
            r = requests.post(url=self.url, timeout=20, headers=self.headers, data=data)
            jsons = r.json()['opChn']
            runCtr = runCtr + 1
            ctr = 0
            for j in jsons:
                ctr = ctr + 1
                if (j['ceQt']['trdSym'][-2:] == 'CE'):
                    tradeSymbol = j['ceQt']['trdSym']
                    optionType = tradeSymbol[-2:]
                    strExpiryDate = tradeSymbol[len(scripName):(len(scripName) + 7)]
                    #ExpiryDate = datetime.datetime.strptime(strExpiryDate, '%d%b%y')
                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strikePrice = float(tradeSymbol[len(scripName) + 7:-2])
                    OI = j['ceQt']['opInt']
                    OI = float(OI)
                    COI = j['ceQt']['opIntChg']
                    IV = j['ceQt']['ltpivfut']
                    VOL = j['ceQt']['vol']
                    COI = float(COI)
                    if pvTime == '':
                        MOI = 0
                        prevOI = ''
                    else:
                        timeDiff = float(strcurrentDateTime.replace(':', '.')) - float(pvTime.replace(':', '.'))
                        if timeDiff == 0.0:
                            timeDiff = 1.0
                        que = 'SELECT OI FROM {} WHERE ScripName=? AND StrikePrice=? AND OptionType=? AND StrTradeDateTime=?'.format(table_name)
                        cur.execute(que, [scripName, strikePrice, optionType, pvTime])
                        rows = cur.fetchall()
                        if len(rows) != 0:
                            prevOI = rows[0][0]
                            MOI = (OI - float(prevOI)) / timeDiff
                        else:
                            prevOI = ''
                            MOI = 0
                        #Notification
                        # threshold = 0.0
                        if abs(float(MOI)) >= float(threshold):
                            self.notifications(strcurrentDateTime, str(strikePrice), scripName, expDate, optionType, str(prevOI), str(OI))

                    if COI != 0.0:
                        self.objDB.insert(conn, currentDate, scripName, IndexORStocks, strikePrice, optionType, strcurrentDateTime, currentDateTime,
                                          strExpiryDate, OI, COI, IV, VOL, MOI, 0, table_name)
                    ctr = ctr + 1

                if (j['peQt']['trdSym'][-2:] == 'PE'):
                    tradeSymbol = j['peQt']['trdSym']
                    optionType = tradeSymbol[-2:]
                    strExpiryDate = tradeSymbol[len(scripName):(len(scripName) + 7)]
                    #ExpiryDate = datetime.datetime.strptime(strExpiryDate, '%d%b%y')
                    strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                    strikePrice = float(tradeSymbol[len(scripName) + 7:-2])
                    OI = j['peQt']['opInt']
                    OI = float(OI)
                    COI = j['peQt']['opIntChg']
                    IV = j['peQt']['ltpivfut']
                    VOL = j['peQt']['vol']
                    COI = float(COI)
                    if pvTime == '':
                        MOI = 0
                        prevOI = ''
                    else:
                        timeDiff = float(strcurrentDateTime.replace(':', '.')) - float(pvTime.replace(':', '.'))
                        if timeDiff == 0.0:
                            timeDiff = 1.0
                        que = 'SELECT OI FROM {} WHERE ScripName=? AND StrikePrice=? AND OptionType=? AND StrTradeDateTime=?'.format(table_name)
                        cur.execute(que, [scripName, strikePrice, optionType, pvTime])
                        rows = cur.fetchall()
                        if len(rows) != 0:
                            prevOI = rows[0][0]
                            MOI = (OI - float(prevOI)) / timeDiff
                        else:
                            prevOI = ''
                            MOI = 0
                        # Notification
                        if abs(float(MOI)) > float(threshold):
                            self.notifications(strcurrentDateTime, str(strikePrice), scripName, expDate, optionType, str(prevOI), str(OI))

                    if COI != 0.0:
                        self.objDB.insert(conn, currentDate, scripName, IndexORStocks, strikePrice, optionType, strcurrentDateTime,
                                          currentDateTime, strExpiryDate, OI, COI, IV, VOL, MOI, 0, table_name)
            print(strcurrentDateTime)
            conn.close()
            return True
        except Exception as e:
            print("In Exception ", e)
            conn.close()
            return False

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
# d = obj.get_expiry_dates()
# print(d)
from datetime import datetime
import datetime
import pandas as pd
import warnings
from pytz import timezone
import requests
from dateutil.parser import parse
import io
import config
from Help.DBOperationsSQLite import DatabaseOp
import time
warnings.filterwarnings("ignore")
import json
import time

class ScrapData:
    def __init__(self):
        self.url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
        self.headers = {'Content-Length': '52', 'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                        'Content-Type': 'application/json', 'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9'}
        self.objDB = DatabaseOp()

    def get_expiry_dates(self):
        try:
            url = 'https://api.kite.trade/instruments'
            urlData = requests.get(url).content
            instrument_data = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
            exp_dt_stks = instrument_data[instrument_data['name'] == 'ACC']['expiry'].unique().tolist()[:2]
            expiry_date_indices = instrument_data[instrument_data['name'] == 'BANKNIFTY']['expiry'].unique().tolist()
            # print(expiry_date_indices)
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


    def cal_timeDiff(self, strcurrentDateTime, pvTime):
        strcurrentDateTime_list = strcurrentDateTime.split(':')
        pvTime_list = pvTime.split(':')

        if strcurrentDateTime_list[0] == pvTime_list[0]:
            timeDiff = abs(float(strcurrentDateTime_list[1]) - float(pvTime_list[1]))
            # print(timeDiff)
        else:
            timeDiff = abs(float(strcurrentDateTime_list[0]) - float(pvTime_list[0]))
            # print(timeDiff)
        return timeDiff




    def start_scraping(self, symbol, EDStocks, EDIndicesW, stprice):

        currentDate = str(datetime.datetime.now(timezone('Asia/Calcutta'))).split(' ')[0]
        if symbol == 'FINNIFTY' or symbol == 'BANKNIFTY' or symbol == 'NIFTY':
            #EXD = EDStocks + EDIndicesW
            EXD = EDStocks
        else:
            EXD = EDStocks
        for expiryDate in EXD:
            print(f"___ {symbol} \t {expiryDate} ___")
            exd = expiryDate.replace(' ', '_')
            if symbol == 'FINNIFTY' or symbol == 'BANKNIFTY' or symbol == 'NIFTY':
                data = '{ ' + "'exp':'{0}','aTyp':'OPTIDX','uSym':'{1}'".format(expiryDate, symbol) + '}'
                table_name = config.TableName + exd
                table_name = table_name.lower()
            else:
                data = '{ ' + "'exp':'{0}','aTyp':'OPTSTK','uSym':'{1}'".format(expiryDate, symbol) + '}'
                table_name = config.TableName + exd
                table_name = table_name.lower()
            try:
                # runCtr = 0
                r = requests.post(url=self.url, timeout=10, headers=self.headers, data=data)
                jsons = r.json()['opChn']
                ctr = 0
                currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))
                strcurrentDateTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                stPrice =stprice
                bulk_insert=[]
                for j in jsons:
                    ctr = ctr + 1
                    if (j['ceQt']['trdSym'][-2:] == 'CE'):
                        tradeSymbol = j['ceQt']['trdSym']
                        optionType = tradeSymbol[-2:]
                        strikePrice = float(tradeSymbol[len(symbol) + 7:-2])
                        OI = j['ceQt']['opInt']
                        OI = float(OI)
                        COI = j['ceQt']['opIntChg']
                        IV = j['ceQt']['ltpivfut']
                        VOL = j['ceQt']['vol']
                        COI = float(COI)
                        # self.objDB.insert(currentDate, symbol, strikePrice, optionType, strcurrentDateTime, currentDateTime,
                        #                   OI, COI, IV, VOL,stPrice, table_name)
                        addpara= (currentDate, symbol, strikePrice, optionType, strcurrentDateTime, currentDateTime,OI, COI, IV, VOL,stPrice)
                        bulk_insert.append(addpara)
                        ctr = ctr + 1

                    if (j['peQt']['trdSym'][-2:] == 'PE'):
                        tradeSymbol = j['peQt']['trdSym']
                        optionType = tradeSymbol[-2:]
                        strikePrice = float(tradeSymbol[len(symbol) + 7:-2])
                        OI = j['peQt']['opInt']
                        OI = float(OI)
                        COI = j['peQt']['opIntChg']
                        IV = j['peQt']['ltpivfut']
                        VOL = j['peQt']['vol']
                        COI = float(COI)
                        # self.objDB.insert(currentDate, symbol, strikePrice, optionType, strcurrentDateTime,
                        #                   currentDateTime, OI, COI, IV, VOL,stPrice, table_name)
                        addpara = (currentDate, symbol, strikePrice, optionType, strcurrentDateTime, currentDateTime, OI, COI, IV,
                        VOL, stPrice)
                        bulk_insert.append(addpara)

                t= time.time()
                self.objDB.dpinsert(bulk_insert, table_name)
                #print('done in second',time.time()-t)
                #print("Count===",len(bulk_insert))
                query = "SELECT StrTradeDateTime FROM "+table_name+" WHERE ScripName='"+symbol+"' AND ScrapedDate='"+currentDate+"' ORDER BY StrTradeDateTime DESC LIMIT 1"
                #print("query==",query)
                conn = self.objDB.create_connection()
                cur= conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                cur.close()
                conn.close()

                if len(rows) == 0:
                    return False

            except Exception as e:
                # Log
                f = open("error.txt", "a")
                f.write(symbol + '\t' + exd + '\t' + datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M') + '\t' + str(e) + '\n')
                f.close()
                print("In Exception ", e)

        ### Insert all records


        return True

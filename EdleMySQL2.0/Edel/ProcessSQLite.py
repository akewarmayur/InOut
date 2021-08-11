from Edel.ScrapDataSQLite import ScrapData
import time
from pytz import timezone
import datetime
import config
import warnings
import os
from Edel.gAPISQLite import GoogleAPI
warnings.filterwarnings("ignore")
from Help.DBOperationsSQLite import DatabaseOp
import requests
import json

obj=DatabaseOp()

class ProcessEd():

    def process(self, symbol, EDStocks, EDIndicesW, stprice):
        objScrap = ScrapData()
        try:
            status = objScrap.start_scraping(symbol, EDStocks, EDIndicesW, stprice)
            if status == True:
                return True
            else:
                print(f"Scrapping df empty for : {symbol}")
                return False
        except Exception as e:
            print('Exception in Edle Scrapping Process:', e)
            return False

    # def change_format(self,dt):
    #     dt = parse(dt)
    #     return dt.strftime('%d %b %Y')

    def gen_table(self,stocksORindicesExpiryDates):
        try:
            for dt in stocksORindicesExpiryDates:
                # dt = dt.split(' ')
                # dt[1] = dt[1][0:3]
                # dt= ' '.join(dt)
                dt = dt.replace(' ', '_')
                obj.create_table(config.TableName + dt)
        except Exception as e:
            print('Exception in creating Table:', e)

    def get_token(self):
        url = 'https://in.investing.com/'
        # print(url)
        USER_AGENT = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=USER_AGENT)
        res = response.text[5168:5209].split('"')
        for row in res:
            if len(row) > 20:
                token = row.isalnum()
                if token == True:
                    return row
                    break


    def cnvNumberWithDateMinus5(self,numofDays):
        tod = datetime.datetime.now()
        date_time = tod.strftime("%Y-%m-%d") + " 12:00:00"
        backdate = datetime.timedelta(days=numofDays)
        next_date_time = tod - backdate
        #print("minus time :", next_date_time)
        next_datetime1 = next_date_time.strftime("%Y-%m-%d") + " 12:00:00"
        #print("next date time :", next_datetime1)
        element = datetime.datetime.strptime(next_datetime1, "%Y-%m-%d %H:%M:%S")
        timestamp = datetime.datetime.timestamp(element)
        #print("Minus date=========================", int(timestamp))
        return int(timestamp)

    def cnvNumberWithDatePlus5(self,numofDays):
        tod = datetime.datetime.now()
        date_time = tod.strftime("%Y-%m-%d") + " 12:00:00"
        backdate = datetime.timedelta(days=numofDays)
        next_date_time = tod + backdate
        #print("Add time :", next_date_time)
        next_datetime1 = next_date_time.strftime("%Y-%m-%d") + " 12:00:00"
        #print("next date time :", next_datetime1)
        element = datetime.datetime.strptime(next_datetime1, "%Y-%m-%d %H:%M:%S")
        timestamp = datetime.datetime.timestamp(element)
        #print("Plus date=========================", int(timestamp))
        return int(timestamp)

    def parse_url(self,pid,bf5date,af5date):
        try:
            readToken = ""
            try:

                with open("token.txt", "r+") as f:
                    readToken = f.read()  # read everything in the file
                    f.close()
            except Exception as e:
                f.close()
                print("Reading file error===",e)
                #print("==========================================",readToken)

            URL = 'https://tvc4.investing.com/' + str(readToken) + '/1626943211/56/56/23/history?symbol=' + str(
                pid) + '&resolution=1D&from=' + str(bf5date) + '&to=' + str(af5date) + ''
            #### URL='https://tvc4.investing.com/3c56685e0bcd1192bf342d953e8cbb54/1626943211/56/56/23/history?symbol=17950&resolution=1D&from=1626503400&to=1627367400'
            #URL = 'https://tvc4.investing.com/'+str(self.get_token())+'/1626943211/56/56/23/history?symbol='+str(pid)+'&resolution=1D&from='+str(bf5date)+'&to='+str(af5date)+''
            #URL = 'https://tvc4.investing.com/bb14c2c9b28e3fe16546d6ca55ce3dca/1626856516/1/1/8/quotes?symbols=NSE%20%3A'+str(stockName)
            USER_AGENT = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            response = requests.get(URL, headers=USER_AGENT,timeout=(10,200))
            #print(URL)
            if response.text =='null' or response.text =='None' or response.text == '':
                ## write

                try:

                    with open("token.txt", "r+") as f:
                        f.seek(0)  # rewind
                        token = self.get_token()
                        f.write(token)
                        f.close()
                        print("New token============",token)
                except Exception as e:
                    f.close()
                    print("Reading file error===", e)
                    ### read
                readToken = ""
                with open("token.txt", "r+") as f:
                    readToken = f.read()  # read everything in the file
                    f.close()
                    #print("==========================================", readToken)

                URL = 'https://tvc4.investing.com/' + str(readToken) + '/1626943211/56/56/23/history?symbol=' + str(
                    pid) + '&resolution=1D&from=' + str(bf5date) + '&to=' + str(af5date) + ''

                response = requests.get(URL, headers=USER_AGENT,timeout=(10,200))
                response = json.loads(response.text)
            else:
                response= json.loads(response.text)

            closingValue = round(response['c'][-1],2)
            #print(f'=====Pid===== {pid}===========lp(list price)====== {closingValue}')
            return closingValue
        except Exception as e:
            pass

    def regentakon(self,pid, before5daysfromtodaydate, After5daysfromtodaydate):
        for i in range(10):
            #print("Regenetoken=======")
            time.sleep(10)
            stprice = self.parse_url(pid, before5daysfromtodaydate, After5daysfromtodaydate)
            if stprice == "" or stprice == "null" or stprice == "None" or stprice == "None":
                continue
            else:
                return stprice


    def start(self, symbol_list,MarketFlag):
        before5daysfromtodaydate = self.cnvNumberWithDateMinus5(5)
        After5daysfromtodaydate = self.cnvNumberWithDatePlus5(5)
        if MarketFlag == 'True':
            iterations = 1
            while True:
                s = time.time()
                currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))
                strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                strcurrentTime = strcurrentTime.replace(':', '.')
                start = time.time()
                for index, row in symbol_list.iterrows():
                    if float(strcurrentTime) > float(15.30):
                        print('Market is not ON. Try tomorrow or change isMarketON flag')
                        break
                    else:
                        #print(row['Symbol'], row['Expiry Date'])
                        expiry_lst = []
                        expiry_lst.append(row['Expiry Date'])
                        self.gen_table(expiry_lst)
                        stprice = self.parse_url(row['Pid'], before5daysfromtodaydate, After5daysfromtodaydate)
                        status = self.process(row['Symbol'], expiry_lst, expiry_lst,stprice)

                if float(strcurrentTime) > float(15.30):
                    break
        else:
            currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))
            #print('Time Now: ', currentDateTime)
            strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
            strcurrentTime = strcurrentTime.replace(':', '.')
            start = time.time()
            # for symbol in symbol_list:
            #     status = self.process(symbol, EDStocks, EDIndicesW, conn)
            for index, row in symbol_list.iterrows():
                #print(row['Symbol'], row['Expiry Date'])
                expiry_lst =[]
                expiry_lst.append(row['Expiry Date'])
                self.gen_table(expiry_lst)
                stprice = self.parse_url(row['Pid'],before5daysfromtodaydate,After5daysfromtodaydate)
                status = self.process(row['Symbol'], expiry_lst, expiry_lst, stprice)


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
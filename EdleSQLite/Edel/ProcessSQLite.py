from Edel.ScrapDataSQLite import ScrapData
import time
from pytz import timezone
import datetime
import config
import warnings
import os
from Edel.gAPISQLite import GoogleAPI
warnings.filterwarnings("ignore")


class ProcessEd():

    def process(self, symbol, EDStocks, EDIndicesW, conn):
        objScrap = ScrapData()
        try:
            status = objScrap.start_scraping(symbol, EDStocks, EDIndicesW, conn)
            if status == True:
                return True
            else:
                print(f"Scrapping df empty for : {symbol}")
                return False
        except Exception as e:
            print('Exception in Edle Scrapping Process:', e)
            return False

    def start(self, symbol_list, EDStocks, EDIndicesW, conn, MarketFlag):
        if MarketFlag == 'True':
            iterations = 1
            while True:
                s = time.time()
                print('Iterations: ', iterations)
                currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))
                print('Time Now: ', currentDateTime)
                strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
                strcurrentTime = strcurrentTime.replace(':', '.')
                start = time.time()
                for symbol in symbol_list:
                    if float(strcurrentTime) > float(15.30):
                        print('Market is not ON. Try tomorrow or change isMarketON flag')
                        break
                    else:
                        status = self.process(symbol, EDStocks, EDIndicesW, conn)
                if float(strcurrentTime) > float(15.30):
                    break
                end = int(time.time() - start)
                iterations += 1
                print("time_taken==", end)
                if end <= config.TIME_SLEEP:
                    rows = config.TIME_SLEEP - end
                    objGAPI = GoogleAPI()
                    service = objGAPI.intiate_gdAPI()
                    file_id = objGAPI.search_file(service, config.DB_Name, 'mime_type',
                                                  '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', True)
                    if file_id != 0:
                        objGAPI.delete_file(service, file_id)
                    objGAPI.upload_file(service, config.DB_Name, os.getcwd() + '/DB/' + config.DB_Name,
                                        '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', 'application/vnd.sqlite3')
                    time.sleep(rows)
                # if s - config.TableName <= 0:

            # return True
        else:
            currentDateTime = datetime.datetime.now(timezone('Asia/Calcutta'))
            print('Time Now: ', currentDateTime)
            strcurrentTime = datetime.datetime.now(timezone('Asia/Calcutta')).strftime('%H:%M')
            strcurrentTime = strcurrentTime.replace(':', '.')
            start = time.time()
            for symbol in symbol_list:
                status = self.process(symbol, EDStocks, EDIndicesW, conn)
        objGAPI = GoogleAPI()
        service = objGAPI.intiate_gdAPI()
        file_id = objGAPI.search_file(service, config.DB_Name, 'mime_type',
                                      '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', True)
        if file_id != 0:
            objGAPI.delete_file(service, file_id)
        objGAPI.upload_file(service, config.DB_Name, os.getcwd() + '/DB/' + config.DB_Name,
                            '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', 'application/vnd.sqlite3')

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
import config
from common.gAPI import GoogleAPI
from common.DBOperations import DatabaseOp
from Edelweiss.scrapEd import ScrapData
import time
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import pandas as pd
import os

class HelpEdDB:

    def __init__(self):
        self.objDB = DatabaseOp()
        self.objGAPI = GoogleAPI()
        self.objDBOP = DatabaseOp()

    def get_sd_from_prev_day(self, scripName, table_name):
        sd = 0
        try:
            conn = self.objDB.create_connection()
            #query = 'SELECT ScrapedDate FROM {} WHERE ScripName=? ORDER BY StrTradeDateTime DESC LIMIT 1'.format(table_name)
            #'SELECT MinuteOI FROM {} WHERE ScripName=? AND ScrapedDate=? AND MinuteOI > ?'.format(table_name)
            query = 'SELECT ChangeCOI FROM {} WHERE ScripName=? AND ChangeCOI > ?'.format(table_name)
            cur = conn.cursor()
            cur.execute(query, [scripName, '0.0'])
            data = cur.fetchall()
            data = [float(x[0]) for x in data if float(x[0]) != 0.0]
            sd = np.std(data)
            return sd, True
        except Exception as e:
            print('Exception in SD calculation:', e)
            return sd, False

    def DB2CSV(self, scripName, table_name):
        try:
            conn = self.objDB.create_connection()
            cur = conn.cursor()
            #query = 'SELECT StrTradeDateTime FROM {} WHERE ScripName=? ORDER BY StrTradeDateTime DESC LIMIT 1'.format(table_name)
            query = 'SELECT * FROM {} WHERE ScripName=?'.format(table_name)
            cur.execute(query, [scripName])
            data = cur.fetchall()

            columns = ['ID', 'currentDate', 'scripName', 'IndexORStocks', 'strikePrice', 'optionType', 'strcurrentDateTime',
                       'currentDateTime', 'ExpiryDate', 'OI', 'COI', 'IV', 'VOL', 'MinuteOI', 'Flag', 'CreatedAT']
            df = pd.DataFrame(data, columns=columns)
            # df.to_csv(os.getcwd() + '/Edelweiss/csv/' + file_name, index=False)
            return df, True
            # print(df.head())
        except Exception as e:
            print('Exception in converting db to csv:', e)
            return 0, False

    def createTable(self, conn, stocksORindicesExpiryDates):
        try:
            for dt in stocksORindicesExpiryDates:
                dt = dt.replace(' ', '_')
                self.objDBOP.create_table(conn, config.TableName + dt)
        except Exception as e:
            print('Exception in creating Table:', e)

    def InsertThreshold(self, conn, ScripName, ExpiryDate, Threshold):

        que = 'SELECT Threshold FROM Threshold WHERE ExpiryDate=? AND ScripName=?'
        cur = conn.cursor()
        cur.execute(que, [ExpiryDate, ScripName])
        rows = cur.fetchone()
        if rows == None:
            self.objDBOP.insertThreshold(conn, ScripName, ExpiryDate, Threshold)
        else:
            self.objDBOP.updateThreshold(conn, ScripName, ExpiryDate, Threshold)


    def downloadDB(self, service, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
        try:
            name_of_file = config.DB_Name
            file_id = self.objGAPI.search_file(service, name_of_file, "text/csv", '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con',
                                               True)
            if file_id == 0:
                # Create new DB
                conn = self.objDBOP.create_connection()
                # Create Tables as per Expiry dates
                self.createTable(conn, expiry_date_stocks)
                self.createTable(conn, expiry_date_indices_monthly)
                self.createTable(conn, expiry_date_indices_weekly)
            else:
                file_to_save = os.getcwd() + '/DB/' + config.DB_Name
                self.objGAPI.download_files(service, file_to_save, file_id, False)
                conn = self.objDBOP.create_connection()
                # Create Tables as per Expiry dates
                self.createTable(conn, expiry_date_stocks)
                self.createTable(conn, expiry_date_indices_monthly)
                self.createTable(conn, expiry_date_indices_weekly)
            return True
        except Exception as e:
            print('Exception in downloading DB:', e)
            return False

    def downLoadAllCSV(self, service, Ndict, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
        try:
            for key, value in Ndict.items():
                if value == 'FALSE':
                    for f in expiry_date_indices_monthly:
                        f = f.replace(' ', '_')
                        name_of_file = str(key) + "_" + str(f) + ".csv"
                        file_saved_as = os.getcwd() + "/Edelweiss/d_csv/" + str(key) + "_" + str(f) + ".csv"
                        file_id = self.objGAPI.search_file(service, name_of_file, "text/csv", '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
                        if file_id != 0:
                            self.objGAPI.download_files(service, file_saved_as, file_id, False)

                    for f in expiry_date_indices_weekly:
                        f = f.replace(' ', '_')
                        name_of_file = str(key) + "_" + str(f) + ".csv"
                        file_saved_as = os.getcwd() + "/Edelweiss/d_csv/" + str(key) + "_" + str(f) + ".csv"
                        file_id = self.objGAPI.search_file(service, name_of_file, "text/csv", '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
                        if file_id != 0:
                            self.objGAPI.download_files(service, file_saved_as, file_id, False)
                else:
                    for f in expiry_date_stocks:
                        f = f.replace(' ', '_')
                        name_of_file = str(key) + "_" + str(f) + ".csv"
                        file_saved_as = os.getcwd() + "/Edelweiss/d_csv/" + str(key) + "_" + str(f) + ".csv"
                        file_id = self.objGAPI.search_file(service, name_of_file, "text/csv", '1GLA0S461C1yAc47jMXdwxBdoAWX9onbA')
                        if file_id != 0:
                            self.objGAPI.download_files(service, file_saved_as, file_id, False)
        except Exception as e:
            print('Exception in Downloading all CSVs:', e)





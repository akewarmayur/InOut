import sqlite3
from sqlite3 import Error
import os
import config
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
from Edel.gAPISQLite import GoogleAPI
# pip install DBUtils==1.3
# from DBUtils.PooledDB import PooledDB

# https://www.programmersought.com/article/78166137449/

# LOCALMYSQL = {
#         'host':'localhost',
#         'user': 'root',
#         'password': 'R@ting#2021',#
#         'db': 'edelweissdb',
#         'OPTIONS': {
#            "init_command": "SET GLOBAL max_connections = 100000"}
# }

LOCALMYSQL = {
        'host':'137.135.52.58',
        'user': 'admin',
        'password': 'HeJMU#2021',#
        'db': 'edelweissdb',
        'OPTIONS': {
           "init_command": "SET GLOBAL max_connections = 100000"}
}


class DatabaseOp:


    def checkInsertedRecords(self, conn,DateTime,Symbol,Resolution):
        cur = conn.cursor()
        cur.execute("SELECT id FROM stockDetails WHERE datetime = ? AND symbol= ? AND resolution=?", [DateTime,Symbol,Resolution])
        rows = cur.fetchall()
        return rows

    # def insert(self, conn, ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime,
    #            OI, COI, IV, VOL, table_name):
    #     insert_table_sql = """INSERT INTO {} (ScrapedDate, ScripName,StrikePrice,OptionType,StrTradeDateTime,
    #                                 TradeDateTime,OI, COI, IV, VOL)
    #                               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(table_name)
    #     try:
    #         queryparameter = ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime, OI, COI, IV, VOL
    #         c = conn.cursor()
    #         c.execute(insert_table_sql, queryparameter)
    #         conn.commit()
    #         # print("records inserted successfully")
    #     except Error as e:
    #         print(e)

    def DF2SQL(self, data, table_name, engine):
        # engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
        #                        .format(user="root",
        #                                pw="InOut@909",
        #                                db="indexdb"))
        # df = pd.read_sql("select * from {}".format(table_name), engine)
        # final = pd.concat([df, data]).drop_duplicates().reset_index(drop=True)
        # print(final.head())
        # print(final.columns)
        # data['datetime'] = data['datetime'].apply(lambda x: str(x))
        try:
            conn = engine.connect()
            # some simple data operations
            data.to_sql(table_name, con=conn, if_exists='append', chunksize=1000, index=False)
            conn.close()
            # engine.dispose()
        except Exception as e:
            print('Exception in converting DF to SQL:', e)

    import sqlite3
    from sqlite3 import Error
    import os
    import config

    ######

    def create_database(self):
        """ create a database connection to a SQLite database """
        DB_FILE = os.getcwd() + '/DB/' + config.DB_Name
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=50)
            print(sqlite3.version)
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()


    def create_connection(self):
        conn = None
        try:
            conn = pymysql.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'], password=LOCALMYSQL['password'],
                                   database=LOCALMYSQL['db'])
        except Exception as e:
            print("Connection failed====",e)

        return conn

    def create_table(self,table_name):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        conn = self.create_connection()
        c = conn.cursor()
        create_table_sql = ''' CREATE TABLE IF NOT EXISTS {}(
                                                           id INTEGER PRIMARY KEY AUTO_INCREMENT,  
                                                           ScrapedDate date NOT NULL,
                                                           ScripName varchar(12) NOT NULL,
                                                           StrikePrice float NOT NULL,
                                                           OptionType varchar(2) NOT NULL,
                                                           StrTradeDateTime varchar(6) NOT NULL,
                                                           TradeDateTime datetime NOT NULL, 
                                                           OI float NOT NULL,
                                                           COI float NOT NULL,
                                                           IV float NOT NULL,
                                                           VOL float NOT NULL,
                                                           SpotPrice float,
                                                           MinuteCOI float Null
                                                       );'''.format(table_name.lower())

        try:
            c.execute(create_table_sql)
        except Error as e:
            print(e)
        finally:
            c.close()
            conn.close()

    # def checkInsertedRecords(self, conn, DateTime, Symbol, Resolution):
    #     cur = conn.cursor()
    #     cur.execute("SELECT id FROM stockDetails WHERE datetime = ? AND symbol= ? AND resolution=?",
    #                 [DateTime, Symbol, Resolution])
    #     rows = cur.fetchall()
    #     return rows

    def dpinsert(self, data, table_name):

        conn = self.create_connection()
        c = conn.cursor()
        ## mysql parameters
        insert_table_sql = """INSERT INTO {} (ScrapedDate, ScripName,StrikePrice,OptionType,StrTradeDateTime,
                                           TradeDateTime,OI, COI, IV, VOL,SpotPrice)
                                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(table_name)

        ## SQLite parameters
        # insert_table_sql = """INSERT INTO {} (ScrapedDate, ScripName,StrikePrice,OptionType,StrTradeDateTime,
        #                     TradeDateTime, OI, COI, IV, VOL,SpotPrice)
        #                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""".format(table_name)
        try:
            #queryparameter = ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime, OI, COI, IV, VOL,SpotPriceVal
            #queryparameter = ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime, OI, COI, IV, VOL, SpotPriceVal
            c.executemany(insert_table_sql, data)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            c.close()
            conn.close()
    def insert(self, ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime,
               TradeDateTime, OI, COI, IV, VOL,SpotPriceVal, table_name):

        conn = self.create_connection()
        c = conn.cursor()
        ## mysql parameters
        insert_table_sql = """INSERT INTO {} (ScrapedDate, ScripName,StrikePrice,OptionType,StrTradeDateTime,
                                           TradeDateTime,OI, COI, IV, VOL,SpotPrice)
                                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(table_name)

        ## SQLite parameters
        # insert_table_sql = """INSERT INTO {} (ScrapedDate, ScripName,StrikePrice,OptionType,StrTradeDateTime,
        #                     TradeDateTime, OI, COI, IV, VOL,SpotPrice)
        #                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""".format(table_name)
        try:
            queryparameter = ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime, OI, COI, IV, VOL,SpotPriceVal
            #queryparameter = ScrapedDate, ScripName, StrikePrice, OptionType, StrTradeDateTime, OI, COI, IV, VOL, SpotPriceVal
            c.execute(insert_table_sql, queryparameter)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            c.close()
            conn.close()

    def downloadDB(self, service, expiry_date_stocks, expiry_date_indices_monthly, expiry_date_indices_weekly):
        try:
            tables = expiry_date_stocks + expiry_date_indices_monthly + expiry_date_indices_weekly
            table_names = []
            for t in tables:
                t = t.replace(' ', '_')
                t = config.TableName + t
                table_names.append(t)
            # print('___________________')
            # print(expiry_date_stocks)
            objGAPI = GoogleAPI()
            name_of_file = config.DB_Name
            file_id = objGAPI.search_file(service, name_of_file, "text/csv", '1llZZacQjhf2iNPjjpCBSSD4AdKFc5Con', True)
            if file_id == 0:
                # Create new DB
                conn = self.create_connection()
                # Create Tables as per Expiry dates
                for table_na in table_names:
                    self.create_table(conn, table_na)
                # for table_name in expiry_date_indices_monthly:
                #     self.create_table(conn, table_name)
                # for table_name in expiry_date_indices_weekly:
                #     self.create_table(conn, table_name)
            else:
                file_to_save = os.getcwd() + '/DB/' + config.DB_Name
                objGAPI.download_files(service, file_to_save, file_id, False)
                conn = self.create_connection()
                # Create Tables as per Expiry dates
                # self.create_table(conn, expiry_date_stocks)
                # self.create_table(conn, expiry_date_indices_monthly)
                # self.create_table(conn, expiry_date_indices_weekly)
                ## Added proper date(Jitu code)
                for table_na in table_names:
                    self.create_table(conn, table_na)

            return True
        except Exception as e:
            print('Exception in downloading DB:', e)
            return False





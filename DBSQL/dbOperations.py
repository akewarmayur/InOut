import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import numpy as np

class DBOperations:

    def __init__(self):
        print('Initiate')

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "InOut@909"
            )
            # db = db.cursor()
            return conn
        except Exception as e:
            print("Connection Exception:", e)

    def connectDB(self):
        try:
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "InOut@909",
                database = 'investing'
            )
            # db = db.cursor()
            return conn
        except Exception as e:
            print("Connection Exception:", e)

    def createDB(self):
        conn = self.connect()
        cursor = conn.cursor()
        query = "CREATE DATABASE IF NOT EXISTS invest"
        cursor.execute(query)


    def createTables(self):
        conn = self.connectDB()
        cursor = conn.cursor()
        TABLES = {}
        TABLES['stocks'] = (
            "CREATE TABLE IF NOT EXISTS `stocks`("
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  PRIMARY KEY (`pid`), UNIQUE KEY `symbol` (`symbol`)"
            ") ENGINE=InnoDB")

        TABLES['week'] = (
            "CREATE TABLE IF NOT EXISTS `week`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `week_ibfk_1` FOREIGN KEY (`pid`) "
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['day'] = (
            "CREATE TABLE IF NOT EXISTS `day`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `day_1` FOREIGN KEY (`pid`)"
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['30_MIN'] = (
            "CREATE TABLE IF NOT EXISTS `30_MIN`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `30_MIN_1` FOREIGN KEY (`pid`)"
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['15_MIN'] = (
            "CREATE TABLE IF NOT EXISTS `15_MIN`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `15_MIN_1` FOREIGN KEY (`pid`)"
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['5_MIN'] = (
            "CREATE TABLE IF NOT EXISTS `5_MIN`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `5_MIN_1` FOREIGN KEY (`pid`)"
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['2_H'] = (
            "CREATE TABLE IF NOT EXISTS `2_H`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `2_H_1` FOREIGN KEY (`pid`)"
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['1_MIN'] = (
            "CREATE TABLE IF NOT EXISTS `1_MIN`("
            "  `datetime` TIMESTAMP NOT NULL,"
            "  `symbol` varchar(256) NOT NULL,"
            "  `pid` int(12) NOT NULL,"
            "  `resolution` varchar(4) NOT NULL,"
            "  `open` float NOT NULL,"
            "  `close` float NOT NULL,"
            "  `high` float NOT NULL,"
            "  `low` float NOT NULL,"
            "  `volume` double NOT NULL,"
            "  `ema_50` float,"
            " `ema_100` float,"
            "  `ema_200` float,"
            "  `BBL_14_2.0` float,"
            "  `BBM_14_2.0` float,"
            "  `BBU_14_2.0` float,"
            "  `BBB_14_2.0` float,"
            "  `RSI_14` float,"
            "  `PSARl_0.02_0.2` float,"
            "  `PSARs_0.02_0.2` float,"
            "  `PSARaf_0.02_0.2` float,"
            "  `PSARr_0.02_0.2` varchar(32),"
            "  `ISA_9` float,"
            "  `ISB_26` float,"
            "  `ITS_9` float,"
            "  `IKS_26` float,"
            "  `ICS_26` float,"
            "  `per_change` float,"
            "  `volume_high_count` int(12),"
            "  `close_count` int(12),"
            "  `per_change_count` int(12),"
            "  `ha_close` float,"
            "  `ha_open` float,"
            "  `ha_high` float,"
            "  `ha_low` float,"
            "  PRIMARY KEY (`symbol`,`datetime`),"
            "  CONSTRAINT `1_MIN_1` FOREIGN KEY (`pid`)"
            "     REFERENCES `stocks` (`pid`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()
        conn.close()

    def inertStocks(self, symbol, pid):
        conn = self.connectDB()
        cursor = conn.cursor()
        add_stock = ("INSERT INTO stocks "
                        "(symbol, pid) "
                        "VALUES (%s, %s)")
        data_stock = (symbol, pid)
        cursor.execute(add_stock, data_stock)
        conn.commit()

        cursor.close()
        conn.close()

    def inertData(self, table_name, data_tuple):
        dt = data_tuple[0]
        sy = data_tuple[1]
        data_tuple_add = list(data_tuple)
        data_tuple_add.append(dt)
        data_tuple_add.append(sy)
        data_tuple_add = tuple(data_tuple_add)
        conn = self.connectDB()
        #34
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT datetime, pid FROM {} WHERE datetime=%s AND symbol=%s".format(table_name), (dt, sy))
            data = cursor.fetchall()
            if len(data) !=0:
                sql = "UPDATE {} SET datetime=%s, symbol=%s, pid=%s, resolution=%s," \
                      "open=%s, close=%s, high=%s, low=%s, volume=%s, ema_50=%s, " \
                      "ema_100=%s, ema_200=%s, `BBL_14_2.0`=%s, `BBM_14_2.0`=%s, `BBU_14_2.0`=%s, `BBB_14_2.0`=%s, RSI_14=%s,"\
                      "`PSARl_0.02_0.2`=%s,`PSARs_0.02_0.2`=%s, `PSARaf_0.02_0.2`=%s, `PSARr_0.02_0.2`=%s, ISA_9=%s, ISB_26=%s, ITS_9=%s,"\
                      "IKS_26=%s, ICS_26=%s, per_change=%s, volume_high_count=%s, close_count=%s, per_change_count=%s, ha_close=%s,"\
                      "ha_open=%s, ha_high=%s, ha_low=%s WHERE datetime=%s AND symbol=%s".format(table_name)
                cursor.execute(sql, data_tuple_add)
                cursor.close()
            else:
                cursor = conn.cursor()
                add_stock_data = ("INSERT INTO {} "
                                "(datetime, symbol, pid, resolution, open, close, high, low, volume, "
                             "ema_50, ema_100, ema_200, `BBL_14_2.0`, `BBM_14_2.0`, `BBU_14_2.0`, `BBB_14_2.0`, RSI_14,"
                             "`PSARl_0.02_0.2`,`PSARs_0.02_0.2`, `PSARaf_0.02_0.2`, `PSARr_0.02_0.2`, ISA_9, ISB_26, ITS_9,"
                             "IKS_26, ICS_26, per_change, volume_high_count, close_count, per_change_count, ha_close,"
                             "ha_open, ha_high, ha_low) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s,"
                                  "%s, %s, %s, %s, %s, %s, %s,"
                                  "%s, %s, %s, %s, %s, %s, %s,"
                                  "%s, %s, %s, %s, %s, %s, %s,"
                                  "%s, %s, %s, %s, %s, %s)").format(table_name)

                data_stock = data_tuple
                cursor.execute(add_stock_data, data_stock)
                conn.commit()

                cursor.close()
                conn.close()
        except mysql.connector.Error as err:
            conn.close()
            print(err.msg)


    def executeQuery(self, query, table_name, data_tuple):
        conn = self.connectDB()
        cursor = conn.cursor()
        data = []
        try:
            cursor.execute(query.format(table_name), data_tuple)
            data = cursor.fetchall()
        except Exception as e:
            print('Exception in fetching results:', e)
        cursor.close()
        conn.close()
        return data

    def DF2SQL(self, data, table_name):
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                               .format(user="root",
                                       pw="InOut@909",
                                       db="investing"))

        # df = pd.read_sql("select * from {}".format(table_name), engine)
        # final = pd.concat([df, data]).drop_duplicates().reset_index(drop=True)
        # print(final.head())
        # print(final.columns)
        data['datetime'] = data['datetime'].apply(lambda x: str(x))
        try:
            data.to_sql(table_name, con=engine, if_exists='append', chunksize=100, index= False)
        except Exception as e:
            print('Exception in converting DF to SQL:', e)



    def DFintoSQL(self, data, table_name):
        # print(data.columns)
        try:
            for index, row in data.iterrows():
                data_list = row.tolist()
                data_list = [x if str(x) != 'nan' else None for x in data_list]
                data_tuple = tuple(data_list)
                self.inertData(table_name, data_tuple)
        except Exception as e:
            print('Exception in converting DF to SQL:', e)


    def get_previous_data(self, table_name, symbl):
        try:
            query = "SELECT * FROM {} WHERE symbol=%s ORDER BY datetime DESC LIMIT 200".format(table_name)
            res = self.executeQuery(query, table_name, (symbl,))
            columns = ['datetime', 'symbol', 'pid', 'resolution', 'open', 'close', 'high', 'low', 'volume',
                       'EMA_50', 'EMA_100', 'EMA_200', 'BBL_14_2.0', 'BBM_14_2.0', 'BBU_14_2.0', 'BBB_14_2.0',
                       'RSI_14', 'PSARl_0.02_0.2', 'PSARs_0.02_0.2', 'PSARaf_0.02_0.2', 'PSARr_0.02_0.2', 'ISA_9',
                       'ISB_26', 'ITS_9', 'IKS_26', 'ICS_26', 'per_change', 'volume_high_count', 'close_count',
                       'per_change_count', 'ha_close', 'ha_open', 'ha_high', 'ha_low']
            df = pd.DataFrame(res, columns=columns)
            return df
        except Exception as e:
            print("Exception in getting previous data:", e)



# obj = DBOperations()
# obj.createTables()


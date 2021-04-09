import sqlite3
from sqlite3 import Error
import os
import config

class DatabaseOp:


    def create_database(self):
        """ create a database connection to a SQLite database """
        DB_FILE = os.getcwd() + '/DB/' + config.DB_Name
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


    def create_connection(self):
        DB_FILE = os.getcwd() + '/DB/' + config.DB_Name
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, conn, table_name):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        create_table_sql=''' CREATE TABLE IF NOT EXISTS {}(
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            ScrapedDate TEXT NOT NULL,
                                            ScripName TEXT NOT NULL,
                                            IndexORStocks INTEGER NOT NULL,
                                            StrikePrice TEXT NOT NULL,
                                            OptionType TEXT NOT NULL,
                                            StrTradeDateTime TEXT NOT NULL,
                                            TradeDateTime TEXT NOT NULL, 
                                            ExpiryDate text NOT NULL ,
                                            OI TEXT NOT NULL,
                                            COI TEXT NOT NULL,
                                            IV TEXT NOT NULL,
                                            VOL TEXT NOT NULL,
                                            MinuteOI TEXT NOT NULL,
                                            Flag INTEGER NOT NULL,
                                            createdDate DATETIME DEFAULT CURRENT_TIMESTAMP 
                                        );'''.format(table_name)
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            c.close()
            print("Table created successfully")
        except Error as e:
            print(e)

    def create_tableThreshold(self, conn):
        #InstrumentName, ExpiryDate, Threshold
        create_table_sql=''' CREATE TABLE IF NOT EXISTS Threshold(
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            ScripName TEXT NOT NULL,
                                            ExpiryDate text NOT NULL ,
                                            Threshold TEXT NOT NULL);'''
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            c.close()
            print("Table created successfully")
        except Error as e:
            print(e)

    def insertThreshold(self, conn, ScripName, ExpiryDate, Threshold):
        insert_table_sql = """INSERT INTO Threshold (ScripName, ExpiryDate, Threshold) VALUES(?,?,?)"""
        try:
            queryparameter = ScripName, ExpiryDate, Threshold
            c = conn.cursor()
            c.execute(insert_table_sql, queryparameter)
            conn.commit()
            # print("records inserted successfully")
        except Error as e:
            print(e)

    def updateThreshold(self, conn, ScripName, ExpiryDate, Threshold):
        insert_table_sql = """UPDATE Threshold SET Threshold=? WHERE ScripName=? AND ExpiryDate=?"""
        try:
            queryparameter = [Threshold, ScripName, ExpiryDate]
            c = conn.cursor()
            c.execute(insert_table_sql, queryparameter)
            conn.commit()
            # print("records inserted successfully")
        except Error as e:
            print(e)

    def delete(self, conn):
        create_table_sql = """ delete from stockDetails """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            conn.close()
            print("records deleted successfully")
        except Error as e:
            print(e)


    def checkInsertedRecords(self, conn,DateTime,Symbol,Resolution):
        cur = conn.cursor()
        cur.execute("SELECT id FROM stockDetails WHERE datetime = ? AND symbol= ? AND resolution=?", [DateTime,Symbol,Resolution])
        rows = cur.fetchall()
        return rows

    def insert(self, conn, ScrapedDate, ScripName, IndexORStocks, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime,
               ExpiryDate, OI, COI, IV, VOL, MOI, Flag, table_name):

        insert_table_sql="""INSERT INTO {} (ScrapedDate, ScripName,IndexORStocks,StrikePrice,OptionType,StrTradeDateTime,
                            TradeDateTime,ExpiryDate, OI, COI, IV, VOL, MinuteOI, Flag)
                          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(table_name)
        try:
            queryparameter = ScrapedDate, ScripName, IndexORStocks, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime, ExpiryDate, OI, COI, IV, VOL, MOI, Flag
            c = conn.cursor()
            c.execute(insert_table_sql, queryparameter)
            conn.commit()
            # print("records inserted successfully")
        except Error as e:
            print(e)

    # #
    # if __name__ == '__main__':
    #     #### create_database()
    #     conn= create_connection()

        # create_table(conn)
        # dropTable(conn)
        # stockMaster(conn)
        #delete(conn)
# importing rquired libraries
import mysql.connector
from datetime import datetime

LOCALMYSQL = {
        'host':'localhost',
        'user': 'root',
        'password': 'R@ting#2021',#
        'db': 'fnodb'
}

def connect2Mysql(inputDict=LOCALMYSQL):
    inputDict['cnx'] = mysql.connector.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'],password=LOCALMYSQL['password'],database=LOCALMYSQL['db'],allow_local_infile=1,autocommit=True)
    return(inputDict['cnx'])


def delete_Fno_datewise_Records(datewise):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        datewise = datetime.strptime(datewise, '%d-%m-%Y')
        query=""" delete from fno where TDate ='""" +str(datewise)+ """'"""
        mysqlCursor.execute(query)
        mysqlDB.commit()
    except Exception as e:
        print("query error==", e)
    mysqlCursor.close()
    mysqlDB.close()

def insertFno(favcopyPath,input_date):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        # delete records if already there
        delete_Fno_datewise_Records(input_date)

        query = """ LOAD DATA LOW_PRIORITY LOCAL INFILE '""" +str(favcopyPath)+"""' INTO TABLE fnodb.fno CHARACTER SET utf8 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Instrument, Symbol, @expiryDate , StrikePrice, OptionType, OpenPrice, HighPrice, LowPrice, ClosePrice, SettlementPrice, Contracts, ValueInLakh, OpenInterest, ChangeInOI, @TDate) set ExpiryDate = STR_TO_DATE(@expiryDate, '%d-%M-%Y'), TDate = STR_TO_DATE(@TDate, '%d-%M-%Y') """
        mysqlCursor.execute(query)
        mysqlDB.commit()
    except Exception as e:
        print("query error==", e)
    mysqlCursor.close()
    mysqlDB.close()

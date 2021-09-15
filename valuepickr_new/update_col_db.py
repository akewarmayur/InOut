# importing rquired libraries
import mysql.connector

LOCALMYSQL = {
        'host':'localhost',
        'user': 'root',
        'password': 'R@ting#2021',#
        'db': 'valuepickrDB'
}
def connect2Mysql(inputDict=LOCALMYSQL):
    inputDict['cnx'] = mysql.connector.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'],password=LOCALMYSQL['password'],database=LOCALMYSQL['db'])
    return(inputDict['cnx'])


def getUserDetails():
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output=[]
    try:
        mysqlCursor.callproc('getdiscuss')
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("error==", e)

    mysqlCursor.close()
    mysqlDB.close()
    return output

def updatediscussdate(tpid,datetimevalue):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        datetimevalue=datetimevalue[0]
        mysqlCursor.callproc('updateDiscussDate', [datetimevalue,tpid])
        mysqlDB.commit()
        print("Records insert successfully======")
    except Exception as e:
        print("error==", e)
    mysqlCursor.close()
    mysqlDB.close()

def convvartoDate(dateCol):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output=[]
    try:
        mysqlCursor.callproc('ConvStrToDate', [dateCol])
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("error==", e)

    mysqlCursor.close()
    mysqlDB.close()
    return output[0]


out= getUserDetails()
for row in out:
    print(row[0],row[1])
    returndate= convvartoDate(row[1])
    updatediscussdate(row[0],returndate)
    print("done")

# importing rquired libraries
import mysql.connector
import valuepickrconfig as config

LOCALMYSQL = {
        'host':'localhost',
        'user': 'root',
        'password': 'R@ting#2021',#
        'db': 'valuepickrDB'
}

def create_database():
    dataBase = mysql.connector.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'] ,password=LOCALMYSQL['password'])
    # preparing a cursor object
    cursorObject = dataBase.cursor()
    # creating database
    cursorObject.execute("CREATE DATABASE valuepickrDB")
    #print("database created")
    return

def connect2Mysql(inputDict=LOCALMYSQL):
    inputDict['cnx'] = mysql.connector.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'],password=LOCALMYSQL['password'],database=LOCALMYSQL['db'])
    return(inputDict['cnx'])

def create_table_Topic():
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor()
    # creating table
    queryCmd = """CREATE TABLE Topic (
                           TopicId INT AUTO_INCREMENT PRIMARY KEY,
                           TopicName  VARCHAR(200),
                           TopicURL VARCHAR(200),
                           CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP
                           )"""
    mysqlCursor.execute(queryCmd)
    mysqlDB.commit()
    mysqlCursor.close()
    mysqlDB.close()
    print("User Topic created")

def create_table_User():
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor()
    # creating table
    queryCmd = """CREATE TABLE User (
                           UserId INT AUTO_INCREMENT PRIMARY KEY,
                           UserName  VARCHAR(100),
                           UserCreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP
                           )"""
    mysqlCursor.execute(queryCmd)
    mysqlDB.commit()
    print("User table created")
    mysqlCursor.close()
    mysqlDB.close()

def create_table_TopicCategory():
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor()
    # creating table
    queryCmd = """CREATE TABLE TopicCategory (
                           TopicCategoryId INT AUTO_INCREMENT PRIMARY KEY,
                           TopicId INT,
                           FOREIGN KEY(TopicId) REFERENCES Topic(TopicId),
                           CategoryName  VARCHAR(200)
                           
                           )"""
    mysqlCursor.execute(queryCmd)
    mysqlDB.commit()
    print("User TopicCategory created")
    mysqlCursor.close()
    mysqlDB.close()


def create_table_TopicDiscussion():
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor()
    # creating table
    queryCmd = """CREATE TABLE TopicDiscussion (
                           TopicDiscussionId INT AUTO_INCREMENT PRIMARY KEY,
                           TopicId INT,
                           FOREIGN KEY(TopicId) REFERENCES Topic(TopicId),
                           UserId INT,
                           FOREIGN KEY(UserId) REFERENCES User(UserId),
                           DiscussionText  TEXT,
                           DiscussionDate varchar(100)

                           )"""
    mysqlCursor.execute(queryCmd)
    mysqlDB.commit()
    print("User TopicDiscussion created")
    mysqlCursor.close()
    mysqlDB.close()


def check_connection():
    print(mysql.connector.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'] ,password=LOCALMYSQL['password']))


def insertTopic(topicName, topicURL):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))

    try:
        mysqlCursor.callproc('SP_Insert_topic', [topicName, topicURL])
        mysqlDB.commit()
        # results = mysqlCursor.fetchone()
        # print(results[0])
        # if results ==1:
        #     print("Records Already exist !!")
    except Exception as e:
        print("error==", e)
    mysqlCursor.close()
    mysqlDB.close()

def getUserDetails(username):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output=[]
    try:
        mysqlCursor.callproc('getUserDetails', [username])
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("error==", e)

    mysqlCursor.close()
    mysqlDB.close()
    return output

def getReadTopic(tpname):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output=[]
    try:
        #mysqlCursor.callproc('getTopic',[tpurl,tpname])
        mysqlCursor.callproc('getTopic', [tpname])
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("error==", e)

    mysqlCursor.close()
    mysqlDB.close()
    return output

def check_topic_details(tpname):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output=[]
    try:
        mysqlCursor.callproc('checkTopic',[tpname])
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("error==", e)

    mysqlCursor.close()
    mysqlDB.close()
    return output


def insertTopicCategory(TopicId,CategoryName):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        mysqlCursor.callproc('SP_Insert_topicCategory', [TopicId,CategoryName])
        mysqlDB.commit()
    except Exception as e:
        print("error==", e)
    mysqlCursor.close()
    mysqlDB.close()

def insertTopicDiscussion(topicid,userid,discussiontext,discussiondatecpy):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        mysqlCursor.callproc('SP_Insert_TopicDiscussion', [topicid,userid,discussiontext,discussiondatecpy])
        mysqlDB.commit()
        #print("Records insert successfully======")
    except Exception as e:
        print("error==", e)
    mysqlCursor.close()
    mysqlDB.close()


def update_url(urls,url_first):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        mysqlCursor.callproc('update_url', [urls,url_first])
        mysqlDB.commit()
    except Exception as e:
        print("update error ==", e)
    mysqlCursor.close()
    mysqlDB.close()

def check_discussion_record_is_exist(topicids,userids,discdate):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output = []
    try:
        mysqlCursor.callproc('check_discussion_record', [topicids,userids,discdate])
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("update error ==", e)
    mysqlCursor.close()
    mysqlDB.close()
    return output


def insertUser(username):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    try:
        d= mysqlCursor.callproc('SP_Insert_User', [username])
        mysqlDB.commit()
        #print("Records insert successfully======")
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

def checkDiscussionDate(dateCol):
    mysqlDB = connect2Mysql(LOCALMYSQL)
    mysqlCursor = mysqlDB.cursor(LOCALMYSQL)
    mysqlCursor.execute("""use {};""".format(LOCALMYSQL['db']))
    output=[]
    try:
        mysqlCursor.callproc('checkDiscussionDate', [dateCol])
        for result in mysqlCursor.stored_results():
            output = result.fetchall()
    except Exception as e:
        print("error==", e)

    mysqlCursor.close()
    mysqlDB.close()
    return output[0]


## Check Connection
##check_connection()
## Create Database
#create_database()
#create_table_Topic()
#create_table_User()
# create_table_TopicCategory()
# create_table_TopicDiscussion()
## getReadTopic()

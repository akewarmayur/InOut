import pymysql
LOCALMYSQL = {
        'host':'137.135.52.58',
        'user': 'admin',
        'password': 'HeJMU#2021',#
        'db': 'edelweissdb',
        'OPTIONS': {
           "init_command": "SET GLOBAL max_connections = 100000"}
}


def create_connection():
    conn = None
    try:
        conn = pymysql.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'], password=LOCALMYSQL['password'],
                               database=LOCALMYSQL['db'])
    except Exception as e:
        print("Connection failed====", e)

    return conn

create_connection()

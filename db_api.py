import pymysql.cursors
import mysql.connector
import pandas as pd
# https://stackoverflow.com/questions/28981770/store-sql-result-in-a-variable-in-python

# def createMYSQLConnection():
#     try:
#         connection = mysql.connector.connect(
#             host = 'localhost',
#             user='blast', 
#             password='shift12345', 
#             database='pgmsdb')

#         cursor = connection.cursor()
#         return cursor
#     except mysql.connectorError as e:
#         print("Error reading data from MYSQL table", e)
#         return NULL
# Todo: 
# Create

# 0. Function that creates connection to the server and returns the cursor (which is used to execute statements)
def create_mysql_connection():
    connection = mysql.connector.connect(host='localhost', 
                                user='blast', 
                                password='shift12345', 
                                database='pgmsdb')

    cursor = connection.cursor()
    return cursor

def create_pymysql_connection():
    connection = pymysql.connect(host='localhost', 
                                 user='blast', 
                                 password='shift12345', 
                                 database='pgmsdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

#0.1 Closes connection
def close_connection(cursor, connection):
    try:
        cursor.close()
        connection.close()
        print("Cursor and Connection closed")
    except err:
        print("Unsuccessful closing of cursor and connection with error:", err)
    
# 1. Function that would get values of a type of data (e.g. temp, soil moisture) and indicated a sensor_idx and displays to terminal the number of rows gotten
def get_values(table_name, sensor_idx, sensor_type):
    """
    This function retrieves all values of a certain type of data (e.g. temperature, soil moisture) based on an indicated sensor type
    """
    connection = create_pymysql_connection()
    query = "select * from " + table_name + " where sensor_idx = %s AND type = %s"
    df = pd.read_sql_query(query, connection, params=[sensor_idx, sensor_type])
    return df

def get_all_values(table_name):
    connection = create_pymysql_connection()
    query = "select * from " + table_name
    df = pd.read_sql_query(query, connection)
    return df


    
    # sqlArray = []
    # with connection:
    #     with connection.cursor() as cursor:
    #         query = "SELECT * from dlsu_cherrytomato_0 WHERE sensor_idx = '0'"
    #         sqlArray = cursor.execute(query)
    #         result = cursor.fetchone()
    #         print(result)
# 2. Function gets the latest sensor data, and displays it

# 3. Converter from data to CSV or dataframe




# 4. Function that stores to the DB, adding data to the DB
def insert_data_db(data):
    cursor = create_connection()
    query = ("SELECT * from dlsu_cherrytomato_0  WHERE sensor_idx =  %s AND type = %s")
    cursor.execute(query, (sensor_idx, sensor_type))
    records = cursor.fetchall()
    print("Executed")
    i = 0
    for x in records:
        if i < 5:
            print("id:",x[0],type(x[0]))
            print("date:",x[1],type(x[1]))
            print("exp_num:", x[2],type(x[2]))
            
            print("sitename:",x[3],type(x[3]))
            print("type:",x[4],type(x[4]))
            print("idx:",x[5],type(x[5]))
            
            print("value:",x[6],type(x[6]))
            print("\n")
        i=i+ 1
    # Close connection
# def insertModelOutput(cursor, table_name, value):
#     query = f"INSERT INTO {table_name} (value) VALUES ({value})"
#     cursor.execute(query)
#     connection.commit()


df = get_values("dlsu_cherrytomato_0", "0", "temperature")
df2 = get_all_values("dlsu_cherrytomato_0")
print(df2['type'].value_counts())



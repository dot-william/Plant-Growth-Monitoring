import pymysql.cursors
import mysql.connector
import pandas as pd
# https://stackoverflow.com/questions/28981770/store-sql-result-in-a-variable-in-python

# Todo: 
# Create

def create_mysql_connection():
    """Creates a MySQL Connection and returns the cursor"""
    connection = mysql.connector.connect(host='localhost', 
                                user='blast', 
                                password='shift12345', 
                                database='pgmsdb')

    cursor = connection.cursor()
    return cursor

def create_pymysql_connection():
    """Creates a PyMySQL Connection"""
    connection = pymysql.connect(host='localhost', 
                                 user='blast', 
                                 password='shift12345', 
                                 database='pgmsdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

#0.1 Closes connection
def close_connection(cursor, connection):
    """Closes a MySQL Connection"""
    try:
        cursor.close()
        connection.close()
        print("Cursor and Connection closed")
    except err:
        print("Unsuccessful closing of cursor and connection with error:", err)
    
def get_values(connection, table_name, sensor_idx, sensor_type):
    """
    Retrieves all rows from a certain table pertaining to the given sensor index and sensor type 
    
    Args:
        connection (object): PyMySql connection
        table_name (string): name of the table to get values from
        sensor_idx (string): index of sensor
        sensor_type (string): type of sensor (e.g. temperature, soil moisture)
    Returns:
        Pandas df containing the results of the query given the parameters
    """
    df = []
    try:
        query = "select * from " + table_name + " where sensor_idx = %s AND type = %s"
        df = pd.read_sql_query(query, connection, params=[sensor_idx, sensor_type])
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df

def get_all_values(table_name):
    """
    Retrieves all rows from a certain table 
    
    Args:
        table_name (string): name of the table to get values from
    Returns:
        Pandas df containing the results of the query 
    """
    df = []
    try:
        connection = create_pymysql_connection()
        query = "select * from " + table_name
        df = pd.read_sql_query(query, connection)
    except Exception as err:
        print("Error occured:", err)
    finally:
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

connection = create_pymysql_connection()
print(type(connection))
df = get_values(connection, "dlsu_cherrytomato_0", "0", "temperature")
df2 = get_all_values("dlsu_cherrytomato_0")

if len(df) != 0:
    print(df.head())
else:
    print("empty")




import pymysql.cursors
import mysql.connector
import pandas as pd
import datetime
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
    return connection, cursor

def create_pymysql_connection():
    """Creates a PyMySQL Connection"""
    connection = pymysql.connect(host='localhost', 
                                 user='blast', 
                                 password='shift12345', 
                                 database='pgmsdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

#0.1 Closes connection
def close_mysql_connection(mysql_connection, mysql_cursor):
    """Closes a MySQL Connection"""
    try:
        mysql_cursor.close()
        mysql_connection.close()
        print("Cursor and Connection closed")
    except Exception as err:
        print("Unsuccessful closing of cursor and connection with error:", err)
    
def get_values(pymysql_connection, table_name, sensor_idx, sensor_type):
    """
    Retrieves all rows from a certain table pertaining to the given sensor index and sensor type 
    
    Args:
        pymysql_connection (object): PyMySql connection
        table_name (string): name of the table to get values from
        sensor_idx (string): index of sensor
        sensor_type (string): type of sensor (e.g. temperature, soil moisture)
    Returns:
        Pandas df containing the results of the query given the parameters
    """
    df = []
    try:
        query = "SELECT * FROM " + table_name + " WHERE sensor_idx = %s AND type = %s"
        df = pd.read_sql_query(query, pymysql_connection, params=[sensor_idx, sensor_type])
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df

def get_all_values(pymysql_connection, table_name):
    """
    Retrieves all rows from a certain table 
    
    Args:
        table_name (string): name of the table to get values from
    Returns:
        Pandas df containing the results of the query 
    """
    df = []
    try:
        query = "SELECT * FROM " + table_name
        df = pd.read_sql_query(query, pymysql_connection)
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df

# 2. Function gets the latest sensor data, and displays it
def display_latest_data(pymysql_connection, table_name, sensor_idx, sensor_type):
    try:
        query = "SELECT * FROM " + table_name + " WHERE ID=(SELECT MAX(id) FROM " + table_name + " WHERE sensor_idx = %s AND type = %s )"
        df = pd.read_sql_query(query, pymysql_connection, params=[sensor_idx, sensor_type])
        print(df)
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df

# 4. Function that stores to the table in the DB
def insert_data_table(mysql_connection, mysql_cursor, table_name, array_data):
    query = ("INSERT INTO " + table_name + " (datetime, expt_num, sitename, type, sensor_idx, value) VALUES (%s, %s, %s, %s, %s, %s)")
    for data in array_data:
        date = data["datetime"]
        expt_num = data["expt_num"]
        site_name = data["sitename"]
        type_value = data["type"]
        sensor_idx = data["index"]
        value = data["value"]
        try:
            mysql_cursor.execute(query, (date, expt_num, site_name, type_value, sensor_idx, value))
            mysql_connection.commit() 
        except Exception as err:
            print("An error has occurred:", err)
        


connection = create_pymysql_connection()
print(type(connection))
df = get_values(connection, "dlsu_cherrytomato_0", "0", "temperature")
df2 = get_all_values(connection, "dlsu_cherrytomato_0")

if len(df2) != 0:
    print(df2.head())
else:
    print("empty")

# Test sample
sample_array_dict =[{
                    'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'expt_num': 0,
                    'sitename': "DLSU_BLAST",
                    'index': 0, 
                    'value': 1,
                    'type':  "pred_ph"
                    },
                    {
                    'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'expt_num': 0,
                    'sitename': "DLSU_BLAST",
                    'index': 0, 
                    'value': 2.5,
                    'type':  "pred_moisture"
                    },
                    {
                    'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'expt_num': 0,
                    'sitename': "DLSU_BLAST",
                    'index': 0, 
                    'value': 3.1,
                    'type':  "pred_moisture"
                    },
                    {
                    'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'expt_num': 0,
                    'sitename': "DLSU_BLAST",
                    'index': 1, 
                    'value': 4.5,
                    'type':  "pred_moisture"
                    },
                    {
                    'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'expt_num': 0,
                    'sitename': "DLSU_BLAST",
                    'index': 0, 
                    'value': 5.5,
                    'type':  "pred_moisture"
                    },
                    {
                    'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'expt_num': 0,
                    'sitename': "DLSU_BLAST",
                    'index': 0, 
                    'value': 6.7,
                    'type':  "pred_moisture"
                    }] 
display_latest_data(connection, "dlsu_cherrytomato_0", "0", "solution_EC")
db, cursor = create_mysql_connection()
insert_data_table(db, cursor, "test_data_table", sample_array_dict)
close_mysql_connection(db, cursor)
print("done")
# Store data

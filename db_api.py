import pymysql.cursors
import mysql.connector
import pandas as pd
import datetime
import sqlalchemy
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

def create_engine():
    engine = sqlalchemy.create_engine('mysql+pymysql://blast:shift12345@localhost/pgmsdb')
    return engine

#0.1 Closes connection
def close_mysql_connection(mysql_connection, mysql_cursor):
    """Closes a MySQL Connection"""
    try:
        mysql_cursor.close()
        mysql_connection.close()
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

        # Preprocess before used by the model
        df.drop(['id'], axis=1, inplace=True)
        df = df.rename(columns={"sensor_idx":"index"})
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df

def get_all_preds(pymysql_connection, table_name):
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
        df.drop(['id'], axis=1, inplace=True)
        
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df
    
# 2. Function gets the latest sensor data, and displays it
def get_latest_data(pymysql_connection, table_name, sensor_idx, sensor_type):
    try:
        query = "SELECT * FROM " + table_name + " WHERE ID=(SELECT MAX(id) FROM " + table_name + " WHERE sensor_idx = %s AND type = %s )"
        df = pd.read_sql_query(query, pymysql_connection, params=[sensor_idx, sensor_type])
        df.drop(['id'], axis=1, inplace=True)
        df = df.rename(columns={"sensor_idx":"index"})
    except Exception as err:
        print("Error occured:", err)
    finally:
        return df

# 4. Function that stores to the table in the DB
def insert_many_data_table(mysql_connection, mysql_cursor, table_name, array_data):
    query = ("INSERT INTO " + table_name + " (datetime, expt_num, sitename, type, sensor_idx, value) VALUES (%s, %s, %s, %s, %s, %s)")
    for data in array_data:
        date = data["datetime"]
        expt_num = int(data["expt_num"])
        site_name = data["sitename"]
        type_value = data["type"]
        sensor_idx = int(data["index"])
        value = float(data["value"])
        try:
            mysql_cursor.execute(query, (date, expt_num, site_name, type_value, sensor_idx, value))
            mysql_connection.commit() 
        except Exception as err:
            print("An error has occurred:", err)
        
def insert_data(table_name, data):
    try:
        db, cursor = create_mysql_connection()
        query = ("INSERT INTO " + table_name + " (datetime, expt_num, sitename, type, sensor_idx, value) VALUES (%s, %s, %s, %s, %s, %s)")
        date = data["datetime"]
        expt_num = int(data["expt_num"])
        site_name = data["sitename"]
        type_value = data["type"]
        sensor_idx = int(data["index"])
        value = float(data["value"])
        cursor.execute(query, (date, expt_num, site_name, type_value, sensor_idx, value))
        db.commit() 
        close_mysql_connection(db, cursor)
    except Exception as err:
        print("An error has occurred:", err)

def insert_dli(table_name, raw_data):
    try:
        create_dli_table(table_name)
        db, cursor = create_mysql_connection()
        for data in raw_data:
            query = ("INSERT INTO " + table_name + " (datetime, expt_num, type, sensor_idx, value) VALUES (%s, %s, %s, %s, %s)")
            date = data["datetime"]
            expt_num = int(data["expt_num"])
            type_value = data["type"]
            sensor_idx = int(data["index"])
            value = float(data["value"])
            cursor.execute(query, (date, expt_num, type_value, sensor_idx, value))
            db.commit() 
        close_mysql_connection(db, cursor)
    except Exception as err:
        print("An error has occurred:", err)

def create_pred_table(table_name):
    try:
        db, cursor = create_mysql_connection()
        cursor.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (id INT AUTO_INCREMENT, datetime DATETIME, expt_num TINYINT(1), type VARCHAR(25), value FLOAT, PRIMARY KEY (id))')
        close_mysql_connection(db, cursor)
    except Exception as err:
        print("An error has occurred in creating table:", err)

def create_dli_table(table_name):
    try:
        db, cursor = create_mysql_connection()
        cursor.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (id INT AUTO_INCREMENT, datetime DATETIME, expt_num TINYINT(1), type VARCHAR(25), sensor_idx TINYINT(1), value FLOAT, PRIMARY KEY (id))')
        close_mysql_connection(db, cursor)
    except Exception as err:
        print("An error has occurred in creating table:", err)

def insert_predictions_data(table_name, raw_data):
    try:
        # Create table if does not exist
        create_pred_table(table_name)
        db, cursor = create_mysql_connection()
        for data in raw_data:
            query = ("INSERT INTO " + table_name + " (datetime, expt_num, type, value) VALUES (%s, %s, %s, %s)")
            date = data["datetime"]
            expt_num = int(data["expt_num"])
            type_value = data["type"]
            value = float(data["value"])
            cursor.execute(query, (date, expt_num, type_value, value))
            db.commit() 
        close_mysql_connection(db, cursor)
    except Exception as err:
        print("An error has occurred in inserting", err)

def insert_prediction_data(table_name, data):
    try:
        # Create table if does not exist
        create_pred_table(table_name)
        db, cursor = create_mysql_connection()
        query = ("INSERT INTO " + table_name + " (datetime, expt_num, type, value) VALUES (%s, %s, %s, %s)")
        date = data["datetime"]
        expt_num = int(data["expt_num"])
        type_value = data["type"]
        value = float(data["value"])
        cursor.execute(query, (date, expt_num, type_value, value))
        db.commit() 
        close_mysql_connection(db, cursor)
    except Exception as err:
        print("An error has occurred in inserting", err)



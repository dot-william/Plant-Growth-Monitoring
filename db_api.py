import pymysql.cursors

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
# 0. Function that creates connection to the server

# 1. Function that would get values of a type of data (e.g. temp, soil moisture) and indicated a sensor_idx and displays to terminal the number of rows gotten
def getValues(table_name, sensor_idx, type):

    query = "SELECT * from %s WHERE (sensor_idx = %s AND type = %s  ORDER BY id ASC"
    with pymysql.connect(host='localhost', user='blast', password='shift12345', database='pgmsdb') as conn:
        c = conn.cursor()
        sqlArray = c.execute(query, (table_name, sensor_idx, type))
  
    return sqlArray
# 2. Function gets the latest sensor data, and displays it
# 3. Converter from data to CSV or dataframe
# 4. Function that stores to the DB, adding data to the DB
# def insertModelOutput(cursor, table_name, value):
#     query = f"INSERT INTO {table_name} (value) VALUES ({value})"
#     cursor.execute(query)
#     connection.commit()


values = getValues("test_data_table", "8", "temperature")
print(values)
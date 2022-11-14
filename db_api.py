import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user='blast', 
    password='shift12345', 
    database='pgmsdb')

mycusor = db.cursor()


print("Hello world!")
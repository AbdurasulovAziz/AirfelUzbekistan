import mysql.connector
from bot_create import dotenv

mydb = mysql.connector.connect(
    host=dotenv['DATABASE_HOST'],
    user=dotenv['DATABASE_USER'],
    password=dotenv['DATABASE_PASS'],
    database=dotenv['DATABASE']
)
mydb.reconnect(attempts=10, delay=0)

cursor = mydb.cursor()

mydb.commit()

import mysql.connector
from bot_create import dotenv

mydb = mysql.connector.connect(
    host=dotenv['DATABASE_HOST'],
    user=dotenv['DATABASE_USER'],
    password=dotenv['DATABASE_PASS'],
    database=dotenv['DATABASE']
)

mydb.ping(reconnect=True)

cursor = mydb.cursor()

mydb.commit()

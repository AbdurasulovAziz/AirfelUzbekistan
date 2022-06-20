import mysql.connector
from bot_create import dotenv

mydb = mysql.connector.connect(
    host=dotenv['DATABASE_HOST'],
    user=dotenv['DATABASE_USER'],
    password=dotenv['DATABASE_PASS'],
    database=dotenv['DATABASE']
)

cursor = mydb.cursor()

cursor.execute('''TRUNCATE TABLE `masters`''')



mydb.commit()

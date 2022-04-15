from .cfg import *
import mysql.connector
import random


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=sql_pass,
    database="friend_test"
)

mycursor = mydb.cursor()


def get_email_user(email):
    mycursor.execute(f"SELECT * FROM users_customuser WHERE email='{email}'")
    myresult = mycursor.fetchall()
    confirm_code = random.randint(1000, 9999)
    sql = "UPDATE users_customuser SET telegram_confirm_code = %s WHERE email = %s"
    val = (confirm_code, email)
    mycursor.execute(sql, val)
    mydb.commit()
    return confirm_code
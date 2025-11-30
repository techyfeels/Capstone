import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="211213fk",
        database="capstone_mod1"
    )

    return conn
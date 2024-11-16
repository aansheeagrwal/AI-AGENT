import mysql.connector

# Database connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aa@24042004",
    database="my_database"
)

if conn.is_connected():
    print("Connected to MySQL database: my_database")
else:
    print("Connection failed")

# Cursor for executing queries
cursor = conn.cursor()

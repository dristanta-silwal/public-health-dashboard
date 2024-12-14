import os
import psycopg2

connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()
cursor.execute("SELECT version();")
db_version = cursor.fetchone()
print(f"Connected to: {db_version[0]}")

cursor.close()
connection.close()

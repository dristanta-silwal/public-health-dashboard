import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def initialize_table():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS health_records (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(80) NOT NULL,
                    age INT NOT NULL,
                    condition TEXT NOT NULL
                );
            """)
            connection.commit()
            cursor.close()
            connection.close()
            print("Database table 'health_records' initialized.")
    except Exception as e:
        print(f"Failed to initialize table: {e}")

@app.route("/")
def index():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM health_records ORDER BY id;")
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("index.html", records=records)
    except Exception as e:
        return render_template("error.html", error_message=str(e))

@app.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        condition = request.form["condition"]
        try:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO health_records (name, age, condition) VALUES (%s, %s, %s);",
                    (name, age, condition),
                )
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for("index"))
        except Exception as e:
            return render_template("error.html", error_message=str(e))
    return render_template("add_record.html")

@app.route("/edit/<int:record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    try:
        connection = get_db_connection()
        if request.method == "POST":
            name = request.form["name"]
            age = request.form["age"]
            condition = request.form["condition"]
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE health_records SET name=%s, age=%s, condition=%s WHERE id=%s;",
                (name, age, condition, record_id),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for("index"))
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM health_records WHERE id = %s;", (record_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template("edit_record.html", record=record)
    except Exception as e:
        return render_template("error.html", error_message=str(e))

@app.route("/delete/<int:record_id>", methods=["GET", "POST"])
def delete_record(record_id):
    try:
        connection = get_db_connection()
        if request.method == "POST":
            cursor = connection.cursor()
            cursor.execute("DELETE FROM health_records WHERE id = %s;", (record_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for("index"))
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM health_records WHERE id = %s;", (record_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template("delete_confirm.html", record=record)
    except Exception as e:
        return render_template("error.html", error_message=str(e))
    

if __name__ == "__main__":
    initialize_table()
    app.run(debug=True, host="0.0.0.0", port=5000)

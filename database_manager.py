import mysql.connector
import pandas as pd

class DatabaseManager:
    def __init__(self, host="localhost", user="week9user", password="MyPassword123", database="week9_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor(dictionary=True)

            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.conn.database = self.database
            self._ensure_schema()
        except Exception as e:
            print("Error connecting to MySQL:", e)

    def _ensure_schema(self):
        if self.conn is None:
            return
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password_hash VARCHAR(255),
            role VARCHAR(20)
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            incident_id VARCHAR(50) UNIQUE,
            date DATE,
            category VARCHAR(50),
            subcategory VARCHAR(50),
            severity VARCHAR(20),
            status VARCHAR(20),
            assigned_to VARCHAR(50),
            resolution_time_hours FLOAT,
            description TEXT
        )""")
        self.conn.commit()

    def add_user(self, username, password_hash, role="analyst"):
        sql = "INSERT INTO users (username, password_hash, role) VALUES (%s,%s,%s)"
        self.cursor.execute(sql, (username, password_hash, role))
        self.conn.commit()

    def get_user(self, username):
        sql = "SELECT * FROM users WHERE username=%s"
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone()

    def insert_incident(self, incident):
        sql = """INSERT INTO cyber_incidents
        (incident_id, date, category, subcategory, severity, status, assigned_to, resolution_time_hours, description)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        self.cursor.execute(sql, (
            incident["incident_id"],
            incident["date"],
            incident["category"],
            incident["subcategory"],
            incident["severity"],
            incident["status"],
            incident["assigned_to"],
            incident["resolution_time_hours"],
            incident["description"]
        ))
        self.conn.commit()

    def get_all_incidents(self):
        self.cursor.execute("SELECT * FROM cyber_incidents ORDER BY date DESC")
        return self.cursor.fetchall()

    def get_incident_by_id(self, id_):
        sql = "SELECT * FROM cyber_incidents WHERE id=%s"
        self.cursor.execute(sql, (id_,))
        return self.cursor.fetchone()

    def update_incident(self, id_, fields):
        cols = ", ".join([f"{k}=%s" for k in fields.keys()])
        vals = list(fields.values()) + [id_]
        sql = f"UPDATE cyber_incidents SET {cols} WHERE id=%s"
        self.cursor.execute(sql, vals)
        self.conn.commit()

    def delete_incident(self, id_):
        sql = "DELETE FROM cyber_incidents WHERE id=%s"
        self.cursor.execute(sql, (id_,))
        self.conn.commit()

    def to_pandas(self):
        return pd.read_sql("SELECT * FROM cyber_incidents", con=self.conn)

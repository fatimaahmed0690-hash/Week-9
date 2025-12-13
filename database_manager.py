import mysql.connector

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="week9user",
                password="MyPassword123",
                database="week9_cyber_db"
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Database connected")

        except mysql.connector.Error as e:
            print("Database error:", e)
            self.connection = None
            self.cursor = None

    def get_user(self, username):
        if self.cursor is None:
            return None
        sql = "SELECT * FROM users WHERE username=%s"
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone()

    def add_user(self, username, password):
        if self.cursor is None:
            return False
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(sql, (username, password))
        self.connection.commit()
        return True

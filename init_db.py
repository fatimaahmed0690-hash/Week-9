import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="week9user",
    password="MyPassword123",
    database="week9_cyber_db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
)
""")

conn.commit()
conn.close()

print(" Database ready successfully")

from database_manager import DatabaseManager
from auth import register_user
import pandas as pd

db = DatabaseManager(user="week9user", password="MyPassword123", database="week9_db")

if not db.get_user("admin"):
    register_user("admin", "admin123", role="admin")

db.cursor.execute("DELETE FROM cyber_incidents")
db.conn.commit()

df = pd.read_csv("data/cyber_incidents_sample.csv")
for _, row in df.iterrows():
    incident = {
        "incident_id": row["incident_id"],
        "date": row["date"],
        "category": row["category"],
        "subcategory": row["subcategory"],
        "severity": row["severity"],
        "status": row["status"],
        "assigned_to": row["assigned_to"],
        "resolution_time_hours": row["resolution_time_hours"],
        "description": row["description"]
    }
    db.insert_incident(incident)

print("Database initialized successfully!")

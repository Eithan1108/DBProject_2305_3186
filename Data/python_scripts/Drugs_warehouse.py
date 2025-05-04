import psycopg2
import random
from datetime import time

# חיבור לדאטהבייס
conn = psycopg2.connect(
    host="localhost",
    port="5432",  # לא 5050!
    database="mydatabase",
    user="eitan",  # או המשתמש שלך
    password="ekfl2345"
)
cur = conn.cursor()

# יצירת 400 רשומות
data = []
for i in range(1, 401):
    has_frozen = random.choice([True, False])
    hour = random.randint(6, 20)
    minute = random.randint(0, 59)
    audit_time = time(hour, minute)
    data.append((i, has_frozen, audit_time))

# הכנסת הנתונים
insert_query = """
INSERT INTO Drugs_warehouse (warehouse_id, has_frozen_area, daily_drug_audit_time)
VALUES (%s, %s, %s)
"""
cur.executemany(insert_query, data)

# שמירת השינויים וסגירה
conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 rows into Drugs_warehouse successfully.")

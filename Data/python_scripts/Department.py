import psycopg2
import random

# שמות מחלקות אפשריים לדוגמה
base_names = [
    "Emergency", "Surgery", "Pediatrics", "Cardiology", "Neurology", "Orthopedics",
    "Oncology", "ICU", "Internal Medicine", "Dermatology", "Psychiatry", "Radiology",
    "Maternity", "Geriatrics", "ENT", "Urology", "Gastroenterology", "Rehabilitation"
]

# חיבור לבסיס הנתונים
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

# יצירת 400 מחלקות
data = []
for i in range(1, 401):
    name = random.choice(base_names)
    emergency_level = random.randint(1, 5)
    data.append((i, name, emergency_level))

# הכנסת הנתונים
insert_query = """
INSERT INTO department (department_id, name, emergency_level)
VALUES (%s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 departments into 'department' table.")

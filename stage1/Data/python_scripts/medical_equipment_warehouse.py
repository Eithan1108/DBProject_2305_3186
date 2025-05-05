import psycopg2
import random

# חיבור לבסיס הנתונים
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",  # או מה שהגדרת
    password="ekfl2345"
)
cur = conn.cursor()

# יצירת רשומות בטווח 401–800
data = []
for i in range(401, 801):
    storage_place = round(random.uniform(100.0, 2000.0), 2)  # נפח אחסון סביר
    stock_period = random.randint(1, 12)  # מספר חודשי מלאי
    data.append((i, storage_place, stock_period))

# הכנסה לטבלת medical_equipment_warehouse
insert_query = """
INSERT INTO medical_equipment_warehouse (warehouse_id, storage_place, stock_period)
VALUES (%s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 rows into medical_equipment_warehouse with IDs 401–800.")

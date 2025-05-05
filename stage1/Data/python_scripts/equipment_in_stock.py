import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

data = []
used_keys = set()

# נכניס 3 מחסנים לכל ציוד רפואי
for equipment_id in range(1, 401):
    for _ in range(3):
        warehouse_id = random.randint(400, 800)
        key = (equipment_id, warehouse_id)
        if key in used_keys:
            continue
        used_keys.add(key)

        amount = random.randint(1, 50)
        data.append((equipment_id, warehouse_id, amount))

# הכנסת הנתונים
insert_query = """
INSERT INTO equipment_in_stock (medical_equipment_id, warehouse_id, amount)
VALUES (%s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {len(data)} rows into equipment_in_stock.")

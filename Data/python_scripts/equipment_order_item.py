import csv
import psycopg2
import random

CSV_FILE_PATH = "data-1745434140672.csv"

order_pairs = []
with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        order_id = int(row['order_id'])
        department_id = int(row['department_id'])
        order_pairs.append((order_id, department_id))

order_pairs = order_pairs[:400]

statuses = ["pending", "approved", "delivered"]

# יצירת הנתונים
data = []
for order_id, department_id in order_pairs:
    medical_equipment_id = random.randint(1, 400)
    is_urgent = random.choice([True, False])
    amount = random.randint(1, 20)
    need_to_be_built = random.choice([True, False]) if medical_equipment_id < 50 else False
    status = random.choice(statuses)
    data.append((medical_equipment_id, order_id, department_id, is_urgent, amount, need_to_be_built, status))

# הכנסת הנתונים לדאטהבייס
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

insert_query = """
INSERT INTO equipment_order_item (medical_equipment_id, order_id, department_id, is_urgent, amount, need_to_be_built, status)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 rows into equipment_order_item.")

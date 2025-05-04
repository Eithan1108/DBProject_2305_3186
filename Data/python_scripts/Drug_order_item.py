import csv
import psycopg2
import random

# הגדרת הקובץ שלך – ודא שהנתיב נכון!
CSV_FILE_PATH = "data-1745434140672.csv"

# קריאת הצמדים מתוך הקובץ
order_pairs = []
with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        order_id = int(row['order_id'])
        department_id = int(row['department_id'])
        order_pairs.append((order_id, department_id))

# נוודא שיש רק 400
order_pairs = order_pairs[:400]

# הגדרת סטטוסים
statuses = ["pending", "approved", "delivered"]

# יצירת 400 רשומות
data = []
for order_id, department_id in order_pairs:
    drug_id = random.randint(1, 400)
    amount = random.randint(10, 200)
    is_urgent = random.choice([True, False])
    status = random.choice(statuses)
    data.append((order_id, department_id, drug_id, amount, is_urgent, status))

# חיבור והכנסה לדאטהבייס
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

insert_query = """
INSERT INTO Drug_order_item (order_id, department_id, drug_id, amount, is_urgent, status)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 rows into Drug_order_item.")

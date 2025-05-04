import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

data = []
used_keys = set()  # לוודא שאין כפילויות במפתח המשולב

# נייצר 3 מופעים לכל תרופה – עם מחסנים ותאריכים שונים
for drug_id in range(1, 401):
    for _ in range(3):
        warehouse_id = random.randint(1, 400)
        since = datetime.today() - timedelta(days=random.randint(1, 1000))
        since_str = since.date()

        # בדיקה שאין כפילות של שילוב מפתח
        key = (drug_id, warehouse_id, since_str)
        if key in used_keys:
            continue
        used_keys.add(key)

        amount = random.randint(10, 500)
        data.append((drug_id, warehouse_id, since_str, amount))

# הכנסת הנתונים
insert_query = """
INSERT INTO Drug_in_stock (drug_id, warehouse_id, since, amount)
VALUES (%s, %s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {len(data)} rows into Drug_in_stock.")

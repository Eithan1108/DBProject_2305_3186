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

for i in range(1, 401):
    department_id = random.randint(1, 400)
    order_date = datetime.today() - timedelta(days=random.randint(0, 730))  # עד שנתיים אחורה
    data.append((i, department_id, order_date.date()))

insert_query = """
INSERT INTO "Order" (order_id, department_id, order_date)
VALUES (%s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 orders into Order table.")

import psycopg2
import random

# ניצור 1–3 מחלקות לכל עובד לוגיסטיקה
data = []
used_pairs = set()

for worker_id in range(1, 401):
    for _ in range(random.randint(1, 3)):
        dept_id = random.randint(1, 400)
        key = (worker_id, dept_id)
        if key in used_pairs:
            continue
        used_pairs.add(key)
        hours = random.randint(5, 40)
        data.append((worker_id, dept_id, hours))

# הכנסת לדאטהבייס
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

insert_query = """
INSERT INTO works_for (logistic_worker_id, department_id, hours)
VALUES (%s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {len(data)} rows into works_for.")

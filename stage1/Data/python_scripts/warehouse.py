import psycopg2
from faker import Faker
import random

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port="5432",  # תיקון כאן!
    database="mydatabase",
    user="eitan",  # או שם היוזר שלך
    password="ekfl2345"   # הסיסמה שאתה יודע
)
cur = conn.cursor()

data = []
for i in range(401, 801):
    name = fake.bothify(text='??-###').upper()
    location = fake.street_address()
    active_hours = str(round(random.uniform(2.0, 12.0), 1))
    data.append((i, name, location, active_hours))

insert_query = "INSERT INTO warehouse (warehouse_id, name, location, active_hours) VALUES (%s, %s, %s, %s)"
cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()
print("✅ Inserted 400 rows successfully.")

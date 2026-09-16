import os
import random
import psycopg2
from dotenv import load_dotenv
from faker import Faker

load_dotenv()
fake = Faker()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
cur = conn.cursor()

NUM_CUSTOMERS = 50

customer_ids = []
for _ in range(NUM_CUSTOMERS):
    cur.execute(
        "INSERT INTO customers (name, email, join_date, region) VALUES (%s, %s, %s, %s) RETURNING customer_id",
        (fake.name(), fake.unique.email(), fake.date_between(start_date='-3y', end_date='today'), random.choice(['APAC', 'EMEA', 'AMER']))
    )
    customer_ids.append(cur.fetchone()[0])

account_ids = []
for cid in customer_ids:
    for _ in range(random.randint(1, 2)):
        cur.execute(
            "INSERT INTO accounts (customer_id, account_type, balance, opened_date) VALUES (%s, %s, %s, %s) RETURNING account_id",
            (cid, random.choice(['savings', 'checking']), round(random.uniform(100, 50000), 2), fake.date_between(start_date='-3y', end_date='today'))
        )
        account_ids.append(cur.fetchone()[0])

for aid in account_ids:
    for _ in range(random.randint(5, 20)):
        amount = round(random.uniform(5, 5000), 2)
        risk = 'high' if random.random() < 0.05 else 'low'
        cur.execute(
            "INSERT INTO transactions (account_id, amount, transaction_time, transaction_type, risk_flag) VALUES (%s, %s, %s, %s, %s)",
            (aid, amount, fake.date_time_between(start_date='-1y', end_date='now'), random.choice(['debit', 'credit', 'transfer']), risk)
        )

for cid in random.sample(customer_ids, k=int(NUM_CUSTOMERS * 0.3)):
    cur.execute(
        "INSERT INTO loans (customer_id, amount, status, interest_rate, issue_date) VALUES (%s, %s, %s, %s, %s)",
        (cid, round(random.uniform(1000, 50000), 2), random.choice(['active', 'paid_off', 'defaulted']), round(random.uniform(3, 12), 2), fake.date_between(start_date='-3y', end_date='today'))
    )

conn.commit()
cur.close()
conn.close()
print("Synthetic data generated successfully!")
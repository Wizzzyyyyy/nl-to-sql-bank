import os
import re
import psycopg2
from dotenv import load_dotenv
from nl_to_sql import nl_to_sql

load_dotenv()

def clean_sql(sql):
    # strips ```sql / ``` wrapping if the model adds it despite instructions
    sql = re.sub(r"^```sql\s*|^```\s*|```$", "", sql.strip(), flags=re.MULTILINE)
    return sql.strip()

def execute_sql(sql):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    cur = conn.cursor()
    cur.execute(sql)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return columns, rows

def ask(question):
    raw_sql = nl_to_sql(question)
    sql = clean_sql(raw_sql)
    print("Question:", question)
    print("Generated SQL:", sql)
    try:
        columns, rows = execute_sql(sql)
        print("Columns:", columns)
        for row in rows:
            print(row)
    except Exception as e:
        print("Execution failed:", e)

if __name__ == "__main__":
    ask("What's the credit score of each customer?")
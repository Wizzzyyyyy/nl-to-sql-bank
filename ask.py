import os
import re
import psycopg2
from dotenv import load_dotenv
from nl_to_sql import nl_to_sql

load_dotenv()

def clean_sql(sql):
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
    try:
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        return columns, rows
    finally:
        cur.close()
        conn.close()

def ask(question):
    raw_sql = nl_to_sql(question)
    sql = clean_sql(raw_sql)
    print("Question:", question)
    print("Generated SQL:", sql)

    if not sql.strip().upper().startswith("SELECT"):
        print("⚠️ Refusing to run this — it doesn't look like a SELECT query.")
        return

    try:
        columns, rows = execute_sql(sql)
    except psycopg2.Error as e:
        print(f"⚠️ Couldn't run that query — it may reference a column or table that doesn't exist. ({e.pgerror or e})")
        return
    except Exception as e:
        print(f"⚠️ Something went wrong: {e}")
        return

    if not rows:
        print("No results found for that question.")
        return

    print("Columns:", columns)
    for row in rows:
        print(row)

if __name__ == "__main__":
    ask("Who is the youngest customer?")
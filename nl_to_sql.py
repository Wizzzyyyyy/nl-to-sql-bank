import os
import time
from dotenv import load_dotenv
from google import genai
import sqlglot

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SCHEMA = """
customers(customer_id, name, email, join_date, region)
accounts(account_id, customer_id, account_type, balance, opened_date)
transactions(transaction_id, account_id, amount, transaction_time, transaction_type, risk_flag) -- risk_flag is TEXT with values 'low' or 'high', never boolean
loans(loan_id, customer_id, amount, status, interest_rate, issue_date)
"""

def nl_to_sql(question, history=None, max_retries=3):
    history_text = ""
    if history:
        history_text = "Previous conversation:\n" + "\n".join(
            f'Q: {h["question"]}\nSQL: {h["sql"]}' for h in history[-2:]
        )

    prompt = f"""You are a SQL expert. Given this PostgreSQL schema:

{SCHEMA}

{history_text}

Write ONE PostgreSQL SELECT query that answers this new question:
"{question}"

If the new question references something from the previous conversation (like "that", "them", or a follow-up filter), use that context.

Rules:
- Output ONLY the raw SQL query — no explanation, no markdown, no backticks.
- Only use SELECT statements, never write/update/delete anything.
"""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"Model busy, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise

def is_select_only(sql):
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
    except Exception:
        return False
    return parsed.key.upper() == "SELECT"

def explain_result(question, columns, rows):
    if not rows:
        return "No results were found for this question."
    preview = rows[:10]
    prompt = f"""A user asked: "{question}"
The database returned these results (columns: {columns}):
{preview}

Write a single, clear sentence in plain English answering the user's question based on this data. Do not mention SQL or databases.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text.strip()

if __name__ == "__main__":
    question = "What's the total value of transactions flagged as high-risk in the last 30 days?"
    sql = nl_to_sql(question)
    print("Question:", question)
    print("Generated SQL:", sql)
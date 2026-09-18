import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SCHEMA = """
customers(customer_id, name, email, join_date, region)
accounts(account_id, customer_id, account_type, balance, opened_date)
transactions(transaction_id, account_id, amount, transaction_time, transaction_type, risk_flag)
loans(loan_id, customer_id, amount, status, interest_rate, issue_date)
"""

def nl_to_sql(question, max_retries=3):
    prompt = f"""You are a SQL expert. Given this PostgreSQL schema:

{SCHEMA}

Write ONE PostgreSQL SELECT query that answers this question:
"{question}"

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
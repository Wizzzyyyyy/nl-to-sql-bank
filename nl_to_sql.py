import os 
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

def nl_to_sql(question):
	prompt = f"""You are a SQL expert.Given this PostgreSQL schema:

{SCHEMA}

Write ONE PostgreSQL SELECT query that answers this question:
"{question}"

Rules:
- Output ONLY the raw SQL query - no explanation, no markdown, no backticks.
- Only use SELECT statements, never write/update/delete anything.
"""
	response = client.models.generate_content(
		model="gemini-3.6-flash",
		contents = prompt
	)
	return response.text.strip()

if __name__ == "__main__":
	question = "What's the total value of transactions flagged as high-risk in the last 30 days?"
	sql = nl_to_sql(question)
	print("Question:", question)
	print("Generated SQL:", sql)
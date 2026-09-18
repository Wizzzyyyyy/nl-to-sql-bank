from nl_to_sql import nl_to_sql

questions = [
	"What's the total value of transactions flagged as high-risk in the last 30 days?",
    "Which region has the most customers?",
    "List the top 5 customers by total transaction amount.",
    "How many accounts does each customer have?",
    "What is the average loan interest rate for defaulted loans?",
]

for q in questions:
	print("=" * 60)
	print("Q:", q)
	sql = nl_to_sql(q)
	print("SQL:", sql)
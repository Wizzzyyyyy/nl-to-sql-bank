from nl_to_sql import nl_to_sql, is_select_only
from ask import clean_sql, execute_sql

questions = [
    "What's the average account balance for savings accounts only?",
    "How many transactions happened on a Saturday or Sunday?",
    "Which customer has the highest single transaction?",
    "What's the total loan amount for defaulted loans only?",
    "List the 3 most recent loans issued.",
    "Show me customers who joined in 2025.",
    "What's the smallest transaction amount for each transaction type?",
    "Find accounts with a balance between 10000 and 20000.",
    "How many distinct account types are there?",
    "Which customer's accounts have the highest combined balance, and how many accounts do they have?",
    "What percentage of customers are from the EMEA region?",
    "Show me the oldest account for each customer.",
    "List transactions with no risk flag set.",
    "How many customers have an email ending in '.org'?",
    "What's the median transaction amount?",
]

for q in questions:
    print("=" * 70)
    print("Q:", q)
    sql = clean_sql(nl_to_sql(q))
    print("SQL:", sql)
    if not is_select_only(sql):
        print("BLOCKED: not a SELECT")
        continue
    try:
        columns, rows = execute_sql(sql)
        print("Columns:", columns)
        for r in rows[:10]:
            print(r)
        if len(rows) > 10:
            print(f"... ({len(rows)} rows total)")
    except Exception as e:
        print("Execution failed:", e)
import csv
import os
from datetime import datetime

LOG_FILE = "audit_log.csv"

def log_query(question, sql, status, row_count=None):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "question", "generated_sql", "status", "row_count"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), question, sql, status, row_count])
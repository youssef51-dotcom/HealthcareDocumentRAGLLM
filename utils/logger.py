from datetime import datetime

LOG_FILE = "llm_logs.txt"

def log(step: str, data):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"{datetime.now()} - {step}\n")
        f.write("-"*80 + "\n")
        f.write(str(data) + "\n")
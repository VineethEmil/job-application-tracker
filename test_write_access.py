import os, datetime
BASE_DIR = r"E:\Github_Projects\Job_Automation\job-application-tracker"
LOG_PATH = os.path.join(BASE_DIR, "test_output.txt")

with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"Ran at {datetime.datetime.now()}\n")

print("✅ Write success:", LOG_PATH)
import os, datetime, time
from dotenv import dotenv_values
from auto_update_jobs import push_jobs_to_sheet

BASE_DIR = r"E:\Github_Projects\Job_Automation\job-application-tracker"
LOG_PATH = os.path.join(BASE_DIR, "task_log.txt")
ENV_PATH = os.path.join(BASE_DIR, ".env")

def log(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

env = dotenv_values(ENV_PATH)
for k, v in env.items():
    os.environ[k] = v

interval = int(os.getenv("POLL_INTERVAL_MINUTES", 15))

if __name__ == "__main__":
    try:
        log("Task started.")
        push_jobs_to_sheet("data analyst", "India", 3)
        log("Job fetch success.")
    except Exception as e:
        log(f"Error: {e}")
    time.sleep(10)
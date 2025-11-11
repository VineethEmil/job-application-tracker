from job_fetcher import fetch_jobs
from gsheet_client import GoogleSheetClient
from datetime import datetime
import os

HISTORY_LOG = os.path.join(os.path.dirname(__file__), "run_history.log")

def push_jobs_to_sheet(keyword="data analyst", location="India", limit=5):
    gs = GoogleSheetClient()
    jobs = fetch_jobs(keyword, location, limit)

    if not jobs:
        print("No jobs fetched.")
        return

    # Add timestamp
    for job in jobs:
        job["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_count = gs.add_entries(jobs)
    if new_count:
        print(f"✅ {new_count} new jobs added to Google Sheet.")

    with open(HISTORY_LOG, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] Added {new_count} new jobs.\n")

if __name__ == "__main__":
    push_jobs_to_sheet("data analyst", "India", 3)

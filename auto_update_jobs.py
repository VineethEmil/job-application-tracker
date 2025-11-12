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
        with open(HISTORY_LOG, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] No jobs fetched.\n")
        return

    rows = []
    for job in jobs:
        date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_id = job.get("Job_ID") or f"{job.get('Company','')}_{job.get('Role','')}_{job.get('Link','')}".replace(" ", "").lower()
        new_row = [
            date_today,
            job.get("Company", ""),
            job.get("Role", ""),
            job.get("Source", ""),
            job.get("Application_Status", ""),
            job.get("Link", ""),
            job.get("Notes", ""),
            job_id
        ]
        rows.append(new_row)

    # Use batch add_entries and get count
    new_count = gs.add_entries(rows)
    print(f"✅ {new_count} new jobs added to Google Sheet.")

    with open(HISTORY_LOG, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] Added {new_count} new jobs.\n")


if __name__ == "__main__":
    push_jobs_to_sheet("data analyst", "India", 3)
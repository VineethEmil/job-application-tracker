import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetClient:
    def __init__(self):
        load_dotenv()
        creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
        sheet_name = os.getenv("SHEET_NAME")

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name).sheet1

    def get_existing_job_ids(self):
        """Fetch all Job_IDs already in the sheet."""
        data = self.sheet.get_all_records()
        return {row.get("Job_ID") for row in data if "Job_ID" in row}

    def add_entries(self, jobs):
        """Append only new job rows."""
        existing_ids = self.get_existing_job_ids()
        new_jobs = [job for job in jobs if job["Job_ID"] not in existing_ids]

        if not new_jobs:
            print("✅ No new jobs to add — all duplicates skipped.")
            return 0

        for job in new_jobs:
            row = [
                job.get("Date"),
                job.get("Company"),
                job.get("Role"),
                job.get("Source"),
                job.get("Application_Status"),
                job.get("Link"),
                job.get("Notes"),
                job.get("Job_ID")
            ]
            self.sheet.append_row(row)
        return len(new_jobs)

    def clear(self):
        self.sheet.clear()
        self.sheet.append_row(["Date", "Company", "Role", "Source", "Application_Status", "Link", "Notes", "Job_ID"])

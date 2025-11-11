from datetime import datetime
from gsheet_client import GoogleSheetClient

gs = GoogleSheetClient()

def add_job_entry(company, role, source, status, link="", notes=""):
    date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [date_today, company, role, source, status, link, notes]
    gs.add_entry(new_row)
    print(f"✅ Added: {company} — {role}")

if __name__ == "__main__":
    add_job_entry("Amazon", "Logistics Associate", "Indeed", "Applied", "https://www.indeed.com/job", "Testing modular insert")

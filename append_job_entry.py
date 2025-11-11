import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
sheet_name = os.getenv("SHEET_NAME")

# Setup Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)
sheet = client.open(sheet_name).sheet1

def add_job_entry(company, role, source, status, link="", notes=""):
    date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [date_today, company, role, source, status, link, notes]
    sheet.append_row(new_row)
    print(f"✅ Job entry added for {company} — {role}")

# Example test entry
if __name__ == "__main__":
    add_job_entry(
        company="Flipkart",
        role="Operations Analyst",
        source="LinkedIn",
        status="Applied",
        link="https://www.linkedin.com/jobs/view/",
        notes="Initial test entry"
    )

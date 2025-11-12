import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

class GoogleSheetClient:
    def __init__(self):
        load_dotenv()

        # Try to read credentials from GitHub Actions secret
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        if creds_json:
            # Parse directly from secret string
            creds_dict = json.loads(creds_json)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        elif creds_path and os.path.exists(creds_path):
            # Fallback for local .env usage
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        else:
            raise FileNotFoundError("No valid Google Sheets credentials found.")

        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(os.getenv("SHEET_NAME")).sheet1

    def add_entry(self, row_data):
        self.sheet.append_row(row_data)

    def get_all(self):
        return self.sheet.get_all_records()

    def clear(self):
        self.sheet.clear()
        self.sheet.append_row([
            "Date", "Company", "Role", "Source",
            "Application_Status", "Link", "Notes", "Job_ID"
        ])

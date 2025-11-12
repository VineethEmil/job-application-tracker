import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

class GoogleSheetClient:
    def __init__(self):
        load_dotenv()

        # Read credentials either from secret JSON or path
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        if creds_json:
            creds_dict = json.loads(creds_json)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        elif creds_path and os.path.exists(creds_path):
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        else:
            raise FileNotFoundError("No valid Google Sheets credentials found. Set GOOGLE_SHEETS_CREDENTIALS or GOOGLE_SHEETS_CREDENTIALS_PATH.")

        self.client = gspread.authorize(creds)
        sheet_name = os.getenv("SHEET_NAME")
        if not sheet_name:
            raise EnvironmentError("SHEET_NAME environment variable not set.")
        self.sheet = self.client.open(sheet_name).sheet1

    def add_entry(self, row_data):
        """Append a single row (list) to the sheet."""
        self.sheet.append_row(row_data)
        return 1

    def add_entries(self, rows):
        """Append multiple rows. Returns number of rows appended.
        Uses append_row in a loop to preserve compatibility with gspread.
        """
        count = 0
        for row in rows:
            # ensure row is a list
            if not isinstance(row, (list, tuple)):
                raise TypeError("Each row must be a list or tuple.")
            self.sheet.append_row(row)
            count += 1
        return count

    def get_all(self):
        return self.sheet.get_all_records()

    def clear(self):
        self.sheet.clear()
        self.sheet.append_row(["Date", "Company", "Role", "Source", "Application_Status", "Link", "Notes", "Job_ID"])

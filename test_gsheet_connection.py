import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access values from .env
creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
sheet_name = os.getenv("SHEET_NAME")

# Define scope for Sheets and Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authorize and connect
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Open the target sheet
sheet = client.open(sheet_name).sheet1

# Fetch headers only
headers = sheet.row_values(1)
print("✅ Headers fetched successfully:")
print(headers)
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Load credentials from the JSON key file
SERVICE_ACCOUNT_FILE = r"C:\Users\Athashree\Downloads\feedbackform-455212-b63bdb921718.json"  # Change this to your JSON key file path

# Define API scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive"
]


# Authenticate and connect to Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet by name or URL
SHEET_NAME = "feebackform(responses)"
spreadsheet = client.open(SHEET_NAME)

# Select the first worksheet
worksheet = spreadsheet.sheet1  # Use `spreadsheet.worksheet("Sheet Name")` for specific sheets

# Get all data as a list of lists
data = worksheet.get_all_values()

# Convert to DataFrame
df = pd.DataFrame(data[1:], columns=data[0])  # Skip headers

# Save to Excel (for Power BI or further processing)
df.to_excel("feedback_responses.xlsx", index=False)

print("✅ Google Form responses fetched and saved to 'feedback_responses.xlsx'.")

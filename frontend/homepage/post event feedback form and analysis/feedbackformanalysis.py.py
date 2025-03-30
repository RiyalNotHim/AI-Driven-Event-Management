import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import google.generativeai as genai
import schedule
import time
import os
from dotenv import load_dotenv

# 🔹 Load environment variables
load_dotenv("configs.env")

# 🔹 Read credentials from .env
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SHEET_NAME = os.getenv("SHEET_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔹 Authenticate with Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 🔹 Open the Google Sheet
spreadsheet = client.open(SHEET_NAME)
worksheet = spreadsheet.sheet1  # Change if needed

# 🔹 Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# 🔹 Track last processed row
last_processed_row = 0

# Function to analyze sentiment using Gemini
def analyze_sentiment(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"Analyze the sentiment of this feedback: '{text}'. Return as Positive, Neutral, or Negative."
    response = model.generate_content(prompt)
    return response.text.strip()

# 🔹 Fetch and Process New Responses
def fetch_and_analyze_feedback():
    global last_processed_row
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])  # Convert to DataFrame

    # Check for new responses
    if len(df) > last_processed_row:
        new_responses = df.iloc[last_processed_row:]  # Get new rows
        print(f"🔄 Processing {len(new_responses)} new responses...")

        # Analyze sentiment for each new response
        for index, row in new_responses.iterrows():
            feedback_text = row['Any feedback?']  # Adjust column name as needed
            sentiment = analyze_sentiment(feedback_text)
            df.at[index, 'Sentiment'] = sentiment  # Store sentiment

        # Save updated data to Excel
        df.to_excel("feedback_responses.xlsx", index=False)
        print("✅ Updated 'feedback_responses.xlsx' with sentiment analysis.")

        last_processed_row = len(df)  # Update last processed row count

# 🔄 Schedule the script to run every 2 minutes
schedule.every(2).minutes.do(fetch_and_analyze_feedback)

print("🔁 Real-time feedback processing started... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(10)  # Check every 10 seconds

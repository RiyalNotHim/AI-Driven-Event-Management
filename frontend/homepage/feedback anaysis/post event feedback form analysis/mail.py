from flask import Flask, render_template, jsonify
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

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
spreadsheet = client.open(SHEET_NAME)
worksheet = spreadsheet.sheet1

# 🔹 Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def analyze_sentiment(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"Analyze the sentiment of this feedback: '{text}'. Return as Positive, Neutral, or Negative."
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    
    if not df.empty:
        df['Sentiment'] = df['Any feedback?'].apply(analyze_sentiment)
        df.to_excel("feedback_responses1.xlsx", index=False)
        return jsonify({"message": "Sentiment analysis completed!"})
    else:
        return jsonify({"message": "No feedback found!"})

if __name__ == '__main__':
    app.run(debug=True)

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv("api_key.env")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set it in the .env file.")

# Configure Google AI
genai.configure(api_key=api_key)

# Check API access
try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Hello, are you working?")
    print("API Test Response:", response.text)
except Exception as e:
    print("Error:", str(e))

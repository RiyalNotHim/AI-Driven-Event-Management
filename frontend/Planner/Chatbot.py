import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv("api_key.env")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set it in the .env file.")

# Configure the API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")  # Use "gemini-pro" or "gemini-pro-vision"

def chat_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gemini(user_input)
        print("Chatbot:", response)

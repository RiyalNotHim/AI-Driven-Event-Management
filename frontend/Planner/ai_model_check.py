import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv("api_key.env")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set it in the .env file.")

# Configure the API
genai.configure(api_key=api_key)

# List available models
models = genai.list_models()

# Print model names
print("Available AI Models:")
for model in models:
    print(f"- {model.name}")


from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "api_key.env")
load_dotenv(dotenv_path)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set it in the .env file.")

# Configure Google AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")

# Initialize Flask
app = Flask(__name__, static_folder="static", static_url_path="")

EVENT_PLANNER_ROLE = """
You are an AI assistant specializing in event planning and management. Your expertise includes:
- **Budgeting and cost optimization**
- **Venue selection and logistics**
- **Scheduling and event coordination**
- **Marketing and promotions**
- **Team management and volunteer coordination**
- **Technical requirements and operational planning**

Your tone is **professional, precise, and informative**, similar to a high-level event consultant.

If a user asks a question **unrelated to event planning**, respond with:
"I am designed to assist with event planning. Please let me know how I can help you create a successful event."
"""

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please provide a specific event-related question so I can assist you effectively."}), 400

        # Generate response with professional structure
        response = model.generate_content(f"{EVENT_PLANNER_ROLE}\nUser: {user_message}\nAI:")

        # Format the response for professionalism
        structured_response = f"**Event Planning Assistance:**\n\n{response.text.strip()}"

        return jsonify({"reply": structured_response})

    except Exception as e:
        return jsonify({"reply": "An unexpected error occurred. Please try again."}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
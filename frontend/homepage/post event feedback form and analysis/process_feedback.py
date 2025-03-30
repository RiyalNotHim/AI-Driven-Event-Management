import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv("configs.env")

# Fetch credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Validate credentials
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("⚠ Missing email credentials! Set EMAIL_ADDRESS and EMAIL_PASSWORD in configs.env")

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Server is running!"})

@app.route("/send", methods=["POST"])
def send_mail():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    event_name = data.get("event_name")
    recipient_name = data.get("recipient_name")
    event_details = data.get("event_details")
    emails = data.get("emails", [])

    if not event_name or not recipient_name or not event_details or not emails:
        return jsonify({"error": "Missing required fields"}), 400

    subject = f"Feedback Request for {event_name}"
    body = f"""
    Hi {recipient_name},

    Thank you for attending {event_name}!
    We value your feedback and would love to hear your thoughts.

    Event Details:
    {event_details}

    Please submit your feedback here: https://forms.gle/XKau1VnDP1khXXWa9

    Best Regards,
    Event Team
    """

    # Sending emails
    for email in emails:
        send_email(email, subject, body)

    return jsonify({"message": "✅ Emails sent successfully!"})

def send_email(to_email, subject, body):
    """Function to send emails via SMTP"""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

if __name__ == "__main__":
    app.run(debug=True)

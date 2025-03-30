from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import pymongo
import smtplib
from email.mime.text import MIMEText

# Flask App
app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://bogeprathmesh:secure12345@cluster0.iwmcgzx.mongodb.net/eventDB?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "eventDB"
COLLECTION_NAME = "formdatas"

# Email Configuration
SENDER_EMAIL = "hiddeninthepast530@gmail.com"
APP_PASSWORD = "esmu eces tyhj jsus"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to find matching users by experience
def find_matching_experience():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Group users by experience
    pipeline = [
        {"$group": {"_id": "$experience", "users": {"$push": "$email"}}},
        {"$match": {"users.1": {"$exists": True}}}  # Ensure at least 2 users
    ]

    matches = list(collection.aggregate(pipeline))
    if not matches:
        return []

    matching_users = []
    for match in matches:
        experience = match["_id"]
        emails = match["users"]
        matching_users.append((experience, emails))

    return matching_users

# Function to send emails
def send_email(to_email1, to_email2, experience):
    subject = "Skill Match Found!"
    body = f"Hey {to_email1} and {to_email2},\n\nYou both have experience in '{experience}'. You should connect! 🤝"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = f"{to_email1}, {to_email2}"

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        # Send email to both users
        server.sendmail(SENDER_EMAIL, to_email1, msg.as_string())
        server.sendmail(SENDER_EMAIL, to_email2, msg.as_string())

        server.quit()
        return True
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
        return False

# API Route to trigger email matching
@app.route("/match_users", methods=["POST"])
def match_users():
    matches = find_matching_experience()
    
    if matches:
        response_data = []
        for experience, emails in matches:
            if len(emails) >= 2:
                success = send_email(emails[0], emails[1], experience)
                response_data.append({
                    "experience": experience,
                    "emails": emails,
                    "email_sent": success
                })
        
        return jsonify({"status": "success", "data": response_data})
    
    return jsonify({"status": "error", "message": "No matching users found."})

# Serve HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)

# # MongoDB Connection
# # MONGO_URI = "mongodb+srv://bogeprathmesh:secure12345@cluster0.iwmcgzx.mongodb.net/eventDB?retryWrites=true&w=majority&appName=Cluster0"
# # client = MongoClient(MONGO_URI)
# # db = client["eventDB"]
# # collection = db["formdatas"]

# # Email Config
# SENDER_EMAIL = "hiddeninthepast530@gmail.com"
# APP_PASSWORD = "esmu eces tyhj jsus"
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587


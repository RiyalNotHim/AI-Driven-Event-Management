from flask import Flask, render_template, request
import os
import smtplib
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
import schedule
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv("config.env")  # Load environment variables

gemini_api_key = os.getenv("GEMINI_API_KEY")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

genai.configure(api_key=gemini_api_key)

def generate_email_content(event_name, recipient_name, event_details, call_to_action):
    prompt = f"""
    Write a compelling email for {recipient_name} about {event_name}. Include the details: {event_details}.
    End with a strong call to action: {call_to_action}.
    """
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text if response else "Error: Could not generate email content."

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, to_email, msg.as_string())
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_bulk_emails(email_list, subject, body):
    for email in email_list:
        send_email(email, subject, body)
        time.sleep(1)

def schedule_bulk_emails(email_list, subject, body, send_time):
    def job():
        send_bulk_emails(email_list, subject, body)
    
    schedule.every().day.at(send_time).do(job)
    print(f"📅 Emails scheduled for {send_time}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_scheduler, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        event_name = request.form['event_name']
        recipient_name = request.form['recipient_name']
        event_details = request.form['event_details']
        call_to_action = request.form['call_to_action']
        to_emails = request.form['to_emails'].split(',')
        schedule_time = request.form.get('schedule_time')
        
        email_body = generate_email_content(event_name, recipient_name, event_details, call_to_action)
        subject = f"You're Invited: {event_name}!"
        
        if schedule_time:
            schedule_bulk_emails(to_emails, subject, email_body, schedule_time)
        else:
            send_bulk_emails(to_emails, subject, email_body)
        
        return "Emails processed successfully!"
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

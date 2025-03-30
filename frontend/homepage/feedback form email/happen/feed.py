from flask import Flask, render_template, request
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
from dotenv import load_dotenv
import schedule

app = Flask(__name__)
load_dotenv("configs.env")

gemini_api_key = os.getenv("GEMINI_API_KEY")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FEEDBACK_FORM_LINK = "https://forms.gle/XKau1VnDP1khXXWa9"

genai.configure(api_key=gemini_api_key)

def generate_email_content(event_name, recipient_name, event_details):
    prompt = f"""
    Write a polite and engaging email for {recipient_name} who attended {event_name}.
    Thank them for their participation and request their feedback.
    
    Event Details:
    {event_details}
    
    Their feedback is valuable, and they can submit it using this form:
    {FEEDBACK_FORM_LINK}
    
    Keep the email short, warm, and professional.
    """
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text if response else "Error: Could not generate email content."
    except Exception as e:
        return f"Error in AI generation: {e}"

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
            print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_bulk_emails(email_list, subject, body):
    for email in email_list:
        send_email(email, subject, body)
        time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        event_name = request.form['event_name']
        recipient_name = request.form['recipient_name']
        event_details = request.form['event_details']
        to_emails = request.form['to_emails'].split(',')
        schedule_time = request.form.get('schedule_time')
        
        email_body = generate_email_content(event_name, recipient_name, event_details)
        subject = f"Your Feedback Matters! {event_name}"
        
        if schedule_time:
            def job():
                send_bulk_emails(to_emails, subject, email_body)
            schedule.every().day.at(schedule_time).do(job)
        else:
            send_bulk_emails(to_emails, subject, email_body)
        
        return "Emails sent successfully!"
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
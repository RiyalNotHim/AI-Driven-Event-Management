import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "hiddeninthepast530@gmail.com"
APP_PASSWORD = "esmu eces tyhj jsus"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

receiver_email = "bogeprathmesh@gmail.com"

subject = "Test Email"
body = "This is a test email to check SMTP."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = SENDER_EMAIL
msg["To"] = receiver_email

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()
    print("Test email sent successfully!")
except smtplib.SMTPException as e:
    print(f"Error sending test email: {e}")
